# Corte operativo de Flentio a PostgreSQL

## Estado verificado

Desde el 01-08-2026 el backend de desarrollo usa `PLATFORM_DATASTORE=postgres`,
`PLATFORM_IDENTITY_DATASTORE=postgres`, `PLATFORM_WORKFLOW_DATASTORE=postgres` y
`PLATFORM_AUDIT_DATASTORE=postgres`. El proceso web no carga
`backend/src/db/index.js`; `/api/health` debe mostrar `datastoreMode=postgres`.
`better-sqlite3` fue eliminado completamente; toda la persistencia reside en
PostgreSQL.

Flentio conserva dos dominios de datos separados por responsabilidad, pero ya
no dos motores incompatibles:

- `flentio_rag`: documentos, versiones, fragmentos, embeddings, conectores,
  procedencia, reindexación y observabilidad del conocimiento;
- `flentio_platform`: organizaciones, usuarios, secretos, workflows,
  ejecuciones, colas, ajustes y auditoría de la plataforma.

En desarrollo ambos esquemas residen en PostgreSQL 16/pgvector del mismo
clúster, con roles y pools distintos. En producción sus URL pueden apuntar a
clústeres separados o a PgBouncer sin cambiar los repositorios de aplicación.

## Capacidades reales

- RLS forzada por organización y contexto transaccional compatible con
  PgBouncer transaction mode.
- Índices compuestos y parciales para identidad activa, auditoría, colas y
  estados reclamables.
- Webhooks, cron y workers durables con idempotencia, heartbeat y
  `FOR UPDATE SKIP LOCKED`.
- Aprobaciones y reintentos de ejecuciones persistidos y reanudados por cola.
- Auditoría append-only con secuencia monotónica por tenant, cadena SHA-256
  calculada en PostgreSQL y verificación completa de cada evento.
- Outbox SIEM durable, reclamación concurrente y reintentos exponenciales. La
  entrega externa permanece `NO_CONFIGURADO` hasta seleccionar destino,
  autenticación y allowlist HTTPS.
- El copiloto devuelve evidencia RAG real; generación estructurada de flujos,
  self-healing y swarm autónomo devuelven `NO_CONFIGURADO`.
- Nodos históricos de correo, KYC/AML, SEPA/SWIFT, SQL externo, monitorización,
  scripts locales o sandbox JS no ejecutan resultados inventados: la política
  los bloquea antes de comenzar el grafo.

## Configuración

```env
PLATFORM_DATASTORE=postgres
PLATFORM_IDENTITY_DATASTORE=postgres
PLATFORM_WORKFLOW_DATASTORE=postgres
PLATFORM_AUDIT_DATASTORE=postgres
PLATFORM_DATABASE_URL=postgresql://flentio_platform_app:<secreto>@postgres/flentio
PLATFORM_MIGRATION_DATABASE_URL=postgresql://rol_migracion:<secreto>@postgres/flentio
PLATFORM_WORKFLOW_WORKER_ENABLED=true
PLATFORM_WORKFLOW_WORKER_CONCURRENCY=2
SIEM_DESTINATION_HOST_ALLOWLIST=
```

El rol de migración no debe existir en el runtime. `ENCRYPTION_KEY` puede ser un
fichero local sólo en desarrollo; producción exige una clave compartida
entregada por un gestor de secretos. Las claves `SIEM_*` no se aceptan desde el
formulario genérico de ajustes.

## Migraciones 007–012

`007` crea auditoría y outbox; `008` añade baja lógica de usuarios; `009`
encapsula verificación y finalización SIEM en funciones privilegiadas; `010`
cualifica `pgcrypto` con `search_path` endurecido; `011` añade secuencia
monotónica; `012` reconstruye el orden histórico siguiendo `parent_hash`.
Todas son ascendentes, versionadas y protegidas por checksum. La auditoría no
tiene migración destructiva de vuelta.

## Escalado sin afirmar HA

El estado compartido permite añadir procesos web y workers: cada instancia usa
un `PLATFORM_INSTANCE_ID`, pools acotados, claves idempotentes y colas
reclamables. Esto prepara escalado horizontal, pero el entorno de desarrollo
single-node no demuestra disponibilidad, failover, RPO, RTO ni carga.

| Opción PostgreSQL | Ventajas | Costes y límites |
|---|---|---|
| Azure/AWS/GCP gestionado | backups, réplicas, PITR y operación del plano de datos | dependencia de nube, región, coste y contrato |
| Patroni + etcd/Consul | failover portable y controlado | complejidad SRE, fencing y ensayos obligatorios |
| CloudNativePG/Crunchy | operador y backups declarativos en Kubernetes | exige madurez Kubernetes y aislamiento de fallos |
| Réplica física sin orquestador | sencilla para lectura y DR inicial | no ofrece failover seguro por sí sola |

PgBouncer reduce conexiones, pero no replica datos ni aporta HA. El sharding no
se introduce sin evidenciar antes que primaria/réplicas, particiones e índices
son insuficientes.

## Backup y restauración: opciones abiertas

La API devuelve `PLATFORM_BACKUP_NO_CONFIGURADO`; no fabrica un fichero JSON ni
un snapshot.

| Opción | Ventajas | Inconvenientes |
|---|---|---|
| Backup/PITR gestionado | menor operación, KMS y réplicas integrables | bloqueo de proveedor y coste de retención/egress |
| pgBackRest | completos/diferenciales, repositorios y restore sólidos | operación y pruebas a cargo de Flentio |
| Barman | gestión centralizada para varios PostgreSQL | servidor y operación adicionales |
| WAL-G | WAL/backups a objetos y automatización cloud-native | catálogo y restore exigen runbooks rigurosos |

No se seleccionará almacenamiento, retención ni KMS sin autorización. La puerta
productiva exige restauración real, PITR, cifrado, cuentas separadas,
inmutabilidad y medición de RPO/RTO.

## KMS/HSM y secretos

Azure Key Vault/Managed HSM encaja con Entra/Sentinel; AWS KMS/CloudHSM con IAM;
Google Cloud KMS/HSM con GCP; HashiCorp Vault Transit aporta portabilidad y
control propio; CyberArk Conjur encaja donde ya existe PAM. Los gestionados
reducen operación y aumentan dependencia de nube; Vault/Conjur trasladan HA,
unseal, backup y guardias al equipo. Ninguno está seleccionado. Hasta entonces
health informa `credentialVault.multinodeReady=false`.

## SIEM

La outbox no elige producto. Sentinel, Splunk, Elastic, Google SecOps, QRadar y
OpenSearch se comparan en `RAG_PRODUCTION_READINESS.md`. El transporte actual
sólo permite HTTPS hacia hosts allowlisted y aún no incorpora autenticación
específica de proveedor; por ello no se declara integración SIEM. Una
implantación debe definir identidad técnica, formato, acuse, retención,
reconciliación y DLQ antes de provisionar `SIEM_WEBHOOK_URL` por runbook.

## Operación y reversión

1. Aplicar migraciones con rol separado: `npm run migrate:platform`.
2. Ejecutar `npm test`, auditorías npm y validadores `platform-multinode`,
   `platform-identity-api` y `platform-orchestration-api`.
3. Confirmar health PostgreSQL y SQLite no cargado.
4. En incidente, detener publishers/workers antes de cambiar versión.
5. Revertir el binario manteniendo esquemas aditivos. Volver a SQLite sólo es
   contingencia manual de desarrollo, single-node y con riesgo de divergencia;
   nunca es rollback automático de datos.

No borrar migraciones 007–012, eventos de auditoría ni datos PostgreSQL durante
la reversión.

