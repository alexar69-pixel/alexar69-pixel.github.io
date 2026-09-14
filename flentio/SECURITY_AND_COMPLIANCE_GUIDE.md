# Guía integral de seguridad y cumplimiento de Flentio

> Versión documental: 05-09-2026. Alcance: checkout local de Flentio y su
> configuración de referencia. Este documento es explicativo y no constituye
> asesoramiento jurídico, certificación, pentest, auditoría independiente ni
> autorización para producción.

## 1. Resumen ejecutivo

Flentio incorpora controles técnicos para proteger identidades, organizaciones,
workflows, credenciales, documentos, evidencias y operaciones asistidas por IA.
Los controles más relevantes observados son autenticación JWT, contraseñas con
`bcrypt`, autorización por roles, aislamiento PostgreSQL mediante Row Level
Security (RLS), auditoría encadenada con HMAC, cifrado AES-256-GCM de originales
RAG, análisis antimalware, cuarentena, control de inyección de prompt,
clasificación documental, evidencia con procedencia y estados de fallo cerrado.

Estos mecanismos **facilitan** un programa de cumplimiento, pero no hacen que un
despliegue sea automáticamente conforme con RGPD, DORA, NIS2, ENS, Reglamento de
IA, ISO/IEC 27001 o SOC 2. El cumplimiento final depende del caso de uso, los
datos, la entidad responsable, contratos, infraestructura, configuración,
operación, pruebas y evaluación independiente.

Estado general del checkout:

| Área | Estado documental | Lectura correcta |
|---|---|---|
| Controles de aplicación | `IMPLEMENTADO_CON_LIMITES` | Existen controles verificables en código y pruebas locales. |
| Demo local | `OPERATIVO_NO_PRODUCTIVO` | Sirve para validar recorridos; utiliza datos sintéticos. |
| Producción empresarial | `NO_VALIDADA` | Faltan endurecimiento, infraestructura, pruebas y aceptación del cliente. |
| Certificación ISO/ENS/SOC 2 | `NO_ACREDITADA` | El repositorio no contiene un certificado o informe independiente vigente. |
| Conformidad regulatoria | `DEPENDENCIA_CLIENTE` | Requiere análisis jurídico, de riesgos y del tratamiento concreto. |

## 2. Cómo interpretar los estados

| Estado | Significado |
|---|---|
| `OPERATIVO` | El control superó la comprobación indicada en el entorno evaluado. |
| `SIN_DATOS` | La fuente real respondió, pero todavía no existen observaciones. |
| `NO_CONFIGURADO` | Falta una clave, proveedor, destino o decisión obligatoria. |
| `NO_DISPONIBLE` | El componente configurado no respondió o falló su comprobación. |
| `NO_VALIDADA` | No existe evidencia suficiente para afirmar la capacidad. |
| `DEPENDENCIA_CLIENTE` | La organización usuaria debe aportar una decisión, infraestructura o evidencia. |
| `NO_BANCARIO` | Dato o escenario sintético que no acredita operación bancaria. |

Un estado desconocido nunca debe convertirse en cero, éxito u `OPERATIVO`.

## 3. Modelo de responsabilidad compartida

### Responsabilidad del producto Flentio

- aplicar autenticación, autorización, aislamiento y validación de entradas;
- minimizar datos en logs, métricas y telemetría;
- conservar trazabilidad y procedencia;
- mostrar dependencias ausentes o fallidas sin fabricar resultados;
- ofrecer configuración segura y documentación de operación;
- corregir vulnerabilidades del código y dependencias dentro de su alcance.

### Responsabilidad del operador o cliente

- determinar base jurídica, finalidad, minimización y plazos de conservación;
- clasificar información y configurar grupos, entidades y jurisdicciones;
- gestionar identidades corporativas, MFA/SSO y ciclo de altas/bajas;
- custodiar y rotar secretos mediante una bóveda autorizada;
- aportar TLS, WAF/gateway, segmentación, backups, HA, SIEM y monitorización;
- aprobar proveedores, transferencias internacionales y residencia de datos;
- realizar DPIA/EIPD, análisis de riesgos, continuidad, pentest y auditorías;
- gestionar solicitudes de interesados, incidentes y notificaciones legales.

### Responsabilidad del proveedor de infraestructura o IA

- cumplir el contrato, ubicación, disponibilidad y seguridad acordados;
- proporcionar métricas, registros y compromisos de subencargados;
- permitir configuración de retención/no entrenamiento cuando corresponda;
- notificar incidentes conforme al contrato y legislación aplicable.

## 4. Arquitectura y límites de confianza

Los límites principales son:

1. navegador y API;
2. proceso web y workers de workflows/RAG;
3. PostgreSQL de plataforma y PostgreSQL/pgvector para conocimiento;
4. almacenamiento de objetos para originales;
5. ClamAV y servicios de extracción;
6. proveedores de modelos y reranking;
7. integraciones corporativas, SIEM y sistemas de tickets.

Cada cruce requiere identidad, tenant, autorización, validación, timeout,
tratamiento explícito del error y una fuente de evidencia. El `docker-compose`
incluido representa una topología local de nodo único, no una arquitectura de
alta disponibilidad certificada.

## 5. Identidad, autenticación y sesiones

| Control | Implementación observada | Límite o acción necesaria |
|---|---|---|
| Contraseñas | Hash `bcrypt` en `backend/src/api/auth.js` e `identitySecretsRepository.js`. | Definir política corporativa de longitud, bloqueo, rotación y recuperación. |
| Sesión API | JWT firmado y validación del usuario activo. | `JWT_SECRET` debe ser aleatorio, externo al repositorio y rotado de forma controlada. |
| Usuario deshabilitado | La resolución de identidad excluye `disabled_at`. | Integrar bajas y recertificación con el IdP corporativo. |
| Roles | Middleware RBAC para `admin`, `editor`, `operator` y otros perfiles. | Mantener matriz de permisos y pruebas negativas ruta por ruta. |
| SSO/OAuth | Capacidad condicionada por proveedor y configuración. | MFA, políticas del IdP y sesiones empresariales son `DEPENDENCIA_CLIENTE`. |
| Protección de login | Límite de intentos por IP. | Complementar con gateway, detección de abuso y alertas. |

No deben usarse credenciales predeterminadas ni sesiones personales OAuth en
producción. Las credenciales demo están limitadas al laboratorio.

## 6. Autorización y aislamiento multitenant

Flentio fija `organization_id` y `actor_id` dentro de transacciones PostgreSQL
cortas. Las tablas sensibles aplican RLS forzada y políticas que comparan los
atributos de la fila con el contexto de la transacción. El RAG añade controles
por tenant, clearance, grupos, entidades legales, jurisdicciones y departamentos.

Principios:

- ninguna organización se obtiene de una cabecera no confiable como autoridad;
- las consultas heredan la identidad autenticada;
- la autorización documental se aplica antes de reranking o generación;
- los workers conservan el contexto de tenant al reclamar trabajos;
- el rol de aplicación no ejecuta DDL: las migraciones usan un rol separado;
- una prueba positiva no sustituye pruebas negativas de cruce entre tenants.

Evidencia principal: migraciones de `backend/src/platform/migrations/` y
`backend/src/rag/migrations/`, además de `backend/src/platform/postgres.js`.

## 7. Secretos, claves y credenciales

- Los secretos se obtienen de configuración o del gestor autorizado; no deben
  incluirse en Git, imágenes, logs, prompts o tickets.
- `JWT_SECRET`, `AUDIT_HMAC_SECRET` y claves de cifrado requieren generación
  criptográfica, control de acceso, rotación y recuperación documentada.
- Las credenciales de conectores deben tener mínimo privilegio y ámbito exacto.
- Los valores de `.env.example` son ejemplos de configuración, no secretos
  productivos ni prueba de que una integración esté operativa.
- La rotación debe conservar capacidad de descifrado del histórico autorizado y
  disponer de rollback seguro.

Producción debe usar una bóveda/KMS corporativa. La existencia de un adaptador no
acredita que el proveedor externo esté configurado o homologado.

## 8. Cifrado y protección de datos

### En tránsito

El despliegue productivo debe terminar TLS en un gateway homologado, restringir
hosts/orígenes y proteger el tráfico interno según la topología. El servidor
incluye Helmet y allowlists configurables, pero la CSP y COEP están desactivadas
en el checkout y requieren diseño y prueba antes de producción.

### En reposo

Los originales RAG admiten cifrado AES-256-GCM; el modo empresarial puede usar
cifrado envolvente con AWS KMS. El almacenamiento y sus versiones/WORM dependen
del object store configurado. PostgreSQL, backups, snapshots y volúmenes deben
cifrarse en la capa de infraestructura.

### Minimización

