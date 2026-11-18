# Conocimiento RAG de errores, incidentes y alertas de seguridad

## Estado

- **CISA KEV:** plantilla pública real añadida al catálogo de fuentes externas;
  requiere importación, revisión humana, descarga, cuarentena y publicación por
  cada organización. No se ha publicado automáticamente en ningún tenant.
- **Errores e incidentes internos:** `NO_CONFIGURADO`; requieren conectores y
  autorización del cliente.
- **NVD, OSV, GitHub Advisory y avisos de fabricantes:** `NO_CONFIGURADO` como
  conectores estructurados.
- **SIEM/EDR/SOC:** `NO_CONFIGURADO`; la selección de proveedor exige
  autorización humana.

La presencia de una vulnerabilidad en una fuente pública no demuestra que una
aplicación esté afectada. Hasta correlacionar producto, versión efectiva, SBOM,
configuración y exposición, el estado será `NO_EVALUADO`.

## Arquitectura de conocimiento

No toda base de errores debe copiarse íntegramente al vector store. El
conocimiento privado procede de documentación y RAG internos del cliente; la
federación es el modo predeterminado. Contrato:
`docs/RAG_CLIENT_KNOWLEDGE_FEDERATION.md`.

```text
Fuentes públicas                         Fuentes privadas
CISA / NVD / OSV / fabricantes          Grafana / SIEM / ITSM / CI-CD / CMDB
              │                                      │
              ├── normalización y deduplicación ─────┤
              │                                      │
       PostgreSQL estructurado                almacén de origen
       CVE, versión, estado, fechas,          métricas/logs/trazas
       activo, incidente, cambio, relación          │
              │                                      │ referencias
              └──────────────┬───────────────────────┘
                             │
                    RAG documental del cliente o federado
                    advisories, runbooks, postmortems,
                    resoluciones y procedimientos
                             │
                    análisis y líneas de acción
```

### En RAG

- descripción y contexto de advisories;
- acciones requeridas y mitigaciones oficiales;
- boletines de fabricante;
- runbooks internos;
- postmortems aprobados;
- resoluciones documentadas de incidentes;
- procedimientos SOC/SRE vigentes;
- arquitectura y manuales de aplicación autorizados.

Estos contenidos permanecen en los RAG/repositorios del cliente salvo copia
controlada explícitamente autorizada.

### En datos estructurados

- CVE/GHSA/OSV ID y alias;
- proveedor, producto, paquete, ecosistema y versiones afectadas/corregidas;
- CVSS y vector con su versión y fuente;
- pertenencia a KEV, fecha de incorporación y fecha límite;
- withdrawn/rejected/superseded;
- aplicación, componente, SBOM y versión desplegada;
- exposición, reachability y controles compensatorios;
- alerta, incidente, estado, severidad y timestamps;
- cambio, despliegue, owner, aprobación y rollback;
- decisión humana: afectado, no afectado, aceptado o pendiente.

Los filtros exactos y el matching de versiones no se delegan a embeddings ni al
LLM.

## Fuentes previstas

| Fuente | Valor | Integración correcta | Estado |
|---|---|---|---|
| CISA KEV | Vulnerabilidades explotadas en la práctica y acción requerida | Snapshot JSON versionado + registros estructurados | Plantilla RAG disponible; estructurado pendiente |
| NVD | CVE, CVSS, CPE y referencias | API incremental paginada, caché y control de cambios | `NO_CONFIGURADO` |
| OSV | Vulnerabilidades por paquete, versión o commit | Consulta por SBOM/versiones; formato OSV | `NO_CONFIGURADO` |
| GitHub Advisory | Advisories por ecosistema y versiones | REST/GraphQL o dataset OSV según licencia y permisos | `NO_CONFIGURADO` |
| Fabricantes | Fixes, mitigaciones y avisos específicos | Adaptadores allowlist por proveedor | `NO_CONFIGURADO` |
| Grafana/Prometheus/APM | Alertas y evidencia operacional | Webhook + referencias a consultas acotadas | `NO_CONFIGURADO` |
| SIEM/EDR | Detecciones y respuesta de seguridad | Conector gobernado del proveedor autorizado | `NO_CONFIGURADO` |
| Jira | Incidentes, problemas, cambios, causas y soluciones confirmadas | API incremental con contrato canónico, ownership y webhooks autorizados | `AUTORIZADO_NO_CONFIGURADO` |
| BMC Helix ITSM + HelixGPT | Registros estructurados y conocimiento recuperado por el RAG interno de Helix | REST ITSM/CMDB + consulta federada de Knowledge/HelixGPT con citas | `AUTORIZADO_NO_CONFIGURADO` |
| CI/CD y repositorios | Cambios realmente desplegados | Eventos firmados y artefactos/versiones | `NO_CONFIGURADO` |
| CMDB/SBOM | Activos, dependencias y versiones efectivas | Sincronización estructurada y temporal | `NO_CONFIGURADO` |

