# Tecnología interna de bancos líderes — infraestructura, ingeniería y canales (2026)

## Alcance, método y límites

Investigación documental actualizada al 01-08-2026. El análisis se limita al área tecnológica interna: infraestructura y core, plataformas de ingeniería, web y móvil, APIs, datos/IA, DevSecOps y código publicado. Se priorizan informes anuales, páginas corporativas, portales técnicos y organizaciones oficiales en GitHub.

La mayor parte del código de producción de banca web, móvil y core es propietario y no es públicamente auditable. Una oferta de empleo permite comprobar el uso de una tecnología en un equipo, pero no demuestra que sea el estándar de todo el banco. Una alianza cloud tampoco demuestra qué cargas se alojan allí. Este documento separa por ello:

- **Confirmado:** declaración o artefacto primario público.
- **Indicio limitado:** evidencia de un equipo o componente, no extrapolable al conjunto.
- **No público:** no existe evidencia suficiente para afirmarlo.

No se ha realizado ingeniería inversa, análisis de binarios, escaneo ni acceso a sistemas de terceros.

## Conclusión ejecutiva

1. **No hay un único patrón cloud.** Santander está trasladando el core desde mainframe a Gravity, su plataforma cloud-native; ING combina nube privada, plataforma bancaria y pipeline común; BBVA ha globalizado en AWS su plano de datos e IA; Capital One declara operar completamente en cloud. Esto no autoriza a asumir que todo el patrimonio aplicativo de cada banco sea cloud-native.
2. **La plataforma interna es el activo central.** Gravity+ODS, Ether con ASO/APX y Cells, ADA, ONE, ING Scalable Tech Platform y los sistemas modulares de DBS buscan reutilización, controles comunes y despliegue global. Un producto externo que duplique estas capas tendrá una adopción difícil.
3. **Web y app son sólo la superficie.** Santander es el caso que más explícitamente publica la separación: ODS como tecnología cloud interna para apps/web y Gravity como back-end. Los demás publican componentes, prácticas o plataformas, pero no el árbol real de dependencias de sus canales.
4. **El código abierto es una ventana parcial.** ING y JPMorganChase publican proyectos reales y mantenidos; BBVA publica, entre otros, Mercury. Sirven para observar capacidades y cultura, pero no representan el código de sus apps bancarias ni sus controles internos completos.
5. **La IA ya entra en ingeniería.** JPMorganChase declara asistentes de código usados por más del 90% de sus ingenieros; BBVA automatiza gobierno y despliegue de ML en ADA; DBS declara automatización de ingeniería. Generación de código aislada no es una oportunidad diferencial.
6. **Implicación para Flentio:** debe ser una capa federada de evidencia, autoridad y ejecución de excepciones sobre plataformas existentes, usando APIs y contratos estables. No debe pretender reemplazar el core, la plataforma de desarrolladores, el canal web/móvil ni el MLOps del banco.

## Matriz comparativa

