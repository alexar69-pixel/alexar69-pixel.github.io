# Guía de Automatización No-Code — Flentio Platform

> Guía paso a paso para diseñar automatizaciones sin escribir código. Dirigida a usuarios que quieren crear flujos de trabajo propios.

---

## Antes de empezar: conceptos clave

| Concepto | Qué es | Ejemplo |
|---|---|---|
| **Flujo** (Workflow) | Secuencia de pasos que se ejecutan automáticamente | Recibir email → Clasificar con IA → Notificar por Slack |
| **Nodo** | Un paso individual del flujo | "Enviar email", "Clasificar texto", "Consultar base de datos" |
| **Trigger** | El evento que arranca el flujo | Un webhook, un cron, un email recibido, un clic manual |
| **Variable de expresión** | Dato de un paso anterior que usas en el siguiente | `{{ $input.cuerpo_email }}` |
| **Credencial** | La autorización para conectarse a un servicio externo | Cuenta de Gmail, token de Slack — la configura el administrador |

---

## Anatomía de un flujo típico

```
TRIGGER          PROCESAMIENTO          ACCIÓN
────────         ─────────────          ──────
Webhook ──→ IA: Clasificar ──→ Switch ──→ [true]  Gmail: Enviar alerta
                                     └──→ [false] Slack: Registrar evento
```

Todos los flujos tienen:
1. **Exactamente un Trigger** — el punto de entrada
2. **Uno o más nodos de procesamiento** — transforman o enrutan los datos
3. **Una o más acciones finales** — envían, guardan o notifican

---

## Guía práctica: Flujo de alerta de errores

**Objetivo:** Cuando llegue una alerta de monitorización, clasificarla con IA y notificar al equipo técnico por Slack si es crítica.

### Paso 1 — Crear el flujo

1. Dashboard → botón **+ Nuevo flujo**
2. Nombre: `Alerta de monitorización → Slack`
3. Descripción: `Recibe alertas por webhook, filtra las críticas y notifica al equipo`
4. Categoría: `Monitoreo e IT-Ops`
5. Pulsa **Crear flujo vacío**

### Paso 2 — Añadir el Trigger

1. Doble clic en el lienzo → busca **"Webhook"**
2. Arrastra o haz clic en **Webhook Trigger**
3. Abre su configuración (clic en el nodo): anota la **URL del webhook** que aparece — es la dirección donde tu sistema enviará las alertas

### Paso 3 — Añadir clasificación IA

1. Doble clic → busca **"IA Ollama"** o **"IA Gemini"**
2. En la configuración:
   - **Prompt:** `Clasifica esta alerta como CRITICA, ADVERTENCIA o INFO: {{ $input.body.message }}`
3. Conecta: arrastra del punto derecho del Webhook al punto izquierdo del nodo IA

### Paso 4 — Añadir el Switch (enrutador)

1. Doble clic → **Switch**
2. Configuración:
   - **Propiedad a evaluar:** `{{ $input.resultado }}`
   - **Regla:** si el valor es `CRITICA` → salida `true`
3. Conecta el nodo IA al Switch

### Paso 5 — Añadir la notificación Slack

1. Doble clic → **Slack Webhook**
2. Configuración:
   - **URL de webhook Slack:** (se autocompleta si el administrador configuró la credencial)
   - **Mensaje:** `🚨 Alerta CRÍTICA: {{ $input.body.message }}`
3. Conecta la salida **true** del Switch al nodo Slack

### Paso 6 — Validar y guardar

1. Pulsa **Validar** en la barra superior — revisa que no haya nodos desconectados
2. Si el panel de validación muestra ✅ sin errores, guarda con **💾**
3. Pulsa **▶ Ejecutar** para probarlo manualmente con datos de prueba

### Paso 7 — Activar

1. Toggle **Activo** en la barra superior
2. El flujo ya responde automáticamente a cada webhook recibido

---

## Tipos de Trigger disponibles

| Trigger | Cuándo se activa | Caso de uso típico |
|---|---|---|
| **Webhook** | Al recibir una llamada HTTP POST | Alertas de Grafana, eventos de Jira, notificaciones externas |
| **Cron** | En un horario fijo | Informes diarios, limpieza semanal, sincronización nocturna |
| **Manual** | Al pulsar "Ejecutar" | Pruebas, procesos bajo demanda |
| **Email** | Al recibir un email (si está configurado) | Procesamiento de solicitudes por email |

---

## Nodos más usados

### Procesamiento
| Nodo | Qué hace |
|---|---|
| **IA Ollama** / **IA Gemini** | Clasifica, resume, extrae datos o responde preguntas en lenguaje natural |
| **Agente IA** | IA que puede consultar la base de conocimiento (RAG) antes de responder |
| **Switch** | Enruta el flujo según el valor de una propiedad |
| **Código** | Ejecuta lógica JavaScript simple (para usuarios avanzados) |
| **Establecer variable** | Guarda un valor para usarlo después |

### Acciones
| Nodo | Qué hace |
|---|---|
| **Gmail: Enviar** | Envía un email desde la cuenta configurada |
| **Slack Webhook** | Envía un mensaje a un canal de Slack |
| **HTTP Request** | Llama a cualquier API externa |
| **PostgreSQL Query** | Guarda o consulta datos en la base de datos |
| **Telegram Bot** | Envía mensaje por Telegram |

### Triggers
| Nodo | Qué hace |
|---|---|
| **Webhook Trigger** | Escucha llamadas HTTP entrantes |
| **Cron Trigger** | Se activa en el horario configurado |
| **Manual Trigger** | Se activa al pulsar Ejecutar |

---

## Expresiones y variables

Puedes referenciar datos de pasos anteriores usando la sintaxis `{{ $input.campo }}`:

```
{{ $input.body.message }}        ← El campo "message" del cuerpo del webhook
{{ $input.resultado }}           ← La respuesta del nodo anterior
{{ $input.ai_gemini.text }}      ← La respuesta del nodo IA Gemini
```

El **asistente de variables** (botón `{{ }}` en cada campo de configuración) muestra los nodos disponibles con nombres legibles y te ayuda a construir la expresión sin conocer la sintaxis exacta.

---

## Resolución de problemas comunes

| Problema | Causa probable | Solución |
|---|---|---|
| El flujo no se ejecuta | No está **Activo** | Activa el toggle en la barra superior |
| Un nodo falla con error de credencial | La integración no está configurada | Pide al administrador que configure la credencial |
| El Switch no enruta correctamente | El valor de la propiedad no coincide con la regla | Ejecuta manualmente y revisa el log para ver el valor real |
| La IA devuelve respuestas inesperadas | El prompt es ambiguo | Revisa y reformula el prompt con instrucciones más específicas |
| El Webhook no recibe datos | URL incorrecta en el sistema externo | Copia la URL exacta del panel de configuración del nodo Webhook |

---

## Buenas prácticas

1. **Nombra los nodos** — haz doble clic en el nodo y cambia el nombre por algo descriptivo (ej: "Clasificar severidad" en lugar de "ai_gemini_1")
2. **Prueba antes de activar** — usa **Ejecutar** con datos reales y revisa la consola
3. **Añade notas** — el nodo **Nota Adhesiva** permite documentar el flujo para tu equipo
4. **Empieza simple** — 3-4 nodos bien configurados son mejor que un flujo complejo con errores
5. **Revisa el historial** — en la pestaña **Ejecuciones** del flujo puedes ver todos los runs anteriores con sus resultados
