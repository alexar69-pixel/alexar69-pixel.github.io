# Evidencia de reconciliación WORM — 01-08-2026

## Alcance

Validación local real contra PostgreSQL/pgvector y MinIO. Se usaron originales
ya existentes; no se alteraron retenciones, legal holds o bytes para provocar
resultados.

## Implementación

- migración idempotente `010_worm_reconciliation.sql`;
- cola durable con `SKIP LOCKED`, cursor y recuperación de jobs;
- funciones `SECURITY DEFINER` acotadas al job/tenant y sin contenido;
- comparación de tamaño, ETag, checksums, legal hold y retención;
- endpoints autenticados, tarjeta no-code, métricas y alertas;
- ninguna remediación automática.

## Resultado real y defectos corregidos

| Ejecución | Resultado |
| --- | --- |
| Primera, programada | `completed`, 0 objetos; reveló acceso insuficiente por ACL/RLS |
| Segunda | `failed` con PostgreSQL `22023`; el array JSONB no estaba serializado explícitamente |
| Tercera, corregida | `completed`: 9 escaneados, 9 `MATCH`, 0 divergentes, 0 no disponibles |

Los resultados anteriores permanecen en PostgreSQL y auditoría. RLS se resolvió
con funciones que validan que objeto y job comparten tenant, no con grupos
inventados. El error JSONB se corrigió serializando el array antes de PostgreSQL.

## Verificaciones

- `npm run migrate:rag`: `OPERATIVO`, pgvector 0.8.6.
- `npm run build` en `frontend`: correcto; advertencia no bloqueante por el
  tamaño del bundle existente.
- `npm test`: 60 pruebas ejecutadas, 60 superadas, 0 fallos y 0 omitidas.
- snapshot operacional PostgreSQL: `OPERATIVO`, 0 divergencias WORM, 0 no
  disponibles y ninguna alerta WORM.

## Validación visual

Se utilizó Playwright CLI porque el plugin Browser no estaba disponible. El
flujo `/admin` → **Configuración Global Servidores** → **Operación RAG** mostró
la tarjeta sin overlay ni errores de consola. **Comprobar ahora** presentó la
confirmación de sólo lectura y, tras aceptarla, el tenant técnico vacío mostró
un resultado real `completed`, 0 comprobados y 0 incidencias. El cero procede de
la consulta real de ese tenant, no de la ejecución de 9 originales de otro
tenant. Se comprobaron 1440×1000 y 390×844; la tarjeta no se solapó y el selector
móvil conservó **Operación RAG**. Las capturas quedaron fuera del repositorio y
el servidor aislado de validación en 3001 se detuvo al finalizar.

El proceso local principal se reinició de forma controlada después de la
validación. `http://localhost:3000/api/health` respondió `OPERATIVO` con el nuevo
proceso; por tanto, scheduler, endpoints y frontend actualizados están cargados.

## Rollback y límites

Detener el scheduler no cambia datos remotos. Deben conservarse jobs y
hallazgos. No retirar la migración 010 con evidencia existente. La validación no
acredita AWS, HA, carga ni políticas del cliente. Los estados negativos se
cubren en tests, sin alterar objetos operativos para fabricar divergencias.
