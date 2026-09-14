# Contrato de interoperabilidad gobernada

**Estado:** `IMPLEMENTACION_PARCIAL_EN_VALIDACION_LOCAL`.

Este documento define el contrato objetivo para interoperar con plataformas de automatización y agentes de terceros. La primera implementación incorpora evidencia estructurada a una investigación existente mediante una ruta administrativa autenticada, después de comprobar que la Skill correspondiente está validada y activa. No habilita recepción pública, órdenes externas, compensaciones ni autorización nueva. Las capacidades actuales de descubrimiento y activación siguen sujetas a la [arquitectura de Integration Skills](INTEGRATION_SKILLS_ARCHITECTURE.md) y al [Client Integration Gateway v1](../CLIENT_INTEGRATION_GATEWAY_V1.md).

## Propósito

Flentio debe poder aportar gobierno a una plataforma existente —por ejemplo, una automatización SaaS, un orquestador técnico o una plataforma interna de un banco— sin sustituirla ni recibir privilegios implícitos. El contrato conserva:

- identidad y aislamiento por tenant;
- evidencia mínima, correlacionable y sin secretos;
- aprobación humana antes de toda acción de impacto;
- trazabilidad de la decisión, ejecución y resultado;
- reversión o compensación declarada por el sistema ejecutor.

No pretende importar flujos propietarios ni ofrecer compatibilidad universal con Zapier, Make, n8n, LangChain u otro producto.

## Límites y reparto de responsabilidades

| Responsabilidad | Plataforma externa | Flentio |
|---|---|---|
| Diseñar y ejecutar la lógica propia | Mantiene su runtime, credenciales y cambios | No ejecuta código externo arbitrario |
| Emitir hechos operativos | Entrega eventos con esquema y origen verificables | Valida, minimiza y conserva referencias |
| Autorizar acciones de impacto | No asume aprobación por un callback técnico | Exige revisión humana y política vigente |
| Ejecutar una acción aprobada | Realiza una operación idempotente y reporta resultado | Emite una orden limitada y audita el expediente |
| Revertir o compensar | Declara soporte, precondiciones y resultado | Solicita sólo la reversión autorizada |

La plataforma externa sigue siendo sistema de ejecución; Flentio es el plano de gobierno y evidencia. Un `HTTP 200` no prueba que una acción haya ocurrido ni que esté autorizada.

## Prerrequisitos de incorporación

Antes de procesar eventos o solicitar acciones, cada integración debe tener:

1. proveedor, edición, tenant externo, ámbito y propietario registrados;
2. identidad de workload de mínimo privilegio desde la bóveda;
3. egress, DNS, TLS/mTLS y retención aprobados;
4. esquema versionado, límites de tamaño y política de campos permitidos;
5. prueba real de conectividad vigente y activación auditada;
6. runbook de fallo, revocación y, si aplica, compensación;
7. decisión explícita de si el flujo sólo informa, solicita aprobación o puede ejecutar una orden aprobada.

Sin estos elementos el estado es `NO_CONFIGURADO`, `NO_DISPONIBLE` o `PENDIENTE_AUTORIZACION`, según corresponda.

## Mensajes objetivo

Todos los mensajes comparten un sobre versionado. Los valores se ilustran para definir semántica; no son payloads aceptados hoy por la API.

```json
{
  "schemaVersion": "1.0",
  "messageId": "uuid",
  "correlationId": "uuid",
  "organizationId": "uuid",
  "externalTenant": "bank-es",
  "source": {"integrationId": "n8n", "instanceId": "hash"},
  "occurredAt": "2026-08-12T10:00:00Z",
  "classification": "INTERNAL",
  "payload": {}
}
```

La ruta implementada `POST /api/admin/governed-interoperability/investigations/:id/evidence` acepta `evidence.observed` como cuerpo autenticado de administración. Exige `schemaVersion: "1.0"`, UUIDs para mensaje y correlación, una Skill activa, referencia HTTPS, clasificación y evidencia estructurada. Persiste sólo los campos permitidos por la investigación operacional y conserva el resto fuera de Flentio. La ejecución de acciones responde `GOVERNED_INTEROP_ACTION_EXECUTION_NOT_IMPLEMENTED`.

`organizationId`, `externalTenant`, `source.integrationId` y `schemaVersion` se validan contra el perfil activo. Los secretos, cookies, tokens, prompts, documentos completos y payloads no permitidos se rechazan o se eliminan antes de persistir.

| Tipo | Lo emite | Uso permitido | Controles mínimos |
|---|---|---|---|
| `evidence.observed` | Externo | Incorporar un hecho o referencia | identidad, esquema, deduplicación, clasificación |
| `approval.requested` | Flentio | Presentar propuesta a revisor humano | evidencia suficiente, política y alcance |
| `approval.decided` | Flentio | Registrar aprobación o rechazo | revisor, motivo, timestamp y expediente |
| `action.requested` | Flentio | Solicitar ejecución limitada | aprobación vigente, idempotency key, TTL y precondiciones |
| `action.completed` | Externo | Informar resultado verificable | correlación, estado final, referencias y error sanitizado |
| `compensation.requested` | Flentio | Solicitar reversión autorizada | acción original, capacidad declarada y aprobación |

## Puerta de acción y rollback

Una orden `action.requested` sólo podrá emitirse cuando el adaptador futuro compruebe, en este orden:

1. perfil, validación y activación vigentes;
2. tenant, ámbito, identidad y capacidad permitida;
3. evidencia suficiente y sin contradicción bloqueante;
4. política de acción y aprobación humana no expirada;
5. idempotency key, TTL, precondiciones y mecanismo de compensación declarados.

Si cualquiera falla, no se realiza una llamada externa y se registra el motivo sin exponer datos sensibles. El rollback no es una instrucción genérica: requiere una capacidad explícita, una nueva revisión cuando la política lo exija y confirmación del sistema ejecutor.

## Observabilidad y evidencia

El futuro cuadro de mando debe mostrar por tenant y adaptación: estado, última prueba, eventos aceptados/rechazados, decisiones pendientes, órdenes emitidas, resultados, compensaciones, errores, versión de esquema y frescura. No mostrará secretos ni payloads completos. La instrumentación deberá cumplir el [estándar de cuadros de mando](../DASHBOARD_STANDARD.md).

## Criterios de aceptación para implementar el contrato

- prueba real y aislada de identidad, tenant y esquema;
- rechazo verificable de replay, tenant cruzado, esquema no permitido y orden sin aprobación;
- trazabilidad íntegra desde evidencia hasta resultado o compensación;
- límites de tamaño, cuota y timeout aplicados;
- desactivación que detenga nuevos mensajes sin borrar auditoría;
- pruebas de contrato, estados vacíos/error y visualización administrativa.

## Decisión de adopción

La primera integración no debe elegirse por volumen de conectores, sino por un proceso crítico y una plataforma ya autorizada por un cliente. Hasta completar un piloto con evidencias reales, la propuesta de interoperabilidad permanece `NO_VALIDADA`.
