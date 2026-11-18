# Guía para Gestores — Flentio Platform

> Para responsables de área, jefes de equipo y gestores de procesos que supervisan las automatizaciones de sus equipos y necesitan visibilidad operacional sin gestionar la configuración técnica.

---

## ¿Para qué sirve Flentio en tu día a día?

Como gestor, Flentio te permite:

| Necesidad | Cómo Flentio lo resuelve |
|---|---|
| **Saber qué flujos están activos** | Panel de flujos con estado activo/inactivo, ejecuciones y errores |
| **Revisar si las automatizaciones funcionan** | Historial de ejecuciones con resultado, hora y log |
| **Recibir alertas cuando algo falla** | Flujos configurados para notificar por Slack/email ante errores |
| **Consultar política o normativa interna** | Copiloto RAG responde con citas de documentos oficiales |
| **Aprobar o rechazar propuestas de IA** | Panel de investigación con revisión humana obligatoria |
| **Auditar quién hizo qué** | Log de auditoría inmutable por usuario, fecha y acción |

---

## El Panel Principal (Dashboard)

Al acceder, el **Dashboard** muestra:

- **Mis flujos** — los flujos de tu organización, filtrables por estado y categoría
- **Centro de Control Ejecutivo** — métricas agregadas de las últimas 24 horas:
  - Flujos activos / inactivos
  - Ejecuciones completadas / con error
  - Investigaciones en curso
  - Revisiones humanas pendientes

> El Centro de Control sólo muestra datos reales de tu organización (tenant). Nunca muestra datos de otras organizaciones.

---

## Supervisar el estado de los flujos

### Ver todos los flujos del equipo

1. Panel izquierdo → **Mis flujos**
2. Cada tarjeta muestra:
   - Nombre y descripción del flujo
   - Badge **ACTIVO** (verde, pulsante) o **INACTIVO** (gris)
   - Entorno: 🚀 PROD, 🧪 STAGING o 🏗️ DEV
   - Número de nodos
   - Categoría

3. Pulsa cualquier tarjeta para abrirla en el editor y ver su estructura

### Revisar el historial de ejecuciones

1. Abre un flujo → pestaña **Ejecuciones** en la barra superior
2. Verás cada ejecución con:
   - Fecha y hora (UTC)
   - Estado: ✅ Completado, ❌ Error, ⏸ Pendiente
   - Duración
   - Enlace al log completo

3. Pulsa una ejecución para ver el log detallado nodo por nodo

### ¿Qué hacer si hay errores recurrentes?

1. Identifica el nodo que falla (aparece en rojo en el log)
2. El mensaje de error indica el problema: credencial caducada, campo faltante, servicio no disponible
3. Si es una credencial, contacta al **administrador de sistema**
4. Si es un problema de configuración del nodo, el usuario que creó el flujo puede corregirlo

---

## Usar el Copiloto RAG para consultas de conocimiento

El **Copiloto RAG** (Retrieval-Augmented Generation) consulta la base documental de tu organización:

1. Desde cualquier pantalla del editor → botón **"Consultar Documentación (RAG)"** (esquina inferior izquierda)
2. Escribe tu pregunta en lenguaje natural:
   > *"¿Cuál es el procedimiento de aprobación para préstamos superiores a 50.000€?"*
   > *"¿Qué normativa aplica a los clientes de banca privada en operaciones con derivados?"*
3. El sistema responde con el texto relevante **más la cita del documento fuente**

> **Importante:** El copiloto responde con evidencia documental real. Si la información no está indexada, responde `SIN_DATOS` en lugar de inventar una respuesta.

### ¿Qué documentos están disponibles en el RAG?

El administrador gestiona qué documentos se indexan. Tipos habituales:
- Políticas y normativa interna
- Runbooks operativos
- Informes periódicos
- Manuales de procedimiento
- Regulación bancaria publicada

---

## Revisión y aprobación de propuestas de IA

En el módulo de **Investigación Operacional**, la IA puede generar propuestas de acción ante incidentes. Como gestor:

1. Accede a **Administración → Investigaciones**
2. Las propuestas con estado `SUGGEST/NOT_EXECUTED` requieren revisión humana
3. Cada propuesta muestra:
   - Evidencia utilizada y sus citas
   - Contradicciones detectadas por el sistema
   - Checks de seguridad superados
   - Alcance y riesgo de la acción propuesta
   - Runbook de rollback
4. Debes **aprobar o rechazar** con motivo explícito
5. La aprobación queda registrada en el log de auditoría con tu identidad y timestamp

> El sistema nunca ejecuta una propuesta automáticamente. **«Aprobar sin ejecutar»** es el estado final máximo sin una decisión activa adicional.

---

## Auditoría y trazabilidad

Todas las acciones significativas quedan registradas:

| Acción auditada | Qué registra |
|---|---|
| Activación/desactivación de flujo | Usuario, timestamp, flujo afectado |
| Ejecución manual | Usuario, timestamp, resultado |
| Aprobación/rechazo de propuesta | Usuario, motivo, timestamp |
| Modificación de credencial | Usuario, acción (sin mostrar el secreto) |
| Acceso a documentos RAG | Usuario, consulta (sin el contenido del documento) |

Para ver el log de auditoría: **Administración → Auditoría** (rol administrador) o solicítalo a tu administrador.

---

## Indicadores clave de salud

Como gestor, estos son los indicadores a revisar periódicamente:

| Indicador | Dónde verlo | Señal de alerta |
|---|---|---|
| Flujos con error en 24h | Centro de Control Ejecutivo | >0 errores en flujos críticos |
| Ejecuciones fallidas / total | Historial de cada flujo | Ratio de error >5% sostenido |
| Nodos con `NO_CONFIGURADO` | Panel del flujo → Validar | Impide que el flujo funcione |
| Propuestas IA pendientes de revisión | Investigaciones | Pendientes >48h sin revisar |
| Documentos RAG desactualizados | Administración → RAG | Documentos con fecha >90 días sin actualizar |

---

## Preguntas frecuentes para gestores

**¿Puedo ver los flujos de todos mis empleados?**
Sí, si tu rol tiene acceso de lectura. Los flujos de tu organización son visibles para todos los miembros según su nivel de acceso.

**¿Puedo crear flujos yo mismo?**
Sí. Flentio está diseñado para usuarios no técnicos. Usa el asistente IA del Dashboard o las plantillas prediseñadas.

**¿Quién puede activar o desactivar un flujo crítico?**
Cualquier usuario con acceso de escritura al flujo. Para flujos críticos, se recomienda que el administrador configure el flujo como sólo lectura para usuarios no autorizados.

**¿Cómo sé si el sistema está funcionando correctamente?**
El **Centro de Control Ejecutivo** muestra el estado general. El administrador recibe alertas automáticas si hay degradación de servicios.

**¿El sistema cumple con regulación bancaria?**
El sistema está diseñado con los principios de la regulación bancaria europea (DORA, BCE, EBA): aislamiento por organización, auditoría inmutable, revisión humana obligatoria en decisiones críticas y transparencia de evidencias. La homologación formal es responsabilidad de cada organización cliente.
