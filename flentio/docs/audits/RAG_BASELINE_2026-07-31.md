# F0 — Línea base verificable del RAG

**Fecha:** 31-07-2026  
**Estado:** VALIDACIÓN  
**Entorno:** local efímero, Docker `pgvector/pgvector:pg16`, Ollama local  
**Datos:** corpus técnico F0 no productivo, creado exclusivamente para validación; no contiene datos bancarios ni de clientes.

## Alcance

Esta auditoría congela el comportamiento observable anterior a las fases F1–F7. No implementa nuevas capacidades. OCR permanece fuera de alcance.

F0 no se marca `TERMINADA` porque todavía falta repetir calidad, planes y carga con un corpus de tamaño y distribución representativos expresamente autorizado por el responsable del banco. Los resultados de seis documentos sólo demuestran funcionamiento, no capacidad productiva.

## Inventario técnico

### Persistencia y seguridad

| Elemento | Estado observado |
|---|---|
| Motor | PostgreSQL 16 + pgvector 0.8.6 |
| Esquema | `flentio_rag` |
| Tablas | `documents`, `document_versions`, `chunks`, `ingestion_jobs`, `query_metrics` |
| RLS | habilitado y forzado en las cinco tablas |
| Políticas | una política `ALL` por tabla basada en `app.tenant_id` |
| Rol de aplicación | `flentio_rag_app`, sin DDL ni `BYPASSRLS` |
| Funciones privilegiadas | `claim_next_ingestion_job(text)` y `recover_stale_ingestion_jobs(integer)` |
| Índices de recuperación | HNSW coseno, GIN `tsvector`, índices B-tree por tenant/documento/cola |
| Cola | PostgreSQL, `FOR UPDATE SKIP LOCKED`, reintentos y recuperación de trabajos |

Las funciones `SECURITY DEFINER` tienen `search_path` vacío, permisos públicos revocados y sólo exponen las operaciones globales necesarias al worker.

### API observada

| Ruta | Operación |
|---|---|
| `GET /api/rag/status` | salud y contadores del tenant |
| `GET /api/rag/documents` | listado paginado |
| `GET /api/rag/metrics` | métricas agregadas sin pregunta en claro |
| `POST /api/rag/upload` | ingesta textual |
| `POST /api/rag/upload-file` | PDF con texto, DOCX y formatos textuales |
| `GET /api/rag/jobs/:jobId` | estado de trabajo |
| `POST /api/rag/query` | recuperación híbrida |
| `DELETE /api/rag/documents/:documentId` | archivado lógico |
| `POST /api/rag/sync-gdrive` | sincronización real con OAuth |
| `POST /api/rag/sync-eulegislation` | descarga real desde EUR-Lex |

### Configuración inventariada

`RAG_DATABASE_URL`, `RAG_MIGRATION_DATABASE_URL`, `RAG_AUTO_MIGRATE`, `RAG_DB_POOL_MAX`, `RAG_POSTGRES_PORT`, `RAG_EMBEDDING_PROVIDER`, `RAG_EMBEDDING_MODEL`, `RAG_EMBEDDING_DIMENSIONS`, `OPENAI_API_KEY`, `OLLAMA_URL`, `RAG_CHUNK_CHARS`, `RAG_CHUNK_OVERLAP_CHARS`, `RAG_DEFAULT_TOP_K`, `RAG_MAX_CONTENT_CHARS`, `RAG_WORKER_CONCURRENCY` y `RAG_STALE_JOB_MINUTES`.

Se observó que `RAG_STALE_JOB_MINUTES` estaba consumida por el worker pero no documentada en `backend/.env.example`; se añadió durante F0 con valor de referencia de 30 minutos.

## Resultados reproducibles

### Línea base de código

- backend: 12/12 pruebas superadas;
- dependencias backend productivas: `npm audit --omit=dev`, cero vulnerabilidades conocidas;
- frontend: lint completado con advertencias preexistentes, sin errores;
- frontend: compilación Vite completada;
- advertencia vigente: bundle principal de 1.420,49 kB sin comprimir, fuera del alcance funcional de F0 pero registrado como deuda.

### Ingesta y recuperación real

Proveedor real: Ollama `nomic-embed-text`, 768 dimensiones.

| Métrica | Resultado observado |
|---|---:|
| Documentos/versiones/fragmentos | 6 / 6 / 6 |
| Tiempo de ingesta | 1.926 ms |
| Rendimiento aparente | 186,92 documentos/minuto |
| Recall@5 | 1,0000 |
| MRR | 1,0000 |
| Latencias de consulta | 1865, 66, 70, 80, 82 y 77 ms |
| p50 observado | 77 ms |
| p95/p99 observado | 1.865 ms |
| Resultados visibles desde otro tenant | 0 |
| Listado visible desde otro tenant | 0 |

El primer embedding de consulta incurrió en un arranque frío de 1.865 ms. Con sólo seis muestras, los percentiles no son estadísticamente representativos. La telemetría persistida calculó p50 72,5 ms y p95 1.413,3 ms para las seis consultas autorizadas.

