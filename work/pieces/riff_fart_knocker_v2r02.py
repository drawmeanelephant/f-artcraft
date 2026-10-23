#!/usr/bin/env python3
"""fart-knocker-V2R02 — fix pass on V2R01: the bowtie reads as a notch;
scale it up and let it straddle the face/shoulder seam. Opens V2R01,
saves V2R02."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from v2style import ship

d = Draw()
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "art")
d.open(f"{ART}/fart-knocker-V2R01.vectorcraft")

def find(name):
    r = d.call("run_command", {"command": "document.find",
                               "params": {"name": name, "limit": 10}}, f"find {name}")
    return [m["id"] for m in (r or {}).get("matches", [])]

ids = find("Bowtie") + find("Bowtie knot")
print("bowtie ids:", ids)
if ids:
    d.call("transform", {"ids": ids, "scale": 160, "dy": -12, "origin": [400, 610]},
           "grow + seat bowtie")

ship(d, "fart-knocker", "V2R02")
