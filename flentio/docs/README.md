# Biblioteca de documentación Flentio

> Punto de entrada por perfil. Las guías describen únicamente capacidades, evidencias y límites documentados; los documentos de auditoría conservan la evidencia histórica.

La aplicación publica este corpus en el portal web `/docs`, con búsqueda por
contenido, navegación por audiencia y respuestas extractivas que enlazan siempre
las fuentes. El portal no llama a un modelo ni inventa información cuando no
encuentra evidencia suficiente.

## Elige tu perfil

| Perfil | Documento inicial | Complemento principal |
|---|---|---|
| Usuario | [Guía de usuario básica](users/GUIA_USUARIO_BASICA.md) | [Automatización No-Code](users/GUIA_AUTOMATIZACION_NOCODE.md) |
| Gestor | [Guía para gestores](managers/GUIA_GESTOR.md) | [Gobierno de flujos](managers/GUIA_GOBIERNO_FLUJOS.md) |
| Operador | [Manual de operaciones](operators/ENTERPRISE_OPERATIONS_MANUAL.md) | [Salud de infraestructura](admins/PLATFORM_INFRASTRUCTURE_HEALTH.md) |
| Administrador | [Administración de integraciones](admins/ADMIN_EXTERNAL_INTEGRATIONS.md) | [Homologación bancaria](M2_BANKING_HOMOLOGATION.md) |
| Arquitecto | [Presentación y alcance](architects/PRESENTACION_Y_ALCANCE.md) | [Arquitectura de integraciones](architects/INTEGRATION_SKILLS_ARCHITECTURE.md) |
| Desarrollador | [Continuidad de desarrollo](developers/DEVELOPER_HANDOVER.md) | [Guía de contribución](developers/CONTRIBUTING.md) |
| Ventas | [Propuesta de valor](sales/DECK_PROPUESTA_VALOR.md) | [Análisis competitivo](sales/COMPETITIVE_ANALYSIS.md) |
| Dirección | [Resumen ejecutivo](leadership/EXECUTIVE_SUMMARY.md) | [Registro de riesgos](leadership/RISK_REGISTER.md) |

## Seguridad y capacidad

- [Guía integral de seguridad y cumplimiento](SECURITY_AND_COMPLIANCE_GUIDE.md)
  — explicación completa para clientes, seguridad, privacidad, IA, marcos de
  cumplimiento, responsabilidades, brechas y checklist de homologación.
- [Seguridad de Flentio](SECURITY.md) — modelo de confianza, controles reales,
  configuración mínima y bloqueos de producción conocidos.
- [Capacidad, carga y escalado](architects/CAPACIDAD_CARGA_USUARIOS_Y_PROCESOS.md)
  — límites configurados, estado de validación y método de benchmark.
- [Última revisión integral de documentación](audits/DOCUMENTATION_REVIEW_2026-09-05.md)
- [Revisión de símbolos indefinidos del frontend](audits/FRONTEND_UNDEFINED_SYMBOLS_2026-09-07.md)
- [Decisión de autenticación OpenAI](audits/OPENAI_AUTHENTICATION_2026-09-07.md)
- [Implementación OAuth de Gemini](audits/GEMINI_OAUTH_2026-09-07.md)
  — alcance, hallazgos y trabajo pendiente.
- [Evidencia del portal documental](audits/DOCUMENTATION_PORTAL_2026-09-05.md)
  — alcance web, validación visual, privacidad, límites y rollback.

## Referencia técnica compartida

- [Catálogo de Flujos de Demostración](presentation/DEMO_FLOWS.md) — catálogo con los 20 flujos avanzados para presentaciones de la plataforma.
- [Flujos de la presentación pública](users/FLUJOS_PRESENTACION_FLENTIO.md) — plantillas no-code de facturas, normativa y alertas, con dependencias explícitas.
- [Operación técnica del RAG](developers/RAG_OPERATIONS.md) — ingesta, recuperación, conectores y límites.
- [Investigación operacional gobernada](developers/GOVERNED_INCIDENT_INVESTIGATION.md) — evidencias, propuestas y aprobación humana.
- [Integración Sidecar de Gobierno](architects/SIDECAR_GOVERNANCE_INTEGRATION.md) — especificación para integrar Flentio como middleware en plataformas bancarias internas.
- [Contrato de interoperabilidad gobernada](architects/GOVERNED_INTEROPERABILITY_CONTRACT.md) — especificación de eventos, aprobación y compensación; no implementada.
- [Kit de extensión de adaptadores](developers/INTEGRATION_ADAPTER_SDK.md) — guía pro-code para futuras Skills; no es un SDK instalable.
- [Seguridad de ingesta RAG](RAG_SECURITY_INGESTION.md) — cuarentena, análisis de malware y control de acceso.
- [Estándar de cuadros de mando](DASHBOARD_STANDARD.md) — contrato de estados y métricas para los paneles.
- [ADRs](adr/) — decisiones técnicas versionadas.

## Estrategia, evidencia y plantillas

- [Estrategia y mercado](strategy/) — hipótesis, investigación y posicionamiento; no sustituye validación con clientes.
- [Auditorías y evidencias](audits/) — resultados fechados y alcance de las comprobaciones ejecutadas.
- [Plantillas](templates/) — intake, aceptación, runbooks y registros reutilizables.
- [Especificación de adaptador](templates/INTEGRATION_ADAPTER_SPEC.md) — plantilla de contrato, gobierno y validación de una integración.

## Estados de la documentación

| Estado | Significado |
|---|---|
| `OPERATIVO` | Verificado con la comprobación descrita. |
| `NO_CONFIGURADO` | Requiere configuración o credenciales autorizadas. |
| `NO_DISPONIBLE` | La comprobación falló o el servicio no respondió. |
| `NO_VALIDADA` | Hipótesis pendiente de evidencia suficiente. |
| `NO_VALIDADO` | Variante masculina del mismo estado; no ha superado la evidencia requerida. |
| `DEPENDENCIA_CLIENTE` | Requiere datos, infraestructura o autorización del cliente. |
| `NO_BANCARIO` | Escenario o dato sintético; no es evidencia productiva. |

Actualiza la guía afectada y, si aplica, su evidencia técnica en el mismo cambio funcional. Consulta [la guía de contribución](developers/CONTRIBUTING.md) antes de modificar código o documentación.
