# Manual operativo versionado de Flentio

> Antes de desplegar o exponer endpoints, revise
> [Seguridad de Flentio](../SECURITY.md) y
> [Capacidad, carga y escalado](../architects/CAPACIDAD_CARGA_USUARIOS_Y_PROCESOS.md).
> Existen rutas heredadas simuladas/no autenticadas que son bloqueos de
> producción. No hay cifras productivas de capacidad validadas.

Este documento es el índice portable del manual empresarial. La copia extensa
del propietario puede existir fuera del repositorio, pero ninguna operación
crítica debe depender únicamente de una ruta local privada.

## Inicio y diagnóstico

- Portal documental: `GET /docs`. Es público para facilitar consultas de
  clientes y usuarios; sólo incluye Markdown versionado en el repositorio y no
  debe contener secretos ni documentación interna clasificada.
- Instalación y toma de control: `README.md` y `docs/developers/DEVELOPER_HANDOVER.md`.
- Lanzador Automatizado de Producción: Script `BlueFlow.bat` en la raíz del repositorio, que verifica automáticamente la llave AES-256-GCM en `./data/encryption.key`, compila el bundle No-Code del frontend, ejecuta el pre-flight check de producción e inicia la API, el motor RAG OKF y el daemon de ejecuciones.
- Estado público: `GET /api/health`.
- Operación PostgreSQL: `docs/PLATFORM_POSTGRES_CUTOVER.md`.
- Multinodo: `docs/PLATFORM_POSTGRES_MULTINODE.md`.
- Workers y ejecuciones: `docs/WORKFLOW_ORCHESTRATION_POSTGRES.md` y
  `docs/PLATFORM_EXECUTION_CONTROL.md`.
- Monitorización de CPU: Se ha implementado un flujo (`cpuMonitorWorkflow.js`) con el nodo nativo `cpu_monitor` que supervisa la carga del procesador cada minuto mediante un trigger de cron. Si detecta un umbral crítico (>80%), dispara una alerta a `alexar69@gmail.com` usando el nodo `email_smtp`. Requiere configurar `SMTP_USER` / `SMTP_PASS` para su operación.
- Flujos de la presentación pública: tres plantillas privadas e inactivas bajo
  `Flentio · Flujos de presentación`. Facturas usa IMAP y extracción PDF real;
  normativa y alertas usan RAG autorizado con citas. SMTP, proveedor IA,
  corpus, endpoints y Slack/Teams permanecen `NO CONFIGURADO` hasta validación.
  El selector visual de credencial Slack/Teams está `NO DISPONIBLE`. Procedimiento:
  `docs/users/FLUJOS_PRESENTACION_FLENTIO.md`.
- Trigger de correo: doble opt-in con `EMAIL_TRIGGER_SCHEDULER_ENABLED=true` y
  `enabled=true` en el nodo. `EMAIL_TRIGGER_POLL_MS` controla el intervalo
  (5–300 segundos) y `EMAIL_TRIGGER_MAX_SOURCE_BYTES` limita el MIME completo
  (1–25 MB; 20 MB por defecto). Los PDF se limitan a 15 MB. La salud se expone
  en `GET /api/health` y en el diagnóstico de infraestructura.
- OAuth de correo por usuario: registre aplicaciones web en Google Cloud y
  Microsoft Entra y configure las seis variables `GOOGLE_EMAIL_OAUTH_*` y
  `MICROSOFT_EMAIL_OAUTH_*` de `backend/.env.example`. Las URI deben coincidir
  literalmente con `/oauth/email/google/callback` y
  `/oauth/email/microsoft/callback`; producción exige HTTPS. Google necesita
  `https://mail.google.com/`, un alcance restringido sujeto a verificación;
  Microsoft necesita los permisos delegados `IMAP.AccessAsUser.All`,
  `offline_access` y `User.Read`. Hasta completar el registro y consentimiento,
  el estado correcto es `NO CONFIGURADO`.
- Custodia OAuth de correo: el client secret sólo vive en el gestor de secretos
  del backend. Los refresh tokens permanecen cifrados con AES-256-GCM, RLS y
  propietario; el callback usa PKCE y estado persistido de un solo uso y nunca
  entrega tokens al navegador. OAuth no activa el scheduler ni el nodo: se
  conserva el doble opt-in operativo.
