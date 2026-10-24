#!/usr/bin/env python3
"""HAI-0004 Boily McPlaterton — haiku plate V1R00. Thermal meltdown made
visual: warped casing, screaming fan, smoke rising, eight haiku stanzas
flanking a central overheating core. Thermal palette. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("HAI-0004 Boily McPlaterton — Haiku Plate", 1000, 1000)

INK = "#2A140E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#22100B"}, {"offset": 1, "color": "#0C0403"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A3222"}, {"offset": 0.7, "color": "#481C12"},
    {"offset": 1, "color": "#240D08"}]}}
CASE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8985E"}, {"offset": 0.6, "color": "#C46838"},
    {"offset": 1, "color": "#8A3A22"}]}}
CORE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFF3C8"}, {"offset": 0.45, "color": "#FFB45E"},
    {"offset": 1, "color": "#D84A22"}]}}
CHIP = "#2A0E08"
CREAM = "#F2D4B0"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A1A0E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8A87A", strokeWidth=3, opacity=45)
# heat bloom behind the whole scene
d.shape("ellipse", "Heat bloom", x=250, y=270, width=500, height=500,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#E86A3A", "opacity": 0.4},
            {"offset": 1, "color": "#E86A3A", "opacity": 0}]}},
        stroke=NONE)

# --- title ----------------------------------------------------------------------
d.text("Thermal spike is high", "Title 1", x=500, y=152, size=20,
       font="Virelai Sans", color=CREAM, justify="center")
d.text("meaning bends around the heat", "Title 2", x=500, y=182, size=20,
       font="Virelai Sans", color="#E8B88A", justify="center")

# --- Boily: warped casing, cracked open on the core ------------------------------
# translucent heat haze columns flanking the casing
d.shape("ellipse", "Haze L", x=330, y=420, width=90, height=270,
        fill="#E86A3A", opacity=12, stroke=NONE)
d.shape("ellipse", "Haze R", x=580, y=420, width=90, height=270,
        fill="#E86A3A", opacity=12, stroke=NONE)
# warped tower: sides bow outward, top sags — the casing is melting
d.path("M412,418 C384,510 388,620 404,732 L596,732 "
       "C612,620 616,510 588,418 Q500,402 412,418 Z",
       "Boily casing", fill=CASE_GRAD, stroke=INK, strokeWidth=6)
# casing sheen + baked shadow at the bottom
d.path("M430,440 C416,520 418,620 428,710", "Casing sheen",
       fill=NONE, stroke="#FFE0B8", strokeWidth=10, opacity=20, cap="round")
d.path("M420,700 L580,700 L596,732 L404,732 Z", "Base shadow",
       fill="#6A2818", opacity=50, stroke=NONE)
# the casing has split: a jagged void with the overheating core burning inside
d.path("M486,428 L514,486 L492,544 L522,602 L500,648 "
       "L506,596 L478,540 L500,482 L478,430 Z",
       "Split void", fill="#1E0803", stroke=NONE)
d.path("M492,436 L510,488 L490,542 L514,596 L500,634 "
       "L502,592 L484,540 L498,486 L484,438 Z",
       "Split glow", fill=CORE_GRAD, stroke=NONE)
d.path("M494,442 L506,488 L490,540 L508,590 L500,622 "
       "L498,588 L488,538 L496,488 L488,444 Z",
       "Split heart", fill="#FFF3C8", opacity=85, stroke=NONE)
# worried face high on the casing, held clear of the split
d.shape("ellipse", "Eye L", x=430, y=468, width=16, height=22,
        fill="#2A0E06", stroke=NONE)
d.shape("ellipse", "Eye R", x=556, y=468, width=16, height=22,
        fill="#2A0E06", stroke=NONE)
d.shape("ellipse", "Glint L", x=434, y=473, width=4, height=4,
        fill="#FFFFFF", opacity=80, stroke=NONE)
d.shape("ellipse", "Glint R", x=560, y=473, width=4, height=4,
        fill="#FFFFFF", opacity=80, stroke=NONE)
d.path("M426,454 Q438,445 450,451", "Brow L", fill=NONE,
       stroke="#2A0E06", strokeWidth=4, cap="round")
d.path("M552,451 Q564,445 576,454", "Brow R", fill=NONE,
       stroke="#2A0E06", strokeWidth=4, cap="round")
d.shape("ellipse", "Mouth", x=424, y=516, width=52, height=32,
        fill="#2A0E06", stroke=NONE)
d.shape("ellipse", "Mouth heat", x=437, y=529, width=28, height=13,
        fill="#E86A3A", opacity=60, stroke=NONE)
# screaming fan low in the casing
d.shape("ellipse", "Fan ring", x=448, y=596, width=104, height=104,
        fill="#3A1A10", stroke=INK, strokeWidth=4)
import math
for i, ang in enumerate([0, 60, 120, 180, 240, 300]):
    a1 = math.radians(ang + 18)
    a2 = math.radians(ang + 50)
    x1 = 500 + math.cos(a1) * 36
    y1 = 648 + math.sin(a1) * 36
    x2 = 500 + math.cos(a2) * 19
    y2 = 648 + math.sin(a2) * 19
    d.path(f"M500,648 L{x2:.0f},{y2:.0f} L{x1:.0f},{y1:.0f} Z",
           f"Fan blade {i+1}", fill="#C9B68E", opacity=85, stroke=NONE)
d.shape("ellipse", "Fan hub", x=489, y=637, width=22, height=22,
        fill=CORE_GRAD, stroke=INK, strokeWidth=2)
d.path("M444,614 A64,64 0 0 1 556,606", "Spin arc 1", fill=NONE,
       stroke=CREAM, strokeWidth=3, opacity=50, cap="round")
d.path("M448,694 A64,64 0 0 0 558,686", "Spin arc 2", fill=NONE,
       stroke=CREAM, strokeWidth=3, opacity=50, cap="round")
# core glow venting through the top seam
d.shape("ellipse", "Core vent", x=432, y=406, width=136, height=26,
        fill=CORE_GRAD, opacity=80, stroke=NONE)
# smoke column rising off the top
for i, (sx, sy, sw, sh, op) in enumerate([(462, 356, 58, 34, 42),
                                          (434, 318, 76, 44, 34),
                                          (478, 278, 92, 52, 26),
                                          (446, 234, 106, 58, 18)]):
    d.shape("ellipse", f"Smoke {i+1}", x=sx, y=sy, width=sw, height=sh,
            fill="#C9B6A4", opacity=op, stroke=NONE)
# sparks popping off the warped edges
for i, (sx, sy, sr) in enumerate([(398, 492, 6), (604, 532, 5),
                                   (402, 636, 5), (600, 614, 6)]):
    d.path(f"M{sx},{sy-sr} L{sx+sr*0.3},{sy-sr*0.3} L{sx+sr},{sy} "
           f"L{sx+sr*0.3},{sy+sr*0.3} L{sx},{sy+sr} L{sx-sr*0.3},{sy+sr*0.3} "
           f"L{sx-sr},{sy} L{sx-sr*0.3},{sy-sr*0.3} Z",
           f"Spark {i+1}", fill="#FFD98A", opacity=85, stroke=NONE)

# --- eight haiku stanzas flanking the core --------------------------------------
STANZAS_L = [
    ("casing softens now", "rivets weep in warm dark", "shape forgets itself"),
    ("smoke writes its own verse", "grey columns rising slow", "the room reads along"),
    ("the fans are screaming", "eight thousand rpm", "no one turns them down"),
    ("thermal paste was never", "applied in this lifetime", "the manual wept"),
]
STANZAS_R = [
    ("form 88-b filed", "in triplicate flames", "stamped insufficient"),
    ("heat bends the meaning", "words warp around the core", "still the verse holds"),
    ("capacitors pop", "like small fireworks", "goodnight, motherboard"),
    ("silent thought descends", "the chassis cools at last", "fans forget to scream"),
]
def stanza_chip(x, y, lines, side, idx):
    d.shape("rectangle", f"Stanza {side}{idx} chip", x=x, y=y, width=196,
            height=70, radius=8, fill=CHIP, opacity=72,
            stroke="#E8A87A", strokeWidth=1.5)
    for j, line in enumerate(lines):
        d.text(line, f"Stanza {side}{idx} line {j+1}", x=x + 98,
               y=y + 21 + j * 18, size=11.5, font="Virelai Sans",
               color=CREAM, justify="center")

for i, lines in enumerate(STANZAS_L):
    stanza_chip(132, 292 + i * 102, lines, "L", i + 1)
for i, lines in enumerate(STANZAS_R):
    stanza_chip(672, 292 + i * 102, lines, "R", i + 1)
# --- name + role ------------------------------------------------------------------
d.text("BOILY MCPLATERTON", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("HAI-0004 BOILY MCPLATERTON", "Role", x=500, y=968, size=19,
           font="Virelai Sans", color="#C9906A", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=180)

d.finish("hai-004-boily-mcplaterton-V1R00")
