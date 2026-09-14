# Administración restringida de integraciones externas

## Alcance real

El portal **Administración → Integraciones externas** centraliza las herramientas
que dependen del cliente, necesitan autorización o siguen `NO_CONFIGURADO`. La
ruta web `/admin?tab=integrations` sólo admite el rol `admin`; las rutas de API
están bajo `/api/admin` y el backend vuelve a exigir autenticación y rol
`admin`. Un control visual no sustituye este segundo control.

**Acceso a infraestructura de clientes**: actualmente **no disponemos** de acceso
a la infraestructura de clientes. Por tanto, todas las Skills permanecen
`NO_CONFIGURADO` o `CONFIGURADO_NO_VERIFICADO` hasta que el cliente aporte
endpoints, credenciales, permisos y controles de red/TLS específicos. Los
formularios y contratos están implementados para recibir esos valores, pero no
para simularlos ni inventarlos.

Cada entrada usa `configurationMode: DEDICATED_FRONTEND` y tiene un contrato
visual propio: título operativo, prerequisitos y campos permitidos específicos
del producto. La implementación reutiliza el motor de formularios sólo para
consistencia y seguridad; no presenta al administrador un formulario genérico,
un editor JSON ni instrucciones para modificar `.env`, YAML u otros ficheros.

Las entradas son además **Integration Skills**. El panel separa manifiesto,
configuración, runtime y activación. Disponer del formulario no significa que el
adaptador esté instalado. Arquitectura, estados y carga diferida:
`docs/architects/INTEGRATION_SKILLS_ARCHITECTURE.md`.

El catálogo incluye observabilidad, cloud, ITSM/conocimiento, IA/RAG,
seguridad, identidad, inventario y plataforma. Entre otras: Grafana,
Prometheus, OpenTelemetry, Dynatrace, Datadog, CloudWatch, Azure Monitor,
Google Cloud Operations, Splunk/ITSI, SIEM, BMC Helix Operations, Jira, BMC
Helix ITSM, HelixGPT, OpenAI API, Gemini, Ollama, TEI, S3, KMS/HSM, Vault/PAM,
IdP y CMDB/SBOM.

La categoría **Infraestructura y secretos** incluye perfiles diferenciados para
HashiCorp Vault, CyberArk PAM/Conjur, AWS Secrets Manager, Azure Key Vault,
Google Secret Manager y una bóveda/PAM genérica. Sus formularios permiten
declarar método de autenticación, namespace, mount, rol, cuenta, tenant, región
y prefijo de secretos según el proveedor. El método se selecciona de una lista
cerrada: AppRole, OIDC, workload/managed identity, service account, certificado
o token bootstrap.

## Operación

1. Acceder con una cuenta `admin` y abrir **Integraciones externas**.
2. Buscar la herramienta y abrir su ficha.
3. Revisar la lista **Antes de configurar**, que cambia según el producto.
4. Completar el formulario dedicado. La credencial se elige de la bóveda y
   nunca se pega el secreto.
5. Guardar. El estado cambia a `CONFIGURADO_NO_VERIFICADO`, no a operativo.
6. Ejecutar **Probar conexión**. Sólo las Skills con runtime real pueden superar
   la validación y después activarse.

API:

- `GET /api/admin/external-integrations`: catálogo y perfiles del tenant.
- `PUT /api/admin/external-integrations/:id`: guarda únicamente los campos
  permitidos de un perfil; exige endpoint HTTP(S).
- `DELETE /api/admin/external-integrations/:id`: retira el perfil de forma
  auditada y devuelve la herramienta a `NO_CONFIGURADO`.
- `POST /api/admin/external-integrations/:id/test`: prueba la conexión real sólo
  si el paquete implementa el contrato; las 29 Skills disponen actualmente de runtime.
- `POST .../:id/enable|disable`: activa tras validación o desactiva y descarga
  el runtime de la caché.

El selector carga únicamente las credenciales visibles para el administrador
autenticado. El backend rechaza referencias inexistentes o pertenecientes a
otro propietario. Los perfiles se guardan en la configuración aislada del tenant con claves
`EXTERNAL_INTEGRATION_<ID>_PROFILE`. No contienen contraseñas, tokens ni claves
API. Cada actualización genera `EXTERNAL_INTEGRATION_PROFILE_UPDATED` en la
auditoría sin registrar valores.

## Riesgos y límites

- `CONFIGURADO_NO_VERIFICADO` sólo acredita que existe un perfil sintácticamente
  válido; no acredita conectividad, permisos, TLS, alcance ni salud.
