#!/usr/bin/env python3
"""Vanda Uiguard — mascot portrait V1R00.
A component-card sentinel patrolling a wireframe layout at night. Her cape
is an unused <aside> — dashed, translucent, still in spec. Her lantern is
the holy alignment grid, and its light has found one misbehaving block.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Vanda Uiguard — Mascot Portrait", 1000, 1000)

INK = "#26202E"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0B0D1A"}, {"offset": 1, "color": "#05060E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E4E6E"}, {"offset": 0.7, "color": "#293450"},
    {"offset": 1, "color": "#171E32"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "start": [500, 700], "end": [500, 880], "stops": [
    {"offset": 0, "color": "#222C44"}, {"offset": 1, "color": "#121828"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [484, 430], "end": [484, 540], "stops": [
    {"offset": 0, "color": "#4E6488"}, {"offset": 1, "color": "#2C3850"}]}}
PANEL_GRAD = {"gradient": {"kind": "linear", "start": [500, 560], "end": [500, 696], "stops": [
    {"offset": 0, "color": "#1E2A44"}, {"offset": 1, "color": "#141C30"}]}}
LANT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F8E0A0"}, {"offset": 0.6, "color": "#F0C85E"},
    {"offset": 1, "color": "#B8862E"}]}}
MOON_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2ECD8"}, {"offset": 0.8, "color": "#D8CEAE"},
    {"offset": 1, "color": "#B0A480"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5A6E9A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#8CA0C8", strokeWidth=3, opacity=30)

# --- night sky: moon + stars -------------------------------------------------------
d.shape("ellipse", "Moon halo", x=628, y=96, width=144, height=144,
        fill="#EAE2C8", opacity=12, stroke=NONE)
d.shape("ellipse", "Moon", x=650, y=118, width=100, height=100,
        fill=MOON_GRAD, stroke=NONE)
d.shape("ellipse", "Crater 1", x=678, y=142, width=14, height=14,
        fill="#B8AC8A", opacity=60, stroke=NONE)
d.shape("ellipse", "Crater 2", x=712, y=168, width=10, height=10,
        fill="#B8AC8A", opacity=50, stroke=NONE)
d.shape("ellipse", "Crater 3", x=668, y=176, width=8, height=8,
        fill="#B8AC8A", opacity=45, stroke=NONE)
for i, (x, y, w, op) in enumerate([
        (208, 168, 5, 60), (316, 128, 4, 50), (428, 172, 6, 65),
        (540, 118, 4, 55), (168, 316, 4, 45), (262, 258, 5, 55),
        (380, 224, 3, 50), (608, 268, 4, 45), (806, 300, 5, 55),
        (852, 200, 4, 40), (150, 448, 4, 40), (862, 448, 3, 35)]):
    if on_disc(x, y, 20):
        d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w,
                fill="#C8D4E8", opacity=op, stroke=NONE)

# --- the layout she patrols ---------------------------------------------------------
d.shape("rectangle", "Layout page", x=190, y=560, width=620, height=135,
        radius=10, fill=PANEL_GRAD, stroke="#3A5278", strokeWidth=4)
# header bar
d.shape("rectangle", "Header block", x=208, y=572, width=584, height=30,
        radius=6, fill="#26344E", stroke="#3A5278", strokeWidth=3)
d.shape("ellipse", "Header dot", x=222, y=583, width=10, height=10,
        fill="#6A86B0", stroke=NONE)
d.shape("rectangle", "Header line", x=244, y=583, width=180, height=9,
        radius=4, fill="#4A6288", stroke=NONE)
# hero block
d.shape("rectangle", "Hero block", x=208, y=614, width=258, height=66,
        radius=6, fill="#222E48", stroke="#3A5278", strokeWidth=3)
d.path("M222,634 L452,634 M222,650 L400,650 M222,666 L340,666",
       "Hero rules", fill=NONE, stroke="#3E5578", strokeWidth=2.5,
       opacity=70, cap="round")
# quiet block
d.shape("rectangle", "Quiet block", x=482, y=614, width=148, height=66,
        radius=6, fill="#222E48", stroke="#3A5278", strokeWidth=3)
d.path("M496,634 L616,634 M496,650 L580,650 M496,666 L560,666",
       "Quiet rules", fill=NONE, stroke="#3E5578", strokeWidth=2.5,
       opacity=70, cap="round")

# --- the misbehaving component, caught in lantern light ---------------------------------
d.path("M614,458 L640,698 L800,698 L634,458 Z", "Light cone",
       fill="#F0C85E", opacity=8, stroke=NONE)
d.shape("ellipse", "Light pool", x=640, y=656, width=170, height=36,
        fill="#F0C85E", opacity=14, stroke=NONE)
mb = d.path(rot_rect_path(718, 647, 148, 66, -6), "Naughty block",
            fill="#3A2E3E", stroke="#D88A8A", strokeWidth=3,
            dash=[7, 5])
d.path(rot_rect_path(718, 637, 96, 9, -6), "Naughty rule 1",
       fill="#9A6A72", stroke=NONE, opacity=80)
d.path(rot_rect_path(718, 656, 70, 9, -6), "Naughty rule 2",
       fill="#9A6A72", stroke=NONE, opacity=80)

# --- Vanda ----------------------------------------------------------------------------
d.shape("ellipse", "Vanda shadow", x=400, y=686, width=180, height=18,
        fill="#080A14", opacity=55, stroke=NONE)
# the aside cape: spec-dashed, translucent, billowing on watch
d.path("M436,442 C384,462 340,502 326,556 C352,546 368,570 390,558 "
       "C404,576 426,572 440,556 Z",
       "Aside cape", fill="#5E7EA0", opacity=38, stroke="#8AA8C8",
       strokeWidth=3.5, dash=[9, 6], join="round")
ct = d.text("aside", "Cape label", x=382, y=520, size=15,
            font="Source Sans 3", color="#B8CCE0", justify="center")
if ct and ct.get("id"):
    d.cmd("object.rotate", "cape label tilt", ids=[ct["id"]], angle=-18,
          origin=[382, 520])
# legs, mid-stride
d.shape("rectangle", "Leg L", x=452, y=528, width=24, height=34, radius=7,
        fill="#2A3448", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Leg R", x=498, y=528, width=24, height=34, radius=7,
        fill="#2A3448", stroke=INK, strokeWidth=4)
# body: a component card with a header strip and a will
d.shape("rectangle", "Body", x=428, y=432, width=112, height=104,
        radius=16, fill=BODY_GRAD, stroke=INK, strokeWidth=5)
d.path("M428,462 L540,462", "Body header rule", fill=NONE, stroke=INK,
       strokeWidth=3, opacity=60)
d.shape("ellipse", "Body dot 1", x=442, y=443, width=9, height=9,
        fill="#9AB4D8", stroke=NONE)
d.shape("ellipse", "Body dot 2", x=460, y=443, width=9, height=9,
        fill="#9AB4D8", stroke=NONE)
# face: eyes lowered at the block, stern little brows
d.shape("ellipse", "Eye L", x=452, y=478, width=27, height=31,
        fill="#D8E4F0", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye R", x=493, y=478, width=27, height=31,
        fill="#D8E4F0", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil L", x=463, y=486, width=12, height=16,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=504, y=486, width=12, height=16,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=466, y=487, width=6, height=6,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=507, y=487, width=6, height=6,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M452,472 L478,477", "Brow L", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M494,477 L520,472", "Brow R", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M474,518 L500,518", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
# arm to the lantern
d.path("M538,472 C560,458 580,442 592,430 L606,444 C592,460 570,476 "
       "544,488 Z", "Arm", fill=BODY_GRAD, stroke=INK, strokeWidth=4,
       join="round")
d.shape("ellipse", "Hand", x=590, y=424, width=20, height=18,
        fill="#D8E4F0", stroke=INK, strokeWidth=3)
# the lantern: the holy grid, carried low over the layout
d.shape("ellipse", "Lantern glow", x=566, y=372, width=110, height=110,
        fill="#F0C85E", opacity=18, stroke=NONE)
d.path("M600,430 C602,412 612,402 624,404", "Lantern hook", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.shape("rectangle", "Lantern", x=600, y=404, width=46, height=56,
        radius=9, fill="#3A2E22", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Lantern pane", x=607, y=412, width=32, height=40,
        radius=5, fill=LANT_GRAD, stroke=NONE)
d.path("M618,412 L618,452 M628,412 L628,452 M607,425 L639,425 "
       "M607,438 L639,438", "Lantern grid", fill=NONE, stroke="#7A5A22",
       strokeWidth=2, opacity=80)

# --- the whispered z-index threat -----------------------------------------------------
d.path("M522,510 C560,530 600,548 640,562", "Whisper trail", fill=NONE,
       stroke="#9AB8D8", strokeWidth=2.5, dash=[2, 7], cap="round",
       opacity=70)
d.text("z-index: 9999;", "Whisper", x=640, y=550, size=15,
       font="Source Sans 3", color="#C8D4E8", justify="center")

# --- captions ----------------------------------------------------------------------
d.text("VANDA UIGUARD", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#DCE4F0", justify="center")
r = d.text("GUARDIAN OF THE HOLY GRID", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AA8C8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("069.vanda-uiguard-V1R00")
