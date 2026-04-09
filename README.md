# 🚗 Tool Analisi Recensioni — Quiz Patente Guida e Vai

Tool automatizzato per raccogliere, analizzare e reportare le recensioni
dell'app Quiz Patente Ufficiale da Google Play e App Store.

---

## ⚙️ Requisiti

- Python 3.11+
- Una API key OpenAI (https://platform.openai.com)

---

## 🚀 Installazione

### 1. Clona il repository

git clone https://github.com/TUO-USERNAME/deliverable-1.git
cd deliverable-1

### 2. Installa le dipendenze

pip install -r requirements.txt

### 3. Configura la API key

Crea un file .env nella root del progetto:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx

---

## ▶️ Utilizzo

Esegui tutto con un solo comando:

python main.py

Il tool eseguirà automaticamente:
- Step 1 → Scraping recensioni da Google Play e App Store
- Step 2 → Analisi AI con GPT-4o-mini
- Step 3 → Generazione report HTML

---

## 📁 Output

Tutti i file vengono salvati nella cartella /output/:

| File                  | Descrizione                              |
|-----------------------|------------------------------------------|
| reviews.json          | Recensioni grezze raccolte dagli store   |
| analysis_result.json  | Analisi strutturata in JSON              |
| report.html           | Report finale — aprire nel browser       |

---

## 📊 Esempio di output

Un esempio di report già generato è disponibile in:

output/report.html

Aprilo nel browser con doppio click.

---

## 🏗️ Struttura del progetto

deliverable-1/
├── main.py               # Entry point — esegui questo
├── scraper.py            # Raccolta recensioni dagli store
├── analyzer.py           # Analisi AI con OpenAI
├── report_generator.py   # Generazione report HTML
├── requirements.txt      # Dipendenze Python
├── .env                  # API key (non committare su GitHub)
├── .gitignore
└── output/
    ├── reviews.json
    ├── analysis_result.json
    └── report.html

---

## 🛠️ Stack tecnico

| Componente      | Tool                    |
|-----------------|-------------------------|
| Scraping        | google-play-scraper, app-store-scraper |
| Analisi AI      | OpenAI GPT-4o-mini      |
| Report          | Jinja2 + HTML/CSS       |
| Linguaggio      | Python 3.11+            |

---

## ⚠️ Note

- Lo scraping degli store è basato su dati pubblici, nessuna API key necessaria
- Il costo stimato OpenAI per 400 recensioni è circa 0.05-0.10$
- Se l'App Store non trova l'app per nome, sostituire app_name con app_id numerico in scraper.py