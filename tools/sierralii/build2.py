"""Append Acts read from Parliament of Sierra Leone prints (Internet Archive copies; the site is dead) and from
Sierra Leone Web (www.sierra-leone.org/laws.html, a secondary compilation) to sierra-leone-law main.

    python -X utf8 tools/build2.py <repo> [--dry]

Same layout and checks as build_leg.py: one folder per Act, one file per section/schedule/long title, one commit per
Act as enacted, dated noon Freetown (GMT) on the in-force day. A PDF is committed only if the side-note reader keeps
every printed word from the enacting formula to "Passed in Parliament" (none added), the sections run 1..N, and N
equals the Arrangement of Sections (or, with no Arrangement, the section numbers found in order in the text).
In-force day: the date of commencement printed on the Act; else its Gazette date (Constitution s. 106(3)); else held.
Official copy first: a Parliament print wins over the Sierra Leone Web copy of the same Act.
"""
import hashlib, json, os, re, subprocess, sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fitz  # noqa
fitz.TOOLS.mupdf_display_errors(False)
import readpdf  # noqa
from build_leg import slug_of, iso, MONTHS  # noqa

SLWEB = "Sierra Leone Web, https://www.sierra-leone.org/laws.html"


def date_of(s):
    m = re.search(r"(\d{1,2})\s*(?:st|nd|rd|th)?\s+(?:day\s+of\s+)?([A-Za-z]+)\s*,?\s*(\d{4})", s or "")
    if m and m.group(2).lower() in MONTHS:
        try:
            return iso(*m.groups())
        except Exception:
            return None
    return None


def seq_in_text(full):
    """Section numbers 1, 2, 3 ... found in order at line starts after the enacting formula."""
    i = full.find("ENACTED")
    t = full[i:] if i >= 0 else full
    pos, k = 0, 0
    while True:
        m = re.compile(r"(?m)^\s*%d\.\s" % (k + 1)).search(t, pos)
        if not m:
            return k
        k += 1; pos = m.end()


def ident(full):
    m = re.search(r"No\.\s*(\d+)\s+(\d{4})\s+Sierra\s+Leone\s+(?:THE\s+|The\s+)?(.{5,160}?(?:Act|ACT|Decree|DECREE),?\s*\d{4})\s*\.?",
                  re.sub(r"\s+", " ", full[:40000]))
    if not m:
        return None
    title = re.sub(r"\s+", " ", m.group(3)).strip()
    if title.isupper():
        title = re.sub(r"\b(Of|And|The|For|In|On|To|A)\b", lambda x: x.group(0).lower(), title.title())
    title = title[0].upper() + title[1:]
    return int(m.group(1)), int(m.group(2)), "The " + title if not title.lower().startswith("the ") else title


def ident_from_name(src, k, titles):
    """Sierra Leone Web files are named <year>-<Act number>[p|s].pdf; the title is the index's link text."""
    if src != "slweb":
        return None
    m = re.fullmatch(r"slweb/Laws/(\d{4})-0*(\d+)[ps]?\.pdf", k)
    t = titles.get(k)
    if not m or not t or not re.search(r"\bAct\b", t):
        return None
    t = re.sub(r"\s+", " ", t.replace("\xa0", " ")).strip()
    return int(m.group(2)), int(m.group(1)), t


def slweb_titles():
    out = {}
    for page in ("laws.html", "ordinances.html"):
        p = ROOT / "cache2" / "slweb" / page
        if not p.exists():
            continue
        h = p.read_text("utf8", "replace")
        for href, txt in re.findall(r'(?s)<a[^>]+href="(Laws/[^"]+\.pdf)"[^>]*>(.*?)</a>', h):
            import html as H
            out["slweb/" + H.unescape(href)] = H.unescape(re.sub(r"<[^>]+>", "", txt)).strip()
    return out


def br_ok(meta):
    return bool(date_of(meta.get("commencement_bracket")))


def existing(repo):
    out = set()
    log = subprocess.run(["git", "-C", repo, "log", "--format=%(trailers:key=Law,valueonly,separator=;)"],
                         capture_output=True, text=True).stdout
    for m in re.finditer(r"Act (?:No\. )?(\d+) of (\d{4})", log):
        out.add((int(m.group(2)), int(m.group(1))))
    return out


