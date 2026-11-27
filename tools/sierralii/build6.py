"""Whole-text Acts: an Act whose print has a good text layer but that the side-note reader cannot split into sections
is committed as one file, <act-folder>/text.md (layout decision 2026-11-27, as malawi-law and eritrea-law).

    python -X utf8 tools/build6.py <repo> [--dry]

Candidates: held Parliament / Sierra Leone Web / FAOLEX prints (build2/build5 results), SierraLII source PDFs the
reader could not split (leg_result.json), and WIPO Lex English PDFs (cache3/wipo). Gates, all required:
- a text layer (no OCR of ours; a scan's own layer is used and tagged Text-source: publisher OCR);
- no page repeated (identical page text), so a copy with doubled pages is left out;
- complete: the section numbers 1..N appear at line starts in order after the enacting formula, where N is the last
  number of the printed Arrangement of Sections (or, with none, at least 2 sections found); a gap means missing pages;
- dated by build2's rules: the commencement date printed; else the Gazette date printed (Constitution s. 106(3));
  else (SierraLII) its expression date; else (WIPO Lex) the record's entry-into-force date. An Act left to a
  commencement order is held. Pre-1970: 1970-01-01 stamp, the real day in the subject and In-force.
The text is the print's text layer in reading order (two-up pages halved as batch2 does), from the title to the end,
with page numbers dropped and lines joined only where a word was hyphenated; every other printed word is kept.
"""
import hashlib, html, json, os, re, subprocess, sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fitz  # noqa
fitz.TOOLS.mupdf_display_errors(False)
import readpdf  # noqa
import build2  # noqa
from build_leg import slug_of  # noqa

WIPO = {  # file: (record, title, Act number, year, entry into force from the record or None)
    "sl012en_1": ("https://www.wipo.int/wipolex/en/legislation/details/14529", "The Copyright Act, 2011", 8, 2011, None),
    "sl007en": ("https://www.wipo.int/wipolex/en/legislation/details/11462", "The Pharmacy and Drugs Act, 2001", 12, 2001,
                "2001-12-13"),
    "sl021en": ("https://www.wipo.int/wipolex/en/legislation/details/20541", "The Customs Act, 2011", 9, 2011, None),
    "sl023en": ("https://www.wipo.int/wipolex/en/legislation/details/20543", "The Goods and Services Tax Act, 2009", 6,
                2009, "2009-09-01"),
    "sl013en_1": ("https://www.wipo.int/wipolex/en/legislation/details/14551",
                  "The Patents and Industrial Designs Act, 2012", 10, 2012, None),
}
LATER = re.compile(r"(?i)(?:come|comes) into (?:operation|force) on (?:such )?(?:a |the )?(?:day|date)s? (?:as|that|which) "
                   r"the (?:President|Minister|Prime Minister)")


def candidates():
    out = []
    b2 = json.loads((ROOT / "build2_result.json").read_text())
    b5 = json.loads((ROOT / "build5_result.json").read_text()) if (ROOT / "build5_result.json").exists() else {"held": []}
    for k, title, why in b2["held"] + b5["held"]:
        why = str(why)
        if not title or why.startswith(("withdrawn", "commencement left", "no commencement date", "Gazette date")):
            continue
        if not re.match(r"sections read|reader:|no Arrangement|second reading", why):
            continue
        src = k.split("/")[0]
        if src not in ("parl", "slweb", "faolex") or "Statutes Relating" in k:  # land-law compilations, not one Act
            continue
        out.append({"path": ROOT / "cache2" / k, "src": src, "k": k, "title": title})
    parl = {Path(d).relative_to(ROOT / "cache2").as_posix(): (u, r) for u, d, r in json.loads((ROOT / "parl_items.json").read_text())}
    slw = {Path(d).relative_to(ROOT / "cache2").as_posix(): u for u, d in json.loads((ROOT / "slweb_items.json").read_text())}
    for c in out:
        if c["src"] == "parl":
            c["url"], c["cdx"] = parl[c["k"]]
        elif c["src"] == "slweb":
            c["url"] = slw[c["k"]]
        else:
            c["url"] = "https://faolex.fao.org/docs/pdf/" + c["k"].split("/", 1)[1]
            rec = next((json.loads(p.read_text("utf8")).get("_url") for p in (ROOT / "cache3/faolex/rec").glob("*.json")
                        if c["k"].split("/", 1)[1] in (json.loads(p.read_text("utf8")).get("links_to_full_text") or [])), None)
            c["record"] = rec
    leg = json.loads((ROOT / "leg_result.json").read_text())
    for key, title, why in leg["held"]:
        m = re.fullmatch(r"act/(\d{4})/(\d+)", key)
        if not m or not why.startswith(("PDF layout not read", "sections read")):
            continue
        pdfs = sorted((ROOT / "cache" / "akn" / "sl" / "act" / m.group(1) / m.group(2)).glob("eng_at_*/source.pdf"))
        if not pdfs:
            continue
        expr = pdfs[-1].parent.name[len("eng_at_"):]
        out.append({"path": pdfs[-1], "src": "sierralii", "k": key, "title": html.unescape(title), "num": int(m.group(2)),
                    "year": int(m.group(1)), "expr": expr,
                    "url": f"https://sierralii.gov.sl/akn/sl/act/{m.group(1)}/{m.group(2)}/eng@{expr}/source.pdf"})
    for f, (rec, title, num, year, eif) in WIPO.items():
        out.append({"path": ROOT / "cache3" / "wipo" / f"{f}.pdf", "src": "wipo", "k": f"wipo/{f}", "title": title,
                    "num": num, "year": year, "eif": eif, "record": rec,
                    "url": f"https://wipolex-res.wipo.int/edocs/lexdocs/laws/en/sl/{f}.pdf"})
    return out


