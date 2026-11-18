# Salud y observabilidad de infraestructura

## Objetivo y estado

Estado: **OPERATIVO en desarrollo local** desde el 01-08-2026.

La pestaña **Administración → Salud del Servidor** reúne comprobaciones reales,
historial por organización, reglas de alerta no-code, incidentes y exportación
de métricas. No ejecuta reparación automática, no acepta hosts o comandos desde
el navegador y no presenta muestras inexistentes como cero.

## Arquitectura y seguridad

`GET /api/admin/health-diagnostic` realiza una observación y la persiste en
PostgreSQL. El monitor interno repite la recogida cada cinco minutos por defecto.
La migración `014_infrastructure_observability.sql` crea:

- `infrastructure_health_snapshots`, con métricas numéricas agregadas;
- `external_provider_observations`, sin credenciales ni contenido de clientes;
- `health_alert_rules`, limitadas a un catálogo de métricas y operadores;
- `health_incidents`, con apertura, reconocimiento, resolución y deduplicación.

Las cuatro tablas aplican RLS por organización. Los índices combinan tenant y
tiempo; reglas activas e incidentes abiertos usan índices parciales. Cada
persistencia usa una transacción corta y las llamadas HTTPS se realizan antes
o después de ella. La función `health_collection_targets()` sólo entrega al
monitor el tenant y un administrador habilitado; no omite RLS para leer datos.

Se conservan 30 días por defecto. La limpieza elimina snapshots antiguos y sus
observaciones hijas. No elimina incidentes ni auditoría.

## Fuentes locales comprobadas

| Dominio | Comprobación real | Ausencia o fallo |
| --- | --- | --- |
| Host y proceso | API `os` y métricas del proceso Node.js. | `SIN_DATOS` cuando no existe valor numérico. |
| Almacenamiento | `statfs` sobre el volumen del backend. | `NO_DISPONIBLE` si no puede leerse. |
| Docker | Comando fijo `docker info`, timeout 4 s. | `NO_DISPONIBLE`; nunca se inventan contenedores. |
| PostgreSQL | Versión, tamaño, conexiones, cache hit, latencia y pools. | `NO_CONFIGURADO` o `NO_DISPONIBLE`. |
| RAG | pgvector, ClamAV, MinIO, reranker y conectores del tenant. | Estado explícito por dependencia. |
| Plataforma | Worker, scheduler, bóveda y escritor/outbox de auditoría. | Estado real del proceso. |

## Proveedores externos integrados

Las URL son fijas en el backend, sólo HTTPS, timeout 6 s y caché de 60 s. El
fallo de una fuente se registra como `NO_DISPONIBLE`; no hay respuesta de
respaldo simulada.

| Proveedor | Fuente oficial y lectura | Alcance que no debe inferirse |
| --- | --- | --- |
| Google Cloud | `https://status.cloud.google.com/incidents.json`; incidencias públicas globales activas. | La salud de proyectos concretos es `DEPENDENCIA_CLIENTE` y requiere Personalized Service Health, identidad y proyecto del cliente. |
| Banco de España | API JSON de estadísticas, serie pública `D_1NBAF472`; valida código, frecuencia y fecha publicada. | Disponibilidad de una serie no garantiza todos los servicios del Banco de España ni vigencia normativa. |
| CISA KEV | Catálogo JSON oficial y número real de vulnerabilidades. | La afectación de activos Flentio permanece `NO_EVALUADO` hasta correlacionar inventario y versiones. |

El panel enlaza cada fuente oficial para permitir verificación humana.

Cada proveedor integrado expone dos señales alertables: disponibilidad y
latencia. La disponibilidad se guarda internamente como `1` tras una respuesta
operativa y `0` tras una degradación o indisponibilidad comprobada; si nunca se
observó, permanece `SIN_DATOS`. El formulario oculta esta codificación y ofrece
la condición **Alertar cuando no esté operativo**. También muestra la hora de la
comprobación actual y el último contacto satisfactorio persistido.

## Otras opciones de mercado

No están integradas y requieren decisión y, cuando corresponda, credenciales
del cliente:

| Categoría | Opciones | Ventajas | Costes o límites |
| --- | --- | --- | --- |
| Salud cloud | AWS Health, Azure Service Health, Google Personalized Service Health | Incidentes asociados a cuenta, región y recursos. | Identidad cloud, permisos mínimos, residencia, cuota y dependencia del proveedor. |
| Información monetaria | BCE Data API, Banco de España | Fuentes primarias para tipos, agregados y series europeas/españolas. | Contratos y esquemas distintos; una API disponible no valida la semántica de una serie. |
| Regulación/mercado | EUR-Lex, EBA, ESMA, CNMV, Eurostat | Cobertura normativa, supervisora y estadística oficial. | Frecuencias, licencias, metadatos y políticas de cambio diferentes; requieren conectores gobernados. |
| Amenazas | CISA KEV, NVD, ENISA y feeds comerciales | Mejor cobertura y enriquecimiento. | Duplicados, latencia, licencias y necesidad de correlación con inventario/SBOM. |
| Observabilidad | Prometheus/Grafana, OpenTelemetry Collector, Datadog, Dynatrace, Azure Monitor, CloudWatch, Google Cloud Operations | Desde portabilidad abierta hasta suites gestionadas. | Operación propia o coste, residencia, retención y lock-in. |

