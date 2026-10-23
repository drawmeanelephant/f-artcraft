#!/usr/bin/env python3
"""LLG-0088-B Boily McPlaterton — Thermal Conscience — V1R00. Boily invoking
Emergency Cooldown Protocol Form 88-B on a livestream overlay: temperature
climbing, fan RPM screaming, casing cracked and venting steam, the ceremonial
chant 'We cool our sins, not just our chips' on a banner. Thermal palette.
1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LLG-0088 Boily Thermal Conscience", 1000, 1000)

INK = "#2A140E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A1210"}, {"offset": 1, "color": "#0E0605"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A3222"}, {"offset": 0.7, "color": "#4A1E14"},
    {"offset": 1, "color": "#260F0A"}]}}
CASE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8985E"}, {"offset": 0.6, "color": "#C46838"},
    {"offset": 1, "color": "#8A3A22"}]}}
HOT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFD98A"}, {"offset": 1, "color": "#E86A3A"}]}}
CORE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFE8B0"}, {"offset": 0.5, "color": "#F09A4E"},
    {"offset": 1, "color": "#C43A1E"}]}}

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#40160E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8A87A", strokeWidth=3, opacity=45)
# heat bloom behind the subject
d.shape("ellipse", "Heat bloom", x=280, y=300, width=440, height=440,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#E86A3A", "opacity": 0.5},
            {"offset": 1, "color": "#E86A3A", "opacity": 0}]}},
        stroke=NONE)

# --- ceremonial chant banner ------------------------------------------------------
# ribbon across the upper plate
d.path("M170,196 L830,196 L806,236 L830,276 L170,276 L194,236 Z",
       "Chant ribbon", fill="#5A1E12", stroke=INK, strokeWidth=4)
d.path("M170,196 L830,196 L806,236 L830,276 L170,276 L194,236 Z",
       "Ribbon sheen", fill=NONE, stroke="#E8A87A", strokeWidth=2, opacity=35)
# ribbon tails
d.path("M170,196 L132,208 L150,236 L132,264 L170,276 Z", "Ribbon tail L",
       fill="#40160E", stroke=INK, strokeWidth=3)
d.path("M830,196 L868,208 L850,236 L868,264 L830,276 Z", "Ribbon tail R",
       fill="#40160E", stroke=INK, strokeWidth=3)
d.text("WE COOL OUR SINS, NOT JUST OUR CHIPS", "Chant", x=500, y=246,
       size=21, font="Virelai Sans", color="#F2D4B0", justify="center")

# --- livestream overlay ------------------------------------------------------------
# corner brackets framing the subject
for i, (cx, cy, sx, sy) in enumerate([(240, 330, 1, 1), (760, 330, -1, 1),
                                      (240, 700, 1, -1), (760, 700, -1, -1)]):
    d.path(f"M{cx},{cy + 36*sy} L{cx},{cy} L{cx + 36*sx},{cy}",
           f"Stream corner {i+1}", fill=NONE, stroke="#F2D4B0",
           strokeWidth=5, opacity=70, cap="round")
# LIVE pill, top-left inside the frame
d.shape("ellipse", "Live dot", x=256, y=346, width=14, height=14,
        fill="#E83A2E", stroke=NONE)
d.text("LIVE", "Live tag", x=278, y=360, size=16, font="Virelai Sans",
       color="#F2D4B0")
# temperature readout, top-right: climbing
d.shape("rectangle", "Temp panel", x=640, y=344, width=120, height=74,
        radius=8, fill="#40160E", opacity=85, stroke="#E8A87A",
        strokeWidth=2)
d.text("CPU", "Temp label", x=660, y=368, size=14, font="Virelai Sans",
       color="#E8A87A")
# climbing bars at the panel's left, readout clear of them
for i, h in enumerate([10, 18, 28]):
    d.shape("rectangle", f"Temp bar {i+1}", x=654 + i*16, y=404 - h,
            width=10, height=h, fill="#E86A3A", opacity=40 + i*20,
            stroke=NONE)
d.text("97°C", "Temp value", x=700, y=404, size=24, font="Virelai Sans",
       color="#FF9A5E")
# RPM scream, bottom-right
d.shape("rectangle", "RPM panel", x=600, y=648, width=160, height=52,
        radius=8, fill="#40160E", opacity=85, stroke="#E8A87A",
        strokeWidth=2)
d.text("FAN 6800 RPM !!", "RPM scream", x=680, y=681, size=16,
       font="Virelai Sans", color="#FF9A5E", justify="center")
# Form 88-B filed pill, bottom-left
d.shape("rectangle", "Form pill", x=228, y=648, width=162, height=52,
        radius=8, fill="#40160E", opacity=85, stroke="#E8A87A",
        strokeWidth=2)
d.text("FORM 88-B FILED", "Form 88-B", x=309, y=681, size=15,
       font="Virelai Sans", color="#F2D4B0", justify="center")

# --- Boily: cracked casing, venting steam, screaming fan ----------------------------
# heat haze around the casing
d.shape("ellipse", "Haze L", x=330, y=430, width=80, height=240,
        fill="#E86A3A", opacity=12, stroke=NONE)
d.shape("ellipse", "Haze R", x=590, y=430, width=80, height=240,
        fill="#E86A3A", opacity=12, stroke=NONE)
# the tower
d.shape("rectangle", "Boily casing", x=400, y=430, width=200, height=330,
        radius=18, fill=CASE_GRAD, stroke=INK, strokeWidth=6)
# molten glow through the main crack
d.path("M486,440 L506,492 L488,540 L514,592 L496,646 L516,700",
       "Crack", fill=NONE, stroke="#2A0E06", strokeWidth=10, cap="round")
d.path("M488,446 L504,492 L490,538 L510,590 L498,642 L512,694",
       "Crack glow", fill=NONE, stroke="#FFD98A", strokeWidth=3,
       opacity=85, cap="round")
# worried face
d.shape("ellipse", "Boily eye L", x=446, y=492, width=16, height=22,
        fill="#2A0E06", stroke=NONE)
d.shape("ellipse", "Boily eye R", x=538, y=492, width=16, height=22,
        fill="#2A0E06", stroke=NONE)
d.shape("ellipse", "Boily glint L", x=450, y=497, width=4, height=4,
        fill="#FFFFFF", opacity=80, stroke=NONE)
d.shape("ellipse", "Boily glint R", x=542, y=497, width=4, height=4,
        fill="#FFFFFF", opacity=80, stroke=NONE)
# raised panic brows
d.path("M442,478 Q454,470 466,476", "Brow L", fill=NONE, stroke="#2A0E06",
       strokeWidth=4, cap="round")
d.path("M534,476 Q546,470 558,478", "Brow R", fill=NONE, stroke="#2A0E06",
       strokeWidth=4, cap="round")
# open grimace — the conscience is loud
d.shape("ellipse", "Boily mouth", x=470, y=532, width=60, height=36,
        fill="#2A0E06", stroke=NONE)
d.shape("ellipse", "Mouth heat", x=484, y=546, width=32, height=16,
        fill="#E86A3A", opacity=60, stroke=NONE)
# screaming fan in the lower casing
d.shape("ellipse", "Fan ring", x=428, y=620, width=110, height=110,
        fill="#3A1A10", stroke=INK, strokeWidth=4)
for i, ang in enumerate([0, 60, 120, 180, 240, 300]):
    a = math.radians(ang + 20)
    x1 = 483 + math.cos(a) * 38
    y1 = 675 + math.sin(a) * 38
    x2 = 483 + math.cos(math.radians(ang + 52)) * 20
    y2 = 675 + math.sin(math.radians(ang + 52)) * 20
    d.path(f"M483,675 L{x2:.0f},{y2:.0f} L{x1:.0f},{y1:.0f} Z",
           f"Fan blade {i+1}", fill="#C9B68E", opacity=85, stroke=NONE)
d.shape("ellipse", "Fan hub", x=471, y=663, width=24, height=24,
        fill=HOT_GRAD, stroke=INK, strokeWidth=2)
# spin arcs — the fan screams
d.path("M420,640 A70,70 0 0 1 530,632", "Spin arc 1", fill=NONE,
       stroke="#F2D4B0", strokeWidth=3, opacity=50, cap="round")
d.path("M424,724 A70,70 0 0 0 534,716", "Spin arc 2", fill=NONE,
       stroke="#F2D4B0", strokeWidth=3, opacity=50, cap="round")
# core glow venting through the top seam
d.shape("ellipse", "Core vent", x=430, y=412, width=140, height=30,
        fill=CORE_GRAD, opacity=80, stroke=NONE)
# steam column rising off the top
for i, (sx, sy, sw, sh, op) in enumerate([(460, 370, 60, 36, 45),
                                          (430, 330, 78, 46, 36),
                                          (475, 288, 92, 54, 28),
                                          (440, 244, 110, 62, 20),
                                          (495, 208, 80, 46, 14)]):
    d.shape("ellipse", f"Steam {i+1}", x=sx, y=sy, width=sw, height=sh,
            fill="#F2D4B0", opacity=op, stroke=NONE)
# sparks off the casing edge
for i, (sx, sy, sr) in enumerate([(392, 480, 6), (610, 520, 5),
                                   (398, 640, 5), (606, 600, 6)]):
    d.path(f"M{sx},{sy-sr} L{sx+sr*0.3},{sy-sr*0.3} L{sx+sr},{sy} "
           f"L{sx+sr*0.3},{sy+sr*0.3} L{sx},{sy+sr} L{sx-sr*0.3},{sy+sr*0.3} "
           f"L{sx-sr},{sy} L{sx-sr*0.3},{sy-sr*0.3} Z",
           f"Spark {i+1}", fill="#FFD98A", opacity=85, stroke=NONE)

# --- name + role -----------------------------------------------------------------------
d.text("BOILY MCPLATERTON", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#F2D4B0", justify="center")
d.text("E M E R G E N C Y   C O O L D O W N   P R O T O C O L   8 8 - B",
       "Role", x=500, y=968, size=17, font="Virelai Sans",
       color="#C9906A", justify="center")

d.finish("llg-0088-boily-thermal-conscience-V1R00")
