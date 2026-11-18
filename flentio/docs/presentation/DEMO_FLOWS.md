# Catálogo de Flujos de Demostración (Presentación)

Este documento detalla los 20 flujos de trabajo (workflows) integrados en las plantillas semilla (`seed-templates.js`) de Flentio. Estos flujos han sido diseñados específicamente para presentaciones comerciales y demostraciones técnicas, ilustrando el potencial de Flentio en diversos sectores e integraciones complejas.

## 1. Atención al Cliente
- **Zendesk: Soporte IA (`pres_1_customer_support`)**
  - **Descripción:** Clasifica tickets de Zendesk automáticamente con IA y redacta auto-respuesta inicial.
  - **Nodos:** Webhook (Zendesk) -> Agente IA Ollama -> Petición HTTP (Zendesk Update).
- **Soporte: Intercom L1 RAG (`pres_11_support_rag`)**
  - **Descripción:** Responde chats usando base de conocimiento. Si no sabe, deriva a humano con resumen.
  - **Nodos:** Webhook (Intercom) -> Agente IA RAG -> Petición HTTP (Intercom).

## 2. Recursos Humanos
- **HR: Auto-Onboarding Empleados (`pres_2_hr_onboarding`)**
  - **Descripción:** Crea cuenta en Google Workspace y lanza flujo de bienvenida en Slack al añadir empleado en Workday.
  - **Nodos:** Webhook (Workday) -> Petición HTTP (Google Workspace) -> Slack Message.
- **HR: Análisis Clínico de Clima (`pres_10_hr_feedback`)**
  - **Descripción:** Pide feedback mensual (Typeform) e IA resume inquietudes clave hacia un dashboard.
  - **Nodos:** Cron Trigger -> Petición HTTP (Typeform) -> Agente IA (Resumen).

## 3. Ciberseguridad y SecOps
- **SecOps: Bloqueo de Amenazas IAM (`pres_3_secops_iam`)**
  - **Descripción:** Analiza logins inusuales en AWS y bloquea cuenta preventiva alertando por PagerDuty.
  - **Nodos:** Webhook (AWS CloudTrail) -> Petición HTTP (Bloqueo IAM) -> Petición HTTP (PagerDuty).
- **SecOps: Respuesta a Phishing (`pres_17_secops_phishing`)**
  - **Descripción:** Analiza adjunto de correo reportado y si hay malware, lo purga de todas las bandejas.
  - **Nodos:** Webhook (Exchange) -> Petición HTTP (VirusTotal) -> Petición HTTP (Exchange Purge).

## 4. Ventas y CRM
- **Ventas: Enriquecimiento Leads (`pres_4_sales_enrichment`)**
  - **Descripción:** Enriquece datos de nuevos contactos con Clearbit y los sincroniza automáticamente con Salesforce.
  - **Nodos:** Webhook (Formulario) -> Petición HTTP (Clearbit) -> Petición HTTP (Salesforce).
- **Retención: Oferta Churn Rescue (`pres_19_churn_rescue`)**
  - **Descripción:** Detecta cancelación en Stripe, IA analiza uso previo y envía email de retención con descuento.
  - **Nodos:** Webhook (Stripe) -> Agente IA (Generador Oferta) -> Send Gmail.

## 5. Marketing y Eventos
- **Marketing: Análisis Sentimiento (`pres_5_mktg_sentiment`)**
  - **Descripción:** Monitorea Twitter/X y usa IA para detectar quejas, abriendo ticket prioritario en HubSpot.
  - **Nodos:** Cron Trigger -> Agente IA (Sentimiento) -> Petición HTTP (HubSpot).
- **Eventos: Seguimiento Hyper-Personal (`pres_13_events_leads`)**
  - **Descripción:** Capta asistentes en Airtable e IA envía email único basándose en su industria/cargo (LinkedIn).
  - **Nodos:** Webhook (Airtable) -> Agente IA (Redactor) -> Send Gmail.

