# Implementación OAuth de Gemini — 2026-09-07

## Alcance

Se añadió autorización OAuth 2.0 por usuario para Gemini mediante Google, PKCE
S256, estado PostgreSQL de un solo uso y refresh token cifrado por propietario.
La credencial `gemini_oauth` se usa tanto en el nodo `ai_gemini` como en el
Copiloto, con `Authorization: Bearer` y `x-goog-user-project`. La API key sigue
siendo compatible mediante `x-goog-api-key`.

El consentimiento solicita únicamente
`https://www.googleapis.com/auth/generative-language.retriever`. Se rechazó
durante el diseño el alcance amplio `cloud-platform`; no forma parte de la
implementación.

## Validación local

- Sintaxis de rutas y nodo Gemini: correcta.
- Pruebas OAuth, correo y PDF: 12/12.
- Contratos cubiertos: estado `NO_CONFIGURADO`, API key compatible, Bearer con
  proyecto, refresh token ausente de cabeceras y renovación mediante Google.

No se realizó un consentimiento live porque el despliegue no contiene todavía
client ID, client secret y project ID autorizados. Por tanto, Google Gemini
OAuth permanece `NO_CONFIGURADO` hasta que el operador complete el alta.

Fuente oficial: https://ai.google.dev/gemini-api/docs/oauth
