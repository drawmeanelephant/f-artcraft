#!/usr/bin/env python3
"""mascot-sleep V1R00 — issue #1250.

Idle dim / screen-lock curtain: arms drooped, closed lid arcs, small o mouth, three cream Z's climbing off the dome.
64x64 master on transparent; same slot as the rest of the set
(mascot(d, 32, 5, 52, **POSES["sleep"])) so poses swap cleanly.
Proof gate: must read at 24 px — silhouette + eyes carry it.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.sexiburger import mascot, POSES

POSE = "sleep"
d = Draw()
d.call("run_command", {"command": "file.new", "params": {
    "name": f"VirelaiOS — mascot {POSE}", "width": 64, "height": 64,
    "units": "Pixels", "backgroundContents": "transparent",
    "colorMode": "rgb"}}, "file.new")

mascot(d, 32, 5, 52, **POSES[POSE])

r = d.finish(f"mascot-{POSE}-V1R00")
