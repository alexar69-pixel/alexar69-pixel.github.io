import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_bbva_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # blank layout

    # BBVA & Dark Executive Palette
    BG_DARK = RGBColor(6, 11, 20)           # #060b14 Dark Navy/Slate
    CARD_BG = RGBColor(12, 21, 39)          # #0c1527 Card Navy
    BBVA_BLUE = RGBColor(0, 68, 129)        # #004481 BBVA Core Blue
    BBVA_NAVY = RGBColor(20, 100, 165)      # #1464a5 BBVA Accent Blue
    CYAN = RGBColor(34, 211, 238)           # #22d3ee High-tech Cyan
    AMBER = RGBColor(249, 115, 22)          # #f97316 Alert Amber
    RED = RGBColor(239, 68, 68)             # #ef4444 Failure Red
    MINT = RGBColor(52, 211, 153)           # #34d399 Resilience Mint
    TEXT_LIGHT = RGBColor(248, 250, 252)    # #f8fafc Text Light
    TEXT_MUTED = RGBColor(148, 163, 184)    # #94a3b8 Text Muted

    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    diag_dir = os.path.join(repo_dir, "blog", "assets", "presentation")

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

    def add_header(slide, title, category="// BBVA TECH LEADERSHIP · RELIABILITY & RESILIENCE"):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        p_cat = tf.paragraphs[0]
        p_cat.text = category
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = CYAN
        
        p_tit = tf.add_paragraph()
        p_tit.text = title
        p_tit.font.size = Pt(22)
        p_tit.font.bold = True
        p_tit.font.color.rgb = TEXT_LIGHT

    # ==========================================================
    # SLIDE 1: PORTADA EJECUTIVA
    # ==========================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1)

    s1_card = add_card(s1, Inches(1), Inches(1.2), Inches(11.333), Inches(5.1), CYAN)
    tf1 = s1_card.text_frame
    tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "// BBVA · DIRECCIÓN DE INFRAESTRUCTURA, ARQUITECTURA Y OPERACIONES"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = CYAN

    p1 = tf1.add_paragraph()
    p1.text = "LA GRAN ILUSIÓN DEL MTBF FRENTE AL MTTR"
    p1.font.size = Pt(38)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT

    p2 = tf1.add_paragraph()
    p2.text = "Por qué diseñar para el 'cero fallos' es una trampa y cómo la reducción del MTTR protege la banca crítica"
    p2.font.size = Pt(19)
    p2.font.color.rgb = AMBER

    p3 = tf1.add_paragraph()
    p3.text = "\nAlexander Armentia (Alexar69)\nReliability & Resilience Manager | +25 años en operaciones críticas y banca"
    p3.font.size = Pt(14)
    p3.font.color.rgb = TEXT_MUTED

    s1.notes_slide.notes_text_frame.text = (
        "GUION DE PONENTE:\n"
        "(Pausa inicial de 3 segundos mirando al equipo directivo).\n"
        "Buenos días a todos. Durante los últimos treinta años, la industria tecnológica y bancaria ha vivido bajo una ilusión muy reconfortante: "
        "la promesa de que si compramos suficiente hierro redundante, si firmamos suficientes contratos de soporte prémium y si planificamos con comités de cambios exhaustivos, "
        "podemos conseguir que nuestros sistemas nunca fallen. Es el culto al MTBF: el tiempo medio entre fallos.\n"
        "Vengo hoy aquí a deciros, con el máximo respeto por nuestra arquitectura pero con la crudeza que exige mi rol de fiabilidad, "
        "que en un banco hiperconectado como BBVA esa premisa está muerta. Perseguir el 'cero fallos' es hoy el mayor multiplicador de riesgo que tenemos. "
        "La verdadera excelencia operativa no está en prometer que nunca caeremos, sino en garantizar que nos levantamos en menos de ocho minutos antes de que el negocio o el cliente noten el tropiezo."
    )

    # ==========================================================
    # SLIDE 2: EL ESPEJISMO DEL 'CERO FALLOS'
    # ==========================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "EL ESPEJISMO DEL 'CERO FALLOS' EN SISTEMAS HIPERCONECTADOS")

    c2_l = add_card(s2, Inches(0.8), Inches(1.35), Inches(5.6), Inches(5.6), AMBER)
    tf2_l = c2_l.text_frame
    tf2_l.word_wrap = True
    p = tf2_l.paragraphs[0]
    p.text = "DE LA BANCA DE LOS 90 AL ECOSISTEMA 2026"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = AMBER

    p = tf2_l.add_paragraph()
    p.text = (
        "\n1. La era del Mainframe monolítico (1995):\n"
        "   Un sistema cerrado, transacciones por lotes (*batch*) nocturnos, dependencias locales. El MTBF funcionaba como métrica porque el entorno era finito y predecible.\n\n"
        "2. El ecosistema hiperconectado actual (2026):\n"
        "   Miles de microservicios en clústeres híbridos, nubes públicas, tokenización con Visa/Mastercard, transferencias SEPA Instant y Bizum, APIs de terceros y millones de apps móviles concurrentes.\n\n"
        "3. La certeza matemática del fallo:\n"
        "   En un ecosistema con miles de componentes distribuidos, la probabilidad de que al menos una pieza falle en cualquier segundo es del 100%."
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    c2_r = add_card(s2, Inches(6.7), Inches(1.35), Inches(5.8), Inches(5.6), RED)
    tf2_r = c2_r.text_frame
    tf2_r.word_wrap = True
    p = tf2_r.paragraphs[0]
    p.text = "EL PELIGRO DEL PARADIGMA LEGACY"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RED

    p = tf2_r.add_paragraph()
    p.text = (
        "\n• Fragilidad oculta:\n"
        "  Cuando una organización cree que su sistema no puede fallar, no entrena el músculo de recuperación. Cuando el fallo inevitable llega, el equipo se congela en la perplejidad.\n\n"
        "• La trampa de la sobre-ingeniería en CAPEX:\n"
        "  Invertir millones en réplicas idénticas pasivas no protege contra bugs lógicos, archivos de configuración corruptos o fallos en cascada.\n\n"
        "• Conclusión directiva:\n"
        "  El fallo no es una anomalía evitable; el fallo es una propiedad intrínseca de los sistemas complejos. Debemos gobernar asumiendo la quiebra."
    )
    p.font.size = Pt(12.5)
    p.font.color.rgb = TEXT_LIGHT

    s2.notes_slide.notes_text_frame.text = (
        "GUION DE PONENTE:\n"
        "Miremos cómo ha cambiado nuestro trabajo. Hace 25 años podíamos diseñar para MTBF porque controlábamos todo el stack: teníamos el host central en el búnker y sabíamos exactamente cuántos terminales se conectaban. "
        "Hoy, una simple transferencia Bizum de un usuario atraviesa 14 saltos de red, microservicios en Kubernetes, llamadas a pasarelas interbancarias y validaciones biométricas. "
        "Matemáticamente, la probabilidad de que todos esos componentes funcionen al 100% todo el tiempo es cero. "
        "Si nuestra estrategia sigue siendo 'vamos a invertir para que nada rompa', estamos engañando al Consejo de Administración. "
        "Las piezas van a romper. La pregunta es: ¿cuánto tardamos en aislar el trozo roto para que el 99.9% del banco siga cobrando y pagando?"
    )

    # ==========================================================
    # SLIDE 3: LA PARADOJA DE LOS DOS BANCOS
    # ==========================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "LA PARADOJA DE LOS DOS BANCOS: MTBF VS. MTTR EN LA PRÁCTICA")

    c3_l = add_card(s3, Inches(0.8), Inches(1.35), Inches(5.2), Inches(5.6), CYAN)
    tf3_l = c3_l.text_frame
    tf3_l.word_wrap = True
    p = tf3_l.paragraphs[0]
    p.text = "EL DILEMA ESTRATÉGICO"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN

    p = tf3_l.add_paragraph()
    p.text = (
        "\nImaginemos dos entidades financieras competidoras:\n\n"
        "• BANCO A (Obsesión MTBF):\n"
        "  Presume de aguantar 364 días sin incidencias. Pero el día que cae, la llamada técnica se alarga 4 horas y media debatiendo hipótesis.\n"
        "  Resultado: 270 minutos de apagón nacional en Black Friday.\n\n"
        "• BANCO B (Maestría en MTTR):\n"
        "  Sufre 6 micro-incidencias al año. Pero cada una se detecta en 90s y se revierte en 3 minutos gracias a Circuit Breakers y rollback automático.\n"
        "  Resultado: 18 minutos acumulados en todo el año. Cero impacto en clientes."
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    d3_img = os.path.join(diag_dir, "bbva_mtbf_vs_mttr_paradoja.png")
    if os.path.exists(d3_img):
        s3.shapes.add_picture(d3_img, Inches(6.25), Inches(1.35), width=Inches(6.28), height=Inches(3.53))

    c3_callout = add_card(s3, Inches(6.25), Inches(5.05), Inches(6.28), Inches(1.9), MINT)
    tf3_c = c3_callout.text_frame
    tf3_c.word_wrap = True
    p = tf3_c.paragraphs[0]
    p.text = "EL VEREDICTO REGULATORIO (DORA / BCE):"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = MINT
    p = tf3_c.add_paragraph()
    p.text = "El Banco A se enfrenta a sanciones millonarias de supervisión europea por superar los umbrales de interrupción de servicios esenciales. El Banco B pasa las auditorías con nota máxima porque su disponibilidad real supera el 99.96%."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_LIGHT

    s3.notes_slide.notes_text_frame.text = (
        "GUION DE PONENTE:\n"
        "Miren la comparativa en pantalla. Es una pregunta que hago a menudo a los comités de riesgos: ¿Qué banco preferiríais gestionar? "
        "El Banco A tiene un dashboard publicitario precioso que dice 'cero caídas en doce meses'... hasta el fatídico viernes en que se le cae el autorizador a las dos de la tarde y tarda cuatro horas en levantarlo. "
        "En esas cuatro horas pierde 50 millones de transacciones, sale abriendo el telediario de las nueve y recibe una carta demoledora del Banco Central Europeo. "
        "El Banco B, en cambio, tiene la humildad de asumir que tropezará. Ha diseñado su sistema para que, cuando tropieza, el disyuntor salta en 30 segundos, el rollback se aplica en dos minutos y el cliente en la gasolinera sólo nota que su tarjeta tardó cuatro segundos en lugar de dos. "
        "El Banco B tiene 18 minutos de parada total al año frente a los 270 minutos del Banco A. Esa es la diferencia entre el humo del MTBF y la realidad del MTTR."
    )

    # ==========================================================
    # SLIDE 4: DISPONIBILIDAD REAL VS MARKETING
    # ==========================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "DISPONIBILIDAD REAL VS. DISPONIBILIDAD DE MARKETING")

    c4_l = add_card(s4, Inches(0.8), Inches(1.35), Inches(5.2), Inches(5.6), AMBER)
    tf4_l = c4_l.text_frame
    tf4_l.word_wrap = True
    p = tf4_l.paragraphs[0]
    p.text = "LA MENTIRA DEL 'HTTP 200'"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = AMBER

    p = tf4_l.add_paragraph()
    p.text = (
        "\n• La medición ciega tradicional:\n"
        "  Sondas externas lanzando pings al balanceador de carga (*Load Balancer*). Si el proxy responde OK, el informe corporativo reporta 99.99%.\n\n"
        "• El fallo invisible:\n"
        "  El proxy responde, pero las llamadas a la base de datos están bloqueadas por un deadlock o la pasarela de Bizum está devolviendo respuestas vacías.\n\n"
        "• La realidad del 99.99% (Cuatro Nueves):\n"
        "  Solo permite 4 minutos y 19 segundos de indisponibilidad al mes en toda la plataforma.\n\n"
        "• La métrica que importa:\n"
        "  Tasa de éxito transaccional (*Good Business Transactions / Total Invocations*)."
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    d4_img = os.path.join(diag_dir, "bbva_disponibilidad_real_vs_marketing.png")
    if os.path.exists(d4_img):
        s4.shapes.add_picture(d4_img, Inches(6.25), Inches(1.35), width=Inches(6.28), height=Inches(3.53))

    c4_callout = add_card(s4, Inches(6.25), Inches(5.05), Inches(6.28), Inches(1.9), CYAN)
    tf4_c = c4_callout.text_frame
    tf4_c.word_wrap = True
    p = tf4_c.paragraphs[0]
    p.text = "EL SALTO CULTURAL EN BBVA:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN
    p = tf4_c.add_paragraph()
    p.text = "Debemos desterrar las métricas sintéticas de complacencia. El único indicador de disponibilidad válido es aquel que mide si un cliente ha podido completar su pago o consultar su saldo de forma real."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_LIGHT

    s4.notes_slide.notes_text_frame.text = (
        "GUION DE PONENTE:\n"
        "Tenemos que ser implacables con nosotros mismos en esto: el informe que dice que tuvimos un 99.99% el mes pasado es a menudo una mentira reconfortante. "
        "Si medimos pings a la URL de bienvenida, todo está verde. Pero si un cliente intenta entrar a la app y la base de datos de saldos responde con error 500 silencioso, para ese cliente el banco está al 0%. "
        "En fiabilidad moderna, los SLOs tienen que estar pegados al negocio. Medimos transacciones bancarias válidas completadas. "
        "Y cuando asumimos esa métrica real, descubrimos que los cuatro nueves son una disciplina espartana: cuatro minutos de holgura al mes. "
        "Si tardamos veinte minutos en ponernos de acuerdo en quién abre la incidencia, ya hemos reventado el objetivo de medio año."
    )

    # ==========================================================
    # SLIDE 5: ANATOMÍA DEL MTTR BANCARIO (< 8 MINUTOS)
    # ==========================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "ANATOMÍA DEL MTTR BANCARIO: EL PIPELINE A < 8 MINUTOS")

    c5_l = add_card(s5, Inches(0.8), Inches(1.35), Inches(5.2), Inches(5.6), MINT)
    tf5_l = c5_l.text_frame
    tf5_l.word_wrap = True
    p = tf5_l.paragraphs[0]
    p.text = "DECONSTRUCCIÓN DEL INCIDENTE P1"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = MINT

    p = tf5_l.add_paragraph()
    p.text = (
        "\n1. MTTD (Detección < 90s):\n"
        "   Telemetría de alta resolución. Si el volumen de pagos exitosos cae un 2% interanual instantáneo, salta la alerta sin intervención humana.\n\n"
        "2. MTTI (Triage & Aislamiento < 2 min):\n"
        "   Incident Commander en Canal Alfa. Circuit Breakers aíslan el microservicio defectuoso para proteger el Core.\n\n"
        "3. MTTR (Mitigación < 3 min):\n"
        "   Rollback automatizado o failover celular. Prohibido intentar parches en caliente en producción.\n\n"
        "4. MTTA (Causa Raíz Post-Mortem):\n"
        "   Análisis forense en frío, sin culpa y con acciones preventivas vinculadas a Jira."
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    d5_img = os.path.join(diag_dir, "bbva_pipeline_mttr_8_minutos.png")
    if os.path.exists(d5_img):
        s5.shapes.add_picture(d5_img, Inches(6.25), Inches(1.35), width=Inches(6.28), height=Inches(3.53))

    c5_callout = add_card(s5, Inches(6.25), Inches(5.05), Inches(6.28), Inches(1.9), AMBER)
    tf5_c = c5_callout.text_frame
    tf5_c.word_wrap = True
    p = tf5_c.paragraphs[0]
    p.text = "REGLA DE ORO DE GESTIÓN DE INCIDENTES:"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = AMBER
    p = tf5_c.add_paragraph()
    p.text = "'Mitigar no es arreglar'. En una War Room P1 nadie investiga por qué falló el código. El único cometido es restaurar el servicio comercial. La autopsia se realiza al día siguiente con café y datos fríos."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_LIGHT

    s5.notes_slide.notes_text_frame.text = (
        "GUION DE PONENTE:\n"
        "Miren este pipeline de la derecha. Es el estándar de oro que debemos exigirnos en BBVA. "
        "Cuando un servicio P1 se degrada, cada segundo debe estar coreografiado. "
        "Primeros 90 segundos: la monitorización sintética detecta la desviación. "
        "Siguientes dos minutos: el Incident Commander toma el mando y acciona el disyuntor que impide que el microservicio enfermo tire abajo la base de datos de cuentas. "
        "Tres minutos siguientes: se ejecuta el rollback al release anterior. Son las 02:24 de la mañana; el servicio ha vuelto. Tiempo total: 6 minutos y medio. "
        "¿Por qué tantas empresas tardan tres horas? Porque en cuanto se abre la llamada, los ingenieros se ponen a depurar el código, a mirar stacktraces y a intentar compilar parches deprisa y corriendo. "
        "En mi guardia eso está terminantemente prohibido: en una crisis de madrugada no somos programadores, somos médicos de urgencias. Paramos la hemorragia primero; la biopsia se hace mañana en el laboratorio."
    )

    # ==========================================================
    # SLIDE 6: PATRONES DE ARQUITECTURA RESILIENTE
    # ==========================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "PATRONES DE ARQUITECTURA PARA DESPLOMAR EL MTTR")

    c_w = Inches(3.6)
    c_h = Inches(5.4)

    card1 = add_card(s6, Inches(0.8), Inches(1.35), c_w, c_h, CYAN)
    tf1 = card1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "1. ARQUITECTURA CELULAR (BULKHEADS)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN
    p = tf1.add_paragraph()
    p.text = (
        "\n• Inspirado en los compartimentos estancos de los submarinos.\n\n"
        "• Cada clúster o segmento atiende a un subconjunto cerrado de clientes o empresas.\n\n"
        "• Si una célula se corrompe por una sobrecarga, el fallo queda confinado al 5% de la carga; el 95% restante del banco sigue operando sin inmutarse."
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    card2 = add_card(s6, Inches(4.866), Inches(1.35), c_w, c_h, AMBER)
    tf2 = card2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "2. COLAS ASÍNCRONAS CON PERSISTENCIA"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = AMBER
    p = tf2.add_paragraph()
    p.text = (
        "\n• Desacoplamiento estricto del Core Bancario.\n\n"
        "• Si la pasarela de pagos cae durante 4 minutos, las transacciones no se rechazan: se encolan en Kafka con acuse de recibo y sellado criptográfico.\n\n"
        "• Se procesan en segundo plano en cuanto el backend recupera capacidad. Cero transacciones perdidas."
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    card3 = add_card(s6, Inches(8.733), Inches(1.35), c_w, c_h, MINT)
    tf3 = card3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "3. CANARY RELEASES & CIRCUIT BREAKERS"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = MINT
    p = tf3.add_paragraph()
    p.text = (
        "\n• Despliegue por anillos progresivos (1% -> 5% -> 25%).\n\n"
        "• Monitoreo de latencia y errores de negocio por segundo.\n\n"
        "• Si el anillo de prueba supera el umbral de riesgo, el disyuntor salta de inmediato y revierte el release en 30 segundos sin intervención manual."
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    s6.notes_slide.notes_text_frame.text = (
        "GUION DE PONENTE:\n"
        "Aquí está la conversación clave con nuestros arquitectos de software e infraestructura. "
        "Reducir el MTTR no es una cuestión de que los ingenieros tecleen más rápido; es una propiedad del diseño de software. "
        "Primero: compartimentos estancos celulares. Como en los barcos: si entra agua en la bodega tres, cerramos la compuerta y el barco sigue navegando. "
        "Segundo: amortiguación con colas. El cliente en la tienda no debe ver un cartel de 'error bancario' porque un microservicio esté saturado. Encolamos la petición y la ejecutamos en dos minutos. "
        "Tercero: despliegues canarios obligatorios. No más despliegues 'Big Bang' en viernes. Todo cambio entra al 1% del tráfico. Si falla, el Circuit Breaker lo apaga solo. "
        "La tecnología para hacer esto ya la tenemos en BBVA. Lo que necesitamos es el mandato corporativo para que sea el estándar inviolable en todos nuestros Tiers."
    )

    # ==========================================================
    # SLIDE 7: ERROR BUDGETS & CUMPLIMIENTO DORA
    # ==========================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "GOBERNANZA DE ERROR BUDGETS & REGULACIÓN DORA")

    c7_l = add_card(s7, Inches(0.8), Inches(1.35), Inches(5.6), Inches(5.6), CYAN)
    tf7_l = c7_l.text_frame
    tf7_l.word_wrap = True
    p = tf7_l.paragraphs[0]
    p.text = "ERROR BUDGETS: EL PACTO DEV VS. OPS"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN

    p = tf7_l.add_paragraph()
    p.text = (
        "\n• El conflicto histórico:\n"
        "  Negocio y Desarrollo quieren lanzar features a diario; Operaciones e Infraestructura quieren congelar cambios para evitar caídas.\n\n"
        "• La solución matemática (Error Budget):\n"
        "  El margen de indisponibilidad (0.01% - 0.1%) pertenece a ambos equipos.\n\n"
        "• La regla sagrada de SRE:\n"
        "  - Si hay presupuesto verde: vía libre para desplegar e innovar rápido.\n"
        "  - Si el presupuesto se agota por incidentes: congelación inmediata de nuevas funcionalidades comerciales. El 100% del sprint se dedica a resiliencia, refactorización y amortiguación de deuda técnica."
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    c7_r = add_card(s7, Inches(6.7), Inches(1.35), Inches(5.8), Inches(5.6), AMBER)
    tf7_r = c7_r.text_frame
    tf7_r.word_wrap = True
    p = tf7_r.paragraphs[0]
    p.text = "EL IMPERATIVO LEGAL DORA (2025/2026)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = AMBER

    p = tf7_r.add_paragraph()
    p.text = (
        "\n• Fin de las auditorías de 'checklist':\n"
        "  El reglamento europeo DORA ya no acepta planes de recuperación teóricos en archivadores PDF. Exige pruebas de estrés reales en vivo (*Threat-Led Penetration Testing*).\n\n"
        "• Notificación estricta de incidentes mayores:\n"
        "  Plazos de notificación al Banco de España medidos en horas. Un MTTR largo expone a la entidad a sanciones regulatorias públicas automáticas.\n\n"
        "• Auditoría de terceros críticos:\n"
        "  Exigencia de resiliencia demostrable a todos los proveedores cloud y SaaS de la cadena de suministro."
    )
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_LIGHT

    s7.notes_slide.notes_text_frame.text = (
        "GUION DE PONENTE:\n"
        "Hablemos ahora de gobernanza y regulación, porque aquí es donde la ingeniería se encuentra con el Comité de Dirección. "
        "Durante años hemos tenido tensiones entre los equipos de producto, que querían sacar funcionalidades a toda prisa, y los equipos de operaciones, que teníamos que aguantar las caídas de madrugada. "
        "El Error Budget resuelve esa fricción con números objetivos. Es un contrato social: mientras el servicio esté sano, desarrollo corre todo lo que quiera. "
        "Pero si una incidencia nos come el margen de indisponibilidad del mes, el siguiente sprint se congela. No entran nuevas pantallas ni botones: todo el equipo se sienta a arreglar la causa raíz. "
        "Y esto ya no es una recomendación interna: con la directiva europea DORA en pleno vigor, el regulador exige ver este mecanismo en funcionamiento. "
        "Tener un MTTR bajo y un control de Error Budget auditado es hoy nuestro mayor escudo de protección legal frente al Banco de España y el BCE."
    )

    # ==========================================================
    # SLIDE 8: HOJA DE RUTA TÁCTICA PARA BBVA
    # ==========================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "HOJA DE RUTA TÁCTICA PARA BBVA: TRES DECISIONES INAPLAZABLES")

    c8_card = add_card(s8, Inches(1), Inches(1.35), Inches(11.333), Inches(5.6), MINT)
    tf8 = c8_card.text_frame
    tf8.word_wrap = True

    p = tf8.paragraphs[0]
    p.text = "EL PLAN DE ACCIÓN PARA INFRAESTRUCTURA, ARQUITECTURA Y OPERACIONES"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = MINT

    p = tf8.add_paragraph()
    p.text = (
        "\n1. INSTITUCIONALIZAR EL COMANDO DE INCIDENTES (INCIDENT COMMAND)\n"
        "   • Blindar el Canal Alfa técnico en War Rooms: máximo 5 voces operativas.\n"
        "   • El Incident Commander tiene autoridad delegada absoluta para ejecutar rollbacks inmediatos sin esperar aprobación directiva.\n"
        "   • Canal Bravo independiente para mantener informados a comités y negocio con updates cada 30 minutos.\n\n"
        "2. VINCULAR LOS SLOS A TRANSACCIONES DE NEGOCIO REALES\n"
        "   • Sustituir las métricas sintéticas de pings al balanceador por la tasa de éxito de pagos reales en tiempo real.\n"
        "   • Objetivo corporativo homogéneo en Tier 1 bancario: MTTR medio inferior a 8 minutos.\n\n"
        "3. INTRODUCIR CIRCUIT BREAKERS Y CHAOS TESTING PROGRAMADO\n"
        "   • Ningún servicio pasa a producción sin disyuntores automáticos y colas de degradación asíncrona probadas.\n"
        "   • Inyectar fallos controlados en preproducción de forma rutinaria: la resiliencia no se asume, se entrena."
    )
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_LIGHT

    s8.notes_slide.notes_text_frame.text = (
        "GUION DE PONENTE:\n"
        "Para cerrar, quiero dejaros una propuesta pragmática con tres decisiones que podemos tomar desde hoy mismo en esta mesa. "
        "Primera: blindar el mando de incidentes. Cuando salte un P1, el Incident Commander manda. No entran 40 directores a preguntar '¿para cuándo?'. Los directores tienen su canal de comunicación formal con partes cada media hora. "
        "Segunda: cambiar las métricas de nuestros cuadros de mando. Dejemos de medir si el servidor contesta; midamos si los clientes están pudiendo pagar. Y comprometámonos a que ningún Tier 1 tarde más de ocho minutos en mitigar un incidente. "
        "Tercera: entrenar el fallo. Empecemos a romper cosas nosotros mismos de forma controlada los martes por la mañana. Si un servicio no aguanta la caída de una zona en preproducción, no puede salir a la calle. "
        "Si aplicamos estas tres palancas, no solo seremos el banco más ágil; seremos el banco más inquebrantable de Europa."
    )

    # ==========================================================
    # SLIDE 9: CONCLUSIÓN Y CIERRE EJECUTIVO
    # ==========================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)

    s9_card = add_card(s9, Inches(1.2), Inches(1.3), Inches(10.933), Inches(4.9), CYAN)
    tf9 = s9_card.text_frame
    tf9.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf9.word_wrap = True

    p = tf9.paragraphs[0]
    p.text = '"El prestigio y la solidez de una gran entidad financiera no se miden por la soberbia de proclamar que sus sistemas jamás fallarán,\n\nsino por la disciplina, arquitectura y humildad operativa para levantarse en cuestión de minutos antes de que sus clientes noten que ha tropezado."'
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT
    p.alignment = PP_ALIGN.CENTER

    p2 = tf9.add_paragraph()
    p2.text = (
        "\nAlexander Armentia (Alexar69)\n"
        "Reliability & Resilience Manager · BBVA\n"
        "alexanderarmentia.com"
    )
    p2.font.size = Pt(15)
    p2.font.color.rgb = CYAN
    p2.alignment = PP_ALIGN.CENTER

    s9.notes_slide.notes_text_frame.text = (
        "GUION DE PONENTE:\n"
        "(Pausa final. Mirada serena a los directores presentes).\n"
        "Compañeros: los sistemas complejos fallarán siempre. El software fallará, el hardware fallará, los proveedores cloud fallarán. "
        "Pero lo que define el liderazgo técnico de BBVA es la estatura de nuestra respuesta. "
        "Dejemos atrás la ilusión infantil del cero fallos. Abracemos la madurez de la resiliencia: aislemos el impacto, entrenemos a nuestros equipos y hagamos del MTTR nuestro mayor orgullo de ingeniería. "
        "Muchas gracias y quedo a vuestra disposición para el debate."
    )

    output_path = os.path.join(repo_dir, "presentacion-mtbf-vs-mttr-bbva.pptx")
    prs.save(output_path)
    print(f"BBVA Presentation saved successfully to: {output_path}")
    return output_path

if __name__ == "__main__":
    create_bbva_deck()

