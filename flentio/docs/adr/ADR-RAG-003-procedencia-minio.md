# ADR-RAG-003: procedencia y custodia de originales en desarrollo

- Fecha: 2026-07-31
- Estado: aceptada para validación local
- Alcance: RAG F3; no autoriza producción bancaria

## Contexto

El conocimiento extraído no basta para auditar una respuesta. Flentio necesita conservar el fichero exacto, el pipeline aplicado, su vigencia y las decisiones de conservación. La decisión humana autoriza MinIO single-node para desarrollo, cifrado previo a la carga, Object Lock/legal hold y ninguna eliminación física automática. HA se aplaza.

## Decisión

PostgreSQL conserva metadatos, relaciones y eventos; MinIO conserva originales cifrados y versionados. El original limpio se escribe antes del parser con AES-256-GCM y AAD ligado al tenant/objeto/checksum. Se exigen `VersionId`, Object Lock y comprobación posterior. Legal hold y retención GOVERNANCE se verifican mediante lectura del estado real antes de reflejarlos en PostgreSQL.

Sólo documentos `effective`, dentro de vigencia y autorizados por RLS participan en recuperación. Las transiciones son explícitas y auditadas. No se concede DELETE a la identidad de aplicación sobre originales, eventos, documentos, versiones o fragmentos.

El contenedor de desarrollo compila la última release fuente oficial conocida con la corrección de seguridad de octubre de 2025. Dado que MinIO quedó archivado, la decisión no lo selecciona como almacenamiento productivo.

## Alternativas consideradas

- Guardar binarios en PostgreSQL: simplifica atomicidad, pero aumenta presión sobre backups/WAL y no ofrece Object Lock nativo.
- Imagen binaria oficial antigua de MinIO: descartada porque no incluye la release fuente de seguridad posterior.
- Amazon S3 Object Lock o Azure Blob immutable storage: candidatas preferentes para producción gestionada; requieren decisión de nube, residencia, contrato y KMS.
- Simular almacenamiento o WORM: descartado por la regla del proyecto que prohíbe mocks como capacidades operativas.

## Consecuencias

Hay evidencia restaurable y aislamiento real, pero la transacción abarca dos sistemas. Un fallo tras proteger MinIO puede dejar PostgreSQL temporalmente desactualizado; el resultado es conservador y exige reconciliación operativa. La clave local no equivale a KMS/HSM. HA, rotación, replicación, modo COMPLIANCE y destrucción regulada quedan como decisiones posteriores documentadas.

## Reversión

Detener nuevas ingestas, mantener el bucket y sus versiones, exportar inventario con hashes, migrar objetos cifrados a un proveedor aprobado y cambiar el adaptador sólo después de restauraciones comparadas byte a byte. No se elimina el origen durante la reversión mientras exista retención o legal hold.

