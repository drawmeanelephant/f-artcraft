#!/usr/bin/env python3
"""spot-offline V1R00 — issue #1253.

No network: an unplugged cable end — chunky plug hanging loose with a
slack curl, and a dashed arc where the link would be. 160x120 transparent,
reads at 80x60 on dark AND light. One subject.
"""
import sys, os, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import INK

d = Draw()
d.call("run_command", {"command": "file.new", "params": {
    "name": "VirelaiOS — spot offline", "width": 160, "height": 120,
    "units": "Pixels", "backgroundContents": "transparent",
    "colorMode": "rgb"}}, "file.new")

STEEL_HI, STEEL, STEEL_LO = "#8B99AC", "#5E6E82", "#3C4657"
BRASS = "#E8C26A"

def lin(c0, c1, start, end):
    return {"gradient": {"kind": "linear", "stops": [
        {"offset": 0, "color": c0}, {"offset": 1, "color": c1}],
        "start": list(start), "end": list(end)}}

def rr(x0, y0, x1, y1, r):
    return (f"M{x0+r},{y0} L{x1-r},{y0} Q{x1},{y0} {x1},{y0+r} L{x1},{y1-r} "
            f"Q{x1},{y1} {x1-r},{y1} L{x0+r},{y1} Q{x0},{y1} {x0},{y1-r} "
            f"L{x0},{y0+r} Q{x0},{y0} {x0+r},{y0} Z")

# slack cable curling in from the lower left, ending at the plug neck
d.path("M20,104 C30,84 44,96 52,80 C58,68 54,60 62,54", "cable",
       fill=NONE, stroke=INK, strokeWidth=12, cap="round")
d.path("M20,104 C30,84 44,96 52,80 C58,68 54,60 62,54", "cable skin",
       fill=NONE, stroke=STEEL_LO, strokeWidth=6, cap="round")
# plug body, tilted — two-prong barrel connector hanging free
d.path("M58,62 L74,46 L104,74 L88,92 Z", "plug body",
       fill=lin(STEEL_HI, STEEL_LO, (60, 50), (100, 90)), stroke=INK,
       strokeWidth=4.5, join="round")
d.path("M74,46 L86,34 L110,58 L104,74 Z", "plug collar",
       fill=lin(STEEL, STEEL_LO, (80, 36), (108, 70)), stroke=INK,
       strokeWidth=4.5, join="round")
# the two prongs, brass tips
d.path("M92,36 L100,18", "prong a", fill=NONE, stroke=INK, strokeWidth=10,
       cap="round")
d.path("M92,36 L100,18", "prong a tip", fill=NONE, stroke=BRASS,
       strokeWidth=5, cap="round")
d.path("M104,48 L112,30", "prong b", fill=NONE, stroke=INK, strokeWidth=10,
       cap="round")
d.path("M104,48 L112,30", "prong b tip", fill=NONE, stroke=BRASS,
       strokeWidth=5, cap="round")
# dashed link arc where the connection would be, upper right
import math
for i in range(3):
    a0 = math.radians(-150 + i * 32)
    a1 = math.radians(-150 + i * 32 + 20)
    cx, cy, r = 138, 40, 26
    x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    am = math.radians(-150 + i * 32 + 10)
    qx, qy = cx + r * 1.35 * math.cos(am), cy + r * 1.35 * math.sin(am)
    d.path(f"M{x0:.1f},{y0:.1f} Q{qx:.1f},{qy:.1f} {x1:.1f},{y1:.1f}",
           f"ghost{i}", fill=NONE, stroke="#8B98A5", strokeWidth=3.5,
           cap="round", opacity=55)

os.makedirs("work/out", exist_ok=True)
d.finish("spot-offline-V1R00")
res = d.m.request("tools/call", {"name": "render_preview",
                                 "arguments": {"max_side": 320}})
for c in res.get("content", []):
    if "data" in c:
        open("work/out/spot-offline-V1R00-preview.png", "wb").write(
            base64.b64decode(c["data"]))
