"""Append SierraLII legislation to sierra-leone-law main: one folder per Act, one file per section, one commit per
Act (the text as SierraLII publishes it), dated noon Freetown (GMT, +0000) on the in-force day.

    python -X utf8 tools/build_leg.py <repo> [--dry]

HTML (Akoma Ntoso) pages are read with peachjam.units_of; PDF-only pages with readpdf.read (text layer only).
A PDF is committed only if every printed word is kept and the section count equals the Arrangement of Sections
(or the sections run 1..N without gaps where no Arrangement is printed). Everything else is listed as held.
"""
import glob, json, os, re, subprocess, sys, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, r"C:\Users\alany\Documents\lexifina\scripts\sierra-leone-law")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import peachjam  # noqa
import readpdf  # noqa

ALREADY = {"act/2023/15", "act/2022/11", "act/2022/12", "act/2022/19", "act/2022/20", "act/2021/7", "act/2019/6", "act/2013/5"}  # act/2013/5 is replayed in constitution/
MONTHS = {m: i for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august",
                                      "september", "october", "november", "december"], 1)}
STOP = {"the", "of", "and", "act", "a", "for", "on", "to", "in"}


def iso(d, mon, y):
    return f"{int(y):04d}-{MONTHS[mon.lower()]:02d}-{int(d):02d}"


def date_in(text):
    m = re.search(r"(\d{1,2})(?:st|nd|rd|th)?\s+(?:day\s+of\s+)?([A-Za-z]+),?\s+(\d{4})", text or "")
    if m and m.group(2).lower() in MONTHS:
        return iso(*m.groups())
    return None


def slug_of(title):
    t = re.sub(r",?\s*\d{4}\s*$", "", title.strip())
    t = re.sub(r"\(.*?\)", lambda m: m.group(0), t)
    words = re.findall(r"[a-z0-9]+", t.lower().replace("'", ""))
    w = [x for x in words if x not in STOP] or words
    return "-".join(w)[:70].strip("-")


