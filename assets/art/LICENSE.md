# Map illustrations

Flat 2D illustrations (vehicles, ships, landmarks, dams, animals, weather, props)
generated with FLUX.1-dev (Black Forest Labs) through NVIDIA's hosted API (build.nvidia.com), cut out
with rembg (isnet-general-use), specks and the ground-shadow ellipse removed, cropped, max 420 px.
Prompt + seed for each image: `prompts/<name>.json`. Vehicles and ships are drawn facing right; the
renderer mirrors them to their travel direction. Every image was reviewed by eye.

Scripts use them as `art:<name>`; pictorial emoji are mapped to these drawings in `src/geo.mjs`
(`EMOJI_ART`), so no emoji font artwork appears in the videos.

Generator: `tools/gen_art_nvidia.py` (reads NVIDIA_API_KEY from the environment; the key is never
stored in the repository).
