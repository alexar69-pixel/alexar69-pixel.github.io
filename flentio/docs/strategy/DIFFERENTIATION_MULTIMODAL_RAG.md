# Ficha de diferenciación de producto - RAG Multimodal Avanzado (Visión Médica e Imágenes)

> Esta ficha es obligatoria antes de implementar una solución o evolución relevante. Debe distinguir hechos verificados, inferencias e hipótesis. Una hipótesis pendiente nunca se presenta como capacidad operativa ni como ventaja demostrada.

## Identificación

- Propuesta: Procesamiento Multimodal y Visión IA Integrada para Triaje Médico y Soporte Técnico.
- Responsable: Arquitectura
- Fecha y versión: Septiembre 2026, v1.0
- Estado: `NO_VALIDADA`
- Usuarios y proceso afectados: Analistas clínicos, SREs (Site Reliability Engineers) e investigadores de cumplimiento.

## Necesidad no cubierta

- Problema concreto: Actualmente el motor RAG solo puede procesar texto e interpretar PDFs estructurados, dejando fuera una inmensa cantidad de datos corporativos visuales críticos como diagramas de arquitectura en la nube, radiografías DICOM anonimizadas o facturas escaneadas no OCR.
- Frecuencia, impacto y coste actual: Alta. Más del 60% del contexto diagnóstico en hospitales depende de la imagen y los esquemas. En banca/SRE, el 80% de los manuales de red se apoyan en diagramas.
- Evidencia aportada por usuarios o datos operativos: Feedback del inversor (Sector Medical) indica que una IA que no entiende imágenes diagnósticas es un "agente a medias".
- Por qué merece resolverse ahora: Es el factor habilitador para la penetración total en entornos hospitalarios (Medical), desbloqueando automatización en radiología y documentación clínica manuscrita.

## Mercado y alternativas

| Alternativa actual | Qué resuelve | Carencia comprobada | Fuente y fecha |
|---|---|---|---|
| Sistemas OCR Tradicionales | Extracción de texto plano de imágenes | No tienen comprensión contextual ni razonamiento sobre esquemas (ej. no saben qué es un switch de red en un diagrama). | Industria, 2026 |
| ChatGPT Enterprise / Claude Pro | Permite adjuntar imágenes para análisis | Fuga de privacidad masiva. No están enrutados por el Motor DLP de Flentio. | Análisis Competitivo |

- Búsqueda realizada y alcance geográfico/sectorial: Mercado global Healthcare e ITSM Bancario.
- Información que todavía falta: Rendimiento exacto y latencia de inferencia de modelos VLMs (Vision-Language Models) open-source ejecutados on-premise.
- Riesgo de que la necesidad ya esté cubierta: Bajo. Existen modelos visuales, pero no orquestados en un pipeline de flujos de trabajo "No-Code" seguro y auditable.

## Ventaja propuesta de Flentio

- Resultado diferencial esperado: Flentio permitirá arrastrar imágenes (Radiografías, Diagramas AWS) en el Trigger o usar el nodo "Visión IA" para extraer contextos complejos con precisión.
- Flujo no-code para conseguirlo: Nuevo nodo "Procesador Visual", conectado tras el Motor DLP.
- Capacidades verificadas que reutiliza: Motor de flujos actual, auditoría, bóveda criptográfica.
- Capacidades nuevas necesarias: Integración de VLMs (Ej: LLaVA, Florence-2 o Llama-3-Vision) en el Enjambre Multi-IA.
- Qué queda expresamente fuera de alcance: Diagnóstico médico autónomo (la herramienta es soporte, el humano siempre confirma).

## Defensa legítima frente a réplica

Marque y justifique únicamente las defensas reales:

- [X] Integración profunda con procesos autorizados.
- [X] Controles regulatorios, seguridad y auditoría integrados.
- [X] Automatizaciones compuestas difíciles de coordinar por separado.

Explique por qué un competidor competente no podría reproducir el mismo resultado rápidamente sólo copiando la interfaz:
Un competidor puede integrar un modelo de visión, pero el valor de Flentio reside en que la imagen pasa por nuestro **Motor DLP en tiempo real** (para anonimizar etiquetas médicas antes de procesar), se coteja con la base de conocimiento interna (RAG) y deja rastro auditable (WORM) en un flujo gobernado para CFR 21 Part 11.

## Validación y métricas

| Hipótesis | Método de validación | Métrica y umbral | Resultado | Estado |
|---|---|---|---|---|
| Los VLMs open-source son viables en coste/tiempo para procesar un diagrama o DICOM y devolver JSON estructurado. | PoC técnico en entorno aislado | Latencia < 5s por imagen, 90% de exactitud en extracción de etiquetas. | - | `NO_VALIDADA` |

- Criterio para continuar: Superar el 90% de precisión en un entorno de pruebas controlado sin exponer PHI (Datos Médicos Protegidos).
- Criterio para modificar: Si la latencia es demasiado alta, se derivará el procesamiento a un proceso asíncrono.
- Criterio para descartar: Incapacidad de los VLMs locales para entender terminología clínica compleja.

## Riesgos y obligaciones

- Riesgos para cliente, seguridad, privacidad y regulación: Falsos positivos/negativos en el diagnóstico. Exposición de imágenes médicas si el DLP falla.
- Dependencias externas y autorizaciones humanas: Requiere firma electrónica obligatoria (Human in the Loop) antes de emitir informes clínicos basados en visión.
- Portabilidad e interoperabilidad: Formatos DICOM y PNG estándar.
- Cómo se evita dependencia artificial o retención abusiva: Los análisis visuales son efímeros o se almacenan en el SIEM del propio cliente.
- Reversión si la hipótesis no se confirma: El nodo visual se deshabilita, regresando al procesamiento RAG de solo texto.

## Dictamen

- Decisión: `CONTINUAR`
- Evidencia que sustenta la decisión: Interés altísimo del sector Healthcare de inversión.
- Limitaciones y afirmaciones que no pueden comunicarse todavía: No se debe afirmar que la plataforma ya diagnostica imágenes en tiempo real en producción; se comunicará exclusivamente como el *Roadmap Estratégico* Q4.
