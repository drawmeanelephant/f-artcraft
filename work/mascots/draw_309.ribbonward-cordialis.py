#!/usr/bin/env python3
"""Ribbonward Cordialis — mascot portrait V1R00.
Custodian mascot holding a frayed gold satin ribbon between both hands,
scissors and three dedication albums on the shelf behind. 1000x1000.
Gradients + translucency, never flat."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Ribbonward Cordialis — Mascot Portrait", 1000, 1000)

INK = "#2E2030"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1C1420"}, {"offset": 1, "color": "#0B080E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DACBDD"}, {"offset": 0.7, "color": "#A48EAC"},
    {"offset": 1, "color": "#6B5978"}]}}
UNIFORM_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#456055"}, {"offset": 0.7, "color": "#2E4438"},
    {"offset": 1, "color": "#1C2C24"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0D2B4"}, {"offset": 1, "color": "#D2A57F"}]}}
GOLD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4D060"}, {"offset": 0.55, "color": "#D9A832"},
    {"offset": 1, "color": "#A87A1E"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4EBD6"}, {"offset": 1, "color": "#D9CCA9"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5638"}, {"offset": 1, "color": "#503521"}]}}
STEEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#CCD1D9"}, {"offset": 1, "color": "#848C99"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A6488", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EBDFF0", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(210,224,7),(786,216,6),(240,714,7),(750,704,7),(170,450,6),
                               (834,454,6),(350,150,6),(646,144,7),(294,796,6),(706,800,6)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6A5878", opacity=38, stroke=NONE)

# --- the shelf behind, with three dedication albums ------------------------------
d.shape("rectangle", "Shelf", x=236, y=588, width=528, height=18,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=5, radius=4)
d.shape("ellipse", "Shelf shadow", x=250, y=606, width=500, height=16,
        fill="#3A2C44", opacity=35, stroke=NONE)

def album(x, y, w, h, tilt, cover, label):
    """Standing dedication album: spine to the viewer, gilt page block on top."""
    t = math.radians(tilt); c, s = math.cos(t), math.sin(t)
    def rot(px, py):
        return (x + px*c - py*s, y + px*s + py*c)
    def poly(pts):
        p = [rot(px, py) for px, py in pts]
        return "M" + " L".join(f"{a:.0f},{b:.0f}" for a, b in p) + " Z"
    d.path(poly([(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]), label,
           fill=cover, stroke=INK, strokeWidth=5, join="round")
    # gilt page block along the top edge
    d.path(poly([(-w/2+8,-h/2+6),(w/2-8,-h/2+6),(w/2-8,-h/2+22),(-w/2+8,-h/2+22)]),
           f"{label} pages", fill=PAPER_GRAD, stroke=INK, strokeWidth=3)
    for j in range(3):
        a = rot(-w/2+12, -h/2+10+j*4); b = rot(w/2-12, -h/2+10+j*4)
        d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}",
               f"{label} page line {j+1}", fill=NONE, stroke="#B09A6A",
               strokeWidth=1.8, opacity=70)
    # spine label plate + gilt rules
    d.path(poly([(-w/2+12,-h/4),(w/2-12,-h/4),(w/2-12,h/4-14),(-w/2+12,h/4-14)]),
           f"{label} label", fill="#E8DDBE", stroke=INK, strokeWidth=3)
    for j in range(2):
        a = rot(-w/2+18, -h/4+10+j*12); b = rot(w/2-18, -h/4+10+j*12)
        d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}",
               f"{label} title {j+1}", fill=NONE, stroke="#8A7454",
               strokeWidth=3, cap="round", opacity=80)
    # gilt corner flourish
    a = rot(-w/2+10, h/2-14); b = rot(w/2-10, h/2-14)
    d.path(f"M{a[0]:.0f},{a[1]:.0f} L{b[0]:.0f},{b[1]:.0f}",
           f"{label} gilt rule", fill=NONE, stroke=GOLD_GRAD,
           strokeWidth=3.5, cap="round")

album(300, 500, 96, 176, -5, {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A3244"}, {"offset": 1, "color": "#4E1F2C"}]}}, "Album L")
album(420, 492, 104, 190, 2, {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A4A6A"}, {"offset": 1, "color": "#232E48"}]}}, "Album C")
album(646, 500, 96, 176, 6, {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3C5648"}, {"offset": 1, "color": "#24382E"}]}}, "Album R")

# --- scissors resting on the shelf at right ---------------------------------------
# finger rings
d.shape("ellipse", "Scissor ring T", x=676, y=548, width=26, height=24,
        fill=NONE, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Scissor ring B", x=700, y=556, width=26, height=24,
        fill=NONE, stroke=INK, strokeWidth=6)
# blades, half-open, points toward the ribbon
d.path("M694,556 L752,500 L758,508 L702,564 Z", "Blade T",
       fill=STEEL_GRAD, stroke=INK, strokeWidth=3.5, join="round")
d.path("M706,570 L760,544 L762,554 L710,578 Z", "Blade B",
       fill=STEEL_GRAD, stroke=INK, strokeWidth=3.5, join="round")
d.shape("ellipse", "Scissor pivot", x=700, y=559, width=9, height=9,
        fill="#5A4A34", stroke=INK, strokeWidth=2.5)
# blade glint
d.path("M716,540 L746,510", "Blade glint", fill=NONE, stroke="#FFFFFF",
       strokeWidth=2.5, cap="round", opacity=70)

# --- the custodian -----------------------------------------------------------------
d.shape("ellipse", "Figure shadow", x=300, y=762, width=340, height=30,
        fill="#3A2C44", opacity=40, stroke=NONE)
# uniform body: straight-sided custodian jacket
d.path("M368,762 C366,680 372,600 394,540 C414,486 448,462 474,466 "
       "C524,474 556,540 560,612 C564,676 562,722 560,762 Z",
       "Uniform", fill=UNIFORM_GRAD, stroke=INK, strokeWidth=7, join="round")
# jacket center seam + gold buttons
d.path("M470,500 L470,758", "Jacket seam", fill=NONE, stroke="#16211B",
       strokeWidth=4, opacity=60)
for j, yy in enumerate([540, 592, 644]):
    d.shape("ellipse", f"Button {j+1}", x=482, y=yy, width=14, height=14,
            fill=GOLD_GRAD, stroke=INK, strokeWidth=3)
# collar notch
d.path("M444,486 L470,514 L496,486", "Collar", fill="#223028",
       stroke=INK, strokeWidth=4, join="round")
# sleeve cuffs reaching to the hands on the ribbon
d.path("M392,556 C376,568 366,584 362,600 L392,606 C396,590 402,576 412,566 Z",
       "Sleeve L", fill=UNIFORM_GRAD, stroke=INK, strokeWidth=4)
d.path("M552,556 C568,568 578,584 582,600 L552,606 C548,590 542,576 532,566 Z",
       "Sleeve R", fill=UNIFORM_GRAD, stroke=INK, strokeWidth=4)
# custodian's peaked cap
d.path("M416,306 C420,272 448,254 478,256 C510,258 532,280 534,310 "
       "C508,296 442,294 416,306 Z",
       "Cap crown", fill=UNIFORM_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M404,310 C440,294 516,296 546,314 C548,322 544,326 536,326 "
       "C500,312 448,310 410,320 C404,318 402,314 404,310 Z",
       "Cap brim", fill="#1C2C24", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Cap badge", x=468, y=268, width=16, height=16,
        fill=GOLD_GRAD, stroke=INK, strokeWidth=3)
# head
d.shape("ellipse", "Head", x=398, y=318, width=146, height=142,
        fill=FACE_GRAD, stroke=INK, strokeWidth=6)
# face: the custodian's level, watchful regard
d.shape("ellipse", "Eye L", x=434, y=386, width=17, height=20, fill="#241822", stroke=NONE)
d.shape("ellipse", "Eye R", x=496, y=386, width=17, height=20, fill="#241822", stroke=NONE)
d.shape("ellipse", "Glint L", x=438, y=390, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=500, y=390, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M430,368 C440,364 452,364 460,368", "Brow L",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round", opacity=70)
d.path("M488,368 C498,364 510,364 518,368", "Brow R",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round", opacity=70)
d.path("M454,434 L492,434", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4.5, cap="round")
d.shape("ellipse", "Cheek L", x=414, y=414, width=24, height=10, fill="#C98E72", opacity=35, stroke=NONE)
d.shape("ellipse", "Cheek R", x=510, y=414, width=24, height=10, fill="#C98E72", opacity=35, stroke=NONE)

# --- the frayed gold satin ribbon, held taut ----------------------------------------
# main band sagging gently between her hands
d.path("M352,596 C420,622 520,624 592,596 L596,612 C524,640 420,638 348,612 Z",
       "Ribbon band", fill=GOLD_GRAD, stroke=INK, strokeWidth=4, join="round")
# satin sheen along the band's upper edge
d.path("M360,600 C424,624 518,626 588,600", "Ribbon sheen",
       fill=NONE, stroke="#F8E89A", strokeWidth=4, cap="round", opacity=70)
# tail past the right hand, hanging to a swallowtail notch
d.path("M592,596 C616,614 628,640 630,668 L642,652 L644,680 "
       "C626,672 604,650 588,620 L596,612 Z",
       "Ribbon tail", fill=GOLD_GRAD, stroke=INK, strokeWidth=4, join="round")
# frayed strands escaping the cut end
d.path("M632,668 C646,682 652,696 650,712", "Strand 1",
       fill=NONE, stroke=GOLD_GRAD, strokeWidth=4, cap="round")
d.path("M640,672 C654,682 662,692 664,704", "Strand 2",
       fill=NONE, stroke="#D9A832", strokeWidth=3.5, cap="round")
d.path("M626,672 C636,688 638,700 634,714", "Strand 3",
       fill=NONE, stroke="#B8860B", strokeWidth=3.5, cap="round")
d.path("M644,664 C658,672 666,680 670,690", "Strand 4",
       fill=NONE, stroke="#F4D060", strokeWidth=3, cap="round", opacity=85)
# loose thread on the band, already drifting
d.path("M430,626 C426,640 430,652 438,660", "Loose thread",
       fill=NONE, stroke="#F4D060", strokeWidth=3, cap="round", opacity=80)
# her mitten hands pinching the band
d.shape("ellipse", "Hand L", x=340, y=590, width=34, height=38,
        fill=FACE_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=584, y=588, width=34, height=38,
        fill=FACE_GRAD, stroke=INK, strokeWidth=4)
# thumb creases
d.path("M354,604 C360,608 366,608 372,604", "Thumb L",
       fill=NONE, stroke=INK, strokeWidth=3, cap="round", opacity=60)
d.path("M596,602 C602,606 608,606 614,602", "Thumb R",
       fill=NONE, stroke=INK, strokeWidth=3, cap="round", opacity=60)

# --- name + role -------------------------------------------------------------------
d.text("RIBBONWARD CORDIALIS", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#EBDFF0", justify="center")
r = d.text("COMMEMORATIVE ARTIFACT CUSTODIAN", "Role", x=500, y=968,
           size=23, font="Virelai Sans", color="#B9A5C4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("309.ribbonward-cordialis-V1R00")
