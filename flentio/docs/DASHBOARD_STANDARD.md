# Estándar obligatorio de cuadros de mando

## Regla de producto

Toda capacidad de Flentio orientada a operación, administración, investigación,
integración o gobierno debe estar representada en un cuadro de mando. Puede ser
un panel propio o una sección explícita de un panel agregado. Una API, worker,
Skill o conector sin visibilidad operacional no se considera terminado.

El cuadro de mando no sustituye la observabilidad técnica ni el sistema fuente:
presenta una vista gobernada para comprender estado, riesgo y siguiente acción.
No debe replicar Grafana, Helix, Jira o un SIEM completo.

## Contrato mínimo

Cada panel documentará y mostrará, cuando resulte aplicable:

1. estado efectivo y motivo, sin convertir ausencia en éxito;
2. volumen o actividad real dentro de una ventana temporal visible;
3. errores, alertas, degradaciones y configuración caducada;
4. dependencias y estado `NO_CONFIGURADO`, `NO_DISPONIBLE`, `SIN_DATOS` o
   `NO_VERIFICADO`;
5. última actualización, zona horaria, unidades y fuente de cada métrica;
6. tendencia frente a observaciones anteriores, sólo si existe histórico real;
7. acceso al detalle, expediente, evidencia, runbook o configuración responsable;
8. límites conocidos y separación visible entre objetivo, observación y
   estimación.

No son válidos un contador aislado, una colección decorativa de tarjetas, datos
hardcodeados, un estado verde por defecto ni un gráfico sin fuente, periodo o
unidad. Con cero registros debe mostrarse `SIN_DATOS`, no un cero operacional,
salvo que la consulta real demuestre que el valor medido es cero.

## Seguridad y experiencia

- Toda consulta hereda tenant, identidad, RBAC, clasificación y alcance.
- Las agregaciones no incluyen secretos, prompts, documentos, payloads completos
  ni identificadores sensibles innecesarios.
- Las acciones modificadoras mantienen confirmación, consecuencias, permisos y
  auditoría; el dashboard nunca convierte una recomendación en ejecución tácita.
- Las alertas críticas se comunican con texto e iconografía, no sólo con color.
- La interfaz debe ser responsive, navegable por teclado, legible con zoom y
  comprensible sin editar JSON, SQL, YAML o consultas del proveedor.
- La actualización automática será visible y acotada; un fallo conserva la
  última observación con su antigüedad y marca `NO_DISPONIBLE`, sin aparentar
  frescura.

## Criterio de aceptación

Antes de cerrar un módulo se debe aportar:

- contrato y fuente real de cada dato;
- pruebas de autorización, aislamiento, normalización y estados con datos,
  vacío, error y dependencia no configurada;
- prueba de que un valor desconocido no se transforma en cero o `OPERATIVO`;
- drill-down o enlace seguro al objeto responsable;
- build y lint del frontend;
- comprobación visual e interactiva en escritorio y móvil, sin errores de
  consola, solapamientos ni desbordamiento horizontal;
- documentación de actualización, retención, alertas, limitaciones y rollback.

Si el backend está implementado pero el panel o sus pruebas no lo están, el
estado máximo permitido es `IMPLEMENTADO_SIN_CUADRO_DE_MANDO`; no puede marcarse
como entrega funcional terminada.

## Evolución

Los nuevos módulos deben reutilizar tokens visuales, filtros temporales,
componentes de estado y patrones de accesibilidad existentes. Compartir
componentes no autoriza a mezclar tenants ni a ocultar diferencias semánticas
entre métricas. Cualquier excepción requiere justificación arquitectónica,
propietario, fecha de revisión y un cuadro agregado alternativo.
