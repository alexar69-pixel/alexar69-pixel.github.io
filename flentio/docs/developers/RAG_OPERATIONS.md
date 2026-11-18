# RAG empresarial de Flentio

La evolución posterior del sistema, excluyendo expresamente OCR, está definida en `docs/RAG_ENTERPRISE_ROADMAP.md`. Ese documento es planificación y no representa capacidades ya operativas.

**Acceso a infraestructura de clientes**: actualmente **no disponemos** de acceso
a la infraestructura de clientes. Por tanto, las Skills de integración externa
están implementadas, pero **sin probar ni validar** contra sistemas reales. El
estado `NO_CONFIGURADO` refleja esta falta de acceso, no una omisión de código.
Cualquier parámetro, endpoint o credencial específica del cliente debe
proporcionarla el propio cliente bajo sus controles de homologación.

La fase F0 está en `VALIDACIÓN`. Sus medidas, inventario, matriz de datos/amenazas y límites se conservan en `docs/audits/RAG_BASELINE_2026-07-31.md`; no deben extrapolarse a carga bancaria hasta repetirlas con un corpus representativo autorizado.

La fase F2 también está en `VALIDACIÓN`: la cuarentena, ClamAV, límites documentales, aprobación humana y aislamiento superaron pruebas locales reales. Funcionamiento, operación y alternativas comerciales están en `docs/RAG_SECURITY_INGESTION.md`; la evidencia y los riesgos pendientes, en `docs/audits/RAG_F2_SECURITY_2026-07-31.md`.

La fase F3 está en `VALIDACIÓN`: conserva originales cifrados y versionados en MinIO single-node, registra la procedencia completa, gobierna vigencia/legal hold/retención y excluye conocimiento obsoleto. Su diseño y límites están en `docs/RAG_PROVENANCE_LIFECYCLE.md`; MinIO no está seleccionado para producción y HA se mantiene aplazada a F6.

La fase F4 está en `VALIDACIÓN`: añade fragmentación por tipo documental, búsqueda multilingüe, fechas de captura, reranking real y umbral de evidencia. La guía completa, proveedores alternativos y fallo cerrado están en `docs/RAG_RETRIEVAL_QUALITY.md`; la evidencia local, en `docs/audits/RAG_F4_QUALITY_2026-07-31.md`.

El 01-08-2026 se añadió un corpus público bancario reproducible con 16 fuentes oficiales de DORA, SEPA, PSD2, PBC-FT, FATCA, SWIFT y materias relacionadas. Quedaron 15 documentos vigentes y una referencia SWIFT histórica expirada, con 4.604 fragmentos. Configuración, fuentes y rollback: `docs/RAG_PUBLIC_BANKING_CORPUS.md`; evidencia: `docs/audits/RAG_PUBLIC_BANKING_CORPUS_2026-08-01.md`. Las especificaciones CBPR+ actuales y Knowledge Centre siguen `NO_CONFIGURADO` hasta recibir cuenta y permisos del cliente.

El panel incorpora además un flujo persistente para materializar esas plantillas,
revisarlas humanamente, descargarlas o relanzarlas bajo demanda y registrar
fuentes HTTPS/CELEX nuevas sin programar un endpoint por documento. Guardar no
ejecuta: la aprobación persiste actor, fecha y nota, y cualquier cambio vuelve a
`pending_review`. La descarga se ejecuta en el worker y atraviesa seguridad,
custodia y extracción, pero queda en staging. Un segundo acto humano, con nota,
publica o rechaza el contenido; sólo publicar crea la ingesta. El panel permite
ver hashes, escáner, comparación, texto extraído y restaurar el original. Configuración, estados, límites y
rollback: `docs/RAG_EXTERNAL_DOCUMENT_SOURCES.md`; evidencia:
`docs/audits/RAG_EXTERNAL_DOCUMENT_SOURCES_2026-08-01.md`.

Los agentes de workflow consumen el RAG mediante un contrato de evidencia
estructurado. Si no hay fragmentos suficientes, el modelo no se invoca; si se
invoca, la respuesta debe declarar JSON y citar identificadores `[E#]` que
pertenezcan exactamente al conjunto recuperado. PostgreSQL registra hashes,
referencias, proveedor, modelo y resultado sin guardar pregunta, respuesta o
contenido. Ollama `llama3.2:3b` está validado localmente; los adaptadores OpenAI
y Gemini están implementados pero no validados sin credenciales. Diseño:
`docs/RAG_AGENT_EVIDENCE_CONTRACT.md`; evidencia:
`docs/audits/RAG_AGENT_EVIDENCE_2026-08-01.md`.

