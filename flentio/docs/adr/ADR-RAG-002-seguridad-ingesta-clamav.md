# ADR-RAG-002 — Cuarentena y antimalware antes de indexar

- Estado: aceptada para F2; despliegue bancario pendiente de validación externa
- Fecha: 2026-07-31

## Contexto

El RAG alimenta agentes de distintos proveedores. Indexar directamente una carga permitiría distribuir malware a parsers u operadores y convertir instrucciones hostiles en contexto de IA. El banco necesita cierre seguro, segregación de funciones y evidencia durable.

## Decisión

Se adopta una máquina de estados PostgreSQL protegida por RLS y ClamAV `clamd` 1.4 como scanner operativo inicial. Los bytes se envían por `INSTREAM` antes de cualquier parser. Malware o indisponibilidad implican rechazo. Los límites estructurales frenan entradas expansivas. Las reglas deterministas de prompt injection y la clasificación documental determinan cuarentena; el grupo firmado de seguridad decide. Sólo `approved` crea un trabajo y sólo `indexed` participa en recuperación.

La inserción del trabajo y su enlace con la evaluación se serializan bloqueando la fila, de modo que aprobaciones concurrentes son idempotentes. Un trigger restringe transiciones y registra eventos append-only.

## Alternativas consideradas

- Defender for Storage y GuardDuty para S3: apropiados si el repositorio de entrada vive respectivamente en Azure Blob o S3; no se eligen ahora porque la carga actual entra directamente en Flentio y debe poder residir en infraestructura privada.
- Appliance comercial ICAP/API: opción válida cuando el cliente designe su motor homologado. Requiere un contrato de adaptador y pruebas de equivalencia; no existe todavía.
- Confiar sólo en extensión/MIME o en un clasificador LLM: rechazado. No detecta malware de forma suficiente y un modelo generativo no es una frontera antimalware determinista.
- Saltar scanner cuando está caído: rechazado por diseño; el sistema falla cerrado.

## Consecuencias

Se añade un servicio con consumo aproximado recomendado de 4 GiB, actualización de firmas, monitorización y capacidad HA pendiente. ClamAV no sustituye sandbox, CDR ni controles SOC. A cambio, ningún contenido llega a parsers o embeddings sin un resultado real, y cada decisión es trazable y aislada por tenant.
