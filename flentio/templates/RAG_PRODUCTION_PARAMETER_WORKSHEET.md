# Hoja de parámetros productivos del RAG

**Estado:** `PLANTILLA_SIN_DATOS`. Esta hoja mapea parámetros reales del
runtime a referencias de configuración. No contiene valores secretos y no crea
soporte para proveedores que el código todavía no implemente.

Valores de estado: `PENDIENTE_CLIENTE`, `APROBADO`, `PROVISIONADO`, `VALIDADO`.

| Variable/grupo | Secreto | Propietario | Valor no secreto o referencia de bóveda | Entorno | Estado | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| `NODE_ENV` | no | Plataforma | `production` | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| `JWT_SECRET` | sí | Seguridad | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| `ENCRYPTION_KEY` | sí | Seguridad | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| `RAG_DATABASE_URL` | sí | Datos | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| `RAG_MIGRATION_DATABASE_URL` | sí | Datos | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| `RAG_DB_POOL_MAX` | no | Datos | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| `PLATFORM_DATABASE_URL` | sí | Datos | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| `PLATFORM_MIGRATION_DATABASE_URL` | sí | Datos | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| `PLATFORM_DB_POOL_MAX` y timeouts | no | Datos | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| `RAG_EMBEDDING_PROVIDER` | no | IA/Datos | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| `RAG_EMBEDDING_MODEL` y dimensiones | no | IA/Datos | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| `OLLAMA_URL` o `OPENAI_API_KEY` | mixto | IA/Seguridad | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| `RAG_RERANKER_PROVIDER` | no | IA/Datos | `tei` mientras no exista otro adaptador | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| endpoint/modelo/timeout/candidatos reranker | no | IA/Plataforma | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| chunk/solapamiento/top K/score mínimo | no | IA/Datos | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| límites/concurrencia/retención de jobs | no | Plataforma | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| URL pública/poll/reconciliación de conectores | no | Integraciones | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| `RAG_CONNECTOR_WEBHOOK_SECRET` | sí | Seguridad | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| ClamAV host/port/timeout | no | Seguridad/Plataforma | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| grupos de aprobadores y records managers | no | Identidad | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| proveedor/endpoint/región/bucket de objetos | no | Datos | `minio`, `aws-s3` o `s3-compatible` | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| acceso/secreto del almacén de objetos | sí | Datos/Seguridad | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| `RAG_OBJECT_KEY_PROVIDER` | no | Seguridad | `static` o `aws-kms` | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| clave/ID estático o AWS KMS KeyId/región | sí/mixto | Seguridad | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| health interval/retention | no | Operaciones | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| OTLP endpoint/allowlist | no | Operaciones/SOC | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| OTLP bearer y `AUDIT_HMAC_SECRET` | sí | SOC/Seguridad | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| SIEM destination allowlist | no | SOC | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Google Drive client ID/redirect URI | no | Integraciones | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Google Drive client secret | sí | Integraciones/Seguridad | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |

Antes de aplicar esta hoja se compara con `backend/.env.example` y con la
versión desplegada. Una variable documentada pero no consumida por el código no
se considera configurada.
