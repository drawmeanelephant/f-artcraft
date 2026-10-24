#!/usr/bin/env python3
"""spot-no-notifications V1R00 — issue #1253.

The bell is quiet: a resting bell with clapper still, and three faint
rest-dots where a ring would be. 160x120 transparent, reads at 80x60 on
dark AND light. One subject.
"""
import sys, os, math, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import INK

d = Draw()
d.call("run_command", {"command": "file.new", "params": {
    "name": "VirelaiOS — spot no notifications", "width": 160, "height": 120,
    "units": "Pixels", "backgroundContents": "transparent",
    "colorMode": "rgb"}}, "file.new")

BRASS_HI, BRASS, BRASS_LO = "#F0D08A", "#D8A94E", "#9C7230"

def lin(c0, c1, start, end):
    return {"gradient": {"kind": "linear", "stops": [
        {"offset": 0, "color": c0}, {"offset": 1, "color": c1}],
        "start": list(start), "end": list(end)}}

# bell dome: crown knob + swept body + skirt flare + clapper
d.shape("ellipse", "crown", x=73, y=16, width=14, height=12,
        fill=lin(BRASS_HI, BRASS, (80, 16), (80, 28)), stroke=INK,
        strokeWidth=4)
d.path("M80,24 C60,26 48,44 46,66 C45,78 40,84 34,88 "
       "Q30,92 36,94 L124,94 Q130,92 126,88 C120,84 115,78 114,66 "
       "C112,44 100,26 80,24 Z", "bell body",
       fill=lin(BRASS_HI, BRASS_LO, (56, 24), (110, 94)), stroke=INK,
       strokeWidth=4.5, join="round")
# lit edge on the dome's upper left
d.path("M56,60 C58,44 66,34 78,31", "bell lit edge", fill=NONE,
       stroke="#F6E2AE", strokeWidth=3.5, cap="round", opacity=75)
# mouth rim + resting clapper
d.shape("line", "mouth rim", x1=40, y1=94, x2=120, y2=94, stroke=INK,
        strokeWidth=4.5, cap="round", opacity=90)
d.shape("ellipse", "clapper", x=73, y=94, width=14, height=11,
        fill=lin(BRASS, BRASS_LO, (80, 94), (80, 105)), stroke=INK,
        strokeWidth=4)
# the quiet: three rest-dots where ring arcs would be, upper right
for i, (x, y, w) in enumerate([(122, 48, 4), (131, 38, 4), (140, 29, 4)]):
    d.shape("ellipse", f"rest{i}", x=x - w / 2, y=y - w / 2, width=w,
            height=w, fill="#94A3B8", opacity=55 - i * 12, stroke=NONE)
# a faint dust speck on the dome — it's been quiet a while
d.shape("ellipse", "dust", x=94, y=40, width=4, height=3, fill="#F6E2AE",
        opacity=40, stroke=NONE)

os.makedirs("work/out", exist_ok=True)
d.finish("spot-no-notifications-V1R00")
res = d.m.request("tools/call", {"name": "render_preview",
                                 "arguments": {"max_side": 320}})
for c in res.get("content", []):
    if "data" in c:
        open("work/out/spot-no-notifications-V1R00-preview.png", "wb").write(
            base64.b64decode(c["data"]))
