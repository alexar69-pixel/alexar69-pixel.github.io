# Arquitectura de Entornos (DEV / PREPROD / PROD) y Versionado Inmutable — Flentio Platform

Este documento define la arquitectura para la gestión del ciclo de vida de entornos y control de versiones inmutables para flujos y agentes especializados en **Flentio Platform**.

---

## 1. Ciclo de Vida de Entornos

```mermaid
graph LR
    DEV["🟢 Entorno DEV (Desarrollo)<br/>v1.0.0-draft (Editable)"] -->|Promoción con Hash SHA-256| PREPROD["🟡 Entorno PREPROD (Preproducción)<br/>v1.0.0-rc1 (Inmutable)"]
    PREPROD -->|Puerta de Homologación & Revisión| PROD["🔴 Entorno PROD (Producción)<br/>v1.0.0 (Congelado)"]
```

---

## 2. Reglas Invariables de Inmutabilidad
1. **Edición Restringida**: Ningún flujo o agente en `PREPROD` o `PROD` puede editarse directamente. Toda modificación requiere clonar un borrador hacia `DEV`.
2. **Hash de Integridad SHA-256**: Cada versión promovida calcula un hash SHA-256 de la definición completa. Si el contenido cambia, el hash cambiará e invalidará la promoción.
3. **Auditoría Append-Only**: Cada cambio de entorno emite un registro inmutable en `flentio_platform.audit_logs`.
