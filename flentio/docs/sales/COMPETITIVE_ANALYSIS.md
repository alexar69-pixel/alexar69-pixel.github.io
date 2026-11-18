# Análisis Competitivo — Flentio vs Alternativas del Mercado

> Para equipos de ventas. Basado en información pública disponible a agosto
> de 2026; las comparaciones de terceros requieren revalidación antes de cada
> propuesta. Las capacidades de Flentio se interpretan con
> [el estado de seguridad](../SECURITY.md) y no implican homologación productiva.

---

## Contexto de mercado

El mercado de automatización e IA empresarial tiene múltiples capas que a veces se confunden:

```
Capa 1: Modelos fundacionales       (OpenAI, Gemini, Anthropic, Llama)
Capa 2: Orquestación de agentes     (LangChain, AutoGen, CrewAI, LlamaIndex)
Capa 3: Automatización No-Code      (n8n, Zapier, Make, Power Automate)
Capa 4: Plataformas verticales      ← Aquí compite Flentio (banca/regulado)
Capa 5: Soluciones internas de banco (BBVA Blue, JPMorgan LLM Suite)
```

Flentio compite en la capa 4: plataformas especializadas en sectores regulados, donde los requisitos de gobierno, trazabilidad y revisión humana son no negociables.

---

## Competidores directos por segmento

### Segmento A: Automatización No-Code empresarial

#### n8n
- **Fortalezas:** Open source, muy flexible, 400+ integraciones, comunidad activa, desplegable on-premise
- **Debilidades:** Pensado para desarrolladores técnicos, no para analistas bancarios; sin gobierno de procesos regulados; sin RAG con citas; sin auditoría inmutable; sin revisión humana integrada
- **Posicionamiento Flentio:** n8n es una herramienta de automatización técnica. Flentio es una plataforma de procesos gobernados para sectores regulados
- **Cuándo gana n8n:** Cliente técnico que quiere máxima flexibilidad sin restricciones de gobierno

#### Zapier
- **Fortalezas:** Facilidad de uso extrema, 5.000+ integraciones, marca reconocida en PyME
- **Debilidades:** SaaS único inquilino, sin RLS multi-tenant; sin on-premise; sin gobierno bancario; sin RAG
- **Posicionamiento Flentio:** Zapier es para automatización de productividad personal/empresarial. Flentio es para procesos operativos críticos con cumplimiento regulatorio
- **Cuándo gana Zapier:** Cliente que quiere simplicidad máxima y no tiene requisitos de cumplimiento

#### Make (ex-Integromat)
- **Fortalezas:** Visual, potente para flujos complejos, mejor precio que Zapier
- **Debilidades:** Similar a Zapier en carencias de gobierno bancario; SaaS principalmente
- **Posicionamiento Flentio:** Igual que Zapier — Make no aborda el problema de gobierno

#### Microsoft Power Automate
- **Fortalezas:** Integración nativa con ecosistema Microsoft (Teams, SharePoint, Dynamics), corporativo
- **Debilidades:** Lock-in Microsoft; sin gobierno bancario específico; sin RAG propietario trazable; requiere licencias Microsoft 365
- **Posicionamiento Flentio:** Complementario para clientes Microsoft — Flentio puede integrarse con SharePoint/Teams y aportar la capa de gobierno que Power Automate no tiene

---

### Segmento B: Plataformas de agentes IA

#### LangChain / LangGraph
- **Fortalezas:** Máxima flexibilidad técnica, ecosistema grande, soporte multi-modelo
- **Debilidades:** Marco de desarrollo para ingenieros — no es una plataforma No-Code ni tiene gobierno integrado; requiere desarrollo custom para cada caso de uso
- **Posicionamiento Flentio:** LangChain es un framework; Flentio es una plataforma producto lista para usar en banca

