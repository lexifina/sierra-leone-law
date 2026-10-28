# How this repository was made (Sierra Leone)

This file is written by the build on 2026-10-28, the day the source data was retrieved. Everything below is enough to rebuild this repository hash for hash.

## Sources

| Source | Address | Retrieved | Requests | Licence |
| --- | --- | --- | ---: | --- |
| Parliament of Sierra Leone (parliament.gov.sl), through the Internet Archive | <https://www.parliament.gov.sl> | 2026-10-28 | 5 | Acts of Parliament of Sierra Leone; parliament.gov.sl states no licence. The 1991 text and the 2001 Act are Sierra Leone Web (sierra-leone.org) transcriptions that Parliament publishes. |
| SierraLII (Sierra Leone Legal Information Institute, on the Laws.Africa Peachjam platform) | <https://sierralii.gov.sl> | 2026-10-28 | 58 | CC BY-NC 4.0, crediting SierraLII as the source (https://sierralii.gov.sl/terms-of-use/, s. 9) |
| Common Crawl and the Internet Archive Wayback Machine | <https://commoncrawl.org> | 2026-10-28 | None | Archived copies; the content licence is the original publisher's. Common Crawl data is used under its terms of use (https://commoncrawl.org/terms-of-use). |

Every response is cached by the sha256 of its URL, and the table above lists every source with its retrieval date. Lexifina keeps its fetch scripts privately; `tools/parse.py` reads only the cache and writes `corpus.json`, so the same cache always gives the same corpus.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | The Constitution of Sierra Leone, 1991 | 5 | 1991-10-01 to 2016-06-16 |
| `employment` | Employment Act, 2023 | 1 | 2023-05-11 to 2023-05-11 |

The build made 6 commits:

| Commits | Kind |
| ---: | --- |
| 2 | first version of an act |
| 4 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-28.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 6 laws in the record.
- 12 tags.

## Dates

Each commit is dated at noon (Africa/Freetown) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Constitution of Sierra Leone, 1991, s. 106(3): "An Act signed by the President shall come into operation on the date of its publication in the Gazette or such other date as may be prescribed therein or in any other enactment." SierraLII versions keep SierraLII's own expression date (the Gazette publication of the act, or the commencement date SierraLII states). https://web.archive.org/web/20210814090237id_/https://www.parliament.gov.sl/uploads/other_resources/2-Sierra%20Leone%201991%20Constitution.pdf

## Commands, in order

```sh
# fill the cache from the sources listed above (network; Lexifina's fetch scripts are kept privately)
python -X utf8 tools/parse.py                  # cache -> corpus.json (no network)
python -X utf8 tools/build.py <folder> --repo <empty folder> --docs-date 2026-10-28
python -X utf8 tools/check_repo.py <repo> --corpus <folder>/corpus.json --write
python -X utf8 tools/build.py <folder> --repo <another empty folder> --docs-date 2026-10-28 --compare <repo>
```

In the main Lexifina repository these files live as follows:
- `fetch.py`, `parse.py` and `repo/`: in `scripts/sierra-leone-law/`.
- `build.py`, `check_repo.py` (`check.py` there) and `on.py`: in `scripts/gitlaw_common/`, with the corpus format in `SCHEMA.md`.

## Exact inputs

- `corpus.json` sha256 `62ccfe3d91f7c4ca80401ffc710b14eaf498f47c31e28a2c2d7f5f1bf1240ea7` (446685 bytes)
- Script blob hashes (`git hash-object`):

| Script | Blob |
| --- | --- |
| build.py | `2bfc4ac9df193a7be844556d7f69cdb9d93ec3f2` |
| check.py | `cd346c7ff9996d450240e3bab52bcae03b2bc865` |
| on.py | `644a6c0857fbcc72562032b58d57aa113fee0641` |
| fetch.py | `4ffa6e56d2c1932495133339a2c263a319866e83` |
| parse.py | `c37eccd4c1e0a15dda48d1234f8f264c928072ca` |

- Tools:
  - Python 3.14.0
  - git version 2.52.0.windows.1
  - curl 8.21.0 (Windows) libcurl/8.21.0 Schannel zlib/1.3.2 WinIDN WinLDAP

## Checks

1 versions of 1 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

A second build from the same corpus into an empty folder gave identical hashes for all 1 history commits and 2 tags (history tip `b1013885ba9425ba4eb3e9fb5aaae07e531e4fd2`).

These results are from the check run on the build before this one, from the same corpus.

## Decisions made by hand