El reranker procesa 40 candidatos en lotes TEI secuenciales de 5. En desarrollo puede usarse `codex-oauth-local` con la sesión ChatGPT oficial de Codex CLI; crea un proceso efímero, sin herramientas web, en sandbox de sólo lectura y queda bloqueado en producción. OpenAI API es el proveedor productivo autorizado y permanece `NO_CONFIGURADO` hasta disponer de credencial y homologación. Todos fallan cerrados. Evidencia: `docs/audits/RAG_OPENAI_RERANKER_2026-08-01.md`.

La aceptación OAuth aislada obtuvo MRR `1,0000`, igual que la recuperación base, pero p95 `5.770 ms` frente a `115 ms`. El umbral local se calibró provisionalmente en `0,70`. Estas cifras confirman su uso exclusivo para desarrollo y no acreditan calidad, latencia ni coste productivos.

El subproceso OAuth recibe un entorno reducido: nunca hereda URLs de base de datos, credenciales de MinIO/S3 ni claves API del backend. Codex ejecuta con herencia de entorno para herramientas desactivada, web deshabilitada, sandbox de sólo lectura y directorio temporal vacío.

`RAG_CODEX_OAUTH_MAX_CONCURRENCY=1` evita tormentas de procesos y consumo accidental de cuota local. Cuando el cupo está ocupado, la API falla explícitamente con 503; no encola peticiones ni degrada a otro proveedor. El contador se libera en éxito, error y timeout.

El perfil OAuth ignora configuración, reglas, plugins y MCP del usuario; niega lectura general del disco y red de herramientas. `RAG_MAX_QUERY_CHARS=4000` rechaza entradas excesivas antes de ejecutar PostgreSQL, embeddings o modelos. El panel no-code aplica valores iniciales coherentes por proveedor y sólo muestra concurrencia OAuth cuando corresponde.

La salida JSONL se audita antes de aceptar el ranking. Cualquier evento de comando, archivo, MCP o búsqueda invalida por completo la consulta y se trata como indisponibilidad del reranker.

La v3 amplía cada canal a 160 candidatos, incorpora metadatos documentales indexados y selecciona por rondas con máximo inicial de 4 fragmentos por documento antes de enviar 40 a TEI. En el corpus público verificado obtuvo Recall@K 1,0000 y p95 878 ms; no es evidencia de carga bancaria. Parámetros: `RAG_RETRIEVAL_POOL_MULTIPLIER` y `RAG_RETRIEVAL_MAX_CHUNKS_PER_DOCUMENT`. Evidencia y rollback: `docs/audits/RAG_F4_CANDIDATE_DIVERSITY_2026-08-01.md`.

El 31-07-2026 se completó una aceptación local integral F0–F7 con OAuth y Google Drive reales, tres Google Docs sintéticos identificados, ClamAV, MinIO, Ollama, TEI, consulta, reindexación, RLS, restauración de originales y panel autenticado. El informe `docs/audits/RAG_FULL_ACCEPTANCE_2026-07-31.md` contiene resultados, defectos corregidos y puertas pendientes. Esta evidencia no acredita escala ni producción bancaria.

## Estado y alcance

El RAG productivo utiliza PostgreSQL 16 con pgvector. No utiliza los antiguos archivos JSON de `backend/data/knowledge_rag`, que se conservan únicamente como datos históricos y no intervienen en consultas nuevas.

El sistema implementa:

