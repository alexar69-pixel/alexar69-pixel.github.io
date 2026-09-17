# Matriz de Entornos Empresariales: Corporativo Neutro, Medical y Bancario

> **Documento de Arquitectura y Gobierno Corporativo.** Define las especificaciones técnicas, operativas y de cumplimiento para los tres entornos empresariales soportados por la plataforma Flentio.

---

## 1. Visión y Alcance Multi-Sectorial

Flentio ha evolucionado de su diseño inicial de alta criticidad para convertirse en una plataforma de orquestación no-code e inteligencia artificial gobernada capaz de adaptarse formalmente a **tres entornos empresariales diferenciados**:

```
+---------------------------------------------------------------------------------------+
|                                    FLENTIO PLATFORM                                   |
|               Motor de Orquestación No-Code · Gobernanza EU AI Act · RLS              |
+--------------------------+----------------------------+-------------------------------+
|   🏢 ENTORNO CORPORATIVO |   🏥 ENTORNO MEDICAL       |   🏦 ENTORNO BANCARIO         |
|         NEUTRO           |     Y CIENCIAS SALUD       |      Y FINANCIERO             |
|                          |                            |                               |
| · Perfil:                | · Perfil:                  | · Perfil:                     |
|   CORPORATE_NEUTRAL      |   HEALTHCARE_CLINICAL      |   BANKING_ENTERPRISE          |
| · Ámbito: Cross-Industry | · Ámbito: Salud & Farma    | · Ámbito: Banca, Seguros      |
| · Enfoque: Eficiencia,   | · Enfoque: Privacidad PHI, | · Enfoque: Resiliencia DORA,  |
|   RRHH, Compras, TI,     |   Ensayos Clínicos,        |   AML/CFT, Doble Aprobación   |
|   Legal, Operaciones     |   FDA 21 CFR 11, HIPAA     |   M2, Auditoría Financiera    |
+--------------------------+----------------------------+-------------------------------+
```

Cada entorno activa de manera determinista un conjunto de salvaguardas, integraciones, tiempos de retención y protocolos de supervisión humana (HITL) adaptados a la regulación sectorial correspondiente, sin comprometer el aislamiento entre organizaciones.

---

## 2. Matriz Comparativa Multidimensional

| Criterio / Dimensión | 🏢 Corporativo Neutro | 🏥 Medical & Farma | 🏦 Bancario & Financiero |
|---|---|---|---|
| **Identificador de Perfil** | `CORPORATE_NEUTRAL` (alias `EXPRESS`) | `HEALTHCARE_CLINICAL` | `BANKING_ENTERPRISE` |
| **Variable Frontend** | `VITE_APP_EDITION=corporate` (o por defecto) | `VITE_APP_EDITION=medical` | `VITE_APP_EDITION=banking` |
| **Variable Backend** | `APP_EDITION=corporate` | `APP_EDITION=medical` | `APP_EDITION=banking` |
| **Marco Legal Primario** | RGPD (UE 2016/679) · EU AI Act (UE 2024/1689) | HIPAA Safe Harbor · FDA 21 CFR Part 11 · RGPD Art. 9 | DORA (UE 2022/2554) · AML/SEPBLAC · EBA Outsourcing |
| **Supervisión Humana (HITL)** | Aprobación estándar simple | Revisión médica calificada con firma electrónica individual | Doble aprobación humana independiente (4 ojos - M2) |
| **Filtro DLP Activo** | Detección PII general (email, DNI, teléfono, secretos) | Detección estricta de PHI (18 identificadores HIPAA Safe Harbor) | Detección PII financiero (IBAN, tarjetas, transferencias, cuentas) |
| **Retención WORM de Auditoría** | 30 días (ampliable por contrato) | 2.555 días ($\ge 7$ años, exigencia regulatoria clínica) | 90 días a 10 años (exigencia contable y supervisión bancaria) |
| **Time-out Inactividad de Sesión** | 60 minutos | 15 minutos (estricto HIPAA Security Rule) | 30 minutos (estándar bancario) |
| **Conmutación SRE y Failover** | Alta disponibilidad estándar | Alta disponibilidad con custodia inmutable | Conmutación DORA en $< 30\text{ s}$ (RTO $18,55\text{ ms}$, RPO $= 0\text{ s}$) |
| **Integraciones Clave** | ServiceNow, Jira, Slack, SAP, Salesforce, Office 365 | SMART on FHIR, Epic Systems, Medidata Rave, Veeva Vault, Benchling | Core Banking, SWIFT ISO 20022, Pasarelas de Pago, Prevención Blanqueo |
| **Firma Electrónica Avanzada** | Opcional | Obligatoria con manifestación de motivo y timestamp criptográfico | Obligatoria con verificación de rol y grupo independiente |
| **Aislamiento Multi-Tenant** | PostgreSQL RLS estricto | PostgreSQL RLS estricto + Cuarentena clínica | PostgreSQL RLS estricto + Particionado contable |

