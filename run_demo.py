from pathlib import Path

from export_data import write_csv, write_report, write_xlsx
from scrape_data import fetch_html, normalize_item, parse_items


SOURCE_URL = "https://books.toscrape.com/"
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"


def main() -> None:
    html = fetch_html(SOURCE_URL, timeout=20)
    rows = [normalize_item(item) for item in parse_items(html)[:10]]
    if not rows:
        raise RuntimeError("No items parsed from training site")
    write_csv(rows, OUTPUT / "scraped_books.csv")
    write_xlsx(rows, OUTPUT / "scraped_books.xlsx")
    write_report(rows, OUTPUT / "processing_report.txt", SOURCE_URL)
    print(f"Exported {len(rows)} rows to {OUTPUT}")


if __name__ == "__main__":
    main()
