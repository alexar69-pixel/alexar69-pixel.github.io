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
| Autorización | Middleware RBAC y contexto de organización | Aplicado en rutas RAG, operaciones y administración; debe verificarse ruta por ruta. |
| Aislamiento | PostgreSQL RLS con tenant y actor fijados por transacción | Implementado en repositorios de plataforma/RAG; la validación local no acredita despliegue cliente. |
| Contraseñas | `bcrypt` | Implementado por la capa de identidad; la política corporativa final es `DEPENDENCIA_CLIENTE`. |
| HTTP | Helmet | Activo, pero CSP y COEP están desactivados expresamente; endurecimiento pendiente. |
| CORS | Allowlist configurable | En producción, sin `CORS_ORIGINS`, sólo acepta origen ausente o localhost; configurar dominios reales. |
| Abuso | Rate limiting | Login/registro y varias familias RAG/webhook tienen límites; no existe un límite global uniforme. |
| Payloads | JSON 6 MB y límites específicos | OpenAPI 10 MB; fichero RAG 15 MB; PDF/DOCX tienen defensas estructurales. |
| Ingesta RAG | ClamAV, cuarentena, prompt guard y aprobación humana | Falla cerrado; detalle en [Seguridad de ingesta](RAG_SECURITY_INGESTION.md). |
| Originales RAG | AES-256-GCM y object store versionado/WORM configurable | Producción requiere KMS/object store y política autorizados; MinIO local no acredita HA. |
| Auditoría | Cadena HMAC y outbox PostgreSQL | `AUDIT_HMAC_SECRET` impide arranque productivo si falta; entrega SIEM queda `NO_CONFIGURADO` sin destino. |
| Secretos | Bóveda/cifrado e integraciones con proveedores | Cada proveedor exige configuración y prueba real; nunca copiar `.env` o sesiones personales. |
| IA/RAG | ACL antes de reranking, evidencia y abstención | Los proveedores externos sólo son operativos tras prueba autorizada; OAuth personal es sólo desarrollo. |

## Bloqueos de producción encontrados

Estas condiciones proceden del montaje actual de rutas y deben tratarse como
riesgos abiertos, no como endpoints productivos:

| Riesgo | Evidencia en código | Estado / mitigación inmediata |
|---|---|---|
| `/api/sdk/*` acepta tenant desde cabecera/body, no monta autenticación y devuelve `X-Flentio-Simulated: true` | `backend/src/api/routes.js`, `backend/src/api/sdk.js` | `NO_DISPONIBLE`; bloquear en proxy o retirar. No usar como evidencia, DLP, RAG ni WORM. |
| `/api/interop/sidecar/*` tiene el mismo patrón y contenido sintético | `backend/src/api/routes.js`, `backend/src/api/governedSidecar.js` | `NO_DISPONIBLE`; bloquear hasta reemplazar por contrato autenticado, persistente y probado. |
| `/api/openapi/import` se monta sin autenticación y admite JSON de hasta 10 MB | `backend/src/api/routes.js`, `backend/src/api/openapi.js` | `NO_VALIDADA`; bloquear externamente y añadir autenticación, RBAC y límites antes de habilitar. |
| CSP y COEP desactivados | `backend/src/platform/app.js` | `NO_VALIDADA`; definir política compatible y probar frontend antes de producción. |
| Sin rate limit global | `backend/src/platform/app.js` y routers | `NO_VALIDADA`; dimensionar y aplicar límites por identidad, tenant y ruta en gateway/API. |
| Compose publica la aplicación en todas las interfaces (`3000:3000`) | `docker-compose.yml` | Topología local; usar red privada, TLS y gateway aprobado. |
| Compose de nodo único | `docker-compose.yml` | Sin HA acreditada para PostgreSQL, MinIO, ClamAV o reranker. |

Hasta corregir y validar estos puntos, el repositorio no debe describirse como
`PREPARADO_PARA_PRODUCCION`.

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
