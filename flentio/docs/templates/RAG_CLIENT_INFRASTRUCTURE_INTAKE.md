# Plantilla de entrada de infraestructura RAG del cliente

**Estado:** `PLANTILLA_SIN_DATOS`. Completar con identificadores y referencias;
no incluir contraseñas, tokens, claves privadas, secretos OAuth ni material KMS.

## Control del documento

| Campo | Valor |
| --- | --- |
| Cliente / deployment ID | PENDIENTE_CLIENTE |
| Entorno | PENDIENTE_CLIENTE |
| Clasificación máxima | PENDIENTE_CLIENTE |
| Propietario técnico | PENDIENTE_CLIENTE |
| Propietario de datos | PENDIENTE_CLIENTE |
| Fecha y versión | PENDIENTE_CLIENTE |
| Enlace al registro de decisiones | PENDIENTE_CLIENTE |

## Arquitectura y residencia

- Regiones primaria/secundaria: `PENDIENTE_CLIENTE`
- Países permitidos/prohibidos para datos, backups, logs y soporte:
  `PENDIENTE_CLIENTE`
- Modelo de tenancy y aislamiento: `PENDIENTE_CLIENTE`
- Diagrama de red aprobado: `PENDIENTE_CLIENTE`
- Volumen inicial, crecimiento y tamaño máximo por documento:
  `PENDIENTE_CLIENTE`

## Decisiones de proveedor

| ID | Componente | Proveedor/servicio | Región/edición | Responsable | Estado/aprobación |
| --- | --- | --- | --- | --- | --- |
| EXT-DB-001 | PostgreSQL/pgvector | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| EXT-OBJ-001 | Objetos/WORM | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| EXT-KMS-001 | KMS/HSM/secret manager | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| EXT-IDP-001 | IdP | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| EXT-SIEM-001 | SIEM/WORM | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| EXT-OBS-001 | OTLP/APM | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| EXT-LLM-001 | Embeddings/reranker/generación | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| EXT-AV-001 | Antimalware | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |

## Red, DNS y TLS

- FQDN público/privado y propietarios: `PENDIENTE_CLIENTE`
- Ingress/WAF/API gateway: `PENDIENTE_CLIENTE`
- Autoridad certificadora y referencia del certificado: `PENDIENTE_CLIENTE`
- Proxy de salida, DNS y allowlist HTTPS: `PENDIENTE_CLIENTE`
- CIDR/segmentos para aplicación, datos y administración:
  `PENDIENTE_CLIENTE`
- Requisitos mTLS/private endpoints/service mesh: `PENDIENTE_CLIENTE`

## Datos, cifrado y retención

- Endpoint y base PostgreSQL (sin credenciales): `PENDIENTE_CLIENTE`
- Referencias de roles runtime/migración/backup: `PENDIENTE_CLIENTE`
- Bucket/contenedor y endpoint (sin credenciales): `PENDIENTE_CLIENTE`
- Referencia de clave, versión y alias KMS: `PENDIENTE_CLIENTE`
- Custodios, doble control y calendario de rotación: `PENDIENTE_CLIENTE`
- Retención por clasificación y política de legal hold:
  `PENDIENTE_CLIENTE`
- Residencia y procedimiento de borrado/cripto-borrado:
  `PENDIENTE_CLIENTE`

## Identidad y autorizaciones

- Issuer/metadata del IdP: `PENDIENTE_CLIENTE`
- Client ID no secreto: `PENDIENTE_CLIENTE`
- Claims de tenant, usuario, grupos y clasificación: `PENDIENTE_CLIENTE`
- Grupos de administradores, aprobadores de seguridad y records managers:
  `PENDIENTE_CLIENTE`
- MFA, acceso condicional, altas/bajas y cuentas de emergencia:
  `PENDIENTE_CLIENTE`

## Modelos y conectores

- Modelos exactos, versiones y dimensiones: `PENDIENTE_CLIENTE`
- Política de residencia, entrenamiento con datos y retención del proveedor:
  `PENDIENTE_CLIENTE`
- Límites de cuota, timeout, reintentos y presupuesto: `PENDIENTE_CLIENTE`
- Fuentes autorizadas y propietarios: `PENDIENTE_CLIENTE`
- Aplicaciones OAuth, scopes y redirect URI (sin secretos):
  `PENDIENTE_CLIENTE`
- Webhook HTTPS, proxy y reconciliación: `PENDIENTE_CLIENTE`

## Operación y continuidad

- SLO de disponibilidad/latencia/frescura: `PENDIENTE_CLIENTE`
- RPO/RTO aprobados por BIA: `PENDIENTE_CLIENTE`
- Backup/PITR, repositorio y calendario de restauración:
  `PENDIENTE_CLIENTE`
- Guardias, escalados y ventanas de mantenimiento: `PENDIENTE_CLIENTE`
- SIEM/OTLP endpoints y referencias de credenciales: `PENDIENTE_CLIENTE`
- Retención de auditoría y acuse de recepción: `PENDIENTE_CLIENTE`
- Revisión independiente y responsables de aceptación:
  `PENDIENTE_CLIENTE`

## Evidencias requeridas

Enlazar tickets, decisiones, salidas de pruebas, dashboards y actas. No marcar
`VALIDADO` sin fecha, responsable y resultado reproducible.

| Control | Evidencia | Fecha | Responsable | Resultado |
| --- | --- | --- | --- | --- |
| Aprovisionamiento | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Seguridad/IAM | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Restauración | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Auditoría/SIEM | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Rollback | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |

