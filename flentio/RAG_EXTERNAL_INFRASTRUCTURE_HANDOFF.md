# Entrega de infraestructura externa para el RAG

## Finalidad y estado

Este documento define qué debe aportar un cliente para desplegar el RAG de
Flentio fuera del entorno local. Es un contrato técnico de preparación, no una
declaración de que la infraestructura productiva exista. Mientras no haya una
decisión, aprovisionamiento y prueba con evidencia, el estado será
`DEPENDENCIA_CLIENTE` o `NO_CONFIGURADO`; nunca se sustituirá por datos
simulados.

La configuración productiva se completa con:

- la plantilla de entrada `docs/templates/RAG_CLIENT_INFRASTRUCTURE_INTAKE.md`;
- la hoja de parámetros `docs/templates/RAG_PRODUCTION_PARAMETER_WORKSHEET.md`;
- la aceptación `docs/templates/RAG_PRODUCTION_ACCEPTANCE_CHECKLIST.md`;
- los objetivos provisionales de `docs/RAG_PRODUCTION_READINESS.md`;
- los procedimientos de recuperación de `docs/PLATFORM_POSTGRES_CUTOVER.md`.

No se escriben contraseñas, tokens, claves privadas ni claves de cifrado en
estos documentos. Sólo se anotan identificadores de secretos administrados por
la bóveda elegida por el cliente.

## Frontera de responsabilidades

| Área | Flentio | Cliente | Validación compartida |
| --- | --- | --- | --- |
| Aplicación RAG | código, migraciones, contratos de API y estados explícitos | plataforma de ejecución y ventanas de cambio | arranque, consulta, ingesta y rollback |
| PostgreSQL/pgvector | esquema, RLS, pools y consultas | clúster, red privada, réplicas, PITR y credenciales | migración, restauración y aislamiento por tenant |
| Originales | adaptadores MinIO, AWS S3 y S3 compatible con cifrado cliente AES-256-GCM | almacenamiento, retención, residencia y capacidad | versionado, Object Lock y restauración |
| Claves y secretos | clave estática heredada o envelope encryption con AWS KMS | KMS/HSM, secret manager, rotación, custodios | rotación y recuperación sin exponer material |
| Identidad | autorización interna y grupos RAG | IdP, MFA, ciclo de vida y claims | acceso positivo/negativo y revocación |
| Modelos IA | OpenAI/Ollama para embeddings y TEI para reranking | proveedor, región, contrato, cuotas y privacidad | dimensiones, calidad, latencia y fallo cerrado |
| Ingesta | cuarentena, validación y conector Drive | ClamAV y aplicaciones OAuth/fuentes | malware, webhook y reconciliación |
| Observabilidad | métricas, health, outbox y exportación OTLP | colector, APM, SIEM/WORM y guardias | entrega, alerta, acuse y retención |
| Continuidad | procedimientos y compatibilidad de restauración | backup, DR, BIA, RPO/RTO y simulacros | prueba documentada de restauración |

## Dependencias y decisiones obligatorias

Los estados admitidos son `PENDIENTE_CLIENTE`, `APROBADO`, `PROVISIONADO` y
`VALIDADO`. Una aprobación comercial o arquitectónica no equivale a una prueba.

