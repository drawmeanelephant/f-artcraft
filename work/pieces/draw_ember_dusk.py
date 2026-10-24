#!/usr/bin/env python3
"""Ember Dusk V1R00 — gradient-sky sunset: stars, sun, ridges, shimmer, birds.
800x600. The piece that started the V2 idiom."""
import random, os
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE
from tools.v2style import ship

d = Draw()
d.new_doc("Ember Dusk V1R00", 800, 600)
W, H, HORIZON = 800, 600, 430

d.shape("rectangle", "Sky", x=0, y=0, width=W, height=HORIZON + 60, stroke=NONE,
        fill={"gradient": {"kind": "linear", "start": [0, 0], "end": [0, HORIZON + 60],
              "stops": [{"offset": 0.00, "color": "#1b1035"},
                        {"offset": 0.35, "color": "#4a1d5e"},
                        {"offset": 0.65, "color": "#c94b32"},
                        {"offset": 0.88, "color": "#f79d4d"},
                        {"offset": 1.00, "color": "#ffd98e"}]}})

random.seed(11)
for i in range(28):
    sx, sy = random.uniform(15, W - 15), random.uniform(12, 200)
    r = random.uniform(0.8, 2.2)
    d.shape("ellipse", f"Star {i+1:02d}", x=sx - r, y=sy - r, width=2 * r, height=2 * r,
            fill="#fff6e8", stroke=NONE, opacity=random.randint(35, 90))

SUN_CX, SUN_CY, SUN_R = 560, 355, 58
d.shape("ellipse", "Sun halo", x=SUN_CX - 140, y=SUN_CY - 140, width=280, height=280,
        stroke=NONE, fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#ffb85c", "opacity": 0.55},
            {"offset": 1, "color": "#ffb85c", "opacity": 0}]}})
d.shape("ellipse", "Sun", x=SUN_CX - SUN_R, y=SUN_CY - SUN_R, width=2 * SUN_R, height=2 * SUN_R,
        stroke=NONE, fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#fff3c4"},
            {"offset": 0.7, "color": "#ffd76a"},
            {"offset": 1, "color": "#ff9a3d"}]}})

far = "M0,390 " + " ".join(f"L{x},{y}" for x, y in
      [(90, 300), (175, 355), (250, 285), (330, 360), (420, 315), (500, 375),
       (620, 330), (700, 380), (800, 345), (800, 390), (800, 470), (0, 470)]) + " Z"
d.path(far, "Mountains far", fill="#5a2d63", stroke=NONE, opacity=85)

d.path("M0,460 C80,440 80,438 160,438 C240,438 260,460 340,475 "
       "C430,492 470,498 560,485 C660,470 700,448 800,455 L800,600 L0,600 Z",
       "Dunes", stroke=NONE,
       fill={"gradient": {"kind": "linear", "start": [0, HORIZON], "end": [0, H],
             "stops": [{"offset": 0, "color": "#3a1740"},
                       {"offset": 1, "color": "#160a24"}]}})

random.seed(11)
for i in range(9):
    yy = HORIZON + 52 + i * 14
    ww = 90 + (i % 3) * 55 + (0 if i < 5 else -30)
    cx = SUN_CX + (-1) ** i * random.uniform(6, 26)
    d.shape("ellipse", f"Shimmer {i+1}", x=cx - ww / 2, y=yy, width=ww, height=4.5,
            fill="#ff9a3d", stroke=NONE, opacity=max(12, 48 - i * 4))

for i, (bx, by, s) in enumerate([(230, 150, 1.0), (290, 120, 0.75),
                                 (185, 195, 0.6), (640, 140, 0.85)]):
    d.path(f"M{bx-16*s},{by} L{bx},{by-9*s} L{bx+16*s},{by}", f"Bird {i+1}",
           fill=NONE, stroke="#1c0f2e", strokeWidth=2.4 * s, cap="round", join="round")

ship(d, "ember-dusk", "V1R00")
