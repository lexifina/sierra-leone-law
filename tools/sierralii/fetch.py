"""SierraLII fetcher: legislation pages (+ source PDFs when no HTML text), then judgments.

One request at a time, 5 s apart (robots.txt Crawl-delay: 5). Back off on 429/5xx. Cache: ../cache/<path>.
Every request is logged to ../cache/requests.jsonl; progress to ../progress.log.
"""
import json, os, re, sys, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
BASE = "https://sierralii.gov.sl"
UA = "Mozilla/5.0 (compatible; LexifinaLawArchive/1.0; +https://lexifina.com)"
DELAY = 5.0
_last = [0.0]
LOG = open(ROOT / "progress.log", "a", encoding="utf8", buffering=1)
REQ = open(CACHE / "requests.jsonl", "a", encoding="utf8", buffering=1) if CACHE.exists() else None


def log(msg):
    LOG.write(time.strftime("%Y-%m-%dT%H:%M:%S ") + msg + "\n")


def cpath(path):
    p = path.lstrip("/")
    if p.endswith("/") or p == "":
        p += "index.html"
    elif not p.endswith(".pdf"):
        p += ".html"
    return CACHE / p.replace("?", "_q_").replace("@", "_at_")


def get(path, binary=False):
    f = cpath(path)
    if f.exists():
        return f.read_bytes()
    back = 60
    for attempt in range(8):
        wait = _last[0] + DELAY - time.time()
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        code, body = None, b""
        try:
            req = urllib.request.Request(BASE + path, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                code, body = r.status, r.read()
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:  # network
            code = f"ERR {type(e).__name__}"
        REQ.write(json.dumps({"t": time.time(), "path": path, "code": code, "bytes": len(body)}) + "\n")
        if code == 200:
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(body)
            return body
        if code == 404:
            log(f"404 {path}")
            return None
        if code in (403,):
            log(f"STOP 403 {path}")
            sys.exit(3)
        log(f"retry {code} {path} sleep {back}")
        time.sleep(back)
        back = min(back * 2, 900)
    log(f"GAVE UP {path}")
    return None


def links(b, rx):
    return sorted(set(re.findall(rx, b.decode("utf8", "replace"))))


def main():
    CACHE.mkdir(exist_ok=True)
    global REQ
    REQ = open(CACHE / "requests.jsonl", "a", encoding="utf8", buffering=1)
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    if stage in ("all", "leg"):
        sm = get("/sitemaps/legislation.xml")
        locs = [l.replace(BASE, "") for l in re.findall(r"<loc>([^<]+)</loc>", sm.decode())]
        for p in ("/legislation/", "/legislation/?page=2", "/legislation/subsidiary", "/legislation/repealed"):
            b = get(p)
            if b:
                locs += links(b, r'href="(/akn/sl/[^"#?]+eng@[0-9-]+)"')
        locs = sorted(set(locs))
        log(f"leg: {len(locs)} expressions")
        for i, p in enumerate(locs):
            b = get(p)
            if not b:
                continue
            h = b.decode("utf8", "replace")
            # other expressions (points in time) listed on the page
            for q in links(b, r'href="(' + re.escape(p.split("/eng@")[0]) + r'/eng@[0-9-]+)"'):
                if q not in locs:
                    locs.append(q)
            if "akn-akomaNtoso" not in h and "akn-section" not in h:
                m = re.search(r'data-pdf="([^"]+)"', h)
                if m:
                    get(m.group(1), binary=True)
            log(f"leg {i+1}/{len(locs)} {p}")
        log("leg done")
    if stage in ("all", "judg"):
        b = get("/judgments/")
        courts = links(b, r'href="/judgments/([A-Za-z]+)/"')
        allj = []
        for c in courts:
            first = get(f"/judgments/{c}/")
            if not first:
                continue
            js = links(first, r'href="(/akn/sl/judgment/[^"#?]+)"')
            n = 2
            while "?page=%d" % n in (pb if n > 2 else first).decode("utf8", "replace") and n < 200:
                pb = get(f"/judgments/{c}/?page={n}")
                if not pb:
                    break
                new = links(pb, r'href="(/akn/sl/judgment/[^"#?]+)"')
                if not new:
                    break
                js += new
                n += 1
            js = sorted(set(js))
            log(f"judg court {c}: {len(js)}")
            allj += js
        allj = sorted(set(allj))
        (ROOT / "judgments.json").write_text(json.dumps(allj, indent=0))
        log(f"judg: {len(allj)} decisions")
        for i, p in enumerate(allj):
            b = get(p)
            if b:
                h = b.decode("utf8", "replace")
                if "akn-akomaNtoso" not in h:
                    m = re.search(r'data-pdf="([^"]+)"', h)
                    if m:
                        get(m.group(1), binary=True)
            if i % 25 == 0:
                log(f"judg {i+1}/{len(allj)} {p}")
        log("judg done")


if __name__ == "__main__":
    main()
