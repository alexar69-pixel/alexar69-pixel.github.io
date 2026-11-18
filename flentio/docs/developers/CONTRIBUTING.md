# Contribuir a Flentio

## Condición previa

Lee completamente `.agents/AGENTS.md` y `docs/developers/DEVELOPER_HANDOVER.md`. Si usas un
asistente de IA, entrégale también `docs/AI_ASSISTANT_CONTEXT.md`. Ninguna
conversación anterior es una fuente canónica del producto.

## Flujo de cambio

1. Define una fase y un criterio de aceptación verificable.
2. Inspecciona código, migraciones y documentación antes de editar.
3. Preserva cambios ajenos y limita el alcance al checkout `Flentio`.
4. Implementa comportamiento real. Los dobles sólo pertenecen a tests.
5. Añade pruebas de contrato, error y aislamiento relevantes.
6. Si hay frontend, proporciona formulario específico, ayuda, alertas y
   reconfirmación proporcional al riesgo. No expongas JSON o secretos.
7. Ejecuta pruebas backend, build frontend y una verificación visual cuando
   cambie la interfaz.
8. Actualiza código, documentación técnica, manual operativo y rollback.
9. Registra limitaciones como `NO_CONFIGURADO`, `NO_DISPONIBLE`,
   `DEPENDENCIA_CLIENTE` o `NO_VALIDADA`.
10. En llamadas a modelos, conserva prefijos estables y usa Prompt Caching si
    está soportado. Prueba aislamiento, versionado, invalidación, métricas reales
    y fallback sin caché; no afirmes ahorro cuando el proveedor no lo acredita.
11. Añade o amplía el cuadro de mando que representa la capacidad. Verifica
    datos reales, estados vacío/error/no configurado, RBAC, alertas, drill-down,
    escritorio y móvil conforme a `docs/DASHBOARD_STANDARD.md`.

## Comandos obligatorios antes de entregar

```powershell
cd backend
npm test
npm run migrate:platform
cd ../frontend
npm run build
npm run lint
```

Las migraciones sólo se ejecutan contra un entorno autorizado y con la URL de
migración separada. En una revisión sin infraestructura, documenta claramente
qué comando no se pudo ejecutar y por qué.

## Migraciones

- Nunca modifiques una migración ya aplicada: el gestor verifica checksum.
- Añade el siguiente número correlativo en `backend/src/platform/migrations` o
  `backend/src/rag/migrations`.
- Incluye RLS, índices, grants mínimos, retención y rollback operativo.
- No añadas datos ficticios a migraciones de producción.

## Integraciones externas

Cada proveedor es una Integration Skill con manifiesto, integridad, carga
diferida, prueba real, frontend dedicado y estados separados de configuración,
runtime y activación. Los secretos se seleccionan desde la bóveda. Añadir una
entrada al catálogo no significa que exista el runtime.

No selecciones por cuenta propia reranker externo, antivirus, almacenamiento,
KMS/HSM, SIEM o tecnología de ejecución de remediación. Requieren autorización
humana del propietario o cliente.

## Pull request o entrega

Incluye: problema, alcance, archivos principales, pruebas ejecutadas, evidencia
real, riesgos, capacidades pendientes, migraciones, configuración, impacto de
seguridad y rollback. Indica además el cuadro de mando afectado, sus fuentes,
ventana temporal, capturas verificadas y comportamiento sin datos. Nunca
incluyas tokens o salidas que los contengan.
