# Ficha de diferenciación: puerta de calidad de evidencia operacional

## Identificación

- Propuesta: puerta determinista previa al diagnóstico de incidentes.
- Fecha y versión: 02-08-2026, v0.1.
- Estado: `NO_VALIDADA` comercialmente; implementación local en `VALIDACIÓN`.
- Usuarios: SRE, Operaciones, Riesgo Tecnológico y revisores de incidentes.

## Necesidad no cubierta

El usuario ha descrito un proceso donde alertas, cambios, tickets, runbooks y
catálogo están dispersos. El riesgo concreto es sugerir una solución con datos
incompletos, contradictorios o temporalmente incoherentes. Falta medir frecuencia,
tiempo ahorrado y falsos positivos con expedientes bancarios autorizados.

## Mercado y alternativas

| Alternativa actual | Qué resuelve | Carencia pendiente de comprobar | Fuente y fecha |
|---|---|---|---|
| Consolas de observabilidad e ITSM | Consultan señales y tickets | Gobierno conjunto y trazable antes de sugerir | Investigación de mercado pendiente |
| Revisión manual | Aplica conocimiento experto | Coste, consistencia y escala no medidos | Testimonio del usuario, 2026-08-02 |

No se afirma exclusividad. Es obligatorio contrastar el flujo con clientes y
productos actuales antes de comunicar una ventaja comercial.

## Ventaja propuesta de Flentio

Un expediente no-code muestra cobertura, diversidad, incoherencias temporales y
conflictos de versión sin copiar el contenido fuente ni inferir causa. Reutiliza
RLS, clearance, hashes, auditoría y referencias HTTPS. Quedan fuera el diagnóstico,
la decisión humana y cualquier ejecución.

## Defensa legítima frente a réplica

- [x] Integración profunda con procesos autorizados.
- [x] Conocimiento especializado y trazable.
- [x] Controles regulatorios, seguridad y auditoría integrados.
- [x] Automatizaciones compuestas difíciles de coordinar por separado.
- [x] Experiencia no-code sustancialmente superior.

La defensa sólo existiría tras acumular mapeos autorizados, reglas auditables y
evaluaciones humanas por proceso bancario; copiar la pantalla no reproduce eso.

## Validación y métricas

| Hipótesis | Método | Umbral inicial | Resultado | Estado |
|---|---|---|---|---|
| Reduce revisiones con evidencia defectuosa | Comparativa ciega sobre expedientes | >=30% menos devoluciones sin aumentar falsos READY | Pendiente | `NO_VALIDADA` |
| Señala conflictos reales | Etiquetado por dos revisores | precisión >=90% | Pendiente | `NO_VALIDADA` |

Continuar sólo si un dataset autorizado confirma utilidad y no oculta evidencia
relevante. Reformular umbrales con falsos positivos; descartar si no mejora la
revisión humana.

## Riesgos y reversión

Los hashes no prueban veracidad; diversidad de sistemas no implica independencia;
la evidencia fuera de ventana puede seguir siendo relevante. No se persiste una
nueva copia. Reversión: retirar el bloque visual y la evaluación calculada, sin
borrar expedientes, referencias o auditoría.

## Dictamen

- Decisión: `CONTINUAR` sólo en validación técnica y con lenguaje no causal.
- Limitación: no puede comunicarse todavía como ventaja de mercado demostrada.
