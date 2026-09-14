# Ficha de diferenciación — remediación gobernada de incidencias bancarias

## Estado

`NO_VALIDADA` — concepto de producto y protocolo de validación. No existe todavía integración operativa ni capacidad de ejecutar cambios en infraestructura bancaria.

Contrato técnico del recorrido de investigación: [Investigación y líneas de acción para incidencias](../developers/GOVERNED_INCIDENT_INVESTIGATION.md).

Evolución estratégica: [sistema inmunitario operativo](INFRASTRUCTURE_IMMUNE_SYSTEM_VISION.md).

## Necesidad concreta

Los equipos de Operaciones, SRE y soporte reciben alertas de múltiples herramientas. El problema no termina al detectar una anomalía: deben determinar si la alerta es real, identificar servicio y proceso de negocio afectados, revisar cambios recientes, encontrar el procedimiento vigente, comprobar permisos y ventana operativa, ejecutar una acción segura, verificar la recuperación y documentar todo.

La propuesta es que Flentio pueda:

1. recibir una alerta o detectar una inconsistencia en la monitorización;
2. correlacionarla con topología, despliegues, logs, métricas, trazas, CMDB y proceso bancario;
3. construir hipótesis de causa con evidencia y nivel de confianza;
4. recuperar el runbook y controles aplicables;
5. **sugerir** una solución cuando no exista autoridad suficiente;
6. **ejecutar** sólo una acción previamente autorizada, acotada y reversible;
7. comprobar mediante señales independientes si la recuperación fue real;
8. revertir o escalar si empeoran los indicadores;
9. generar el expediente de decisión, ejecución y resultado.

## El mercado ya cubre

