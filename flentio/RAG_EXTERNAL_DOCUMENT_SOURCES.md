# Descargas de documentación externa para el RAG

## Finalidad y alcance

Este módulo permite que un operador autenticado registre y actualice documentos
oficiales desde **Configuración corporativa → Ingesta RAG / Drive** sin mantener
un script por documento. La descarga es real: no crea contenido de ejemplo ni
marca como publicado un trabajo antes de que el worker, la revisión de contenido
y la ingesta terminen.

El catálogo inicial reutiliza las 16 fuentes públicas versionadas de
`backend/data/rag-public-corpus/catalog.json`. También existe un formulario
modelo para nuevas fuentes EUR-Lex por CELEX o documentos HTTPS alojados en un
dominio previamente aprobado. OCR no forma parte del flujo.

## Recorrido operativo

1. El operador selecciona una plantilla o declara clave estable, autoridad,
   categoría, URL/CELEX, formato y tipo documental. La fuente queda pendiente;
   guardar nunca inicia la descarga.
2. La API valida RBAC, tenant, gobierno documental y grupos del token. La UI no
   puede conceder grupos que la identidad no tenga.
3. Otro usuario autorizado —o el mismo operador en desarrollo— revisa la ficha,
   deja una nota y aprueba o solicita cambios. PostgreSQL registra actor, fecha,
   nota y decisión. Cualquier modificación invalida la aprobación anterior.
4. Sólo una fuente aprobada permite **Lanzar descarga** o **Relanzar descarga**.
   PostgreSQL persiste una ejecución durable bajo RLS. El endpoint
   devuelve inmediatamente; la descarga no ocupa la petición del navegador.
5. Un worker reclama el trabajo con `FOR UPDATE SKIP LOCKED`, valida HTTPS, host,
   redirecciones, MIME y tamaño, descarga los bytes y calcula SHA-256.
6. El pipeline analiza el original con ClamAV, lo cifra y versiona, extrae el
   texto y aplica controles de formato e instrucciones hostiles. La evaluación
   se crea con `defer_enqueue=true`: superar seguridad **no** crea todavía un
   trabajo de ingesta.
7. La ejecución queda en `awaiting_content_review`. El panel muestra proveedor y
   versión del escáner, nivel de riesgo, tamaños, SHA-256 binario y textual, una
   comparación con la versión efectiva, una vista de hasta 12.000 caracteres y
   permite restaurar/descargar el original cifrado con verificación de integridad.
8. Un operador deja una nota obligatoria y elige **Publicar en el RAG** o
   **Rechazar contenido**. Publicar exige que seguridad esté aprobada y encola
   exactamente una ingesta; rechazar persiste actor, fecha y motivo, conserva
   original/evidencia y nunca crea un trabajo de ingesta.
9. El panel conserva todas las ejecuciones. Una publicación duplicada sin cambios
   termina como completada porque confirma que el texto canónico ya presente es
   idéntico; no crea una versión documental artificial. Cada publicación o
   rechazo muestra también actor, fecha y justificación en el historial.

```text
Frontend autenticado -> API/RBAC -> fuente RLS -> revisión humana persistida
                                  -> ejecución RLS -> worker -> HTTPS oficial -> SHA-256
                                  -> ClamAV -> original cifrado/versionado
                                  -> extracción y comparación -> staging
                                  -> decisión humana -> cola de ingesta -> RAG
```

## Alta de una fuente nueva

- Use **EUR-Lex por CELEX** para legislación disponible por identificador CELEX.
- Use **Documento HTTPS** para PDF, HTML, texto o DOCX en un host autorizado.
- La `sourceKey` es el identificador funcional estable. Manténgala para
  actualizaciones del mismo documento; use otra clave cuando se trate de otra
  edición cuya vigencia deba coexistir.
- El título, autoridad, categoría, clasificación, entidad, jurisdicción,
  departamento, vigencia y ACL se conservan como gobierno del documento.
- El nombre de fichero y MIME esperado deben corresponder al recurso real.

Una URL bien formada no basta. Si el dominio no aparece en el panel, un
administrador de infraestructura debe revisar autoridad, licencia, residencia,
disponibilidad y riesgo de red, y añadir exclusivamente su nombre DNS a:

```env
RAG_EXTERNAL_SOURCE_ALLOWED_HOSTS=publications.example-authority.eu
RAG_EXTERNAL_SOURCE_STALE_MINUTES=15
```

La variable acepta una lista separada por comas. No acepta IP, CIDR ni una
allowlist aportada por el navegador. El valor debe llegar tanto al servicio web
como a todos los workers. Tras cambiarlo se reinician esos procesos y se
comprueba que el host aparece en el formulario. Los hosts integrados son
EUR-Lex, European Payments Council, SWIFT e IRS.

## API y permisos

