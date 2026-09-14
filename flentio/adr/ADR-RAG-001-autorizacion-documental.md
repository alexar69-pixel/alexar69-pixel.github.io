# ADR-RAG-001 — Autorización documental previa a recuperación

**Estado:** aceptada para validación  
**Fecha:** 31-07-2026

## Decisión

Flentio utiliza cuatro niveles documentales ordenados: `PUBLIC`, `INTERNAL`, `CONFIDENTIAL` y `RESTRICTED`. El acceso requiere simultáneamente:

1. pertenecer al tenant;
2. tener clearance igual o superior;
3. coincidir con entidad jurídica, jurisdicción y departamento cuando el documento los limita;
4. estar dentro de la vigencia para operaciones de lectura;
5. disponer de una concesión explícita de usuario o grupo.

La decisión se ejecuta en PostgreSQL mediante RLS y `flentio_rag.can_access_document`. El rol administrativo no sustituye una concesión documental. El creador obtiene una concesión explícita `manage`; los grupos seleccionados obtienen `read`.

Los atributos de identidad proceden de JWT firmados generados desde la base local de usuarios. Una petición no puede ampliar grupos mediante el cuerpo HTTP: sólo se aceptan grupos ya presentes en la identidad autenticada. SSO/LDAP permanece `NO_CONFIGURADO` hasta validar criptográficamente un IdP real.

## Motivos

- evita filtrar información después de recuperarla;
- protege también títulos, metadatos, versiones y fragmentos;
- separa administración de plataforma y conocimiento documental;
- permite indexar atributos usados por RLS;
- mantiene denegación predeterminada cuando falta clearance o concesión.

## Consecuencias

- los documentos anteriores reciben una concesión `manage` sólo para su creador;
- usuarios existentes tienen clearance local `INTERNAL` y ninguna pertenencia de grupo hasta que un administrador de su organización la configure;
- los tokens emitidos antes de cambiar atributos conservan sus claims hasta volver a iniciar sesión o expirar;
- documentos futuros o vencidos pueden administrarse, pero no leerse ni recuperarse;
- un IdP corporativo deberá mapear estos mismos claims sin aceptar valores enviados por el navegador.

## Reversión

Conservar columnas y concesiones. Si una incidencia obliga a deshabilitar temporalmente la autorización fina, aplicar una migración explícita que restaure las políticas de tenant anteriores, documentar el periodo y auditar accesos. No borrar ACL ni ampliar permisos desde Node o frontend.

