# Calidad de recuperación del RAG (F4)

## Finalidad y estado

F4 mejora la selección de evidencia que consumen todos los agentes de Flentio, con independencia de que el modelo generativo sea Gemini, OpenAI/ChatGPT, Ollama u otro. Está en **VALIDACIÓN local**: existe implementación real y evidencia reproducible, pero no se declara rendimiento bancario ni selección productiva definitiva.

El OCR continúa fuera de alcance. La expansión y descomposición automáticas de preguntas tampoco se han activado: sólo se incorporarán si un corpus bancario autorizado demuestra una mejora medible sin degradar autorización, citas ni latencia.

## Canalización real

1. PostgreSQL aplica tenant, RLS, ACL, clasificación, vigencia y estado documental antes de entregar candidatos.
2. La recuperación híbrida combina HNSW vectorial, texto español y `tsvector(simple)` multilingüe mediante RRF.
3. Los filtros opcionales `capturedAfter` y `capturedBefore` restringen la fecha de captura dentro de SQL.
4. Se amplía un pool acotado por canal, se añade coincidencia de título/categoría/clave de fuente mediante GIN y se selecciona por rondas entre documentos.
5. La selección se reduce a `RAG_RERANKER_CANDIDATES`. TEI procesa lotes secuenciales; OpenAI recibe el conjunto completo en una petición estructurada para que sus puntuaciones sean comparables. Ambos adaptadores ordenan únicamente puntuaciones reales del proveedor.
6. Sólo se devuelven resultados con puntuación mínima `RAG_EVIDENCE_MIN_SCORE`.
7. La respuesta incluye versión del pipeline, proveedor/modelo, latencia, número de candidatos y resultado `EVIDENCIA_SUFICIENTE` o `EVIDENCIA_INSUFICIENTE`.

La API pública no acepta una opción para omitir el reranker. El modo base sin reranker sólo está disponible en el evaluador interno. Si el servicio falla, la consulta devuelve `503 NO_DISPONIBLE`, registra `RAG_RERANKER_UNAVAILABLE` y no fabrica puntuaciones ni utiliza silenciosamente conocimiento general del modelo.

El procesamiento por lotes es completamente fail-closed: si falla una sola petición, se descartan los resultados parciales. El modelo GTE/TEI devuelve una puntuación independiente por par pregunta-fragmento; la prueba real del 01-08-2026 produjo `0,6770471` para el mismo par evaluado solo y dentro de un lote distinto, con diferencia absoluta cero.

## Fragmentación tipada

El fragmentador `flentio-typed-structured/typed-structured-v3` conserva estructura y es reproducible. El usuario puede seleccionar el tipo desde la interfaz no-code; la inferencia por contenido/MIME sólo actúa como alternativa conservadora.

| Tipo | Tratamiento |
|---|---|
| `regulation` | Mantiene artículos y encabezados normativos |
| `contract` | Mantiene cláusulas |
| `procedure` | Mantiene pasos y secciones operativas |
| `report` | Conserva jerarquía de encabezados |
| `table` | Repite cabecera y registra intervalo de filas |
| `general` | Fragmentación estructural genérica |

## Proveedor actual y contrato de sustitución

El proveedor validado en desarrollo es **Hugging Face Text Embeddings Inference (TEI) 1.9** con `Alibaba-NLP/gte-multilingual-reranker-base`, revisión inmutable `a6258e9d2b1a11aa7bccdff9efde562bbca4393d`. También existe `codex-oauth-local`, que invoca una sesión oficial de Codex CLI autenticada con ChatGPT, en proceso efímero, directorio vacío y sandbox de solo lectura. El backend lo prohíbe con `NODE_ENV=production`. El 01-08-2026 se verificó realmente con dos textos sintéticos. Para producción, **OpenAI API** sigue siendo la opción principal: Responses API, JSON Schema estricto y credencial de workload.

`backend/src/rag/rerankerProvider.js` separa el contrato de la implementación. Todo adaptador futuro debe:

- recibir pregunta y candidatos ya autorizados;
- devolver exactamente un índice único y una puntuación finita entre 0 y 1 por candidato;
- respetar timeout y normalizar errores como indisponibilidad explícita;
- exponer una comprobación real de salud;
- registrar proveedor, modelo y versión sin alterar el significado de las métricas.

Añadir un nombre en configuración sin su adaptador no habilita un proveedor: Flentio permanece `NO_CONFIGURADO` o `NO_DISPONIBLE`.

## Opciones de mercado

