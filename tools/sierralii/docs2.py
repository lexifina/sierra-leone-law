"""Update sierra-leone-law README.md, REPRODUCE.md and LICENSE in place from build2_result.json (re-runnable)."""
import collections, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
repo = Path(sys.argv[1])
res = json.loads((ROOT / "build2_result.json").read_text())
com, held = res["committed"], res["held"]
n_parl = sum(1 for c in com if c["src"] == "parl")
n_web = sum(1 for c in com if c["src"] == "slweb")
n_fao = sum(1 for c in com if c["src"] == "faolex")
n_ocr = sum(1 for c in com if c["kind"] == "ocr")
total = 43 + len(com)
first = min([c["year"] for c in com] + [2007])


def sub(text, pat, new):
    out, n = re.subn(pat, lambda m: new, text, count=1, flags=re.M)
    if n != 1:
        raise SystemExit(f"pattern not found: {pat[:60]}")
    return out


r = (repo / "README.md").read_text("utf8")
r = sub(r, r"^\*\*What is in it now:\*\*.*$",
        f"**What is in it now:** the Constitution of Sierra Leone, 1991 with its amendments to 2016 (5 versions), and "
        f"{total} Acts as enacted, {first} to 2024: 37 from SierraLII (its Akoma Ntoso text, or the text layer of the print "
        f"it publishes), {6 + n_parl} from Government Printing Department prints that Parliament published, {n_web} "
        f"from the same prints as copied by Sierra Leone Web, and {n_fao} as copied by FAOLEX (both secondary copies; "
        f"each such commit says so). Each Act "
        f"is held as enacted, one version; scanned Acts without a text layer are not here. [`REPRODUCE.md`](REPRODUCE.md) "
        f"lists every act with its source and what is held back.")
r = sub(r, r"^- History is append-only:.*$",
        "- History is append-only: no merge commits, no commit rewritten, and none dated after the build. Acts are "
        "added in batches, so a later batch can hold Acts older than the one before it.")
r = sub(r, r"^- \*\*Most Sierra Leonean law\.\*\*.*$",
        f"- **Most Sierra Leonean law.** {total} Acts are here. Held back: scans with no text layer (no OCR is done), "
        "prints the side-note reader cannot yet split by section (most amending Acts and Appropriation Acts), Acts that "
        "leave their commencement to a later order whose date is not printed, prints with no Gazette or commencement "
        "date, and subordinate legislation. Most of the Laws of Sierra Leone, 1960 and the Acts of 1961 to 2000 exist "
        "only as scans. No bill is held.")
r = sub(r, r"^\| \[Parliament of Sierra Leone\].*$",
        f"| [Parliament of Sierra Leone](https://www.parliament.gov.sl) | Acts as passed and signed, printed by the "
        f"Government Printing Department | no, the Act as enacted | {6 + n_parl} Acts, read from the PDFs' text layer "
        f"(no OCR), each from an Internet Archive copy (the site no longer answers) |")
if "Sierra Leone Web" not in r.split("## Sources", 1)[1].split("## Licence", 1)[0]:
    r = re.sub(r"(^\| \[SierraLII\]\(https://sierralii\.gov\.sl\).*$)",
               lambda m: m.group(1) + "\n| [Sierra Leone Web](https://www.sierra-leone.org/laws.html) | copies of the "
               "Government Printing Department prints, collected since 1996 (secondary) | no, the Act as enacted | "
               f"{n_web} Acts not found in an official copy with a text layer; commits carry `Source-status: secondary "
               "copy`, and `Text-source: publisher OCR` where the copy is a scan with its own text layer |",
               r, count=1, flags=re.M)
else:
    r = sub(r, r"^\| \[Sierra Leone Web\].*$",
            "| [Sierra Leone Web](https://www.sierra-leone.org/laws.html) | copies of the Government Printing Department "
            f"prints, collected since 1996 (secondary) | no, the Act as enacted | {n_web} Acts not found in an official "
            "copy with a text layer; commits carry `Source-status: secondary copy`, and `Text-source: publisher OCR` "
            "where the copy is a scan with its own text layer |")
