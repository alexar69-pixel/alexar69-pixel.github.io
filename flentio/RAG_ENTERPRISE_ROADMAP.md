# Plan maestro de evolución del RAG empresarial

## Propósito y límites

Este documento permite que Codex u otra IA continúe la evolución del RAG sin depender del contexto de una conversación anterior. Combina planificación y estado comprobado: cada fase indica qué está implementado en `VALIDACIÓN`; los trabajos y criterios todavía pendientes **no deben mostrarse como operativos** hasta aportar su evidencia.

Queda expresamente fuera de alcance cualquier OCR. Los PDF sin capa de texto seguirán rechazándose de forma explícita.

Son obligatorias en todas las fases las dos normas del proyecto:

1. documentar código, configuración, operación, riesgos y resultados reales;
2. no utilizar mocks, simulaciones ni respuestas ficticias en recorridos productivos.

## Estado de partida verificable

Antes de iniciar una fase, la IA ejecutora debe comprobar el estado actual y no asumirlo:

- PostgreSQL 16 con pgvector y esquema `flentio_rag`;
- aislamiento RLS por organización y rol `flentio_rag_app` sin `BYPASSRLS`;
- recuperación híbrida HNSW + `tsvector` español + RRF;
- embeddings reales de Ollama u OpenAI;
- cola persistente y servicio `rag-worker` recuperable;
- extracción de PDF con texto, DOCX y formatos textuales;
- conectores Google Drive y EUR-Lex;
- métricas básicas y evaluación Recall@K/MRR.

La línea base mínima es: pruebas del backend, auditoría de dependencias, compilación del frontend, migración idempotente e ingesta/consulta real contra un entorno efímero pgvector. Si alguna falla, debe resolverse o registrarse como bloqueo antes de ampliar funcionalidad.

## Reglas de ejecución para cualquier IA

- Trabajar una fase cada vez y respetar el orden de dependencias.
- Inspeccionar el repositorio antes de decidir nombres, rutas o migraciones.
- Preservar cambios ajenos y no borrar datos históricos.
- Diseñar migraciones compatibles y repetibles; nunca modificar en producción una dimensión vectorial en el sitio.
- Aplicar autorización dentro de PostgreSQL antes de recuperar fragmentos, no filtrar resultados después.
- Utilizar servicios externos sólo con credenciales reales y estados `NO_CONFIGURADO`/`NO_DISPONIBLE` cuando falten.
- No declarar una fase terminada con pruebas omitidas, datos inventados o infraestructura no verificada.
- Actualizar `docs/developers/RAG_OPERATIONS.md`, `memoria_descriptiva_flentio.md`, el sitio documental y el manual corporativo externo en cada fase.
- Entregar siempre: archivos cambiados, decisiones, migración, pruebas ejecutadas, resultados, limitaciones y procedimiento de reversión.

## Orden de ejecución

```text
F0 Línea base
 └─ F1 Gobierno y autorización documental
     ├─ F2 Cuarentena y seguridad de ingesta
     └─ F3 Procedencia y ciclo de vida
         └─ F4 Calidad de recuperación
             ├─ F5 Sincronización incremental
             └─ F6 Escala, HA y reindexación
                 └─ F7 Observabilidad y auditoría
```

F2 y F3 pueden diseñarse en paralelo después de F1, pero sus migraciones deben integrarse de forma secuencial. F5 no debe desplegarse hasta que F3 defina la procedencia canónica.

## F0. Línea base y contrato de arquitectura

**Objetivo:** congelar una referencia medible antes de introducir cambios.

**Trabajo:** inventariar tablas, políticas RLS, funciones `SECURITY DEFINER`, endpoints, conectores, configuración y volumen; capturar `EXPLAIN (ANALYZE, BUFFERS)` de consulta híbrida; registrar Recall@K, MRR, p50/p95/p99, tasa sin resultados, trabajos/minuto y tamaño del índice con un conjunto real autorizado.

**Entregables:** informe `docs/audits/RAG_BASELINE_<fecha>.md`, conjunto de evaluación sin datos sensibles en Git o referencia segura a él, y matriz de amenazas/datos.

