# Guía de Usuario — Flentio Platform

> Para usuarios finales: analistas, operativos, gestores de procesos y cualquier persona que use Flentio para automatizar tareas o consultar información corporativa.

---

## ¿Qué puedes hacer con Flentio?

Flentio te permite, **sin escribir código**:

- **Automatizar procesos repetitivos** — enviar alertas, procesar documentos, sincronizar datos entre sistemas
- **Consultar el conocimiento de tu organización** — documentos, normativa, runbooks, informes mediante el Copiloto RAG
- **Supervisar automatizaciones activas** — ver ejecuciones, resultados y errores en tiempo real
- **Colaborar en flujos** — compartir, duplicar y revisar flujos con tu equipo

---

## Primer acceso

1. Accede a la URL de tu organización (ej: `https://flentio.tuempresa.com`)
2. Inicia sesión con tu cuenta corporativa
3. Llegarás al **Dashboard** — el panel principal

### Lo que verás en el Dashboard

```
┌─────────────────────────────────────────────────────┐
│  Panel izquierdo     │  Panel principal              │
│  ─────────────────   │  ────────────────────────     │
│  Mis flujos          │  Genera un flujo con IA       │
│  Plantillas          │  [campo de texto]             │
│  Administración      │                               │
│  Documentación       │  Mis flujos guardados         │
│                      │  □ Flujo 1  □ Flujo 2 ...     │
└─────────────────────────────────────────────────────┘
```

---

## Crear tu primer flujo de automatización

### Opción A — Con Inteligencia Artificial (recomendada para nuevos usuarios)

1. En el **Dashboard**, escribe en el cuadro central lo que quieres automatizar en lenguaje natural:
   > *"Cuando llegue un email con adjunto, extrae el texto y guárdalo en la base de datos"*
   > *"Cada lunes a las 8am, envíame un resumen de los flujos activos por Slack"*

2. Pulsa **Generar con IA** — el sistema crea el grafo de nodos automáticamente

3. Si la IA necesita más información, verás **chips de respuesta rápida** — pulsa el que corresponda o escribe la respuesta en el campo de texto

4. El flujo se abre en el **Editor visual** — puedes revisarlo y ajustarlo antes de activarlo

### Opción B — Desde una plantilla

1. Pulsa **Manual** o explora la galería de **Plantillas**
2. Filtra por categoría: *Monitoreo*, *IA*, *Google Workspace*, *Bancario*...
3. Pulsa **Usar esta plantilla** — se abre en el editor listo para configurar

### Opción C — En blanco

1. Pulsa el botón **+ Nuevo flujo**
2. Aparece un modal donde escribes el **nombre** (obligatorio), descripción y categoría
3. Pulsa **Crear flujo vacío** para entrar al editor

---

## El Editor de Flujos

El editor es un **lienzo visual** donde conectas nodos (bloques funcionales):

```
[Trigger: Webhook] ──→ [IA: Clasificar] ──→ [Switch] ──→ [Gmail: Enviar]
                                                      ──→ [Slack: Alertar]
```

### Cómo añadir nodos

- **Doble clic en el lienzo** — se abre un menú de nodos agrupados por categoría
- **Arrastrar desde el panel izquierdo** — la barra lateral muestra todos los nodos disponibles
- **Buscar** — escribe el nombre del nodo en la caja de búsqueda del menú

### Colores de estado de los nodos en la barra lateral

| Color / Indicador | Significado |
|---|---|
| Normal (sin advertencia) | Nodo listo para usar |
| ⚙ CONF. REQUERIDA (ámbar) | Necesita credenciales o configuración — el administrador debe habilitarlo |

> Si un nodo muestra ⚙ CONF. REQUERIDA, puedes añadirlo al lienzo y configurarlo, pero no ejecutará hasta que el administrador active la credencial correspondiente.

### Configurar un nodo

1. **Haz clic** en cualquier nodo del lienzo — se abre el panel derecho de configuración
2. Verás los **campos requeridos** claramente marcados. Los campos faltantes aparecen en un banner naranja en la parte superior del panel
3. Usa el **asistente de variables** (`{% raw %}{{{% endraw %} }}`) para referenciar la salida de nodos anteriores — el asistente muestra los nodos disponibles con nombres legibles
4. Cuando todos los campos estén completos, el nodo está listo

### Conectar nodos

- Arrastra desde el **punto de salida** (círculo derecho del nodo) al **punto de entrada** (círculo izquierdo del siguiente)
- El nodo **Switch** tiene salidas múltiples (true/false) — cada rama va a un nodo diferente

---

## Guardar, probar y activar

| Acción | Cómo |
|---|---|
| **Guardar** | Botón 💾 en la barra superior (o Ctrl+S) |
| **Ejecutar manualmente** | Botón ▶ **Ejecutar** — útil para probar |
| **Ver resultado** | Se abre la **Consola de ejecución** con el log en tiempo real |
| **Validar estructura** | Botón **Validar** — revisa que todos los nodos estén conectados y configurados; muestra un panel con los problemas específicos |
| **Activar** | Botón toggle **Activo/Inactivo** — un flujo activo responde a sus triggers automáticamente |

---

## El Copiloto RAG — Consulta el conocimiento de tu organización

El botón **"Consultar Documentación (RAG)"** en la esquina inferior izquierda del editor abre el **Copiloto de conocimiento**:

- Responde preguntas sobre documentos internos: normativa, runbooks, políticas, informes
- **Incluye citas** de las fuentes reales para que puedas verificar la respuesta
- **No modifica el lienzo** ni ejecuta acciones — es sólo consulta
- Si la información no está en el sistema, responde con `SIN_DATOS` en lugar de inventar

> Para crear flujos desde lenguaje natural, usa el campo de texto del **Dashboard**, no el Copiloto.

---

## Preguntas frecuentes

**¿Puedo borrar un flujo accidentalmente?**
Los flujos eliminados van a la **Papelera** y pueden recuperarse. Sólo el administrador puede eliminarlos permanentemente.

**¿Por qué un nodo aparece con ⚙ CONF. REQUERIDA?**
El administrador aún no ha configurado la credencial de ese servicio (Gmail, Slack, etc.). Puedes diseñar el flujo igualmente, pero necesitarás pedir al administrador que active la integración.

**¿Puedo compartir un flujo con un compañero?**
Sí. En las opciones del flujo, puedes marcarlo como **Público** (visible para tu organización) o mantenerlo **Privado**.

**¿El sistema guarda el historial de ejecuciones?**
Sí. En cada flujo verás el historial de ejecuciones con fecha, estado (éxito/error) y logs detallados.

**¿Puedo usar plantillas de IA sin conocimientos técnicos?**
Sí, esa es la función principal de las plantillas. Seleccionas la plantilla, configuras los campos (normalmente sólo parámetros de negocio como direcciones de email o canales de Slack) y activas.
