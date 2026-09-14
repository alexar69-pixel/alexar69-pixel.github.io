# Presentación y Definición del Proyecto: Flentio Platform

## 1. Visión General del Proyecto
**Flentio Platform** es una plataforma de orquestación visual "No-Code", automatización avanzada, investigación operacional y Retrieval-Augmented Generation (RAG) empresarial, diseñada específicamente para entornos bancarios e infraestructuras críticas. Su propósito principal es permitir a usuarios sin conocimientos técnicos diseñar, gobernar y auditar procesos automatizados y asistentes de IA conversacional mediante un panel gráfico interactivo.

Flentio se fundamenta en principios estrictos de transparencia, seguridad mediante aislamiento multiempresa (Row-Level Security - RLS) y uso de implementaciones exclusivamente reales, prohibiendo de forma taxativa el uso de simulaciones, mocks o datos prefabricados en operaciones productivas.

## 2. Objetivos Principales
1. **Democratización de la Automatización:** Proveer un entorno visual No-Code para la creación de flujos de trabajo (workflows), integrando servicios externos y modelos de IA generativa.
2. **Conocimiento Empresarial Seguro (RAG):** Construir una base de conocimiento documental indexada, segmentada por roles y organizaciones (RLS), con validación de seguridad antimalware (ClamAV) e inmutabilidad (WORM).
3. **Observabilidad Obligatoria:** Garantizar que toda capacidad funcional cuente con cuadros de mando (dashboards) operativos basados en datos reales para supervisión y auditoría.
4. **Integración Gobernada:** Establecer pasarelas estandarizadas (Client Integration Gateway) para la conexión segura con sistemas corporativos del cliente.

## 3. Arquitectura del Sistema
Flentio separa API y workers sobre PostgreSQL. El compose incluido es una
topología local de nodo único y no acredita resiliencia, HA ni preparación
multicloud; esas topologías requieren diseño y validación del cliente:
* **Frontend:** Single Page Application (SPA) en React.js, construida con HTML5 y Vanilla CSS3, orientada a la experiencia visual No-Code.
* **Backend:** API REST y motor de ejecución en Node.js (Express), procesando la lógica de negocio y conectividad asíncrona.
* **Base de Datos Principal:** PostgreSQL 16 con RLS (aislamiento por organización), gestionando tanto la plataforma (usuarios, flujos, auditorías) como la extensión `pgvector` para búsquedas RAG híbridas.
* **Almacenamiento de Objetos WORM:** MinIO o servicios S3 compatibles para custodia inmutable y cifrada (AES-256-GCM) de los documentos originales.
* **Procesamiento de IA:** Inferencia local mediante TEI (Text Embeddings Inference) para vectorización, e integración flexible con proveedores LLM (OpenAI, Gemini, Ollama) bajo contratos de evidencia estricta.

Los límites configurados y la ausencia de cifras productivas verificadas están
en [Capacidad, carga y escalado](CAPACIDAD_CARGA_USUARIOS_Y_PROCESOS.md). Los
bloqueos actuales se mantienen en [Seguridad](../SECURITY.md).

## 4. Alcance Funcional (En Alcance)
El desarrollo y operación del proyecto abarca las siguientes áreas principales:

### A. Motor de Orquestación Visual (No-Code)
* Creación de grafos lógicos para conectar entradas/salidas (Correo, Slack, Webhooks, Bases de Datos).
* Ejecución asíncrona mediante un sistema de workers durables en PostgreSQL.
* Capacidad de suspensión, reanudación y cancelación cooperativa de tareas y automatizaciones.

### B. Sistema RAG Empresarial Trazable
* **Ingesta Segura:** Análisis por streaming con motores de seguridad, cuarentena y aprobación segregada.
* **Autorización Estricta:** Control de acceso granular (tenant, clearance, ACL) previo a la recuperación de información confidencial.
* **Trazabilidad Verificable:** Custodia cifrada del original y preservación exhaustiva del ciclo de vida de cada fragmento entregado a la IA.
* **Conectores Incrementales:** Sincronización continua con orígenes documentales (ej. Google Drive) para mantener la vigencia de datos.

### C. Client Integration Gateway
* Estandarización de integraciones con ecosistemas del cliente (EDR, SIEM, Vault) validando identidad, ámbito y capacidades sin exponer lógica interna de las credenciales, exigiendo respuestas válidas y operativas.

### D. Gobernanza y Observabilidad
* Auditoría inmutable de accesos, aprobaciones y transacciones críticas.
* Módulos administrativos de salud de infraestructura, con alertas y runbooks asociados.
* Incorporación de metodologías de optimización como Prompt Caching para modelos compatibles.

## 5. Fuera de Alcance y Limitaciones Conocidas
* **Simulaciones Funcionales:** Está estrictamente prohibido simular integraciones exitosas. Si falta una credencial o conexión real, el sistema debe reportar un estado explícito de `NO_CONFIGURADO` o `NO_DISPONIBLE`.
* **Reconocimiento Óptico de Caracteres (OCR):** Queda formalmente excluido del alcance del sistema actual de ingesta de documentos.
* **Aprovisionamiento Externo del Cliente:** Elementos como Alta Disponibilidad perimetral (HA/DR final), sistemas SSO corporativos externos y SIEM definitivos se categorizan como `DEPENDENCIA_CLIENTE` y no se asumen resueltos sin el aprovisionamiento real de los mismos.
* **Fidelidad Jurídica Incondicional:** El modelo valida las citas proporcionadas a la IA, pero la responsabilidad técnica no se extiende a confirmar plenamente la interpretación jurídica generada.
* **SDK y Sidecar heredados:** Sus rutas actuales están marcadas como simuladas
  y se consideran `NO_DISPONIBLE` para operación hasta su sustitución y prueba.

## 6. Requisitos Esenciales de Ingeniería
Toda evolución o mantenimiento debe adherirse a los principios de Flentio:
1. **Documentación Continua:** Toda modificación y configuración debe quedar debidamente descrita en los manuales operativos corporativos.
2. **Prioridad No-Code:** Minimizar exposición de lenguajes crudos al usuario; favorecer interfaces visuales de configuración y bóvedas amigables.
3. **Innovación con Valor Diferencial:** Diseñar mejoras orientadas a necesidades operativas específicas y comprobables, asegurando una barrera técnica y operativa sólida que justifique la innovación sobre soluciones genéricas.
