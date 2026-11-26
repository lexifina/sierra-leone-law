"""Read one SierraLII source.pdf (Government Printing Department print) into section units, via the
sierra-leone-law gazette.py side-note reader (text layer only, no OCR). Mirrors batch2.read_act for any PDF."""
import collections, re, sys
from pathlib import Path

SLD = r"C:\Users\alany\Documents\lexifina\scripts\sierra-leone-law"
sys.path.insert(0, SLD)
import batch2  # noqa: E402  (sets gazette WIDE_MIN / NOTE_SIZE for A5 prints)
import gazette as g  # noqa: E402


def read(b: bytes):
    import fitz
    doc = fitz.open(stream=b, filetype="pdf")
    chars = sum(len(p.get_text("text").strip()) for p in doc)
    if chars < 200 * max(1, len(doc)) * 0.2:
        return None, {"error": "no text layer", "pages": len(doc), "chars": chars}, {}
    if sum(1 for p in doc if p.get_images()) > len(doc) / 2:
        return None, {"error": "scan (its text layer is someone's OCR; no OCR text is used)", "pages": len(doc)}, {}
    for page in doc:
        if page.rotation:
            page.remove_rotation()
    hs = batch2.halves(doc)
    pages = g.read_pages(hs, 0, len(hs) - 1, head_max_y=72, hang=45,
                         sides={k: ("R" if h.rect.x0 > 0 else "L") for k, h in enumerate(hs)})
    body = " ".join(l.text for p in pages.values() for l in p.body)
    vocab = set(re.findall(r"[a-z]+", body.lower()))
    hyph = set(re.findall(r"[a-z]+-[a-z]+", body.lower()))
    full = batch2.page_text(doc)
    start = re.compile(r"^(?:BE IT )?ENACTED by|^ENACTED by")
    units, rep = g.split_units(pages, start, re.compile(r"^Passed in Parliament"),
                               re.compile(r"^(?:[A-Z]+ +)?SCHEDULE(?!S)\b"), drop_rx=g.COLOPHON)
    out, headings = {}, []
    for u in units:
        if u.heading and u.kind == "sec":
            u.heading = g.dehyphen(u.heading, vocab, hyph)
            headings.append(u.heading)
        if u.kind == "schedule":
            m = re.match(r"^((?:[A-Z]+ +)?SCHEDULE)", u.heading or "")
            u.label = re.sub(r"\s+", " ", m.group(1)).title() if m else u.label
        out[u.key] = {"label": u.label, "kind": u.kind, "text": re.sub(r" {2,}", " ", g.unit_text(u))}
    printed = collections.Counter(rep["words"])
    ours = collections.Counter()
    for k, uu in out.items():
        head, _, rest = uu["text"].partition("\n")
        ours.update(re.findall(r"\w+", rest))
        if k.startswith("sch-"):
            ours.update(re.findall(r"\w+", head))
        elif k.startswith("sec-"):
            ours.update([re.sub(r"^0+", "", k[4:7]) + k[8:].upper()])
    for t in rep["structure_lines"] + rep["dropped"]:
        ours.update(re.findall(r"\w+", t))
    secs = [k for k in out if k.startswith("sec-")]
    toc = re.findall(r"(?m)^\s*(\d{1,3})\.\s*$", full.split("ENACTED by")[0])
    report = {"units": len(out), "sections": len(secs), "last_section": secs[-1] if secs else None,
              "toc_last": max(map(int, toc)) if toc else None,
              "no_heading": rep["no_heading"], "orphans": len(rep["orphans"]),
              "words_printed": sum(printed.values()), "words_kept": sum(ours.values()),
              "words_missing": sorted((printed - ours).items())[:20],
              "words_added": sorted((ours - printed).items())[:20],
              "n_missing": sum((printed - ours).values()), "n_added": sum((ours - printed).values())}
    m = re.search(r"Supplement\s+to\s+the\s+Sierra\s+Leone\s+Gazette\s+(?:Extra?o?r?dinary\s+)?Vol\.\s*[A-Z]+,?\s*"
                  r"No\.\s*(\d+)\s+dated\s+(\d+)(?:st|nd|rd|th)?\s+([A-Za-z]+),?\s+(\d{4})", full)
    signed = re.search(r"SIGNED\s+this\s+(\d+)(?:st|nd|rd|th)?\s+day\s+of\s+([A-Za-z]+),?\s+(\d{4})", full)
    br = re.search(r"\[\s*([^\]]{0,80}?)\s*\]\s*(?:BE IT )?ENACTED", full, re.S)
    meta = {"pages": len(doc), "gazette": m.groups() if m else None, "signed": signed.groups() if signed else None,
            "commencement_bracket": br.group(1) if br else None,
            "title_line": next((l.strip() for l in full.splitlines() if re.search(r"Act,?\s+\d{4}", l)), None)}
    return out, report, meta


if __name__ == "__main__":
    import glob, json
    res = {}
    for f in sorted(glob.glob(str(Path(__file__).resolve().parent.parent / "cache/akn/sl/act/**/source.pdf"), recursive=True)):
        try:
            out, rep, meta = read(open(f, "rb").read())
        except Exception as e:
            rep, meta = {"error": f"{type(e).__name__}: {e}"[:200]}, {}
        res[f.split("cache")[1]] = {"report": rep, "meta": meta}
        print(f.split("act")[-1][:40], {k: rep.get(k) for k in ("error", "sections", "toc_last", "n_missing", "n_added")}, meta.get("gazette"), flush=True)
    Path(__file__).resolve().parent.parent.joinpath("pdf_report.json").write_text(json.dumps(res, indent=1, default=str))
