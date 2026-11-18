# Ficha de diferenciación: laboratorio gobernado de presentación

## Identificación

- Propuesta: Centro de Demostración autocontenido y verificable.
- Responsable: Flentio.
- Fecha y versión: 02-08-2026, v1.
- Estado: `NO_VALIDADA` comercialmente; implementación técnica en validación local.
- Usuarios: responsables de operaciones, SRE, seguridad, riesgo y tecnología que
  evalúan el producto antes de existir una integración cliente.

## Necesidad no cubierta

Un comprador debe comprender la correlación gobernada, las contradicciones y la
revisión humana sin entregar antes sus sistemas o documentos. Una demo estática
no acredita el motor; una demo que finge conectores degrada confianza. No se ha
validado todavía mediante entrevistas que esta carencia determine una compra.

## Mercado y alternativas

| Alternativa | Qué resuelve | Carencia pendiente de contrastar |
|---|---|---|
| Capturas o vídeo | Narrativa repetible | No prueba interacción ni cálculo real |
| Sandbox con mocks | Recorrido controlado | Puede ocultar fallos y confundirse con capacidad operativa |
| Prueba contra cliente | Máxima fidelidad | Exige acceso, seguridad y tiempo antes de evaluar el producto |

La comparación competitiva específica sigue pendiente. No se afirma que esta
experiencia sea única ni que ningún competidor disponga de laboratorio similar.

## Ventaja propuesta de Flentio

- Ejecutar código real sobre acontecimientos sintéticos físicamente separados.
- Hacer visibles causalidad no establecida, contradicciones y abstención.
- Restaurar sólo la sesión demo con confirmación explícita.
- Mostrar de manera conjunta qué está operativo, disponible para configurar y
  dependiente del futuro cliente.

Quedan fuera la remediación, homologación bancaria y cualquier resultado de ROI.

## Defensa legítima frente a réplica

- [x] Conocimiento especializado y trazable.
- [x] Controles de seguridad y auditoría integrados.
- [x] Automatización compuesta entre correlación, contradicción y revisión.
- [x] Experiencia no-code.

La defensa potencial no es la interfaz: es mantener alineados manifests,
aislamiento, motor, evidencia, auditoría, conectores reales y fronteras de
ejecución. Esa ventaja sigue siendo una hipótesis hasta medirla con evaluadores.

## Validación y métricas

| Hipótesis | Método | Umbral inicial | Estado |
|---|---|---|---|
| Un evaluador entiende el valor sin asistencia técnica | Cinco demos observadas | 4/5 explican correlación, abstención y revisión | `NO_VALIDADA` |
| El recorrido es repetible | Reinicios automáticos | 100 % sin datos residuales fuera de la sesión | Validación local |
| La demo acelera el acceso a un piloto | Seguimiento comercial | Mediana menor a dos reuniones | `NO_VALIDADA` |

Continuar si el recorrido es comprendido y genera solicitudes de piloto;
reformular si se percibe como dashboard genérico; descartar claims diferenciales
si una comparación ciega no muestra ventaja.

## Riesgos y dictamen

Riesgos: confundir sintético con cliente, interpretar confianza como causalidad o
presentar runtimes como conexiones. Se mitigan mediante marcas persistentes,
estados literales y guion. No hay retención artificial: los manifests son
versionados y los conectores interoperables.

- Decisión: `CONTINUAR` con validación comercial.
- No comunicar todavía: superioridad competitiva, precisión bancaria, ROI,
  reducción de MTTR o preparación productiva.
