# Orquestacion durable de workflows en PostgreSQL

## Finalidad

Esta fase separa la recepcion de un evento de su ejecucion. Un webhook o un tick
de cron publica un trabajo en `flentio_platform.workflow_run_jobs`; uno de los
workers lo reclama y ejecuta el grafo. El estado deja de depender del disco de
un servidor web y se puede aumentar el numero de consumidores sin que dos
procesos reclamen simultaneamente la misma fila.

El corte local se controla con `PLATFORM_WORKFLOW_DATASTORE=postgres`. No cambia
el modo de los modulos que aun siguen en SQLite.

## Flujo operativo

```text
API autenticada / webhook / cron
               |
               v
      workflow_run_jobs (PostgreSQL)
       deduplicacion + RLS + lease
               |
        FOR UPDATE SKIP LOCKED
          +----+----+
          |         |
       worker-1  worker-N
          |         |
          +----+----+
               |
          WorkflowRunner
               |
       executions (PostgreSQL)
```

Los webhooks devuelven HTTP `202 Accepted`; `jobId` permite consultar el estado
en `GET /api/workflows/jobs/:id`. No se devuelve exito de ejecucion al aceptar
la peticion: el exito solo existe cuando el worker ha persistido la ejecucion.

## Webhooks

Un administrador o editor crea o rota el secreto con:

```http
POST /api/workflows/{workflowId}/webhook-token
Authorization: Bearer <JWT>
```

El token se muestra una sola vez. PostgreSQL conserva exclusivamente SHA-256.
El emisor lo presenta mediante `X-Flentio-Webhook-Token`. `Idempotency-Key` es
opcional y, cuando existe, evita repetir el mismo evento dentro del workflow.
Las cabeceras `Authorization`, `Cookie` y el propio token nunca se guardan en la
cola; solo se conservan `Content-Type`, `User-Agent`, `X-Request-Id` y
`traceparent` con tamaño acotado.

Un workflow debe estar activo, contener `webhook_trigger` y pertenecer a
`staging` o `production`. El modo mantenimiento rechaza nuevas publicaciones.
La rotacion invalida inmediatamente el token anterior y `DELETE` deshabilita el
endpoint.

## Cron distribuido

Cada instancia puede cargar las mismas expresiones. Para cada tick genera la
clave `cron:workflow:nodo:intervalo`; un indice unico por organizacion admite
una sola insercion. Cron no ejecuta el grafo dentro del servidor web. Una
expresion invalida queda registrada y no se programa.

## Workers, leases y reintentos

`claim_workflow_run_job` usa `FOR UPDATE SKIP LOCKED` y confirma la reclamacion
antes de ejecutar red, scripts o modelos IA. El worker actualiza un heartbeat.
Un lease abandonado vuelve a `pending` hasta `max_attempts`; al agotarlos queda
`failed`. Los fallos usan espera exponencial acotada y cada intento produce una
ejecucion auditable.

El modelo es **at-least-once**, no exactly-once. Si un proceso realiza un efecto
externo y muere antes de confirmar PostgreSQL, el trabajo puede repetirse. Cada
conector con efectos debe enviar `job.id` como clave idempotente al proveedor o
implementar reconciliacion. La fase no afirma que todos los nodos historicos ya
cumplan esta condicion.

## Prohibicion de resultados simulados

`executionPolicy.js` revisa el grafo antes del primer nodo. Los tipos historicos
que fabricaban respuestas, metricas, correos, consultas o ficheros fallan con
`WORKFLOW_NODE_NO_CONFIGURADO`. OpenAI, Gemini y Ollama usan sus adaptadores
reales y fallan si no hay credencial o servicio. Esta barrera evita que cron,
webhook o ejecucion manual registren un mock como exito.

El importador XML legacy permanece `NO_CONFIGURADO` en el modo PostgreSQL hasta
que su transformacion elimine el codigo generado que anuncia comandos sin
ejecutarlos. No se oculta mediante fallback a SQLite.

## Configuracion

```env
PLATFORM_WORKFLOW_DATASTORE=postgres
PLATFORM_WORKFLOW_WORKER_ENABLED=true
PLATFORM_WORKFLOW_WORKER_CONCURRENCY=2
PLATFORM_WORKFLOW_WORKER_POLL_MS=1000
PLATFORM_WORKFLOW_JOB_LEASE_SECONDS=300
PLATFORM_INSTANCE_ID=flentio-web-1
```

