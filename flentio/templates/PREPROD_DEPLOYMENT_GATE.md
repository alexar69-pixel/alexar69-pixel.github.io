# Plantilla de puerta de despliegue PREPROD

Estado: `DEPENDENCIA_CLIENTE`.

## Evidencias requeridas

- Release inmutable, SBOM y firmas.
- Migraciones verificadas y rollback.
- Configuración desde frontend/bóveda, sin secretos en ficheros.
- Tests unitarios, integración, aislamiento, resiliencia y carga.
- SAST, dependencias, secretos y contenedores sin hallazgos críticos abiertos.
- Backup/restore, SLO/RPO/RTO y observabilidad.
- Aprobaciones segregadas y auditoría exportable.

## Resultado

`READY_FOR_PREPROD_REVIEW` sólo permite revisión. Producción y ejecución R1
permanecen bloqueadas hasta homologación independiente.
