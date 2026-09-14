# Plantilla de adaptador Client Gateway v1

Estado: `PLANTILLA_NO_CONFIGURADA`. No contiene endpoint, identidad ni proveedor.

## Identidad y alcance

- Producto y edición:
- Tenant externo:
- Ámbito de sólo lectura:
- Identidad técnica y propietario:
- Capacidades exactas:
- Egress, proxy, DNS y TLS/mTLS:
- Rotación y revocación:

## Contrato de comprobación

El adaptador debe implementar `/.well-known/flentio-integration/v1`, devolver el
challenge exacto, tenant y scope esperados, `readOnly: true`, capacidades
allowlist y bindings del producto. No debe devolver secretos, eventos completos
ni contenido documental durante la prueba.

## Puertas

1. proveedor autorizado por tenant;
2. perfil guardado sin secretos;
3. credencial seleccionada desde bóveda;
4. prueba real vigente;
5. activación reconfirmada;
6. rollback: desactivar, descargar runtime y revocar identidad.
