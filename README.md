# Web Scraping to Excel/CSV Demo

Self-created demonstration project for a common freelance task: collect structured data from a public website and deliver clean spreadsheet files.

## What it does
- Fetches a public training website intended for web scraping: https://books.toscrape.com/
- Extracts book title, GBP price, availability, and product URL.
- Normalizes whitespace and numeric prices.
- Exports matching CSV and XLSX files.
- Generates a concise processing report.
- Handles timeouts, HTTP errors, missing fields, and UTF-8 decoding explicitly.

## Run
```powershell
python run_demo.py
python -m pytest -v
```

## Demo result
Fresh verified run: 10 rows exported, 0 missing prices, CSV/XLSX content matched exactly, 10 automated tests passed.

## Notes
This is a self-created demonstration project. It uses only public training data and does not bypass logins, CAPTCHAs, or access controls.
