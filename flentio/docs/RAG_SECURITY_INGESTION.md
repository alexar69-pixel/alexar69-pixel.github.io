# Seguridad de ingesta del RAG

## Finalidad

Esta capa impide que un fichero dañino o un documento que intenta dar órdenes a un modelo entre directamente en el conocimiento activo. Se ejecuta antes de extraer, fragmentar, generar embeddings o publicar contenido a los agentes. No es OCR, no es un sandbox de ejecutables y no sustituye los controles de seguridad del puesto, correo o almacenamiento.

## Recorrido real

1. La API crea una evaluación `received` con tenant, actor, nombre, MIME, tamaño y SHA-256.
2. Pasa a `scanning` y envía los bytes en memoria a `clamd` mediante `INSTREAM`; no comparte rutas ni guarda el original en disco.
3. Una firma de malware produce `rejected`. Un fallo o timeout del scanner también cierra la ingesta: nunca continúa sin análisis.
4. Un resultado limpio permite validar tipo, firma y límites estructurales y extraer texto.
5. Las reglas versionadas `rules-es-en-v1` buscan instrucciones hostiles. Sólo generan hallazgos; nunca ejecutan el texto.
6. Riesgo alto o una clasificación incluida en `RAG_HUMAN_APPROVAL_CLASSIFICATIONS` produce `quarantined`.
7. Sólo un usuario con rol `admin`/`editor` y el grupo firmado `RAG_SECURITY_APPROVER_GROUP` puede aprobar o rechazar.
8. La aprobación crea exactamente un trabajo aun con solicitudes concurrentes. El worker genera embeddings reales y mueve la evaluación a `indexed` al confirmar la transacción.

Los estados y sus actores, fechas y motivos quedan en `ingestion_security_events`. La carga preparada es inmutable después de la decisión. RLS limita evaluaciones al creador o al grupo aprobador dentro del mismo tenant.

## Controles y límites

| Control | Valor actual | Propósito |
|---|---:|---|
| Carga binaria | 15 MB, un fichero | Acotar memoria y superficie de parser |
| Frecuencia API RAG | 120 solicitudes/minuto por identidad/IP | Limitar abuso y agotamiento |
| ClamAV | timeout 30 s configurable | Fallar cerrado si el motor no responde |
| DOCX | 5.000 entradas, 75 MB descomprimidos, ratio 200:1 | Detener ZIP bombs y contenedores anómalos |
| PDF | 2.000 páginas | Acotar documentos extremos |
| Texto normalizado | 5.000.000 caracteres por defecto | Acotar fragmentación y embeddings |
| Clasificación | `RESTRICTED` por defecto requiere persona | Aplicar cuatro ojos al conocimiento sensible |

El contenedor ClamAV dispone de 4 GiB y un volumen persistente de firmas. Se fija la rama `clamav/clamav:1.4`, en lugar de una etiqueta flotante, para controlar cambios de versión. En producción deben monitorizarse la fecha de firmas, latencia, rechazos, cola de cuarentena y disponibilidad; debe probarse la actualización primero en preproducción.

## Configuración

```env
RAG_MALWARE_SCANNER=clamav
CLAMAV_HOST=clamav
CLAMAV_PORT=3310
CLAMAV_TIMEOUT_MS=30000
RAG_SECURITY_APPROVER_GROUP=rag-security-approvers
RAG_HUMAN_APPROVAL_CLASSIFICATIONS=RESTRICTED
```

`GET /api/rag/status` sólo informa `OPERATIVO` si PostgreSQL, embeddings y ClamAV están disponibles. La interfaz muestra el motor y versión observados, la cola de cuarentena y las acciones de aprobación para identidades autorizadas.

## Operación e incidentes

- Scanner no disponible: detener ingestas, mantener consultas de documentos ya indexados y restaurar el servicio. Nunca puentear la cuarentena.
- Malware: no aprobar; conservar la evidencia de evaluación, investigar el origen y seguir el procedimiento SOC. Flentio no conserva el binario infectado.
- Falso positivo: seguridad debe validar fuera de Flentio con herramientas aprobadas. No existe una excepción automática.
- Prompt injection: revisar si el texto describe legítimamente ataques o intenta dirigir al agente. Aceptar sólo con motivo registrado.
- Trabajo fallido después de aprobación: permanece aprobado con el error del trabajo; corregir la causa y reintentar mediante procedimiento operativo, sin modificar silenciosamente la evidencia.

## Opciones disponibles en el mercado

| Opción | Encaje | Ventajas | Costes/limitaciones | Estado en Flentio |
|---|---|---|---|---|
| ClamAV/clamd | Docker, on-premise o nube privada | Código abierto, bytes por stream, control de residencia, firmas persistentes | Operación y alta disponibilidad propias; detección principalmente por firmas; no aporta sandbox/CDR | Integrado y validado |
| Microsoft Defender for Storage | Cargas alojadas en Azure Blob | Escaneo al subir o bajo demanda, resultados integrables en Azure | Dependencia y coste Azure; requiere diseño de eventos, identidad y tratamiento de resultados | No integrado |
| Amazon GuardDuty Malware Protection for S3 | Fuentes almacenadas en S3 | Escanea objetos nuevos y publica resultado mediante tags/EventBridge | Dependencia, permisos, regiones y coste AWS; no cubre una carga que no pase por S3 | No integrado |
| Motor comercial mediante ICAP/API | Bancos con appliance corporativo ya homologado | Puede aportar soporte empresarial, políticas centralizadas, sandbox o CDR según producto | Contrato, latencia, formatos, residencia e interfaz varían por fabricante | Adaptador futuro; no implementado |

La decisión debe comparar residencia de datos, SLA/HA, frecuencia de firmas, tamaño máximo, latencia, evidencia de auditoría, sandbox/CDR, soporte, coste por GB y dependencia del proveedor. ClamAV es la implementación actual porque funciona en la topología privada de Flentio y permite enviar bytes sin persistir el original; no se presenta como equivalente a un sandbox avanzado.

Fuentes técnicas: [ClamAV Docker](https://docs.clamav.net/manual/Installing/Docker.html), [protocolo clamd INSTREAM](https://docs.clamav.net/manual/Usage/ClamdProtocol.html), [Microsoft Defender for Storage](https://learn.microsoft.com/en-us/azure/defender-for-cloud/introduction-malware-scanning) y [Amazon GuardDuty Malware Protection for S3](https://docs.aws.amazon.com/guardduty/latest/ug/gdu-malware-protection-s3.html).

## Reversión

Detener endpoints de carga y sincronización y conservar lectura sobre `indexed`. No eliminar evaluaciones ni eventos, no mover `quarantined` directamente a `indexed` y no desactivar `RAG_MALWARE_SCANNER` para continuar. La vuelta al servicio exige ClamAV sano y una prueba limpia/EICAR controlada.
