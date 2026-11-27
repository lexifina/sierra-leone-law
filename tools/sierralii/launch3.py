"""Start a tools/ script detached (no window, below-normal priority): python tools/launch3.py <name> [args...]"""
import subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
name = sys.argv[1]
p = subprocess.Popen([sys.executable, "-X", "utf8", "-u", "-W", "ignore", str(ROOT / "tools" / f"{name}.py"), *sys.argv[2:]],
                     cwd=ROOT, stdout=open(ROOT / f"{name}.out", "w"), stderr=subprocess.STDOUT,
                     creationflags=0x08000000 | 0x00004000 | 0x00000008)
(ROOT / f"{name}.pid").write_text(str(p.pid))
print(p.pid)
