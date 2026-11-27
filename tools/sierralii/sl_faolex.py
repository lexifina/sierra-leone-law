"""Secondary source: FAOLEX (FAO) records for Sierra Leone and their full-text PDFs.

    python -X utf8 tools/sl_faolex.py      # records then PDFs, 1 in flight, ~1 s apart; STOP file ends it

Record URLs come from FAOLEX's public sitemaps (cache3/faolex_sle_urls.json). Policies, strategies and plans are skipped
(not law). Same pacing rules as fetch2.py; 403/429 stops the run.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent.parent
C = HERE / 'cache3' / 'faolex'
LOG = HERE / 'progress.log'
UA = {'User-Agent': 'Mozilla/5.0 (compatible; law-archive-research)'}
NOT_LAW = re.compile(r'polic|strateg|-plan-|programme|program-|guideline|vision|framework-for|action-plan|roadmap'
                     r'|master-plan|manual|white-paper|report', re.I)


def log(msg: str) -> None:
    line = time.strftime('%Y-%m-%d %H:%M:%S ') + 'sl_faolex: ' + msg
    print(line, flush=True)
    with LOG.open('a', encoding='utf-8') as f:
        f.write(line + '\n')


def get(s, url, gap):
    for attempt in range(4):
        if (HERE / 'STOP').exists():
            raise SystemExit('STOP')
        try:
            r = s.get(url, timeout=(30, 120))
            if r.status_code in (403, 429):
                log(f'{r.status_code} on {url}: stopping (no way round a block)')
                raise SystemExit(1)
            if r.status_code < 500:
                return r, gap
        except requests.RequestException as e:
            log(f'{type(e).__name__} on {url}')
        gap = min(30.0, gap * 2)
        time.sleep(gap)
    return None, gap


def main() -> None:
    (C / 'rec').mkdir(parents=True, exist_ok=True)
    (C / 'pdf').mkdir(parents=True, exist_ok=True)
    urls = [u for u in json.loads((HERE / 'cache3' / 'faolex_sle_urls.json').read_text()) if not NOT_LAW.search(u)]
    log(f'{len(urls)} records (policies etc. skipped)')
    s = requests.Session()
    s.headers.update(UA)
    gap = 1.0
    for u in urls:
        fid = re.search(r'LEX-FAOC(\d+)', u).group(1)
        p = C / 'rec' / f'{fid}.json'
        if p.exists():
            continue
        r, gap = get(s, u, gap)
        m = r and re.search(r'id="prerendered-document">(.*?)</script>', r.text, re.S)
        if not m:
            log(f'record {fid}: {r.status_code if r else "failed"}')
            time.sleep(gap)
            continue
        d = json.loads(m.group(1))['doc']
        d['_url'] = u
        p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
        time.sleep(gap)
    n = 0
    for p in sorted((C / 'rec').glob('*.json')):
        d = json.loads(p.read_text(encoding='utf-8'))
        for f in d.get('links_to_full_text') or []:
            if not f.lower().endswith('.pdf') or (C / 'pdf' / f).exists():
                continue
            r, gap = get(s, 'https://faolex.fao.org/docs/pdf/' + f, gap)
            if r is not None and r.status_code == 200 and r.content[:4] == b'%PDF':
                (C / 'pdf' / f).write_bytes(r.content)
                n += 1
                if n % 25 == 0:
                    log(f'{n} PDFs')
            else:
                log(f'pdf {f}: {r.status_code if r is not None else "failed"}')
            time.sleep(gap)
    (C / 'DONE').write_text(time.strftime('%Y-%m-%dT%H:%M:%S'))
    log(f'done: {n} PDFs this run')


if __name__ == '__main__':
    main()
