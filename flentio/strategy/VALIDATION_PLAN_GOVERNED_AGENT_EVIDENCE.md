# Plan de validación — Ejecución no-code con evidencia gobernada

## Objetivo

Determinar si bancos y otras organizaciones reguladas sufren una carencia prioritaria al reconstruir y aprobar decisiones de agentes, y si el contrato de evidencia de Flentio reduce de forma medible tiempo, riesgo y dependencia técnica.

Este plan valida el problema antes de ampliar el producto. No autoriza datos bancarios reales, acceso a sistemas de clientes ni afirmaciones comerciales de exclusividad.

## Preguntas que deben resolverse

1. ¿Qué decisiones automatizadas necesitan reconstruir hoy y por qué?
2. ¿Qué evidencia falta habitualmente entre documento, recuperación, decisión, aprobación y acción?
3. ¿Cuánto trabajo manual provoca y qué incidentes, observaciones o retrasos genera?
4. ¿Qué herramientas y controles actuales utilizan?
5. ¿Pagarían o cambiarían procesos para resolverlo?
6. ¿Qué integración mínima sería necesaria para que Flentio tuviera valor?
7. ¿Qué requisito impediría comprar o desplegar la solución?

## Muestra mínima

Realizar entre 8 y 12 entrevistas, evitando concentrarlas en un solo perfil:

| Perfil | Mínimo | Perspectiva buscada |
|---|---:|---|
| Operaciones bancarias | 2 | Excepciones, tiempos y continuidad |
| Riesgo o Cumplimiento | 2 | Evidencia, controles y responsabilidad |
| Auditoría interna/externa | 2 | Reconstrucción, muestreo y hallazgos |
| Arquitectura, Seguridad o Plataforma | 2 | Integración, identidad, datos y operación |
| Propietario de proceso o transformación | 1 | Prioridad, presupuesto y adopción |

No se considerarán suficientes entrevistas realizadas únicamente con desarrolladores, proveedores o miembros del equipo Flentio.

## Selección y consentimiento

- Registrar organización, sector, país, rol y tamaño sólo con consentimiento.
- No solicitar nombres de clientes, expedientes, credenciales, documentos ni incidentes confidenciales.
- Permitir respuestas anonimizadas.
- Indicar que Flentio está validando un problema y no vendiendo una capacidad certificada.
- Separar notas textuales, interpretación y conclusión.

## Guion de entrevista neutral

### Contexto

1. Describa la última vez que tuvo que explicar o auditar una decisión automatizada.
2. ¿Qué desencadenó la revisión y quién participó?
3. ¿Qué sistemas y documentos fue necesario consultar?

### Proceso actual

4. ¿Cómo reconstruyeron qué identidad, regla, dato o versión influyó en la decisión?
5. ¿Qué partes estaban disponibles automáticamente y cuáles hubo que recopilar a mano?
6. ¿Cuánto tiempo transcurrió y qué perfiles intervinieron?
7. ¿Qué evidencia no pudo recuperarse o resultó ambigua?
8. ¿Qué ocurre cuando cambia un documento, modelo, permiso o workflow?

### Impacto

9. ¿Qué coste, retraso, riesgo o trabajo repetido produjo?
10. ¿Con qué frecuencia sucede?
11. ¿Cómo se prioriza frente a otras necesidades?

### Alternativas

12. ¿Qué productos o desarrollos internos emplean actualmente?
13. ¿Qué funciona bien y no debería sustituirse?
14. ¿Qué carencia concreta permanece?
15. ¿Han presupuestado o intentado resolverla? ¿Qué detuvo el proyecto?

### Validación de solución — sólo después de comprender el problema

16. Si pudiera recorrer desde la acción hasta el original, permisos, fragmentos, modelo, aprobación y versión del workflow, ¿qué parte aportaría valor y cuál no?
17. ¿Quién usaría el recorrido y quién debería administrarlo?
18. ¿Qué sistemas tendría que integrar obligatoriamente?
19. ¿Qué requisitos de residencia, retención, identidad, SIEM, KMS, HA o revisión bloquearían un piloto?
20. ¿Qué resultado justificaría continuar después de cuatro semanas?

No preguntar «¿le gusta la idea?» ni aceptar interés general como intención de compra.

## Registro de evidencia

