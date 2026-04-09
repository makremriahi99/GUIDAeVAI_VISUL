import json
from jinja2 import Template
from datetime import datetime

def load_analysis(filepath="analysis_result.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_report(data):
    template_str = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report Recensioni — Quiz Patente Guida e Vai</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', sans-serif;
            background: #f4f6f9;
            color: #1a1a2e;
        }

        header {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: white;
            padding: 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        header h1 { font-size: 1.8rem; }
        header p  { opacity: 0.7; margin-top: 6px; font-size: 0.9rem; }

        .badge {
            background: #e94560;
            padding: 10px 20px;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .container { max-width: 1100px; margin: 0 auto; padding: 40px 20px; }

        /* ── KPI ── */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 40px;
        }

        .kpi-card {
            background: white;
            border-radius: 16px;
            padding: 28px;
            text-align: center;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }

        .kpi-card .number {
            font-size: 2.8rem;
            font-weight: 700;
            color: #e94560;
        }

        .kpi-card .label {
            font-size: 0.85rem;
            color: #666;
            margin-top: 6px;
        }

        /* ── SEZIONI ── */
        .section {
            background: white;
            border-radius: 16px;
            padding: 32px;
            margin-bottom: 28px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }

        .section h2 {
            font-size: 1.2rem;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .section h2 .icon {
            width: 36px; height: 36px;
            background: #f0f4ff;
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.1rem;
        }

        /* ── SENTIMENT TEMI ── */
        .tema-row {
            margin-bottom: 18px;
        }

        .tema-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 0.9rem;
        }

        .tema-name { font-weight: 600; text-transform: capitalize; }

        .bar-container {
            background: #f0f0f0;
            border-radius: 50px;
            height: 10px;
            overflow: hidden;
            display: flex;
        }

        .bar-pos { background: #2ecc71; height: 100%; transition: width 0.5s; }
        .bar-neg { background: #e94560; height: 100%; transition: width 0.5s; }

        .tema-sintesi {
            font-size: 0.8rem;
            color: #888;
            margin-top: 6px;
            font-style: italic;
        }

        /* ── PROBLEMI ── */
        .problema-card {
            display: flex;
            gap: 16px;
            align-items: flex-start;
            padding: 16px 0;
            border-bottom: 1px solid #f0f0f0;
        }

        .problema-card:last-child { border-bottom: none; }

        .rank-badge {
            min-width: 36px; height: 36px;
            border-radius: 50%;
            background: #e94560;
            color: white;
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; font-size: 0.9rem;
        }

        .problema-body h3 { font-size: 0.95rem; margin-bottom: 4px; }

        .problema-body .citazione {
            font-size: 0.82rem;
            color: #888;
            font-style: italic;
        }

        .impatto {
            margin-left: auto;
            padding: 4px 12px;
            border-radius: 50px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .impatto.alto   { background: #fde8ec; color: #e94560; }
        .impatto.medio  { background: #fff3e0; color: #e67e22; }
        .impatto.basso  { background: #e8f5e9; color: #27ae60; }

        /* ── PUNTI DI FORZA ── */
        .forza-card {
            display: flex;
            gap: 16px;
            padding: 16px 0;
            border-bottom: 1px solid #f0f0f0;
            align-items: flex-start;
        }

        .forza-card:last-child { border-bottom: none; }

        .forza-icon {
            min-width: 36px; height: 36px;
            border-radius: 50%;
            background: #e8f5e9;
            color: #27ae60;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.1rem;
        }

        .forza-body h3 { font-size: 0.95rem; margin-bottom: 4px; }
        .forza-body .citazione { font-size: 0.82rem; color: #888; font-style: italic; }

        /* ── SUGGERIMENTI ── */
        .suggerimento-card {
            border-left: 4px solid #e94560;
            padding: 16px 20px;
            margin-bottom: 16px;
            background: #fafafa;
            border-radius: 0 12px 12px 0;
        }

        .suggerimento-card .priorita {
            font-size: 0.75rem;
            color: #e94560;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }

        .suggerimento-card h3 { font-size: 0.95rem; margin-bottom: 6px; }

        .suggerimento-card p {
            font-size: 0.85rem;
            color: #555;
            margin-bottom: 4px;
        }

        .suggerimento-card .impatto-atteso {
            font-size: 0.8rem;
            color: #27ae60;
            font-weight: 600;
        }

        /* ── FOOTER ── */
        footer {
            text-align: center;
            padding: 30px;
            color: #aaa;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>

<header>
    <div>
        <h1>📊 Report Analisi Recensioni</h1>
        <p>Quiz Patente Ufficiale — Guida e Vai &nbsp;|&nbsp; Generato il {{ data_generazione }}</p>
    </div>
    <div class="badge">{{ totale }} recensioni analizzate</div>
</header>

<div class="container">

    <!-- KPI -->
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="number">{{ rating_medio }}</div>
            <div class="label">⭐ Rating medio (su 5)</div>
        </div>
        <div class="kpi-card">
            <div class="number">{{ totale }}</div>
            <div class="label">📝 Recensioni analizzate</div>
        </div>
        <div class="kpi-card">
            <div class="number">{{ n_problemi }}</div>
            <div class="label">🔴 Problemi identificati</div>
        </div>
    </div>

    <!-- SENTIMENT PER TEMA -->
    <div class="section">
        <h2><span class="icon">📈</span> Sentiment per Tema</h2>
        {% for tema, valori in sentiment.items() %}
        {% set totale_tema = valori.positivo + valori.negativo %}
        {% set perc_pos = ((valori.positivo / totale_tema) * 100)|round if totale_tema > 0 else 0 %}
        {% set perc_neg = 100 - perc_pos %}
        <div class="tema-row">
            <div class="tema-header">
                <span class="tema-name">{{ tema.replace('_', ' ') }}</span>
                <span style="color:#888; font-size:0.82rem;">
                    ✅ {{ valori.positivo }} positivi &nbsp;|&nbsp; ❌ {{ valori.negativo }} negativi
                </span>
            </div>
            <div class="bar-container">
                <div class="bar-pos" style="width: {{ perc_pos }}%"></div>
                <div class="bar-neg" style="width: {{ perc_neg }}%"></div>
            </div>
            {% if valori.sintesi %}
            <div class="tema-sintesi">{{ valori.sintesi }}</div>
            {% endif %}
        </div>
        {% endfor %}
    </div>

    <!-- TOP 5 PROBLEMI -->
    <div class="section">
        <h2><span class="icon">🔴</span> Top 5 Problemi Ricorrenti</h2>
        {% for p in problemi %}
        <div class="problema-card">
            <div class="rank-badge">{{ p.rank }}</div>
            <div class="problema-body">
                <h3>{{ p.problema }}</h3>
                <div class="citazione">"{{ p.citazione }}"</div>
            </div>
            <div class="impatto {{ p.impatto }}">{{ p.impatto|upper }}</div>
        </div>
        {% endfor %}
    </div>

    <!-- TOP 3 PUNTI DI FORZA -->
    <div class="section">
        <h2><span class="icon">✅</span> Top 3 Punti di Forza</h2>
        {% for f in forze %}
        <div class="forza-card">
            <div class="forza-icon">⭐</div>
            <div class="forza-body">
                <h3>{{ f.forza }}</h3>
                <div class="citazione">"{{ f.citazione }}"</div>
            </div>
        </div>
        {% endfor %}
    </div>

    <!-- SUGGERIMENTI PRODOTTO -->
    <div class="section">
        <h2><span class="icon">💡</span> Suggerimenti per il Product Manager</h2>
        {% for s in suggerimenti %}
        <div class="suggerimento-card">
            <div class="priorita">Priorità {{ s.priorita }}</div>
            <h3>{{ s.azione }}</h3>
            <p>{{ s.motivazione }}</p>
            <div class="impatto-atteso">→ {{ s.impatto_atteso }}</div>
        </div>
        {% endfor %}
    </div>

</div>

<footer>
    Report generato automaticamente · {{ data_generazione }} · Dati da App Store e Google Play
</footer>

</body>
</html>
"""

    template = Template(template_str)

    html = template.render(
        data_generazione=datetime.now().strftime("%d/%m/%Y %H:%M"),
        totale=data.get("totale_recensioni_analizzate", 0),
        rating_medio=data.get("rating_medio", 0),
        n_problemi=len(data.get("top5_problemi", [])),
        sentiment=data.get("sentiment_per_tema", {}),
        problemi=data.get("top5_problemi", []),
        forze=data.get("top3_punti_forza", []),
        suggerimenti=data.get("suggerimenti_prodotto", [])
    )

    with open("output/report.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ Report generato → output/report.html")

if __name__ == "__main__":
    import os
    os.makedirs("output", exist_ok=True)
    data = load_analysis()
    generate_report(data)