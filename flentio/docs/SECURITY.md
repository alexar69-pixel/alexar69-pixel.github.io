# Seguridad de Flentio

> Estado documental del checkout a 05-09-2026. Este documento describe
> controles observados en código; no es una certificación, pentest ni aprobación
> bancaria. Los despliegues externos permanecen `DEPENDENCIA_CLIENTE`.

## Modelo de seguridad

Flentio procesa identidades, workflows, credenciales, documentos y evidencias
por organización. Los límites de confianza principales son navegador/API,
procesos web y workers, PostgreSQL, object storage, proveedores de IA,
antimalware e integraciones del cliente.

Objetivos mínimos:

- negar el acceso sin identidad y autorización válidas;
- preservar aislamiento entre tenants mediante contexto y RLS;
- fallar cerrado cuando falte una dependencia de seguridad;
- no incluir secretos ni contenido sensible en logs o métricas;
- conservar trazabilidad de decisiones sin afirmar inmutabilidad externa no
  configurada;
- impedir que datos de demo o respuestas simuladas entren en operación.

## Controles implementados observados

| Dominio | Control | Estado y límite |
|---|---|---|
| Autenticación | JWT HS256, comprobación de expiración/validez y resolución de usuario activo | `JWT_SECRET` es obligatorio en operación; falta de secreto devuelve `NO_CONFIGURADO`. |
| Autorización | Middleware RBAC y contexto de organización | Aplicado en rutas RAG, operaciones, administración, SDK, Interop Sidecar y OpenAPI; validado con tests negativos de rol. |
| Aislamiento | PostgreSQL RLS con tenant y actor fijados por transacción | Implementado en repositorios de plataforma/RAG; tenant extraído estrictamente de la sesión autenticada en `/api/sdk` e `/api/interop` sin permitir suplantación por cabecera. |
| Contraseñas | `bcrypt` | Implementado por la capa de identidad; la política corporativa final es `DEPENDENCIA_CLIENTE`. |
| HTTP | Helmet con CSP estricto y defensivo en producción | Activo; directivas `defaultSrc: ["'self'"]`, `scriptSrc: ["'self'"]`, `styleSrc: ["'self'", "'unsafe-inline'"]`, `imgSrc: ["'self'", "data:", "blob:"]`, `objectSrc: ["'none'"]`, `frameAncestors: ["'none'"]`. |
| CORS | Allowlist configurable | En producción, sin `CORS_ORIGINS`, sólo acepta origen ausente o localhost; configurar dominios reales. |
| Abuso | Rate limiting global y especializado | Rate limiter defensivo global en `/api` (1000 req/5 min con bypass exclusivo en `/api/health`), sumado a límites específicos en auth, RAG y webhooks. |
| Payloads | JSON 6 MB y límites específicos | OpenAPI 10 MB protegido por RBAC admin/editor; fichero RAG 15 MB; PDF/DOCX tienen defensas estructurales. |
| Ingesta RAG | ClamAV, cuarentena, prompt guard y aprobación humana | Falla cerrado; detalle en [Seguridad de ingesta](RAG_SECURITY_INGESTION.md). |
| Originales RAG | AES-256-GCM y object store versionado/WORM configurable | Producción requiere KMS/object store y política autorizados; MinIO local no acredita HA. |
| Auditoría | Cadena HMAC y outbox PostgreSQL | `AUDIT_HMAC_SECRET` impide arranque productivo si falta; trazas WORM automáticas registradas en `/api/sdk` y `/api/interop`. |
| Secretos | Bóveda/cifrado e integraciones con proveedores | Cada proveedor exige configuración y prueba real; nunca copiar `.env` o sesiones personales. |
| IA/RAG | ACL antes de reranking, evidencia y abstención | Los proveedores externos sólo son operativos tras prueba autorizada; OAuth personal es sólo desarrollo. |

## Bloqueos de producción y riesgos abiertos

### Mitigados en el checkout actual (Verificados en suite de seguridad)
- **/api/sdk/\***: Autenticación obligatoria montada con RBAC (`admin`, `editor`, `operator`). El tenant se deriva estrictamente del usuario autenticado (`req.user.organizationId`), rechazando suplantación arbitraria por cabecera/body. Cabecera `X-Flentio-Simulated` eliminada. Registro de auditoría WORM emitido en cada llamada.
- **/api/interop/sidecar/\***: Autenticación obligatoria montada con RBAC. Cabecera simulada eliminada y eventos auditados formalmente en WORM ledger.
- **/api/openapi/import**: Protegido por autenticación y RBAC restringido a `admin` y `editor`. Emisión de evento de auditoría `OPENAPI_SPEC_IMPORTED`.
- **Content Security Policy (CSP)**: Habilitado en producción a través de Helmet con directivas estrictas que mitigan XSS y clickjacking (`frameAncestors: ['none']`).
- **Rate Limit Defensivo Global**: Activado para todas las rutas bajo `/api` (1000 req / 5 min) con bypass transparente exclusivo para probes de orquestador (`/api/health`).
- **Validador Estático AST de Remediación (`scriptAstSecurityGuard.js`)**: Detección léxica y sintáctica determinista que bloquea comandos destructivos (`rm -rf`, `DROP`, reverse shells, exfiltración, escalada) antes de cualquier aprobación humana HITL o ejecución en el sandbox de auto-healing.
- **Compilador de Dossier Técnico EU AI Act (`euAiActTechnicalDossierService.js`)**: Generación del expediente formal de 5 secciones (Anexo IV, Reglamento UE 2024/1689) con sellado criptográfico WORM SHA-256 (`GET /api/governance/compliance/eu-ai-act-dossier`).
- **Topología HA y PgBouncer (`docker-compose.ha.yml`)**: Manifiesto distribuido con nodos redundantes (`flentio-app-1`, `flentio-app-2`), replicación PostgreSQL primario/standby mediante PgBouncer en red interna aislada (`internal: true`), y MinIO multi-nodo.
- **Edge Gateway Nginx TLS 1.3 (`docker/nginx/nginx.conf`)**: Suprime la publicación directa de puertos de aplicación a internet (`3000:3000`). Enrutamiento cifrado con TLS 1.3, rate limiting L7 (100 req/s), HSTS y CSP estricto.