| Alternativa | Características favorables | Costes, riesgos o límites | Estado |
|---|---|---|---|
| TEI + GTE multilingual local | Datos y operación bajo control propio; modelo Apache-2.0; más de 70 idiomas; contexto de 8.192 tokens; API estable de reranking | Requiere GPU, capacidad, actualizaciones, observabilidad y HA propias; no aporta SLA gestionado | Integrado y validado sólo en desarrollo |
| OpenAI Responses API | Servicio administrado, salida estructurada, modelos multilingües y operación productiva simplificada | Envía consulta y fragmentos autorizados a un tercero; exige contrato, residencia, retención, coste, SLO y calibración del score | Integrado por autorización; prueba real pendiente de credencial y homologación |
| ChatGPT OAuth mediante Codex CLI | Reutiliza en local el inicio de sesión oficial sin API key; salida estructurada y proceso efímero | Cuenta personal, cuota interactiva, latencia de proceso y sin contrato de servicio backend | Integrado y probado sólo en desarrollo; bloqueado en producción |
| Cohere Rerank v4 | Servicio administrado, variantes Pro/Fast y soporte multilingüe superior a 100 idiomas; reduce operación propia | Salida de fragmentos hacia un tercero, coste por uso, residencia/contrato/SLA y dependencia del proveedor | Posible adaptador futuro, no integrado |
| Jina Reranker v3 / API | Multilingüe, contexto largo y opciones API o despliegue controlado según oferta | La API implica salida de datos; la licencia publicada del modelo v3 es CC-BY-NC para uso no comercial y el uso comercial/autohospedado requiere revisar contrato/licencia | Posible adaptador futuro, no integrado |
| Reranker corporativo homologado | Puede ajustarse a nube privada, residencia, soporte y contrato bancario existentes | Calidad, normalización de puntuación, API y coste dependen del producto; exige evaluación con el mismo corpus | Contrato preparado, proveedor no seleccionado |

