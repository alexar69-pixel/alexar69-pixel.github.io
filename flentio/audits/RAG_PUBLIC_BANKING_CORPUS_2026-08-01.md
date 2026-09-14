# Evidencia local del corpus público bancario — 01-08-2026

## Resultado

Estado: `VALIDACION_LOCAL_PUBLICA`. Se descargaron e ingirieron 16 fuentes oficiales reales en el tenant aislado `flentio-public-quality-v1`: 16 documentos `ready`, 15 `effective`, 1 handbook SWIFT histórico `expired` y 4.604 fragmentos con embeddings `nomic-embed-text`.

Los originales proceden de EUR-Lex, European Payments Council, IRS y SWIFT. Pasaron por ClamAV, extracción `flentio-html-text` o `pdf-parse`, cifrado y MinIO. PostgreSQL conserva tamaño, SHA-256, origen y versión. El catálogo exacto, URLs y estados están en `backend/data/rag-public-corpus/catalog.json`.

## Calidad observada

| Métrica | Híbrido base | TEI/GTE | Diferencia |
|---|---:|---:|---:|
| Recall@5 | 0,6875 | 0,6875 | 0,0000 |
| MRR | 0,5729 | 0,6458 | +0,0729 |
| nDCG@5 | 0,6019 | 0,6563 | +0,0543 |
| Precisión@5 | 0,5250 | 0,5333 | +0,0083 |
| Precisión automática de citas | 0,5250 | 0,5915 | +0,0665 |
| p50 | 258 ms | 341 ms | +83 ms |
| p95 | 296 ms | 401 ms | +105 ms |
| p99 | 296 ms | 401 ms | +105 ms |

Se evaluaron 16 preguntas de alcance documental. El lote local del reranker fue 5 y no hubo reintentos por sobrecarga. Las métricas muestran mejora de ordenación, no suficiencia para producción bancaria.

## Incidencia real y corrección

Dos ejecuciones previas fallaron cerradas porque TEI devolvió HTTP 429 `Model is overloaded`. Los logs mostraron `no permits available` al enviar el lote local de 40 candidatos. Una petición real de dos textos funcionó. El arnés se limitó explícitamente a cinco candidatos para esta GPU y la ejecución final terminó sin reintentos; el límite productivo no se cambió ni se simuló una respuesta.

El control de idempotencia se corrigió en dos pasos. Primero pasó a consultar la captura verificada más reciente y no sólo el original primario de su versión. Una segunda ejecución mostró que EUR-Lex varía bytes de plantilla entre peticiones aunque el texto jurídico sea igual: PDF se compara por SHA-256 binario y HTML por SHA-256 del texto canónico indexable, conservando ambas huellas como evidencia.

La comprobación final devolvió `SKIPPED_UNCHANGED` para 16/16 fuentes. Durante una repetición intermedia Ollama local dejó de escuchar en el puerto 11434 y la evaluación falló con `fetch failed`; el servicio se levantó de nuevo con el mismo modelo y no se fabricaron embeddings. La repetición final completó recuperación y TEI. Su p95 base incluyó el calentamiento de Ollama (2.376 ms), por lo que la tabla conserva la primera ejecución completa y estable; no se usa esa repetición como nueva línea base de latencia.

## Pruebas y límites

- `npm test`: 62/62 pruebas superadas.
- Se verificaron allowlist HTTPS, redirección final, MIME/tamaño, extracción HTML sin scripts, PDFs reales y ciclo de vida histórico.
- SWIFT MyStandards/CBPR+ vigente y Knowledge Centre: `NO_CONFIGURADO`, requieren identidad/permisos del cliente.
- Fidelidad jurídica: `NO_EVALUADA`; faltan jueces humanos y protocolo aprobado.
- No se ejecutaron OCR, estrés, HA, SLO/RPO/RTO ni revisión independiente.

## Rollback

Eliminar el automatismo no elimina documentos. Se deja de ejecutar el comando y se revierte el catálogo/descargador. Las fuentes se retiran mediante archivo gobernado y sus originales permanecen sujetos a retención/legal hold. Nunca se borra directamente MinIO o PostgreSQL.
