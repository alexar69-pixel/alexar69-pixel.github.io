# Evidencia del adaptador OpenAI para reranking — 2026-08-01

## Dictamen

OpenAI API queda **INTEGRADO / NO_CONFIGURADO** como opción productiva autorizada. No se realizó una llamada externa ni se declaran métricas de calidad, coste o latencia porque no se proporcionó una credencial de workload ni se aprobó todavía el tratamiento de corpus.

## Controles comprobados localmente

- selección no-code entre `tei` y `openai`;
- uso de `POST /v1/responses` con JSON Schema estricto;
- conjunto completo de candidatos en una petición para mantener comparabilidad;
- clave únicamente en `Authorization`, nunca en cuerpo, respuesta o frontend;
- rechazo de JSON inválido, cobertura parcial, índices duplicados y scores fuera de 0–1;
- timeout y HTTP no satisfactorio convertidos en `RAG_RERANKER_UNAVAILABLE`;
- salud autenticada mediante consulta del modelo configurado;
- TEI local conservado sin cambios funcionales.

## Pruebas

Se añadió `codex-oauth-local` para desarrollo, bloqueado en producción. Una prueba real con Codex CLI 0.146 autenticado mediante ChatGPT OAuth comparó dos textos sintéticos: la norma de transferencias/pagos obtuvo `0,99` y la política de vacaciones `0,01`. No se usaron documentos del repositorio ni una API key.

La primera aceptación integral detectó que el umbral TEI `0,12` no era transferible: una ejecución OAuth clasificó una pregunta inexistente como evidencia. La configuración local OAuth se elevó a `0,70`; esta corrección es una calibración provisional del corpus aislado, no un umbral productivo aprobado.

Una repetición reveló además que el arnés conservaba un tenant fijo y cambiaba el propietario; PostgreSQL/RLS rechazó correctamente versionar esas fuentes. El arnés asigna ahora un tenant aislado por ejecución, sin relajar políticas ni borrar evidencia previa.

## Aceptación integral OAuth final

`npm run validate:rag-f4` terminó `VALIDADO` sobre seis documentos y cinco preguntas del corpus aislado no bancario:

- MRR base `1,0000`; MRR OAuth `1,0000`; delta `0`;
- p95 base `115 ms`; p95 OAuth `5.770 ms`;
- multilingüe, filtro temporal y aislamiento entre tenants: correctos;
- evidencia insuficiente: correcta con umbral local provisional `0,70`;
- caída controlada del ejecutable: consulta cerrada y fallo registrado.

La latencia confirma que abrir Codex CLI por consulta sólo es apropiado para desarrollo interactivo. No satisface un SLO productivo ni sustituye OpenAI API.

La comprobación operativa quedó cerrada con una sonda real de `codex login status`: confirma la sesión ChatGPT sin consumir una inferencia, devuelve `NO_DISPONIBLE` ante error/timeout y conserva `productionAllowed: false`. Resultado local: `OPERATIVO`, modelo `gpt-5.6-luna`, umbral `0,70`, 40 candidatos. Suite final: **81/81 pruebas correctas**.

## Aislamiento del proceso OAuth

El proceso Codex ya no hereda el entorno completo del backend. Recibe sólo rutas del sistema, directorios de perfil necesarios para el login OAuth, temporales y proxy; quedan fuera `RAG_DATABASE_URL`, credenciales de objetos, claves API y demás configuración sensible. Además se fuerza `shell_environment_policy.inherit="none"`, sandbox de sólo lectura, directorio vacío, sesiones efímeras y web deshabilitada. Una prueba real posterior mantuvo la salud `OPERATIVO` y ordenó `transferencias bancarias` (`0,95`) por encima de `vacaciones` (`0`).

Se limitó la concurrencia OAuth a un proceso por defecto. La prueba automatizada demostró rechazo del segundo proceso con motivo `RAG_RERANKER_BUSY` y liberación posterior del cupo. Suite final: **82/82 pruebas correctas**.

## Cierre de endurecimiento

Codex ignora configuración, reglas, plugins y MCP del usuario; usa aprobación `never`, red desactivada para herramientas y un perfil que deniega lectura general del disco salvo binarios mínimos. Se añadió límite de consulta de 4.000 caracteres aplicado antes de cualquier dependencia y configuración contextual no-code.

La aceptación real posterior volvió a terminar `VALIDADO`: MRR base/OAuth `1,0000`, p95 base `127 ms`, p95 OAuth `8.167 ms`, multilingüe, filtro temporal, RLS, evidencia insuficiente, fallo cerrado y registro de error correctos. El aumento de latencia refuerza su clasificación exclusiva de desarrollo. Suite backend: **83/83**; auditoría productiva npm: **0 vulnerabilidades**; frontend compilado correctamente con el aviso conocido de bundle superior a 500 kB.

Como control final, el parser JSONL rechaza cualquier evento de comando, cambio de archivo, MCP o búsqueda web, incluso si Codex produce después un ranking conforme al esquema. La prueba negativa y una llamada OAuth real posterior fueron correctas (`0,98` pagos frente a `0,02` vacaciones). Suite final: **84/84 pruebas correctas**.

Las pruebas automatizadas verifican además el contrato y la prohibición productiva. Los dobles permanecen exclusivamente dentro del código de test y no simulan disponibilidad productiva.

## Puertas pendientes

- credencial real en bóveda y prueba contra OpenAI;
- contrato, residencia, retención, subencargados y autorización de datos;
- modelo productivo fijado y evaluación A/B sobre corpus autorizado;
- calibración independiente de `RAG_EVIDENCE_MIN_SCORE`;
- coste, p95/p99, resiliencia y límites de cuota.

## Reversión

Establecer `RAG_RERANKER_PROVIDER=tei`, restaurar endpoint/modelo TEI y comprobar `/api/rag/status`. No se requiere migración ni se destruyen índices o métricas históricas.