def text_of(doc):
    """Pages set upright; two-up landscape pages halved and ordered by printed page number (batch2.halves, for
    booklet prints); portrait pages in file order. Each page or half read top to bottom (sort=True)."""
    for page in doc:
        if page.rotation:
            page.remove_rotation()
    if any(p.rect.width > p.rect.height for p in doc):
        return "\f".join(h.page.get_text("text", clip=h.rect, sort=True) for h in readpdf.batch2.halves(doc))
    return "\f".join(p.get_text("text", sort=True) for p in doc)


def whole_text(full):
    """From the title (the line before 'Being an Act', else the enacting formula) to the end; page numbers and running
    heads (a short line on at least a third of the pages) dropped; a word hyphenated at a line end joined."""
    lines = [re.sub(r"\s+", " ", l).strip() for l in full.splitlines()]
    lines = [l for l in lines if l]
    i = next((k for k, l in enumerate(lines) if re.match(r"(?i)being an act", l)), None)
    if i is None:
        i = next((k for k, l in enumerate(lines) if re.search(r"(?i)\benacted by\b", l)), 0)
    else:
        i = max(0, i - 1)
    body = lines[i:]
    pages = max(1, full.count("\f") + 1)
    cnt, heads = {}, {}
    for l in body:
        cnt[l] = cnt.get(l, 0) + 1
        h = re.sub(r"\d+", "#", l)
        heads[h] = heads.get(h, 0) + 1
    keep = []
    for l in body:
        if re.fullmatch(r"[ivxlc\d]{1,4}", l, re.I):
            continue
        h = re.sub(r"\d+", "#", l)  # running head with the page number: "2 No. 6 Goods and Services Tax Act 2009"
        if "No. #" in h and len(l) <= 120 and heads[h] >= max(3, pages / 3):
            continue
        if len(l) <= 60 and cnt[l] >= max(3, pages / 3) and not re.match(r"^\(?[a-z0-9]{1,4}[).]", l):
            continue
        if keep and keep[-1].endswith("-") and not keep[-1].endswith(" -") and re.match(r"^[a-z]", l):
            keep[-1] = keep[-1][:-1] + l
        else:
            keep.append(l)
    return keep


def complete(full):
    i = full.find("ENACTED")
    if i < 0:
        m = re.search(r"(?i)\benacted by\b", full)
        i = m.start() if m else -1
    if i < 0:
        return None, "no enacting formula found"
    arr = full[:i]
    toc = [int(x) for x in re.findall(r"(?m)^\s*(\d{1,3})\s*\.", arr)]
    body = full[i:]
    want = max(toc) if toc else None
    pos, k = 0, 0
    while True:
        # at a line start, or after the side note printed on the same line ("Interpretation. 1. In this Act")
        m = re.compile(r"(?m)^(?:[^\n]{0,80}?[.\-]\s+|\s*)%d\s*\.\s*(?:\(1\)|[A-Z\"(“]|$)" % (k + 1)).search(body, pos)
        if not m:
            break
        k += 1; pos = m.end()
    if want:
        if k < want:
            return None, f"sections found in order 1..{k}, Arrangement lists {want} (pages missing or unreadable)"
        return k, None
    if k < 2:
        return None, f"no Arrangement and only {k} section numbers found in order"
    return k, None


