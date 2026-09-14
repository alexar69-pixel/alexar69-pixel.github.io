# Resumen Ejecutivo — Flentio Platform

> Para la dirección y el C-Suite. Estado real del producto, inversión, posicionamiento estratégico y hoja de ruta. Todos los datos son verificables en el sistema.

---

## ¿Qué es Flentio y por qué existe?

**Flentio** es una plataforma de automatización gobernada, conocimiento institucional (RAG) e investigación operacional diseñada para entornos bancarios y de infraestructura crítica.

**El problema que resuelve:** Los bancos necesitan desplegar IA en procesos operativos críticos, pero los marcos regulatorios (BCE, EBA, DORA) exigen transparencia, responsabilidad humana clara y trazabilidad de evidencias. Las plataformas genéricas de automatización e IA no cubren estos requisitos de gobierno.

**La apuesta diferencial:** Flentio no compite con los asistentes horizontales de empleados ni con los constructores genéricos de agentes — compite por ser la **capa de control y evidencia** sobre procesos agentic bancarios, donde el mercado tiene cobertura incompleta.

---

## Estado del producto — Agosto 2026

### Capacidades operativas verificadas

| Capacidad | Estado |
|---|---|
| Motor No-Code de automatización visual | ✅ OPERATIVO |
| RAG empresarial con citas verificables | ✅ OPERATIVO |
| Investigación de incidentes con IA | ✅ OPERATIVO · `NO_BANCARIO_HOMOLOGADO` |
| Generación de flujos por lenguaje natural | ✅ OPERATIVO |
| Aislamiento multi-tenant (RLS) | ✅ OPERATIVO |
| Auditoría inmutable | ✅ OPERATIVO |
| Motor de workers durables (PostgreSQL) | ✅ OPERATIVO |
| Centro de Control Ejecutivo (dashboards) | ✅ OPERATIVO |
| Laboratorio de demostración autocontenido | ✅ OPERATIVO |

### Capacidades implementadas pendientes de configuración del cliente

| Capacidad | Estado |
|---|---|
| Jira Cloud / BMC Helix | ✅ IMPLEMENTADO · `NO_CONFIGURADO` (requiere endpoint del cliente) |
| Grafana / Prometheus / Dynatrace | ✅ IMPLEMENTADO · `NO_CONFIGURADO` |
| Google Drive / SharePoint conectores | ✅ IMPLEMENTADO · `NO_CONFIGURADO` |
| SIEM corporativo | `DEPENDENCIA_CLIENTE` |
| KMS/HSM en producción | `DEPENDENCIA_CLIENTE` |

### Pendiente de homologación

| Capacidad | Estado |
|---|---|
| Homologación M2 con datos bancarios reales | `NO_HOMOLOGADO` — requiere dataset bancario autorizado |
| Ejecución autónoma M3 (remediación física) | `BLOQUEADO_HASTA_NUEVA_FASE` |

---

## Validez regulatoria — principios de diseño

El sistema está diseñado con los principios exigidos por los reguladores bancarios europeos:

| Exigencia regulatoria | Cómo Flentio la aborda |
|---|---|
| Responsabilidad humana sobre decisiones IA (BCE/SSM) | Toda propuesta de IA es `SUGGEST/NOT_EXECUTED` hasta aprobación humana con motivo |
| Trazabilidad de evidencias (EBA) | Cada respuesta incluye citas de fuente; log inmutable de decisiones |
| Aislamiento de datos por entidad (DORA) | RLS estricto por organización en toda la pila |
| Resiliencia y continuidad (DORA) | Worker durable con PostgreSQL; failover de modelos IA |
| Explicabilidad (BCE/SSM) | Evidencias, contradicciones y checks visibles antes de cada decisión |
| Control de modelos durante todo el ciclo (EBA) | Versionado de prompts, modelos y políticas; métricas de caché y uso |

> **Aviso legal:** El cumplimiento regulatorio formal de una implementación es responsabilidad del cliente y su equipo de cumplimiento. Flentio proporciona los mecanismos técnicos; la homologación regulatoria requiere un proceso adicional.

---

## Posicionamiento estratégico de mercado

Según el análisis de mercado actualizado a agosto 2026 ([fuente](../strategy/BANKING_AI_MARKET_LANDSCAPE_2026.md)):

