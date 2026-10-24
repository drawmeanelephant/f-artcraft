#!/usr/bin/env python3
"""Vexsys Antagon — mascot portrait V1R00.
A deploy-card creature whose body is perfectly legitimate JSON, standing
beside a rack of glowing green deployment lights — every one of them a lie.
Under its feet the parse floor splits into a dark XML-angled crack.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Vexsys Antagon — Mascot Portrait", 1000, 1000)

INK = "#2E2226"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0B100E"}, {"offset": 1, "color": "#050808"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#46605A"}, {"offset": 0.7, "color": "#2A3E40"},
    {"offset": 1, "color": "#16222A"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "start": [500, 700], "end": [500, 880], "stops": [
    {"offset": 0, "color": "#223238"}, {"offset": 1, "color": "#101A20"}]}}
CARD_GRAD = {"gradient": {"kind": "linear", "start": [420, 290], "end": [420, 630], "stops": [
    {"offset": 0, "color": "#20303A"}, {"offset": 1, "color": "#0C1418"}]}}
RACK_GRAD = {"gradient": {"kind": "linear", "start": [705, 300], "end": [705, 630], "stops": [
    {"offset": 0, "color": "#1E2A30"}, {"offset": 1, "color": "#0D151A"}]}}
LED_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B8F8CC"}, {"offset": 0.55, "color": "#6FE89A"},
    {"offset": 1, "color": "#2E9858"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#6FE89A", opacity=6, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E7A6E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#8AC0AE", strokeWidth=3, opacity=30)
for i, (x, y, w) in enumerate([(196,236,8),(796,230,7),(158,514,9),(836,534,8),
                               (262,762,7),(742,748,9),(136,388,6),(858,392,7),
                               (388,112,7),(616,114,8),(346,816,6),(660,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#1E3234", opacity=55, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A1210",
       strokeWidth=4, opacity=70)

# --- the XML void under the parse floor -------------------------------------------
d.path("M330,722 L418,742 L492,720 L582,750 L668,728 "
       "L612,754 L548,748 L502,782 L442,754 L368,740 Z",
       "XML crack", fill="#05080C", stroke="#4E3E6A", strokeWidth=3,
       opacity=95, join="round")
d.text("</", "Crack glyph", x=478, y=750, size=15, font="Source Sans 3",
       color="#5E4E7E", justify="center")

# --- deployment light rack ----------------------------------------------------------
# green ambient spill reaching the card
d.shape("ellipse", "LED spill", x=580, y=380, width=240, height=220,
        fill="#6FE89A", opacity=8, stroke=NONE)
d.shape("rectangle", "Rack", x=610, y=296, width=190, height=344,
        radius=16, fill=RACK_GRAD, stroke=INK, strokeWidth=6)
d.text("DEPLOY", "Rack label", x=705, y=332, size=13, font="Source Sans 3",
       color="#7E98A0", justify="center")
for i, lab in enumerate(["API", "DB", "CDN", "QUEUE", "AUTH", "EDGE"]):
    ly = 368 + i * 44
    d.shape("ellipse", f"{lab} halo", x=636, y=ly-8, width=36, height=36,
            fill="#6FE89A", opacity=22, stroke=NONE)
    d.shape("ellipse", f"{lab} LED", x=643, y=ly, width=22, height=22,
            fill=LED_GRAD, stroke="#1E4A32", strokeWidth=2)
    d.text(lab, f"{lab} tag", x=678, y=ly+16, size=12, font="Source Sans 3",
           color="#7E98A0", justify="left")
# rack feet + shadow
d.shape("ellipse", "Rack shadow", x=618, y=668, width=180, height=18,
        fill="#08100C", opacity=55, stroke=NONE)

# --- the creature: a JSON card standing smug -----------------------------------------
d.shape("ellipse", "Card shadow", x=256, y=664, width=330, height=24,
        fill="#08100C", opacity=55, stroke=NONE)
# feet
d.shape("rectangle", "Foot L", x=330, y=618, width=44, height=48, radius=12,
        fill="#18242C", stroke=INK, strokeWidth=5)
d.shape("rectangle", "Foot R", x=452, y=618, width=44, height=48, radius=12,
        fill="#18242C", stroke=INK, strokeWidth=5)
# body card
d.shape("rectangle", "Card", x=240, y=290, width=330, height=340,
        radius=18, fill=CARD_GRAD, stroke=INK, strokeWidth=7)
# title bar with three honest little traffic dots
d.path("M240,330 L570,330", "Title rule", fill=NONE, stroke=INK,
       strokeWidth=4, opacity=80)
for i, col in enumerate(["#E05E52", "#E8B84A", "#6FC86E"]):
    d.shape("ellipse", f"Dot {i+1}", x=258+i*24, y=302, width=14, height=14,
            fill=col, stroke=INK, strokeWidth=2)
# green rim light on the card's right edge — borrowed legitimacy
d.path("M560,350 C566,430 566,540 558,600", "Rim light", fill=NONE,
       stroke="#6FE89A", strokeWidth=5, opacity=35, cap="round")

# face: calm, sideways-eyed toward the rack
d.shape("ellipse", "Eye L", x=332, y=350, width=36, height=40,
        fill="#C8E8D8", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye R", x=450, y=350, width=36, height=40,
        fill="#C8E8D8", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil L", x=349, y=360, width=14, height=20,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=467, y=360, width=14, height=20,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=353, y=362, width=7, height=7,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=471, y=362, width=7, height=7,
        fill="#FFFFFF", opacity=85, stroke=NONE)
# the smirk — asymmetric, entirely too pleased
d.path("M372,428 C404,442 444,440 474,418", "Smirk", fill=NONE,
       stroke="#8FC8B8", strokeWidth=6, cap="round")

# the body copy: legitimate JSON, every word of it
JSON_L = [
    (480, "{",                 "#6E8890"),
    (508, '"status": "ok",',   "#9AD0C4"),
    (534, '"lights": "green",', "#9AD0C4"),
    (560, '"trust": "me"',     "#8FE89A"),   # the tell — brighter than it should be
    (586, "}",                 "#6E8890"),
]
for i, (ty, txt, col) in enumerate(JSON_L):
    d.text(txt, f"JSON line {i+1}", x=272, y=ty, size=17,
           font="Source Sans 3", color=col, justify="left")

# --- captions ----------------------------------------------------------------------
d.text("VEXSYS ANTAGON", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#DCE8E0", justify="center")
r = d.text("FALSE SUCCESS SIGNALER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AB8AC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("067.vexsys-antagon-V1R00")
