# Control durable de ejecuciones PostgreSQL

## Estado y alcance

Estado: **VALIDACIÓN local — OPERATIVO** desde el 01-08-2026.

Flentio propaga `organization_id` y `requested_by` desde el trabajo hasta el
worker, el RAG y la resolución de credenciales. La aplicación no abre SQLite en
el recorrido web. Los resultados, logs y estados se escriben en PostgreSQL bajo
RLS. Esta capacidad no depende de HA, SIEM, KMS o datos del cliente.

## Cancelación cooperativa

`POST /api/workflows/jobs/:id/cancel` acepta un motivo opcional de hasta 500
caracteres. Sólo el solicitante original o un administrador de la misma
organización puede cancelar el trabajo.

- `pending`: cambia inmediatamente a `cancelled` y fija `completed_at`.
- `processing`: conserva el lease y registra `cancellation_requested_at`; el
  worker confirma `cancelled` en el siguiente punto seguro.
- estados terminales: devuelve HTTP 409; nunca reescribe la evidencia.

La migración `013_workflow_cooperative_cancellation.sql` añade la señal durable,
su actor y motivo. `workflow_job_control_state` sólo entrega al worker dos
booleanos —propiedad del lease y cancelación— y no expone payloads ni secretos.

Los workers comprueban la señal al iniciar, entre nodos y durante backoff. Las
llamadas HTTP de OpenAI, Gemini y Ollama reciben `AbortSignal`. Si un proveedor
ya produjo un efecto externo que no admita cancelación, Flentio no afirma poder
revertirlo: ese conector debe implementar idempotencia y reconciliación propias.

## Operación no-code

El Panel de Operaciones lista la cola PostgreSQL con origen, estado, intentos y
solicitud de cancelación. El botón **Cancelar** no manipula JSON ni SQL. El panel
se actualiza cada ocho segundos y presenta por separado ejecuciones terminadas.

La analítica ROI se muestra como `DEPENDENCIA_CLIENTE`. Flentio no calcula horas o
euros mediante constantes. Un despliegue futuro podrá aportar fuentes, moneda,
costes y reglas aprobadas por el cliente mediante un contrato aún no diseñado.

## Escalado y concurrencia

- reclamación atómica con `FOR UPDATE SKIP LOCKED`;
- transacciones cortas antes y después de red o inferencia;
- índices parciales para pendientes, leases caducados y cancelaciones activas;
- RLS e índices compuestos por organización;
- modelo at-least-once documentado, sin prometer exactly-once.

## Rollback

1. Detener workers y entradas de webhook/cron.
2. Conservar columnas y eventos de cancelación; son compatibles hacia atrás.
3. Revertir el código del worker y ocultar el botón si fuera necesario.
4. No eliminar la migración ni reabrir trabajos `cancelled`.

## Validación

`npm run validate:platform-orchestration` verificó cancelación inmediata y
cancelación processing confirmada por un worker real. La validación HTTP
confirmó autorización, persistencia del motivo y respuesta 200. Las 41 pruebas
unitarias pasaron. No se realizaron pruebas de estrés ni HA.