| Ruta | Rol | Resultado |
|---|---|---|
| `GET /api/rag/external-source-templates` | lector RAG | Catálogo instalado y hosts autorizados |
| `GET /api/rag/external-sources` | lector RAG | Fuentes y última ejecución del tenant |
| `GET /api/rag/external-sources/:sourceId/runs` | lector RAG | Historial efectivo, intentos, hash y errores |
| `POST /api/rag/external-sources` | escritor RAG | Valida y guarda una fuente |
| `POST /api/rag/external-sources/import-template` | escritor RAG | Materializa una plantilla para el tenant |
| `POST /api/rag/external-sources/:sourceId/review` | escritor RAG | Persiste aprobación o cambios solicitados |
| `POST /api/rag/external-sources/:sourceId/run` | escritor RAG | Encola o devuelve la ejecución activa |
| `GET /api/rag/external-sources/:sourceId/runs/:runId/original` | lector RAG autorizado | Restaura, verifica y descarga el original exacto |
| `POST /api/rag/external-sources/:sourceId/runs/:runId/content-review` | escritor RAG | Publica o rechaza el staging con nota auditable |
| `POST /api/rag/external-sources/:sourceId/disable` | escritor RAG | Detiene futuras descargas sin borrar evidencia |

Los estados de fuente son `configured`, `syncing`, `operational`, `unavailable`
y `disabled`. Los estados de ejecución son `pending`, `processing`,
`awaiting_content_review`, `ingestion_queued`, `quarantined`,
`content_rejected`, `rejected`, `completed` y `failed`. La revisión de fuente usa
`pending_review`, `approved` y `changes_requested`; la revisión del contenido usa
`pending`, `approved` y `rejected`. La API deriva `completed` cuando el trabajo
de ingesta asociado ha terminado, aunque la fila durable conserve
`ingestion_queued` para representar el handoff.

La comparación es determinista sobre texto extraído: distingue primera versión,
texto idéntico o cambio y calcula prefijo/sufijo común para presentar extractos
«antes/después». No es un diff jurídico o semántico, no sustituye la lectura del
original y puede señalar cambios debidos al HTML dinámico de la autoridad. El
checksum textual permite verificar si el conocimiento normalizado cambió aunque
los bytes de la página sean distintos.

## Seguridad, recuperación y escalado

- La validación de host se repite después de cada redirección y bloquea destinos
  locales o no aprobados. HTTPS sigue siendo obligatorio.
- Sólo se almacenan contextos de identidad y gobierno necesarios; PostgreSQL
  fuerza RLS en fuentes y ejecuciones y audita estado y revisión humana.
- Una única ejecución activa (`pending`, `processing`, staging, cuarentena o
  ingesta en curso) puede existir por fuente. Los errores
  transitorios de red, HTTP 429/5xx y respuestas incompletas se reintentan con
  espera acotada; los errores permanentes quedan visibles.
- `RAG_EXTERNAL_SOURCE_STALE_MINUTES` devuelve a cola un trabajo cuyo worker fue
  interrumpido. El mínimo efectivo es cinco minutos.
- Varios workers pueden reclamar fuentes concurrentemente mediante
  `SKIP LOCKED`. Esto hace horizontalmente escalable la cola, pero la validación
  local no demuestra capacidad, HA ni SLO bancarios.

## Operación, alternativas y límites

La implementación actual es un **flujo revisable y manual bajo demanda**. No existe todavía
un calendario periódico para estas fuentes; la frescura depende de pulsar
**Lanzar/Relanzar descarga** o de una futura política de scheduling auditada. Los portales
con autenticación o licencia —por ejemplo áreas privadas de SWIFT— quedan
`NO_CONFIGURADO` hasta disponer de contrato, cuenta y permisos del cliente.

En desarrollo, el mismo usuario con rol escritor puede revisar la fuente y el
contenido. La segregación obligatoria de cuatro ojos para producción es
`DEPENDENCIA_CLIENTE`: requiere la matriz de funciones, grupos del IdP y política
de excepciones del banco. La aprobación de una cuarentena de seguridad conserva
su permiso específico y no se sustituye por esta revisión editorial.

Opciones arquitectónicas que pueden evaluarse sin cambiar el gobierno RAG:

| Opción | Ventaja | Coste o límite | Estado |
|---|---|---|---|
| Descarga HTTPS oficial | Fuente primaria y trazabilidad directa | Cada autoridad publica y versiona de forma distinta | Implementada |
| Agregador regulatorio contratado | Normalización, alertas y cobertura | Licencia, residencia, subencargados y dependencia contractual | Sin proveedor seleccionado |
| Repositorio corporativo | Aplica el control editorial interno | Requiere credenciales y conector por plataforma | Google Drive disponible; otros futuros |
| Portal autenticado de autoridad | Accede a contenido licenciado | OAuth/API/contrato específicos; no debe automatizarse por scraping | No configurado |

## Rollback

1. Pulse **Deshabilitar** para impedir nuevas ejecuciones. Solicitar cambios
   bloquea el relanzamiento hasta una nueva aprobación. Los documentos ya
   ingeridos, originales, hashes y auditoría se conservan.
2. Si una versión no debe recuperarse, archívela con la API de ciclo de vida;
   no borre filas ni objetos directamente.
3. Para revertir el software, retire primero web y workers que usen el flujo.
   Las migraciones `012_external_document_sources.sql`,
   `013_external_source_review.sql` y `014_external_content_staging.sql` son
   aditivas y pueden quedar sin uso. No elimine columnas/tablas ni originales
   hasta terminar retenciones y confirmar que ninguna instancia las utiliza.
4. El endpoint EUR-Lex anterior se mantiene por compatibilidad durante la
   transición; el frontend nuevo no depende de él.

Evidencia reproducible: `docs/audits/RAG_EXTERNAL_DOCUMENT_SOURCES_2026-08-01.md`.
