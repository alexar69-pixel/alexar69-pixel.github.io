# Cuadro de mando de consumo de IA y Prompt Caching

## Objetivo y alcance

El módulo administrativo `ai_usage` muestra consumo observado de OpenAI y Gemini por organización y ventana temporal (24 horas o 7 días). Se alimenta exclusivamente de los contadores que devuelve el proveedor tras una llamada real.

No almacena prompts, respuestas, credenciales ni contenido del cliente. La tabla es append-only para el rol de aplicación, aplica RLS forzada y registra proveedor, modelo, tokens, latencia, resultado y fecha.

## Semántica operacional

- `OBSERVED`: existe una respuesta real con contadores declarados por el proveedor.
- `SIN_DATOS`: no hay observaciones para la organización y ventana seleccionadas.
- `NO_VERIFICADO`: el proveedor no devolvió el detalle de caché o no existe todavía una tarifa contractual aprobada.
- `NO_DISPONIBLE`: no se pudo consultar o persistir la telemetría.

Un valor ausente nunca se transforma en cero. Los ahorros económicos permanecen `NO_VERIFICADO` hasta configurar precios contractuales versionados. El panel no habilita acciones ni cambia la prohibición física de M3.

## API y operación

`GET /api/admin/model-usage-dashboard?hours=24` requiere acceso administrativo. Sólo admite ventanas de 24 o 168 horas; cualquier otro valor se reduce de forma segura a 24 horas.

Si el almacenamiento de telemetría falla, la respuesta del modelo no se descarta: el nodo devuelve `telemetry.status=NO_DISPONIBLE`. Esto evita convertir una indisponibilidad FinOps en una interrupción del proceso, manteniendo visible la falta de evidencia.

## Prompt Caching

Prompt Caching es una norma de diseño cuando el proveedor y el modelo lo soportan. Este módulo prueba su utilización únicamente cuando OpenAI declara `cached_tokens` o Gemini declara `cachedContentTokenCount`. No se mezclan prefijos, métricas ni observaciones entre organizaciones.
