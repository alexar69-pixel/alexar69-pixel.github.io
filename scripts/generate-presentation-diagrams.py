import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blog", "assets", "presentation")
os.makedirs(output_dir, exist_ok=True)

# Dark theme palette
BG_COLOR = "#06060f"
CARD_BG = "#0f0f22"
CYAN = "#22d3ee"
AMBER = "#f97316"
RED = "#ef4444"
MINT = "#34d399"
TEXT_COLOR = "#f1f1f3"
MUTED_COLOR = "#9ca3af"

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# ==========================================================
# 1. SLIDE 2: GOODHART & NORMALIZATION OF DEVIANCE
# ==========================================================
def make_goodhart_diagram():
    fig, ax = plt.subplots(figsize=(12, 6.75), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    
    # Title
    ax.text(0.5, 0.94, "LA TRAMPA DE LA EFICIENCIA: NORMALIZACIÓN DE LA DESVIACIÓN",
            color=TEXT_COLOR, fontsize=16, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "La métrica verde en el cuadro de mando oculta la acumulación invisible de microfallos",
            color=CYAN, fontsize=11, ha='center', va='center')
    
    # Top box: Dashboard illusion
    rect_top = patches.FancyBboxPatch((0.08, 0.68), 0.84, 0.15, boxstyle="round,pad=0.02",
                                      facecolor=CARD_BG, edgecolor=MINT, linewidth=2)
    ax.add_patch(rect_top)
    ax.text(0.12, 0.77, "DASHBOARD COMERCIAL (ILUSION DE EXITO):", color=MINT, fontsize=11, fontweight='bold')
    ax.text(0.12, 0.72, "• Puntualidad: 99.8%  [OK]   • Ocupación de vía: 98%  [MÁXIMA]   • Retrasos penalizados: 0  [OBJETIVO CUMPLIDO]",
            color=TEXT_COLOR, fontsize=10)
    
    # Timeline curve below
    x = np.linspace(0.1, 0.9, 200)
    # Exponential stress curve
    y = 0.18 + 0.05 * np.exp(3.2 * (x - 0.1) / 0.8)
    
    ax.plot(x, y, color=RED, linewidth=3.5, label="Tensión y fatiga estructural acumulada")
    
    # Critical threshold line
    ax.axhline(0.52, color=AMBER, linestyle='--', linewidth=1.8, xmin=0.1, xmax=0.9)
    ax.text(0.12, 0.54, "LÍMITE FÍSICO DE SEGURIDAD (PUNTO CRÍTICO)", color=AMBER, fontsize=9.5, fontweight='bold')
    
    # Anomaly points along the curve
    pts_x = [0.25, 0.42, 0.60, 0.75]
    for px in pts_x:
        py = 0.18 + 0.05 * np.exp(3.2 * (px - 0.1) / 0.8)
        ax.plot(px, py, 'o', color=AMBER, markersize=8)
        ax.text(px, py - 0.05, "Vibración ignorada\n'Ayer no pasó nada'", color=MUTED_COLOR, fontsize=8, ha='center')
        
    # Catastrophic failure point
    fail_x = 0.86
    fail_y = 0.18 + 0.05 * np.exp(3.2 * (fail_x - 0.1) / 0.8)
    ax.plot(fail_x, fail_y, '*', color=RED, markersize=20)
    ax.text(fail_x, fail_y + 0.05, "ROTURA / COLAPSO\n(Adamuz / Urda)", color=RED, fontsize=11, fontweight='bold', ha='center')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0.05, 1)
    ax.axis('off')
    
    path = os.path.join(output_dir, "slide2_goodhart_deviance.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ==========================================================
# 2. SLIDE 3: ADAMUZ VS URDA ARCHITECTURAL COMPARISON
# ==========================================================
def make_adamuz_urda_diagram():
    fig, ax = plt.subplots(figsize=(12, 6.75), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    
    ax.text(0.5, 0.94, "ANATOMÍA DE DOS FALLOS EN LA MISMA INFRAESTRUCTURA",
            color=TEXT_COLOR, fontsize=16, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "Dos escenarios técnicos distintos que comparten la misma raíz: la quiebra de la resiliencia",
            color=CYAN, fontsize=11, ha='center', va='center')
    
    # Left box: ADAMUZ
    box_a = patches.FancyBboxPatch((0.06, 0.12), 0.42, 0.70, boxstyle="round,pad=0.02",
                                   facecolor=CARD_BG, edgecolor=RED, linewidth=2)
    ax.add_patch(box_a)
    ax.text(0.27, 0.76, "CASO 1: ADAMUZ (Enero 2026)\nFallo de Componente + Cero Contención",
            color=RED, fontsize=12, fontweight='bold', ha='center')
    
    a_steps = [
        "1. Fatiga de carril / soldadura debilitada",
        "2. Decenas de trenes pasan sobre la fisura",
        "   (Señales débiles no atendidas)",
        "3. Descarrilamiento en vía par",
        "4. Quiebra de Blast Radius:",
        "   Invasión física de la vía contraria",
        "5. Colisión frontal Alvia sin frenado previo"
    ]
    y_pos = 0.65
    for s in a_steps:
        color = TEXT_COLOR if not s.startswith("4.") else AMBER
        ax.text(0.10, y_pos, s, color=color, fontsize=10)
        y_pos -= 0.075

    # Right box: URDA
    box_u = patches.FancyBboxPatch((0.52, 0.12), 0.42, 0.70, boxstyle="round,pad=0.02",
                                   facecolor=CARD_BG, edgecolor=AMBER, linewidth=2)
    ax.add_patch(box_u)
    ax.text(0.73, 0.76, "CASO 2: URDA (Octubre 2026)\nFallo de Estado Degradado + Sin Fail-Safe",
            color=AMBER, fontsize=12, fontweight='bold', ha='center')
    
    u_steps = [
        "1. Tren 1 detenido en vía por avería mecánica",
        "   (Escenario operativo nominal previsto)",
        "2. Pérdida de detección / bloqueo de cantón",
        "3. Ausencia de Graceful Degradation:",
        "   El sistema no forzó parada de emergencia",
        "4. Tren 2 (AVE) aproxima a velocidad comercial",
        "5. Colisión por alcance en la misma vía"
    ]
    y_pos = 0.65
    for s in u_steps:
        color = TEXT_COLOR if not s.startswith("3.") else RED
        ax.text(0.56, y_pos, s, color=color, fontsize=10)
        y_pos -= 0.075
        
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    path = os.path.join(output_dir, "slide3_adamuz_vs_urda.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ==========================================================
# 3. SLIDE 4: RELIABILITY VS RESILIENCE MATRIX
# ==========================================================
def make_rel_vs_res_diagram():
    fig, ax = plt.subplots(figsize=(12, 6.75), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    
    ax.text(0.5, 0.94, "RELIABILITY VS. RESILIENCIA: LA FRONTERA VITAL",
            color=TEXT_COLOR, fontsize=16, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "Dos disciplinas complementarias que jamás deben confundirse en un comité de dirección",
            color=CYAN, fontsize=11, ha='center', va='center')
    
    # Left Box: RELIABILITY
    box_r = patches.FancyBboxPatch((0.08, 0.12), 0.40, 0.70, boxstyle="round,pad=0.02",
                                   facecolor=CARD_BG, edgecolor=CYAN, linewidth=2)
    ax.add_patch(box_r)
    ax.text(0.28, 0.76, "RELIABILITY (Fiabilidad)\n'Diseñar para no fallar'", color=CYAN, fontsize=13, fontweight='bold', ha='center')
    
    r_items = [
        ("Objetivo:", "Que las piezas no se rompan"),
        ("Métrica rey:", "MTBF (Mean Time Between Failures)"),
        ("Estrategia:", "Tolerancias, calidad de acero, balasto"),
        ("Enfoque:", "Prevención antes del suceso"),
        ("Límite:", "En el mundo real, todo material fatiga."),
        ("Realidad:", "La fiabilidad siempre se agota.")
    ]
    y_pos = 0.65
    for title, desc in r_items:
        ax.text(0.12, y_pos, f"• {title} ", color=CYAN, fontsize=10, fontweight='bold')
        ax.text(0.12, y_pos - 0.035, f"   {desc}", color=TEXT_COLOR, fontsize=9.5)
        y_pos -= 0.085

    # Right Box: RESILIENCE
    box_res = patches.FancyBboxPatch((0.52, 0.12), 0.40, 0.70, boxstyle="round,pad=0.02",
                                     facecolor=CARD_BG, edgecolor=MINT, linewidth=2)
    ax.add_patch(box_res)
    ax.text(0.72, 0.76, "RESILIENCE (Resiliencia)\n'Sobrevivir cuando el fallo ocurre'", color=MINT, fontsize=13, fontweight='bold', ha='center')
    
    res_items = [
        ("Objetivo:", "Que el fallo no destruya el sistema"),
        ("Métrica rey:", "MTTR y Contención de Blast Radius"),
        ("Estrategia:", "Degradación elegante, Fail-Safe, Andon"),
        ("Enfoque:", "Absorción y respuesta post-fallo"),
        ("Garantía:", "El descarrilamiento no invade vía contraria."),
        ("Realidad:", "Es lo que salva vidas cuando el metal rompe.")
    ]
    y_pos = 0.65
    for title, desc in res_items:
        ax.text(0.56, y_pos, f"• {title} ", color=MINT, fontsize=10, fontweight='bold')
        ax.text(0.56, y_pos - 0.035, f"   {desc}", color=TEXT_COLOR, fontsize=9.5)
        y_pos -= 0.085

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    path = os.path.join(output_dir, "slide4_rel_vs_res.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ==========================================================
# 4. SLIDE 5: ANDON PROTOCOL (STOP THE LINE)
# ==========================================================
def make_andon_diagram():
    fig, ax = plt.subplots(figsize=(12, 6.75), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    
    ax.text(0.5, 0.94, "EL PRINCIPIO ANDON: EL CORAJE DE PARAR LA LÍNEA",
            color=TEXT_COLOR, fontsize=16, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "Nacido en Toyota: La autoridad indiscutible de cualquier operario de detener la producción",
            color=AMBER, fontsize=11, ha='center', va='center')
    
    # 3-step workflow diagram
    steps = [
        ("1. DETECCIÓN", "Cualquier maquinista, sensor o técnico detecta una señal débil o vibración fuera de norma.", CARD_BG, CYAN),
        ("2. STOP THE LINE", "Se pulsa el botón rojo. La vía o el servicio se detiene de inmediato. Sin represalias.", CARD_BG, RED),
        ("3. CULTURA DE GRATITUD", "La dirección aplaude al operador: 'Gracias por evitar un siniestro millonario e irreparable'.", CARD_BG, MINT)
    ]
    
    x_coords = [0.08, 0.38, 0.68]
    for i, (title, desc, bg, border) in enumerate(steps):
        bx = patches.FancyBboxPatch((x_coords[i], 0.32), 0.25, 0.45, boxstyle="round,pad=0.02",
                                    facecolor=bg, edgecolor=border, linewidth=2.5)
        ax.add_patch(bx)
        ax.text(x_coords[i] + 0.125, 0.70, title, color=border, fontsize=12, fontweight='bold', ha='center')
        ax.text(x_coords[i] + 0.02, 0.55, desc, color=TEXT_COLOR, fontsize=9.5, wrap=True)
        
        # Arrow between steps
        if i < 2:
            ax.annotate("", xy=(x_coords[i+1] - 0.01, 0.54), xytext=(x_coords[i] + 0.27, 0.54),
                        arrowprops=dict(arrowstyle="->", color=MUTED_COLOR, lw=3))
            
    # Bottom callout
    bot = patches.FancyBboxPatch((0.15, 0.10), 0.70, 0.14, boxstyle="round,pad=0.02",
                                 facecolor=CARD_BG, edgecolor=AMBER, linewidth=1.5)
    ax.add_patch(bot)
    ax.text(0.5, 0.17, "LA PREGUNTA PARA NUESTRAS EMPRESAS:\n¿Tienen hoy nuestros técnicos la tranquilidad de parar un tren sin miedo al titular de prensa?",
            color=TEXT_COLOR, fontsize=10.5, ha='center', va='center', fontweight='bold')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    path = os.path.join(output_dir, "slide5_andon_protocol.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ==========================================================
# 5. SLIDE 6: SRE CIRCUIT BREAKER PATTERN
# ==========================================================
def make_circuit_breaker_diagram():
    fig, ax = plt.subplots(figsize=(12, 6.75), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    
    ax.text(0.5, 0.94, "DE LA BANCA AL FERROCARRIL: PATRONES DE AISLAMIENTO",
            color=TEXT_COLOR, fontsize=16, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "Cómo los principios de SRE protegen plataformas críticas de colapsos sistémicos",
            color=CYAN, fontsize=11, ha='center', va='center')
    
    # 3 circular or pill patterns
    patterns = [
        ("CIRCUIT BREAKER", "Cortar el flujo de forma automática en milisegundos en cuanto se detecta una anomalía crítica. En banca aísla transacciones; en ferrocarril bloquea cantones.", CYAN),
        ("ERROR BUDGET", "El margen de riesgo no es infinito. Si se consumen fallos en alertas de vía, se congelan frecuencias adicionales hasta sanear la infraestructura.", AMBER),
        ("BLAMELESS POST-MORTEM", "No se buscan cabezas de turco en el maquinista o técnico. Se auditan los incentivos del sistema: ¿por qué los KPIs empujaron a operar al límite?", MINT)
    ]
    
    x_positions = [0.08, 0.38, 0.68]
    for i, (title, text, color) in enumerate(patterns):
        box = patches.FancyBboxPatch((x_positions[i], 0.20), 0.25, 0.60, boxstyle="round,pad=0.02",
                                     facecolor=CARD_BG, edgecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(x_positions[i] + 0.125, 0.72, title, color=color, fontsize=12, fontweight='bold', ha='center')
        ax.text(x_positions[i] + 0.02, 0.48, text, color=TEXT_COLOR, fontsize=9.5, wrap=True)
        
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    path = os.path.join(output_dir, "slide6_circuit_breakers.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ==========================================================
# 6. SLIDE 7: BALANCE DE KPIS (EFICIENCIA VS RESILIENCIA)
# ==========================================================
def make_balance_diagram():
    fig, ax = plt.subplots(figsize=(12, 6.75), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    
    ax.text(0.5, 0.94, "REEQUILIBRANDO EL CUADRO DE MANDO CORPORATIVO",
            color=TEXT_COLOR, fontsize=16, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "Sustituir métricas de ilusión comercial por invariantes de resiliencia estructural",
            color=CYAN, fontsize=11, ha='center', va='center')
    
    # Left Box: Métricas Frágiles
    left_box = patches.FancyBboxPatch((0.08, 0.16), 0.39, 0.65, boxstyle="round,pad=0.02",
                                     facecolor=CARD_BG, edgecolor=RED, linewidth=2)
    ax.add_patch(left_box)
    ax.text(0.275, 0.74, "[FRAGIL]  METRICAS DE ILUSION (Eficiencia)", color=RED, fontsize=12, fontweight='bold', ha='center')
    
    l_items = [
        "• % Puntualidad comercial a cualquier precio",
        "• Frecuencia máxima saturando la vía",
        "• Ahorro en ventanas nocturnas de mantenimiento",
        "• MTTR orientado a reabrir la vía en minutos",
        "• Buscar culpables individuales en el reporte"
    ]
    y = 0.64
    for it in l_items:
        ax.text(0.11, y, it, color=TEXT_COLOR, fontsize=9.5)
        y -= 0.10

    # Right Box: Métricas de Resiliencia
    right_box = patches.FancyBboxPatch((0.53, 0.16), 0.39, 0.65, boxstyle="round,pad=0.02",
                                      facecolor=CARD_BG, edgecolor=MINT, linewidth=2)
    ax.add_patch(right_box)
    ax.text(0.725, 0.74, "[RESILIENTE]  METRICAS DE RESILIENCIA (Supervivencia)", color=MINT, fontsize=12, fontweight='bold', ha='center')
    
    r_items = [
        "• % Respeto estricto a ventanas de mantenimiento",
        "• Margen dinámico garantizado entre cantones",
        "• Velocidad de inspección física de señales débiles",
        "• Garantía de causa raíz antes de reanudar tráfico",
        "• Cultura 'Blameless' que premia parar ante la duda"
    ]
    y = 0.64
    for it in r_items:
        ax.text(0.56, y, it, color=TEXT_COLOR, fontsize=9.5)
        y -= 0.10

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    path = os.path.join(output_dir, "slide7_balance_kpis.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

if __name__ == "__main__":
    make_goodhart_diagram()
    make_adamuz_urda_diagram()
    make_rel_vs_res_diagram()
    make_andon_diagram()
    make_circuit_breaker_diagram()
    make_balance_diagram()
    print("All explanatory diagrams generated successfully!")