**Aceptación:** resultados reproducibles; consultas entre dos tenants demuestran aislamiento; backup y restauración del entorno de prueba comprobados; ningún dato bancario se copia a fixtures.

**Reversión:** no aplica, porque la fase debe ser de sólo lectura salvo documentación.

## F1. Gobierno y autorización documental avanzada

**Objetivo:** impedir que un usuario recupere un fragmento que no esté autorizado a conocer.

**Modelo previsto:** clasificación, jurisdicción, entidad jurídica, grupos autorizados, propietario, residencia, fechas de vigencia y etiquetas de expediente. Separar atributos documentales de ACL para evitar arrays ilimitados. Indexar columnas usadas por RLS y comprobar sus planes.

**Trabajo:**

- definir taxonomías y herencia de permisos con negocio y seguridad;
- añadir tablas normalizadas de clasificación y concesiones;
- extender el contexto de sesión con identidad y grupos verificados por el backend;
- crear políticas RLS sobre documentos, versiones y fragmentos;
- incluir permisos en ingesta, listado, consulta, archivado y conectores;
- crear una interfaz no-code para seleccionar clasificación y destinatarios;
- prohibir el filtrado de ACL exclusivamente en Node o en el frontend.

**Aceptación:** pruebas reales positivas y negativas por tenant, entidad, país, grupo y confidencialidad; `EXPLAIN` confirma índices utilizables; cambiar parámetros HTTP no amplía permisos; las citas nunca revelan títulos no autorizados.

**Reversión:** feature flag de lectura para volver temporalmente a RLS sólo por tenant, conservando las columnas nuevas; nunca eliminar ACL durante el rollback.

## F2. Cuarentena y seguridad de ingesta

**Objetivo:** evitar que contenido dañino o instrucciones hostiles entren en el conocimiento activo.

**Trabajo:**

- crear estados `received`, `quarantined`, `scanning`, `approved`, `rejected` e `indexed` con transiciones auditables;
- integrar un antivirus real elegido por despliegue y comprobar firma/estado del motor;
- limitar descompresión, páginas, relaciones DOCX, tiempo, memoria y frecuencia;
- detectar prompt injection documental mediante reglas deterministas y, opcionalmente, un clasificador real versionado;
- almacenar hallazgos y confianza sin convertirlos automáticamente en instrucciones;
- exigir aprobación humana según clasificación/riesgo;
- hacer que sólo `approved/indexed` participe en recuperación.

**Aceptación:** archivo EICAR en un entorno de seguridad controlado queda rechazado por el motor real; formatos manipulados y bombas de descompresión se detienen por límites; un documento con instrucciones hostiles nunca se incorpora al contexto antes de aprobarse; toda transición tiene actor, fecha y motivo.

**Reversión:** detener nuevas ingestas y mantener consulta sobre documentos previamente aprobados; no saltarse la cuarentena como mecanismo de continuidad.

## F3. Procedencia, vigencia y ciclo de vida

**Estado 01-08-2026: VALIDACIÓN local ampliada.** Implementación y evidencia en `docs/RAG_PROVENANCE_LIFECYCLE.md`, `docs/RAG_WORM_RECONCILIATION.md`, `docs/adr/ADR-RAG-003-procedencia-minio.md`, `docs/audits/RAG_F3_PROVENANCE_2026-07-31.md` y `docs/audits/RAG_WORM_RECONCILIATION_2026-08-01.md`. La reconciliación durable verificó 9/9 originales locales comparando evidencia, legal hold y retención. La validación usa MinIO real single-node; no hay HA y no se considera una selección productiva. El borrado gobernado permanece pendiente de una política bancaria aprobada, por lo que no existe eliminación física automática.

**Objetivo:** demostrar de dónde procede cada afirmación y si sigue siendo aplicable.

**Trabajo:** registrar URI/ID de origen, checksum, página/sección, extractor y versión, fragmentador y versión, embedding/modelo/dimensión, fecha de captura, propietario, aprobación, vigencia, revisión, retención y legal hold. Implementar estados `draft`, `approved`, `effective`, `superseded`, `expired`, `archived` y borrado gobernado. Guardar originales en almacenamiento de objetos real y cifrado; PostgreSQL conserva referencias y conocimiento extraído.