- aislamiento por organización mediante RLS forzado;
- rol de aplicación sin privilegios DDL ni `BYPASSRLS`;
- embeddings reales mediante Ollama u OpenAI;
- índice vectorial HNSW y búsqueda textual GIN en español;
- combinación de resultados mediante Reciprocal Rank Fusion;
- fragmentación estructural con tamaño y solapamiento acotados;
- deduplicación por checksum y versionado por fuente;
- cola PostgreSQL reclamada mediante `FOR UPDATE SKIP LOCKED`;
- paginación por cursor;
- citas con documento, versión y número de fragmento;
- conectores reales para Google Drive y EUR-Lex.
- extracción segura de PDF, DOCX y formatos de texto de hasta 15 MB;
- worker dedicado con reintentos y recuperación de trabajos interrumpidos;
- telemetría sin texto de consulta y evaluación Recall@K/MRR reproducible.
- autorización documental RLS por clasificación, concesión, entidad jurídica, jurisdicción, departamento y vigencia.
- antimalware ClamAV anterior a los parsers, cuarentena y decisiones humanas auditables;
- límites contra DOCX expansivos, PDF extremos e instrucciones hostiles documentales.
- originales cifrados con AES-256-GCM, versionados y verificados en almacenamiento de objetos;
- procedencia hasta versión, página/sección y versiones del pipeline;
- estados documentales, legal hold y retención GOVERNANCE con eventos auditables.
- fragmentación versionada para norma, contrato, procedimiento, informe y tabla;
- recuperación española/multilingüe con filtros de captura y reranking TEI/GTE real;
- umbral explícito de evidencia, fallo cerrado y métricas de calidad/versionado del pipeline.
- contrato de agentes con abstención previa al modelo, salida JSON, citas `[E#]`
  validadas y auditoría RLS sin texto en claro.

## Autorización documental F1

Todo documento requiere una concesión explícita de usuario o grupo. `PUBLIC` no significa público en Internet: continúa limitado al tenant y a su ACL. Los niveles son `PUBLIC`, `INTERNAL`, `CONFIDENTIAL` y `RESTRICTED`.

El administrador configura en el panel de usuarios el clearance, grupos, entidades jurídicas, jurisdicciones y departamentos. Esos valores se incluyen en el JWT del siguiente inicio de sesión. El rol administrativo permite gestionar identidades, pero no leer documentos sin concesión.

Las cargas aceptan `classification`, `legalEntityId`, `jurisdiction`, `department`, `effectiveFrom`, `effectiveUntil` y `allowedGroupIds`. El backend rechaza grupos que no estén incluidos en la identidad firmada. Los conectores pueden utilizar los mismos campos en su petición de sincronización.

SSO/LDAP no está configurado actualmente: sus endpoints devuelven `NO_CONFIGURADO` y no aceptan identidades proporcionadas por el navegador. Para un banco debe integrarse un IdP OIDC/SAML real antes de utilizar identidad federada.

## Relación entre el RAG y los modelos de IA

El RAG es la fuente corporativa común de conocimiento y no pertenece a ningún proveedor generativo. Los agentes pueden utilizar Gemini, modelos de OpenAI/ChatGPT u Ollama, pero todos siguen el mismo recorrido:

En clientes que ya disponen de RAG internos, «fuente corporativa común» no
significa copiar su contenido a Flentio. El modo objetivo es consulta federada,
con citas, versiones, autorización y hashes; el texto permanece en el perímetro
del cliente. Diseño: `docs/RAG_CLIENT_KNOWLEDGE_FEDERATION.md`. El adaptador
permanece `NO_CONFIGURADO`.

1. Flentio recibe la pregunta y la organización autenticada.
2. El motor RAG genera un embedding de consulta con el proveedor de embeddings configurado.
3. PostgreSQL recupera fragmentos autorizados mediante búsqueda vectorial y textual.
4. Flentio construye un contexto delimitado con citas y lo marca como evidencia, no como instrucciones.
5. El modelo generativo seleccionado recibe la pregunta y ese contexto común.
6. La respuesta conserva la trazabilidad hacia documento, versión y fragmento.

El **modelo de embeddings** y el **modelo generativo** cumplen funciones diferentes:

- El modelo de embeddings indexa y localiza conocimiento. Su dimensión queda asociada al índice pgvector.
- Gemini, OpenAI/ChatGPT u Ollama redactan la respuesta o toman la decisión utilizando los fragmentos recuperados.

Cambiar de Gemini a OpenAI no exige reindexar documentos. Cambiar el modelo de embeddings por otro con distinta dimensión sí requiere un índice nuevo y una reindexación controlada.

Los agentes no deben responder con supuesto conocimiento interno cuando el RAG no aporta evidencia suficiente. En ese caso deben declarar que no existe información documental verificable.

El catálogo incluye una plantilla pública para `cisa:kev:live`. Su importación
no es automática: cada tenant debe revisar, descargar, inspeccionar y publicar
la fuente. KEV aporta contexto sobre explotación conocida, pero la afectación
local permanece `NO_EVALUADO` hasta correlacionar SBOM, versión, configuración y
exposición. Diseño de errores, incidentes y otras fuentes de seguridad:
`docs/RAG_OPERATIONAL_SECURITY_KNOWLEDGE.md`.

