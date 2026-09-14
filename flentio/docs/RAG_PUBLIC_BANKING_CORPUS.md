# Corpus público bancario del RAG

## Objetivo y alcance

Este corpus aporta conocimiento normativo y operativo público para desarrollar y medir el RAG sin utilizar datos de clientes. No contiene expedientes, contratos, políticas internas, mensajes de pago ni datos personales de una entidad. Por ello sirve para ingeniería de recuperación y citas, pero no acredita que Flentio interprete correctamente una obligación jurídica concreta ni sustituye el corpus privado que entregue cada banco.

El catálogo versionado está en `backend/data/rag-public-corpus/catalog.json`. Cada entrada declara autoridad, URL oficial, identificador estable, formato, vigencia, categoría y estado de acceso. Las preguntas sólo etiquetan la fuente documental esperada: `ENGINEERING_SOURCE_SCOPE_NOT_LEGAL_HUMAN_JUDGMENT`.

El mismo catálogo alimenta ahora el selector **Descargas documentales oficiales**
del frontend. Un operador puede materializar una plantilla o registrar una
fuente nueva mediante el modelo HTTPS/CELEX. Guardar la deja pendiente de
revisión; sólo una aprobación humana persistida permite lanzarla o relanzarla.
La descarga queda en staging después de ClamAV, custodia y extracción: una
segunda decisión humana, con nota y evidencia visible, publica o rechaza el
contenido. Rechazar no crea un trabajo ni altera el documento efectivo.
Este camino no
modifica la definición reproducible del corpus ni sustituye su arnés de calidad.
Detalle: `docs/RAG_EXTERNAL_DOCUMENT_SOURCES.md`.

## Contenido público incorporado

- EUR-Lex: DORA, RGPD, AI Act, NIS2, PSD2, Reglamento SEPA, Reglamento de transferencias inmediatas y Reglamento europeo PBC-FT.
- European Payments Council: SCT Rulebook 2025 v1.1, guías ISO 20022 Customer-to-PSP e Inter-PSP, códigos de motivo de R-transactions y aclaraciones SCT/SCT Inst.
- IRS: Publication 5190, guía de uso de IDES para FATCA.
- SWIFT: página pública actual de MyStandards y CBPR+ User Handbook SR 2023 como referencia histórica expirada.

