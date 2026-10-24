#!/usr/bin/env python3
"""Sol Burnout — mascot portrait V1R00. Legacy Tech Bro:
a sun-headed ex-sysadmin in a faded Java tee, arms crossed, parked at
an orange-on-orange CRT; a framed SPARC chip hangs crooked on the wall
and a stack of CDE install floppies waits on the desk. Burnt-amber
plate on an umber-night backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Sol Burnout — Mascot Plate", 1000, 1000)

INK = "#2E1C14"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#1E0F0A"}, {"offset": 1, "color": "#0A0402"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B8642C"}, {"offset": 0.6, "color": "#7A3E1A"},
    {"offset": 1, "color": "#3A1C0E"}]}}
SUN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFD98A"}, {"offset": 0.62, "color": "#F0A848"},
    {"offset": 1, "color": "#C8701E"}]}}
TEE_GRAD = {"gradient": {"kind": "linear", "start": [0, 460], "end": [0, 720], "stops": [
    {"offset": 0, "color": "#4E6E8C"}, {"offset": 0.55, "color": "#3A5470"},
    {"offset": 1, "color": "#243A50"}]}}
CRT_GRAD = {"gradient": {"kind": "linear", "start": [0, 420], "end": [0, 660], "stops": [
    {"offset": 0, "color": "#B8A88E"}, {"offset": 0.6, "color": "#8E7E66"},
    {"offset": 1, "color": "#5E5240"}]}}
SCREEN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9A3A10"}, {"offset": 0.7, "color": "#6E2408"},
    {"offset": 1, "color": "#3C1204"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "start": [0, 660], "end": [0, 730], "stops": [
    {"offset": 0, "color": "#8A5630"}, {"offset": 1, "color": "#4E2C16"}]}}
AMBER = "#FFB35C"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#B8642C", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1E0E06", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8B878", strokeWidth=3, opacity=28)
# terminal glow pooling on the left of the scene
d.shape("ellipse", "Screen glow", x=210, y=380, width=320, height=280,
        fill="#FF8A2C", opacity=13, stroke=NONE)
d.shape("ellipse", "Patina 1", x=580, y=150, width=240, height=140,
        fill="#8A4A20", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=170, y=620, width=250, height=140,
        fill="#3A1C0E", opacity=24, stroke=NONE)
for i, (x, y, w) in enumerate([(222,342,5),(788,335,6),(176,545,5),(844,550,5),
                               (266,755,5),(726,762,6),(156,450,5),(852,645,5),
                               (435,128,5),(600,124,6),(340,148,4),(696,196,5),
                               (248,662,4),(672,715,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0C890", opacity=28, stroke=NONE)
# ghost scanline arcs on the dark backdrop
d.path("M938,165 A108,108 0 0 0 838,62", "Ghost arc TR",
       fill=NONE, stroke="#8A4A20", strokeWidth=14, opacity=10, cap="round")
d.path("M72,775 A120,120 0 0 0 188,878", "Ghost arc BL",
       fill=NONE, stroke="#8A4A20", strokeWidth=10, opacity=8, cap="round")

# --- the framed SPARC chip, hung crooked ---------------------------------------------
FR_CX, FR_CY, FR_A = 296, 242, -6
d.path(rot_rect_path(FR_CX, FR_CY, 168, 150, FR_A), "SPARC frame",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#7A4E28"}, {"offset": 1, "color": "#4A2C14"}]}},
       stroke=INK, strokeWidth=4)
d.path(rot_rect_path(FR_CX, FR_CY, 138, 120, FR_A), "SPARC mat",
       fill="#E4D6B8", stroke=INK, strokeWidth=2.5)
# the chip: dark slab, gold cap, pin stubs all around
d.path(rot_rect_path(FR_CX, FR_CY + 6, 74, 62, FR_A), "SPARC die",
       fill="#1E1A14", stroke=INK, strokeWidth=2.5)
d.path(rot_rect_path(FR_CX, FR_CY + 6, 40, 32, FR_A), "SPARC cap",
       fill="#3A3226", stroke="#7A5E28", strokeWidth=2)
for j in range(5):
    ox = -34 + j * 17
    d.path(rot_rect_path(FR_CX + ox, FR_CY - 32, 6, 10, FR_A),
           f"Pin T{j+1}", fill="#C8A04E", stroke=NONE)
    d.path(rot_rect_path(FR_CX + ox, FR_CY + 44, 6, 10, FR_A),
           f"Pin B{j+1}", fill="#C8A04E", stroke=NONE)
# frame glint
d.path(rot_rect_path(FR_CX - 30, FR_CY - 44, 60, 8, FR_A), "Frame glint",
       fill="#FFE9B0", opacity=30, stroke=NONE)

# --- the Sun-diamond plaque opposite ---------------------------------------------------
d.path(rot_rect_path(706, 224, 96, 96, 45), "Plaque diamond",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#7A4E28"}, {"offset": 1, "color": "#4A2C14"}]}},
       stroke=INK, strokeWidth=4)
d.path(rot_rect_path(706, 224, 66, 66, 45), "Plaque inset",
       fill="#2E1A0E", stroke="#C8A04E", strokeWidth=2)
d.path(rot_rect_path(706, 224, 30, 30, 45), "Plaque mark",
       fill=NONE, stroke="#E8A04C", strokeWidth=5)

# --- Sol: sun-headed burnout --------------------------------------------------------------
# desk-side shadow
d.shape("ellipse", "Body shadow", x=360, y=730, width=300, height=30,
        fill="#1E0E06", opacity=35, stroke=NONE)
# torso: faded Java tee
d.path("M500,452 C566,452 608,500 614,584 C618,652 610,700 594,730 "
       "C552,750 448,750 406,730 C390,700 382,652 386,584 "
       "C392,500 434,452 500,452 Z",
       "Java tee", fill=TEE_GRAD, stroke=INK, strokeWidth=5)
# collar
d.path("M468,456 C480,478 520,478 532,456 C522,470 478,470 468,456 Z",
       "Collar", fill="#2A3E52", stroke=INK, strokeWidth=3)
# the coffee-cup emblem — Java pride, faded
d.path("M472,548 L528,548 L522,606 C508,614 492,614 478,606 Z",
       "Cup", fill="#D8CBA8", opacity=90, stroke=INK, strokeWidth=3.5)
d.path("M528,556 C548,556 552,580 534,588 L526,584 C538,576 536,564 526,564 Z",
       "Cup handle", fill="#D8CBA8", opacity=90, stroke=INK, strokeWidth=3)
for j, sx in enumerate((486, 500, 514)):
    d.path(f"M{sx},536 C{sx - 5},528 {sx + 5},522 {sx},514",
           f"Steam {j+1}", fill=NONE, stroke="#D8CBA8", strokeWidth=3.5,
           opacity=60, cap="round")
# crossed arms — the bitterness posture
d.path("M396,600 C440,596 500,602 560,624 C578,632 586,650 578,664 "
       "C540,646 470,632 404,634 C394,622 392,610 396,600 Z",
       "Arm under", fill="#3A5470", stroke=INK, strokeWidth=4.5)
d.path("M604,596 C566,600 508,610 452,634 C434,642 428,660 438,672 "
       "C476,650 546,634 608,630 C616,616 614,604 604,596 Z",
       "Arm over", fill="#42607C", stroke=INK, strokeWidth=4.5)
d.shape("ellipse", "Hand R", x=566, y=622, width=34, height=28,
        fill=SUN_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Hand L", x=404, y=632, width=34, height=28,
        fill=SUN_GRAD, stroke=INK, strokeWidth=3.5)

# sun head: disc + corona rays
HX, HY, HR = 500, 330, 86
for j in range(12):
    a = math.radians(j * 30 - 90)
    a2 = math.radians(j * 30 - 90 + 11)
    a3 = math.radians(j * 30 - 90 - 11)
    bx, by = HX + math.cos(a) * (HR - 6), HY + math.sin(a) * (HR - 6)
    tx, ty = HX + math.cos(a) * (HR + 42), HY + math.sin(a) * (HR + 42)
    b2x, b2y = HX + math.cos(a2) * (HR - 6), HY + math.sin(a2) * (HR - 6)
    b3x, b3y = HX + math.cos(a3) * (HR - 6), HY + math.sin(a3) * (HR - 6)
    d.path(f"M{b2x:.0f},{b2y:.0f} L{tx:.0f},{ty:.0f} L{b3x:.0f},{b3y:.0f} Z",
           f"Ray {j+1}", fill=SUN_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Sun face", x=HX - HR, y=HY - HR, width=HR * 2, height=HR * 2,
        fill=SUN_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Face light", x=HX - 56, y=HY - 66, width=90, height=54,
        fill="#FFF0C0", opacity=30, stroke=NONE)
# weary eyes: droop lids, bags underneath
d.shape("ellipse", "Eye L", x=HX - 44, y=HY - 18, width=22, height=26,
        fill="#2A1408", stroke=NONE)
d.shape("ellipse", "Eye R", x=HX + 22, y=HY - 18, width=22, height=26,
        fill="#2A1408", stroke=NONE)
d.shape("ellipse", "Glint L", x=HX - 38, y=HY - 12, width=6, height=6,
        fill="#FFFFFF", opacity=80, stroke=NONE)
d.shape("ellipse", "Glint R", x=HX + 28, y=HY - 12, width=6, height=6,
        fill="#FFFFFF", opacity=80, stroke=NONE)
d.path(f"M{HX - 48},{HY - 22} L{HX - 18},{HY - 26}", "Lid L",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path(f"M{HX + 18},{HY - 26} L{HX + 48},{HY - 22}", "Lid R",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path(f"M{HX - 42},{HY + 14} C{HX - 34},{HY + 20} {HX - 26},{HY + 20} {HX - 20},{HY + 16}",
       "Bag L", fill=NONE, stroke="#A85E20", strokeWidth=3, opacity=70, cap="round")
d.path(f"M{HX + 20},{HY + 16} C{HX + 26},{HY + 20} {HX + 34},{HY + 20} {HX + 42},{HY + 14}",
       "Bag R", fill=NONE, stroke="#A85E20", strokeWidth=3, opacity=70, cap="round")
# the flat mouth of a man who saw the acquisition
d.path(f"M{HX - 26},{HY + 42} L{HX + 26},{HY + 40}", "Flat mouth",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# one sweat bead — 13:37 truss o'clock approaches
d.path(f"M{HX + 66},{HY - 52} C{HX + 74},{HY - 40} {HX + 72},{HY - 30} {HX + 66},{HY - 26} "
       f"C{HX + 60},{HY - 30} {HX + 58},{HY - 40} {HX + 66},{HY - 52} Z",
       "Sweat", fill="#BEE0E8", opacity=85, stroke=INK, strokeWidth=2)

# --- the desk ---------------------------------------------------------------------------
d.shape("rectangle", "Desk", x=196, y=664, width=608, height=46, radius=8,
        fill=DESK_GRAD, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Desk edge light", x=206, y=668, width=588, height=8,
        radius=4, fill="#C88040", opacity=50, stroke=NONE)
d.shape("rectangle", "Desk shadow", x=210, y=716, width=580, height=20,
        radius=8, fill="#140A04", opacity=40, stroke=NONE)

# --- orange-on-orange CRT ------------------------------------------------------------------
CRT_A = -3
d.path(rot_rect_path(330, 530, 210, 170, CRT_A), "CRT body",
       fill=CRT_GRAD, stroke=INK, strokeWidth=5)
d.path(rot_rect_path(330, 518, 168, 120, CRT_A), "CRT screen",
       fill=SCREEN_GRAD, stroke=INK, strokeWidth=4)
# glowing terminal lines, brighter amber on amber — kept inside the bezel
for j, lw in enumerate([96, 128, 66, 108]):
    d.path(rot_rect_path(258 + lw / 2, 480 + j * 20, lw, 7, CRT_A),
           f"Term line {j+1}", fill=AMBER, opacity=85, stroke=NONE)
# blinking cursor block
d.path(rot_rect_path(264, 558, 14, 10, CRT_A), "Cursor",
       fill=AMBER, opacity=95, stroke=NONE)
# scanlines + glare
for j in range(4):
    d.path(rot_rect_path(330, 474 + j * 30, 160, 2, CRT_A), f"Scan {j+1}",
           fill="#2A0E02", opacity=35, stroke=NONE)
d.path(rot_rect_path(302, 490, 40, 84, CRT_A - 20), "Screen glare",
       fill="#FFD9A0", opacity=12, stroke=NONE)
# bezel LED + brand slot
d.shape("ellipse", "CRT LED", x=402, y=600, width=9, height=9,
        fill="#7AE86E", opacity=90, stroke=NONE)
d.path(rot_rect_path(310, 604, 90, 8, CRT_A), "CRT slot",
       fill="#4A3E2E", stroke=NONE)
# stand
d.path(rot_rect_path(330, 636, 96, 22, CRT_A), "CRT stand",
       fill="#6E5E48", stroke=INK, strokeWidth=4)
# glow the CRT throws onto the desk
d.shape("ellipse", "CRT desk glow", x=230, y=640, width=210, height=30,
        fill="#FF8A2C", opacity=22, stroke=NONE)

# --- CDE install floppies ------------------------------------------------------------------
def floppy(cx, cy, deg, label, tag):
    d.path(rot_rect_path(cx, cy, 104, 108, deg), f"{label} shell",
           fill={"gradient": {"kind": "linear", "stops": [
               {"offset": 0, "color": "#3A4654"}, {"offset": 1, "color": "#222A34"}]}},
           stroke=INK, strokeWidth=3.5)
    d.path(rot_rect_path(cx + 8, cy - 34, 56, 34, deg), f"{label} shutter",
           fill={"gradient": {"kind": "linear", "stops": [
               {"offset": 0, "color": "#B8BEC6"}, {"offset": 1, "color": "#6E7680"}]}},
           stroke=INK, strokeWidth=2.5)
    d.path(rot_rect_path(cx, cy + 26, 76, 42, deg), f"{label} label",
           fill="#E8DEC2", stroke=INK, strokeWidth=2)
    for k, lw in enumerate((52, 40, 58)):
        d.path(rot_rect_path(cx - 28 + lw / 2 - 10, cy + 16 + k * 11, lw, 4, deg),
               f"{label} line {k+1}", fill="#8A7654", opacity=80, stroke=NONE)
    if tag:
        d.text(tag, f"{label} tag", x=int(cx - 30), y=int(cy + 12), size=13,
               font="Virelai Sans", color="#4A3418", justify="left")

floppy(664, 628, 8, "Floppy 1", None)
floppy(688, 616, -4, "Floppy 2", None)
floppy(650, 600, 14, "Floppy 3", None)
floppy(676, 588, 2, "Floppy 4", "CDE")

# coffee mug, forever refilled
d.path("M568,612 L614,612 L610,664 C596,670 586,670 572,664 Z",
       "Mug", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#8A3E2A"}, {"offset": 1, "color": "#542014"}]}},
       stroke=INK, strokeWidth=3.5)
d.path("M614,620 C634,620 638,644 620,652 L612,648 C624,640 622,628 612,628 Z",
       "Mug handle", fill="#8A3E2A", stroke=INK, strokeWidth=3)
for j, sx in enumerate((580, 596)):
    d.path(f"M{sx},604 C{sx - 5},594 {sx + 5},588 {sx},578",
           f"Mug steam {j+1}", fill=NONE, stroke="#E8D0B0", strokeWidth=3.5,
           opacity=55, cap="round")

# --- name + role ----------------------------------------------------------------------------
d.text("SOL BURNOUT", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#F2D9B0", justify="center")
r = d.text("LEGACY TECH BRO", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#D8A468", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("034.sol-burnout-V1R00")
