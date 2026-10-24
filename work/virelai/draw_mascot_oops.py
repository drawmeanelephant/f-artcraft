#!/usr/bin/env python3
"""mascot-oops V1R00 — issue #1250.

Error banners / crash receipts / empty states: apologetic shrug (both gloves up at shoulder height), wavy mouth, sideways pupils, sweat drop.
64x64 master on transparent; same slot as the rest of the set
(mascot(d, 32, 5, 52, **POSES["oops"])) so poses swap cleanly.
Proof gate: must read at 24 px — silhouette + eyes carry it.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.sexiburger import mascot, POSES

POSE = "oops"
d = Draw()
d.call("run_command", {"command": "file.new", "params": {
    "name": f"VirelaiOS — mascot {POSE}", "width": 64, "height": 64,
    "units": "Pixels", "backgroundContents": "transparent",
    "colorMode": "rgb"}}, "file.new")

mascot(d, 32, 5, 52, **POSES[POSE])

r = d.finish(f"mascot-{POSE}-V1R00")