## Despliegue recomendado

1. Copie `backend/.env.example` a un almacén seguro de configuración. No confirme secretos en Git.
2. Defina valores diferentes y aleatorios para `RAG_POSTGRES_PASSWORD` y `RAG_APP_PASSWORD`.
   PostgreSQL se publica sólo en loopback mediante `RAG_POSTGRES_PORT`; en producción puede retirarse el puerto y utilizar la red privada del orquestador.
3. Seleccione un modelo de embeddings y mantenga fija su dimensión durante la vida del índice.
4. Inicie Docker y ejecute `docker compose up -d`. Esto levanta PostgreSQL, ClamAV, MinIO single-node de desarrollo, la aplicación y el worker dedicado. Reserve al menos 4 GiB para ClamAV y persistencia para sus firmas. Defina credenciales MinIO y una clave AES de 32 bytes; perderla hace irrecuperables los originales.
5. La aplicación aplica la migración al arrancar cuando `RAG_AUTO_MIGRATE=true`; para un proceso controlado ejecute `npm run migrate:rag` desde `backend` antes del despliegue.
6. Compruebe `GET /api/rag/status`; debe devolver `OPERATIVO` tanto para RAG como para `securityScanner`.

Para migrar los antiguos JSON, defina `RAG_IMPORT_ORGANIZATION` con el identificador estable de la organización y ejecute `npm run import:legacy-rag`. El importador conserva únicamente la versión más reciente de cada título, genera embeddings reales y espera la confirmación de cada trabajo. No borra los ficheros históricos.

El contenedor crea dos identidades:

- `flentio_rag`: propietaria, utilizada exclusivamente para migraciones;
- `flentio_rag_app`: utilizada por la aplicación, sin privilegios administrativos.

En un banco se recomienda sustituir las contraseñas de Compose por secretos del orquestador, colocar PgBouncer en modo transacción delante de PostgreSQL y desplegar varias réplicas de workers.

## Proveedores de embeddings

### Ollama local

```env
RAG_EMBEDDING_PROVIDER=ollama
RAG_EMBEDDING_MODEL=nomic-embed-text
RAG_EMBEDDING_DIMENSIONS=768
OLLAMA_URL=http://127.0.0.1:11434
```

Instalación del modelo: `ollama pull nomic-embed-text`.

### OpenAI

```env
RAG_EMBEDDING_PROVIDER=openai
RAG_EMBEDDING_MODEL=text-embedding-3-small
RAG_EMBEDDING_DIMENSIONS=1536
OPENAI_API_KEY=<secreto gestionado fuera de Git>
```

Cambiar a un modelo con otra dimensión exige crear un índice nuevo y reindexar todos los fragmentos. El sistema rechaza vectores de dimensión incorrecta.

## API