CISA describe KEV como entrada para priorización de vulnerabilidades, no como
inventario local. [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
NVD ofrece una API de vulnerabilidades; OSV permite consultar por paquete,
versión o commit; GitHub Advisory publica advisories por ecosistema y versiones.
[OSV API](https://google.github.io/osv.dev/api/), [GitHub Advisory Database](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/fix-reported-vulnerabilities/browse-advisory-database)

## Ingesta de errores internos

Un incidente sólo podrá convertirse en memoria RAG de alta confianza del
cliente —o en evidencia federada consultable por Flentio— cuando
incluya:

1. aplicación, servicio, entorno y ventana temporal;
2. síntomas y señales originales referenciadas;
3. cambios relacionados, sin confundir correlación con causalidad;
4. causa confirmada y aprobador;
5. solución aplicada y versión del runbook;
6. verificación técnica y del proceso bancario;
7. rollback, daño lateral y acciones que no funcionaron;
8. datos personales y secretos eliminados;
9. clasificación, owner, vigencia y fecha de revisión.

Los tickets abiertos, duplicados, autocerrados o sin causa confirmada pueden
usarse para búsqueda de precedentes, pero tendrán confianza reducida y no
autorizarán una remediación.

## Correlación de exposición

El resultado para cada advisory será uno de:

| Estado | Significado |
|---|---|
| `NO_EVALUADO` | Existe información externa, sin correlación local |
| `POTENCIALMENTE_AFECTADO` | Coincide producto/versión, faltan configuración o reachability |
| `AFECTADO_CONFIRMADO` | Evidencia técnica y revisión autorizada confirman exposición |
| `NO_AFECTADO_VERIFICADO` | Evidencia reproducible descarta afectación |
| `MITIGADO` | Control o parche aplicado y verificado |
| `RIESGO_ACEPTADO` | Decisión temporal aprobada con vencimiento |

El modelo no puede asignar `AFECTADO_CONFIRMADO`, `MITIGADO` o
`RIESGO_ACEPTADO` por sí solo.

## Uso desde Incident Lab

Al investigar una alerta, Flentio podrá recuperar:

- advisories aplicables a las versiones desplegadas;
- KEV explotadas que eleven la prioridad;
- alertas de seguridad cercanas en tiempo y topología;
- incidentes internos con causa y solución confirmadas;
- runbooks y mitigaciones del fabricante vigentes;
- cambios de siete días que afecten al componente;
- controles compensatorios y decisiones de riesgo no caducadas.

La salida distinguirá siempre:

1. hecho observado;
2. correlación;
3. hipótesis;
4. recomendación;
5. acción autorizada.

## Operación de la plantilla CISA KEV

Un operador RAG puede:

1. abrir **Configuración corporativa → Ingesta RAG / fuentes externas**;
2. importar `cisa:kev:live`;
3. definir clasificación y grupos autorizados;
4. revisar y aprobar la fuente;
5. ejecutar la descarga real;
6. revisar el contenido descargado tras cuarentena;
7. publicar la versión en el RAG.

Cada actualización crea una versión y conserva procedencia. No se activa una
sincronización automática ni se afirma que el contenido afecte al tenant.

## Seguridad

- Sólo HTTPS y host CISA incorporado a la allowlist de backend.
- Límite de descarga de 15 MB, timeout, MIME y contenido validados.
- Original cifrado/versionado y publicación tras revisión humana.
- RLS, clasificación y grupos por organización.
- El contenido externo no contiene instrucciones ejecutables autorizadas.
- Una remediación nunca se genera directamente desde el texto del advisory.

## Próxima fase

1. Normalizador estructurado CISA KEV con claves idempotentes.
2. Inventario/SBOM de una aplicación de preproducción.
3. Correlación sin ejecución y revisión de falsos positivos.
4. Conector ITSM para incidentes resueltos.
5. Conector de cambios desplegados.
6. OSV por versiones del SBOM.
7. NVD/fabricantes sólo si añaden evidencia no duplicada.

No se conectará un SIEM, EDR ni proveedor comercial sin autorización humana.

Jira y BMC Helix sí han sido autorizados como sistemas objetivo. Su contrato y
discovery necesario se documentan en `docs/ITSM_JIRA_HELIX_INTEGRATION.md`; no se
consideran operativos hasta validar una instancia real.

## Rollback

Retirar la plantilla del catálogo impide nuevas importaciones, pero no elimina
fuentes o documentos ya aprobados por un tenant. Éstos se deshabilitan mediante
la API gobernada y se conservan según retención. Para retirar CISA de la
allowlist se elimina `www.cisa.gov` en una versión posterior del backend tras
deshabilitar las fuentes activas.