### Requisitos de Acreditación en Despliegue Externo (`DEPENDENCIA_CLIENTE`)

Los artefactos de infraestructura (`docker-compose.ha.yml` y `docker/nginx/nginx.conf`) están formalizados y validados sintácticamente en el repositorio (`test/haTopology.test.js`). No obstante, en un entorno de producción bancario, el aprovisionamiento real de certificados CA corporativos, balanceadores cloud y almacenamiento en bloque redundante debe ser acreditado por el equipo de infraestructura cliente.

## Configuración mínima de despliegue

- Generar `JWT_SECRET`, `AUDIT_HMAC_SECRET`, claves de cifrado y secretos HMAC
  con el gestor corporativo; no usar valores de ejemplo.
- Definir `CORS_ORIGINS`, `ALLOWED_HOSTS` y `OAUTH_REDIRECT_BASE_URL` con HTTPS.
- Separar rol de migración y rol de aplicación; verificar RLS y grants después
  de cada migración.
- Mantener `ALLOW_LOCAL_AUTH_BYPASS=false` y prohibir OAuth personal en
  producción.
- Aprovisionar TLS, gateway/WAF, protección DDoS, rotación, backups, retención,
  SIEM y alertas según decisiones del cliente.
- Autorizar explícitamente hosts salientes; cualquier integración no probada se
  muestra `NO_CONFIGURADO` o `NO_DISPONIBLE`.
- Ejecutar análisis de dependencias, secretos, SAST, DAST y pentest con alcance
  y fecha registrados. Este checkout no contiene evidencia vigente suficiente
  para afirmar que esas puertas estén cerradas.

## Operación e incidentes

1. Identificar tenant, actor, ruta, versión y ventana sin copiar payloads o
   secretos al ticket.
2. Revocar sesión/credencial afectada y aislar la integración; preservar
   auditoría y evidencias.
3. Si hay posible cruce de tenant, detener el recorrido afectado y verificar
   RLS antes de reabrirlo.
4. Si falla ClamAV, KMS, object store, PostgreSQL o una firma, fallar cerrado;
   no activar bypasses locales.
5. Rotar secretos mediante el sistema autorizado, evaluar datos expuestos y
   seguir notificación/regulación del cliente.
6. Documentar causa, alcance, recuperación, controles compensatorios y prueba
   posterior. No borrar eventos para cerrar el incidente.

## Verificación y evidencias requeridas

| Puerta | Evidencia mínima |
|---|---|
| Identidad/RBAC | tests negativos por rol, sesión revocada y usuario deshabilitado |
| Tenant | pruebas de cruce entre organizaciones en API y acceso SQL forzado-RLS |
| Entradas | 401/403/413/429, MIME/firma inválidos, ZIP bomb, malware y prompt injection |
| Salidas | redacción de secretos/PII, citas autorizadas, logs y métricas minimizados |
| Proveedores | conexión real autorizada, TLS, timeout, error y estado no configurado |
| Auditoría | integridad HMAC, acceso RLS, outbox, entrega SIEM y recuperación |
| Resiliencia | backup/restore, pérdida de worker, renovación de lease y dependencia caída |

Publique las ejecuciones fechadas en `docs/audits/`. Una prueba automatizada con
dobles acredita el contrato del código, no la seguridad del proveedor real.

## Documentos relacionados

- [Guía integral de seguridad y cumplimiento](SECURITY_AND_COMPLIANCE_GUIDE.md)
- [Semántica de estados](PLATFORM_OPERATIONAL_STATUS.md)
- [Seguridad de ingesta RAG](RAG_SECURITY_INGESTION.md)
- [Producción RAG](RAG_PRODUCTION_READINESS.md)
- [Salud de infraestructura](admins/PLATFORM_INFRASTRUCTURE_HEALTH.md)
- [Registro de riesgos](leadership/RISK_REGISTER.md)
- [Capacidad y carga](architects/CAPACIDAD_CARGA_USUARIOS_Y_PROCESOS.md)

## Rollback

Un cambio de seguridad se revierte sólo hacia una configuración que conserve
autenticación, autorización, RLS, auditoría y fallo cerrado. Si no existe una
reversión segura, deshabilite la ruta o integración y marque `NO_DISPONIBLE`.
