# Evidencia F6 — 31-07-2026

Estado: `VALIDACIÓN local`.

En PostgreSQL real `pgvector/pgvector:pg16` se aplicaron migraciones 001–007 y se reaplicó 007. Se crearon simultáneamente particiones HNSW de 768 y 1.536 dimensiones. La cola reclamó una sola tarea; se activó atómicamente el candidato 1.536D y se reactivó el 768D como rollback. Otro tenant obtuvo `RLS_OK` y cero catálogos visibles. Backend: 30/30 pruebas y cero vulnerabilidades; frontend: compilación y auditoría sin vulnerabilidades.

Después se ejecutó un backfill real sobre los tres documentos de Drive mediante Ollama: candidato 3/3, activación atómica, consulta real con reranker y rollback al índice original 3/3. Se reutilizó `nomic-embed-text` con 768 dimensiones, por lo que la prueba acredita la mecánica online y no una mejora del modelo. No se generaron embeddings ficticios.

El corpus sintético de tres documentos no acredita rendimiento, escala ni calidad bancaria. HA está deliberadamente fuera del desarrollo actual por decisión del propietario. Evidencia integrada y límites: `docs/audits/RAG_FULL_ACCEPTANCE_2026-07-31.md`.
