"""For each committed build2/build3 Act, rerun the reader and list body lines left outside any section (orphans)."""
import json, sys, warnings
from pathlib import Path
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fitz  # noqa
fitz.TOOLS.mupdf_display_errors(False)
import readpdf  # noqa

res = json.loads((ROOT / "build2_result.json").read_text())
for c in res["committed"]:
    b = (ROOT / "cache2" / c["k"]).read_bytes()
    units, rep, meta = readpdf.read(b, allow_ocr=c["kind"] == "ocr")
    if rep["orphans"]:
        print(c["folder"], rep["orphans"])
