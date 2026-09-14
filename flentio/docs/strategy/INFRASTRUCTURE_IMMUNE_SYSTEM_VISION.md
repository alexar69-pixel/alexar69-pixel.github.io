# Visión audaz — sistema inmunitario operativo para infraestructura bancaria

## Estado y ambición

`VISION_NO_VALIDADA`. Flentio evolucionaría desde un orquestador con RAG hacia
un **sistema inmunitario operativo**: observa, recuerda, ensaya, recomienda,
contiene y —sólo cuando existe evidencia suficiente— repara de forma limitada.

No busca sustituir Grafana, Prometheus, OpenTelemetry, Splunk, Dynatrace,
Datadog, Instana, ITSM, CMDB o los motores de automatización del banco. Los
conecta mediante una capa bancaria de causalidad, autoridad, reversibilidad y
evidencia.

El conocimiento privado procede de la documentación y los RAG internos del
cliente. Flentio los consulta de forma federada por defecto y no crea un lago de
conocimiento paralelo. Véase `docs/RAG_CLIENT_KNOWLEDGE_FEDERATION.md`.

La audacia está en anticipar y probar soluciones; la ejecución permanece
limitada por políticas deterministas. DORA exige programas de pruebas de
resiliencia basados en riesgo, corrección de deficiencias y validación interna;
no autoriza autonomía sin control. [Reglamento DORA, arts. 24–25](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX%3A32022R2554)

## Principios