| Método y ruta | Rol mínimo | Comportamiento real |
|---|---|---|
| `GET /api/rag/status` | viewer | Estado de PostgreSQL, pgvector, modelo, almacenamiento de objetos y contadores |
| `GET /api/rag/documents` | viewer | Lista paginada por cursor y aislada por organización |
| `POST /api/rag/upload` | operator | Valida y encola un documento; devuelve HTTP 202 y `job.id` |
| `POST /api/rag/upload-file` | operator | Extrae y encola PDF, DOCX, TXT, MD, CSV, JSON o XML real; máximo 15 MB |
| `GET /api/rag/security-assessments` | viewer | Lista evaluaciones accesibles; creador o aprobador dentro del tenant |
| `POST /api/rag/security-assessments/:id/approve` | admin/editor + grupo de seguridad | Aprueba una cuarentena y crea un único trabajo |
| `POST /api/rag/security-assessments/:id/reject` | admin/editor + grupo de seguridad | Rechaza con actor y motivo auditable |
| `GET /api/rag/jobs/:id` | viewer | Estado verificable de una ingesta |
| `GET /api/rag/documents/:id/provenance` | viewer autorizado | Cadena documento-versión-original, hashes, pipeline y eventos |
| `GET /api/rag/documents/:id/original?version=N` | viewer autorizado | Restaura y verifica criptográficamente la versión exacta |
| `POST /api/rag/documents/:id/lifecycle` | operator con `manage` | Aprueba, activa, sustituye, expira o archiva con motivo |
| `POST /api/rag/documents/:id/legal-hold` | gestor documental con `manage` | Aplica y verifica legal hold por versión en MinIO |
| `POST /api/rag/documents/:id/retention` | gestor documental con `manage` | Amplía y verifica retención GOVERNANCE; no permite acortarla |
| `GET /api/rag/metrics?days=7` | viewer | Volumen, consultas sin resultado y latencias p50/p95, sin guardar preguntas |
| `POST /api/rag/query` | viewer | Recuperación híbrida con citas y puntuaciones separadas |
| `DELETE /api/rag/documents/:id` | operator | Archivado lógico; deja de participar en recuperación |
| `GET /api/rag/connectors` | viewer | Estado real, cursor, frescura y errores de conectores del tenant |
| `GET /api/rag/connector-providers` | viewer | Lista únicamente adaptadores instalados realmente |
| `POST /api/rag/connectors/google-drive` | operator | Registra una carpeta y encola sincronización inicial incremental |
| `POST /api/rag/connectors/:id/sync` | operator | Consume cambios desde el cursor durable |
| `POST /api/rag/connectors/:id/reconcile` | operator | Enumera y repara pérdidas o eliminaciones mediante tombstones |
| `POST /api/rag/connectors/:id/webhook` | operator | Crea un canal Google real renovable; requiere HTTPS y OAuth |
| `POST /api/rag/connectors/:id/disable` | operator | Deshabilita sin borrar cursor, eventos ni procedencia |
| `POST /api/rag/sync-gdrive` | operator | Compatibilidad: registra conector y encola; ya no relee todo en la petición |
| `POST /api/rag/sync-eulegislation` | operator | Descarga el texto oficial real desde EUR-Lex |
| `GET /api/rag/external-source-templates` | viewer | Catálogo instalado y hosts HTTPS autorizados |
| `GET /api/rag/external-sources` | viewer | Fuentes y última ejecución aisladas por tenant |
| `GET /api/rag/external-sources/:id/runs` | viewer | Historial real de ejecuciones, hashes e intentos |
| `POST /api/rag/external-sources` | operator | Valida y guarda una fuente HTTPS o CELEX |
| `POST /api/rag/external-sources/import-template` | operator | Materializa una plantilla oficial para el tenant |
| `POST /api/rag/external-sources/:id/review` | operator | Aprueba o solicita cambios con actor, fecha y nota |
| `POST /api/rag/external-sources/:id/run` | operator | Encola una descarga durable; deduplica ejecuciones activas |
| `GET /api/rag/external-sources/:id/runs/:runId/original` | viewer autorizado | Restaura el original cifrado y verifica tamaño/SHA-256 antes de descargar |
| `POST /api/rag/external-sources/:id/runs/:runId/content-review` | operator | Publica o rechaza contenido staged con actor, fecha y nota |
| `POST /api/rag/external-sources/:id/disable` | operator | Detiene futuras descargas y conserva la evidencia |
| `GET /api/rag/embedding-indexes` | viewer | Lista activo, candidatos, cobertura y trabajo por tenant |
| `POST /api/rag/embedding-indexes` | admin | Crea partición/HNSW candidato y backfill resumible |
| `POST /api/rag/embedding-indexes/jobs/:id/pause` | admin | Pausa sin eliminar progreso |
| `POST /api/rag/embedding-indexes/jobs/:id/resume` | admin | Reanuda el trabajo persistente |
| `POST /api/rag/embedding-indexes/:id/activate` | admin | Conmuta con cobertura completa y evaluación aprobada |
| `GET /api/rag/observability` | viewer | Estado, colas, frescura, calidad y latencias agregadas por tenant |
| `GET /api/rag/observability/prometheus` | viewer | Exportación agregada autenticada sin contenido sensible |
| `GET /api/rag/observability/audit` | admin/editor | Auditoría append-only paginada y aislada por tenant |
| `GET /api/rag/agent-evidence-runs` | viewer | Historial propio de consumo por agentes, sin preguntas, respuestas ni fragmentos |
| `GET /api/rag/worm-reconciliation` | admin/editor | Ejecuciones y divergencias WORM del tenant |
| `POST /api/rag/worm-reconciliation` | admin/editor | Encola una comprobación de sólo lectura |
| `POST /api/rag/monitoring/ingest` | operator | Ingresa texto de monitorización como documento RAG |
| `GET /api/rag/monitoring/sources` | viewer | Lista fuentes de monitorización registradas |
| `POST /api/rag/monitoring/sources` | operator | Registra una fuente de monitorización y encola su procesamiento |