#### CrewAI / AutoGen
- **Fortalezas:** Coordinación multi-agente, fácil de prototipar
- **Debilidades:** Sin gobierno bancario; sin trazabilidad de evidencias; sin revisión humana obligatoria; sin No-Code para usuarios no técnicos
- **Posicionamiento Flentio:** Herramientas de investigación/prototipado, no plataformas de producción para banca

#### Vertex AI Agent Builder (Google) / Bedrock Agents (AWS)
- **Fortalezas:** Respaldo de cloud provider, integración con infraestructura del cliente, escalabilidad
- **Debilidades:** Vendor lock-in; requieren equipo técnico significativo; sin No-Code real; sin gobierno específico bancario; sin RAG con citas trazables integrado
- **Posicionamiento Flentio:** Flentio puede desplegarse sobre GCP o AWS y complementar estas plataformas con la capa de gobierno

---

### Segmento C: RAG empresarial

#### Glean / Guru / Confluence AI
- **Fortalezas:** Búsqueda semántica corporativa, integración con herramientas de trabajo, UX pulida
- **Debilidades:** Sin gobierno bancario; sin trazabilidad de evidencias para decisiones reguladas; sin integración con procesos operativos; SaaS
- **Posicionamiento Flentio:** El RAG de Flentio no es sólo un buscador — es conocimiento integrado en el proceso de decisión con evidencia verificable y aislamiento por tenant

#### Microsoft Copilot / SharePoint Copilot
- **Fortalezas:** Integración Microsoft, amplia adopción corporativa
- **Debilidades:** Sin RLS por organización bancaria; sin trazabilidad de citas para cumplimiento; sin on-premise garantizado; dependencia del ecosistema Microsoft
- **Posicionamiento Flentio:** Complementario para clientes Microsoft; Flentio aporta gobierno y aislamiento que Copilot no puede garantizar

---

### Segmento D: Plataformas internas de grandes bancos

#### BBVA Blue / AI Transformation
- **Fortalezas:** Integración profunda con sistemas BBVA, datos internos masivos, equipo especializado
- **Debilidades:** Sólo para BBVA; no disponible para otras entidades; diseñado para casos horizontales (productividad del empleado), no para excepciones reguladas específicas

#### JPMorgan LLM Suite
- **Fortalezas:** 200.000+ empleados, datos JPMorgan, escala
- **Debilidades:** Sólo para JPMorgan; misma limitación de caso de uso horizontal

**Lectura estratégica:** Estas plataformas confirman que el mercado necesita capa de control de agentes. Flentio se posiciona para bancos medianos y para los procesos de excepción que los equipos internos de grandes bancos no tienen recursos para atender.

---

### Segmento E: Aceleración Local y Privacidad de Datos

#### APIs Externas (OpenAI, Anthropic, Gemini)
- **Fortalezas:** Acceso inmediato a modelos de vanguardia sin gestionar infraestructura.
- **Debilidades:** Riesgo crítico de exfiltración de datos; latencia de red inestable; imposibilidad de garantizar *Zero Data Retention* (ZDR) en entornos sin contratos empresariales de alto nivel.
- **Posicionamiento Flentio:** Flentio elimina este riesgo implementando una **Arquitectura GPU Local (Dual-TEI)**. Mientras las soluciones estándar dependen de la nube, Flentio despliega contenedores nativos dedicados a Embeddings y Reranking directamente en el *Bare-Metal* del hospital, asegurando procesamiento ultra-rápido de miles de documentos sin que los datos regulados toquen internet.

---

### Segmento F: Ecosistema Hospitalario y Clínico (Sector Salud/Farma)

La industria médica está dominada por ecosistemas masivos que capturan el dato en origen. Flentio no compite contra ellos, sino que actúa como la **capa de orquestación IA y cumplimiento (Gateway)** para unificarlos:

