# Orquestación gobernada de investigaciones

Estado: `IMPLEMENTADA_EN_VALIDACION_LOCAL`. No acredita conexiones bancarias ni
habilita remediación.

## Comportamiento

`POST /api/admin/operational-investigations/:id/orchestrate` acepta sólo un plan
de lectura con Prometheus, Jira y BMC Helix ITSM. Ejecuta hasta cuatro collectors
en paralelo, aplica timeout individual y distingue fuentes obligatorias y
opcionales. Shell, herramientas arbitrarias y capacidades de escritura no están
en la allowlist. Si falla una fuente obligatoria o ninguna fuente termina, el
resultado es `EVIDENCIA_INSUFICIENTE`.

Los resultados persistidos contienen estado, duración, conteos y hashes, nunca
payloads, secretos o contenido libre del proveedor. PostgreSQL conserva runs,
análisis y revisiones bajo RLS mediante las migraciones `022` y `023`.

## Correlación e hipótesis

El motor filtra por servicio, entorno y ventana; ordena referencias y crea
relaciones `TEMPORALLY_ADJACENT_NOT_CAUSAL`. Compara atributos estructurados
allowlist para detectar versiones o estados incompatibles. Sus hipótesis son
deterministas:

- cambio reciente + telemetría;
- activo/dependencia CMDB + telemetría;
- incidente cerrado + runbook;
- seguridad + telemetría.

Todas quedan `CANDIDATE_NOT_CAUSAL` o `CONTRADICTED_CANDIDATE`, con referencias,
checks y confianza calculada. El contrato público conserva siempre
`causality: NOT_ESTABLISHED`.

## Revisión humana

`GET .../:id/analysis` devuelve el último análisis visible. Un administrador
puede registrar una vez `ACCEPT_FOR_REVIEW`, `REJECT` o
`NEEDS_MORE_EVIDENCE`, con motivo mínimo y reconfirmación frontend. La revisión
no modifica evidencia, no aprueba M2 y no ejecuta acciones.

## Prompt Caching

El prompt M2 v2 comienza por una política y esquema estables y coloca después
el contexto variable. Ollama 0.2 informa `NO_VERIFICADO` porque su respuesta no
acredita tokens cacheados; no se inventa ahorro. Los proveedores productivos
deberán exponer tokens cacheados y respetar tenant, privacidad y versionado.

## Operación y rollback

Desactivar las rutas detiene nuevas orquestaciones. Las tablas son evidencia y
no deben borrarse. Para rollback de código se revierten servicio, repositorio,
API y UI; las migraciones aplicadas permanecen. Reducir la allowlist o marcar
fuentes obligatorias es compatible hacia atrás. Nunca se habilita una ruta de
ejecución como rollback.
