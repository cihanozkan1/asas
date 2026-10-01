#!/bin/bash
# Blender 4.2 LTS (headless) + BlenderGIS add-on (SRTM / OSM / shapefile -> 3D terrain). Heavy: needs a GPU machine for good speed.
# usage: tools/blender/setup.sh [install_dir]     (default tools/vendor/blender, gitignored)
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DIR="${1:-$ROOT/tools/vendor/blender}"
if [ ! -x "$DIR/blender" ]; then
  mkdir -p "$DIR"
  curl -sL -o /tmp/blender.tar.xz https://download.blender.org/release/Blender4.2/blender-4.2.3-linux-x64.tar.xz
  tar xf /tmp/blender.tar.xz -C "$DIR" --strip-components=1
fi
export BLENDER_USER_SCRIPTS="$DIR/user_scripts"
ADD="$BLENDER_USER_SCRIPTS/addons"
mkdir -p "$ADD"; rm -rf "$ADD/BlenderGIS"; cp -r "$ROOT/tools/vendor/BlenderGIS" "$ADD/BlenderGIS"
"$DIR/blender" -b --python-expr "import addon_utils; m,s=addon_utils.check('BlenderGIS'); print('BlenderGIS available:', m); r=addon_utils.enable('BlenderGIS', default_set=True, persistent=True); print('BlenderGIS enabled:', r is not None)" 2>&1 | grep -i "blendergis"
printf '#!/bin/bash\nexport BLENDER_USER_SCRIPTS="%s"\nexec "%s/blender" "$@"\n' "$BLENDER_USER_SCRIPTS" "$DIR" > "$ROOT/tools/blender/blender.sh"; chmod +x "$ROOT/tools/blender/blender.sh"
echo "Blender wrapper: tools/blender/blender.sh -b scene.blend -a"
