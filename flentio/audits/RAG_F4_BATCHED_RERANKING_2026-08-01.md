# Evidencia F4 — reranking TEI por lotes, 01-08-2026

## Objetivo y cambio real

La GPU local devolvió HTTP 429 al enviar 40 fragmentos en una sola petición TEI. Flentio separa ahora la amplitud de recuperación (`RAG_RERANKER_CANDIDATES=40`) de la capacidad física por petición (`RAG_RERANKER_BATCH_SIZE=5`). El adaptador procesa lotes secuenciales, traduce índices locales a globales y ordena las puntuaciones reales. Un fallo de cualquier lote invalida toda la consulta.

La versión observable del pipeline es `hybrid-multilingual-rrf-tei-batched-v2`. La salud publica candidatos, lote, ejecución secuencial y política `fail_closed`. La interfaz muestra estos valores como estado real y no intenta modificar dinámicamente parámetros de infraestructura.

## Evidencia

- 64/64 pruebas backend superadas.
- Build React/Vite completada; persiste el aviso preexistente de bundle principal superior a 500 kB.
- Consistencia TEI real: el mismo par obtuvo `0,6770471` solo y dentro de otro lote; diferencia absoluta 0.
- Corpus: 16/16 fuentes `SKIPPED_UNCHANGED`; no se alteró conocimiento para mejorar métricas.
- Evaluación: 16 preguntas, 40 candidatos, lotes de 5, cero HTTP 429 y cero reintentos.

| Métrica | Base híbrida | TEI por lotes | Diferencia |
|---|---:|---:|---:|
| Recall@5 | 0,6875 | 0,8125 | +0,1250 |
| MRR | 0,5729 | 0,7813 | +0,2083 |
| nDCG@5 | 0,6019 | 0,7894 | +0,1875 |
| Precisión@5 | 0,5250 | 0,6250 | +0,1000 |
| Precisión automática de citas | 0,5250 | 0,6250 | +0,1000 |
| p50 candidato | — | 718 ms | — |
| p95 candidato | — | 746 ms | — |
| p99 candidato | — | 746 ms | — |

El p95 base de esa ejecución fue 1.581 ms por calentamiento de Ollama y no se utiliza para afirmar que TEI reduce latencia. La evidencia válida es el p95 absoluto del candidato y la ausencia de sobrecarga.

## Tres fallos restantes

Los documentos esperados no aparecieron en los 40 candidatos, por lo que TEI no pudo ordenarlos:

1. EPC132-08, guía Customer-to-PSP ISO 20022.
2. EPC135-18, códigos de motivo de R-transactions SCT.
3. EPC131-17, aclaraciones SCT/SCT Inst.

Los candidatos están dominados por múltiples fragmentos de documentos EUR-Lex extensos. La siguiente mejora será ampliar y diversificar el conjunto previo con un límite por documento, conservando RLS y midiendo de nuevo. No se modificaron preguntas, fuentes esperadas ni umbral.

## Configuración, riesgo y rollback

`RAG_RERANKER_BATCH_SIZE` admite 1–64 y no puede superar `RAG_RERANKER_CANDIDATES`. Cada lote dispone del timeout configurado; ocho lotes pueden aumentar el tiempo total. Una caída intermedia falla cerrada y no entrega parciales.

Para volver temporalmente a una petición se iguala el lote a los candidatos, sólo con capacidad demostrada. El rollback de código restaura el adaptador único y la versión v1. No se modifican documentos, embeddings ni esquema PostgreSQL.