- Constitution: SierraLII does not publish the 1991 Constitution and no consolidated point-in-time text of it is published anywhere we could read, so its history is rebuilt from Parliament's own PDFs (parliament.gov.sl, read through Internet Archive id_ captures because the site serves an invalid TLS certificate): the Constitution as enacted, then each amending Act replayed on it by code written for its instructions.
- Constitution: the 1991 text is the Sierra Leone Web transcription that Parliament publishes (uploads/other_resources/2-Sierra Leone 1991 Constitution.pdf). Parliament's other copy (uploads/acts/THE CONSTITUTION OF SIERRA LEONE 1991.pdf, the same transcription) lost its subsection numbers in conversion and was not used. The transcription prints paragraph letters as "a.", "b."; the amending Acts print "(a)"; each is kept as its source prints it.
- Constitution: chapter and part headings, the Arrangement of Sections and the page heads are not provisions and are left out (34 heading lines). A marginal note beside a section's first line is its heading; other marginal notes (citations such as "Act No. 12 of 1978") are kept as "[Margin: ...]" lines at the end of the section they sit beside.
- Constitution: each version is dated by the amending Act's stated commencement date or, where the Act leaves it blank, its Gazette publication date (Constitution s. 106(3)); 1 October 1991 is the Constitution's own commencement (s. 192).
- Constitution: quotation marks that delimit inserted wording in the amending Acts are dropped, and a word broken at a hyphen across lines is joined; the wording is otherwise as printed.
- Constitution: not in this history, because their only copies are scans without a text layer: the Constitution of Sierra Leone Amendment Decree, 1997 and The Constitution Reinstatement (1996) on parliament.gov.sl. The suspension of the Constitution under military rule (1992-1996, 1997-1998) is not recorded.
- Constitution: not applied, so the last version is not today's text: the Constitution of Sierra Leone (Amendment) Act, 2022 (Act No. 22 of 2022; Gazette No. 89 of 22 December 2022; renames the Political Parties Registration Commission and amends ss. 34 and 35), whose only copy on parliament.gov.sl is a scan with an unusable OCR layer (no OCR is done here); and a Constitution of Sierra Leone (Amendment) Act, 2022 amending s. 32(2) and (8), whose only copy is an unnumbered, undated print, so no in-force date can be sourced. The 2017, 2018, 2021 and 2022 (s. 76) texts on parliament.gov.sl are Bills, not enacted Acts, and are not applied. For these reasons the Constitution is not published to main.
- SierraLII publishes about 80 acts (2026-10-28 listing), each as one expression: the act as published. It holds no consolidated point-in-time versions and not the Constitution of 1991, so each SierraLII act here has one version, credited to the act itself.
- Licence and terms: SierraLII licenses primary and secondary law content CC BY-NC 4.0, crediting SierraLII as the source (terms s. 9); its terms (s. 4) say "Scraping and bulk downloading from this website is strictly prohibited"; its robots.txt sends Content-Signal ai-train=no, search=yes, ai-input=no and Crawl-delay 5. No SierraLII document page was fetched: every version is read from an archived copy (Common Crawl or the Internet Archive). The user decided on 2026-10-28 that reading archived copies is acceptable (relayed by the coordinator: "scraping wayback is fair game, dont overdo it"). The repository stays private; CC BY-NC allows only non-commercial use. No legal text was given to a model.
- Cyber Security and Crime Act, 2021 (Act 7 of 2021) is not built: SierraLII holds it only as a PDF (source.pdf, 11.5 MB) with no Akoma Ntoso text; all 18 archived captures of its expression page (2023-06 to 2026-05) show only the PDF viewer.
- Version dates are SierraLII's expression dates. Laws.Africa's terminology guide (https://docs.laws.africa/getting-started/terminology-guide) says "Amendments to Principal works come into force on the Commencement date of the Amending work" and that the first point in time is "the work as originally published"; so an amendment's expression is dated by its commencement (in force), and an act's original expression by its publication, which is replaced by the commencement date the page states.
- Credits: a version whose History names exactly one amending law (and no consolidation) between it and the previous version is credited to that law for every provision that changed. Otherwise a provision is credited only to laws that SierraLII's editorial note inside that provision links to; the rest are unexplained (publisher).
- Editorial notes (akn-remark) are left out of the text and used only as credit evidence, except where a provision has no other text (repealed or spent), where the note is the provision's whole printed content.
- Part, Chapter and Division headings are left out; each provision file starts with its own number and heading. Every other text of each version is in a provision file: parse.py checks this per version (verification.json, fidelity).

## What AI did and did not do

The fetch, parse and check scripts were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above, through code that anyone can rerun.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote the configuration and the Constitution replay script and chose the acts. No model wrote, summarised or transformed legal text: parse.py and constitution.py are deterministic code, and the amendment instructions are applied by code written for each instruction.
