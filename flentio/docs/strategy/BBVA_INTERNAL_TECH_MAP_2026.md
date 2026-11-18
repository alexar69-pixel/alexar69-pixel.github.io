# Mapa tecnológico interno de BBVA para integración con Flentio

## Propósito y clasificación de evidencia

Este documento transforma la investigación pública y el conocimiento bancario aportado al proyecto en un mapa de trabajo. No representa una arquitectura oficial de BBVA ni autoriza una integración.

| Etiqueta | Significado |
|---|---|
| `CONFIRMADO_PUBLICAMENTE` | Existe una fuente primaria pública de BBVA |
| `EXPERIENCIA_EXPERTA_PENDIENTE_DE_CONTRASTE` | Conocimiento interno aportado al proyecto, pendiente de contrastar con documentación autorizada |
| `INDICIO_PUBLICO_LIMITADO` | Fuente local, histórica o de un equipo; no extrapolable al Grupo |
| `NO_CONFIRMADO_PUBLICAMENTE` | No hay evidencia pública suficiente |

## Vista lógica provisional

```text
Clientes y empleados
        │
        ├── App móvil / web / canales empresariales
        │       ├── GEMA y plataforma móvil global
        │       ├── SENDA
        │       ├── Horizon / open banking
        │       └── BBVA Experience / componentes de canal
        │
        ├── Cells / capacidades reutilizables de canal
        │
        ├── ASO / catálogo de servicios y APIs
        │
        ├── APX online y batch / lógica backend y procesos
        │
        ├── Sistemas core y plataformas locales/globales
        │
        └── Datos, analítica e IA
                └── ADA sobre AWS + gobierno/MLOps

Ejecución híbrida progresiva
        ├── NextGen: nube privada
        └── AWS: nube pública estratégica

Capacidades transversales
        ├── Ether / plataforma tecnológica
        ├── ONE / modelo de ingeniería
        ├── DevOps, pruebas automáticas y seguridad
        └── IAM, observabilidad, continuidad y gobierno
```

El diagrama expresa relaciones lógicas, no flujo físico, protocolo, dependencia exacta ni ubicación de cada carga.

## Capas y estado conocido

### 1. Canales digitales

