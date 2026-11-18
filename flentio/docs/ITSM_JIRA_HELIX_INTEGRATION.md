# Integración ITSM con Jira y BMC Helix

## Estado

Jira y BMC Helix han sido seleccionados por el propietario del proyecto como
primeros sistemas ITSM. Estado de ambos: `AUTORIZADO_NO_CONFIGURADO`.

El contrato canónico local está implementado en
`backend/src/integrations/itsmRecordContract.js`. No existen todavía endpoint,
credencial, proyecto/formulario, webhook ni prueba contra una instancia real.

## Objetivos

1. Recuperar incidentes, problemas, cambios y solicitudes autorizadas.
2. Relacionar errores actuales con incidentes anteriores realmente resueltos.
3. Correlacionar los cambios de los últimos siete días con la investigación.
4. Incorporar resoluciones, postmortems y runbooks al conocimiento federado.
5. Crear enlaces o comentarios de evidencia en el ticket, sólo tras habilitar
   escritura expresamente.
6. Mantener Jira/Helix como sistema de registro; Flentio no reemplaza el ITSM.

## Arquitectura

```text
Jira Cloud/Data Center ─┐
                       ├─ adaptadores de sólo lectura
BMC Helix ITSM/CMDB ───┘       │
                               ↓
                    contrato ITSM canónico
                               │
          ┌────────────────────┴────────────────────┐
          ↓                                         ↓
PostgreSQL estructurado                     conocimiento federado/RAG
estado, tiempos, relaciones,                descripción, resolución,
servicios, cambios, decisión                postmortem y runbook
          │                                         │
          └────────────────────┬────────────────────┘
                               ↓
                     Flentio Incident Lab
```

## Contrato canónico

Cada adaptador transforma su esquema propietario en:

- proveedor e ID externo;
- tipo: incidente, problema, cambio, solicitud o alerta de seguridad;
- estado canónico;
- resumen, descripción, causa y resolución;
- confianza de resolución;
- servicios, aplicaciones, cambios y registros relacionados;
- owner, fechas, URI, versión y clasificación;
- hash de integridad del registro normalizado.

Sólo un ticket `resolved/closed` con resolución y confirmación de operador,
problema o postmortem puede entrar en memoria operacional de alta confianza.

## Jira

### Lectura inicial

- Jira REST API v3 para Cloud; el cliente deberá indicar si utiliza Cloud o Data
  Center, pues no comparten necesariamente autenticación ni contrato.
- JQL aprobada y construida por configuración, nunca texto libre del navegador.
- Campos mínimos y allowlist de custom fields.
- Paginación, cursor temporal por `updated` e idempotencia por issue/version.
- Incidentes, problemas y cambios se identificarán por project/issue type y
  mapeo del cliente, no por nombres supuestos.
- Webhooks de issue created/updated/deleted filtrados por JQL cuando la edición
  lo permita. Atlassian documenta registro de webhooks con eventos, campos y
  filtros JQL. [Jira webhooks](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-webhooks/)

### Autenticación pendiente

OAuth 2.0/3LO, Forge/Connect, token/API o mecanismo corporativo dependen del
despliegue y política del cliente. La credencial estará en la bóveda y los scopes
serán de lectura inicialmente. No se selecciona un método hasta conocer la
instancia.

## BMC Helix

### Lectura inicial

- Simplified REST API o REST de Innovation Suite según versión y módulos.
- Mapeo explícito de Incident, Problem, Change y CMDB; no se codifican nombres de
  forms del cliente sin discovery.
- Cursor por modificación, paginación e idempotencia.
- Permisos del usuario técnico limitados a compañías, grupos y formularios
  autorizados.

