# Registro de Riesgos — Flentio Platform

> Documento para dirección y responsables de producto. Registra los riesgos técnicos, operativos, comerciales y regulatorios identificados. Se actualiza con cada cambio funcional significativo.
>
> Última revisión: Agosto 2026

---

## Escala de valoración

| Probabilidad | Descripción |
|---|---|
| **Alta** | Esperado que ocurra sin acción |
| **Media** | Posible en condiciones normales |
| **Baja** | Requiere circunstancias adversas específicas |

| Impacto | Descripción |
|---|---|
| **Crítico** | Paraliza el producto o compromete datos de cliente |
| **Alto** | Afecta significativamente adopción, ingresos o cumplimiento |
| **Medio** | Degrada la experiencia o la propuesta de valor |
| **Bajo** | Impacto menor o fácilmente mitigable |

---

## Riesgos técnicos

### RT-01 — Alta disponibilidad de PostgreSQL no implementada
- **Estado:** `ABIERTO`
- **Descripción:** El sistema usa PostgreSQL como único datastore. No existe configuración de HA (réplica, failover automático) ni procedimientos de backup/restore validados con SLO bancarios.
- **Probabilidad:** Media | **Impacto:** Crítico
- **Mitigación actual:** PostgreSQL con RLS; infraestructura del cliente puede añadir HA
- **Acción requerida:** Definir SLO, procedimientos de backup/restore y configuración de réplica antes de despliegue productivo bancario

### RT-02 — Sin acceso a infraestructura del cliente para validar conectores
- **Estado:** `ABIERTO`
- **Descripción:** Los 29 conectores de integración (Jira, Grafana, Dynatrace, etc.) están implementados pero no probados contra sistemas reales de clientes. El estado real de cada conector es `NO_CONFIGURADO`.
- **Probabilidad:** Alta (actual) | **Impacto:** Medio
- **Mitigación actual:** Documentación clara del estado `NO_CONFIGURADO`; conectores técnicamente completos
- **Acción requerida:** Primer cliente real para validar conectores prioritarios

### RT-03 — Dependencia de proveedores LLM externos
- **Estado:** `ACTIVO · MITIGADO PARCIALMENTE`
- **Descripción:** El sistema depende de APIs externas de Gemini, OpenAI y NVIDIA para inferencia IA. Una interrupción o cambio en los términos de servicio afectaría a funciones de IA.
- **Probabilidad:** Media | **Impacto:** Medio
- **Mitigación actual:** Fallback multi-modelo implementado (Gemini → OpenAI → Ollama); soporte para modelos locales con NVIDIA NIM y Ollama
- **Acción requerida:** Política de selección de modelo por criticidad del proceso; validación de Ollama en entornos aislados

### RT-04 — Tamaño de chunks de bundle frontend
- **Estado:** `MONITOREADO`
- **Descripción:** Algunos chunks del bundle superan 500KB, lo que puede afectar la carga inicial en redes lentas.
- **Probabilidad:** Baja | **Impacto:** Bajo
- **Mitigación actual:** Code-splitting parcial implementado (lazy loading de paneles pesados)
- **Acción requerida:** Optimizar chunking en las próximas iteraciones de build

---

## Riesgos operativos

### RO-01 — Homologación M2 sin dataset bancario real
- **Estado:** `ABIERTO`
- **Descripción:** El evaluador M2 existe y funciona, pero con el dataset sintético `NO_BANCARIO_NO_HOMOLOGABLE`. La homologación real requiere un dataset bancario autorizado y revisión independiente.
- **Probabilidad:** Media | **Impacto:** Alto (para ventas a banca)
- **Mitigación actual:** Documentación transparente del estado `NO_HOMOLOGADO`
- **Acción requerida:** Obtener dataset bancario autorizado con primer cliente piloto

### RO-02 — M3 (ejecución física) bloqueada por diseño
- **Estado:** `CONTROLADO`
- **Descripción:** La Skill de remediación M3 (`r1.preprod.restart_workload.v1`) está construida pero con ejecución físicamente bloqueada en código y tests. No existe endpoint de ejecución.
- **Probabilidad:** N/A (bloqueado) | **Impacto:** Crítico si se desbloquea sin proceso aprobado
- **Mitigación actual:** Triple bloqueo: código, tests y ausencia de endpoint
- **Acción requerida:** No habilitar sin nueva fase aprobada, game day real y credencial efímera

