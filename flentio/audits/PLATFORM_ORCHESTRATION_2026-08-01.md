# Auditoria de orquestacion PostgreSQL — 01-08-2026

## Dictamen

`VALIDACION LOCAL — CORTE DE ORQUESTACION ACTIVO`.

Workflows, versiones, ejecuciones, catalogo publico, webhooks y cron utilizan
PostgreSQL cuando `PLATFORM_WORKFLOW_DATASTORE=postgres`. La afirmacion se limita
al entorno local verificado; no equivale a HA ni preparacion bancaria productiva.

## Cambios examinados

- migraciones `003` a `006`: webhooks, deduplicacion, leases, catalogo y
  ejecuciones ad-hoc auditables;
- `workflowRepository.js`: RLS y transacciones acotadas;
- `workflowsPostgres.js`: CRUD, versiones, ejecuciones y rotacion de token;
- `webhooks.js`: autenticacion y publicacion HTTP 202;
- `cronDaemon.js`: scheduler idempotente;
- `workflowWorker.js`: reclamacion, heartbeat, reintentos y persistencia;
- `executionPolicy.js`: fallo cerrado para nodos simulados.

## Evidencia real

PostgreSQL informado por el servidor: `16.14`.

`npm run validate:platform-orchestration`:

```json
{"success":true,"postgres":"16","rls":"AISLADO","webhookToken":"SHA256_ONLY","webhookReplay":"DEDUPLICADO","cronPublishers":2,"cronJobs":1,"workers":2,"distinctClaims":2,"executions":2}
```

`npm run validate:platform-orchestration-api`:

```json
{"success":true,"health":"POSTGRES","workflow":"CRUD_OK","versions":"OK","publicCatalog":"OK","manualExecution":"PERSISTED","webhook":"HTTP_202","worker":"COMPLETED","secretHeaders":"NOT_STORED"}
```

La primera ejecucion de la validacion descubrio una ambiguedad SQL real en
`invoke_workflow_webhook`. No se oculto: la migracion `006` corrigio el conflicto
y la prueba completa se repitio con exito. Las filas efimeras se eliminaron.

Regresion de cierre: 38/38 pruebas superadas y `npm audit --omit=dev` sin
vulnerabilidades. Incluye politica de nodos, privacidad del payload webhook,
redaccion de secretos y clave temporal de cron.

## Seguridad y concurrencia

- RLS forzada y contexto transaccional por organizacion.
- Funciones `SECURITY DEFINER` acotadas; `PUBLIC` no puede ejecutarlas.
- Tokens aleatorios de 256 bits, almacenados solo como SHA-256 y rotables.
- `Authorization`, cookies y secretos de webhook excluidos del payload durable.
- Indice parcial unico para idempotencia por organizacion.
- Reclamacion atomica `SKIP LOCKED`, transaccion terminada antes de I/O externo.
- Heartbeat y recuperacion limitada de leases; reintento exponencial.
- Archivo en lugar de borrado para preservar historial empresarial.
- Preflight que impide registrar como correctos los nodos historicos simulados.

## Riesgos y pendientes

El procesamiento es at-least-once. Los conectores externos deben implementar
idempotencia y reconciliacion usando el job ID. La clave de credenciales y la
auditoria siguen siendo locales, otros modulos aun usan SQLite y no se han
probado carga, HA/DR, cancelacion ni aprobaciones humanas durables. El importador
XML legacy devuelve `NO_CONFIGURADO` en PostgreSQL porque generaba codigo que
declaraba comandos ejecutados sin ejecutarlos realmente.

## Rollback

Detener productores/workers, conservar cola y ejecuciones, cambiar
`PLATFORM_WORKFLOW_DATASTORE=sqlite` y reiniciar un unico nodo. No existe
dual-write ni copia inversa automatica; PostgreSQL permanece como evidencia.
