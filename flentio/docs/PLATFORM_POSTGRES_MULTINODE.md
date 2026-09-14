# Persistencia PostgreSQL y preparación multinodo de Flentio

## Estado

Estado al 01-08-2026: `VALIDACIÓN LOCAL — CORTE POSTGRESQL OPERATIVO`.

El esquema PostgreSQL compartido, migraciones, RLS y colas están verificados con PostgreSQL 16 real. Identidad, secretos, workflows, ejecuciones, webhooks, cron, administración y auditoría utilizan PostgreSQL. El proceso web no carga SQLite. La clave local de credenciales, backup, SIEM externo y la ausencia de HA impiden anunciar producción multinodo; el diseño para añadir procesos sí está preparado.

No se han realizado pruebas de estrés porque no forman parte del objetivo actual. La validación demuestra que la persistencia deja preparados los mecanismos necesarios para añadir nodos; no demuestra capacidad, latencia ni disponibilidad productiva.

## Alcance empresarial

La migración abarca el núcleo completo de la plataforma:

- identidades, organizaciones, roles y límites;
- workflows, versiones y programación;
- ejecuciones de scripts y flujos;
- credenciales y autorizaciones OAuth;
- configuración por organización;
- cola durable para workers de orquestación;
- conocimiento RAG, que conserva su esquema PostgreSQL/pgvector separado;
- monitorización y agentes, que podrán producir trabajos y eventos sin depender del disco de un nodo web.

El RAG y la plataforma pueden compartir un clúster PostgreSQL durante desarrollo usando roles y esquemas distintos. En producción, `PLATFORM_DATABASE_URL` y `RAG_DATABASE_URL` permiten separarlos en clústeres independientes sin cambiar el código funcional.

## Topología prevista

```text
Usuarios / API / webhooks
          |
   balanceador HTTPS
          |
  +-------+-------+
  |               |
web-1           web-N          servicios de monitorización
  |               |                     |
  +-------+-------+---------------------+
          |
   PgBouncer transaction mode
          |
 PostgreSQL primario ---- réplicas de lectura futuras
   |            |
 plataforma     RAG/pgvector
   |
 cola durable -- workers de workflows/scripts/agentes
```

PgBouncer no está desplegado todavía. El cliente `pg` ya usa pools acotados, timeouts y transacciones compatibles con pooling en modo transaction. Las réplicas, failover y HA se incorporarán sólo cuando se decida la topología productiva.

## Controles implementados

- Esquema `flentio_platform` con claves, restricciones e índices para accesos por organización, workflow, estado y tiempo.
- Rol `flentio_platform_app` sin superusuario, creación de roles, bases, esquemas ni bypass de RLS.
- RLS forzada por `app.organization_id`; sin contexto no se muestran filas.
- Función exacta y acotada para login antes de conocer la organización.
- Cola `workflow_run_jobs` con reclamación atómica `FOR UPDATE SKIP LOCKED`.
- Bloqueo advisory transaccional para que sólo un nodo aplique cada migración.
- Historial de migraciones con SHA-256; modificar una migración ya aplicada provoca fallo cerrado.
- Pools máximos y timeouts configurables por nodo.
- Importación idempotente, transaccional y sin borrar SQLite.
- Ajustes antes globales se convierten en configuración separada por organización.
- `/api/health` informa componentes reales y el modo de persistencia; ya no devuelve una base de datos conectada de forma prefabricada.
- `PLATFORM_IDENTITY_DATASTORE` permite cortar identidad/secretos a PostgreSQL sin ocultar que el núcleo de workflows sigue en SQLite.
- Las credenciales nuevas usan AES-256-GCM autenticado; CBC queda sólo como lector transitorio de registros históricos.
- En producción, identidad PostgreSQL falla al arrancar si `ENCRYPTION_KEY` no procede de configuración compartida.
- `PLATFORM_WORKFLOW_DATASTORE` permite cortar la orquestación sin falsear el modo de los módulos restantes.
- Webhooks con token aleatorio mostrado una vez, hash SHA-256 persistido y cabeceras sensibles excluidas.
- Cron publica trabajos con clave de tick idempotente; no ejecuta el grafo dentro del nodo web.
- Workers con reclamación global `SKIP LOCKED`, heartbeat, lease, reintento acotado y resultado PostgreSQL.
- Los nodos históricos que fabricaban resultados fallan antes de ejecutar con `WORKFLOW_NODE_NO_CONFIGURADO`.

