import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blog", "assets", "presentation")
os.makedirs(output_dir, exist_ok=True)

BG_COLOR = "#070714"
CARD_BG = "#0f1026"
CYAN = "#22d3ee"
AMBER = "#f97316"
RED = "#ef4444"
MINT = "#34d399"
YELLOW = "#fbbf24"
TEXT_COLOR = "#f8fafc"
MUTED_COLOR = "#94a3b8"

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

def make_andon_explanatory_infographic():
    fig, ax = plt.subplots(figsize=(14, 8), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    
    # Header
    ax.text(0.5, 0.94, "EL PRINCIPIO ANDON: 'STOP THE LINE' (TOYOTA SYSTEM)",
            color=AMBER, fontsize=18, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.89, "La autoridad de detener la marcha ante la sospecha: el pilar que separa la resiliencia de la catástrofe",
            color=TEXT_COLOR, fontsize=11.5, ha='center', va='center')
    
    # 4 Phases Horizontal Flow
    phases = [
        {
            "num": "01",
            "title": "DETECCIÓN TEMPRANA\n(Señal Débil)",
            "desc": "El técnico o maquinista nota una vibración, holgura o lectura fuera de norma en vía.",
            "color": YELLOW,
            "badge": "ANOMALÍA DETECTADA",
            "badge_color": YELLOW
        },
        {
            "num": "02",
            "title": "ACTIVAR ANDON\n('Tirar de la Cuerda')",
            "desc": "El operario pulsa la parada o tira de la cuerda. La señal visual/acústica alerta a toda la planta.",
            "color": RED,
            "badge": "LÍNEA DETENIDA",
            "badge_color": RED
        },
        {
            "num": "03",
            "title": "SOPORTE AL 'GEMBA'\n(Cultura Sin Culpa)",
            "desc": "El jefe de equipo y especialistas acuden en segundos para ayudar, no para interrogar ni sancionar.",
            "color": CYAN,
            "badge": "APOYO INMEDIATO",
            "badge_color": CYAN
        },
        {
            "num": "04",
            "title": "CAUSA RAÍZ & FIX\n(Garantía Total)",
            "desc": "Se analizan los '5 Porqués' y se corrige el defecto estructural antes de reanudar el flujo.",
            "color": MINT,
            "badge": "REANUDACIÓN SEGURA",
            "badge_color": MINT
        }
    ]
    
    card_w = 0.205
    card_h = 0.38
    y_card = 0.46
    
    for i, p in enumerate(phases):
        x = 0.05 + i * 0.235
        # Box
        card = patches.FancyBboxPatch((x, y_card), card_w, card_h, boxstyle="round,pad=0.015",
                                      facecolor=CARD_BG, edgecolor=p["color"], linewidth=2)
        ax.add_patch(card)
        
        # Step number circle
        circle = patches.Circle((x + 0.03, y_card + card_h - 0.04), 0.022, facecolor=p["color"])
        ax.add_patch(circle)
        ax.text(x + 0.03, y_card + card_h - 0.04, p["num"], color=BG_COLOR, fontsize=11, fontweight='bold', ha='center', va='center')
        
        # Title
        ax.text(x + 0.065, y_card + card_h - 0.04, p["title"], color=p["color"], fontsize=10, fontweight='bold', va='center')
        
        # Description
        ax.text(x + 0.015, y_card + card_h - 0.14, p["desc"], color=TEXT_COLOR, fontsize=9, wrap=True, va='top')
        
        # Badge at bottom of card
        badge_box = patches.FancyBboxPatch((x + 0.015, y_card + 0.025), card_w - 0.03, 0.045, boxstyle="round,pad=0.008",
                                          facecolor="#181938", edgecolor=p["badge_color"], linewidth=1.2)
        ax.add_patch(badge_box)
        ax.text(x + card_w/2, y_card + 0.0475, p["badge"], color=p["badge_color"], fontsize=8.5, fontweight='bold', ha='center', va='center')
        
        # Arrow between cards
        if i < len(phases) - 1:
            arrow_x = x + card_w + 0.005
            ax.annotate("", xy=(arrow_x + 0.02, y_card + card_h/2), xytext=(arrow_x, y_card + card_h/2),
                        arrowprops=dict(arrowstyle="->", color=MUTED_COLOR, lw=2.5))

    # Bottom Comparison Table: CULTURA FRÁGIL VS CULTURA ANDON
    bot_y = 0.07
    bot_h = 0.33
    
    # Left comparison box: Cultura del Miedo al Retraso
    box_fragil = patches.FancyBboxPatch((0.05, bot_y), 0.435, bot_h, boxstyle="round,pad=0.015",
                                        facecolor=CARD_BG, edgecolor=RED, linewidth=1.8)
    ax.add_patch(box_fragil)
    ax.text(0.2675, bot_y + bot_h - 0.04, "[X] CULTURA DEL REPREGÚNTAME (Fragilidad por KPIs)",
            color=RED, fontsize=11.5, fontweight='bold', ha='center')
    
    fragil_points = [
        "• El operario calla la vibración: teme abrir expediente por retrasos.",
        "• Se asume que 'si ayer pasó el tren, hoy aguantará igual'.",
        "• La puntualidad comercial en verde disfraza la fractura progresiva.",
        "• Consecuencia: Rotura catastrófica de carril (Adamuz) o colisión (Urda)."
    ]
    y_f = bot_y + bot_h - 0.09
    for pt in fragil_points:
        ax.text(0.07, y_f, pt, color=TEXT_COLOR, fontsize=9.2)
        y_f -= 0.055

    # Right comparison box: Cultura Andon Resiliente
    box_andon = patches.FancyBboxPatch((0.515, bot_y), 0.435, bot_h, boxstyle="round,pad=0.015",
                                       facecolor=CARD_BG, edgecolor=MINT, linewidth=1.8)
    ax.add_patch(box_andon)
    ax.text(0.7325, bot_y + bot_h - 0.04, "[V] CULTURA ANDON (Resiliencia Operativa)",
            color=MINT, fontsize=11.5, fontweight='bold', ha='center')
    
    andon_points = [
        "• Se premia y agradece al maquinista o técnico que frena ante la duda.",
        "• Detener la vía 30 min cuesta dinero; descarrilar destruye vidas y la marca.",
        "• La dirección asume que parar es la máxima manifestación de fiabilidad.",
        "• Consecuencia: Cero accidentes graves por normalización de la desviación."
    ]
    y_a = bot_y + bot_h - 0.09
    for pt in andon_points:
        ax.text(0.535, y_a, pt, color=TEXT_COLOR, fontsize=9.2)
        y_a -= 0.055

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    path = os.path.join(output_dir, "slide5_andon_protocol.png")
    plt.tight_layout()
    plt.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated enhanced Andon diagram at: {path}")

if __name__ == "__main__":
    make_andon_explanatory_infographic()

