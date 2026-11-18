# Centro de Demostración de Flentio

> Los flujos ejecutables con entrada, operación y salida documentadas están en [Flujos reales del entorno demo](DEMO_REAL_WORKFLOWS.md).

## Propósito y frontera

El Centro de Demostración permite presentar el producto sin infraestructura ni
datos de un cliente. Todo el recorrido muestra de forma persistente
`LABORATORIO SINTÉTICO · NO BANCARIO · NO PRODUCCIÓN`. Los acontecimientos son
manifiestos estructurales creados para la demostración; el análisis no está
prefabricado: lo calcula en cada ejecución el motor real de correlación,
contradicciones e hipótesis.

El laboratorio se guarda en `demo_lab_sessions`, separado de alertas, expedientes
y evidencia operacional. RLS exige organización y actor. El resultado declara
`bankingData:false`, `productionData:false` y `executable:false`. No existe ruta
de remediación y el estado visible es siempre `BLOCKED_NO_EXECUTION`.

## Arranque autocontenido

Requisitos: Docker Desktop con Compose y puertos 3000/55432 disponibles.

```powershell
./scripts/start-demo.ps1 -Rebuild
```

El primer arranque genera `.env.demo` con secretos aleatorios y una contraseña
de presentador. El fichero está ignorado por Git y la contraseña no se imprime.
Consúltela localmente sólo cuando vaya a iniciar sesión:

```powershell
Get-Content .env.demo | Select-String '^DEMO_ADMIN_(USERNAME|PASSWORD)='
```

Abra `http://localhost:3000/demo`. Arranques posteriores conservan la sesión y
rotan la contraseña del usuario con el valor actual de `.env.demo`.

Para detener sin perder volúmenes:

```powershell
./scripts/stop-demo.ps1
```

No use `docker compose down -v` salvo que quiera destruir expresamente toda la
pila de laboratorio. Ese borrado no es necesario para restaurar una demo.

## Recorrido recomendado de diez minutos

1. Muestre el aviso no bancario y el bloqueo de ejecución.
2. Abra **Arquitectura**: explique separación, motor real, revisión humana y
   auditoría.
3. Vuelva a **Resumen** y ejecute **Degradación tras despliegue**.
4. Recorra E1–E5 y señale que proximidad temporal no es causalidad.
5. Abra la hipótesis focal. La confianza mostrada es la calculada; una
   contradicción la penaliza.
6. Registre `NEEDS_MORE_EVIDENCE` con un motivo. La revisión es una acción real
   sobre la sesión del presentador.
7. Pulse **Explicar expediente** y resuma qué se ha demostrado.
8. Abra **Integraciones** para distinguir fuentes del laboratorio, runtimes
   disponibles y conectores del cliente todavía `NO_CONFIGURADO`.
9. Prepare **Evidencia contradictoria** y muestre la abstención sin hipótesis.
10. Restaure el laboratorio escribiendo `RESTABLECER LABORATORIO`.

## Escenarios

| Escenario | Comportamiento verificable |
|---|---|
| Degradación tras despliegue | Cambio, telemetría, activo, ITSM y runbook; contradicción de versión |
| Dependencia degradada | CMDB y telemetría producen una candidata de dependencia |
| Incidente conocido | ITSM y runbook producen una candidata sujeta a versión y entorno |
| Señal de seguridad | SIEM sintético y telemetría escalan al SOC sin contención automática |
| Evidencia contradictoria | Versiones incompatibles; contradicción y abstención |

## Restauración y auditoría

La restauración exige una frase exacta, elimina únicamente resultado y revisión
de la sesión demo del actor y conserva el evento de auditoría. No modifica
usuarios, integraciones, expedientes, RAG ni infraestructura. Para repetir sólo
un escenario no hace falta restaurar: **Repetir investigación** recalcula el
resultado sobre el mismo manifiesto y un nuevo instante ancla.

## Limitaciones que deben explicarse

- No demuestra utilidad ni precisión bancarias.
- No representa infraestructura, incidentes o clientes reales.
- No prueba conectividad con Grafana, Jira, Helix, CMDB, SIEM o cloud.
- No acredita HA, DR, RPO/RTO, pentest ni homologación regulatoria.
- La UI puede mostrar el estado de los conectores, pero no los convierte en
  operativos.
- R1/M3 sigue bloqueado incluso después de una revisión favorable.

Conceptos visuales de referencia:
`docs/design/concepts/demo-center-desktop.png` y
`docs/design/concepts/demo-center-mobile.png`.
