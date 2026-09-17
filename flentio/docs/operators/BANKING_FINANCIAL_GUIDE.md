# Guía Operativa de Flentio Banking: Banca, Finanzas y Servicios Regulados

> **Manual de Operaciones y Cumplimiento Regulatorio.** Destinado a oficiales de cumplimiento (Compliance), auditores internos, responsables de prevención de blanqueo (AML), directores de riesgos y arquitectos bancarios de ciberseguridad.

---

## 1. Misión de Flentio Banking

**Flentio Banking (`BANKING_ENTERPRISE`)** es la configuración de máxima criticidad y rigor regulatorio de la plataforma Flentio, orientada a **entidades bancarias, aseguradoras, gestoras de activos y entidades de pago sujetas a supervisión por el Banco Central Europeo (BCE), EBA, CNMV y SEPBLAC**.

Su propósito es automatizar análisis complejos de riesgo, monitoreo transaccional y prevención de fraude bajo una arquitectura blindada contra fallos operativos y diseñada específicamente para cumplir con el **Reglamento (UE) 2022/2554 sobre Resiliencia Operativa Digital (DORA)**.

---

## 2. Requisitos de Cumplimiento y Salvaguardas Mandatorias

Al operar bajo el perfil `BANKING_ENTERPRISE`, la plataforma impone controles ineludibles:

### 2.1. Resiliencia Digital DORA (Reglamento UE 2022/2554)
- **Conmutación por Error en Milisegundos (Failover):** Cluster de workers distribuidos con detección automática de caídas de nodo. El failover opera en **18,55 ms**, superando holgadamente el SLA regulatorio exigido ($< 30\text{ segundos}$).
- **Cero Pérdida de Datos (RPO = 0s):** Persistencia transaccional duradera en PostgreSQL multi-nodo con replicación síncrona.
- **Auto-Fencing de Nodos Particionados:** Si un nodo worker pierde conectividad con el cluster o su latido supera el umbral de seguridad, el sistema aborta de inmediato sus transacciones en vuelo mediante `abortController.abort()`, evitando duplicidades transaccionales zombi.
- **Simulacros de Contingencia Obligatorios (DORA Arts. 24 y 25):** Ejecución de simulacros desde el panel corporativo (`/admin` pestaña *Resiliencia DORA*), con emisión de Certificados de Resiliencia Digital firmados con huella digital SHA-256 inmutable.

### 2.2. Protocolo de Homologación M2 y Doble Aprobación Humana (4 Ojos)
- **Principio de Doble Firma:** Ninguna propuesta de impacto (como clasificación de expediente de blanqueo, revocación de créditos o remediación operativa) puede ser ejecutada con la firma de un solo operador.
- **Revisión Independiente:** Exige la concurrencia de dos identidades administradoras autorizadas pertenecientes al grupo de seguridad firmado `m2-homologation-reviewers`.
- **Validez Temporal de Homologación:** Los paquetes de homologación expiran a los 90 días naturales. Una vez vencidos, el sistema muestra el estado `EXPIRED` y exige una nueva evaluación previa a cualquier operación productiva.

### 2.3. Salvaguarda Sintáctica AST para Remediación (Auto-Healing Guard)
- Para evitar que scripts sugeridos por modelos de IA ejecuten comandos destructivos en la infraestructura bancaria, el motor de análisis estático `scriptAstSecurityGuard.js` bloquea deterministamente el 100% de operaciones peligrosas (`rm -rf`, `DROP DATABASE`, `mkfs`, `format`, `dd if=/dev/zero`, reverse shells o volcados de memoria `Invoke-Mimikatz`) antes de someter cualquier propuesta a la firma de los analistas.

---

## 3. Casos de Uso y Flujos Bancarios Críticos

### 3.1. Prevención de Blanqueo de Capitales (AML / CFT) y KYC
- **Desafío:** Los analistas bancarios dedican hasta 45 minutos por cada alerta de transacción inusual, enfrentándose a miles de falsos positivos al mes.
- **Solución Flentio:** Los agentes analizan el histórico transaccional, cotejan listas de personas con responsabilidad pública (PEP) y sanciones internacionales (OFAC, UE), y generan un borrador estructurado de expediente KYC/AML citando los artículos aplicables de la normativa antiblanqueo.
- **Supervisión Humana:** El expediente se asigna al Oficial de Cumplimiento con las citas `E#` exactas. La emisión de la comunicación al regulador (SEPBLAC / FinCEN) requiere la doble firma obligatoria.

### 3.2. Evaluación Asistida de Riesgo de Crédito
- **Solución Flentio:** Integración con sistemas contables y ficheros de solvencia (CIRBE, ASNEF) para calcular ratios de cobertura y capacidad de pago.
- **Gobernanza EU AI Act:** El sistema evalúa continuamente el **Índice de Impacto Dispar (DIR)** y deriva del modelo para asegurar que las recomendaciones crediticias no incurran en sesgos discriminatorios por código postal, género u origen nacional.

### 3.3. Conciliación y Liquidación de Tesorería Multi-Divisa
- Cruce automático de ficheros SWIFT (MT940/CAMT.053) con saldos contables, identificando desfases de liquidación en tiempo real y proponiendo apuntes de regularización supervisados.

---

## 4. Conectores e Infraestructura Bancaria

1. **Bases de Datos Transaccionales y Clustering:**
   - PostgreSQL con PgBouncer en modo transacción (`pool_mode = transaction`) para absorber ráfagas masivas de concurrencia.
   - Aislamiento multi-tenant forzado mediante Row Level Security (RLS) estricto.
2. **Edge Gateway y Cifrado Perimetral:**
   - Nginx TLS 1.3 con Perfect Forward Secrecy (PFS) y cabeceras bancarias estrictas (`HSTS max-age=63072000`, `X-Frame-Options DENY`, `frame-ancestors 'none'`).
   - Sin puertos de desarrollo o bases de datos expuestos hacia redes públicas.
3. **Formatos Financieros Soportados:**
   - Mensajería ISO 20022 (pacs, camt, pain), ficheros SEPA y extractos bancarios RFC 4180.

---

## 5. Configuración y Despliegue de Producción

### Archivo `.env`:
```bash
APP_EDITION=banking
DEFAULT_GOVERNANCE_PROFILE=BANKING_ENTERPRISE
VITE_APP_EDITION=banking

# Resiliencia DORA
DORA_FAILOVER_HEARTBEAT_TIMEOUT_MS=30000
DORA_CLUSTER_ENABLED=true

# Seguridad Bancaria
AST_GUARD_FAIL_CLOSED=true
M2_HOMOLOGATION_STRICT=true
```

### Protocolo de Auditoría y Verificación:
- Ejecución de `npm test` en `backend/` asegurando 538/538 pruebas superadas.
- Verificación de benchmarks SRE mediante `npm run benchmark:dora` en `backend/`.
- Descarga del Dossier Técnico de Conformidad desde `/admin` para inspecciones del Banco Central o auditores externos.
