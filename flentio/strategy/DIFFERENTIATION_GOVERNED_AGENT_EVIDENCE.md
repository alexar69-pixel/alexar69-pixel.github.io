# Ficha de diferenciación — Ejecución no-code con evidencia gobernada

## Identificación

- **Propuesta:** convertir cada decisión y acción de un agente Flentio en una cadena de evidencia autorizada, reproducible y restaurable, desde el documento original hasta la ejecución del workflow.
- **Responsable:** Producto e Ingeniería Flentio.
- **Fecha:** 01-08-2026.
- **Estado:** `NO_VALIDADA` como oportunidad de mercado; capacidades técnicas parciales en `VALIDACIÓN local`.
- **Usuarios:** equipos bancarios de operaciones, riesgo, cumplimiento, auditoría y tecnología que diseñan automatizaciones sin código.

## Necesidad no cubierta

### Hipótesis

Los equipos regulados no necesitan únicamente respuestas RAG con citas ni un diseñador de agentes. Necesitan demostrar, para cada acción automatizada, qué identidad la solicitó, qué conocimiento autorizado se recuperó, qué versión exacta del original sustentó la decisión, qué permisos se aplicaron, qué modelo y pipeline intervinieron, qué aprobación humana existió y cómo reconstruir o revertir el recorrido.

El impacto y la disposición a pagar todavía no están comprobados mediante entrevistas o procesos de compra. Por ello la necesidad permanece `NO_VALIDADA` y no puede comunicarse como carencia universal del mercado.

## Mercado y alternativas examinadas

| Alternativa actual | Capacidades publicadas | Límite relevante para la hipótesis | Fuente consultada |
|---|---|---|---|
| Microsoft Copilot Studio | RAG empresarial, fuentes autenticadas, citas, moderación, validación de grounding y gobierno | Su propia guía sitúa el RAG principalmente en preguntas factuales y no en comparación documental o evaluación compleja de políticas. Las citas de una fuente de conocimiento no pueden utilizarse como entrada de otras herramientas o acciones en determinados modos | [Guía RAG](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/retrieval-augmented-generation), [fuentes de conocimiento](https://learn.microsoft.com/en-in/microsoft-copilot-studio/knowledge-copilot-studio) |
| LangSmith | Datasets, evaluación offline/online, trazas, evaluación de recuperación, respuesta y pasos intermedios | Es una plataforma sólida de evaluación y observabilidad; no se presenta como diseñador bancario no-code que gobierne originales WORM, ACL documentales y aprobación de acciones dentro del mismo contrato operativo | [Evaluación RAG](https://docs.langchain.com/langsmith/evaluate-rag-tutorial), [pasos intermedios](https://docs.langchain.com/langsmith/evaluate-on-intermediate-steps) |

Este análisis no demuestra ausencia de competidores. Faltan entrevistas, pruebas de producto y revisión estructurada de más plataformas de automatización, búsqueda empresarial, gobierno de IA y process mining.

## Ventaja propuesta de Flentio

La oportunidad no es competir como otro chatbot RAG. La ventaja propuesta es un **contrato de evidencia ejecutable** que atraviese todo el flujo no-code:

1. autorización PostgreSQL/RLS antes de recuperar contenido;
2. procedencia hasta el original cifrado, versionado y sujeto a retención/legal hold;
3. recuperación versionada, umbral de evidencia y fallo cerrado;
4. entrega de un sobre de evidencia tipado a cada agente o nodo;
5. aprobación humana vinculada a evidencia y versión del workflow;
6. auditoría reconstruible de consulta, decisión, herramienta, resultado y reversión;
7. validación continua que convierte fallos reales autorizados en nuevos casos de evaluación.

El usuario empresarial debería configurar políticas, responsabilidades y criterios mediante lenguaje y formularios, sin editar JSON, SQL o prompts internos.

## Defensa legítima frente a réplica

- [x] Integración profunda con procesos autorizados.
- [x] Conocimiento especializado y trazable.
- [x] Controles regulatorios, seguridad y auditoría integrados.
- [x] Automatizaciones compuestas difíciles de coordinar por separado.
- [x] Experiencia no-code como objetivo de producto.
- [ ] Datos o aprendizaje diferencial: pendiente de clientes y permisos reales.
- [ ] Efectos de red: no demostrados.

La defensa potencial procede de acumular conectores gobernados, taxonomías aprobadas, evaluaciones representativas, políticas por jurisdicción y evidencia operativa verificable. El código o la interfaz aislados sí serían replicables; la ventaja sólo será defendible si el conjunto reduce de forma medible el esfuerzo de aprobación, auditoría y operación del cliente.

## Validación y métricas

| Hipótesis | Método | Umbral inicial | Resultado | Estado |
|---|---|---|---|---|
| El banco no puede reconstruir fácilmente por qué un agente actuó | 8–12 entrevistas con Operaciones, Riesgo, Auditoría y Arquitectura | ≥60 % identifica el problema entre sus tres principales fricciones | Sin entrevistas | `NO_VALIDADA` |
| El contrato de evidencia reduce preparación de auditoría | Piloto controlado frente al proceso actual | ≥50 % menos tiempo, cero evidencia crítica ausente | Sin piloto | `NO_VALIDADA` |
| El flujo no-code permite gobernar sin soporte técnico continuo | Prueba con usuarios objetivo | ≥80 % completa configuración y revisión sin editar código | Sin prueba | `NO_VALIDADA` |
| La evidencia conserva seguridad y fidelidad | Corpus autorizado y revisión humana | 0 fugas de autorización; ≥95 % citas correctas; fidelidad aprobada | Sólo evidencia local no bancaria | `VALIDACIÓN` |
| La operación cumple el presupuesto del cliente | Carga representativa | SLO contractual todavía por definir | No medido | `NO_VALIDADA` |

### Criterios de decisión

- **Continuar:** la fricción aparece repetidamente, el piloto reduce tiempo/riesgo y existe patrocinador con datos autorizados.
- **Reformular:** se valora la trazabilidad, pero como complemento de una plataforma existente y no como producto independiente.
- **Descartar:** los clientes resuelven el recorrido con coste aceptable o no autorizan integrar la evidencia necesaria.

## Riesgos y obligaciones

- La composición de controles puede ser valiosa sin ser única; no se afirmará exclusividad.
- Los competidores pueden ampliar rápidamente sus capacidades.
- La defensa depende de conocimiento, integración y evidencia acumulada, no de encerrar datos.
- Exportaciones, originales, métricas y políticas deben conservar formatos documentados y portabilidad.
- No se usarán datos bancarios en validación sin autorización expresa.
- OCR permanece fuera de alcance.
- Una hipótesis fallida debe poder retirarse sin destruir procedencia ni bloquear workflows existentes.

## Dictamen

- **Decisión:** `CONTINUAR` únicamente con validación de problema y prototipo medible; no ampliar todavía como gran módulo comercial.
- **Evidencia:** Flentio ya verifica localmente varios componentes del contrato, mientras las alternativas publican capacidades fuertes de RAG y evaluación pero no demuestran en las fuentes revisadas el mismo recorrido bancario completo.
- **Afirmaciones prohibidas por ahora:** “único”, “sin competencia”, “imposible de replicar”, “cumplimiento bancario garantizado” o “preparado para producción”.
