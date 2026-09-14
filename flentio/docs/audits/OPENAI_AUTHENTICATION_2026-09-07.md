# Autenticación de OpenAI — 2026-09-07

## Hallazgo

La bóveda mostraba **OpenAI (OAuth)** y el backend construía enlaces hacia
endpoints OAuth no documentados como mecanismo público para que una aplicación
externa obtenga acceso de inferencia a la API de OpenAI. La implementación no
era operativa: además dependía de funciones y campos incompatibles con el
repositorio PostgreSQL actual.

## Decisión

La opción se retiró de la interfaz y se desregistraron y eliminaron sus rutas y
artefactos públicos. Flentio ofrece **OpenAI API Key (método oficial)**. La clave
se envía únicamente al backend, se cifra en la bóveda y se valida contra la API
real. No se añadieron valores OAuth simulados ni secretos predeterminados.

La compatibilidad de lectura del tipo histórico `openai_oauth` se conserva
temporalmente para no romper registros existentes, pero Flentio ya no permite
crear nuevas credenciales de ese tipo desde la interfaz ni iniciar un flujo
OAuth no soportado.

## Fuente oficial

La referencia oficial de autenticación indica que la API de OpenAI utiliza API
keys y que deben permanecer en servidor o en un gestor seguro, nunca expuestas
en código cliente:
https://platform.openai.com/docs/api-reference/authentication
