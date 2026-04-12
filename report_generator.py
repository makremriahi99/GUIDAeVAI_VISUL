import json
import os
from jinja2 import Template
from datetime import datetime

def load_analysis(filepath="analysis_result.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_report(data):
    # Carica template branded da file esterno
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template_report.html")
    with open(template_path, "r", encoding="utf-8") as tpl_file:
        template_str = tpl_file.read()

    # --- Calcolo variabili aggiuntive per il template branded ---
    sentiment = data.get("sentiment_per_tema", {})

    # Label leggibili per i temi
    tema_labels = {
        "bug_tecnici": "Bug Tecnici",
        "ux_design": "UX / Design",
        "contenuti_quiz": "Contenuti Quiz",
        "performance": "Performance",
        "soddisfazione_generale": "Soddisfazione",
    }

    # Dati sentiment pre-calcolati per il template
    temi_sentiment = []
    tema_critico_nome = ""
    tema_critico_perc = 0

    for key, valori in sentiment.items():
        tot = valori["positivo"] + valori["negativo"]
        if tot == 0:
            continue
        pct_pos = round(valori["positivo"] / tot * 100)
        pct_neg = round(valori["negativo"] / tot * 100)
        pct_neu = 100 - pct_pos - pct_neg

        temi_sentiment.append({
            "label": tema_labels.get(key, key.replace("_", " ").title()),
            "pct_pos": pct_pos,
            "pct_neu": pct_neu,
            "pct_neg": pct_neg,
        })

        if pct_neg > tema_critico_perc:
            tema_critico_perc = pct_neg
            tema_critico_nome = tema_labels.get(key, key.replace("_", " ").title())

    # Percentuale positiva globale (dalla soddisfazione generale)
    sodd = sentiment.get("soddisfazione_generale", {})
    tot_sodd = sodd.get("positivo", 0) + sodd.get("negativo", 0)
    perc_positive = round(sodd["positivo"] / tot_sodd * 100, 1) if tot_sodd > 0 else 0

    # Stelline visuali
    rating = data.get("rating_medio", 0)
    stelle_piene = int(round(rating))
    stelle = chr(9733) * stelle_piene + chr(9734) * (5 - stelle_piene)

    now = datetime.now()

    template = Template(template_str)

    html = template.render(
        data_generazione=now.strftime("%d/%m/%Y %H:%M"),
        mese_anno=now.strftime("%B %Y").capitalize(),
        totale=data.get("totale_recensioni_analizzate", 0),
        rating_medio=data.get("rating_medio", 0),
        stelle=stelle,
        perc_positive=perc_positive,
        tema_critico_nome=tema_critico_nome,
        tema_critico_perc=tema_critico_perc,
        temi_sentiment=temi_sentiment,
        problemi=data.get("top5_problemi", []),
        forze=data.get("top3_punti_forza", []),
        suggerimenti=data.get("suggerimenti_prodotto", []),
    )

    with open("output/report.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Report branded generato -> output/report.html")

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    data = load_analysis()
    generate_report(data)