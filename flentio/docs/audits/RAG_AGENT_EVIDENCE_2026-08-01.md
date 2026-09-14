# Evidencia — contrato RAG para agentes (01-08-2026)

## Alcance y entorno

Validación local real sobre PostgreSQL 16/pgvector, embeddings Ollama,
reranker TEI `Alibaba-NLP/gte-multilingual-reranker-base`, el documento DORA
oficial efectivo del tenant técnico y Ollama `llama3.2:3b`. No se utilizaron
respuestas prefabricadas, mocks de modelo ni datos de clientes.

La migración 015 se aplicó dos veces sin error. El registro usa RLS y no conserva
consulta, respuesta o contenido: una consulta SQL confirmó
`jsonb_path_exists(evidence_references,'$[*].content') = false`.
El endpoint autenticado devolvió HTTP 200 con los tres estados y las únicas
claves de referencia fueron identificadores, título, versión, ubicación,
procedencia, cita y puntuaciones; `hasContentField=false`.

## Ejecuciones verificadas

1. **Fallo cerrado anterior al esquema.** TEI seleccionó 4 fragmentos DORA entre
   40 candidatos; el mejor reranker fue 0,9548163. `llama3.2:3b` respondió sin
   `[E#]`. Flentio devolvió `AGENT_CITATION_VALIDATION_FAILED`, no propagó la
   respuesta y registró `citation_rejected/CITATIONS_REQUIRED`.
2. **Respuesta estructurada aceptada.** Con esquema JSON nativo y temperatura 0,
   la misma consulta seleccionó 4 evidencias. El modelo respondió con `[E2]` y
   declaró `E2`; Flentio comprobó pertenencia e igualdad, devolvió
   `RESPUESTA_CON_EVIDENCIA`, `grounded=true` y persistió `grounded`.
3. **Abstención real.** Se pidió una categoría inexistente y se configuró
   deliberadamente un nombre de modelo inexistente. La recuperación devolvió
   cero evidencias y Flentio produjo `EVIDENCIA_INSUFICIENTE`,
   `modelCalled=false`, sin intentar resolver ese modelo. El registro durable
   tiene `answer_sha256=NULL`.

Los registros de correlación usados fueron
`local-agent-evidence-validation`,
`local-agent-evidence-structured-validation` y
`local-agent-abstention-validation`. Son etiquetas técnicas de desarrollo, no
identidades ni ejecuciones de cliente.

## Dictamen y límites

Resultado: **VALIDACIÓN local**. Está probada la mecánica de recuperación,
abstención, esquema, citas, rechazo y auditoría con Ollama real. No prueba que la
respuesta sea jurídicamente correcta, que cada afirmación esté respaldada, el
rendimiento bajo carga ni compatibilidad real con OpenAI/Gemini. Esas puertas
siguen `NO EVALUADA`, aplazadas o `DEPENDENCIA_CLIENTE` según corresponda.

El 01-08-2026 se contrastaron los formatos con la documentación oficial:
OpenAI conserva Structured Outputs en Chat Completions y Gemini documenta el
API Interactions con `response_format`. Los adaptadores quedaron alineados a
esos contratos y la clave Gemini pasó de la URL a `x-goog-api-key`. Esta revisión
estática no sustituye una ejecución autorizada contra ninguno de los dos
proveedores.

## Verificaciones finales

```powershell
cd backend
npm run migrate:rag
npm run migrate:rag
npm test
# 77/77 pruebas superadas

cd ../frontend
npm run build
# compilación correcta; permanece el aviso conocido de bundle > 500 kB

cd ..
docker compose --env-file backend/.env config --quiet
# configuración válida
```

Tras reiniciar web y worker, `/api/health` devolvió `OPERATIVO` y confirmó los
datastores PostgreSQL de plataforma, identidad y workflows.

Diseño, operación y rollback: `docs/RAG_AGENT_EVIDENCE_CONTRACT.md`.