- La telemetría de caché no almacena prompts, respuestas, secretos ni contenido.
- La evidencia operacional debe conservar hashes, referencias y metadatos
  suficientes, evitando payloads completos innecesarios.
- Los logs no deben incluir tokens, contraseñas, claves, documentos íntegros o
  datos personales salvo necesidad aprobada y protegida.

## 9. Seguridad de API y frontend

Controles presentes:

- Helmet para cabeceras HTTP;
- CORS y hosts permitidos configurables;
- límites de tamaño: JSON general, importaciones y documentos RAG;
- rate limiting en autenticación y varias familias de endpoints;
- validación de roles en rutas administrativas y operativas;
- estados de dependencia explícitos y respuestas de fallo cerrado.

Trabajo pendiente antes de exposición pública:

- diseñar y activar CSP/COEP compatibles con el frontend;
- establecer rate limit global y cuotas por identidad/tenant/ruta;
- bloquear o retirar `/api/sdk/*` y `/api/interop/sidecar/*`, que siguen siendo
  heredados y simulados;
- proteger `/api/openapi/import` con autenticación, RBAC y límites aprobados;
- colocar la aplicación tras HTTPS, WAF/API gateway y protección DDoS;
- ejecutar SAST, SCA, detección de secretos, DAST y pentest independientes.

## 10. Seguridad documental y RAG

El pipeline RAG seguro contempla:

1. recepción y normalización del archivo;
2. validación de tamaño, tipo y estructura;
3. análisis real con ClamAV;
4. inspección de patrones de prompt injection;
5. cuarentena o rechazo ante hallazgos;
6. revisión humana cuando procede;
7. indexación únicamente después de aprobación;
8. registro de versión, procedencia, hash y ciclo de vida;
9. autorización documental antes de recuperación y reranking;
10. respuesta con citas o abstención cuando falta evidencia.

Si ClamAV, object store, KMS, reranker obligatorio o fuente de conocimiento no
está disponible, el recorrido debe detenerse o declararse `NO_CONFIGURADO` /
`NO_DISPONIBLE`; nunca debe degradar silenciosamente a una respuesta inventada.

Documentación detallada: [Seguridad de ingesta RAG](RAG_SECURITY_INGESTION.md),
[Procedencia](RAG_PROVENANCE_LIFECYCLE.md) y
[Preparación productiva](RAG_PRODUCTION_READINESS.md).

## 11. Gobierno de IA

Flentio está diseñado para que las salidas de IA sean propuestas o evidencia,
no autoridad automática ilimitada. Los controles documentados incluyen:

- citas y referencias a evidencia autorizada;
- abstención cuando no existe evidencia suficiente;
- separación entre recomendación y ejecución;
- supervisión/aprobación humana para acciones de riesgo;
- contratos de salida, versión de prompt/modelo y trazabilidad;
- DLP y minimización antes de enviar información a proveedores;
- métricas de uso y caché sin almacenar el texto de prompts/respuestas;
- caché aislada por organización, proveedor, modelo, versión y prefijo estable;
- fallback sin caché cuando el proveedor no la soporta, sin debilitar RLS,
  evidencia, citas o abstención;
- prohibición de presentar mocks o simulaciones como operaciones reales.

La clasificación jurídica del sistema de IA depende de su finalidad y uso. El
cliente debe inventariar cada caso, determinar si es de alto riesgo, asignar
responsables y completar evaluación, documentación y vigilancia aplicables.

## 12. Auditoría, integridad y no repudio

La plataforma mantiene eventos de auditoría por tenant con secuencia, hash
padre y HMAC-SHA-256, y dispone de verificación de cadena. Una outbox permite la
entrega posterior a un SIEM. El RAG mantiene además eventos de ingesta,
autorización, procedencia y ciclo de vida.

Límites importantes:

- una cadena HMAC evidencia alteraciones dentro del modelo previsto, pero no
  equivale por sí sola a un servicio externo de sellado de tiempo;
- la inmutabilidad WORM sólo queda acreditada si el object store real está
  configurado y probado con sus políticas de retención;
- la entrega SIEM es `NO_CONFIGURADO` hasta disponer de destino autorizado;
- `AUDIT_HMAC_SECRET` debe ser externo, restringido y rotado con procedimiento.

## 13. Retención, privacidad y derechos

El responsable del tratamiento debe crear un inventario por tipo de dato:

