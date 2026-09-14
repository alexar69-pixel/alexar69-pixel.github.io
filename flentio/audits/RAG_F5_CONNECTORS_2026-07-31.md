# Evidencia F5 — 31-07-2026

## Resultado

Estado `VALIDACIÓN local integral`, no `TERMINADA`. Se utilizó PostgreSQL real `pgvector/pgvector:pg16`, OAuth y Google Drive reales, sin datos bancarios ni servicios simulados.

- migraciones 001–006 aplicadas con `ON_ERROR_STOP`;
- migración 006 reaplicada correctamente;
- `claim_next_connector_sync_job` devolvió un único trabajo y elevó `attempts`;
- primer mensaje de canal: `accepted=true, duplicate=false`;
- repetición: `accepted=true, duplicate=true`;
- segundo tenant: `RLS_OK` y cero conectores visibles;
- token HMAC válido aceptado y token alterado rechazado;
- backend: 28/28 pruebas superadas;
- frontend: compilación Vite completada;
- análisis sintáctico Node superado para servicio, API, ingesta y servidor.
- autorización OAuth completada con `drive.readonly`, PKCE, estado de un solo uso, acceso offline y verificación Drive antes de custodiar la credencial;
- carpeta real `Flentio RAG Testing` sincronizada con tres Google Docs nativos marcados como sintéticos;
- el feed incremental detectó tres cambios reales y la reconciliación los dejó en versión 2;
- cursor `LISTO`, conector `OPERATIONAL`, cola cero y cero eventos pendientes;
- los fallos descubiertos durante la aceptación permanecen en auditoría y se distinguen de fallos sin resolver.

## Puertas pendientes

- Movimiento/borrado, revocación OAuth y renovación de canal en URL HTTPS pública.
- Carga, cuotas y p95/p99 con decenas de miles de documentos.
- Bóveda de red y workers separados si se adopta HA.
- Revisión independiente y credenciales/consentimiento del banco.

La evidencia integrada, incluida la limitación del corpus, está en `docs/audits/RAG_FULL_ACCEPTANCE_2026-07-31.md`.
