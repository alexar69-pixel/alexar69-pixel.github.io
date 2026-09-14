# Lista de aceptación productiva del RAG

**Estado:** `PLANTILLA_SIN_DATOS`. Ninguna casilla está preaprobada. Cada
resultado necesita evidencia real, fecha y responsable.

| Puerta | Criterio verificable | Evidencia | Responsable | Resultado |
| --- | --- | --- | --- | --- |
| Alcance | intake, clasificación, regiones y responsables aprobados | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Arquitectura | diagrama y decisiones EXT aprobadas, sin componentes implícitos | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Red/TLS | endpoints privados, egress permitido, TLS y DNS probados | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Identidad | MFA, claims, grupos, revocación y accesos negativos probados | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Secretos | referencias de bóveda, rotación, doble control y logs sin secretos | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| PostgreSQL | versión/pgvector, RLS, roles separados, TLS, pool y réplica probados | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Originales | cifrado, versionado, WORM, legal hold y restauración probados | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Ingesta | ClamAV real, cuarentena, fallo cerrado y actualización de firmas | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Modelos | modelos/versiones, región, privacidad, cuotas y fallo cerrado validados | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Conectores | OAuth, scopes, webhook HTTPS, reconciliación y revocación probados | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Auditoría | outbox entregada con acuse al SIEM/WORM y retención verificada | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Observabilidad | métricas, trazas, alertas, guardias y escalados reciben eventos reales | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Recuperación | restauración PITR aislada cumple el RPO/RTO del BIA y conserva RLS/auditoría | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Rendimiento | latencia, frescura, capacidad y concurrencia se miden contra objetivos aprobados | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Seguridad | análisis, pentest/revisión independiente y excepciones formalmente cerrados | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Privacidad/legal | residencia, DPA, retención, borrado y legal hold aprobados | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |
| Rollback | versión/configuración anterior restaurada sin perder auditoría | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE | PENDIENTE_CLIENTE |

## Dictamen

- Deployment/versión: `PENDIENTE_CLIENTE`
- Fecha: `PENDIENTE_CLIENTE`
- Excepciones y caducidad: `PENDIENTE_CLIENTE`
- Dictamen: `NO_APROBADO` hasta cerrar todas las puertas obligatorias.
- Firmas de Aplicación, Arquitectura, Seguridad, Datos, SOC, Continuidad y
  propietario del servicio: `PENDIENTE_CLIENTE`.

`SIN_DATOS`, `NO_CONFIGURADO`, `NO_DISPONIBLE`, `NO_EVALUADO` y
`DEPENDENCIA_CLIENTE` no son resultados aprobatorios. Las pruebas omitidas no
se interpretan como superadas.

