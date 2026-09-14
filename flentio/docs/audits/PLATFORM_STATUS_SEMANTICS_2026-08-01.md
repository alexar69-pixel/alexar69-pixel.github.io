# Evidencia de semántica operativa — 01-08-2026

## Hallazgos corregidos

El resumen de plataforma contenía porcentajes, tendencias, ubicaciones, riesgos
y estados visuales estáticos sin una fuente operativa. Se retiraron. También se
eliminó el cálculo de ROI basado en constantes.

## Fuentes reales

- PostgreSQL: workflows, ejecuciones, incidentes y trabajos de cola; un cero es
  el resultado real de la consulta por organización.
- CISA KEV: consulta HTTPS al catálogo público, timeout de cinco segundos y caché
  de quince minutos; no se infiere afectación local.
- CPD y certificados: `SIN_DATOS` hasta ejecutar inspecciones autorizadas.
- ROI, gestores PKI y destinos corporativos: `DEPENDENCIA_CLIENTE`.

## Presentación

Las tarjetas se apilan por debajo de 1100 píxeles y reducen márgenes y barra
lateral en pantallas de hasta 640 píxeles para evitar texto solapado. La UI usa
estados explícitos y no sustituye nulos por cero.

## Límites

Esta validación no acredita correlación de vulnerabilidades, cobertura de
activos, carga, HA ni disponibilidad de producción. Esas evidencias requieren
la infraestructura y las fuentes del cliente.