def candidates():
    survey = json.loads((ROOT / "survey2.json").read_text())
    urls = {}
    for u, d, r in json.loads((ROOT / "parl_items.json").read_text()):
        urls[Path(d).relative_to(ROOT / "cache2").as_posix()] = ("parl", u, r)
    for u, d in json.loads((ROOT / "slweb_items.json").read_text()):
        urls[Path(d).relative_to(ROOT / "cache2").as_posix()] = ("slweb", u, None)
    return survey, urls


def build(repo, dry=False):
    survey, urls = candidates()
    have = existing(repo)
    titles = slweb_titles()
    items, held = {}, []
    for k, s in sorted(survey.items()):
        if k not in urls or s.get("kind") not in ("digital", "ocr"):
            continue
        src, url, cdx = urls[k]
        b = (ROOT / "cache2" / k).read_bytes()
        doc = fitz.open(stream=b, filetype="pdf")
        full = readpdf.batch2.page_text(doc)
        plain = "\n".join(p.get_text("text") for p in doc)
        idt = ident(plain) or ident(full) or ident_from_name(src, k, titles)
        if not idt:
            held.append((k, None, "no 'No. N YYYY Sierra Leone <title>' head line (not an Act print the reader knows)"))
            continue
        num, year, title = idt
        key = (year, num)
        if key in have or "constitution" in title.lower():
            continue
        try:
            units, rep, meta = readpdf.read(b, allow_ocr=s["kind"] == "ocr")
        except Exception as e:
            held.append((k, title, f"reader: {str(e)[:60]}")); continue
        if units is None:
            held.append((k, title, rep.get("error"))); continue
        secs = [x for x in units if re.fullmatch(r"sec-\d{3}", x)]
        nums = [int(x[4:]) for x in secs]
        want = rep["toc_last"] or seq_in_text(full)
        if not rep["toc_last"] and len(secs) * 1.5 < len(doc):
            held.append((k, title, f"no Arrangement of Sections and only {len(secs)} sections read from {len(doc)} pages")); continue
        if not secs or nums != list(range(1, len(nums) + 1)) or want != len(secs):
            held.append((k, title, f"sections read {len(secs)} vs {'Arrangement' if rep['toc_last'] else 'numbers in text'} {want}")); continue
        if rep["n_missing"] or rep["n_added"]:
            held.append((k, title, f"word check: {rep['n_missing']} not kept, {rep['n_added']} added")); continue
        alltext = " ".join(u["text"] for u in units.values())
        if not br_ok(meta) and re.search(r"(?i)come into (?:operation|force) on (?:such )?(?:a |the )?(?:day|date)s? (?:as|that|which) the (?:President|Minister)", alltext):
            held.append((k, title, "commencement left to a later order (President or Minister); its date is not in the print")); continue
        gz = meta.get("gazette")
        if not gz:
            m = re.search(r"GAZETTE\s+(?:EXTRAORDINARY\s+)?(?:Vol\.\s*[A-Z]+,?\s*)?No\.\s*(\d+)\s+(?:OF|dated)\s+(\d{1,2})\s*(?:ST|ND|RD|TH)?\s+([A-Z]+),?\s+(\d{4})",
                          plain, re.I)
            if m and m.group(3).lower() in MONTHS:
                gz = m.groups()
        br = date_of(meta.get("commencement_bracket"))
        if br:
            day, basis = br, f"date of commencement printed on the Act: [{meta['commencement_bracket'].strip()}]"
        elif gz:
            day = iso(gz[1], gz[2], gz[3])
            basis = f"no commencement date printed; Gazette No. {gz[0]} of {day}, in force on publication (Constitution s. 106(3))"
        else:
            held.append((k, title, "no commencement date and no Gazette date printed")); continue
        sg = date_of(" ".join(meta["signed"])) if meta.get("signed") else None
        if not br and sg and day < sg:
            held.append((k, title, f"Gazette date {day} printed before the signing date {sg}")); continue
        it = dict(k=k, src=src, url=url, cdx=cdx, title=title, num=num, year=year, day=day, basis=basis, units=units,
                  sha=hashlib.sha256(b).hexdigest(), kind=s["kind"],
                  signed=date_of(" ".join(meta["signed"])) if meta.get("signed") else None,
                  gazette=f"Supplement to the Sierra Leone Gazette No. {gz[0]} of {iso(gz[1], gz[2], gz[3])}" if gz else None)
        prev = items.get(key)
        if prev is None or (prev["src"] == "slweb" and src == "parl") or (prev["kind"] == "ocr" and it["kind"] == "digital"):
            items[key] = it
    items = sorted(items.values(), key=lambda x: (x["day"], x["year"], x["num"]))
    seen = {p.name for p in Path(repo).iterdir()}
    for it in items:
        it["folder"] = slug_of(it["title"])
        while it["folder"] in seen:
            it["folder"] += f"-{it['year']}"
        seen.add(it["folder"])
    if dry:
        for it in items:
            print(it["day"], it["year"], it["num"], it["src"], it["kind"], it["folder"], len(it["units"]))
        for h in held:
            print("HELD", *h)
        return items, held
    done = []
    for it in items:
        d = Path(repo) / it["folder"]
        d.mkdir()
        for ukey, u in it["units"].items():
            (d / f"{ukey}.md").write_bytes(u["text"].encode("utf8"))
        label = f"Act No. {it['num']} of {it['year']}"
        pre70 = it["day"] < "1970-01-01"
        stamp = "1970-01-01T12:00:00+0000" if pre70 else f"{it['day']}T12:00:00+0000"
        if it["src"] == "parl":
            via = ("the Parliament of Sierra Leone's copy of the Government Printing Department print, read from an "
                   "Internet Archive capture (parliament.gov.sl no longer answers)")
            orig = it["cdx"]["original"].replace(":80/", "/")
            srcl = f"Source: {orig}\nArchived-copy: {it['url']}\n"
            status = ""
        else:
            via = "the Sierra Leone Web copy of the Government Printing Department print (a secondary compilation)"
            srcl = f"Source: {it['url']}\n"
            status = f"Source-status: secondary copy ({SLWEB})\n"
        msg = (f"{it['title']} as enacted ({label})" + (f", in force {it['day']}" if pre70 else "") + "\n\n"
               f"{it['title']}: the text as printed, from {via}; read from the PDF's text layer by section side notes, "
               "every printed word kept.\n\n"
               f"Law: {label}\nKind: law\n" + (f"Enacted: {it['signed']}\n" if it["signed"] else "")
               + (f"Published: {it['gazette']}\n" if it["gazette"] else "")
               + f"In-force: {it['day']}\nIn-force-basis: {it['basis']}\n" + srcl + status
               + ("Text-source: publisher OCR\n" if it["kind"] == "ocr" else "")
               + f"Source-sha256: {it['sha']}\nAct: {it['title']}\nProvisions: {len(it['units'])}\n")
        env = dict(os.environ, GIT_AUTHOR_NAME=label, GIT_AUTHOR_EMAIL=f"act-{it['year']}-{it['num']}@sierra-leone-law.invalid",
                   GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp, GIT_COMMITTER_NAME="Lexifina",
                   GIT_COMMITTER_EMAIL="sierra-leone-law@lexifina.com")
        subprocess.run(["git", "-C", repo, "add", "--", it["folder"]], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-q", "-F", "-"], input=msg.encode(), env=env, check=True)
        done.append(it)
    res = ROOT / "build2_result.json"
    old = json.loads(res.read_text()) if res.exists() else {"committed": []}
    res.write_text(json.dumps({"committed": old["committed"] + [{k: v for k, v in it.items() if k not in ("units", "cdx")}
                                                                 | {"provisions": len(it["units"])} for it in done],
                               "held": held}, indent=1))
    print(len(done), "committed;", len(held), "held")
    return done, held


if __name__ == "__main__":
    build(sys.argv[1], "--dry" in sys.argv)
