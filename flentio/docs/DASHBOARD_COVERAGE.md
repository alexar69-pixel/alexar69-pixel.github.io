# Cobertura de cuadros de mando

El inventario incluye el cuadro especializado `ai_usage` para consumo real de OpenAI/Gemini y Prompt Caching. Muestra `NO_VERIFICADO` cuando el proveedor no aporta contadores o falta una tarifa contractual; no estima ahorros.

Estado verificado: 02-08-2026. Fuente ejecutable:
`backend/src/platform/executiveDashboardService.js`.

| Área | Superficie | Estado | Límite actual |
| --- | --- | --- | --- |
| Control ejecutivo | Administración / Overview | `COVERED` | Agrega observaciones; no sustituye los paneles fuente |
| Workflows | Dashboard de flujos | `COVERED` | ROI y ahorro dependen del cliente |
| Operación SRE | Telemetría | `COVERED` | Remediación automática no configurada |
| Infraestructura | Salud, alertas y runbooks | `COVERED` | HA/SLO productivos no homologados |
| Investigaciones | Expediente gobernado | `COVERED` | Fuentes del cliente no configuradas |
| Integraciones | Catálogo de Skills | `COVERED` | Configuración no demuestra conectividad |
| RAG | Operación e ingesta RAG | `COVERED` | Proveedores productivos pendientes |
| Identidad y auditoría | Administración | `COVERED` | SIEM/WORM externo pendiente |
| Seguridad | Certificados y SOC | `COVERED` | Proveedores del cliente pendientes |
| Demo | Centro de Demostración | `COVERED` | Sintético, no bancario, no productivo |
| Consumo IA | Consumo y Prompt Caching | `COVERED` | Ahorro no verificado sin tarifa contractual |
| Homologación M2 | Investigaciones | `PARTIAL` | Dataset bancario y revisión independiente pendientes |
| Preparación M3 | Investigaciones | `PARTIAL` | `BLOCKED_NO_EXECUTION` |

El endpoint `GET /api/admin/executive-dashboard` calcula métricas tenant-aware
desde PostgreSQL con ventana UTC de 24 horas: workflows, ejecuciones,
investigaciones, revisiones, incidentes, auditoría y estados de configuración de
las Integration Skills. También publica el inventario de cobertura versionado.

La interfaz no transforma ausencia en cero operativo: las métricas cuya consulta
demuestra un conteo cero pueden mostrar `0`; las métricas desconocidas o externas
usan estados explícitos. Toda tarjeta y alerta ofrece drill-down al panel
responsable. M2 y M3 permanecen parciales hasta que existan las evidencias que no
pueden fabricarse sin cliente.

## Cuadros especializados

El Centro Ejecutivo incorpora cinco vistas con pestañas sobre el mismo snapshot,
sin crear cascadas de peticiones:

- Operaciones: incidentes activos/críticos e investigaciones abiertas.
- Automatización: workflows, ejecuciones y éxito observado; sin estimar ROI.
- Integraciones: configuración, validación, activación y carencias por categoría.
- RAG y conocimiento: cobertura de proveedores IA/RAG e ITSM; la actividad RAG
  se mantiene `NO_DISPONIBLE_EN_RESUMEN` hasta integrar su contrato específico.
- Seguridad y gobierno: auditoría, incidentes críticos y proveedores de
  seguridad, secretos, identidad y plataforma.

Cada vista expone estado, límites y un botón al cuadro detallado. En móvil las
pestañas son desplazables horizontalmente y el contenido se apila sin perder el
contexto temporal ni la frontera `BLOCKED_NO_EXECUTION`.

El cuadro independiente `ai_usage` consulta el endpoint tenant-aware de consumo,
con ventanas de 24 horas y 7 días. Su contrato se describe en
`docs/MODEL_USAGE_DASHBOARD.md`.

## Rollback

Retirar el componente `ExecutiveControlCenter` y la ruta agregada devuelve el
Overview anterior sin modificar datos ni esquemas. El inventario no persiste
estado y no habilita ejecución. No debe eliminarse el estándar transversal
`docs/DASHBOARD_STANDARD.md` durante un rollback funcional.
