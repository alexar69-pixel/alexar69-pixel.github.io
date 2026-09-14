# Contexto para continuar Flentio con otro asistente de IA

Este archivo permite que una persona continúe el proyecto con sus propias
credenciales de ChatGPT, Codex o Gemini. No sustituye las normas de
`.agents/AGENTS.md`.

## Prompt inicial recomendado

> Trabaja en este checkout de Flentio. Lee completamente `.agents/AGENTS.md`,
> `docs/developers/DEVELOPER_HANDOVER.md`, `CONTRIBUTING.md` y la documentación específica
> de la fase antes de actuar. Inspecciona primero, preserva cambios ajenos, no
> uses mocks en producción ni anuncies integraciones no verificadas. Trabaja una
> fase por vez, ejecuta pruebas y build, actualiza documentación y rollback. No
> elijas proveedores externos regulados ni ejecutes remediaciones sin autorización.
> Usa Prompt Caching siempre que el proveedor y el contrato empresarial lo
> permitan, conservando aislamiento por tenant, versionado, métricas reales y
> fallback sin caché.
> Ningún módulo operativo está terminado sin un cuadro de mando gobernado según
> `docs/DASHBOARD_STANDARD.md`; no fabriques métricas ni estados verdes.

## Hechos que no deben inferirse

- Tener formulario no significa tener adaptador.
- Tener runtime instalado no significa estar configurado o activo.
- Una prueba automatizada con servidor efímero no demuestra conexión bancaria.
- `READY_REVIEW` sólo acredita cobertura mínima de evidencia.
- Correlación temporal no demuestra causalidad.
- `VALIDACIÓN local` no equivale a aceptación productiva, HA, SLO o cumplimiento.
- OAuth personal de ChatGPT/Codex es sólo desarrollo local; producción usa API
  empresarial y bóveda.
- Prompt Caching es una optimización de coste y latencia, no una autorización
  para compartir contexto entre tenants, ampliar retención o omitir controles.

## Forma de informar avances

Indica siempre: comportamiento implementado, evidencia verificada, pruebas,
estado de cada dependencia, limitaciones, riesgos, archivos documentados y
rollback. Evita expresiones como "operativo" o "único" sin evidencia vigente.

## Información que nunca se debe pedir ni copiar

Cookies de ChatGPT, sesiones OAuth, tokens personales, `.env`, claves AES/KMS,
datos de `backend/data`, dumps, contraseñas PostgreSQL o secretos de webhook.
Cada colaborador provisiona los suyos mediante el proceso autorizado.

## Mismo equipo, distinta cuenta de IA

El desarrollador puede conservar el checkout y las credenciales técnicas/cloud
ya instaladas en el equipo, mientras usa su propia cuenta ChatGPT/Codex. El
asistente no debe cerrar, rotar, exportar o modificar credenciales Google Cloud,
service accounts, proyectos o billing salvo petición explícita. Debe tratar el
acceso cloud existente como infraestructura puesta en alcance, comprobar primero
la identidad efectiva mediante operaciones de lectura y nunca imprimir tokens.

Aunque sea técnicamente posible usar una sesión Google del propietario, la
opción auditable es una identidad IAM individual de mínimo privilegio. La cuenta
de IA y la identidad cloud son independientes y no deben fusionarse ni copiarse.
