#!/usr/bin/env python3
"""spot-trash-empty V1R00 — issue #1253.

Nothing to recover: a wire wastebasket with nothing in it, one small
clean glint. 160x120 transparent, reads at 80x60 on dark AND light.
One subject.
"""
import sys, os, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import INK

d = Draw()
d.call("run_command", {"command": "file.new", "params": {
    "name": "VirelaiOS — spot trash empty", "width": 160, "height": 120,
    "units": "Pixels", "backgroundContents": "transparent",
    "colorMode": "rgb"}}, "file.new")

STEEL_HI, STEEL, STEEL_LO = "#8B99AC", "#5E6E82", "#3C4657"

def lin(c0, c1, start, end):
    return {"gradient": {"kind": "linear", "stops": [
        {"offset": 0, "color": c0}, {"offset": 1, "color": c1}],
        "start": list(start), "end": list(end)}}

# tapered wire bin: wide mouth, narrow base; vertical slots make the weave
d.path("M46,30 L114,30 L104,102 Q103,108 96,108 L64,108 Q57,108 56,102 Z",
       "bin body", fill=lin(STEEL_HI, STEEL_LO, (50, 30), (110, 108)),
       stroke=INK, strokeWidth=4.5, join="round")
# mouth rim band
d.path("M42,26 L118,26 Q123,26 123,31 L122,36 Q121.5,40 116,40 L44,40 "
       "Q39,40 38,36 L37,31 Q37,26 42,26 Z", "rim",
       fill=lin(STEEL_HI, STEEL, (40, 26), (120, 40)), stroke=INK,
       strokeWidth=4.5, join="round")
# the dark empty mouth
d.path("M48,40 L112,40 L110,50 L50,50 Z", "empty mouth", fill="#232B3A",
       stroke=NONE, opacity=85)
# wire slots (the weave read)
for i, x in enumerate([58, 70, 82, 94, 104]):
    x_top = x - 6 + (x - 58) * 0.12
    d.shape("line", f"slot{i}", x1=46 + (x - 46) * 1.0, y1=56,
            x2=52 + (x - 52) * 0.82, y2=100, stroke=INK, strokeWidth=3,
            cap="round", opacity=55)
# hoop ring mid-bin
d.path("M50,74 L110,74", "hoop", fill=NONE, stroke=INK, strokeWidth=3,
       cap="round", opacity=55)

# one clean glint inside — nothing to recover, and it sparkles
d.path("M80,58 l3,7 l7,3 l-7,3 l-3,7 l-3,-7 l-7,-3 l7,-3 Z", "glint",
       fill="#F0E4BC", stroke=NONE, opacity=85)

os.makedirs("work/out", exist_ok=True)
d.finish("spot-trash-empty-V1R00")
res = d.m.request("tools/call", {"name": "render_preview",
                                 "arguments": {"max_side": 320}})
for c in res.get("content", []):
    if "data" in c:
        open("work/out/spot-trash-empty-V1R00-preview.png", "wb").write(
            base64.b64decode(c["data"]))