- **>85% de los bancos supervisados por el BCE ya usa IA** — la adopción es masiva pero el gobierno del proceso aún es débil
- **Los grandes bancos están internalizando la creación de agentes** (BBVA Blue, JPMorgan LLM Suite) — la oportunidad no está en construir el agente, sino en gobernar el proceso
- **Los reguladores señalan como carencias:** calidad/linaje de datos, explicabilidad, responsabilidad humana, resiliencia, concentración de proveedores — todas son áreas donde Flentio aporta

### Oportunidades priorizadas (hipótesis — `NO_VALIDADAS`)

| Oportunidad | Señal de mercado | Estado de validación |
|---|---|---|
| Gestión de excepciones operativas gobernadas | Santander ejecutó pago agentic; BCE exige responsabilidad | `NO_VALIDADA` |
| Cambio regulatorio → control → proceso | Proceso completamente manual en bancos | `NO_VALIDADA` |
| Autoridad delegada para agentes | Reguladores exigen control del ciclo completo | `NO_VALIDADA` |

> Estas oportunidades están identificadas por investigación documental. Deben validarse con entrevistas a operativos bancarios antes de invertir en desarrollo específico.

---

## Arquitectura tecnológica — resumen

| Componente | Tecnología | Estado |
|---|---|---|
| Frontend | React.js SPA, No-Code | ✅ Producción |
| Backend API | Node.js / Express | ✅ Producción |
| Base de datos | PostgreSQL 16 + pgvector + RLS | ✅ Producción |
| Almacenamiento WORM | MinIO / S3 compatible | ✅ Implementado |
| Motor de IA | TEI (vectorización) + LLMs (Gemini, OpenAI, Ollama, NVIDIA) | ✅ Producción |
| Cifrado | AES-256-GCM en reposo; TLS en tránsito | ✅ Producción |
| Despliegue | Docker / Kubernetes | ✅ Producción |

---

## Hoja de ruta — próximos pasos prioritarios

### Inmediato (Q3–Q4 2026)
1. **Conectar infraestructura del cliente** — Jira, Helix, Grafana, SIEM requieren los endpoints reales del primer cliente
2. **Evaluación M2 con dataset bancario** — la evaluación estructural existe; falta el dataset bancario autorizado y revisión independiente
3. **Validación de hipótesis de mercado** — talleres con operativos bancarios para confirmar o descartar las 3 oportunidades P1

### Medio plazo (2027)
4. **Ledger de autoridad delegada** — gestión de qué puede proponer/aprobar/ejecutar un agente según política bancaria
5. **Módulo de gestión de excepciones operativas** — biblioteca de patrones de excepción bancarios con resolución gobernada
6. **Conectores regulatorios** — integración con sistemas GRC y normativa estructurada

---

## Riesgos clave

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Bancos grandes internalizan la capa de control | Media | Alto | Especialización en excepciones/regulación donde los equipos internos no tienen recursos |
| Falta de acceso a infraestructura del cliente para validar integraciones | Alta (actual) | Medio | Los conectores están implementados; el riesgo baja cuando llega el primer cliente real |
| Cambio regulatorio que invalide el diseño actual | Baja | Alto | Diseño basado en principios regulatorios (BCE/EBA/DORA), no en interpretaciones específicas |
| Dependencia de proveedores LLM externos | Media | Medio | Multi-proveedor implementado con fallback automático; soporte para modelos locales (Ollama/NIM) |
| Mercado saturado de "plataformas de agentes" | Alta | Medio | El posicionamiento en gobierno/evidencia/excepciones bancarias es diferencial del constructor genérico |

Para el registro completo de riesgos: [Registro de Riesgos](RISK_REGISTER.md)

---

## Métricas de estado del sistema

Datos verificables del sistema a agosto 2026:

| Métrica | Valor | Fuente |
|---|---|---|
| Tests backend pasados | 246/246 | `npm test` — evidencia fechada, no garantía futura |
| Build frontend | ✅ Sin errores | `npm run build` |
| Nodos del catálogo de automatización | 29 tipos de nodo operativos | Registro de Skills |
| Integraciones implementadas | 29 conectores | Catálogo de Skills |
| Tipos de documento RAG soportados | PDF, DOCX, MD, HTML, TXT | Ingesta real |
| Migraciones de BD aplicadas | 024 (PostgreSQL) | Schema de migrations |

---

*Para consultas sobre implementación, licencia o proyectos piloto, contactar al equipo técnico responsable del producto.*
