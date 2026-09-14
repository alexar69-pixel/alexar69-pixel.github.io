# Propuesta de Valor Flentio — Argumentario Comercial

> Documento para equipos de ventas y business development. Debe leerse junto a
> [Seguridad de Flentio](../SECURITY.md) y la
> [revisión documental vigente](../audits/DOCUMENTATION_REVIEW_2026-09-05.md).
> Una implementación local o test con datos sintéticos no acredita una
> integración del cliente, capacidad productiva ni homologación bancaria.

---

## ¿Qué es Flentio?

**Flentio** es una plataforma empresarial de automatización No-Code, conocimiento institucional (RAG) e investigación operacional gobernada, diseñada específicamente para entornos bancarios y de infraestructura crítica.

No es:
- Un constructor genérico de agentes IA (hay decenas en el mercado)
- Un chatbot bancario
- Una plataforma de automatización de propósito general
- Una herramienta de análisis de modelos IA

Es:
- Una **capa de control y evidencia sobre procesos agentic bancarios**
- Un **motor de excepciones operativas gobernadas** con revisión humana integrada
- Un **repositorio de conocimiento institucional trazable** con citas verificables
- Una **plataforma de investigación de incidentes** con propuestas auditables

---

## Los 3 diferenciadores centrales

### 1. Revisión humana estructurada — no opcional

La IA de Flentio nunca ejecuta acciones de impacto sin aprobación humana. Cada propuesta incluye:
- La evidencia usada para generarla (con citas de fuentes reales)
- Las contradicciones detectadas automáticamente
- El alcance exacto y el rollback
- La identidad del aprobador y el timestamp (auditoría inmutable)

**Por qué importa:** El BCE y la EBA exigen responsabilidad humana clara sobre decisiones de IA. Los bancos que despliegan agentes autónomos enfrentan el riesgo regulatorio de no poder reconstruir quién autorizó qué.

### 2. Conocimiento institucional trazable (RAG con evidencia)

Flentio indexa los documentos de la organización y los hace consultables con citas verificables:
- Ninguna respuesta se da sin citar el documento fuente
- Si la información no está indexada, el sistema responde `SIN_DATOS` — no inventa
- Los documentos tienen trazabilidad completa: origen, versión, quién los aprobó
- El acceso es por rol y organización (RLS) — un usuario nunca ve documentos de otro tenant

**Por qué importa:** Los reguladores exigen que las decisiones basadas en políticas internas puedan reconstruirse. Un sistema que "resume documentos" sin citar no cumple con ese requisito.

### 3. No-Code real — no un editor de código disfrazado

Flentio está diseñado para que analistas y operativos sin perfil técnico puedan:
- Crear flujos de automatización completos desde lenguaje natural
- Conectar servicios corporativos (email, Slack, bases de datos, APIs) sin escribir código
- Configurar integraciones mediante formularios dedicados con validación visual
- Consultar el estado de cualquier integración sin interpretar JSON o logs

### 4. Ecosistema de Extensibilidad Gobernada (OpenAPI Importer, Zapier Bridge, SDK y Sidecar)

> Estado actual: el importador OpenAPI necesita autenticación/RBAC antes de
> exponerse. Las rutas SDK y Sidecar heredadas devuelven resultados marcados
> como simulados y son `NO_DISPONIBLE` para uso operativo. Los puntos siguientes
> describen el objetivo del producto, no una disponibilidad productiva actual.

Flentio ofrece máxima adaptabilidad tecnológica sin perder el control ni exigir reescribir plataformas:
- **Importador OpenAPI/Swagger/Postman**: Genera nodos No-Code en segundos cargando cualquier especificación JSON de API externa.
- **Zapier & Make Governed Bridge**: integración por validar con cada proveedor;
  el tamaño del catálogo externo no equivale a conectores Flentio validados.
- **Flentio Client SDK & Custom Code Sandbox**: Permite a desarrolladores pro-code escribir scripts custom en V8 sandbox (`$dlp`, `$vault`, `$http`) o integrar `@flentio/sdk` en proyectos LangChain.
- **Perfiles de Gobierno Dinámicos (`EXPRESS` vs `BANKING_ENTERPRISE`)**: Permite ajustar el rigor operativo según las necesidades reguladoras del cliente.
- **Governance Sidecar Middleware**: contrato objetivo `NO_VALIDADO`; el endpoint
  heredado actual no autentica ni persiste el comportamiento descrito.

**Por qué importa:** Resuelve la fricción de integración, permite convivir con software bancario existente y ofrece flexibilidad tanto a usuarios No-Code como a ingenieros Pro-Code.

---

## Casos de uso verificados (estado del sistema real)

