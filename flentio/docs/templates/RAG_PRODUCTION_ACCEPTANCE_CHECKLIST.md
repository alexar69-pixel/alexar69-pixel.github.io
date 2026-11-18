# Lista de aceptación productiva del RAG

**Estado:** `PLANTILLA_SIN_DATOS`. Ninguna casilla está preaprobada. Cada
resultado necesita evidencia real, fecha y responsable.

| Puerta | Criterio verificable | Evidencia | Responsable | Resultado |
| --- | --- | --- | --- | --- |
| Alcance | intake, clasificación, regiones y responsables aprobados | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Arquitectura | diagrama y decisiones EXT aprobadas, sin componentes implícitos | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Red/TLS | endpoints privados, egress permitido, TLS y DNS probados | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Identidad | MFA, claims, grupos, revocación y accesos negativos probados | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Secretos | referencias de bóveda, rotación, doble control y logs sin secretos | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| PostgreSQL | versión/pgvector, RLS, roles separados, TLS, pool y réplica probados | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Originales | cifrado, versionado, WORM, legal hold y restauración probados | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Ingesta | ClamAV real, cuarentena, fallo cerrado y actualización de firmas | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Modelos | modelos/versiones, región, privacidad, cuotas y fallo cerrado validados | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Conectores | OAuth, scopes, webhook HTTPS, reconciliación y revocación probados | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Auditoría | outbox entregada con acuse al SIEM/WORM y retención verificada | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Observabilidad | métricas, trazas, alertas, guardias y escalados reciben eventos reales | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Recuperación | restauración PITR aislada cumple el RPO/RTO del BIA y conserva RLS/auditoría | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Rendimiento | latencia, frescura, capacidad y concurrencia se miden contra objetivos aprobados | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Seguridad | análisis, pentest/revisión independiente y excepciones formalmente cerrados | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Privacidad/legal | residencia, DPA, retención, borrado y legal hold aprobados | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |
| Rollback | versión/configuración anterior restaurada sin perder auditoría | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] | [A_CONFIGURAR_POR_TENANT] |

## Dictamen

- Deployment/versión: `[A_CONFIGURAR_POR_TENANT]`
- Fecha: `[A_CONFIGURAR_POR_TENANT]`
- Excepciones y caducidad: `[A_CONFIGURAR_POR_TENANT]`
- Dictamen: `NO_APROBADO` hasta cerrar todas las puertas obligatorias.
- Firmas de Aplicación, Arquitectura, Seguridad, Datos, SOC, Continuidad y
  propietario del servicio: `[A_CONFIGURAR_POR_TENANT]`.

`SIN_DATOS`, `NO_CONFIGURADO`, `NO_DISPONIBLE`, `NO_EVALUADO` y
`DEPENDENCIA_CLIENTE` no son resultados aprobatorios. Las pruebas omitidas no
se interpretan como superadas.