| ID | Decisión del cliente | Entregable mínimo | Estado inicial |
| --- | --- | --- | --- |
| EXT-DB-001 | PostgreSQL gestionado o autogestionado, topología y regiones | endpoints privados, versión, pgvector, roles, backup y capacidad | `PENDIENTE_CLIENTE` |
| EXT-OBJ-001 | almacenamiento de originales y política WORM | bucket/contenedor, residencia, versionado, retención y legal hold | `PENDIENTE_CLIENTE` |
| EXT-KMS-001 | KMS/HSM y secret manager | identificadores de claves, política IAM, custodios, rotación y recuperación | `PENDIENTE_CLIENTE` |
| EXT-IDP-001 | IdP corporativo | issuer, client ID no secreto, claims, grupos, MFA y cuentas de emergencia | `PENDIENTE_CLIENTE` |
| EXT-SIEM-001 | destino de auditoría | endpoint/colector, esquema, acuse, retención y responsables SOC | `PENDIENTE_CLIENTE` |
| EXT-OBS-001 | métricas, trazas y alertas | endpoint OTLP, allowlist, dashboards, guardias y escalados | `PENDIENTE_CLIENTE` |
| EXT-NET-001 | red, DNS, TLS, proxy y egress | diagrama, FQDN, certificados, reglas y propietarios | `PENDIENTE_CLIENTE` |
| EXT-BACKUP-001 | PITR y recuperación regional | política, repositorio, cifrado, runbook y calendario de pruebas | `PENDIENTE_CLIENTE` |
| EXT-LLM-001 | embeddings, reranker y modelos generativos autorizados | proveedor, modelo/versionado, región, DPA, cuotas y límites | `PENDIENTE_CLIENTE` |
| EXT-AV-001 | motor antimalware | servicio, actualización de firmas, HA, timeout y escalado | `PENDIENTE_CLIENTE` |
| EXT-CON-001 | Drive y futuras fuentes | propietario OAuth, scopes, cuentas técnicas, webhook y reconciliación | `PENDIENTE_CLIENTE` |
| EXT-BIA-001 | criticidad y continuidad | SLO, RPO, RTO, retenciones y ventanas aprobados | `PENDIENTE_CLIENTE` |

## Compatibilidad real actual y adaptadores pendientes

| Componente | Consumido hoy por Flentio | Alternativas de mercado | Condición antes de producción |
| --- | --- | --- | --- |
| Base vectorial | PostgreSQL con pgvector | servicios PostgreSQL gestionados compatibles | probar extensión, RLS, pool, réplica y PITR en el servicio elegido |
| Originales | `minio`, `aws-s3` y `s3-compatible`; exige VersionId y Object Lock | Azure Blob y Google Cloud Storage nativos | AWS/S3 compatible ya tiene adaptador; Azure/GCS nativos requieren implementación y validación |
| Cifrado de originales | AES-256-GCM estático v1 y envelope encryption v2 con AWS KMS | Azure Managed HSM/Key Vault, Google Cloud KMS, Vault/PKCS#11 | AWS KMS está implementado; los demás requieren adaptador y prueba real |
| Embeddings | Ollama u OpenAI | servicios privados o modelos aprobados | validar dimensiones y reindexar en paralelo si cambian |
| Reranking | TEI con modelo declarado | Cohere, Voyage, Jina, Vertex AI u otro servicio homologado | requiere autorización humana y un adaptador probado para cualquier proveedor distinto de TEI |
| Antimalware | protocolo ClamAV | servicio corporativo o gateway ICAP | ClamAV es el único contrato implementado; otro motor requiere adaptador |
| Conectores | Google Drive OAuth/webhook/reconciliación | SharePoint, Box, S3, repositorios corporativos | cada fuente nueva requiere conector real, permisos mínimos e idempotencia |
| Telemetría | Prometheus y exportación OTLP HTTP/JSON | OpenTelemetry Collector y APM compatibles | endpoint HTTPS, host permitido, credencial de bóveda y prueba de recepción |
| Auditoría externa | outbox PostgreSQL durable sin transporte elegido | Sentinel, Splunk, Elastic, Google SecOps, QRadar, OpenSearch | elegir destino, implementar adaptador con acuse y demostrar retención/WORM |

Las opciones anteriores no son una recomendación ni una selección. La decisión
de almacenamiento, KMS/HSM, reranker, antimalware y SIEM requiere autorización
humana del cliente y revisión de residencia, certificaciones, soporte, coste,
portabilidad y contrato.

## Parámetros que consume el runtime

La fuente ejecutable es `backend/.env.example`. Esta tabla explica los grupos;
la hoja de trabajo registra referencias a secretos sin copiar sus valores.

