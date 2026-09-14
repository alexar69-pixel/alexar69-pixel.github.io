# Revisión integral de documentación — 05-09-2026

## Alcance y método

Se inventariaron los Markdown del repositorio y se contrastaron los documentos
principales con rutas, middleware, configuración, workers, pools, límites y
`docker-compose.yml`. Se comprobó la resolución de enlaces locales Markdown.
La revisión es estática: no acredita proveedores, infraestructura cliente,
seguridad ofensiva ni capacidad productiva.

## Resultado

- Se creó una referencia transversal de seguridad con controles, dependencias y
  bloqueos de producción: `docs/SECURITY.md`.
- Se sustituyeron cifras de capacidad no sustentadas por límites observables y
  un protocolo reproducible de benchmark.
- Se incorporaron seguridad, capacidad y esta revisión a los índices principales.
- Los documentos históricos de `docs/audits/` se conservan como evidencia
  fechada; no se reescriben para aparentar vigencia actual.
- Estrategia, ventas y visión describen hipótesis o posicionamiento y no
  sustituyen validación técnica, de mercado o del cliente.

## Hallazgos que afectan a afirmaciones del corpus

| Hallazgo | Clasificación documental |
|---|---|
| SDK y sidecar heredados responden contenido marcado `X-Flentio-Simulated` y se montan sin autenticación | `NO_DISPONIBLE` para operación; bloqueo de producción |
| Importador OpenAPI se monta sin autenticación | `NO_VALIDADA`; bloquear externamente hasta corregir y probar |
| No existe benchmark reproducible para usuarios, RPS/QPS o workflows/s | Toda cifra de capacidad productiva queda `NO_VALIDADA` |
| Compose es una pila local de nodo único | No acredita HA, SLO, DR ni topología bancaria |
| Adaptadores instalados o manifiestos | No implican credenciales, conectividad, activación ni homologación |
| Evidencias locales fechadas | Sólo acreditan el alcance y entorno escritos en cada acta |

## Política de lectura del corpus

1. Código, migraciones y configuración definen el comportamiento actual.
2. `docs/audits/` prueba únicamente una ejecución fechada y acotada.
3. `docs/strategy/`, ventas, presentaciones, plantillas y `okf-bundle/` no son
   evidencia de disponibilidad operativa.
4. Ante contradicción, aplicar el estado más conservador y abrir una corrección.
5. Los términos `OPERATIVO`, `NO_CONFIGURADO`, `NO_DISPONIBLE`, `NO_VALIDADA`,
   `DEPENDENCIA_CLIENTE` y `NO_BANCARIO` siguen `docs/INDEX.md` y
   `docs/PLATFORM_OPERATIONAL_STATUS.md`.

## Trabajo pendiente

- Corregir o retirar las rutas simuladas señaladas; este cambio documental no
  modifica su implementación.
- Incorporar autenticación/RBAC al importador OpenAPI antes de exponerlo.
- Ejecutar pruebas de carga sobre topología representativa y publicar resultados.
- Realizar revisión independiente de seguridad, pentest y validación de DR/HA.
- Revisar afirmaciones competitivas con fuentes externas vigentes en una tarea
  de investigación separada; no se consideraron confirmadas por esta auditoría.

## Repetición

Ejecutar pruebas y build según `docs/developers/CONTRIBUTING.md`. Comprobar
enlaces relativos de todos los Markdown y registrar el conteo y cualquier
excepción. La ausencia de enlaces rotos no demuestra exactitud funcional.

## Validación ejecutada

| Comprobación | Resultado |
|---|---|
| Enlaces relativos en Markdown (excluido `node_modules`) | 0 enlaces rotos |
| `backend: npm test` | 351/351 pruebas correctas |
| `frontend: npm run build` | Correcto; advertencia de chunk de iconos superior a 500 kB |
| `frontend: npm run lint` | Código de salida 0; conserva avisos preexistentes, incluidos símbolos JSX no definidos |

La suite contiene pruebas y mensajes de recorridos sandbox. Su aprobación no
convierte las rutas SDK/Sidecar simuladas en funcionalidad operativa ni acredita
servicios externos.
