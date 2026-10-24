#!/usr/bin/env python3
"""Minute Absolution — mascot portrait V1R00.
The secretary at its lectern: both palms press the stenographer's pad while
three jagged hours of shouting are squeezed through its hands into a single
tidy paragraph; the binder clip is already shut. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Minute Absolution — Mascot Portrait", 1000, 1000)

INK = "#33241C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#181208"}, {"offset": 1, "color": "#0A0704"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#54453A"}, {"offset": 0.7, "color": "#2E241C"},
    {"offset": 1, "color": "#151009"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#33261E"}, {"offset": 1, "color": "#141009"}]}}
SUIT = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E7A6E"}, {"offset": 0.7, "color": "#3E564A"},
    {"offset": 1, "color": "#24352C"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0DEC8"}, {"offset": 0.7, "color": "#D4BC9C"},
    {"offset": 1, "color": "#AC8F6E"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDE0C8"}, {"offset": 1, "color": "#C4B192"}]}}
DESK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A4130"}, {"offset": 1, "color": "#2C1E16"}]}}
SHOUT = "#8A3E34"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A08872", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2D2B8", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#483C30", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E0A06",
       strokeWidth=4, opacity=70)

# --- three jagged hours of shouting, descending --------------------------------------
# each bolt is a zigzag pressed toward the pad, converging on the clip
d.path("M388,215 L420,255 L398,275 L436,315 L414,335 L452,375 L434,396 L458,430",
       "Shout bolt 1", fill=NONE, stroke=SHOUT, strokeWidth=6,
       cap="round", join="round", opacity=85)
d.path("M500,205 L484,250 L514,272 L488,312 L516,334 L492,374 L512,398 L500,428",
       "Shout bolt 2", fill=NONE, stroke=SHOUT, strokeWidth=6,
       cap="round", join="round", opacity=85)
d.path("M612,218 L580,258 L602,278 L564,318 L586,338 L548,376 L566,396 L542,430",
       "Shout bolt 3", fill=NONE, stroke=SHOUT, strokeWidth=6,
       cap="round", join="round", opacity=85)
# sound marks above the bolts
for i, (x, y, a) in enumerate([(430,195,-20),(500,185,0),(572,198,20)]):
    for j in (-1, 1):
        x0 = x + j*18; y0 = y - 22
        d.path(rot_rect_path(x0, y0, 26, 4, a + j*25), f"Sound mark {i+1}-{j}",
               fill=SHOUT, opacity=70, stroke=NONE)
# --- the secretary's body (behind the desk) --------------------------------------------
d.shape("ellipse", "Body shadow", x=380, y=660, width=240, height=26,
        fill="#080606", opacity=50, stroke=NONE)
d.path("M500,395 C580,395 620,455 622,540 C624,605 610,655 600,690 "
       "L400,690 C390,655 376,605 378,540 C380,455 420,395 500,395 Z",
       "Body", fill=SUIT, stroke=INK, strokeWidth=6)
# shirt front
d.path("M478,420 C478,470 480,540 486,610 L514,610 C520,540 522,470 522,420 Z",
       "Shirt front", fill="#C9C4B2", stroke=INK, strokeWidth=3, opacity=95)
d.path("M486,430 L514,430 M484,470 L516,470 M486,510 L514,510",
       "Shirt buttons", fill=NONE, stroke="#8A8472", strokeWidth=2,
       opacity=70)
# collar points
d.path("M478,398 L500,428 L522,398", "Collar", fill=NONE, stroke=INK,
       strokeWidth=5, join="round", cap="round")

# --- head --------------------------------------------------------------------------------
d.shape("ellipse", "Head", x=425, y=250, width=150, height=140,
        fill=SKIN, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Head sheen", x=450, y=262, width=60, height=26,
        fill="#FFFFFF", opacity=20, stroke=NONE)
# the green eyeshade of the conscientious recorder
d.path("M438,318 C460,300 540,300 562,318 L560,332 C538,316 462,316 440,332 Z",
       "Eyeshade", fill="#2E5E4A", stroke=INK, strokeWidth=3, opacity=95)
# glasses beneath the shade: two rims and a bridge
d.shape("ellipse", "Lens L", x=447, y=330, width=44, height=40,
        fill="#FFFFFF", opacity=18, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Lens R", x=509, y=330, width=44, height=40,
        fill="#FFFFFF", opacity=18, stroke=INK, strokeWidth=4)
d.path("M491,344 L509,344", "Bridge", fill=NONE, stroke=INK, strokeWidth=4,
       cap="round")
# eyes: flat, fixed on the pad
d.path("M456,350 L480,350", "Eye L", fill=NONE, stroke="#241812",
       strokeWidth=5, cap="round")
d.path("M520,350 L544,350", "Eye R", fill=NONE, stroke="#241812",
       strokeWidth=5, cap="round")
# flat professional mouth
d.path("M478,368 L522,368", "Mouth", fill=NONE, stroke=INK, strokeWidth=4,
       cap="round")

# --- the desk --------------------------------------------------------------------------------
d.shape("ellipse", "Desk shadow", x=300, y=676, width=400, height=24,
        fill="#080606", opacity=50, stroke=NONE)
d.shape("rectangle", "Desk front", x=316, y=600, width=368, height=26,
        fill=DESK, stroke=INK, strokeWidth=5, radius=6)
d.shape("rectangle", "Leg L", x=344, y=624, width=20, height=76,
        fill=DESK, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Leg R", x=636, y=624, width=20, height=76,
        fill=DESK, stroke=INK, strokeWidth=4)

# --- the stenographer's pad, pressed flat on the desk -----------------------------------------
# slightly perspective parallelogram lying on the desk top
d.path("M398,540 L602,540 L626,600 L374,600 Z", "Pad", fill=PAPER,
       stroke=INK, strokeWidth=5, join="round")
# spiral binding at the top edge
for i, x in enumerate(range(416, 600, 26)):
    d.shape("ellipse", f"Ring {i+1}", x=x, y=533, width=10, height=12,
            fill=NONE, stroke=INK, strokeWidth=2.5)
# ruled margins
d.path("M410,560 L610,560 M404,585 L616,585", "Rules", fill=NONE,
       stroke="#B09A76", strokeWidth=2, opacity=70)
# the single paragraph: tidy compressed lines in the middle
d.path("M428,568 L560,568 M426,575 L566,575 M432,582 L554,582",
       "Paragraph", fill=NONE, stroke="#4A3A30", strokeWidth=3.5,
       cap="round")
# the binder clip on the pad's top edge
d.shape("rectangle", "Clip body", x=486, y=528, width=28, height=18,
        fill="#2A2A30", stroke=INK, strokeWidth=3, radius=4)
d.path("M490,528 C490,518 510,518 510,528", "Clip wire", fill=NONE,
       stroke="#6E6E78", strokeWidth=3, cap="round")

# --- arms pressing the pad ----------------------------------------------------------------------
d.path("M412,470 C398,505 408,535 435,552", "Arm L", fill=NONE,
       stroke=INK, strokeWidth=16, cap="round")
d.path("M588,470 C602,505 592,535 565,552", "Arm R", fill=NONE,
       stroke=INK, strokeWidth=16, cap="round")
d.shape("ellipse", "Hand L", x=418, y=540, width=34, height=22,
        fill=SKIN, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=548, y=540, width=34, height=22,
        fill=SKIN, stroke=INK, strokeWidth=4)
# pressure marks around the hands
d.path("M410,562 L394,575 M425,568 L412,584", "Press marks L", fill=NONE,
       stroke="#8A6A4C", strokeWidth=4, cap="round", opacity=80)
d.path("M590,562 L606,575 M575,568 L588,584", "Press marks R", fill=NONE,
       stroke="#8A6A4C", strokeWidth=4, cap="round", opacity=80)

# --- the bolts squeezed thin, drawn through the hands into the pad's top edge -------------
d.path("M458,430 C448,468 440,505 448,542", "Bolt 1 squeezed", fill=NONE,
       stroke=SHOUT, strokeWidth=3.5, cap="round", opacity=75)
d.path("M500,428 C506,460 503,500 500,536", "Bolt 2 squeezed", fill=NONE,
       stroke=SHOUT, strokeWidth=3.5, cap="round", opacity=75)
d.path("M542,430 C552,468 560,505 552,542", "Bolt 3 squeezed", fill=NONE,
       stroke=SHOUT, strokeWidth=3.5, cap="round", opacity=75)

# --- captions -------------------------------------------------------------------------
d.text("MINUTE ABSOLUTION", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F0E2C8", justify="center")
r = d.text("CERTIFIES THE TIDY, NEVER THE TRUE", "Role", x=500, y=968,
           size=23, font="Virelai Sans", color="#C8AA8C", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("297.minute-absolution-V1R00")
