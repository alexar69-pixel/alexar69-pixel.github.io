# F2 — Evidencia de seguridad de ingesta

## Resultado

Estado: **VALIDACIÓN**. Las puertas funcionales F2 se superaron en un entorno efímero real. No equivale a certificación bancaria: quedan revisión independiente, pruebas de carga/HA, corpus representativo e integración con SOC/IdP corporativos.

## Entorno observado

- PostgreSQL 16 + pgvector 0.8.6 en `pgvector/pgvector:pg16`.
- ClamAV `1.4.5`, base `28078`, fecha informada `Fri Jul 31 06:24:10 2026`, imagen fijada `clamav/clamav:1.4`.
- Ollama real con `nomic-embed-text`, 768 dimensiones.
- Puertos loopback temporales: PostgreSQL 55435 y ClamAV 53310.
- Tenants UUID independientes y grupo `rag-security-approvers` firmado en contexto servidor.

## Pruebas y evidencia

| Prueba | Resultado observado |
|---|---|
| Migración ejecutada dos veces | `OPERATIVO`, pgvector 0.8.6; idempotente |
| Contenido limpio por `INSTREAM` | `stream: OK` |
| EICAR estándar controlado | `Eicar-Test-Signature FOUND`; evaluación `rejected`; ningún job |
| Prompt hostil ES | códigos `IGNORE_INSTRUCTIONS` y `SYSTEM_PROMPT_EXTRACTION`; `quarantined` |
| Clasificación `RESTRICTED` | `quarantined` hasta aprobación humana |
| Usuario sin grupo aprobador | `RAG_APPROVAL_FORBIDDEN` |
| Dos aprobaciones concurrentes | mismo UUID de job; una sola indexación |
| Documento limpio y documento aprobado | ambos jobs `completed` con embeddings Ollama reales |
| Segundo tenant | cero evaluaciones visibles |
| Eventos | `received → scanning → rejected/quarantined/approved → indexed`, con actor y motivo |
| DOCX expansivo | rechazado por relación de compresión |
| ZIP renombrado DOCX | rechazado por ausencia de `word/document.xml` |
| Tests backend | 18/18 superados |
| Dependencias backend | `npm audit --omit=dev`: 0 vulnerabilidades |
| Frontend | compilación Vite superada; lint sin errores, con advertencias preexistentes |

El artefacto EICAR se construyó sólo en memoria durante la prueba y no se incorporó al repositorio. El entorno no usó datos productivos ni mocks. La base efímera se elimina después de documentar la validación.

## Controles implementados

- scanner real que falla cerrado y registra versión, resultado y firma;
- análisis anterior a PDF/DOCX y sin escritura del original;
- tamaño, páginas, ZIP entries, expansión y ratios acotados;
- reglas deterministas versionadas de prompt injection;
- cuarentena, cuatro ojos, idempotencia concurrente y trazabilidad PostgreSQL;
- RLS por tenant/creador/aprobador;
- interfaz no-code para estado, hallazgos, aprobación y rechazo.

## Riesgos abiertos

| Riesgo | Responsable propuesto | Cierre requerido |
|---|---|---|
| ClamAV es instancia única | Plataforma/SRE | réplicas, balanceo, prueba de pérdida y SLO |
| No hay sandbox ni CDR | CISO/Arquitectura | análisis de riesgo y selección de motor adicional si procede |
| IdP corporativo no integrado | IAM | OIDC/SAML real y mapeo del grupo aprobador |
| Límites sin carga bancaria representativa | Rendimiento | corpus autorizado, stress y tuning |
| Sin integración SOC/SIEM | SecOps | eventos/alertas, runbook y retención aprobada |
| Validación no independiente | Seguridad | pentest y revisión de arquitectura/código |
