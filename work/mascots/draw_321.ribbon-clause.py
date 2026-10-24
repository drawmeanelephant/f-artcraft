#!/usr/bin/env python3
"""Ribbon Clause — mascot portrait V1R00.
A contract document tied in a silk ribbon bow, calligraphy lettering
visible beneath: the knot is purely aesthetic, the obligation is real.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Ribbon Clause — Mascot Portrait", 1000, 1000)

INK = "#1E1A24"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0C1218"}, {"offset": 1, "color": "#05080C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#46586E"}, {"offset": 0.7, "color": "#2C3A4C"},
    {"offset": 1, "color": "#141C26"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E3440"}, {"offset": 1, "color": "#12161C"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2E8D0"}, {"offset": 1, "color": "#D2C29E"}]}}
BACK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8CAA8"}, {"offset": 1, "color": "#A89472"}]}}
RIBBON_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D4566A"}, {"offset": 1, "color": "#8A2438"}]}}
RIBBON_DARK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A2438"}, {"offset": 1, "color": "#521220"}]}}
INKLINE = "#4A4252"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A8EA6", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D6E0EC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#2E3E50", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0E14",
       strokeWidth=4, opacity=70)

# --- the document ------------------------------------------------------------------
d.shape("ellipse", "Doc shadow", x=320, y=682, width=380, height=24,
        fill="#06090E", opacity=50, stroke=NONE)
d.path(rot_rect_path(512, 480, 340, 420, 3), "Back sheet",
       fill=BACK_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Contract page", x=330, y=280, width=340, height=410,
        fill=PAGE_GRAD, stroke=INK, strokeWidth=5)
# header + calligraphy headline
d.text("CONTRACT", "Doc title", x=500, y=326, size=20, font="Virelai Sans",
       color="#5E5238", justify="center")
d.path("M390,344 C430,332 570,332 610,344 C570,352 430,352 390,344 Z",
       "Title flourish", fill=NONE, stroke=INKLINE, strokeWidth=2.5,
       opacity=70)
# calligraphy rows: wavy ink strokes with pressure taper
def hand(y, x1, x2, wob, label, op):
    mid = (x1 + x2) / 2
    d.path(f"M{x1},{y} C{x1+40},{y-wob} {mid-30},{y+wob} {mid},{y} "
           f"C{mid+30},{y-wob} {x2-40},{y+wob} {x2},{y-2}",
           label, fill=NONE, stroke=INKLINE, strokeWidth=3,
           cap="round", opacity=op)
hand(378, 392, 560, 9, "Hand row 1", 85)
hand(404, 392, 610, 8, "Hand row 2", 80)
hand(430, 392, 580, 10, "Hand row 3", 75)
# swash capital at the paragraph start
d.path("M396,378 C382,368 372,380 380,392 C388,402 404,398 402,384 "
       "C400,372 388,368 380,376", "Swash capital", fill=NONE,
       stroke=INKLINE, strokeWidth=4, cap="round", opacity=90)
hand(560, 392, 596, 8, "Hand row 4", 70)
hand(586, 392, 628, 9, "Hand row 5", 65)
hand(616, 392, 560, 8, "Hand row 6", 60)
# signature line + flourish at the foot of the page
d.path("M380,652 L520,652", "Signature rule", fill=NONE, stroke="#8A7A60",
       strokeWidth=2.5, opacity=70)
d.path("M386,642 C420,620 460,664 500,640 C512,632 522,634 530,644",
       "Signature", fill=NONE, stroke=INKLINE, strokeWidth=3.5,
       cap="round", opacity=85)

# --- the silk ribbon: band across, bow at center -------------------------------------
# horizontal band wrapping the page
d.shape("rectangle", "Ribbon band", x=330, y=452, width=340, height=34,
        fill=RIBBON_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M330,458 L670,458", "Band sheen", fill=NONE, stroke="#F0929E",
       strokeWidth=3, opacity=50)
# tails hanging from the knot, past the page edge onto the floor
d.path("M488,484 C470,540 458,610 466,672 L440,690 L430,664 "
       "C420,600 436,536 458,486 Z", "Tail left",
       fill=RIBBON_DARK, stroke=INK, strokeWidth=4, join="round")
d.path("M512,484 C536,534 556,584 566,640 L596,630 L578,676 "
       "C552,660 534,590 504,492 Z", "Tail right",
       fill=RIBBON_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M462,510 C452,560 448,616 452,656", "Tail left sheen", fill=NONE,
       stroke="#E87A8A", strokeWidth=3, cap="round", opacity=45)
# bow loops
d.path("M496,468 C462,424 408,424 400,458 C394,486 428,502 462,494 "
       "C480,489 492,480 496,468 Z", "Loop left",
       fill=RIBBON_GRAD, stroke=INK, strokeWidth=4, join="round")
d.path("M504,468 C538,424 592,424 600,458 C606,486 572,502 538,494 "
       "C520,489 508,480 504,468 Z", "Loop right",
       fill=RIBBON_GRAD, stroke=INK, strokeWidth=4, join="round")
# loop inner folds
d.path("M480,470 C456,448 428,448 422,462 C418,474 436,484 460,482",
       "Loop left fold", fill=NONE, stroke="#6E1A2C", strokeWidth=3,
       cap="round", opacity=80)
d.path("M520,470 C544,448 572,448 578,462 C582,474 564,484 540,482",
       "Loop right fold", fill=NONE, stroke="#6E1A2C", strokeWidth=3,
       cap="round", opacity=80)
# knot
d.path(rot_rect_path(500, 470, 38, 30, -4), "Knot", fill=RIBBON_DARK,
       stroke=INK, strokeWidth=4)
d.path("M484,462 L492,478 M516,462 L508,478", "Knot creases", fill=NONE,
       stroke="#3E0C18", strokeWidth=2.5, cap="round", opacity=70)

# --- an ink pot and quill at the page's foot ------------------------------------------
d.shape("ellipse", "Ink pot shadow", x=688, y=668, width=86, height=14,
        fill="#06090E", opacity=45, stroke=NONE)
d.path("M700,620 L748,620 L756,668 L692,668 Z", "Ink pot",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#3A4454"}, {"offset": 1, "color": "#161C26"}]}},
       stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Ink mouth", x=702, y=612, width=44, height=16,
        fill="#0C1016", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Ink sheen", x=706, y=632, width=14, height=26,
        fill="#8A9AB0", opacity=25, stroke=NONE)
# quill leaning on the pot: wide vane, shaft, barbs
d.path("M726,614 C700,542 662,498 614,470 C652,478 682,506 704,548 "
       "C716,572 722,594 726,614 Z",
       "Quill feather", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#E8E0D0"}, {"offset": 1, "color": "#A89C84"}]}},
       stroke=INK, strokeWidth=3, join="round")
d.path("M726,614 C700,542 662,498 614,470 C604,478 606,494 620,502 "
       "C652,518 686,556 706,610 Z",
       "Quill vane low", fill="#C8BCA0", stroke=INK, strokeWidth=3,
       join="round", opacity=95)
d.path("M720,608 C692,544 658,506 622,480", "Quill shaft", fill=NONE,
       stroke="#8A8070", strokeWidth=2.5, cap="round", opacity=80)
for i, t in enumerate([(0.22, 1), (0.4, 1), (0.58, 1)]):
    sx, sy = 720 - t[0]*96, 608 - t[0]*126
    d.path(f"M{sx:.0f},{sy:.0f} L{sx-17:.0f},{sy+5:.0f}", f"Barb {i+1}",
           fill=NONE, stroke="#8A8070", strokeWidth=2, cap="round",
           opacity=55)
d.path("M706,616 C714,624 720,634 722,644 L712,642 C710,632 706,622 700,616 Z",
       "Quill nib", fill="#C8BCA0", stroke=INK, strokeWidth=3, join="round")

# --- captions ----------------------------------------------------------------------
d.text("RIBBON CLAUSE", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#D6E0EC", justify="center")
r = d.text("THE KNOT IS PURELY AESTHETIC", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#96A8BE", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("321.ribbon-clause-V1R00")
