# Evidencia del portal documental — 05-09-2026

## Alcance implementado

- Ruta pública `GET /docs` y alias `/documentation`.
- Corpus compilado desde `docs/**/*.md`, documentos raíz, Skills documentales y
  el paquete OKF, sin leer `.env`, datos locales ni credenciales.
- Navegación por audiencia, búsqueda de texto, lector Markdown y diseño
  responsive.
- Preguntas extractivas locales: recuperan fragmentos del corpus, muestran sus
  fuentes y se abstienen cuando no encuentran evidencia suficiente.
- Acceso desde la portada de Flentio.

El asistente no invoca un LLM, no genera hechos nuevos y no presenta sus
fragmentos como asesoramiento. El lector debe abrir las fuentes antes de tomar
una decisión operativa o contractual.

## Validación

| Comprobación | Resultado |
|---|---|
| Corpus visible en navegador | 149 documentos antes de generar esta acta; el build final indexa 150 incluyéndola |
| Pregunta sobre preparación productiva | Recuperó primero `docs/SECURITY.md` y su bloqueo explícito |
| Viewport escritorio | 1440 × 900, cuatro áreas visibles |
| Viewport móvil | 390 × 844, lector visible y asistente bajo botón `Preguntar` |
| Consola del navegador | 0 errores, 0 avisos de aplicación |
| Build Vite | Correcto; el corpus produce un chunk documental grande conocido |
| Imagen Docker de demostración | El builder copia explícitamente el corpus público; `/docs` no depende de archivos del host en runtime |
| Lint | Código de salida 0; permanecen avisos preexistentes fuera del portal |

Capturas locales de comprobación: `output/playwright/documentation-desktop.png`
y `output/playwright/documentation-mobile-final.png`. `output/` está ignorado y
no constituye evidencia versionada.

## Seguridad y privacidad

La ruta es pública. Antes de añadir un Markdown al corpus, su autor debe
confirmar que puede ser visible para clientes y usuarios. No se indexan
`.agents/`, archivos de entorno, datos runtime ni secretos. Si en el futuro se
incorpora documentación clasificada, deberá separarse en una API autenticada con
RBAC/RLS; no se añadirá al bundle público.

El `Dockerfile` copia a la etapa de compilación `docs/`, `okf-bundle/`,
`backend/src/skills/` y los Markdown raíz seleccionados. El runtime recibe sólo
los assets compilados, no esas fuentes ni directorios adicionales.

## Limitaciones y rollback

- La búsqueda es léxica y local, no semántica.
- La representación Markdown prioriza lectura simple; no ejecuta HTML embebido.
- Incluir el corpus completo aumenta el tamaño del chunk de `/docs`; la ruta se
  carga de forma diferida y no aumenta el bundle inicial.

Rollback: retirar las rutas `/docs` y `/documentation`, los accesos de portada y
el componente. No es necesaria una migración ni se modifican datos persistidos.