## 6. Finanzas y Banca
- **Finanzas: OCR Facturas a ERP (`pres_6_fin_invoices`)**
  - **Descripción:** Recibe facturas PDF por email, extrae datos por OCR (IA) e inserta entrada contable en SAP.
  - **Nodos:** Webhook (Email) -> Agente IA (OCR Extract) -> Petición HTTP (SAP).
- **Banca: Prevención de Fraude AML (`pres_12_bank_aml`)**
  - **Descripción:** Valida transferencias SWIFT sospechosas contra bases AML y bloquea si el riesgo es Alto.
  - **Nodos:** Webhook (SWIFT) -> Petición HTTP (AML API) -> Petición HTTP (Bloqueo Core Bancario).

## 7. Operaciones y Logística
- **Logística: Auto-Etiquetas (`pres_7_ecom_shipping`)**
  - **Descripción:** Detecta pago en Shopify, genera etiqueta en ShipStation y notifica al cliente por SMS.
  - **Nodos:** Webhook (Shopify) -> Petición HTTP (ShipStation) -> Petición HTTP (Twilio SMS).
- **IoT: Mantenimiento Predictivo (`pres_14_iot_predictive`)**
  - **Descripción:** Lectura anómala de sensor en InfluxDB dispara orden urgente de revisión en Jira Service Desk.
  - **Nodos:** Webhook (IoT) -> Petición HTTP (Jira Service Desk).
- **Ops: Alerta Clima Multi-Canal (`pres_18_ops_critical`)**
  - **Descripción:** Cruza alertas gubernamentales con oficinas en riesgo y envía SMS/WhatsApp a empleados locales.
  - **Nodos:** Webhook (API Clima) -> Petición HTTP (SMS) -> Petición HTTP (WhatsApp Business).

## 8. Ingeniería y DevOps
- **DevOps: Resolución IA Pipelines (`pres_8_devops_autofix`)**
  - **Descripción:** Captura logs de pipelines fallidos (GitLab) e IA sugiere parche enviándolo al canal de Slack.
  - **Nodos:** Webhook (GitLab) -> Agente IA (Diagnóstico) -> Slack Message.
- **Data: ETL Legacy a Snowflake (`pres_15_data_etl`)**
  - **Descripción:** Extracción diaria de base legacy MySQL, transformación en memoria y carga en Snowflake.
  - **Nodos:** Cron Trigger -> Petición HTTP (MySQL API) -> Petición HTTP (Snowflake API).
- **DevSecOps: Revisión PR GitHub (`pres_20_dev_security`)**
  - **Descripción:** Analiza Pull Request en GitHub buscando vulnerabilidades OWASP top 10 con un agente IA.
  - **Nodos:** Webhook (GitHub) -> Agente IA (SAST) -> Petición HTTP (GitHub Comment).

## 9. Reportes y Legal
- **Ejecutivos: Reporte Semanal (`pres_9_exec_reporting`)**
  - **Descripción:** Consolida métricas de Stripe y Mixpanel cada viernes a las 17:00, generando PDF para el Board.
  - **Nodos:** Cron Trigger -> Petición HTTP (Stripe/Mixpanel) -> Generador PDF.
- **Legal: Auditoría IA de Contratos (`pres_16_legal_risk`)**
  - **Descripción:** Sube documento a Drive e IA alerta por Teams si detecta cláusulas asimétricas de riesgo.
  - **Nodos:** Webhook (Google Drive) -> Agente IA (Analista Legal) -> Petición HTTP (MS Teams).

---
> **Nota Operativa:** Estos flujos están disponibles al ejecutar `node backend/seed-templates.js` en una instancia nueva o existente de la plataforma. Ninguno de estos flujos contiene credenciales en duro; requieren ser configurados desde la bóveda de credenciales mediante el UI no-code por el operador final (ver *Reglas de Proyecto*).
