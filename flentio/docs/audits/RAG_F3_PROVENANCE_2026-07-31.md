# Evidencia de validación RAG F3 — 2026-07-31

## Dictamen

F3 queda en **VALIDACIÓN local**. La implementación es real y no utiliza mocks: PostgreSQL 16/pgvector, ClamAV y un servidor MinIO single-node aislado en Docker. No equivale a certificación ni preparación para carga bancaria.

## Controles implementados

- migración idempotente de procedencia, originales, estados y eventos;
- índices parciales para lectura de documentos efectivos e índices de claves foráneas;
- RLS forzado y comprobación `manage` para gobierno documental;
- AES-256-GCM autenticado antes de cargar en MinIO;
- versionado, Object Lock, legal hold y retención GOVERNANCE reales;
- comprobación de escritura y lectura de vuelta de controles WORM;
- restauración con doble SHA-256 y autenticación GCM;
- citas PDF con página y otros formatos con sección cuando existe;
- exclusión de documentos expirados y sustituidos;
- ninguna API de borrado físico ni permiso DELETE para la identidad de aplicación.

## Evidencia ejecutada

- pruebas unitarias backend: cifrado/restauración, manipulación del cifrado y fragmentación estructural;
- carga real limpia de extremo a extremo hasta trabajo `completed`;
- descarga idéntica byte a byte y checksum original coincidente;
- PDF real de tres páginas, con recuperación y cita de página 2;
- legal hold leído como `ON`; después de un DELETE administrativo la versión exacta siguió legible y protegida (MinIO puede confirmar la petición aunque no elimine el objeto);
- retención GOVERNANCE futura aplicada a la versión;
- sustitución y expiración excluidas de consultas de lector;
- consulta de procedencia de otro tenant sin resultados;
- migraciones repetidas para verificar idempotencia;
- auditoría de dependencias de producción sin vulnerabilidades conocidas en npm.

### Resultado final reproducible

El comando `npm run validate:rag-f3`, protegido por `RAG_F3_VALIDATION_CONFIRM=YES_ISOLATED_ENVIRONMENT`, devolvió:

- trabajo `completed`;
- original `verified` con `VersionId`;
- restauración idéntica byte a byte;
- procedencia inaccesible desde otro tenant;
- versión preservada y legal hold `ON` tras un intento de DELETE;
- documento expirado ausente de la recuperación.

La última ejecución partió de volúmenes vacíos. Las cuatro migraciones se aplicaron dos veces sin error con pgvector `0.8.6` y columna `vector(768)`. Un intento previo deliberadamente incompleto falló antes de crear el esquema (`to_regnamespace('flentio_rag') = NULL`); esto valida el nuevo preflight que impide fijar accidentalmente una dimensión por defecto. `EXPLAIN` seleccionó `rag_documents_effective_list_idx` y la consulta de catálogo no encontró claves foráneas sin índice.

MinIO reportó `RELEASE.2025-10-15T17-29-55Z`, commit `9e49d5e7a648`, Go `1.24.8`. Backend: 21/21 pruebas; `npm audit --omit=dev`: 0 vulnerabilidades. Frontend: compilación Vite completada; conserva un aviso no bloqueante por bundle superior a 500 kB.

## Riesgos abiertos

1. MinIO está en un solo nodo y su repositorio fue archivado: sólo desarrollo.
2. La clave AES reside en configuración: falta KMS/HSM, rotación y recifrado.
3. Falta reconciliación automática entre almacenamiento y PostgreSQL.
4. Falta política bancaria aprobada de retención/destrucción por jurisdicción.
5. Faltan HA, DR, carga representativa, pentest y revisión independiente.

## Criterio de salida hacia producción

Seleccionar proveedor de objetos soportado, integrar KMS/HSM, definir modo y plazos regulatorios, implementar reconciliación y borrado gobernado, completar F6/DR y repetir las pruebas con corpus y controles autorizados por el banco.
