#!/usr/bin/env python3
"""Holy DOSwell — mascot portrait V1R00. Divine Segmentation Prophet:
a hooded prophet in DOS-blue robes blessing floating .sys cards with a
heated branding iron, burnt floppy relic at hand, the sixteen-color
console glowing behind. TempleOS/DOS lineage: reverent and unstable.
Warm temple-stone plate on an ember-night backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Holy DOSwell — Mascot Plate", 1000, 1000)

INK = "#241C16"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#18100C"}, {"offset": 1, "color": "#0A0705"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6B5A48"}, {"offset": 0.62, "color": "#43352A"},
    {"offset": 1, "color": "#241B14"}]}}
CONSOLE_GRAD = {"gradient": {"kind": "linear", "start": [0, 150], "end": [0, 330], "stops": [
    {"offset": 0, "color": "#161D26"}, {"offset": 1, "color": "#0B0E13"}]}}
ROBE_GRAD = {"gradient": {"kind": "linear", "start": [0, 380], "end": [0, 770], "stops": [
    {"offset": 0, "color": "#3A50A8"}, {"offset": 0.55, "color": "#26346E"},
    {"offset": 1, "color": "#16204A"}]}}
HOOD_INNER = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A3226"}, {"offset": 1, "color": "#120E0A"}]}}
CARD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E9DDC2"}, {"offset": 1, "color": "#C9B992"}]}}
EMBER_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFE9A8"}, {"offset": 0.6, "color": "#F0913A"},
    {"offset": 1, "color": "#D84E14"}]}}
FLOPPY_GRAD = {"gradient": {"kind": "linear", "start": [0, 660], "end": [0, 780], "stops": [
    {"offset": 0, "color": "#333B46"}, {"offset": 1, "color": "#161A20"}]}}
GOLD = "#C89A3C"

CGA = ["#1A1A1A", "#0000AA", "#00AA00", "#00AAAA", "#AA0000", "#AA00AA",
       "#AA5500", "#AAAAAA", "#555555", "#5555FF", "#55FF55", "#55FFFF",
       "#FF5555", "#FF55FF", "#FFFF55", "#FFFFFF"]

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#8A6A4A", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1A140E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C9AE84", strokeWidth=3, opacity=30)
# ember glow low on the plate — the iron's ambient light
d.shape("ellipse", "Ember ambience", x=330, y=600, width=340, height=200,
        fill="#D8702A", opacity=9, stroke=NONE)
# temple patina + flecks
d.shape("ellipse", "Patina 1", x=190, y=360, width=230, height=150,
        fill="#54432F", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=560, width=230, height=140,
        fill="#7A6248", opacity=15, stroke=NONE)
for i, (x, y, w) in enumerate([(215,340,5),(795,335,6),(180,545,5),(848,560,5),
                               (260,765,5),(730,770,6),(155,455,5),(860,625,5),
                               (430,125,5),(600,138,6),(335,160,4),(705,200,5),
                               (245,650,4),(665,720,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#E0CFA8", opacity=32, stroke=NONE)
# ghost arcs on the dark backdrop
d.path("M935,150 A105,105 0 0 0 845,60", "Ghost arc TR",
       fill=NONE, stroke="#6A4A30", strokeWidth=14, opacity=10, cap="round")
d.path("M75,770 A120,120 0 0 0 185,875", "Ghost arc BL",
       fill=NONE, stroke="#6A4A30", strokeWidth=10, opacity=8, cap="round")

# --- the sixteen-color console, behind him ---------------------------------------
d.shape("rectangle", "Console shadow", x=224, y=158, width=556, height=178,
        radius=10, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Console", x=216, y=150, width=556, height=178,
        radius=10, fill=CONSOLE_GRAD, stroke="#3D332A", strokeWidth=3)
d.shape("rectangle", "Console titlebar", x=216, y=150, width=556, height=26,
        radius=10, fill="#242C38", stroke=NONE)
d.path("M236,163 L308,163", "Console title",
       fill=NONE, stroke="#7A8694", strokeWidth=4, cap="round", opacity=70)
d.shape("ellipse", "Console close dot", x=744, y=158, width=10, height=10,
        fill="#AA4444", stroke=NONE, opacity=85)
# the canonical sixteen
for i, c in enumerate(CGA):
    col, row = i % 8, i // 8
    x, y = 244 + col * 64, 196 + row * 52
    d.shape("rectangle", f"CGA {i:02d}", x=x, y=y, width=54, height=40,
            radius=4, fill=c, stroke="#05070A", strokeWidth=2)
# the prompt, waiting on a gospel
d.text("C:\\>_", "Prompt", x=250, y=318, size=17, font="Source Sans 3",
       color="#6FDC6F")
# faint scanlines
for j, yy in enumerate((206, 252, 300)):
    d.path(f"M232,{yy} L760,{yy}", f"Scanline {j+1}",
           fill=NONE, stroke="#FFFFFF", strokeWidth=1, opacity=4)

# --- floating .sys cards awaiting blessing ----------------------------------------
def sys_card(cx, cy, w=86, h=58, lit=False):
    d.shape("rectangle", f"SYS card {cx}", x=cx - w // 2, y=cy - h // 2,
            width=w, height=h, radius=6, fill=CARD_GRAD,
            stroke="#6A5A40", strokeWidth=2.5)
    d.shape("rectangle", f"SYS card header {cx}", x=cx - w // 2 + 6,
            y=cy - h // 2 + 6, width=w - 12, height=12, radius=3,
            fill="#8A7A56", opacity=70, stroke=NONE)
    d.text(".SYS", f"SYS label {cx}", x=cx, y=cy + 18, size=15,
           font="Virelai Sans", color="#5A4C34", justify="center")

sys_card(640, 210)
sys_card(778, 232)
# the card being branded — directly under the iron tip
sys_card(726, 268, lit=True)
d.shape("ellipse", "Brand glow", x=700, y=252, width=52, height=40,
        fill="#F6B84E", opacity=30, stroke=NONE)
d.path(rot_rect_path(726, 272, 22, 22, 45), "Brand mark",
       fill=EMBER_GRAD, stroke="#8A4A10", strokeWidth=2)

# --- the prophet -------------------------------------------------------------------
# left sleeve reaching toward the relic
d.path("M452,520 C420,560 402,620 404,668 C414,682 434,684 446,674 "
       "C446,628 458,580 474,548 Z",
       "Sleeve L", fill=ROBE_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand L", x=404, y=658, width=30, height=26,
        fill="#C9A888", stroke=INK, strokeWidth=3)
# robe body: bell silhouette
d.path("M500,430 C552,432 586,470 596,540 C604,600 612,680 606,742 "
       "C560,768 440,768 396,742 C390,680 398,600 406,540 "
       "C416,470 448,432 500,430 Z",
       "Robe", fill=ROBE_GRAD, stroke=INK, strokeWidth=5)
# robe shade right side + hem shade
d.path("M560,460 C590,510 606,620 602,736 C580,750 552,758 528,760 "
       "C556,700 566,560 560,460 Z",
       "Robe shade", fill="#101838", opacity=45, stroke=NONE)
d.path("M398,712 C450,732 550,732 604,712 L606,742 C560,768 440,768 396,742 Z",
       "Hem shade", fill="#0E1430", opacity=40, stroke=NONE)
# center trim, gold
d.path("M500,468 C498,560 498,660 500,748", "Robe trim",
       fill=NONE, stroke=GOLD, strokeWidth=6, opacity=85)
d.path("M470,520 L530,520 M462,600 L538,600 M456,684 L544,684",
       "Trim bars", fill=NONE, stroke=GOLD, strokeWidth=3, opacity=45)
# right sleeve raised with the iron
d.path("M548,470 C596,440 636,412 664,376 C678,376 690,390 690,404 "
       "C662,448 622,488 580,512 C564,500 552,486 548,470 Z",
       "Sleeve R", fill=ROBE_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=658, y=372, width=32, height=28,
        fill="#C9A888", stroke=INK, strokeWidth=3)
# hood over the robe's shoulders
d.path("M500,368 C556,368 588,408 586,458 C584,496 548,520 500,520 "
       "C452,520 416,496 414,458 C412,408 444,368 500,368 Z",
       "Hood", fill=ROBE_GRAD, stroke=INK, strokeWidth=5)
d.path("M500,368 C556,368 588,408 586,458 C570,444 540,436 500,436 "
       "C460,436 430,444 414,458 C412,408 444,368 500,368 Z",
       "Hood rim light", fill="#5468C0", opacity=55, stroke=NONE)
# face shadow inside the hood
d.shape("ellipse", "Face shadow", x=448, y=422, width=104, height=78,
        fill=HOOD_INNER, stroke=NONE)
# the eyes: two small votive flames
d.shape("ellipse", "Eye glow L", x=466, y=448, width=22, height=22,
        fill="#F6B84E", opacity=30, stroke=NONE)
d.shape("ellipse", "Eye glow R", x=512, y=448, width=22, height=22,
        fill="#F6B84E", opacity=30, stroke=NONE)
d.shape("ellipse", "Eye L", x=471, y=453, width=12, height=12,
        fill=EMBER_GRAD, stroke=NONE)
d.shape("ellipse", "Eye R", x=517, y=453, width=12, height=12,
        fill=EMBER_GRAD, stroke=NONE)

# --- the heated branding iron -------------------------------------------------------
# rod from the raised hand up toward the blessed card
d.path("M668,388 L730,296", "Iron rod",
       fill=NONE, stroke="#3A3230", strokeWidth=8, cap="round")
d.path("M668,388 L696,348", "Iron rod sheen",
       fill=NONE, stroke="#6A5C50", strokeWidth=3, cap="round", opacity=70)
d.shape("ellipse", "Iron tip glow", x=712, y=268, width=52, height=52,
        fill="#F6A83C", opacity=28, stroke=NONE)
d.path(rot_rect_path(738, 290, 26, 26, 45), "Iron tip",
       fill=EMBER_GRAD, stroke="#8A4A10", strokeWidth=2.5)
# heat shimmer above the tip
d.path("M728,252 C736,240 744,244 750,232", "Heat wisp 1",
       fill=NONE, stroke="#F6C35C", strokeWidth=3, opacity=45, cap="round")
d.path("M748,258 C756,246 764,250 770,238", "Heat wisp 2",
       fill=NONE, stroke="#F6C35C", strokeWidth=3, opacity=35, cap="round")

# --- the burnt floppy relic, at his left hand ---------------------------------------
fx, fy = 310, 690
d.shape("ellipse", "Relic aura", x=fx - 20, y=fy - 18, width=140, height=132,
        fill="#C89A3C", opacity=10, stroke=NONE)
d.path(rot_rect_path(fx + 48, fy + 48, 96, 96, -8), "Floppy body",
       fill=FLOPPY_GRAD, stroke=INK, strokeWidth=4)
d.path(rot_rect_path(fx + 52, fy + 22, 56, 34, -8), "Floppy shutter",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#9AA4AE"}, {"offset": 1, "color": "#5E6874"}]}},
       stroke=INK, strokeWidth=3)
d.path(rot_rect_path(fx + 66, fy + 24, 14, 26, -8), "Shutter window",
       fill="#14181E", stroke=NONE)
d.path(rot_rect_path(fx + 42, fy + 74, 46, 30, -8), "Floppy label",
       fill="#C9BC9C", stroke="#6A5A40", strokeWidth=2)
# scorch: burnt corner + embers + a thin smoke line
d.path("M344,748 C356,724 380,710 402,712 C400,738 384,760 358,766 "
       "C350,762 344,756 344,748 Z",
       "Scorch", fill="#100C08", opacity=85, stroke=NONE)
d.shape("ellipse", "Scorch ember 1", x=366, y=730, width=8, height=8,
        fill=EMBER_GRAD, opacity=80, stroke=NONE)
d.shape("ellipse", "Scorch ember 2", x=384, y=742, width=6, height=6,
        fill="#F0913A", opacity=70, stroke=NONE)
d.path("M352,700 C344,678 356,664 348,644", "Relic smoke",
       fill=NONE, stroke="#B8B0A0", strokeWidth=3, opacity=22, cap="round")

# --- name + role ----------------------------------------------------------------------
d.text("HOLY DOSWELL", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#E8D9B8", justify="center")
r = d.text("DIVINE SEGMENTATION PROPHET", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B89A6A", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=170)

d.finish("030.holy-doswell-V1R00")
