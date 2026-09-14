# Semántica de estados operativos

## Objetivo

Flentio distingue ausencia de configuración, ausencia de observaciones y un
valor cero confirmado. La interfaz no transforma valores nulos en ceros ni
presenta como activa una integración que sólo tenga una tarjeta visual.

## Estados

| Estado | Significado verificable | Ejemplo |
| --- | --- | --- |
| `OPERATIVO` | La fuente respondió correctamente. | Catálogo público CISA KEV recuperado. |
| `SIN_DATOS` | La capacidad puede recibir datos, pero todavía no existen observaciones. | No se ha ejecutado un escaneo CPD autorizado. |
| `0` | Una consulta real ejecutada devolvió cero. | PostgreSQL no contiene trabajos pendientes para la organización. |
| `NO_CONFIGURADO` | Falta implementar o configurar una capacidad propia de Flentio. | No existe proveedor real para un nodo de workflow. |
| `DEPENDENCIA_CLIENTE` | La decisión, credencial, política o fuente corresponde al despliegue del cliente. | Modelo de ROI, Venafi, Vault PKI o SIEM. |
| `NO_DISPONIBLE` | La fuente está configurada o es pública, pero no respondió. | CISA KEV supera el timeout o devuelve un error. |
| `NO_EVALUADO` | Hay información externa, pero no se ha correlacionado con activos locales. | Una entrada CISA KEV no demuestra afectación de Flentio. |

## Reglas de implementación

- `null` o ausencia de observaciones se representa como `SIN_DATOS`, nunca `0`.
- El valor `0` exige una consulta o medición real y trazable.
- La disponibilidad de un feed externo no demuestra exposición local.
- Las dependencias productivas que aportará el cliente no bloquean el desarrollo
  local y se muestran como `DEPENDENCIA_CLIENTE`.
- Un error de red no se presenta como ausencia de datos: se muestra
  `NO_DISPONIBLE`.

## Aplicación actual

El resumen de plataforma obtiene conteos de workflows, ejecuciones, incidentes y
cola desde PostgreSQL. Consulta CISA KEV mediante HTTPS con timeout de cinco
segundos y caché en memoria de quince minutos. Certificados y descubrimiento CPD
permanecen `SIN_DATOS` hasta que se ejecute una inspección real. La correlación
entre CISA y activos de Flentio permanece `NO_EVALUADO`.

La pestaña administrativa de salud aplica el mismo contrato a host, disco,
Docker, PostgreSQL, RAG y workers. Detalle: `docs/admins/PLATFORM_INFRASTRUCTURE_HEALTH.md`.

Desde la migración 014, también persiste series reales y observaciones de
Google Cloud, Banco de España y CISA KEV. Las tendencias requieren al menos dos
muestras. Una API pública operativa no demuestra la salud personalizada de una
cuenta cloud ni la afectación local por una vulnerabilidad: se conservan
`DEPENDENCIA_CLIENTE` y `NO_EVALUADO`, respectivamente. Las reglas sólo admiten
métricas agregadas en allowlist; sus incidentes se abren, reconocen y resuelven
con evidencia persistida y auditoría.

La disponibilidad y latencia de los tres proveedores instalados ya forman parte
de esa allowlist. El panel presenta una condición no-code de indisponibilidad y
calcula el último contacto satisfactorio mediante observaciones RLS; la ausencia
histórica sigue siendo `SIN_DATOS`.

## Rollback

La semántica no modifica datos persistidos. Para revertir la presentación se
puede desplegar la versión anterior del frontend y del endpoint de resumen; no
deben inventarse ceros durante el rollback ni eliminarse eventos de auditoría.