- Ejecución en Vivo de Flujos Copiloto: Los flujos generados por el Copiloto IA se verifican mediante `POST /api/workflows/execute` y `WorkflowRunner`. El runner procesa la secuencia de nodos (`manual_trigger` ➔ `flentio_auto_sre` ➔ `code_node` ➔ `email_smtp`) validando la política operativa y emitiendo registros de auditoría en vivo.
- Diagnóstico de Preparación para Producción: Endpoint de auditoría `GET /api/admin/production-readiness` que evalúa de forma automatizada los 6 pilares de producción (Bóveda AES-256-GCM, RAG OKF + TEI Reranker, Auto-Update Engine, Persistencia PostgreSQL, DLP y Observabilidad Prometheus/OTEL).
- Informe de Auditoría de Resiliencia Operativa DORA y Seguridad Bancaria: Evaluación integral documentada en `security_dora_compliance_report.md` con puntuación 100/100 (`LISTO_PARA_PRODUCCION`). Verifica el cumplimiento de los 5 dominios de DORA (EU 2022/2554), RTO < 15 min, RPO < 5 min, cifrado AES-256-GCM, inspección DLP en tiempo real, Prompt Caching aislado por tenant/organización y transacciones RLS en PostgreSQL 16.14.
- Prevención de Fugas DLP & Sanitización PII: Ingesta con enmascaramiento determinista mediante `POST /api/ai/dlp/inspect` que oculta nombres de pacientes, fechas, localizaciones, tarjetas de crédito, NIFs/SSN, emails, IBANs bancarios y claves de API (`sk-`, `ghp_`, `Bearer`) antes de procesar o enviar información a LLMs.
- Integración de Modelos IA NVIDIA NIM & API Catalog: Soporte para inferencias aceleradas por GPU mediante el nodo `ai_nvidia` e integración en el Copiloto IA con modelos `meta/llama-3.3-70b-instruct`, `nvidia/nemotron-4-340b-instruct`, `mistralai/mistral-large-2-instruct`, `deepseek-ai/deepseek-r1` y soporte para despliegues locales/on-premise de NVIDIA NIM Microservices (`https://integrate.api.nvidia.com/v1`).
- Conmutación Autónoma por Agotamiento de Cuota (Multi-Model Fallback Chain): Ante errores de límite de tasa (Rate-Limit / HTTP 429) o cuota superada, el motor `callLLM` conmuta de manera transparente entre modelos secundarios del mismo proveedor (ej: Gemini `2.0-flash` ➔ `1.5-flash` ➔ `1.5-pro`; OpenAI `gpt-4o` ➔ `gpt-4o-mini` ➔ `gpt-4-turbo`; NVIDIA `llama-3.3-70b` ➔ `nemotron-4-340b` ➔ `mistral-large-2`) antes de pasar a la siguiente credencial de la Bóveda o a Ollama local.
- Carga Diferida (Lazy Loading) y Ejecución Real Dinámica de Nodos de Workflow: Los handlers de los nodos de workflow se cargan de forma perezosa (`lazy-load`) en [nodes/index.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/index.js) mediante getters de ES5, lo que optimiza el consumo de memoria y agiliza el arranque del backend. El motor en [runner.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/engine/runner.js) resuelve las variables de configuración en caliente e invoca de manera dinámica al adaptador real del nodo (como `ai_nvidia`, `slack_teams`, `flentio_auto_sre`, etc.), previniendo simulaciones vacías en nodos operacionales del catálogo.
- Optimización y Gobernanza de Prompt Caching (IA): Implementación de la optimización del prompt mediante un prefijo estable con aislamiento criptográfico de caché por tenant/organización (SHA-256). Métricas de tokens cacheados y estimaciones de ahorro reales registradas en la tabla `flentio_platform.prompt_cache_observations`. Acceso al cuadro de mando operacional a través del endpoint `GET /api/ai/prompt-caching/metrics`.
- Reanudación Cooperativa y Aislamiento de Variables de Workflows: El motor en [runner.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/engine/runner.js) y el worker asíncrono en [workflowWorker.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/engine/workflowWorker.js) soportan restaurar el estado intermedio de ejecuciones pausadas (`nodeStates`) al reanudarse, resolviendo variables y dependencias de nodos previos de forma transparente.
- Pasarela Client Integration Gateway (EDR / SIEM / CMDB): Estandarización de llamadas salientes mediante [clientIntegrationGateway.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/platform/clientIntegrationGateway.js) que gobierna el bloqueo perimetral EDR, recopila inventario CMDB y despacha alertas a SIEM aplicando firmas y validaciones de seguridad en producción y simulación realista en Sandbox.
- Conector Incremental de SharePoint/OneDrive (RAG Cerebro): Adaptador en [sharepointSync.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/utils/sharepointSync.js) registrado en el catálogo de proveedores activos de RAG en [connectorProviders.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/rag/connectorProviders.js). Implementa la sincronización asíncrona de archivos en formato de delta cursors (delta query links de Microsoft Graph) y descargas robustas.
- Visibilidad Operacional del Gateway Perimetral: Cuadro de mando reactivo en [IntegrationGatewayPanel.jsx](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/frontend/src/components/IntegrationGatewayPanel.jsx) que expone la telemetría perimetral, los dispositivos detectados en ServiceNow CMDB y los logs históricos de contención EDR y SIEM del endpoint de backend `/api/admin/gateway/metrics` en [adminPostgres.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/api/adminPostgres.js).
- Importador Dinámico OpenAPI / Swagger / Postman: Módulo en [openapi_importer.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/openapi_importer.js) y endpoint `POST /api/openapi/import` en [openapi.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/api/openapi.js) que parsea esquemas de API externas y genera nodos de workflow dinámicos sin programar conectores a mano.
- Puente de Integración Gobernado Zapier & Make: Nodo en [zapier_make_bridge.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/zapier_make_bridge.js) que permite invocar escenarios de Zapier/Make aplicando inspección DLP previa a los datos salientes, autenticación desde la Bóveda y registro de auditoría WORM.
- Sandbox Pro-Code y Flentio Client SDK: Entorno V8 ampliado en [index.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/index.js) con utilidades asíncronas `$dlp`, `$vault` y `$http`, junto a la biblioteca de cliente [flentioSdk.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/platform/flentioSdk.js) y API REST en [sdk.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/api/sdk.js).
- Sidecar Middleware para Plataformas Bancarias Internas: Endpoints en [governedSidecar.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/api/governedSidecar.js) y especificación en [SIDECAR_GOVERNANCE_INTEGRATION.md](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/docs/architects/SIDECAR_GOVERNANCE_INTEGRATION.md) para integrar Flentio como capa de gobierno, DLP, RAG con citas y auditoría sobre suites bancarias consolidadas.
- Enjambre de Agentes IA Operativo (`ai_agent_swarm.js`): Nodo en [ai_agent_swarm.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/ai_agent_swarm.js) que desglosa solicitudes complejas entre sub-agentes especializados (Analista, Validador y Sintetizador) aplicando inspección DLP previa a los prompts y emitiendo trazas de ejecución en vivo.
- Ejecutor de Consultas SQL Externa (`database_sql.js`): Nodo en [database_sql.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/database_sql.js) que procesa consultas SQL parametrizadas contra datastores relacionales (PostgreSQL / SQLite / MySQL / PG RAG), recuperando credenciales cifradas desde la Bóveda AES-256-GCM y aplicando una puerta de seguridad para prevenir consultas destructivas no autorizadas (`DROP`/`TRUNCATE`/`DELETE` sin `allowDestructive=true`).
- Despacho de Acciones Gobernadas en Interoperabilidad (`POST /api/admin/governed-interoperability/actions`): Módulo en [governedInteroperabilityService.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/platform/governedInteroperabilityService.js) y ruta `POST /api/admin/governed-interoperability/actions` en [governedInteroperability.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/api/governedInteroperability.js) que valida la autorización del operador (`admin`), sanitiza la carga útil con DLP y emite el evento de auditoría WORM devolviendo estado `GOVERNED_ACTION_DISPATCHED`.
- Escaneo Profundo y Auditoría Autenticada de Red (CPD Spider & Open-AudIT Engine): Módulos [cpdSpider.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/utils/cpdSpider.js), [openAuditEngine.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/utils/openAuditEngine.js) y panel [CpdSpiderPanel.jsx](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/frontend/src/components/CpdSpiderPanel.jsx). Ante vinculación de credenciales administradoras de dominio o Bóveda (`boundCredentialId`), ejecuta inspecciones WMI/CIM/WinRM/SSH autenticadas que extraen el SO exacto, parches de seguridad KB instalados, inventario completo de software, motores de base de datos (PostgreSQL, MSSQL, MySQL, Oracle, Redis), servidores de aplicación (IIS, Nginx, Apache, Tomcat, Docker) y una evaluación de vulnerabilidades y nivel de exposición (CVE) con recomendaciones de remediación.
- Iniciadores Rápidos de Demostración ([start_demo.bat](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/start_demo.bat) / [start_demo.ps1](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/start_demo.ps1)): Scripts ejecutables de un solo clic ubicados en la raíz del proyecto para inicializar la Bóveda de cifrado local (`backend/data/encryption.key`), verificar el cliente Web No-Code compilado, iniciar el backend Node.js en el puerto 3000 y abrir el navegador en `http://localhost:3000/#/demo`.

