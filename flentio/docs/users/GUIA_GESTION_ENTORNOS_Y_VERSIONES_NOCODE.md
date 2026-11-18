# Guía No-Code: Gestión de Entornos (DEV / PREPROD / PROD) y Versiones

> Para usuarios finales y administradores de negocio: Aprende a probar tus automatizaciones en Desarrollo antes de desplegarlas en Producción.

---

## ¿Cómo funciona el ciclo de vida?

1. **Creación en DEV**: Al crear un nuevo flujo o agente, nace en el entorno **Desarrollo (DEV)** en modo borrador (`v1.0.0-draft`). Aquí puedes realizar todas las pruebas y modificaciones que necesites.
2. **Promoción a PREPROD**: Cuando tu flujo esté listo, pulsa el botón **Promover a Preproducción**. El sistema generará una versión inmutable (`v1.0.0-rc1`) con una firma de seguridad SHA-256. En Preproducción podrás realizar pruebas de homologación con datos de prueba realistas.
3. **Despliegue en PROD**: Tras aprobar las pruebas en Preproducción, el botón **Desplegar en Producción** activará la versión congelada (`v1.0.0`) para operar de forma segura.

---

## Preguntas Frecuentes

**¿Puedo modificar un flujo directamente en Producción?**  
No. Por seguridad y cumplimiento regulatorio, los flujos en Producción están congelados. Si deseas realizar un cambio, haz clic en **Crear Nuevo Borrador en DEV**, realiza los ajustes y vuelve a promover la versión.
