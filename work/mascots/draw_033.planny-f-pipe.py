#!/usr/bin/env python3
"""Planny F. PipeMD — mascot portrait V1R00. Pipe Network Engineer:
Glenda's great-niece threading a glowing 9P pipe through union-mount
couplers, an organ-bank of vertical pipes behind her, miniature "9P"
flags and a tiny Glenda icon stuck to her toolkit. Sage-steel plate on
a slate-night backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Planny F. PipeMD — Mascot Plate", 1000, 1000)

INK = "#3A2A24"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#122028"}, {"offset": 1, "color": "#060B0E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C4D8CE"}, {"offset": 0.62, "color": "#8AAFA2"},
    {"offset": 1, "color": "#466A6C"}]}}
PIPE_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [70, 0], "stops": [
    {"offset": 0, "color": "#E8BE6A"}, {"offset": 0.5, "color": "#C8913C"},
    {"offset": 1, "color": "#8A5E24"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0E4CE"}, {"offset": 0.7, "color": "#D5C1A0"},
    {"offset": 1, "color": "#AC9270"}]}}
SUIT_GRAD = {"gradient": {"kind": "linear", "start": [0, 500], "end": [0, 800], "stops": [
    {"offset": 0, "color": "#3E6070"}, {"offset": 0.55, "color": "#2A4654"},
    {"offset": 1, "color": "#182C38"}]}}
TOOL_GRAD = {"gradient": {"kind": "linear", "start": [0, 700], "end": [0, 800], "stops": [
    {"offset": 0, "color": "#8A5A48"}, {"offset": 1, "color": "#54342C"}]}}
GLOW = "#FFECA8"
CRIMSON = "#C8485C"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#7EA89E", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1C2A28", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8ECE2", strokeWidth=3, opacity=30)
# cool glow where the union mount happens
d.shape("ellipse", "Stage glow", x=300, y=300, width=400, height=300,
        fill="#D0E8DC", opacity=12, stroke=NONE)
d.shape("ellipse", "Patina 1", x=580, y=150, width=240, height=140,
        fill="#5E8A82", opacity=18, stroke=NONE)
d.shape("ellipse", "Patina 2", x=170, y=600, width=250, height=150,
        fill="#2C4A50", opacity=20, stroke=NONE)
for i, (x, y, w) in enumerate([(222,352,5),(788,330,6),(176,540,5),(842,545,5),
                               (268,752,5),(722,760,6),(156,450,5),(852,640,5),
                               (430,128,5),(598,126,6),(342,150,4),(694,196,5),
                               (246,660,4),(668,712,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#E4F2E8", opacity=30, stroke=NONE)
# ghost pipe-elbow arcs on the dark backdrop
d.path("M940,160 A110,110 0 0 0 840,60", "Ghost arc TR",
       fill=NONE, stroke="#5E8A84", strokeWidth=14, opacity=10, cap="round")
d.path("M70,780 A120,120 0 0 0 185,880", "Ghost arc BL",
       fill=NONE, stroke="#5E8A84", strokeWidth=10, opacity=8, cap="round")

# --- the pipe organ bank -------------------------------------------------------------
def pipe(cx, top, bottom, w, label):
    """Vertical brass pipe: rounded cap, one coupler ring (union mount),
    faint highlight stripe."""
    d.shape("rectangle", f"{label} body", x=int(cx - w / 2), y=top,
            width=w, height=bottom - top, fill=PIPE_GRAD,
            stroke=INK, strokeWidth=3.5)
    d.shape("ellipse", f"{label} cap", x=int(cx - w / 2), y=top - 10,
            width=w, height=20, fill="#E8BE6A", stroke=INK, strokeWidth=3.5)
    # coupler ring — the union mount
    ry = top + (bottom - top) * 0.45
    d.shape("rectangle", f"{label} coupler", x=int(cx - w / 2 - 7), y=int(ry),
            width=w + 14, height=26, radius=8, fill="#7A5322",
            stroke=INK, strokeWidth=3)
    for j, bx in enumerate((cx - w / 2 - 2, cx + w / 2 + 2)):
        d.shape("ellipse", f"{label} bolt {j+1}", x=int(bx - 3), y=int(ry + 10),
                width=6, height=6, fill="#E8BE6A", stroke=NONE)
    # highlight stripe
    d.shape("rectangle", f"{label} light", x=int(cx - w / 4), y=top + 14,
            width=6, height=bottom - top - 30, fill="#FFE9B0", opacity=30,
            stroke=NONE)

pipe(228, 320, 700, 44, "Pipe L1")
pipe(300, 240, 700, 54, "Pipe L2")
pipe(376, 370, 700, 40, "Pipe L3")
pipe(624, 360, 700, 40, "Pipe R3")
pipe(700, 230, 700, 54, "Pipe R2")
pipe(772, 310, 700, 44, "Pipe R1")
# elbows tying the tall pair into the wall
d.path("M300,240 C300,190 340,170 392,168", "Elbow L",
       fill=NONE, stroke=PIPE_GRAD, strokeWidth=40, cap="round")
d.path("M700,230 C700,182 660,164 608,162", "Elbow R",
       fill=NONE, stroke=PIPE_GRAD, strokeWidth=40, cap="round")
# elbow outlines
d.path("M300,222 C300,178 344,152 392,150", "Elbow L top",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
d.path("M300,258 C300,206 344,188 392,186", "Elbow L bot",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
d.path("M700,212 C700,170 656,146 608,144", "Elbow R top",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
d.path("M700,248 C700,196 656,180 608,178", "Elbow R bot",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")

# --- the pipe she is threading ---------------------------------------------------------
# translucent barrel crossing the scene, bright bytes sliding inside
d.shape("rectangle", "Pipe barrel", x=250, y=548, width=500, height=46,
        radius=23, fill="#BFDAD2", opacity=45, stroke=INK, strokeWidth=3.5)
d.shape("rectangle", "Pipe glass light", x=260, y=554, width=480, height=12,
        radius=6, fill="#FFFFFF", opacity=35, stroke=NONE)
# union-mount rings it passes through
for i, ux in enumerate((318, 682)):
    d.shape("ellipse", f"Union ring {i+1}", x=ux - 20, y=532, width=40, height=78,
            fill="#7A5322", stroke=INK, strokeWidth=3.5)
    d.shape("ellipse", f"Union bore {i+1}", x=ux - 11, y=544, width=22, height=54,
            fill="#33505A", stroke=INK, strokeWidth=2.5)
# the bytes in flight
for i, bx in enumerate((290, 352, 470, 528, 596, 712)):
    d.shape("rectangle", f"Byte {i+1}", x=bx, y=561, width=26, height=20,
            radius=6, fill=GLOW, opacity=90, stroke=NONE)
    d.shape("ellipse", f"Byte halo {i+1}", x=bx - 8, y=555, width=42, height=32,
            fill=GLOW, opacity=22, stroke=NONE)
# end collars
d.shape("ellipse", "Barrel end L", x=244, y=548, width=22, height=46,
        fill="#7A5322", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Barrel end R", x=734, y=548, width=22, height=46,
        fill="#7A5322", stroke=INK, strokeWidth=3)

# --- Planny: bunny engineer -------------------------------------------------------------
# ground shadow
d.shape("ellipse", "Ground shadow", x=380, y=776, width=260, height=30,
        fill="#14201E", opacity=35, stroke=NONE)
# ears: one tall, one cocked
d.path("M472,352 C456,296 452,236 468,196 C484,206 494,272 494,344 Z",
       "Ear L", fill=FUR_GRAD, stroke=INK, strokeWidth=4.5)
d.path("M474,338 C464,296 462,252 470,220 C478,240 484,292 486,338 Z",
       "Ear L inner", fill="#C08A7A", opacity=70, stroke=NONE)
d.path("M524,346 C548,296 576,258 606,244 C608,272 570,330 542,352 Z",
       "Ear R", fill=FUR_GRAD, stroke=INK, strokeWidth=4.5)
d.path("M532,342 C552,306 574,278 592,262 C588,286 560,326 544,344 Z",
       "Ear R inner", fill="#C08A7A", opacity=70, stroke=NONE)
# head
d.shape("ellipse", "Head", x=424, y=342, width=152, height=140,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Head light", x=446, y=352, width=80, height=44,
        fill="#FFF6E0", opacity=35, stroke=NONE)
# muzzle + the smug grin
d.shape("ellipse", "Muzzle", x=464, y=424, width=72, height=48,
        fill="#EFE2CA", opacity=85, stroke=NONE)
d.path("M478,446 C494,458 514,458 528,444", "Smirk",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Nose", x=493, y=426, width=16, height=12,
        fill="#A85E5E", stroke=INK, strokeWidth=2.5)
# one buck tooth under the grin
d.shape("rectangle", "Tooth", x=496, y=450, width=12, height=14, radius=3,
        fill="#F8F2E2", stroke=INK, strokeWidth=2)
# eyes: calm, a little smug — upper lids lowered
d.shape("ellipse", "Eye L", x=452, y=394, width=24, height=30,
        fill="#241C14", stroke=NONE)
d.shape("ellipse", "Eye R", x=524, y=394, width=24, height=30,
        fill="#241C14", stroke=NONE)
d.shape("ellipse", "Glint L", x=458, y=400, width=7, height=7,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=530, y=400, width=7, height=7,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M448,398 L476,394", "Lid L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M524,394 L552,398", "Lid R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# whisker dots
for i, (x, y) in enumerate([(440,432),(436,448),(560,432),(564,448)]):
    d.shape("ellipse", f"Whisker dot {i+1}", x=x, y=y, width=5, height=5,
            fill="#8A7458", opacity=70, stroke=NONE)

# torso: engineer overalls
d.path("M500,486 C558,486 596,530 600,600 C603,668 592,724 574,756 "
       "C534,776 466,776 426,756 C408,724 397,668 400,600 "
       "C404,530 442,486 500,486 Z",
       "Overalls", fill=SUIT_GRAD, stroke=INK, strokeWidth=5)
# bib + straps
d.path("M452,560 L548,560 L544,660 C520,672 480,672 456,660 Z",
       "Bib", fill="#2A4654", stroke=INK, strokeWidth=3.5)
d.path("M452,560 L440,494 L460,488 L472,560 Z", "Strap L",
       fill="#2A4654", stroke=INK, strokeWidth=3.5)
d.path("M548,560 L560,494 L540,488 L528,560 Z", "Strap R",
       fill="#2A4654", stroke=INK, strokeWidth=3.5)
for i, bx in enumerate((462, 530)):
    d.shape("ellipse", f"Bib button {i+1}", x=bx, y=566, width=10, height=10,
            fill="#D9A44E", stroke=INK, strokeWidth=2)
# the tiny Glenda icon pinned to her bib — great-aunt watching
d.path("M500,606 C512,606 520,616 520,628 C520,640 512,648 500,648 "
       "C488,648 480,640 480,628 C480,616 488,606 500,606 Z",
       "Glenda badge", fill="#EFE2CA", stroke=INK, strokeWidth=2.5)
d.path("M492,610 C488,600 488,592 492,586 C496,592 496,602 495,610 Z",
       "Glenda ear L", fill="#EFE2CA", stroke=INK, strokeWidth=2)
d.path("M508,610 C512,600 512,592 508,586 C504,592 504,602 505,610 Z",
       "Glenda ear R", fill="#EFE2CA", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Glenda eye L", x=491, y=622, width=5, height=6,
        fill="#241C14", stroke=NONE)
d.shape("ellipse", "Glenda eye R", x=504, y=622, width=5, height=6,
        fill="#241C14", stroke=NONE)
# tool belt with pouches
d.shape("rectangle", "Tool belt", x=404, y=686, width=192, height=30,
        radius=10, fill=TOOL_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Pouch L", x=420, y=694, width=40, height=34, radius=6,
        fill="#6E463A", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Pouch R", x=540, y=694, width=40, height=34, radius=6,
        fill="#6E463A", stroke=INK, strokeWidth=3)
# belt buckle — a tiny pipe ring
d.shape("ellipse", "Buckle", x=488, y=690, width=26, height=22,
        fill=NONE, stroke="#D9A44E", strokeWidth=5)
# arms: right hand steadying the barrel, left arm down at the toolkit
d.path("M414,560 C380,590 364,630 366,668 C378,680 396,678 404,664 "
       "C406,632 418,600 438,580 Z",
       "Sleeve L", fill=SUIT_GRAD, stroke=INK, strokeWidth=4.5)
d.shape("ellipse", "Paw L", x=358, y=654, width=36, height=30,
        fill=FUR_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M586,540 C612,528 640,530 658,548 C662,564 652,578 636,578 "
       "C616,568 600,560 586,556 Z",
       "Sleeve R", fill=SUIT_GRAD, stroke=INK, strokeWidth=4.5)
d.shape("ellipse", "Paw R", x=636, y=544, width=34, height=30,
        fill=FUR_GRAD, stroke=INK, strokeWidth=3.5)
# feet: sturdy work boots
d.shape("ellipse", "Boot L", x=414, y=752, width=76, height=34,
        fill="#241E1C", stroke=INK, strokeWidth=4.5)
d.shape("ellipse", "Boot R", x=510, y=752, width=76, height=34,
        fill="#241E1C", stroke=INK, strokeWidth=4.5)

# --- the toolkit, flagged ----------------------------------------------------------------
d.shape("rectangle", "Toolkit", x=640, y=706, width=140, height=76, radius=10,
        fill=TOOL_GRAD, stroke=INK, strokeWidth=4.5)
d.path("M672,706 C672,688 748,688 748,706", "Toolkit handle",
       fill=NONE, stroke=INK, strokeWidth=9, cap="round")
d.shape("rectangle", "Toolkit latch", x=696, y=712, width=28, height=16, radius=4,
        fill="#D9A44E", stroke=INK, strokeWidth=2.5)
# second Glenda sticker on the toolkit
d.path("M664,742 C674,742 680,750 680,760 C680,770 674,776 664,776 "
       "C654,776 648,770 648,760 C648,750 654,742 664,742 Z",
       "Glenda sticker", fill="#EFE2CA", stroke=INK, strokeWidth=2)
d.path("M658,746 C655,738 655,732 658,727 C661,732 661,740 660,746 Z",
       "Glenda sticker ear L", fill="#EFE2CA", stroke=INK, strokeWidth=1.5)
d.path("M670,746 C673,738 673,732 670,727 C667,732 667,740 668,746 Z",
       "Glenda sticker ear R", fill="#EFE2CA", stroke=INK, strokeWidth=1.5)
# miniature 9P flags on sticks
def flag(x, y, h, label):
    d.path(f"M{x},{y} L{x},{y - h}", f"{label} stick",
           fill=NONE, stroke="#4E3A24", strokeWidth=4, cap="round")
    d.path(f"M{x},{y - h} L{x + 44},{y - h + 10} L{x},{y - h + 24} Z",
           f"{label} pennant", fill=CRIMSON, stroke=INK, strokeWidth=2.5)
    # Virelai Sans has no digits — Source Sans 3 carries the "9P"
    d.text("9P", f"{label} mark", x=x + 6, y=y - h + 19, size=15,
           font="Source Sans 3", color="#F8EAD0", justify="left")

flag(690, 706, 74, "Flag 1")
flag(742, 706, 56, "Flag 2")

# --- name + role ---------------------------------------------------------------------------
d.text("PLANNY F. PIPEMD", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#E8F2EA", justify="center")
r = d.text("PIPE NETWORK ENGINEER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B4CFC2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("033.planny-f-pipe-V1R00")