## Tipos documentales especializados

El chunker estructurado preserva la semántica de tipos documentales específicos
sin fragmentación ciega. Cada tipo infiere su estructura y genera rutas de
encabezado estables para recuperación.

### Normativas y contratos (`regulation`, `contract`)

- Detecta artículos/cláusulas numeradas y los preserva como unidad.
- Configuración óptima: `RAG_CHUNK_CHARS=1800`, `RAG_CHUNK_OVERLAP_CHARS=240`.
- El índice GIN sobre metadatos y el filtro `document_type` aceleran la
  recuperación por artículo o cláusula.

### Diagramas técnicos (`architecture`)

- Preserva bloques Mermaid, PlantUML, GraphViz, sequenceDiagram, classDiagram,
  stateDiagram, erDiagram, flowchart y graph con orientación TD/TB/BT/RL/LR.
- Cada diagrama se fragmenta como chunk completo con 500 caracteres de contexto
  previo cuando es posible.
- Configuración óptima: `RAG_CHUNK_CHARS=4000` para evitar dividir diagramas
  grandes; el chunker no subdivide bloques de código de diagrama.

### Logs estructurados (`monitoring_log`)

- Agrupa por ventanas de severidad (`ERROR`, `WARN`, `INFO`, `DEBUG`, `CRITICAL`).
- Flush automático al cambiar de severidad crítica o superar 50 líneas.
- Configuración óptima: ingerir por ventana temporal (ej. 1h) para mantener
  chunks recuperables; `RAG_CHUNK_CHARS=1800` funciona bien con el agrupador.

### Reportes semanales (`weekly_report`)

- Separa por secciones markdown (`#`, `##`, `###`) y preserva métricas clave.
- Las secciones largas se dividen por párrafos sin romper encabezados.
- Configuración óptima: `RAG_CHUNK_CHARS=2400` para conservar métricas
  agregadas en un solo fragmento.

### Runbooks (`runbook`)

- Detecta precondiciones y pasos numerados (`PASO`, `STEP`, `acción`).
- Cada paso es un chunk independiente con encabezado preservado.
- Configuración óptima: `RAG_CHUNK_CHARS=1800`, `RAG_CHUNK_OVERLAP_CHARS=240`.

### Ingesta programada de monitorización

El servicio `monitoringIngestionService` permite registrar fuentes y procesar
contenido de monitorización:

```env
MONITORING_MAX_CONTENT_CHARS=2000000
MONITORING_RETENTION_DAYS=90
```

Endpoints:
- `POST /api/rag/monitoring/ingest` — ingesta texto con tipo documental.
- `GET /api/rag/monitoring/sources` — lista fuentes registradas.
- `POST /api/rag/monitoring/sources` — registra fuente y encola procesamiento.

Tipos admitidos: `monitoring_log`, `weekly_report`, `runbook`, `architecture`.
El gobierno (clasificación, grupos, entidad, jurisdicción) se aplica igual que
en cualquier documento RAG.

- `NO_CONFIGURADO`: falta una variable, credencial o proveedor.
- `NO_DISPONIBLE`: existe configuración, pero el servicio real no responde.
- `received`/`scanning`: evaluación creada o bytes bajo análisis antimalware.
- `quarantined`: no está indexado; requiere una decisión humana autorizada.
- `awaiting_content_review`: seguridad aprobada, original custodiado y texto
  extraído; no existe todavía trabajo de ingesta.
- `content_rejected`: decisión humana persistida; conserva evidencia y no se indexa.
- `approved`: control superado y trabajo creado o listo para crearse.
- `rejected`: no puede llegar al índice.
- `indexed`: la versión y sus embeddings se confirmaron transaccionalmente.
- `PENDIENTE`: el documento fue aceptado por la cola, pero aún no está indexado.
- `processing`: un worker posee el trabajo.
- `ready`: la versión fue fragmentada, embebida y confirmada transaccionalmente.
- `failed`: se agotaron los reintentos y se conserva el error real.
- `archived`: el documento no participa en consultas.
- `draft`/`approved`/`effective`/`superseded`/`expired`: ciclo documental; sólo `effective`, autorizado y dentro de fechas se recupera.

## Operación y capacidad

Para decenas de miles de documentos:

