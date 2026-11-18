# Flujos de la presentación pública de Flentio

## Alcance real

El catálogo no-code incluye tres plantillas bajo **Flentio · Flujos de presentación**. Al elegir una plantilla se crea un flujo privado e inactivo para que un editor configure y valide sus dependencias antes de activarlo.

Las plantillas no incorporan credenciales, direcciones de destinatarios, webhooks externos ni datos de negocio. Un estado `NO_CONFIGURADO` es esperado hasta completar la configuración del tenant.

## Recepción y registro de facturas

Ruta lógica: correo IMAP → extracción PDF → RAG financiero → agente con evidencia → aprobación humana.

El scheduler sólo arranca con `EMAIL_TRIGGER_SCHEDULER_ENABLED=true`, y cada nodo exige además `enabled=true`. La credencial se resuelve por propietario y organización desde la bóveda. El trigger consulta mensajes IMAP no leídos, filtra opcionalmente el asunto, exige un adjunto PDF y deduplica por workflow, `UIDVALIDITY` y UID antes de marcar el mensaje como leído.

### Conectar el correo sin contraseña

En **Bóveda de Credenciales**, seleccione **Correo Gmail / Microsoft (OAuth recomendado)**, escriba un nombre descriptivo y pulse **Conectar con Google** o **Conectar con Microsoft**. El proveedor solicita el consentimiento en su propia ventana; Flentio no recibe la contraseña. El permiso renovable queda cifrado, asociado al usuario y disponible para el nodo `email_imap_trigger`.

La autorización usa OAuth 2.0 con PKCE y estado de un solo uso durante diez minutos. Google autoriza IMAP mediante `https://mail.google.com/`; Microsoft solicita `IMAP.AccessAsUser.All`, `offline_access` y `User.Read`. Si el administrador no ha registrado la aplicación OAuth, la interfaz muestra `NO CONFIGURADO`: no existe conexión simulada. La contraseña de aplicación queda únicamente para proveedores heredados sin OAuth.

Cada usuario sólo puede listar, conectar y desconectar sus propias cuentas. Los tokens OAuth no se muestran ni se editan desde la interfaz. Al desconectar Google, Flentio intenta revocar el refresh token antes de retirar la credencial local. Microsoft queda desconectado localmente; la revocación global puede completarse mediante la cuenta o la política corporativa de Entra.

El nodo `extract_pdf` recibe el adjunto Base64, limita el binario a 15 MB, verifica la firma `%PDF-` y extrae texto mediante `pdf-parse`. El correo fuente se limita a 20 MB por defecto. El payload y el adjunto permanecen temporalmente en la cola y expediente de ejecución PostgreSQL bajo RLS; la política de retención del tenant debe contemplar esta carga.

Tras la aprobación, el registro en el ERP o sistema contable permanece `NO CONFIGURADO` hasta disponer de un adaptador real, una credencial de bóveda y el contrato de datos del cliente.

## Respuesta a peticiones normativas

Ruta lógica: webhook → RAG normativo → agente con citas → SMTP.

Entrada mínima: `question`, `requesterEmail` y `requestId`. El RAG sólo recupera documentos autorizados para el tenant. Sin evidencia suficiente no se invoca el modelo; una respuesta con citas inválidas se bloquea. El envío exige una credencial SMTP válida seleccionada desde la bóveda.

## Triaje de alertas de seguridad

Ruta lógica: webhook → RAG de runbooks OKF → agente con evidencia → aprobación humana → Slack o Teams.

Entrada mínima: `alertId`, `service`, `severity`, `summary` y `source`. El agente produce diagnóstico y recomendaciones; no ejecuta remediaciones. La notificación exige un webhook real y sólo continúa tras revisión humana. El backend admite `credential_id`, pero el selector visual de credencial para Slack/Teams permanece `NO DISPONIBLE`; no se considera configuración no-code completa hasta incorporarlo.

## Activación segura

1. Crear el flujo desde la categoría **Flentio · Flujos de presentación**.
2. Revisar la nota roja **NO CONFIGURADO** del lienzo.
3. Para facturas, seleccionar la credencial IMAP, activar el nodo y habilitar el scheduler global. Para los otros flujos, configurar el endpoint webhook y rotar su token.
4. Autorizar el corpus RAG y verificar el aislamiento del tenant.
5. Seleccionar proveedor IA y credenciales de notificación desde la bóveda.
6. Ejecutar en desarrollo con un payload autorizado y revisar citas y auditoría.
7. Crear versión firmada y promover mediante DEV → PREPROD → PROD.
