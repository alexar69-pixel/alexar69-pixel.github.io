# Evidencia — Centro de Control Ejecutivo

Fecha: 02-08-2026. Estado: `VALIDACION_LOCAL`.

## Alcance verificado

- Endpoint admin tenant-aware `GET /api/admin/executive-dashboard`.
- Ventana explícita de 24 horas UTC.
- Conteos PostgreSQL de workflows, ejecuciones, investigaciones, revisiones,
  incidentes, auditoría y configuración de Integration Skills.
- Inventario versionado con diez áreas `COVERED` y M2/M3 `PARTIAL`.
- Drill-down desde métricas, alertas e inventario hasta el panel responsable.
- Ejecución preservada como `BLOCKED_NO_EXECUTION`.

La prueba contra PostgreSQL del stack Docker devolvió esquema
`FLENTIO_EXECUTIVE_DASHBOARD_V1`, 29 Skills, 10 áreas cubiertas, 2 parciales,
fuente de plataforma `OBSERVED` e integraciones `NO_CONFIGURADO`.

## Validación

- Backend: 226/226 pruebas correctas tras añadir los cuadros especializados.
- Frontend: build correcto; chunk diferido del componente de 5,45 kB.
- Lint: sin errores; permanecen advertencias históricas fuera del componente.
- Docker: reconstrucción limpia y endpoint autenticado correcto.
- Navegador real: 1440x1000 y 390x844.
- Móvil: `scrollWidth=390`, `clientWidth=390`.
- Consola: cero errores y cero advertencias durante el recorrido.
- Interacción: la alerta de integraciones abrió el catálogo correspondiente.

Capturas: `output/playwright/executive-dashboard-desktop.png` y
`output/playwright/executive-dashboard-mobile.png`.

## Límites y rollback

Los ceros visibles proceden de consultas reales dentro de la ventana; los datos
desconocidos de paneles existentes continúan como `SIN_DATOS`. Configuración no
equivale a validación y no se calcula ROI, SLA o ahorro. M2 necesita dataset
bancario y revisión independiente; M3 permanece bloqueado.

El rollback elimina el componente y la ruta agregada. No hay migración ni estado
nuevo que revertir. Los paneles fuente y la norma transversal permanecen.

## Extensión especializada

Se añadieron cinco pestañas: Operaciones, Automatización, Integraciones, RAG y
conocimiento, y Seguridad y gobierno. Todas reutilizan el snapshot autenticado;
el backend calcula configuración por categoría desde las claves tenant-aware.
La comprobación real devolvió `OBSERVED`, `SIN_DATOS` y tres
`NO_CONFIGURADO`, respectivamente. No se fabricó actividad RAG o de seguridad.

QA adicional: navegación entre RAG y Seguridad, escritorio 1440x1100, móvil
390x844 sin overflow y consola sin errores ni advertencias. Evidencia:
`output/playwright/specialized-dashboards-desktop.png` y
`output/playwright/specialized-dashboards-mobile-detail.png`.
