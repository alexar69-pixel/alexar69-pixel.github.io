# Evidencia PostgreSQL de identidad y secretos — 01-08-2026

## Dictamen

Estado `VALIDACIÓN local — CORTE PARCIAL ACTIVO`. Autenticación, ajustes, credenciales y estado OAuth utilizan PostgreSQL en el entorno local mediante `PLATFORM_IDENTITY_DATASTORE=postgres`. Workflows, ejecuciones y scheduler continúan en SQLite, por lo que Flentio todavía no es multinodo operativo.

## Evidencia real

- Migración `002_identity_secrets.sql` aplicada con checksum y advisory lock.
- Registro real creó organización y usuario atómicamente en PostgreSQL.
- Login verificó bcrypt y emitió un JWT con la organización correcta.
- Dos organizaciones guardaron la misma clave de ajuste con valores distintos y RLS devolvió únicamente el valor propio.
- Una credencial sólo fue visible y recuperable por su propietario y organización; el segundo tenant obtuvo cero resultados.
- Un estado OAuth se consumió una vez; el segundo intento devolvió cero filas.
- Validación HTTP en un backend real: registro 201, login/JWT, escritura/lectura de ajustes, alta/listado/borrado de credencial e inicio OAuth Drive persistido.
- `/oauth/openai` y la prueba genérica de credenciales devolvieron `NO_CONFIGURADO`, no éxitos prefabricados.
- Tras el corte parcial, el backend principal informó `coreStore=sqlite`, `identityStore=postgres` y `platformPostgres=OPERATIVO`.
- El administrador local recuperó desde PostgreSQL tres registros de credencial existentes. Esto acredita la migración y lectura de metadatos, no la validez externa de cada proveedor.
- La credencial OAuth Drive histórica cifrada con CBC se descifró y parseó sin exponer sus valores; confirma compatibilidad de lectura durante la transición.
- Regresión final: 34/34 pruebas backend superadas y `npm audit --omit=dev` sin vulnerabilidades.

Todos los usuarios, ajustes, credenciales y estados OAuth creados por las validaciones se eliminaron al finalizar.

## Bóveda

Las credenciales nuevas se cifran mediante AES-256-GCM con IV aleatorio y tag de autenticación. La lectura CBC histórica permanece temporalmente para poder abrir los secretos ya importados; las nuevas escrituras nunca producen CBC. En producción con identidad PostgreSQL, `ENCRYPTION_KEY` es obligatoria y debe proceder de un secret manager compartido. El fichero de clave local sólo está permitido durante desarrollo y por ello `multinodeReady=false` en health.

## Límites

- La clave de desarrollo sigue en un fichero local; no se declara bóveda multinodo hasta configurar KMS/secret manager.
- Los recorridos de workflows, ejecuciones, webhooks y cron continúan en SQLite.
- Los workers sin organización/propietario fallan al resolver una credencial en PostgreSQL; la propagación completa se cerrará con la fase de orquestación.
- No se ha repetido el consentimiento externo de Google: se validó la persistencia del inicio OAuth y se conserva la autorización real completada en la fase RAG.