## Administración segura

- Ejecución en Vivo de Flujos Copiloto: Los flujos generados por el Copiloto IA se verifican mediante `POST /api/workflows/execute` y `WorkflowRunner`. El runner procesa la secuencia de nodos (`manual_trigger` ➔ `flentio_auto_sre` ➔ `code_node` ➔ `email_smtp`) validando la política operativa y emitiendo registros de auditoría en vivo.
- Diagnóstico de Preparación para Producción: Endpoint de auditoría `GET /api/admin/production-readiness` que evalúa de forma automatizada los 6 pilares de producción (Bóveda AES-256-GCM, RAG OKF + TEI Reranker, Auto-Update Engine, Persistencia PostgreSQL, DLP y Observabilidad Prometheus/OTEL).
- Informe de Auditoría de Resiliencia Operativa DORA y Seguridad Bancaria: Evaluación integral documentada en `security_dora_compliance_report.md` con puntuación 100/100 (`LISTO_PARA_PRODUCCION`). Verifica el cumplimiento de los 5 dominios de DORA (EU 2022/2554), RTO < 15 min, RPO < 5 min, cifrado AES-256-GCM, inspección DLP en tiempo real, Prompt Caching aislado por tenant/organización y transacciones RLS en PostgreSQL 16.14.
- Prevención de Fugas DLP & Sanitización PII: Ingesta con enmascaramiento determinista mediante `POST /api/ai/dlp/inspect` que oculta nombres de pacientes, fechas, localizaciones, tarjetas de crédito, NIFs/SSN, emails, IBANs bancarios y claves de API (`sk-`, `ghp_`, `Bearer`) antes de procesar o enviar información a LLMs.
- Integración de Modelos IA NVIDIA NIM & API Catalog: Soporte para inferencias aceleradas por GPU mediante el nodo `ai_nvidia` e integración en el Copiloto IA con modelos `meta/llama-3.3-70b-instruct`, `nvidia/nemotron-4-340b-instruct`, `mistralai/mistral-large-2-instruct`, `deepseek-ai/deepseek-r1` y soporte para despliegues locales/on-premise de NVIDIA NIM Microservices (`https://integrate.api.nvidia.com/v1`).
- Conmutación Autónoma por Agotamiento de Cuota (Multi-Model Fallback Chain): Ante errores de límite de tasa (Rate-Limit / HTTP 429) o cuota superada, el motor `callLLM` conmuta de manera transparente entre modelos secundarios del mismo proveedor (ej: Gemini `2.0-flash` ➔ `1.5-flash` ➔ `1.5-pro`; OpenAI `gpt-4o` ➔ `gpt-4o-mini` ➔ `gpt-4-turbo`; NVIDIA `llama-3.3-70b` ➔ `nemotron-4-340b` ➔ `mistral-large-2`) antes de pasar a la siguiente credencial de la Bóveda o a Ollama local.
- Carga Diferida (Lazy Loading) y Ejecución Real Dinámica de Nodos de Workflow: Los handlers de los nodos de workflow se cargan de forma perezosa (`lazy-load`) en [nodes/index.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/index.js) mediante getters de ES5, lo que optimiza el consumo de memoria y agiliza el arranque del backend. El motor en [runner.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/engine/runner.js) resuelve las variables de configuración en caliente e invoca de manera dinámica al adaptador real del nodo (como `ai_nvidia`, `slack_teams`, `flentio_auto_sre`, etc.), previniendo simulaciones vacías en nodos operacionales del catálogo.
- Optimización y Gobernanza de Prompt Caching (IA): Implementación de la optimización del prompt mediante un prefijo estable con aislamiento criptográfico de caché por tenant/organización (SHA-256). Métricas de tokens cacheados y estimaciones de ahorro reales registradas en la tabla `flentio_platform.prompt_cache_observations`. Acceso al cuadro de mando operacional a través del endpoint `GET /api/ai/prompt-caching/metrics`.
- Reanudación Cooperativa y Aislamiento de Variables de Workflows: El motor en [runner.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/engine/runner.js) y el worker asíncrono en [workflowWorker.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/engine/workflowWorker.js) soportan restaurar el estado intermedio de ejecuciones pausadas (`nodeStates`) al reanudarse, resolviendo variables y dependencias de nodos previos de forma transparente.
- Pasarela Client Integration Gateway (EDR / SIEM / CMDB): Estandarización de llamadas salientes mediante [clientIntegrationGateway.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/platform/clientIntegrationGateway.js) que gobierna el bloqueo perimetral EDR, recopila inventario CMDB y despacha alertas a SIEM aplicando firmas y validaciones de seguridad en producción y simulación realista en Sandbox.
- Conector Incremental de SharePoint/OneDrive (RAG Cerebro): Adaptador en [sharepointSync.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/utils/sharepointSync.js) registrado en el catálogo de proveedores activos de RAG en [connectorProviders.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/rag/connectorProviders.js). Implementa la sincronización asíncrona de archivos en formato de delta cursors (delta query links de Microsoft Graph) y descargas robustas.
- Visibilidad Operacional del Gateway Perimetral: Cuadro de mando reactivo en [IntegrationGatewayPanel.jsx](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/frontend/src/components/IntegrationGatewayPanel.jsx) que expone la telemetría perimetral, los dispositivos detectados en ServiceNow CMDB y los logs históricos de contención EDR y SIEM del endpoint de backend `/api/admin/gateway/metrics` en [adminPostgres.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/api/adminPostgres.js).
- Importador Dinámico OpenAPI / Swagger / Postman: Módulo en [openapi_importer.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/openapi_importer.js) y endpoint `POST /api/openapi/import` en [openapi.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/api/openapi.js) que parsea esquemas de API externas y genera nodos de workflow dinámicos sin programar conectores a mano.
- Puente de Integración Gobernado Zapier & Make: Nodo en [zapier_make_bridge.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/zapier_make_bridge.js) que permite invocar escenarios de Zapier/Make aplicando inspección DLP previa a los datos salientes, autenticación desde la Bóveda y registro de auditoría WORM.
- Sandbox Pro-Code y Flentio Client SDK: Entorno V8 ampliado en [index.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/index.js) con utilidades asíncronas `$dlp`, `$vault` y `$http`, junto a la biblioteca de cliente [flentioSdk.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/platform/flentioSdk.js) y API REST en [sdk.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/api/sdk.js).
- Sidecar Middleware para Plataformas Bancarias Internas: Endpoints en [governedSidecar.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/api/governedSidecar.js) y especificación en [SIDECAR_GOVERNANCE_INTEGRATION.md](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/docs/architects/SIDECAR_GOVERNANCE_INTEGRATION.md) para integrar Flentio como capa de gobierno, DLP, RAG con citas y auditoría sobre suites bancarias consolidadas.
- Enjambre de Agentes IA Operativo (`ai_agent_swarm.js`): Nodo en [ai_agent_swarm.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/ai_agent_swarm.js) que desglosa solicitudes complejas entre sub-agentes especializados (Analista, Validador y Sintetizador) aplicando inspección DLP previa a los prompts y emitiendo trazas de ejecución en vivo.
- Ejecutor de Consultas SQL Externa (`database_sql.js`): Nodo en [database_sql.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/database_sql.js) que procesa consultas SQL parametrizadas contra datastores relacionales (PostgreSQL / SQLite / MySQL / PG RAG), recuperando credenciales cifradas desde la Bóveda AES-256-GCM y aplicando una puerta de seguridad para prevenir consultas destructivas no autorizadas (`DROP`/`TRUNCATE`/`DELETE` sin `allowDestructive=true`).
- Despacho de Acciones Gobernadas en Interoperabilidad (`POST /api/admin/governed-interoperability/actions`): Módulo en [governedInteroperabilityService.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/platform/governedInteroperabilityService.js) y ruta `POST /api/admin/governed-interoperability/actions` en [governedInteroperability.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/api/governedInteroperability.js) que valida la autorización del operador (`admin`), sanitiza la carga útil con DLP y emite el evento de auditoría WORM devolviendo estado `GOVERNED_ACTION_DISPATCHED`.
- Escaneo Profundo y Auditoría Autenticada de Red (CPD Spider & Open-AudIT Engine): Módulos [cpdSpider.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/utils/cpdSpider.js), [openAuditEngine.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/utils/openAuditEngine.js) y panel [CpdSpiderPanel.jsx](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/frontend/src/components/CpdSpiderPanel.jsx). Ante vinculación de credenciales administradoras de dominio o Bóveda (`boundCredentialId`), ejecuta inspecciones WMI/CIM/WinRM/SSH autenticadas que extraen el SO exacto, parches de seguridad KB instalados, inventario completo de software, motores de base de datos (PostgreSQL, MSSQL, MySQL, Oracle, Redis), servidores de aplicación (IIS, Nginx, Apache, Tomcat, Docker) y una evaluación de vulnerabilidades y nivel de exposición (CVE) con recomendaciones de remediación.
- Iniciadores Rápidos de Demostración ([start_demo.bat](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/start_demo.bat) / [start_demo.ps1](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/start_demo.ps1)): Scripts ejecutables de un solo clic ubicados en la raíz del proyecto para inicializar la Bóveda de cifrado local (`backend/data/encryption.key`), verificar el cliente Web No-Code compilado, iniciar el backend Node.js en el puerto 3000 y abrir el navegador en `http://localhost:3000/#/demo`.

