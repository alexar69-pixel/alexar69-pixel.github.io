# Ficha de diferenciación de producto - Sistema Inmunitario de Infraestructura (Auto-Healing)

> Esta ficha es obligatoria antes de implementar una solución o evolución relevante. Debe distinguir hechos verificados, inferencias e hipótesis. Una hipótesis pendiente nunca se presenta como capacidad operativa ni como ventaja demostrada.

## Identificación

- Propuesta: Flujos de Remediación Autónoma con Aprobación Asíncrona (Auto-Healing HIL).
- Responsable: Arquitectura
- Fecha y versión: Septiembre 2026, v1.0
- Estado: `NO_VALIDADA`
- Usuarios y proceso afectados: SREs (Site Reliability Engineers), DevOps, Operadores Médicos e Informáticos (ITSM).

## Necesidad no cubierta

- Problema concreto: Las plataformas actuales de monitorización (Datadog, Dynatrace, BMC Helix) generan miles de alertas. Un humano debe leerlas, buscar el manual de operaciones y ejecutar scripts manualmente para mitigar el fallo. 
- Frecuencia, impacto y coste actual: Crítica. El Mean Time To Resolve (MTTR) en incidentes hospitalarios o bancarios cuesta decenas de miles de dólares por minuto de inactividad.
- Evidencia aportada por usuarios o datos operativos: Tiempos de inactividad medidos en la banca por la lentitud en la mitigación de errores de configuración.
- Por qué merece resolverse ahora: El Auto-Healing es el "santo grial" de las operaciones. Si Flentio puede pre-redactar la solución y ejecutarla tras un clic humano, el valor de la plataforma se multiplica x10.

## Mercado y alternativas

| Alternativa actual | Qué resuelve | Carencia comprobada | Fuente y fecha |
|---|---|---|---|
| PagerDuty / Opsgenie | Enrutamiento de alertas a guardias | Solo avisan, no solucionan de forma inteligente basada en conocimiento no estructurado. | Industria, 2026 |
| Ansible / Rundeck | Automatización de scripts | Requieren codificación manual estricta por cada posible fallo. No infieren la solución leyendo los logs y el manual. | Industria, 2026 |

- Búsqueda realizada y alcance geográfico/sectorial: Mercado global SRE y SOC.
- Información que todavía falta: Tasa de éxito del modelo LLM generando scripts de Bash/PowerShell correctos en base a manuales RAG.
- Riesgo de que la necesidad ya esté cubierta: Medio. Existen plataformas AIOps, pero no orientadas a la abstracción visual No-Code con trazabilidad inmutable.

## Ventaja propuesta de Flentio

- Resultado diferencial esperado: Flentio consumirá el log de error, usará el RAG para leer el "Runbook de Incidencias" interno, generará el comando de resolución y lo enviará al teléfono del SRE con dos botones: "Aprobar y Ejecutar" o "Rechazar".
- Flujo no-code para conseguirlo: Nuevo nodo de "Ejecución de Código en Sandbox" y un nuevo disparador (Trigger) interactivo asíncrono para aprobación.
- Capacidades verificadas que reutiliza: Base de conocimiento RAG, notificaciones Slack/Email, auditoría.
- Capacidades nuevas necesarias: Motor de ejecución de scripts en Sandbox seguro (MicroVMs / Contenedores efímeros).
- Qué queda expresamente fuera de alcance: Ejecución 100% autónoma en producción (Zero-Touch) sin revisión humana inicial. En entornos altamente regulados, la intervención humana es mandatoria (Human-in-the-Loop).

## Defensa legítima frente a réplica

Marque y justifique únicamente las defensas reales:

- [X] Integración profunda con procesos autorizados.
- [X] Controles regulatorios, seguridad y auditoría integrados.
- [X] Automatizaciones compuestas difíciles de coordinar por separado.

Explique por qué un competidor competente no podría reproducir el mismo resultado rápidamente sólo copiando la interfaz:
La generación de código por IA (Copilot) es común, pero la **ejecución orquestada en un entorno hiper-seguro** (Sandboxing), unida a una firma electrónica que deja rastro WORM (Write-Once Read-Many) para cumplir con el Banco Central Europeo o la FDA, es una barrera arquitectónica inmensa.

## Validación y métricas

| Hipótesis | Método de validación | Métrica y umbral | Resultado | Estado |
|---|---|---|---|---|
| Flentio puede sugerir el script correcto basándose en un log y un manual en PDF, y ejecutarlo de forma segura. | Simulación de incidente web (Nginx) y remediación en Sandbox. | 80% de scripts generados resuelven el incidente sin intervención de código manual. | - | `NO_VALIDADA` |

- Criterio para continuar: Validación técnica del aislamiento del entorno de Sandbox.
- Criterio para modificar: Si los scripts generados son inestables, se limitará a sugerir comandos de solo lectura (diagnóstico) en lugar de escritura (reparación).
- Criterio para descartar: Riesgo crítico de seguridad si la IA intenta ejecutar comandos destructivos (`rm -rf`) que no puedan ser bloqueados por el validador estático.

## Riesgos y obligaciones

- Riesgos para cliente, seguridad, privacidad y regulación: Destrucción de infraestructura si un script malicioso/alucinado es aprobado por accidente.
- Dependencias externas y autorizaciones humanas: Aprobación humana explícita y obligatoria para todos los flujos de "Escritura".
- Portabilidad e interoperabilidad: Compatibilidad con SSH, AWS CLI y Kubernetes API.
- Cómo se evita dependencia artificial o retención abusiva: Los scripts generados son legibles y el cliente puede exportarlos.
- Reversión si la hipótesis no se confirma: El nodo Auto-Healing solo generará recomendaciones en texto para el operador, sin ejecutar código.

## Dictamen

- Decisión: `CONTINUAR`
- Evidencia que sustenta la decisión: Fuerte presión competitiva hacia el concepto de "AIOps" real.
- Limitaciones y afirmaciones que no pueden comunicarse todavía: No afirmar que la plataforma es "completamente autónoma". Siempre posicionarla como "Soporte Amplificado".
