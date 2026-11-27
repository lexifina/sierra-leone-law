"""Secondary source: WIPO Lex English PDFs for a few Sierra Leone Acts not yet held (1 request in flight, >=1 s apart).

    python -X utf8 tools/sl_wipo.py
"""
import html, re, time
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
C = ROOT / "cache3" / "wipo"
UA = {"User-Agent": "Mozilla/5.0 (compatible; law-archive-research)"}
PDFS = ["sl012en_1", "sl007en", "sl021en", "sl023en", "sl013en_1"]
s = requests.Session(); s.headers.update(UA)
for name in PDFS:
    out = C / f"{name}.pdf"
    if out.exists():
        continue
    u = f"https://wipolex-res.wipo.int/edocs/lexdocs/laws/en/sl/{name}.pdf"
    r = s.get(u, timeout=(30, 120)); time.sleep(1)
    b = r.content
    if b[:5] != b"%PDF-":
        m = re.search(r'(?:href|src)="(' + re.escape(u) + r'\?[^"]+)"', r.text)
        if not m:
            print(name, "no signed link", r.status_code); continue
        r = s.get(html.unescape(m.group(1)), timeout=(30, 120)); time.sleep(1)
        b = r.content
    if b[:5] == b"%PDF-":
        out.write_bytes(b); print(name, len(b))
    else:
        print(name, "not a PDF", r.status_code)
