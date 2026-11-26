"""Secondary/official PDF fetcher for Sierra Leone Acts (2026-11-26, max-out brief).

  parl : Parliament of Sierra Leone /uploads/acts/ + /uploads/statutory_instruments/ PDFs, read from Internet Archive
         id_ captures (parliament.gov.sl is dead: 503 on http, invalid TLS on https). Official prints.
  slweb: Sierra Leone Web (www.sierra-leone.org/laws.html, ordinances.html) PDFs, live. Secondary compilation.

One request in flight per host, >= 1 s apart; back off on 429/5xx; stop the host on 403/challenge.
Cache: ../cache2/<source>/<name>. Log: ../progress.log; every request to ../cache2/requests.jsonl.
"""
import hashlib, json, os, re, sys, threading, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C2 = ROOT / "cache2"
C2.mkdir(exist_ok=True)
UA = "Mozilla/5.0 (compatible; LexifinaLawArchive/1.0; +https://lexifina.com)"
LOG = open(ROOT / "progress.log", "a", encoding="utf8", buffering=1)
REQ = open(C2 / "requests.jsonl", "a", encoding="utf8", buffering=1)
PARL = Path(r"C:\Users\alany\Documents\lexifina\scripts\sierra-leone-law\.tmp\parl_pdfs.json")


def log(m):
    LOG.write(time.strftime("%Y-%m-%dT%H:%M:%S ") + "fetch2: " + m + "\n")


def get(url, dest, gap):
    if dest.exists() and dest.stat().st_size:
        return True
    back = 30
    for _ in range(6):
        time.sleep(gap)
        code, body = None, b""
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=120) as r:
                code, body = r.status, r.read()
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:
            code = f"ERR {type(e).__name__}"
        REQ.write(json.dumps({"t": time.time(), "url": url, "code": code, "bytes": len(body)}) + "\n")
        if code == 200:
            if re.search(rb"cf-chl|challenge-platform|captcha", body[:5000], re.I):
                log(f"STOP challenge {url}")
                return "stop"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(body)
            return True
        if code in (403,):
            log(f"STOP 403 {url}")
            return "stop"
        if code == 404:
            return False
        log(f"retry {code} {url} sleep {back}")
        time.sleep(back)
        back = min(back * 2, 600)
    log(f"GAVE UP {url}")
    return False


def parl_items():
    rows = json.load(open(PARL, encoding="utf8"))
    seen, out = set(), []
    for r in sorted(rows, key=lambda r: r["timestamp"], reverse=True):
        o = r["original"]
        m = re.search(r"/uploads/(acts|statutory_instruments)/(.+\.pdf)$", o, re.I)
        if not m or r["statuscode"] != "200":
            continue
        name = urllib.parse.unquote(m.group(2))
        key = (m.group(1), name.lower())
        if key in seen or r["digest"] in seen:
            continue
        seen.add(key); seen.add(r["digest"])
        dest = C2 / "parl" / m.group(1) / re.sub(r'[<>:"/\\|?*]', "_", name)
        out.append((f"https://web.archive.org/web/{r['timestamp']}id_/{o}", dest, r))
    return out


def slweb_items():
    out = []
    for page in ("laws.html", "ordinances.html"):
        d = C2 / "slweb" / page
        get("https://www.sierra-leone.org/" + page, d, 1.0)
        h = d.read_text("utf8", "replace")
        for href in sorted(set(re.findall(r'href="([^"]+\.pdf)"', h, re.I))):
            u = urllib.parse.urljoin("https://www.sierra-leone.org/", href.replace(" ", "%20"))
            if "sierra-leone.org" not in u:
                continue
            name = urllib.parse.unquote(u.split("/Laws/", 1)[-1])
            out.append((u, C2 / "slweb" / "Laws" / re.sub(r'[<>:"\\|?*]', "_", name), None))
    return out


def run(items, gap, tag):
    n = ok = 0
    for url, dest, _ in items:
        r = get(url, dest, gap)
        if r == "stop":
            return
        n += 1; ok += bool(r)
        if n % 25 == 0:
            log(f"{tag} {n}/{len(items)} ok {ok}")
    log(f"{tag} done {n}/{len(items)} ok {ok}")


def main():
    p = parl_items()
    (ROOT / "parl_items.json").write_text(json.dumps([[u, str(d), r] for u, d, r in p], indent=0))
    log(f"parl {len(p)} distinct PDFs")
    t = threading.Thread(target=run, args=(p, 1.2, "parl"))
    t.start()
    s = slweb_items()
    (ROOT / "slweb_items.json").write_text(json.dumps([[u, str(d)] for u, d, _ in s], indent=0))
    log(f"slweb {len(s)} PDFs")
    run(s, 1.0, "slweb")
    t.join()
    log("all done")


if __name__ == "__main__":
    main()
