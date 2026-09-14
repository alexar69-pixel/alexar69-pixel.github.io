# Evidencia del producto de presentación — 2026-08-02

## Resultado

El Centro Demo es reproducible sin cliente y conserva límites verificables:
datos sintéticos no bancarios, cinco escenarios versionados, análisis mediante
el motor real de hipótesis y contradicciones, revisión humana y ejecución
operacional bloqueada. Este resultado no valida utilidad bancaria, proveedores
externos ni comportamiento sobre producción.

## Aislamiento y seguridad

- Marcador inmutable: `FLENTIO_SYNTHETIC_NON_BANKING_DEMO_V1`.
- Sesiones separadas por la migración `024_demo_lab_sessions.sql`.
- RLS forzada por organización y actor.
- Resultado contractual: `bankingData=false`, `productionData=false`,
  `executable=false` y `BLOCKED_NO_EXECUTION`.
- No existe endpoint de ejecución o remediación para el laboratorio.
- Reinicio destructivo de la sesión protegido por la frase exacta
  `RESTABLECER LABORATORIO` y registro de auditoría.
- Jira, Helix, Grafana, Vault y proveedores IA permanecen `NO_CONFIGURADO`.

## Verificación técnica

| Control | Resultado |
| --- | --- |
| Backend | 223/223 pruebas correctas |
| Frontend | build de producción correcto |
| Lint | sin errores; advertencias históricas documentadas |
| Navegador | flujo ejecutar-revisar-explicar-pestañas-reiniciar correcto |
| Consola navegador | cero errores y cero advertencias durante el flujo |
| Responsive | 1536x1024 y 390x844, sin desbordamiento horizontal móvil |
| Migración | aplicada idempotentemente en PostgreSQL local |
| Stack limpio | imagen reconstruida, PostgreSQL saludable y aplicación estable |
| Autenticación | usuario demo admin válido; token inválido rechazado con HTTP 403 |

## Fidelidad visual

Se contrastó la implementación con
`docs/design/concepts/demo-center-desktop.png` y
`docs/design/concepts/demo-center-mobile.png`: jerarquía del encabezado,
aviso sintético permanente, carril de escenarios, línea temporal, inspector de
hipótesis, navegación móvil y confirmación de reinicio. La desviación deliberada
es la confianza: el concepto ilustraba 72 %, mientras el motor real devuelve
55 % tras penalizar evidencia contradictoria. También se muestran E1 y E2 como
soporte y E4 como contradicción, en vez de convertir E4 en respaldo. No se
alteraron los resultados para aproximarlos al concepto.

La automatización visual se realizó con Playwright porque el plugin Browser no
estaba disponible. Las capturas finales se conservan como evidencia de release.

## Arranque y rollback

`scripts/start-demo.ps1 -Rebuild` crea secretos criptográficamente aleatorios en
`.env.demo`, levanta PostgreSQL con pgvector, aplica migraciones, crea o rota el
usuario demostrador y arranca la aplicación. `scripts/stop-demo.ps1` detiene el
stack sin eliminar volúmenes. Para rollback completo se detiene el stack y se
retira únicamente el entorno demo; no se deben reutilizar su base ni sus
credenciales en producción.

La primera construcción limpia reveló que Alpine no encontraba un binario musl
precompilado de `better-sqlite3`. Se corrigió usando Node 22 y un toolchain
efímero de compilación nativa, eliminado de la imagen final. También se añadió
`.dockerignore` para excluir secretos, dependencias, datos y artefactos locales.
La evidencia de arranque que figura en este documento corresponde únicamente a
la reconstrucción posterior a esa corrección.

La primera ejecución de esa imagen expuso además que `helmet`, importado por el
servidor, figuraba como dependencia de desarrollo y quedaba fuera de `npm ci
--omit=dev`. Se reclasificó como dependencia productiva antes de repetir el
arranque limpio.

El siguiente arranque fue correctamente rechazado por la política PostgreSQL al
no recibir `ENCRYPTION_KEY`. El iniciador ahora genera una clave hexadecimal de
32 bytes, la añade a ficheros `.env.demo` anteriores sin rotar otros secretos y
la inyecta en el contenedor. No se imprime su valor.

El registro de rutas reveló que la exclusión inicial de `backend/data` también
retiraba el catálogo público versionado requerido por el módulo RAG. La regla
final admite exclusivamente `backend/data/rag-public-corpus/catalog.json`; las
bases, claves y restantes datos locales siguen excluidos.