1. **Nunca confiar en una sola alarma.** Métricas, logs, trazas y cambios deben
   compartir identidad semántica. OpenTelemetry ofrece señales y convenciones
   comunes que pueden servir de lingua franca. [OpenTelemetry Signals](https://opentelemetry.io/docs/concepts/signals/), [Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/general/)
2. **Correlación no es causalidad.** Un cambio reciente genera una hipótesis,
   no una condena.
3. **Primero replay; después realidad.** Una solución debe superar incidentes
   históricos, gemelo/sandbox y canary antes de obtener más autoridad.
4. **Cada acción lleva freno.** Stop condition, blast radius, timeout, rollback
   y credencial efímera. AWS FIS utiliza objetivos, roles y condiciones de
   parada; Flentio aplicaría el mismo patrón incluso fuera de AWS. [AWS FIS](https://docs.aws.amazon.com/fis/latest/userguide/experiment-templates.html)
5. **Verificar negocio, no sólo CPU.** Una gráfica verde no demuestra que un
   pago, cierre o conciliación se haya recuperado.
6. **Aprender sólo de resultados autorizados.** Un cierre automático o una
   coincidencia temporal no se convierte en conocimiento validado.

## Doce capacidades diferenciales

### 1. Radar de cambios causales

Superpone la alerta con despliegues, configuración, flags, IaC, certificados,
secretos rotados, dependencias, cambios de esquema y ventanas operativas. En vez
de mostrar una lista cronológica, construye una **cadena de propagación** y
expone evidencia a favor y en contra de cada cambio.

**Resultado:** «El despliegue X precede al error, sólo afecta a la versión Y y
la traza termina en Z; confianza 0,78. Falta comprobar la dependencia W».

### 2. Memoria episódica de incidentes

Convierte incidentes resueltos en casos versionados: síntomas, topología,
cambios, hipótesis descartadas, causa humana confirmada, acción, resultado y
rollback. Busca precedentes por trayectoria del fallo, no sólo por similitud de
texto.

**Defensa:** el corpus de decisiones y resultados del propio banco, aislado por
tenant, mejora con el uso autorizado.

### 3. Gemelo de incidentes por replay

Reconstruye un incidente con telemetría anonimizada, configuración declarativa
y dependencias simuladas en un entorno controlado. Prueba varias líneas de
acción sin tocar producción y compara cuál habría restaurado los SLO sin causar
daño lateral.

**Límite:** no se denominará gemelo fiel hasta medir cobertura y divergencia.

### 4. Compilador de runbooks

Transforma un runbook humano en una máquina de estados verificable:

```text
precondiciones → observaciones → decisión → acción tipada
              → condición de éxito → estabilización → rollback/escalado
```

El compilador detecta pasos ambiguos, permisos inexistentes, comandos sin
rollback, documentación caducada y contradicciones con arquitectura/CMDB. No
ejecuta texto libre.

### 5. Firewall de remediación

Intercepta cada acción propuesta y la evalúa contra identidad, entorno,
criticidad, freeze, cut-off, segregación de funciones, radio de impacto, estado
del incidente y riesgo acumulado. El LLM puede proponer; el firewall decide si
la acción está prohibida, requiere aprobación o pertenece a una allowlist.

### 6. Canary de reparación

Aplica la acción primero al mínimo conjunto representativo: una instancia,
partición, cola no crítica o porcentaje de tráfico. Compara contra un control y
detiene automáticamente si empeora cualquier guardrail. Después aumenta el
alcance por etapas, nunca de golpe.

### 7. Rollback predictivo

Antes de actuar, estima si el rollback es técnicamente posible **ahora**:
artefacto anterior disponible, esquema compatible, datos no destruidos,
dependencias vigentes, credenciales válidas y tiempo dentro del RTO. Si el
rollback es ficticio, bloquea la ejecución.

### 8. Detector de monitor mentiroso

Busca tres clases diferentes:

- **falso positivo:** falla sonda/regla, servicio sano;
- **falso negativo:** transacción sintética o señal de negocio falla aunque el
  dashboard esté verde;
- **monitor ciego:** dejó de llegar telemetría y el cero se interpreta como
  salud.

Usa sondas externas, freshness, cardinalidad, trazas y KPI bancario para evitar
confundir ausencia de datos con disponibilidad.

### 9. Cartografía dinámica del radio de impacto

Une topología técnica con productos, procesos, países, horarios, clientes
afectados y obligaciones. Permite priorizar dos alertas técnicamente iguales de
forma distinta si una atraviesa pagos en cut-off y otra un entorno interno.

### 10. Pasaporte de resiliencia por aplicación

Cada aplicación mantiene un expediente vivo:

- owner y criticidad;
- dependencias y hosting NextGen/AWS/legado;
- SLO, error budget, RTO/RPO;
- runbooks vigentes y acciones autorizadas;
- última prueba de rollback, restore y failover;
- deuda de observabilidad;
- incidentes y regresiones pendientes.

Una aplicación sin evidencias no aparece «verde»; aparece `RESILIENCIA_NO_DEMOSTRADA`.

### 11. Mercado interno de soluciones verificadas

Los equipos publican patrones de remediación reutilizables con versión, alcance,
pruebas, métricas y dueño. Flentio recomienda sólo patrones compatibles y
promueve una solución desde `CANDIDATA` hasta `AUTORIZADA_R1/R2` mediante
evidencia acumulada, no votos ni texto generado.

### 12. Game days generados desde incidentes reales

Los incidentes relevantes producen automáticamente candidatos a escenarios de
resiliencia. Un humano los aprueba; después se ejecutan en sandbox o
preproducción con objetivos, stop conditions y reporte. Así, el conocimiento no
queda enterrado en el postmortem.

## Ideas especialmente audaces

### Vacuna operativa

Tras un incidente confirmado, Flentio crea cuatro artefactos candidatos:

1. nueva regla para detección temprana;
2. prueba de regresión para el pipeline;
3. escenario de game day;
4. actualización propuesta del runbook.

Ninguno se activa sin revisión. La «vacuna» se considera eficaz sólo si detecta
el replay y no introduce falsos positivos sobre una muestra acordada.

### Modo cuarentena

En lugar de reiniciar o apagar, puede proponer aislar de forma reversible una
versión, ruta, consumidor o integración: retirar tráfico, pausar consumo sin
perder mensajes, congelar despliegues o degradar una función no esencial. Es
preferible contener con radio limitado que «curar» sin certeza.

### Presupuesto de autonomía

Cada aplicación recibe un presupuesto dinámico basado en criticidad, cobertura
de pruebas, calidad de runbooks, éxito histórico y error budget. Un incidente o
rollback fallido reduce inmediatamente la autonomía; meses de evidencia positiva
permiten sólo incrementos pequeños y revocables.

### Tribunal de hipótesis

Varios analizadores independientes —cambios, topología, precedentes, RAG y
telemetría— presentan evidencia. Un agregador no elige por mayoría: busca
contradicciones, fuentes compartidas y evidencia faltante. Si todos derivan de
la misma alarma, no cuentan como confirmaciones independientes.

### Línea temporal contrafactual

Para cada propuesta responde: «si ésta fuera la causa, ¿qué otras señales
deberíamos observar?». Flentio consulta esas señales antes de recomendar. Esto
reduce diagnósticos plausibles pero falsos.

## Niveles de autonomía ganada

| Nivel | Capacidad | Requisito mínimo |
|---|---|---|
| A0 | Recopilar y explicar | Fuentes de sólo lectura y RLS |
| A1 | Recomendar comprobaciones | Evidencia citada y abstención |
| A2 | Proponer acción tipada | Runbook vigente, riesgo y rollback |
| A3 | Ejecutar R1 en preproducción | Replay, aprobación y credencial efímera |
| A4 | Canary R1 productivo | Historial positivo, stop conditions y guardrails |
| A5 | Contención R2 preautorizada | Doble control y resultado de negocio verificable |

No se propone autonomía para acciones irreversibles, ledger, pérdida de datos,
desactivación de controles o cambios masivos.

## Priorización

| Capacidad | Valor | Diferenciación | Riesgo | Secuencia |
|---|---:|---:|---:|---|
| Detector de monitor mentiroso | 5 | 4 | 1 | P1 |
| Radar de cambios causales | 5 | 4 | 1 | P1 |
| Memoria episódica | 5 | 5 | 1 | P1 |
| Compilador de runbooks | 5 | 5 | 2 | P1 |
| Firewall de remediación | 5 | 5 | 3 | P1 |
| Pasaporte de resiliencia | 4 | 5 | 1 | P2 |
| Replay/gemelo de incidentes | 5 | 5 | 3 | P2 |
| Canary y rollback predictivo | 5 | 4 | 4 | P3 |
| Contención automática limitada | 5 | 5 | 5 | P4 |

## Producto inicial recomendado

### Flentio Incident Lab

Una mesa no-code que recibe una alerta y muestra cinco paneles:

1. **Qué sabemos:** señales confirmadas y freshness.
2. **Qué cambió:** siete días, correlaciones y contradicciones.
3. **Qué ocurrió antes:** precedentes con resultado validado.
4. **Qué permiten los runbooks:** pasos vigentes, owner y límites.
5. **Qué haría Flentio:** comprobaciones y líneas de acción ordenadas.

El primer producto no ejecuta. Su éxito sería reducir el tiempo de investigación
y aumentar la calidad/reproducibilidad del diagnóstico. Esta interfaz alimenta
los activos necesarios para autonomía futura sin asumirla desde el principio.

## Métricas que importan

- tiempo hasta hipótesis útil y tiempo hasta recuperación;
- porcentaje de falsos positivos/falsos negativos de monitor detectados;
- hipótesis aceptadas y descartadas por operadores;
- contradicciones descubiertas antes de ejecutar;
- runbooks incompletos o caducados identificados;
- rollbacks realmente viables frente a declarados;
- reincidencia de la misma clase de fallo;
- daño secundario y acciones innecesarias evitadas;
- cobertura de procesos críticos por pasaporte y replay;
- mejora del KPI bancario afectado, no sólo del dashboard.

## Barrera legítima de réplica

La ventaja acumulativa surgiría de la unión entre:

- grafo servicio–proceso–control–producto;
- memoria de incidentes con causas y resultados confirmados;
- runbooks compilados y probados;
- replays y game days específicos;
- autoridad no-code por contexto bancario;
- historial de canaries, rollbacks y falsos diagnósticos;
- adaptadores neutrales a NextGen, AWS y herramientas existentes.

Un competidor puede copiar la interfaz; no puede copiar legalmente la experiencia
operativa, evidencia y confianza acumuladas por una entidad.

## Condición de realidad

Todas estas capacidades continúan `NO_VALIDADA` o `NO_CONFIGURADA`. No deben
aparecer como operativas hasta disponer de conectores reales, dataset autorizado,
pruebas reproducibles, revisión humana y evidencias de seguridad. La visión se
descartará si el banco obtiene el mismo control de sus herramientas actuales sin
una capa adicional o si Flentio aumenta complejidad y MTTR.

> **Nota Estratégica:** Esta visión técnica se ha traducido a una propuesta de diferenciación comercial estructurada. Ver: [Ficha de Diferenciación: Auto-Healing](DIFFERENTIATION_AUTO_HEALING.md).