**Aceptación:** una cita permite localizar el original y la ubicación exacta; documentos vencidos o sustituidos se excluyen según política; legal hold impide borrado; el checksum detecta alteraciones; la restauración conjunta de objeto y metadatos funciona.

**Reversión:** mantener datos nuevos y volver a la selección de versiones anterior mediante feature flag; no destruir originales ni cadena de custodia.

## F4. Calidad de recuperación

**Estado 01-08-2026: VALIDACIÓN local ampliada.** Se implementaron fragmentación tipada, búsqueda léxica multilingüe, filtros temporales, reranker real TEI/GTE, umbral y evaluación comparativa. La v3 añade metadatos GIN, pool ampliado y diversidad por documento: corrigió los tres fallos EPC de v2 y obtuvo Recall@K 1,0000, MRR 0,96875 y p95 878 ms sobre 16 consultas públicas verificadas, sin 429. Diseño: `docs/RAG_RETRIEVAL_QUALITY.md` y `docs/RAG_PUBLIC_BANKING_CORPUS.md`; evidencia: `docs/audits/RAG_F4_CANDIDATE_DIVERSITY_2026-08-01.md`. El corpus público no sustituye políticas privadas, jueces humanos, escala/SLO, proveedor productivo ni revisión independiente.

**Objetivo:** mejorar precisión sin sacrificar seguridad, citas o latencia acordada.

**Trabajo:**

- implementar fragmentadores versionados por normativa, contrato, procedimiento, informe y tabla;
- añadir búsqueda multilingüe y filtros temporales;
- evaluar expansión/descomposición de consultas sólo cuando aporte una mejora medible;
- integrar un reranker real detrás de una interfaz de proveedor con timeout y fallo explícito;
- definir umbral de evidencia insuficiente y obligar a responder sin evidencia cuando corresponda;
- medir Recall@K, MRR, nDCG, precisión de citas y fidelidad con jueces humanos o evaluación aprobada;
- registrar versión completa de la canalización para reproducibilidad.

**Aceptación:** mejora acordada frente a F0 en el conjunto bancario; cero regresiones de autorización; citas correctas verificadas; presupuesto p95 cumplido; caída del reranker produce un estado observable y una política de degradación previamente aprobada, nunca puntuaciones ficticias.

**Reversión:** conmutación versionada hacia el recuperador anterior y conservación del índice previo.

## F5. Sincronización incremental y conectores

**Estado 31-07-2026: VALIDACIÓN local integral.** Cursores, cola durable, idempotencia, tombstones, reconciliación, webhook renovable y panel no-code están implementados. OAuth y Google Drive reales se validaron con tres Google Docs sintéticos, una modificación incremental y reconciliación. Evidencia: `docs/audits/RAG_F5_CONNECTORS_2026-07-31.md` y `docs/audits/RAG_FULL_ACCEPTANCE_2026-07-31.md`; operación y mercado: `docs/RAG_INCREMENTAL_CONNECTORS.md`; decisión: `docs/adr/ADR-RAG-005-conectores-incrementales.md`. Quedan webhook HTTPS, movimientos/borrados/revocación, carga representativa y revisión independiente.

**Ampliación 01-08-2026: VALIDACIÓN local.** El frontend ofrece plantillas del
corpus público y un formulario modelo HTTPS/CELEX. Fuentes y ejecuciones son
durables y RLS. La migración 013 añade revisión humana auditable de la fuente:
guardar no ejecuta, cualquier cambio invalida la aprobación y el historial
permite revisar y relanzar a voluntad. La migración 014 separa descarga de
publicación: el worker ejecuta seguridad, custodia y extracción reales, deja el
resultado en staging y sólo una segunda decisión humana encola la ingesta. La UI
muestra hashes, evidencia ClamAV, comparación y texto, permite restaurar el
original y registra publicación o rechazo con nota. Es manual bajo demanda: no se afirma
scheduling, HA ni escala. Diseño y evidencia:
`docs/RAG_EXTERNAL_DOCUMENT_SOURCES.md` y
`docs/audits/RAG_EXTERNAL_DOCUMENT_SOURCES_2026-08-01.md`.

**Objetivo:** mantener el conocimiento actualizado sin releer repositorios completos.

