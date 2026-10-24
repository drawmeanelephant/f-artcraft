#!/usr/bin/env python3
"""Robots Dot Txt — mascot portrait V1R00. Crawl Denial Cryptid:
a parchment text file seated at the server root, palm out, announcing
disallowed paths to two halted spider crawlers. Categorical, unbothered.
Phosphor-sage plate on a server-night backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Code-ish directive text in Source Sans 3. Plate = circle (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Robots Dot Txt — Mascot Plate", 1000, 1000)

INK = "#2A2118"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0E1A13"}, {"offset": 1, "color": "#050A07"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#52705C"}, {"offset": 0.62, "color": "#33493B"},
    {"offset": 1, "color": "#16241B"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "start": [0, 280], "end": [0, 660], "stops": [
    {"offset": 0, "color": "#F4EBD2"}, {"offset": 0.7, "color": "#E4D5B0"},
    {"offset": 1, "color": "#CDBB92"}]}}
DOG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FFF8E4"}, {"offset": 1, "color": "#DCCCA6"}]}}
BOT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A545C"}, {"offset": 1, "color": "#1E2428"}]}}
LEDGE_GRAD = {"gradient": {"kind": "linear", "start": [0, 660], "end": [0, 740], "stops": [
    {"offset": 0, "color": "#3C5245"}, {"offset": 1, "color": "#1C2A20"}]}}
PHOSPHOR = "#8FD9A0"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#5E8A6E", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0E1710", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8D9BE", strokeWidth=3, opacity=28)
# phosphor patina + flecks
d.shape("ellipse", "Patina 1", x=200, y=330, width=240, height=150,
        fill="#6E9380", opacity=18, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=560, width=240, height=150,
        fill="#2A4033", opacity=30, stroke=NONE)
for i, (x, y, w) in enumerate([(225,350,5),(790,345,6),(185,545,5),(845,575,5),
                               (265,760,5),(725,765,6),(165,455,5),(852,640,5),
                               (435,130,5),(595,140,6),(340,165,4),(700,205,5),
                               (255,660,4),(655,720,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#CFE8D2", opacity=30, stroke=NONE)
# faint phosphor scanlines across the plate
for j, yy in enumerate((250, 330, 560, 640)):
    d.path(f"M170,{yy} L830,{yy}", f"Scanline {j+1}",
           fill=NONE, stroke=PHOSPHOR, strokeWidth=1, opacity=5)
# ghost arcs on the dark backdrop
d.path("M930,160 A100,100 0 0 0 850,70", "Ghost arc TR",
       fill=NONE, stroke="#4E7A5C", strokeWidth=14, opacity=10, cap="round")
d.path("M80,780 A115,115 0 0 0 185,880", "Ghost arc BL",
       fill=NONE, stroke="#4E7A5C", strokeWidth=10, opacity=8, cap="round")

# --- faint directory tree behind him: the server root -------------------------
d.path("M500,150 L500,200 M500,200 L340,240 M500,200 L660,240",
       "Root tree trunk", fill=NONE, stroke=PHOSPHOR, strokeWidth=3, opacity=18)
for i, (x, y) in enumerate([(500, 146), (340, 246), (660, 246)]):
    d.shape("rectangle", f"Tree node {i+1}", x=x - 11, y=y - 9, width=22,
            height=18, radius=3, fill=NONE, stroke=PHOSPHOR, strokeWidth=2.5,
            opacity=22)
d.text("/", "Root glyph", x=500, y=160, size=15, font="Source Sans 3",
       color="#5E8A68", justify="center")

# --- crawler approach path: dashed crawl line that turns back ------------------
d.path("M848,600 C796,632 758,660 726,690 C756,708 792,714 826,700",
       "Crawler U-turn", fill=NONE, stroke=PHOSPHOR, strokeWidth=2.5,
       dash=[7, 9], opacity=35, cap="round")
for x, y in [(848, 600), (726, 690), (826, 700)]:
    assert on_disc(x, y, 4), (x, y)

# --- the ledge he sits on: the server root --------------------------------------
d.shape("ellipse", "Ledge shadow", x=310, y=700, width=400, height=46,
        fill="#08100B", opacity=45, stroke=NONE)
d.path("M330,668 L670,668 L700,706 C660,726 340,726 300,706 Z",
       "Root ledge", fill=LEDGE_GRAD, stroke=INK, strokeWidth=4)
d.text("/", "Ledge slash", x=502, y=700, size=22, font="Source Sans 3",
       color="#8FB898", justify="center")

# --- the file himself -------------------------------------------------------------
# stubby legs, crossed, sticking out below the sheet
d.path("M430,652 C420,672 428,686 452,686 C472,686 478,676 474,664 Z",
       "Foot L", fill=PAPER_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M570,652 C580,672 572,686 548,686 C528,686 522,676 526,664 Z",
       "Foot R", fill=PAPER_GRAD, stroke=INK, strokeWidth=3.5)
# sheet body with dog-eared top-right corner
d.path("M360,300 L590,300 L640,350 L640,648 C640,662 628,668 612,668 "
       "L388,668 C372,668 360,662 360,648 Z",
       "Sheet body", fill=PAPER_GRAD, stroke=INK, strokeWidth=5)
# dog-ear fold
d.path("M590,300 L640,350 L592,350 C588,336 588,316 590,300 Z",
       "Dog ear", fill=DOG_GRAD, stroke=INK, strokeWidth=3.5)
# sheet edge shading + top light
d.path("M612,360 L612,648 C612,656 606,660 596,660 L600,360 Z",
       "Sheet shade R", fill="#B49B70", opacity=35, stroke=NONE)
d.path("M368,312 L632,312", "Sheet top light",
       fill=NONE, stroke="#FFF9E8", strokeWidth=3, opacity=55, cap="round")

# text lines on the sheet — generic rule-lines, then the readable directives
for j, yy in enumerate((478, 502, 526, 550, 598, 622)):
    d.path(f"M392,{yy} L{604 if j % 2 else 580},{yy}", f"Rule line {j+1}",
           fill=NONE, stroke="#8A7A5C", strokeWidth=6, opacity=38,
           cap="round")
# directive lines on soft phosphor bands
d.shape("rectangle", "Directive band 1", x=388, y=402, width=224, height=30,
        radius=6, fill=PHOSPHOR, opacity=22, stroke=NONE)
d.text("User-agent: *", "Directive UA", x=398, y=424, size=17,
       font="Source Sans 3", color="#4A5A3E")
d.shape("rectangle", "Directive band 2", x=388, y=438, width=224, height=30,
        radius=6, fill=PHOSPHOR, opacity=30, stroke=NONE)
d.text("Disallow: /", "Directive Disallow", x=398, y=460, size=17,
       font="Source Sans 3", color="#3E4E34")

# unbothered face, upper third of the sheet
d.path("M430,356 C444,348 462,348 474,356", "Eye L",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M526,356 C540,348 558,348 570,356", "Eye R",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M478,384 L522,384", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")

# left arm resting on the knee
d.path("M366,520 C340,560 338,610 356,642 C368,650 382,644 384,632 "
       "C372,600 374,562 386,534 Z",
       "Arm L", fill=PAPER_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand L", x=348, y=632, width=30, height=24,
        fill="#E4D5B0", stroke=INK, strokeWidth=3)
# right arm raised, palm out toward the crawlers — the halt
d.path("M634,470 C668,478 696,500 712,530 C716,544 706,556 692,552 "
       "C676,528 654,512 632,506 Z",
       "Arm R", fill=PAPER_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Palm", x=690, y=516, width=34, height=40,
        fill="#E4D5B0", stroke=INK, strokeWidth=3.5)
for j, (dx, fx) in enumerate(((-9, -15), (0, 0), (9, 15))):
    d.path(f"M{707 + dx},521 L{707 + dx + fx * 0.4:.0f},539",
           f"Finger {j+1}", fill=NONE, stroke=INK, strokeWidth=2.5,
           cap="round")

# --- two halted spider crawlers -----------------------------------------------------
def crawler(cx, cy, label, flip=1, lit=True):
    # legs: four thin strokes arcing off the dome
    for j, (dx, dy) in enumerate([(-26, 6), (-18, 22), (18, 22), (26, 6)]):
        d.path(f"M{cx + dx * 0.4:.0f},{cy + 2} L{cx + dx:.0f},{cy + dy}",
               f"{label} leg {j+1}", fill=NONE, stroke=INK, strokeWidth=3,
               cap="round")
    d.shape("ellipse", f"{label} shadow", x=cx - 30, y=cy + 26,
            width=60, height=12, fill="#08100B", opacity=35, stroke=NONE)
    d.path(f"M{cx - 24},{cy + 14} C{cx - 24},{cy - 14} {cx + 24},{cy - 14} "
           f"{cx + 24},{cy + 14} Z",
           f"{label} dome", fill=BOT_GRAD, stroke=INK, strokeWidth=3.5)
    # the one lit eye, facing the file
    ex = cx - 10 * flip
    d.shape("ellipse", f"{label} eye glow", x=ex - 9, y=cy - 4, width=18,
            height=18, fill="#F0913A", opacity=30 if lit else 12, stroke=NONE)
    d.shape("ellipse", f"{label} eye", x=ex - 4, y=cy + 1, width=9,
            height=9, fill="#F6B84E" if lit else "#8A7A56", stroke=NONE)
    # little antenna
    d.path(f"M{cx + 12 * flip},{cy - 12} L{cx + 18 * flip},{cy - 26}",
           f"{label} antenna", fill=NONE, stroke=INK, strokeWidth=2.5,
           cap="round")
    d.shape("ellipse", f"{label} antenna tip", x=cx + 16 * flip - 3,
            y=cy - 30, width=6, height=6, fill="#F6B84E", opacity=80,
            stroke=NONE)

crawler(770, 700, "Crawler near", flip=1)
crawler(660, 770, "Crawler far", flip=1, lit=False)

# --- name + role ----------------------------------------------------------------------
d.text("ROBOTS DOT TXT", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#DEEED8", justify="center")
r = d.text("CRAWL DENIAL CRYPTID", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9CC9A2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("042.robots-dot-txt-V1R00")