BBVA publica una plataforma móvil global basada en procesos, diseño, navegación y componentes reutilizables, manteniendo una app por país con adaptaciones locales. En 2018 declaró más de 970 funciones comunes identificadas y 350 incorporadas entonces. Son cifras históricas y no deben tratarse como inventario actual. [BBVA: plataforma móvil global](https://www.bbva.com/en/global-mobile-banking-platform-quickly-reach-customers/)

En 2024 el banco identificó como soluciones globales GEMA —app móvil—, SENDA —canal empresarial de escritorio— y Horizon, que conecta plataformas de socios mediante APIs. También describió capacidades globales para firma, biometría, pagos y reconciliación. [BBVA: soluciones globales](https://www.bbva.com/en/innovation/bbva-groups-scale-as-a-source-of-value-creation-in-software-development/)

BBVA Experience aporta un catálogo global de diseño y partes de código reutilizables para apps y webs. Esto confirma sistematización del front-end, pero no revela repositorios, frameworks actuales ni arquitectura de ejecución del canal. [BBVA Experience](https://www.bbva.com/es/bbva-crea-una-plataforma-pionera-para-el-diseno-global-de-productos-digitales/)

**Estado:** `CONFIRMADO_PUBLICAMENTE` para el modelo de reutilización; implementación actual completa `NO_CONFIRMADO_PUBLICAMENTE`.

### 2. Cells

Informes territoriales de BBVA incluyen Cells entre las capacidades de Ether y miden reutilización de funcionalidades. Su relación exacta con GEMA, SENDA, canales web/móvil y el runtime actual no está documentada públicamente con suficiente precisión.

**Estado:** existencia y reutilización `CONFIRMADO_PUBLICAMENTE`; contratos y arquitectura `NO_CONFIRMADO_PUBLICAMENTE`.

### 3. ASO y APIs

Las fuentes oficiales agrupan API/ASO dentro de Ether, mencionan catálogos de servicios y cuantifican funcionalidades reutilizables. El portal público de BBVA distingue la orientación a servicios para integración interna/server-to-server de las APIs web orientadas a canales, pero no documenta ASO como producto interno completo. [BBVA Colombia 2019](https://accionistaseinversores.bbva.com/wp-content/uploads/2020/12/COLOMBIA_Informe-Anual-2019_esp.pdf), [BBVA API Market](https://www.bbvaapimarket.com/en/api-world/steps-creating-api-architecture/)

**Hipótesis de integración Flentio:** ASO/API sería el punto preferente para consultar estado, recibir capacidades autorizadas y solicitar acciones, evitando conexión directa con bases de datos o lógica interna.

**Estado:** papel general `CONFIRMADO_PUBLICAMENTE`; contratos, gateway, autenticación y eventos `NO_CONFIRMADO_PUBLICAMENTE`.

### 4. APX online y batch

Los informes de BBVA confirman APX como capacidad de Ether y su uso en soluciones tecnológicas. La asociación con backend Java, servicios online y procesos batch aparece consistentemente en demanda laboral especializada, pero no existe documentación pública oficial suficiente para fijar runtime, versiones, patrones o interfaces.

**Hipótesis de integración Flentio:** Flentio no debería ejecutar dentro de APX por defecto. Debería orquestar mediante contratos ASO/API o eventos; cualquier componente APX tendría que ser desarrollado, revisado y desplegado desde el SDLC autorizado del banco.

**Estado:** capacidad APX `CONFIRMADO_PUBLICAMENTE`; detalle técnico `INDICIO_PUBLICO_LIMITADO` y experiencia por contrastar.

### 5. Core y procesos

BBVA declara que sigue construyendo capacidades fundacionales para transformar sistemas core históricos. No publica un mapa completo entre APX/ASO, productos, ledgers, mainframe, sistemas de registro y plataformas locales. [BBVA: escala en software](https://www.bbva.com/en/innovation/bbva-groups-scale-as-a-source-of-value-creation-in-software-development/)

**Estado:** modernización progresiva `CONFIRMADO_PUBLICAMENTE`; topología real `NO_CONFIRMADO_PUBLICAMENTE`.

### 6. ADA: datos, analítica e IA

ADA es la plataforma global cloud-native de datos e IA sobre AWS. BBVA declara despliegue en todas sus geografías, más de 100.000 tareas diarias, 8,4 PB, más de 30.000 datasets activos, 7.500 profesionales de datos y 40.000 usuarios de negocio. Son métricas corporativas, no auditoría independiente. [BBVA: ADA global](https://www.bbva.com/en/innovation/bbva-completes-its-global-move-to-the-cloud-with-a-single-data-and-artificial-intelligence-platform/)

El nuevo MLOps sobre ADA automatiza entornos, versionado, validación, trazabilidad, aprobación y despliegue de modelos usando servicios AWS. [BBVA: arquitectura MLOps](https://www.bbva.com/en/innovation/bbva-develops-a-new-technology-architecture-with-aws-to-accelerate-its-ai-solutions/)

**Hipótesis de integración Flentio:** consumir productos de datos/modelos autorizados y devolver evidencia operativa; no crear un lago paralelo ni reemplazar el gobierno de modelos de ADA.

**Estado:** `CONFIRMADO_PUBLICAMENTE`.

### 7. Infraestructura: NextGen y AWS

Según conocimiento experto aportado al proyecto, BBVA migra cada vez más servicios hacia **NextGen**, su nube privada, y **AWS**, dentro de un modelo híbrido. Se registra como `EXPERIENCIA_EXPERTA_PENDIENTE_DE_CONTRASTE`.

La parte pública confirma estrategia híbrida/multicloud, nube privada, integración progresiva de nube pública y AWS como proveedor preferente para componentes seleccionados. También confirma ADA y banca de inversión en AWS. No publica el porcentaje total de cargas en cada entorno. [BBVA: cloud híbrido y multicloud](https://www.bbva.com/en/innovation/our-development-platform-allows-us-to-build-global-applications-for-the-entire-group/), [BBVA–AWS](https://www.bbva.com/en/bbva-works-amazon-web-services-accelerate-groups-transformation/)

**Estado:** estrategia híbrida y AWS `CONFIRMADO_PUBLICAMENTE`; nombre, alcance y migración a NextGen `EXPERIENCIA_EXPERTA_PENDIENTE_DE_CONTRASTE`; distribución de cargas `NO_CONFIRMADO_PUBLICAMENTE`.

### 8. Ingeniería y entrega

BBVA agrupa globalmente el desarrollo, impulsa DevOps, pruebas automáticas, seguridad integrada y componentes compartidos. En una referencia pública de la web de BBVA España declaró pasar de 10 a 18 releases y de 500 a 2.700 historias en un año, con más de 1.300 pruebas automáticas. Es una fotografía histórica, no el rendimiento actual de todo el banco. [BBVA: Software Development](https://www.bbva.com/en/innovation/bbva-creates-a-software-development-area-to-drive-global-scalable-solutions/)

ONE busca homogeneizar la experiencia y prácticas de más de 15.000 ingenieros. [BBVA ONE](https://www.bbva.com/es/innovacion/bbva-reinventa-el-desarrollo-de-software-con-one/)

**Estado:** modelo global y DevSecOps `CONFIRMADO_PUBLICAMENTE`; herramientas, gates y pipeline real `NO_CONFIRMADO_PUBLICAMENTE`.

### 9. Continuidad, backup y BRS

Existe referencia pública a una prueba técnica de «BRS Local» en BBVA Perú, sin arquitectura ni asociación demostrada con AWS o NextGen. No se conoce públicamente la asignación de recuperación, RTO/RPO, replicación, failover o soberanía por carga.

**Estado:** BRS local histórico `INDICIO_PUBLICO_LIMITADO`; diseño de continuidad actual `NO_CONFIRMADO_PUBLICAMENTE`.

## Contrato de integración objetivo para Flentio

Flentio debe asumir que el banco conserva la autoridad sobre ejecución, identidad, datos y despliegue:

| Interfaz | Flentio puede | Flentio no debe |
|---|---|---|
| Canal/Cells | Proporcionar componente embebible y expediente legible | Sustituir GEMA, SENDA, Experience o el canal local |
| ASO/API | Consultar y solicitar acciones con mínimo privilegio | Acceder directamente a datos internos fuera de contrato |
| APX | Entregar especificación, pruebas y adaptador revisable | Desplegar código autónomamente en APX |
| Core | Referenciar transacciones y estados autorizados | Escribir directamente en ledgers o sistemas de registro |
| ADA | Consumir productos/modelos y devolver resultados gobernados | Duplicar datasets o crear MLOps paralelo |
| NextGen/AWS | Ser desplegable de forma equivalente según política | Elegir ubicación o mover datos sin decisión del banco |
| SDLC | Aportar SBOM, firma, pruebas, policy-as-code y replay | Evitar gates, revisiones o segregación de funciones |

## Despliegue neutral propuesto

El producto debería empaquetarse de manera que la misma versión pueda ser homologada en NextGen o AWS:

1. servicio sin estado donde sea posible;
2. imágenes firmadas y SBOM;
3. configuración externa y secretos en bóveda corporativa;
4. persistencia mediante servicios aprobados, sin dependencia innecesaria de un proveedor;
5. identidad de workload y mTLS/OAuth según estándar interno;
6. observabilidad exportable al SIEM/APM del banco;
7. salida de red denegada por defecto;
8. replay determinista y compensación de acciones;
9. residencia y retención configurables por jurisdicción;
10. despliegue mediante el pipeline del banco, nunca desde el plano SaaS de Flentio.

Este diseño es una propuesta `NO_VALIDADA`, no evidencia de compatibilidad actual.

## Información que falta solicitar

### Arquitectura y hosting

- definición oficial y catálogo de servicios de NextGen;
- criterios de placement entre NextGen, AWS y legado;
- landing zones, regiones permitidas y restricciones de salida;
- plataforma de contenedores, serverless y servicios gestionados autorizados;
- patrones de alta disponibilidad, BRS/DR, RTO y RPO.

### Aplicaciones e integración

- catálogo ASO/API, esquemas, gateway, cuotas y versionado;
- buses/eventos y semántica de entrega;
- patrones APX online/batch y proceso de certificación;
- ownership por dominio y sistemas de registro;
- relación vigente entre Cells, GEMA, SENDA, Horizon y aplicaciones locales.

### Seguridad y entrega

- IAM para usuarios y workloads, segregación de funciones y PAM;
- pipeline, repositorios, SAST/DAST/SCA, firma y atestaciones;
- observabilidad, trazas, SIEM, gestión de incidentes y SLO;
- clasificación de datos, cifrado, KMS/HSM y políticas de secretos;
- proceso de homologación de terceros e IA.

## Próxima validación experta

El siguiente paso no es escribir un conector. Es seleccionar un proceso —por ejemplo, una excepción de pago— y completar una tabla por cada interacción:

| Paso | Canal | Servicio ASO/API | Proceso APX | Sistema de registro | Hosting | Identidad | Evidencia | Reversión |
|---|---|---|---|---|---|---|---|---|
| Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | NextGen/AWS/legado por confirmar | Pendiente | Pendiente | Pendiente |

Hasta completar y autorizar esa tabla, la integración BBVA permanece `ARQUITECTURA_HIPOTÉTICA_NO_VALIDADA`.

