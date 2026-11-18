import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # blank layout

    # Color palette
    BG_DARK = RGBColor(6, 6, 15)        # #06060f
    CARD_BG = RGBColor(15, 15, 34)      # #0f0f22
    BORDER_COLOR = RGBColor(34, 211, 238) # #22d3ee
    TEXT_LIGHT = RGBColor(241, 241, 243) # #f1f1f3
    TEXT_MUTED = RGBColor(156, 163, 175) # #9ca3af
    ACCENT_AMBER = RGBColor(249, 115, 22) # #f97316
    ACCENT_CYAN = RGBColor(34, 211, 238) # #22d3ee
    ACCENT_RED = RGBColor(239, 68, 68)   # #ef4444
    ACCENT_MINT = RGBColor(52, 211, 153) # #34d399

    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(repo_dir, "blog", "assets")
    diag_dir = os.path.join(assets_dir, "presentation")
    hero_img = os.path.join(assets_dir, "adamuz-urda-kpis-seguridad-ave.png")
    andon_concept_img = os.path.join(diag_dir, "toyota_andon_stop_the_line.jpg")

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_card(slide, left, top, width, height, border_color=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()
        return card

    def add_header(slide, title, category="// RELIABILITY & RESILIENCIA EN INFRAESTRUCTURA"):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p_cat = tf.paragraphs[0]
        p_cat.text = category
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN
        
        p_tit = tf.add_paragraph()
        p_tit.text = title
        p_tit.font.size = Pt(22)
        p_tit.font.bold = True
        p_tit.font.color.rgb = TEXT_LIGHT

    # ==========================================================
    # SLIDE 1: PORTADA
    # ==========================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)
    if os.path.exists(hero_img):
        s1.shapes.add_picture(hero_img, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))
        overlay = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        overlay.fill.solid()
        overlay.fill.fore_color.rgb = RGBColor(6, 6, 15)
        
    s1_card = add_card(s1, Inches(1), Inches(1.2), Inches(11.333), Inches(5.1), ACCENT_CYAN)
    tf1 = s1_card.text_frame
    tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "// KEYNOTE · INFRAESTRUCTURA CRÍTICA & SRE"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_CYAN

    p1 = tf1.add_paragraph()
    p1.text = "LA TRAMPA DEL MINUTERO"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT

    p2 = tf1.add_paragraph()
    p2.text = "Reliability, Resiliencia y la Ilusión del 99.9% en Sistemas de Alta Velocidad"
    p2.font.size = Pt(20)
    p2.font.color.rgb = ACCENT_AMBER

    p3 = tf1.add_paragraph()
    p3.text = "\nAlexander Armentia (Alexar69)\nReliability & Resilience Manager | +25 años en operaciones críticas"
    p3.font.size = Pt(15)
    p3.font.color.rgb = TEXT_MUTED

    s1.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "(Pausa inicial de 3 segundos en silencio antes de hablar).\n"
        "Llevo más de 25 años gestionando sistemas donde el error no es una opción aceptable. "
        "En una War Room bancaria, cuando un servicio crítico empieza a degradarse, el tiempo se mide en pulsaciones por minuto y en millones de transacciones en juego.\n"
        "Pero cuando la infraestructura transporta personas a 300 km/h, la responsabilidad adquiere una dimensión sagrada. "
        "Al ver las noticias de Adamuz en enero de 2026 y luego Urda en octubre, sentí ese nudo en el estómago que todos los que operamos sistemas conocemos: "
        "la confirmación de que la obsesión moderna por los KPIs de eficiencia está matando la resiliencia."
    )

    # ==========================================================
    # SLIDE 2: GOODHART & NORMALIZACIÓN DE LA DESVIACIÓN
    # ==========================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "LA LEY DE GOODHART Y LA NORMALIZACIÓN DE LA DESVIACIÓN")

    c2_left = add_card(s2, Inches(0.8), Inches(1.35), Inches(5.2), Inches(5.6), ACCENT_AMBER)
    tf2 = c2_left.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = '"Cuando una métrica se convierte en el objetivo, deja de ser una buena métrica."'
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT

    p = tf2.add_paragraph()
    p.text = (
        "\n1. El incentivo perverso:\n"
        "   El compromiso de puntualidad y las penalizaciones económicas empujan a no detener convoyes por 'sospechas menores'.\n\n"
        "2. Normalización de la desviación (Diane Vaughan):\n"
        "   Si una vibración anómala o una fisura microscópica no causó un accidente ayer, se reclasifica tácitamente como tolerable hoy.\n\n"
        "3. El espejismo del cuadro de mando:\n"
        "   El SLA comercial marca 99.8% verde mientras la fatiga física y el estrés estructural crecen de forma exponencial e invisible."
    )
    p.font.size = Pt(12.5)
    p.font.color.rgb = TEXT_MUTED

    d2_path = os.path.join(diag_dir, "slide2_goodhart_deviance.png")
    if os.path.exists(d2_path):
        s2.shapes.add_picture(d2_path, Inches(6.25), Inches(1.35), width=Inches(6.28), height=Inches(3.53))
    
    c2_callout = add_card(s2, Inches(6.25), Inches(5.05), Inches(6.28), Inches(1.9), ACCENT_RED)
    tf2_c = c2_callout.text_frame
    tf2_c.word_wrap = True
    p = tf2_c.paragraphs[0]
    p.text = "ANÁLISIS DEL GRÁFICO:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED
    p = tf2_c.add_paragraph()
    p.text = "Mientras el cuadro de mando superior reporta '99.8% puntualidad' (ilusión verde), la curva roja de tensión acumulada rebasa el límite de seguridad sin alertar al operador hasta la rotura súbita."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_LIGHT

    s2.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "Miren el gráfico de la derecha. En el cuadro de mando superior todo está en verde: 99.8% de puntualidad, vía saturada con ingresos máximos. "
        "Pero debajo, en el mundo físico, cada punto amarillo es una vibración ignorada con el argumento 'ayer pasó el tren y no ocurrió nada'. "
        "Eso es exactamente la normalización de la desviación descrita por Diane Vaughan en el Challenger. "
        "Cuando el KPI de eficiencia manda sobre el de seguridad, el desastre ya ha empezado; solo falta que llegue el día de la rotura."
    )

    # ==========================================================
    # SLIDE 3: ADAMUZ VS URDA (ANATOMÍA DE DOS FALLOS)
    # ==========================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "ADAMUZ Y URDA: RADIOGRAFÍA DE DOS QUIEBRAS CRÍTICAS")

    c3_left = add_card(s3, Inches(0.8), Inches(1.35), Inches(5.2), Inches(5.6), ACCENT_CYAN)
    tf3 = c3_left.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "DOS ACCIDENTES, DOS DIMENSIONES DISTINTAS"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p = tf3.add_paragraph()
    p.text = (
        "\n• ADAMUZ (Enero 2026):\n"
        "  - Quiebra de Fiabilidad: Rotura de carril / soldadura y degradación de asiento de balasto.\n"
        "  - Ceguera a señales débiles: convoyes previos sintieron el bote.\n"
        "  - Quiebra de Blast Radius: Invasión de vía contraria sin corte preventivo de gálibo.\n\n"
        "• URDA (Octubre 2026):\n"
        "  - Fallo operativo nominal: Un tren averiado detenido en vía (sucede).\n"
        "  - Quiebra de Resiliencia: El sistema no degradó elegantemente.\n"
        "  - Quiebra de Fail-Safe: Choque por alcance en el mismo cantón."
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    d3_path = os.path.join(diag_dir, "slide3_adamuz_vs_urda.png")
    if os.path.exists(d3_path):
        s3.shapes.add_picture(d3_path, Inches(6.25), Inches(1.35), width=Inches(6.28), height=Inches(3.53))
    
    c3_callout = add_card(s3, Inches(6.25), Inches(5.05), Inches(6.28), Inches(1.9), ACCENT_AMBER)
    tf3_c = c3_callout.text_frame
    tf3_c.word_wrap = True
    p = tf3_c.paragraphs[0]
    p.text = "ANÁLISIS COMPARATIVO:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p = tf3_c.add_paragraph()
    p.text = "Adamuz ilustra la quiebra física de fiabilidad con invasión de contorno. Urda evidencia el fallo más grave en ingeniería de sistemas: la quiebra de la redundancia fail-safe donde el fallo arrastra a otro convoy."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_LIGHT

    s3.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "Como vemos en el esquema técnico de la derecha, Adamuz y Urda representan las dos pesadillas de un arquitecto de fiabilidad. "
        "En Adamuz falla el metal (reliability), pero la catástrofe se magnifica porque el descarrilamiento invade la vía contraria sin aislamiento de radio de impacto. "
        "En Urda es todavía más doloroso desde la perspectiva de sistemas: que una máquina se pare es un suceso previsto en cualquier manual. "
        "Lo inaceptable es que la señalización y el bloqueo permitan que un segundo tren entre en el cantón ocupado. El principio fail-safe fue violado."
    )

    # ==========================================================
    # SLIDE 4: RELIABILITY VS RESILIENCIA (MATRIZ)
    # ==========================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "RELIABILITY VS. RESILIENCIA: NO SON SINÓNIMOS")

    c4_left = add_card(s4, Inches(0.8), Inches(1.35), Inches(5.2), Inches(5.6), ACCENT_MINT)
    tf4 = c4_left.text_frame
    tf4.word_wrap = True
    p = tf4.paragraphs[0]
    p.text = "LA DIFERENCIA ENTRE EVITAR EL FALLO Y SOBREVIVIR A ÉL"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_MINT

    p = tf4.add_paragraph()
    p.text = (
        "\n• FIABILIDAD (Reliability):\n"
        "  - Filosofía: 'Diseñar e inspeccionar para que nada rompa'.\n"
        "  - Indicador clave: MTBF (Mean Time Between Failures).\n"
        "  - Vulnerabilidad: En el mundo físico, los materiales sufren fatiga y el software tiene imprevistos. La fiabilidad es finita.\n\n"
        "• RESILIENCIA (Resilience):\n"
        "  - Filosofía: 'Asumir que el fallo ocurrirá y contener su daño'.\n"
        "  - Indicador clave: MTTR y Radio de Impacto (Blast Radius).\n"
        "  - Misión: Que la rotura no cause pérdidas humanas."
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    d4_path = os.path.join(diag_dir, "slide4_rel_vs_res.png")
    if os.path.exists(d4_path):
        s4.shapes.add_picture(d4_path, Inches(6.25), Inches(1.35), width=Inches(6.28), height=Inches(3.53))
    
    c4_callout = add_card(s4, Inches(6.25), Inches(5.05), Inches(6.28), Inches(1.9), ACCENT_CYAN)
    tf4_c = c4_callout.text_frame
    tf4_c.word_wrap = True
    p = tf4_c.paragraphs[0]
    p.text = "LA MATRIZ DE DECISIÓN:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p = tf4_c.add_paragraph()
    p.text = "La fiabilidad protege el balance contable y la puntualidad comercial en días normales; la resiliencia es el cinturón de seguridad que protege la vida humana cuando la fiabilidad se agota."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_LIGHT

    s4.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "Observen la comparativa en pantalla. Si solo invertimos en fiabilidad, somos como un funambulista que entrena su equilibrio pero se niega a poner una red debajo. "
        "El equilibrio es la Reliability; la red es la Resiliencia. "
        "En un sistema de alta velocidad, si una soldadura parte a 300 km/h, la fiabilidad ha terminado. "
        "En ese milisegundo exacto, lo único que decide si hay un susto técnico o un luto nacional es la arquitectura de resiliencia del sistema."
    )

    # ==========================================================
    # SLIDE 5: EL PRINCIPIO ANDON (STOP THE LINE - TOYOTA SYSTEM)
    # ==========================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "EL PRINCIPIO ANDON: 'STOP THE LINE' (TOYOTA SYSTEM)")

    c5_left = add_card(s5, Inches(0.8), Inches(1.35), Inches(5.2), Inches(5.6), ACCENT_AMBER)
    tf5 = c5_left.text_frame
    tf5.word_wrap = True
    p = tf5.paragraphs[0]
    p.text = "LA VALENTÍA Y EL DEBER MORAL DE DETENER LA MARCHA"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER

    p = tf5.add_paragraph()
    p.text = (
        "\n1. El origen en Toyota:\n"
        "   En las plantas de producción de Toyota, cualquier operario que detecte una pieza dudosa tira de la cuerda Andon o pulsa el botón rojo, deteniendo la cadena entera.\n\n"
        "2. Sin represalias, sin broncas:\n"
        "   El jefe de equipo acude no para sancionar, sino para decir: 'Gracias por proteger la calidad y evitar que salgan vehículos defectuosos'.\n\n"
        "3. La pregunta crítica para el AVE:\n"
        "   ¿Tiene hoy un maquinista o técnico de vía el respaldo institucional para frenar el corredor ante un golpe anómalo, sabiendo que arruinará el SLA de puntualidad?"
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    if os.path.exists(andon_concept_img):
        s5.shapes.add_picture(andon_concept_img, Inches(6.25), Inches(1.35), width=Inches(6.28), height=Inches(3.53))
    
    c5_callout = add_card(s5, Inches(6.25), Inches(5.05), Inches(6.28), Inches(1.9), ACCENT_AMBER)
    tf5_c = c5_callout.text_frame
    tf5_c.word_wrap = True
    p = tf5_c.paragraphs[0]
    p.text = "ILUSTRACIÓN CONCEPTUAL: LA CUERDA ANDON EN ACCIÓN"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p = tf5_c.add_paragraph()
    p.text = "La imagen muestra al operario activando la señal Andon con total seguridad psicológica: el panel ilumina en rojo la parada, activando la ayuda inmediata de los especialistas para sanear la anomalía in situ."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_LIGHT

    s5.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "Miren la imagen en pantalla. Representa uno de los mayores hitos en la historia de la ingeniería: el Principio Andon de Toyota. "
        "En Toyota, parar la línea no es un fracaso; es el acto supremo de responsabilidad. "
        "Si un operario detecta un tornillo que no entra suave, tira de la cuerda. La fábrica se para. "
        "¿Por qué? Porque parar la fábrica 10 minutos cuesta unos miles de euros. Pero dejar salir coches con frenos defectuosos destruye vidas y arruina la empresa. "
        "En nuestra infraestructura ferroviaria necesitamos exactamente esta misma cultura: que ningún maquinista tema ser reprendido por parar el tren ante una vibración anómala."
    )

    # ==========================================================
    # SLIDE 6: EL PROTOCOLO ANDON FRENTE AL MIEDO AL RETRASO
    # ==========================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "EL PROTOCOLO ANDON: FLUJO DE RESPUESTA Y COMPARATIVA CULTURAL")

    c6_left = add_card(s6, Inches(0.8), Inches(1.35), Inches(5.2), Inches(5.6), ACCENT_MINT)
    tf6 = c6_left.text_frame
    tf6.word_wrap = True
    p = tf6.paragraphs[0]
    p.text = "DE LA TEORÍA A LA OPERACIÓN REAL"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_MINT

    p = tf6.add_paragraph()
    p.text = (
        "\n• Fase 1: Detección temprana\n"
        "  El sensor o el operario identifican la señal débil antes de que se convierta en rotura.\n\n"
        "• Fase 2: Parada preventiva sin debate\n"
        "  Se activa la alerta; el sistema entra en estado seguro de forma inmediata.\n\n"
        "• Fase 3: Soporte al Gemba (Puesto de trabajo)\n"
        "  El equipo multidisciplinar acude a la vía para certificar el estado físico.\n\n"
        "• Fase 4: Solución de causa raíz\n"
        "  No se autoriza el paso hasta validar la corrección definitiva (5 Porqués)."
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    d5_path = os.path.join(diag_dir, "slide5_andon_protocol.png")
    if os.path.exists(d5_path):
        s6.shapes.add_picture(d5_path, Inches(6.25), Inches(1.35), width=Inches(6.28), height=Inches(3.53))
    
    c6_callout = add_card(s6, Inches(6.25), Inches(5.05), Inches(6.28), Inches(1.9), ACCENT_MINT)
    tf6_c = c6_callout.text_frame
    tf6_c.word_wrap = True
    p = tf6_c.paragraphs[0]
    p.text = "COMPARATIVA CULTURAL (INFOGRAFÍA INFERIOR):"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_MINT
    p = tf6_c.add_paragraph()
    p.text = "A la izquierda: la cultura frágil oculta la anomalía por miedo al expediente de retrasos. A la derecha: la cultura Andon premia la parada preventiva, garantizando cero accidentes por fatiga acumulada."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_LIGHT

    s6.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "En este diagrama vemos las 4 etapas del protocolo Andon aplicadas a una línea de alta velocidad. "
        "Y debajo, la diferencia cultural determinante: "
        "En la cultura frágil, el empleado calla por miedo a la bronca o al titular de prensa. "
        "En la cultura Andon, la dirección premia parar. "
        "Parar media hora cuesta dinero; descarrilar cuesta vidas. Es hora de blindar este protocolo en los reglamentos de circulación."
    )

    # ==========================================================
    # SLIDE 7: CIRCUIT BREAKERS Y ERROR BUDGETS
    # ==========================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "PATRONES DE RESILIENCIA: DE LA BANCA DIGITAL AL FERROCARRIL")

    c7_left = add_card(s7, Inches(0.8), Inches(1.35), Inches(5.2), Inches(5.6), ACCENT_CYAN)
    tf7 = c7_left.text_frame
    tf7.word_wrap = True
    p = tf7.paragraphs[0]
    p.text = "PATRONES DE INGENIERÍA SRE APLICADOS A LA VÍA"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p = tf7.add_paragraph()
    p.text = (
        "\n• Circuit Breakers Automatizados:\n"
        "  En software financiero, si la tasa de error sube de 0.5%, el disyuntor abre y desvía tráfico. En trenes: si se pierde telemetría en un cantón, parada automática sin intervención humana negociada.\n\n"
        "• Error Budgets (Presupuesto de Riesgo):\n"
        "  Si el corredor acumula incidencias en catenaria o vía, el presupuesto de error se agota: se reducen frecuencias y velocidades hasta restaurar margen.\n\n"
        "• Blameless Post-Mortem:\n"
        "  Investigar fallos sistémicos e incentivos de gestión en lugar de colgar al técnico de guardia."
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    d6_path = os.path.join(diag_dir, "slide6_circuit_breakers.png")
    if os.path.exists(d6_path):
        s7.shapes.add_picture(d6_path, Inches(6.25), Inches(1.35), width=Inches(6.28), height=Inches(3.53))
    
    c7_callout = add_card(s7, Inches(6.25), Inches(5.05), Inches(6.28), Inches(1.9), ACCENT_CYAN)
    tf7_c = c7_callout.text_frame
    tf7_c.word_wrap = True
    p = tf7_c.paragraphs[0]
    p.text = "AUTOMATIZACIÓN DEL FAIL-SAFE:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p = tf7_c.add_paragraph()
    p.text = "Los tres pilares visualizados: aislamiento en milisegundos (Circuit Breaker), contención de degradación (Blast Radius) y aprendizaje sistémico sin culpabilización personal (Blameless)."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_LIGHT

    s7.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "En la ingeniería de fiabilidad de Google o de los grandes centros financieros no confiamos en que los operarios sean infalibles. "
        "Construimos 'Circuit Breakers'. Como ven en el diagrama, cuando el sistema detecta anomalías consecutivas, el disyuntor salta solo. "
        "Nadie tiene que pedir permiso para proteger el sistema. "
        "Si en banca bloqueamos transferencias por precaución ante una caída de red, ¿cómo es admisible que en una vía férrea un cantón con un tren averiado no bloquee de forma estanca y automática a todo el tráfico que le sigue?"
    )

    # ==========================================================
    # SLIDE 8: REEQUILIBRANDO EL CUADRO DE MANDO (KPIS)
    # ==========================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "REEQUILIBRANDO EL CUADRO DE MANDO: NUEVOS KPIS")

    c8_left = add_card(s8, Inches(0.8), Inches(1.35), Inches(5.2), Inches(5.6), ACCENT_MINT)
    tf8 = c8_left.text_frame
    tf8.word_wrap = True
    p = tf8.paragraphs[0]
    p.text = "DE LA EFICIENCIA COMERCIAL A LA RESILIENCIA ESTRUCTURAL"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_MINT

    p = tf8.add_paragraph()
    p.text = (
        "\n1. Invariante de Mantenimiento:\n"
        "   El 100% de ventanas nocturnas de conservación deben ejecutarse sin recortes por trenes retrasados.\n\n"
        "2. Margen dinámico garantizado:\n"
        "   Tiempo de separación físico blindado entre convoyes, inmune a presiones de saturación comercial.\n\n"
        "3. Tiempo de resolución de señales débiles:\n"
        "   Inspección presencial obligatoria en menos de 2 horas ante cualquier alerta de vibración en vía.\n\n"
        "4. Causa raíz antes de reapertura:\n"
        "   MTTR subordinado a la certificación de seguridad, no al minutero de indemnizaciones."
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    d7_path = os.path.join(diag_dir, "slide7_balance_kpis.png")
    if os.path.exists(d7_path):
        s8.shapes.add_picture(d7_path, Inches(6.25), Inches(1.35), width=Inches(6.28), height=Inches(3.53))
    
    c8_callout = add_card(s8, Inches(6.25), Inches(5.05), Inches(6.28), Inches(1.9), ACCENT_MINT)
    tf8_c = c8_callout.text_frame
    tf8_c.word_wrap = True
    p = tf8_c.paragraphs[0]
    p.text = "COMPARATIVA DIRECTA EN EL COMITÉ DE DIRECCIÓN:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_MINT
    p = tf8_c.add_paragraph()
    p.text = "A la izquierda, métricas de ilusión que maximizan ingresos a corto plazo pero fragilizan la infraestructura; a la derecha, métricas de resiliencia que garantizan supervivencia y confianza pública duradera."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_LIGHT

    s8.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "Aquí está la propuesta práctica para cualquier consejo de administración. Miren las dos columnas del diagrama. "
        "A la izquierda, las métricas de la ilusión: puntualidad forzada, saturación de surcos, recortes en conservación. "
        "A la derecha, las métricas de la resiliencia: respetar las ventanas nocturnas de mantenimiento a rajatabla, premiar al que levanta la mano ante una sospecha, y no abrir jamás una vía sin causa raíz certificada. "
        "La puntualidad no es un objetivo primario; la puntualidad es la consecuencia natural de una infraestructura sana."
    )

    # ==========================================================
    # SLIDE 9: CONCLUSIÓN Y CIERRE
    # ==========================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)

    card_close = add_card(s9, Inches(1.2), Inches(1.3), Inches(10.933), Inches(4.9), ACCENT_CYAN)
    tf_cl = card_close.text_frame
    tf_cl.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_cl.word_wrap = True

    p = tf_cl.paragraphs[0]
    p.text = '"El éxito de una infraestructura crítica no se mide por lo rápido que avanza cuando todo es favorable,\n\nsino por su humildad y valentía para detenerse en seco cuando la seguridad está en duda."'
    p.font.size = Pt(23)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    p.alignment = PP_ALIGN.CENTER

    p2 = tf_cl.add_paragraph()
    p2.text = (
        "\nAlexander Armentia (Alexar69)\n"
        "Reliability & Resilience Manager | SRE & Critical Operations\n"
        "alexanderarmentia.com · linkedin.com/in/alexanderarmentia"
    )
    p2.font.size = Pt(15)
    p2.font.color.rgb = ACCENT_AMBER
    p2.alignment = PP_ALIGN.CENTER

    s9.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "(Pausa final. Mirada fija a la audiencia).\n"
        "Los sistemas complejos fallarán. La IA fallará. El metal se fatigará inevitablemente. "
        "Pero lo que define nuestra estatura como ingenieros y directivos es decidir qué sistema queremos construir: "
        "uno que prioriza el minutero comercial y reza para que la desgracia no toque en nuestro turno, "
        "o uno que tiene la valentía de parar para que todo el mundo regrese sano y salvo a casa. "
        "Llegar media hora tarde es una molestia pasajera. No volver jamás es una tragedia irreparable. "
        "Muchas gracias."
    )

    output_path = os.path.join(repo_dir, "presentacion-reliability-resiliencia-adamuz-urda.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")
    return output_path

if __name__ == "__main__":
    create_deck()