> Los siguientes casos de uso están implementados y probados con datos sintéticos. La homologación con datos bancarios reales de clientes requiere un proyecto de implementación.

### Investigación de incidentes operativos
- **Estado:** `IMPLEMENTADO · NO_BANCARIO_HOMOLOGADO`
- El sistema correlaciona eventos de múltiples fuentes, detecta hipótesis de causa y genera propuestas de remediación con evidencia
- La propuesta es siempre `SUGGEST/NOT_EXECUTED` — requiere aprobación humana con motivo
- Tiene un modo de demostración con 5 escenarios sintéticos (`/demo`)

### Automatización de alertas de monitorización
- **Estado:** `IMPLEMENTADO · DEPENDENCIA_CLIENTE`
- Webhooks de Grafana/Dynatrace → clasificación IA → enrutamiento → notificación Slack/email
- Los nodos de integración con Grafana y Dynatrace están implementados, pero requieren configuración del endpoint real del cliente

### Consulta de normativa y procedimientos internos
- **Estado:** `IMPLEMENTADO · VALIDACIÓN_LOCAL`; proveedores e infraestructura productiva son `DEPENDENCIA_CLIENTE`
- RAG sobre documentos en formatos PDF, DOCX, Markdown, HTML
- Respuesta con cita de fuente — nunca responde sin evidencia documental
- Soporte para Google Drive, SharePoint/OneDrive como fuentes incrementales

### Procesamiento de documentos con IA
- **Estado:** `IMPLEMENTADO · DEPENDENCIA_CLIENTE`; no hay homologación productiva ni OCR
- Extracción de campos de facturas, contratos y formularios mediante nodos de IA
- Clasificación automática y enrutamiento según contenido

### Generación de flujos por lenguaje natural
- **Estado:** `IMPLEMENTADO · DEPENDENCIA_CLIENTE`; requiere proveedor real configurado
- El usuario describe el flujo en texto libre → la IA genera el grafo de nodos
- Si la descripción es ambigua, el sistema hace preguntas con chips de respuesta rápida

---

## Integración con el ecosistema bancario

Integraciones implementadas (requieren configuración del endpoint del cliente):

| Categoría | Integraciones |
|---|---|
| **ITSM** | Jira Cloud, BMC Helix |
| **Observabilidad** | Grafana, Prometheus, Dynatrace, Datadog, OpenTelemetry, Splunk |
| **Colaboración** | Gmail, Slack, Microsoft Teams, Telegram |
| **Cloud** | AWS CloudWatch, Azure Monitor, Google Cloud Operations |
| **Almacenamiento doc.** | Google Drive, SharePoint/OneDrive |
| **Importación de APIs** | OpenAPI 3.0, Swagger 2.0, Postman Collections, HTTP APIs |
| **Integraciones SaaS** | Zapier & Make Governed Bridge (5.000+ conectores externos bajo DLP) |
| **SDK & Middleware** | Flentio Client SDK (`@flentio/sdk`), Sidecar REST API, Custom Code Sandbox |
| **Bases de datos** | PostgreSQL (nativo), HTTP APIs |
| **Modelos IA** | Gemini, OpenAI GPT-4, Ollama (local), NVIDIA NIM |
| **Seguridad** | ClamAV (análisis de malware en documentos), DLP (enmascaramiento PII) |

---

## Lo que Flentio NO hace (honestidad comercial)

Ser transparente sobre los límites es esencial para construir confianza:

| Lo que el cliente podría asumir | La realidad |
|---|---|
| "¿Puede conectarse a mi sistema X inmediatamente?" | Las integraciones requieren que el cliente proporcione el endpoint y las credenciales. Sin esos datos, el estado es `NO_CONFIGURADO` |
| "¿Está homologado por [regulador bancario]?" | El sistema está diseñado con principios de cumplimiento bancario. La homologación formal con datos reales del cliente es responsabilidad del cliente y su equipo de cumplimiento |
| "¿La IA ejecuta las acciones automáticamente?" | La IA propone — el humano autoriza. La ejecución autónoma sin revisión humana está bloqueada por diseño |
| "¿Puedo migrar mis datos de n8n/Zapier?" | Flentio cuenta con un nodo **Zapier & Make Governed Bridge** y un **Importador OpenAPI**, pero los diagramas visuales propietarios de otras herramientas requieren configuración inicial |
| "¿Funciona en producción bancaria inmediatamente?" | El laboratorio de demostración funciona con datos sintéticos. Un despliegue productivo requiere un proyecto de implementación con el equipo de infraestructura del cliente |

---

## Comparativa de posicionamiento

