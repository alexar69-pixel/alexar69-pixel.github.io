# Evidencia de cierre: integraciones externas

Fecha: 02-08-2026. Alcance: catálogo, runtimes, panel administrativo, gobierno
de proveedores y documentación. Esta evidencia local no acredita conectividad
con infraestructuras de un cliente.

## Resultado verificable

- Catálogo: 29 integraciones.
- Runtimes instalados: 29; no falta ningún loader.
- Formularios dedicados: 29, todos con `DEDICATED_FRONTEND`.
- Validación: los 29 runtimes exponen `testConnection` real.
- Backend: 194/194 pruebas superadas.
- Frontend: build Vite correcto; lint sin errores y con advertencias históricas.
- Navegador: 1440x900 y 390x844 sin errores ni warnings de consola.
- API viva: el listado devolvió 29 integraciones; KMS/HSM permaneció
  `NO_CONFIGURADO` y `PENDIENTE_AUTORIZACION`.
- Gobierno: se autorizó temporalmente `QA Gateway Provider` para KMS/HSM. El
  estado pasó a `AUTORIZADA` pero no se habilitó porque continuaba sin perfil ni
  prueba. La revocación eliminó la aprobación y restauró
  `PENDIENTE_AUTORIZACION`; no quedó perfil ni activación.

Las capturas se conservan en `output/playwright/`:
`external-integrations-desktop.png`, `kms-authorization-desktop.png` y
`kms-authorization-mobile.png`.

## Controles comprobados

Los secretos se referencian por identificador de bóveda y no se incorporan al
perfil. Las integraciones que dependen de una elección del cliente no permiten
guardar, probar o activar antes de una autorización auditada. Autorizar no
equivale a configurar, validar ni activar. La revocación descarga el runtime y
elimina perfil, validación y activación para evitar configuraciones huérfanas.

El Client Integration Gateway v1 verifica tenant, ámbito, desafío, antigüedad,
modo de sólo lectura, capacidades y bindings específicos; rechaza respuestas
incompletas o inconsistentes. El contrato completo está en
`docs/CLIENT_INTEGRATION_GATEWAY_V1.md`.

## Límites y estado operativo

No se usaron endpoints ni credenciales bancarias. OpenAI, Gemini, SIEM,
HelixGPT, KMS/HSM, CyberArk, Vault/PAM genérico y EDR/XDR continúan
`NO_CONFIGURADO` mientras no existan proveedor homologado, endpoint, red,
identidad y credencial aprobados. Las pruebas con servidores efímeros controlados
validan el protocolo y el fail-closed, no disponibilidad, rendimiento ni
aceptación productiva del cliente.

## Rollback

Desactivar una Skill descarga su runtime. Revocar un proveedor dependiente de
autorización elimina aprobación, perfil, prueba y activación del tenant, pero
preserva auditoría. Para retirar el gateway se revierten sus wrappers, loaders y
contrato común; no se deben borrar de forma global ajustes ni evidencias.
