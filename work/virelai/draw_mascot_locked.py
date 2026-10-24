#!/usr/bin/env python3
"""mascot-locked V1R00 — issue #1250.

Lock screen / vault: both arms in holding a padlock at the chest, angled guard brows, flat mouth.
64x64 master on transparent; same slot as the rest of the set
(mascot(d, 32, 5, 52, **POSES["locked"])) so poses swap cleanly.
Proof gate: must read at 24 px — silhouette + eyes carry it.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.sexiburger import mascot, POSES

POSE = "locked"
d = Draw()
d.call("run_command", {"command": "file.new", "params": {
    "name": f"VirelaiOS — mascot {POSE}", "width": 64, "height": 64,
    "units": "Pixels", "backgroundContents": "transparent",
    "colorMode": "rgb"}}, "file.new")

mascot(d, 32, 5, 52, **POSES[POSE])

r = d.finish(f"mascot-{POSE}-V1R00")
