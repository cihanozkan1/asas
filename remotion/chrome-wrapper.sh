#!/bin/bash
# Full Chromium (same build our own renderer uses) + software WebGL2 flags, for Remotion's MapLibre / deck.gl / three compositions.
exec /opt/pw-browsers/chromium-1194/chrome-linux/chrome "$@" --no-sandbox --ignore-gpu-blocklist --enable-unsafe-swiftshader --enable-webgl --use-gl=angle --use-angle=swiftshader
