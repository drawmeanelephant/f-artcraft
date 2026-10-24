#!/usr/bin/env python3
"""Slidey the Deckworm — mascot portrait V1R00.
A worm burrowing through a presentation slide marked SLIDE 7; stacked
charts and vague arrows nearby. He is never not on Slide 7.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Slidey the Deckworm — Mascot Portrait", 1000, 1000)

INK = "#33222C"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#101626"}, {"offset": 1, "color": "#05070E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E5070"}, {"offset": 0.7, "color": "#283A55"},
    {"offset": 1, "color": "#141E30"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "start": [0, 700], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#2A3A55"}, {"offset": 1, "color": "#121A28"}]}}
SLIDE_GRAD = {"gradient": {"kind": "linear", "start": [0, 200], "end": [0, 640], "stops": [
    {"offset": 0, "color": "#F2EFE6"}, {"offset": 1, "color": "#CFC9B8"}]}}
HEADBAND = {"gradient": {"kind": "linear", "start": [0, 200], "end": [0, 270], "stops": [
    {"offset": 0, "color": "#5A6E94"}, {"offset": 1, "color": "#3A4A6E"}]}}
WORM_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2A8B8"}, {"offset": 0.7, "color": "#DE7E96"},
    {"offset": 1, "color": "#B45A72"}]}}
ARROW = "#E0705E"
BAR_A, BAR_B, BAR_C = "#5E789E", "#8FA8C8", "#C8B46A"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E789E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D4EC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,240,8),(800,232,7),(160,520,9),(832,545,8),
                               (246,764,7),(754,748,9),(134,392,6),(862,392,7),
                               (392,114,7),(612,112,8),(334,822,6),(664,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A4E72", opacity=45, stroke=NONE)

# --- floor of the boardroom, closed on the disc's arc ----------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E1624",
       strokeWidth=4, opacity=60)
# easel legs under the slide
d.path("M400,640 L360,700 M600,640 L640,700", "Easel legs", fill=NONE,
       stroke="#241E2C", strokeWidth=8, cap="round")

# --- the slide -------------------------------------------------------------------
d.shape("ellipse", "Slide shadow", x=280, y=664, width=440, height=28,
        fill="#0A1220", opacity=50, stroke=NONE)
d.shape("rectangle", "Slide", x=250, y=200, width=500, height=440,
        fill=SLIDE_GRAD, stroke=INK, strokeWidth=6, radius=10)
# header band + title
d.path("M250,210 Q250,200 260,200 L740,200 Q750,200 750,210 L750,272 L250,272 Z",
       "Header band", fill=HEADBAND, stroke=INK, strokeWidth=5)
d.text("SLIDE 7", "Slide title", x=276, y=252, size=38, font="Virelai Sans",
       color="#F0ECDE", justify="left")
d.shape("rectangle", "Draft pill", x=646, y=222, width=76, height=32,
        fill="#2E3C58", stroke="#8FA0C4", strokeWidth=2, radius=15)
d.text("DRAFT", "Draft text", x=684, y=245, size=15, font="Virelai Sans",
       color="#B9C4DC", justify="center")
# bullet stubs, deliberately vague
for i, w in enumerate([(0,150),(0,120),(0,170)]):
    d.shape("ellipse", f"Bullet dot {i+1}", x=272, y=304+i*32, width=9,
            height=9, fill="#8A94AC", stroke=NONE)
    d.shape("rectangle", f"Bullet line {i+1}", x=290, y=301+i*32, width=w[1],
            height=12, fill="#9AA2B4", opacity=70, stroke=NONE, radius=5)
# stacked bar chart, lower-left quadrant
d.path("M270,590 L270,430 M270,590 L460,590", "Chart axes", fill=NONE,
       stroke="#5A6478", strokeWidth=4)
for i, (x, segs) in enumerate([(292,(40,30,22)),(334,(58,24,30)),(376,(34,42,18)),(418,(66,20,26))]):
    y = 590
    for j, (h, c) in enumerate(zip(segs, (BAR_A, BAR_B, BAR_C))):
        y -= h
        d.shape("rectangle", f"Bar {i+1}.{j+1}", x=x, y=y, width=32, height=h,
                fill=c, stroke=INK, strokeWidth=2, opacity=90)
# a vague arrow: dashed sweep curling over the chart, pointing nowhere decisive
d.path("M300,400 C420,330 560,330 660,390", "Vague arrow shaft", fill=NONE,
       stroke=ARROW, strokeWidth=7, dash=[14,10], cap="round", opacity=85)
d.path("M644,364 L674,398 L628,398 Z", "Vague arrow head", fill=ARROW,
       stroke=INK, strokeWidth=3, join="round", opacity=90)
d.text("synergy?", "Arrow tag", x=560, y=330, size=15, font="Virelai Sans",
       color=ARROW, justify="left")
# a second vague arrow pointing back into itself
d.path("M690,470 C720,440 720,410 692,398", "Vague arrow 2", fill=NONE,
       stroke=BAR_B, strokeWidth=6, dash=[10,9], cap="round", opacity=70)
d.path("M676,410 L700,398 L694,424 Z", "Vague arrow 2 head", fill=BAR_B,
       stroke=INK, strokeWidth=3, join="round", opacity=80)
# orphaned KPI chip
d.shape("rectangle", "KPI chip", x=620, y=540, width=96, height=44,
        fill="#E4DECC", stroke=INK, strokeWidth=4, radius=8)
d.text("KPI ↑?", "KPI text", x=636, y=570, size=20, font="Virelai Sans",
       color="#6A5E44", justify="left")

# --- burrow hole A (entry), over the bars -----------------------------------------
d.shape("ellipse", "Hole A", x=338, y=520, width=74, height=56,
        fill="#1A1218", stroke=INK, strokeWidth=4)
# torn slide flaps around the hole
for i, (x1, y1, x2, y2, x3, y3) in enumerate([(342,528,356,514,362,534),
                                             (392,522,404,514,398,538),
                                             (344,566,332,578,358,570)]):
    d.path(f"M{x1},{y1} L{x2},{y2} L{x3},{y3} Z", f"Torn flap A{i+1}",
           fill="#D8D2C0", stroke=INK, strokeWidth=3, join="round")
# cracks
d.path("M336,540 L310,534 M400,556 L424,568", "Cracks A", fill=NONE,
       stroke="#8A8270", strokeWidth=3, opacity=80, cap="round")

# --- Slidey's tail arc, crawling over the slide into hole A ------------------------
# segments laid along a curve from lower-left up to the hole
tail = [(238,608,26),(252,584,24),(268,562,22),(288,548,20),(310,544,18)]
for i, (x, y, r) in enumerate(tail):
    d.shape("ellipse", f"Tail seg {i+1}", x=x-r, y=y-r, width=r*2, height=r*2,
            fill=WORM_GRAD, stroke=INK, strokeWidth=4)
# segment grooves
for i, (x, y, r) in enumerate(tail[1:]):
    d.path(f"M{x-r*0.6},{y-r*0.5} Q{x},{y} {x-r*0.55},{y+r*0.55}",
           f"Tail groove {i+1}", fill=NONE, stroke="#9E4E62", strokeWidth=3,
           opacity=70, cap="round")
# tail tip nub
d.shape("ellipse", "Tail tip", x=224, y=612, width=18, height=14,
        fill="#DE7E96", stroke=INK, strokeWidth=3)

# --- burrow hole B (exit), right-center ---------------------------------------------
d.shape("ellipse", "Hole B", x=560, y=400, width=86, height=64,
        fill="#1A1218", stroke=INK, strokeWidth=4)
for i, (x1, y1, x2, y2, x3, y3) in enumerate([(566,412,582,398,588,420),
                                             (630,404,642,396,638,424),
                                             (566,452,552,462,578,458)]):
    d.path(f"M{x1},{y1} L{x2},{y2} L{x3},{y3} Z", f"Torn flap B{i+1}",
           fill="#D8D2C0", stroke=INK, strokeWidth=3, join="round")
d.path("M560,414 L534,406 M648,442 L672,452", "Cracks B", fill=NONE,
       stroke="#8A8270", strokeWidth=3, opacity=80, cap="round")

# --- Slidey's head + shoulders, leaning out of hole B -------------------------------
# neck segments emerging, angled up-right
d.shape("ellipse", "Neck seg 1", x=576, y=396, width=58, height=50,
        fill=WORM_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Neck seg 2", x=610, y=370, width=62, height=54,
        fill=WORM_GRAD, stroke=INK, strokeWidth=4)
d.path("M620,404 Q634,392 648,398", "Neck groove", fill=NONE,
       stroke="#9E4E62", strokeWidth=3, opacity=70, cap="round")
# head: a happy grub peering out
d.shape("ellipse", "Head", x=644, y=330, width=96, height=88,
        fill=WORM_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Head hi", x=662, y=344, width=40, height=20,
        fill="#FFFFFF", opacity=30, stroke=NONE)
# cheerful vacant eyes
d.shape("ellipse", "Eye L", x=666, y=362, width=20, height=26,
        fill="#FDF4EE", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=672, y=372, width=8, height=10,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=700, y=358, width=20, height=26,
        fill="#FDF4EE", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil R", x=706, y=368, width=8, height=10,
        fill=INK, stroke=NONE)
# open munching grin
d.path("M672,398 C684,410 706,410 716,396 C710,416 678,416 672,398 Z",
       "Grin", fill="#8E3244", stroke=INK, strokeWidth=3, join="round")
# cheek bits of eaten slide
d.shape("ellipse", "Crumb 1", x=726, y=392, width=10, height=8,
        fill="#D8D2C0", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Crumb 2", x=738, y=408, width=7, height=6,
        fill="#D8D2C0", stroke=INK, strokeWidth=2)
# whoosh marks — the retreat noise
d.path("M742,346 C756,340 766,342 774,350", "Whoosh 1", fill=NONE,
       stroke="#9FB4D8", strokeWidth=4, cap="round", opacity=70)
d.path("M748,378 C760,374 768,376 774,382", "Whoosh 2", fill=NONE,
       stroke="#9FB4D8", strokeWidth=4, cap="round", opacity=55)

# slide dust puffing from both holes
for i, (x, y, w) in enumerate([(414,512,14),(316,580,10),(644,468,12),(566,392,10)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#E4DECC", opacity=55, stroke=NONE)

# --- captions -------------------------------------------------------------------
d.text("SLIDEY THE DECKWORM", "Name", x=500, y=930, size=54, font="Virelai Sans",
       color="#C8D4EC", justify="center")
r = d.text("RESIDENT OF SLIDE 7", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#93A8CC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("222.slidey-deckworm-V1R00")
