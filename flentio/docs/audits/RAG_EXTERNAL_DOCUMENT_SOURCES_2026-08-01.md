# Evidencia — flujo de documentación externa RAG (01-08-2026)

## Alcance verificado

Se verificaron la migración idempotente, catálogo, normalización segura,
autorización de grupos, cola PostgreSQL, descarga oficial, pipeline de seguridad
e ingesta, API autenticada y representación responsive. No se usaron mocks para
la descarga ni para los estados operativos.

La ampliación de revisión humana aplicó la migración 013 dos veces sin error.
Sobre el tenant técnico `flentio-external-review-validation-v1`, una fuente DORA
recién guardada fue bloqueada antes de encolar; después se persistieron
`approved`, actor `flow-review-validator`, fecha y nota. Esto demuestra la puerta
de ejecución real, no una desactivación visual.

En una segunda validación completa mediante navegador, el usuario técnico local
añadió la plantilla DORA, comprobó que **Lanzar descarga** estaba deshabilitado,
registró una nota, aprobó y lanzó. La ejecución descargó 810.060 bytes y terminó
`completed`. Después se pulsó **Relanzar descarga**: se creó una segunda
ejecución independiente, también `completed`, y el historial conservó ambas.
Los SHA-256 binarios fueron
`f2db95e0e1a45811049e7c16755a6793787e81eb478ad0f7749a0b73bfb35a7b` y
`2b9dd111141a1d75290e56c73661ce4198a23fd44ae8cbcf36397925e430d91a`;
EUR-Lex entregó HTML dinámico distinto, mientras el RAG mantuvo una única versión
documental efectiva con 288 fragmentos.

La ampliación de staging aplicó la migración 014 dos veces sin error. En una
tercera ejecución real, el worker descargó y custodió el original, ejecutó
ClamAV 1.4.5, extrajo 358.366 caracteres y dejó el estado
`awaiting_content_review` sin `ingestion_job_id`. Mientras esperaba, el panel y
la API siguieron mostrando un documento efectivo y 288 fragmentos. El usuario
restauró el original, revisó la evidencia y publicó con nota: se creó un único
trabajo, terminó `completed` y no apareció una versión nueva porque el checksum
textual era idéntico. Una cuarta ejecución se rechazó con nota y quedó
`content_rejected`, con `ingestion_job_id = NULL`; el conocimiento efectivo se
mantuvo intacto.

## Evidencia real

- El catálogo expuso 16 plantillas oficiales versionadas.
- Una descarga DORA desde EUR-Lex obtuvo 810.059 bytes y SHA-256
  `9d994433ae4ed7fbd079439c206fade5144ac04b7b43ad3897be48b75634f01c`.
- La evaluación de seguridad fue
  `bfd61745-5c7f-4a30-a489-a0f87602a908` y la ingesta
  `cf80e4ff-0425-48c2-8b3e-c8a169ef26d4`.
- El resultado `DUPLICADO_SIN_CAMBIOS` confirmó que el original oficial era
  idéntico al ya custodiado; el panel lo presentó correctamente como completado.
- La publicación staged usó SHA-256 binario
  `bbe75962904f1e566cc28b827c41011b84e7d770b915451391b7e7ec81e61edf`
  y SHA-256 textual
  `227007d873a6c0b82278ccdff7ee1fab2ed78725f6fd78e62632afb958a63445`.
  La restauración criptográfica produjo 810.058 bytes y volvió a calcular
  exactamente el hash binario esperado.
- El rechazo staged conservó 810.059 bytes, SHA-256 binario
  `c0c47d28b46c2c9cfdc62834629fbd279b7cb37fb10ca29108a0196608267a0d`
  y el mismo checksum textual, pero la consulta PostgreSQL confirmó ausencia de
  trabajo de ingesta.
- Desde un navegador real se inició sesión, se abrió **Ingesta RAG / Drive**, se
  añadió DORA con el flujo anterior y se observó la transición desde
  `INGESTA ENCOLADA` hasta `COMPLETADA` sin errores de consola.
- Se inspeccionó el panel a 390 × 844: títulos largos, acciones y estados se
  ajustaron sin solaparse. Captura:
  `output/playwright/rag-external-sources-panel-mobile.png`.
- Se repitió la inspección a 1.440 × 1.200; selector, título DORA y acciones se
  mantuvieron dentro de sus tarjetas. Captura:
  `output/playwright/rag-external-sources-panel-desktop.png`.
- El flujo previo de revisión de fuente se comprobó en escritorio y móvil. Su
  ficha de cuatro etapas y dos ejecuciones queda como evidencia histórica en
  `output/playwright/rag-external-review-flow-desktop.png`; controles apilados e
  historial responsive en `rag-external-review-controls-mobile.png` y
  `rag-external-review-history-mobile.png`.
- El staging real antes de decidir está en
  `output/playwright/rag-external-content-staging-desktop.png`; la publicación
  confirmada y el rechazo terminal están en
  `rag-external-content-published-desktop.png` y
  `rag-external-content-rejected-desktop.png`. No hubo errores de consola.
- La prueba visual descubrió que una nota de contenido podía permanecer en el
  estado React al relanzar. Se corrigió vinculando la nota al identificador de
  ejecución. Un relanzamiento posterior mostró el campo vacío y ambos botones
  de decisión deshabilitados hasta introducir una nota nueva. El rechazo final
  dejó `ingestion_job_id = NULL`, 1 documento efectivo y 288 fragmentos.

## Comandos y resultados

```powershell
cd backend
npm test
# 72/72 pruebas superadas

npm run migrate:rag
npm run migrate:rag
# migraciones, incluida 014, aplicadas dos veces sin error

cd ../frontend
npm run build
# compilación correcta; permanece el aviso preexistente de bundle > 500 kB

cd ..
docker compose --env-file backend/.env config --quiet
# configuración válida
```

Las pruebas específicas rechazan IP/host local y concesiones de grupos que no
pertenecen a la identidad. La comprobación de sintaxis de los módulos Node fue
correcta.

## Dictamen y límites

Resultado: **VALIDACIÓN local**. Está demostrada la ejecución funcional de una
fuente oficial y la UI, no el volumen de decenas de miles, HA, SLO, frescura
automática, validez jurídica ni producción bancaria. No hay scheduler periódico,
OCR ni conectores genéricos para portales autenticados/licenciados. Las fuentes
privadas siguen dependiendo de credenciales y permisos aportados por el cliente.
La validación utilizó el mismo usuario técnico para revisión de fuente y
contenido; no acredita segregación de funciones. Cuatro ojos, IdP corporativo y
matriz de roles continúan como `DEPENDENCIA_CLIENTE` previa a producción.

Diseño, operación y rollback: `docs/RAG_EXTERNAL_DOCUMENT_SOURCES.md`.
