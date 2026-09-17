# Transición Arquitectónica: De Agentes Fragmentados a Enterprise Skills Gobernadas

## 1. Resumen Ejecutivo y Motivación

Históricamente, los sistemas de automatización asistida por IA tendieron a proliferar en agentes aislados y autónomos (*Swarm*, *Compliance Agent*, *FinOps Agent*, *SecOps Agent*). Si bien este modelo ilustra la especialización, introduce graves desventajas en entornos corporativos y bancarios de alta exigencia:

1. **Sobrecarga de Latencia y Serialización (Handoff Overhead):** La coordinación de múltiples agentes que se pasan contexto en cadena genera latencias acumuladas de varios segundos y degradación semántica.
2. **Incompatibilidad con Prompt Caching:** Cada agente define su propio prompt de sistema monolítico, lo que impide reutilizar prefijos estables en proveedores LLM empresariales (Gemini, Claude, OpenAI), violando la optimización de costes y cuotas.
3. **Complejidad de Auditoría y Trazabilidad (DORA / SOC2):** En una auditoría financiera, justificar las decisiones de un enjambre de 5 subagentes opacos que interactúan sin memoria compartida resulta inviable.
4. **Fragilidad de Mantenimiento:** Cualquier cambio funcional exige redefinir la identidad, guardrails y contexto de un agente completo, en lugar de modificar una capacidad atómica.

Para resolver esto, **Flentio Platform transiciona hacia una Arquitectura Unificada de Skills Empresariales (Skill-First Architecture)**:
Un agente base gobernado (o el Copiloto No-Code) equipado dinámicamente con un **Catálogo Modular de Skills**.

---

## 2. Topología Arquitectónica

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COPILOTO NO-CODE / AGENTE CENTRAL GOBERNADO              │
│       (Prefijo estable cacheable · Aislamiento RLS · Guardrails DLP)       │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Invoca bajo demanda (Tool Use / Function Calling)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     ENTERPRISE SKILLS REGISTRY & RUNTIME                    │
│                        (enterpriseSkillsService.js)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  1. Verificación de Manifiesto y Esquema JSON (Entradas / Salidas)          │
│  2. Inspección DLP Automática preventiva de parámetros                      │
│  3. Verificación de Ciclo de Vida: INSTALLED · CONFIGURADA · ACTIVA         │
│  4. Auditoría Append-Only: ENTERPRISE_SKILL_EXECUTED                        │
└──────────────┬───────────────────────────────┬──────────────────────────────┘
               │                               │
               ▼                               ▼
