#!/usr/bin/env python3
"""Search Wikimedia Commons for public-domain / CC0 videos and images (licence is read from the file's own metadata).

  python3 tools/commons_search.py "lava fountain" [--kind video|image] [--limit 20]
Prints: title | licence | duration | size | url. Only PD / CC0 results are listed (CC-BY etc. are skipped:
we want zero attribution and zero share-alike obligations).
"""
import sys, json, urllib.request, urllib.parse, re, time

API = 'https://commons.wikimedia.org/w/api.php'
OK = re.compile(r'^(pd|public domain|cc0|cc-zero|usgs|nasa)', re.I)


def api(**p):
    p['format'] = 'json'
    req = urllib.request.Request(API + '?' + urllib.parse.urlencode(p), headers={'User-Agent': 'geo-shorts/1.0 (https://github.com/cihanozkan1/asas)'})
    for k in range(6):                     # Commons rate-limits bursts: back off and retry
        try:
            time.sleep(1.0)
            return json.load(urllib.request.urlopen(req, timeout=40))
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(4 * (k + 1))
    raise SystemExit('Commons rate limit')


def search(q, kind='video', limit=20):
    t = 'video' if kind == 'video' else 'bitmap'
    r = api(action='query', list='search', srsearch=f'{q} filetype:{t}', srnamespace=6, srlimit=min(50, limit * 3))
    titles = [x['title'] for x in r['query']['search']]
    out = []
    for i in range(0, len(titles), 20):
        info = api(action='query', titles='|'.join(titles[i:i + 20]), prop='imageinfo', iiprop='url|size|mime|extmetadata|mediatype')
        for pg in info['query']['pages'].values():
            ii = (pg.get('imageinfo') or [{}])[0]
            md = ii.get('extmetadata', {})
            lic = (md.get('LicenseShortName') or {}).get('value', '')
            if not OK.search(lic):
                continue
            out.append({'title': pg['title'], 'license': lic, 'url': ii.get('url'), 'size_mb': round((ii.get('size') or 0) / 1e6, 1),
                        'mime': ii.get('mime'), 'author': re.sub('<[^>]+>', '', (md.get('Artist') or {}).get('value', ''))[:60]})
    return out[:limit]


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    kind = sys.argv[sys.argv.index('--kind') + 1] if '--kind' in sys.argv else 'video'
    if kind in args: args.remove(kind)
    lim = 20
    for r in search(args[0], kind, lim):
        print(json.dumps(r, ensure_ascii=False))
