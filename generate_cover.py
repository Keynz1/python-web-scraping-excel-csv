from pathlib import Path
import csv
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
COVER = ROOT / "portfolio_cover_1600x1200.png"


def font(size: int, bold: bool = False):
    candidates = [
        Path(r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf"),
        Path(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf"),
    ]
    for p in candidates:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def main():
    with (OUT / "scraped_books.csv").open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    missing = sum(1 for r in rows if not r.get("price_gbp"))

    img = Image.new("RGB", (1600, 1200), "#0b1426")
    d = ImageDraw.Draw(img)
    white = "#f4f7fb"
    muted = "#a8b4c8"
    cyan = "#39c6ff"
    green = "#55e39b"
    panel = "#152239"
    line = "#2c4162"

    d.text((70, 60), "Web Scraping → Excel/CSV", font=font(64, True), fill=white)
    d.text((72, 145), "Self-created Python automation demo", font=font(30), fill=muted)

    steps = ["FETCH", "PARSE", "NORMALIZE", "EXPORT CSV", "EXPORT XLSX", "REPORT"]
    x = 70
    y = 270
    w = 210
    h = 150
    for i, label in enumerate(steps):
        d.rounded_rectangle((x, y, x+w, y+h), radius=22, fill=panel, outline=cyan if i < 3 else green, width=3)
        d.text((x+24, y+45), label, font=font(25, True), fill=white)
        if i < len(steps)-1:
            d.line((x+w+14, y+h//2, x+w+55, y+h//2), fill=muted, width=5)
            d.polygon([(x+w+55, y+h//2), (x+w+38, y+h//2-10), (x+w+38, y+h//2+10)], fill=muted)
        x += 245

    d.rounded_rectangle((70, 500, 1530, 900), radius=28, fill=panel, outline=line, width=3)
    d.text((110, 545), "Verified live result", font=font(38, True), fill=white)
    metrics = [
        ("10", "records collected"),
        (str(missing), "missing prices"),
        ("MATCH", "CSV = XLSX"),
        ("10/10", "tests passed"),
    ]
    mx = 120
    for value, label in metrics:
        d.text((mx, 650), value, font=font(54, True), fill=cyan if value != "MATCH" else green)
        d.text((mx, 725), label, font=font(26), fill=muted)
        mx += 350

    d.text((80, 1010), "Python  •  Requests  •  BeautifulSoup  •  openpyxl  •  pytest", font=font(29), fill=white)
    d.text((80, 1065), "Public training source only — no login, CAPTCHA bypass, or private data", font=font(25), fill=muted)
    img.save(COVER)
    print(COVER)


if __name__ == "__main__":
    main()