- monitorice longitud de `ingestion_jobs`, latencia p95 de consultas y tamaño de HNSW;
- ejecute `VACUUM (ANALYZE)` según la política de mantenimiento de PostgreSQL;
- revise planes mediante `EXPLAIN (ANALYZE, BUFFERS)` con datos representativos;
- aumente workers antes que conexiones y mantenga un pool acotado;
- realice backups cifrados y pruebas periódicas de restauración;
- evalúe la calidad con un conjunto de preguntas, documentos esperados y métricas Recall@K/MRR antes de cada cambio de modelo.

El control de calidad se ejecuta con `RAG_EVALUATION_ORGANIZATION=<organización> npm run evaluate:rag -- dataset.json`. Cada caso contiene `question`, `expectedSourceKeys` y opcionalmente `topK`. El comando consulta el índice real y devuelve Recall@K y MRR; no inserta datos ni simula respuestas.

## Limitaciones explícitas

- La aplicación no arranca migraciones automáticamente salvo `RAG_AUTO_MIGRATE=true`.
- El conector Drive necesita una credencial OAuth real almacenada en la bóveda.
- F5 ejecuta la cola de conectores en el backend web porque la bóveda SQLite sólo está montada allí. La cola PostgreSQL admite varios reclamadores, pero HA exige primero una bóveda compartida homologada.
- Los webhooks requieren `RAG_PUBLIC_BASE_URL` HTTPS y `RAG_CONNECTOR_WEBHOOK_SECRET`; sin ambos, la sincronización por reconciliación sigue disponible y el webhook falla como no configurado.
- PDF sin capa de texto (por ejemplo, escaneados) se rechaza por falta de texto; OCR aún no está incorporado.
- Para alta disponibilidad se pueden desplegar varias réplicas de `rag-worker`; `SKIP LOCKED` evita el procesamiento concurrente del mismo trabajo.
- ClamAV actual es una instancia; su alta disponibilidad y la integración SOC/SIEM son requisitos abiertos antes de un despliegue bancario.
- MinIO actual es single-node y el proyecto comunitario está archivado; sólo se utiliza para desarrollo. Producción exige proveedor soportado, KMS/HSM, HA/DR y pruebas independientes.
- No hay borrado físico automático: falta aprobar plazos de retención y destrucción por jurisdicción. La API de aplicación tampoco dispone de DELETE sobre originales.
- Una operación WORM abarca MinIO y PostgreSQL; Flentio verifica el estado remoto inmediatamente, pero la reconciliación periódica automática queda pendiente de F5.

## Registro de validación

El 31-07-2026 se ejecutó una prueba integral real sobre `pgvector/pgvector:pg16` y Ollama `nomic-embed-text`:

- migración del esquema y creación de pgvector completadas;
- ingesta asíncrona completada con embeddings reales de 768 dimensiones;
- recuperación híbrida devolvió dos fragmentos;
- cita verificada: `[Política de Continuidad Operativa · v1 · fragmento 1]`;
- una segunda organización no pudo listar ni recuperar el documento de la primera;
- tras archivar el documento dejó de aparecer en recuperación;
- el entorno y volumen efímeros de validación se eliminaron al terminar.

Validación final del mismo día tras incorporar persistencia por lotes, métricas y worker recuperable: migración idempotente completada, trabajo `completed`, una cita real recuperada, cero resultados desde otro tenant y latencia registrada en `query_metrics`. Las 12 pruebas unitarias pasaron y `npm audit --omit=dev` informó cero vulnerabilidades.

Validación F3 final sobre volúmenes vacíos: migraciones aplicadas dos veces con `vector(768)`, MinIO fuente `RELEASE.2025-10-15T17-29-55Z`, trabajo real `completed`, original versionado/verificado, restauración idéntica, aislamiento entre tenants, legal hold preservando la versión tras DELETE y expiración excluida de la consulta. `EXPLAIN` utilizó el índice parcial de documentos efectivos, no quedaron claves foráneas sin índice, pasaron 21/21 pruebas backend y la auditoría npm devolvió cero vulnerabilidades. Evidencia completa en `docs/audits/RAG_F3_PROVENANCE_2026-07-31.md`.

## Integración transversal con la plataforma PostgreSQL

Desde el corte del 01-08-2026, identidad, workflows y auditoría de plataforma
usan PostgreSQL y SQLite queda desactivado durante la operación web. RAG y
plataforma conservan esquemas, migraciones, roles y pools lógicamente separados;
compartir el motor no concede acceso entre organizaciones ni fusiona sus
dominios. La guía de despliegue, escalado y reversión está en
`docs/PLATFORM_POSTGRES_CUTOVER.md`.