El valor de 186,92 documentos/minuto tampoco puede extrapolarse: los documentos eran cortos, generaron un único fragmento y el worker procesó un corpus mínimo.

### Plan SQL

`EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` sobre la rama vectorial devolvió 0,132 ms de ejecución SQL, 41 bloques compartidos en caché y cero lecturas físicas. Se utilizaron:

- `rag_chunks_document_idx` para `tenant_id`;
- `rag_documents_tenant_status_updated_idx` para tenant y estado;
- `document_versions_pkey` para versión.

PostgreSQL realizó ordenación exacta y no eligió HNSW debido al corpus diminuto. Por tanto, esta evidencia valida índices de aislamiento y joins, pero **no valida todavía el comportamiento HNSW a decenas de miles de documentos**.

### Migración, backup y restauración

- migración ejecutada dos veces sin error: idempotencia confirmada;
- backup real creado con `pg_dump` en formato custom: 52.939 bytes;
- restauración realizada en una base nueva `flentio_rag_restore_f0`;
- verificación restaurada: 6 documentos, 6 versiones, 6 fragmentos, 6 trabajos, 7 métricas y pgvector 0.8.6.

La prueba valida el procedimiento lógico en el entorno F0. No demuestra todavía PITR, cifrado de backup, restauración multirregión ni RPO/RTO; corresponden a F6 y requieren decisiones humanas.

## Matriz de datos y amenazas

| Activo/dato | Ubicación actual | Amenaza principal | Control observado | Riesgo pendiente |
|---|---|---|---|---|
| Original subido | memoria de proceso durante carga | malware, agotamiento, fuga | límite 15 MB y validación básica de firma | cuarentena/antivirus en F2 |
| Texto extraído | `document_versions.content` | acceso cruzado, retención excesiva | RLS forzado por tenant | ACL fina y ciclo de vida en F1/F3 |
| Fragmentos | `chunks.content` | revelación en recuperación | RLS y consulta dentro de transacción tenant | clasificación/grupos en F1 |
| Embeddings | `chunks.embedding` | inferencia o exfiltración | RLS, rol limitado | cifrado/segregación infraestructural en F6 |
| Metadatos | JSONB y columnas documentales | títulos/URI sensibles | RLS | minimización y taxonomía en F1/F3 |
| Preguntas | no se persisten en claro en métricas | fuga mediante logs | SHA-256 y agregados | revisar logs/SIEM en F7 |
| Credenciales | ajustes/bóveda y entorno | robo o exposición | valores no devueltos por el RAG | KMS/HSM y rotación requieren decisión |
| Trabajos | `ingestion_jobs.payload` | contenido duplicado y acceso indebido | RLS, reintentos acotados | retención/purga gobernada en F3 |
| Conectores | Google Drive/EUR-Lex | revocación, contenido alterado | OAuth real, errores explícitos, checksum disponible | incrementalidad/firma en F5 |
| Funciones globales | PostgreSQL | escalada entre tenants | operación acotada, `search_path=''`, sin `BYPASSRLS` | revisión independiente antes de F1 |

## Puertas F0

| Puerta | Estado | Evidencia o motivo |
|---|---|---|
| Funcional | SUPERADA_LOCAL | ingesta, consulta y citas con Ollama real |
| Seguridad | SUPERADA_LOCAL | segundo tenant devuelve cero filas/resultados |
| Calidad | PENDIENTE_REPRESENTATIVA | 6/6 Recall@5 y MRR 1,0 sobre corpus F0 |
| Rendimiento | PENDIENTE_REPRESENTATIVO | plan capturado; HNSW no elegido por bajo volumen |
| Resiliencia | SUPERADA_LOCAL | backup y restauración lógica verificados |
| Operación | PARCIAL | procedimiento reproducible; SLO/RPO/RTO no definidos |
| Documentación | SUPERADA | inventario, límites y resultados registrados |
| Dependencias | SUPERADA | cero vulnerabilidades npm productivas conocidas |

## Condiciones para terminar F0

Se necesita autorización humana para seleccionar o facilitar un corpus representativo, sanitizado y legalmente utilizable. Después se deben repetir:

1. Recall@K, MRR y precisión de citas con preguntas aprobadas;
2. latencias calientes y frías con suficientes muestras;
3. ingesta con distribuciones reales de tamaño y fragmentos;
4. planes vectoriales que permitan evaluar HNSW;
5. carga concurrente y uso del pool acordes al escenario objetivo.

No se necesita copiar el corpus al repositorio: puede mantenerse en una ubicación segura y documentar únicamente su identificador, checksum, volumen y autorización.

## Limpieza y reversión

F0 no modifica el esquema funcional. El proyecto Docker, sus dos bases de validación, el backup temporal y el volumen se eliminan al finalizar la sesión de medida. La documentación es el único cambio persistente y puede revertirse sin afectar datos ni servicio.
