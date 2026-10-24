#!/usr/bin/env python3
"""spot-no-image V1R00 — issue #1253.

Decode refused / nothing to preview: a tilted photo card whose frame holds
only a dashed ghost of the picture that should be there — dashed mountain,
dashed sun. 160x120 transparent, reads at 80x60 on dark AND light.
"""
import sys, os, math, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import INK

d = Draw()
d.call("run_command", {"command": "file.new", "params": {
    "name": "VirelaiOS — spot no image", "width": 160, "height": 120,
    "units": "Pixels", "backgroundContents": "transparent",
    "colorMode": "rgb"}}, "file.new")

CARD, CARD_LO = "#E8EDF5", "#B7C2D4"
GHOST = "#5E6E82"

def lin(c0, c1, start, end):
    return {"gradient": {"kind": "linear", "stops": [
        {"offset": 0, "color": c0}, {"offset": 1, "color": c1}],
        "start": list(start), "end": list(end)}}

# photo card, tilted -8 degrees around center (80, 60)
t = math.radians(-8)
c, s = math.cos(t), math.sin(t)
def T(x, y):
    dx, dy = x - 80, y - 62
    return 80 + dx * c - dy * s, 62 + dx * s + dy * c
def poly(pts):
    p0 = T(*pts[0])
    d_ = f"M{p0[0]:.1f},{p0[1]:.1f} " + \
         " ".join(f"L{T(x, y)[0]:.1f},{T(x, y)[1]:.1f}" for x, y in pts[1:])
    return d_ + " Z"

# card body + inner window
d.path(poly([(44, 24), (116, 24), (116, 100), (44, 100)]), "card",
       fill=lin(CARD, CARD_LO, (44, 24), (116, 100)), stroke=INK,
       strokeWidth=4.5, join="round")
d.path(poly([(52, 32), (108, 32), (108, 78), (52, 78)]), "window",
       fill="#232B3A", stroke=INK, strokeWidth=3.5, join="round")
# dashed ghost inside the window: mountain pair + sun
gm = [(56, 72), (70, 52), (78, 62), (88, 48), (104, 72)]
dpath = f"M{T(*gm[0])[0]:.1f},{T(*gm[0])[1]:.1f} " + " ".join(
    f"L{T(x, y)[0]:.1f},{T(x, y)[1]:.1f}" for x, y in gm[1:])
d.path(dpath, "ghost mountains", fill=NONE, stroke="#8B98A5",
       strokeWidth=3, cap="round", join="round", dash=[5, 6], opacity=70)
gx, gy = T(66, 42)
d.shape("ellipse", "ghost sun", x=gx - 6, y=gy - 6, width=12, height=12,
        fill=NONE, stroke="#8B98A5", strokeWidth=3, dash=[4, 5], opacity=70)
# caption bar on the card
p0, p1 = T(58, 90), T(102, 90)
d.shape("line", "caption", x1=p0[0], y1=p0[1], x2=p1[0], y2=p1[1],
        stroke=CARD_LO, strokeWidth=5, cap="round", opacity=80)
# a small warm pin — the card is up on a corkboard of the mind
px, py = T(80, 24)
d.shape("ellipse", "pin", x=px - 5, y=py - 7, width=10, height=10,
        fill="#E04B35", stroke=INK, strokeWidth=3.5)

os.makedirs("work/out", exist_ok=True)
d.finish("spot-no-image-V1R00")
res = d.m.request("tools/call", {"name": "render_preview",
                                 "arguments": {"max_side": 320}})
for c in res.get("content", []):
    if "data" in c:
        open("work/out/spot-no-image-V1R00-preview.png", "wb").write(
            base64.b64decode(c["data"]))
