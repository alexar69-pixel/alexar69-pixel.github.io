# RAG F5: sincronización incremental y conectores

## Qué hace y para qué sirve

F5 mantiene actualizado el conocimiento RAG sin volver a descargar todo el repositorio. Un cambio remoto se convierte en un evento durable e idempotente, pasa por la misma cuarentena, ClamAV, procedencia y gobierno documental que una carga manual y sólo después puede llegar al índice.

El flujo es: notificación o reconciliación → feed de cambios → evento `upsert`, `tombstone` o `ignored` → descarga real → seguridad de ingesta → versión RAG. El cursor sólo avanza cuando los eventos de la página han terminado. Si un archivo se elimina o sale de la carpeta, su documento se archiva; no se destruye el original.

## Garantías implementadas

- estado durable en PostgreSQL y RLS forzada por tenant;
- un solo sync activo por conector y reclamación `SKIP LOCKED`;
- claves idempotentes por cambio y evaluación única por evento;
- paginación de 1.000 elementos y backpressure configurable;
- reintentos exponenciales, recuperación de leases y error observable;
- reconciliación periódica además del webhook;
- deduplicación de mensajes por canal/número;
- token HMAC, `resourceId`, expiración y UUID de canal verificados;
- renovación con solapamiento: el canal anterior sigue aceptando avisos hasta instalar el nuevo;
- credenciales resueltas por propietario y secretos ausentes de PostgreSQL;
- panel no-code para configurar, sincronizar, reconciliar, activar avisos y deshabilitar.

Google envía una notificación sin detalles del cambio; Flentio consulta después `changes.list`. El token del canal es generado por Flentio y devuelto por Google, por lo que no debe describirse como una firma del cuerpo por Google.

## Configuración

| Variable | Uso | Valor de desarrollo |
|---|---|---|
| `RAG_CONNECTOR_POLL_MS` | frecuencia del scheduler | `1000` |
| `RAG_CONNECTOR_MAX_PENDING_EVENTS` | backpressure por conector | `5000` |
| `RAG_CONNECTOR_RECONCILE_HOURS` | reparación periódica | `24` |
| `RAG_PUBLIC_BASE_URL` | origen HTTPS público del webhook | sin valor por defecto operativo |
| `RAG_CONNECTOR_WEBHOOK_SECRET` | HMAC, mínimo 32 caracteres | secreto externo a Git |
| `GOOGLE_DRIVE_OAUTH_CLIENT_ID` | identidad OAuth de Flentio registrada en Google Cloud | obligatorio |
| `GOOGLE_DRIVE_OAUTH_CLIENT_SECRET` | secreto del cliente web; debe residir fuera de Git | obligatorio |
| `GOOGLE_DRIVE_OAUTH_REDIRECT_URI` | callback registrado literalmente en Google | `http://localhost:3000/oauth/google-drive/callback` sólo en desarrollo |

La bóveda ofrece **Google Drive (OAuth, solo lectura)**. `POST /api/credentials/google-drive/oauth/start` genera una petición real con el alcance `drive.readonly`, acceso offline, estado aleatorio de un solo uso, caducidad de diez minutos y PKCE S256. Google retorna a `/oauth/google-drive/callback`; el backend intercambia el código, verifica `drive.about`, exige `refresh_token` y cifra la credencial. El navegador sólo recibe éxito o error, nunca tokens. La revocación produce `GOOGLE_DRIVE_OAUTH_REVOKED`; nunca se sustituye por un token simulado.

Antes de pulsar **Conectar Google Drive**, el propietario de Flentio debe crear un cliente OAuth de tipo *Web application* en un proyecto Google Cloud, habilitar Drive API y registrar exactamente la URI de retorno. No es posible generar una autorización válida sin esa identidad de aplicación. Guía oficial: https://developers.google.com/identity/protocols/oauth2/web-server

## API y operación

- `GET /api/rag/connectors`: estado, frescura, cursor y errores.
- `GET /api/rag/connector-providers`: adaptadores realmente instalados.
- `POST /api/rag/connectors/google-drive`: registra y encola la carga inicial.
- `POST /api/rag/connectors/:id/sync`: procesa cambios desde el cursor.
- `POST /api/rag/connectors/:id/reconcile`: compara toda la carpeta y genera tombstones.
- `POST /api/rag/connectors/:id/webhook`: crea un canal real; exige cursor, OAuth y HTTPS.
- `POST /api/rag/connectors/:id/disable`: detiene nueva actividad sin borrar trazabilidad.
- `POST /api/rag/connectors/google-drive/notifications`: receptor público autenticado por canal.

Ante `unavailable`, revisar `last_error_code`, OAuth, alcance `Files.Read`, conectividad y cuota. No reiniciar eliminando el cursor. Si se pierde un aviso, ejecutar `reconcile`. Si hay backpressure, corregir el consumidor o el proveedor antes de elevar el límite.

## Proveedores posibles

| Proveedor | Ventajas | Inconvenientes / trabajo pendiente |
|---|---|---|
| Google Drive (integrado) | feed de cambios, exportación de formatos Google, canales push | canal máximo de una semana, renovación obligatoria, aviso sin detalle, OAuth y cuotas |
| Microsoft SharePoint/OneDrive (candidato prioritario) | Microsoft Graph `deltaLink`, tombstone `deleted`, encaje habitual en banca/M365 | permisos Graph y consentimiento corporativo; suscripciones y delta tienen semántica propia; aún no integrado |
| Amazon S3 (candidato) | eventos a SQS/SNS/Lambda/EventBridge, versionado, gran escala | entrega al menos una vez y orden parcial; necesita `sequencer`, IAM y reconciliación de inventario; aún no integrado |
| Confluence Cloud/Data Center (candidato) | API de contenido y webhooks de páginas | diferencias Cloud/Data Center, límites y modelo Forge en Cloud; representación rica requiere extractor específico; aún no integrado |
| Azure Blob, Box o repositorio SFTP | útiles según residencia y legado del cliente | contrato de cambios, identidad, borrado y reconciliación deben demostrarse individualmente |

Un adaptador nuevo debe implementar el puerto, usar IDs estables, soportar reanudación, producir tombstones, respetar backpressure y pasar pruebas reales de creación, modificación, movimiento, borrado, duplicado, pérdida de aviso y revocación de credencial.

## Estado y límites

Estado: `VALIDACIÓN local`. PostgreSQL, RLS, reclamación, deduplicación, HMAC, migración idempotente, pruebas backend y compilación frontend están validados. Falta la prueba de aceptación contra una carpeta Google real porque no se proporcionaron OAuth, carpeta y URL HTTPS. No se ha medido carga representativa de decenas de miles ni se declara HA.