Un proceso dedicado se inicia con `npm run start:workflow-worker`. Si los nodos
web tambien consumen, cada uno debe tener un `PLATFORM_INSTANCE_ID` distinto.
Los pools siguen estando limitados por `PLATFORM_DB_POOL_MAX`; aumentar workers
sin calcular el presupuesto total de conexiones puede agotar PostgreSQL.

## Validacion y evidencia

```powershell
cd backend
npm run validate:platform-orchestration
npm run validate:platform-orchestration-api
```

La primera prueba crea dos tenants efimeros, verifica RLS, hash de webhook,
replay idempotente, dos publicadores cron, dos workers y dos ejecuciones. Se
niega a empezar si existen trabajos ajenos pendientes. La segunda arranca un
backend real, usa registro, bcrypt/JWT y HTTP, crea un workflow, ejecuta un grafo
manual, publica un webhook, espera al worker y comprueba que Authorization no
se persistio. Ambas eliminan exclusivamente sus UUID al terminar.

## Opciones de cola disponibles en el mercado

PostgreSQL se eligio para esta etapa porque ya es la fuente transaccional,
permite RLS, deduplicacion atomica y `SKIP LOCKED`, y reduce componentes durante
desarrollo. Es adecuado para trabajos empresariales de volumen moderado y deja
escalar consumidores y nodos de base de datos.

- RabbitMQ ofrece routing, acknowledgements y ecosistema maduro. Añade otro
  cluster, otra politica de recuperacion y coordinacion transaccional con la BD.
- Apache Kafka ofrece retencion, replay y gran caudal. Es potente para eventos,
  pero su modelo de log y operacion es mas complejo que una cola de comandos.
- AWS SQS, Azure Service Bus y Google Pub/Sub reducen operacion propia y escalan
  bien, pero introducen dependencia regional/proveedor, coste y requisitos de
  residencia y conectividad privada.
- Redis Streams es rapido y sencillo, pero requiere diseñar durabilidad,
  failover y reconciliacion con PostgreSQL con especial cuidado.

La interfaz de repositorio permite adoptar otro broker en el futuro. No se ha
seleccionado ni declarado operativo ninguno de estos proveedores.

## Rollback

1. Detener entradas externas y workers; esperar o cancelar de forma explicita
   los trabajos `processing`.
2. Conservar PostgreSQL y sus ejecuciones como evidencia; no borrar la cola.
3. Cambiar `PLATFORM_WORKFLOW_DATASTORE=sqlite` y reiniciar un unico nodo web.
4. Verificar `/api/health` y mantener webhooks/cron externos deshabilitados hasta
   confirmar que el modo anterior puede asumirlos sin duplicidad.

El rollback no copia automaticamente ejecuciones nuevas a SQLite. Volver al
modo anterior pierde continuidad funcional, aunque PostgreSQL conserva la
evidencia. Por ello debe usarse solo durante desarrollo y con ventana controlada.

## Limites pendientes

- SQLite ya no se carga en el proceso web; sólo permanece como herramienta de
  importación heredada. Flentio aún no es HA.
- La clave local no sirve para workers en hosts distintos; faltan KMS/secret
  manager, backup/PITR y adaptador SIEM externo. La auditoría/outbox PostgreSQL
  sí es compartida y append-only.
- No se realizaron pruebas de estres ni se certifican SLO bancarios.
- Las aprobaciones, reintentos y cancelación cooperativa ya son durables. Sigue
  faltando reconciliación específica para cada integración con efectos externos.
- Produccion requiere BIA, topologia, backup/restore, seguridad y revision
  independiente, aunque esa revision no sea posible durante el desarrollo.

## Control de ejecución añadido el 01-08-2026

La migración `013` y el Panel de Operaciones incorporan cancelación real de
trabajos pendientes o reclamados. El worker consulta la señal durable sin
mantener una transacción abierta y propaga `AbortSignal` a OpenAI, Gemini y
Ollama. Contrato, seguridad, rollback y evidencia:
`docs/PLATFORM_EXECUTION_CONTROL.md` y
`docs/audits/PLATFORM_EXECUTION_CONTROL_2026-08-01.md`.