## Comandos

Revisión sin escribir:

```powershell
cd backend
npm run migrate:sqlite-to-postgres
```

Aplicar esquema:

```powershell
npm run migrate:platform
```

Copiar datos después de revisar el inventario:

```powershell
npm run migrate:sqlite-to-postgres -- --apply
```

Validar RLS y dos workers concurrentes:

```powershell
npm run validate:platform-multinode
```

Validar identidad/secretos y sus endpoints HTTP:

```powershell
npm run validate:platform-identity
npm run validate:platform-identity-api
npm run validate:platform-orchestration
npm run validate:platform-orchestration-api
```

Los comandos requieren `PLATFORM_MIGRATION_DATABASE_URL`. La validación y la aplicación usan además `PLATFORM_DATABASE_URL`. Nunca se debe utilizar el rol administrador como identidad ordinaria de Flentio.

## Resultado local del 01-08-2026

La copia real y transaccional produjo el mismo número de filas en origen y destino:

| Entidad | SQLite | PostgreSQL |
|---|---:|---:|
| Usuarios | 3 | 3 |
| Workflows | 70 | 70 |
| Ejecuciones | 9 | 9 |
| Credenciales cifradas | 5 | 5 |
| Estados OAuth | 1 | 1 |
| Ajustes | 0 | 0 |
| Versiones de workflow | 1 | 1 |

Dos conexiones de aplicación reclamaron en paralelo dos trabajos distintos. Cada organización sólo vio su workflow, una consulta sin contexto devolvió cero filas y el rol de aplicación no pudo crear una tabla. Los objetos sintéticos de validación se eliminaron al finalizar.

## Migración gradual y corte

1. **Fundación — validada:** esquema, roles, RLS, importador y cola.
2. **Identidad y secretos — validación local con corte activo:** auth, configuración, credenciales y OAuth usan repositorios PostgreSQL asíncronos; falta KMS/secret manager para multinodo productivo.
3. **Orquestación — validación local con corte activo:** workflows, versiones, ejecuciones, catálogo, webhooks y cron usan PostgreSQL; dos workers y dos publicadores fueron verificados sin duplicidad.
4. **Agentes y monitorización — validación local:** organización/actor llegan al worker, RAG y credenciales; resultados, cancelación y estados se persisten realmente. Los scripts sin aislamiento siguen `NO CONFIGURADO`.
5. **Corte — completado en desarrollo:** `PLATFORM_DATASTORE=postgres`; SQLite no se carga en el proceso web y sólo queda para importación/reversión heredada.
6. **Retirada web — completada:** `better-sqlite3` permanece como dependencia explícita de herramientas legacy, no como datastore operativo.

No se usará dual-write prolongado porque dificulta determinar la fuente autoritativa. El corte será controlado, con una ventana breve sin escrituras y rollback explícito.

## Riesgos abiertos

- Los módulos web operativos usan PostgreSQL. Las herramientas legacy que leen SQLite deben ejecutarse fuera del proceso web y no son multinodo.
- La auditoría/outbox ya es PostgreSQL. La clave de cifrado local sigue siendo una dependencia de desarrollo; el cliente aportará KMS/secret manager en producción.
- Los nodos históricos no implementados son bloqueados antes de ejecutar y se muestran `NO CONFIGURADO`; cada integración futura deberá conectarse realmente.
- “Preparado para varios nodos” no equivale a HA, failover probado o escalabilidad certificada.
