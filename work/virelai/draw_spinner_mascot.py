#!/usr/bin/env python3
"""spinner-mascot V1R00 — issue #1255 (alternative frame set).

Mascot-adjacent option filed beside spinner-arc per the issue: a mini
sesame bun whose seeds sit on an off-center spiral — rotating the spiral
45°/frame over 8 frames reads as a swirl even at 16 px, and the loop is
seamless (8 x 45° = 360°). Bun disc = BUN + INK outline + cel wedge,
same character palette as the pose set; seeds are SEED cream (reads on
dark, survives light against the orange field).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, OUT
from virelai.vkit import BUN, BUN_MID, INK
from virelai.sexiburger import SEED
from virelai import spinner

FRAMES = 8
R_BUN = 10.5

# seed spiral: (angle deg, radius px, seed w, seed h, seed rot) — asymmetric
# so rotation is unambiguous at 16 px. Seed 0 rides the rim: it wobbles the
# silhouette as it orbits, which is the motion cue that survives 16 px.
SEEDS = [(0, 10.2, 5.6, 3.4, 90), (55, 6.4, 4.6, 2.8, -15),
         (115, 5.2, 4.2, 2.6, 30), (180, 4.0, 4.0, 2.4, -25),
         (250, 3.0, 3.8, 2.4, 15)]


def motif(d, cx, cy, f):
    rot = f * 45.0
    # bun disc + cel wedges (same shading language as the mascot)
    d.shape("ellipse", "bun", x=cx - R_BUN, y=cy - R_BUN,
            width=2 * R_BUN, height=2 * R_BUN,
            fill=BUN, stroke=INK, strokeWidth=3.0)
    d.shape("ellipse", "bun shade", x=cx - R_BUN + 9.5, y=cy - R_BUN + 8.5,
            width=2 * R_BUN - 12, height=2 * R_BUN - 12,
            fill=BUN_MID, stroke=NONE)
    d.shape("ellipse", "bun light", x=cx - R_BUN + 2.2, y=cy - R_BUN + 1.8,
            width=9, height=7, fill="#FFD98A", stroke=NONE)
    for i, (a, r, w, h, srot) in enumerate(SEEDS):
        t = math.radians(a + rot)
        sx, sy = cx + r * math.cos(t), cy + r * math.sin(t)
        kw = dict(x=sx - w / 2, y=sy - h / 2, width=w, height=h, fill=SEED,
                  rotation=round((a + rot + srot) % 360, 1))
        if i == 0:
            kw.update(stroke=INK, strokeWidth=2.0)  # rim seed keeps the outline
        else:
            kw["stroke"] = NONE
        d.shape("ellipse", f"seed{i}", **kw)


d = Draw()
spinner.export_frames(d, "spinner-mascot-V1R00", FRAMES, motif, OUT)
spinner.sheet(d, "spinner-mascot-V1R00", FRAMES, motif)
r = d.finish("spinner-mascot-V1R00")
