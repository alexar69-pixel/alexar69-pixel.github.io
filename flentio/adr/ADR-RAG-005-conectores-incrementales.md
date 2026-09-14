# ADR-RAG-005: conectores incrementales con contrato de proveedor

- Estado: aceptada para validación local
- Fecha: 31-07-2026
- Alcance: F5; no autoriza producción ni alta disponibilidad

## Decisión

Flentio conserva cursores, eventos, tombstones, trabajos y canales en PostgreSQL. La orquestación usa colas reclamadas con `FOR UPDATE SKIP LOCKED`, transacciones cortas y RLS por tenant. Las llamadas externas se ejecutan fuera de transacciones.

Google Drive es el primer adaptador real. `connectorProviders.js` define el puerto estable: cursor inicial, enumeración paginada, cambios, descarga, tipo soportado, suscripción y cancelación. La columna `provider` no tiene un `CHECK` cerrado; un proveedor nuevo debe registrarse en código y superar las mismas pruebas. No existe fallback ficticio.

El proceso web ejecuta temporalmente la cola de conectores porque la bóveda de credenciales actual reside en SQLite y sólo se monta allí. La cola ya es compartida, pero mover su ejecución a workers separados exige una bóveda de red homologada. No se declara HA en desarrollo.

## Razones

- Un cursor evita descargar decenas de miles de objetos sin cambios.
- El webhook es una señal, no la fuente de verdad; el feed de cambios permite recuperar pérdidas.
- La idempotencia se fija en PostgreSQL, no en memoria.
- Los tombstones preservan evidencia y archivan el conocimiento sin borrado físico.
- Un puerto de proveedor evita acoplar la cola y la gobernanza a una API concreta.

## Consecuencias y reversión

Se añaden tablas y funciones, pero no se elimina información existente. Para revertir operación se deshabilitan webhooks y conectores, se conserva el cursor para diagnóstico y se ejecuta reconciliación controlada. No se deben eliminar las tablas mientras existan trabajos, evaluaciones o documentos enlazados.

