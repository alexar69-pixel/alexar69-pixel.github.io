# Investigación y líneas de acción para incidencias

## Estado

`M0_IMPLEMENTADO_M1_VALIDACION_LOCAL`. PostgreSQL ya conserva alertas normalizadas,
expedientes y referencias de evidencia con RLS. La administración dispone de API
para ingestión autenticada, consulta y anexado de referencias. Grafana tiene
runtime real para validar salud y organización y recepción autenticada por token
rotatorio. Prometheus dispone de consulta temporal gobernada y sólo conserva
agregados, pero no hay conexión del cliente ni capacidad de remediación. El catálogo histórico `flentio_auto_sre` continúa bloqueado por la
política de ejecución y falla con `AUTO_SRE_NO_CONFIGURADO`.

Desde la migración `022`, M1 incorpora orquestación allowlist de Skills de sólo
lectura, correlación por servicio/entorno/ventana, hipótesis deterministas,
contradicciones estructuradas y revisión humana auditada. El resultado conserva
siempre `NOT_ESTABLISHED`: proximidad temporal no demuestra causalidad. Diseño,
rutas, límites y rollback: `docs/GOVERNED_SKILL_ORCHESTRATION.md`.

## Objetivo

A partir de una alerta de Grafana u otra herramienta autorizada, Flentio debe
construir un expediente temporal y producir líneas de acción basadas únicamente
en evidencias recuperadas:

```text
alerta normalizada
  ├─ telemetría y dependencias
  ├─ cambios de los últimos 7 días
  ├─ incidentes similares y resolución confirmada
  ├─ runbooks/documentación vigentes mediante RAG
  └─ catálogo indexado de aplicaciones y ownership
       ↓
hipótesis con confianza y contradicciones
       ↓
líneas de acción ordenadas, prechecks, riesgo y rollback
```

El periodo de siete días es un valor inicial configurable por política, no una
regla fija ni prueba de causalidad.

## Fuentes de evidencia

| Fuente | Datos mínimos | Uso | Confianza inicial |
|---|---|---|---|
| Grafana Alerting/webhook | regla, estado, etiquetas, timestamps, datasource y enlace estable | Evento inicial; no demuestra la causa | Señal |
| Métricas/logs/trazas | ventana anterior/posterior, servicio, entorno y correlación | Confirmar impacto, tendencia y dependencias | Evidencia técnica |
| Cambios | despliegues, configuración, infraestructura, flags, certificados y dependencias | Construir correlación temporal de 7 días | Indicio hasta validar |
| Jira/BMC Helix ITSM | síntomas, servicio, causa confirmada, solución, cambios, resultado y postmortem | Recuperar precedentes realmente resueltos mediante contrato ITSM canónico | Alta sólo si cierre validado |
| BMC HelixGPT/Knowledge | artículos, tickets y casos recuperados por el RAG de Helix | Fuente federada de conocimiento con referencias; no duplicar el índice | Alta sólo con cita resoluble, versión y permiso |
| RAG documental del cliente | runbooks, arquitectura, catálogo, SLO, calendarios y procedimientos vigentes | Restringir diagnóstico y acciones permitidas mediante consulta federada | Citable, no causal por sí sola |
| CMDB/catálogo | aplicación, owner, criticidad, dependencias, hosting y proceso bancario | Calcular impacto y autoridad | Maestra si está vigente |

No se indexarán secretos, tokens, payloads transaccionales ni datos personales
innecesarios. Logs y tickets requieren DLP, clasificación y retención antes de
ingesta.

El contrato CMDB/SBOM acepta referencias `cmdb`, CycloneDX 1.7 y SPDX 2.3/3.0.
Conserva URI, versión, SHA-256, servicio, aplicación, owner, criticidad, hosting
y listas acotadas de identificadores/dependencias; no copia la CMDB ni el SBOM.
Sólo es elegible si coincide con servicio y entorno, no está fechado en el futuro
y tiene una antigüedad máxima inicial de 24 horas. El importador administrativo
CycloneDX 1.7 procesa JSON autorizado en memoria, con máximos de 5 MiB, 500
componentes y 500 dependencias, y persiste sólo la referencia normalizada. La
ruta es `POST /api/admin/operational-investigations/{id}/import-cyclonedx`.
El adaptador CMDB del cliente sigue `NO_CONFIGURADO`; dicho umbral deberá
convertirse en política por criticidad.

Rollback: deshabilitar la ruta y retirar el uso del contrato. No se conserva el
SBOM; las referencias ya auditadas siguen la retención del expediente y la fuente
corporativa mantiene el documento original y su gobierno.

## Sobre Grafana

