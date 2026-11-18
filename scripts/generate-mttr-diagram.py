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

def make_banking_mttr_diagram():
    fig, ax = plt.subplots(figsize=(14, 7.875), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    ax.text(0.5, 0.94, "ANATOMIA DEL MTTR BANCARIO: DE LA ALERTA A LA RECUPERACION EN < 10 MINUTOS",
            color=CYAN, fontsize=16, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "Por que en banca critica el MTTR importa 10x mas que el MTBF: desglose de tiempos y mitigacion",
            color=TEXT_COLOR, fontsize=11, ha='center', va='center')

    # Top Flow: The 8-Minute Modern SRE MTTR
    steps = [
        ("01. MTTD (90 seg)\nDETECCIÓN AUTOMÁTICA", "Alerta por caída de SLO en transacciones/segundo. Cero falsos positivos.", CYAN),
        ("02. TRIAGE (2 min)\nINCIDENT COMMAND", "Apertura de canal técnico Alfa. Se aísla el microservicio degradado.", AMBER),
        ("03. MITIGACIÓN (3 min)\nROLLBACK / CANARY", "Rollback automático o desvío de tráfico a célula secundaria.", MINT),
        ("04. VALIDACIÓN (2 min)\nTELEMETRÍA VERDE", "Comprobación de latencia p99 < 40ms. Fin del incidente comercial.", YELLOW)
    ]

    card_w = 0.21
    card_h = 0.28
    y_card = 0.54
    for i, (title, desc, color) in enumerate(steps):
        x = 0.05 + i * 0.235
        card = patches.FancyBboxPatch((x, y_card), card_w, card_h, boxstyle="round,pad=0.015",
                                      facecolor=CARD_BG, edgecolor=color, linewidth=2)
        ax.add_patch(card)
        ax.text(x + card_w/2, y_card + card_h - 0.05, title, color=color, fontsize=10, fontweight='bold', ha='center')
        ax.text(x + card_w/2, y_card + card_h - 0.14, desc, color=TEXT_COLOR, fontsize=8.5, ha='center', wrap=True)
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + card_w + 0.015, y_card + card_h/2), xytext=(x + card_w, y_card + card_h/2),
                        arrowprops=dict(arrowstyle="->", color=MUTED_COLOR, lw=2))

    # Bottom Comparison: TRADITIONAL CHAOS (MTTR > 3 HORAS) vs MODERN BANKING RESILIENCE (MTTR < 10 MIN)
    # Left: Tradicional (MTTR 3h+)
    box_old = patches.FancyBboxPatch((0.05, 0.08), 0.435, 0.38, boxstyle="round,pad=0.015",
                                     facecolor=CARD_BG, edgecolor=RED, linewidth=1.8)
    ax.add_patch(box_old)
    ax.text(0.2675, 0.42, "[ANTIPATRÓN] BANCA TRADICIONAL (MTTR: 3 a 6 horas)", color=RED, fontsize=11.5, fontweight='bold', ha='center')
    old_items = [
        "- Detección tardía: el usuario llama a atención al cliente.",
        "- War Room con 50 personas discutiendo hipótesis a ciegas.",
        "- Intentos de 'hotfix' y parches en caliente en base de datos.",
        "- Despliegues 'Big Bang' sin posibilidad de rollback rápido.",
        "- Coste millonario: sanciones del BCE, daño reputacional y Bizum caído."
    ]
    y_o = 0.36
    for it in old_items:
        ax.text(0.07, y_o, it, color=TEXT_COLOR, fontsize=9.2)
        y_o -= 0.055

    # Right: SRE Bancario Moderno (MTTR < 10 min)
    box_new = patches.FancyBboxPatch((0.515, 0.08), 0.435, 0.38, boxstyle="round,pad=0.015",
                                     facecolor=CARD_BG, edgecolor=MINT, linewidth=1.8)
    ax.add_patch(box_new)
    ax.text(0.7325, 0.42, "[PATRÓN SRE] ALTA DISPONIBILIDAD BANCARIA (MTTR < 10 min)", color=MINT, fontsize=11.5, fontweight='bold', ha='center')
    new_items = [
        "+ Detección sintética y telemetría por segundo (MTTD < 90s).",
        "+ Circuit Breakers automáticos: corte selectivo sin colapsar el Core.",
        "+ Rollback incondicional en 1 clic o balanceo celular a zona sana.",
        "+ Resguardo de transacciones en cola persistente sin pérdida de saldo.",
        "+ Cumplimiento estricto DORA / BCE con Post-Mortems sin culpa."
    ]
    y_n = 0.36
    for it in new_items:
        ax.text(0.535, y_n, it, color=TEXT_COLOR, fontsize=9.2)
        y_n -= 0.055

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    path = os.path.join(output_dir, "mttr-bancario-disponibilidad-gestion-incidencias-p1.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated banking MTTR diagram: {path}")

if __name__ == "__main__":
    make_banking_mttr_diagram()
