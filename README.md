# GuidaEVai — Analisi Automatica delle Recensioni

Pipeline automatizzata per raccogliere, analizzare con AI e visualizzare in un report HTML le recensioni dell'app dal **Google Play Store**.

## Come funziona

```
Scraping recensioni dal Play Store
    └─ Analisi del sentiment con AI (positivo / negativo / neutro)
    └─ Archiviazione nel database
    └─ Generazione automatica di un report HTML branded
```

## Come si usa

```bash
pip install -r requirements.txt
python main.py
```

Il report HTML viene generato nella cartella `output/`.

## File

| File | Descrizione |
|---|---|
| `scraper.py` | Scraping recensioni dal Google Play Store |
| `analyzer.py` | Analisi del sentiment con AI |
| `database.py` | Gestione del database delle recensioni |
| `report_generator.py` | Generazione report HTML |
| `template_report.html` | Template HTML del report |
| `main.py` | Script principale — esegue l'intera pipeline |

## Tecnologie

- `Python` — logica principale
- `Google Play scraping` — raccolta recensioni
- Analisi del sentiment con AI
- Report HTML generato automaticamente

## Tag

`python` `web-scraping` `sentiment-analysis` `google-play` `report` `html` `data-analysis` `ai` `recensioni`
