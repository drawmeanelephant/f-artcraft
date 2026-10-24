#!/usr/bin/env python3
"""APH-034 Sol Burnout — motivational-poster aphorism plate V1R00.
A KEEP GOING poster: a CRT terminal burning steady orange phosphor beside
a server tower that has been hot for years — drive bays, pegged thermal
gauge, heat shimmer rising off the vents, one red LED still loyal.
Ember orange on charred umber. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-034 Sol Burnout — Motivational Poster", 1000, 1000)

INK = "#120906"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#241610"}, {"offset": 1, "color": "#0C0605"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5C3420"}, {"offset": 0.7, "color": "#2E190F"},
    {"offset": 1, "color": "#120906"}]}}
POSTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A1A12"}, {"offset": 1, "color": "#150C08"}]}}
CRT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A382C"}, {"offset": 1, "color": "#241A12"}]}}
SCR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8862E"}, {"offset": 0.65, "color": "#A8541A"},
    {"offset": 1, "color": "#4A2008"}]}}
CHASSIS_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E3E32"}, {"offset": 1, "color": "#221710"}]}}
BAY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#362A20"}, {"offset": 1, "color": "#1A120C"}]}}
GOLD = "#E8A050"
FRAME = "#C0A880"
HEAD = "#F4EADC"
PUNCH = "#E8D2BC"
CREAM = "#F4EADC"
FAINT = "#A08468"
ORANGE = "#F09838"
PHOS = "#FFC46A"
EMBER = "#B85A1E"
REDL = "#E85A3A"
GRNL = "#7FD87A"
METAL = "#6A5A48"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A4A2A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8B070", strokeWidth=3, opacity=30)
d.shape("ellipse", "Patina 1", x=200, y=170, width=200, height=110,
        fill="#6E4228", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=620, width=200, height=110,
        fill="#6E4228", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(215, 280, 7), (790, 255, 8), (165, 480, 6),
                               (838, 475, 7), (250, 655, 6), (755, 665, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#7A5030", opacity=35, stroke=NONE)
# embers drifting on the plate
for i, (x, y, w, op) in enumerate([(300, 210, 4, 55), (690, 180, 3, 45),
                                   (810, 350, 4, 50), (210, 420, 3, 40),
                                   (330, 560, 3, 45), (700, 590, 4, 50)]):
    d.shape("ellipse", f"Ember {i+1}", x=x, y=y, width=w, height=w,
            fill=ORANGE, opacity=op, stroke=NONE)

# --- the poster card -------------------------------------------------------------
PX, PY, PW, PH = 220, 150, 560, 440
d.shape("rectangle", "Poster shadow", x=PX + 8, y=PY + 10, width=PW,
        height=PH, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Poster", x=PX, y=PY, width=PW, height=PH,
        fill=POSTER_GRAD, stroke="#4A3222", strokeWidth=4)
d.shape("rectangle", "Frame outer", x=PX + 16, y=PY + 16,
        width=PW - 32, height=PH - 32, fill=NONE, stroke=FRAME,
        strokeWidth=2, opacity=80)
d.shape("rectangle", "Frame inner", x=PX + 24, y=PY + 24,
        width=PW - 48, height=PH - 48, fill=NONE, stroke=GOLD,
        strokeWidth=1.5, opacity=60)

# kicker + two-line headline
r = d.text("KEEP GOING", "Kicker", x=500, y=PY + 40, size=12,
           font="Virelai Sans", color=GOLD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "kicker tracking", ids=[r["id"]], tracking=300)
r = d.text("THE SYSTEM HAS BEEN", "Headline 1", x=500, y=PY + 72,
           size=30, font="Virelai Sans", color=HEAD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "h1 tracking", ids=[r["id"]], tracking=60)
r = d.text("RUNNING SO LONG", "Headline 2", x=500, y=PY + 104,
           size=30, font="Virelai Sans", color=HEAD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "h2 tracking", ids=[r["id"]], tracking=60)
d.path("M370,272 L462,272 M538,272 L630,272", "Headline rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=80)
d.path(rot_rect_path(500, 272, 10, 10, 45), "Headline diamond",
       fill=GOLD, opacity=85, stroke=NONE)

# --- shared heat glow behind the scene ----------------------------------------------
d.shape("ellipse", "Heat glow", x=330, y=330, width=360, height=190,
        fill=ORANGE, opacity=10, stroke=NONE)
# desk shadow
d.shape("ellipse", "Desk shadow", x=285, y=472, width=440, height=18,
        fill="#000000", opacity=35, stroke=NONE)

# --- the CRT terminal, orange phosphor ---------------------------------------------------
MX, MY, MW, MH = 292, 308, 214, 144
# shell
d.shape("rectangle", "CRT shell", x=MX, y=MY, width=MW, height=MH,
        radius=12, fill=CRT_GRAD, stroke="#181008", strokeWidth=3)
# bezel inner edge
d.shape("rectangle", "CRT bezel", x=MX + 10, y=MY + 10, width=MW - 20,
        height=MH - 44, radius=8, fill="#120A06", stroke="#0C0604",
        strokeWidth=2)
# the burning screen
SX, SY, SW, SH = MX + 16, MY + 16, MW - 32, MH - 56
d.shape("rectangle", "CRT screen", x=SX, y=SY, width=SW, height=SH,
        radius=6, fill=SCR_GRAD, stroke=NONE)
# glass glare
d.path(f"M{SX + 10},{SY + 8} Q{SX + SW/2},{SY - 4} {SX + SW - 20},{SY + 12} "
       f"Q{SX + SW/2},{SY + 16} {SX + 14},{SY + 22} Z",
       "Screen glare", fill="#FFE0B0", opacity=18, stroke=NONE)
# scanlines
for j in range(5):
    ly = SY + 10 + j * 14
    d.path(f"M{SX + 4},{ly} L{SX + SW - 4},{ly}", f"Scan {j+1}",
           fill=NONE, stroke="#3A1A08", strokeWidth=2, opacity=35)
# phosphor text: it has stopped checking
d.text("> uptime", "Term line 1", x=SX + 10, y=SY + 18, size=10,
       font="Source Sans 3", color="#FFE8C0", justify="left")
d.text("  forever", "Term line 2", x=SX + 10, y=SY + 32, size=10,
       font="Source Sans 3", color=PHOS, justify="left")
d.text("> load: MAX", "Term line 3", x=SX + 10, y=SY + 50, size=10,
       font="Source Sans 3", color="#FFE8C0", justify="left")
d.text("> stop? ", "Term line 4", x=SX + 10, y=SY + 68, size=10,
       font="Source Sans 3", color=PHOS, justify="left")
d.shape("rectangle", "Term cursor", x=SX + 58, y=SY + 60, width=7,
        height=11, fill="#FFE8C0", opacity=90, stroke=NONE)
# chin: power LED + brand
d.shape("ellipse", "CRT power LED", x=MX + MW - 22, y=MY + MH - 22,
        width=7, height=7, fill=GRNL, opacity=85, stroke=NONE)
d.text("SOL-9", "CRT brand", x=MX + 16, y=MY + MH - 12, size=8,
       font="Source Sans 3", color=FAINT, justify="left")
# stand
d.shape("rectangle", "CRT stand", x=MX + MW/2 - 30, y=MY + MH - 4,
        width=60, height=16, radius=3, fill=CRT_GRAD, stroke="#181008",
        strokeWidth=2.5)
d.shape("rectangle", "CRT foot", x=MX + MW/2 - 44, y=MY + MH + 10,
        width=88, height=8, radius=4, fill=CRT_GRAD, stroke="#181008",
        strokeWidth=2)

# --- the server tower, still hot ----------------------------------------------------------
VX, VY, VW, VH = 580, 298, 128, 176
d.shape("rectangle", "Server", x=VX, y=VY, width=VW, height=VH, radius=8,
        fill=CHASSIS_GRAD, stroke="#160E08", strokeWidth=3)
# hot rim light on the left edge facing the CRT
d.path(f"M{VX + 3},{VY + 10} L{VX + 3},{VY + VH - 10}", "Rim light",
       fill=NONE, stroke=ORANGE, strokeWidth=3, cap="round", opacity=55)
# drive bays
for j in range(3):
    by = VY + 16 + j * 26
    d.shape("rectangle", f"Bay {j+1}", x=VX + 12, y=by, width=VW - 24,
            height=18, radius=3, fill=BAY_GRAD, stroke="#0E0804",
            strokeWidth=1.5)
    d.path(f"M{VX + 18},{by + 9} L{VX + VW - 40},{by + 9}",
           f"Bay slot {j+1}", fill=NONE, stroke="#0C0604",
           strokeWidth=3, cap="round", opacity=80)
# LED column — one green still loyal, one amber tired, one red honest
for j, (ly, lc, op) in enumerate([(VY + 24, GRNL, 85), (VY + 50, GOLD, 70),
                                  (VY + 76, REDL, 90)]):
    d.shape("ellipse", f"LED {j+1}", x=VX + VW - 24, y=ly, width=7,
            height=7, fill=lc, opacity=op, stroke=NONE)
    d.shape("ellipse", f"LED glow {j+1}", x=VX + VW - 27, y=ly - 3,
            width=13, height=13, fill=lc, opacity=op - 55, stroke=NONE)
# thermal gauge, pegged
GX, GY, GR = VX + VW/2, VY + 124, 22
d.shape("ellipse", "Gauge", x=GX - GR, y=GY - GR, width=GR*2, height=GR*2,
        fill="#1E140C", stroke=METAL, strokeWidth=2.5)
# red zone arc on the right of the dial
d.path(f"M{GX + 12},{GY - 15} A{GR - 5},{GR - 5} 0 0 1 {GX + 17},{GY + 8}",
       "Red zone", fill=NONE, stroke=REDL, strokeWidth=3.5, opacity=85)
# needle pegged into the red
d.path(f"M{GX},{GY} L{GX + 13},{GY - 11}", "Needle", fill=NONE,
       stroke=PHOS, strokeWidth=2.5, cap="round")
d.shape("ellipse", "Needle hub", x=GX - 3, y=GY - 3, width=6, height=6,
        fill=METAL, stroke=NONE)
for a in range(4):
    t = math.radians(150 + a * 40)
    x1 = GX + (GR - 9) * math.cos(t); y1 = GY - (GR - 9) * math.sin(t)
    x2 = GX + (GR - 4) * math.cos(t); y2 = GY - (GR - 4) * math.sin(t)
    d.path(f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}", f"Tick {a+1}",
           fill=NONE, stroke=FAINT, strokeWidth=1.5, opacity=70)
d.text("TEMP", "Gauge label", x=GX, y=GY + 17, size=6,
       font="Source Sans 3", color=FAINT, justify="center")
# vent slits below the gauge
for j in range(3):
    vy = VY + 152 + j * 7
    d.path(f"M{VX + 14},{vy} L{VX + VW - 14},{vy}", f"Vent {j+1}",
           fill=NONE, stroke="#0E0804", strokeWidth=3, cap="round",
           opacity=70)
# heat shimmer rising off the top — stays right of the headline rules
for i, hx in enumerate([650, 676, 700]):
    d.path(f"M{hx},292 c-6,-8 6,-14 0,-22 c-6,-8 6,-12 2,-18",
           f"Heat {i+1}", fill=NONE, stroke=ORANGE,
           strokeWidth=2.5, cap="round", opacity=45 - i * 8)

# --- punchline sub-caption -------------------------------------------------------------
r = d.text("THE TERMINAL IS ORANGE.", "Punchline 1", x=500,
           y=PY + PH - 58, size=20, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch1 tracking", ids=[r["id"]], tracking=80)
r = d.text("THE FUTURE IS IRRELEVANT.", "Punchline 2", x=500,
           y=PY + PH - 32, size=20, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch2 tracking", ids=[r["id"]], tracking=80)

# --- flourish on the plate below the poster ----------------------------------------------
d.path("M415,668 L485,668 M515,668 L585,668", "Flourish rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=55)
d.path(rot_rect_path(500, 668, 9, 9, 45), "Flourish diamond", fill=GOLD,
       opacity=60, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("SOL BURNOUT", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("THE TERMINAL IS ORANGE", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-034-sol-burnout-V1R00")
