from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook


FIELDS = ["title", "price_gbp", "availability", "product_url"]


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_xlsx(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Scraped Data"
    ws.append(FIELDS)
    for row in rows:
        ws.append([row.get(field, "") for field in FIELDS])
    wb.save(path)


def write_report(rows: list[dict[str, str]], path: Path, source_url: str) -> None:
    missing_price = sum(1 for row in rows if not row.get("price_gbp"))
    text = "\n".join([
        "Web Scraping Demo Report",
        f"Source: {source_url}",
        f"Rows exported: {len(rows)}",
        f"Rows with missing price: {missing_price}",
        "",
    ])
    path.write_text(text, encoding="utf-8")
