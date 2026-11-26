# Sierra Leone: law history in git

<picture>
<source media="(prefers-color-scheme: dark)" srcset="data/effort-dark.svg">
<img alt="Sierra Leonean law in this repository: what it holds, changes by the year they took effect, completeness against the official sources, and the correctness of what is held" src="data/effort-light.svg" width="880">
</picture>

The law of Sierra Leone as a git history: one file per section (or schedule), one commit per version on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to a section; picking a date gives the text in force that day.

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is Sierra Leone's national law, which global-law reads at `sierra-leone/national/acts/`.

**What is in it now:** the Constitution of Sierra Leone, 1991 with its amendments to 2016 (5 versions), and 110 Acts as enacted, 2003 to 2024: 37 from SierraLII (its Akoma Ntoso text, or the text layer of the print it publishes), 19 from Government Printing Department prints that Parliament published, and 54 from the same prints as copied by Sierra Leone Web (a secondary compilation; each such commit says so). Each Act is held as enacted, one version; scanned Acts without a text layer are not here. [`REPRODUCE.md`](REPRODUCE.md) lists every act with its source and what is held back.

Each act is a folder, one file per provision, plus a `README.md` listing its provisions (`employment/sec-071.md` is section 71 of the Employment Act, 2023, Act 15 of 2023: annual leave).

The text is in English, the language Sierra Leone's laws are published in, as SierraLII and the Government Printing Department print it.

## Questions as git commands

| Question | Command |
| --- | --- |
| Every change to section 71 of the Employment Act | `git log -p --word-diff -- employment/sec-071.md` |
| Which law wrote each line of section 71? | `git blame employment/sec-071.md` |
| Every version of the Employment Act, with the day each took effect | `git log --format="%h %(trailers:key=In-force,valueonly,separator=) %an" -- employment ':!*/README.md'` |
| Section 71 as in force on 1 January 2024 | `python tools/on.py 2024-01-01 employment sec-071` |

**Outside git**, we also host this record publicly, for free:

