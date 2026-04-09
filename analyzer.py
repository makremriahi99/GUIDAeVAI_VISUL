import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ── CARICA RECENSIONI ─────────────────────────────────────
def load_reviews(filepath="reviews.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# ── DIVIDI IN BATCH ───────────────────────────────────────
def chunk_reviews(reviews, batch_size=50):
    for i in range(0, len(reviews), batch_size):
        yield reviews[i:i + batch_size]

# ── ANALIZZA UN SINGOLO BATCH ─────────────────────────────
def analyze_batch(batch):
    testo_recensioni = ""
    for r in batch:
        testo_recensioni += f"[{r['source']} - {r['rating']}⭐ - {r['date']}]\n{r['text']}\n\n"

    prompt = f"""
Sei un analista di prodotto. Analizza queste recensioni di un'app per la preparazione all'esame della patente italiana.

RECENSIONI:
{testo_recensioni}

Rispondi SOLO con un JSON valido, senza testo aggiuntivo, con questa struttura esatta:
{{
  "sentiment_per_tema": {{
    "bug_tecnici": {{"positivo": 0, "negativo": 0, "esempi": []}},
    "ux_design": {{"positivo": 0, "negativo": 0, "esempi": []}},
    "contenuti_quiz": {{"positivo": 0, "negativo": 0, "esempi": []}},
    "performance": {{"positivo": 0, "negativo": 0, "esempi": []}},
    "soddisfazione_generale": {{"positivo": 0, "negativo": 0, "esempi": []}}
  }},
  "problemi": [
    {{"problema": "descrizione", "frequenza": 0, "citazione_esempio": "testo"}}
  ],
  "punti_di_forza": [
    {{"forza": "descrizione", "frequenza": 0, "citazione_esempio": "testo"}}
  ]
}}
"""
    message = client.chat.completions.create(
    model="gpt-4o-mini",  # economico e bravissimo per questo task
    max_tokens=2000,
    messages=[{"role": "user", "content": prompt}]
)
    testo = message.choices[0].message.content.strip()
    # rimuovi eventuali backtick se il modello li aggiunge
    testo = testo.replace("```json", "").replace("```", "").strip()
    return json.loads(testo)

# ── AGGREGA TUTTI I BATCH ─────────────────────────────────
def aggregate_results(batch_results):
    temi = ["bug_tecnici", "ux_design", "contenuti_quiz", "performance", "soddisfazione_generale"]
    
    aggregato = {
        "sentiment_per_tema": {t: {"positivo": 0, "negativo": 0, "esempi": []} for t in temi},
        "tutti_problemi": [],
        "tutti_punti_forza": []
    }

    for result in batch_results:
        # aggrega sentiment
        for tema in temi:
            if tema in result.get("sentiment_per_tema", {}):
                aggregato["sentiment_per_tema"][tema]["positivo"] += result["sentiment_per_tema"][tema]["positivo"]
                aggregato["sentiment_per_tema"][tema]["negativo"] += result["sentiment_per_tema"][tema]["negativo"]
                esempi = result["sentiment_per_tema"][tema].get("esempi", [])
                aggregato["sentiment_per_tema"][tema]["esempi"].extend(esempi[:1])  # 1 esempio per batch

        # accumula problemi e forze
        aggregato["tutti_problemi"].extend(result.get("problemi", []))
        aggregato["tutti_punti_forza"].extend(result.get("punti_di_forza", []))

    return aggregato

# ── SECONDO PASSAGGIO: SINTESI FINALE ─────────────────────
def final_synthesis(aggregato):
    prompt = f"""
Sei un analista di prodotto senior. Hai analizzato centinaia di recensioni di un'app patente italiana.
Ecco i dati aggregati da tutti i batch:

SENTIMENT PER TEMA:
{json.dumps(aggregato["sentiment_per_tema"], ensure_ascii=False, indent=2)}

PROBLEMI RILEVATI (da tutti i batch):
{json.dumps(aggregato["tutti_problemi"], ensure_ascii=False, indent=2)}

PUNTI DI FORZA RILEVATI (da tutti i batch):
{json.dumps(aggregato["tutti_punti_forza"], ensure_ascii=False, indent=2)}

Produci un'analisi finale. Rispondi SOLO con JSON valido:
{{
  "sentiment_per_tema": {{
    "bug_tecnici": {{"positivo": 0, "negativo": 0, "sintesi": ""}},
    "ux_design": {{"positivo": 0, "negativo": 0, "sintesi": ""}},
    "contenuti_quiz": {{"positivo": 0, "negativo": 0, "sintesi": ""}},
    "performance": {{"positivo": 0, "negativo": 0, "sintesi": ""}},
    "soddisfazione_generale": {{"positivo": 0, "negativo": 0, "sintesi": ""}}
  }},
  "top5_problemi": [
    {{"rank": 1, "problema": "", "impatto": "alto/medio/basso", "citazione": ""}}
  ],
  "top3_punti_forza": [
    {{"rank": 1, "forza": "", "citazione": ""}}
  ],
  "suggerimenti_prodotto": [
    {{"priorita": 1, "azione": "", "motivazione": "", "impatto_atteso": ""}}
  ],
  "rating_medio": 0.0,
  "totale_recensioni_analizzate": 0
}}
"""

    message = client.chat.completions.create(
    model="gpt-4o-mini",  # economico e bravissimo per questo task
    max_tokens=2000,
    messages=[{"role": "user", "content": prompt}]
)
    testo = message.choices[0].message.content.strip()
    testo = testo.replace("```json", "").replace("```", "").strip()
    return json.loads(testo)

# ── MAIN ──────────────────────────────────────────────────
def run_analysis(reviews=None):
    print("📂 Caricamento recensioni...")
    if reviews is None:
        reviews = load_reviews()
    print(f"   → {len(reviews)} recensioni caricate")

    # calcola rating medio
    rating_medio = sum(r["rating"] for r in reviews) / len(reviews)

    batch_results = []
    batches = list(chunk_reviews(reviews, batch_size=50))
    
    print(f"\n🔍 Analisi in corso ({len(batches)} batch da 50)...")
    for i, batch in enumerate(batches):
        print(f"   → Batch {i+1}/{len(batches)}...")
        result = analyze_batch(batch)
        batch_results.append(result)

    print("\n🔗 Aggregazione risultati...")
    aggregato = aggregate_results(batch_results)

    print("🧠 Sintesi finale con ChatGPT...")
    finale = final_synthesis(aggregato)
    finale["rating_medio"] = round(rating_medio, 2)
    finale["totale_recensioni_analizzate"] = len(reviews)

    with open("analysis_result.json", "w", encoding="utf-8") as f:
        json.dump(finale, f, ensure_ascii=False, indent=2)

    print("\n✅ Analisi completata → analysis_result.json")
    return finale

if __name__ == "__main__":
    run_analysis()