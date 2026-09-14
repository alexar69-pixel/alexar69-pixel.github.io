# Preparación productiva del RAG: datos, objetivos y controles externos

## Estado y principio de evidencia

Este documento fija una base de ingeniería para continuar sin datos de clientes. No certifica a Flentio para un banco ni atribuye los valores a un cliente. La regulación DORA exige que continuidad, recuperación, redundancia y pruebas partan del análisis de impacto de negocio (BIA); no impone un único número universal de disponibilidad, RPO o RTO. Fuente primaria: Reglamento (UE) 2022/2554, artículos 11 y 12: https://eur-lex.europa.eu/eli/reg/2022/2554/oj/eng

Durante desarrollo se utilizará un **corpus sintético técnico Flentio**, creado desde cero, sin nombres, operaciones, secretos ni documentos de posibles clientes. Es datos de prueba ejecutados por el sistema real, no una fuente para afirmar calidad bancaria. Cada ejecución debe registrar generador/versión, semilla, checksum del manifiesto, número y distribución de documentos, volumen, consultas esperadas y métricas observadas. Los informes usarán las etiquetas `SINTETICO_NO_CLIENTE` y `NO_ACREDITA_PRODUCCION`.

## Objetivos provisionales de ingeniería

El propietario ha autorizado usar objetivos habituales como punto de partida. Se adoptan como **baseline provisional**, sujeto a BIA y contrato de cada banco:

| Servicio | Objetivo inicial | Medición y límite |
|---|---:|---|
| Disponibilidad de recuperación RAG | 99,95 % mensual | API de recuperación autorizada; objetivo arquitectónico 99,99 % para clientes que la clasifiquen Tier 0 |
| Disponibilidad de ingesta/conectores | 99,90 % mensual | acepta degradación temporal porque la consulta sigue usando el último conocimiento efectivo |
| Latencia de recuperación | p95 ≤ 1,5 s; p99 ≤ 3 s | sólo RAG: autorización, búsqueda y reranking; excluye generación del LLM y red del cliente |
| Frescura incremental | p95 ≤ 5 min; p99 ≤ 15 min | desde cambio visible en el proveedor hasta versión efectiva; depende de cuota/webhook |
| RPO de documentos y metadatos | ≤ 5 min | requiere WAL/PITR y almacenamiento versionado productivos; no demostrado en desarrollo |
| RPO de auditoría crítica | 0 eventos confirmados perdidos | exige outbox y destino durable/WORM con acuse; todavía no implementado externamente |
| RTO de recuperación | ≤ 30 min | restauración del servicio de consulta; requiere arquitectura HA/DR productiva |
| RTO de ingesta/conectores | ≤ 4 h | cola durable y reconciliación recuperan cambios pendientes |

Un mes de 30 días al 99,95 % admite aproximadamente 21 min 36 s de indisponibilidad; al 99,99 %, 4 min 19 s. Mantenimientos y exclusiones contractuales deben definirse expresamente, no borrarse de las métricas. En desarrollo sin HA estos objetivos sólo configuran futuros ensayos; no se declaran cumplidos.

Pruebas mínimas futuras: carga sostenida y picos, pérdida de worker/reranker/base/objeto, restauración desde backup, PITR, reconciliación de conectores, rotación/revocación de secretos, rollback de índice y ejercicio de DR. DORA exige probar al menos anualmente los planes que soportan funciones críticas; Flentio propone restauración técnica trimestral y DR integral anual, ajustables por BIA.

## Estrategia SIEM: interoperabilidad antes que bloqueo de proveedor

Un banco grande normalmente ya dispone de SOC y SIEM. Flentio no debe imponer uno: la decisión recomendada es implementar una **outbox de auditoría durable y adaptadores sustituibles**, manteniendo PostgreSQL como fuente operacional y entregando al destino elegido por cada cliente con TLS, identidad técnica, acuse, reintento, deduplicación y reconciliación. OpenTelemetry Collector puede servir de capa de transporte neutral, pero no sustituye al SIEM ni al archivo WORM.

