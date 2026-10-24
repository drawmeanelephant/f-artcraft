#!/usr/bin/env python3
"""Triage Tracy — mascot portrait V1R00.
Scrub-clad mascot holding out a DENIED letter, length-of-stay chart
behind her on the wall. 1000x1000. House style: gradients + translucent
shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Triage Tracy — Mascot Portrait", 1000, 1000)

INK = "#332A33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1A18"}, {"offset": 1, "color": "#050D0C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A7A70"}, {"offset": 0.7, "color": "#325550"},
    {"offset": 1, "color": "#1A3230"}]}}
FLOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E4A44"}, {"offset": 1, "color": "#162622"}]}}
BODY = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2D9CE"}, {"offset": 0.7, "color": "#D9AF9E"},
    {"offset": 1, "color": "#B07E72"}]}}
SCRUB = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E8C84"}, {"offset": 1, "color": "#2E5A54"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2EEE2"}, {"offset": 1, "color": "#CFC9B4"}]}}
CHART = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D9D2BC"}, {"offset": 1, "color": "#B4AC90"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6EA298", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CFE8E0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,240,8),(800,230,7),(160,520,9),(830,540,8),
                               (240,760,7),(760,740,9),(130,390,6),(865,390,7),
                               (390,110,7),(610,110,8),(330,820,6),(665,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A605A", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.shape("ellipse", "Floor", x=170, y=620, width=660, height=130,
        fill=FLOOR, stroke=NONE, opacity=92)
d.shape("ellipse", "Tracy shadow", x=440, y=676, width=170, height=30,
        fill="#050C0A", opacity=55, stroke=NONE)

# --- length-of-stay chart on the wall ---------------------------------------------
d.shape("rectangle", "Chart frame", x=212, y=230, width=210, height=170,
        fill="#3A2E22", stroke=INK, strokeWidth=5, radius=6)
d.shape("rectangle", "Chart paper", x=224, y=242, width=186, height=146,
        fill=CHART, stroke=NONE)
d.text("LENGTH OF STAY", "Chart title", x=317, y=264, size=12,
       font="Virelai Sans", color="#4A3F2C", justify="center")
# declining bars
bars = [108, 88, 70, 56, 42]
for i, h in enumerate(bars):
    x = 244 + i*32
    d.shape("rectangle", f"Bar {i+1}", x=x, y=368-h, width=20, height=h,
            fill="#5A8A80" if i < 3 else "#B06A5E", stroke="#3E4A38",
            strokeWidth=2, radius=2)
d.path("M238,370 L400,370", "Chart axis", fill=NONE, stroke="#4A3F2C",
       strokeWidth=3, cap="round")
d.path("M246,290 C290,308 340,334 392,352", "Trend line", fill=NONE,
       stroke="#B04A3E", strokeWidth=4, cap="round", opacity=85)

# --- wall clock: always later ------------------------------------------------------
d.shape("ellipse", "Clock", x=640, y=240, width=72, height=72,
        fill="#E4DFD0", stroke=INK, strokeWidth=5)
d.path("M676,276 L676,254 M676,276 L692,284", "Clock hands", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")

# --- the denial letter, held out -----------------------------------------------------
d.shape("rectangle", "Letter", x=316, y=440, width=118, height=84,
        fill=PAPER, stroke=INK, strokeWidth=4)
d.path("M316,440 L375,486 L434,440", "Envelope fold", fill=NONE,
       stroke="#9A9076", strokeWidth=3, opacity=60)
for i, y in enumerate([506, 514]):
    d.path(f"M328,{y} L422,{y}", f"Letter line {i+1}", fill=NONE,
           stroke="#8A8064", strokeWidth=2, opacity=50)
# red DENIED stamp across it
d.shape("rectangle", "Stamp frame", x=330, y=452, width=90, height=30,
        fill=NONE, stroke="#C04038", strokeWidth=3, radius=4, opacity=90)
d.text("DENIED", "Stamp text", x=375, y=474, size=17, font="Virelai Sans",
       color="#C04038", justify="center")

# --- Tracy -----------------------------------------------------------------------------
# legs + shoes
d.path("M530,646 L526,682", "Leg L", fill=NONE, stroke="#B07E72",
       strokeWidth=13, cap="round")
d.path("M572,646 L576,682", "Leg R", fill=NONE, stroke="#A67468",
       strokeWidth=13, cap="round")
d.shape("ellipse", "Shoe L", x=510, y=676, width=32, height=15, fill=INK, stroke=NONE)
d.shape("ellipse", "Shoe R", x=564, y=676, width=32, height=15, fill=INK, stroke=NONE)
# body in scrubs
d.path("M554,470 C608,470 632,514 629,560 C626,612 596,648 554,648 "
       "C512,648 482,612 479,560 C476,514 500,470 554,470 Z",
       "Tracy body", fill=BODY, stroke=INK, strokeWidth=6)
# scrub top: V-neck tunic over the lower body
d.path("M516,536 C522,596 536,626 554,646 C572,626 586,596 592,536 "
       "C576,548 532,548 516,536 Z",
       "Scrub top", fill=SCRUB, stroke=INK, strokeWidth=4, join="round")
d.path("M516,536 L554,570 L592,536", "V neck", fill=NONE, stroke="#24504A",
       strokeWidth=4, join="round")
d.shape("ellipse", "Body highlight", x=498, y=482, width=66, height=26,
        fill="#FFFFFF", opacity=20, stroke=NONE)
# surgical cap with a little cross
d.path("M516,462 L516,438 C516,420 534,412 554,412 C574,412 592,420 592,438 L592,462 Z",
       "Scrub cap", fill=SCRUB, stroke=INK, strokeWidth=5, join="round")
d.path("M549,428 L559,428 M554,423 L554,433", "Cap cross", fill=NONE,
       stroke="#C04038", strokeWidth=5, cap="round")
# face: flat, paperwork-weary
d.shape("ellipse", "Eye L", x=524, y=498, width=14, height=18, fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=566, y=498, width=14, height=18, fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=528, y=502, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=570, y=502, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M524,484 L540,482", "Brow L", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M566,482 L582,484", "Brow R", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Cheek L", x=510, y=522, width=22, height=13,
        fill="#C98A84", opacity=50, stroke=NONE)
d.shape("ellipse", "Cheek R", x=576, y=522, width=22, height=13,
        fill="#C98A84", opacity=50, stroke=NONE)
d.path("M540,542 L570,542", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# arm presenting the letter
d.path("M496,540 C470,524 452,510 438,498", "Arm letter", fill=NONE,
       stroke="#D9AF9E", strokeWidth=12, cap="round")
d.shape("ellipse", "Hand letter", x=424, y=490, width=18, height=15,
        fill="#F2D9CE", stroke=INK, strokeWidth=3)
# other arm with the stamp hand, just used
d.path("M610,540 C628,552 636,570 632,586", "Arm stamp", fill=NONE,
       stroke="#C99A8C", strokeWidth=12, cap="round")
d.shape("ellipse", "Hand stamp", x=624, y=578, width=18, height=15,
        fill="#F2D9CE", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Rubber stamp", x=616, y=592, width=26, height=20,
        fill="#6E4A38", stroke=INK, strokeWidth=3, radius=3)
d.path("M622,592 L622,584 L636,584 L636,592", "Stamp grip", fill=NONE,
       stroke="#4A3226", strokeWidth=5, cap="round")

# --- captions ---------------------------------------------------------------------------
d.text("TRIAGE TRACY", "Name", x=500, y=930, size=60,
       font="Virelai Sans", color="#D4EAE2", justify="center")
r = d.text("DENIAL LETTER DESK", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#92BCB0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("442.triage-tracy-V1R00")
