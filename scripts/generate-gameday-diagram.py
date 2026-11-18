import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blog", "assets")
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

def make_gameday_diagram():
    fig, ax = plt.subplots(figsize=(14, 7.875), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    ax.text(0.5, 0.94, "JUEGOS DE SIMULACION DE CAIDAS: GAMEDAYS Y LA RUEDA DE LA DESGRACIA",
            color=AMBER, fontsize=17, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "Como entrenar el musculo del MTTR en banca critica antes de que el fallo ocurra en la realidad",
            color=TEXT_COLOR, fontsize=11, ha='center', va='center')

    modalities = [
        {
            "num": "01",
            "name": "WHEEL OF MISFORTUNE\n(Juego de Rol SRE)",
            "focus": "Entrenamiento de Guardias",
            "desc": "• Game Master simula un P1 historico o inedito.\n• El ingeniero de guardia diagnostica a ciegas.\n• Se miden reflejos y uso de telemetria.",
            "color": CYAN,
            "badge": "ROLE-PLAYING SEMANAL"
        },
        {
            "num": "02",
            "name": "TABLETOP EXERCISE\n(Crisis de Dirección)",
            "focus": "Gobernanza y Negocio",
            "desc": "• Ejercicio de mesa con directores y C-Level.\n• Se simula caida de Bizum o ataque ransomware.\n• Se ensaya comunicacion a medios y BCE/DORA.",
            "color": YELLOW,
            "badge": "SIMULACRO EJECUTIVO"
        },
        {
            "num": "03",
            "name": "CHAOS GAMEDAY\n(Inyeccion en Vivo)",
            "focus": "Validacion de Arquitectura",
            "desc": "• Martes 10:00h con todo el equipo despierto.\n• Se apaga una zona cloud o base de datos.\n• Se valida que el Circuit Breaker salte solo.",
            "color": MINT,
            "badge": "CHAOS ENGINEERING"
        },
        {
            "num": "04",
            "name": "DiRT / BLACKHOLE\n(Resiliencia Extrema)",
            "focus": "Desconexión de Región",
            "desc": "• Simulacro anual a escala masiva.\n• Corte real de un centro de datos entero.\n• Auditoria de cumplimiento DORA obligatoria.",
            "color": RED,
            "badge": "CUMPLIMIENTO DORA"
        }
    ]

    card_w = 0.21
    card_h = 0.65
    y_card = 0.16

    for i, m in enumerate(modalities):
        x = 0.05 + i * 0.235
        card = patches.FancyBboxPatch((x, y_card), card_w, card_h, boxstyle="round,pad=0.015",
                                      facecolor=CARD_BG, edgecolor=m["color"], linewidth=2)
        ax.add_patch(card)

        # Header tag
        tag_box = patches.FancyBboxPatch((x + 0.02, y_card + card_h - 0.07), card_w - 0.04, 0.045, boxstyle="round,pad=0.008",
                                         facecolor="#181938", edgecolor=m["color"], linewidth=1.2)
        ax.add_patch(tag_box)
        ax.text(x + card_w/2, y_card + card_h - 0.0475, m["badge"], color=m["color"], fontsize=8.5, fontweight='bold', ha='center', va='center')

        # Title
        ax.text(x + card_w/2, y_card + card_h - 0.15, m["name"], color=TEXT_COLOR, fontsize=11, fontweight='bold', ha='center', va='center')
        ax.text(x + card_w/2, y_card + card_h - 0.22, f"Foco: {m['focus']}", color=m["color"], fontsize=9.5, ha='center')

        # Desc
        ax.text(x + 0.015, y_card + card_h - 0.28, m["desc"], color=TEXT_COLOR, fontsize=9.2, va='top')

        # Metric box at bottom
        mbox = patches.FancyBboxPatch((x + 0.015, y_card + 0.03), card_w - 0.03, 0.065, boxstyle="round,pad=0.008",
                                      facecolor="#101124", edgecolor=m["color"], linewidth=1)
        ax.add_patch(mbox)
        ax.text(x + card_w/2, y_card + 0.062, f"Impacto en MTTR:\n-40% tiempo de resolución", color=m["color"], fontsize=8, ha='center', va='center')

        if i < len(modalities) - 1:
            arrow_x = x + card_w + 0.005
            ax.annotate("", xy=(arrow_x + 0.02, y_card + card_h/2), xytext=(arrow_x, y_card + card_h/2),
                        arrowprops=dict(arrowstyle="->", color=MUTED_COLOR, lw=2.5))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    path = os.path.join(output_dir, "gamedays-chaos-engineering-simulacion-caidas-banca.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated GameDay diagram: {path}")

if __name__ == "__main__":
    make_gameday_diagram()

