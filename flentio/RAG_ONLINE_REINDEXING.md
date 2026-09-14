# RAG F6: reindexación versionada sin corte

## Finalidad

Cambiar modelo o dimensión de embeddings obliga a recalcular todos los fragmentos. F6 evita apagar consultas o sobrescribir el único índice: activo y candidato coexisten hasta que la calidad y cobertura permiten una conmutación atómica.

Estados: `building` → `evaluating` → `active` → `retired`; un fallo queda `failed`. Los trabajos pueden estar `pending`, `processing`, `paused`, `evaluating`, `failed` o `cancelled`. Una partición por candidato admite dimensiones distintas entre 64 y 2.000 y recibe su HNSW antes del backfill.

## Recorrido no-code

En **Configuración avanzada del motor RAG**, un administrador selecciona proveedor, modelo y dimensión y pulsa **Crear candidato**. El panel muestra cobertura y trabajo. Cuando aparece `EVALUATING`, se ejecuta la evaluación real sobre el mismo corpus autorizado de F4 y se registra su informe. **Activar / rollback** exige la referencia de ese informe y confirmación explícita. Un índice `retired` puede reactivarse como rollback mientras se conserve su partición.

API equivalente:

- `GET /api/rag/embedding-indexes`;
- `POST /api/rag/embedding-indexes`;
- `POST /api/rag/embedding-indexes/jobs/:jobId/pause|resume`;
- `POST /api/rag/embedding-indexes/:indexId/activate` con `evaluation.approved=true`.

## Proveedores

| Proveedor | Estado Flentio | Ventajas | Inconvenientes / validación exigida |
|---|---|---|---|
| Ollama | integrado | ejecución local, control de residencia, modelos abiertos | operación, GPU, parches y capacidad recaen en el cliente; calidad varía por modelo |
| OpenAI embeddings | integrado | API gestionada, dimensiones configurables en la familia `text-embedding-3`, residencia regional sujeta a contrato | coste, dependencia externa, revisión legal/residencia y claves empresariales |
| Gemini / Vertex AI | futuro | ecosistema Google y modelos de embedding dedicados | adaptador, tareas query/document, cuotas, residencia y versiones deben validarse; no operativo |
| Cohere Embed | futuro | modelos multilingües y dimensiones configurables en Embed v4 | adaptador y contrato; ciclo de deprecaciones y coste; no operativo |
| Voyage AI, Jina o modelos TEI locales | futuro | alternativas especializadas o abiertas | benchmarking bancario, soporte, licencia, residencia y adaptador; no operativos |

Los modelos generativos Gemini o ChatGPT siguen separados: redactan sobre los fragmentos recuperados, pero no sustituyen el conocimiento RAG ni determinan por sí solos el modelo de embedding.

## Operación y rollback

1. Confirmar espacio para al menos activo + candidato.
2. Crear candidato con un tamaño de lote conservador.
3. Vigilar `indexed_chunks/expected_chunks`, errores y carga del proveedor.
4. Pausar si afecta a ingesta; no borrar el trabajo.
5. Evaluar Recall@K, MRR, nDCG, precisión/fidelidad de citas y p95/p99 con corpus representativo.
6. Activar sólo con cobertura completa e informe aprobado.
7. Conservar el anterior durante la ventana de rollback bancaria.

La activación no cambia datos documentales. Un query ya iniciado puede terminar usando el índice anterior, que permanece intacto. Nuevas consultas ven el puntero nuevo. No existe limpieza automática ni simulación de métricas.

## Alcance excluido ahora

No se configuraron réplica, PITR, PgBouncer, múltiples nodos, SLO/RPO/RTO ni ensayos de caída. Son parte futura de F6 y requieren decisión del banco. Tampoco se ejecutó un backfill real porque no hay proveedor de embeddings y corpus autorizado activos en este entorno.

