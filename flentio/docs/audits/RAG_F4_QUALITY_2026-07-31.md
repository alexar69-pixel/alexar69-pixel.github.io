# Evidencia de validación F4 — 31-07-2026

## Dictamen

**VALIDACIÓN local**, no terminada ni certificada para banca. La canalización real funciona con PostgreSQL/pgvector, Ollama, MinIO, ClamAV y TEI/GTE en contenedores y GPU. La muestra aislada no bancaria demuestra comportamiento funcional, no escala ni calidad representativa.

## Entorno y datos

- PostgreSQL 16, pgvector 0.8.6;
- TEI 1.9 y revisión fijada de GTE multilingual reranker;
- embeddings reales `nomic-embed-text`, 768 dimensiones, servidos por Ollama;
- seis documentos no bancarios: norma, contrato, procedimiento, informe inglés, tabla e histórico;
- cinco preguntas con fuentes y citas esperadas;
- ninguna copia de datos de cliente o bancarios.

## Evidencia ejecutada

| Comprobación | Resultado real |
|---|---|
| Migraciones 001–005 aplicadas dos veces | OPERATIVO, idempotentes |
| Pruebas backend | 28/28 superadas |
| Validación F4 integral | VALIDADO |
| Multilingüe inglés/español | Superada |
| Filtro de captura temporal | Superado |
| Lectura entre tenants | Bloqueada por RLS |
| Umbral sin evidencia | `EVIDENCIA_INSUFICIENTE`, sin invención |
| Caída del reranker | Fallo cerrado y métrica registrada |
| Índice GIN multilingüe | `Bitmap Index Scan` verificable con `EXPLAIN (ANALYZE, BUFFERS)` |
| Interfaz real, 1280×720 y 390×844 | Sin recortes/solapamientos en el flujo RAG; selector móvil accesible |
| Consola en navegación y consulta | 0 errores, 0 avisos |
| Auditoría npm de producción | backend 0; frontend 0 vulnerabilidades |

## Comparación de recuperación

Resultados de `backend/test/fixtures/rag-f4-quality.json` tras corregir y probar que nDCG no contabilice repetidamente chunks de una misma fuente:

| Métrica | Base híbrida | TEI/GTE | Delta |
|---|---:|---:|---:|
| Recall@K | 1,000 | 1,000 | 0,000 |
| MRR | 1,000 | 1,000 | 0,000 |
| nDCG@K | 1,000 | 1,000 | 0,000 |
| Precisión media | 0,240 | 0,613 | +0,373 |
| Precisión automática de citas | 0,200 | 0,357 | +0,157 |
| p50 | 62 ms | 107 ms | +45 ms |
| p95 | 166 ms | 120 ms | -46 ms |
| p99 | 166 ms | 120 ms | -46 ms |

Las latencias no permiten concluir que el reranker sea más rápido: sólo hubo cinco preguntas, calentamiento/caché y ejecución secuencial local. Sirven para reproducibilidad, no para un SLO.

## Controles de honestidad

- El evaluador consulta datos realmente indexados y no inserta respuestas.
- El corpus se etiqueta `AISLADO_NO_BANCARIO` y exige confirmación explícita.
- La fidelidad aparece como `NO_EVALUADA`; requiere jueces humanos/protocolo aprobado.
- No se atribuye mejora a expansión/descomposición: no están activas.
- Los fallos de proveedor no generan puntuaciones o citas ficticias.
- La prueba visual apuntó al backend F4 real y a PostgreSQL/ClamAV/MinIO/TEI reales. La consulta de interacción usó un tenant sin documentos y obtuvo `EVIDENCIA_INSUFICIENTE`; no se interceptó ni simuló la red.

## Validación visual y dependencias

Playwright abrió `http://127.0.0.1:3100/admin?tab=settings`, accedió a **Ingesta RAG / Drive**, comprobó estado `OPERATIVO`, ejecutó una consulta y verificó la respuesta sin evidencia. Se probaron 1280×720 y 390×844. En móvil, las seis pestañas se sustituyen por un selector completo y las rejillas avanzadas pasan a una columna, evitando el recorte observado antes de la corrección.

La auditoría detectó el aviso alto `GHSA-qwww-vcr4-c8h2` en React Router 7.18.1. El frontend no usa las API RSC inestables afectadas, pero para no aceptar una alerta alta se migraron los imports DOM al paquete unificado `react-router` 8.3.0, versión corregida disponible, y se repitieron auditoría, build y navegación. El resultado final es cero vulnerabilidades npm de producción en backend y frontend. El linter conserva avisos preexistentes de código no utilizado/hooks fuera del alcance F4; no hay errores de lint.

## Riesgos que impiden cerrar F4

1. Ejecutar evaluación con decenas de miles de documentos representativos y consultas bancarias autorizadas.
2. Aprobar objetivos mínimos, presupuesto p95/p99 y umbral por parte de negocio, riesgo y seguridad.
3. Validar citas y fidelidad con jueces humanos.
4. Realizar carga/concurrencia, pentest y revisión independiente.
5. Decidir proveedor, región, contrato, residencia y HA de producción.
6. Ensayar conmutación y rollback productivos versionados.

## Reproducción

Configurar servicios reales según `docs/developers/RAG_OPERATIONS.md`, ejecutar `npm run migrate:rag` dos veces, `npm test`, `npm run validate:rag-f4` con su confirmación aislada y `RAG_EVALUATION_ORGANIZATION=<org> npm run evaluate:rag -- test/fixtures/rag-f4-quality.json`. Los secretos de la ejecución efímera no se conservan en este informe.