def text_of(h, cls):
    m = re.search(r'class="[^"]*\b' + cls + r'\b[^"]*"[^>]*>(.*?)</li>', h, re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip() if m else None


def works():
    out = []
    for f in sorted(glob.glob(str(ROOT / "cache/akn/sl/act/**/*.html"), recursive=True)):
        rel = Path(f).relative_to(ROOT / "cache").as_posix()
        m = re.match(r"akn/sl/(act(?:/si|/ci)?)/(\d{4})/([^/]+)/eng_at_(\d{4}-\d{2}-\d{2})\.html", rel)
        if not m:
            continue
        kind, year, num, expr = m.groups()
        out.append((f, kind, year, num, expr))
    return out


def build(repo, dry=False):
    held, done = [], []
    items = []
    for f, kind, year, num, expr in works():
        key = f"{kind}/{year}/{num}"
        if key in ALREADY:
            continue
        b = open(f, "rb").read()
        h = b.decode("utf8", "replace")
        title = re.sub(r"\s+", " ", re.search(r"<title>(.*?)</title>", h, re.S).group(1)).split("–")[0].strip()
        uri = f"https://sierralii.gov.sl/akn/sl/{kind}/{year}/{num}/eng@{expr}"
        pub = re.search(r"Published in\s+([^<]*?Gazette[^<]*?)\s+on\s+(\d{1,2} \w+ \d{4})", re.sub(r"\s+", " ", h))
        assent = re.search(r"Assented to on (\d{1,2} \w+ \d{4})", re.sub(r"\s+", " ", h))
        comm = re.search(r"Commenced on (\d{1,2} \w+ \d{4})", re.sub(r"\s+", " ", h))
        src, units, meta = "html", None, {}
        if "akn-akomaNtoso" in h:
            try:
                units, _ = peachjam.units_of(b)
                for u in units.values():
                    u.pop("_remarks", None)
            except Exception as e:
                held.append((key, title, f"HTML parse: {e}"))
                continue
            sha = hashlib.sha256(b).hexdigest()
        else:
            pdfs = glob.glob(f[:-5] + "/source.pdf")
            if not pdfs:
                held.append((key, title, "no text and no PDF on SierraLII"))
                continue
            pb = open(pdfs[0], "rb").read()
            sha = hashlib.sha256(pb).hexdigest()
            src = "pdf"
            try:
                units, rep, meta = readpdf.read(pb)
            except Exception as e:
                held.append((key, title, f"PDF layout not read by the side-note reader ({str(e)[:60]})"))
                continue
            if units is None:
                held.append((key, title, "scanned PDF, no text layer (no OCR)"))
                continue
            secs = [k for k in units if re.fullmatch(r"sec-\d{3}", k)]
            nums = [int(k[4:]) for k in secs]
            seq = nums == list(range(1, len(nums) + 1))
            if rep["n_missing"] or rep["n_added"]:
                held.append((key, title, f"word check: {rep['n_missing']} printed words not kept, {rep['n_added']} added"))
                continue
            if rep["toc_last"] and rep["toc_last"] != len(secs) or not seq:
                held.append((key, title, f"sections read {len(secs)} (sequential: {seq}) vs Arrangement {rep['toc_last']}"))
                continue
        if not units:
            held.append((key, title, "no provisions"))
            continue
        # in-force day
        basis = None
        if comm:
            day = date_in(comm.group(1)); basis = f"SierraLII: Commenced on {comm.group(1)}"
        elif meta.get("commencement_bracket") and date_in(meta["commencement_bracket"]):
            day = date_in(meta["commencement_bracket"]); basis = f"date of commencement printed on the Act: [{meta['commencement_bracket']}]"
        elif pub:
            day = date_in(pub.group(2)); basis = (f"no commencement date printed; published in {pub.group(1)} on {pub.group(2)}, "
                                                  "so in force on publication (Constitution s. 106(3))")
        elif meta.get("gazette"):
            gz = meta["gazette"]; day = iso(gz[1], gz[2], gz[3])
            basis = f"no commencement date printed; Gazette No. {gz[0]} of {day}, in force on publication (Constitution s. 106(3))"
        else:
            day = expr; basis = f"SierraLII expression date {expr} (the Act as published)"
        noun = {"act": "Act", "act/si": "Statutory Instrument", "act/ci": "Constitutional Instrument"}[kind]
        label = f"{noun} No. {num} of {year}" if num.isdigit() else f"{noun} {num} ({year})"
        folder = slug_of(title)
        if kind != "act":
            folder = f"{kind.split('/')[1]}-{year}-{num}-{folder}"[:80]
        items.append(dict(key=key, title=title, uri=uri, day=day, basis=basis, units=units, label=label, folder=folder,
                          src=src, sha=sha, assent=assent.group(1) if assent else None,
                          pub=f"{pub.group(1)} on {pub.group(2)}" if pub else None, year=year, num=num, kind=kind))
    items.sort(key=lambda x: (x["day"], x["key"]))
    seen = {p.name for p in Path(repo).iterdir()}
    for it in items:
        while it["folder"] in seen:
            it["folder"] += f"-{it['year']}"
        seen.add(it["folder"])
    if dry:
        for it in items:
            print(it["day"], it["key"], it["folder"], len(it["units"]), it["src"])
        for h_ in held:
            print("HELD", *h_)
        return items, held
    for k, it in enumerate(items):
        d = Path(repo) / it["folder"]
        d.mkdir()
        for ukey, u in it["units"].items():
            (d / f"{ukey}.md").write_bytes(u["text"].encode("utf8"))
        email = f"{it['kind'].replace('/', '-')}-{it['year']}-{it['num']}@sierralii.invalid"
        via = ("SierraLII's Akoma Ntoso text" if it["src"] == "html" else
               "the text layer of the print SierraLII publishes (source.pdf), read by section side notes; "
               "every printed word kept")
        msg = (f"{it['title']} as enacted ({it['label']})\n\n"
               f"{it['title']}: the text as SierraLII publishes it, from {via}.\n\n"
               f"Law: {it['label']}\nKind: law\n"
               + (f"Enacted: {date_in(it['assent'])}\n" if it["assent"] else "")
               + (f"Published: {it['pub']}\n" if it["pub"] else "")
               + f"In-force: {it['day']}\nIn-force-basis: {it['basis']}\nSource: {it['uri']}\n"
               f"Source-sha256: {it['sha']}\nAct: {it['title']}\nProvisions: {len(it['units'])}\n")
        env = dict(os.environ, GIT_AUTHOR_NAME=it["label"], GIT_AUTHOR_EMAIL=email,
                   GIT_AUTHOR_DATE=f"{it['day']}T12:00:00+0000", GIT_COMMITTER_DATE=f"{it['day']}T12:00:00+0000")
        subprocess.run(["git", "-C", repo, "add", "--", it["folder"]], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-q", "-F", "-"], input=msg.encode(), env=env, check=True)
        done.append(it)
    (ROOT / "leg_result.json").write_text(json.dumps(
        {"committed": [{k: v for k, v in it.items() if k != "units"} | {"provisions": len(it["units"])} for it in done],
         "held": held}, indent=1))
    print(len(done), "committed;", len(held), "held")
    return done, held


if __name__ == "__main__":
    build(sys.argv[1], "--dry" in sys.argv)
