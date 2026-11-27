"""Write STRUCTURE.md for the law repo: the layout, and the list of whole-text Acts (from git, Layout: whole text).

    python -X utf8 tools/structure6.py <repo>
"""
import re, subprocess, sys
from pathlib import Path

repo = Path(sys.argv[1])
log = subprocess.run(["git", "-C", str(repo), "log", "--reverse", "--format=%x1e%B"], capture_output=True,
                     text=True, encoding="utf8").stdout
rows = []
for msg in log.split("\x1e"):
    if "Layout: whole text" not in msg:
        continue
    act = re.search(r"^Act: (.+)$", msg, re.M).group(1)
    law = re.search(r"^Law: (.+)$", msg, re.M).group(1)
    day = re.search(r"^In-force: (.+)$", msg, re.M).group(1)
    sec = "secondary copy" if "Source-status:" in msg else "official print"
    folder = None
    for d in repo.iterdir():
        t = d / "text.md"
        if t.exists() and t.read_text("utf8").startswith(f"# {act}\n"):
            folder = d.name
    if folder:
        rows.append((folder, act, law, day, sec))
rows.sort()
out = ["# Structure", "",
       "One folder per law at the top level, named after its short title (`employment/`, `companies/`); a second law "
       "with the same name gets its year (`finance-2016/`). The Constitution is `constitution/`.", "",
       "- **By section** (most Acts): one file per section, `sec-NNN.md` (`sec-071.md` is section 71), plus "
       "`sch-NN.md` for schedules and `README.md` listing the provisions.",
       "- **Whole text** (the Acts listed below): one file, `text.md`, holding the Act as printed from its title to "
       "the printer's colophon, where the print's text layer is complete but could not be split into one file per "
       "section (side notes printed on the same line as the section number, two-column prints, Appropriation "
       "schedules). Their commits carry `Layout: whole text`. Each was checked to hold sections 1 to N in order, N "
       "being the last number of the printed Arrangement of Sections, and no repeated page; copies with missing "
       "pages are not here.", "",
       "Each version is one commit dated noon (Africa/Freetown, GMT) on the day it took effect, with `In-force:` and "
       "`In-force-basis:` trailers; see README.md.", "",
       f"## Whole-text Acts ({len(rows)})", "",
       "| Folder | Act | Law | In force | Source |", "| --- | --- | --- | --- | --- |"]
out += [f"| `{f}/` | {a} | {l} | {d} | {s} |" for f, a, l, d, s in rows]
(repo / "STRUCTURE.md").write_bytes(("\n".join(out) + "\n").encode("utf8"))
print(len(rows), "whole-text Acts")
