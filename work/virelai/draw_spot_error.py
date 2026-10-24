#!/usr/bin/env python3
"""spot-error V1R00 — issue #1253.

Something broke: the mascot does the oops shrug — apologetic, not
alarming (the error spot apologizes). POSES['oops'] from the pose rig:
pupils aside, wavy mouth, shoulders-up gloves, sweat drop. A dropped
wrench at his feet is the only prop. 160x120 transparent, reads at 80x60.
"""
import sys, os, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import INK
from virelai.sexiburger import mascot, POSES

d = Draw()
d.call("run_command", {"command": "file.new", "params": {
    "name": "VirelaiOS — spot error", "width": 160, "height": 120,
    "units": "Pixels", "backgroundContents": "transparent",
    "colorMode": "rgb"}}, "file.new")

STEEL_LO = "#5E6E82"

# the apology
mascot(d, 82, 10, 96, **POSES["oops"])

# the dropped wrench that did it
d.path("M112,104 l10,-4 l18,10 l-4,8 l-18,-8 q-8,4 -10,-2 q-2,-4 4,-4 Z",
       "dropped wrench", fill=STEEL_LO, stroke=INK, strokeWidth=3.5,
       join="round")

os.makedirs("work/out", exist_ok=True)
d.finish("spot-error-V1R00")
res = d.m.request("tools/call", {"name": "render_preview",
                                 "arguments": {"max_side": 320}})
for c in res.get("content", []):
    if "data" in c:
        open("work/out/spot-error-V1R00-preview.png", "wb").write(
            base64.b64decode(c["data"]))