| Capacidad | Flentio | n8n | Zapier | Make | NVIDIA NIM |
|---|---|---|---|---|---|
| No-Code real para analistas bancarios | ✅ | ⚠️ Técnico | ✅ | ✅ | ❌ |
| RAG con citas verificables | ✅ | ❌ | ❌ | ❌ | ⚠️ Parcial |
| Revisión humana integrada (obligatoria) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Importador OpenAPI/Swagger & Zapier Bridge | ✅ | ⚠️ | N/A | N/A | ❌ |
| Pro-Code Sandbox & Flentio Client SDK | ✅ | ✅ | ❌ | ❌ | ⚠️ |
| Perfiles de gobierno dinámicos (`EXPRESS`/`BANKING`) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Governance Sidecar para plataformas bancarias | ✅ | ❌ | ❌ | ❌ | ❌ |
| Auditoría inmutable por tenant | ✅ | ⚠️ | ❌ | ⚠️ | ❌ |
| Aislamiento multi-tenant (RLS) | ✅ | ⚠️ | ⚠️ | ⚠️ | N/A |
| On-premise / nube privada | ✅ | ✅ | ❌ | ❌ | ✅ |
| Diseñado para regulación bancaria | ✅ | ❌ | ❌ | ❌ | ⚠️ |

> ⚠️ = Capacidad parcial o requiere configuración adicional significativa  
> Esta comparativa refleja información pública disponible en agosto de 2026. Puede desactualizarse.

---

## Objeciones frecuentes y respuestas

**"Necesitamos conectarnos a miles de aplicaciones SaaS (Zapier / Make)"**  
Flentio incluye el **Importador Dinámico OpenAPI/Swagger/Postman** para crear nodos No-Code en segundos y el **Zapier & Make Governed Bridge**, que permite ejecutar escenarios de Zapier/Make aplicando filtrado DLP saliente y trazabilidad WORM.

**"Nuestros programadores prefieren LangChain/Python o n8n"**  
Flentio ofrece el **Custom Code Sandbox V8** (`$dlp`, `$vault`, `$http`) dentro de los workflows No-Code y expone la biblioteca **Flentio Client SDK** y API REST para que desarrolladores Python/LangChain utilicen los motores de gobierno y RAG con citas de Flentio en su propio código.

**"No somos un banco regulado, ¿es Flentio demasiado rígido?"**  
Flentio dispone de **Perfiles de Gobierno Dinámicos** (`EXPRESS` vs `BANKING_ENTERPRISE`). El perfil `EXPRESS` desactiva las dobles aprobaciones obligatorias de 2 personas para procesos no regulados, conservando la velocidad de iteración con aislamiento RLS y DLP.

**"Ya tenemos una plataforma de agentes interna (BBVA Blue / JPMorgan LLM Suite)"**  
No es necesario reemplazar la plataforma central. Flentio actúa como un **Governance Sidecar / Middleware** vía API REST que inspecciona prompts con DLP, provee evidencias RAG con citas y registra audiciones WORM directamente para la suite existente del banco.

**"¿Tenemos que cambiar toda nuestra infraestructura?"**
No. Flentio se integra con la infraestructura existente (Jira, Grafana, sistemas de email, bases de datos) a través de sus conectores. El desplegado es Docker/Kubernetes sobre la infraestructura del cliente.

---

## Estado de validación de mercado

> Las hipótesis siguientes son `NO_VALIDADAS` — son oportunidades identificadas mediante investigación documental, no confirmadas por clientes.

| Oportunidad | Estado de validación |
|---|---|
| Gestión de excepciones operativas gobernadas | `NO_VALIDADA` — hipótesis P1 de investigación de mercado |
| Cambio regulatorio → control → proceso | `NO_VALIDADA` — hipótesis P1 |
| Autoridad delegada para agentes financieros | `NO_VALIDADA` — hipótesis P1 |
| Validación continua de agentes con replay | `NO_VALIDADA` — hipótesis P2 |

Para más detalle sobre el análisis de mercado: [Paisaje de mercado IA bancario 2026](../strategy/BANKING_AI_MARKET_LANDSCAPE_2026.md)

---

## Material de demostración

El laboratorio de demostración puede arrancarse en cualquier entorno con Docker:

```powershell
./scripts/start-demo.ps1 -Rebuild
```

Accede a `http://localhost:3000/demo`. Muestra 5 escenarios de investigación operacional con datos sintéticos, claramente marcados como `NO BANCARIO · NO PRODUCCIÓN`.

Guion de la demo de 10 minutos: [docs/operators/DEMO_PRODUCT_GUIDE.md](../operators/DEMO_PRODUCT_GUIDE.md)