Fuentes oficiales consultadas: [modelos soportados por TEI](https://huggingface.co/docs/text-embeddings-inference/en/supported_models), [API `/rerank` de TEI](https://huggingface.co/docs/text-embeddings-inference/quick_tour), [ficha de GTE multilingual reranker](https://huggingface.co/Alibaba-NLP/gte-multilingual-reranker-base), [Cohere Rerank](https://docs.cohere.com/docs/reranking-with-cohere) y [Jina Reranker](https://jina.ai/en-US/reranker/).

La selección bancaria debe evaluar precisión con corpus autorizado, residencia y retención de datos, cifrado, certificaciones, subencargados, SLA, soporte, coste, límites, portabilidad, HA/DR y procedimiento de salida. F4 no decide ese contrato.

## Configuración

| Variable | Función | Valor de desarrollo |
|---|---|---|
| `RAG_RERANKER_PROVIDER` | Adaptador autorizado | `tei` o `codex-oauth-local` en local; `openai` productivo |
| `RAG_RERANKER_ENDPOINT` | Endpoint del servicio | TEI privado; para OpenAI se omite y usa `https://api.openai.com/v1` |
| `RAG_RERANKER_MODEL` | Modelo registrado en métricas | `Alibaba-NLP/gte-multilingual-reranker-base` |
| `RAG_RERANKER_TIMEOUT_MS` | Tiempo máximo antes de fallo cerrado | `15000` |
| `RAG_RERANKER_CANDIDATES` | Amplitud previa al reranking | `40` |
| `RAG_RERANKER_BATCH_SIZE` | Máximo de fragmentos por petición secuencial a TEI | `5` |
| `RAG_RETRIEVAL_POOL_MULTIPLIER` | Amplitud por canal antes de diversificar (2–10; máximo interno 1.000) | `4` |
| `RAG_RETRIEVAL_MAX_CHUNKS_PER_DOCUMENT` | Rondas iniciales por documento antes de rellenar por relevancia (1–20) | `4` |
| `RAG_EVIDENCE_MIN_SCORE` | Umbral de evidencia | `0.12` |
| `OPENAI_API_KEY` | Secreto requerido por el adaptador OpenAI | Bóveda/variable de workload; nunca navegador ni Git |
| `RAG_CODEX_CLI_PATH` | Ruta opcional al ejecutable oficial; se autodetecta en Antigravity | Sólo desarrollo |
| `RAG_CODEX_OAUTH_MAX_CONCURRENCY` | Máximo de procesos OAuth simultáneos (1–4) | `1` |
| `RAG_MAX_QUERY_CHARS` | Límite aplicado antes de PostgreSQL, embeddings o reranking | `4000` |

El umbral es una línea base local, no universal ni transferible entre proveedores. TEI conserva `0.12`; la validación aislada de `codex-oauth-local` parte de `0.70` porque sus scores tienen otra distribución. Debe recalibrarse por versión con falsos positivos/negativos y aprobación humana antes de producción.

## Evaluación reproducible

`npm run evaluate:rag -- <dataset.json>` consulta el índice real dos veces: pipeline híbrido base y candidato con reranker. El JSON exige pregunta y fuentes esperadas; admite relevancia graduada, citas esperadas, `topK` y fechas. Calcula Recall@K, MRR, nDCG@K, precisión, precisión de citas y p50/p95/p99. Nunca inserta documentos ni simula resultados.

La identidad de evaluación se define con `RAG_EVALUATION_ORGANIZATION`, `RAG_EVALUATION_GROUPS`, clearance y actor. Por ello queda sujeta a la misma RLS que un usuario. La fidelidad de respuestas se declara `NO_EVALUADA` hasta disponer de respuestas y jueces humanos o protocolo formalmente aprobado.

`npm run validate:rag-f4` requiere confirmación explícita y usa un corpus aislado, no bancario. Comprueba tipos documentales, consulta multilingüe, tiempo, tenant cruzado, evidencia insuficiente, fallo cerrado y métrica de error. No debe ejecutarse contra producción.

El corpus público bancario reproducible se define en `backend/data/rag-public-corpus/catalog.json` y se opera según `docs/RAG_PUBLIC_BANKING_CORPUS.md`. La v3 diversificada obtuvo Recall@K 1,0000, MRR 0,96875, nDCG 0,97693 y precisión automática de citas 0,7250, sin HTTP 429 ni reintentos; p95 candidato 878 ms. La ejecución reutilizó 16 originales públicos locales verificados porque EUR-Lex no pudo refrescarse y lo declaró expresamente. No son métricas jurídicas, de escala ni productivas.

## Operación y reversión

- `/api/rag/status` muestra salud, modelo, política de fallo y umbral.
- Para `codex-oauth-local`, la salud ejecuta únicamente `codex login status` y sólo publica `OPERATIVO` cuando el cliente confirma `Logged in using ChatGPT`; no realiza inferencia ni expone tokens.
- El modo OAuth no mantiene una cola oculta. Si alcanza `RAG_CODEX_OAUTH_MAX_CONCURRENCY`, devuelve `503 NO_DISPONIBLE` con motivo `RAG_RERANKER_BUSY`; al terminar o fallar libera siempre el cupo.
- Codex se inicia con `--ignore-user-config` y `--ignore-rules`, sin plugins/MCP, aprobación `never`, red de herramientas desactivada y un perfil que niega lectura del disco salvo binarios mínimos. La consulta se limita mediante `RAG_MAX_QUERY_CHARS` antes de tocar infraestructura.
- Flentio inspecciona el JSONL de Codex y rechaza toda ejecución que contenga `command_execution`, `file_change`, `mcp_tool_call` o `web_search`, aunque exista después un mensaje final válido.
- `/api/rag/metrics` agrega p99, consultas sin evidencia, fallos y latencia del reranker.
- El panel **Configuración corporativa → Cerebro IA (RAG)** permite configurar, consultar fechas, elegir tipo y ver puntuaciones/canalización.
- En pantallas estrechas, un selector de sección sustituye a las pestañas horizontales y las rejillas RAG pasan a una columna para evitar texto recortado o solapado.
- Para revertir código, se conserva la versión base en el evaluador, pero la API productiva no debe degradarse silenciosamente. Una conmutación productiva necesita aprobación y variable versionada antes del despliegue.
- Cambiar el tamaño de lote no revierte la selección. El rollback exacto de v3 requiere restaurar el código v2; no debe degradarse silenciosamente desde la API.
- Las migraciones 005 y 011 son aditivas. El rollback seguro deja columnas e índices sin uso; no se recomienda borrarlos hasta terminar la retención y confirmar que ninguna versión los utiliza.

## Límites abiertos

- corpus público de 16 preguntas y 16 documentos, útil para ingeniería pero sin políticas ni datos privados de un banco;
- sin prueba de decenas de miles de documentos ni concurrencia representativa;
- sin jueces humanos de fidelidad;
- sin HA del reranker, por decisión de desarrollo;
- sin umbral/SLO bancario aprobado;
- precisión de citas medida automáticamente, pendiente de validación humana;
- expansión y descomposición aplazadas por falta de mejora demostrada;
- el 1,0000 de Recall se limita a 16 preguntas públicas y no permite afirmar cobertura bancaria general.
- el adaptador OpenAI no está validado contra el corpus mientras falten credencial, homologación contractual y presupuesto autorizado.
