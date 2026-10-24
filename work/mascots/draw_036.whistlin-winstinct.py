#!/usr/bin/env python3
"""Whistlin Winstinct — mascot portrait V1R00. Vista Prophet That
Never Was: a little glass figure whistling on a half-rendered boot
screen — aurora gradients laid down in hard un-antialiased bands, the
taskbar bolted on crooked, corrupted .theme files scattered across
the desktop. His lower half never finished rasterizing; it dissolves
into pixel chunks. Aurora-slate plate on a deep navy night. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Whistlin Winstinct — Mascot Plate", 1000, 1000)

INK = "#241E30"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0C1024"}, {"offset": 1, "color": "#040510"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E6E8E"}, {"offset": 0.6, "color": "#24466A"},
    {"offset": 1, "color": "#101E38"}]}}
GLASS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0FAFF"}, {"offset": 0.6, "color": "#B8DCEC"},
    {"offset": 1, "color": "#7EAEC8"}]}}
CHROME_GRAD = {"gradient": {"kind": "linear", "start": [0, 190], "end": [0, 250], "stops": [
    {"offset": 0, "color": "#D6E8F2"}, {"offset": 0.5, "color": "#9FBECC"},
    {"offset": 1, "color": "#5E8296"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "start": [0, 250], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#16304A"}, {"offset": 1, "color": "#081424"}]}}
TASK_GRAD = {"gradient": {"kind": "linear", "start": [0, 630], "end": [0, 690], "stops": [
    {"offset": 0, "color": "#4E6A80"}, {"offset": 1, "color": "#1E3244"}]}}
# the aurora, in its proudly un-antialiased bands
BANDS = ["#1E5E5C", "#2E8E7C", "#4EBE9C", "#7EDCB4", "#B8F0CC"]

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#3E6E8E", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#12102A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8DCEC", strokeWidth=3, opacity=28)
d.shape("ellipse", "Aurora spill", x=330, y=300, width=360, height=280,
        fill="#4EBE9C", opacity=12, stroke=NONE)
d.shape("ellipse", "Patina 1", x=600, y=160, width=230, height=130,
        fill="#24466A", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=160, y=620, width=240, height=140,
        fill="#101E38", opacity=26, stroke=NONE)
for i, (x, y, w) in enumerate([(220,350,5),(790,336,6),(176,542,5),(844,550,5),
                               (266,754,5),(722,762,6),(156,450,5),(850,646,5),
                               (434,128,5),(600,126,6),(340,150,4),(696,198,5),
                               (248,662,4),(670,714,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C4E2F0", opacity=28, stroke=NONE)
# ghost aero-swoosh arcs on the dark backdrop
d.path("M938,162 A108,108 0 0 0 838,60", "Ghost arc TR",
       fill=NONE, stroke="#3E8E9E", strokeWidth=14, opacity=10, cap="round")
d.path("M72,774 A120,120 0 0 0 188,878", "Ghost arc BL",
       fill=NONE, stroke="#3E8E9E", strokeWidth=10, opacity=8, cap="round")

# --- the boot screen window ---------------------------------------------------------------
WX0, WY0, WX1, WY1 = 246, 192, 754, 706
d.shape("ellipse", "Window shadow", x=280, y=690, width=470, height=34,
        fill="#04060C", opacity=45, stroke=NONE)
d.shape("rectangle", "Window", x=WX0, y=WY0, width=WX1 - WX0,
        height=WY1 - WY0, radius=14, fill=DESK_GRAD, stroke=INK,
        strokeWidth=5)
# aero glass title bar
d.shape("rectangle", "Title bar", x=WX0 + 4, y=WY0 + 4, width=WX1 - WX0 - 8,
        height=52, radius=12, fill=CHROME_GRAD, opacity=90, stroke=NONE)
d.shape("rectangle", "Title sheen", x=WX0 + 12, y=WY0 + 8,
        width=WX1 - WX0 - 24, height=20, radius=10, fill="#FFFFFF",
        opacity=35, stroke=NONE)
d.text("WHISTLER SETUP", "Window title", x=WX0 + 20, y=WY0 + 38, size=19,
       font="Virelai Sans", color="#16202E", justify="left")
# traffic-light-less aero buttons: min, max, close
d.shape("rectangle", "Btn min", x=WX1 - 108, y=WY0 + 18, width=26, height=20,
        radius=4, fill="#7EA0B4", stroke=INK, strokeWidth=2)
d.shape("rectangle", "Btn max", x=WX1 - 74, y=WY0 + 18, width=26, height=20,
        radius=4, fill="#7EA0B4", stroke=INK, strokeWidth=2)
d.shape("rectangle", "Btn close", x=WX1 - 40, y=WY0 + 18, width=26, height=20,
        radius=4, fill="#C05A4E", stroke=INK, strokeWidth=2)
d.path(f"M{WX1 - 34},{WY0 + 23} L{WX1 - 20},{WY0 + 33} M{WX1 - 20},{WY0 + 23} "
       f"L{WX1 - 34},{WY0 + 33}", "Close X", fill=NONE, stroke="#3A1414",
       strokeWidth=2.5, cap="round")

# --- the aurora, half-rendered: hard bands sweeping the desktop ---------------------------
# each band is a closed ribbon whose every point stays inside the window
BAND_PATHS = [
    "M{0},330 C{1},280 {2},290 {3},330 L{3},368 C{2},330 {1},318 {0},368 Z",
    "M{0},392 C{1},340 {2},350 {3},396 L{3},442 C{2},396 {1},386 {0},442 Z",
    "M{0},452 C{1},408 {2},420 {3},462 L{3},512 C{2},462 {1},452 {0},512 Z",
    "M{0},514 C{1},478 {2},490 {3},526 L{3},580 C{2},532 {1},522 {0},580 Z",
    "M{0},578 C{1},550 {2},560 {3},588 L{3},642 C{2},600 {1},596 {0},642 Z",
]
BXS = (WX0 + 16, 380, 620, WX1 - 16)
for i, tmpl in enumerate(BAND_PATHS):
    d.path(tmpl.format(*BXS), f"Aurora band {i+1}", fill=BANDS[i],
           opacity=92 - i * 8, stroke=NONE)
# the bliss-hill silhouette at the bottom of the desktop
d.path(f"M{WX0 + 16},700 C{360},640 {520},668 {620},644 "
       f"C{680},630 {720},640 {WX1 - 16},650 L{WX1 - 16},{WY1 - 4} "
       f"L{WX0 + 16},{WY1 - 4} Z",
       "Bliss hill", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#3E7E46"}, {"offset": 1, "color": "#1E4A28"}]}},
       opacity=85, stroke=NONE)
# a pale aurora sun
d.shape("ellipse", "Aurora sun", x=580, y=300, width=90, height=90,
        fill="#F0F4D8", opacity=55, stroke=NONE)
d.shape("ellipse", "Sun core", x=600, y=320, width=50, height=50,
        fill="#F8FBEA", opacity=60, stroke=NONE)

# --- corrupted .theme files, scattered ------------------------------------------------------
def theme_file(cx, cy, deg, label):
    parts = []
    parts.append(d.path(rot_rect_path(cx, cy, 52, 62, deg), f"{label} page",
                        fill={"gradient": {"kind": "linear", "stops": [
                            {"offset": 0, "color": "#E4E0D0"},
                            {"offset": 1, "color": "#B4AC94"}]}},
                        stroke=INK, strokeWidth=2.5))
    # dog-ear
    parts.append(d.path(rot_rect_path(cx + 15, cy - 22, 22, 20, deg + 45),
                        f"{label} ear", fill="#8E8874", stroke=INK,
                        strokeWidth=2))
    # corrupted palette swatches — one band torn out of alignment
    for k, col in enumerate(("#C05A4E", "#4E8E6E", "#C8A04E")):
        parts.append(d.shape("rectangle", f"{label} swatch {k+1}",
                             x=int(cx - 16), y=int(cy - 12 + k * 11),
                             width=32, height=7, radius=2, fill=col,
                             opacity=90, stroke=NONE))
    parts.append(d.shape("rectangle", f"{label} torn swatch",
                         x=int(cx - 8), y=int(cy + 21), width=32, height=7,
                         radius=2, fill="#4E6E9E", opacity=90, stroke=NONE))
    parts.append(d.text(".theme", f"{label} tag", x=int(cx - 22),
                        y=int(cy + 46), size=11, font="Virelai Sans",
                        color="#2A2418", justify="left"))
    for p in parts:
        if p and p.get("id"):
            d.cmd("object.rotate", f"{label} rot", ids=[p["id"]],
                  angle=deg, origin=[cx, cy])

theme_file(300, 330, -14, "Theme 1")
theme_file(718, 566, -8, "Theme 2")
theme_file(296, 470, 7, "Theme 3")

# --- the misaligned taskbar ------------------------------------------------------------------
TASK_A = 3
d.path(rot_rect_path(520, 668, 530, 44, TASK_A), "Taskbar",
       fill=TASK_GRAD, stroke=INK, strokeWidth=4)
d.path(rot_rect_path(520, 656, 530, 8, TASK_A), "Taskbar sheen",
       fill="#C8DCE8", opacity=30, stroke=NONE)
# start orb with the four-pane flag
d.shape("ellipse", "Start orb", x=256, y=668, width=34, height=34,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#B8E4F4"}, {"offset": 1, "color": "#3E7EA0"}]}},
        stroke=INK, strokeWidth=3)
for j, (ox, oy, col) in enumerate(((-6, -7, "#E06A5A"), (2, -7, "#7EC87E"),
                                   (-6, 1, "#5AA0D8"), (2, 1, "#F0C05E"))):
    d.path(rot_rect_path(273 + ox, 685 + oy, 8, 6, -12), f"Orb pane {j+1}",
           fill=col, stroke=NONE)
# task buttons that never settled
d.path(rot_rect_path(356, 672, 96, 24, TASK_A), "Task btn 1",
       fill="#3A5468", stroke=INK, strokeWidth=2.5)
d.path(rot_rect_path(462, 668, 74, 24, TASK_A + 4), "Task btn 2",
       fill="#3A5468", stroke=INK, strokeWidth=2.5)
# a clock tray, slid too far and tilted
d.path(rot_rect_path(730, 660, 62, 26, TASK_A + 8), "Tray",
       fill="#3A5468", stroke=INK, strokeWidth=2.5)

# --- boot progress, stalled -------------------------------------------------------------------
d.shape("rectangle", "Boot well", x=330, y=586, width=240, height=16,
        radius=8, fill="#0A1826", opacity=85, stroke=NONE)
for j in range(7):
    d.shape("rectangle", f"Boot chunk {j+1}", x=336 + j * 32, y=589,
            width=26, height=10, radius=4,
            fill="#5EC89E" if j < 4 else "#24425A",
            opacity=95 if j < 4 else 70, stroke=NONE)
d.text("BOOTING WHISTLER", "Boot label", x=268, y=576, size=15,
       font="Virelai Sans", color="#B8D8E4", justify="left")

# --- Winstinct: the glass prophet --------------------------------------------------------------
# his four-pane flag cape, streaming behind
CAPE = [(0, "#E06A5A"), (1, "#7EC87E"), (2, "#5AA0D8"), (3, "#F0C05E")]
d.path("M600,430 C660,420 710,440 748,478 C706,470 660,470 620,486 Z",
       "Cape wave", fill="#4E6E8E", opacity=60, stroke=NONE)
for j, (off, col) in enumerate(CAPE):
    px = 606 + (j % 2) * 34
    py = 424 + (j // 2) * 30
    d.path(f"M{px},{py} C{px + 14},{py - 8} {px + 28},{py - 4} {px + 36},{py + 6} "
           f"L{px + 34},{py + 22} C{px + 22},{py + 12} {px + 10},{py + 14} "
           f"{px - 2},{py + 20} Z",
           f"Cape pane {j+1}", fill=col, opacity=85, stroke=INK,
           strokeWidth=2)
# un-rendered pixels dissolving off his hem
for i, (x, y, w, op) in enumerate([(452,596,14,70),(478,612,12,60),(438,620,10,50),
                                   (468,634,11,55),(498,622,9,45),(444,646,8,40),
                                   (486,648,8,35),(462,662,7,30),(508,640,7,30)]):
    d.shape("rectangle", f"Voxel {i+1}", x=x, y=y, width=w, height=w,
            fill=GLASS_GRAD, opacity=op, stroke=NONE)
# body: one smooth glass drop, head and torso in a single pour
d.path("M500,330 C556,330 590,376 590,440 C590,486 574,528 552,556 "
       "C540,584 528,600 500,604 C472,600 460,584 448,556 "
       "C426,528 410,486 410,440 C410,376 444,330 500,330 Z",
       "Glass body", fill=GLASS_GRAD, opacity=88, stroke=INK, strokeWidth=5)
# aero refraction: inner squiggle + edge light
d.path("M440,400 C452,432 452,470 442,502", "Edge light L",
       fill=NONE, stroke="#FFFFFF", strokeWidth=7, opacity=50, cap="round")
d.path("M560,410 C568,438 566,470 556,496", "Edge light R",
       fill=NONE, stroke="#FFFFFF", strokeWidth=5, opacity=35, cap="round")
d.shape("ellipse", "Forehead gleam", x=452, y=348, width=96, height=54,
        fill="#FFFFFF", opacity=45, stroke=NONE)
d.path("M470,560 C480,540 520,540 530,560 C518,572 482,572 470,560 Z",
       "Inner refract", fill="#8FC0D8", opacity=50, stroke=NONE)
# face: aspiring and confused — one brow up, crooked whistle
d.shape("ellipse", "Eye L", x=452, y=420, width=24, height=30,
        fill="#16202E", opacity=95, stroke=NONE)
d.shape("ellipse", "Eye R", x=524, y=420, width=24, height=30,
        fill="#16202E", opacity=95, stroke=NONE)
d.shape("ellipse", "Glint L", x=458, y=426, width=8, height=8,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=530, y=426, width=8, height=8,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M446,404 C456,396 468,396 478,402", "Brow L raised",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path("M522,410 C532,406 544,407 554,412", "Brow R flat",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
# the whistle — a small puckered O
d.shape("ellipse", "Whistle", x=488, y=478, width=24, height=20,
        fill="#3A5468", stroke=INK, strokeWidth=3)
# two notes escaping, half-formed like everything else
d.path("M540,486 L540,462 L560,458 L560,482", "Note 1 stem",
       fill=NONE, stroke="#B8DCF0", strokeWidth=3.5, cap="round")
d.shape("ellipse", "Note 1 head", x=530, y=482, width=13, height=9,
        fill="#B8DCF0", opacity=90, stroke=NONE)
d.path("M584,502 L584,480", "Note 2 stem", fill=NONE, stroke="#B8DCF0",
       strokeWidth=3, cap="round")
d.shape("ellipse", "Note 2 head", x=576, y=498, width=11, height=8,
        fill="#B8DCF0", opacity=70, stroke=NONE)
# stubby glass arms, one raised in prophecy
d.path("M414,470 C388,480 372,500 370,524 C380,534 394,532 402,522 "
       "C406,504 414,490 428,482 Z",
       "Arm L", fill=GLASS_GRAD, opacity=85, stroke=INK, strokeWidth=3.5)
d.path("M586,462 C606,440 620,416 624,392 C634,388 646,394 648,406 "
       "C640,436 622,462 600,480 C592,476 586,470 586,462 Z",
       "Arm R", fill=GLASS_GRAD, opacity=85, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Hand R", x=622, y=378, width=30, height=28,
        fill=GLASS_GRAD, opacity=85, stroke=INK, strokeWidth=3)

# --- name + role -------------------------------------------------------------------------------
d.text("WHISTLIN WINSTINCT", "Name", x=500, y=930, size=52, font="Virelai Sans",
       color="#DCECF4", justify="center")
r = d.text("VISTA PROPHET THAT NEVER WAS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9EC4D8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=140)

d.finish("036.whistlin-winstinct-V1R00")