- IBM Instana ofrece detección, topología, causa probable, investigación agentic, recomendaciones, generación de Bash/Ansible y catálogo de acciones. [IBM Instana Intelligent Investigation](https://www.ibm.com/products/instana/intelligent-incident-investigation), [documentación de remediación](https://www.ibm.com/docs/en/instana-observability/current?topic=capabilities-intelligent-remediation)
- Splunk ITSI correlaciona alertas en episodios, reduce ruido y permite ejecutar acciones automáticas según políticas. [Splunk Event iQ](https://help.splunk.com/en/splunk-it-service-intelligence/splunk-it-service-intelligence/detect-and-act-on-notable-events/4.21/event-correlation/automate-event-correlation-with-event-iq-in-itsi), [Event Analytics](https://help.splunk.com/en/splunk-it-service-intelligence/splunk-it-service-intelligence/detect-and-act-on-notable-events/5.0/overview/overview-of-event-analytics-in-itsi)
- Plataformas APM/AIOps ya compiten en correlación, RCA, reducción de MTTR, runbooks y auto-remediation. Por tanto, estas capacidades por sí solas no diferencian a Flentio.

Las afirmaciones de resultados de proveedores son comerciales y no equivalen a validación independiente en banca.

## Carencia que se investigará

Hipótesis: las plataformas actuales pueden detectar y automatizar, pero la entidad sigue necesitando una capa neutral que pruebe **si esa remediación concreta estaba permitida y fue correcta en términos técnicos, operativos y bancarios**, especialmente cuando:

- la señal cruza NextGen, AWS, legado, APX, ASO y canales;
- el servicio técnico soporta pagos, cierres, conciliación o cut-offs;
- una acción requiere segregación de funciones o aprobación adaptativa;
- existen varios proveedores de observabilidad y automatización;
- la solución debe funcionar sin entregar control autónomo a un SaaS externo;
- es obligatorio reconstruir quién decidió, qué evidencia vio y qué ocurrió después.

La carencia permanece `NO_VALIDADA`: Instana y otros competidores ya anuncian evidencia, control humano y documentación, por lo que debe probarse una diferencia bancaria específica.

## Ventaja propuesta para Flentio

### Control de decisión, no sustitución del monitor

Flentio no competiría como APM. Consumiría alertas de Splunk, Dynatrace, Datadog, Instana, Prometheus/Grafana o herramientas internas y aplicaría un contrato bancario de remediación:

```text
Señal → expediente → hipótesis → runbook aprobado → autoridad
      → simulación/prechecks → ejecución acotada → verificación
      → éxito, rollback o escalado → evidencia y aprendizaje autorizado
```

### Tres modos obligatorios

| Modo | Comportamiento |
|---|---|
| `OBSERVAR` | Correlaciona y explica; nunca propone comandos ejecutables |
| `SUGERIR` | Presenta solución, evidencia, riesgo, prechecks y rollback; requiere aprobación humana |
| `EJECUTAR` | Sólo usa una acción versionada y preautorizada dentro de límites explícitos |

El modelo de IA nunca eleva el modo ni concede permisos.

## Controles mínimos

Antes de ejecutar:

- servicio, entorno, tenant y criticidad identificados;
- alerta confirmada por señales suficientes;
- correlación con cambios y dependencias;
- runbook firmado, versionado y no caducado;
- acción en allowlist; parámetros validados;
- identidad de workload de propósito limitado;
- ventana, freeze, cut-off y calendario comprobados;
- segregación de funciones y aprobaciones satisfechas;
- blast radius calculado y límite de concurrencia;
- prechecks y condición de rollback definidos;
- evidencia suficiente; en caso contrario, abstención.

Después de ejecutar:

- observar una ventana mínima de estabilización;
- validar métrica técnica y resultado del proceso bancario;
- comprobar ausencia de daño colateral;
- revertir automáticamente sólo si el rollback también está autorizado;
- escalar cuando el resultado sea ambiguo;
- registrar comandos/acciones, parámetros, versiones, aprobaciones y resultados sin secretos.

## Acciones por nivel de riesgo

| Nivel | Ejemplos | Política inicial |
|---|---|---|
| R0, lectura | Consultar health, logs, métricas, despliegues y CMDB | Automática con auditoría |
| R1, reversible y local | Reintentar una sonda, renovar caché no crítica, escalar dentro de límites | Aprobación previa por tipo de acción |
| R2, impacto de servicio | Reiniciar instancia/pod, rollback de despliegue, conmutar dependencia | Aprobación humana contextual y doble verificación |
| R3, datos/transacción | Reprocesar batch, reparar cola, modificar configuración transaccional | Sólo runbook específico, separación de funciones y supervisión |
| R4, irreversible/crítico | Cambios de ledger, pérdida de datos, desactivar controles, acciones masivas | Prohibido para ejecución autónoma |

La clasificación exacta se validará con el banco.

## Ejemplo de caso inicial

### Falso positivo o degradación real en un servicio ASO

1. El monitor emite error de latencia o disponibilidad.
2. Flentio comprueba desde una segunda fuente si falla la sonda, el servicio o una dependencia.
3. Correlaciona despliegues APX, cambios de configuración, saturación y errores aguas abajo.
4. Recupera el runbook correspondiente al servicio, entorno y versión.
5. Si la evidencia indica fallo del monitor, sugiere reparar/reiniciar únicamente la sonda; no toca el servicio bancario.
6. Si existe una regresión de despliegue, propone rollback con impacto y aprobación.
7. Verifica recuperación técnica y una transacción sintética autorizada, sin usar datos reales.
8. Cierra sólo si ambas verificaciones son satisfactorias.

Este caso evita comenzar con reprocesamiento de pagos o acciones sobre datos.

## Barrera legítima de réplica

No será el algoritmo de anomalías. La defensa potencial se acumularía mediante:

- grafo autorizado entre servicio técnico, proceso bancario, producto, control y sistema de registro;
- biblioteca versionada de runbooks con límites NextGen/AWS/APX/ASO;
- historial de incidentes, decisiones humanas y resultados de rollback;
- pruebas de replay específicas por servicio y proceso;
- política no-code de autoridad, cut-offs y segregación de funciones;
- conectores neutrales a múltiples monitores y motores de automatización;
- expedientes reutilizables para postmortem, auditoría y resiliencia operativa.

Estos activos requieren conocimiento operativo y evidencia autorizada acumulada; no crean dependencia artificial.

## Métricas de éxito

- precisión de clasificación: fallo de monitor frente a fallo de servicio;
- precisión top-1/top-3 de causa probable validada por humanos;
- porcentaje de propuestas aceptadas sin modificación;
- MTTA y MTTR frente al proceso actual;
- tasa de abstención correcta;
- tasa de rollback y de remediación fallida;
- incidentes secundarios provocados: objetivo inicial cero;
- porcentaje de expedientes completos;
- reducción de alertas repetidas;
- tiempo de auditoría/postmortem;
- recuperación del KPI bancario, no sólo del KPI técnico.

## Criterios de descarte

La propuesta se reformulará o descartará si:

- el monitor actual ya ofrece los controles bancarios requeridos con menor coste;
- no hay acceso autorizado a telemetría, CMDB, cambios y runbooks;
- no se puede verificar el resultado con una señal independiente;
- los equipos no confían ni usan las recomendaciones;
- la integración incrementa el riesgo o el MTTR;
- no se alcanza una mejora medible frente al proceso actual;
- la entidad no permite ejecutar acciones, y el modo sugerencia tampoco aporta valor suficiente.

## Validación inicial sin riesgo productivo

1. Elegir un servicio no transaccional en preproducción.
2. Recopilar 20–30 incidentes históricos anonimizados o reproducibles.
3. Definir cinco runbooks reales y sus dueños.
4. Ejecutar Flentio sólo en modo `OBSERVAR` y comparar con el diagnóstico humano.
5. Pasar a `SUGERIR` cuando alcance los umbrales acordados.
6. Permitir una acción R1 reversible únicamente en entorno controlado.
7. Realizar game day con fallo de monitor, fallo de servicio, dependencia caída y diagnóstico ambiguo.
8. Presentar evidencia a Operaciones, SRE, Seguridad, Riesgo y Auditoría antes de ampliar alcance.

## Dependencias de la arquitectura BBVA

Para un piloto alineado con el mapa provisional hacen falta:

- fuente de alertas y telemetría autorizada;
- CMDB/topología y ownership;
- historial de cambios y despliegues;
- catálogo ASO/API y eventos;
- procedimiento APX cuando aplique;
- runtime objetivo NextGen o AWS;
- IAM/PAM, bóveda de secretos y aprobaciones;
- motor de automatización existente;
- sistema ITSM y repositorio de runbooks;
- entorno preproductivo y pruebas sintéticas autorizadas.

No se seleccionará proveedor de observabilidad, SIEM o automatización sin autorización humana.
