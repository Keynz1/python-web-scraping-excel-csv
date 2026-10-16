from pathlib import Path

import pytest
import requests

try:
    import scrape_data as _scrape
except ModuleNotFoundError:
    _scrape = None


FIXTURE = Path(__file__).parent / "fixtures" / "sample.html"


def impl():
    assert _scrape is not None, "scrape_data module is not implemented yet"
    return _scrape


class FakeResponse:
    def __init__(self, status_code=200, text="<html></html>"):
        self.status_code = status_code
        self.text = text


def test_parse_items_reads_training_site_fields():
    rows = impl().parse_items(FIXTURE.read_text(encoding="utf-8"))
    assert rows[0] == {
        "title": "Book A",
        "price": "£12.34",
        "availability": "In stock",
        "product_url": "catalogue/book-a_1/index.html",
    }
    assert len(rows) == 3


def test_parse_items_missing_price_is_predictable():
    rows = impl().parse_items(FIXTURE.read_text(encoding="utf-8"))
    assert rows[2]["price"] == ""


def test_normalize_item_strips_text_and_normalizes_currency():
    row = impl().normalize_item({
        "title": "  Book A  ",
        "price": "£12.34",
        "availability": "  In stock  ",
        "product_url": " /book-a ",
    })
    assert row == {
        "title": "Book A",
        "price_gbp": "12.34",
        "availability": "In stock",
        "product_url": "/book-a",
    }


def test_normalize_item_invalid_or_missing_price_becomes_blank():
    normalize = impl().normalize_item
    assert normalize({"title": "A", "price": "", "availability": "", "product_url": ""})["price_gbp"] == ""
    assert normalize({"title": "A", "price": "not-money", "availability": "", "product_url": ""})["price_gbp"] == ""


def test_fetch_html_returns_text(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *a, **k: FakeResponse(200, "<p>ok</p>"))
    assert impl().fetch_html("https://example.test", 3) == "<p>ok</p>"


def test_fetch_html_timeout_is_clear(monkeypatch):
    def boom(*a, **k):
        raise requests.Timeout("slow")
    monkeypatch.setattr(requests, "get", boom)
    with pytest.raises(RuntimeError, match="timeout"):
        impl().fetch_html("https://example.test", 1)


def test_fetch_html_non_200_is_clear(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *a, **k: FakeResponse(503, "no"))
    with pytest.raises(RuntimeError, match="HTTP 503"):
        impl().fetch_html("https://example.test", 3)


def test_fetch_html_uses_detected_encoding(monkeypatch):
    response = requests.Response()
    response.status_code = 200
    response._content = "£12.34".encode("utf-8")
    response.encoding = "ISO-8859-1"
    monkeypatch.setattr(requests, "get", lambda *a, **k: response)
    assert impl().fetch_html("https://example.test", 3) == "£12.34"
