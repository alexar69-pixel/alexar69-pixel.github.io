# Preparación gobernada M3

Estado: `BLOCKED_NO_EXECUTION`. Esta fase registra evidencia previa; no instala
ni expone un adaptador de ejecución.

## Contrato

Un expediente sólo acepta entorno `PREPROD`, riesgo `R1` y modo
`DISABLED`. Exige identificador de acción y Skill, target y runbook HTTPS,
versión, rollback HTTPS, referencia de credencial efímera, evidencia de game day
y caducidad futura. El contenido queda resumido mediante SHA-256 y aislado por
organización con RLS en la migración `020_m3_readiness.sql`.

Las decisiones pertenecen a tres dominios: Operaciones, Seguridad y Riesgo.
Cada una requiere identidad distinta de la autora, una identidad no puede cubrir
dos dominios y se exige respectivamente uno de estos grupos firmados:

- `m3-operations-approvers`;
- `m3-security-approvers`;
- `m3-risk-approvers`.

La API administrativa sólo permite listar, registrar y decidir. No existe ruta
de ejecución. Incluso con tres aprobaciones el estado continúa
`BLOCKED_NO_EXECUTION` hasta implementar y homologar una única Skill R1 real,
validar credencial efímera, comprobar M2 vigente y ejecutar rollback en PREPROD.

API: `GET|POST /api/admin/m3-readiness` y
`POST /api/admin/m3-readiness/{id}/decision`.

## Rollback

Deshabilitar las rutas administrativas impide nuevos registros. Los expedientes
y decisiones son evidencia de gobierno y no deben eliminarse sin aplicar la
retención aprobada. No hay efecto de infraestructura que revertir porque esta
fase no ejecuta acciones.

La primera Skill técnica es `r1.preprod.restart_workload.v1`. Construye un plan
PREPROD con baseline de réplicas, máximo indisponible, salud, runbook, credencial
efímera y rollback exacto `RESTORE_REPLICA_BASELINE`. Puede validar un recibo de
rollback saludable, pero su función `execute()` falla siempre con
`M3_EXECUTION_BLOCKED` y no existe ruta API de ejecución. Esto valida el contrato
reversible, no una operación sobre infraestructura.