- **[Ask Claude about Sierra Leonean law](https://global-law.lexifina.com/v1/try_claude?country=sierra-leone)**: opens Claude with a first question ready.
- **[Ask ChatGPT](https://global-law.lexifina.com/v1/try_chatgpt?country=sierra-leone)**: the same question in ChatGPT.
- **[Search Sierra Leonean law on our site](https://lexifina.com/law?country=sierra-leone&q=annual+leave)**: a search for "annual leave", with each provision's text and its versions, no account needed.
- **[Developer REST API](https://global-law.lexifina.com/v1/search_law?query=annual+leave&jurisdiction=sierra-leone)**: the same search as JSON, with no key. See the [documentation here](https://lexifina.com/api/global-law).

Both assistants read the record through the free Global law connector (MCP, `https://global-law.lexifina.com/mcp`); the first time, the chat gives you the link that adds it. Ask in English.

**Host it yourself easily.** All it takes is git and Python, and the tools run on your machine:

```sh
git clone --depth 1 https://github.com/lexifina/global-law && cd global-law
python3 tools/countries.py add sierra-leone/national/acts
python3 tools/law.py show 2026-01-01 sierra-leone/national/acts/employment/sec-071.md
```

Opened in Claude Code, Cursor, VS Code or Codex, the clone also starts a local MCP server with the same tools ([MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md)).

## Dates

Each commit is dated at noon, Africa/Freetown, on the day the version took effect, and carries it in its `In-force:` trailer:

- an Act comes into operation on its publication in the Gazette, or on the date it prescribes (Constitution of Sierra Leone, 1991, s. 106(3));
- the six printed Acts leave their date of commencement blank, so each is dated by its Gazette (the Banking Act, 2019: Gazette No. 51 of 27 June 2019);
- the Employment Act, 2023 is dated by SierraLII's own date for it, its publication on 11 May 2023.

Each act is credited to itself as enacted (`Act No. 6 of 2019 <act-2019-6@sierralii.invalid>`; the Cyber Security and Crime Act, 2021 by its title), with an e-mail address that cannot exist, so `git blame` and `git log --author` name laws. The committer is always Lexifina.

## How it is checked

- `tools/check_repo.py` reads every version back from git on the day it took effect and on the day before, and compares it with the corpus: 7 versions of 7 acts, 0 mismatches, and no commit whose trailers git cannot parse (see [`REPRODUCE.md`](REPRODUCE.md)).
- Every printed word of the six Acts, from the enacting formula to "Passed in Parliament", is in a provision file, a Part heading or the printer's colophon, and none is added; the Employment Act's text, except headings and editorial notes, is checked to be in a provision file.
- A second build from the same corpus gave the same hashes for all 7 history commits and 14 tags.
- History is append-only: no merge commits, no commit rewritten, and none dated after the build. Acts are added in batches, so a later batch can hold Acts older than the one before it.
- [vulnerabilities/](vulnerabilities/): possible drafting mistakes in this law, found by global-law's detectors and checked by hand. Not run yet.

## What it does not show

- **Most Sierra Leonean law.** 110 Acts are here. Held back: scans with no text layer (no OCR is done), prints the side-note reader cannot yet split by section (most amending Acts and Appropriation Acts), Acts that leave their commencement to a later order whose date is not printed, prints with no Gazette or commencement date, and subordinate legislation. Most of the Laws of Sierra Leone, 1960 and the Acts of 1961 to 2000 exist only as scans. No bill is held.
- **Amendments.** Each act is held as enacted. No amending Act to the six printed Acts appears in Parliament's lists of Acts and Bills, but the annual Finance Acts were not read word for word; SierraLII holds no later version of the Employment Act.
- **The Constitution's 2022 amendments.** Its history runs from 1991 to 2016 (5 versions, `constitution/`). Two Constitution (Amendment) Acts of 2022 (ss. 32, 34 and 35) have no usable text (SierraLII's copy of Act No. 22 of 2022 is a scan; the other is an undated print), so sections 32, 34 and 35 may not be today's text.
- **Headings.** Part, Chapter and Division headings and SierraLII's editorial notes are left out; misspellings in the prints are kept as printed.

## Sources

| Source | Kind | Past versions | Notes |
| --- | --- | --- | --- |
| [Parliament of Sierra Leone](https://www.parliament.gov.sl) | Acts as passed and signed, printed by the Government Printing Department | no, the Act as enacted | 19 Acts, read from the PDFs' text layer (no OCR), each from an Internet Archive copy (the site no longer answers) |
| [SierraLII](https://sierralii.gov.sl) (Sierra Leone Legal Information Institute, on Laws.Africa's Peachjam) | Acts as published | no, one expression per act | 37 Acts: the Employment Act, 2023 from an archived copy; 36 more read live on 2026-11-26 (HTML text, or the born-digital print's text layer) |
| [Sierra Leone Web](https://www.sierra-leone.org/laws.html) | copies of the Government Printing Department prints, collected since 1996 (secondary) | no, the Act as enacted | 54 Acts not found in an official copy with a text layer; commits carry `Source-status: secondary copy`, and `Text-source: publisher OCR` where the copy is a scan with its own text layer |

## Licence

See [`LICENSE`](LICENSE). SierraLII licenses its content under CC BY-NC 4.0, crediting SierraLII as the source (its terms of use, section 9), so its texts may be used only for non-commercial purposes; parliament.gov.sl and Sierra Leone Web state no licence for the Acts they publish (Acts of Parliament; Sierra Leone Web's copyright notice covers its own site). Lexifina's own contributions (the arrangement of the history, the commit messages, the tables and the tools) are CC0 1.0.

No AI model wrote, translated or corrected legal text, and none runs when the history is built; the scripts were written by an AI model (see [`REPRODUCE.md`](REPRODUCE.md)).

## Visualisations

- [visualisations/](visualisations/): charts drawn from this repository. Not drawn yet.

## More

From [lexifina/global-law](https://github.com/lexifina/global-law):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): every feature, and what every corpus must support (`git blame`, `law.py`, the MCP tools)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): questions and answers · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): proposing changes · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): the MCP server · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): how it was built · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): how current each corpus is · [Monitoring](https://github.com/lexifina/global-law/tree/main/monitoring): whether updates are running · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): how each official source is watched for changes
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): how fast the tools are, measured
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): charts and bridges across the world's law
- [Vulnerabilities](https://github.com/lexifina/global-law/tree/main/vulnerabilities): mistakes in legislation as published
