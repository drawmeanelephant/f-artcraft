#!/usr/bin/env python3
"""spot-blank-document V1R00 — issue #1253.

Start something: a fresh sheet with a dog-ear, three faint ruled lines
and a waiting caret; a warm pencil rests at the corner. 160x120
transparent, reads at 80x60 on dark AND light. One subject.
"""
import sys, os, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import INK

d = Draw()
d.call("run_command", {"command": "file.new", "params": {
    "name": "VirelaiOS — spot blank document", "width": 160, "height": 120,
    "units": "Pixels", "backgroundContents": "transparent",
    "colorMode": "rgb"}}, "file.new")

PAPER, PAPER_LO = "#F4F7FB", "#C9D4E2"
RULE = "#8B98A5"
PENCIL = "#F59E0B"

def lin(c0, c1, start, end):
    return {"gradient": {"kind": "linear", "stops": [
        {"offset": 0, "color": c0}, {"offset": 1, "color": c1}],
        "start": list(start), "end": list(end)}}

def rr(x0, y0, x1, y1, r):
    return (f"M{x0+r},{y0} L{x1-r},{y0} Q{x1},{y0} {x1},{y0+r} L{x1},{y1-r} "
            f"Q{x1},{y1} {x1-r},{y1} L{x0+r},{y1} Q{x0},{y1} {x0},{y1-r} "
            f"L{x0},{y0+r} Q{x0},{y0} {x0+r},{y0} Z")

# sheet, slightly tall of square, dog-ear top right
d.path("M52,16 L96,16 L112,32 L112,100 Q112,106 106,106 L58,106 "
       "Q52,106 52,100 Z", "sheet",
       fill=lin(PAPER, PAPER_LO, (60, 16), (100, 106)), stroke=INK,
       strokeWidth=4.5, join="round")
d.path("M96,16 L96,30 Q96,34 100,34 L112,34", "dog ear", fill=NONE,
       stroke=INK, strokeWidth=3.5, join="round")
d.path("M96,16 L112,32 L98,32 Q96,32 96,30 Z", "ear shade", fill=PAPER_LO,
       stroke=NONE)
# three faint ruled lines — a start, not a document
for i in range(3):
    w = [34, 44, 26][i]
    d.shape("line", f"rule{i}", x1=62, y1=48 + i * 14, x2=62 + w,
            y2=48 + i * 14, stroke=RULE, strokeWidth=3.5, opacity=60,
            cap="round")
# the waiting caret
d.shape("line", "caret", x1=62, y1=84, x2=62, y2=96, stroke="#3B82F6",
        strokeWidth=4, cap="round")

# pencil resting at the lower right corner
d.path("M96,108 L132,88 L139,95 L103,115 Z", "pencil body", fill=PENCIL,
       stroke=INK, strokeWidth=3.5, join="round")
d.path("M132,88 L144,80 L139,95 Z", "pencil tip", fill="#F0E4BC",
       stroke=INK, strokeWidth=3.5, join="round")
d.path("M141,83 L144,80 L141.5,86 Z", "pencil lead", fill=INK, stroke=NONE)
d.shape("line", "pencil band", x1=100, y1=106, x2=105, y2=111, stroke=INK,
        strokeWidth=3, cap="round", opacity=60)

os.makedirs("work/out", exist_ok=True)
d.finish("spot-blank-document-V1R00")
res = d.m.request("tools/call", {"name": "render_preview",
                                 "arguments": {"max_side": 320}})
for c in res.get("content", []):
    if "data" in c:
        open("work/out/spot-blank-document-V1R00-preview.png", "wb").write(
            base64.b64decode(c["data"]))
