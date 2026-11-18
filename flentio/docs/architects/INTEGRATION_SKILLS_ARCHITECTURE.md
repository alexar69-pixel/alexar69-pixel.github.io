# Arquitectura de Integration Skills

## Objetivo y estado

Las conexiones externas de Flentio se modelan como **Integration Skills**
independientes. El objetivo es que SDK, workers, tareas programadas, nodos y
frontend de un proveedor sólo se carguen cuando el cliente haya instalado,
configurado, validado y activado esa Skill.

La fase actual implementa el contrato, manifiestos, estados, API administrativa
y control de activación. Los 29 runtimes están empaquetados y son verificables.
SIEM, HelixGPT, KMS/HSM, CyberArk, Vault/PAM genérico y EDR usan el Client
Integration Gateway v1 porque requieren proveedor, edición o contrato del cliente.
Todavía no se afirma una
reducción medida de memoria o CPU del proceso completo.

## Manifiesto

Cada manifiesto contiene:

- ID `flentio.integration.<proveedor>` y versión del esquema;
- nombre, categoría y contrato de frontend dedicado;
- política `LAZY_ON_ENABLE`;
- permisos administrativos;
- política `VAULT_REFERENCES_ONLY`;
- digest SHA-256 reproducible.

El digest detecta cambios del contrato, pero no equivale todavía a firma de
publicador. La instalación futura de paquetes deberá verificar firma, versión,
compatibilidad, SBOM y procedencia antes de registrar el runtime.

## Ciclo de vida

Se mantienen estados ortogonales:

1. `manifest`: `INSTALLED`.
2. `configuration`: `NO_CONFIGURADO` o `CONFIGURADO_NO_VERIFICADO`.
3. `runtime`: `NO_INSTALADO` o `INSTALADO`.
4. `activation`: `INACTIVA` o `ACTIVA`.
5. `effectiveLoad`: `NOT_LOADED`, `LAZY_PENDING_FIRST_USE` o `LOADED`.

Una Skill sólo puede activarse cuando tiene runtime real y configuración. El
backend rechaza el resto con `SKILL_RUNTIME_NOT_INSTALLED` o
`SKILL_CONFIGURATION_REQUIRED`; ocultar o habilitar un botón no sustituye este
control.

## API y operación

- El catálogo `GET /api/admin/external-integrations` incluye `skill.manifest` y
  `skill.lifecycle`.
- `POST /api/admin/external-integrations/:id/enable` activa únicamente Skills
  elegibles.
- `POST /api/admin/external-integrations/:id/disable` desactiva y descarga en la
  siguiente fase cualquier runtime asociado.
- `POST /api/admin/external-integrations/:id/test` ejecuta la prueba real que
  aporta cada paquete e invalida cualquier validación anterior si falla.

La activación y sus rechazos quedan auditados. Retirar el perfil elimina además
el indicador de activación, evitando una reactivación accidental.

## Siguiente fase técnica

Para obtener reducción real de peso y proceso se deberá:

1. extraer cada adaptador y SDK a un paquete firmado independiente;
2. cargar backend y nodos mediante importación diferida sólo tras activación;
3. dividir el frontend con `import()` por Skill;
4. arrancar workers y cron jobs bajo demanda y detenerlos al desactivar;
5. medir bundle inicial, RSS, CPU idle, handles, tiempo de arranque y superficie
   de dependencias antes/después;
6. aislar fallos, cuotas, egress y permisos por Skill.

No se añadirá un proveedor a `RUNTIME_LOADERS` hasta que exista el adaptador
real, una prueba de conexión, manejo de errores, unload y documentación.

## Paquete de referencia: Ollama

`backend/integration-skills/ollama` contiene un manifiesto 1.0 y un runtime sin
dependencias de terceros. El gestor restringe IDs y rutas, comprueba versión,
entrypoint y SHA-256 antes de `require()` y mantiene una caché descargable. El
runtime valida el endpoint con `GET /api/tags`, timeout acotado y contrato de
respuesta. El nodo `ai_ollama` y el proveedor Ollama de agentes ya resuelven el
perfil del tenant mediante `integrationSkillExecutionService`, comprueban
fingerprint, validación y activación y sólo entonces cargan el runtime. El
adaptador histórico directo queda bloqueado con
`OLLAMA_DIRECT_ADAPTER_DISABLED`.

El ciclo local real guardó `http://127.0.0.1:11434`, validó cinco modelos y
activó la Skill Ollama. La validación se liga al perfil: modificar el perfil
elimina validación y activación. El 02-08-2026 una primera generación gobernada
detectó correctamente un timeout de 5 s; tras cambiarlo en el perfil a 30 s,
revalidar y reactivar, el nodo devolvió una respuesta real de dos caracteres y
registró `Respuesta real recibida de la Integration Skill Ollama activa`.

