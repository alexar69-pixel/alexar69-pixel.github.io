# Procedencia, originales y ciclo de vida del RAG

## Estado y alcance

Esta capacidad corresponde a F3 y está en **VALIDACIÓN local**, no en producción bancaria. Conserva cada original limpio antes de ejecutar un parser, enlaza la evidencia con la versión extraída y limita la recuperación a documentos vigentes y autorizados. El despliegue de desarrollo utiliza MinIO en un único nodo; la alta disponibilidad se ha aplazado expresamente a F6.

No existe OCR ni borrado físico desde la API. La ausencia de borrado es deliberada: una política de conservación bancaria, sus plazos y las excepciones por jurisdicción todavía deben aprobarse antes de automatizar destrucciones.

## Qué hace y para qué sirve

La cadena verificable es:

`evaluación antimalware -> original cifrado/versionado -> documento -> versión -> fragmento -> cita`

Para cada carga se registran organización, identificador de evaluación, nombre y MIME, tamaños, SHA-256 del original y del cifrado, versión del objeto, origen, fecha de captura, extractor, fragmentador, proveedor/modelo/dimensión del embedding, aprobador y fechas de vigencia. Los PDF añaden página a los fragmentos; otros formatos conservan sección cuando puede determinarse de forma fiable.

Esto permite demostrar qué fichero originó una respuesta, restaurar exactamente la versión utilizada, verificar integridad y retirar conocimiento obsoleto sin destruir evidencia.

## Custodia real del original

- El original sólo se almacena después de un resultado limpio de ClamAV y antes del parser.
- Flentio cifra en el cliente con AES-256-GCM. MinIO recibe sólo el contenedor cifrado.
- El AAD liga organización, UUID del objeto y SHA-256 original; cambiar cualquiera invalida la autenticación GCM.
- La clave procede de `RAG_OBJECT_ENCRYPTION_KEY`; `RAG_OBJECT_ENCRYPTION_KEY_ID` identifica la clave, pero no constituye todavía un KMS ni implementa rotación.
- El bucket se crea con versionado y Object Lock. Cada escritura debe devolver un `VersionId`.
- Tras escribir, Flentio contrasta tamaño y metadatos. Al restaurar, contrasta el SHA-256 cifrado, autentica GCM y vuelve a contrastar tamaño y SHA-256 original.
- Legal hold y retención GOVERNANCE se aplican a cada versión real del objeto y se leen de nuevo desde MinIO antes de actualizar PostgreSQL.

Si MinIO acepta una protección y PostgreSQL falla después, el objeto queda más protegido de lo reflejado en la base, nunca menos por decisión de Flentio. El operador debe repetir la operación y revisar ambos sistemas; F5 deberá incorporar reconciliación periódica automática. Retirar un legal hold exige el grupo de gestión documental y autorización `manage`. La retención no puede acortarse desde Flentio.

## Estados documentales

- `draft`: registrado, aún no aprobado.
- `approved`: aprobado, pero todavía fuera de su ventana efectiva.
- `effective`: recuperable por el RAG si también supera RLS, ACL y fechas.
- `superseded`: sustituido por otro documento vigente; deja de recuperarse.
- `expired`: fuera de vigencia; deja de recuperarse.
- `archived`: preservado pero no recuperable.

Las transiciones se validan en PostgreSQL, se serializan con bloqueo de fila y generan eventos append-only. `refresh_current_tenant_lifecycle()` activa o expira únicamente documentos de la organización actual. RLS continúa siendo obligatoria: conocer un UUID no permite acceder al original ni a su procedencia.

## Operación sin código

En **Administración > Cerebro IA (RAG)** un usuario autorizado puede:

1. indicar propietario, próxima revisión y URI de origen al cargar;
2. consultar procedencia, hashes, versión de objeto y versiones del pipeline;
3. descargar el original descifrado y verificado;
4. aprobar, activar, expirar, archivar o sustituir documentos;
5. activar/desactivar legal hold y ampliar una retención si pertenece al grupo configurado en `RAG_RECORDS_MANAGER_GROUP`.

Las mismas operaciones están disponibles mediante `/api/rag/documents/:id/provenance`, `/original`, `/lifecycle`, `/legal-hold` y `/retention`. No hay endpoint DELETE físico.

## Desarrollo y configuración

El contenedor `Dockerfile.minio` compila el tag oficial `RELEASE.2025-10-15T17-29-55Z`, que contiene la corrección de seguridad posterior al último binario publicado. El repositorio comunitario de MinIO quedó archivado en abril de 2026; por ello este componente se limita al desarrollo y debe reevaluarse antes de producción.

Variables obligatorias: `RAG_OBJECT_STORE_ACCESS_KEY`, `RAG_OBJECT_STORE_SECRET_KEY` y `RAG_OBJECT_ENCRYPTION_KEY`. Cambiar o perder la clave de cifrado impide restaurar los originales. Los secretos deben residir en un gestor de secretos, no en Git ni en `.env` productivos.

Comprobaciones mínimas:

1. `GET /api/rag/status` debe mostrar `objectStore.status=OPERATIVO`, versionado y Object Lock habilitados.
2. Una carga limpia debe terminar con `original_state=verified` y `object_version_id` no vacío.
3. La descarga debe coincidir byte a byte con el original.
4. Con legal hold activo, un intento de borrado no debe eliminar la versión: una lectura posterior debe encontrarla y devolver legal hold `ON`. MinIO puede responder éxito administrativo aunque trate el borrado como operación sin efecto.
5. Un documento expirado o sustituido no debe aparecer para un lector.

## Opciones del mercado para producción

- **Amazon S3 Object Lock:** servicio gestionado, versionado, modos GOVERNANCE/COMPLIANCE, legal hold e integración con KMS. Es la referencia natural cuando la residencia, contratación y arquitectura AWS estén aprobadas.
- **Azure Blob immutable storage:** políticas WORM por tiempo y legal hold, cifrado del servicio y claves administradas por cliente. Es adecuado para una plataforma bancaria asentada en Azure.
- **MinIO single-node:** útil para desarrollo local compatible con S3 y pruebas reales de Object Lock. El estado archivado del proyecto y la ausencia de HA en este despliegue impiden recomendar esta instancia para producción bancaria.

La selección productiva requiere análisis de residencia, certificaciones, soporte, KMS/HSM, modo COMPLIANCE, recuperación ante desastres, coste de salida y contrato. Esta fase no toma esa decisión en nombre del banco.

## Límites pendientes

- no hay HA, réplica ni recuperación regional;
- no hay KMS/HSM, rotación ni recifrado de claves;
- no existe todavía reconciliador periódico MinIO/PostgreSQL;
- no se ha definido una matriz de retención bancaria ni borrado gobernado;
- las pruebas son locales y no sustituyen pentest, revisión independiente, SOC/IdP ni pruebas con corpus autorizado.
