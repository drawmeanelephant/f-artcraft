#!/usr/bin/env python3
"""brand-about-emblem V1R00 — issue #1254.

The tight roundel version of the boot plate pairing: sexiburger mascot +
VIRELAIOS wordmark inside a navy roundel, for the About/sysinfo surface
and the launcher header (replaces the borrowed 64x64 mascot fixture).
256x256 master, drawn chunky enough to read at 64 px — bold shapes, no
fine detail that dies at quarter size. Declared navy field.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from virelai.vkit import DARK, NAVY, INK
from virelai.sexiburger import mascot

T = DARK
CREAM = "#F0E4BC"
d = Draw()
# transparent artboard: the roundel sits on chrome, so it must read on
# dark AND light surfaces (style bible: assets paint on both)
d.call("run_command", {"command": "file.new", "params": {
    "name": "VirelaiOS — brand about emblem", "width": 256, "height": 256,
    "units": "Pixels", "backgroundContents": "transparent",
    "colorMode": "rgb"}}, "file.new")

# --- navy roundel --------------------------------------------------------------
d.shape("ellipse", "roundel", x=8, y=8, width=240, height=240,
        fill=NAVY, stroke=T["Border"], strokeWidth=4)
d.shape("ellipse", "inner ring", x=22, y=22, width=212, height=212,
        fill=NONE, stroke=CREAM, strokeWidth=1.5, opacity=40)
# faint glow behind the mascot
d.shape("ellipse", "inner glow", x=44, y=30, width=168, height=150,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#2A2A44"},
            {"offset": 1, "color": "#1E1E2E"}]}}, stroke=NONE)

# --- mascot (arms out — fits the roundel's width) ------------------------------
mascot(d, 128, 34, 128, arms="out", detail=False)

# --- wordmark bar --------------------------------------------------------------
r = d.text("VIRELAIOS", "wordmark", x=128, y=182, size=24,
           font="Virelai Sans", color=CREAM, justify="center")
d.cmd("text.setStyle", "wordmark tracking", id=r["id"], tracking=110)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o:
            return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit:
                return hit
b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
dy = b["y"] + b["height"] / 2 + 2
for i, sx in enumerate([b["x"] - 12, b["x"] + b["width"] + 12]):
    d.shape("ellipse", f"flank dot{i}", x=sx - 3, y=dy - 3, width=6, height=6,
            fill=CREAM, opacity=55, stroke=NONE)

r = d.finish("brand-about-emblem-V1R00")