**Trabajo:** implementar tokens de cambios, cursores duraderos, webhooks con firma, renovación de suscripciones, idempotencia, tombstones y reconciliación periódica para Google Drive; aplicar el mismo contrato a futuros conectores. Incorporar límites por tenant, backpressure y cola de errores operable.

**Aceptación:** crear, modificar, mover y eliminar un archivo real produce exactamente el cambio esperado; repetir un evento no duplica versiones; perder un webhook se corrige en reconciliación; revocar OAuth cambia el conector a `NO_DISPONIBLE` sin inventar sincronización.

**Reversión:** deshabilitar webhooks y volver a reconciliación completa controlada, preservando cursores para diagnóstico.

## F6. Escala, alta disponibilidad y reindexación sin corte

**Estado 31-07-2026: VALIDACIÓN local.** Se implementaron índices coexistentes por tenant/dimensión, backfill resumible, pausa, evaluación, conmutación y rollback atómicos. La aceptación integrada ejecutó un backfill real 3/3 con Ollama, activó el candidato, consultó y revirtió al índice original. La muestra valida la mecánica, no escala ni mejora del modelo. HA fue aplazada expresamente durante desarrollo. Véanse `docs/RAG_ONLINE_REINDEXING.md`, `docs/adr/ADR-RAG-006-reindexacion-online.md`, `docs/audits/RAG_F6_REINDEX_2026-07-31.md` y `docs/audits/RAG_FULL_ACCEPTANCE_2026-07-31.md`.

**Objetivo:** soportar crecimiento y cambios de embeddings con continuidad verificable.

**Trabajo:**

- instrumentar y demostrar la baseline provisional de SLO, RPO y RTO definida en `docs/RAG_PRODUCTION_READINESS.md`; cada banco deberá confirmarla o sustituirla mediante BIA;
- probar PgBouncer, pools acotados, múltiples workers y límites por tenant;
- configurar backups cifrados, PITR, réplica y restauraciones periódicas;
- introducir índices/lotes de embeddings versionados con estados `building`, `evaluating`, `active`, `retired`;
- efectuar backfill resumible y con límites de carga;
- comparar índice candidato y activo con el mismo conjunto de evaluación;
- realizar conmutación atómica y conservar ventana de rollback;
- ensayar fallo de nodo, worker y proveedor de embeddings.

**Aceptación:** carga objetivo sostenida con datos representativos; RPO/RTO demostrados; restauración exitosa; reindexación no bloquea consultas; cambio y rollback atómicos; no hay conexiones ilimitadas ni consultas sin índice en rutas críticas.

**Reversión:** puntero atómico al índice anterior y detención segura del backfill; eliminación del índice candidato sólo después del periodo de retención aprobado.

## F7. Observabilidad, auditoría y operación bancaria

**Estado 31-07-2026: VALIDACIÓN local integral.** Snapshot RLS, alertas/runbooks, exportación Prometheus y auditoría PostgreSQL append-only están implementados. La aceptación visual autenticada cubrió 1440, 1024 y 768 píxeles sin solapamientos, errores de consola ni peticiones RAG fallidas. Evidencia: `docs/audits/RAG_F7_OBSERVABILITY_2026-07-31.md` y `docs/audits/RAG_FULL_ACCEPTANCE_2026-07-31.md`; operación y mercado: `docs/RAG_OBSERVABILITY_AUDIT.md`; objetivos provisionales y SIEM: `docs/RAG_PRODUCTION_READINESS.md`; decisión: `docs/adr/ADR-RAG-007-observabilidad-auditoria.md`. Faltan entrega SIEM/WORM real, demostración de SLO/RPO/RTO, carga y guardias.

**Revalidación 01-08-2026:** tras el corte PostgreSQL transversal se comprobó
la interfaz real de ingesta y operación a 1889, 768 y 390 píxeles, sin
solapamientos, desbordamiento horizontal ni errores de consola. El Copiloto
ejecutó recuperación real sobre un tenant técnico vacío y devolvió evidencia
insuficiente sin generar contenido. El estado continúa en `VALIDACIÓN` porque
las puertas externas anteriores no han sido satisfechas.

