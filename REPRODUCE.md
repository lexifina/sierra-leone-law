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
- Builder blob hashes (`git hash-object`): `build.py` `0fad90cf931c453951234ecf904d05ee79f3ec7e`, `check.py` `5d719354ea4c62d240c93d2cae446307d81d9e81`, `on.py` `aff48cf1b68d50c7ba8f399ca32261871c301824`.
- Python 3.14.4; git version 2.53.0.

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

## SierraLII, read live (2026-11-26)

`tools/sierralii/fetch.py` read SierraLII directly (not archived copies): the legislation sitemap (106 texts: 94 Acts, 9
Statutory and 3 Constitutional Instruments), each text's page, and its `source.pdf` where the page has no Akoma Ntoso
text. One request at a time, 5 s apart, as SierraLII's robots.txt asks (Crawl-delay: 5); its robots.txt also disallows
/judgments/ and sets Content-Signal ai-train=no, ai-input=no; robots.txt is treated as advisory here, and no model is
trained on or given the text. No 429 or 5xx was seen. `tools/sierralii/build_leg.py <repo>` then appends one commit per Act:

- folder: the short title in English (Sierra Leone's language of law), without "Act", the year and small words
  (`arbitration/`, `public-financial-management/`); Statutory/Constitutional Instruments would go under `si-`/`ci-`;
- one file per section (`sec-NNN.md`), schedule (`sch-NN.md`) and the long title;
- commit dated noon Freetown (GMT, +0000) on the in-force day; author the Act itself (`Act No. 18 of 2022
  <act-2022-18@sierralii.invalid>`); trailers `In-force`, `In-force-basis`, `Enacted`, `Published`, `Source`,
  `Source-sha256`;
- in-force day: SierraLII's "Commenced on" date; else a commencement date printed on the Act; else its Gazette date
  (Constitution s. 106(3): an Act without a stated commencement comes into operation on publication).

Text: SierraLII's HTML (read with `peachjam.units_of`), or for a page with only a PDF, the PDF's text layer read by the
side-note reader (`gazette.py`, as for the Government Printing Department prints). A PDF Act is committed only if
every printed word from the enacting formula to "Passed in Parliament" is kept, none added, and the sections run 1..N
as the Arrangement of Sections lists. Scans are not read (no OCR, and no OCR layer made by others). The Constitution
of Sierra Leone (Amendment) Act, 2013 is not a folder of its own: it is replayed in `constitution/`.

Committed: 36 Acts. Held (63):

- act/1972/18 Consular Fees (Amendment) Act, 1972: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1972/19 Administration of Estates (Amendment) Act, 1972: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1972/20 Non-Citizens (Registration, Immigration and Expulsion) (Amendment) (No. 2) Act, 1972: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1972/21 West African Examinations Council Act, 1972: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1972/22 University of Sierra Leone Act, 1972: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1972/23 Income Tax (Amendment) Act, 1972: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1972/24 Electoral Provisions (Political Parties) (Repeal) Act, 1972: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1976/19 Treasury Bills (Amendment) Act, 1976: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1976/1 Constitution (Amendment) Act, 1976: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1976/20 Bank of Sierra Leone (Amendment) Act, 1976: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1976/21 Customs Tariff (Amendment) Act, 1976: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1976/2 Election of President of Sierra Leone Act, 1976: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1976/3 Courts (Amendment) Act, 1976: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1976/4 Local Tax (Amendment) Act, 1976: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1977/10 Airports (Service Charges) (Amendment) (No. 2) Act, 1977: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1977/11 National Registration (Amendment) Act, 1977: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1977/12 Constitution (Amendment) Act, 1977: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/1977/9 Airports (Service Charges) (Amendment) Act, 1977: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/2012/10 Patents and Industrial Designs Act, 2012: sections read 80 (sequential: True) vs Arrangement 75
- act/2017/11 National Medical Supplies Agency Act, 2017: sections read 25 (sequential: True) vs Arrangement 24
- act/2017/6 Guma Valley Water Company Act, 2017: sections read 62 (sequential: True) vs Arrangement 69
- act/2019/5 Bank of Sierra Leone Act, 2019: sections read 77 (sequential: True) vs Arrangement 79
- act/2019/7 Civil Aviation Act, 2019: sections read 121 (sequential: True) vs Arrangement 130
- act/2020/6 Supplementary Appropriation Act, 2020: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/2021/2 Appropriation Act, 2021: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/2021/8 Sierra Leone Students&#x27; Loan Scheme Act, 2021: scanned PDF, no text layer (no OCR)
- act/2022/16 National Communications Authority Act, 2022: scanned PDF, no text layer (no OCR)
- act/2022/17 Public Elections Act, 2022: scanned PDF, no text layer (no OCR)
- act/2022/1 Finance Act, 2022: scanned PDF, no text layer (no OCR)
- act/2022/21 National Revenue Authority Act, 2022: scanned PDF, no text layer (no OCR)
- act/2022/22 Constitution of Sierra Leone (Amendment) Act, 2022: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/2022/2 Appropriation Act, 2022: scanned PDF, no text layer (no OCR)
- act/2022/3 Allied Health Professions Act, 2022: scanned PDF, no text layer (no OCR)
- act/2022/5 Sierra Leone Meterological Agency (Amendment) Act, 2022: scanned PDF, no text layer (no OCR)
- act/2022/9 Professional Engineering Regulatory Council Act, 2022: scanned PDF, no text layer (no OCR)
- act/2023/11 Work Permit Act, 2023: scanned PDF, no text layer (no OCR)
- act/2023/12 Overseas Employment and Migrant Workers Act, 2023: scanned PDF, no text layer (no OCR)
- act/2023/17 Public Health Act, 2022: scanned PDF, no text layer (no OCR)
- act/2023/19 Wages and Compensation Commission Act, 2023: scanned PDF, no text layer (no OCR)
- act/2023/20 National Development-Induced Resettlement Act, 2023: scanned PDF, no text layer (no OCR)
- act/2023/21 Sierra Leone Public Transport Authority Act, 2023: scanned PDF, no text layer (no OCR)
- act/2023/25 Tax and Duty Exemption Act, 2023: scanned PDF, no text layer (no OCR)
- act/2023/28 Sierra Leone Agricultural Research Institute Act, 2023: scanned PDF, no text layer (no OCR)
- act/2023/29 Sierra Leone Ports and Harbours Authority Act, 2023: scanned PDF, no text layer (no OCR)
- act/2023/30 Supplementary Appropriation Act, 2023: scanned PDF, no text layer (no OCR)
- act/2023/3 Appropriation Act, 2023: scanned PDF, no text layer (no OCR)
- act/2023/9 Sierra Leone Nursing and Midwifery Council Act, 2023: scanned PDF, no text layer (no OCR)
- act/2024/1 Finance Act, 2024: scanned PDF, no text layer (no OCR)
- act/2024/2 Appropriation Act, 2024: scanned PDF, no text layer (no OCR)
- act/2024/4 Anti-Money Laundering and Combating of Financing of Terrorism and Financing of Proliferation of Weapons of Mass Destruction Act, 2024: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/2025/2 Appropriation Act, 2025: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/ci/2018/64 Commission of Inquiry (Examination, Inquiry and Investigation) Notice (1), 2018: scanned PDF, no text layer (no OCR)
- act/ci/2024/7 Drug and Substance Abuse Public Emergency Response Regulations, 2024: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/ci/2024/9 Commencement of Second Session of the Sixth Parliament of the Second Republic of Sierra Leone: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/si/2022/11 Independent Media Commission (Print and Electonic Media) Regulations, 2022: scanned PDF, no text layer (no OCR)
- act/si/2022/14 Public Elections (District Block Proportional Representation System) Regulations, 2022: scanned PDF, no text layer (no OCR)
- act/si/2022/6 Legal Practitioners (Pupillage) Regulations, 2021: scanned PDF, no text layer (no OCR)
- act/si/2022/9 Right to Access Information Regulations, 2022: scanned PDF, no text layer (no OCR)
- act/si/2022/national-payment-systems-oversight National Payment Systems Oversight Regulations, 2022: scanned PDF, no text layer (no OCR)
- act/si/2023/10 Employment Regulations, 2023: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/si/2024/10 Sierra Leone Road Safety Authority (Driving Licence and Miscellaneous Services Fees) Regulations, 2024: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/si/2024/11 Sierra Leone Mines and Minerals Development and Management Corporation (Allocated Minerals and Mineral-Related Assets) Regulations, 2024: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)
- act/si/2024/4 Redenomination of the Leone Regulations, 2024: no enacting formula found in the text layer (scan with an OCR layer, or a layout the reader does not know)

