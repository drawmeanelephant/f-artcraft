#!/usr/bin/env python3
"""wallpaper-quiet-field V1R00 — issue #1251, variant 4.

The sensible option for people who find a guillotine at breakfast a lot:
a soft pre-dawn gradient over rolling navy hills, a few fading stars, and
one tiny mascot cameo sitting on a rise watching the sky. Lowest detail of
the set. 2560x1440, dead-center-safe.
"""
import sys, os, math, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import NAVY, INK
from virelai.sexiburger import mascot

W, H = 2560, 1440
d = Draw()
d.new_doc("VirelaiOS — wallpaper quiet field", W, H)

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0},
                                     {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], \
                                     [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

def ridge(name, base_y, amp, phase, c0, c1, sw=0):
    """One smooth hill silhouette: a soft two-bump curve across the canvas."""
    p = f"M-20,{H + 40} L-20,{base_y:.0f} "
    n = 6
    for i in range(n):
        x0 = -20 + (W + 40) * i / n
        x1 = -20 + (W + 40) * (i + 1) / n
        y0 = base_y - amp * (0.5 + 0.5 * math.sin(phase + i * 1.9))
        y1 = base_y - amp * (0.5 + 0.5 * math.sin(phase + (i + 1) * 1.9))
        cx = (x0 + x1) / 2
        cy = min(y0, y1) - amp * 0.35
        p += f"Q{cx:.0f},{cy:.0f} {x1:.0f},{y1:.0f} "
    p += f"L{W + 20},{H + 40} Z"
    d.path(p, name, fill=lin(c0, c1, (0, base_y - amp), (0, H)),
           stroke="none", strokeWidth=0)

# --- sky: soft pre-dawn gradient -----------------------------------------------
d.shape("rectangle", "sky", x=0, y=0, width=W, height=H,
        fill=lin("#1B1B33", "#0E0E1D", (0, 0), (0, H)), stroke=NONE)
# a thin warm hint at the horizon — first light, not a sunset
d.shape("ellipse", "horizon glow", x=680, y=840, width=1200, height=300,
        fill=rad({"offset": 0, "color": "#8A5E3C", "opacity": 0.20},
                 {"offset": 1, "color": "#8A5E3C", "opacity": 0}), stroke=NONE)
# a handful of fading stars, nothing busy
for i, (x, y, w, o) in enumerate([(420, 260, 5, 30), (980, 160, 4, 24),
                                  (1560, 240, 4, 26), (2050, 170, 5, 30),
                                  (2300, 480, 4, 20), (260, 640, 4, 18),
                                  (1320, 340, 3, 20), (1780, 520, 3, 16)]):
    d.shape("ellipse", f"star{i}", x=x - w / 2, y=y - w / 2, width=w, height=w,
            fill="#C8D6F0", opacity=o, stroke=NONE)
# low soft moon, small and dim — part of the sky, not a subject
d.shape("ellipse", "moon glow", x=1890, y=430, width=190, height=190,
        fill=rad({"offset": 0, "color": "#D8DEEA", "opacity": 0.35},
                 {"offset": 1, "color": "#D8DEEA", "opacity": 0}), stroke=NONE)
d.shape("ellipse", "moon", x=1932, y=472, width=108, height=108,
        fill="#D8DEEA", opacity=80, stroke=NONE)

# --- hills ----------------------------------------------------------------------
ridge("far hills", 1030, 120, 0.7, "#23233C", "#1A1A2C")
ridge("mid hills", 1130, 150, 2.4, "#1C1C31", "#141424")
ridge("near rise", 1270, 190, 4.4, "#161627", "#0D0D18")

# --- the cameo ---------------------------------------------------------------------
# tiny, sitting on the near rise's crest, gazing up. h 150 of 2560x1440 —
# a stage with one small actor.
mascot(d, 1240, 1000, 150,
       eyes="happy", mouth="smile", pupils=(2, -4),
       arms="down", detail=False)

# --- finish ---------------------------------------------------------------------------
os.makedirs("work/out", exist_ok=True)
d.finish("wallpaper-quiet-field-V1R00")
res = d.m.request("tools/call", {"name": "render_preview",
                                 "arguments": {"max_side": 1280}})
for c in res.get("content", []):
    if "data" in c:
        open("work/out/wallpaper-quiet-field-V1R00-preview.png", "wb").write(
            base64.b64decode(c["data"]))
        print("preview saved")
