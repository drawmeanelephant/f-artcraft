#!/usr/bin/env python3
"""bunny-avatar-V2R01 — fix pass on V2R00: the bowtie is dark-on-dark and
reads as a nick in the head's edge; scale it up and warm it so it separates.
Opens V2R00, saves V2R01."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from tools.v2style import ship

d = Draw()
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "art")
d.open(f"{ART}/bunny-avatar-V2R00.vectorcraft")

def find(name):
    r = d.call("run_command", {"command": "document.find",
                               "params": {"name": name, "limit": 10}}, f"find {name}")
    return [m["id"] for m in (r or {}).get("matches", [])]

ids = find("Bowtie") + find("Knot")
print("bowtie ids:", ids)
if ids:
    d.call("transform", {"ids": ids, "scale": 150, "origin": [500, 770]}, "grow bowtie")
    d.call("run_command", {"command": "paint.setFill",
                           "params": {"ids": ids, "color": "#2e2620"}}, "warm bowtie")

ship(d, "bunny-avatar", "V2R01")