Fuentes maestras: [EUR-Lex](https://eur-lex.europa.eu/), [rulebook SCT vigente del EPC](https://www.europeanpaymentscouncil.eu/document-library/rulebooks/2025-sepa-credit-transfer-rulebook-version-11), [SWIFT MyStandards](https://www.swift.com/products/mystandards) y [FATCA IDES User Guide del IRS](https://www.irs.gov/pub/irs-pdf/p5190.pdf).

El handbook CBPR+ SR 2023 se descarga desde SWIFT para conservar evidencia histórica, pero tiene `effectiveUntil` y queda `expired`; no participa en consultas actuales. Las especificaciones CBPR+ vigentes de MyStandards y la documentación de cliente de Knowledge Centre permanecen `NO_CONFIGURADO`: requieren cuenta swift.com y permisos/licencia del cliente. Flentio no descarga copias de terceros ni elude esos controles.

## Descarga e ingesta real

`npm run validate:rag-public-corpus` realiza el recorrido completo:

1. exige `RAG_PUBLIC_CORPUS_CONFIRM=YES_OFFICIAL_PUBLIC_SOURCES`;
2. sólo admite HTTPS y una lista cerrada de autoridades oficiales;
3. valida el host final después de redirecciones, MIME y límite de 15 MB;
   los fallos transitorios de red, HTTP 429 y HTTP 5xx se reintentan como máximo tres veces; 401/403 y formatos inválidos fallan inmediatamente;
4. calcula SHA-256 de los bytes y, para HTML dinámico, otra huella del texto canónico indexable; evita reingestas sin cambio documental;
5. pasa cada original por ClamAV, extracción real de HTML/PDF, cifrado AES-256-GCM y almacenamiento versionado;
6. fragmenta, genera embeddings reales y conserva origen, extractor y vigencia;
7. compara recuperación híbrida y TEI con Recall@K, MRR, nDCG, precisión, precisión de citas y latencias.

No se guarda una copia en Git: el original cifrado vive en el almacén configurado y la evidencia/checksum vive en PostgreSQL. El HTML se conserva como original, pero scripts y estilos se eliminan antes de indexar. No se utiliza OCR.

## Configuración local

```powershell
cd backend
$env:RAG_PUBLIC_CORPUS_CONFIRM='YES_OFFICIAL_PUBLIC_SOURCES'
$env:RAG_PUBLIC_CORPUS_ORGANIZATION='flentio-public-quality-v1'
$env:RAG_PUBLIC_CORPUS_RERANKER_BATCH_SIZE='5'
npm run validate:rag-public-corpus
```

Si una autoridad está temporalmente indisponible, puede medirse sólo el ranking sobre
originales ya verificados con `RAG_PUBLIC_CORPUS_SOURCE_MODE=verified-local`. El comando
falla si falta una fuente lista/verificada y muestra hashes y fechas conservadas. Este
modo no comprueba actualidad remota y nunca debe describirse como descarga nueva. El
valor predeterminado `refresh` sí vuelve a consultar todas las autoridades.

El arnés conserva 40 candidatos y limita cada petición a cinco fragmentos. Se fijó después de observar HTTP 429 real de TEI con un lote único de 40 en la GPU de desarrollo. El runtime usa `RAG_RERANKER_CANDIDATES` y `RAG_RERANKER_BATCH_SIZE`; cada despliegue debe medir su propia capacidad. El error 429 nunca se convierte en una puntuación y la consulta sigue fallando cerrada.

La v3 amplió cada canal a 160 entradas, diversificó 40 candidatos entre documentos y mantuvo lotes de 5. Sobre los 16 originales verificados obtuvo Recall@K 1,0000, MRR 0,96875, nDCG 0,97693, precisión/citas 0,7250 y p95 candidato 878 ms, con cero reintentos. El resultado corrige los tres fallos EPC de v2, pero sigue siendo una muestra pequeña sin validación jurídica ni de escala.

El comando también exige que Ollama y el modelo de embeddings configurado estén disponibles. Si el endpoint cae, la evaluación falla; no reutiliza vectores inventados. Tras reiniciar Ollama conviene ejecutar una consulta de calentamiento antes de tomar latencias como línea base.

## Actualización, gobierno y rollback

- Actualizar una URL o versión exige modificar el catálogo y conservar un nuevo `sourceKey`; una versión histórica debe recibir `effectiveUntil`.
- Repetir el comando captura cambios reales, crea procedencia y vuelve a medir. Un PDF binariamente idéntico o un HTML con texto canónico idéntico queda `SKIPPED_UNCHANGED`; cambios de plantilla de EUR-Lex no crean una versión normativa.
- Revisar cambios regulatorios requiere propietario, calendario y aprobación jurídica del cliente; este script no determina vigencia legal por inferencia.
- Para detener futuras sincronizaciones, no se programa el comando. Para retirar una fuente de recuperación, se archiva mediante la API gobernada; no se borra el original ni se manipula PostgreSQL directamente.
- Revertir el código elimina el catálogo/descargador y restaura el evaluador anterior. Los documentos ya ingeridos se conservan hasta una decisión de retención autorizada.

## Límites

La validación pública usa 16 consultas y no es una prueba de estrés, de HA, de SLO ni de exactitud jurídica. La fidelidad permanece `NO_EVALUADA` al no existir jueces humanos/juristas. El corpus privado de políticas, procedimientos, productos, matrices de control y guías SWIFT autorizadas debe ser aportado y gobernado por cada cliente.
