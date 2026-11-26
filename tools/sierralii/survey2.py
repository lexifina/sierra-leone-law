"""Classify every PDF in ../cache2 and try the side-note reader on it. Writes ../survey2.json.

kind: digital (text layer, few page images) | ocr (page images + a text layer: publisher's OCR) | scan (no layer)
"""
import json, re, sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fitz  # noqa
fitz.TOOLS.mupdf_display_errors(False)
import readpdf  # noqa


def classify(b):
    d = fitz.open(stream=b, filetype="pdf")
    t = " ".join(p.get_text("text") for p in d)
    toks = re.findall(r"[A-Za-z]+", t)
    imgs = sum(1 for p in d if p.get_images())
    if len(toks) < 50 * len(d) * 0.3:
        return "scan", len(d), 0.0
    good = sum(1 for w in toks if re.search(r"[aeiouyAEIOUY]", w) and (w.islower() or w.istitle() or w.isupper()))
    return ("ocr" if imgs > len(d) / 2 else "digital"), len(d), round(good / len(toks), 3)


def main():
    out = {}
    old = {}
    sp = ROOT / "survey2.json"
    if sp.exists():
        old = json.loads(sp.read_text())
    files = sorted(p for p in (ROOT / "cache2").rglob("*.pdf"))
    for f in files:
        k = f.relative_to(ROOT / "cache2").as_posix()
        if k in old and old[k].get("size") == f.stat().st_size:
            out[k] = old[k]; continue
        b = f.read_bytes()
        rec = {"size": len(b)}
        try:
            rec["kind"], rec["pages"], rec["clean"] = classify(b)
        except Exception as e:
            rec["kind"] = f"bad {type(e).__name__}"
            out[k] = rec; continue
        if rec["kind"] == "digital":
            try:
                units, rep, meta = readpdf.read(b)
                if units is None:
                    rec["read"] = rep.get("error")
                else:
                    secs = [x for x in units if re.fullmatch(r"sec-\d{3}", x)]
                    nums = [int(x[4:]) for x in secs]
                    rec.update(sections=len(secs), seq=nums == list(range(1, len(nums) + 1)), toc=rep["toc_last"],
                               missing=rep["n_missing"], added=rep["n_added"], gazette=meta.get("gazette"),
                               signed=meta.get("signed"), bracket=meta.get("commencement_bracket"),
                               title_line=meta.get("title_line"))
            except Exception as e:
                rec["read"] = f"{type(e).__name__}: {e}"[:120]
        out[k] = rec
        print(k[:70], {x: rec.get(x) for x in ("kind", "pages", "sections", "toc", "missing", "added", "read")}, flush=True)
    sp.write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
