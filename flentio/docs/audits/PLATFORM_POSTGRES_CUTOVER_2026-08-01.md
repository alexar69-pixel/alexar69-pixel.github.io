# Evidencia del corte PostgreSQL de plataforma — 01-08-2026

## Alcance

Validación local funcional, no prueba de estrés, HA ni certificación bancaria.
No se usaron datos de clientes. Las identidades creadas por validadores se
etiquetan como validación técnica, se deshabilitan y conservan únicamente la
raíz necesaria para la auditoría append-only.

## Resultados observados

- PostgreSQL `16.14` y pgvector `0.8.6`: `OPERATIVO`.
- Los cuatro selectores de plataforma están en `postgres`.
- SQLite operativo: `DESACTIVADO`, módulo `loaded=false`.
- Worker de workflows: dos consumidores; scheduler PostgreSQL.
- Worker de outbox activo; transporte externo `NO_CONFIGURADO`.
- Cadena SHA-256 válida; cuatro escrituras concurrentes quedaron en secuencias
  consecutivas 22–25.
- RLS aisló dos organizaciones; sin contexto se observaron cero filas.
- Dos workers reclamaron dos filas distintas con `SKIP LOCKED`.
- Identidad API: registro 201, bcrypt/JWT, ajustes, credenciales y OAuth reales.
- Orquestación API: CRUD/versiones, catálogo, ejecución, webhook 202,
  deduplicación y finalización por worker.
- Authorization no se persistió en la cola.
- Self-healing y backup: HTTP 501 `NO_CONFIGURADO`.
- Backend: 40/40 pruebas; ambas auditorías npm: 0 vulnerabilidades publicadas.

## Defectos encontrados y corregidos

1. `pgcrypto.digest` no resolvía con `search_path=''`; `010` lo cualificó.
2. El trigger append-only bloqueaba el backfill; `011` limita su desactivación a
   la transacción privilegiada.
3. Timestamp/UUID no ordenaban la cadena concurrente; `012` reconstruyó el
   orden siguiendo `parent_hash`.
4. `.env` se cargaba tarde y abría SQLite; se adelantó y health verificó el
   corte real.
5. Copilot, self-healing, swarm, KYC/AML, SEPA, SQL, métricas y parches antiguos
   podían anunciar resultados prefabricados; ahora recuperan RAG real o fallan
   explícitamente.
6. El Copiloto ofrecía un selector de modelos y sugerencias de mutación que su
   API no ejecutaba; se redujo a recuperación RAG real sin generación.
7. La barra del editor excedía el viewport en 48 px por sumar relleno a un ancho
   del 100 %; se corrigió con `box-sizing: border-box`.
8. El portal administrativo fallaba si la telemetría omitía familias de
   descubrimientos; ahora normaliza campos ausentes a valores neutros sin
   inventar observaciones.

## Validación visual y funcional

- editor y Copiloto: consulta real, `EVIDENCIA_INSUFICIENTE`, cero errores de
  consola y cero desbordamiento horizontal;
- catálogo: capacidades no implementadas deshabilitadas con `NO CONFIG.`;
- RAG ingesta: 1889, 768 y 390 px sin solapamientos ni overflow horizontal;
- RAG operación: 390 px, métricas reales de una consulta y cero resultados;
- portal administrativo: carga completa aun cuando CPD no informa subdominios,
  endpoints o dispositivos.

Las capturas se conservaron fuera del repositorio como artefactos temporales de
QA; no forman parte del producto ni representan datos de clientes.

## Límites abiertos

- bóveda local no apta para varios nodos hasta elegir KMS/secret manager;
- backup/PITR/restauración y SIEM/WORM externo no configurados;
- SSO, revisión independiente y BIA pendientes;
- sin prueba de carga, HA, failover ni acreditación SLO/RPO/RTO;
- scripts requieren aislamiento externo real antes de habilitarse.

## Conclusión

El corte operativo está completado en desarrollo y preparado para procesos
múltiples. No habilita producción bancaria ni HA y no sustituye puertas externas.
