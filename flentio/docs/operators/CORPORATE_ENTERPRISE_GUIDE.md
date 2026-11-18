# Guía Operativa para Entornos Corporativos Neutros (Cross-Industry Enterprise)

> **Manual de Operaciones y Gobierno.** Destinado a administradores, directores de operaciones, gestores de compras, responsables de RRHH y equipos de TI corporativos.

---

## 1. Propósito del Entorno Corporativo Neutro

El **Entorno Corporativo Neutro (`CORPORATE_NEUTRAL`)** de Flentio está diseñado para organizaciones empresariales de cualquier sector (manufactura, servicios profesionales, logística, telecomunicaciones, retail, energía, educación y consultoría) que requieren:
- Automatizar tareas repetitivas de oficina y flujos entre departamentos.
- Conectar agentes de inteligencia artificial a sus documentos internos (contratos, políticas, procedimientos, manuales).
- Reducir tiempos operativos sin incurrir en costes de desarrollo de software a medida ni depender de nubes públicas que expongan la confidencialidad de la empresa.
- Cumplir de manera natural con el **Reglamento General de Protección de Datos (RGPD UE 2016/679)** y el **Reglamento Europeo de Inteligencia Artificial (EU AI Act UE 2024/1689)**.

A diferencia del entorno bancario (que impone dobles aprobaciones forzadas de 4 ojos) o del entorno médico (que exige auto-desconexión en 15 minutos y firmas clínicas FDA), el entorno corporativo proporciona una **operativa ágil, directa y eficiente**, manteniendo intacto el aislamiento estricto de datos.

---

## 2. Casos de Uso y Procesos Departamentados

### 2.1. Compras y Cuentas a Pagar (Procure-to-Pay)
- **Flujo:** Recepción automática de facturas en PDF por correo o repositorio documental, extracción de metadatos mediante OCR/LLM privado, cotejo con la orden de compra y registro en el sistema contable o ERP.
- **Intervención Humana:** El gestor de compras solo debe revisar y autorizar aquellas facturas con discrepancias de importe o proveedores no habituales.
- **Ahorro típico:** Reducción del 70% en el tiempo de contabilización y eliminación de duplicidades.

### 2.2. Recursos Humanos (Talento y Personas)
- **Onboarding de Empleados:** Creación automática de cuentas, asignación de equipamiento en ServiceNow/Jira, recopilación de documentación contractual y envío de guías de bienvenida.
- **Asistente Interno del Empleado (RAG Corporativo):** Agente de IA que responde consultas sobre convenios laborales, política de vacaciones, beneficios sociales y procedimientos internos, citando siempre el párrafo exacto del manual corporativo.

### 2.3. Gestión Legal y Contratos
- **Revisión Preliminar de Acuerdos:** Análisis comparativo de contratos de proveedores frente a las cláusulas estándar de la compañía.
- **Alertas de Caducidad y Renovación:** Notificación proactiva a los responsables antes de la renovación tácita de contratos de suministros o licencias de software.

### 2.4. Soporte Técnico de TI (Service Desk)
- **Triaje y Resolución de Incidencias:** Clasificación de tickets entrantes, propuesta de solución basada en la base de conocimiento interna y ejecución supervisada de diagnósticos de red o reseteo seguro de permisos.

---

## 3. Configuración del Perfil Corporativo

### 3.1. Activación en el Sistema
En el archivo de configuración del entorno (`.env`):
```bash
APP_EDITION=corporate
DEFAULT_GOVERNANCE_PROFILE=CORPORATE_NEUTRAL
VITE_APP_EDITION=corporate
```

### 3.2. Parámetros Operativos Efectivos
Cuando una organización opera bajo el perfil `CORPORATE_NEUTRAL`:
- **Supervisión Humana (HITL):** Aprobación simple de 1 operador para tareas que impliquen cambios en sistemas externos (sin necesidad de doble firma colegiada).
- **Filtro DLP Transversal:** Redacción automática de DNIs, correos personales, números de teléfono, tarjetas de crédito y credenciales de acceso antes de enviar datos al modelo de IA.
- **Retención WORM de Auditoría:** 30 días de custodia inmutable de logs en disco o PostgreSQL (ampliable según los requisitos de auditoría interna de la empresa).
- **Tiempo de Inactividad de Sesión:** 60 minutos antes de solicitar reautenticación.
- **Aislamiento Multi-Tenant (RLS):** Garantizado a nivel de base de datos PostgreSQL; ninguna empresa u organización puede acceder a los flujos ni documentos de otra.

---

## 4. Conexión de Aplicaciones Empresariales (Bóveda Segura)

El entorno corporativo neutro cuenta con un catálogo de integración directa para la infraestructura típica de una corporación moderna:

1. **Gestión de Servicios y TI:**
   - *ServiceNow:* Integración para lectura de inventario de CMDB y creación de cambios.
   - *Jira Software / Jira Service Management:* Sincronización bidireccional de incidencias.
2. **Comunicación y Notificaciones:**
   - *Slack & Microsoft Teams:* Envío de alertas contextuales con botones interactivos de aprobación para directivos.
3. **Almacenamiento y Documentación:**
   - *Microsoft SharePoint / OneDrive:* Ingesta de carpetas de contratos o manuales para consulta semántica.
   - *Google Drive / Google Workspace:* Ingesta de procedimientos operativos.
4. **Bases de Datos Corporativas:**
   - Conexión segura a PostgreSQL, MySQL, Microsoft SQL Server u Oracle con consultas parametrizadas de sólo lectura y salvaguarda AST contra sentencias `DROP` o `DELETE` accidentales.

---

## 5. Cuadros de Mando y Supervisión para Directivos

Los operadores y directores de negocio cuentan con cuadros de mando visuales específicos en el panel corporativo:
- **Consumo de Modelos de IA (`ai_usage`):** Monitorización de tokens consumidos, porcentaje de acierto de Prompt Caching y costes derivados por departamento.
- **Historial de Ejecuciones de Flujos:** Visibilidad en tiempo real de flujos completados, tiempos de ejecución y tareas pendientes de aprobación humana.
- **Estado de Certificados y Salud de Integraciones:** Alertas tempranas ante tokens expirados o servicios externos caídos.
