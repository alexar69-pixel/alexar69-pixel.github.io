# Contrato Client Integration Gateway v1

## Propósito

Este contrato permite conectar productos cuya API depende de proveedor, edición
o política del cliente sin incorporar una simulación ni seleccionar fabricante
desde Flentio. Se usa para SIEM, BMC HelixGPT, KMS/HSM, CyberArk PAM/Conjur,
Vault/PAM genérico y EDR/XDR. El gateway debe ser un servicio real, desplegado y
homologado por el cliente o por su integrador.

El runtime sólo valida identidad, tenant, ámbito, recursos y capacidades. No
consulta alertas, secretos, claves ni conocimiento durante la prueba. Un HTTP
200 sin el contrato completo se rechaza.

## Petición de descubrimiento

```http
GET /.well-known/flentio-integration/v1?integrationId=siem
Authorization: Bearer <credencial-resuelta-desde-boveda>
Accept: application/json
X-Flentio-Challenge: <uuid-aleatorio>
```

El endpoint base, la credencial, el tenant externo, el ámbito y los bindings
específicos se configuran desde Administración. El secreto nunca forma parte del
perfil ni de la auditoría.

## Respuesta obligatoria

```json
{
  "schemaVersion": "1.0",
  "integrationId": "siem",
  "provider": "proveedor-homologado",
  "tenant": "bank-es",
  "scope": "prod/app-a",
  "principal": "svc-flentio",
  "readOnly": true,
  "capabilities": ["events.query", "audit.delivery"],
  "bindings": {},
  "challenge": "mismo-uuid-de-la-peticion",
  "issuedAt": "2026-08-02T10:00:00.000Z"
}
```

La respuesta no puede superar 64 KiB. `issuedAt` debe estar dentro de cinco
minutos, el challenge debe coincidir y tenant/ámbito deben ser idénticos al
perfil. Flentio conserva un hash SHA-256 del principal, no su valor.

## Capacidades por Skill

| Skill | Capacidades mínimas | Bindings exactos |
|---|---|---|
| SIEM | `events.query`, `audit.delivery` | ninguno |
| BMC HelixGPT | `knowledge.search`, `citations.return` | ninguno |
| KMS/HSM | `keys.metadata.read`, `crypto.capabilities.describe` | `keyId` |
| CyberArk | `accounts.metadata.read`, `secrets.metadata.read` | `account`, `secretPrefix` |
| Vault/PAM genérico | `secrets.metadata.read` | ninguno |
| EDR/XDR | `alerts.read`, `devices.metadata.read` | ninguno |

Estas capacidades describen el contrato futuro autorizado; la prueba siempre
exige `readOnly: true` y no ejecuta `audit.delivery`, criptografía, lectura de
secretos ni recuperación RAG.

## Autorización y estados

Todas las Skills se instalan con carga diferida. KMS/HSM y almacenamiento de
objetos conservan `PENDIENTE_AUTORIZACION`: el backend rechaza guardar, probar o
activar hasta que un administrador autorice en el frontend un proveedor concreto.
La decisión queda auditada por tenant. Revocarla elimina perfil, validación y
activación y descarga el runtime.

Sin endpoint, credencial, gateway o respuesta válida, el estado permanece
`NO_CONFIGURADO` o `NO_DISPONIBLE`; nunca se fabrica una respuesta operativa.

## Seguridad y producción

- HTTPS y controles corporativos de DNS/egress son obligatorios en producción.
- La identidad debe aplicar mínimo privilegio y segregación por tenant/ámbito.
- El gateway debe impedir SSRF, registrar accesos sin secretos y limitar cuota.
- La prueba no sustituye homologación, residencia, DPA, HA/DR, pentest o SLO.
- La operación funcional posterior deberá versionar endpoints y esquemas propios
  conservando las mismas capacidades y puertas de autorización.

## Rollback

Revocar la autorización o desactivar la Skill impide nuevas cargas y elimina el
runtime de caché. Retirar el perfil conserva la autorización de proveedor; revocar
la autorización elimina ambas cosas para evitar reutilización accidental.
