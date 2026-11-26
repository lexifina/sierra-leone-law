"""Sierra Leone case law from SierraLII -> git fast-import stream (one file and one commit per decision).

    python -X utf8 tools/build_judg.py <repo-dir>     # (re)builds branch main from the cache, deterministic

Layout: <court>/<year>/<number>.md (court = SierraLII's court code, lower case, e.g. slca, slsc, slhc).
Commit date: noon Freetown (GMT) on the judgment date; author: the court. Text: SierraLII's HTML text where it has
one, else the text layer of a born-digital PDF (PyMuPDF). Scans (a page image on most pages) are held: no OCR, and
no OCR layer anyone else made. Protected cases (children, family, sexual offences, anonymised parties) are held.
"""
import glob, hashlib, html as H, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COURTS = {"scsl": "Special Court for Sierra Leone", "slsc": "Supreme Court of Sierra Leone",
          "slca": "Court of Appeal of Sierra Leone", "slhc": "High Court of Sierra Leone"}
PROTECT = re.compile(r"\b(infant|juvenile|minor|child(ren)?|adoption|custody|guardianship|rape|sexual|indecent|"
                     r"defilement|incest|divorce|matrimonial|domestic violence|in camera|anonymi[sz]ed|"
                     r"[A-Z]\.\s?[A-Z]\.?\s+v\.?\s|v\.?\s+[A-Z]\.\s?[A-Z]\.?\b)", re.I)


def clean(s):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def meta_of(h):
    m = {}
    m["title"] = clean(re.search(r"<title>(.*?)</title>", h, re.S).group(1)).rsplit("–", 1)[0].strip()
    for k, lab in (("citation", "Media Neutral Citation"), ("court_name", "Court"), ("case_number", "Case number"),
                   ("judges", "Judges"), ("date", "Judgment date")):
        x = re.search(r"<dt[^>]*>\s*" + lab + r"\s*</dt>\s*<dd[^>]*>(.*?)</dd>", h, re.S)
        if x:
            v = clean(x.group(1))
            v = re.sub(r"\s*Copy.*$", "", v) if k == "citation" else v
            m[k] = re.sub(r"(\[\d{4}\] \w+ \d+)\s+\1.*", r"\1", v)
    return m


def html_text(h):
    i = h.find("akn-akomaNtoso")
    if i < 0:
        return None
    start = h.rfind("<", 0, i)
    body = h[start:]
    end = body.find('class="content-and-enrichments__')  # sidebar
    body = re.sub(r"(?is)<(script|style).*?</\1>", " ", body)
    body = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h\d|tr|blockquote)>", "\n", body)
    lines = [re.sub(r"[ \t\xa0]+", " ", H.unescape(re.sub(r"<[^>]+>", "", l))).strip() for l in body.split("\n")]
    return "\n".join(l for l in lines if l)


def pdf_text(p):
    import fitz
    d = fitz.open(p)
    if sum(1 for pg in d if pg.get_images()) > len(d) / 2:
        return None, "scan"
    t = "\n".join(pg.get_text("text") for pg in d)
    lines = [re.sub(r"[ \t\xa0]+", " ", l).strip() for l in t.splitlines()]
    t = "\n".join(l for l in lines if l)
    if len(t) < 500:
        return None, "no text layer"
    return t, "pdf"


def main(repo):
    recs, held = [], []
    for f in sorted(glob.glob(str(ROOT / "cache/akn/sl/judgment/*/*/*/*.html"))):
        rel = Path(f).relative_to(ROOT / "cache").as_posix()
        mm = re.match(r"akn/sl/judgment/(\w+)/(\d{4})/([^/]+)/eng_at_(\d{4}-\d{2}-\d{2})\.html", rel)
        if not mm:
            continue
        court, year, num, day = mm.groups()
        h = open(f, encoding="utf8", errors="replace").read()
        m = meta_of(h)
        uri = f"https://sierralii.gov.sl/akn/sl/judgment/{court}/{year}/{num}/eng@{day}"
        key = f"{court}/{year}/{num}"
        if PROTECT.search(m["title"]):
            held.append((key, m["title"], "protected (child, family, sexual offence or anonymised party)"))
            continue
        text, how = html_text(h), "html"
        sha = hashlib.sha256(h.encode("utf8")).hexdigest()
        if not text or len(text) < 300:
            pdfs = glob.glob(f[:-5] + "/source.pdf")
            if not pdfs:
                held.append((key, m["title"], "no text and no PDF")); continue
            text, how = pdf_text(pdfs[0])
            if not text:
                held.append((key, m["title"], how)); continue
            sha = hashlib.sha256(open(pdfs[0], "rb").read()).hexdigest()
        if PROTECT.search(text[:3000]) and re.search(r"(?i)\b(rape|sexual|defilement|juvenile|infant)\b", text[:3000]):
            held.append((key, m["title"], "protected (subject named in the opening of the text)")); continue
        recs.append(dict(key=key, court=court, year=year, num=num, day=day, uri=uri, how=how, sha=sha, text=text, **m))
    recs.sort(key=lambda r: (r["day"], r["key"]))
    out = open(ROOT / "judg.fi", "wb")
    w = out.write
    prev = None
    for i, r in enumerate(recs):
        num = r["num"].zfill(3) if r["num"].isdigit() else r["num"]
        path = f"{r['court']}/{r['year']}/{num}.md"
        body = (f"# {r['title']}\n\n" + "\n".join(f"{lab}: {r[k]}" for k, lab in (
            ("citation", "Citation"), ("court_name", "Court"), ("case_number", "Case number"), ("judges", "Judges"),
            ("date", "Judgment date")) if r.get(k)) + f"\nSource: {r['uri']}\n\n" + r["text"] + "\n").encode("utf8")
        author = r.get("court_name") or COURTS.get(r["court"], r["court"].upper())
        email = f"{r['court']}@sierralii.invalid"
        msg = (f"{r.get('citation') or r['key']}: {r['title']}\n\n"
               f"Decided: {r['day']}\nIn-force: {r['day']}\nIn-force-basis: judgment date as SierraLII records it\n"
               f"Court: {author}\n" + (f"Citation: {r['citation']}\n" if r.get("citation") else "")
               + f"Source: {r['uri']}\nText-from: {'SierraLII HTML' if r['how'] == 'html' else 'PDF text layer (born-digital)'}\n"
               f"Source-sha256: {r['sha']}\n").encode("utf8")
        ts = f"{int(__import__('calendar').timegm(__import__('time').strptime(r['day'] + ' 12:00', '%Y-%m-%d %H:%M')))} +0000"
        w(b"blob\nmark :%d\ndata %d\n" % (2 * i + 1, len(body)) + body + b"\n")
        w(f"commit refs/heads/main\nmark :{2 * i + 2}\nauthor {author} <{email}> {ts}\ncommitter Lexifina <sierra-leone-law@lexifina.com> {ts}\n".encode())
        w(b"data %d\n" % len(msg) + msg)
        if prev:
            w(f"from :{prev}\n".encode())
        w(f"M 100644 :{2 * i + 1} {path}\n\n".encode())
        prev = 2 * i + 2
    out.close()
    (ROOT / "judg_result.json").write_text(json.dumps({"committed": len(recs), "held": held}, indent=1))
    print(len(recs), "decisions;", len(held), "held")
    if repo:
        subprocess.run(["git", "-C", repo, "fast-import", "--force", "--quiet"], stdin=open(ROOT / "judg.fi", "rb"), check=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