**Objetivo:** permitir operación, investigación y auditoría sin acceder al contenido sensible innecesariamente.

**Trabajo:** panel real de documentos, fragmentos, cola, fallos, p50/p95/p99, tasa sin resultados, frescura, conectores, capacidad, calidad y versiones de índice; métricas exportables; logs estructurados con correlación; auditoría append-only o destino inmutable; integración SIEM; alertas con runbooks.

**Aceptación:** cada gráfico coincide con consultas verificables; alertas se prueban provocando fallos controlados; un auditor puede reconstruir carga, aprobación, consulta, cambio y archivo; preguntas y fragmentos no aparecen en logs por defecto; retención y acceso están documentados.

**Reversión:** el panel puede deshabilitarse sin afectar ingesta o consulta; la auditoría no debe poder desactivarse desde la aplicación.

## Puertas obligatorias por fase

Una fase sólo cambia a `TERMINADA` si cumple todas estas puertas:

| Puerta | Evidencia obligatoria |
|---|---|
| Funcional | Recorrido real reproducible y resultado esperado |
| Seguridad | Pruebas negativas, RLS y revisión de secretos/datos |
| Calidad | Métricas comparadas con la línea base |
| Rendimiento | Planes SQL y p95/p99 con volumen representativo |
| Resiliencia | Fallo y recuperación ensayados |
| Operación | Runbook, alertas y rollback comprobados |
| Documentación | Código, documentación interna, sitio y manual alineados |
| Dependencias | Auditoría sin vulnerabilidades críticas/altas no aceptadas |

Los estados válidos son `NO_INICIADA`, `EN_CURSO`, `BLOQUEADA`, `VALIDACIÓN` y `TERMINADA`. “Código escrito” no equivale a `TERMINADA`.

## Registro de decisiones y seguimiento

Cada fase debe mantener:

- `docs/adr/ADR-RAG-<número>-<tema>.md` para decisiones irreversibles o costosas;
- `docs/audits/RAG_<fase>_<fecha>.md` para evidencias;
- migración ascendente y procedimiento explícito de reversión;
- riesgos abiertos con propietario y fecha objetivo;
- tabla de avance en este documento.

| Fase | Estado inicial | Dependencia | Resultado esperado |
|---|---|---|---|
| F0 | VALIDACIÓN | RAG actual | Línea base local registrada; pendiente corpus representativo autorizado |
| F1 | VALIDACIÓN | F0 | ACL/RLS implementada y verificada localmente; pendiente corpus representativo e IdP corporativo |
| F2 | VALIDACIÓN | F1 | ClamAV/cuarentena/límites/aprobación verificados localmente; pendiente HA, SOC, IdP y revisión independiente |
| F3 | VALIDACIÓN local ampliada | F1 | Procedencia, restauración, Object Lock y reconciliación 9/9 verificados localmente; pendientes proveedor productivo, política de retención y HA |
| F4 | VALIDACIÓN local ampliada | F2 + F3 | Corpus oficial público y reranking verificados; pendientes corpus privado autorizado, fidelidad humana, carga/SLO y selección productiva |
| F5 | VALIDACIÓN local integral | F3 | OAuth, Drive inicial, cambios y reconciliación reales; pendientes webhook HTTPS, casos destructivos y escala |
| F6 | VALIDACIÓN local | F4 | Backfill, activación, consulta y rollback reales; HA y prueba de carga aplazadas |
| F7 | VALIDACIÓN local integral | F5 + F6 | Panel autenticado, métricas y auditoría verificados; SIEM/WORM y operación bancaria pendientes |

### Ampliación transversal — agentes con evidencia (01-08-2026)

**Estado: VALIDACIÓN local.** Los nodos RAG entregan evidencia estructurada a
los agentes; ausencia de evidencia evita la llamada al modelo y las respuestas
generadas deben usar JSON y citas `[E#]` verificadas. La migración 015 conserva
un rastro RLS con hashes y referencias, nunca pregunta/respuesta/contenido en
claro. Ollama `llama3.2:3b` superó un caso grounded; una salida sin cita fue
rechazada y una consulta vacía se abstuvo sin invocar un modelo inexistente.
OpenAI/Gemini siguen sin validación real. Diseño y evidencia:
`docs/RAG_AGENT_EVIDENCE_CONTRACT.md` y
`docs/audits/RAG_AGENT_EVIDENCE_2026-08-01.md`.

