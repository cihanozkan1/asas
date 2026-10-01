#!/bin/bash
# Natural Earth vector data (public domain, nvkelso/natural-earth-vector) -> data/cache/ne/  (gitignored; re-run on a fresh machine).
# Also the world-atlas TopoJSON repo (reference) -> reference-code/world-atlas.  Layers: countries, admin-1, roads, railroads, rivers, lakes,
# coastline, ocean, populated places, airports, ports, glaciers, geography regions, graticules, time zones.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
D="$ROOT/data/cache/ne"; mkdir -p "$D"
BASE=https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson
for f in ne_10m_admin_0_countries ne_50m_admin_0_countries ne_110m_admin_0_countries ne_10m_admin_1_states_provinces ne_10m_roads ne_10m_railroads \
         ne_10m_rivers_lake_centerlines ne_10m_lakes ne_10m_coastline ne_10m_ocean ne_10m_populated_places ne_10m_airports ne_10m_ports \
         ne_10m_glaciated_areas ne_10m_geography_regions_polys ne_10m_geography_marine_polys ne_10m_time_zones ne_10m_graticules_10 ne_10m_land; do
  [ -s "$D/$f.geojson" ] || { curl -sfL --retry 3 -o "$D/$f.geojson" "$BASE/$f.geojson" && echo "ok $f ($(du -h "$D/$f.geojson" | cut -f1))" || echo "FAIL $f"; }
done
[ -d "$ROOT/reference-code/world-atlas" ] || git clone -q --depth 1 https://github.com/topojson/world-atlas.git "$ROOT/reference-code/world-atlas"
echo done
