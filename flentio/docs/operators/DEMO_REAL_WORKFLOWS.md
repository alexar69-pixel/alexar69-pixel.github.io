# Flujos reales del entorno demo

## Alcance y garantías

El arranque demo provisiona tres flujos ejecutables bajo la categoría **Demo verificable**. Sus entradas son sintéticas y versionadas para que el resultado sea repetible, pero las reglas, bifurcaciones y salidas son procesadas por el motor real de Flentio.

No usan conectores externos, no generan efectos fuera del laboratorio y no presentan respuestas simuladas como operaciones reales. Cada nodo muestra su nota funcional y el contrato de salida esperado. Tras ejecutar, el JSON real permite contrastar el resultado.

## 1. Clasificar solicitud por importe

Resultado esperado: `{"decision":"REVISION_HUMANA_REQUERIDA"}`.

| Paso | Entrada | Operación real | Salida clara |
|---|---|---|---|
| 1. Entrada controlada | Ninguna | Carga `DEMO-IMPORTE-001`, importe `1250` EUR | `caseId`, `amount`, `currency` |
| 2. Evaluar umbral | `amount=1250` | Compara numéricamente `amount > 1000` | `branch="true"`, `condition_met=true` |
| 3A. Revisión humana | Rama `true` | Asigna la decisión | `decision="REVISION_HUMANA_REQUERIDA"` |
| 3B. Tramitación estándar | Rama `false` | No se ejecuta con la entrada versionada | `decision="TRAMITACION_ESTANDAR"` |

## 2. Validar expediente y evidencias

Resultado esperado: `{"validation":"EXPEDIENTE_VALIDADO"}`.

| Paso | Entrada | Operación real | Salida clara |
|---|---|---|---|
| 1. Cargar expediente | Ninguna | Carga consentimiento `PRESENTE` y 3 evidencias | `requestId`, `consent`, `evidenceCount` |
| 2. Validar consentimiento | `consent="PRESENTE"` | Comprueba igualdad con `PRESENTE` | Rama `true` |
| 3. Comprobar evidencias | `evidenceCount=3` | Comprueba `evidenceCount > 0` | Rama `true` |
| Salida válida | Ambas reglas verdaderas | Asigna el resultado | `validation="EXPEDIENTE_VALIDADO"` |
| Salidas de rechazo | Alguna regla falsa | Cierre seguro según la regla fallida | `RECHAZADO_SIN_CONSENTIMIENTO` o `RECHAZADO_SIN_EVIDENCIAS` |

## 3. Respuesta segura ante servicio no configurado

Resultado esperado: HTTP `503` y cuerpo `{"code":"NO_CONFIGURADO","service":"crm-demo","retryable":false}`.

| Paso | Entrada | Operación real | Salida clara |
|---|---|---|---|
| 1. Leer estado | Ninguna | Carga `NO_CONFIGURADO` | `service`, `operationalStatus` |
| 2. Comprobar operación | Estado declarado | Compara con `OPERATIVO` | Rama `false` |
| 3B. No disponible | Rama `false` | Prepara una respuesta, sin invocar el CRM | HTTP `503`, código `NO_CONFIGURADO` |

## Cómo comprobarlos

1. Inicia el entorno con `scripts/start-demo.ps1 -Rebuild`.
2. Accede con las credenciales definidas en `.env.demo`.
3. Abre **Workflows** y filtra por **Demo verificable** o busca `DEMO REAL`.
4. Revisa las etiquetas numeradas y el bloque **Salida de este paso**.
5. Ejecuta el flujo e inspecciona el JSON real de cada nodo recorrido.
6. Contrasta la salida con el contrato visible y las tablas anteriores.

El bootstrap restaura las definiciones canónicas en cada arranque. Para experimentar sin perder cambios, duplica primero el flujo.
