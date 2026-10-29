# Sierra Leone: law history in git

The law of Sierra Leone as a git history: one file per provision, one commit per law on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to a provision; `tools/on.py` gives the text in force on any day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `sl/`.

**What is in it now**

| Folder | Act | Versions | History | Source |
| --- | --- | ---: | --- | --- |
| `constitution/` | [The Constitution of Sierra Leone, 1991](https://web.archive.org/web/20210814090237id_/https://www.parliament.gov.sl/uploads/other_resources/2-Sierra%20Leone%201991%20Constitution.pdf) | 5 | 1991-10-01 to 2016-06-16 | Parliament of Sierra Leone PDFs, replayed |

**The Constitution of Sierra Leone, 1991**

| In force | Author |
| --- | --- |
| 1991-10-01 | Act No. 6 of 1991 (as enacted) |
| 2002-02-07 | Act No. 15 of 2001 |
| 2008-07-31 | Act No. 9 of 2008 |
| 2014-01-09 | Act No. 5 of 2013 |
| 2016-06-16 | Act No. 10 of 2016 |

## Sources

- **The Constitution** is not on SierraLII, and no consolidated, dated text of it is published anywhere we could read. Its history is rebuilt from the Parliament of Sierra Leone's own PDFs (parliament.gov.sl, which publishes the Constitution as enacted and the amending Acts with a text layer): each amending Act's instructions are applied by code to the text before it, and the new wording is read from the Act's own PDF. Parliament's site serves an invalid TLS certificate, so each PDF is read from its Internet Archive copy, pinned by capture time and sha256. The 1991 text and the 2001 Act are Sierra Leone Web (sierra-leone.org) transcriptions that Parliament publishes.

## What is missing

- Constitution: the Constitution of Sierra Leone (Amendment) Act, 2022 (Act No. 22 of 2022, Gazette of 22 December 2022; Political Parties Regulation Commission, ss. 34 and 35): its only copy is a scan whose OCR layer is unusable, and no OCR is done here.
- Constitution: a Constitution of Sierra Leone (Amendment) Act, 2022 amending s. 32(2) and (8) (Electoral Commission): its only copy is an unnumbered, undated print, so no in-force date can be sourced.
- Constitution: the Constitution of Sierra Leone Amendment Decree, 1997 and the Constitution Reinstatement (1996): scans only. The suspension of the Constitution under military rule is not recorded.
- Constitution: because of these, its last version (2016) is not today's text; the Constitution is on the `preview` branch only.
- SierraLII acts: one version each (the act as published); later amendments are not on SierraLII.

## Dates

- Each commit is dated at **noon, Africa/Freetown, on the day the change took effect**; the day is also in the `In-force:` trailer, which the tools read.
- An Act of Parliament comes into operation on its publication in the Gazette, or on the date it prescribes (Constitution, s. 106(3)). Each Constitution version is dated by the amending Act's stated commencement or, where the Act leaves it blank, its Gazette date; the Constitution itself commenced on 1 October 1991 (s. 192). SierraLII acts are dated by SierraLII's expression date or its stated commencement.
- `--before="YYYY-MM-DD"` alone uses your clock's time of day; use `T23:59:59Z`, or the tool.

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did section 38 say on 2010-01-01? | `python tools/on.py 2010-01-01 constitution sec-038` |
| Which law wrote each line? | `git blame constitution/sec-079.md` |
| Every change, word by word | `git log -p --word-diff constitution/sec-038.md` |
| Every law in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |
| Everything one law changed | `git show law/<key>` |

## How it is checked

- Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`); both must match `corpus.json`. Results are in `REPRODUCE.md`.
- Constitution: the 1991 parse keeps every character of the source's body text (page heads, the Arrangement of Sections, and chapter and part headings aside); each replayed amendment changes exactly the provisions its Act names.
- SierraLII acts: the last version is the expression SierraLII's own listing names as current.

## Licence

- SierraLII content: Source: SierraLII (https://sierralii.gov.sl), licensed under the Creative Commons Attribution-NonCommercial 4.0 International licence (CC BY-NC 4.0). The repository is private: CC BY-NC 4.0 allows only non-commercial use.
- Acts of Parliament from parliament.gov.sl: no licence is stated there; they are public legislation.
- Archived copies come from the Internet Archive and Common Crawl (https://commoncrawl.org/terms-of-use).

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist, so `git blame` and `git log --author` name laws. The committer is always Lexifina.

This repository is not legal advice.
