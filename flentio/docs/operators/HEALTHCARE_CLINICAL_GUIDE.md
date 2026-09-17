# Guía Operativa de Flentio Medical: Salud, Ensayos Clínicos y Farmacia

> **Manual de Operaciones y Validación Regulatoria.** Destinado a investigadores principales, directores médicos, coordinadores de ensayos clínicos, comités de ética, auditores de calidad y administradores hospitalarios.

---

## 1. Misión de Flentio Medical

**Flentio Medical (`HEALTHCARE_CLINICAL`)** es la edición especializada de la plataforma Flentio destinada al sector de las **Ciencias de la Salud, la Investigación Clínica y la Industria Farmacéutica**. 

Su propósito es acelerar los ciclos de investigación, optimizar el reclutamiento en ensayos clínicos y asegurar la farmacovigilancia continua, bajo el más riguroso cumplimiento de las normativas internacionales de protección de datos sanitarios y validación de sistemas computarizados:
- **HIPAA Security & Privacy Rules (EE. UU.)**
- **FDA 21 CFR Part 11 (Registros y Firmas Electrónicas)**
- **Reglamento General de Protección de Datos (RGPD UE 2016/679, Artículo 9 - Datos de Salud)**
- **Buenas Prácticas Clínicas (GCP - ICH E6 R2) y de Laboratorio (GLP)**

---

## 2. Salvaguardas y Requisitos Técnicos Mandatorios

Al operar bajo el perfil `HEALTHCARE_CLINICAL`, la plataforma impone automáticamente salvaguardas estrictas que no pueden ser desactivadas:

### 2.1. Desidentificación Automática de PHI (HIPAA Safe Harbor)
Antes de que cualquier texto, historial clínico o nota de laboratorio sea procesado por un modelo de inteligencia artificial o indexado en el RAG, el motor de Data Loss Prevention (`dlp.js`) redacta los **18 identificadores protegidos por la norma HIPAA**:
- Nombres de pacientes y facultativos.
- Todas las subdivisiones geográficas inferiores a un estado (ciudades, códigos postales, direcciones).
- Fechas exactas de nacimiento, admisión hospitalaria, alta o defunción (conservando únicamente intervalos de edad válidos para criterios de inclusión clínica).
- Números de teléfono, fax y direcciones de correo electrónico.
- Números de Seguro Social (SSN), DNI, NIE o pasaporte.
- Números de historia clínica (MRN) y de cuentas médicas.
- Números de póliza de seguro médico.
- Números de serie de dispositivos médicos o implantes.
- URLs, direcciones IP y rasgos biométricos.

### 2.2. Cumplimiento con FDA 21 CFR Part 11
- **Pistas de Auditoría Inmutables (Audit Trails):** Todo evento (creación de registro, edición de protocolo, importación de datos clínicos, validación de criterios) queda sellado criptográficamente con hash SHA-256 en registros WORM (Write Once, Read Many).
- **Firma Electrónica Avanzada:** Toda decisión de aceptación de paciente o reporte de evento adverso exige:
  1. Identificación unívoca del firmante (Nombre, Rol y Organización).
  2. Manifestación expresa del motivo de la firma (*«Aprobación de inclusión»*, *«Notificación de farmacovigilancia»*, *«Cierre de lote de laboratorio»*).
  3. Timestamp UTC fehaciente no modificable.
- **Retención Prolongada de Auditoría:** Mínimo de **2.555 días (7 años)** de persistencia obligatoria para coincidir con los periodos de inspección regulatoria de la FDA y la Agencia Europea de Medicamentos (EMA).
- **Visor de Auditoría Forense:** Interfaz visual accesible en `/audit` (`CFR21AuditViewer.jsx`) para que auditores externos e inspectores puedan verificar la integridad de las firmas sin exponer código ni bases de datos.