- Las 29 integraciones tienen runtime empaquetado. SIEM, HelixGPT, KMS/HSM,
  CyberArk, Vault/PAM genérico y EDR validan el Client Integration Gateway v1;
  siguen `NO_CONFIGURADO` hasta que el cliente aporte gateway y credencial.
- Se admite HTTP para laboratorios locales. Producción debe usar HTTPS y los
  controles de egress, certificados y DNS aprobados por el cliente.
- La referencia a credencial no confirma que la credencial exista o sea válida;
  esa comprobación corresponde a la validación real del adaptador.
- Este cambio prepara la conexión administrativa, pero no instala todavía los
  SDK ni adaptadores de lectura de cada bóveda. Todos permanecen
  `NO_CONFIGURADO` o `CONFIGURADO_NO_VERIFICADO`.
- El acceso futuro deberá pedir secretos bajo demanda, respetar el prefijo
  permitido, evitar persistir el valor recuperado y auditar sólo metadatos.

## Prometheus: operación y límites actuales

La ficha Prometheus solicita endpoint, credencial de bóveda opcional, ámbito y timeout. **Probar conexión**
ejecuta una consulta constante `vector(1)` contra `/api/v1/query`; así valida el
API real sin leer métricas del cliente. El runtime se verifica mediante SHA-256,
permanece descargado hasta su primer uso y vuelve a descargarse al desactivar.

El perfil del cliente continúa `NO_CONFIGURADO` hasta que un administrador
aporte un endpoint y supere la prueba. La versión 0.2.0 acepta bearer directo o
JSON `{"token":"..."}` desde la bóveda y nunca lo persiste fuera de ella. En
**Investigación operacional**, una política visual genera PromQL acotado y la
consulta de rango conserva sólo agregados y hash. mTLS o proxies con contratos
distintos siguen pendientes de implementación y homologación.

Las ejecuciones cron y webhook en PostgreSQL conservan tenant y solicitante en
el trabajo durable. En SQLite heredado se cargan los claims del propietario real
del workflow; si éste no existe, se falla cerrado con
`WORKFLOW_OWNER_CONTEXT_NOT_FOUND`. Authorization, cookies y tokens no pasan al
estado persistible del webhook.

## Grafana: operación y límites actuales

La ficha Grafana solicita endpoint, credencial de bóveda, ámbito y timeout. La
credencial debe contener directamente el token de service account o un JSON
`{"token":"..."}`; el secreto se descifra únicamente dentro del backend y se
envía como Bearer durante la llamada. **Probar conexión** consulta `/api/health`
y `/api/org`, conservando sólo versión, estado de base de datos, ID y nombre de
organización como evidencia de validación.

Estado al 02-08-2026: runtime instalado, pero perfil del cliente
`NO_CONFIGURADO` y Skill `INACTIVA`. Todavía no se leen alertas, dashboards ni
datasources. El endpoint debe quedar bajo controles corporativos de egress, DNS
y TLS; el service account ha de ser de sólo lectura y pertenecer al tenant que
configura la Skill.

Tras validar y activar Grafana, **Investigación operacional** permite crear un
canal de alertas. La pantalla avisa de las consecuencias y exige confirmación
antes de crear, rotar o desactivar. El token sólo se muestra una vez; el operador
debe configurar en Grafana la ruta presentada y la cabecera
`X-Flentio-Webhook-Token`. Rotar invalida inmediatamente el token anterior.

El canal exige HMAC-SHA256 del cuerpo, timestamp reciente, ID de entrega de un
solo uso y allowlist exacta de IP. La pantalla configura la allowlist y muestra
una sola vez el secreto que debe custodiar el contact point o gateway firmante.
TLS es obligatorio y mTLS, compatibilidad real de la edición Grafana y gateway
quedan pendientes de homologación bancaria. La interfaz no sustituye esa
aprobación.

## IA, identidad, bóvedas, S3 y CMDB/SBOM

Las pruebas son de lectura mínima: modelos disponibles, discovery OIDC,
salud/token propio de Vault, metadatos de secretos por prefijo, health de TEI,
Object Lock del bucket y CycloneDX 1.7. No se genera contenido, no se leen
valores de secretos u objetos y no se copia el SBOM. BMC Helix Operations usa
una búsqueda `size: 0`. Cada perfil continúa `NO_CONFIGURADO` hasta su validación
en infraestructura del cliente.

KMS/HSM y almacenamiento de objetos muestran una puerta adicional de
autorización. El administrador debe indicar proveedor y confirmar la decisión;
hasta entonces el backend rechaza guardar, probar y activar. Revocar la decisión
elimina perfil, validación y activación. Detalle del contrato y rollback:
`docs/CLIENT_INTEGRATION_GATEWAY_V1.md`.

## Prevención de errores humanos

