# Hoja de parámetros productivos del RAG

**Estado:** `PLANTILLA_SIN_DATOS`. Esta hoja mapea parámetros reales del
runtime a referencias de configuración. No contiene valores secretos y no crea
soporte para proveedores que el código todavía no implemente.

Valores de estado: `[REQUERIDO_POR_TENANT]`, `APROBADO`, `PROVISIONADO`, `VALIDADO`.

| Variable/grupo | Secreto | Propietario | Valor no secreto o referencia de bóveda | Entorno | Estado | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| `NODE_ENV` | no | Plataforma | `production` | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| `JWT_SECRET` | sí | Seguridad | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| `ENCRYPTION_KEY` | sí | Seguridad | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| `RAG_DATABASE_URL` | sí | Datos | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| `RAG_MIGRATION_DATABASE_URL` | sí | Datos | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| `RAG_DB_POOL_MAX` | no | Datos | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| `PLATFORM_DATABASE_URL` | sí | Datos | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| `PLATFORM_MIGRATION_DATABASE_URL` | sí | Datos | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| `PLATFORM_DB_POOL_MAX` y timeouts | no | Datos | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| `RAG_EMBEDDING_PROVIDER` | no | IA/Datos | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| `RAG_EMBEDDING_MODEL` y dimensiones | no | IA/Datos | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| `OLLAMA_URL` o `OPENAI_API_KEY` | mixto | IA/Seguridad | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| `RAG_RERANKER_PROVIDER` | no | IA/Datos | `tei` mientras no exista otro adaptador | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| endpoint/modelo/timeout/candidatos reranker | no | IA/Plataforma | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| chunk/solapamiento/top K/score mínimo | no | IA/Datos | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| límites/concurrencia/retención de jobs | no | Plataforma | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| URL pública/poll/reconciliación de conectores | no | Integraciones | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| `RAG_CONNECTOR_WEBHOOK_SECRET` | sí | Seguridad | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| ClamAV host/port/timeout | no | Seguridad/Plataforma | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| grupos de aprobadores y records managers | no | Identidad | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| proveedor/endpoint/región/bucket de objetos | no | Datos | `minio`, `aws-s3` o `s3-compatible` | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| acceso/secreto del almacén de objetos | sí | Datos/Seguridad | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| `RAG_OBJECT_KEY_PROVIDER` | no | Seguridad | `static` o `aws-kms` | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| clave/ID estático o AWS KMS KeyId/región | sí/mixto | Seguridad | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| health interval/retention | no | Operaciones | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| OTLP endpoint/allowlist | no | Operaciones/SOC | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| OTLP bearer y `AUDIT_HMAC_SECRET` | sí | SOC/Seguridad | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| SIEM destination allowlist | no | SOC | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| Google Drive client ID/redirect URI | no | Integraciones | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |
| Google Drive client secret | sí | Integraciones/Seguridad | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] | [REQUERIDO_POR_TENANT] |

Antes de aplicar esta hoja se compara con `backend/.env.example` y con la
versión desplegada. Una variable documentada pero no consumida por el código no
se considera configurada.
