#!/usr/bin/env python3
"""Real road routes from the Natural Earth 10m roads network (public domain, no attribution needed).

  python3 tools/roadroute.py "70.3,-148.7" "64.8,-147.7" "8.15,-77.69" [--ferry] [--max 80]

Prints a JSON list of [lat, lon] along the road network between the waypoints (Dijkstra over the road graph,
each waypoint snapped to the nearest road node; --ferry also allows ferry links). Used by helpers.road().
First run downloads the dataset to data/cache/ne_roads.geojson and caches the graph.
"""
import sys, os, json, math, heapq, pickle, urllib.request
import numpy as np
from scipy.spatial import cKDTree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GJ = os.path.join(ROOT, 'data/cache/ne_roads.geojson')
PK = os.path.join(ROOT, 'data/cache/ne_roads.graph.pkl')
URL = 'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_roads.geojson'


def hav(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))


def build():
    if not os.path.exists(GJ):
        os.makedirs(os.path.dirname(GJ), exist_ok=True)
        urllib.request.urlretrieve(URL, GJ)
    d = json.load(open(GJ))
    key = {}
    nodes = []
    adj = []

    def node(lat, lon):
        k = (round(lat, 3), round(lon, 3))
        if k not in key:
            key[k] = len(nodes); nodes.append((lat, lon)); adj.append([])
        return key[k]

    for f in d['features']:
        p = f['properties']
        if p.get('type') == 'Track':
            continue
        ferry = p.get('type') == 'Ferry Route'
        g = f['geometry']
        lines = g['coordinates'] if g['type'] == 'MultiLineString' else [g['coordinates']]
        for ln in lines:
            prev = None
            for lon, lat in ln:
                n = node(lat, lon)
                if prev is not None and prev != n:
                    w = hav(nodes[prev], nodes[n])
                    adj[prev].append((n, w, ferry)); adj[n].append((prev, w, ferry))
                prev = n
    # tiny gaps between road ends (digitising): join nodes closer than 1.2 km
    tree = cKDTree(np.array(nodes))
    for i, j in tree.query_pairs(0.011):
        w = hav(nodes[i], nodes[j])
        if w < 1.2:
            adj[i].append((j, w, False)); adj[j].append((i, w, False))
    # data gaps (roads missing in the source, e.g. parts of Central America / Patagonia): bridge dead ends and
    # separate components with straight links up to 90 km, penalised x2 so real roads are always preferred
    comp = [-1] * len(nodes); c = 0
    for s0 in range(len(nodes)):
        if comp[s0] >= 0: continue
        st = [s0]; comp[s0] = c
        while st:
            u = st.pop()
            for v, w, fer in adj[u]:
                if comp[v] < 0: comp[v] = c; st.append(v)
        c += 1
    sizes = np.bincount(comp)
    for i, j in tree.query_pairs(0.82):
        if comp[i] == comp[j]: continue
        if min(sizes[comp[i]], sizes[comp[j]]) < 5: continue
        w = hav(nodes[i], nodes[j])
        if w <= 90:
            adj[i].append((j, w * 2, False)); adj[j].append((i, w * 2, False))
    return nodes, adj


def graph():
    if os.path.exists(PK):
        return pickle.load(open(PK, 'rb'))
    g = build()
    pickle.dump(g, open(PK, 'wb'))
    return g


def route(waypoints, ferry=False, max_pts=80):
    nodes, adj = graph()
    tree = cKDTree(np.array(nodes))
    ids = []
    for w in waypoints:
        dist, i = tree.query(w)
        if dist > 0.6:
            raise SystemExit(f'no road near {w} (nearest {dist:.2f} deg away)')
        ids.append(int(i))
    path = []
    for a, b in zip(ids, ids[1:]):
        D = {a: 0.0}; prev = {}; pq = [(0.0, a)]
        while pq:
            d0, u = heapq.heappop(pq)
            if u == b:
                break
            if d0 > D.get(u, 1e18):
                continue
            for v, w, fer in adj[u]:
                if fer and not ferry:
                    continue
                nd = d0 + w * (3 if fer else 1)
                if nd < D.get(v, 1e18):
                    D[v] = nd; prev[v] = u; heapq.heappush(pq, (nd, v))
        if b not in prev and a != b:
            raise SystemExit(f'roads between {waypoints[ids.index(a)]} and {waypoints[ids.index(b)]} are not connected in the dataset')
        seg = [b]
        while seg[-1] != a:
            seg.append(prev[seg[-1]])
        seg.reverse()
        path += seg if not path else seg[1:]
    pts = [nodes[i] for i in path]
    # Douglas-Peucker thinning to max_pts
    def dp(P, eps):
        if len(P) < 3:
            return P
        a, b = np.array(P[0]), np.array(P[-1]); ab = b - a; n = np.linalg.norm(ab) or 1e-9
        d = [abs(np.cross(ab, np.array(p) - a)) / n for p in P[1:-1]]
        m = int(np.argmax(d))
        if d[m] > eps:
            return dp(P[:m + 2], eps)[:-1] + dp(P[m + 1:], eps)
        return [P[0], P[-1]]
    eps = 0.002
    out = pts
    while len(out) > max_pts:
        eps *= 1.6
        out = dp(pts, eps)
    return [[round(p[0], 4), round(p[1], 4)] for p in out]


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    ferry = '--ferry' in sys.argv
    mx = 80
    if '--max' in sys.argv:
        mx = int(sys.argv[sys.argv.index('--max') + 1]); args = [a for a in args if a != str(mx)]
    wps = [tuple(float(x) for x in a.split(',')) for a in args]
    print(json.dumps(route(wps, ferry, mx)))
