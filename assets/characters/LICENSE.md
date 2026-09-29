# Character art

Flat 2D cartoon characters generated with FLUX.1-dev (Black Forest Labs) through NVIDIA's hosted API
(build.nvidia.com), background removed with rembg (isnet-general-use), main figure kept, cropped to
700 px height. Prompt + seed for each character: `prompts/<id>.json`. Every image was reviewed by eye:
one figure, no extra people or stray props, period-appropriate and modest clothing.

Generator: `tools/gen_character_nvidia.py` (reads NVIDIA_API_KEY from the environment; the key is
never stored in the repository).