La primera integración recomendada es **Grafana Alerting por webhook firmado**.
Grafana inicia el expediente, pero Flentio no debe depender del texto libre de
la alerta. El adaptador normaliza un contrato estable:

```json
{
  "source": "grafana",
  "externalAlertId": "identificador-estable",
  "status": "firing",
  "startedAt": "fecha-ISO-8601",
  "serviceId": "catalogo-servicio",
  "environment": "preproduction",
  "severity": "high",
  "labels": {},
  "metricRefs": [],
  "sourceUrl": "enlace-permitido"
}
```

La firma, replay protection, allowlist de origen, límite de tamaño e
idempotencia son obligatorios. Un datasource no reconocido deja el expediente
en `EVIDENCIA_INSUFICIENTE`.

Las migraciones `016_grafana_webhook_channels.sql` y
`021_grafana_webhook_security.sql` implementan el canal
autenticado. El administrador sólo puede crearlo si la Skill Grafana está
validada y activa. El token aleatorio se muestra una vez, se conserva únicamente
como SHA-256 y se rota invalidando el anterior. Grafana debe enviarlo en
`X-Flentio-Webhook-Token` a
`POST /api/integration-webhooks/grafana/{channelId}`. El receptor limita cada
payload a 512 KiB, 50 alertas y 120 peticiones/minuto; exige `service` y
`environment`, descarta anotaciones de texto libre y reutiliza la idempotencia
del expediente.

Cada entrega exige allowlist exacta de IP, timestamp Unix con tolerancia máxima
de cinco minutos, identificador único y `X-Flentio-Webhook-Signature` calculada
como HMAC-SHA256 sobre `timestamp.deliveryId.rawBody`. El identificador se reclama
atómicamente en PostgreSQL y un replay se rechaza. Los recibos técnicos expiran
tras 24 horas. Como Grafana puede no generar este contrato de forma nativa según
edición, el cliente debe validar un contact point compatible o un gateway firmante
homologado. mTLS y esa homologación siguen pendientes; no se declara producción.

## Telemetría Prometheus gobernada

Administración define una política visual por tenant: métrica, etiquetas de
servicio/entorno, agregación, función de rango, ventana, horizonte y paso. No se
acepta PromQL libre. La recogida es manual, de sólo lectura y exige confirmación;
consulta `/api/v1/query_range` por HTTPS usando, si procede, un bearer resuelto
desde la bóveda. El expediente conserva referencia, hash, ventana, número de
series/muestras y min/max/media/primero/último; nunca series, labels o secreto.

Rollback: desactivar la Skill Prometheus. Esto impide nuevas consultas sin borrar
políticas, auditoría ni evidencia histórica. El perfil del cliente permanece
`NO_CONFIGURADO` hasta validación real y homologación de red/TLS.

## Línea temporal de cambios

La consulta inicial cubre `[inicio_alerta - 7 días, momento_investigación]` y
ordena los cambios por proximidad, dependencia e impacto potencial. Debe incluir:

- commits y pull requests desplegados, no sólo fusionados;
- releases, artefacto, SBOM y versión efectiva;
- cambios de configuración y feature flags;
- infraestructura como código y plataforma;
- certificados, secretos rotados y políticas;
- cambios de dependencias externas;
- actor, aprobación, ventana y rollback asociado.

Una coincidencia temporal se presenta como **correlación**, nunca como causa.

El contrato `changeRecordContract` admite fuentes ASO/APX, GitHub Actions,
GitLab CI, Jenkins, Argo CD y Azure DevOps, además de alta manual verificada.
Un despliegue sólo es evidencia elegible si está efectivo, aprobado, pertenece al
mismo servicio/entorno y ventana, y referencia tanto aprobación como rollback.
Commits, merges o planes de despliegue no bastan. El contrato está implementado;
los adaptadores reales del cliente permanecen `NO_CONFIGURADO`.

## Incidentes similares

La similitud debe combinar:

1. servicio, dependencia, entorno y versión;
2. patrón de métricas/logs/trazas;
3. firma de error y propagación;
4. cambios cercanos;
5. impacto bancario;
6. causa y resolución confirmadas.

Los tickets cerrados sin causa validada o sin verificación de recuperación no
se usarán como precedentes de alta confianza. El RAG devuelve fragmentos y citas;
los campos estructurados de incidente permanecen en PostgreSQL para filtros y
relaciones exactas.

## Separación RAG y datos estructurados