| Grupo | Variables principales | Reglas |
| --- | --- | --- |
| PostgreSQL RAG | `RAG_DATABASE_URL`, `RAG_MIGRATION_DATABASE_URL`, `RAG_DB_POOL_MAX`, `RAG_AUTO_MIGRATE` | roles separados; TLS y endpoint privado en producción; migraciones por ventana controlada |
| Plataforma | `PLATFORM_DATABASE_URL`, `PLATFORM_MIGRATION_DATABASE_URL`, `PLATFORM_DB_POOL_MAX`, timeouts y leases | puede usar otro clúster; no compartir rol de aplicación con migración |
| Embeddings | `RAG_EMBEDDING_PROVIDER`, `RAG_EMBEDDING_MODEL`, `RAG_EMBEDDING_DIMENSIONS`, `OLLAMA_URL` o `OPENAI_API_KEY` | `openai` y `ollama` son los únicos proveedores aceptados actualmente |
| Reranker | `RAG_RERANKER_PROVIDER`, `RAG_RERANKER_ENDPOINT`, `RAG_RERANKER_MODEL`, timeouts y candidatos | proveedor actual obligatorio: `tei`; sin fallback ficticio |
| Recuperación | chunk, solapamiento, `TOP_K`, contenido máximo, concurrencia y trabajo obsoleto | versionar los cambios; no alterar dimensión sobre un índice activo |
| Conectores | poll, cola máxima, reconciliación, base URL y secreto HMAC | webhook público sólo por HTTPS; secreto mínimo de 32 caracteres |
| Seguridad | ClamAV, grupos de aprobación y clasificaciones | si el escáner real no responde, la ingesta queda bloqueada |
| Originales | proveedor, endpoint, región, bucket, credenciales, key provider, clave/KeyId | `minio`, `aws-s3` o `s3-compatible`; `static` o `aws-kms`; credenciales desde identidad de workload/bóveda |
| Observabilidad | intervalos, retención, endpoint OTLP, allowlist, bearer token y HMAC de auditoría | endpoint externo HTTPS; token nunca visible en panel ni repositorio |
| OAuth Drive | client ID, client secret y redirect URI | URI exacta registrada; HTTPS salvo localhost |

Las variables AWS documentadas son consumidas por el runtime. No deben añadirse
variables de Azure o Google KMS como si fueran funcionales hasta que exista
código que las consuma, pruebas y documentación de rollback.

## Red y exposición mínima

| Flujo | Puerto/protocolo | Exposición esperada |
| --- | --- | --- |
| Usuario/IdP hacia Flentio | 443/TLS | ingress o proxy corporativo; el puerto Node 3000 no se publica directamente |
| Flentio hacia PostgreSQL | 5432/TLS | red privada y reglas restringidas a workloads autorizados |
| Flentio hacia ClamAV | 3310/TCP | red interna; sin exposición pública |
| Flentio hacia MinIO actual | 9000/HTTP(S) S3 | red interna; TLS obligatorio fuera del host local |
| Flentio hacia TEI actual | 8085/HTTP(S) | red interna; TLS o mTLS según política del cliente |
| Flentio hacia APIs/OAuth/OTLP/SIEM | 443/TLS | egress por allowlist, proxy y DNS corporativos |

La consola MinIO 9001 y los puertos de administración no forman parte del flujo
de aplicación y no se publican a usuarios. El cliente deberá concretar FQDN,
CIDR, proxy, mTLS, autoridades certificadoras y resolución DNS.

## Identidad, IAM y secretos

1. Crear roles distintos para migración, runtime, backup, observabilidad y
   administración; conceder sólo las operaciones necesarias.
2. Separar tenants mediante RLS y probar accesos negativos, no sólo accesos
   válidos.
3. Inyectar secretos en memoria o fichero efímero desde el secret manager. No
   hornearlos en imágenes, manifests, logs, documentación ni variables de CI
   visibles.
