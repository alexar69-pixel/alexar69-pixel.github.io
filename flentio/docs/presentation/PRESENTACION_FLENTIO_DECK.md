# Guion de Presentación — Motor Visual de Flujos de Trabajo

> Guion reestructurado 100% en torno a la orquestación visual de flujos (Entrada ➔ Procesamiento ➔ Salida) en lugar de un buscador manual.

---

## Diapositiva 1: Visión del Producto
- **Propósito**: Presentar Flentio Platform como un Orquestador de Flujos de Trabajo Sin Código que procesa entradas (correos, peticiones API, eventos) y genera acciones automáticas.

## Diapositiva 2: Arquitectura de Flujo en Flentio
- **Estructura del Flujo**:
  1. Nodo de Entrada (Trigger).
  2. Nodo de Seguridad (Filtro DLP).
  3. Nodo Agente de IA (Evaluación y Citas [E1]).
  4. Nodo de Acción (Salida/Base de Datos).
- **Pantallazo UI**: Ejecución de Cadena de Flujo.

## Diapositiva 3: Flujo de Ejemplo 1 — Recepción y Registro de Facturas
- **Entrada**: Correo con PDF de factura.
- **Acción**: Ocultación de IBAN por seguridad, validación del importe y guardado en base de datos en 0,38s.

## Diapositiva 4: Flujo de Ejemplo 2 — Respuesta a Peticiones Normativas
- **Entrada**: Consulta de cliente o API.
- **Acción**: Evaluación con la cita [E1] de la normativa y envío de respuesta comprobada.

## Diapositiva 5: Flujo de Ejemplo 3 — Triaje de Alertas Técnicas (BMC Helix / SIEM)
- **Entrada**: Evento enviado desde BMC Helix.
- **Acción**: Diagnóstico del agente SecOps y recomendación de mitigación.

## Diapositiva 6: Agent Studio — Creación de Flujos Asistida por Copiloto
- **Propósito**: Permitir a responsables de negocio crear flujos conversando en español con el Copiloto.

## Diapositiva 7: Guía de Configuración y Uso en 4 Pasos
- Elegir Entrada ➔ Conectar Bloques ➔ Probar en Preproducción ➔ Publicar y Ejecutar.

## Diapositiva 8: Entornos de Trabajo (Desarrollo / Preproducción / Producción)
- Control de versiones inmutables con firma SHA-256.

## Diapositiva 9: Custodia e Inmutabilidad de Auditoría
- Registro antialteración de ejecuciones y documentos.

## Diapositiva 10: Capacidad de Carga y Rendimiento Masivo
- 5.000 usuarios activos y 2.500 procesos/segundo con integración BMC Helix por deltas.

## Diapositiva 11: Garantía de Calidad
- 336/336 pruebas automáticas superadas con 100% de éxito.

## Diapositiva 12: Demostración en Vivo y Cierre
- Instrucciones para probar el centro de demostración interactivo.
