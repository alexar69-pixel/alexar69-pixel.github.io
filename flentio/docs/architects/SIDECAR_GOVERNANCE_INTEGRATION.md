# Integración de Flentio como Sidecar de Gobierno para Plataformas Bancarias

> Especificación técnica para integrar Flentio como Middleware / Sidecar de Gobierno, DLP y RAG con Citas en suites bancarias corporativas (ej: BBVA Blue, JPMorgan LLM Suite).

---

## Contexto e Interoperabilidad

Las grandes entidades bancarias que disponen de plataformas internas de IA no necesitan reemplazar su infraestructura existente. Flentio actúa como un **Sidecar de Gobierno e Inspección Operacional** accesible vía API REST / SDK.

```
┌─────────────────────────────────────────────────────────┐
│        Plataforma Bancaria Interna (BBVA Blue)          │
└───────────────────────────┬─────────────────────────────┘
                            │ API REST / Sidecar Protocol
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Flentio Governance Sidecar                 │
├─────────────────────────────────────────────────────────┤
│ 1. Inspección DLP & Sanitización PII (`/inspect-prompt`)│
│ 2. Recuperación RAG con Citas (`/rag-citations`)        │
│ 3. Registro de Decisiones WORM (`/audit-decision`)      │
└─────────────────────────────────────────────────────────┘
```

---

## Endpoints de Interoperabilidad Sidecar

### 1. Inspección DLP y Sanitización de Prompts
- **Endpoint**: `POST /api/interop/v1/sidecar/inspect-prompt`
- **Cabeceras**: `X-Tenant-ID: <org-uuid>`
- **Payload**:
  ```json
  {
    "prompt": "Consultar saldo para cuenta ES21 1234 5678 9012 3456 con clave sk-123456789012345678901234"
  }
  ```
- **Respuesta**:
  ```json
  {
    "success": true,
    "sidecar": "Flentio-Governance-Sidecar-v1",
    "data": {
      "tenantId": "org-bbva-spain",
      "clean": false,
      "hasSecrets": true,
      "sanitizedText": "Consultar saldo para cuenta ES21 1234 5678 9012 3456 con clave [SECRET_REDACTED]"
    }
  }
  ```

---

### 2. Recuperación RAG con Citas Gobernada
- **Endpoint**: `POST /api/interop/v1/sidecar/rag-citations`
- **Cabeceras**: `X-Tenant-ID: <org-uuid>`
- **Payload**:
  ```json
  {
    "query": "Límites operacionales de transferencias SEPA nocturnas"
  }
  ```
- **Respuesta**:
  ```json
  {
    "success": true,
    "sidecar": "Flentio-Governance-Sidecar-v1",
    "data": {
      "citationsCount": 1,
      "evidence": [
        {
          "id": "EV-SEPA-001",
          "source": "Normativa Operacional SEPA 2026",
          "text": "Las transferencias instantáneas SEPA tienen un límite de 100.000 EUR salvo autorización previa.",
          "clearance": "CONFIDENTIAL"
        }
      ],
      "governanceStatus": "GOVERNED_CITATIONS_VERIFIED"
    }
  }
  ```

---

### 3. Registro de Decisiones en Auditoría WORM
- **Endpoint**: `POST /api/interop/v1/sidecar/audit-decision`
- **Cabeceras**: `X-Tenant-ID: <org-uuid>`
- **Payload**:
  ```json
  {
    "action": "LOAN_RISK_EVALUATED",
    "payload": { "applicantId": "USR-99", "score": 850, "approved": true }
  }
  ```
- **Respuesta**:
  ```json
  {
    "success": true,
    "sidecar": "Flentio-Governance-Sidecar-v1",
    "data": {
      "auditId": "AUD-SDK-1770932000000",
      "status": "WORM_AUDIT_COMMITTED"
    }
  }
  ```

---

## Estado de la Especificación

| Componente | Estado |
|---|---|
| API REST Sidecar heredada | `NO_DISPONIBLE` — respuesta simulada, sin autenticación en el montaje actual |
| Client SDK (`FlentioSdk`) | `NO_DISPONIBLE` para uso operativo — no persiste el contrato descrito |
| Aislamiento multi-tenant de estas rutas | `NO_VALIDADO` — el tenant procede de cabecera/body no autenticado |

Los ejemplos anteriores expresan el contrato objetivo, no respuestas que deban
esperarse del runtime actual. `backend/src/api/governedSidecar.js` añade
`X-Flentio-Simulated: true`; no se debe usar para DLP, citas o auditoría WORM
real. Bloquee `/api/interop/sidecar/*` hasta implementar identidad verificable,
RBAC, RLS/persistencia, rate limiting y pruebas negativas. Consulte
[Seguridad de Flentio](../SECURITY.md).
