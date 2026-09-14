# Evidencia F7 — 31-07-2026

Estado: `VALIDACIÓN local`.

- migraciones 001–008 aplicadas en PostgreSQL/pgvector real;
- migración 008 reaplicada de forma idempotente;
- transición real de prueba `pending → processing → failed` generó tres eventos con correlación y sólo código de error;
- otro tenant obtuvo `RLS_OK` y cero eventos;
- el rol `flentio_rag_app` recibió `permission denied` al intentar modificar auditoría;
- la consulta completa del snapshot operativo se ejecutó correctamente bajo RLS;
- 32/32 pruebas backend y auditoría npm sin vulnerabilidades;
- frontend compilado y auditoría npm sin vulnerabilidades.

La revisión visual autenticada alcanzó las pestañas `Operación RAG` e `Ingesta RAG / Drive` con la identidad local real y su tenant correcto. Se comprobó Chromium a 1440, 1024 y 768 píxeles: sin errores de consola, peticiones RAG fallidas ni solapamientos. El panel mostró 3 documentos, 6 fragmentos versionados, 7 consultas, p95 de 156 ms para esta muestra mínima, cola cero y `OPERATIVO`. Capturas: `output/playwright/`.

Durante la aceptación se corrigió la consulta SQL del período y se separaron los fallos históricos de los fallos de ingesta aún sin resolver. El estado final conserva tres fallos históricos, informa cero sin resolver y no mantiene una alerta falsa.

No se eligió ni probó SIEM externo. No hay carga representativa, alertas conectadas a guardias, SLO aprobados ni almacenamiento WORM externo; F7 no está terminada para banca. Evidencia integrada: `docs/audits/RAG_FULL_ACCEPTANCE_2026-07-31.md`.