## Prompt de relevo para otra IA

Utilizar este texto al iniciar una fase:

> Trabaja exclusivamente en la fase `<FASE>` de `docs/RAG_ENTERPRISE_ROADMAP.md`. Lee primero `.agents/AGENTS.md`, el roadmap completo, `docs/developers/RAG_OPERATIONS.md` y el código afectado. Verifica la línea base; no asumas capacidades ni uses mocks productivos. Presenta antes de editar el alcance, dependencias y archivos previstos. Implementa migraciones idempotentes, seguridad en PostgreSQL, interfaz no-code cuando corresponda, pruebas reales y rollback. Actualiza toda la documentación obligatoria. No marques la fase terminada hasta aportar evidencia de cada puerta de aceptación. OCR está fuera de alcance.

## Decisiones que requieren autorización humana

La IA debe detenerse y pedir decisión antes de:

- elegir proveedor antivirus, reranker, almacenamiento de objetos, KMS/HSM o SIEM;
- fijar taxonomías de confidencialidad, residencia, retención o legal hold;
- definir SLO, RPO, RTO y regiones de réplica;
- utilizar datos bancarios reales en pruebas;
- habilitar borrado físico o migrar datos productivos;
- aceptar una vulnerabilidad o incumplir una puerta de calidad.

## Corte transversal de plataforma — 01-08-2026

El proceso web ya no carga SQLite: identidad, secretos, workflows, ejecuciones,
webhooks, cron, administración y auditoría usan `flentio_platform` en PostgreSQL,
mientras el conocimiento permanece aislado en `flentio_rag`. La auditoría de
plataforma es append-only, secuencial y verificable; la outbox SIEM es durable,
pero su transporte externo sigue `NO_CONFIGURADO`. La arquitectura permite
varios procesos y nodos de base de datos, sin declarar HA ni rendimiento.

El corte, opciones de PostgreSQL/backup/KMS/SIEM, rollback y límites constan en
`docs/PLATFORM_POSTGRES_CUTOVER.md`; evidencia reproducible en
`docs/audits/PLATFORM_POSTGRES_CUTOVER_2026-08-01.md`. Siguen requiriendo
autorización humana el proveedor de backup/objetos, KMS/HSM y SIEM.

La observabilidad transversal del 01-08-2026 incorpora además reglas no-code de
disponibilidad y latencia para Google Cloud, Banco de España y CISA KEV, con
último contacto satisfactorio calculado desde observaciones RLS. La prueba real
de latencia abrió y resolvió un incidente externo; no se simuló ninguna caída.
Evidencia: `docs/audits/PLATFORM_EXTERNAL_PROVIDER_ALERTS_2026-08-01.md`.

Las alertas transversales disponen además de ocho runbooks operables y
versionados. Las reglas no pueden guardar referencias inexistentes y el panel
muestra pasos, precauciones y fuentes oficiales sin ejecutar remediaciones.
Evidencia: `docs/audits/PLATFORM_HEALTH_RUNBOOKS_2026-08-01.md`.

## Compatibilidad con infraestructura externa — 01-08-2026

Se entrega el contrato `docs/RAG_EXTERNAL_INFRASTRUCTURE_HANDOFF.md` con intake,
hoja de parámetros y aceptación sin datos. El software admite ahora originales
en MinIO, AWS S3 o API S3 compatible, y cifrado envelope real mediante AWS KMS
además del formato estático heredado. La migración 009 amplía de forma explícita
los proveedores persistibles y conserva compatibilidad con objetos existentes.

La migración se aplicó sobre PostgreSQL/pgvector local y pasaron 56/56 pruebas.
No se llamó a AWS ni se afirma validación de ese entorno porque no existen
credenciales o recursos del cliente. Azure Blob, Google Cloud Storage, Azure
Managed HSM, Google Cloud KMS, SIEM/WORM e IdP continúan como adaptadores o
dependencias pendientes de elección y validación humana. Evidencia:
`docs/audits/RAG_EXTERNAL_INFRASTRUCTURE_2026-08-01.md`.
