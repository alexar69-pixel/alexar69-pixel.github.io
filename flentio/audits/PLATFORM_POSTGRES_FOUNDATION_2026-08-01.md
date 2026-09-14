# Evidencia de fundación PostgreSQL multinodo — 01-08-2026

## Dictamen

Estado `EN CURSO — FUNDACIÓN VALIDADA`. PostgreSQL compartido está preparado para la migración gradual, pero SQLite sigue siendo la fuente activa de la aplicación. No se declara multinodo operativo ni HA.

## Pruebas reales

- PostgreSQL `16.14` respondió con el esquema `flentio_platform` operativo.
- Migración protegida por advisory lock y checksum aplicada correctamente.
- Importación transaccional: origen y destino coincidieron en 3 usuarios, 70 workflows, 9 ejecuciones, 5 credenciales, 1 estado OAuth, 0 ajustes y 1 versión.
- La importación se aplicó una segunda vez y conservó exactamente los mismos recuentos, verificando su idempotencia.
- RLS: organización A vio sólo A; organización B vio sólo B; sin contexto se obtuvieron cero usuarios.
- Dos conexiones reales reclamaron dos trabajos diferentes mediante `SKIP LOCKED`.
- El rol `flentio_platform_app` recibió denegación al intentar crear una tabla.
- La validación eliminó sus organizaciones, usuarios, workflows y trabajos sintéticos al terminar.
- SQLite no fue modificado ni eliminado por el importador.

## Cambios contra éxitos simulados preexistentes

- `/api/health` consulta SQLite, PostgreSQL RAG y PostgreSQL plataforma; ya no responde `database: Connected` sin comprobarlo.
- Los popups OpenAI OAuth y SSO prefabricados devuelven `NO_CONFIGURADO` hasta disponer de integraciones reales.
- La prueba genérica de credenciales deja de validar únicamente el formato y devolver éxito; responde `NO_CONFIGURADO` hasta instalar verificadores reales por proveedor.

## Pendiente

La migración de repositorios de auth, credenciales, configuración, workflows, ejecuciones, cron y workers es el siguiente bloque. También quedan auditoría compartida, KMS/secret manager, PgBouncer externo y configuración productiva de réplicas/failover.
