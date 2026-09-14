# Evidencia local: runbooks de salud operables

Fecha: 01-08-2026. Alcance: desarrollo local, sin datos de clientes.

## Resultado

Flentio incorpora un catálogo backend de ocho procedimientos operativos:
diagnóstico general, capacidad del host, PostgreSQL de plataforma, PostgreSQL
RAG, auditoría, Google Cloud, Banco de España y CISA KEV. Cada entrada contiene
código estable, título, alcance, descripción, cuatro o más pasos, precauciones y
fuente oficial cuando corresponde.

El endpoint autenticado `GET /api/admin/infrastructure-health/runbooks` sólo
devuelve este catálogo versionado. El formulario recomienda el procedimiento
según la métrica y ofrece un selector visual. El backend rechaza HTTP 400
`HEALTH_RUNBOOK_INVALID` si una regla intenta referenciar un código inexistente.
Los pasos y enlaces no pueden ser inyectados desde el navegador.

## Recorrido real

En una organización QA aislada se recuperaron los 8 runbooks. Una petición con
`RUNBOOK_INVENTADO` fue rechazada con HTTP 400. Después se creó una regla de
latencia real de Google Cloud asociada a `PROVIDER_GOOGLE_CLOUD`; una medición de
84,56 ms abrió un incidente `external_provider`.

Playwright abrió el incidente y confirmó título, cuatro pasos, precaución y
enlace a Google Cloud Service Health. El incidente pasó realmente por
`OPEN → ACKNOWLEDGED → RESOLVED` al elevar el umbral y ejecutar una nueva
observación; conservó el código de runbook durante todo el ciclo.

## Pruebas y presentación

- Backend: **56/56 pruebas superadas**.
- Frontend: compilación Vite y lint sin errores; permanecen avisos heredados en
  componentes ajenos.
- Playwright/Chromium: escritorio y móvil sin overflow ni errores de consola.
- La inspección visual detectó y corrigió el estilo nativo del botón de cierre.

Los datos operativos QA se eliminaron y su usuario se deshabilitó al terminar.
La auditoría append-only y la organización raíz se conservaron.

## Seguridad, límites y rollback

Un runbook informa y guía: no reinicia servicios, elimina datos, termina
sesiones ni ejecuta remediación automática. En producción, responsables,
escalados, guardias y procedimientos propios del cliente deberán aprobarse.

Para revertir, retirar el visor y el endpoint, volver al código general
`INFRA_HEALTH_REVIEW` para nuevas reglas y conservar los códigos ya persistidos
hasta migrarlos de forma controlada. No hace falta revertir esquema.
