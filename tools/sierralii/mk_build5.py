"""Write tools/build5.py: build2 for FAOLEX copies (secondary), with build4's orphan gate."""
from pathlib import Path
T = Path(__file__).resolve().parent
s = (T / "build2.py").read_text("utf8")
s = s.replace('"""Append Acts read from Parliament of Sierra Leone prints',
              '"""(build5: FAOLEX copies; generated from build2.py by mk_build5.py.) Append Acts read from Parliament of Sierra Leone prints', 1)
old_cand = s[s.index("def candidates():"):s.index("def build(repo")]
new_cand = '''def candidates():
    """FAOLEX records (cache3/faolex/rec) and their PDFs, copied under cache2/faolex/ so build2's paths hold."""
    import shutil
    survey, urls = {}, {}
    (ROOT / "cache2" / "faolex").mkdir(exist_ok=True)
    for p in sorted((ROOT / "cache3" / "faolex" / "rec").glob("*.json")):
        d = json.loads(p.read_text("utf8"))
        for f in d.get("links_to_full_text") or []:
            src = ROOT / "cache3" / "faolex" / "pdf" / f
            if not src.exists():
                continue
            dst = ROOT / "cache2" / "faolex" / f
            if not dst.exists():
                shutil.copyfile(src, dst)
            try:
                doc = fitz.open(dst)
            except Exception:
                continue
            chars = sum(len(pg.get_text("text").strip()) for pg in doc)
            imgs = sum(1 for pg in doc if pg.get_images())
            kind = "scan" if chars < 100 * max(1, len(doc)) else ("ocr" if imgs > len(doc) / 2 else "digital")
            k = "faolex/" + f
            survey[k] = {"kind": kind, "pages": len(doc)}
            urls[k] = ("faolex", "https://faolex.fao.org/docs/pdf/" + f, {"record": d.get("_url")})
    return survey, urls


'''
s = s.replace(old_cand, new_cand)
old_else = s[s.index('        else:\n            via = "the Sierra Leone Web copy'):s.index("        msg = (")]
new_else = '''        else:
            via = ("FAOLEX's copy of the Government Printing Department print (FAO's legal database, a secondary "
                   "copy)")
            srcl = f"Source: {it['url']}\\nRecord: {it['cdx']['record']}\\n"
            status = "Source-status: secondary copy (FAOLEX, https://faolex.fao.org)\\n"
'''
s = s.replace(old_else, new_else)
s = s.replace('ROOT / "build2_result.json"', 'ROOT / "build5_result.json"')
s = s.replace("import readpdf  # noqa", "import readpdf  # noqa\nimport build4  # noqa: F401  (second reading + orphan gate)")
assert "build4" in s and "FAOLEX's copy" in s and "build5_result" in s
(T / "build5.py").write_text(s, "utf8")
print("ok")
