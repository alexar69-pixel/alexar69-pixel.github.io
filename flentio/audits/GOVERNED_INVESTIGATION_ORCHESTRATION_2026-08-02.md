# Evidencia local del orquestador gobernado de investigaciones

Fecha: 02-08-2026. Alcance: evidencia técnica local; no es homologación bancaria,
prueba productiva ni acreditación de conexión con sistemas del cliente.

## Resultado

| Control | Evidencia | Resultado |
|---|---|---|
| Regresión backend | `npm test` | 215/215 |
| Persistencia | `npm run migrate:platform` dos veces | PostgreSQL 16.14, `OPERATIVO`, hasta 023 |
| Carga estructural | 1.200 referencias sintéticas de prueba | 273 ms, presupuesto 2,5 s |
| M2 estructural | `npm run evaluate:m2:structural` | `STRUCTURE_VALID_NO_BANKING_HOMOLOGATION` |
| Dependencias | `npm audit --audit-level=high` en backend y frontend | 0 vulnerabilidades reportadas |
| Secretos | `node scripts/scan-secrets.js` | 655 archivos, sin patrón de alta confianza |
| Frontend | build Vite y lint | build correcto; lint sin errores, advertencias históricas |
| QA visual | Playwright, escritorio y 390×844 | flujo completo, sin errores de consola |

Hash del dataset estructural no bancario:
`68f7799cdba35daf4d6162d7643f54ccabff1ba23030ec34559f54be54f7a710`.
Sus siete casos son referencias estructurales no ejecutables, marcadas
`NO_BANCARIO_NO_HOMOLOGABLE`; no contienen incidentes ni datos bancarios.

## Controles funcionales

El orquestador admite únicamente collectors en allowlist, opera en lectura,
aplica timeout y concurrencia acotada y no devuelve payloads ni tenant en el
resultado. Si ninguna fuente completa, devuelve `EVIDENCIA_INSUFICIENTE` aunque
todas fueran opcionales. La correlación exige servicio, entorno y ventana; una
proximidad sólo es `TEMPORALLY_ADJACENT_NOT_CAUSAL`. Las hipótesis son candidatas
deterministas, conservan referencias y nunca establecen causalidad. Los conflictos
se limitan a atributos permitidos y reducen la confianza.

La UI exige confirmación antes de investigar y antes de registrar una revisión.
Las revisiones son inmutables, una por actor; otros revisores autorizados pueden
añadir la suya. En QA se verificaron tres eventos, tres relaciones, una hipótesis
contradicha, una contradicción y una revisión `NEEDS_MORE_EVIDENCE`. Los registros
sintéticos de QA se eliminaron con una transacción exacta y no son recuperables;
la auditoría se conservó.

## Rendimiento, seguridad y release

La división manual y carga diferida redujeron el chunk principal desde unos
1.504 kB a 224 kB minificados. Permanece un chunk de iconos de 643 kB debido al
catálogo dinámico histórico de Lucide; es deuda de rendimiento conocida, no se
oculta elevando el umbral. CI instala desde lockfiles, ejecuta pruebas, evaluador,
auditoría de dependencias, escaneo de secretos, build, lint y genera un manifiesto
de evidencias con hashes. Estos controles son dirigidos al cambio y no equivalen
a un pentest ni a un análisis exhaustivo del repositorio.

## R1 y rollback

`r1.preprod.restart_workload.v1` sólo construye un plan PREPROD/R1 con baseline,
máximo indisponible uno y rollback `RESTORE_REPLICA_BASELINE`; `execute()` arroja
siempre `M3_EXECUTION_BLOCKED`. No existe endpoint de ejecución. Para revertir la
entrega se deshabilitan las rutas de orquestación, se retira la UI y se revierte
022/023 mediante un cambio de base aprobado; nunca se eliminan expedientes o
auditoría sin la política de retención.

Capturas locales: `output/playwright/governed-investigation-desktop.png` y
`output/playwright/governed-investigation-reviewed-mobile.png`.