def meta_of(full):
    norm = re.sub(r"\s+", " ", full)
    m = re.search(r"Supplement\s+to\s+the\s+Sierra\s+Leone\s+Gazette\s+(?:Extra?o?r?dinary\s+)?(?:Vol\.\s*[A-Z]+,?\s*)?"
                  r"No\.\s*(\d+)\s+(?:dated|of)\s+(\d+)(?:st|nd|rd|th)?\s+([A-Za-z]+),?\s+(\d{4})", norm)
    gz = m.groups() if m and m.group(3).lower() in build2.MONTHS else None
    sg = re.search(r"SIGNED\s+this\s+(\d+)(?:st|nd|rd|th)?\s+day\s+of\s+([A-Za-z]+),?\s+(\d{4})", norm, re.I)
    br = re.search(r"\[\s*([^\]]{0,80}?)\s*\]\s*(?:BE IT )?ENACTED", full, re.S)
    return gz, (build2.date_of(" ".join(sg.groups())) if sg else None), (br.group(1) if br else None)


def build(repo, dry=False):
    have = build2.existing(repo)
    seen = {p.name for p in Path(repo).iterdir()}
    items, held = {}, []
    for c in candidates():
        b = c["path"].read_bytes()
        try:
            doc = fitz.open(stream=b, filetype="pdf")
        except Exception as e:
            held.append((c["k"], c["title"], f"PDF: {e}")); continue
        chars = sum(len(p.get_text("text").strip()) for p in doc)
        if chars < 200 * len(doc) * 0.2:
            held.append((c["k"], c["title"], "no text layer")); continue
        ocr = sum(1 for p in doc if p.get_images()) > len(doc) / 2
        ptexts = [re.sub(r"\s+", " ", p.get_text("text")).strip() for p in doc]
        dup = [t for t in set(ptexts) if len(t) > 200 and ptexts.count(t) > 1]
        if dup:
            held.append((c["k"], c["title"], "a page is repeated in the copy")); continue
        sorted_text = text_of(doc)  # sets the pages upright too
        variants = [sorted_text, readpdf.batch2.page_text(doc).replace("\n", "\n"),
                    "\f".join(p.get_text("text") for p in doc)]
        full, plain = sorted_text, variants[2]
        if "num" not in c:
            idt = build2.ident(plain) or build2.ident(full)
            m = re.search(r"(\d{4})", c["title"])
            if idt:
                c["num"], c["year"] = idt[0], idt[1]
            else:
                mm = re.fullmatch(r"slweb/Laws/(\d{4})-0*(\d+)[ps]?\.pdf", c["k"])
                if not mm:
                    held.append((c["k"], c["title"], "no Act number found")); continue
                c["year"], c["num"] = int(mm.group(1)), int(mm.group(2))
        key = (c["year"], c["num"])
        if not c["num"]:
            held.append((c["k"], c["title"], "no Act number printed")); continue
        if key in have:
            continue
        n, why, best = None, None, 0
        for v in variants:  # the reading order that shows the most sections in order, the upright one on a tie
            nv, w = complete(v)
            why = why or w
            if nv is not None and nv > best:
                n, full, best = nv, v, nv
        # without an Arrangement, a reading that stops early is not proof of the whole: every reading must agree
        if n is not None and not re.findall(r"(?m)^\s*(\d{1,3})\s*\.", full[:max(0, full.find("ENACTED"))]):
            if any((complete(v)[0] or 0) > n for v in variants):
                n = None; why = "readings disagree on the number of sections"
        if n is None:
            held.append((c["k"], c["title"], why)); continue
        text = whole_text(full)
        alltext = " ".join(text)
        gz, signed, br = meta_of(full)
        brd = build2.date_of(br)
        if not brd and LATER.search(alltext):
            held.append((c["k"], c["title"], "commencement left to a later order; its date is not in the print")); continue
        if brd:
            day, basis = brd, f"date of commencement printed on the Act: [{br.strip()}]"
        elif gz:
            day = build2.iso(gz[1], gz[2], gz[3])
            basis = f"no commencement date printed; Gazette No. {gz[0]} of {day}, in force on publication (Constitution s. 106(3))"
        elif c.get("expr"):
            day, basis = c["expr"], f"SierraLII expression date {c['expr']} (the Act as published)"
        elif c.get("eif"):
            day, basis = c["eif"], f"no date printed; WIPO Lex records entry into force on {c['eif']} ({c['record']})"
        else:
            held.append((c["k"], c["title"], "no commencement date and no Gazette date printed")); continue
        if not brd and signed and day < signed:
            held.append((c["k"], c["title"], f"in-force date {day} before the signing date {signed}")); continue
        rank = {"parl": 0, "sierralii": 1, "slweb": 2, "faolex": 3, "wipo": 4}[c["src"]]
        it = dict(c, day=day, basis=basis, text=text, sections=n, ocr=ocr, signed=signed,
                  gazette=f"Supplement to the Sierra Leone Gazette No. {gz[0]} of {build2.iso(gz[1], gz[2], gz[3])}" if gz else None,
                  sha=hashlib.sha256(b).hexdigest(), rank=rank)
        if key not in items or rank < items[key]["rank"]:
            items[key] = it
    items = sorted(items.values(), key=lambda x: (x["day"], x["year"], x["num"]))
    for it in items:
        t = re.sub(r"\s+", " ", it["title"]).strip()
        t = re.sub(r"^The \.\s*", "", t).replace("Sierr a Leone", "Sierra Leone")
        it["title"] = t if t.lower().startswith("the ") else "The " + t
        it["folder"] = slug_of(it["title"])
        while it["folder"] in seen:
            it["folder"] += f"-{it['year']}"
        seen.add(it["folder"])
    if dry:
        for it in items:
            print(it["day"], it["year"], it["num"], it["src"], "ocr" if it["ocr"] else "digital", it["folder"],
                  it["sections"], len(it["text"]), it["basis"][:70])
        for h in held:
            print("HELD", *h)
        return items, held
    done = []
    for it in items:
        d = Path(repo) / it["folder"]
        d.mkdir()
        body = f"# {it['title']}\n\n" + "\n\n".join(it["text"]) + "\n"
        (d / "text.md").write_bytes(body.encode("utf8"))
        label = f"Act No. {it['num']} of {it['year']}"
        pre70 = it["day"] < "1970-01-01"
        stamp = "1970-01-01T12:00:00+0000" if pre70 else f"{it['day']}T12:00:00+0000"
        via = {"parl": "the Parliament of Sierra Leone's copy of the Government Printing Department print, read from an "
                       "Internet Archive capture (parliament.gov.sl no longer answers)",
               "slweb": "the Sierra Leone Web copy of the Government Printing Department print (a secondary compilation)",
               "faolex": "FAOLEX's copy of the Government Printing Department print (a secondary copy)",
               "wipo": "WIPO Lex's copy of the Act (a secondary copy)",
               "sierralii": "the print SierraLII publishes for the Act"}[it["src"]]
        srcl = f"Source: {it['url']}\n"
        if it["src"] == "parl":
            srcl = f"Source: {it['cdx']['original'].replace(':80/', '/')}\nArchived-copy: {it['url']}\n"
        if it.get("record"):
            srcl += f"Record: {it['record']}\n"
        status = {"slweb": f"Source-status: secondary copy ({build2.SLWEB})\n",
                  "faolex": "Source-status: secondary copy (FAOLEX, https://faolex.fao.org)\n",
                  "wipo": "Source-status: secondary copy (WIPO Lex, https://www.wipo.int/wipolex)\n"}.get(it["src"], "")
        msg = (f"{it['title']} as enacted ({label})" + (f", in force {it['day']}" if pre70 else "") + "\n\n"
               f"{it['title']}: the whole text as printed, in one file (text.md), from {via}; read from the PDF's text "
               f"layer. Its sections could not be split one per file, so the Act is kept whole; sections 1 to "
               f"{it['sections']} were found in order (the Arrangement of Sections, where printed, ends at the same "
               "number).\n\n"
               f"Law: {label}\nKind: law\nLayout: whole text\n" + (f"Enacted: {it['signed']}\n" if it["signed"] else "")
               + (f"Published: {it['gazette']}\n" if it["gazette"] else "")
               + f"In-force: {it['day']}\nIn-force-basis: {it['basis']}\n" + srcl + status
               + ("Text-source: publisher OCR\n" if it["ocr"] else "")
               + f"Source-sha256: {it['sha']}\nAct: {it['title']}\nProvisions: 1\n")
        env = dict(os.environ, GIT_AUTHOR_NAME=label, GIT_AUTHOR_EMAIL=f"act-{it['year']}-{it['num']}@sierra-leone-law.invalid",
                   GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp, GIT_COMMITTER_NAME="Lexifina",
                   GIT_COMMITTER_EMAIL="sierra-leone-law@lexifina.com")
        subprocess.run(["git", "-C", repo, "add", "--", it["folder"]], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-q", "-F", "-"], input=msg.encode(), env=env, check=True)
        done.append(it)
    (ROOT / "build6_result.json").write_text(json.dumps(
        {"committed": [{k: v for k, v in it.items() if k not in ("text", "path", "cdx")} for it in done],
         "held": held}, indent=1, default=str))
    print(len(done), "committed;", len(held), "held")


if __name__ == "__main__":
    build(sys.argv[1], "--dry" in sys.argv)
