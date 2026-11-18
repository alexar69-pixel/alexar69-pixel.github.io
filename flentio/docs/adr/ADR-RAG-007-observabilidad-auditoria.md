# ADR-RAG-007: observabilidad agregada y auditoría append-only

- Estado: aceptada para validación local
- Fecha: 31-07-2026

## Decisión

PostgreSQL es la fuente de verdad de F7. Las métricas se calculan sobre tablas RLS y sólo contienen conteos, estados, tiempos, tasas, códigos de error y tamaño vectorial estimado. Las preguntas ya se guardan únicamente como SHA-256 y ningún endpoint F7 devuelve contenido o fragmentos.

`audit_events` registra automáticamente transiciones de ingesta, seguridad, conectores e índices. El rol de aplicación sólo tiene `SELECT`; inserta mediante una función `SECURITY DEFINER` y no puede actualizar ni borrar. Un trigger constituye una segunda barrera append-only. La correlación de una petición se conserva si el cliente entrega un identificador válido o el backend genera un UUID.

No se selecciona SIEM. El endpoint Prometheus permite una integración posterior y el webhook SIEM heredado sigue siendo best-effort, no entrega garantizada. La retención, WORM externo y destino SIEM requieren decisión bancaria.