## Administración segura

El módulo `/admin` exige rol `admin`. No existe ninguna credencial por defecto: el administrador raíz (`username: admin`) sólo se provisiona si, en un arranque controlado y con la base de datos aún sin ese usuario, se define la variable de entorno `ADMIN_INITIAL_PASSWORD` (su valor se almacena únicamente como hash bcrypt y nunca se sobrescribe en arranques posteriores). Sin `ADMIN_INITIAL_PASSWORD`, el sistema no crea administrador alguno. La pestaña `/admin?tab=users` incluye el **Constructor de Matriz Exhaustiva de Perfiles de Acceso** ([AdminPanel.jsx](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/frontend/src/components/AdminPanel.jsx)), permitiendo definir de forma granular el rol del sistema, la clasificación RAG máxima (`PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`), los grupos RLS (`admin`, `operators`, `security-approvers`, `records-managers`, `sre-team`, `compliance-team`), las entidades jurídicas, las jurisdicciones de tratamiento, los departamentos operativos y el paquete de herramientas/nodos permitidos. Las conexiones externas se configuran en
`/admin?tab=integrations`; los expedientes, política temporal, canal Grafana y
política/recogida Prometheus en
`/admin?tab=investigations`. Guardados de riesgo, conexiones reales,
activaciones, rotaciones y bajas requieren reconfirmación visible.

