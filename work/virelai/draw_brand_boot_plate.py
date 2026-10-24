#!/usr/bin/env python3
"""brand-boot-plate V1R00 — issue #1254.

The VirelaiOS boot/splash plate: Virelai Sans wordmark + sexiburger mascot
on a declared navy field (#1E1E2E — WALLPAPER.QOI's dominant, matching the
seat's dark boot surface). 800x450 master (16:9, center-weighted — the
boot surface letterboxes). The mascot presents the wordmark: gloved hands
raised, bow tie on. Confident + welcoming — cousin of the #595 vigil
plate, not its copy. No version text, no trademarks.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import DARK, NAVY, INK
from virelai.sexiburger import mascot

T = DARK
CREAM = "#F0E4BC"       # field-plate caption gold family
d = Draw()
d.new_doc("VirelaiOS — brand boot plate", 800, 450)

# --- declared navy field -----------------------------------------------------
d.shape("rectangle", "navy field", x=0, y=0, width=800, height=450,
        fill=NAVY, stroke=NONE)
# soft spotlight behind the mascot — the one sanctioned gradient is the
# seat's; inside art, a radial glow is house shading
d.shape("ellipse", "spotlight", x=190, y=26, width=420, height=330,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#2A2A44"},
            {"offset": 0.72, "color": "#23233A"},
            {"offset": 1, "color": "#1E1E2E"}]}}, stroke=NONE)

# --- mascot, presenting ------------------------------------------------------
mascot(d, 400, 44, 236, arms="up")

# --- wordmark ----------------------------------------------------------------
r = d.text("VIRELAIOS", "wordmark", x=400, y=334, size=60,
           font="Virelai Sans", color=CREAM, justify="center")
d.cmd("text.setStyle", "wordmark tracking", id=r["id"], tracking=180)

# underline: measured from the real text bounds, sesame-dot terminals
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o:
            return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit:
                return hit
b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
x0, x1 = b["x"], b["x"] + b["width"]
uy = b["y"] + b["height"] + 22
d.shape("line", "wordmark rule", x1=x0, y1=uy, x2=x1, y2=uy,
        stroke=CREAM, strokeWidth=2, opacity=45, cap="round")
for i, sx in enumerate([x0 - 14, x1 + 14]):
    d.shape("ellipse", f"rule dot{i}", x=sx - 4, y=uy - 4, width=8, height=8,
            fill=CREAM, opacity=55, stroke=NONE)

r = d.finish("brand-boot-plate-V1R00")
