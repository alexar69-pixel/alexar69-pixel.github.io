# ADR-RAG-004: reranking intercambiable con TEI local y OpenAI productivo

- Estado: aceptada para validación de desarrollo
- Fecha: 31-07-2026
- Decisor: autorización humana del propietario de Flentio

## Contexto

F4 necesita ordenar candidatos autorizados con un modelo real, mantener los fragmentos fuera de APIs externas durante el desarrollo y permitir cambiar de proveedor en el futuro. El usuario autorizó TEI local con GTE multilingüe y pidió documentar alternativas. HA queda fuera del desarrollo actual.

## Decisión

Se integra `Alibaba-NLP/gte-multilingual-reranker-base` mediante TEI, fijando imagen y revisión del modelo en Compose. El 01-08-2026 el propietario autorizó OpenAI API como proveedor productivo principal, conservando TEI/Ollama para trabajo local. El adaptador OpenAI utiliza Responses API con JSON Schema estricto, exige todos los índices una vez y conserva las puntuaciones entregadas por el modelo. Gemini permanece como extensión futura, no operativa.

La política ante timeout, respuesta incompleta, índice duplicado, puntuación inválida o caída es **fallo cerrado**: HTTP 503, métrica explícita y ninguna evidencia entregada. Se rechaza la degradación silenciosa porque podría cambiar la calidad y procedencia sin quedar visible.

## Consecuencias

Favorables: privacidad local durante desarrollo, proveedor administrado para producción, interfaz común y fallo uniforme. Costes: TEI requiere GPU; OpenAI implica transferencia de contenido autorizado, coste por uso y homologación contractual. La autorización técnica no aprueba por sí sola datos bancarios, residencia, retención, SLO ni el umbral.

## Alternativas consideradas

- Cohere: menor operación y oferta multilingüe administrada; no elegido ahora por salida de contenido, contrato, residencia y coste pendientes.
- Jina: opciones multilingües API/on-prem; no elegido ahora por los mismos controles de terceros y revisión de licencia comercial.
- Sin reranker: menor latencia, pero no satisface la fase ni aporta un segundo juicio semántico.
- Puntuaciones simuladas o fallback heurístico: rechazados por las normas permanentes y por imposibilidad de auditar su equivalencia.

## Revisión futura

OpenAI debe superar evaluación A/B sobre el mismo corpus autorizado antes de activarse. Un proveedor adicional, incluido Gemini, requiere adaptador, salud, normalización estricta, análisis legal/seguridad y prueba de fallo. Cambiar sólo variables no constituye una integración.
