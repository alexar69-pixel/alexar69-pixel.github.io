# Evidencia de control de ejecuciones — 01-08-2026

## Resultado

- migración PostgreSQL `013` aplicada sobre PostgreSQL 16.14;
- trabajo pendiente: `CANCELLED` inmediato;
- trabajo reclamado: lease conservado, señal observada y ejecución
  `cancelled` persistida por el worker;
- API autenticada: cancelación 200 y motivo persistido;
- RLS: aislamiento ya validado por organización;
- llamadas OpenAI, Gemini y Ollama: `AbortSignal` propagado;
- 41/41 pruebas backend y build frontend correctos.

## Defecto corregido

El panel calculaba horas y costes ahorrados con constantes sin fuente. Esas
métricas eran resultados inventados y se retiraron. ROI queda como
`DEPENDENCIA_CLIENTE` hasta disponer de un modelo verificable aportado por el cliente.

## Límites

La cancelación es cooperativa. No revierte efectos externos confirmados ni
sustituye la idempotencia del conector. No acredita carga, HA o producción.
