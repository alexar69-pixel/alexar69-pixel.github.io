# Evidencia de salud de infraestructura — 01-08-2026

## Resultado local

- host Windows: lectura operativa de CPU, memoria y uptime;
- volumen `C:`: capacidad, uso y espacio libre leídos mediante `statfs`;
- Docker Desktop 29.6.1: cuatro de cuatro contenedores ejecutándose;
- PostgreSQL 16.14: Plataforma y RAG operativos sobre la misma base física, con
  pools lógicos separados y cero conexiones esperando;
- ClamAV 1.4.5, MinIO y reranker TEI: `OPERATIVO`;
- workers: dos consumidores PostgreSQL activos;
- conectores del tenant: total real `0`, estado `SIN_DATOS`;
- HA, monitorización externa y SLO: `DEPENDENCIA_CLIENTE`.

Los números anteriores son evidencia puntual del entorno local y no valores de
demostración. Cambiarán en cada comprobación.

## Validación

- 46/46 pruebas backend correctas;
- endpoint administrativo autenticado correcto;
- build frontend correcto;
- actualización manual renovó la marca temporal;
- 1440 × 1000 y 390 × 844 sin overflow horizontal;
- cero errores de consola durante el recorrido;
- la etiqueta heredada `SQLite WAL` ya no aparece.

## Límites

No se realizaron estrés, HA, failover, series temporales ni alertas externas.
La revisión visual se ejecutó con Playwright CLI porque el plugin Browser no
estaba disponible.