## Paquete Prometheus

`backend/integration-skills/prometheus` ofrece una prueba real y de sólo lectura
contra el API HTTP del cliente. Ejecuta `GET /api/v1/query?query=vector(1)`, una
consulta constante que valida protocolo y contrato sin leer series operativas.
El endpoint, credencial opcional y timeout se guardan por tenant desde Administración.
La versión 0.2.0 resuelve bearer desde la bóveda sólo en memoria y también ofrece
`queryRange`: limita resultados a 100 series/10.000 muestras y devuelve únicamente
conteo, min/max/media/primero/último. La política no-code construye la consulta;
el runtime no devuelve labels ni valores crudos al servicio llamador. El paquete
verifica integridad antes de carga y se descarga al desactivar la Skill.

Estado al 02-08-2026: runtime `INSTALADO`, perfil del cliente `NO_CONFIGURADO` y
activación `INACTIVA`. La prueba automatizada valida el contrato contra un servidor
HTTP efímero de test, pero no demuestra conectividad con infraestructura bancaria.

Rollback: desactivar el paquete descarga su runtime e impide nuevas consultas;
no elimina perfiles, políticas, auditoría ni referencias ya incorporadas.

## Identidad en ejecuciones automáticas

En PostgreSQL, cron y webhooks publican trabajos durables con `organization_id` y
`requested_by`; el worker carga los claims persistidos del usuario antes de crear
el runner. En SQLite heredado, cron y webhooks reconstruyen el contexto desde el
propietario real del workflow y fallan con `WORKFLOW_OWNER_CONTEXT_NOT_FOUND` si
no existe. El payload webhook persistible elimina Authorization, cookies y tokens.
Así, una Integration Skill nunca recibe un tenant sintético ni ejecuta sin contexto.

## Paquete Grafana

`backend/integration-skills/grafana` valida de forma real `GET /api/health` y
`GET /api/org`. La primera llamada comprueba salud y versión; la segunda obliga
a demostrar acceso de lectura a una organización. Si se selecciona una credencial,
el backend la resuelve por propietario y tenant, entrega el token Bearer al runtime
sólo en memoria y no lo incorpora al perfil, validación, auditoría ni respuesta.

Estado al 02-08-2026: runtime `INSTALADO`, perfil del cliente `NO_CONFIGURADO` y
activación `INACTIVA`. La suite usa un servidor HTTP efímero exclusivamente como
doble de prueba; no demuestra conexión con una instancia Grafana bancaria. Esta
versión todavía no consulta alertas, dashboards ni datasources y no alimenta el
correlador operacional.

Riesgos: el endpoint provoca egress desde backend y debe someterse a allowlist,
DNS y TLS corporativos; un service account excesivo ampliaría el alcance de lectura.
La fase de producción deberá restringir tipos de credencial, verificar certificados
corporativos y aplicar scopes por carpetas/datasources cuando la API lo permita.

Rollback: desactivar Grafana desde Administración descarga el runtime. Para retirar
el paquete se elimina `grafana` de `RUNTIME_LOADERS` y se conserva el perfil inerte
o se retira mediante la API auditada; nunca se borra globalmente la configuración.

## Oleada de observabilidad 0.1

Dynatrace valida acceso de sólo lectura mediante `GET /api/v2/metrics`; Datadog
comprueba la API key mediante `GET /api/v1/validate`; OpenTelemetry valida un
`healthEndpoint` separado sin enviar telemetría; y Splunk/ITSI consulta
`GET /services/server/info?output_mode=json`. Los cuatro runtimes aplican timeout,
límites de respuesta, resolución de credenciales sólo en memoria y devuelven
metadatos mínimos, nunca secretos ni payloads operativos completos.

Estado al 02-08-2026: paquetes e integridad verificados, pero perfiles del cliente
`NO_CONFIGURADO` y Skills `INACTIVA`. Sus pruebas contra servidores HTTP efímeros
demuestran el contrato del adaptador, no conectividad ni homologación bancaria.

## Oleada cloud 0.1

CloudWatch ejecuta `ListMetrics` mediante el SDK oficial y firma SigV4; Azure
Monitor lee `metricDefinitions` del `resourceId` autorizado; Google Cloud
Operations lista un único descriptor del proyecto. Ninguno consulta valores de
métricas, logs o alertas durante la prueba. Las credenciales se resuelven desde
la bóveda sólo en memoria y el resultado conserva metadatos mínimos.

Estado al 02-08-2026: los tres runtimes están instalados, pero todas las cuentas
del cliente permanecen `NO_CONFIGURADO`. Los tests recorren SDK/protocolo HTTP
real contra servidores efímeros; no demuestran acceso a AWS, Azure o GCP reales.

## Oleadas IA, identidad, bóvedas e inventario 0.1

