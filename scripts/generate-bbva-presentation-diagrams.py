import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blog", "assets", "presentation")
os.makedirs(output_dir, exist_ok=True)

BG_COLOR = "#060b14"        # Dark Executive Navy/Slate
CARD_BG = "#0c1527"         # Card background
BBVA_BLUE = "#004481"       # BBVA Blue
BBVA_NAVY = "#1464a5"       # BBVA Accent Blue
CYAN = "#22d3ee"            # Cyan accent
AMBER = "#f97316"           # Amber alert
RED = "#ef4444"             # Red error
MINT = "#34d399"            # Mint recovery
YELLOW = "#fbbf24"          # Yellow tag
TEXT_COLOR = "#f8fafc"
MUTED_COLOR = "#94a3b8"

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# ==============================================================================
# 1. PARADOJA DE LOS DOS BANCOS (MTBF vs MTTR)
# ==============================================================================
def make_two_banks_diagram():
    fig, ax = plt.subplots(figsize=(14, 7.875), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    ax.text(0.5, 0.94, "LA PARADOJA DE LOS DOS BANCOS: MTBF VS. MTTR EN LA PRÁCTICA",
            color=CYAN, fontsize=17, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "¿Qué entidad presenta un riesgo operativo y regulatorio (DORA/BCE) más letal?",
            color=TEXT_COLOR, fontsize=11, ha='center', va='center')

    # Left Box: Banco A (Obsesión MTBF)
    box_a = patches.FancyBboxPatch((0.06, 0.12), 0.42, 0.70, boxstyle="round,pad=0.02",
                                   facecolor=CARD_BG, edgecolor=RED, linewidth=2)
    ax.add_patch(box_a)
    ax.text(0.27, 0.76, "BANCO A: OBSESION POR EL MTBF\n'Diseñado para no caer nunca'",
            color=RED, fontsize=12, fontweight='bold', ha='center')

    a_metrics = [
        ("Frecuencia de fallo:", "1 sola caída al año (MTBF aparente: 8.760h)"),
        ("Tiempo de recuperación:", "4 horas y media (270 minutos de parada)"),
        ("Indisponibilidad anual:", "270 minutos (SLA real: 99.48%)"),
        ("Impacto en clientes:", "Pagos con tarjeta y Bizum caídos en hora punta"),
        ("Impacto regulatorio:", "Aviso obligatorio BCE + Multas severas DORA"),
        ("Consecuencia reputacional:", "Apertura en informativos nacionales y Twitter")
    ]
    y_pos = 0.64
    for title, val in a_metrics:
        ax.text(0.09, y_pos, f"• {title}", color=RED, fontsize=9.5, fontweight='bold')
        ax.text(0.09, y_pos - 0.035, f"   {val}", color=TEXT_COLOR, fontsize=9)
        y_pos -= 0.085

    # Right Box: Banco B (Maestría en MTTR)
    box_b = patches.FancyBboxPatch((0.52, 0.12), 0.42, 0.70, boxstyle="round,pad=0.02",
                                   facecolor=CARD_BG, edgecolor=MINT, linewidth=2)
    ax.add_patch(box_b)
    ax.text(0.73, 0.76, "BANCO B: MAESTRIA EN MTTR\n'Diseñado para recuperarse en minutos'",
            color=MINT, fontsize=12, fontweight='bold', ha='center')

    b_metrics = [
        ("Frecuencia de fallo:", "6 micro-degradaciones al año (1 cada 2 meses)"),
        ("Tiempo de recuperación:", "3 minutos por evento (MTTR: < 180 seg)"),
        ("Indisponibilidad anual:", "18 minutos en total (SLA real: 99.96%)"),
        ("Impacto en clientes:", "Reintento transparente en segundo plano; cero pánico"),
        ("Impacto regulatorio:", "Dentro de Error Budget; reporte ordinario sin sanción"),
        ("Consecuencia reputacional:", "Inapreciable; confianza del mercado blindada")
    ]
    y_pos = 0.64
    for title, val in b_metrics:
        ax.text(0.55, y_pos, f"• {title}", color=MINT, fontsize=9.5, fontweight='bold')
        ax.text(0.55, y_pos - 0.035, f"   {val}", color=TEXT_COLOR, fontsize=9)
        y_pos -= 0.085

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    path = os.path.join(output_dir, "bbva_mtbf_vs_mttr_paradoja.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ==============================================================================
# 2. EL PIPELINE DEL MTTR BANCARIO A < 8 MINUTOS
# ==============================================================================
def make_mttr_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(14, 7.875), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    ax.text(0.5, 0.94, "EL PIPELINE SRE DE RECUPERACION BANCARIA A < 8 MINUTOS",
            color=CYAN, fontsize=17, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "Deconstrucción temporal de un incidente P1: automatización vs fricción humana",
            color=TEXT_COLOR, fontsize=11, ha='center', va='center')

    phases = [
        {
            "num": "T1",
            "title": "MTTD: DETECCION\n< 90 Segundos",
            "desc": "Telemetría sintética y alertas por caída de SLO en transacciones/segundo.\nCero falsos positivos.",
            "color": CYAN,
            "badge": "ALERTING ACTIVO"
        },
        {
            "num": "T2",
            "title": "MTTI: AISLAMIENTO\n< 2 Minutos",
            "desc": "El Incident Commander abre canal Alfa.\nCircuit Breaker corta el flujo hacia el nodo anómalo.",
            "color": AMBER,
            "badge": "CIRCUIT BREAKER"
        },
        {
            "num": "T3",
            "title": "MTTR: MITIGACION\n< 3 Minutos",
            "desc": "Rollback automático o desvío celular a zona sana.\nNo se analiza el código en caliente.",
            "color": MINT,
            "badge": "SERVICIO RESTAURADO"
        },
        {
            "num": "T4",
            "title": "MTTA: APRENDIZAJE\nPost-Incidente",
            "desc": "Blameless Post-Mortem y 5 Porqués.\nCierre de acciones en backlog para blindar el sistema.",
            "color": YELLOW,
            "badge": "MEJORA SISTÉMICA"
        }
    ]

    card_w = 0.21
    card_h = 0.36
    y_card = 0.46

    for i, p in enumerate(phases):
        x = 0.05 + i * 0.235
        card = patches.FancyBboxPatch((x, y_card), card_w, card_h, boxstyle="round,pad=0.015",
                                      facecolor=CARD_BG, edgecolor=p["color"], linewidth=2)
        ax.add_patch(card)

        # Step tag
        circle = patches.Circle((x + 0.03, y_card + card_h - 0.04), 0.022, facecolor=p["color"])
        ax.add_patch(circle)
        ax.text(x + 0.03, y_card + card_h - 0.04, p["num"], color=BG_COLOR, fontsize=10, fontweight='bold', ha='center', va='center')

        # Title
        ax.text(x + 0.065, y_card + card_h - 0.04, p["title"], color=p["color"], fontsize=10, fontweight='bold', va='center')

        # Desc
        ax.text(x + 0.015, y_card + card_h - 0.14, p["desc"], color=TEXT_COLOR, fontsize=9, va='top')

        # Badge
        badge = patches.FancyBboxPatch((x + 0.015, y_card + 0.025), card_w - 0.03, 0.045, boxstyle="round,pad=0.008",
                                       facecolor="#181938", edgecolor=p["color"], linewidth=1.2)
        ax.add_patch(badge)
        ax.text(x + card_w/2, y_card + 0.0475, p["badge"], color=p["color"], fontsize=8.5, fontweight='bold', ha='center', va='center')

        if i < len(phases) - 1:
            arrow_x = x + card_w + 0.005
            ax.annotate("", xy=(arrow_x + 0.02, y_card + card_h/2), xytext=(arrow_x, y_card + card_h/2),
                        arrowprops=dict(arrowstyle="->", color=MUTED_COLOR, lw=2.5))

    # Bottom summary box
    bot_card = patches.FancyBboxPatch((0.05, 0.08), 0.90, 0.30, boxstyle="round,pad=0.015",
                                      facecolor=CARD_BG, edgecolor=CYAN, linewidth=1.5)
    ax.add_patch(bot_card)
    ax.text(0.5, 0.32, "LA DISTINCIÓN VITAL PARA EL COMITÉ DE DIRECCIÓN:", color=CYAN, fontsize=12, fontweight='bold', ha='center')
    ax.text(0.5, 0.25, "'MITIGAR NO ES ARREGLAR'. La War Room técnica tiene como único cometido restaurar el tráfico en minutos.\nLa investigación forense y la corrección de código pertenecen al laboratorio de día.", color=TEXT_COLOR, fontsize=10.5, ha='center', va='center')
    ax.text(0.5, 0.15, "Meta BBVA: Tiempo total de parada comercial P1 < 8 minutos | Cero pérdida de transacciones financieras", color=MINT, fontsize=11, fontweight='bold', ha='center')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    path = os.path.join(output_dir, "bbva_pipeline_mttr_8_minutos.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ==============================================================================
# 3. DISPONIBILIDAD DE MARKETING VS DISPONIBILIDAD TRANSACCIONAL
# ==============================================================================
def make_availability_pyramid_diagram():
    fig, ax = plt.subplots(figsize=(14, 7.875), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    ax.text(0.5, 0.94, "DISPONIBILIDAD REAL VS. DISPONIBILIDAD DE MARKETING",
            color=YELLOW, fontsize=17, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "Por qué los 'pings' al balanceador ocultan el fallo y cómo medir el SLO de negocio",
            color=TEXT_COLOR, fontsize=11, ha='center', va='center')

    # Left: Disponibilidad de Marketing (La mentira del 99.99%)
    b_left = patches.FancyBboxPatch((0.06, 0.12), 0.42, 0.70, boxstyle="round,pad=0.02",
                                    facecolor=CARD_BG, edgecolor=RED, linewidth=2)
    ax.add_patch(b_left)
    ax.text(0.27, 0.76, "[METRICA CIEGA] DISPONIBILIDAD SINTETICA\n'El servidor devuelve HTTP 200'",
            color=RED, fontsize=12, fontweight='bold', ha='center')

    blind_points = [
        "- Medición en el balanceador o CDN externa",
        "- El endpoint /healthcheck responde OK en 10 ms",
        "- Realidad oculta: La base de datos tiene deadlock",
        "- Las transacciones de Bizum fallan por debajo",
        "- En el informe corporativo: 'Disponibilidad 99.99%'",
        "- En redes sociales: Miles de clientes quejándose",
        "- Consecuencia: Ceguera ejecutiva ante el fallo real"
    ]
    y_m = 0.64
    for pt in blind_points:
        ax.text(0.09, y_m, pt, color=TEXT_COLOR, fontsize=9.2)
        y_m -= 0.07

    # Right: Disponibilidad Transaccional (La verdad de SRE)
    b_right = patches.FancyBboxPatch((0.52, 0.12), 0.42, 0.70, boxstyle="round,pad=0.02",
                                     facecolor=CARD_BG, edgecolor=MINT, linewidth=2)
    ax.add_patch(b_right)
    ax.text(0.73, 0.76, "[METRICA SRE] TASA DE ÉXITO DE NEGOCIO\n'Transacciones válidas completadas'",
            color=MINT, fontsize=12, fontweight='bold', ha='center')

    sre_points = [
        "+ Medición de 'Good Requests / Total Valid Requests'",
        "+ Telemetría end-to-end: del login a la persistencia",
        "+ Alerta inmediata si el volumen de pagos cae un 3%",
        "+ Detección de 'fallos silenciosos' en menos de 60s",
        "+ Visibilidad 100% veraz para el Comité de Dirección",
        "+ Respeto riguroso de Error Budget y SLAs de negocio",
        "+ Cumplimiento proactivo con la regulación europea DORA"
    ]
    y_s = 0.64
    for pt in sre_points:
        ax.text(0.55, y_s, pt, color=TEXT_COLOR, fontsize=9.2)
        y_s -= 0.07

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    path = os.path.join(output_dir, "bbva_disponibilidad_real_vs_marketing.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

if __name__ == "__main__":
    make_two_banks_diagram()
    make_mttr_pipeline_diagram()
    make_availability_pyramid_diagram()
    print("All BBVA MTBF vs MTTR diagrams generated successfully!")