4. Registrar custodios, fecha de rotación, versión y procedimiento de
   recuperación. Las claves de emergencia requieren doble control.
5. Rotar primero las aplicaciones consumidoras y retirar la versión anterior
   sólo tras verificar lectura, escritura y restauración.
6. No destruir una clave mientras existan backups u objetos retenidos cifrados
   con ella: la retención WORM no evita que la pérdida de la clave vuelva los
   datos ilegibles.

## Copias, retención y recuperación

PostgreSQL debe disponer de backup base y archivado continuo de WAL para PITR;
un `pg_dump` aislado no satisface este requisito. El cliente define retención,
región, inmutabilidad, cifrado y separación de cuentas. Cada entorno productivo
debe demostrar una restauración a infraestructura aislada y recoger tiempos,
punto recuperado, integridad, RLS, originales y audit trail.

Para los originales, habilitar versionado antes de Object Lock y decidir modo de
retención/legal hold con Legal y Records Management. Algunas políticas son
irreversibles al bloquearse; se validan primero en un bucket no productivo. El
runbook de baja conserva el orden: detener escrituras, exportar evidencia,
verificar retención, migrar/descifrar si procede y sólo después retirar claves o
cuentas.

## Secuencia de aprovisionamiento

1. El cliente completa las tres plantillas sin incluir secretos.
2. Arquitectura, Seguridad, Datos, Legal/Privacidad, SOC y Continuidad aprueban
   sus decisiones y responsables.
3. Se aprovisionan red, DNS/TLS, IdP, secret manager/KMS, PostgreSQL,
   almacenamiento, modelos, antimalware y observabilidad en un entorno no
   productivo equivalente.
4. Se implementan los adaptadores que falten. Una alternativa de mercado no se
   configura sólo mediante documentación.
5. Se inyectan referencias de secretos y se ejecutan migraciones con cuenta
   separada.
6. Se prueban fallo cerrado, RLS, malware, restauración, rotación, auditoría,
   reconciliación y rollback, guardando evidencia fechada.
7. Se comparan resultados con el BIA/SLO del cliente. Sólo los controles con
   evidencia cambian a `VALIDADO`.
   La aceptación incluye una reconciliación completa con 0 divergencias y 0
   objetos no disponibles mediante `docs/RAG_WORM_RECONCILIATION.md`.
8. La revisión independiente de seguridad y cumplimiento permanece como puerta
   previa a producción; puede realizarla el equipo de assurance del banco.

## Criterio de aceptación y reversión

El despliegue no se acepta si falta una dependencia obligatoria, si una prueba
se omite o si un control devuelve `NO_CONFIGURADO`, `NO_DISPONIBLE` o
`DEPENDENCIA_CLIENTE`. `SIN_DATOS` no equivale a éxito y un cero sólo es válido
cuando una consulta real lo confirma.

El rollback debe restaurar la versión previa de aplicación/configuración,
conservar los eventos de auditoría y evitar migraciones destructivas. Los
cambios de dimensión de embeddings, esquema o proveedor de originales se hacen
en paralelo y con conmutación reversible; no se modifican en sitio.

## Fuentes técnicas oficiales

- PostgreSQL: [archivado continuo y recuperación a un punto en el tiempo](https://www.postgresql.org/docs/16/continuous-archiving.html).
- AWS: [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html) y [gestión de Object Lock y claves](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-managing.html).
- Microsoft: [almacenamiento inmutable de Azure Blob](https://learn.microsoft.com/en-us/azure/storage/blobs/immutable-storage-overview) y [control de acceso de Managed HSM](https://learn.microsoft.com/en-us/azure/key-vault/managed-hsm/access-control).
- Google Cloud: [Bucket Lock](https://cloud.google.com/storage/docs/bucket-lock) y [niveles de protección de Cloud KMS](https://cloud.google.com/kms/docs/protection-levels).
