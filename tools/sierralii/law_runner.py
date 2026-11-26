"""Detached: every 30 min while fetch2 runs (and once after it exits), survey new PDFs, append readable Acts to the
law repo (build2), update README/REPRODUCE/LICENSE (docs2), commit the docs and push fast-forward."""
import os, shutil, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
REPO = str(ROOT / "law")
NW = 0x08000000
LOG = open(ROOT / "progress.log", "a", encoding="utf8", buffering=1)
def log(m): LOG.write(time.strftime("%Y-%m-%dT%H:%M:%S ") + "law_runner: " + m + "\n")
def run(*a, **k): return subprocess.run(list(a), capture_output=True, text=True, creationflags=NW, cwd=ROOT, **k)
def alive(pid): return str(pid) in run("tasklist", "/FI", f"PID eq {pid}", "/NH").stdout
pid = int((ROOT / "fetch2.pid").read_text().strip())
env = dict(os.environ, GIT_AUTHOR_NAME="Lexifina", GIT_AUTHOR_EMAIL="sierra-leone-law@lexifina.com",
           GIT_COMMITTER_NAME="Lexifina", GIT_COMMITTER_EMAIL="sierra-leone-law@lexifina.com")
while True:
    running = alive(pid)
    py = [sys.executable, "-X", "utf8", "-W", "ignore"]
    run(*py, "tools/survey2.py")
    before = run("git", "-C", REPO, "rev-parse", "HEAD").stdout.strip()
    b = run(*py, "tools/build2.py", REPO)
    after = run("git", "-C", REPO, "rev-parse", "HEAD").stdout.strip()
    if after != before:
        run(*py, "tools/docs2.py", REPO)
        for f in ("build2.py", "fetch2.py", "docs2.py", "survey2.py", "readpdf.py"):
            shutil.copy(ROOT / "tools" / f, Path(REPO) / "tools" / "sierralii" / f)
        run("git", "-C", REPO, "add", "-A")
        run("git", "-C", REPO, "commit", "-q", "-m", "README, REPRODUCE.md: more Acts from Parliament prints and "
            "Sierra Leone Web copies", "-m", "Kind: docs", env=env)
        p = run("git", "-C", REPO, "push", "-q", "origin", "main")
        ls = run("git", "-C", REPO, "ls-remote", "origin", "refs/heads/main").stdout.split()[:1]
        log(f"{b.stdout.strip()[-80:]} pushed {ls} {p.returncode}")
    else:
        log(f"nothing new ({b.stdout.strip()[-60:]})")
    if not running:
        log("fetch2 finished; last pass done"); break
    time.sleep(1800)
