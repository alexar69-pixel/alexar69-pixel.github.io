# F1 — Evidencia de autorización documental

**Estado:** VALIDACIÓN  
**Fecha:** 31-07-2026  
**Entorno:** PostgreSQL/pgvector efímero y Ollama real  
**Datos:** documentos técnicos de validación sin datos bancarios.

## Implementación verificada

- migración `002_document_authorization.sql` repetible;
- clasificación, entidad jurídica, jurisdicción, departamento y vigencia;
- concesiones normalizadas por usuario/grupo con permisos `read/manage`;
- RLS previo a listado, recuperación, cita, actualización y archivado;
- atributos de usuario persistidos localmente y firmados en JWT;
- gestión visual de clearance y ámbitos por administrador de la misma organización;
- selector no-code de gobierno en carga textual y de archivo;
- SSO y LDAP simulados sustituidos por respuestas reales `NO_CONFIGURADO`;
- bloqueo asesor por tenant/fuente para deduplicación concurrente.

## Matriz real de acceso

Documento: `CONFIDENTIAL`, entidad `bank-es`, jurisdicción `ES`, departamento `compliance`, grupo `risk-emea`.

| Identidad | Listado | Recuperación | Resultado |
|---|---:|---:|---|
| creador con `manage` | 1 | 1 | permitido |
| lector del grupo con clearance y ámbitos correctos | 1 | 1 | permitido |
| administrador sin concesión | 0 | 0 | denegado |
| grupo correcto con clearance `INTERNAL` | 0 | 0 | denegado |
| entidad incorrecta | 0 | 0 | denegado |
| jurisdicción incorrecta | 0 | 0 | denegado |
| departamento incorrecto | 0 | 0 | denegado |

El administrador sin concesión tampoco pudo archivar el documento. Un intento de conceder acceso a un grupo ausente del JWT firmado fue rechazado antes de encolar la ingesta.

Un lector de grupo intentó insertar directamente una concesión `manage` y PostgreSQL lo rechazó por RLS. Las ACL sólo pueden consultarse o modificarse por gestores explícitos; existe una excepción transaccional limitada al UUID que el creador está ingestando para insertar su primera concesión.

Un documento `CONFIDENTIAL` con vigencia futura alcanzó estado `completed`, pero devolvió cero filas en listado y recuperación. Esto confirma la separación entre administración y lectura vigente.

## Concurrencia

Tres trabajos simultáneos con la misma fuente terminaron `completed`. La base conservó un documento y una versión. Durante la primera ejecución se descubrió una violación de unicidad real; se corrigió con `pg_advisory_xact_lock(hashtextextended(tenant|source|sourceKey))` y una segunda comprobación dentro de la transacción.

## Rendimiento SQL

`EXPLAIN (ANALYZE, BUFFERS)` confirmó que la búsqueda de concesiones puede usar `rag_document_grants_subject_idx`; ejecución observada: 0,05 ms. El listado autorizado ejecutó en 2,443 ms sobre el corpus pequeño. Estas cifras prueban el recorrido e índice, no capacidad bancaria representativa.

## Verificación de código

- 14/14 pruebas backend superadas;
- cero vulnerabilidades en `npm audit --omit=dev`;
- frontend lint sin errores, con advertencias preexistentes;
- compilación Vite completada;
- migración 001 + 002 aplicada repetidamente sin error.

## Riesgos y pendientes

- F0 sigue pendiente de corpus y volumen representativos;
- un IdP OIDC/SAML real no está configurado; SSO/LDAP devuelve `NO_CONFIGURADO`;
- los usuarios deben volver a iniciar sesión tras cambiar atributos para recibir un JWT nuevo;
- falta revisión independiente de seguridad antes de un despliegue bancario;
- el bundle frontend continúa por encima de 500 kB, deuda no introducida por la lógica ACL.

## Reversión

Seguir ADR-RAG-001. El entorno efímero y su volumen se eliminan después de documentar la prueba. No se utilizaron ni modificaron datos productivos.