| Entidad | Infraestructura/core confirmados | Plataforma de ingeniería y entrega | Web/móvil y APIs | Código público observable | Transparencia pública |
|---|---|---|---|---|---|
| Santander | Gravity, core cloud-native propio; migración paralela desde mainframe; despliegue global en progreso | Stack global propio; 24.000 profesionales tecnológicos declarados; más de 400 cambios semanales en la visión Gravity 2.0 | ODS, tecnología cloud interna para apps/web; Openbank US combina ODS con Gravity | Proyectos de IA publicados, pero no código de ODS/Gravity ni de la app | **Alta** en arquitectura objetivo; **baja** en implementación concreta |
| BBVA | Ether incorpora capacidades corporativas como ASO, APX y Cells; ADA global sobre AWS cubre datos e IA, no todo el core/canal | ONE para más de 15.000 ingenieros; plataforma global de desarrollo; APX online/batch y ASO/API aparecen en procesos y servicios; MLOps común en ADA | Reutilización de componentes y productos globales; Cells para canal; detalle actual del código de la app no público | Mercury y otros activos puntuales; no la app bancaria ni APX/ASO | **Alta** en capacidades de plataforma; **baja** en implementación propietaria |
| ING | Scalable Tech Platform: ING Private Cloud, OnePipeline y Banking Technology Platform | Infraestructura autoservicio, pipeline común, componentes reutilizables; objetivos y adopción publicados | Developer Portal/APIs; IPC aloja servicios como apps móviles. Un equipo de gateway publica Java, OpenShift, Azure DevOps y observabilidad, sólo como indicio local | Organización oficial con proyectos de web components, orquestación, seguridad, datos y testing | **Alta** en modelo de plataforma; **media** en componentes; **baja** en app final |
| JPMorganChase | Uso combinado de infraestructura privada y proveedores públicos; detalle de distribución de cargas no público | IA para ingeniería a gran escala; plataformas y herramientas internas no expuestas íntegramente | Catálogos de APIs/SDK; Salt Design System y Modular muestran componentes front-end, no el canal Chase completo | Organización oficial con decenas de repositorios en TypeScript, Python, Kotlin y otros | **Media** en cultura/herramientas; **baja** en arquitectura productiva del canal |
| DBS | Objetivo de stack cloud-optimised; sistemas modulares/reutilizables; plataforma empresarial de datos y analítica ADA | Automatización de ingeniería; en 2025 declara 25% menos tiempo de despliegue de código | No se publica arquitectura completa ni código de la app/web | Sin evidencia suficiente en esta revisión para equipararlo a los repositorios anteriores | **Media** en dirección y resultados; **baja** en detalle técnico |
| Capital One | Declara operar completamente en cloud y usar serverless a escala | Fuerte orientación open source; historial público detallado de CI/CD móvil | Evidencia histórica de CI compartido para iOS/Android, 3.000–4.000 builds diarios; no debe tratarse como estado actual sin nueva confirmación | Amplia ingeniería pública, pero no código de la app bancaria | **Alta** en filosofía cloud; evidencia móvil pública **antigua** |

## Lectura por entidad

### Santander: plataforma vertical propia, del core al canal

Es el competidor con la descripción pública más completa de una plataforma bancaria integrada:

