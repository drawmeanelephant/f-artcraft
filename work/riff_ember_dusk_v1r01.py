#!/usr/bin/env python3
"""Ember Dusk V1R01 — riff on V1R00: atmospheric back ridge, cloud streaks,
crescent moon, shooting star, vignette. Opens V1R00, saves V1R01 (AGENTS.md
revision rule: never overwrite)."""
import os
from vc import Draw, NONE
from v2style import ship

d = Draw()
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "art")
d.open(f"{ART}/ember-dusk-V1R00.vectorcraft")

# atmospheric back ridge: lighter silhouette behind the far mountains
back = "M0,415 " + " ".join(f"L{x},{y}" for x, y in
       [(70, 360), (150, 395), (240, 350), (310, 390), (410, 355), (480, 400),
        (560, 370), (660, 405), (740, 365), (800, 395), (800, 470), (0, 470)]) + " Z"
d.path(back, "Mountains back", fill="#8a5580", stroke=NONE, opacity=50)
d.cmd("object.arrange.sendToBack", "ridge to back")
d.cmd("object.arrange.bringForward", "ridge above sky")

def cloud(name, cx, cy, w, h, color, opacity):
    d.shape("ellipse", name, x=cx - w / 2, y=cy - h / 2, width=w, height=h,
            stroke=NONE, opacity=opacity,
            fill={"gradient": {"kind": "radial", "stops": [
                {"offset": 0, "color": color, "opacity": 1},
                {"offset": 1, "color": color, "opacity": 0}]}})

cloud("Cloud ember 1", 520, 250, 380, 26, "#ff8a4d", 30)
cloud("Cloud ember 2", 300, 300, 300, 18, "#ff9a5c", 22)
cloud("Cloud mauve 1", 180, 175, 340, 20, "#b06a9e", 26)
cloud("Cloud mauve 2", 620, 120, 260, 14, "#9e5f96", 22)

# crescent moon: disc minus an offset disc
r = d.shape("ellipse", "Moon disc", x=90, y=70, width=56, height=56, fill="#f5e9c8", stroke=NONE)
moon_id = (r or {}).get("id")
r = d.shape("ellipse", "Moon cutter", x=106, y=60, width=56, height=56, fill="#000000", stroke=NONE)
cutter_id = (r or {}).get("id")
if moon_id and cutter_id:
    d.call("run_command", {"command": "select.set", "params": {"ids": [moon_id, cutter_id]}}, "select moon pair")
    d.call("pathfinder", {"operation": "minusFront"}, "crescent")
    d.cmd("object.setProps", "name moon", name="Moon")
d.shape("ellipse", "Moon glow", x=60, y=40, width=116, height=116, stroke=NONE,
        opacity=18, fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#f5e9c8"}, {"offset": 1, "color": "#f5e9c8", "opacity": 0}]}})
d.cmd("object.arrange.sendBackward", "glow behind moon")

# shooting star
d.path("M680,60 L760,95", "Shooting star", fill=NONE, stroke="#ffe9c9", strokeWidth=2.2, cap="round")
d.cmd("stroke.set", "taper streak", profile="taperEnd")
d.shape("ellipse", "Shooting head", x=758, y=92, width=7, height=7, fill="#fff6e8", stroke=NONE)

# vignette
d.shape("rectangle", "Vignette", x=0, y=0, width=800, height=600, stroke=NONE,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#120722", "opacity": 0},
            {"offset": 0.62, "color": "#120722", "opacity": 0},
            {"offset": 1, "color": "#120722", "opacity": 0.38}]}})

ship(d, "ember-dusk", "V1R01")