| Contenido | Almacenamiento propuesto |
|---|---|
| Runbooks, postmortems, arquitectura y procedimientos | RAG interno del cliente; índice Flentio dentro de su perímetro sólo si se autoriza |
| Aplicaciones, servicios, owners y dependencias | PostgreSQL/grafo autorizado |
| Alertas, incidentes, cambios y acciones | PostgreSQL temporal y auditable |
| Métricas masivas, logs y trazas | Permanecen en la herramienta de observabilidad; Flentio guarda referencias y agregados mínimos |
| Secretos | Bóveda corporativa; nunca RAG ni expediente |

Esto evita convertir pgvector en CMDB o copiar toda la telemetría.

## Puerta de calidad calculada

Al abrir un expediente, el backend evalúa únicamente las referencias visibles
según el clearance del usuario. Informa cobertura de `TELEMETRY`, `CHANGE` y
`RUNBOOK`, número de sistemas, referencias fuera de ventana, timestamps futuros
y una misma referencia con hashes distintos. Un conflicto se expone mediante el
hash de su clave canónica, sin revelar contenido adicional.

`SUFFICIENT_FOR_HUMAN_REVIEW` exige los tres tipos, tres sistemas distintos y
ausencia de fechas futuras o conflictos de versión. No confirma causalidad ni
autoriza M2/M3. La ficha diferencial está en
`docs/differentiation/EVIDENCE_QUALITY_GATE.md` y continúa `NO_VALIDADA` en mercado.

Rollback: retirar el cálculo y bloque visual. No requiere migración ni elimina
evidencia, expedientes o auditoría porque el resultado se calcula al consultar.

## Referencias Jira resueltas

Un administrador puede confirmar una consulta de sólo lectura sobre la Skill
Jira activa. Flentio genera JQL con proyecto, `statusCategory = Done` y la ventana
del expediente; solicita como máximo 25 issues y sólo estado, tipo, actualización,
fecha y presencia de resolución. Cada resultado se adjunta como referencia ITSM
HTTPS. No se copia texto libre ni se considera una resolución confirmada para
memoria operacional. La ruta es
`POST /api/admin/operational-investigations/{id}/collect-jira`.

Rollback: desactivar Jira impide consultas nuevas. Las referencias ya auditadas
se conservan según retención y pueden revisarse sin acceso al secreto.

## Motor de análisis

El análisis debe ejecutar fases verificables:

1. **Normalización:** validar fuente, servicio, entorno, tiempo y deduplicación.
2. **Confirmación:** comprobar que la anomalía existe mediante señales
   independientes; distinguir fallo de sonda, ausencia de datos y fallo real.
3. **Contexto:** resolver topología, proceso bancario, owner y criticidad.
4. **Cambios:** recuperar siete días y puntuar correlación sin atribuir causa.
5. **Precedentes:** recuperar incidentes comparables con resolución validada.
6. **Seguridad:** correlacionar advisories, CISA KEV y futuras fuentes
   estructuradas con inventario/SBOM; sin coincidencia local permanecer en
   `NO_EVALUADO`.
7. **Documentación:** consultar RAG con filtros por aplicación, entorno, versión
   y vigencia; rechazar citas inválidas.
8. **Hipótesis:** enumerar evidencia a favor, en contra y faltante.
9. **Acciones:** ordenar opciones por evidencia, riesgo y reversibilidad.
10. **Abstención:** si falta evidencia, solicitar la comprobación exacta o
   escalar; nunca completar huecos con el modelo.

## Contrato de salida

Cada línea de acción debe contener:

```json
{
  "title": "descripción legible",
  "mode": "SUGGEST",
  "hypothesisId": "referencia",
  "confidence": 0.0,
  "evidenceRefs": [],
  "contradictions": [],
  "requiredChecks": [],
  "expectedOutcome": "señal medible",
  "riskLevel": "R0",
  "blastRadius": "alcance conocido",
  "requiredRole": "rol autorizado",
  "runbookVersion": "versión citada",
  "rollback": "procedimiento o NO_DISPONIBLE",
  "executionStatus": "NOT_EXECUTED"
}
```

La confianza no puede proceder sólo del LLM: debe calcularse a partir de
cobertura, calidad, actualidad y concordancia de las evidencias. La interfaz
mostrará siempre contradicciones y datos faltantes.

El contrato backend `actionRecommendationContract` ya aplica esta frontera:
recalcula la confianza con cobertura/diversidad/apoyos/contradicciones, rechaza
citas que no pertenezcan al expediente y sólo admite `mode=SUGGEST` con
`executionStatus=NOT_EXECUTED`. R1/R2 requieren rollback disponible. El servicio
`operationalRecommendationGeneratorService` recupera evidencia RAG autorizada,
invoca exclusivamente una Skill Ollama configurada, probada y activa, valida el
JSON estricto y sus citas y persiste la propuesta con referencias RAG durables.
Se abstiene antes del modelo si la evidencia operacional es insuficiente y
después del RAG si no existen fragmentos autorizados. No ejecuta acciones.

