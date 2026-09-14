# Kit de extensión para adaptadores de integración

**Estado:** `BASE_INTERNA_IMPLEMENTADA_EN_VALIDACION_LOCAL`.

El módulo interno `backend/src/platform/integrationAdapterSdk.js` implementa la primera base del kit: valida manifiestos y crea adaptadores de sólo lectura con `testConnection` y `collect`. No existe aún un SDK publicable ni autoriza instalar código de terceros. Los adaptadores actuales se rigen por la [arquitectura de Integration Skills](../architects/INTEGRATION_SKILLS_ARCHITECTURE.md).

## Objetivo

Permitir que un equipo técnico implemente un adaptador específico sin modificar el núcleo de Flentio ni debilitar tenant, RLS, bóveda, auditoría, aprobación humana o límites de red. El kit se dirige a ingeniería; la configuración final del cliente sigue siendo no-code desde Administración.

## Límites del SDK futuro

Un adaptador podrá:

- declarar su manifiesto, esquema de configuración no secreta y capacidades;
- resolver referencias de credenciales únicamente durante una llamada;
- ejecutar pruebas reales de mínimo privilegio;
- leer datos expresamente permitidos y devolver resultados minimizados;
- declarar operaciones idempotentes y compensaciones soportadas.

Un adaptador no podrá:

- cargar código remoto, ejecutar shell ni evaluar expresiones arbitrarias;
- almacenar o devolver secretos, cookies, tokens o payloads completos;
- elegir tenant, saltar RLS o reutilizar un perfil de otra organización;
- activar una Skill, concederse capacidades o aprobar una acción;
- simular conectividad o éxito cuando falte configuración.

## Superficie contractual prevista

La futura librería deberá exponer tipos estables equivalentes a los siguientes:

```text
manifest() -> manifiesto versionado e íntegro
validateProfile(profile) -> errores de configuración no secreta
testConnection(context) -> resultado real, mínimo y sanitizado
capabilities(context) -> capacidades efectivas verificadas
collect(request, context) -> evidencia estructurada allowlist
executeApproved(request, context) -> resultado idempotente y correlacionable
compensate(request, context) -> resultado de reversión, si se declara soporte
```

`executeApproved` y `compensate` no se implementarán hasta que exista el [contrato de interoperabilidad](../architects/GOVERNED_INTEROPERABILITY_CONTRACT.md), política de aprobación, control de idempotencia y pruebas de extremo a extremo. La base actual bloquea manifiestos que declaren operaciones de escritura; la versión inicial de cada adaptador debe ser de sólo lectura.

## Estructura recomendada del paquete

```text
backend/integration-skills/<proveedor>/
  manifest.json
  runtime.js
  schemas/profile.schema.json
  schemas/evidence.schema.json
  test/runtime.contract.test.js
  README.md
  SBOM.cdx.json
```

La estructura es una convención propuesta. El cargador actual sólo aceptará paquetes que cumplan sus controles reales de manifiesto, versión, entrypoint e integridad; no se debe crear un directorio para presentarlo como instalado.

## Flujo de contribución

1. Definir proceso, usuario, clasificación, fuente y capacidad mínima.
2. Completar la [plantilla de adaptador](../templates/INTEGRATION_ADAPTER_SPEC.md).
3. Acordar endpoint, identidad, egress, TLS, cuotas, retención y rollback con el propietario de la plataforma externa.
4. Implementar primero `testConnection` de sólo lectura y sus pruebas de contrato.
5. Incorporar UI administrativa dedicada: sin JSON, secretos ni configuración por `.env` para el cliente.
6. Medir y documentar estados, errores, carga diferida y desactivación.
7. Solicitar revisión de seguridad y homologación antes de activar en un tenant.

## Checklist de aceptación

- Manifiesto con ID, versión, permisos, política de bóveda y digest verificable.
- Esquemas con campos allowlist, clasificación y límites de respuesta.
- Credenciales por referencia de bóveda y sólo en memoria durante la llamada.
- Timeout, cuota, cancelación y errores sanitizados.
- Tenant, ámbito y propietario obligatorios en cada ejecución.
- Prueba real de mínimo privilegio; sin éxito fabricado.
- Auditoría de configuración, prueba, activación, desactivación y rechazo.
- Dashboard con estado efectivo y última comprobación, conforme a `docs/DASHBOARD_STANDARD.md`.
- SBOM, licencia, procedencia y revisión de dependencias antes de distribución.

## Versionado y compatibilidad

El manifiesto, esquema de perfil, esquema de evidencia y capacidades se versionan de forma independiente. Un cambio incompatible invalida la prueba y activación hasta revalidación. El adaptador deberá declarar migración o bloqueo explícito; nunca reinterpretar silenciosamente una configuración existente.

## Salida y rollback

Desactivar un adaptador debe impedir nuevas ejecuciones y descargar su runtime cuando el cargador lo soporte. La retirada conserva auditoría y evidencia bajo la política de retención aplicable. Revocar una credencial o autorización deja el perfil en `NO_CONFIGURADO` o `PENDIENTE_AUTORIZACION`; no se sustituye por una respuesta sintética.