r = sub(r, r"^See \[`LICENSE`\]\(LICENSE\)\..*$",
        "See [`LICENSE`](LICENSE). SierraLII licenses its content under CC BY-NC 4.0, crediting SierraLII as the source "
        "(its terms of use, section 9), so its texts may be used only for non-commercial purposes; parliament.gov.sl "
        "and Sierra Leone Web state no licence for the Acts they publish (Acts of Parliament; Sierra Leone Web's "
        "copyright notice covers its own site). Lexifina's own contributions (the arrangement of the history, the "
        "commit messages, the tables and the tools) are CC0 1.0.")
(repo / "README.md").write_text(r, "utf8", newline="\n")

# REPRODUCE: one section, regenerated
p = repo / "REPRODUCE.md"
t = p.read_text("utf8")
H = "## Parliament prints and Sierra Leone Web (2026-11-26)"
reasons = collections.Counter(re.sub(r"\d+", "N", h[2] or "") for h in held)
sec = [H, "",
       "`tools/sierralii/fetch2.py` read the Parliament of Sierra Leone's /uploads/acts/ and /uploads/statutory_instruments/",
       "PDFs from Internet Archive captures (parliament.gov.sl answers 503, or with an invalid certificate), and the PDFs",
       "Sierra Leone Web lists on www.sierra-leone.org/laws.html and ordinances.html (live; a secondary compilation, no",
       "robots.txt, no terms beyond its copyright notice). One request in flight per host, at least 1 s apart.",
       "`tools/sierralii/build2.py <repo>` then appends one commit per Act, with the same layout, reader and word check",
       "as `build_leg.py`, and these rules:",
       "",
       "- an Act already here (same number and year) is skipped; a Parliament copy wins over the Sierra Leone Web copy;",
       "- sections must run 1..N and N must equal the Arrangement of Sections; a print with no Arrangement is held",
       "  unless it reads at least one section per 1.5 pages;",
       "- in-force day: the date of commencement printed on the Act; else its Gazette date (Constitution s. 106(3)); an",
       "  Act that leaves commencement to a later order, or prints no date, or a Gazette date before its signing, is",
       "  held;",
       "- a Sierra Leone Web copy carries `Source-status: secondary copy (Sierra Leone Web, ...)`; a scan whose PDF",
       "  already carries a text layer is read from that layer and carries `Text-source: publisher OCR` (no OCR by",
       "  Lexifina); a Parliament copy carries `Source` (the Parliament URL) and `Archived-copy` (the capture read);",
       "- an Act in force before 1970 is stamped 1970-01-01 (git cannot store earlier dates), with its real day in the",
       "  subject and the `In-force` trailer.",
       "",
       f"Committed: {len(com)} Acts ({n_parl} Parliament, {n_web} Sierra Leone Web, {n_ocr} of them from a publisher's OCR layer):",
       ""]
for c in sorted(com, key=lambda c: (c["year"], c["num"])):
    sec.append(f"- Act No. {c['num']} of {c['year']} {c['title']} (`{c['folder']}/`, in force {c['day']}, "
               f"{'Parliament' if c['src'] == 'parl' else 'Sierra Leone Web'}{', publisher OCR' if c['kind'] == 'ocr' else ''})")
sec += ["", f"Held ({len(held)} files; a file can be a second copy of an Act):", ""]
for k, n in reasons.most_common():
    sec.append(f"- {n}: {k}")
sec.append("")
block = "\n".join(sec) + "\n"
if H in t:
    t = re.sub(re.escape(H) + r".*?(?=\n## |\Z)", lambda m: block.rstrip("\n") + "\n", t, count=1, flags=re.S)
else:
    t = t.replace("\n## What AI did and did not do", "\n" + block + "\n## What AI did and did not do", 1)
p.write_text(t, "utf8", newline="\n")

lic = repo / "LICENSE"
L = lic.read_text("utf8")
if "Acts marked Source-status" not in L:
    L = L.rstrip("\n") + "\n\nActs marked Source-status: secondary copy come from Sierra Leone Web\n" \
        "(https://www.sierra-leone.org/laws.html), an independent site that has collected copies of the\n" \
        "Government Printing Department prints since 1996. They are Acts of Parliament; the site states no\n" \
        "licence for them (its notice \"(c) 1996-2024 Sierra Leone Web\" covers the site). Other Acts come from\n" \
        "the Parliament of Sierra Leone's own copies, read from the Internet Archive; parliament.gov.sl states\n" \
        "no licence. The wording of each Act was not changed.\n"
    lic.write_text(L, "utf8", newline="\n")
print("docs updated", total, n_parl, n_web, len(held))
