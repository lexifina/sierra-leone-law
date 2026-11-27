"""QA every Act folder in the law repo: flag sections whose body holds another section's start line
("7. Members ...", "8. (1) The ...") or that have no body, and Acts with reader orphans.

    python -X utf8 tools/qa3.py <repo>
"""
import json, re, sys
from pathlib import Path

repo = Path(sys.argv[1])
ROOT = Path(__file__).resolve().parent.parent
orph = {}
for line in (ROOT / "orphans3.out").read_text("utf8").splitlines() if (ROOT / "orphans3.out").exists() else []:
    line = line.strip("\ufeff ").strip()
    if " " not in line:
        continue
    f, n = line.rsplit(" ", 1)
    orph[f] = int(n)
out = {}
for d in sorted(p for p in repo.iterdir() if p.is_dir() and not p.name.startswith((".", "tools", "data"))):
    secs = sorted(d.glob("sec-*.md"))
    if not secs:
        continue
    n = len(secs)
    bad = []
    for f in secs:
        own = int(re.match(r"sec-(\d+)", f.stem).group(1))
        lines = f.read_text("utf8").splitlines()
        body = [l for l in lines[1:] if l.strip()]
        if not body:
            bad.append((f.stem, "empty"))
            continue
        for l in body:
            m = re.match(r"^(\d{1,3})\.\s+(?:\(1\)\s+)?[A-Z\"]", l)
            if m and int(m.group(1)) != own and 1 <= int(m.group(1)) <= n:
                bad.append((f.stem, "holds " + l[:50]))
                break
    if bad or orph.get(d.name):
        out[d.name] = {"sections": n, "bad": bad[:6], "n_bad": len(bad), "orphans": orph.get(d.name, 0)}
for k, v in out.items():
    print(k, v["sections"], v["n_bad"], v["orphans"], v["bad"][:3])
print(len(out), "flagged")
(ROOT / "qa3.json").write_text(json.dumps(out, indent=1))
