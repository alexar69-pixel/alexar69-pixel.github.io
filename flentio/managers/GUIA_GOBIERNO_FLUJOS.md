# Gobierno de Flujos — Gestores Flentio

> Guía de auditoría, ciclo de vida y aprobación de automatizaciones para gestores y responsables de proceso.

---

## Ciclo de vida de un flujo

```
BORRADOR → REVISIÓN → ACTIVO → SUSPENDIDO → ARCHIVADO
   │           │         │
   └─ Creación  └─ Tests   └─ Operación continua
```

| Estado | Descripción | Quién lo cambia |
|---|---|---|
| **Borrador** | En construcción, no ejecuta automáticamente | El creador |
| **Activo** | Responde a triggers automáticamente | Cualquiera con acceso de escritura |
| **Inactivo / Suspendido** | Toggle desactivado — no ejecuta | Cualquiera con acceso de escritura |
| **Archivado (Papelera)** | Eliminado lógicamente, recuperable 90 días | El creador o administrador |

---

## Criterios de aprobación antes de activar un flujo de producción

Antes de activar un flujo crítico en producción, el gestor responsable debe verificar:

### ✅ Criterios técnicos
- [ ] Todos los nodos tienen estado `OPERATIVO` (sin ⚙ CONF. REQUERIDA)
- [ ] La validación estructural (`Validar` en barra superior) no muestra errores
- [ ] El flujo se ha ejecutado manualmente al menos una vez con resultado correcto
- [ ] Los datos sensibles no se registran en campos de texto libre

### ✅ Criterios operativos
- [ ] El flujo tiene nombre descriptivo y descripción clara de su propósito
- [ ] El creador del flujo ha documentado el caso de uso
- [ ] Existe un responsable nominado en caso de error
- [ ] Se ha verificado que el flujo no duplica uno ya existente

### ✅ Criterios de gobierno
- [ ] El flujo está asignado a la categoría correcta
- [ ] El entorno está marcado correctamente (DEV / STAGING / PROD)
- [ ] El acceso al flujo está restringido si contiene lógica sensible
- [ ] Los flujos de alto impacto (financiero, regulatorio) tienen revisión de segundo nivel

---

## Auditoría de flujos del equipo

### Revisar actividad reciente

1. **Administración → Centro de Control Ejecutivo** (rol administrador o gestor)
2. En la ventana de 24 horas verás:
   - Total de ejecuciones del período
   - Ejecuciones con error (con enlace a cada una)
   - Flujos modificados recientemente
   - Revisiones humanas realizadas

### Generar vista de flujos por estado

Desde el **Dashboard**, la vista de flujos muestra:
- Filtro por **Categoría** (AML, IA, Monitoreo, Finanzas, etc.)
- Filtro por **Estado** (Activo / Inactivo)
- Filtro por **Entorno** (PROD / STAGING / DEV)
- Buscador por nombre

Para exportar el inventario a CSV: contacta al administrador (el endpoint `/api/admin/workflows` está disponible con rol administrador).

---

## Control de versiones de flujos

Flentio mantiene **historial de versiones** de cada flujo:

1. Abre el flujo en el editor
2. Barra superior → botón **⟳ Versiones**
3. Verás las versiones anteriores con fecha y número
4. Puedes **restaurar** cualquier versión anterior

> Nunca se borran versiones hasta que el flujo sea eliminado permanentemente. La auditoría de cambios incluye qué usuario guardó cada versión.

---

## Gestión de flujos de alto impacto

Para flujos que ejecutan acciones financieras, regulatorias o que afectan a clientes:

### Flujos con revisión obligatoria (recomendación)

| Tipo de flujo | Revisión recomendada | Frecuencia |
|---|---|---|
| Envío automático de comunicaciones a clientes | Segundo nivel (gestor senior) | Por cada cambio al flujo |
| Consultas o escrituras en bases de datos de producción | Revisión técnica + gestor | Por cada cambio |
| Generación de reportes regulatorios | Gestor + Cumplimiento | Por cada activación |
| Flujos de decisión con IA (crédito, AML) | Revisión humana integrada en el flujo | Por cada decisión |

### Configurar revisión humana en el flujo

Para flujos donde la IA propone una acción:
1. El nodo **Agente IA** puede configurarse en modo `SUGGEST_ONLY`
2. La propuesta queda en estado `NOT_EXECUTED` hasta que un humano la aprueba
3. El panel de investigación muestra evidencias, contradicciones y checklist antes de aprobar

---

## Respuesta ante incidentes en flujos

Si un flujo crítico falla:

1. **Desactiva inmediatamente** el flujo (toggle → Inactivo) para evitar ejecuciones en error
2. Abre el **historial de ejecuciones** y localiza el primer error
3. Identifica el nodo fallido y el mensaje de error
4. Si es un problema de credencial → contacta al administrador
5. Si es un problema de lógica → el creador del flujo debe corregirlo en STAGING antes de volver a activar en PROD
6. Documenta el incidente en el sistema de tickets (Jira/Helix si está configurado)

---

## Política de retención y archivo

| Tipo de dato | Retención por defecto | Quién puede eliminar |
|---|---|---|
| Flujos activos | Indefinida | Propietario o administrador |
| Flujos en papelera | 90 días | Administrador |
| Historial de ejecuciones | 90 días | Administrador (configurable) |
| Log de auditoría | Permanente (inmutable) | Nadie — es append-only |
| Documentos RAG | Según política de cada corpus | Administrador RAG |

> El log de auditoría es inmutable y no puede modificarse ni eliminarse. Cualquier acción significativa queda registrada permanentemente.
