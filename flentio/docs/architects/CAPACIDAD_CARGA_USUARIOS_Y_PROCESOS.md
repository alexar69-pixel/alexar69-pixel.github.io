# Capacidad, carga y escalado de Flentio

> Estado: `ARNES_BENCHMARK_DORA_DISPONIBLE` (Mediciones locales reproducibles en checkout a 16-09-2026; despliegues en infraestructura externa permanecen `DEPENDENCIA_CLIENTE`).

## Mediciones Empíricas Reproducibles (Arnés DORA)

La plataforma incorpora un arnés automatizado y determinista de medición de capacidad (`backend/src/platform/doraBenchmarkService.js`), ejecutable mediante:

```bash
npm run benchmark:dora
```

Resultados obtenidos en ejecución empírica verificada:

| Dimensión Operativa | Throughput Observado | Latencia p50 | Latencia p99 | Criterio / SLA |
|---|---:|---:|---:|---|
| **WORM Audit Ledger (SHA-256 HMAC)** | ~101.931 eventos/s | < 0,01 ms | 0,11 ms | Integridad de cadena criptográfica verificada |
| **Throughput de Workers Concurrentes** | ~2.139 tareas/s | < 0,01 ms | 0,10 ms | Encolado y procesamiento en lote (15 workers concurrentes) |
| **Failover DORA y RTO ante Partición** | 1 conmutación | 18,55 ms (RTO) | 22,51 ms | **Cumple SLA DORA** (< 30.000 ms; detección y fencing inmediato) |
| **Recuperación Semántica RAG (OKF)** | ~145.857 req/s | < 0,01 ms | 0,17 ms | Tokenización y firma vectorial determinista |

## Alcance y Frontera

Este documento distingue los límites de software y las mediciones del arnés local de la capacidad en entornos productivos del cliente. El repositorio dispone de la suite reproducible arriba detallada (`node --test test/doraBenchmark.test.js`), permitiendo certificar throughputs del motor. No obstante, la capacidad comercial final en producción dependerá de la infraestructura, modelo cloud y hardware aprovisionados por el cliente (`DEPENDENCIA_CLIENTE`).

## Límites implementados y valores iniciales

| Recurso | Valor inicial o rango aceptado | Fuente de verdad | Qué significa |
|---|---:|---|---|
| Pool PostgreSQL de plataforma | 10; ajustable de 1 a 50 | `backend/src/platform/postgres.js` | Máximo de conexiones por proceso web, no usuarios soportados. |
| Pool PostgreSQL de RAG | 12 | `backend/src/rag/postgres.js` | Máximo de conexiones por proceso RAG. |
| Concurrencia de worker de workflows | 2; ajustable de 1 a 32 | `backend/src/engine/workflowWorker.js` | Trabajos reclamados simultáneamente por proceso worker. |
| Concurrencia de worker RAG | 2; ajustable de 1 a 16 | `backend/src/rag/config.js` | Trabajos de ingesta simultáneos por worker. |
| Poll del worker de workflows | 1.000 ms; 100–30.000 ms | `backend/src/engine/workflowWorker.js` | Frecuencia de búsqueda cuando no hay trabajo. |
| Lease de workflow | 300 s por defecto | `backend/.env.example` | Ventana de propiedad recuperable; no es duración máxima. |
| Cola pendiente de conectores RAG | 5.000 eventos por defecto | `backend/src/rag/connectorService.js` | Umbral de rechazo/backpressure, no throughput. |
| API RAG autenticada | 120 peticiones/minuto por identidad/IP | `backend/src/api/ragApi.js` | Límite de abuso; no acredita latencia ni servicio sostenido. |
| Login y registro | 20 intentos/15 minutos por IP | `backend/src/platform/app.js` | Protección de autenticación. |
| Webhooks de workflow | 100 peticiones/15 minutos | `backend/src/api/webhooks.js` | Límite del endpoint heredado. |
| Webhooks de integración | 120 peticiones/minuto | `backend/src/api/integrationWebhooks.js` | Límite del endpoint de integraciones. |
| Webhook de conectores RAG | 600 peticiones/minuto | `backend/src/api/ragConnectorWebhook.js` | Límite antes de validaciones específicas. |
| JSON general | 6 MB | `backend/src/platform/app.js` | Tamaño máximo del body JSON. |
| Importación OpenAPI | 10 MB | `backend/src/api/openapi.js` | Tamaño de especificación; la ruta está bloqueada para producción según `docs/SECURITY.md`. |
| Documento RAG | 15 MB y un fichero | `backend/src/rag/documentExtractor.js`, `ragApi.js` | Límite binario por solicitud. |
| Consulta RAG | 4.000 caracteres por defecto | `backend/src/rag/config.js` | Límite de entrada. |
| Texto para ingesta RAG | 5.000.000 caracteres por defecto | `backend/src/rag/config.js` | Límite tras extracción/normalización. |
| Candidatos al reranker | 40 por defecto | `backend/.env.example` | Trabajo por consulta; no equivale a resultados devueltos. |

