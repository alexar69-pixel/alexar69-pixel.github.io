# ADR-RAG-006: reindexación de embeddings sin corte

- Estado: aceptada para validación local
- Fecha: 31-07-2026
- Exclusión: no implementa HA en desarrollo

## Decisión

Cada tenant posee un puntero lógico a un índice `active`. Un candidato `building` usa su propia partición de `chunk_embeddings` y su propio HNSW, incluso con otra dimensión. El backfill se reclama mediante `SKIP LOCKED`, llama al proveedor fuera de la transacción y guarda lotes idempotentes. Al completar cobertura pasa a `evaluating`; sólo un administrador puede activarlo aportando una evaluación explícitamente aprobada. La transacción retira el activo anterior y activa el candidato bajo un advisory lock. El índice retirado se conserva para rollback.

La columna vectorial histórica de `chunks` se mantiene nullable para migración y reversión, pero las nuevas consultas usan el catálogo versionado. Si el activo cambia durante una ingesta, la transacción se revierte y el trabajo se reintenta con el modelo nuevo.

## Consecuencias

La coexistencia consume almacenamiento aproximadamente proporcional al número de candidatos. No se permite borrar particiones desde la API. La eliminación requiere retención aprobada, backup verificado y una migración administrativa posterior. El worker prioriza ingestas ordinarias y usa el tiempo libre para reindexar, reduciendo impacto durante desarrollo.

