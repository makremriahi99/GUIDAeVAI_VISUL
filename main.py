import os
import sys
from scraper import get_play_store_reviews, get_app_store_reviews
from analyzer import run_analysis
from report_generator import load_analysis, generate_report
import json

def print_step(numero, titolo):
    print(f"\n{'='*50}")
    print(f"  STEP {numero}: {titolo}")
    print(f"{'='*50}")

def main():
    print("\n🚀 TOOL ANALISI RECENSIONI — Guida e Vai")
    print("=========================================")

    # ── STEP 1: SCRAPING ──────────────────────────────────
    print_step(1, "RACCOLTA RECENSIONI")

    print("\n📱 Google Play Store...")
    play_reviews = get_play_store_reviews(200)
    print(f"   → {len(play_reviews)} recensioni raccolte")

    # print("🍎 App Store...")
    # apple_reviews = get_app_store_reviews(200)
    # print(f"   → {len(apple_reviews)} recensioni raccolte")
    apple_reviews = []  # Temporaneamente disabilitato a causa di problemi con la libreria

    all_reviews = play_reviews + apple_reviews

    os.makedirs("output", exist_ok=True)
    with open("output/reviews.json", "w", encoding="utf-8") as f:
        json.dump(all_reviews, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Totale: {len(all_reviews)} recensioni salvate in output/reviews.json")

    # ── STEP 2: ANALISI ───────────────────────────────────
    print_step(2, "ANALISI CON AI")

    analysis = run_analysis(reviews=all_reviews)

    with open("output/analysis_result.json", "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print("✅ Analisi salvata in output/analysis_result.json")

    # ── STEP 3: REPORT HTML ───────────────────────────────
    print_step(3, "GENERAZIONE REPORT")

    generate_report(analysis)

    print("✅ Report salvato in output/report.html")

    # ── RIEPILOGO FINALE ──────────────────────────────────
    print(f"\n{'='*50}")
    print("  ✅ TUTTO COMPLETATO")
    print(f"{'='*50}")
    print(f"\n📊 Recensioni analizzate : {len(all_reviews)}")
    print(f"⭐ Rating medio          : {analysis.get('rating_medio', 'N/A')}")
    print(f"🔴 Problemi trovati      : {len(analysis.get('top5_problemi', []))}")
    print(f"💡 Suggerimenti generati : {len(analysis.get('suggerimenti_prodotto', []))}")
    print(f"\n📁 Output nella cartella /output/")
    print(f"   → reviews.json")
    print(f"   → analysis_result.json")
    print(f"   → report.html  ← apri questo nel browser\n")

if __name__ == "__main__":
    main()