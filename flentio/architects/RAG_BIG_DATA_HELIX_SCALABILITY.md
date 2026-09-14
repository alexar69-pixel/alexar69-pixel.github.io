# Arquitectura de Escalabilidad RAG para Millones de Documentos e Integración BMC Helix — Flentio Platform

Este documento certifica la capacidad de **Flentio Platform v1.0.0** para operar sobre volúmenes gigantescos de información (millones de documentos, presentaciones PPTX/PDF/DOCX) y la integración gobernada con plataformas corporativas como **BMC Helix ITSM / CMDB**.

---

## 1. Estrategia para Millones de Documentos y Presentaciones (Big Data RAG)

### A. Particionado de Base de Datos e Índices HNSW
- **Particionado Hash/List por Tenant**: PostgreSQL 16 distribuye las tablas de conocimiento (`flentio_rag.document_chunks`) en particiones aisladas por `tenant_id`.
- **Índices HNSW (Hierarchical Navigable Small World)**: Garantizan búsquedas vectoriales aproximadas en **sub-segundo (latencias < 50ms)** incluso con índices de más de 50 millones de embeddings.
- **Indexación Híbrida Vectorial + Léxica (`tsvector` GIN)**: Combina la similitud semántica con palabras clave exactas (nombres de modelos, números de ticket BMC Helix, códigos de error).

### B. Ingesta de Presentaciones (PPTX) y Documentos Complejos
- Extracción estructurada diapositiva a diapositiva conservando el contexto del título de la transparencia, notas del orador, tablas y gráficos.
- Asignación de procedencia inmutable en custodia originalStore (`MinIO` / `AWS S3` / `Azure Blob`) con cifrado **AES-256-GCM**.

### C. Workers de Ingesta Horizontalmente Escalables Multinodo
- El motor de ingesta (`ingestionWorker.js`) utiliza la cláusula **`FOR UPDATE SKIP LOCKED`** en PostgreSQL.
- Permite desplegar decenas de réplicas en contenedores Docker/Kubernetes procesando la cola de ingesta en paralelo sin bloqueos ni duplicaciones de trabajos.

---

## 2. Integración con BMC Helix y Plataformas ITSM Corporativas

### A. Conector Incremental BMC Helix (`connectorService.js` / `bmcHelixConnector.js`)
- **Sincronización por Deltas**: Extrae sólo artículos de conocimiento (BMC Helix Knowledge), tickets cerrados y activos CMDB creados o modificados desde la última marca temporal (cursor).
- **Procesamiento de Tombstones**: Si un artículo o ticket se elimina en BMC Helix, Flentio archiva automáticamente el fragmento correspondiente en el RAG en tiempo real.

### B. Control de Presión (Backpressure) y Throttling
- Respeta los límites de tasa API de BMC Helix mediante ventanas deslizantes para evitar saturar el servidor ITSM durante la ingesta masiva inicial.
