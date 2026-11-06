#!/usr/bin/env python3
"""Download the latest Monero Merchant Index from xmrlist.com and write it to data/.
Runs daily from .github/workflows/update.yml. Standard library only."""
import csv, json, os, urllib.request
BASE = 'https://xmrlist.com'
UA = {'User-Agent': 'monero-merchant-index-updater/1.0 (+https://xmrlist.com/stats)'}
os.makedirs('data/snapshots', exist_ok=True)

def get(path):
    with urllib.request.urlopen(urllib.request.Request(BASE + path, headers=UA), timeout=60) as r:
        return r.read()

listings = json.loads(get('/data.json'))
stats = json.loads(get('/api/v1/stats'))
if len(listings.get('listings', [])) < 100:
    raise SystemExit('listing export looks incomplete, not updating')

with open('data/listings.json', 'w', encoding='utf-8') as f:
    json.dump(listings, f, ensure_ascii=False, indent=1)
cols = ['name', 'slug', 'url', 'website', 'onion', 'category', 'subcategory', 'status', 'grade', 'accepts_xmr',
        'xmr_discount', 'kyc', 'operating_since', 'country', 'last_checked', 'uptime_30d', 'rating', 'reviews']
with open('data/listings.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
    w.writeheader()
    for row in sorted(listings['listings'], key=lambda x: x['slug']):
        w.writerow(row)
with open('data/stats.json', 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=1)
for name in ('categories', 'countries', 'history'):
    with open(f'data/{name}.csv', 'wb') as f:
        f.write(get(f'/stats/{name}.csv'))
day = str(stats.get('generated_at', listings['generated']))[:10]
with open(f'data/snapshots/{day}.json', 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=1)
# fill in any earlier daily snapshots listed in history.csv that are not in the repo yet
for row in csv.DictReader(open('data/history.csv', encoding='utf-8')):
    p = f"data/snapshots/{row['date']}.json"
    if not os.path.exists(p):
        try:
            open(p, 'wb').write(get(f"/stats/snapshots/{row['date']}.json"))
        except Exception as e:
            print('no snapshot for', row['date'], e)
print('updated', day, len(listings['listings']), 'listings')