---

## 3. Especificación Detallada por Entorno

### 3.1. Entorno Corporativo Neutro (`CORPORATE_NEUTRAL`)
- **Público Objetivo:** Empresas multisectoriales (servicios profesionales, manufactura, retail, logística, energía, educación, telecomunicaciones).
- **Casos de Uso Típicos:**
  - Automatización de solicitudes de compras y aprobación de facturas (OCR + conciliación contable).
  - Onboarding y offboarding de empleados en Recursos Humanos.
  - Clasificación y enrutamiento inteligente de tickets en Helpdesk / Service Desk (ServiceNow, Jira).
  - Gestión contractual y extracción asistida de cláusulas legales con RAG privado.
- **Ventajas Operativas:** Puesta en marcha ágil en días, sin la fricción de dobles aprobaciones para operaciones no críticas, manteniendo la garantía de cero fuga de secretos hacia modelos externos.

### 3.2. Entorno Medical y Ciencias de la Salud (`HEALTHCARE_CLINICAL`)
- **Público Objetivo:** Hospitales, redes sanitarias, laboratorios farmacéuticos, CROs (organizaciones de investigación clínica) y biotecnología.
- **Casos de Uso Típicos:**
  - Cribado y reclutamiento de candidatos para ensayos clínicos mediante cotejo automatizado con protocolos.
  - Farmacovigilancia y procesamiento de Informes de Casos de Seguridad Individual (ICSR).
  - Sincronización de cuadernos de laboratorio electrónicos (ELN) con inventario de muestras y reactivos.
  - Detección temprana de anomalías en constantes vitales con derivación inmediata al personal médico.
- **Garantías Sanitarias:** Cumplimiento nativo con **FDA 21 CFR Part 11** (firmas inalterables, pistas de auditoría que registran quién, cuándo y por qué modificó un dato) y desidentificación automática de PHI (Protected Health Information) según **HIPAA**.

### 3.3. Entorno Bancario y Financiero (`BANKING_ENTERPRISE`)
- **Público Objetivo:** Bancos centrales, banca comercial y corporativa, gestoras de fondos, aseguradoras y proveedores de servicios de pago regulados.
- **Casos de Uso Típicos:**
  - Análisis de transacciones sospechosas de blanqueo de capitales (AML) y verificación KYC.
  - Evaluación asistida de riesgos crediticios y comités de riesgo.
  - Conciliación de liquidaciones y tesorería multi-divisa.
  - Homologación de modelos y evaluación de contingencia bajo la Directiva DORA.
- **Garantías Bancarias:** Resiliencia extrema con conmutación en milisegundos, salvaguarda sintáctica de scripts destructivos (AST Security Guard), paquete formal de homologación M2 y doble revisión obligatoria para cualquier cambio de configuración o ejecución sensible.

---

## 4. Configuración de Entornos y Despliegue

La plataforma permite conmutar el entorno de manera global en el despliegue o por organización (*tenant*) mediante la API administrativa:

### Configuración en Despliegue (`.env`):
```bash
# Para Entorno Corporativo Neutro:
APP_EDITION=corporate
DEFAULT_GOVERNANCE_PROFILE=CORPORATE_NEUTRAL

# Para Entorno Medical y Salud:
APP_EDITION=medical
DEFAULT_GOVERNANCE_PROFILE=HEALTHCARE_CLINICAL

# Para Entorno Bancario y Financiero:
APP_EDITION=banking
DEFAULT_GOVERNANCE_PROFILE=BANKING_ENTERPRISE
```

### Configuración en Frontend (`frontend/.env`):
```bash
# Controla la apariencia visual, menús y etiquetas sectoriales:
VITE_APP_EDITION=corporate   # o 'medical' o 'banking'
```

### Conmutación Dinámica por Tenant (API Segura):
```http
PUT /api/admin/tenants/{tenantId}/governance-profile
Authorization: Bearer <TOKEN_ADMIN>
Content-Type: application/json

{
  "profile": "HEALTHCARE_CLINICAL"
}
```

---

## 5. Gobernanza de IA Común (EU AI Act - Reglamento UE 2024/1689)

Con independencia del entorno empresarial seleccionado, **todos los entornos comparten los principios no negociables de la gobernanza de IA de Flentio**:
1. **Supervisión Humana Obligatoria (HITL):** Ningún agente ejecuta acciones irreversibles de manera autónoma.
2. **Fundamentación y Citas Reales:** Toda conclusión se apoya en evidencias indexadas (`E#`), quedando prohibida la alucinación de datos normativos.
3. **Inmutabilidad WORM:** Registro con huella digital SHA-256 de cada decisión, consulta y respuesta.
4. **Minimización de Datos y Zero Data Retention (ZDR):** Los datos corporativos privados nunca se utilizan para entrenar modelos públicos de terceros.