### RO-03 — Gestión de credenciales en entornos multi-desarrollador
- **Estado:** `ACTIVO`
- **Descripción:** El riesgo de compartir credenciales entre desarrolladores o versionar `.env` existe en todo proyecto con múltiples contribuidores.
- **Probabilidad:** Media | **Impacto:** Alto
- **Mitigación actual:** `.gitignore` configurado; herramienta de detección de secretos recomendada; política documentada
- **Acción requerida:** Escáner automático de secretos en CI/CD antes de primer cliente

### RO-04 — Documentos RAG desactualizados sin alerta
- **Estado:** `MONITOREADO`
- **Descripción:** Los documentos indexados en el RAG pueden desactualizarse. Si la normativa cambia y el documento no se reindexa, el copiloto puede citar información obsoleta.
- **Probabilidad:** Media | **Impacto:** Medio
- **Mitigación actual:** Conectores incrementales para Google Drive y SharePoint; procedencia y WORM registran versiones
- **Acción requerida:** Política de revisión periódica de corpus RAG por el administrador; alertas de documentos con antigüedad >90 días

---

## Riesgos comerciales y de mercado

### RC-01 — Internalización de la capa de control por grandes bancos
- **Estado:** `MONITOREADO`
- **Descripción:** BBVA, Santander, JPMorgan y otros grandes bancos están construyendo sus propias plataformas de agentes (Blue, LLM Suite). Si internalizan la capa de gobierno, el mercado TAM de Flentio se reduce.
- **Probabilidad:** Media (largo plazo) | **Impacto:** Alto
- **Mitigación:** Especialización en excepciones operativas y regulatorias donde los equipos internos no tienen recursos ni experiencia acumulada; foco en bancos medianos que no pueden invertir en plataformas propias

### RC-02 — Hipótesis de mercado sin validar
- **Estado:** `ABIERTO`
- **Descripción:** Las 3 oportunidades P1 (excepciones gobernadas, cambio regulatorio → proceso, autoridad delegada) son hipótesis de investigación documental. No están confirmadas por clientes.
- **Probabilidad:** N/A | **Impacto:** Alto si se invierte en el ángulo equivocado
- **Mitigación:** Plan de validación documentado: talleres con operativos bancarios, 5 especialistas de proceso, prototipo no-code con dataset sintético antes de integración productiva
- **Acción requerida:** Ejecutar taller de validación Q3 2026

### RC-03 — Mercado saturado de "plataformas de agentes IA"
- **Estado:** `ACTIVO`
- **Descripción:** El mercado de construcción de agentes IA está hipercompetido (LangChain, AutoGen, CrewAI, Vertex AI, Bedrock, n8n...). Posicionarse como "plataforma de agentes" genérica es inviable.
- **Probabilidad:** Alta | **Impacto:** Medio (si no se diferencia)
- **Mitigación:** Posicionamiento claro en gobierno/evidencia/excepciones bancarias — no en construcción de agentes

---

## Riesgos regulatorios

### RR-01 — Cambio regulatorio que invalide supuestos de diseño
- **Estado:** `MONITOREADO`
- **Descripción:** Los marcos regulatorios de IA (AI Act, DORA, BCE/SSM) están evolucionando. Un cambio en los requisitos podría invalidar partes del diseño actual.
- **Probabilidad:** Baja (próximos 12 meses) | **Impacto:** Alto
- **Mitigación:** Diseño basado en principios (responsabilidad humana, trazabilidad, aislamiento, explicabilidad) más que en reglas específicas; seguimiento activo de publicaciones BCE/EBA

### RR-02 — Homologación de proveedores IA para uso bancario
- **Estado:** `ABIERTO`
- **Descripción:** Los bancos europeos están empezando a exigir que los proveedores LLM cumplan condiciones de residencia de datos, ZDR y auditoría. El estado de esta homologación varía por proveedor y jurisdicción.
- **Probabilidad:** Media (próximos 24 meses) | **Impacto:** Medio
- **Mitigación:** Soporte para modelos locales (Ollama/NIM) que no requieren enviar datos a terceros; configuración de residencia por proveedor

---

## Historial de cierre de riesgos

| ID | Descripción | Fecha cierre | Cómo se resolvió |
|---|---|---|---|
| RT-00 | SQLite sin RLS como datastore principal | 2026-08 | Migración completa a PostgreSQL con RLS |
| RO-00 | Sin aislamiento multi-tenant | 2026-08 | RLS implementado en toda la pila |
| RT-05 | Tests con mocks que sustituían comportamiento real | 2026-08 | Tests refactorizados para usar SDKs reales contra servidores efímeros |