Rollback: retirar el consumidor del contrato. No hay migración ni ejecución que
revertir; cualquier recomendación futura deberá conservarse por auditoría.

La migración `017_operational_recommendations.sql` persiste hipótesis y
recomendaciones por tenant con RLS. Crear una propuesta exige que la puerta de
evidencia sea suficiente; queda `PENDING`. Un administrador puede aprobar o
rechazar una única vez con motivo obligatorio. `APPROVED` sólo significa revisión
favorable: continúa `NOT_EXECUTED` y no existe ruta de ejecución. API:
`GET|POST /api/admin/operational-investigations/{id}/recommendations`,
`POST /api/admin/operational-investigations/{id}/recommendations/generate` y
`POST /api/admin/operational-recommendations/{id}/review`.

HelixGPT/Knowledge se incorpora mediante el contrato federado, que exige
decisión de política, coincidencia de consulta/fuente, permisos, vigencia,
versión, hash y cita resoluble. El runtime específico continúa
`NO_CONFIGURADO`: no se afirma conexión hasta recibir del cliente edición,
endpoint oficial, autenticación, alcance y una prueba real. Mientras tanto el
generador sólo consume el RAG local autorizado; no simula respuestas HelixGPT.

El frontend restringido del expediente incluye una sección **Líneas de acción
M2**. Sólo habilita la generación cuando la puerta de evidencia resulta
`SUFFICIENT_FOR_HUMAN_REVIEW`; antes de invocar RAG/Ollama exige reconfirmación
y recuerda que la propuesta se audita sin ejecutarse. Cada tarjeta separa
hipótesis, acción, riesgo, confianza calculada, runbook, checks, rollback,
contradicciones y citas RAG. Aprobar o rechazar exige motivo y una segunda
reconfirmación irreversible; el botón dice explícitamente «Aprobar sin
ejecutar». Las cargas independientes de expediente y propuestas se realizan en
paralelo.

QA visual real: build Vite y lint sin errores, panel autenticado comprobado en
1440×900 y 390×844, sin errores de consola. Se usó un tenant QA efímero con un
expediente y referencias reales de la API local; la cuenta quedó deshabilitada
y la evidencia aislada se conserva para auditoría. Capturas:
`output/playwright/m2-investigation-desktop.png` y
`output/playwright/m2-investigation-mobile.png`.

La homologación se gobierna mediante `docs/M2_BANKING_HOMOLOGATION.md`. Un
paquete que supera umbrales sólo llega a `READY_FOR_INDEPENDENT_REVIEW`; el
autor no puede homologarlo. Sin dataset del cliente y segunda identidad revisora
el estado visible permanece `NO HOMOLOGADA`.

Rollback: deshabilitar la ruta de generación y la Skill Ollama sin borrar
registros revisados ni revertir destructivamente la migración. Las propuestas
ya persistidas conservan su evidencia para auditoría.

## Ejemplo de líneas de acción

Ante aumento de errores tras un despliegue reciente:

1. **R0 — confirmar:** comparar tasa de error por versión y revisar trazas de la
   dependencia señalada; no produce cambios.
2. **R0 — aislar:** ejecutar prueba sintética autorizada desde otra ubicación
   para distinguir sonda de servicio.
3. **R1/R2 — sugerir rollback:** sólo si el artefacto anterior, runbook, ventana,
   aprobación y condición de reversión están disponibles.
4. **Escalar:** si el precedente histórico contradice la telemetría actual o el
   runbook está caducado.

No se generará un comando improvisado. Una futura ejecución utilizará una
acción tipada y versionada del catálogo de automatización.

## Modelo de datos mínimo futuro

- `operational_alerts`: alerta normalizada e idempotencia;
- `incident_investigations`: estado, ventana y resultado;
- `investigation_evidence`: referencias tipadas, hash y tiempo;
- `application_services`: catálogo mínimo y owner;
- `service_dependencies`: relaciones versionadas;
- `change_events`: cambio efectivo, actor y rollback;
- `incident_cases`: causa/resolución validadas;
- `action_recommendations`: hipótesis, riesgo y autorización;
- `action_executions`: sólo cuando exista motor real y aprobación.

Todas requerirán `organization_id`, RLS, retención, auditoría y separación entre
datos operativos y contenido RAG.

### Implementación disponible

