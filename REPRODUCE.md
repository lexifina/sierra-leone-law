# How this repository was made (Sierra Leone)

This file is written by the build on 2026-10-29, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| SierraLII (Sierra Leone Legal Information Institute, on the Laws.Africa Peachjam platform) | <https://sierralii.gov.sl> | 2026-10-28 | CC BY-NC 4.0, crediting SierraLII as the source (https://sierralii.gov.sl/terms-of-use/, s. 9) |
| Internet Archive Wayback Machine | <https://commoncrawl.org> | 2026-10-28 | Archived copies; the content licence is the original publisher's. |
| Government Printing Department, Sierra Leone: The Cyber Security and Crime Act, 2021 (Gazette No. 71, 2021-11-25) | <https://www.parliament.gov.sl/uploads/acts/THE%20CYBER%20SECURITY%20AND%20CRIME%20ACT,%202021.pdf> | 2026-10-29 | Act of the Parliament of Sierra Leone as printed by the Government Printing Department; the copy states no licence. |
| Government Printing Department, Sierra Leone: The Customary Land Rights Act, 2022 (Gazette No. 69, 2022-09-23) | <https://www.parliament.gov.sl/uploads/acts/THE%20CUSTOMARY%20LAND%20RIGHTS%20ACT,%202022.pdf> | 2026-10-29 | Act of the Parliament of Sierra Leone as printed by the Government Printing Department; the copy states no licence. |
| Government Printing Department, Sierra Leone: The National Land Commission Act, 2022 (Gazette No. 69, 2022-09-23) | <https://www.parliament.gov.sl/uploads/acts/THE%20NATIONAL%20LAND%20COMMISSION%20ACT,%202022.pdf> | 2026-10-29 | Act of the Parliament of Sierra Leone as printed by the Government Printing Department; the copy states no licence. |
| Government Printing Department, Sierra Leone: The Anti-Human Trafficking and Migrant Smuggling Act, 2022 (Gazette No. 51, 2022-07-21) | <https://www.parliament.gov.sl/uploads/acts/ANTI-HUMAN%20TRAFFICKIING%20AND%20MIGRANT%20ACT,2022.pdf> | 2026-10-29 | Act of the Parliament of Sierra Leone as printed by the Government Printing Department; the copy states no licence. |
| Government Printing Department, Sierra Leone: The Banking Act, 2019 (Gazette No. 51, 2019-06-27) | <https://www.parliament.gov.sl/uploads/acts/THE%20BANKING%20ACT%202019.pdf> | 2026-10-29 | Act of the Parliament of Sierra Leone as printed by the Government Printing Department; the copy states no licence. |
| Government Printing Department, Sierra Leone: The National Investment Board Act, 2022 (Gazette No. 49, 2022-07-14) | <https://www.parliament.gov.sl/uploads/acts/THE%20NATIONAL%20INVESTMENT%20BOARD%20ACT%202022.pdf> | 2026-10-29 | Act of the Parliament of Sierra Leone as printed by the Government Printing Department; the copy states no licence. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `employment` | Employment Act, 2023 | 1 | 2023-05-11 to 2023-05-11 |
| `cyber-security-crime` | The Cyber Security and Crime Act, 2021 | 1 | 2021-11-25 to 2021-11-25 |
| `customary-land-rights` | The Customary Land Rights Act, 2022 | 1 | 2022-09-23 to 2022-09-23 |
| `national-land-commission` | The National Land Commission Act, 2022 | 1 | 2022-09-23 to 2022-09-23 |
| `anti-human-trafficking` | The Anti-Human Trafficking and Migrant Smuggling Act, 2022 | 1 | 2022-07-21 to 2022-07-21 |
| `banking` | The Banking Act, 2019 | 1 | 2019-06-27 to 2019-06-27 |
| `national-investment-board` | The National Investment Board Act, 2022 | 1 | 2022-07-14 to 2022-07-14 |

The build made 7 commits:

| Commits | Kind |
| ---: | --- |
| 7 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-29.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 7 laws in the record.
- 14 tags.

## Dates