The Constitution's history (1991 to 2016, 5 versions) was moved from the `preview` branch to `main` on 2026-11-26,
commit for commit (same authors, dates and messages, plus an `In-force-basis` trailer); its 2022 amendments remain
missing, as above.

## Parliament prints and Sierra Leone Web (2026-11-26)

`tools/sierralii/fetch2.py` read the Parliament of Sierra Leone's /uploads/acts/ and /uploads/statutory_instruments/
PDFs from Internet Archive captures (parliament.gov.sl answers 503, or with an invalid certificate), and the PDFs
Sierra Leone Web lists on www.sierra-leone.org/laws.html and ordinances.html (live; a secondary compilation, no
robots.txt, no terms beyond its copyright notice). One request in flight per host, at least 1 s apart.
`tools/sierralii/build2.py <repo>` then appends one commit per Act, with the same layout, reader and word check
as `build_leg.py`, and these rules:

- an Act already here (same number and year) is skipped; a Parliament copy wins over the Sierra Leone Web copy;
- sections must run 1..N and N must equal the Arrangement of Sections; a print with no Arrangement is held
  unless it reads at least one section per 1.5 pages;
- in-force day: the date of commencement printed on the Act; else its Gazette date (Constitution s. 106(3)); an
  Act that leaves commencement to a later order, or prints no date, or a Gazette date before its signing, is
  held;