OpenAI y Gemini enumeran modelos sin generar contenido. OIDC exige discovery,
JWKS y authorization code. HashiCorp Vault comprueba salud y `lookup-self`; las
tres bóvedas cloud sólo enumeran un metadato por prefijo. TEI consulta `/health`.
S3 compatible exige Object Lock sin leer objetos. BMC Helix Operations ejecuta
`msearch` con tamaño cero. CMDB/SBOM valida CycloneDX 1.7 y conserva sólo hash y
conteo. Todos los perfiles del cliente permanecen `NO_CONFIGURADO`.

## Client Integration Gateway v1

Los seis conectores dependientes del cliente validan un gateway real mediante
challenge de un solo uso, timestamp reciente, bearer de bóveda, tenant, ámbito,
principal, modo de sólo lectura y capacidades obligatorias. KMS/HSM liga además
el `keyId`; CyberArk liga cuenta y prefijo. Una respuesta 200 incompleta se
rechaza. Contrato: `docs/CLIENT_INTEGRATION_GATEWAY_V1.md`.

KMS/HSM y object storage permanecen `PENDIENTE_AUTORIZACION` aunque su runtime
esté instalado. El frontend exige una decisión humana auditada por proveedor
antes de guardar, probar o activar y permite revocarla eliminando perfil,
validación y activación.

## Interoperabilidad y extensiones futuras

La interoperabilidad con plataformas de automatización, orquestadores técnicos
o plataformas internas no se resolverá importando sus flujos ni ejecutando su
código dentro de Flentio. El [contrato de interoperabilidad gobernada](GOVERNED_INTEROPERABILITY_CONTRACT.md)
define el objetivo de eventos, evidencias, aprobación, órdenes idempotentes y
compensación. La incorporación de evidencia a investigaciones por una Skill
activa está implementada en validación local; recepción pública, órdenes y
compensación continúan `NO_IMPLEMENTADO`.

El [kit de extensión de adaptadores](../developers/INTEGRATION_ADAPTER_SDK.md)
define cómo un equipo técnico podrá crear un Integration Skill sin modificar el
núcleo ni omitir controles de tenant, bóveda, auditoría o activación. La base
interna valida manifiestos y adaptadores de sólo lectura; no existe todavía un
SDK distribuible y la primera versión de cada adaptador debe ser de sólo lectura.

## Medición inicial de frontend

Antes de separar el panel, el chunk principal medía 1.506.200 bytes. Tras usar
`React.lazy`, el panel pasó a un chunk independiente de 10.739 bytes y el chunk
principal quedó en 1.496.839 bytes: reducción inicial de 9.361 bytes en la carga
base. El total descargado al abrir administración es similar; falta dividir el
frontend particular de cada proveedor.

## Rollback

Revertir el registro `integrationSkillRegistry.js`, los campos `skill` de la
API, las rutas `enable/disable` y los elementos de ciclo de vida del frontend.
Los perfiles existentes permanecen inertes. Las claves `*_ENABLED` deben
eliminarse por tenant mediante operación auditada; nunca mediante borrado
global.

## Diferenciación

Necesidad: bancos con ecosistemas distintos no deben ejecutar ni auditar
conectores que no utilizan. Ventaja propuesta: Skills con frontend dedicado,
secretos referenciados, evidencia y ciclo de vida gobernado. La barrera legítima
será la acumulación de adaptadores bancarios, contratos, runbooks y controles
verificados. Métricas: reducción de bundle/RSS/CPU idle, tiempo de instalación,
aislamiento de fallos y porcentaje de Skills verificadas. Hipótesis de mercado:
`NO_VALIDADA`.

## Paquete Jira Cloud

`backend/integration-skills/jira` valida REST API v3 mediante dos GET de sólo
lectura: identidad y proyecto. La credencial `email` + `apiToken` se resuelve
desde la bóveda y sólo existe en memoria durante la petición. El manifiesto
0.2.0 está protegido por SHA-256. `searchResolvedReferences` construye JQL desde
proyecto y ventana, limita 25 resultados y devuelve sólo referencias y metadatos
técnicos. No devuelve texto libre del issue.

Estado: instalado pero cliente `NO_CONFIGURADO`. OAuth 3LO, Data Center y BMC
Helix se mantienen como paquetes separados. Desactivar descarga el runtime.

## Paquete BMC Helix ITSM

`backend/integration-skills/bmc_helix_itsm` implementa exclusivamente la variante
Simplified REST. Autentica contra Innovation Suite y valida el recurso persona
con una cookie efímera. La contraseña se resuelve desde la bóveda sólo durante
la llamada. El manifiesto 0.1.0 declara `authentication-ephemeral` y
`person-readonly`; búsquedas ITSM, Platform REST, Operations y HelixGPT no están
instaladas en este paquete.