| Dato | Finalidad | Retención a decidir | Eliminación/limitación |
|---|---|---|---|
| Identidad y permisos | Acceso y seguridad | Política laboral/contractual | Baja, anonimización o conservación legal. |
| Workflows y versiones | Operación y trazabilidad | Ciclo de vida del proceso | Archivado gobernado; preservar evidencia obligatoria. |
| Ejecuciones y logs | Diagnóstico/auditoría | Según riesgo y regulación | Purgado controlado, minimización y legal hold. |
| Documentos/originales RAG | Conocimiento autorizado | Propietario y vigencia documental | Borrado coordinado de índice, versiones y objeto. |
| Auditoría/WORM | Seguridad y evidencia | Requisito contractual/legal | Retención protegida; excepción documentada. |
| Métricas | Capacidad y FinOps | Ventana operacional | Agregación/anonimización cuando sea posible. |

Flentio no decide por sí solo base jurídica, plazo o respuesta a acceso,
rectificación, supresión, oposición, limitación y portabilidad. El cliente debe
documentar procedimientos, verificar copias/índices/backups y resolver conflictos
entre supresión, conservación obligatoria y legal hold.

## 14. Continuidad, disponibilidad y recuperación

El repositorio incorpora colas durables, leases recuperables y health checks,
pero no acredita alta disponibilidad, RTO, RPO o capacidad productiva. Antes de
producción se requiere:

- SLO y presupuesto de errores aprobados;
- PostgreSQL con HA, backup cifrado y restauración probada;
- object store redundante y prueba de recuperación;
- réplicas y escalado de web/workers dimensionados mediante carga real;
- gestión de caída de proveedores y circuit breaking/timeouts;
- runbooks, guardias, comunicación y simulacros;
- pruebas de pérdida de nodo, corrupción, restauración y reconciliación WORM.

Véase [Capacidad, carga y escalado](architects/CAPACIDAD_CARGA_USUARIOS_Y_PROCESOS.md).

## 15. Gestión de vulnerabilidades y desarrollo seguro

Puertas mínimas recomendadas para cada entrega:

1. revisión de cambios y separación de funciones;
2. lint, pruebas unitarias, integración y autorización negativa;
3. análisis de dependencias y licencia;
4. escaneo de secretos e imágenes de contenedor;
5. SAST y DAST con triage y SLA por severidad;
6. SBOM y procedencia del artefacto;
7. firma/verificación de releases y migraciones;
8. pentest antes de producción y tras cambios de alto riesgo;
9. evidencia fechada en `docs/audits/`;
10. rollback que no elimine autenticación, RLS, auditoría o fallo cerrado.

El checkout contiene pruebas funcionales y auditorías locales, pero no evidencia
suficiente para afirmar que todas estas puertas se ejecutan en un CI/CD
empresarial.

## 16. Gestión de incidentes

1. Clasificar severidad, datos, tenant, actor, versión y ventana temporal.
2. Contener: revocar sesiones/credenciales, aislar el conector o deshabilitar la
   ruta sin eliminar evidencias.
3. Preservar auditoría, hashes, logs mínimos y objetos sujetos a legal hold.
4. Analizar posible cruce de tenant y verificar RLS antes de reabrir.
5. Recuperar desde artefactos y backups autorizados; reconciliar colas/WORM.
6. Determinar obligaciones contractuales y regulatorias de notificación.
7. Documentar causa raíz, alcance, corrección, controles compensatorios y prueba
   posterior.

No se debe “resolver” un incidente borrando eventos o activando bypasses de
autenticación, antimalware, autorización o auditoría.

## 17. Mapa orientativo de cumplimiento

Este mapa muestra qué controles de Flentio pueden aportar evidencia. **No es una
declaración de conformidad** y debe validarse con asesoría jurídica y auditoría.