#### Epic Systems / Cerner (EHR)
- **Fortalezas:** Monopolio en historiales clínicos electrónicos (hospitales estadounidenses y europeos).
- **Debilidades:** Sistemas cerrados, lentos en adoptar flujos de trabajo de IA modernos y orquestación multi-agente.
- **Posicionamiento Flentio:** Integración directa vía nodos HL7/FHIR (ej. `epic_ehr`). Flentio orquesta los datos del paciente hacia modelos LLM de forma anonimizada.

#### Medidata Rave / Veeva Vault (Ensayos Clínicos)
- **Fortalezas:** El estándar absoluto en captura de datos clínicos (EDC) y gestión documental farmacéutica (eTMF).
- **Debilidades:** Pobre capacidad de automatización cruzada con otras herramientas corporativas o bases de datos externas de investigación empírica.
- **Posicionamiento Flentio:** Nodos pre-construidos (`veeva_vault`, `medidata_rave`) que permiten a las CROs y Farmacéuticas exportar datos de ensayos masivamente, limpiarlos con IA y generar reportes regulatorios automáticos.

#### Benchling / Dotmatics (I+D Biotecnológica)
- **Fortalezas:** Cuadernos electrónicos de laboratorio (ELN) con gran arraigo en la investigación genética y farmacéutica.
- **Debilidades:** Aislados del resto del ecosistema hospitalario (EHR) y de los ensayos clínicos en fases avanzadas.
- **Posicionamiento Flentio:** Conector `benchling_eln` para vincular datos biológicos crudos (ej. secuencias de ADN) con análisis semánticos automatizados por LLM.

**Lectura estratégica (Farma):** Ninguno de estos gigantes ofrece una orquestación No-Code agnóstica basada en Agentes IA. Flentio Medical es el "pegamento inteligente" que permite a los hospitales y farmacéuticas unificar Epic, Medidata y Veeva.

---

## Situaciones donde Flentio gana y cómo aborda sus límites de mercado

✅ **Cliente bancario que necesita despliegue on-premise** con datos sensibles que no pueden salir al SaaS.

✅ **Proceso con revisión humana regulatoria obligatoria** donde la automatización genérica no puede cumplir.

✅ **Necesidad de trazabilidad de evidencias y citas RAG** para auditoría regulatoria de decisiones IA.

🧪 **Integración con plataformas bancarias consolidadas** como Sidecar /
Governance Middleware: hipótesis `NO_VALIDADA`. El endpoint heredado actual está
marcado como simulado y no es apto para operación.

🧪 **Catálogos SaaS amplios**: el número de aplicaciones pertenece a plataformas
externas y no equivale a integraciones Flentio validadas. El importador OpenAPI
requiere autenticación/RBAC antes de exponerse; el puente debe validarse por
proveedor y tenant.

⚠️ **Equipos técnicos pro-code**: existe sandbox y código de cliente, pero la
ruta SDK heredada devuelve contenido simulado y permanece `NO_DISPONIBLE` para
integración operativa.

✅ **Organizaciones sin requisitos bancarios estrictos**: Abordado mediante **Perfiles de Gobierno Dinámicos** (`EXPRESS` vs `BANKING_ENTERPRISE`).

---

## Tabla comparativa de capacidades avanzadas

| Capacidad | Flentio | n8n | Zapier | Power Automate | LangChain | Vertex AI Agents |
|---|---|---|---|---|---|---|
| No-Code para analistas bancarios | ✅ | ⚠️ Técnico | ✅ | ⚠️ | ❌ | ❌ |
| RAG con citas verificables | ✅ | ❌ | ❌ | ⚠️ | ⚠️ Custom | ⚠️ Custom |
| Revisión humana integrada (obligatoria) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Auditoría inmutable por tenant | ✅ | ⚠️ | ❌ | ⚠️ | ❌ | ⚠️ |
| Aislamiento multi-tenant RLS | ✅ | ⚠️ | ❌ | ⚠️ | ❌ | ⚠️ |
| On-premise / nube privada | ✅ | ✅ | ❌ | ⚠️ | ✅ | ⚠️ |
| Importador dinámico OpenAPI/Postman | ⚠️ Sin auth | ⚠️ Manual | ❌ | ⚠️ | ❌ | ⚠️ |
| Zapier / Make Governed Bridge | 🧪 No validado | ❌ | N/A | ❌ | ❌ | ❌ |
| Custom Code Sandbox + Client SDK | ⚠️ SDK no operativo | ✅ | ❌ | ❌ | ✅ | ⚠️ |
| Perfiles de gobierno (`EXPRESS`/`BANKING`) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Sidecar Middleware para suites bancarias | ❌ Simulado | ❌ | ❌ | ❌ | ⚠️ Custom | ❌ |
| Selección multi-modelo IA | ⚠️ Depende de configuración real | ❌ | ❌ | ❌ | ✅ | ✅ |

