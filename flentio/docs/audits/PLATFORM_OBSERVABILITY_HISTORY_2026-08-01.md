# Evidencia local: historial, alertas y proveedores externos

Fecha: 01-08-2026. Alcance: desarrollo local, sin datos de clientes.

## Implementación inspeccionada

- Migración PostgreSQL 014 aplicada con RLS, índices tenant/tiempo e índices
  parciales para reglas e incidentes activos.
- Monitor periódico con exclusión de ejecuciones solapadas y cierre elegante.
- Comprobaciones HTTPS de Google Cloud, Banco de España y CISA KEV mediante
  endpoints oficiales fijos, timeout y validación de esquema.
- Historial, reglas no-code, incidentes, Prometheus y exportador OTLP opcional.
- El frontend no transforma `null` en cero y exige dos observaciones para una
  tendencia.

## Evidencia automatizada

Comandos:

```powershell
cd backend
npm test
cd ../frontend
npm run build
```

Resultado: **52/52 pruebas superadas** y compilación Vite correcta. Las pruebas
validan parsers, rechazo de métricas arbitrarias y payload OTLP numérico. Los
dobles sólo existen dentro de tests y no sustituyen las comprobaciones de
producción.

## Validación integrada

Se creó una organización QA aislada mediante la API real de registro y se
autenticó con JWT. El flujo obtuvo estos resultados:

| Evidencia | Resultado |
| --- | --- |
| Historial | 3 snapshots PostgreSQL del tenant. |
| Google Cloud | `OPERATIVO`, endpoint público oficial. |
| Banco de España | `OPERATIVO`, serie oficial con fecha publicada. |
| CISA KEV | `OPERATIVO`, catálogo oficial. |
| Regla CPU `>= 0`, una muestra | Abrió 1 incidente real. |
| Reconocimiento | `OPEN` → `ACKNOWLEDGED`. |
| Umbral actualizado a 101 | `ACKNOWLEDGED` → `RESOLVED` en la observación siguiente. |
| Prometheus | Incluyó timestamp y métricas numéricas persistidas. |
| OTLP sin destino | `NO_CONFIGURADO`, sin declarar entrega. |

Playwright real abrió la SPA, inició sesión, navegó al centro administrativo y
validó el panel a 1440 × 1000 y 390 × 844. No detectó overflow horizontal ni
errores de consola. La inspección visual confirmó tarjetas, proveedores,
historial y formulario sin solapamiento. Las capturas se guardaron fuera del
repositorio en el directorio temporal local.

El wrapper Linux disponible no pudo ejecutarse en Windows por ausencia de
`/bin/bash`; se utilizó Playwright 1.62.1 directamente, con Chromium real.

Al terminar se eliminaron 32 filas operativas QA, incluidas muestras, reglas e
incidentes, y se deshabilitaron los dos usuarios temporales. Los eventos de
auditoría append-only y sus organizaciones raíz se conservaron deliberadamente:
la limpieza no desactiva controles de inmutabilidad para ocultar una prueba. No
se usaron datos de clientes.

## Conclusión

Resultado: **VALIDACIÓN LOCAL INTEGRAL SUPERADA**. La evidencia confirma el
comportamiento funcional local, no HA, carga, SLO, RPO/RTO ni producción
bancaria.

## Rollback

Desactivar monitor y reglas, retirar OTLP y desplegar la versión previa. No
editar la migración aplicada ni eliminar incidentes o auditoría.