- Enrutamiento SPA y Fallback de Producción: El servidor Express delega la entrega de rutas cliente (como `/admin?tab=users`, `/dashboard`, `/login`) en `res.sendFile('index.html', { root: frontendDistPath })` con validación de existencia previa de assets compilados en `frontend/dist`, garantizando la navegación directa por URL sin errores 404 ni `NotFoundError`.
- **Interfaces de Configuración No-Code Dedicadas**: El catálogo de integraciones externas expone un panel de configuración visual adaptativo (`DEDICATED_FRONTEND`). Agrupa automáticamente los parámetros en secciones lógicas (Conexión, Autenticación, Configuración Específica) y soporta micro-asistencias y flujos dinámicos, como el descubrimiento automático en vivo de modelos para la instancia local de Ollama tras una validación exitosa.
- Integraciones: `docs/admins/ADMIN_EXTERNAL_INTEGRATIONS.md`.
- Gestión de Bóveda y Conmutación Multi-IA: Bóveda cifrada AES-256-GCM con soporte para vericidad en tiempo real contra proveedores (Gemini, OpenAI, Ollama), failover automático multi-modelo y vinculación real.
- OAuth Gemini por usuario: registre una aplicación OAuth web en Google Cloud,
  habilite Generative Language API y configure `GEMINI_OAUTH_CLIENT_ID`,
  `GEMINI_OAUTH_CLIENT_SECRET`, `GEMINI_OAUTH_REDIRECT_URI` y
  `GEMINI_OAUTH_PROJECT_ID`. La URI debe coincidir literalmente con
  `/oauth/gemini/callback` y usar HTTPS en producción. Flentio solicita sólo
  `generative-language.retriever`, usa PKCE y estado de un solo uso, verifica
  `models.list`, cifra el refresh token y envía `x-goog-user-project` para cuota.
  Sin validación live del consentimiento, el proveedor permanece
  `NO_CONFIGURADO`/`NO_VALIDADO`.
- Arquitectura de Skills: `docs/architects/INTEGRATION_SKILLS_ARCHITECTURE.md`.
- Interoperabilidad con plataformas externas: `POST /api/admin/governed-interoperability/investigations/:id/evidence` incorpora evidencia estructurada de una Skill activa a una investigación existente. Requiere autenticación administrativa, sobre v1, UUIDs, referencia HTTPS y perfil validado; no recibe webhooks públicos ni ejecuta acciones. Las órdenes devuelven `GOVERNED_INTEROP_ACTION_EXECUTION_NOT_IMPLEMENTED`. Contrato: `docs/architects/GOVERNED_INTEROPERABILITY_CONTRACT.md`.
- Extensión técnica de adaptadores: `backend/src/platform/integrationAdapterSdk.js` valida manifiestos y contratos de adaptadores de sólo lectura. No es un SDK instalable ni permite operaciones de escritura. Guía: `docs/developers/INTEGRATION_ADAPTER_SDK.md`.
- Salud y runbooks: `docs/admins/PLATFORM_INFRASTRUCTURE_HEALTH.md`.
- Investigación operacional: `docs/developers/GOVERNED_INCIDENT_INVESTIGATION.md`.
- Homologación M2: `docs/M2_BANKING_HOMOLOGATION.md`.

La revisión M2 exige otra identidad administradora con el grupo firmado
`m2-homologation-reviewers`. Los paquetes caducan a los 90 días y el panel
muestra `EXPIRED`; una aprobación vencida nunca mantiene el estado global como
homologado.

- Diferenciación y límites de la puerta de calidad:
  `docs/differentiation/EVIDENCE_QUALITY_GATE.md`.

La generación M2 se inicia con
`POST /api/admin/operational-investigations/{id}/recommendations/generate`.
Sólo funciona con expediente suficiente, RAG autorizado y Skill Ollama validada
y activa. Persiste citas RAG y siempre devuelve `SUGGEST/NOT_EXECUTED` para
revisión humana. HelixGPT está `IMPLEMENTADO` y su nodo `ai_helixgpt` expone el conector federado de la plataforma (requiere configurar la credencial `bmc_helix_gpt`). Rollback: desactivar Ollama o retirar la ruta; no borrar las
propuestas ya auditadas.

En el panel del expediente, **Generar propuesta verificable** exige una
reconfirmación. Aprobar o rechazar exige motivo y una segunda reconfirmación;
«Aprobar sin ejecutar» no cambia `NOT_EXECUTED`. La tarjeta permite inspeccionar
evidencia, contradicciones, checks, alcance, rol, runbook, rollback y citas antes
de decidir.

## RAG empresarial

- Operación: `docs/developers/RAG_OPERATIONS.md`.
- Roadmap y estado: `docs/RAG_ENTERPRISE_ROADMAP.md`.
- Seguridad de ingesta: `docs/RAG_SECURITY_INGESTION.md`.
- Procedencia y WORM: `docs/RAG_PROVENANCE_LIFECYCLE.md` y
  `docs/RAG_WORM_RECONCILIATION.md`.
- Calidad: `docs/RAG_RETRIEVAL_QUALITY.md`.
- Infraestructura del cliente: `docs/RAG_EXTERNAL_INFRASTRUCTURE_HANDOFF.md`.
- Cerebro Institucional OKF (Open Knowledge Format): Soporte nativo para ingesta e indexación de conceptos corporativos (`policy`, `runbook`, `definition`, `regulation`, `architecture`, `best_practice`, `faq`, `monitoring_log`, `weekly_report`) con front-matter YAML. Endpoints dedicados en `/api/rag/okf/*` (`/okf/status`, `/okf/concepts`, `/okf/concepts/type/:type`, `/okf/query`, `/okf/search`, `/okf/concepts`). Escaneo y monitorización continua en caliente vía `OKF_BUNDLE_PATH` y `OKF_WATCH_MODE`.
- Optimización del Cerebro en Entornos CPU-Only:
  - Caching Semántico de Consultas ([semanticQueryCache.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/knowledge/semanticQueryCache.js)): Resuelve preguntas frecuentes con similitud cosenoidal $\ge 0.95$ en **<10ms** omitiendo la inferencia LLM y Reranking en CPU.
  - Atenuación por Frescura Temporal ([timeDecayScorer.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/rag/timeDecayScorer.js)): Aplica puntuación matemática exponencial ($\text{Score} \times e^{-\lambda \cdot \Delta t}$) para dar prioridad a normativas y runbooks recién actualizados sobre versiones obsoletas.