La migración `015_operational_investigations.sql` crea las tres primeras tablas:
`operational_alerts`, `incident_investigations` e `investigation_evidence`. La
clave `(organization_id, source, external_alert_id)` actualiza una alerta ya
conocida en lugar de duplicarla. Cada referencia de evidencia conserva tipo,
sistema, identificador externo, URI HTTPS, timestamp, clasificación, atributos
acotados y hash; no guarda el documento, log, métrica o secreto original.

API administrativa real, protegida con rol `admin`:

- `POST /api/admin/operational-investigations/alerts` normaliza o actualiza una
  alerta y abre su expediente con ventana inicial de siete días;
- `GET /api/admin/operational-investigations` lista expedientes del tenant;
- `GET /api/admin/operational-investigations/:id` devuelve el expediente y sólo
  las referencias visibles para el clearance del usuario;
- `POST /api/admin/operational-investigations/:id/evidence` añade una referencia
  idempotente y recalcula cobertura.
- `GET /api/admin/grafana-webhook-channel` muestra el estado sin revelar token;
- `POST /api/admin/grafana-webhook-channel/rotate` crea o rota el canal y muestra
  el nuevo token una sola vez;
- `POST /api/admin/grafana-webhook-channel/disable` revoca la recepción.

El estado `READY_REVIEW` exige como mínimo referencias `TELEMETRY`, `CHANGE` y
`RUNBOOK`. Sólo significa cobertura mínima para revisión humana: no confirma
causa, vigencia, concordancia ni corrección de una acción. Mientras falte un tipo,
el estado es `EVIDENCIA_INSUFICIENTE` y se enumeran los tipos ausentes.

## Fases de entrega

### M0 — contrato y dataset

- aprobar fuentes, taxonomía y esquema;
- seleccionar una aplicación de preproducción;
- recopilar incidentes anonimizados y runbooks reales;
- definir métricas y criterio de descarte.

Estado técnico: esquema, normalizadores, RLS, idempotencia y API implementados.
Dataset bancario y evaluación humana continúan `DEPENDENCIA_CLIENTE`.

### M1 — observar

- webhook Grafana real;
- expediente, deduplicación y timeline;
- consultas de sólo lectura a cambios, ITSM, catálogo y RAG;
- hipótesis con citas; ninguna acción ejecutable.

Estado técnico: expediente, referencias, webhook Grafana con HMAC/anti-replay,
Prometheus, Jira y recogida Helix ITSM implementados. Los perfiles del cliente,
mTLS/gateway Grafana, conectores de cambio/CMDB y HelixGPT/RAG permanecen
pendientes o `NO_CONFIGURADO` según corresponda.

### M2 — sugerir

- líneas de acción tipadas;
- riesgo, prechecks, owner, aprobación y rollback;
- evaluación retrospectiva y game days.

### M3 — ejecutar R1

- una única acción reversible y preautorizada en preproducción;
- credencial efímera de mínimo privilegio;
- verificación independiente y rollback probado;
- autorización conjunta de Operaciones, Seguridad y Riesgo.

Estado técnico: la migración 020, el contrato, la API y el frontend registran
únicamente la preparación y las tres decisiones segregadas. El estado permanece
`BLOCKED_NO_EXECUTION`; no existe endpoint ni adaptador de ejecución. Véase
`docs/M3_PREPROD_READINESS.md`.

## Puertas de aceptación M1

- cero alertas perdidas o duplicadas en pruebas de replay;
- RLS entre organizaciones verificada;
- toda hipótesis enlazada a evidencia real;
- toda afirmación documental con cita válida;
- cambios mostrados como correlación, no causalidad automática;
- abstención ante servicio desconocido, RAG insuficiente o fuentes caídas;
- ningún comando, script o cambio de infraestructura generado o ejecutado;
- trazabilidad completa del expediente;
- evaluación humana sobre incidentes conocidos antes de piloto vivo.

## Configuración futura, no operativa

Los nombres siguientes reservan el contrato y **no deben añadirse al `.env`
hasta existir adaptadores reales y homologados**:

- origen y secreto de webhook Grafana;
- conectores de cambios/CI-CD;
- conector ITSM;
- catálogo/CMDB;
- ventana temporal máxima;
- límites de evidencia y confianza;
- motor de automatización y bóveda.

La selección de SIEM, plataforma de observabilidad o automatización requiere
autorización humana.

## Rollback del cambio actual

Deshabilitar primero las rutas administrativas y detener cualquier futura
ingesta. Exportar referencias si existe obligación de conservación. Las tablas
de la migración 015 no se eliminan automáticamente porque contienen trazabilidad
tenant; su retirada requiere cambio aprobado, retención cumplida y backup. No
debe restaurarse la implementación simulada de Auto-SRE.
