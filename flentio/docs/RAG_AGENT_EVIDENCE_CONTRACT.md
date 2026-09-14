# Contrato de evidencia RAG para agentes IA

## Finalidad

Este contrato impide que un agente de workflow presente como documentada una
respuesta que Flentio no pueda vincular con fragmentos autorizados del RAG. Es
independiente del modelo generativo: el mismo conjunto RLS se entrega a Ollama,
Gemini u OpenAI mediante identificadores locales `E1`…`E50`.

Estado: **VALIDACIÓN local**. Ollama `llama3.2:3b` está validado de extremo a
extremo. Los adaptadores de salida estructurada para OpenAI y Gemini están
implementados, pero permanecen `NO VALIDADO` hasta disponer de credenciales y
modelos autorizados. Esto no demuestra fidelidad semántica o jurídica.

## Recorrido real

1. El nodo **Vector Store (RAG)** ejecuta recuperación híbrida RLS, diversidad,
   reranking real y umbral de evidencia.
2. Cada fragmento recibe un identificador efímero (`E1`, `E2`…) válido sólo para
   esa invocación. No procede del usuario ni del modelo.
3. Si la recuperación devuelve `EVIDENCIA_INSUFICIENTE`, el agente registra la
   abstención y **no llama** al proveedor generativo.
4. Con evidencia suficiente, Flentio envía contenido delimitado y un esquema
   JSON obligatorio: `answer` y `evidenceIds`. El texto debe incluir `[E#]` y la
   lista debe coincidir exactamente.
5. Flentio analiza la respuesta, rechaza JSON inválido, ausencia de citas,
   identificadores inexistentes o listas inconsistentes. Una respuesta
   rechazada no se propaga a nodos posteriores.
6. Una respuesta válida queda como `RESPUESTA_CON_EVIDENCIA` con respuesta,
   referencias, proveedor, modelo, pipeline y registro de auditoría.

La validación comprueba pertenencia de las citas, no que cada frase esté
semánticamente implicada por el fragmento. Esa fidelidad requiere evaluación
humana o un protocolo aprobado y continúa `NO EVALUADA`.

## Configuración visual

El nodo muestra como campos principales **Consulta** y **Evidencias máximas**.
En **Opciones avanzadas** quedan categoría documental, fechas de captura y
similitud vectorial mínima. La política de citas/abstención no puede desactivarse
desde el navegador. El panel de salida presenta estado, respuesta y referencias;
el JSON técnico queda plegado.

Ejemplo de configuración persistida por el lienzo:

```json
{
  "query": "{{ $json.question }}",
  "similarityLimit": 5,
  "category": "Normativa bancaria",
  "capturedAfter": "2026-01-01T00:00"
}
```

## Resultado para nodos posteriores

Una respuesta aceptada expone `status`, `answer`/`result`, `citations`,
`evidence`, `retrieval`, `provider`, `model`, `modelCalled`, `grounded` y
`evidenceAuditId`. La evidencia visible contiene referencias y puntuaciones, no
el texto completo del fragmento. Una abstención usa `answer=null`,
`modelCalled=false` y `grounded=false`.

Los estados auditables son:

| Estado | Significado |
|---|---|
| `grounded` | JSON correcto y todas las citas pertenecen al conjunto recuperado |
| `evidence_insufficient` | No hay evidencia; el modelo no se invocó |
| `citation_rejected` | El modelo respondió, pero incumplió el contrato |
| `generation_failed` | El proveedor real falló o no estaba disponible |

## Auditoría y privacidad

La migración `015_agent_evidence_runs.sql` crea un registro RLS por tenant. Se
guardan actor, correlación de workflow/job, nodo, proveedor/modelo, estado,
pipeline, referencias sin contenido y SHA-256 de consulta/respuesta. No se
guardan en esta tabla la pregunta, la respuesta ni el texto de los fragmentos.
`GET /api/rag/agent-evidence-runs` devuelve sólo los registros del actor
autenticado. **Operación RAG** los muestra plegados.

La ejecución durable del workflow conserva la respuesta autorizada y sus
referencias para que los nodos posteriores puedan consumirla. Los errores de
citación detienen el workflow o siguen exclusivamente una rama de error
configurada.

## Proveedores y alternativas

| Proveedor | Ventaja | Límite | Estado |
|---|---|---|---|
| Ollama | Datos y modelo locales; esquema JSON soportado | Capacidad y calidad dependen del hardware/modelo | Validado con `llama3.2:3b` |
| OpenAI | Esquema JSON estricto en modelos compatibles | Transferencia externa, coste, contrato y credencial | Chat Completions `response_format`; implementado, no validado |
| Gemini | Esquema JSON en el API Interactions | Transferencia externa, región, contrato y credencial | `response_format` de Interactions; implementado, no validado |
| Otro proveedor | Puede integrarse tras el mismo contrato | Requiere adaptador, homologación y prueba negativa | `NO_CONFIGURADO` |

Elegir proveedor productivo, región y política de datos exige autorización
humana. Cambiar el LLM no modifica el conocimiento ni obliga a reindexar; cambiar
el modelo de embeddings sí requiere el proceso F6.

Referencias de compatibilidad consultadas el 01-08-2026: documentación oficial
de [salidas estructuradas de OpenAI](https://developers.openai.com/api/docs/guides/structured-outputs)
y [salidas estructuradas de Gemini](https://ai.google.dev/gemini-api/docs/structured-output).
Los identificadores de modelo son texto configurable en el frontend para evitar
acoplar Flentio a un catálogo que cambia. Toda combinación proveedor/modelo debe
homologarse con credenciales autorizadas antes de declararla operativa.

## Operación y rollback

- Una caída del reranker o del modelo es visible y falla cerrada.
- Una cita rechazada debe revisarse en la salida del nodo y en **Operación RAG**;
  no se debe convertir manualmente en éxito.
- Para revertir, despliegue juntos runner y adaptadores anteriores. La migración
  015 es aditiva y puede permanecer instalada sin escrituras nuevas.
- No elimine registros hasta que la política de retención del cliente lo permita.
- Si se deshabilita un proveedor, el sistema debe mostrar `NO CONFIGURADO` o
  `NO DISPONIBLE`; nunca genera una respuesta de respaldo ficticia.

Evidencia: `docs/audits/RAG_AGENT_EVIDENCE_2026-08-01.md`.