- a Sierra Leone Web copy carries `Source-status: secondary copy (Sierra Leone Web, ...)`; a scan whose PDF
  already carries a text layer is read from that layer and carries `Text-source: publisher OCR` (no OCR by
  Lexifina); a Parliament copy carries `Source` (the Parliament URL) and `Archived-copy` (the capture read);
- an Act in force before 1970 is stamped 1970-01-01 (git cannot store earlier dates), with its real day in the
  subject and the `In-force` trailer.

Committed: 70 Acts (16 Parliament, 54 Sierra Leone Web, 13 of them from a publisher's OCR layer):

- Act No. 4 of 2003 The State Salaries, Pensions, Gratuities and other Benefits Act, 2003 (`state-salaries-pensions-gratuities-other-benefits/`, in force 2003-07-17, Sierra Leone Web)
- Act No. 1 of 2004 The Local Government Act, 2004 (`local-government/`, in force 2004-03-01, Sierra Leone Web)
- Act No. 2 of 2004 The Education Act, 2004 (`education/`, in force 2004-04-01, Sierra Leone Web)
- Act No. 3 of 2004 The External Telecommunications Tax (Amendment) Act, 2004 (`external-telecommunications-tax-amendment/`, in force 2002-07-26, Sierra Leone Web, publisher OCR)
- Act No. 6 of 2004 The Income Tax (Amendment) Act, 2004 (`income-tax-amendment/`, in force 2004-05-27, Sierra Leone Web)
- Act No. 11 of 2004 The Payroll Tax (Amendment) Act, 2004 (`payroll-tax-amendment/`, in force 2004-04-01, Sierra Leone Web, publisher OCR)
- Act No. 13 of 2004 The Legal Practitioners (Amendment) Act, 2004 (`legal-practitioners-amendment/`, in force 2004-12-19, Sierra Leone Web)
- Act No. 14 of 2004 The Public Procurement Act, 2004 (`public-procurement-2004/`, in force 2004-12-16, Sierra Leone Web)
- Act No. 1 of 2005 The Universities Act, 2005 (`universities-2005/`, in force 2005-03-10, Sierra Leone Web)
- Act No. 7 of 2005 The Anti-Human Trafficking Act, 2005 (`anti-human-trafficking-2005/`, in force 2005-08-18, Sierra Leone Web)
- Act No. 8 of 2005 The Income Tax (Amendment) Act, 2005 (`income-tax-amendment-2005/`, in force 2005-01-01, Sierra Leone Web, publisher OCR)
- Act No. 3 of 2006 The Independent Media Commission (Amendment) Act, 2006 (`independent-media-commission-amendment/`, in force 2005-03-01, Sierra Leone Web, publisher OCR)
- Act No. 4 of 2006 The Sierra Leone The National Power Authority (Amendment) Act, 2006 (`sierra-leone-national-power-authority-amendment/`, in force 2005-03-31, Sierra Leone Web)
- Act No. 6 of 2006 The Income Tax (Amendment) (No. 2) Act, 2006 (`income-tax-amendment-no-2/`, in force 2005-01-01, Sierra Leone Web, publisher OCR)
- Act No. 7 of 2006 The Finance Act, 2006 (`finance-2006/`, in force 2006-01-01, Sierra Leone Web)
- Act No. 2 of 2007 The Diamond Cutting and Polishing Act, 2007 (`diamond-cutting-polishing/`, in force 2007-04-05, Sierra Leone Web)
- Act No. 3 of 2007 The Sierra Leone Investment and Export Promotion Agency Act, 2007 (`sierra-leone-investment-export-promotion-agency/`, in force 2007-05-10, Parliament)
- Act No. 17 of 2007 The Development Learning Centre Act, 2007 (`development-learning-centre/`, in force 2007-09-11, Sierra Leone Web)
- Act No. 18 of 2007 The Registration of Business Act, 2007 (`registration-business/`, in force 2007-09-11, Sierra Leone Web)
- Act No. 19 of 2007 The Independent Media Commission (Amendment) Act, 2007 (`independent-media-commission-amendment-2007/`, in force 2007-09-13, Sierra Leone Web)
- Act No. 21 of 2007 The Devolution of Estates Act, 2007 (`devolution-estates/`, in force 2007-09-13, Sierra Leone Web)
- Act No. 1 of 2008 The Medical Practitioners and Dental Surgeons (Amendment) Act, 2008 (`medical-practitioners-dental-surgeons-amendment/`, in force 2008-05-01, Sierra Leone Web)
- Act No. 4 of 2008 The National Registration Act, 2008 (`national-registration/`, in force 2008-07-03, Sierra Leone Web)
- Act No. 5 of 2008 The Merchant Shipping (Amendment) Act, 2008 (`merchant-shipping-amendment/`, in force 2008-07-10, Sierra Leone Web)
- Act No. 6 of 2008 The Bumbuna Watershed Management Authority and the Bumbuna Conservation Area Act, 2008 (`bumbuna-watershed-management-authority-bumbuna-conservation-area/`, in force 2008-07-17, Parliament)
- Act No. 7 of 2008 The Finance Act, 2008 (`finance-2008/`, in force 2008-01-01, Sierra Leone Web)
- Act No. 10 of 2008 The National Drugs Control Act, 2008 (`national-drugs-control/`, in force 2008-08-07, Sierra Leone Web)
- Act No. 11 of 2008 The Environment Protection Agency Act, 2008 (`environment-protection-agency/`, in force 2008-09-11, Sierra Leone Web)
- Act No. 13 of 2008 The National Drugs Control (Amendment) Act, 2008 (`national-drugs-control-amendment/`, in force 2008-09-18, Sierra Leone Web, publisher OCR)
- Act No. 3 of 2009 The Payment Systems Act, 2009 (`payment-systems/`, in force 2009-06-04, Sierra Leone Web)
- Act No. 4 of 2009 The Home Mortgage Finance Act, 2009 (`home-mortgage-finance/`, in force 2009-06-11, Sierra Leone Web)
- Act No. 5 of 2009 The Companies Act, 2009 (`companies/`, in force 2009-08-13, Sierra Leone Web)
- Act No. 7 of 2009 The Bankruptcy Act, 2009 (`bankruptcy/`, in force 2009-08-27, Sierra Leone Web)
- Act No. 1 of 2010 The Sierra Leone Broadcasting Corporation Act, 2009 (`sierra-leone-broadcasting-corporation/`, in force 2010-01-28, Sierra Leone Web)
- Act No. 5 of 2010 The Weights and Measures Act, 2010 (`weights-measures/`, in force 2010-07-29, Sierra Leone Web)
- Act No. 6 of 2010 The Sierra Leone National Commission on Small Arms Act, 2010 (`sierra-leone-national-commission-small-arms/`, in force 2010-07-29, Sierra Leone Web)
- Act No. 1 of 2011 The Sierra Leone Teaching Service Commission Act, 2011 (`sierra-leone-teaching-service-commission/`, in force 2011-03-10, Sierra Leone Web)
- Act No. 3 of 2011 The Persons with Disability Act, 2011 (`persons-with-disability/`, in force 2011-05-05, Sierra Leone Web)
- Act No. 3 of 2012 The National Minerals Agency Act, 2012 (`national-minerals-agency/`, in force 2012-05-03, Sierra Leone Web)
- Act No. 5 of 2012 The Postal Services Regulatory Agency Act, 2012 (`postal-services-regulatory-agency/`, in force 2012-06-21, Sierra Leone Web)
- Act No. 6 of 2012 The Legal Aid Act, 2012 (`legal-aid/`, in force 2012-08-23, Sierra Leone Web)
- Act No. 7 of 2012 The Nuclear Safety and Radiation Protection Act, 2012 (`nuclear-safety-radiation-protection/`, in force 2012-08-23, Sierra Leone Web)
- Act No. 8 of 2012 The National Pharmaceutical Procurement Unit Act, 2012 (`national-pharmaceutical-procurement-unit/`, in force 2012-08-30, Sierra Leone Web)
- Act No. 11 of 2012 The National Protected Area Authority and Conservation Trust Fund Act, 2012 (`national-protected-area-authority-conservation-trust-fund/`, in force 2012-11-01, Sierra Leone Web)
- Act No. 14 of 2012 The Geneva Conventions Act, 2012 (`geneva-conventions/`, in force 2012-12-20, Sierra Leone Web)
- Act No. 15 of 2012 The Sierra Leone Red Cross Society Act, 2012 (`sierra-leone-red-cross-society/`, in force 2012-12-20, Sierra Leone Web)
- Act No. 3 of 2013 The Finance Act, 2013 (`finance-2013/`, in force 2013-12-12, Sierra Leone Web)
- Act No. 2 of 2014 The PETROLEUM (EXPLORATION AND PRODUCTION) (AMENDMENT) A C T, 2014. Being an Act to amend the Petroleum ( Exploration and Production) Act, 2011 (`petroleum-exploration-production-amendment-c-t-2014-being-an-amend-pet/`, in force 2014-05-20, Parliament, publisher OCR)
- Act No. 5 of 2014 The Sierra Leone Correctional Service Act, 2014 (`sierra-leone-correctional-service/`, in force 2014-09-18, Parliament)
- Act No. 7 of 2014 The Polytechnics (Amendment) Act, 2014 (`polytechnics-amendment/`, in force 2014-09-25, Sierra Leone Web, publisher OCR)
- Act No. 8 of 2014 The Trade Marks Act, 2014 (`trade-marks/`, in force 2014-10-09, Parliament)
- Act No. 13 of 2014 The Borrowers and Lenders Act, 2014 (`borrowers-lenders/`, in force 2014-12-30, Parliament)
- Act No. 1 of 2015 The Telecommunications (Amendment) Act, 2015 (`telecommunications-amendment/`, in force 2015-04-16, Sierra Leone Web, publisher OCR)
- Act No. 3 of 2015 The National Commission for Social Action (Amendment) Act, 2015 (`national-commission-social-action-amendment/`, in force 2015-08-06, Sierra Leone Web)
- Act No. 6 of 2016 The Finance Act, 2016 (`finance-2016/`, in force 2016-03-24, Sierra Leone Web)
- Act No. 7 of 2016 The National Social Security and Insurance Trust (Amendement) Act, 2016 (`national-social-security-insurance-trust-amendement/`, in force 2016-03-31, Sierra Leone Web, publisher OCR)
- Act No. 9 of 2016 The Sierra Leone Road Safety Authority (Amendment) Act, 2016 (`sierra-leone-road-safety-authority-amendment/`, in force 2016-06-16, Sierra Leone Web, publisher OCR)
- Act No. 11 of 2016 The Local Government (Amendment) Act, 2016 (`local-government-amendment/`, in force 2016-07-14, Sierra Leone Web, publisher OCR)
- Act No. 2 of 2017 The Local Government (Amendment) Act, 2017 (`local-government-amendment-2017/`, in force 2017-06-22, Parliament)
- Act No. 8 of 2017 The Sierra Leone Meteorological Agency Act, 2017 (`sierra-leone-meteorological-agency/`, in force 2017-09-28, Parliament)
- Act No. 2 of 2019 The Finance Act, 2019 (`finance-2019/`, in force 2019-01-11, Parliament)
- Act No. 3 of 2019 The Anti-Money Laundering and Combating of Financing of Terrorism (Amendment) Act, 2019 (`anti-money-laundering-combating-financing-terrorism-amendment/`, in force 2019-06-20, Sierra Leone Web)
- Act No. 4 of 2019 The Borrowers and Lenders Act, 2019 (`borrowers-lenders-2019/`, in force 2019-06-20, Parliament)
- Act No. 4 of 2020 The Public Order (Amendment) Act, 2020 (`public-order-amendment/`, in force 2020-08-18, Sierra Leone Web, publisher OCR)
- Act No. 6 of 2020 The Breast Milk Substitutes Act, 2021 (`breast-milk-substitutes-2020/`, in force 2021-09-16, Parliament)
- Act No. 3 of 2022 The Allied Health Professions Act 2022 (`allied-health-professions/`, in force 2022-02-24, Parliament)
- Act No. 5 of 2022 The Sierra Leone Meteorological Agency (Amendment) Act, 2022 (`sierra-leone-meteorological-agency-amendment/`, in force 2022-03-03, Parliament)
- Act No. 9 of 2022 The Professional Engineering Regulatory Council Act, 2022 (`professional-engineering-regulatory-council/`, in force 2022-06-23, Parliament)
- Act No. 17 of 2022 The Public Elections Act, 2022 (`public-elections/`, in force 2022-09-20, Parliament)
- Act No. 21 of 2022 The National Revenue Authority Act, 2022 (`national-revenue-authority/`, in force 2022-09-23, Parliament)

Held (718 files; a file can be a second copy of an Act):

- 553: no 'No. N YYYY Sierra Leone <title>' head line (not an Act print the reader knows)
- 49: no Arrangement of Sections and only N sections read from N pages
- 46: reader: start line not found: ^(?:BE IT )?ENACTED by|^ENACTED by
- 36: sections read N vs Arrangement N
- 14: sections read N vs numbers in text N
- 10: no commencement date and no Gazette date printed
- 6: commencement left to a later order (President or Minister); its date is not in the print
- 4: Gazette date N-N-N printed before the signing date N-N-N

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote the configuration and the Constitution replay code and chose the acts. No model wrote, summarised or transformed legal text: the code is deterministic, and the amendment instructions are applied by code written for each instruction.
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote Lexifina's code and the Sierra Leone changes to the vendored Lexifina's code, and chose the sources. No model wrote, summarised or transformed legal text: the reader is deterministic code reading the PDFs' text layer.
