"""build2 with a second reading for prints whose section starts the side-note reader missed.

    python -X utf8 tools/build4.py <repo> [--dry]

Second reading: a line that starts with the next section number ("26. ...") opens that section even when the line
before looks like it runs on (gazette.starts_para), so one missed start no longer swallows the rest of the Act.
It is accepted only under stricter gates than build2's: an Arrangement of Sections is printed and its last number
equals the sections read (run 1..N), every printed word is kept and none added, and no body line is left outside a
section (orphans). Everything else is as build2 (dates, layout, commit messages).
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build2  # noqa: E402
import readpdf  # noqa: E402

g = readpdf.g
_starts_para = g.starts_para


def starts_para(prev, ln, t):
    if g.SEC.match(t) or g.SEC_DASH.match(t):
        return True
    return _starts_para(prev, ln, t)


_split = g.split_units
_read = readpdf.read
CAP = {}


def split_units(*a, **k):
    units, rep = _split(*a, **k)
    CAP["orphans"] = list(rep["orphans"])
    return units, rep


def read(b, allow_ocr=False):
    CAP.clear()
    units, rep, meta = _read(b, allow_ocr=allow_ocr)
    if units is None:
        return units, rep, meta
    if CAP.get("orphans"):
        return None, {"error": f"second reading: {len(CAP['orphans'])} body lines outside any section"}, meta
    if not rep.get("toc_last"):
        return None, {"error": "second reading needs a printed Arrangement of Sections"}, meta
    return units, rep, meta


g.starts_para = starts_para
g.split_units = split_units
readpdf.read = read

if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    res = root / "build2_result.json"
    before = json.loads(res.read_text())
    keep = [h for h in before["held"] if str(h[2]).startswith("withdrawn")]
    build2.build(sys.argv[1], "--dry" in sys.argv)
    if "--dry" not in sys.argv:
        after = json.loads(res.read_text())
        after["held"] += keep
        res.write_text(json.dumps(after, indent=1))
