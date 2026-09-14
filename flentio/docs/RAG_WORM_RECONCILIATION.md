# Reconciliación de originales y controles WORM

## Finalidad y comportamiento real

La reconciliación compara periódicamente PostgreSQL con la versión exacta del
original almacenado. Detecta pérdida, inaccesibilidad o divergencias de tamaño,
ETag, checksums, legal hold y retención. No descarga el contenido, no cambia
controles remotos, no elimina objetos y no autorrepara una discrepancia.

El trabajo es durable, reanudable y multiinstancia. PostgreSQL reclama cada job
con `FOR UPDATE SKIP LOCKED`, procesa lotes ordenados por UUID y recupera jobs
interrumpidos. Las funciones `SECURITY DEFINER` sólo permiten leer objetos que
pertenecen al tenant del job reclamado y registrar su resultado; no conceden al
actor técnico acceso a chunks ni contenido documental.

## Estados y hallazgos

- `SIN_DATOS`: todavía no existe una ejecución visible para el tenant.
- `pending` / `processing`: trabajo durable pendiente o en curso.
- `completed`: se comprobaron todos los originales del job.
- `failed`: falló la ejecución; se conserva código y error acotado.
- `MATCH`: almacenamiento y PostgreSQL coinciden.
- `DIVERGENT`: existe evidencia verificable diferente.
- `UNAVAILABLE`: el proveedor no pudo comprobarse; no se infiere corrupción.

Los códigos persistidos son `PROVIDER_MISMATCH`, `OBJECT_UNAVAILABLE`,
`EVIDENCE_MISMATCH`, `LEGAL_HOLD_MISMATCH` y `RETENTION_MISMATCH`. Los hallazgos
contienen metadatos operativos, nunca bytes, fragmentos, tokens ni claves.

## Operación no-code

En **Configuración corporativa → Operación RAG**, la tarjeta **Integridad de
originales y controles WORM** muestra la última ejecución y permite
**Comprobar ahora** a administradores y editores. La confirmación aclara que la
acción es de sólo lectura. El botón se deshabilita mientras existe un job activo.

| Método y ruta | Rol | Resultado |
| --- | --- | --- |
| `GET /api/rag/worm-reconciliation` | admin/editor | últimas ejecuciones y hallazgos del tenant |
| `POST /api/rag/worm-reconciliation` | admin/editor | crea o devuelve el job activo; HTTP 202 |

## Configuración

```dotenv
RAG_WORM_RECONCILE_INTERVAL_HOURS=24
RAG_WORM_RECONCILE_POLL_MS=5000
RAG_WORM_RECONCILE_BATCH_SIZE=50
RAG_WORM_RECONCILE_STALE_MINUTES=15
```

El intervalo admite 1–720 horas, el lote 1–500 objetos, el polling 500–120000
ms y la recuperación 1–1440 minutos. El scheduler crea como máximo un job
activo por tenant. PostgreSQL garantiza una sola reclamación entre nodos.

## Alertas y runbook RB-F3-WORM

`WORM_DIVERGENCE` es crítica; `WORM_UNAVAILABLE` es advertencia. Ambas se
exportan como métricas Prometheus agregadas.

1. No modificar ni borrar el objeto afectado.
2. Confirmar proveedor, versión, región, permisos y conectividad.
3. Comparar el hallazgo con la procedencia y auditoría append-only.
4. Escalar divergencias a Seguridad, Datos y Records Management.
5. Sólo un cambio autorizado puede restablecer legal hold o ampliar retención;
   nunca reducirlos automáticamente.
6. Ejecutar de nuevo y cerrar únicamente con `MATCH` real.

## Rollback

Detener el scheduler no cambia datos remotos; jobs y hallazgos permanecen como
evidencia. No eliminar la migración 010 si existen registros. Al reanudar, los
jobs `processing` obsoletos vuelven a `pending` tras el umbral configurado.

## Evidencia y límites

La validación local comprobó 9 originales reales en MinIO: 9 `MATCH`, 0
divergencias y 0 indisponibles. Un primer intento reveló que RLS ocultaba
documentos al actor técnico; permanece auditado. Se corrigió con funciones
acotadas por job/tenant, sin claims inventados. Evidencia:
`docs/audits/RAG_WORM_RECONCILIATION_2026-08-01.md`.

No acredita AWS S3, AWS KMS, HA, capacidad ni controles del cliente.

