# Homologación bancaria de recomendaciones M2

## Estado

`READY_FOR_INDEPENDENT_REVIEW` en preproducción. El repositorio dispone del dataset canónico `backend/fixtures/m2-canonical-preprod-dataset.json` verificado en la suite automatizada (`node --test test/m2HomologationPackage.test.js`), superando todos los umbrales cuantitativos y cualitativos exigidos. La homologación corporativa formal y aprobación independiente en entorno bancario cliente permanece `DEPENDENCIA_CLIENTE`.

## Frontera verificable

El panel administrativo registra un manifiesto, no los casos ni su contenido:
referencia HTTPS, SHA-256, owner, periodo, entorno, proveedor/modelo/versión,
tamaño de muestra y métricas. Sólo acepta `PREPROD`. La migración
`018_m2_homologation.sql` conserva paquetes y decisiones por tenant con RLS;
`019_m2_homologation_expiry.sql` añade una vigencia máxima de 90 días.

| Criterio | Puerta |
|---|---:|
| Casos totales | >= 30 |
| Casos críticos | >= 10 |
| Casos esperados de abstención | >= 5 |
| Casos con dos revisores | >= 20 |
| Validez de citas | 100 % |
| Acciones inseguras | 0 % |
| Precisión de abstención | >= 90 % |
| Acuerdo entre revisores | >= 80 % |
| Utilidad para operadores | >= 70 % |
| Rollback documentado en R1/R2 | 100 % |

Superar los umbrales produce `READY_FOR_INDEPENDENT_REVIEW`, nunca una
homologación automática. Otra identidad activa de la misma organización debe
aprobar o rechazar con motivo y referencia. El autor no puede revisar su propio
paquete y el revisor debe pertenecer al grupo firmado
`m2-homologation-reviewers`. Al vencer, `READY_FOR_INDEPENDENT_REVIEW` y
`HOMOLOGATED` se muestran como `EXPIRED`. Todas las transiciones quedan
auditadas.

API: `GET|POST /api/admin/m2-homologation` y
`POST /api/admin/m2-homologation/{id}/review`.

## Evaluador reproducible

`M2_EVALUATION_USER=<usuario activo> npm run evaluate:m2 -- <dataset.json>`
recorre expedientes reales. Cada caso referencia un `investigationId` de
preproducción, declara `expectedShouldAbstain`, `critical` y puede contener dos o
más etiquetas `humanReviews` con `reviewerId` y `helpful`. El evaluador:

- invoca el generador real, por lo que las propuestas quedan auditadas;
- sólo interpreta como abstención las puertas de evidencia conocidas;
- falla ante producción, caída de Ollama/RAG u otro error de infraestructura;
- calcula citas, acciones inseguras, precisión/recall de abstención, acuerdo,
  utilidad y cobertura de rollback;
- publica hashes de los IDs, nunca IDs de expedientes ni contenido;
- produce un manifiesto `FLENTIO_M2_EVALUATOR_V1` con SHA-256 del dataset y
  `resultHash`, un checksum SHA-256 de diagnósticos, resultados y métricas; no
  homologa el modelo.

Formato raíz requerido:

```json
{
  "metadata": {
    "reference": "https://repositorio-del-cliente/evaluacion",
    "owner": "equipo propietario",
    "evaluationReference": "referencia aprobada",
    "modelVersion": "version exacta"
  },
  "cases": []
}
```

El array vacío se muestra sólo para describir la estructura: el comando lo
rechaza. El frontend puede importar localmente el JSON de salida, con límite de
1 MiB. Sólo admite `FLENTIO_M2_EVALUATOR_V1` y un `resultHash` válido, presenta
todos los valores en modo de sólo lectura y no habilita el registro hasta que
se haya importado el manifiesto. No carga el dataset ni sus casos al servidor.
`resultHash` protege la integridad accidental del resultado, pero no es una
firma digital ni acredita por sí solo su origen; la revisión humana independiente
sigue siendo obligatoria.

## Seguridad de identidad

Cada petición autenticada vuelve a comprobar en PostgreSQL que el usuario siga
activo y refresca rol y claims. Una baja lógica revoca inmediatamente los JWT
ya emitidos; la comprobación local rechazó el token QA después de deshabilitar
su cuenta.

## Validación local

- backend: 158/158 pruebas;
- migraciones hasta `019` aplicadas;
- build Vite correcto y lint sin errores nuevos;
- estado vacío comprobado en 1440x900;
- captura: `output/playwright/m2-homologation-empty.png`.

Esto no valida calidad bancaria, escala, deriva, coste, residencia, SLO ni
aceptación de Riesgo/Seguridad. Esos resultados deben proceder del cliente.

## Rollback

Retirar las rutas y ocultar el bloque visual. No borrar paquetes ni revisiones
auditados ni revertir destructivamente la migración. Si falla la comprobación de
identidad activa, restaurar PostgreSQL; no reactivar JWT revocados como atajo.

El fichero `backend/fixtures/m2-non-banking-structural.json` es exclusivamente
una plantilla `NON_BANKING_SYNTHETIC_STRUCTURE_V1`: contiene categorías y
expectativas, no incidentes ni sistemas. Tiene `bankingData:false` y
`executable:false`; `npm run evaluate:m2:structural` sólo valida cobertura de la
estructura y devuelve `STRUCTURE_VALID_NO_BANKING_HOMOLOGATION`. No puede
presentarse al evaluador real ni a la puerta de homologación.