| Marco | Temas relevantes | Apoyo de Flentio | Brecha o responsabilidad externa |
|---|---|---|---|
| RGPD | Seguridad, minimización, responsabilidad, derechos, DPIA y brechas | RLS, cifrado, auditoría, minimización, clasificación y procedencia | Base jurídica, registro de tratamientos, DPIA, DPO, contratos, transferencias, plazos y derechos. |
| DORA | Gobierno del riesgo TIC, incidentes, continuidad, pruebas y terceros | Health, auditoría, colas, estados explícitos, inventario de integraciones y runbooks | Marco de gestión, registro contractual, reporting, TLPT cuando aplique, HA y pruebas corporativas. |
| NIS2 | Medidas de gestión de riesgos y notificación | Acceso, cifrado, ingesta segura, auditoría, vulnerabilidades e incidentes | Determinar ámbito, gobierno, cadena de suministro, notificación y autoridad nacional. |
| ENS | Organización, operación, protección, trazabilidad y auditoría | Identidad, RLS, cifrado, auditoría y fallo cerrado | Categorización, declaración/certificación, medidas ENS completas y auditoría acreditada. |
| Reglamento de IA | Riesgo, datos, documentación, logs, transparencia y supervisión humana | Evidencia, contratos de salida, logs, versiones, abstención y aprobación humana | Clasificación del caso, evaluación de conformidad, FRIA/DPIA cuando aplique, vigilancia y registro. |
| ISO/IEC 27001:2022 | Sistema de gestión de seguridad basado en riesgos | Controles técnicos y documentación reutilizable como evidencia | Alcance del SGSI, políticas, SoA, riesgos, auditoría interna, revisión directiva y certificación. |
| SOC 2 | Seguridad y, según alcance, disponibilidad, confidencialidad, integridad y privacidad | Acceso, aislamiento, auditoría, cifrado, monitorización y operación | Diseño/eficacia durante el periodo, controles organizativos e informe de auditor independiente. |

Fuentes oficiales de referencia:

