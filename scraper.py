from google_play_scraper import reviews, Sort
import json
from datetime import datetime

# ── GOOGLE PLAY ──────────────────────────────────────────
def get_play_store_reviews(count=200):
    result, _ = reviews(
        'com.bokapp.quizpatente',
        lang='it',
        country='it',
        sort=Sort.NEWEST,
        count=count
    )
    cleaned = []
    for r in result:
        cleaned.append({
            "source": "Google Play",
            "rating": r["score"],
            "text": r["content"],
            "date": r["at"].strftime("%Y-%m-%d")
        })
    return cleaned

# ── APP STORE ─────────────────────────────────────────────
def get_app_store_reviews(count=200):
    # Temporaneamente disabilitato a causa di problemi con le librerie disponibili
    # Le librerie esistenti sono obsolete e non compatibili con l'API attuale di Apple
    return []

# ── SALVA TUTTO ───────────────────────────────────────────
if __name__ == "__main__":
    print("Scaricando recensioni Google Play...")
    play = get_play_store_reviews(400)
    
    print("Scaricando recensioni App Store...")
    apple = get_app_store_reviews(400)
    
    all_reviews = play + apple
    
    with open("reviews.json", "w", encoding="utf-8") as f:
        json.dump(all_reviews, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Salvate {len(all_reviews)} recensioni in reviews.json")
    print(f"   → Google Play: {len(play)}")
    print(f"   → App Store:   {len(apple)}")