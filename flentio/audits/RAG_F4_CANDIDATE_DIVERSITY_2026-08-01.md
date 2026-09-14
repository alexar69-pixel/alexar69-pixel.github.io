# Evidencia F4 — candidatos diversificados y metadatos, 01-08-2026

## Dictamen

**VALIDACIÓN local ampliada**, no certificación bancaria ni prueba de escala. La tubería
`hybrid-multilingual-metadata-rrf-diverse-tei-v3` evita que normas extensas ocupen todo el
conjunto previo al reranker. No se modificaron las 16 preguntas, las fuentes esperadas,
el umbral ni los documentos para mejorar el resultado.

## Cambio real

- PostgreSQL recupera un pool autorizado por los canales vectorial, léxico de fragmento
  y metadatos documentales (`title`, `category`, `source_key`).
- La migración idempotente 011 crea un `tsvector` almacenado y un índice GIN sobre esos
  metadatos. RLS, ACL, clasificación, vigencia y fechas se aplican dentro de SQL.
- `RAG_RETRIEVAL_POOL_MULTIPLIER=4` amplía cada canal desde 40 hasta 160 entradas; el
  resultado SQL observado fue de 163–168 filas en las consultas EPC diagnosticadas.
- `RAG_RETRIEVAL_MAX_CHUNKS_PER_DOCUMENT=4` selecciona por rondas entre documentos y
  después rellena capacidad, por lo que un tenant pequeño no pierde resultados.
- TEI sigue recibiendo exactamente 40 candidatos en lotes secuenciales de 5. El texto
  enviado incluye título y categoría autorizados junto al fragmento, sin crear contenido.
- La respuesta y salud exponen versión, filas del pool, candidatos finales, límite por
  documento y parámetros físicos del reranker.

## Evidencia reproducible

- Migración 011 aplicada dos veces: `OPERATIVO`, pgvector 0.8.6.
- Columna generada e índice `rag_documents_metadata_search_gin` comprobados en PostgreSQL.
- Backend: 68/68 pruebas superadas, incluidas las 4 pruebas focales de
  diversificación/normalización.
- Frontend Vite compilado; persiste el aviso preexistente de bundle principal >500 kB.
- Docker Compose validado con `backend/.env`.
- Los tres documentos EPC ausentes en v2 entraron antes de TEI: EPC132-08 en rango 7,
  EPC135-18 en rango 2 y EPC131-17 en rango 2.
- El comando oficial se ejecutó con `RAG_PUBLIC_CORPUS_SOURCE_MODE=verified-local` porque
  EUR-Lex devolvió contenido incompleto al intentar refrescar. Este modo exigió los 16
  originales locales en estado verificado, informó URL, SHA-256, bytes y fecha de última
  verificación, y no afirmó una descarga nueva.

| Métrica | Base v3 sin TEI | Candidato v3 TEI | Diferencia |
|---|---:|---:|---:|
| Recall@K | 0,9375 | 1,0000 | +0,0625 |
| MRR | 0,765625 | 0,968750 | +0,203125 |
| nDCG@K | 0,809650 | 0,976933 | +0,167283 |
| Precisión@K | 0,1875 | 0,7250 | +0,5375 |
| Precisión automática de citas | 0,1875 | 0,7250 | +0,5375 |
| p50 | 242 ms | 742 ms | +500 ms |
| p95 | 406 ms | 878 ms | +472 ms |
| p99 | 406 ms | 878 ms | +472 ms |

TEI produjo cero 429 y cero reintentos. Estas cifras describen 16 consultas locales y
no demuestran SLO, concurrencia, decenas de miles de documentos ni fidelidad jurídica.

## Seguridad, capacidad y rollback

La consulta de metadatos se genera sólo con letras/dígitos Unicode, un máximo de 16
términos y parámetros PostgreSQL; no concatena texto del usuario en SQL. El pool queda
acotado a 1.000 entradas por canal y 2.000 filas combinadas. El índice GIN reduce la ruta
de metadatos, pero su plan y capacidad deben volver a medirse con distribución bancaria.

Rollback de código: restaurar v2 y dejar la migración 011 instalada pero sin uso; es
aditiva y no expone documentos. No se debe borrar índice/columna hasta confirmar que
ninguna instancia v3 los usa y completar la ventana de mantenimiento. Reducir el
multiplicador o aumentar el límite documental cambia capacidad, pero **no** reproduce
exactamente v2 y no se documenta como rollback equivalente.

## Puertas pendientes

Corpus privado autorizado, evaluación de fidelidad por humanos, objetivos/SLO aprobados,
capacidad y concurrencia representativas, HA productiva, homologación del proveedor y
revisión independiente. F4 continúa en `VALIDACIÓN local ampliada`.