- [RGPD, Reglamento (UE) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679)
- [DORA, Reglamento (UE) 2022/2554](https://eur-lex.europa.eu/eli/reg/2022/2554/oj)
- [NIS2, Directiva (UE) 2022/2555](https://eur-lex.europa.eu/eli/dir/2022/2555/oj)
- [Reglamento de IA, Reglamento (UE) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- [ENS, Real Decreto 311/2022 consolidado](https://www.boe.es/eli/es/rd/2022/05/03/311/con)
- [ISO/IEC 27001:2022](https://www.iso.org/standard/27001)
- [AICPA: SOC 2 y Trust Services Criteria](https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2/)

## 18. Brechas conocidas y bloqueos de producción

| Riesgo | Estado | Acción obligatoria |
|---|---|---|
| Rutas SDK y sidecar heredadas con contenido simulado | `NO_DISPONIBLE` | Bloquear/retirar hasta reemplazo autenticado, persistente y probado. |
| Importación OpenAPI sin protección suficiente | `NO_VALIDADA` | Añadir autenticación, RBAC, cuota y validación antes de exponer. |
| CSP y COEP desactivadas | `NO_VALIDADA` | Diseñar política, corregir incompatibilidades y probar navegador. |
| Ausencia de rate limit global uniforme | `NO_VALIDADA` | Implantar límites por identidad, tenant y ruta en API gateway. |
| Infraestructura local de nodo único | `NO_VALIDADA` | Diseñar HA, backup/restore, DR, TLS, red privada y monitorización. |
| Conectores sin entorno real autorizado | `NO_CONFIGURADO` | Homologar uno por uno con credenciales mínimas y pruebas de error. |
| SIEM/WORM/KMS externos | `DEPENDENCIA_CLIENTE` | Configurar, probar integridad/retención y documentar propietario. |
| Certificaciones y pentest | `NO_ACREDITADA` | Contratar evaluación independiente con alcance y fecha. |
| Capacidad, RTO y RPO | `NO_VALIDADA` | Ejecutar benchmarks y simulacros sobre arquitectura objetivo. |

Hasta cerrar y acreditar estas brechas no debe usarse la expresión
`PREPARADO_PARA_PRODUCCION` ni presentarse una certificación como obtenida.

## 19. Evidencias mínimas para una homologación

| Dominio | Evidencia requerida |
|---|---|
| Identidad | MFA/SSO, altas-bajas, roles, sesiones revocadas y recertificación. |
| Tenant | Pruebas API/SQL de acceso cruzado fallido y RLS forzada. |
| Secretos | Inventario, bóveda, rotación, acceso y escaneo sin hallazgos abiertos críticos. |
| Datos | Inventario, clasificación, residencia, retención, borrado y backups. |
| API | 401/403/413/429, validación, CSP/CORS/hosts y pentest. |
| RAG | Malware, cuarentena, inyección, ACL, citas, abstención y procedencia. |
| IA | Inventario de casos, modelos/versiones, supervisión, evaluación y monitorización. |
| Auditoría | Integridad HMAC, RLS, entrega SIEM, reloj y conservación. |
| Resiliencia | Carga, caída de dependencias, failover, backup/restore y DR. |
| Terceros | Due diligence, DPA/SLA, subencargados, ubicación y salida contractual. |
| SDLC | SAST/SCA/DAST, SBOM, secretos, firma y gestión de vulnerabilidades. |
| Gobierno | Riesgos, políticas, responsables, excepciones, auditoría y revisión directiva. |

## 20. Preguntas frecuentes para clientes

### ¿Flentio está certificado en ISO 27001, ENS o SOC 2?

No hay evidencia de una certificación o informe independiente vigente en este
repositorio. Flentio incorpora controles que pueden formar parte del alcance de
una futura evaluación, pero no deben presentarse como certificación obtenida.

### ¿Flentio cumple automáticamente RGPD o DORA?

No. La aplicación aporta controles técnicos, pero el cumplimiento depende del
tratamiento, entidad, contratos, configuración, infraestructura y operación del
cliente.

### ¿Los tenants están aislados?

El diseño implementa contexto transaccional y RLS forzada. La homologación debe
confirmarlo mediante pruebas negativas sobre el despliegue objetivo.

### ¿Se almacenan prompts en la telemetría de caché?

No. El esquema registra proveedor, modelo, versión, hash, contadores, latencia y
ahorro estimado; no guarda prompts ni respuestas.

### ¿Qué ocurre si falta una integración?

Debe mostrarse `NO_CONFIGURADO` o `NO_DISPONIBLE`. Una respuesta simulada no es
una integración operativa y está prohibida en producción.

### ¿La IA ejecuta cambios automáticamente?

Las capacidades gobernadas separan recomendación y ejecución, exigen evidencia
y contemplan aprobación humana. Cualquier autonomía adicional requiere un caso
de riesgo y autorización específicos.

### ¿Los documentos están protegidos frente a malware e inyección?

El pipeline contempla ClamAV, prompt guard, cuarentena y revisión. Si esas
dependencias obligatorias no están configuradas, la ingesta productiva debe
fallar cerrado.

## 21. Checklist de salida a producción

- [ ] Arquitectura, datos, jurisdicciones y responsables aprobados.
- [ ] Análisis de riesgos y, cuando proceda, DPIA/FRIA completados.
- [ ] SSO/MFA, RBAC y ciclo de vida de identidades validados.
- [ ] Secretos en bóveda/KMS, rotación y recuperación probadas.
- [ ] RLS y pruebas de aislamiento cruzado superadas.
- [ ] TLS, WAF, CSP, CORS, hosts, cuotas y rate limits endurecidos.
- [ ] Rutas simuladas/no autenticadas bloqueadas.
- [ ] ClamAV, object store, KMS, reranker y conectores homologados.
- [ ] Retención, borrado, legal hold y derechos documentados.
- [ ] SIEM, alertas, reloj, auditoría y WORM verificados.
- [ ] SAST, SCA, secretos, imagen, DAST y pentest cerrados.
- [ ] Prueba de carga, HA, backup/restore y DR aceptados.
- [ ] Contratos de terceros, DPA/SLA y subencargados aprobados.
- [ ] Runbooks, guardias, formación e incidente simulado completados.
- [ ] Evidencia independiente y aceptación formal archivadas.

## 22. Documentos relacionados

- [Seguridad técnica resumida](SECURITY.md)
- [Estados operacionales](PLATFORM_OPERATIONAL_STATUS.md)
- [Registro de riesgos](leadership/RISK_REGISTER.md)
- [Manual de operaciones](operators/ENTERPRISE_OPERATIONS_MANUAL.md)
- [Seguridad de ingesta RAG](RAG_SECURITY_INGESTION.md)
- [Preparación productiva RAG](RAG_PRODUCTION_READINESS.md)
- [Observabilidad y auditoría RAG](RAG_OBSERVABILITY_AUDIT.md)
- [Capacidad y carga](architects/CAPACIDAD_CARGA_USUARIOS_Y_PROCESOS.md)
- [Checklist de aceptación productiva](templates/RAG_PRODUCTION_ACCEPTANCE_CHECKLIST.md)

## 23. Mantenimiento del documento

Revisar esta guía cuando cambien controles de identidad, RLS, cifrado, RAG, IA,
auditoría, retención, infraestructura o normativa aplicable. Cada afirmación de
estado debe enlazar una prueba fechada; una prueba local o con dobles no acredita
un proveedor, infraestructura o proceso organizativo real.