- Gravity es software y plataforma core cloud-native desarrollada internamente. Permite ejecutar en paralelo mainframe y cloud para probar en tiempo real sin interrumpir el servicio. Santander declara que está implantada al 70% y que Gravity 2.0 aspira a operar capacidades globales entre 2026 y 2028. [Santander: Gravity](https://www.santander.com/en/stories/7-questions-on-how-gravity-is-transforming-santander), [Investor Day 2026](https://www.santander.com/content/dam/santander-com/es/documentos/otra-informacion-relevante/2026/02/hr-2026-02-25-investor-day-executive-chair-presentation-disponible-solo-en-ingles-es.pdf)
- ODS es la tecnología cloud interna del front-end de apps y sitios web. Openbank en Estados Unidos combina ODS con Gravity, mostrando una separación explícita entre experiencia/canal y core. [Informe semestral 2024](https://www.santander.com/content/dam/santander-com/en/documentos/informacion-publica-periodica-c-n-m-v-/2024/cnmv-2024-informe-financiero-semestral-1s-2024-en.pdf), [Openbank US](https://www.santander.com/en/press-room/features/openbank-us-milestone-in-santander-transformation)
- La información pública no revela repositorios, lenguajes, topología de servicios, controles CI/CD ni dependencias de la app. Por tanto, no es válido afirmar que conocemos el código o la arquitectura física completa.

**Lectura competitiva:** Santander está internalizando una plataforma vertical global. Flentio sólo tendría cabida si se integra con su capa de APIs/eventos y aporta controles de proceso que Gravity/ODS no declaren cubrir, sin competir con el core o el front-end.

### BBVA: plataforma global de ingeniería, datos e IA

- **Corrección de alcance: ASO/APX son piezas esenciales del mapa transaccional y de procesos.** Informes oficiales de BBVA Colombia describen Ether como la plataforma que reúne capacidades de Channels, API/ASO, Data, APX, Advanced Middleware, DevOps y Security. También documentan funcionalidades de negocio reutilizables en ASO y APX. BBVA Perú informa de ejecución de ASO y APX Physics, adopción DevOps y trazabilidad desde planificación hasta análisis de código y seguridad. [BBVA Colombia 2019](https://accionistaseinversores.bbva.com/wp-content/uploads/2020/12/COLOMBIA_Informe-Anual-2019_esp.pdf), [BBVA Perú 2021](https://accionistaseinversores.bbva.com/wp-content/uploads/2023/05/memoria-anual-Peru-2021-informe-integrado.pdf)
- La evidencia pública y las ofertas técnicas actuales vinculan **ASO** con la arquitectura/catálogo de servicios y APIs, y **APX** con desarrollo backend Java tanto online como batch. Esta segunda fuente es un indicio operativo, no documentación pública completa del producto interno. No se deben inventar sus contratos, runtime, topología o versiones sin documentación autorizada de BBVA.
- **Modelo operativo híbrido NextGen + AWS.** Según conocimiento experto aportado al proyecto, BBVA migra progresivamente servicios hacia **NextGen**, su nube privada, y hacia AWS, distribuyendo las cargas según sus requisitos. Esta descripción queda `EXPERIENCIA_EXPERTA_PENDIENTE_DE_CONTRASTE` hasta validarla con inventario, estándares de hosting o arquitectura interna autorizada. Es coherente con la estrategia pública híbrida/multicloud: BBVA partió de nube privada e integra progresivamente componentes en nubes públicas. AWS fue nombrado proveedor preferente de infraestructura cloud para migrar **componentes seleccionados**, y existen cargas importantes confirmadas —ADA y la plataforma de banca de inversión—, además de alianzas con Google Cloud, Microsoft Azure, Red Hat, Cisco y otros. [BBVA: estrategia híbrida y multicloud](https://www.bbva.com/en/innovation/our-development-platform-allows-us-to-build-global-applications-for-the-entire-group/), [acuerdo AWS](https://www.bbva.com/en/bbva-works-amazon-web-services-accelerate-groups-transformation/), [alianzas tecnológicas](https://www.bbva.com/en/innovation/alliances-that-keep-bbva-at-the-forefront-of-technology/)
- Un informe de BBVA Perú menciona una prueba técnica de un «plan BRS Local», pero no identifica AWS como su soporte ni permite extrapolar el diseño de continuidad al Grupo. El papel de AWS en backup, disaster recovery o BRS queda `NO_CONFIRMADO_PUBLICAMENTE` hasta disponer de arquitectura de continuidad, regiones, RTO/RPO y matriz de cargas autorizada. [BBVA Perú 2020](https://accionistaseinversores.bbva.com/wp-content/uploads/2021/06/Informe-Anual-Integrado-Peru-2020_esp.pdf)
- ONE normaliza cultura, colaboración y prácticas para más de 15.000 ingenieros. BBVA ya describía una plataforma global con automatización y seguridad para construir aplicaciones reutilizables entre geografías. [BBVA ONE](https://www.bbva.com/es/innovacion/bbva-reinventa-el-desarrollo-de-software-con-one/), [plataforma global](https://www.bbva.com/es/innovacion/nuestra-plataforma-de-desarrollo-nos-habilita-para-construir-aplicaciones-globales-para-todo-el-grupo/)
- ADA es su plataforma global de datos e IA basada en AWS, desplegada en todas sus geografías desde 2025. En 2026 BBVA añadió una arquitectura MLOps con entornos comunes, reutilización y automatización de controles; declara más de 6.500 usuarios internos y reducciones de hasta el 75% en ciertos ciclos de desarrollo. Son cifras corporativas, no auditoría independiente. [BBVA ADA global](https://www.bbva.com/es/innovacion/2025-un-ano-en-el-que-bbva-completa-el-salto-global-a-la-nube-con-una-unica-plataforma-de-datos-e-inteligencia-artificial/), [MLOps](https://www.bbva.com/es/innovacion/bbva-desarrolla-junto-a-aws-una-nueva-arquitectura-tecnologica-para-acelerar-sus-soluciones-de-ia/)
- Mercury confirma reutilización de código analítico interno abierto posteriormente; parte de sus componentes se vincula a recomendaciones y categorización de movimientos en la app. No publica el código de la app ni demuestra el stack completo del canal. [BBVA Mercury](https://www.bbva.com/es/innovacion/bbva-comparte-su-libreria-de-codigo-mercury-con-la-comunidad-de-desarrolladores-open-source/)

**Lectura competitiva:** BBVA ya dispone de plataforma transaccional y de procesos sobre Ether/ASO/APX/Cells, además de data/AI platform y disciplina de ingeniería global. Flentio debe integrarse con los servicios ASO/APIs y cargas APX autorizadas, y con modelos/datos gobernados por ADA; no recrear estas plataformas, MLOps, RAG genérico o un portal de agentes horizontal.

### ING: ingeniería de plataforma explícita y código abierto observable

- El informe anual 2025 define la Scalable Tech Platform mediante tres piezas: ING Private Cloud, OnePipeline y Banking Technology Platform; esta última aloja componentes modulares reutilizados entre países y líneas de negocio. [ING Annual Report 2025](https://ing.com/binaries/content/assets/documents/annual-reports/2025-ing-groep-nv-annual-report.pdf)
- ING había descrito IPC como infraestructura estandarizada, autoservicio para desarrollo/operaciones y alojamiento de servicios como apps móviles. Su Developer Portal expone APIs internas y algunas para terceros. [ING cloud](https://ing.com/news/2021/01/banks-on-cloud-nine.html), [ING Annual Report 2018](https://www.ing.com/MediaEditPage/2018-Annual-Report-ING-Groep-N.V..htm)
- Una vacante de 2026 para un equipo de API Gateway enumera Java, Python, Bash, Rego, OpenShift, Azure DevOps, Grafana, Prometheus, ELK, OAuth2/JWT y Zero Trust. Es evidencia válida para ese componente, no para toda ING ni para su app. [ING API Gateway](https://careers.ing.com/en/job/bukarest/senior-java-developer-api-gateway-ing-hubs-romania/3121/36065345344)
- Su [organización oficial de GitHub](https://github.com/orgs/ing-bank/repositories) publica proyectos como Lion (web components), Baker (orquestación), INGenious (testing), Rokku (acceso S3) y herramientas de datos/seguridad. Esto prueba profundidad técnica pública, pero no expone sistemas bancarios productivos.

**Lectura competitiva:** es un entorno platform-engineering maduro. La integración de Flentio debería adoptar contratos API/eventos, observabilidad y despliegue independiente; vender otro pipeline o catálogo de componentes sería redundante.

### JPMorganChase: enorme plataforma interna y adopción masiva de IA en desarrollo

- En su informe 2025, el banco declara que más del 90% de sus ingenieros usa asistentes de código. También mantiene LLM Suite como plataforma interna y una estrategia de datos preparada para IA. [JPMorganChase Annual Report 2025](https://www.jpmorganchase.com/ir/annual-report/2025/ar-ceo-letter-petno-rohrbaugh)
- La organización oficial de GitHub publica 74 repositorios en la captura consultada, incluidos Salt Design System, Modular, SDKs, investigación y herramientas de notebooks. También ofrece portales de APIs para Chase y J.P. Morgan. [JPMorganChase Open Source](https://github.com/jpmorganchase)
- Estos activos permiten observar estándares de UI, investigación y SDK, pero no reconstruir la aplicación Chase, sus backends ni la cadena de suministro interna.

**Lectura competitiva:** su escala impide competir con asistentes horizontales, plataformas LLM o tooling general. Una oportunidad exige un proceso bancario estrecho, integración federada y evidencia regulatoria superior a la que aporten sus plataformas internas.

### DBS: modernización modular y automatización de ingeniería

El CIO de DBS declara para 2025 sistemas modulares y reutilizables, una plataforma empresarial gobernada de datos/analítica, automatización de procesos de ingeniería, reducción del 25% en tiempo de despliegue de código y objetivo de un stack completamente optimizado para cloud. No publica suficiente detalle para identificar frameworks de web/app o afirmar qué proporción del core está modernizada. [DBS CIO Statement 2025](https://www.dbs.com/annualreports/2025/cio-statement.html)

**Lectura competitiva:** los resultados refuerzan el patrón de plataforma y reutilización, pero el bajo detalle público obliga a discovery técnico con la entidad antes de diseñar conectores.

### Capital One: referencia cloud, con evidencia móvil que debe fecharse

Capital One declara operar totalmente en cloud, usar serverless a escala y priorizar open source. [Capital One technology stack](https://www.capitalone.com/tech/our-stack/). Una publicación técnica histórica describió CI/CD compartido para iOS y Android, con 3.000–4.000 builds móviles diarios y uso de Fastlane, Xcode, infraestructura Mac y AWS. La fuente es de 2019 y sólo sirve como antecedente, no como confirmación del stack actual. [Capital One mobile CI/CD](https://www.capitalone.com/tech/software-engineering/4-lessons-from-scaling-ios-ci-cd/)

## Qué sabemos realmente sobre el código web y móvil

| Pregunta | Respuesta defendible |
|---|---|
| ¿Podemos revisar el código de las apps bancarias? | No. No está publicado y no se debe inferir desde binarios ni ofertas de empleo. |
| ¿Los repositorios públicos reflejan producción? | Algunos proyectos sí nacen de necesidades internas, pero no prueban que estén desplegados en el canal ni muestran configuración, controles o versiones internas. |
| ¿Podemos conocer frameworks concretos? | Sólo en componentes expresamente publicados. Lion o Salt prueban capacidades front-end abiertas de ING/JPMC; no que toda su banca web use exclusivamente esas librerías. |
| ¿Podemos deducir arquitectura desde una vacante? | Sólo como indicio del equipo y fecha mencionados. No como arquitectura corporativa. |
| ¿Qué falta para evaluar una entidad concreta? | Inventario aplicativo, diagramas C4, catálogo API/eventos, ownership, repositorios autorizados, SBOM, pipelines, SLO, incidentes, modelo IAM y mapa de datos. |

## Estado de madurez observable

Escala cualitativa basada únicamente en evidencia pública; **no es una auditoría ni ranking global**.

| Capacidad | Santander | BBVA | ING | JPMorganChase | DBS |
|---|---|---|---|---|---|
| Arquitectura objetivo publicada | Alta | Media | Alta | Baja-media | Media |
| Plataforma interna reutilizable | Alta | Alta | Alta | Alta | Alta |
| Modernización cloud observable | Alta, core en progreso | Alta en datos/IA | Alta, híbrida/privada | Parcialmente pública | Dirección clara, detalle limitado |
| Canal web/móvil documentado | Media (ODS) | Baja-media | Media | Baja | Baja |
| Código abierto útil para ingeniería | Media | Media | Alta | Alta | No determinado |
| IA aplicada al SDLC/ML lifecycle | Alta | Alta | Media-alta | Muy alta | Alta |

## Consecuencias para la arquitectura de Flentio

### Lo que Flentio no debe construir

- un nuevo core bancario;
- un front-end bancario universal que sustituya las apps existentes;
- otra internal developer platform, pipeline CI/CD o portal API;
- una nueva plataforma MLOps horizontal;
- un copiloto de código genérico;
- un repositorio que requiera copiar código o datos sensibles del banco.

### Interfaz de entrada viable

Flentio debería funcionar como **control plane federado de procesos**, desplegable en el perímetro elegido por el banco:

1. conectores API/eventos de mínimo privilegio hacia core, canal, BPM, GRC y observabilidad;
2. adaptador de identidad a IAM corporativo y separación de funciones;
3. contratos versionados para evidencia, decisiones, comandos y compensaciones;
4. ejecución local o por proveedor autorizado, sin obligar a sacar datos;
5. registro inmutable/reconstruible, pero con referencias a datos maestros en origen;
6. SDK y componentes UI embebibles para que la experiencia aparezca dentro de la app, web o herramienta interna existente;
7. controles automatizables desde el pipeline del banco: policy-as-code, pruebas de replay, SBOM, firma y atestación.

### Diferenciación que aún debe validarse

La hipótesis defendible no es «Flentio conoce mejor la tecnología que el banco». Es:

> Flentio puede convertir conocimiento operativo bancario, autoridad delegada y evidencia regulatoria en un contrato ejecutable y portable entre plataformas internas heterogéneas, sin sustituirlas.

Sigue en estado `NO_VALIDADA`. Su barrera legítima surgiría de taxonomías de procesos/excepciones, integraciones aprobadas, casos de replay y evidencia histórica autorizada; no de ocultar código ni crear dependencia artificial.

## Siguiente investigación necesaria

Para pasar de mercado público a diseño real se necesita seleccionar **una entidad tipo y un proceso**, y completar con conocimiento experto:

1. sistemas que participan y sistema de registro por dato;
2. canal que inicia la operación: app, web, oficina, API o batch;
3. eventos, APIs y colas disponibles;
4. pasos manuales, excepciones y compensaciones;
5. identidad, roles, límites y doble autorización;
6. controles del pipeline y requisitos de despliegue;
7. observabilidad, SLA/SLO, incidentes y evidencias exigidas;
8. restricción cloud/on-prem y política de modelos de IA.

Hasta obtener esa información, cualquier diagrama de integración de una entidad concreta debe marcarse `ARQUITECTURA_HIPOTÉTICA_NO_VALIDADA`.

## Estado

Investigación pública completada para orientar producto. No se ha auditado código propietario ni infraestructura interna. Las conclusiones competitivas e hipótesis de integración permanecen `NO_VALIDADA` hasta contrastarlas con responsables de arquitectura, ingeniería, operaciones, seguridad y riesgo de una entidad.
