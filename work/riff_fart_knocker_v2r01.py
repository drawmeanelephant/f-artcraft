#!/usr/bin/env python3
"""fart-knocker-V2R01 — fix pass on V2R00: the bowtie was drawn before the
shoulders and got buried; bring it forward and seat it at the neck seam.
Opens V2R00, saves V2R01."""
import os
from vc import Draw, NONE
from v2style import ship

d = Draw()
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "art")
d.open(f"{ART}/fart-knocker-V2R00.vectorcraft")

# find the bowtie objects and bring them to the front, nudged onto the shoulder
found = d.call("run_command", {"command": "document.find",
                               "params": {"name": "Bowtie", "limit": 10}}, "find bowtie")
ids = [m["id"] for m in (found or {}).get("matches", [])]
print("bowtie ids:", ids)
if ids:
    d.call("run_command", {"command": "select.set", "params": {"ids": ids}}, "select bowtie")
    d.call("transform", {"ids": ids, "dy": 26}, "seat bowtie")
    d.call("run_command", {"command": "object.arrange.bringToFront", "params": {}}, "bowtie to front")

ship(d, "fart-knocker", "V2R01")