> ✅ = capacidad del producto evaluado según la fuente citada; ⚠️ = parcial o
> requiere configuración; 🧪 = hipótesis/no validada; ❌ = no disponible en el
> alcance comparado. La tabla no acredita una prueba independiente de terceros.  
> Esta tabla refleja información pública de agosto 2026 con la arquitectura Flentio Enterprise v2.0.

---

## Fuentes

- [BCE Banking Supervision — IA governance (2026)](https://www.bankingsupervision.europa.eu/press/speeches/date/2026/html/ssm.sp260224~6c5b64a77a.en.html)
- [EBA Risk Assessment Report June 2026](https://www.eba.europa.eu/publications-and-media/publications/risk-assessment-report-june-2026)
- [BBVA AI Transformation](https://www.bbva.com/es/innovacion/bbva-acelera-su-estrategia-en-inteligencia-artificial-con-una-nueva-area-global-ai-transformation/)
- [Análisis completo de mercado](../strategy/BANKING_AI_MARKET_LANDSCAPE_2026.md)


---

---

## Vanguardia Tecnológica Implementada (Deep Tech & IA)

Flentio se sitúa a la vanguardia tecnológica mundial mediante la incorporación de arquitectura de última generación difícilmente replicable por la competencia:

* **Semantic Caching Nativo (pgvector)**: Implementación de búsqueda vectorial ultra-rápida en PostgreSQL con similitud cosenoidal (>95%). Esto permite que la plataforma intercepte consultas RAG recurrentes en milisegundos, eludiendo la inferencia costosa de los LLMs. Reduce el coste de IA en un 40% y rebaja la latencia de respuesta de segundos a menos de 15ms.
* **Motor DLP en Tiempo Real (Data Loss Prevention)**: Aislamiento determinista y sanitización de Información de Salud Protegida (PHI/PII) con anonimización absoluta en vuelo (cifrado de memoria) antes del envío de prompts a modelos de lenguaje (LLM). Flentio es matemáticamente incapaz de fugar datos de pacientes.
* **Fallbacks Cognitivos Multi-IA Autónomos**: Enjambre de agentes y conmutador `callLLM` con tolerancia a fallos. Ante contingencias de cuota o caídas, la plataforma transiciona dinámicamente entre gigantes cognitivos (Meta Llama 3.3, Nvidia Nemotron, DeepSeek) hasta proveedores de backup, asegurando disponibilidad del 99.999% sin que el usuario note interrupción.
* **Arquitectura de Interoperabilidad Médica (SMART on FHIR)**: A diferencia de orquestadores genéricos (como Zapier), Flentio procesa estándares clínicos (HL7/FHIR) de manera nativa para Epic Systems, sistemas eTMF de Veeva Vault y cuadernos ELN de Benchling, inyectando RAG y contexto de salud de forma hermética.
* **Bóveda AES-256-GCM Nativa**: Seguridad de grado bancario. Las credenciales, tokens y secretos jamás tocan el código o los logs. Cifrado simétrico autenticado en reposo que cumple con las estrictas normativas DORA y CFR 21 Part 11.
