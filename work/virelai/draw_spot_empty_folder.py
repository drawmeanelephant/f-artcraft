#!/usr/bin/env python3
"""spot-empty-folder V1R00 — issue #1253.

Empty-state spot for GOFILES: an open folder with nothing in it. 160x120
transparent master, must read at 80x60 on dark AND light surfaces —
mid-tone fills + warm INK outline do that work. One subject, no scene.
"""
import sys, os, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import INK

d = Draw()
d.call("run_command", {"command": "file.new", "params": {
    "name": "VirelaiOS — spot empty folder", "width": 160, "height": 120,
    "units": "Pixels", "backgroundContents": "transparent",
    "colorMode": "rgb"}}, "file.new")

TAN_HI, TAN, TAN_LO = "#E3C184", "#C9A86A", "#8F6E3C"
INSIDE = "#2A2118"                     # dark hollow, not pure black

def lin(c0, c1, start, end):
    return {"gradient": {"kind": "linear", "stops": [
        {"offset": 0, "color": c0}, {"offset": 1, "color": c1}],
        "start": list(start), "end": list(end)}}

def rr(x0, y0, x1, y1, r):
    return (f"M{x0+r},{y0} L{x1-r},{y0} Q{x1},{y0} {x1},{y0+r} L{x1},{y1-r} "
            f"Q{x1},{y1} {x1-r},{y1} L{x0+r},{y1} Q{x0},{y1} {x0},{y1-r} "
            f"L{x0},{y0+r} Q{x0},{y0} {x0+r},{y0} Z")

# folder back plate with the tab
d.path(f"M34,44 L66,44 L74,36 L100,36 Q106,36 106,42 L106,52 L126,52 "
       f"Q132,52 132,58 L132,96 Q132,102 126,102 L40,102 Q34,102 34,96 "
       f"L34,50 Q34,44 40,44 Z", "folder back",
       fill=lin(TAN, TAN_LO, (80, 36), (80, 102)), stroke=INK,
       strokeWidth=4.5, join="round")
# dark hollow mouth — the empty inside
d.path("M40,58 L126,58 L120,92 L46,92 Z", "empty inside",
       fill=INSIDE, stroke=NONE)
# faint echo dots drifting out — nothing but dust
for i, (x, y, w, o) in enumerate([(60, 50, 4, 45), (80, 44, 3, 35),
                                  (100, 50, 4, 40)]):
    d.shape("ellipse", f"mote{i}", x=x - w / 2, y=y - w / 2, width=w,
            height=w, fill="#F0E4BC", opacity=o, stroke=NONE)
# front flap, hinged open
d.path("M34,62 L126,62 L118,102 L42,102 Z", "folder flap",
       fill=lin(TAN_HI, TAN, (80, 62), (80, 102)), stroke=INK,
       strokeWidth=4.5, join="round")
d.shape("line", "flap lit edge", x1=42, y1=66, x2=118, y2=66,
        stroke="#F0DCB0", strokeWidth=3, opacity=70, cap="round")

os.makedirs("work/out", exist_ok=True)
d.finish("spot-empty-folder-V1R00")
res = d.m.request("tools/call", {"name": "render_preview",
                                 "arguments": {"max_side": 320}})
for c in res.get("content", []):
    if "data" in c:
        open("work/out/spot-empty-folder-V1R00-preview.png", "wb").write(
            base64.b64decode(c["data"]))
