# Revisión de símbolos indefinidos del frontend — 2026-09-07

## Motivo

La vista de plantillas fallaba en tiempo de ejecución porque `Dashboard.jsx`
usaba `templateTotal` y otros estados de paginación que habían desaparecido
durante una refactorización parcial.

## Corrección

`frontend/src/Dashboard.jsx` vuelve a declarar y alimentar desde `getTemplates`
los estados `templateResults`, `templateTotal`, `templatePage`,
`templateCategory` y `templateSearchInput`. La carga aplica paginación local,
espera breve para la búsqueda, descarte de respuestas obsoletas y estado vacío
ante error. También se retiró el import no utilizado de `TemplatesView`.

## Validaciones ejecutadas

- `npm.cmd run lint`: completado sin errores `no-undef` ni `jsx-no-undef`.
- Búsqueda de `ReferenceError`, `is not defined` y referencias de la galería:
  no se encontraron más fallos equivalentes.
- `node --check` sobre los 177 archivos JavaScript de `backend/src`:
  completado sin errores sintácticos.
- `npm.cmd run build`: compilación Vite completada correctamente.

## Riesgos no confundidos con este defecto

Oxlint mantiene advertencias preexistentes por imports/variables sin uso y
dependencias de hooks en algunos componentes. No equivalen a símbolos
indefinidos y no se modificaron sin una prueba funcional específica. El build
mantiene el aviso conocido de chunks superiores a 500 kB. Esta revisión es
estática y de compilación; no sustituye una navegación completa en navegador de
todas las rutas y estados dependientes de servicios externos.

## Verificación del despliegue

Tras la primera compilación local, `http://localhost:3000` seguía entregando el
bundle antiguo `assets/index-CTvaM1H8.js`; por eso el navegador continuaba
mostrando `templateTotal is not defined`. El servicio activo pertenecía a
`docker-compose.demo.yml`, no al Compose principal. Se reconstruyó únicamente
`demo-app` con `.env.demo`, sin modificar secretos ni los servicios de datos.
Después del reemplazo, el servidor entrega `assets/index-KLnQxXAG.js`,
`GET /api/health` responde HTTP 200 y el contenedor figura activo.
