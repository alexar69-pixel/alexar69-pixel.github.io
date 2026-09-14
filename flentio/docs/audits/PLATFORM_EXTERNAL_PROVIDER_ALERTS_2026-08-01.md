# Evidencia local: alertas de proveedores externos

Fecha: 01-08-2026. Alcance: desarrollo local sin datos de clientes.

## Cambio verificado

El catálogo cerrado de métricas admite disponibilidad y latencia de Google
Cloud, Banco de España y CISA KEV. Una respuesta satisfactoria produce
disponibilidad `1`; una degradación o indisponibilidad comprobada produce `0`;
la ausencia de observación permanece `null`/`SIN_DATOS`.

La interfaz traduce la disponibilidad a **Alertar cuando no esté operativo** y
no expone el valor 0/1 al administrador. También muestra última comprobación y
último contacto satisfactorio. Este último se calcula en PostgreSQL dentro del
tenant y permite distinguir un fallo actual de una fuente que nunca respondió.

No fue necesaria una migración: las métricas versionables ya se almacenan en el
JSONB de snapshots y el índice compuesto de la migración 014 cubre tenant,
proveedor y tiempo. Las claves permitidas continúan definidas en código; no se
aceptan rutas arbitrarias del navegador.

## Recorrido real

Se creó una organización QA aislada y se ejecutaron cuatro observaciones contra
los endpoints oficiales. Google Cloud respondió con una latencia medida de
96,65 ms. Una regla temporal `latencia >= 0` abrió un incidente con fuente
`external_provider`. Al actualizar el umbral a 1.000.000.000 ms, la siguiente
observación lo resolvió. El incidente conservó el umbral histórico que motivó
su apertura.

Se creó además una regla de disponibilidad `Google Cloud no operativo`, con dos
muestras consecutivas. Como ambas comprobaciones reales fueron operativas, se
registraron **0 incidentes**; no se simuló una caída.

## Pruebas y pantalla

- Backend: **53/53 pruebas superadas**.
- Frontend: compilación Vite correcta.
- Playwright/Chromium: regla visual, último contacto satisfactorio, escritorio
  y móvil sin overflow horizontal ni errores de consola.
- La inspección visual detectó y corrigió dos defectos antes de aceptar: texto
  de condición estrecho y operador ausente en el historial de incidentes.

La organización QA produjo 4 snapshots, 2 reglas y 1 incidente resuelto. Al
terminar se eliminaron sus filas operativas y se deshabilitó el usuario. La
auditoría append-only y la organización raíz se conservaron deliberadamente.

## Límites y rollback

La prueba valida la mecánica y fuentes públicas, no una caída real de Google,
un SLO contractual ni salud personalizada de proyectos cloud. Para revertir,
se retiran las seis claves `provider.*` del catálogo y del selector; las
observaciones JSONB históricas pueden conservarse. No se modifica ni revierte
la migración 014.