| Opción | Encaje favorable | Costes/riesgos | Recomendación |
|---|---|---|---|
| Microsoft Sentinel | bancos con Azure, Entra, Defender y KQL; servicio gestionado; tier analítico y data lake | coste por ingesta/consulta, diseño DCR, región y dependencia Azure | opción preferente si el cliente es Microsoft-first |
| Splunk Enterprise Security / Cloud | ecosistema maduro, HEC HTTPS, SPL y alertado basado en riesgo; buen encaje heterogéneo | licencia y almacenamiento normalmente elevados; exige gobernar índices, ack y capacidad | opción preferente si el banco ya opera Splunk |
| Elastic Security | cloud o self-managed, búsqueda potente, SIEM/XDR y portabilidad relativa | operación propia compleja en self-managed; licencias y características varían por tier | buena opción soberana o para clientes con Elastic existente |
| Google Security Operations | escala gestionada, normalización y retención base amplia | dependencia Google, política de residencia/retención y contrato; una retención global por instancia | opción para clientes Google Cloud/SecOps |
| IBM QRadar | presencia histórica bancaria, cloud/on-prem, flujos y numerosas integraciones | operación y coste; migraciones/versiones requieren planificación | adaptador por demanda de clientes existentes |
| OpenSearch Security Analytics | abierto y autogestionable, detecciones y alertas | mayor carga operativa y responsabilidad de soporte/cumplimiento | desarrollo/laboratorio o despliegue soberano con equipo competente |

Fuentes oficiales consultadas:

- Sentinel, arquitectura y retención: https://learn.microsoft.com/en-us/azure/sentinel/datalake/sentinel-lake-overview
- Sentinel, modelo de costes: https://learn.microsoft.com/en-us/azure/sentinel/billing
- Splunk Cloud HEC: https://docs.splunk.com/Documentation/SplunkCloud/9.3.2411/Service/SplunkCloudservice
- Splunk Enterprise Security y riesgo: https://docs.splunk.com/Documentation/ES/8.1.0/User/AnalyzeInvestigationEvents
- Elastic Security: https://www.elastic.co/guide/en/security/current/es-overview.html
- Google Security Operations, retención: https://docs.cloud.google.com/chronicle/docs/about/data-retention
- IBM QRadar: https://www.ibm.com/docs/en/security-qradar/security-qradar-siem/saas?topic=qradar-platform-overview
- OpenSearch Security Analytics: https://docs.opensearch.org/latest/security-analytics/

No se selecciona proveedor final sin conocer el SIEM corporativo, residencia, volumen diario, retención, contrato, SOC, formato y presupuesto del cliente. La primera integración de producto debe soportar al menos Sentinel y Splunk mediante adaptadores, dejando abierta Elastic/Google/QRadar.

## Revisión independiente no disponible

La falta de revisión independiente no bloquea el desarrollo. Flentio continuará con pruebas automatizadas, análisis de dependencias, revisión interna, threat model, pruebas negativas, trazabilidad y evidencia reproducible. Sin embargo, esos controles no se renombrarán como independientes. Antes de producción bancaria seguirá existiendo una puerta externa: pentest o revisión por una parte que no haya desarrollado el componente, más validaciones legales, privacidad, continuidad y del SOC del cliente. Si el banco aporta sus propios equipos de assurance, su revisión puede satisfacer esta puerta.

## Paquete de entrega al cliente

La preparación de cada instalación se registra mediante
`docs/RAG_EXTERNAL_INFRASTRUCTURE_HANDOFF.md` y las plantillas
`RAG_CLIENT_INFRASTRUCTURE_INTAKE.md`,
`RAG_PRODUCTION_PARAMETER_WORKSHEET.md` y
`RAG_PRODUCTION_ACCEPTANCE_CHECKLIST.md`. Los objetivos de esta página son una
baseline provisional: sólo el BIA y la aceptación firmada del cliente pueden
convertirlos en compromisos productivos.

Flentio implementa AWS S3/S3 compatible y envelope encryption con AWS KMS, pero
sin infraestructura ni credenciales del cliente su estado es
`NO_CONFIGURADO`. La existencia del adaptador no demuestra residencia, HA,
RPO/RTO, WORM, capacidad ni cumplimiento.