Añadir un proveedor exige un adaptador backend con URL permitida, parser de
esquema, timeout, pruebas, documentación y clasificación explícita del alcance.
No se aceptan endpoints arbitrarios introducidos desde la interfaz.

## Reglas e incidentes

El formulario no-code permite nombre, métrica autorizada, operador, umbral,
severidad, muestras consecutivas, cooldown y código de runbook. Sólo se admiten
CPU, memoria, disco, heap, uso/latencia de conexiones PostgreSQL y fallos del
escritor de auditoría, además de disponibilidad/latencia de los tres proveedores
instalados. Las claves de proveedor están en una allowlist de código; añadir una
URL no crea automáticamente una métrica ni una regla.

Una regla abre un incidente sólo tras el número de muestras consecutivas. La
huella por regla evita duplicados; una nueva muestra actualiza valor, contador y
fecha. Cuando deja de cumplirse se resuelve. Desactivar la regla resuelve sus
incidentes activos en la misma transacción. Reconocer un incidente no lo cierra;
la recuperación de la métrica lo resuelve. Todas las transiciones se auditan.

Los umbrales locales son configuración de desarrollo, no SLO bancarios. El
cliente debe proporcionar BIA, severidades, guardias, canales y objetivos
contractuales antes de producción.

## API y exportación

Todas las rutas siguientes exigen JWT y rol administrador:

- `GET /api/admin/infrastructure-health/history?hours=24&limit=240`
- `GET|POST /api/admin/infrastructure-health/rules`
- `GET /api/admin/infrastructure-health/runbooks`
- `PUT /api/admin/infrastructure-health/rules/{id}`
- `GET /api/admin/infrastructure-health/incidents`
- `POST /api/admin/infrastructure-health/incidents/{id}/acknowledge`
- `GET /api/admin/infrastructure-health/prometheus`
- `GET /api/admin/infrastructure-health/otel`

Prometheus se descarga en formato de texto bajo autenticación. OTLP HTTP/JSON es
opcional. Fuera de localhost exige HTTPS y allowlist; el bearer token sólo se
lee del entorno y nunca se devuelve al frontend.

```dotenv
INFRA_HEALTH_MONITOR_ENABLED=true
INFRA_HEALTH_INTERVAL_MS=300000
INFRA_HEALTH_RETENTION_DAYS=30
OTEL_EXPORTER_OTLP_ENDPOINT=
OTEL_EXPORTER_HOST_ALLOWLIST=
OTEL_EXPORTER_OTLP_BEARER_TOKEN=
```

Vacío significa `NO_CONFIGURADO`, no un envío correcto. Para producción se
recomienda apuntar OTLP a un Collector gobernado en vez de acoplar Flentio al
backend final; esa elección queda abierta.

## Operación y runbook

Flentio incluye ocho runbooks versionados para host, PostgreSQL, RAG, auditoría
y proveedores externos. El selector recomienda uno según la métrica. Desde un
incidente, **Ver runbook** muestra alcance, pasos, precauciones y fuente oficial.
El backend rechaza códigos inexistentes: una etiqueta sin procedimiento real no
puede guardarse. Los runbooks no ejecutan remediación automática.

1. Abrir **Administración → Salud del Servidor** y actualizar.
2. Revisar timestamp, monitor, estado global y fuente concreta.
3. Distinguir estado público de proveedor y salud personalizada del cliente.
4. Comparar **Última comprobación** con **Último contacto satisfactorio**. Si la
   segunda no existe, el panel muestra `SIN DATOS`, no una fecha inventada.
5. Consultar el historial; dos muestras son el mínimo para una tendencia.
6. Para una alerta de disponibilidad, seleccionar el proveedor y confirmar
   muestras consecutivas, severidad, cooldown y runbook. Para latencia se define
   además un umbral medido en milisegundos.
7. Reconocer significa que una persona la ha visto; confirmar recuperación real
   antes de darla por resuelta.
8. Verificar una incidencia con la consola oficial del proveedor antes de una
   actuación destructiva.
9. Abrir **Ver runbook**, seguir los pasos de diagnóstico y respetar sus
   precauciones. Reconocer el incidente sólo después de asumir su seguimiento.

## Rollback

1. Desactivar el monitor con `INFRA_HEALTH_MONITOR_ENABLED=false` y reiniciar.
2. Desactivar reglas desde el panel; esto resuelve incidentes activos y deja
   trazabilidad.
3. Retirar el endpoint OTLP para detener exportación sin perder historial.
4. Revertir backend/frontend si fuera necesario. No modificar la migración 014
   ya aplicada ni borrar auditoría. Una reversión de esquema requiere una nueva
   migración revisada y ventana de cambio.

## Límites

La validación local no acredita HA, failover, carga, capacidad bancaria,
disponibilidad contractual, RPO/RTO, guardias ni cumplimiento. El monitor local
no sustituye observabilidad externa: si el proceso o emplazamiento completo cae,
no puede informar de su propia caída. La revisión independiente de seguridad y
cumplimiento sigue pendiente para producción.
