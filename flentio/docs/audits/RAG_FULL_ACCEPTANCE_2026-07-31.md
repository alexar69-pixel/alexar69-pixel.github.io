# Aceptación local integral del RAG — 31-07-2026

## Dictamen

Las fases F0–F7 están implementadas y han superado una aceptación local integrada con servicios reales. El resultado es `VALIDACIÓN local integral`, no certificación bancaria ni autorización de producción. No se utilizaron datos de clientes. Los tres documentos del ensayo están marcados `SINTÉTICO NO CLIENTE — NO ACREDITA PRODUCCIÓN`.

## Entorno realmente ejecutado

- PostgreSQL 16 con pgvector y RLS, rol de aplicación limitado y migraciones 001–008.
- Ollama con `nomic-embed-text`, embeddings de 768 dimensiones.
- TEI 1.9 con `Alibaba-NLP/gte-multilingual-reranker-base` sobre GPU.
- ClamAV 1.4 y firmas reales.
- MinIO `RELEASE.2025-10-15T17-29-55Z`, single-node de desarrollo.
- Backend y worker RAG separados.
- Google Drive y Google Docs reales mediante OAuth `drive.readonly`.

La carpeta real de ensayo fue `Flentio RAG Testing`, ID `1Dh_URmMZcxZR7-aa88slWJw_ipdnSpk1`. Contenía tres Google Docs nativos con marcadores únicos: política de acceso, recuperación ante índice incompleto y guía multilingüe. Una modificación posterior añadió `REVISION-DRIVE-001` a los tres documentos para comprobar el feed incremental.

## Evidencia de extremo a extremo

1. OAuth completó autorización, canje, verificación contra Drive y custodia cifrada del refresh token. Los tokens no llegaron al frontend.
2. La sincronización inicial exportó y descargó los tres Google Docs reales, los sometió a ClamAV, conservó originales cifrados, creó procedencia y generó embeddings reales.
3. El feed de cambios detectó tres modificaciones. La reconciliación posterior reparó los eventos que habían fallado durante el descubrimiento del defecto descrito más abajo.
4. El estado final contiene 3 documentos activos `ready/effective`, versión 2, un fragmento vigente y un embedding vigente por documento en el índice activo.
5. Tres consultas —español, inglés y recuperación— devolvieron el documento esperado como primera evidencia, aplicaron reranker y tardaron 180, 135 y 123 ms. La muestra es demasiado pequeña para acreditar un SLO.
6. La descarga de los tres originales devolvió HTTP 200; tamaños 686, 712 y 688 bytes; el SHA-256 declarado coincidió con los bytes y todos conservaron `REVISION-DRIVE-001`.
7. La prueba RLS devolvió 3 documentos para el mismo tenant con clearance `INTERNAL`, cero con `PUBLIC` y cero desde otro tenant.
8. Un fichero EICAR real y no dañino fue rechazado por ClamAV con HTTP 422 y `Eicar-Test-Signature`; no llegó al índice ni solicitó aprobación.
9. La reindexación creó un candidato real, completó 3/3 embeddings, lo activó, consultó sobre él y revirtió atómicamente al índice original. Se reutilizó deliberadamente el mismo modelo: valida la mecánica, no una mejora de calidad.
10. Observabilidad terminó en `OPERATIVO`, cola cero, cero fallos de ingesta sin resolver y tres fallos históricos preservados. Prometheus diferencia `ingestion_failed_unresolved` de `ingestion_failed_historical`.
11. La interfaz autenticada fue inspeccionada con Chromium real a 1440, 1024 y 768 píxeles. No hubo errores de consola, respuestas API fallidas ni solapamientos de texto. Las capturas están en `output/playwright/`.

## Defectos descubiertos y corregidos

- La clave del rate limiter normalizaba mal IPv6. Ahora usa el generador oficial y prioriza la identidad autenticada.
- La ingesta insertaba fragmentos y después intentaba releerlos mientras el documento seguía `processing`; RLS ocultaba esas filas y el trabajo podía terminar sin vectores. Los UUID se generan antes del insert y los embeddings se vinculan sin relajar RLS.
- La consulta de observabilidad reservaba un parámetro SQL que PostgreSQL no podía tipar. El período usa ahora el primer parámetro real.
- Los fallos históricos mantenían una alerta crítica después de una reconciliación correcta. Se conservan como historia, pero sólo los fallos sin una ejecución posterior completada activan la alerta.

## Regresión final

- Backend: 32/32 pruebas superadas.
- Backend `npm audit --omit=dev`: cero vulnerabilidades.
- Frontend: compilación Vite superada.
- Frontend `npm audit --omit=dev`: cero vulnerabilidades.
- Advertencia conocida: el bundle principal minificado mide aproximadamente 1,45 MB; requiere separación futura, pero no invalida la función RAG.

## Límites y puertas de producción

- Corpus de tres documentos sintéticos: no demuestra decenas de miles de documentos, concurrencia, calidad bancaria ni los SLO provisionales.
- Los webhooks de Drive no se probaron porque el desarrollo no dispone de URL pública HTTPS. La sincronización incremental por cursor y la reconciliación sí se probaron.
- No hay HA en este entorno por decisión expresa de desarrollo.
- MinIO single-node no es una selección productiva; faltan KMS/HSM y HA/DR.
- No se ha conectado un SIEM/WORM durable ni guardias operativas.
- No existe BIA de cliente, IdP corporativo ni corpus bancario autorizado.
- La revisión independiente de seguridad y cumplimiento sigue siendo una puerta obligatoria previa a producción; las pruebas internas no la sustituyen.

Por estas razones no se utiliza el estado `TERMINADA`. La siguiente etapa válida es preparación productiva con decisiones del cliente y evidencia de carga, resiliencia, recuperación y control independiente.