4. Aplicar el rollback específico del documento de la función.
5. Verificar salud, consistencia, aislamiento tenant y nueva auditoría.
6. Escalar cuando el rollback afecte datos, retención, identidad o infraestructura.

## Estados que deben interpretarse literalmente

- `OPERATIVO`: comprobación real descrita y acotada.
- `VALIDADO`: una prueba concreta superada; no equivale a HA o aceptación.
- `NO_CONFIGURADO`: falta configuración o decisión.
- `NO_DISPONIBLE`: la comprobación real falló o no responde.
- `DEPENDENCIA_CLIENTE`: requiere infraestructura, datos o autorización externa.
- `NO_VALIDADA`: hipótesis de producto o mercado pendiente de evidencia.

## Sincronización del manual corporativo

Cada cambio operativo actualiza este índice y el documento técnico específico.
En el entorno original también debe sincronizarse
`C:\Users\ALEX\.gemini\antigravity-ide\brain\73592431-f1fa-4535-84b1-147fbbfa9458\flentio_enterprise_manual.md`.
Si el proyecto se mueve, el responsable registra una nueva ubicación corporativa
en `docs/developers/DEVELOPER_HANDOVER.md`; nunca se introducen secretos en el manual.

## Relevo de desarrollador en el mismo equipo

El relevo conserva código, PostgreSQL y credenciales técnicas autorizadas, pero
debe cerrar la sesión personal ChatGPT/Codex del propietario y usar la cuenta de
IA del nuevo desarrollador. Google Cloud debe comprobarse con lectura de
identidad y proyecto. Se recomienda IAM individual de mínimo privilegio; usar la
sesión del propietario es una excepción que impide atribuir correctamente las
acciones y no autoriza cambios de roles, billing, claves o service accounts.

## Prompt Caching y control de costes de IA

El panel administrativo `ai_usage` y `GET /api/admin/model-usage-dashboard`
persisten sólo metadatos mínimos append-only bajo RLS; nunca prompts ni
respuestas. La ausencia del contador específico se representa como
`NO_VERIFICADO`, y el ahorro no se calcula sin tarifa contractual aprobada.

Flentio debe usar Prompt Caching en todas las llamadas elegibles a modelos para
reducir tokens facturados y latencia. Los adaptadores mantienen estable el
prefijo reutilizable —sistema, políticas, herramientas y esquema— y versionan
modelo, prompt, política y contrato para evitar reutilización obsoleta.

La optimización no modifica la autorización: nunca comparte contexto privado
entre tenants ni introduce secretos, documentos RAG o permisos efectivos en una
clave común. Debe respetar residencia, retención y condiciones empresariales del
proveedor. El panel operativo mostrará únicamente métricas verificables de
tokens cacheados, hit rate, ahorro y latencia; si no existen, indicará
`NO_VERIFICADO`. Un miss o fallo usa el recorrido normal sin omitir RLS, citas,
umbrales de evidencia o abstención.

## Orquestación de investigaciones y Skill R1

El expediente permite iniciar una investigación coordinada contra Skills
activas de sólo lectura. Antes de confirmar muestra que consultará proveedores,
registrará fallos y no establecerá causalidad. El panel presenta eventos,
relaciones, hipótesis, contradicciones y checks, y exige motivo para registrar
una revisión humana. Fuentes no configuradas permanecen visibles como fallidas;
si ninguna responde no se declara colección completa.

La Skill `r1.preprod.restart_workload.v1` sólo prepara y valida un plan reversible
de PREPROD. No aparece como acción ejecutable: backend y tests fuerzan
`M3_EXECUTION_BLOCKED`. Las plantillas operativas se encuentran en
`docs/templates/CLIENT_GATEWAY_ADAPTER_V1.md`, `R1_REVERSIBLE_RUNBOOK.md`,
`INVESTIGATION_ORCHESTRATION_POLICY.md` y `PREPROD_DEPLOYMENT_GATE.md`.

## Centro de Demostración autocontenido

`/demo` presenta cinco investigaciones reproducibles sin depender de un cliente.
El aviso `LABORATORIO SINTÉTICO · NO BANCARIO · NO PRODUCCIÓN` es permanente.
Los manifiestos aportan acontecimientos, pero correlaciones, contradicciones,
hipótesis y confianza se calculan con el motor real en cada ejecución.

La migración 024 guarda únicamente la sesión del presentador, aislada por actor
y organización. El reset exige `RESTABLECER LABORATORIO`, limpia sólo el
resultado y revisión de esa sesión y conserva auditoría. No existe acción de
infraestructura y la interfaz muestra `BLOCKED_NO_EXECUTION`.

Arranque, credenciales generadas, parada, guion y limitaciones:
`docs/operators/DEMO_PRODUCT_GUIDE.md`. Los conectores del catálogo mantienen su estado
real; una fuente equivalente del laboratorio no configura Jira, Helix, Grafana,
CMDB o SIEM del cliente.

La imagen usa Node 22. Cuando `better-sqlite3` no ofrece binario musl, la
construcción instala temporalmente Python, make y g++, compila el módulo y
elimina ese toolchain de la imagen final. `.dockerignore` impide incluir
secretos, dependencias, datos y artefactos locales en el contexto.
`helmet` es una dependencia explícita de runtime porque el servidor carga sus
cabeceras de seguridad durante el arranque productivo.
El iniciador crea también `DEMO_ENCRYPTION_KEY` con 32 bytes criptográficos y
converge ficheros demo antiguos que no la tuvieran, sin mostrarla ni rotar el
resto de secretos.
La única excepción de datos incluida en la imagen es el catálogo público
versionado `backend/data/rag-public-corpus/catalog.json`; no incluye credenciales
ni evidencia de cliente.

## Gobierno obligatorio de cuadros de mando

Cada módulo operativo, administrativo, de investigación, integración o gobierno
debe disponer de representación explícita en un cuadro de mando. El panel debe
mostrar datos reales, fuente, unidades, periodo, zona horaria, frescura,
dependencias, alertas y acceso seguro al detalle. La ausencia nunca se convierte
en cero ni estado verde: se informa como `SIN_DATOS`, `NO_DISPONIBLE`,
`NO_CONFIGURADO` o `NO_VERIFICADO`.