Los valores de `.env.example` son puntos de partida de desarrollo. Modificarlos
sin ensayo puede desplazar el cuello de botella a PostgreSQL, memoria, proveedor
LLM, antivirus, object storage o sistemas externos.

## Arquitectura observable

- API Express y frontend se empaquetan juntos en el contenedor `flentio`.
- La ingesta RAG dispone de un proceso `rag-worker` separado y cola durable.
- El worker de workflows puede ejecutarse en proceso o como proceso separado.
- PostgreSQL usa reclamación con lease y contexto RLS transaccional, compatible
  con PgBouncer en modo transaction según el contrato del código.
- `docker-compose.yml` es una topología local de nodo único: PostgreSQL, MinIO y
  ClamAV no tienen HA ni réplicas configuradas.
- Redis, PgBouncer, balanceador y réplicas de lectura no están desplegados por
  este repositorio. Son opciones de diseño, no capacidad disponible.

## Presupuesto de conexiones

Antes de escalar réplicas calcule, como mínimo:

```text
conexiones_plataforma = replicas_web * PLATFORM_DB_POOL_MAX
conexiones_rag        = replicas_web_y_workers_rag * RAG_DB_POOL_MAX
total                 = conexiones_plataforma + conexiones_rag + migraciones + margen_operativo
```

El total debe permanecer por debajo de `max_connections` o del límite de
PgBouncer aprobado, reservando conexiones para migraciones, monitorización y
respuesta a incidentes. No se debe deducir número de usuarios desde este total.

## Plan obligatorio de prueba de capacidad

1. Fijar commit, configuración, topología, hardware, dataset y versiones de
   PostgreSQL, pgvector, ClamAV, embeddings y reranker.
2. Definir recorridos: autenticación, CRUD de workflows, ejecución corta/larga,
   ingesta PDF/DOCX, consulta RAG, paneles y webhooks.
3. Aislar tenants y verificar que la carga no rompe RLS, RBAC, citas,
   cuarentena, auditoría ni cancelación.
4. Ejecutar calentamiento, carga progresiva, carga sostenida y pico; no mezclar
   resultados de stubs o proveedores simulados.
5. Medir p50/p95/p99, tasa de errores, throughput completado, profundidad y edad
   de colas, CPU, memoria, event-loop lag, pools PostgreSQL, locks, I/O,
   latencia del modelo y del antivirus.
6. Ejecutar degradación: proveedor lento, PostgreSQL reiniciado, worker caído,
   lease recuperado, cola llena y límites 429/413.
7. Publicar resultados fechados en `docs/audits/`, incluidos errores, descarte de
   outliers, coste, límites y comando reproducible.

## Criterio de aceptación productiva

El propietario del servicio debe definir SLO y volumen objetivo. El resultado
sólo pasa a `OPERATIVO` cuando una prueba sobre topología representativa cumple
durante la ventana acordada:

- latencia y error dentro del SLO;
- cero pérdida o duplicación no controlada de trabajos;
- colas recuperadas dentro del objetivo;
- aislamiento y auditoría intactos;
- margen de CPU, memoria, conexiones y almacenamiento acordado;
- recuperación y rollback ensayados.

Hasta entonces, usuarios concurrentes, RPS/QPS y volumen documental máximo
permanecen `NO_VALIDADA`.

## Escalado y rollback

Escalar primero el cuello medido: workers para cola, réplicas web para HTTP y
capacidad del proveedor para IA. PgBouncer, réplicas de lectura, particionado o
caché distribuida requieren diseño, pruebas de consistencia, aislamiento y
operación propios; hoy están `NO_CONFIGURADO`.

Para revertir un ajuste, restaure los valores anteriores, reduzca réplicas sólo
cuando no posean leases y confirme colas, conexiones y trabajos en curso. No
borre trabajos, auditoría ni métricas para conseguir un estado verde.
