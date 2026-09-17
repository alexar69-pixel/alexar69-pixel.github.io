# Continuidad de desarrollo de Flentio

Actualizado: 12-08-2026. Este documento es la fuente de orientación para un nuevo desarrollador.

## Estado resumido

| Área | Estado verificable | Pendiente principal |
|---|---|---|
| Plataforma PostgreSQL | Único datastore operativo; workflows, ejecuciones, credenciales y usuarios en RLS | HA, backup/restore y SLO bancarios |
| Orquestación | Worker durable, cancelación, cron y webhooks con tenant real | Pruebas multinodo y carga productiva |
| RAG F1–F7 | Implementación y evidencias locales documentadas | Infraestructura/aceptación del cliente y proveedores homologados |
| Ecosistema de Arquitectura | OpenAPI Importer, Zapier Bridge, Pro-Code Sandbox & FlentioSdk, Perfiles de Gobierno y Sidecar Middleware | Homologación en entornos del cliente |

La última validación integral obtuvo 538/538 pruebas backend pasando limpiamente (`npm test`), Validador Estático AST de Auto-Healing (`scriptAstSecurityGuard.js`), Compilador de Dossier Técnico EU AI Act Anexo IV (`euAiActTechnicalDossierService.js`), arnés automatizado de capacidad y benchmark DORA (`npm run benchmark:dora` con RTO medido de 18,55 ms), paquete canónico de homologación bancaria M2 en estado `READY_FOR_INDEPENDENT_REVIEW`, ecosistema pro-code extendido para OpenAPI 3.1 y `FlentioSdk` resiliente con reintentos idempotentes, topología distribuida HA (`docker-compose.ha.yml` con PgBouncer) y edge gateway Nginx TLS 1.3, build de producción frontend sin errores con Vite (`npm run build`), y verificación de handover exitosa (`scripts/verify-handover.ps1`).

## Mapa técnico

- Entrada backend: [index.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/index.js).
- Validador Estático AST (Auto-Healing): [scriptAstSecurityGuard.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/platform/scriptAstSecurityGuard.js) y nodo [auto_healing_sandbox.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/auto_healing_sandbox.js).
- Dossier Técnico EU AI Act (Anexo IV): [euAiActTechnicalDossierService.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/platform/euAiActTechnicalDossierService.js).
- Importador OpenAPI: [openapi_importer.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/openapi_importer.js) y API [openapi.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/api/openapi.js).
- Zapier / Make Bridge: [zapier_make_bridge.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/nodes/zapier_make_bridge.js).
- Flentio Client SDK & REST API: [flentioSdk.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/platform/flentioSdk.js) y [sdk.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/api/sdk.js).
- Perfiles de Gobierno Dinámicos: [tenantGovernance.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/platform/tenantGovernance.js) y [governance.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/api/governance.js).
- Governed Sidecar Middleware: [governedSidecar.js](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/backend/src/api/governedSidecar.js) y especificación [SIDECAR_GOVERNANCE_INTEGRATION.md](file:///c:/Users/ALEX/.gemini/antigravity/scratch/Flentio/docs/architects/SIDECAR_GOVERNANCE_INTEGRATION.md).
- API protegida de administración: `backend/src/api/adminPostgres.js`.
- Catálogo y Skills: `backend/src/platform/externalIntegrationCatalog.js`, `integrationSkillRegistry.js` y `backend/integration-skills/*`.
- Investigación operacional: `operationalInvestigationService.js`, `governedSkillOrchestrator.js`, `investigationCorrelationEngine.js`, `investigationOrchestrationService.js`.
- PostgreSQL/RLS: `backend/src/platform/postgres.js` y `migrations/`.
- RAG: `backend/src/rag/`, sus migraciones y `docs/RAG_*`.
- Pruebas: `backend/test/**/*.test.js`.

## Configuración y secretos

`backend/.env.example` documenta contratos heredados y de infraestructura. Las integraciones de cliente nuevas se configuran desde el frontend administrativo, no editando ficheros. Un nuevo colaborador crea su propio `backend/.env` y nunca recibe el de otro desarrollador.

No versionar: `.env`, claves de cifrado, tokens, cookies, certificados privados, `backend/data`, bases SQLite, dumps, logs, sesiones Playwright ni credenciales de ChatGPT. Revisar `.gitignore` antes del primer commit y ejecutar una herramienta de detección de secretos aprobada antes de publicar.