La interfaz de administración muestra exclusivamente estados devueltos por los
servicios reales. Un bloque ausente se representa como desconocido o no
configurado; nunca se completa con telemetría simulada. El Copiloto recupera
evidencia autorizada con citas y no selecciona un modelo generativo ni modifica
el lienzo. Si no encuentra fragmentos, responde `EVIDENCIA_INSUFICIENTE`.

Validación visual real del 01-08-2026: ingesta y operación RAG se comprobaron a
1889, 768 y 390 píxeles sin solapamientos ni desbordamiento horizontal. Un tenant
técnico vacío ejecutó una consulta real y obtuvo cero resultados; la métrica de
operación registró una consulta y 100 % sin resultado. Esta validación no mide
capacidad, estrés, HA ni objetivos de producción.

## Dependencias externas usadas por el conocimiento

El centro administrativo de salud complementa la observabilidad RAG con
disponibilidad y latencia de Google Cloud, Banco de España y CISA KEV. Estas
señales se obtienen de endpoints públicos oficiales, se persisten por
organización y pueden activar reglas no-code con muestras consecutivas,
cooldown y runbook. Se muestra el último contacto satisfactorio para no confundir
un fallo actual con una fuente que nunca respondió.

La salud pública de Google Cloud no representa proyectos concretos; la
disponibilidad de una serie del Banco de España no acredita todos sus servicios;
y CISA KEV no demuestra exposición local. La operación y rollback completos
están en `docs/admins/PLATFORM_INFRASTRUCTURE_HEALTH.md`; evidencia en
`docs/audits/PLATFORM_EXTERNAL_PROVIDER_ALERTS_2026-08-01.md`.

Cada regla de salud debe referenciar uno de los runbooks versionados que entrega
`GET /api/admin/infrastructure-health/runbooks`. Existen procedimientos
específicos para PostgreSQL RAG y para cada proveedor externo. La interfaz los
presenta como títulos y pasos, no como códigos técnicos. Ningún runbook ejecuta
acciones sobre la infraestructura. Evidencia:
`docs/audits/PLATFORM_HEALTH_RUNBOOKS_2026-08-01.md`.

## Infraestructura externa y custodia portable

El contrato de entrega productiva está en
`docs/RAG_EXTERNAL_INFRASTRUCTURE_HANDOFF.md` y sus plantillas en
`docs/templates/`. Separa parámetros consumidos por el runtime, decisiones del
cliente y adaptadores aún pendientes; una plantilla vacía nunca acredita una
capacidad operativa.

Los originales admiten `minio`, `aws-s3` y `s3-compatible`. Todos exigen
versionado, `VersionId` y Object Lock verificable. En producción el bucket se
aprovisiona externamente (`RAG_OBJECT_STORE_AUTO_PROVISION=false`). AWS S3 puede
usar la cadena estándar de credenciales del SDK y el rol del workload sin
guardar access keys en Flentio.

`RAG_OBJECT_KEY_PROVIDER=static` conserva el formato AES-256-GCM v1. La opción
`aws-kms` solicita una data key AES-256 a KMS por original, cifra localmente y
guarda únicamente la clave envuelta dentro del formato v2. Tenant, identificador
de objeto y checksum forman parte tanto del AAD como del Encryption Context. El
descifrado permite claves KMS históricas para que una rotación no impida
restaurar versiones anteriores. Azure Blob/GCS y sus KMS nativos siguen
`NO_IMPLEMENTADO`; requieren adaptadores explícitos, no variables decorativas.

Evidencia de migración y regresión:
`docs/audits/RAG_EXTERNAL_INFRASTRUCTURE_2026-08-01.md`.

## Reconciliación WORM

La migración 010 implementa una cola durable que compara cada versión
verificada con PostgreSQL: tamaño, ETag, checksums, legal hold y retención. El
scheduler procesa lotes, se recupera tras una caída y funciona en varios nodos
mediante reclamación PostgreSQL. Nunca corrige ni borra automáticamente.
Operación, parámetros, alertas y rollback:
`docs/RAG_WORM_RECONCILIATION.md`; evidencia:
`docs/audits/RAG_WORM_RECONCILIATION_2026-08-01.md`.
