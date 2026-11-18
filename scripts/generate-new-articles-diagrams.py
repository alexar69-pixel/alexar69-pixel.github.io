import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

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

# ==============================================================================
# 1. WAR ROOM DE 14 HORAS: CRONOLOGÍA Y GOBERNANZA DE CRISIS
# ==============================================================================
def make_war_room_diagram():
    fig, ax = plt.subplots(figsize=(14, 7.875), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    ax.text(0.5, 0.94, "ANATOMIA DE UNA WAR ROOM CRITICA DE 14 HORAS (INCIDENT COMMAND)",
            color=AMBER, fontsize=17, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "Como proteger el foco tecnico del ruido directivo y mitigar el colapso bajo niebla de guerra",
            color=TEXT_COLOR, fontsize=11, ha='center', va='center')

    # Top: Flow steps
    steps = [
        ("T0: 02:14h\nALERTA P1", "Disparo de latencia\ny caida transaccional.", RED),
        ("T+15m\nWAR ROOM", "Incident Commander toma el mando y bloquea ruido.", CYAN),
        ("T+2h\nNIEBLA TOTAL", "Directivos entran pidiendo ETA; IC los deriva al comite.", AMBER),
        ("T+6h\nROLLBACK", "Hipotesis invalidada. Aislamiento de capas core.", YELLOW),
        ("T+11h\nESTABILIZACION", "Canary traffic 5% -> 100%. Mitigacion lograda.", MINT),
        ("T+24h\nBLAMELESS", "Causa raiz real identificada sin buscar culpables.", CYAN)
    ]

    card_w = 0.14
    card_h = 0.28
    y_card = 0.54
    for i, (title, desc, color) in enumerate(steps):
        x = 0.05 + i * 0.155
        card = patches.FancyBboxPatch((x, y_card), card_w, card_h, boxstyle="round,pad=0.015",
                                      facecolor=CARD_BG, edgecolor=color, linewidth=2)
        ax.add_patch(card)
        ax.text(x + card_w/2, y_card + card_h - 0.05, title, color=color, fontsize=10, fontweight='bold', ha='center')
        ax.text(x + card_w/2, y_card + card_h - 0.14, desc, color=TEXT_COLOR, fontsize=8.5, ha='center', wrap=True)
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + card_w + 0.015, y_card + card_h/2), xytext=(x + card_w, y_card + card_h/2),
                        arrowprops=dict(arrowstyle="->", color=MUTED_COLOR, lw=2))

    # Bottom: 2 comparison boxes
    # Left: Ruido destructivo
    box_bad = patches.FancyBboxPatch((0.05, 0.08), 0.435, 0.38, boxstyle="round,pad=0.015",
                                     facecolor=CARD_BG, edgecolor=RED, linewidth=1.8)
    ax.add_patch(box_bad)
    ax.text(0.2675, 0.42, "[ANTIPATRON] LA WAR ROOM CAOTICA", color=RED, fontsize=11.5, fontweight='bold', ha='center')
    bad_items = [
        "- 40 personas hablando a la vez en la llamada.",
        "- Directores preguntando cada 10 minutos '¿para cuándo está?'.",
        "- Ingenieros intentando parches improvisados en caliente sobre producción.",
        "- Fatiga cognitiva severa y toma de decisiones impulsivas.",
        "- Busqueda prematura de 'quien toco el cambio'."
    ]
    y_b = 0.36
    for it in bad_items:
        ax.text(0.07, y_b, it, color=TEXT_COLOR, fontsize=9.2)
        y_b -= 0.055

    # Right: Incident Commander profesional
    box_good = patches.FancyBboxPatch((0.515, 0.08), 0.435, 0.38, boxstyle="round,pad=0.015",
                                      facecolor=CARD_BG, edgecolor=MINT, linewidth=1.8)
    ax.add_patch(box_good)
    ax.text(0.7325, 0.42, "[PATRON SRE] GOBERNANZA INCIDENT COMMAND", color=MINT, fontsize=11.5, fontweight='bold', ha='center')
    good_items = [
        "+ Una sola voz de mando (Incident Commander) gestiona el flujo.",
        "+ Canal separado para directivos con updates regulares cada 30 min.",
        "+ Ingenieros en silencio concentrados en una hipotesis a la vez.",
        "+ Rotacion obligatoria de guardias cada 6 horas para evitar errores.",
        "+ Enfoque absoluto en mitigar impacto antes de buscar causa raiz."
    ]
    y_g = 0.36
    for it in good_items:
        ax.text(0.535, y_g, it, color=TEXT_COLOR, fontsize=9.2)
        y_g -= 0.055

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    path = os.path.join(output_dir, "anatomia-de-una-war-room-14-horas-incident-management.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ==============================================================================
# 2. MONOCULTURA Y BLAST RADIUS (CROWDSTRIKE & CLOUD)
# ==============================================================================
def make_monoculture_diagram():
    fig, ax = plt.subplots(figsize=(14, 7.875), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    ax.text(0.5, 0.94, "LA TRAMPA DE LA MONOCULTURA TECNOLOGICA: RADIO DE IMPACTO GLOBAL",
            color=CYAN, fontsize=17, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "Por que la redundancia identica no es resiliencia: lecciones del caso CrowdStrike a la nube",
            color=TEXT_COLOR, fontsize=11, ha='center', va='center')

    # Left: Monocultura (Single point of failure)
    box_mono = patches.FancyBboxPatch((0.06, 0.12), 0.42, 0.70, boxstyle="round,pad=0.02",
                                      facecolor=CARD_BG, edgecolor=RED, linewidth=2)
    ax.add_patch(box_mono)
    ax.text(0.27, 0.76, "[FRAGIL] MONOCULTURA GLOBAL", color=RED, fontsize=13, fontweight='bold', ha='center')
    ax.text(0.27, 0.71, "El mismo agente / OS / Cloud en el 100% de la flota", color=MUTED_COLOR, fontsize=9.5, ha='center')

    # Visual representation: all nodes fail simultaneously
    ax.text(0.27, 0.58, "DESPLIEGUE GLOBAL INSTANTANEO", color=YELLOW, fontsize=10, fontweight='bold', ha='center')
    ax.annotate("", xy=(0.27, 0.48), xytext=(0.27, 0.55), arrowprops=dict(arrowstyle="->", color=RED, lw=3))
    
    # 5 nodes in red
    for i in range(5):
        cx = 0.11 + i * 0.08
        circle = patches.Circle((cx, 0.42), 0.025, facecolor=RED)
        ax.add_patch(circle)
        ax.text(cx, 0.42, "BSOD", color="#fff", fontsize=7.5, fontweight='bold', ha='center', va='center')

    mono_points = [
        "- Un solo archivo de configuracion corrompido",
        "- Actualizacion 'Big Bang' a 8.5 millones de endpoints",
        "- Redundancia inutil: replicas con identico defecto",
        "- MTTR de semanas: recuperacion manual presencial",
        "- Blast Radius = 100% de la infraestructura"
    ]
    y_m = 0.34
    for pt in mono_points:
        ax.text(0.09, y_m, pt, color=TEXT_COLOR, fontsize=9.5)
        y_m -= 0.055

    # Right: Arquitectura Celular y Canario (Resilience)
    box_cell = patches.FancyBboxPatch((0.52, 0.12), 0.42, 0.70, boxstyle="round,pad=0.02",
                                      facecolor=CARD_BG, edgecolor=MINT, linewidth=2)
    ax.add_patch(box_cell)
    ax.text(0.73, 0.76, "[RESILIENTE] ARQUITECTURA CELULAR & CANARY", color=MINT, fontsize=13, fontweight='bold', ha='center')
    ax.text(0.73, 0.71, "Aislamiento de fallo y despliegue por fases graduadas", color=MUTED_COLOR, fontsize=9.5, ha='center')

    ax.text(0.73, 0.58, "CANARY PROGRESSIVE ROLLOUT", color=CYAN, fontsize=10, fontweight='bold', ha='center')
    ax.annotate("", xy=(0.73, 0.48), xytext=(0.73, 0.55), arrowprops=dict(arrowstyle="->", color=MINT, lw=3))

    # 5 nodes: 1 red, 4 mint
    for i in range(5):
        cx = 0.57 + i * 0.08
        color = RED if i == 0 else MINT
        txt = "HALT" if i == 0 else "OK"
        circle = patches.Circle((cx, 0.42), 0.025, facecolor=color)
        ax.add_patch(circle)
        ax.text(cx, 0.42, txt, color="#fff", fontsize=7.5, fontweight='bold', ha='center', va='center')

    cell_points = [
        "+ Despliegue en 1% -> 5% con monitoreo automatico",
        "+ Deteccion instantanea de kernel panic y freno automatico",
        "+ Diversidad de arquitecturas y proveedores secundarios",
        "+ El 99% de la flota permanece intacta y operativa",
        "+ Blast Radius contenido = Incidente menor aislado"
    ]
    y_c = 0.34
    for pt in cell_points:
        ax.text(0.55, y_c, pt, color=TEXT_COLOR, fontsize=9.5)
        y_c -= 0.055

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    path = os.path.join(output_dir, "la-trampa-de-la-monocultura-del-caso-crowdstrike-a-la-fragilidad-cloud.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ==============================================================================
# 3. AGENTES DE IA EN SRE (AUTONOMIA VS HUMAN-IN-THE-LOOP)
# ==============================================================================
def make_ai_sre_diagram():
    fig, ax = plt.subplots(figsize=(14, 7.875), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    ax.text(0.5, 0.94, "NIVELES DE AUTONOMIA PARA AGENTES DE IA EN OPERACIONES CRITICAS (SRE)",
            color=MINT, fontsize=17, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "Del analisis pasivo a la remediacion autonoma: limites de seguridad y Circuit Breakers",
            color=TEXT_COLOR, fontsize=11, ha='center', va='center')

    levels = [
        {
            "lvl": "NIVEL 1",
            "name": "OBSERVABILIDAD\nAGÉNTICA",
            "role": "Sintesis y Alertas",
            "actions": "• Agrupa millones de logs.\n• Detecta anomalias sutiles.\n• Cero accion destructiva.",
            "risk": "RIESGO: CERO",
            "color": CYAN
        },
        {
            "lvl": "NIVEL 2",
            "name": "DIAGNÓSTICO &\nRECOMENDACIÓN",
            "role": "Asesor de Guardia",
            "actions": "• Correlaciona trazas.\n• Sugiere 3 hipotesis probables.\n• Prepara comandos en borrador.",
            "risk": "RIESGO: MUY BAJO",
            "color": MINT
        },
        {
            "lvl": "NIVEL 3",
            "name": "CO-PILOTO CON\nHUMAN-IN-THE-LOOP",
            "role": "Ejecución Supervisada",
            "actions": "• El agente propone el rollback.\n• Requiere confirmacion humana.\n• Valida telemetria posterior.",
            "risk": "ESTÁNDAR SEGURO 2026",
            "color": AMBER
        },
        {
            "lvl": "NIVEL 4",
            "name": "REMEDIACIÓN\nAUTÓNOMA ACOTADA",
            "role": "Acción Independiente",
            "actions": "• Rollback automatico con Circuit Breakers estrictos.\n• Limites de gasto y radio de impacto.",
            "risk": "SOLO EN ESCENARIOS HOMOLOGADOS",
            "color": RED
        }
    ]

    card_w = 0.205
    card_h = 0.65
    y_card = 0.16

    for i, lv in enumerate(levels):
        x = 0.05 + i * 0.235
        card = patches.FancyBboxPatch((x, y_card), card_w, card_h, boxstyle="round,pad=0.015",
                                      facecolor=CARD_BG, edgecolor=lv["color"], linewidth=2)
        ax.add_patch(card)

        # Level tag
        tag_box = patches.FancyBboxPatch((x + 0.02, y_card + card_h - 0.07), card_w - 0.04, 0.045, boxstyle="round,pad=0.008",
                                         facecolor="#181938", edgecolor=lv["color"], linewidth=1.2)
        ax.add_patch(tag_box)
        ax.text(x + card_w/2, y_card + card_h - 0.0475, lv["lvl"], color=lv["color"], fontsize=10, fontweight='bold', ha='center', va='center')

        # Title
        ax.text(x + card_w/2, y_card + card_h - 0.14, lv["name"], color=TEXT_COLOR, fontsize=11, fontweight='bold', ha='center', va='center')
        ax.text(x + card_w/2, y_card + card_h - 0.20, f"Rol: {lv['role']}", color=lv["color"], fontsize=9.5, ha='center')

        # Actions
        ax.text(x + 0.015, y_card + card_h - 0.26, lv["actions"], color=TEXT_COLOR, fontsize=9.2, va='top')

        # Risk badge at bottom
        badge = patches.FancyBboxPatch((x + 0.015, y_card + 0.03), card_w - 0.03, 0.05, boxstyle="round,pad=0.008",
                                       facecolor="#121326", edgecolor=lv["color"], linewidth=1.2)
        ax.add_patch(badge)
        ax.text(x + card_w/2, y_card + 0.055, lv["risk"], color=lv["color"], fontsize=8, fontweight='bold', ha='center', va='center')

        if i < len(levels) - 1:
            arrow_x = x + card_w + 0.005
            ax.annotate("", xy=(arrow_x + 0.02, y_card + card_h/2), xytext=(arrow_x, y_card + card_h/2),
                        arrowprops=dict(arrowstyle="->", color=MUTED_COLOR, lw=2.5))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    path = os.path.join(output_dir, "agentes-ia-en-produccion-remediacion-autonoma-sre.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

# ==============================================================================
# 4. RESILIENCE SCORECARD Y BLAMELESS POST-MORTEM
# ==============================================================================
def make_scorecard_diagram():
    fig, ax = plt.subplots(figsize=(14, 7.875), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    ax.text(0.5, 0.94, "EL RESILIENCE SCORECARD: LOS 5 PILARES DE LA INFRAESTRUCTURA INQUEBRANTABLE",
            color=YELLOW, fontsize=17, fontweight='bold', ha='center', va='center')
    ax.text(0.5, 0.88, "Marco de autoevaluacion tecnica para CTOs, Arquitectos y Lideres de Operaciones",
            color=TEXT_COLOR, fontsize=11, ha='center', va='center')

    pillars = [
        ("1. BLAST RADIUS", "Aislamiento de Fallo", "• Particionado celular estanco.\n• Despliegues Canario graduados.\n• Caida de un nodo nunca tumba al cluster.", CYAN),
        ("2. FAIL-SAFE", "Seguridad por Defecto", "• Degradacion elegante probada.\n• Ante perdida de senal, estado seguro.\n• Parada automatica ante la duda.", RED),
        ("3. PROTOCOLO ANDON", "Cultura Sin Miedo", "• Maquinista o dev frena la marcha.\n• Respaldo directivo a la parada.\n• Cero represalias por retraso.", AMBER),
        ("4. ERROR BUDGETS", "Gobernanza de Riesgo", "• Margen de error publico en el SLA.\n• Congelacion automatica de features.\n• Todo el foco a la fiabilidad.", MINT),
        ("5. BLAMELESS POST", "Aprendizaje Sistémico", "• Investigacion de incentivos.\n• Desterrar el 'error humano'.\n• 5 Porques y accion correctiva.", YELLOW)
    ]

    card_w = 0.17
    card_h = 0.65
    y_card = 0.16

    for i, (name, subtitle, desc, col) in enumerate(pillars):
        x = 0.04 + i * 0.19
        card = patches.FancyBboxPatch((x, y_card), card_w, card_h, boxstyle="round,pad=0.015",
                                      facecolor=CARD_BG, edgecolor=col, linewidth=2)
        ax.add_patch(card)

        # Header badge
        badge = patches.FancyBboxPatch((x + 0.015, y_card + card_h - 0.07), card_w - 0.03, 0.045, boxstyle="round,pad=0.008",
                                       facecolor="#181938", edgecolor=col, linewidth=1.2)
        ax.add_patch(badge)
        ax.text(x + card_w/2, y_card + card_h - 0.0475, name, color=col, fontsize=9.5, fontweight='bold', ha='center', va='center')

        ax.text(x + card_w/2, y_card + card_h - 0.13, subtitle, color=TEXT_COLOR, fontsize=10.5, fontweight='bold', ha='center')
        ax.text(x + 0.015, y_card + card_h - 0.22, desc, color=TEXT_COLOR, fontsize=9, va='top')

        # Score rating placeholder
        score_box = patches.FancyBboxPatch((x + 0.015, y_card + 0.03), card_w - 0.03, 0.07, boxstyle="round,pad=0.008",
                                           facecolor="#101124", edgecolor=col, linewidth=1)
        ax.add_patch(score_box)
        ax.text(x + card_w/2, y_card + 0.065, "Nivel de Madurez:\n[ 1  2  3  4  5 ]", color=col, fontsize=8, ha='center', va='center')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    path = os.path.join(output_dir, "resilience-scorecard-plantilla-blameless-post-mortem.png")
    plt.tight_layout()
    plt.savefig(path, dpi=180, facecolor=BG_COLOR)
    plt.close()
    print(f"Generated: {path}")

if __name__ == "__main__":
    make_war_room_diagram()
    make_monoculture_diagram()
    make_ai_sre_diagram()
    make_scorecard_diagram()
    print("All 4 hero diagrams generated successfully!")

