# 🚗 Tool Analisi Recensioni — Quiz Patente Guida e Vai

Pipeline automatizzata per raccogliere, analizzare con AI e visualizzare in un report branded le recensioni dell'app **Quiz Patente 2026** (`com.bokapp.quizpatente`) dal Google Play Store.

---

## ⚙️ Requisiti

- **Python 3.11+**
- Una **API key OpenAI** → [platform.openai.com](https://platform.openai.com)

---

## 🚀 Installazione

### 1. Clona il repository

```bash
git clone https://github.com/TUO-USERNAME/GUIDAeVAI_VISUL.git
cd GUIDAeVAI_VISUL
```

### 2. Installa le dipendenze

```bash
pip install -r requirements.txt
```

### 3. Configura la API key

Crea un file `.env` nella root del progetto:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

---

## ▶️ Utilizzo

Esegui tutto con un solo comando:

```bash
python main.py
```

Il tool eseguirà automaticamente 3 step in sequenza:

| Step | Azione | Dettaglio |
|------|--------|-----------|
| 1 | **Scraping** | Raccoglie le ultime 400 recensioni dal Google Play Store (lingua IT, ordinate per data) |
| 2 | **Analisi AI** | Invia le recensioni a GPT-4o-mini in batch da 50, classificando sentiment su 5 temi |
| 3 | **Report** | Genera un report HTML brandizzato Guida e Vai con grafici e raccomandazioni |

Al termine vengono stampate le statistiche principali: totale recensioni, rating medio, problemi trovati e suggerimenti generati.

---

## 📁 Output

Tutti i file vengono salvati nella cartella `output/`:

| File                  | Descrizione                                        |
|-----------------------|----------------------------------------------------|
| `reviews.json`        | Recensioni grezze (source, rating, text, date)     |
| `analysis_result.json`| Analisi strutturata: sentiment, problemi, punti di forza, suggerimenti |
| `report.html`         | Report finale brandizzato — aprire nel browser     |

---

## 📊 Cosa contiene il report

Il report HTML generato include:

- **KPI cards** — Rating medio, % recensioni positive, tema più critico
- **Sentiment per tema** — Barre orizzontali positive/neutre/negative per ognuno dei 5 temi analizzati:
  - Bug tecnici
  - UX Design
  - Contenuti quiz
  - Performance
  - Soddisfazione generale
- **Top 5 problemi** — Classificati per impatto con citazioni dirette dalle recensioni
- **Top 3 punti di forza** — I principali aspetti apprezzati dagli utenti
- **Raccomandazioni prodotto** — Suggerimenti prioritizzati (alta/media/bassa priorità)
- **Metodologia** — Descrizione dell'approccio analitico utilizzato

Un esempio di report già generato è disponibile in `output/report.html` — aprilo nel browser con doppio click.

---

## 🏗️ Struttura del progetto

```
GUIDAeVAI_VISUL/
├── main.py                # Entry point — orchestratore pipeline
├── scraper.py             # Raccolta recensioni da Google Play Store
├── analyzer.py            # Analisi AI con OpenAI (batch da 50 recensioni)
├── report_generator.py    # Generazione report HTML con Jinja2
├── template_report.html   # Template HTML brandizzato Guida e Vai
├── requirements.txt       # Dipendenze Python
├── .env                   # API key OpenAI (non committare!)
├── .gitignore
├── reviews.json           # Cache recensioni (root)
├── analysis_result.json   # Cache analisi (root)
└── output/
    ├── reviews.json
    ├── analysis_result.json
    └── report.html
```

---

## 🛠️ Stack tecnico

| Componente       | Tool / Libreria                          |
|------------------|------------------------------------------|
| Scraping         | `google-play-scraper` 1.2.7             |
| Analisi AI       | OpenAI `GPT-4o-mini`                    |
| Templating       | `Jinja2` 3.1.2                          |
| Variabili env    | `python-dotenv` 1.0.0                   |
| Report           | HTML/CSS custom (Plus Jakarta Sans, brand Guida e Vai) |
| Linguaggio       | Python 3.11+                            |

---

## ⚠️ Note

- Lo scraping del Google Play Store è basato su dati pubblici, nessuna API key necessaria
- Lo scraping dall'**App Store** è attualmente disabilitato per incompatibilità della libreria — il tool usa solo Google Play
- Il costo stimato OpenAI per ~400 recensioni è circa **$0.05–0.10**
- Le recensioni vengono processate in batch da 50 per ottimizzare le chiamate API
- Il file `.env` è incluso nel `.gitignore` e **non deve essere committato**