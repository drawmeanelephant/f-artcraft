#!/usr/bin/env python3
"""spot-no-results V1R00 — issue #1253.

The find came back dry: a magnifier over a dashed not-found ring. 160x120
transparent master, reads at 80x60 on dark AND light. One subject.
"""
import sys, os, math, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import INK

d = Draw()
d.call("run_command", {"command": "file.new", "params": {
    "name": "VirelaiOS — spot no results", "width": 160, "height": 120,
    "units": "Pixels", "backgroundContents": "transparent",
    "colorMode": "rgb"}}, "file.new")

STEEL_HI, STEEL_LO = "#8B99AC", "#4A5468"
GLASS = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8E4F0", "opacity": 0.35},
    {"offset": 1, "color": "#D8E4F0", "opacity": 0.10}]}}

def lin(c0, c1, start, end):
    return {"gradient": {"kind": "linear", "stops": [
        {"offset": 0, "color": c0}, {"offset": 1, "color": c1}],
        "start": list(start), "end": list(end)}}

CX, CY, R = 70, 52, 34

# handle first (behind the rim), angled down-right
hx = CX + R * 0.72; hy = CY + R * 0.72
d.path(f"M{hx},{hy} L{hx + 34},{hy + 34}", "handle", fill=NONE,
       stroke=INK, strokeWidth=15, cap="round")
d.path(f"M{hx},{hy} L{hx + 34},{hy + 34}", "handle fill", fill=NONE,
       stroke=STEEL_LO, strokeWidth=8, cap="round")
# glass + rim
d.shape("ellipse", "glass", x=CX - R + 6, y=CY - R + 6, width=2 * (R - 6),
        height=2 * (R - 6), fill=GLASS, stroke=NONE)
d.shape("ellipse", "rim", x=CX - R, y=CY - R, width=2 * R, height=2 * R,
        fill=NONE, stroke=INK, strokeWidth=9)
d.shape("ellipse", "rim band", x=CX - R, y=CY - R, width=2 * R, height=2 * R,
        fill=NONE, stroke={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": STEEL_HI},
            {"offset": 1, "color": STEEL_LO}]}}, strokeWidth=5)
# inside the lens: the dashed not-found ring, a couple of dry specks
dr = 13
seg = 10
for i in range(6):
    a0 = math.radians(i * 60 + 10)
    a1 = math.radians(i * 60 + 10 + 38)
    am = math.radians(i * 60 + 10 + 19)
    x0, y0 = CX + dr * math.cos(a0), CY + dr * math.sin(a0)
    x1, y1 = CX + dr * math.cos(a1), CY + dr * math.sin(a1)
    qx, qy = CX + dr * 1.35 * math.cos(am), CY + dr * 1.35 * math.sin(am)
    d.path(f"M{x0:.1f},{y0:.1f} Q{qx:.1f},{qy:.1f} {x1:.1f},{y1:.1f}",
           f"dry{i}", fill=NONE, stroke="#8B98A5", strokeWidth=3,
           cap="round", opacity=75)
d.shape("ellipse", "speck", x=CX - 3, y=CY - 3, width=6, height=6,
        fill="#8B98A5", opacity=55, stroke=NONE)
# glint on the rim
d.path(f"M{CX - R * 0.6},{CY - R * 0.72} Q{CX - R * 0.15},{CY - R * 0.95} "
       f"{CX + R * 0.35},{CY - R * 0.78}", "rim glint", fill=NONE,
       stroke="#D8E4F0", strokeWidth=4, cap="round", opacity=80)

os.makedirs("work/out", exist_ok=True)
d.finish("spot-no-results-V1R00")
res = d.m.request("tools/call", {"name": "render_preview",
                                 "arguments": {"max_side": 320}})
for c in res.get("content", []):
    if "data" in c:
        open("work/out/spot-no-results-V1R00-preview.png", "wb").write(
            base64.b64decode(c["data"]))
