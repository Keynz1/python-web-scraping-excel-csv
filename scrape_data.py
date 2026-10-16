from __future__ import annotations

from decimal import Decimal, InvalidOperation

import requests
from bs4 import BeautifulSoup


def fetch_html(url: str, timeout: float = 15.0) -> str:
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "PortfolioDemo/1.0"})
    except requests.Timeout as exc:
        raise RuntimeError(f"Request timeout for {url}") from exc
    except requests.RequestException as exc:
        raise RuntimeError(f"Request failed for {url}: {exc}") from exc
    if response.status_code != 200:
        raise RuntimeError(f"HTTP {response.status_code} for {url}")
    content = getattr(response, "content", None)
    if isinstance(content, (bytes, bytearray)):
        try:
            return bytes(content).decode("utf-8")
        except UnicodeDecodeError:
            pass
    return response.text


def parse_items(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    rows: list[dict[str, str]] = []
    for article in soup.select("article.product_pod"):
        link = article.select_one("h3 a")
        price = article.select_one(".price_color")
        availability = article.select_one(".availability")
        rows.append({
            "title": ((link.get("title") if link else "") or "").strip(),
            "price": (price.get_text(" ", strip=True) if price else "").strip(),
            "availability": (availability.get_text(" ", strip=True) if availability else "").strip(),
            "product_url": ((link.get("href") if link else "") or "").strip(),
        })
    return rows


def normalize_item(raw: dict[str, str]) -> dict[str, str]:
    price_text = str(raw.get("price", "")).strip().replace("£", "").replace(",", "")
    price_gbp = ""
    if price_text:
        try:
            price_gbp = f"{Decimal(price_text):.2f}"
        except InvalidOperation:
            price_gbp = ""
    return {
        "title": str(raw.get("title", "")).strip(),
        "price_gbp": price_gbp,
        "availability": " ".join(str(raw.get("availability", "")).split()),
        "product_url": str(raw.get("product_url", "")).strip(),
    }