Each commit is dated at noon (Africa/Freetown) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Constitution of Sierra Leone, 1991, s. 106(3): "An Act signed by the President shall come into operation on the date of its publication in the Gazette or such other date as may be prescribed therein or in any other enactment." SierraLII versions keep SierraLII's own expression date (the Gazette publication of the act, or the commencement date SierraLII states). https://web.archive.org/web/20210814090237id_/https://www.parliament.gov.sl/uploads/other_resources/2-Sierra%20Leone%201991%20Constitution.pdf

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `791b3b816b79707c3beff294f04bb630f43a73ac177d5077562dad6fd37e1a0f` (653424 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3d00541d258745461ab52b1b0cb4e1716a27a95d`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

7 versions of 7 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

A second build from the same corpus into an empty folder gave identical hashes for all 7 history commits and 14 tags (history tip `ae45809ea79c5bd63562fcb55b525717f8ff3f47`).

## Decisions made by hand

- SierraLII publishes about 80 acts (2026-10-28 listing), each as one expression: the act as published. It holds no consolidated point-in-time versions and not the Constitution of 1991, so each SierraLII act here has one version, credited to the act itself.
- Licence: SierraLII licenses primary and secondary law content CC BY-NC 4.0, crediting SierraLII as the source (terms s. 9); CC BY-NC allows only non-commercial use. Every version is read from an archived copy. No legal text was given to a model.
- Cyber Security and Crime Act, 2021 (Act 7 of 2021) is not built: SierraLII holds it only as a PDF (source.pdf, 11.5 MB) with no Akoma Ntoso text; all 18 archived captures of its expression page (2023-06 to 2026-05) show only the PDF viewer.
- Version dates are SierraLII's expression dates. Laws.Africa's terminology guide (https://docs.laws.africa/getting-started/terminology-guide) says "Amendments to Principal works come into force on the Commencement date of the Amending work" and that the first point in time is "the work as originally published"; so an amendment's expression is dated by its commencement (in force), and an act's original expression by its publication, which is replaced by the commencement date the page states.
- Credits: a version whose History names exactly one amending law (and no consolidation) between it and the previous version is credited to that law for every provision that changed. Otherwise a provision is credited only to laws that SierraLII's editorial note inside that provision links to; the rest are unexplained (publisher).
- Editorial notes (akn-remark) are left out of the text and used only as credit evidence, except where a provision has no other text (repealed or spent), where the note is the provision's whole printed content.
- Part, Chapter and Division headings are left out; each provision file starts with its own number and heading. Every other text of each version is in a provision file: this is checked per version (verification.json, fidelity).
- The Cyber Security and Crime Act, 2021: one version, the Act as passed (Parliament) and signed by the President on 2021-11-15, printed as a supplement to Gazette No. 71 of 2021-11-25. Its date of commencement is left blank in the print ("[ ]"), so it is in force from its publication in the Gazette, 2021-11-25 (Constitution of Sierra Leone, 1991, s. 106(3)). 58 sections, as the Arrangement of Sections lists.
- The Customary Land Rights Act, 2022: one version, the Act as passed (Parliament) and signed by the President on 2022-09-06, printed as a supplement to Gazette No. 69 of 2022-09-23. Its date of commencement is left blank in the print ("[ ]"), so it is in force from its publication in the Gazette, 2022-09-23 (Constitution of Sierra Leone, 1991, s. 106(3)). 48 sections, as the Arrangement of Sections lists.
- The National Land Commission Act, 2022: one version, the Act as passed (Parliament) and signed by the President on 2022-09-06, printed as a supplement to Gazette No. 69 of 2022-09-23. Its date of commencement is left blank in the print ("[ ]"), so it is in force from its publication in the Gazette, 2022-09-23 (Constitution of Sierra Leone, 1991, s. 106(3)). 91 sections, as the Arrangement of Sections lists.
- The Anti-Human Trafficking and Migrant Smuggling Act, 2022: one version, the Act as passed (Parliament) and signed by the President on 2022-07-18, printed as a supplement to Gazette No. 51 of 2022-07-21. Its date of commencement is left blank in the print ("[ ]"), so it is in force from its publication in the Gazette, 2022-07-21 (Constitution of Sierra Leone, 1991, s. 106(3)). 39 sections, as the Arrangement of Sections lists.
- The Banking Act, 2019: one version, the Act as passed (Parliament) and signed by the President on 2019-06-17, printed as a supplement to Gazette No. 51 of 2019-06-27. Its date of commencement is left blank in the print ("[ ]"), so it is in force from its publication in the Gazette, 2019-06-27 (Constitution of Sierra Leone, 1991, s. 106(3)). 125 sections, as the Arrangement of Sections lists.
- The National Investment Board Act, 2022: one version, the Act as passed (Parliament) and signed by the President on 2022-07-04, printed as a supplement to Gazette No. 49 of 2022-07-14. Its date of commencement is left blank in the print ("[ ]"), so it is in force from its publication in the Gazette, 2022-07-14 (Constitution of Sierra Leone, 1991, s. 106(3)). 53 sections, as the Arrangement of Sections lists; section(s) 18 have no side note, so their files start "# Section N" with no heading.
- Batch 2 acts (Government Printing Department prints): no Act amending any of them appears in the Parliament of Sierra Leone's published lists of Acts and Bills (Internet Archive captures to April 2026), so each enacted text is taken as today's text. The annual Finance Acts, which can amend other Acts, were not read word for word (the 2024 ones are image scans).
- Batch 2 acts: read from the PDFs' text layer (two printed pages per PDF page, each read as its own page, in printed page order: some prints are imposed as a booklet). Side notes give the section headings; Part headings are left out of the provision files; section and subsection numbers printed in the margin are body text; a section number printed without its full stop ("2 (1)", "9 (1)") is read as a section number. Every printed word from the enacting formula to "Passed in Parliament" is in a provision file, a Part heading or the printer's colophon, and none is added (verification-batch2.json). Spelling errors in the prints are kept as printed.
- Batch 2 acts: the prints' right margin is ragged, so a line that does not end in a full stop, semicolon, colon or dash and runs close to the margin is joined to the next one; a sentence carried over to the next page is joined too. The Cyber Security and Crime Act's section 43 side note ("Electronic signature.") stands at the top of the next page, too far from the section for the reader to pair them; it is set as the section's heading by hand.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote the configuration and the Constitution replay code and chose the acts. No model wrote, summarised or transformed legal text: the code is deterministic, and the amendment instructions are applied by code written for each instruction.
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote Lexifina's code and the Sierra Leone changes to the vendored Lexifina's code, and chose the sources. No model wrote, summarised or transformed legal text: the reader is deterministic code reading the PDFs' text layer.