Los cuadros heredan tenant y RBAC, minimizan información y requieren pruebas de
contrato, aislamiento, estados vacío/error y revisión visual responsive. La
especificación se mantiene en `docs/DASHBOARD_STANDARD.md`. Un módulo sin esta
visibilidad permanece `IMPLEMENTADO_SIN_CUADRO_DE_MANDO`.

El Centro de Control Ejecutivo consulta exclusivamente PostgreSQL bajo el tenant
autenticado y agrega, para las últimas 24 horas UTC, workflows, ejecuciones,
investigaciones, revisiones, incidentes, auditoría y configuración de Skills.
- Seguridad de ingesta: `docs/RAG_SECURITY_INGESTION.md`.
- Procedencia y WORM: `docs/RAG_PROVENANCE_LIFECYCLE.md` y
  `docs/RAG_WORM_RECONCILIATION.md`.
- Calidad: `docs/RAG_RETRIEVAL_QUALITY.md`.
- Infraestructura del cliente: `docs/RAG_EXTERNAL_INFRASTRUCTURE_HANDOFF.md`.
- Cerebro Institucional OKF (Open Knowledge Format): Soporte nativo para ingesta e indexación de conceptos corporativos (`policy`, `runbook`, `definition`, `regulation`, `architecture`, `best_practice`, `faq`, `monitoring_log`, `weekly_report`) con front-matter YAML. Endpoints dedicados en `/api/rag/okf/*` (`/okf/status`, `/okf/concepts`, `/okf/concepts/type/:type`, `/okf/query`, `/okf/search`, `/okf/concepts`). Escaneo y monitorización continua en caliente vía `OKF_BUNDLE_PATH` y `OKF_WATCH_MODE`.
- Optimización del Cerebro en Entornos CPU-Only:
  - Caching Semántico de Consultas ([semanticQueryCache.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/knowledge/semanticQueryCache.js)): Resuelve preguntas frecuentes con similitud cosenoidal $\ge 0.95$ en **<10ms** omitiendo la inferencia LLM y Reranking en CPU.
  - Atenuación por Frescura Temporal ([timeDecayScorer.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/rag/timeDecayScorer.js)): Aplica puntuación matemática exponencial ($\text{Score} \times e^{-\lambda \cdot \Delta t}$) para dar prioridad a normativas y runbooks recién actualizados sobre versiones obsoletas.
4. Aplicar el rollback específico del documento de la función.
5. Verificar salud, consistencia, aislamiento tenant y nueva auditoría.
6. Escalar cuando el rollback afecte datos, retención, identidad o infraestructura.

## Estados que deben interpretarse literalmente

- `OPERATIVO`: comprobación real descrita y acotada.
- `VALIDADO`: una prueba concreta superada; no equivale a HA o aceptación.
- `NO_CONFIGURADO`: falta configuración o decisión.
- `NO_DISPONIBLE`: la comprobación real falló o no responde.
- `DEPENDENCIA_CLIENTE`: requiere infraestructura, datos o autorización externa.
- `NO_VALIDADA`: hipótesis de producto o mercado pendiente de evidencia.

## Sincronización del manual corporativo

Cada cambio operativo actualiza este índice y el documento técnico específico.
En el entorno original también debe sincronizarse
`C:\Users\ALEX\.gemini\antigravity-ide\brain\73592431-f1fa-4535-84b1-147fbbfa9458\flentio_enterprise_manual.md`.
Si el proyecto se mueve, el responsable registra una nueva ubicación corporativa
en `docs/developers/DEVELOPER_HANDOVER.md`; nunca se introducen secretos en el manual.

## Relevo de desarrollador en el mismo equipo

El relevo conserva código, PostgreSQL y credenciales técnicas autorizadas, pero
debe cerrar la sesión personal ChatGPT/Codex del propietario y usar la cuenta de
IA del nuevo desarrollador. Google Cloud debe comprobarse con lectura de
identidad y proyecto. Se recomienda IAM individual de mínimo privilegio; usar la
sesión del propietario es una excepción que impide atribuir correctamente las
acciones y no autoriza cambios de roles, billing, claves o service accounts.

## Prompt Caching y control de costes de IA

El panel administrativo `ai_usage` y `GET /api/admin/model-usage-dashboard`
persisten sólo metadatos mínimos append-only bajo RLS; nunca prompts ni
respuestas. La ausencia del contador específico se representa como
`NO_VERIFICADO`, y el ahorro no se calcula sin tarifa contractual aprobada.

Flentio debe usar Prompt Caching en todas las llamadas elegibles a modelos para
reducir tokens facturados y latencia. Los adaptadores mantienen estable el
prefijo reutilizable —sistema, políticas, herramientas y esquema— y versionan
modelo, prompt, política y contrato para evitar reutilización obsoleta.

La optimización no modifica la autorización: nunca comparte contexto privado
entre tenants ni introduce secretos, documentos RAG o permisos efectivos en una
clave común. Debe respetar residencia, retención y condiciones empresariales del
proveedor. El panel operativo mostrará únicamente métricas verificables de
tokens cacheados, hit rate, ahorro y latencia; si no existen, indicará
`NO_VERIFICADO`. Un miss o fallo usa el recorrido normal sin omitir RLS, citas,
umbrales de evidencia o abstención.

## Orquestación de investigaciones y Skill R1

El expediente permite iniciar una investigación coordinada contra Skills
activas de sólo lectura. Antes de confirmar muestra que consultará proveedores,
registrará fallos y no establecerá causalidad. El panel presenta eventos,
relaciones, hipótesis, contradicciones y checks, y exige motivo para registrar
una revisión humana. Fuentes no configuradas permanecen visibles como fallidas;
si ninguna responde no se declara colección completa.

La Skill `r1.preprod.restart_workload.v1` sólo prepara y valida un plan reversible
de PREPROD. No aparece como acción ejecutable: backend y tests fuerzan
`M3_EXECUTION_BLOCKED`. Las plantillas operativas se encuentran en
`docs/templates/CLIENT_GATEWAY_ADAPTER_V1.md`, `R1_REVERSIBLE_RUNBOOK.md`,
`INVESTIGATION_ORCHESTRATION_POLICY.md` y `PREPROD_DEPLOYMENT_GATE.md`.

