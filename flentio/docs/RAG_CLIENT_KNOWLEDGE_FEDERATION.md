# Federación de conocimiento operativo del cliente

## Principio

El conocimiento que permite investigar una incidencia pertenece al cliente y
procede principalmente de:

- su documentación técnica y operativa;
- sus RAG internos;
- CMDB y catálogos de aplicaciones;
- ITSM, problemas, incidentes y postmortems;
- repositorios de runbooks;
- CI/CD, configuración e inventarios;
- SIEM, SOC y fuentes de seguridad autorizadas.

Flentio no presupone que esos contenidos deban copiarse a su propio RAG. La
opción predeterminada es **federar la consulta** y conservar únicamente la
evidencia mínima necesaria para reconstruir la decisión.

## Modos de integración

| Modo | Funcionamiento | Uso recomendado |
|---|---|---|
| `FEDERATED_REFERENCE` | Consulta el RAG/servicio del cliente y recibe fragmentos, citas y referencias autorizadas | Predeterminado para producción |
| `CLIENT_HOSTED_INDEX` | El índice Flentio se despliega dentro del perímetro y cuenta del cliente | Cuando no existe RAG interno compatible |
| `CONTROLLED_COPY` | Copia autorizada, clasificada, versionada y sujeta a retención | Excepción por rendimiento o disponibilidad |
| `PUBLIC_SHARED` | Fuentes públicas como CISA KEV en el RAG gobernado | Contexto externo, nunca prueba de afectación local |

El modo se decide por fuente y jurisdicción. No existe fallback silencioso de
federación a copia.

## Contrato mínimo de un RAG interno

El adaptador no debe depender de un proveedor concreto. Una respuesta federada
normalizada contiene:

```json
{
  "queryId": "identificador-del-cliente",
  "sourceSystem": "rag-interno",
  "retrievedAt": "fecha-ISO-8601",
  "policyDecisionId": "referencia-de-autorización",
  "results": [
    {
      "documentId": "id-opaco",
      "version": "versión",
      "title": "título autorizado",
      "section": "sección",
      "excerpt": "fragmento mínimo autorizado",
      "score": 0.0,
      "classification": "INTERNAL",
      "sourceUri": "referencia estable",
      "contentHash": "sha256",
      "effectiveFrom": "fecha",
      "effectiveUntil": null
    }
  ]
}
```

Flentio valida esquema, tenant, vigencia, clasificación, cobertura y hashes. El
score de otro RAG no se compara directamente con el score local sin calibración.

## Evidencia que conserva Flentio

Por defecto:

- sistema consultado y query ID;
- timestamp y actor/workload;
- decisión de autorización;
- IDs opacos de documento y versión;
- hash y URI estable;
- citas utilizadas;
- clasificación y vigencia;
- resultado de la investigación y acción;
- hash del fragmento si el cliente no permite persistir texto.

El texto completo, embeddings, logs, documentos y credenciales permanecen en el
cliente. Un fragmento sólo se persiste si la política lo permite y existe una
retención aprobada.

## Consulta de múltiples RAG

Una investigación puede consultar RAG diferentes:

1. runbooks de Operaciones;
2. arquitectura de aplicaciones;
3. incidentes y problemas;
4. seguridad/SOC;
5. normativa y controles;
6. conocimiento público.

El agregador preserva procedencia y autorización por resultado. No fusiona
fragmentos en una afirmación sin mantener sus citas ni resuelve contradicciones
ocultándolas. Si dos fuentes discrepan, la salida muestra ambas, vigencia, owner
y el dato necesario para decidir.

## Disponibilidad y fallo

- Un RAG no disponible produce `FUENTE_CONOCIMIENTO_NO_DISPONIBLE`.
- Una respuesta sin citas/versiones produce `EVIDENCIA_RECHAZADA`.
- Un documento caducado no autoriza acciones.
- Una fuente denegada por política no se sustituye por conocimiento del modelo.
- Si falta el RAG crítico, Flentio puede continuar recopilando telemetría, pero
  se abstiene de recomendar acciones que dependan de esa documentación.

## Seguridad

- identidad federada de workload y mínimo privilegio;
- mTLS/OAuth según estándar del cliente;
- consultas acotadas y sin secretos;
- RLS/ABAC coherente con identidad del usuario;
- DLP antes de persistir cualquier fragmento;
- sin entrenamiento de modelos con contenido del cliente;
- sin caché compartida entre organizaciones;
- borrado/expiración propagados cuando exista copia controlada;
- trazabilidad de cada acceso y cita.

## Despliegue BBVA provisional

En un entorno BBVA, el adaptador se desplegaría en NextGen o AWS según la
política de la carga. Consultaría los RAG y repositorios internos autorizados
desde el perímetro del banco. Flentio no enviaría documentación de ASO, APX,
Cells, aplicaciones, incidentes o runbooks a un SaaS externo por defecto.

Esta topología es `ARQUITECTURA_HIPOTÉTICA_NO_VALIDADA` hasta conocer identidad,
API, modelo de autorización, residencia, latencia y contratos de los RAG reales.

## Primer RAG objetivo: BMC HelixGPT

BMC HelixGPT está autorizado como primer proveedor federado y permanece
`NO_CONFIGURADO`. Flentio priorizará la API oficial de conocimiento recomendado
de Helix ITSM y, si la edición del cliente ofrece una API externa soportada, el
puerto de HelixGPT/Agentic Chat. No se automatizará su interfaz web.

La respuesta deberá mapear artículos/tickets/casos a IDs, versiones, enlaces y
permisos. El texto generado por HelixGPT no sustituye esas fuentes. Sin citas
resolubles, la respuesta puede mostrarse como contexto no verificado, pero no
autoriza líneas de acción ni remediación.

## Datos necesarios del cliente

- catálogo de RAG/repositorios y owner;
- API y esquema de respuesta;
- identidad y autorización;
- clasificación y reglas de persistencia;
- versionado, vigencia y URI estable;
- límites de consulta, latencia y disponibilidad;
- política de citas, hashes y auditoría;
- tratamiento de revocación y borrado;
- entorno NextGen/AWS permitido;
- procedimiento de homologación del adaptador.

## Estado

`CONTRATO_VALIDADO_LOCALMENTE`, proveedor BMC HelixGPT
`AUTORIZADO_NO_CONFIGURADO`. El módulo
`backend/src/rag/federatedKnowledgeContract.js` valida el sobre normalizado,
pertenencia a consulta/fuente, hashes SHA-256, duplicados, clasificación y
vigencia. No realiza conexiones ni concede acceso. La selección o conexión de un
RAG concreto requiere autorización del cliente y pruebas reales de aislamiento,
citas, vigencia, fallo cerrado y rendimiento.

El contrato se limita a 50 resultados y 8.000 caracteres por fragmento. Sólo
admite URI HTTPS o URN opaca sin credenciales y timestamps ISO-8601 UTC
normalizados. Un score se conserva como señal del proveedor, pero no se compara
ni fusiona directamente con puntuaciones de otros RAG.

El orquestador `backend/src/rag/federatedKnowledgeService.js` consulta hasta
diez puertos inyectados, con timeout acotado. Una fuente marcada obligatoria
falla cerrado; una opcional queda `NO_DISPONIBLE` sin ocultarlo. Filtra por
clearance, preserva el score dentro de su fuente, no fabrica ranking global y
detecta como contradicción que una misma fuente entregue contenido diferente
bajo el mismo documento y versión. Los puertos de test no constituyen
proveedores de producción.
