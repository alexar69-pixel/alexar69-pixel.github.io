# Evidencia — consumo IA y Prompt Caching

Fecha: 02-08-2026.

- Backend: 231/231 pruebas correctas.
- Frontend: build Vite correcto; panel en chunk diferido independiente.
- API autenticada: esquema `FLENTIO_MODEL_USAGE_DASHBOARD_V1`, estado real
  `SIN_DATOS`, caché `NO_VERIFICADO` y `promptsStored=false`.
- Migración `025` aplicada en Docker demo con RLS forzada y permisos de
  aplicación limitados a `SELECT, INSERT`.
- Navegador real: 1440×1000 y 390×844, sin overflow horizontal ni mensajes de
  consola. Capturas en `output/playwright/model-usage-dashboard-desktop.png` y
  `output/playwright/model-usage-dashboard-mobile.png`.
- Límite: no se ejecutaron llamadas facturables a OpenAI/Gemini. No existe
  evidencia de hit de caché ni ahorro y ambos permanecen `NO_VERIFICADO`.

M3 continúa `BLOCKED_NO_EXECUTION`.