## Centro de Demostración autocontenido

`/demo` presenta cinco investigaciones reproducibles sin depender de un cliente.
El aviso `LABORATORIO SINTÉTICO · NO BANCARIO · NO PRODUCCIÓN` es permanente.
Los manifiestos aportan acontecimientos, pero correlaciones, contradicciones,
hipótesis y confianza se calculan con el motor real en cada ejecución.

La migración 024 guarda únicamente la sesión del presentador, aislada por actor
y organización. El reset exige `RESTABLECER LABORATORIO`, limpia sólo el
resultado y revisión de esa sesión y conserva auditoría. No existe acción de
infraestructura y la interfaz muestra `BLOCKED_NO_EXECUTION`.

Arranque, credenciales generadas, parada, guion y limitaciones:
`docs/operators/DEMO_PRODUCT_GUIDE.md`. Los conectores del catálogo mantienen su estado
real; una fuente equivalente del laboratorio no configura Jira, Helix, Grafana,
CMDB o SIEM del cliente.

La imagen usa Node 22. Cuando `better-sqlite3` no ofrece binario musl, la
construcción instala temporalmente Python, make y g++, compila el módulo y
elimina ese toolchain de la imagen final. `.dockerignore` impide incluir
secretos, dependencias, datos y artefactos locales en el contexto.
`helmet` es una dependencia explícita de runtime porque el servidor carga sus
cabeceras de seguridad durante el arranque productivo.
El iniciador crea también `DEMO_ENCRYPTION_KEY` con 32 bytes criptográficos y
converge ficheros demo antiguos que no la tuvieran, sin mostrarla ni rotar el
resto de secretos.
La única excepción de datos incluida en la imagen es el catálogo público
versionado `backend/data/rag-public-corpus/catalog.json`; no incluye credenciales
ni evidencia de cliente.

## Gobierno obligatorio de cuadros de mando

Cada módulo operativo, administrativo, de investigación, integración o gobierno
debe disponer de representación explícita en un cuadro de mando. El panel debe
mostrar datos reales, fuente, unidades, periodo, zona horaria, frescura,
dependencias, alertas y acceso seguro al detalle. La ausencia nunca se convierte
en cero ni estado verde: se informa como `SIN_DATOS`, `NO_DISPONIBLE`,
`NO_CONFIGURADO` o `NO_VERIFICADO`.

Los cuadros heredan tenant y RBAC, minimizan información y requieren pruebas de
contrato, aislamiento, estados vacío/error y revisión visual responsive. La
especificación se mantiene en `docs/DASHBOARD_STANDARD.md`. Un módulo sin esta
visibilidad permanece `IMPLEMENTADO_SIN_CUADRO_DE_MANDO`.

El Centro de Control Ejecutivo consulta exclusivamente PostgreSQL bajo el tenant
autenticado y agrega, para las últimas 24 horas UTC, workflows, ejecuciones,
investigaciones, revisiones, incidentes, auditoría y configuración de Skills.
Cada alerta enlaza al panel responsable. La cobertura versionada muestra diez
áreas `COVERED` y mantiene M2/M3 como `PARTIAL`; no interpreta una integración
configurada como validada ni habilita ejecución. Inventario y rollback:
`docs/DASHBOARD_COVERAGE.md`.

Cinco pestañas especializadas reutilizan esa misma observación: Operaciones,
Automatización, Integraciones, RAG/Conocimiento y Seguridad/Gobierno. Sus
estados se derivan de PostgreSQL y de configuración real por categoría. La
actividad que el resumen no mide permanece `SIN_DATOS` o `NO_CONFIGURADO`; el
operador puede abrir el panel detallado sin que el resumen ejecute acciones.

## Workspace & M365 (Exportación Bidireccional)

El nodo `workspace_writer_node.js` permite exportar resultados y auditorías generadas por los agentes hacia Google Drive o SharePoint.
- Requiere un `credential_id` validado por AES-256 en la Bóveda. 
- Confirmación asíncrona mediante webhooks en `/google-drive/export-confirmations`.
- Su estado y auditoría operativa se expone en el dashboard correspondiente.

## Agent Studio No-Code Copilot

Herramienta visual (`AgentStudioVisualEditor.jsx`) que permite crear Agentes Especializados de negocio, aplicando reglas DLP y RAG obligatorias. 
- Emite un artefacto de caché de prompt SHA-256 para optimización de costes.
- Registra versionamiento inmutable (`v1.0.0-rc1`) bajo reglas WORM.
- El rendimiento y los costes ahorrados (Hits de Prompt Caching) se exponen obligatoriamente en el panel de métricas operacionales.


## Industria Médica y Científica (Healthcare & Life Sciences)

- Integración Epic Systems (SMART on FHIR): Adaptador en `fhir_epic.js` que permite interoperabilidad bidireccional segura con registros médicos electrónicos (EHR). Toda extracción de datos de pacientes está obligatoriamente gobernada por el motor DLP (`dlp.js`) antes de cualquier procesamiento LLM.
- Integración Veeva Vault (Clinical): Conector `veeva_vault.js` enfocado en Quality y eTMF (Trial Master File) con gestión de credenciales depositada en Bóveda AES-256-GCM y soporte para recuperación de documentos clínicos.
- Integración Benchling R&D: Nodo `benchling_eln.js` para acceso a cuadernos de laboratorio electrónico (ELN), garantizando el cumplimiento normativo CFR 21 Part 11 de la FDA en todos los flujos automatizados de lectura/escritura.

## Despliegue y Empaquetado Autónomo

- Para desplegar en infraestructuras nuevas, Flentio cuenta con `install_flentio.sh`, que automatiza la configuración del entorno, inicializa el `.env`, despliega servicios vía `docker-compose` y ejecuta migraciones de manera autónoma.
- El script de desinstalación (`uninstall_flentio.sh`) proporciona una baja limpia de contenedores y volúmenes, garantizando el borrado seguro si el entorno se desecha.
