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
    CARD_BG = RGBColor(15, 15, 32)      # #0f0f20
    BORDER_COLOR = RGBColor(34, 211, 238) # #22d3ee
    TEXT_LIGHT = RGBColor(241, 241, 243) # #f1f1f3
    TEXT_MUTED = RGBColor(156, 163, 175) # #9ca3af
    ACCENT_AMBER = RGBColor(249, 115, 22) # #f97316
    ACCENT_CYAN = RGBColor(34, 211, 238) # #22d3ee
    ACCENT_RED = RGBColor(239, 68, 68)   # #ef4444
    ACCENT_MINT = RGBColor(52, 211, 153) # #34d399

    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hero_img = os.path.join(repo_dir, "blog", "assets", "adamuz-urda-kpis-seguridad-ave.png")

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

    # ==========================================================
    # SLIDE 1: PORTADA
    # ==========================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)
    if os.path.exists(hero_img):
        img = s1.shapes.add_picture(hero_img, Inches(0), Inches(0), width=Inches(13.333), height=Inches(7.5))
        # Add dark gradient / overlay
        overlay = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        overlay.fill.solid()
        overlay.fill.fore_color.rgb = RGBColor(6, 6, 15)
        # Note: PPTX transparency is handled via XML if needed, or overlay card
        # Let's place a sleek card in center-left
        
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
    # SLIDE 2: LA LEY DE GOODHART & LA ILUSIÓN DE LA PUNTUALIDAD
    # ==========================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)

    s2_card1 = add_card(s2, Inches(1), Inches(1), Inches(11.333), Inches(2.2), ACCENT_AMBER)
    tf2_1 = s2_card1.text_frame
    tf2_1.word_wrap = True
    p = tf2_1.paragraphs[0]
    p.text = "LA LEY DE GOODHART EN INFRAESTRUCTURA"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER

    p = tf2_1.add_paragraph()
    p.text = '"Cuando una métrica se convierte en el objetivo,\ndeja de ser una buena métrica."'
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT

    # Two columns below
    c1 = add_card(s2, Inches(1), Inches(3.6), Inches(5.4), Inches(3.2))
    tfc1 = c1.text_frame
    tfc1.word_wrap = True
    p = tfc1.paragraphs[0]
    p.text = "EL INCENTIVO PERVERSO"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED

    p = tfc1.add_paragraph()
    p.text = "• Métrica reina: % Puntualidad comercial en destino\n• Penalización económica inmediata por retraso\n• Consecuencia: Se tiende a apurar los márgenes de tolerancia física para no romper el minuto comercial."
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_MUTED

    c2 = add_card(s2, Inches(6.9), Inches(3.6), Inches(5.4), Inches(3.2))
    tfc2 = c2.text_frame
    tfc2.word_wrap = True
    p = tfc2.paragraphs[0]
    p.text = "NORMALIZACIÓN DE LA DESVIACIÓN"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p = tfc2.add_paragraph()
    p.text = "• Concepto acuñado tras la tragedia del Challenger (D. Vaughan).\n• Se detecta una vibración atípica o parámetro límite.\n• Como 'ayer no pasó nada', la anomalía se reclasifica tácitamente como tolerable.\n• Hasta que el metal o el software rompen."
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_MUTED

    s2.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "Durante tres décadas España presumió con orgullo del compromiso de puntualidad del AVE. "
        "Pero la Ley de Goodhart nos enseña que cuando dices a una organización que el único número que importa es llegar en hora, "
        "alteras todos los incentivos humanos. Parar a inspeccionar una vía se convierte en un 'estorbo comercial'. "
        "Nadie toma una decisión temeraria adrede; simplemente se normaliza la desviación milímetro a milímetro hasta la catástrofe."
    )

    # ==========================================================
    # SLIDE 3: ADAMUZ VS URDA (ANATOMÍA DE DOS FALLOS)
    # ==========================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)

    hdr = s3.shapes.add_textbox(Inches(1), Inches(0.6), Inches(11.333), Inches(0.8))
    p = hdr.text_frame.paragraphs[0]
    p.text = "ADAMUZ Y URDA: LAS DOS CARAS DEL COLAPSO"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT

    # Card Adamuz
    card_adamuz = add_card(s3, Inches(1), Inches(1.6), Inches(5.4), Inches(5.2), ACCENT_RED)
    tf_a = card_adamuz.text_frame
    tf_a.word_wrap = True
    p = tf_a.paragraphs[0]
    p.text = "ADAMUZ (Enero 2026)\nFallo de Componente + Cero Contención"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED

    p = tf_a.add_paragraph()
    p.text = (
        "\n1. Quiebra de Fiabilidad (Reliability):\n"
        "   Rotura de carril / soldadura y base de balasto fatigada.\n\n"
        "2. Ceguera ante 'Señales Débiles':\n"
        "   Decenas de convoyes pasaron previamente por el tramo degradado sin que se disparara la parada preventiva.\n\n"
        "3. Quiebra de Contención (Blast Radius):\n"
        "   El descarrilamiento en vía par invadió la vía impar, sin detección instantánea de gálibo que frenara al Alvia frontal."
    )
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # Card Urda
    card_urda = add_card(s3, Inches(6.9), Inches(1.6), Inches(5.4), Inches(5.2), ACCENT_AMBER)
    tf_u = card_urda.text_frame
    tf_u.word_wrap = True
    p = tf_u.paragraphs[0]
    p.text = "URDA (Octubre 2026)\nColapso en Cascada + Quiebra del Fail-Safe"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER

    p = tf_u.add_paragraph()
    p.text = (
        "\n1. Escenario Nominal Previsto:\n"
        "   Un tren se detiene por avería mecánica (sucede con frecuencia).\n\n"
        "2. Quiebra de la Resiliencia:\n"
        "   El sistema no se degradó con elegancia (Graceful Degradation). No protegió el cantón ocupado.\n\n"
        "3. Quiebra del Principio Fail-Safe:\n"
        "   Ante la duda o pérdida de telemetría, el estado por defecto debe ser la parada de emergencia del cantón posterior. La colisión por alcance demostró el fallo de la redundancia."
    )
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    s3.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "Miremos los dos accidentes con ojos de arquitectos de sistemas. "
        "En Adamuz falló el material (la soldadura), pero lo devastador fue que no existió contención de impacto: el tren invadió la vía contraria sin freno de emergencia para el tren que venía de frente. "
        "En Urda es aún más claro: que un tren se pare es normal. Lo que jamás puede pasar en un sistema con resiliencia es que dos trenes compartan cantón y choquen por alcance. "
        "El estado por defecto ante el error siempre tiene que ser la parada absoluta."
    )

    # ==========================================================
    # SLIDE 4: RELIABILITY VS RESILIENCIA (LA MATRIZ CONCEPTUAL)
    # ==========================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)

    hdr = s4.shapes.add_textbox(Inches(1), Inches(0.6), Inches(11.333), Inches(0.8))
    p = hdr.text_frame.paragraphs[0]
    p.text = "RELIABILITY VS. RESILIENCIA: NO SON LO MISMO"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT

    # Reliability box
    box_rel = add_card(s4, Inches(1), Inches(1.6), Inches(5.4), Inches(5.2), ACCENT_CYAN)
    tf_r = box_rel.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "RELIABILITY (Fiabilidad)\nObjetivo: Que las cosas no fallen"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p = tf_r.add_paragraph()
    p.text = (
        "\n• Métricas: MTBF (Mean Time Between Failures), SLA, Uptime 99.9%.\n"
        "• Enfoque: Mantenimiento preventivo, tolerancias de carga, calidad de componentes.\n"
        "• Límite intrínseco: En sistemas complejos en el mundo real, los materiales envejecen, el software tiene bugs y los humanos erran.\n\n"
        "La Reliability siempre se romperá en algún momento."
    )
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_MUTED

    # Resilience box
    box_res = add_card(s4, Inches(6.9), Inches(1.6), Inches(5.4), Inches(5.2), ACCENT_MINT)
    tf_rs = box_res.text_frame
    tf_rs.word_wrap = True
    p = tf_rs.paragraphs[0]
    p.text = "RESILIENCE (Resiliencia)\nObjetivo: Qué hacemos cuando el fallo ocurre"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_MINT

    p = tf_rs.add_paragraph()
    p.text = (
        "\n• Métricas: MTTR (Mean Time to Recovery), Capacidad de absorción de shock.\n"
        "• Enfoque: Blast Radius Containment (aislamiento del daño), Graceful Degradation (degradación controlada).\n"
        "• Pregunta clave: Cuando el carril parte o el tren se detiene, ¿el sistema colapsa o entra en parada segura?\n\n"
        "La Resiliencia es la garantía de supervivencia ante lo imprevisto."
    )
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_MUTED

    s4.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "En los comités de dirección estas dos palabras se confunden a diario. "
        "Reliability es diseñar para que no se caiga. Es magnífico, pero es finito. "
        "Resiliencia es lo que pasa el segundo después de que la fiabilidad se rompe. "
        "La resiliencia no te promete que no habrá averías; te garantiza que la avería no costará vidas ni destruirá la organización."
    )

    # ==========================================================
    # SLIDE 5: EL PRINCIPIO ANDON (EL CORAJE DE PARAR)
    # ==========================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)

    card_andon = add_card(s5, Inches(1), Inches(1), Inches(11.333), Inches(5.5), ACCENT_AMBER)
    tf_and = card_andon.text_frame
    tf_and.word_wrap = True
    p = tf_and.paragraphs[0]
    p.text = "EL PRINCIPIO ANDON: 'STOP THE LINE'"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER

    p = tf_and.add_paragraph()
    p.text = (
        "\nNacido en las líneas de fabricación de alta fiabilidad de Toyota:\n"
        "Cualquier operario, maquinista o técnico tiene la autoridad y el deber de presionar el botón rojo y detener toda la línea ante una duda técnica o de seguridad.\n\n"
        "Sin represalias. Sin broncas. Sin explicaciones comerciales previas.\n\n"
        "LA PREGUNTA INCÓMODA PARA NUESTRAS EMPRESAS:\n"
        "¿Tienen hoy nuestros técnicos de vía o maquinistas el respaldo cultural para parar un tren ante una vibración anómala, sabiendo que arruinarán la estadística de puntualidad del corredor?\n\n"
        "Si la respuesta no es un 'SÍ' rotundo, el sistema tiene una brecha de seguridad latente."
    )
    p.font.size = Pt(16)
    p.font.color.rgb = TEXT_LIGHT

    s5.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "Taiichi Ohno introdujo la cuerda Andon en Toyota. Parar la fábrica 10 minutos cuesta dinero; sacar coches con frenos defectuosos quiebra la empresa. "
        "¿Respaldan nuestras organizaciones al técnico que levanta la mano? "
        "Si un empleado tiene miedo al titular de prensa sobre 'caos ferroviario', la cultura corporativa está rota."
    )

    # ==========================================================
    # SLIDE 6: LECCIONES DE BANCA CRÍTICA Y SRE
    # ==========================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)

    hdr = s6.shapes.add_textbox(Inches(1), Inches(0.6), Inches(11.333), Inches(0.8))
    p = hdr.text_frame.paragraphs[0]
    p.text = "PATRONES DE RESILIENCIA: DE LA BANCA AL FERROCARRIL"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT

    # 3 horizontal cards
    c_w = Inches(3.6)
    c_h = Inches(5.2)

    card_cb = add_card(s6, Inches(1), Inches(1.6), c_w, c_h, ACCENT_CYAN)
    tf_cb = card_cb.text_frame
    tf_cb.word_wrap = True
    p = tf_cb.paragraphs[0]
    p.text = "CIRCUIT BREAKERS\n(Interruptores de Corte)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p = tf_cb.add_paragraph()
    p.text = "\nEn banca: ante picos de fallos, cortamos transacciones en milisegundos para aislar el núcleo transaccional.\n\nEn transporte: el sistema debe cortar el flujo del corredor automáticamente en cuanto se pierde telemetría en un cantón."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    card_eb = add_card(s6, Inches(4.866), Inches(1.6), c_w, c_h, ACCENT_AMBER)
    tf_eb = card_eb.text_frame
    tf_eb.word_wrap = True
    p = tf_eb.paragraphs[0]
    p.text = "ERROR BUDGETS\n(Presupuesto de Riesgo)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p = tf_eb.add_paragraph()
    p.text = "\nEn SRE: si consumimos el presupuesto de error con caídas, se congelan despliegues nuevos y todo el foco va a estabilidad.\n\nEn transporte: si una vía acumula anomalías, se reducen velocidades y frecuencias hasta sanear la infraestructura."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    card_bp = add_card(s6, Inches(8.733), Inches(1.6), c_w, c_h, ACCENT_MINT)
    tf_bp = card_bp.text_frame
    tf_bp.word_wrap = True
    p = tf_bp.paragraphs[0]
    p.text = "BLAMELESS POST-MORTEM\n(Cultura Sin Culpa)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_MINT
    p = tf_bp.add_paragraph()
    p.text = "\nBuscar culpables individuales en el eslabón más débil no soluciona nada.\n\nDebemos auditar los incentivos de gobernanza: ¿por qué el sistema empujó a operar en condiciones degradadas?"
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    s6.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "En banca crítica si una pasarela falla hacemos rollback sin pestañear. "
        "Si somos capaces de aplicar Circuit Breakers y congelar despliegues por dinero, ¿cómo no lo vamos a hacer cuando lo que viaja son personas? "
        "La tecnología no sustituye la disciplina operativa."
    )

    # ==========================================================
    # SLIDE 7: LA NUEVA TABLA DE KPIS
    # ==========================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)

    hdr = s7.shapes.add_textbox(Inches(1), Inches(0.6), Inches(11.333), Inches(0.8))
    p = hdr.text_frame.paragraphs[0]
    p.text = "REEQUILIBRANDO EL CUADRO DE MANDO CORPORATIVO"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT

    card_tbl = add_card(s7, Inches(1), Inches(1.6), Inches(11.333), Inches(5.2))
    tf_tbl = card_tbl.text_frame
    tf_tbl.word_wrap = True
    
    p = tf_tbl.paragraphs[0]
    p.text = "KPIs DE ILUSIÓN (Eficiencia) vs. KPIs DE RESILIENCIA (Supervivencia)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p = tf_tbl.add_paragraph()
    p.text = (
        "\n❌  Puntualidad comercial a cualquier precio\n"
        "   👉  ✅ % Cumplimiento estricto de ventanas nocturnas de mantenimiento\n\n"
        "❌  Saturación máxima de surcos por hora en el corredor\n"
        "   👉  ✅ Margen de seguridad dinámico garantizado entre cantones\n\n"
        "❌  Coste mínimo de conservación por kilómetro de vía\n"
        "   👉  ✅ Velocidad de resolución física de anomalías reportadas por sensores\n\n"
        "❌  MTTR orientado a reabrir la vía en minutos para evitar indemnizaciones\n"
        "   👉  ✅ Verificación exhaustiva de causa raíz antes de autorizar la reanudación del tráfico"
    )
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT_LIGHT

    s7.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "No digo que la puntualidad no importe. Claro que importa. "
        "Pero la puntualidad tiene que ser la consecuencia de una infraestructura sana, no una máscara para tapar un sistema fatigado. "
        "Cambiemos los KPIs en los comités de dirección."
    )

    # ==========================================================
    # SLIDE 8: CONCLUSIÓN Y CIERRE
    # ==========================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)

    card_close = add_card(s8, Inches(1.5), Inches(1.5), Inches(10.333), Inches(4.5), ACCENT_CYAN)
    tf_cl = card_close.text_frame
    tf_cl.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_cl.word_wrap = True

    p = tf_cl.paragraphs[0]
    p.text = '"El éxito de una infraestructura crítica no se mide por lo rápido que avanza cuando todo es favorable,\n\nsino por su humildad y valentía para detenerse en seco cuando la seguridad está en duda."'
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    p.alignment = PP_ALIGN.CENTER

    p2 = tf_cl.add_paragraph()
    p2.text = "\nAlexander Armentia · Reliability & Resilience Manager\nalexanderarmentia.com"
    p2.font.size = Pt(16)
    p2.font.color.rgb = ACCENT_AMBER
    p2.alignment = PP_ALIGN.CENTER

    s8.notes_slide.notes_text_frame.text = (
        "GUION:\n"
        "(Pausa final. Mirada a la audiencia).\n"
        "Los sistemas complejos fallarán. La IA fallará. El metal se fatigará. "
        "Pero lo que está en nuestras manos es decidir qué tipo de profesionales queremos ser: "
        "gestores del minutero que cruzan los dedos esperando que la catástrofe no ocurra en su turno, "
        "o arquitectos de resiliencia que ponen la vida humana por encima de cualquier estadística. "
        "Llegar 10 minutos tarde es una anécdota. No volver jamás es una herida que no cicatriza. "
        "Muchas gracias."
    )

    # Save presentation
    output_path = os.path.join(repo_dir, "presentacion-reliability-resiliencia-adamuz-urda.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")
    return output_path

if __name__ == "__main__":
    create_deck()
