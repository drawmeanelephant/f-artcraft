#!/usr/bin/env python3
"""Annex Lurker — mascot portrait V1R00.
The Lurker at the threshold between lit and unlit shelving, broom
extended into the dark side, sweeping loose papers in one direction:
in, never back out. The annex is one level dimmer than the main
text, never dark — what it hides, it keeps. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Annex Lurker — Mascot Portrait", 1000, 1000)

INK = "#33262E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#221C30"}, {"offset": 1, "color": "#0C0914"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5C5268"}, {"offset": 0.7, "color": "#3B3350"},
    {"offset": 1, "color": "#1B1629"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#433A55"}, {"offset": 1, "color": "#171126"}]}}
CLOAK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E3450"}, {"offset": 1, "color": "#1C1528"}]}}
SHELF_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A4638"}, {"offset": 1, "color": "#392A22"}]}}
PAPER = "#E4DCC4"
DARK = "#0E0A18"
WARM = "#E8C878"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A6F92", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D6CFE6", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(206,238,7),(806,240,8),(164,530,8),(838,552,7),
                               (262,764,8),(744,752,7),(142,398,6),(856,402,7),
                               (404,118,7),(606,116,8),(340,822,6),(668,818,7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#453C5E", opacity=45, stroke=NONE)

# --- the two halves: lit main text / annex dark --------------------------------
# warm light shaft falling from upper left, kept inside the disc
d.path("M282,112 L522,112 L386,700 L206,700 Z", "Light shaft",
       fill=WARM, opacity=10, stroke=NONE)
# the annex side: right region of the disc carried one level dimmer, never black
d.path("M560,44 L640,856 A420,420 0 0 0 560,44 Z", "Annex dark",
       fill=DARK, opacity=58, stroke=NONE)
# faint shelf uprights inside the dark side — shelving that is there, barely
for i, (x, w) in enumerate([(668, 34), (782, 30)]):
    d.shape("rectangle", f"Dark shelf upright {i+1}", x=x, y=200, width=w,
            height=480, fill="#1A1426", opacity=85, stroke=NONE)
for i, y in enumerate([286, 402, 518, 634]):
    d.shape("rectangle", f"Dark shelf board {i+1}", x=650, y=y, width=210,
            height=12, fill="#201A30", opacity=80, stroke=NONE)
# dim spines of kept papers on the dark shelves
for i, (x, y, w, h) in enumerate([(676,240,18,44),(700,232,14,52),(800,356,16,44),
                                  (824,350,20,50),(680,470,16,46),(704,478,12,38),
                                  (806,590,18,42),(830,596,14,36)]):
    d.shape("rectangle", f"Kept spine {i+1}", x=x, y=y, width=w, height=h,
            fill="#2C2440", opacity=70, stroke=NONE)

# --- lit shelf on the main-text side -------------------------------------------
d.shape("rectangle", "Shelf post", x=196, y=200, width=34, height=500,
        fill=SHELF_GRAD, stroke=INK, strokeWidth=4)
for i, y in enumerate([316, 436, 556, 676]):
    d.shape("rectangle", f"Shelf board {i+1}", x=196, y=y, width=142,
            height=14, fill=SHELF_GRAD, stroke=INK, strokeWidth=4)
# tidy stacks on the lit shelves — the main document, in order
for i, (x, y, w, h, c) in enumerate([(244,272,16,42,"#6B5A48"),(266,278,14,36,"#7A6850"),(286,266,18,48,"#5E4E42"),
                                     (244,392,20,42,"#71604C"),(270,398,14,36,"#5E4E42"),(292,388,16,46,"#7A6850"),
                                     (248,516,16,38,"#655444"),(272,510,20,44,"#71604C"),(300,522,12,32,"#5E4E42")]):
    d.shape("rectangle", f"File spine {i+1}", x=x, y=y, width=w, height=h,
            fill=c, stroke=INK, strokeWidth=3)
# the Lurker's tally: it keeps a count of what it holds — scratched on the post
for i in range(4):
    d.path(f"M{206 + i*6},640 L{204 + i*6},664", f"Tally {i+1}",
           fill=NONE, stroke="#C9B68A", strokeWidth=3, cap="round", opacity=75)
d.path("M202,664 L222,638", "Tally strike", fill=NONE,
       stroke="#C9B68A", strokeWidth=3, cap="round", opacity=75)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0814",
       strokeWidth=4, opacity=70)

# --- loose papers, swept one way: lit side to the dark ---------------------------
for i, (cx, cy, deg, op) in enumerate([
        (296,712,-8,95),(354,728,6,95),(418,742,-4,90),(480,722,10,88),
        (552,734,-6,80),(624,716,8,66),(690,730,-10,48),(748,720,5,30),
        (790,730,-4,16)]):
    d.path(rot_rect_path(cx, cy, 46, 30, deg), f"Floor paper {i+1}",
           fill=PAPER, stroke=INK, strokeWidth=3, opacity=op)
# dust edge on the side that faced the main text
d.path("M300,702 L300,724 M358,716 L358,738", "Dust edges", fill=NONE,
       stroke="#F4EDD8", strokeWidth=3, cap="round", opacity=60)
# two slips still mid-fall, already past the threshold
d.path(rot_rect_path(660, 586, 24, 44, 28), "Falling paper 1",
       fill=PAPER, stroke=INK, strokeWidth=3, opacity=42)
d.path(rot_rect_path(724, 630, 18, 42, 26), "Falling paper 2",
       fill=PAPER, stroke=INK, strokeWidth=3, opacity=26)

# --- the Lurker ------------------------------------------------------------------
d.shape("ellipse", "Lurker shadow", x=400, y=700, width=210, height=26,
        fill="#060410", opacity=50, stroke=NONE)
# cloak: hunched back rising from the hem, hood bowed toward the dark
d.path("M418,706 C400,620 404,540 432,500 C452,470 472,446 504,440 "
       "C536,442 558,462 564,494 C572,540 576,620 580,706 Z",
       "Cloak", fill=CLOAK_GRAD, stroke=INK, strokeWidth=6, join="round")
# rim light down the lit side — it waits at the threshold, not in the dark
d.path("M420,700 C404,616 408,544 434,502 C452,474 470,452 498,445",
       "Rim light", fill=NONE, stroke="#C9AE7C", strokeWidth=5,
       cap="round", opacity=60)
# hood opening, facing right into the annex
d.path("M524,478 C544,468 562,480 565,500 C553,514 534,514 523,500 Z",
       "Hood opening", fill="#100C1C", stroke=NONE)
d.shape("ellipse", "Eye glint", x=547, y=491, width=7, height=5,
        fill="#D8CEB0", opacity=85, stroke=NONE)
# sleeve reaching in after the papers
d.path("M540,556 C570,558 596,580 618,606 L600,624 C576,606 552,592 530,590 Z",
       "Sleeve", fill="#4A3E5C", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Hand", x=606, y=608, width=18, height=13,
        fill="#2A2138", stroke=INK, strokeWidth=3)
# broom: lit shaft, then the working end already inside the dark
d.path("M606,602 L668,664", "Broom shaft lit", fill=NONE,
       stroke="#6B5236", strokeWidth=7, cap="round")
d.path("M668,664 L726,722", "Broom shaft dim", fill=NONE,
       stroke="#6B5236", strokeWidth=7, cap="round", opacity=45)
d.path("M714,706 L762,752 L744,770 L698,724 Z", "Broom bristles",
       fill="#4A3828", stroke=INK, strokeWidth=3, opacity=50, join="round")
# sweep wake: a soft push of shadow where the bristles work
d.shape("ellipse", "Sweep wake", x=700, y=716, width=120, height=40,
        fill=DARK, opacity=40, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("ANNEX LURKER", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E4DEF2", justify="center")
r = d.text("CERTIFIER OF DEFERRED REALITY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A89ECB", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("239.annex-lurker-V1R00")