┌───────────────────────────────┐┌────────────────────────────────────────────┐
│ SKILLS OPERACIONALES NATIVAS  ││ INTEGRATION SKILLS (31 conectores)         │
├───────────────────────────────┤├────────────────────────────────────────────┤
│ • flentio.skill.compliance_dora││ • Prometheus · Grafana · Datadog           │
│ • flentio.skill.finops_prompt ││ • Ollama · OpenAI · Gemini · NVIDIA        │
│ • flentio.skill.secops_triage ││ • Jira · BMC Helix · HashiCorp Vault · AWS  │
│ • flentio.skill.sre_probe     ││ • CMDB / SBOM · Splunk ITSI · Dynatrace    │
└───────────────────────────────┘└────────────────────────────────────────────┘
```

---

## 3. Catálogo de Skills Operacionales Nativas

Las capacidades previamente repartidas en agentes monolíticos se han consolidado como Skills nativas tipificadas:

### 3.1 `flentio.skill.compliance_dora`
- **Categoría:** `compliance`.
- **Contrato:** Exige `regulation` ('DORA', 'SEPA_INST', 'PSD2', 'AML_KYC') y `contextSnippets`.
- **Regla Invariable:** Si no se aportan evidencias documentales (`contextSnippets` vacío), se abstiene de inmediato emitiendo `NO_EVIDENCIA_SUFICIENTE` (`grounded: false`). Si hay evidencia, emite veredicto conforme con citas `[E#]`.

### 3.2 `flentio.skill.finops_prompt_cache`
- **Categoría:** `finops`.
- **Contrato:** Exige `usageStats` (`inputTokens`, `outputTokens`, `cachedTokens`).
- **Función:** Calcula el ratio efectivo de Prompt Caching (`cacheHitRatio`), calcula el consumo total y prescribe optimizaciones de prefijo inmutable.

### 3.3 `flentio.skill.secops_triage`
- **Categoría:** `security`.
- **Contrato:** Exige objeto `alert`, opcionalmente `cveId` y `severity`.
- **Gobernanza Bancaria:** Clasifica la alerta preservando la etiqueta `CANDIDATE_NOT_CAUSAL` para impedir remediaciones destructivas no autorizadas.

### 3.4 `flentio.skill.sre_probe`
- **Categoría:** `operations`.
- **Contrato:** Exige `probeType` ('spider', 'cve', 'pki', 'dora', 'dlp', 'sbom', 'chaos') y `targetScope`.
- **Ejecución Real:** Despacha la sonda al motor SRE real; si no está configurada, devuelve error estructurado sin fabricar datos.

---

## 4. Gobernanza y Prompt Caching

Al unificar las herramientas bajo el paradigma de Skills:

1. **Prefijo de Sistema Cacheable:**
   El Agent Studio compila un prefijo estático con:
   ```text
   <system_policy>
   Domain: COMPLIANCE
   Enforce DLP: true
   Require Citations: true
   <equipped_skills>
   flentio.skill.compliance_dora
   </equipped_skills>
   </system_policy>
   ```
   Este bloque genera un hash SHA-256 idéntico entre ejecuciones para el mismo tenant y configuración, maximizando los hits de Prompt Caching en proveedores como Gemini, OpenAI o Anthropic.

2. **DLP Preventivo:**
   Toda ejecución en `executeSkill` inspecciona y enmascara automáticamente cadenas de texto antes de llegar al runtime de la Skill, protegiendo tarjetas de crédito, IBANs, emails, tokens de API y claves privadas.

3. **Trazabilidad Append-Only:**
   Toda invocación emite un evento `ENTERPRISE_SKILL_EXECUTED` con `tenantId`, `actorId`, `skillId`, `category` y `executionTimeMs`.

---

## 5. Compatibilidad Retroactiva

Para garantizar la no interrupción del servicio ni de las pruebas automáticas existentes:
- `executeComplianceAgent`, `executeFinOpsAgent` y `executeSecOpsAgent` han sido refactorizados para delegar internamente en `enterpriseSkillsService.executeSkill()`.
- El nodo `flentio_single_agent` delega en `flentio.skill.sre_probe`.
- El nuevo nodo `flentio_skill_node` permite a cualquier usuario de flujos visuales ejecutar cualquier Skill del catálogo de forma declarativa y No-Code.

---

## 6. Enterprise Skills IA Especializadas para los 3 Entornos (DEV, PREPROD, PROD)

Para solventar las necesidades dispares de seguridad, validación y resiliencia a lo largo del ciclo de vida de software bancario, se han incorporado tres Skills IA nativas en el catálogo:

### 6.1 `flentio.skill.dev_workflow_assistant` (Entorno DEV)
- **Propósito:** Asistente de diseño y desarrollo en DEV.
- **Capacidades Operativas:**
  - **Inspección de Grafos:** Detección automática de nodos huérfanos y de anti-patrones de seguridad (secretos o API keys en texto plano en lugar de la Bóveda AES-256).
  - **Generación de Fixtures Controlados:** Produce conjuntos de datos sintéticos marcados explícitamente como `TEST_ONLY_DATA` y `_synthetic_fixture: true` (cumpliendo con la Regla Invariable #2 de no mezclar datos ficticios con producción).
  - **Validación de Borradores:** Estampa versiones mutables `1.0.0-draft` para iteración rápida.

### 6.2 `flentio.skill.preprod_gatekeeper` (Entorno PREPROD)
- **Propósito:** Pre-vuelo y certificación inmutable para pase a producción.
- **Capacidades Operativas:**
  - **Pre-flight Audit:** Verifica el cumplimiento de políticas DORA (citas obligatorias `ragCitationRequired: true` y DLP activo). Si faltan políticas, bloquea con `BLOCKED_DEFICIENCIES`.
  - **Firma Criptográfica SHA-256:** Congela la definición con digest SHA-256 inmutable y semver de release candidate `1.0.0-rc1`.
  - **Proyección FinOps:** Calcula la eficiencia esperada de Prompt Caching antes de producción.

### 6.3 `flentio.skill.prod_guard_monitor` (Entorno PROD)
- **Propósito:** Guardián de resiliencia bancaria y prevención de incidentes en vivo.
- **Capacidades Operativas:**
  - **Circuit Breaker Activo:** Bloquea de inmediato consultas o comandos destructivos (`DROP TABLE`, `TRUNCATE`, `rm -rf`) que no cuenten con confirmación administrativa explícita.
  - **Monitor de SLA:** Detecta latencias anómalas o roturas de umbral de ejecución (`slaThresholdMs`), prescribiendo conmutación por cuota o escalado de workers.
  - **Puerta de Ejecución con Aislamiento RLS:** Garantiza aislamiento multi-tenant por RLS y auditoría WORM append-only.

---

## 7. Enterprise Skills Especializadas por Sector: Bancario, Médico y Corporativo

Para satisfacer los requisitos normativos y operacionales de los sectores más regulados, se han incorporado tres Skills IA de dominio vertical:

### 7.1 `flentio.skill.banking_iso20022_validator` (Sector Bancario)
- **Propósito:** Validación y liquidación conforme de transferencias financieras e instrucciones de pago.
- **Capacidades Operativas:**
  - **Algoritmo MOD-97 para IBAN (ISO 13616):** Cálculo matemático determinista de checksum sobre enteros de precisión arbitraria (`BigInt`), garantizando cero mocks y cero falsos positivos en cuentas bancarias europeas.
  - **Validación BIC/SWIFT (ISO 9362):** Comprobación estructural de 8 u 11 caracteres alfanuméricos.
  - **Reglas SEPA Instant e ISO 20022:** Verificación de estándares `pacs.008.001.08` y `pain.001.001.09`, control de divisa (EUR) y límite legal por transacción (100.000 EUR).
  - **Control AML / Prevención de Blanqueo:** Alerta automática (`REQUIRES_AML_DECLARATION`) ante operaciones que igualen o superen el umbral de 10.000 EUR.

### 7.2 `flentio.skill.medical_fhir_governance` (Sector Médico y Healthcare)
- **Propósito:** Interoperabilidad clínica segura, cumplimiento de privacidad y firma electrónica.
- **Capacidades Operativas:**
  - **Validación Estructural HL7 FHIR R4:** Inspección de esquemas y conceptos clínicos LOINC, SNOMED-CT y CIE-10 para recursos `Patient`, `Observation`, `Condition` y `MedicationRequest`.
  - **Anonimización HIPAA Safe Harbor:** Supresión automática de nombres, teléfonos, direcciones e identificadores de pacientes (sustituidos por hashes irreversibles `ANON-...`) y conservación exclusiva del año de nacimiento.
  - **Sellado FDA 21 CFR Part 11:** Generación de digests de auditoría SHA-256 para firma y trazabilidad inmutable de registros electrónicos en laboratorios y ensayos clínicos (eTMF / ELN).

### 7.3 `flentio.skill.corporate_cmdb_compliance` (Sector Corporativo y TI)
- **Propósito:** Gobierno de activos de infraestructura, inventario CMDB y seguridad en la cadena de suministro de software.
- **Capacidades Operativas:**
  - **Auditoría de Activos CMDB:** Detección de sistemas operativos en Fin de Vida (`EOL_OPERATING_SYSTEM`: Windows Server 2003/2008/2012, Ubuntu 14/16, CentOS 6/7) y puertos de red inseguros (Telnet 23, FTP 21, SMBv1 445).
  - **Inspección de SBOM CycloneDX (1.6/1.7):** Verificación de integridad SHA-256 del manifiesto de componentes, detección de dependencias sin versión fijada y control de licencias copyleft (`GPL`/`AGPL`) en entornos comerciales.

### 7.4 `flentio.skill.medical_document_imaging` (Sector Médico: PDF, OCR y Radiografías)
- **Propósito:** Procesamiento clínico multiformato de informes PDF, recetas/volantes escaneados mediante OCR y estudios radiológicos.
- **Capacidades Operativas:**
  - **Lectura e Interpretación de PDF Clínicos (`read_pdf`):** Extracción de diagnósticos, medicaciones, constantes vitales y desidentificación automática de PHI (Safe Harbor HIPAA) con cálculo de digest SHA-256.
  - **Extracción OCR de Documentos Escaneados (`read_ocr`):** Extracción de valores de laboratorio en tablas analíticas con detección de valores anormales respecto al rango de referencia.
  - **Análisis de Radiografías e Imagen Médica (`read_radiography`):** Inspección de estudios de tórax, traumatología y DICOM/Base64. Clasificación estructurada de hallazgos (infiltrado/consolidación, fracturas, derrame pleural, cardiomegalia) conforme a estándares ACR y Fleischner Society, con firma electrónica **FDA 21 CFR Part 11**.



