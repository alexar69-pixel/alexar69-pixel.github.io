# Análisis de Agentes de Inteligencia Artificial — Flentio Platform (v1.0.0)

Este documento analiza la arquitectura, proveedores, seguridad y contratos de los **Agentes de IA** configurados en **Flentio Platform**.

---

## 1. Clasificación y Tipología de Agentes

| Tipo de Agente | Fichero Fuente | Propósito y Capacidades | Nivel de Autonomía |
|---|---|---|---|
| **Single Agent** | `flentio_single_agent.js` | Razonamiento autónomo monoproceso para decisiones simples, traducción o clasificación. | Automatizado con DLP previo |
| **Multi-Agent Swarm** | `ai_agent_swarm.js` | Coordinación entre múltiples agentes (Triage, Investigador, Síntesis). | Enjambre coordinado con RLS |
| **Auto-SRE Agent** | `flentio_auto_sre.js` | Diagnóstico de incidentes operacionales, telemetría e integración ITSM. | `CANDIDATE_NOT_CAUSAL` (Sin remediación autónoma) |
| **Agente RAG con Evidencia** | `agentEvidenceAudit.js` | Agentes conectados a la base de conocimiento vectorial con citas obligatorias `[E#]`. | Abstención si falta evidencia |

---

## 2. Adaptadores de Modelos Generativos (LLM Engine Matrix)

### 2.1 Ollama (Local — Soberanía Total de Datos)
- **Modelo Validado**: `llama3.2:3b` / `llama3`.
- **Ventajas**: 100% local, latencia predecible, cero transferencia externa de datos y sin costes por token.
- **Soporte de Citas**: Soporta salidas en esquema JSON con referencias `[E1]..[E50]`.

### 2.2 OpenAI (Responses API / Chat Completions)
- **Modo**: Salida estructurada con esquema JSON estricto (`response_format`).
- **Seguridad**: Requiere credencial aprovisionada en la Bóveda AES-256-GCM y evaluación A/B aprobada.

### 2.3 Google Gemini (Interactions API)
- **Modo**: Integración con contrato estructurado de Interactions API.
- **Seguridad**: Respeto de Zero Data Retention contratada y aislamiento por tenant.

### 2.4 Codex OAuth Local (`codex-oauth-local`)
- **Modo**: Adaptador de desarrollo que reutiliza la sesión oficial de Codex CLI para pruebas locales sin exponer claves API.

---

## 3. Mecanismos de Gobierno y Seguridad

```mermaid
graph TD
    A[Petición del Usuario / Flujo] --> B[Filtro DLP: Prevención Fugas]
    B --> C[Verificación RLS Tenant]
    C --> D{¿Consulta a Conocimiento RAG?}
    D -- "Sí" --> E[Recuperación HNSW + TEI Rerank]
    E --> F{¿Hay Evidencia?}
    F -- "No" --> G[Abstención Automática: SIN_DATOS / No llama al LLM]
    F -- "Sí" --> H[Asignación Citas Efímeras E1..E50]
    H --> I[Invocación LLM: Ollama / OpenAI / Gemini]
    D -- "No" --> I
    I --> J[Verificador de Citas [E#] y JSON]
    J --> K[Auditoría Inmutable 015_agent_evidence_runs]
```

### 3.1 Prevención de Fugas de Datos (DLP Previo)
Antes de enviar el prompt a cualquier modelo generativo (local o externo), el motor DLP inspecciona y enmascara:
- Tarjetas de crédito/débito.
- Números de cuenta e IBAN.
- Documentos de identidad (DNI/NIE).
- Secretos y llaves de API.

### 3.2 Abstención Inteligente (Contrato de Evidencia)
Si una consulta RAG no devuelve fragmentos autorizados con la puntuación mínima requerida:
- El agente se abstiene inmediatamente devolviendo `EVIDENCIA_INSUFICIENTE`.
- **No se realiza ninguna llamada al modelo generativo**, eliminando el riesgo de alucinaciones.

### 3.3 Prompt Caching Gobernado
- Mantiene estables las instrucciones de sistema, esquemas y políticas en la cabecera del prompt.
- La clave de caché incluye obligatoriamente `tenantId` para evitar cualquier fuga de contexto entre organizaciones diferentes.

---

## 4. Matriz de Auditoría y Trazabilidad

- **Tabla de Auditoría**: `flentio_rag.agent_evidence_runs` (Migración `015`).
- **Datos Registrados**: Identificador de actor, correlación de workflow/job, proveedor/modelo, estado (`grounded`, `evidence_insufficient`, `citation_rejected`), puntuaciones y SHA-256 de las consultas.
- **Privacidad**: Nunca se almacenan las preguntas o respuestas en texto plano en la tabla de auditoría general.
