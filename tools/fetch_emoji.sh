#!/bin/bash
# Google Noto Animated Emoji (CC BY 4.0) alpha WebM files for Remotion's <AnimatedEmoji> -> remotion/public/animated-emoji/ (gitignored, ~130 MB).
# Already-ingested curated clips live in assets/vfx/emoji_* (committed); run this only if you want all 411 emoji inside Remotion.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
D="$ROOT/remotion/public/animated-emoji"; mkdir -p "$D"
curl -sfL -o "$D/emojis.json" https://raw.githubusercontent.com/remotion-dev/animated-emoji/main/emojis.json
for n in $(python3 -c "import json;print(' '.join(e['name'] for e in json.load(open('$D/emojis.json'))))"); do
  [ -s "$D/$n-1x.webm" ] || curl -sfL --retry 3 -o "$D/$n-1x.webm" "https://raw.githubusercontent.com/remotion-dev/animated-emoji/main/public/$n-1x.webm" || echo "miss $n"
done
echo "$(ls "$D"/*-1x.webm | wc -l) emoji in $D"