Guardar sobre un perfil existente, probar una conexión real, activar, desactivar
o retirar una Skill presenta una reconfirmación con la consecuencia concreta.
La política temporal del expediente sólo admite 1–30 días y también requiere
confirmación. Añadir evidencia avisa expresamente de que alcanzar
`READY_REVIEW` no confirma la causa. Estas barreras complementan las validaciones
del backend; no dependen únicamente de botones deshabilitados.

## Dynatrace, Datadog, OpenTelemetry y Splunk/ITSI

Cada producto dispone de ficha dedicada y prueba de conexión acotada. Dynatrace
enumera como máximo la primera página mínima de métricas; Datadog valida la API
key; OpenTelemetry prueba exclusivamente el endpoint de salud configurado y no
emite spans, métricas ni logs; Splunk/ITSI lee información básica del servidor.
El resultado persistido contiene sólo latencia y metadatos mínimos. Los cuatro
perfiles del cliente permanecen `NO_CONFIGURADO` hasta completar endpoint,
credencial, red, TLS, permisos de sólo lectura y homologación.

## CloudWatch, Azure Monitor y Google Cloud Operations

Las fichas cloud separan cuenta/proyecto, región o recurso, ámbito, endpoint,
timeout y credencial de bóveda. La prueba CloudWatch usa el SDK oficial para
`ListMetrics`; Azure consulta las definiciones del recurso exacto; Google lista
como máximo un descriptor. No se leen valores, logs ni alertas. Los perfiles
siguen `NO_CONFIGURADO` hasta que el cliente autorice identidades de mínimo
privilegio, endpoints, egress, TLS y ámbitos.

## Rollback

Para retirar la interfaz se revierten `ExternalIntegrationsAdmin.jsx`, sus dos
funciones de `adminOps.js`, la pestaña de `PlatformOverviewPanel.jsx`, el
registro de rutas y los módulos `externalIntegrations.js` y
`externalIntegrationCatalog.js`. Los perfiles persistidos son inertes sin esas
rutas; su borrado debe realizarse mediante un cambio auditado y específico por
tenant, nunca con una eliminación global.

## Ficha de diferenciación

La necesidad es reducir errores al incorporar el heterogéneo ecosistema técnico
de un banco sin exponer secretos ni confundir configuración con disponibilidad.
La ventaja propuesta es un inventario gobernado y auditable conectado al futuro
motor de investigación de incidentes. La barrera legítima será la acumulación de
contratos, controles y conocimiento operativo autorizado del cliente, no el
bloqueo tecnológico. Métrica propuesta: tiempo hasta perfil completo y porcentaje
de integraciones que superan validación real sin incidencias de secreto. Estado
de validación de mercado: `NO_VALIDADA`.

## Jira Cloud: validación de sólo lectura

La Skill Jira 0.2.0 se carga bajo demanda. El formulario pide base URL HTTPS,
proyecto, scope, timeout y una credencial de bóveda JSON con `email` y
`apiToken`. **Probar conexión** consulta únicamente `/rest/api/3/myself` y
`/rest/api/3/project/{key}`. Desde un expediente puede ejecutar JQL generado por
Flentio contra `/rest/api/3/search/jql`, limitado al proyecto, categoría Done,
ventana temporal, 25 resultados y cinco campos técnicos. Persiste referencias
ITSM, nunca resumen, descripción, comentarios, adjuntos o contenido libre.

OAuth 2.0 3LO y Jira Data Center requieren métodos distintos y permanecen fuera
de este paquete Cloud. Estado: runtime `INSTALADO`, cliente `NO_CONFIGURADO` y
Skill `INACTIVA`. Rollback: desactivar descarga el runtime; retirar el perfil
elimina configuración/validación sin borrar credencial o auditoría.

## BMC Helix ITSM: validación Simplified REST

La Skill 0.1.0 pide endpoint de Innovation Suite, usuario técnico, scope, timeout
y una credencial de bóveda JSON `{"password":"..."}`. **Probar conexión** inicia
una sesión efímera en `/api/rx/authentication/loginrequest` y consulta únicamente
`/api/com.bmc.dsm.itsm.itsm-rest-api/person/{usuario}`. La cookie devuelta se usa
sólo en memoria y no se persiste ni se devuelve al frontend.

Este paquete requiere Simplified REST habilitada. No consulta tickets, no usa
formularios AR personalizados y no representa Helix Operations ni HelixGPT.
Estado: runtime `INSTALADO`, cliente `NO_CONFIGURADO`, Skill `INACTIVA`.
Rollback: desactivar descarga el runtime y retirar el perfil invalida su prueba;
la credencial y la auditoría permanecen bajo sus ciclos independientes.
