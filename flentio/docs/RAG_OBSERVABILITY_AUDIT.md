# RAG F7: observabilidad y auditoría

## Panel operativo

La pestaña **Operación RAG** consulta PostgreSQL en tiempo real y muestra estado, documentos listos, fragmentos, consultas, tasa sin resultado, p95, colas, conectores y tamaño estimado de vectores. No usa cifras prefabricadas. Si el RAG no está configurado, el endpoint falla explícitamente.

Las alertas internas utilizan umbrales de desarrollo. Los objetivos provisionales de ingeniería autorizados para carga, disponibilidad, frescura, RPO y RTO se mantienen separados en `docs/RAG_PRODUCTION_READINESS.md`; todavía no están demostrados ni aprobados por un BIA de cliente:

- `INGESTION_FAILED` / `INGESTION_STALE` → `RB-F7-INGESTION`;
- `CONNECTOR_UNAVAILABLE` → `RB-F7-CONNECTOR`;
- `REINDEX_FAILED` → `RB-F7-REINDEX`;
- `RERANKER_FAILURE` → `RB-F7-RETRIEVAL`;
- `ZERO_RESULT_RATE` → `RB-F7-QUALITY`.
- `WORM_DIVERGENCE` / `WORM_UNAVAILABLE` → `RB-F3-WORM`.

`RAG_ALERT_PENDING_SECONDS` vale 900 y `RAG_ALERT_ZERO_RESULT_RATE` 0,35 por defecto. Cambiarlos no equivale a aprobar un SLO.

## API

- `GET /api/rag/observability?days=7`: snapshot JSON RLS.
- `GET /api/rag/observability/prometheus?days=7`: texto Prometheus protegido por autenticación.
- `GET /api/rag/observability/audit?limit=50&cursor=...`: eventos append-only; roles admin/editor.

El exportador usa una métrica con etiqueta de nombre y nunca expone tenant, actor, pregunta, texto, filename o secreto. La integración de un scraper debe usar identidad técnica y TLS en el proxy corporativo.

## Runbooks

### RB-F7-INGESTION

Revisar estado de ClamAV, MinIO y proveedor de embeddings; consultar `error_code`; verificar edad y reintentos. No cambiar trabajos a `completed` manualmente. Recuperar el proveedor y reanudar el worker.

### RB-F7-CONNECTOR

Revisar OAuth, cuota, cursor, último éxito y eventos fallidos. Una revocación requiere una credencial nueva del mismo propietario. Ejecutar reconciliación; no borrar cursor ni tombstones.

### RB-F7-REINDEX

Revisar modelo, dimensión, cuota y cobertura. Pausar para proteger ingesta. Reanudar conserva embeddings confirmados. No activar con cobertura incompleta ni eliminar el activo anterior.

### RB-F7-RETRIEVAL / RB-F7-QUALITY

Comprobar reranker, endpoint y modelo. Para tasa sin resultados, revisar corpus, vigencia, ACL y evaluación F4 antes de bajar umbrales. Nunca fabricar evidencia ni desactivar RLS.

### RB-F3-WORM

No modificar el original. Confirmar proveedor, versión, permisos y
conectividad; distinguir `UNAVAILABLE` de una divergencia comprobada. Preservar
el hallazgo y escalar a Seguridad, Datos y Records Management. Legal hold y
retención sólo cambian mediante decisión autorizada. Cerrar únicamente tras un
nuevo `MATCH`. Procedimiento: `docs/RAG_WORM_RECONCILIATION.md`.

## Auditoría y privacidad

Los triggers guardan entidad, transición, actor, correlación, resultado y código de error. El payload documental, la pregunta y el mensaje de error completo quedan excluidos. Las tablas históricas de seguridad y ciclo documental permanecen disponibles con sus propias RLS.

Un trabajo `failed` permanece en el historial. La alarma `INGESTION_FAILED` cuenta como no recuperado únicamente si no existe después un trabajo `completed` para la misma fuente y clave; Prometheus separa `ingestion_failed_unresolved` de `ingestion_failed_historical`. Recuperar el documento no borra ni reescribe el fallo original.

El archivo heredado `data/audit.log` es un sink de compatibilidad. Usa HMAC sólo con `AUDIT_HMAC_SECRET`; sin secreto declara `sha256-unkeyed`. No es WORM y no sustituye `audit_events` ni un SIEM homologado.

## Opciones de mercado

| Destino | Ventajas | Inconvenientes / pendiente |
|---|---|---|
| Splunk HEC | token HTTPS e indexer acknowledgement según edición/configuración | coste, esquema, reintentos y ack deben implementarse; webhook actual no basta |
| Microsoft Sentinel | encaje con Entra/Azure, AMA, Event Hub y conectores custom | DCR, workspace, identidad, coste y región requieren diseño del banco |
| Elastic/OpenSearch | control on-prem o gestionado y ecosistema abierto | operación, ILM, seguridad y soporte dependen del despliegue |
| Datadog | SaaS integrado de logs/métricas/APM | residencia, coste por volumen y dependencia externa |
| OpenTelemetry Collector | contrato neutral y enrutamiento a varios backends | no es SIEM por sí solo; requiere collector HA y un destino final |

Ninguno está integrado como entrega durable en F7. La estrategia aprobada evita imponer proveedor: outbox durable y adaptadores sustituibles, priorizando Sentinel o Splunk según la plataforma ya operada por cada banco. Comparativa y fuentes: `docs/RAG_PRODUCTION_READINESS.md`.
