"""Manim Community scene: map-like arrow growing with a label (transparent render).

  manim -t -qm tools/py/manim_arrow.py ArmyArrow       (-t = transparent background; output in media/)
Then:  python3 tools/vfx_ingest.py media/videos/manim_arrow/720p30/ArmyArrow.mov fx_manim_arrow --key alpha
"""
from manim import *

class ArmyArrow(Scene):
    def construct(self):
        path = CubicBezier(LEFT * 4 + DOWN * 2, LEFT * 1 + UP * 3, RIGHT * 1 + DOWN * 3, RIGHT * 4 + UP * 2).set_color("#ff3b3b").set_stroke(width=14)
        head = Triangle(color="#ff3b3b", fill_opacity=1).scale(0.35)
        head.move_to(path.get_start())
        label = Text("1453", font_size=60, color=WHITE).to_edge(UP)
        self.play(Write(label), run_time=0.6)
        self.play(Create(path), MoveAlongPath(head, path), run_time=2.4)
        self.play(Indicate(head), run_time=0.6)