Crear una fila por entrevista sin información sensible:

Utilizar `docs/templates/PROBLEM_INTERVIEW_RECORD.md` como registro individual.

| Campo | Contenido |
|---|---|
| Código | Identificador anónimo |
| Perfil y jurisdicción | Categoría, no identidad personal |
| Proceso narrado | Hecho observado |
| Frecuencia | Valor o intervalo aportado |
| Tiempo/personas | Estimación del entrevistado |
| Herramientas actuales | Productos o desarrollo interno |
| Carencia | Expresión textual breve |
| Prioridad | Top 3 / media / baja |
| Evidencia de presupuesto | Existente / previsto / inexistente / desconocido |
| Bloqueadores | Seguridad, legal, integración, operación |
| Interpretación Flentio | Separada de los hechos |

## Puerta de problema

Continuar hacia un piloto sólo si se cumplen todas:

- al menos 60 % identifica la reconstrucción/evidencia entre sus tres fricciones principales;
- al menos cuatro organizaciones o unidades independientes relatan un caso reciente;
- existe evidencia de tiempo, riesgo o coste, no sólo opiniones;
- al menos dos participantes aceptan explorar un piloto o proceso de compra;
- la carencia no queda resuelta adecuadamente por la configuración normal de su plataforma actual;
- los bloqueadores permiten un piloto sin datos productivos.

Si sólo se valora la observabilidad, reformular como complemento exportable. Si el problema no aparece repetidamente, descartar la ampliación.

## Piloto controlado

### Alcance

- Un proceso de bajo riesgo y alto valor explicativo.
- Corpus sintético o público aprobado; datos reales sólo con autorización posterior.
- Un workflow versionado, una aprobación humana y una acción reversible.
- Dos roles de lectura y un rol de revisión.
- Comparación contra el procedimiento actual.

### Recorrido mínimo

1. Ingerir y aprobar un documento con procedencia verificable.
2. Ejecutar una consulta y conservar el sobre de evidencia.
3. Proponer una acción sin ejecutarla automáticamente.
4. Aprobar o rechazar mostrando exactamente la evidencia utilizada.
5. Ejecutar una acción reversible tras aprobación.
6. Cambiar una versión documental y demostrar qué ejecuciones quedan afectadas.
7. Reconstruir el recorrido completo sin consultar logs técnicos crudos.

### Métricas

| Métrica | Umbral para continuar |
|---|---:|
| Tiempo de reconstrucción frente al proceso actual | Reducción ≥50 % |
| Evidencias críticas ausentes | 0 |
| Accesos no autorizados | 0 |
| Citas/originales correctos en revisión humana | ≥95 % |
| Usuarios que completan revisión sin código/SQL/JSON | ≥80 % |
| Acciones sin aprobación exigida | 0 |
| Satisfacción sobre utilidad | Secundaria; nunca sustituye métricas anteriores |

## Prototipo no-code previsto

El prototipo debe añadir una vista «Explicar esta ejecución» sobre capacidades existentes, no crear un producto paralelo. Mostrará:

- propósito y resultado de la ejecución;
- línea temporal de identidad, consulta, evidencia, decisión, aprobación y acción;
- documentos y versiones con acceso al original autorizado;
- controles de seguridad aplicados y denegaciones;
- cambios posteriores que puedan afectar la vigencia;
- exportación de un expediente de auditoría sin contenido innecesario.

Las vistas utilizarán lenguaje operativo y divulgación progresiva. JSON, SQL, hashes completos y trazas técnicas permanecerán en un nivel avanzado o exportación autorizada.

## Decisión final

| Resultado | Acción |
|---|---|
| Cumple puerta de problema y métricas del piloto | `CONTINUAR` con roadmap y ficha actualizada a `VALIDADA` |
| Problema existe pero se compra como complemento | `REFORMULAR` como capa de evidencia interoperable |
| Interés sin coste, prioridad, patrocinador o piloto | Mantener `NO_VALIDADA`; no ampliar |
| Alternativas actuales resuelven adecuadamente el problema | `DESCARTAR` y documentar aprendizaje |

Toda decisión debe enlazar notas anonimizadas, métricas reproducibles, limitaciones y responsable. Ninguna decisión automática sustituye la autorización humana de producto, seguridad y cumplimiento.