### 2.3. Cierre de Sesión Automático por Inactividad (Auto-Logoff)
Para prevenir el acceso no autorizado a terminales desatendidos en puestos de enfermería o laboratorios, el cliente web (`App.jsx`) monitoriza continuamente la actividad del usuario (ratón, teclado, toques en pantalla) y **fuerza el cierre de sesión tras 15 minutos de inactividad**, revocando el token de sesión y redirigiendo al login.

---

## 3. Casos de Uso y Flujos Clínicos Especializados

### 3.1. Reclutamiento Automatizado de Pacientes para Ensayos Clínicos
- **Desafío:** Hasta el 80% de los ensayos clínicos sufren retrasos por falta de pacientes compatibles o por errores en el cribado de criterios complejos de inclusión/exclusión.
- **Solución Flentio:** El agente ingesta el protocolo del ensayo (criterios de edad, biomarcadores, tratamientos previos, función renal) y cruza de forma segura historiales anonimizados procedentes de sistemas de Historia Clínica Electrónica (EHR).
- **Supervisión Médica:** El sistema genera un listado de pre-candidatos clasificados con su porcentaje de idoneidad y citas exactas a los criterios del protocolo. La decisión final de contacto e inclusión corresponde exclusivamente al Investigador Principal (PI).

### 3.2. Farmacovigilancia y Procesamiento de Eventos Adversos (ICSR)
- **Desafío:** Las compañías farmacéuticas reciben miles de reportes no estructurados de posibles efectos secundarios en múltiples idiomas y canales.
- **Solución Flentio:** El flujo extrae la sospecha de fármaco, la reacción adversa (codificada según terminología MedDRA) y evalúa la gravedad (hospitalización, riesgo vital, incapacidad).
- **Cumplimiento:** Si el evento se clasifica como grave, el flujo genera el borrador en formato E2B(R3) y alerta de inmediato al Responsable de Farmacovigilancia para su validación y envío a las agencias en el plazo legal (7 a 15 días).

### 3.3. Cuadernos de Laboratorio Electrónicos (ELN) y Trazabilidad Biotecnológica
- **Solución Flentio:** Integración con cuadernos electrónicos (Benchling) para registrar experimentos moleculares, pasajes celulares y validaciones de PCR con trazabilidad completa de reactivos y lotes.

---

## 4. Conectores e Integraciones del Ecosistema Sanitario

Flentio Medical incorpora soporte nativo para los principales estándares y suites del sector biomédico:

1. **SMART on FHIR (Fast Healthcare Interoperability Resources):**
   - Intercambio interoperable de recursos clínicos (`Patient`, `Condition`, `Observation`, `MedicationRequest`) según el estándar HL7 FHIR R4.
2. **Epic Systems EHR:**
   - Conector federado con autenticación OAuth2 para consulta segura de historiales bajo consentimiento.
3. **Medidata Rave EDC (Electronic Data Capture):**
   - Sincronización de formularios de recogida de datos clínicos (CRF) y resolución de discrepancias.
4. **Veeva Vault Clinical (eTMF / CTMS):**
   - Ingesta y clasificación automática de documentación del Master File del Ensayo Clínico.
5. **Benchling ELN:**
   - Trazabilidad de entidades biológicas, plásmidos y registros analíticos.

---

## 5. Procedimiento de Despliegue y Validación (IQ/OQ/PQ)

Para certificar el entorno ante auditorías farmacéuticas (GAMP 5):
1. **Instalación (`.env`):**
   ```bash
   APP_EDITION=medical
   DEFAULT_GOVERNANCE_PROFILE=HEALTHCARE_CLINICAL
   VITE_APP_EDITION=medical
   ```
2. **Cualificación de Instalación (IQ):** Ejecutar la suite automatizada `npm test` en `backend/` verificando 538/538 pruebas superadas y el módulo `CFR21AuditViewer`.
3. **Cualificación Operacional (OQ):** Comprobar que el auto-logoff se dispara a los 15 minutos y que el filtro DLP anonimiza el 100% de los datos de prueba sin exponer nombres de pacientes.
4. **Cualificación de Desempeño (PQ):** Emisión y descarga del Certificado de Auditoría desde `/audit` firmado con SHA-256.
