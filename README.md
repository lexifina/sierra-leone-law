# Sierra Leone: law history in git

The law of Sierra Leone as a git history: one file per provision, one commit per law on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to a provision; `tools/on.py` gives the text in force on any day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `sl/`.

**What is in it now**

| Folder | Act | Versions | History | Source |
| --- | --- | ---: | --- | --- |
| `constitution/` | [The Constitution of Sierra Leone, 1991](https://web.archive.org/web/20210814090237id_/https://www.parliament.gov.sl/uploads/other_resources/2-Sierra%20Leone%201991%20Constitution.pdf) | 5 | 1991-10-01 to 2016-06-16 | Parliament of Sierra Leone PDFs, replayed |
| `employment/` | [Employment Act, 2023](https://sierralii.gov.sl/akn/sl/act/2023/15) | 1 | 2023-05-11 to 2023-05-11 | SierraLII |
| `banking/` | [The Banking Act, 2019](https://www.parliament.gov.sl/uploads/acts/THE%20BANKING%20ACT%202019.pdf) | 1 | 2019-06-27 to 2019-06-27 | Government Printing Department print (Parliament of Sierra Leone) |
| `cyber-security-crime/` | [The Cyber Security and Crime Act, 2021](https://www.parliament.gov.sl/uploads/acts/THE%20CYBER%20SECURITY%20AND%20CRIME%20ACT,%202021.pdf) | 1 | 2021-11-25 to 2021-11-25 | Government Printing Department print (Parliament of Sierra Leone) |
| `customary-land-rights/` | [The Customary Land Rights Act, 2022](https://www.parliament.gov.sl/uploads/acts/THE%20CUSTOMARY%20LAND%20RIGHTS%20ACT,%202022.pdf) | 1 | 2022-09-23 to 2022-09-23 | Government Printing Department print (Parliament of Sierra Leone) |
| `national-land-commission/` | [The National Land Commission Act, 2022](https://www.parliament.gov.sl/uploads/acts/THE%20NATIONAL%20LAND%20COMMISSION%20ACT,%202022.pdf) | 1 | 2022-09-23 to 2022-09-23 | Government Printing Department print (Parliament of Sierra Leone) |
| `anti-human-trafficking/` | [The Anti-Human Trafficking and Migrant Smuggling Act, 2022](https://www.parliament.gov.sl/uploads/acts/ANTI-HUMAN%20TRAFFICKIING%20AND%20MIGRANT%20ACT,2022.pdf) | 1 | 2022-07-21 to 2022-07-21 | Government Printing Department print (Parliament of Sierra Leone) |
| `national-investment-board/` | [The National Investment Board Act, 2022](https://www.parliament.gov.sl/uploads/acts/THE%20NATIONAL%20INVESTMENT%20BOARD%20ACT%202022.pdf) | 1 | 2022-07-14 to 2022-07-14 | Government Printing Department print (Parliament of Sierra Leone) |

**The Constitution of Sierra Leone, 1991**

| In force | Author |
| --- | --- |
| 1991-10-01 | Act No. 6 of 1991 (as enacted) |
| 2002-02-07 | Act No. 15 of 2001 |
| 2008-07-31 | Act No. 9 of 2008 |
| 2014-01-09 | Act No. 5 of 2013 |
| 2016-06-16 | Act No. 10 of 2016 |

**Employment Act, 2023**

| In force | Author |
| --- | --- |
| 2023-05-11 | Act 15 of 2023 (as enacted) |

## Sources

The Banking Act, 2019, the Cyber Security and Crime Act, 2021 and four Acts of 2022 (Customary Land Rights, National Land Commission, Anti-Human Trafficking and Migrant Smuggling, National Investment Board) are each the Act as passed and signed, read from the Government Printing Department's print that the Parliament of Sierra Leone publishes (text layer, no OCR). Each is in force from its publication in the Gazette, since its date of commencement is left blank (Constitution, s. 106(3)). No amending Act to any of them appears in Parliament's lists of Acts and Bills, so each text is taken as today's text; the annual Finance Acts were not read word for word.

- **The Constitution** is not on SierraLII, and no consolidated, dated text of it is published anywhere we could read. Its history is rebuilt from the Parliament of Sierra Leone's own PDFs (parliament.gov.sl, which publishes the Constitution as enacted and the amending Acts with a text layer): each amending Act's instructions are applied by code to the text before it, and the new wording is read from the Act's own PDF. Each PDF is read from its Internet Archive copy, pinned by capture time and sha256. The 1991 text and the 2001 Act are Sierra Leone Web (sierra-leone.org) transcriptions that Parliament publishes.
- **Other acts** are SierraLII's (Sierra Leone Legal Information Institute, on the Laws.Africa Peachjam platform). SierraLII publishes about 80 acts, each as one expression, the act as published; it has no point-in-time consolidations. Each page is read from an archived copy, pinned in `tools/sources.json`.

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
- SierraLII acts: the Internet Archive's index of every archived SierraLII page holds exactly one expression of each act (SierraLII's listing itself is not read: only archived copies are), and that expression is the version here.

## Licence

- SierraLII content: Source: SierraLII (https://sierralii.gov.sl), licensed under the Creative Commons Attribution-NonCommercial 4.0 International licence (CC BY-NC 4.0). The repository is private: CC BY-NC 4.0 allows only non-commercial use.
- Acts of Parliament from parliament.gov.sl: no licence is stated there; they are public legislation.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist, so `git blame` and `git log --author` name laws. The committer is always Lexifina.

This repository is not legal advice.
