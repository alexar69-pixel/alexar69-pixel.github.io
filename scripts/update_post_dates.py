import json

date_mapping = {
    "gamedays-chaos-engineering-simulacion-caidas-banca": "2026-11-17",
    "adamuz-urda-kpis-seguridad-ave": "2026-11-10",
    "mttr-bancario-disponibilidad-gestion-incidencias-p1": "2026-10-28",
    "anatomia-de-una-war-room-14-horas-incident-management": "2026-10-14",
    "la-trampa-de-la-monocultura-del-caso-crowdstrike-a-la-fragilidad-cloud": "2026-09-22",
    "agentes-ia-en-produccion-remediacion-autonoma-sre": "2026-08-26",
    "resilience-scorecard-plantilla-blameless-post-mortem": "2026-07-29",
    "ia-y-resiliencia-en-sistemas-criticos-sre-2026": "2026-06-18"
}

with open("blog/data/posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

for p in posts:
    slug = p["slug"]
    if slug in date_mapping:
        p["date"] = date_mapping[slug]

# Sort posts descending by date
posts.sort(key=lambda x: x["date"], reverse=True)

with open("blog/data/posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Updated dates in blog/data/posts.json successfully. New order:")
for p in posts:
    print(f"  {p['date']} -> {p['slug']}")

