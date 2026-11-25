#!/usr/bin/env python3
"""Cross-check the data embedded in index.html against the IUIS 2024 source tables.

Usage:  python3 tools/check_genes.py [index.html] [tools/iuis2024_source_rows.tsv]

Reports, table by table:
  * source rows whose gene is missing from the site (or present fewer times),
  * site rows whose gene text does not appear in the source (typos such as CSFR2B),
  * rows where the inheritance differs.
Exit code 1 if any gene is missing or misspelled, so it can be run before every upload.
"""
import collections, json, re, sys

page = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
ref = sys.argv[2] if len(sys.argv) > 2 else 'tools/iuis2024_source_rows.tsv'

html = open(page, encoding='utf-8').read()
data = json.loads(re.search(r'<script type="application/json" id="data">(.*?)</script>', html, re.S).group(1))
site = data['entries']

def key(g):  # ignore spacing, asterisks, case and Greek/ASCII spelling differences
    g = g.replace('γ', 'g').replace('α', 'a').replace('ω', 'w').replace('†', '').replace('^b^', '')
    return re.sub(r'[\s*\-]', '', g).upper()

src = collections.defaultdict(list)
for line in open(ref, encoding='utf-8').read().splitlines()[1:]:
    t, n, g, i, o = (line.split('\t') + [''] * 5)[:5]
    src[int(t) - 1].append((key(g), g, i))

bad = 0
for ti in range(len(data['tables'])):
    s_rows = [(key(e['g']), e['g'], e['i']) for e in site if e['t'] == ti]
    a = collections.Counter(k for k, _, _ in src[ti])
    b = collections.Counter(k for k, _, _ in s_rows)
    missing, extra = a - b, b - a
    name = {k: g for k, g, _ in src[ti]}
    sname = {k: g for k, g, _ in s_rows}
    if missing or extra:
        print(f'Table {data["tables"][ti]["id"]}:')
        for k, c in missing.items():
            print(f'  MISSING on site  ({c}x): {name[k]}'); bad += 1
        for k, c in extra.items():
            print(f'  NOT IN SOURCE    ({c}x): {sname[k]}'); bad += 1
    inh_src = collections.Counter((k, re.sub(r'\W', '', i).upper()) for k, _, i in src[ti] if i)
    inh_site = collections.Counter((k, re.sub(r'\W', '', i).upper()) for k, _, i in s_rows)
    for (k, i), c in (inh_src - inh_site).items():
        if k in b:
            print(f'  Table {data["tables"][ti]["id"]} inheritance differs for {name[k]}: source "{i}"')

genes = {s for e in site for s in e['y']}
print(f'\n{len(site)} entries, {len(genes)} distinct current gene symbols.')
print('OK: every source gene is on the site.' if not bad else f'{bad} problem(s) found.')
sys.exit(1 if bad else 0)
