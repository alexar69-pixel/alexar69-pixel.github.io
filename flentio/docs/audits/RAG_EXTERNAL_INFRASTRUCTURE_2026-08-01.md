# Evidencia de compatibilidad con infraestructura RAG externa — 01-08-2026

## Alcance

Se documentó la entrega productiva y se amplió el software para originales en
AWS S3/S3 compatible y envelope encryption con AWS KMS. No se utilizaron datos
de clientes, no se fabricaron métricas y no se realizó ninguna llamada a AWS.

## Cambios verificables

- `backend/src/rag/objectStore.js`: adaptadores `minio`, `aws-s3` y
  `s3-compatible`; credenciales estándar del SDK; autoaprovisionamiento
  deshabilitable; cifrado estático v1 y AWS KMS envelope v2.
- `backend/src/rag/config.js`: validación diferenciada de endpoint,
  credenciales y key provider.
- `backend/src/rag/migrations/009_external_object_storage.sql`: constraint de
  proveedores implementados y documentación de KeyId.
- `backend/.env.example`: parámetros no secretos, estados y límites.
- documentación operativa, readiness, roadmap, memoria, manual y plantillas de
  cliente actualizadas.

## Ejecuciones reales

| Comprobación | Resultado |
| --- | --- |
| `npm install @aws-sdk/client-kms@^3.1100.0` | dependencia instalada; auditoría npm: 0 vulnerabilidades |
| `npm run migrate:rag` | `OPERATIVO`, pgvector 0.8.6, migración aplicada |
| `npm test` | 56 pruebas, 56 superadas, 0 fallos/omitidas |

Las pruebas criptográficas verificaron restauración byte a byte y rechazo de
ciphertext alterado para el formato estático existente. No se creó un KMS falso
ni se interpretó una prueba unitaria como validación AWS. La validación AWS
requiere un bucket real con Object Lock, una clave real, identidad de workload y
la lista de aceptación del cliente.

## Riesgos y rollback

- Azure/GCS y KMS/HSM no AWS permanecen `NO_IMPLEMENTADO`.
- El proveedor S3 compatible debe demostrar `VersionId`, Object Lock, legal hold
  y retención; declarar compatibilidad de API no basta.
- Para revertir código se conserva el formato v1 y los objetos existentes. No
  debe revertirse la constraint 009 si ya existen filas `aws-s3` o
  `s3-compatible`.
- Para retirar AWS KMS, descifrar y reingestar bajo una clave autorizada antes
  de deshabilitar las claves históricas. Object Lock no evita pérdida por
  destrucción de claves.

## Dictamen

`VALIDACIÓN_LOCAL_DE_COMPATIBILIDAD`. El software y la documentación están
preparados para configuración AWS/S3, pero la capacidad externa permanece
`NO_CONFIGURADO` hasta disponer de infraestructura y evidencia del cliente.