BMC documenta OAuth 2.0 mediante Helix SSO para clientes API y permisos ligados
al usuario. [Helix SSO OAuth](https://docs.bmc.com/xwiki/bin/view/Service-Management/Innovation-Suite/BMC-Helix-Innovation-Suite/is253/Developing-applications-by-using-BMC-Helix-Innovation-Studio/Developing-and-deploying-code-based-applications/Customizing-an-application-with-REST-APIs/Using-authorization-REST-APIs-to-consume-BMC-Helix-Single-Sign-On/)
La API ITSM permite trabajar con incidentes, cambios, problemas y solicitudes.
[BMC Helix ITSM REST](https://docs.bmc.com/xwiki/bin/view/Service-Management/IT-Service-Management/BMC-Helix-ITSM/itsm2105/Developing/Integrating-ITSM-with-third-party-applications-by-using-the-REST-API/The-REST-API-references/)

### HelixGPT y su RAG

El cliente ha indicado que su instalación de Helix integra IA y que se utilizará
su RAG. Por tanto, Helix tendrá dos puertos separados:

1. **BMC Helix ITSM/CMDB estructurado:** tickets, estados, relaciones, cambios,
   servicios, assets y fechas mediante REST.
2. **BMC HelixGPT/Knowledge federado:** respuestas y artículos recuperados por
   el RAG de Helix, conservando enlaces, versiones, permisos y referencias.

BMC confirma que HelixGPT utiliza RAG sobre fuentes como Helix ITSM Knowledge
Management, ComAround, Digital Workplace y Business Workflows. También indica
que la búsqueda agentic obtiene respuestas desde artículos, incidentes y otros
datos empresariales, respetando permisos sobre artículos publicados.
[BMC: provisión RAG](https://docs.bmc.com/xwiki/bin/view/Service-Management/Employee-Digital-Workplace/BMC-HelixGPT/helixgpt252/Setting-up-and-going-live/Provisioning-and-setting-up-the-generative-AI-provider-for-your-application/),
[BMC: Knowledge como fuente](https://docs.bmc.com/xwiki/bin/view/Service-Management/Knowledge-Management/BMC-Helix-Innovation-Suite-Knowledge-Management/iskm262/Administering/Configuring-BMC-Helix-Innovation-Suite-Knowledge-Management-as-a-knowledge-source-for-BMC-HelixGPT-capabilities-in-BMC-Helix-ITSM/)

La API simplificada de ITSM documenta un endpoint para recuperar artículos de
conocimiento e incidentes recomendados para un incidente o problema. Este será
el primer mecanismo técnico a validar porque devuelve referencias recuperadas
sin depender de automatizar la interfaz gráfica.
[BMC: recommended knowledge API](https://docs.bmc.com/xwiki/bin/view/Service-Management/IT-Service-Management/BMC-Helix-ITSM/itsm261/Developing/Integrating-third-party-applications-with-BMC-Helix-ITSM-by-using-the-simplified-REST-API/Learning-about-the-simplified-REST-API/Example-of-using-the-simplified-REST-API-to-retrieve-recommended-knowledge-articles-and-tickets/)

No se asumirá que el chat HelixGPT expone una API externa estable en todas las
ediciones. Si el cliente no dispone de una API soportada, Flentio usará los
endpoints oficiales de conocimiento/recomendaciones; no hará scraping ni
automatización de la UI.

Una respuesta generada por HelixGPT se tratará como **síntesis**, no como fuente
primaria. Para recomendar una acción debe incluir o poder resolverse a artículos,
tickets o casos autorizados. Si sólo devuelve texto sin cita/versionado, Flentio
la marcará `EVIDENCIA_RECHAZADA` para decisiones operativas.

### Autenticación pendiente

Se priorizará OAuth 2.0/Helix SSO sobre credenciales persistentes. El método
exacto depende de versión y configuración. Un token se tratará como contraseña,
con rotación, caducidad y revocación.

### Recogida M1 implementada

La Skill `bmc_helix_itsm` 0.2 implementa `POST
/api/com.bmc.dsm.itsm.itsm-rest-api/{version}/incident/search` con el filtro
oficial `My Group Tickets`, límite 25 y sesión efímera. El formulario dedicado
exige versión API, lista de estados resueltos y nombres exactos de los campos de
servicio y modificación porque estos valores dependen de la edición y del modelo
del cliente. Flentio filtra localmente por estado resuelto, mismo servicio y
ventana del expediente; sólo conserva ID, URI, estado, campo de servicio y fecha.
No copia descripciones, comentarios, work info ni resolución.

La ruta administrativa es `POST
/api/admin/operational-investigations/{id}/collect-helix`. El perfil del cliente
continúa `NO_CONFIGURADO`; la prueba con servidor HTTP controlado valida el
contrato del adaptador, no una instancia bancaria real. HelixGPT permanece como
puerto federado separado y `NO_CONFIGURADO`.

## Lectura frente a escritura

| Fase | Jira | Helix |
|---|---|---|
| M1 | Leer issues/cambios y recibir webhooks | Leer registros y cambios autorizados |
| M2 | Añadir enlace/comentario a expediente, con aprobación | Añadir work info/enlace, con aprobación |
| M3 | Transición allowlist específica | Actualización allowlist específica |

Crear, resolver, cerrar, reasignar o cambiar prioridad queda prohibido hasta
definir autoridad, campos, transiciones y rollback. Flentio nunca cerrará un
ticket sólo porque una métrica vuelva a verde.

## Datos que no deben ir al RAG

- tokens, cookies, cabeceras y secretos;
- adjuntos sin escaneo y aprobación;
- datos personales no necesarios;
- worklogs privados o campos restringidos;
- payloads transaccionales;
- comentarios sin distinguir autor, fecha y estado de validación;
- tickets abiertos como si fueran soluciones confirmadas.

## Información requerida del cliente

### Común

- entorno y versión/edición;
- URL privada y conectividad desde NextGen/AWS;
- proyectos, compañías y grupos incluidos;
- taxonomía de incident/problem/change;
- custom fields/forms y estados;
- clasificación, retención y campos prohibidos;
- identidad técnica, scopes y proceso de alta;
- límites de API, ventanas y SLO;
- política de webhook y replay;
- responsables de Operaciones, ITSM, Seguridad y Datos.

### Jira

- Cloud o Data Center;
- project keys e issue types;
- JQL base autorizada;
- campos de servicio, aplicación, causa y cambio;
- transiciones y permisos, inicialmente sólo lectura.

### Helix

- ITSM/Innovation Suite y versión;
- API simplificada o AR System REST;
- forms/record definitions aprobados;
- company/support group y permisos;
- CMDB reconciliation identity y datasets cuando aplique.
- HelixGPT habilitado, versión y licencia;
- proveedor de conocimiento: ISKM, ComAround, BWF u otro;
- API soportada para Agentic Chat o recommended knowledge;
- esquema de citas/enlaces, identidad y propagación de permisos;
- política para conservar fragmentos o únicamente hashes/referencias.

## Criterios de aceptación M1

- lectura real de al menos un incidente, problema y cambio autorizados;
- cero registros cruzados entre organizaciones/ámbitos;
- cursor incremental reproducible e idempotente;
- timestamps y estados mapeados sin pérdida semántica;
- borrado/restricción propagados;
- secretos y campos prohibidos ausentes del RAG y auditoría;
- ticket abierto no promovido a solución;
- caída de Jira/Helix visible como `NO_DISPONIBLE`;
- ninguna escritura efectuada;
- comparación manual de una muestra por owner ITSM.

## Rollback

Deshabilitar el conector detiene webhooks y sincronización sin borrar evidencia.
Se revoca la credencial en el sistema del cliente, se conserva el cursor y se
archiva el conocimiento derivado según retención. Las futuras escrituras deberán
ser idempotentes y registrar la operación inversa cuando exista.
