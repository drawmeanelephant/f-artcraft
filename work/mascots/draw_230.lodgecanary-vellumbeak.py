#!/usr/bin/env python3
"""Lodgecanary Vellumbeak — mascot portrait V1R00. mascots/M-0230.
Canary with a vellum beak perched in a document annex, feathers falling.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Lodgecanary Vellumbeak — Mascot Portrait", 1000, 1000)

INK = "#2A1F18"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1C1610"}, {"offset": 1, "color": "#0C0806"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8C9A6"}, {"offset": 0.7, "color": "#9A856A"},
    {"offset": 1, "color": "#54463A"}]}}
BIRD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0D264"}, {"offset": 0.7, "color": "#CCA238"},
    {"offset": 1, "color": "#8A6A24"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5E42"}, {"offset": 1, "color": "#4A3826"}]}}
VELLUM = "#F4ECDC"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E4E3E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EDE2C8", strokeWidth=3, opacity=55)
# annex hush — lamp warmth and paper dust
d.shape("ellipse", "Lamp warmth", x=230, y=140, width=320, height=180,
        fill="#F0D8A0", opacity=18, stroke=NONE)
for i, (x, y) in enumerate([(640,200),(700,300),(380,240),(300,480),(740,520)]):
    d.shape("ellipse", f"Dust {i+1}", x=x-3, y=y-3, width=7, height=7,
            fill="#EFE4CC", opacity=30, stroke=NONE)

# --- the annex: a wall of document cubbies, left of the perch ---------------------
d.shape("rectangle", "Shelf unit", x=176, y=196, width=296, height=420,
        radius=8, fill=WOOD_GRAD, stroke=INK, strokeWidth=6)
# cubby dividers: 2 columns x 3 rows
d.shape("rectangle", "Divider V", x=318, y=206, width=12, height=400,
        fill="#3E3020", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Divider H1", x=186, y=328, width=276, height=12,
        fill="#3E3020", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Divider H2", x=186, y=466, width=276, height=12,
        fill="#3E3020", stroke=INK, strokeWidth=3)
# cubby interiors: rolled minutes, stacked testimony, bound volumes
# top-left: scroll rolls lying on their sides
for i, (x, y) in enumerate([(216,268),(264,268),(240,296)]):
    d.shape("ellipse", f"Roll {i+1}", x=x-26, y=y-16, width=52, height=32,
            fill="#E8DCBE", stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Roll core {i+1}", x=x-8, y=y-8, width=16, height=16,
            fill="#C8B88E", stroke=INK, strokeWidth=3)
# top-right: a bound volume with clasp
d.shape("rectangle", "Volume", x=356, y=240, width=88, height=76,
        radius=4, fill="#8A4E3A", stroke=INK, strokeWidth=4)
d.path("M356,268 L444,268", "Volume band", fill=NONE, stroke="#E8DCBE",
       strokeWidth=6, opacity=85)
# mid-left: stacked transcripts, edges fanned
d.path("M200,408 L300,404 L302,424 L202,428 Z", "Stack a",
       fill="#E4D8BC", stroke=INK, strokeWidth=3, join="round")
d.path("M204,388 L296,384 L300,404 L200,408 Z", "Stack b",
       fill="#EDE2C8", stroke=INK, strokeWidth=3, join="round")
d.path("M208,370 L292,366 L296,384 L204,388 Z", "Stack c",
       fill="#E4D8BC", stroke=INK, strokeWidth=3, join="round")
# mid-right: more rolls, one slipping — annex entropy
d.shape("ellipse", "Roll 4", x=360, y=392, width=52, height=32,
        fill="#E8DCBE", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Roll 4 core", x=378, y=400, width=16, height=16,
        fill="#C8B88E", stroke=INK, strokeWidth=3)
d.path("M414,404 L452,428 L444,444 L406,420 Z", "Roll slipping",
       fill="#E4D8BC", stroke=INK, strokeWidth=4, join="round")
# bottom row: sealed bundles tied with cord
for i, x in enumerate([216, 368]):
    d.shape("rectangle", f"Bundle {i+1}", x=x, y=510, width=90, height=84,
            radius=6, fill="#DCCFAE", stroke=INK, strokeWidth=4)
    d.path(f"M{x+45},510 L{x+45},594 M{x},552 L{x+90},552", f"Cord {i+1}",
           fill=NONE, stroke="#8A6E4A", strokeWidth=4, opacity=85)

# --- the perch: observer's rail, jutting right off the shelf ----------------------
d.path("M456,630 L470,646 L470,668 L456,652 Z", "Bracket", fill=WOOD_GRAD,
       stroke=INK, strokeWidth=4, join="round")
d.path("M430,640 C540,632 680,632 780,640", "Perch rod", fill=NONE,
       stroke="#5A4630", strokeWidth=14, cap="round")
d.path("M430,636 C540,628 680,628 780,636", "Perch light", fill=NONE,
       stroke="#8A7050", strokeWidth=4, opacity=70, cap="round")
# the seating-chart tag, hung from the perch — 'observer, annex'
d.path("M706,640 L706,668", "Tag string", fill=NONE, stroke="#3E3020",
       strokeWidth=3, opacity=80)
d.path("M690,668 L722,668 L726,700 L686,700 Z", "Tag", fill="#EDE2C8",
       stroke=INK, strokeWidth=3, join="round")
d.path("M694,680 L716,680 M696,690 L714,690", "Tag rules",
       fill=NONE, stroke="#9A8E74", strokeWidth=3, opacity=85)

# --- the canary: present at everything, singing at nothing -------------------------
d.shape("ellipse", "Bird shadow", x=560, y=630, width=140, height=16,
        fill="#3E3020", opacity=40, stroke=NONE)
# tail, dipped down-right past the perch
d.path("M668,560 C700,584 722,614 730,648 C712,656 686,652 668,636 "
       "C652,622 644,600 646,580 Z", "Tail", fill="#A87E28",
       stroke=INK, strokeWidth=5, join="round")
d.path("M672,586 C692,608 706,628 712,644", "Tail seam",
       fill=NONE, stroke="#6E5220", strokeWidth=4, opacity=60, cap="round")
# body, upright and alert
d.path("M548,626 C528,596 520,556 530,516 C540,478 566,452 600,448 "
       "C638,444 668,470 676,512 C682,546 676,586 656,612 "
       "C634,634 570,644 548,626 Z",
       "Body", fill=BIRD_GRAD, stroke=INK, strokeWidth=6, join="round")
# breast light
d.path("M544,540 C546,578 560,608 586,622 C566,622 548,610 540,588 "
       "C534,570 536,552 544,540 Z", "Breast light", fill="#F4E4A0",
       opacity=55, stroke=NONE)
# folded wing
d.path("M586,500 C628,492 660,512 668,550 C662,586 640,610 608,614 "
       "C596,580 588,540 586,500 Z", "Wing", fill="#B08A30",
       stroke=INK, strokeWidth=5, join="round")
d.path("M600,540 C620,548 644,550 662,544 M604,568 C624,576 644,576 658,570",
       "Wing seams", fill=NONE, stroke="#6E5220", strokeWidth=4,
       opacity=60, cap="round")
# head, crest feathers slightly raised — attending
d.path("M552,478 C538,442 542,404 566,382 C590,360 628,360 650,384 "
       "C656,372 666,364 678,364 C672,378 670,390 672,400 "
       "C676,428 666,458 644,474 C616,494 574,496 552,478 Z",
       "Head", fill=BIRD_GRAD, stroke=INK, strokeWidth=6, join="round")
# the vellum beak — same material as the mandates, shut
d.path("M548,428 L496,442 L544,462 C540,450 540,438 548,428 Z",
       "Beak upper", fill=VELLUM, stroke=INK, strokeWidth=4, join="round")
d.path("M502,444 L540,454", "Beak crease", fill=NONE, stroke="#B0A084",
       strokeWidth=3, opacity=80)
# the eye that does the warning the beak cannot
d.shape("ellipse", "Eye", x=582, y=412, width=18, height=18,
        fill="#241A12", stroke=NONE)
d.shape("ellipse", "Eye glint", x=586, y=414, width=5, height=5,
        fill="#F4E4C0", opacity=90, stroke=NONE)
d.path("M570,398 C580,392 594,392 604,398", "Brow",
       fill=NONE, stroke=INK, strokeWidth=4, opacity=60, cap="round")
# feet gripping the rail
d.path("M578,616 C578,630 576,640 572,646 M574,640 C582,644 590,644 596,640 "
       "M616,618 C616,632 614,642 610,648 M608,642 C616,646 624,646 630,642",
       "Feet", fill=NONE, stroke="#4A3826", strokeWidth=6, cap="round")

# --- feathers, still falling — participation has a cost ----------------------------
d.path("M388,700 C406,684 428,686 440,706 C426,718 402,716 388,706 Z",
       "Feather 1", fill="#D8AC40", stroke=INK, strokeWidth=3, join="round",
       opacity=85)
d.path("M392,702 C408,696 424,698 434,708", "Quill 1", fill=NONE,
       stroke="#8A6A24", strokeWidth=2.5, opacity=70, cap="round")
d.path("M560,752 C542,736 520,738 508,758 C522,770 546,768 560,758 Z",
       "Feather 2", fill="#D8AC40", stroke=INK, strokeWidth=3, join="round",
       opacity=85)
d.path("M556,754 C540,748 524,750 514,760", "Quill 2", fill=NONE,
       stroke="#8A6A24", strokeWidth=2.5, opacity=70, cap="round")
d.path("M668,716 C686,700 708,702 720,722 C706,734 682,732 668,722 Z",
       "Feather 3", fill="#D8AC40", stroke=INK, strokeWidth=3, join="round",
       opacity=85)
d.path("M672,718 C688,712 704,714 714,724", "Quill 3", fill=NONE,
       stroke="#8A6A24", strokeWidth=2.5, opacity=70, cap="round")
d.path("M470,800 C455,788 438,790 428,806 C440,815 460,814 470,806 Z",
       "Feather 4", fill="#D8AC40", stroke=INK, strokeWidth=3, join="round",
       opacity=80)
d.path("M466,802 C452,796 440,798 432,806", "Quill 4", fill=NONE,
       stroke="#8A6A24", strokeWidth=2.5, opacity=70, cap="round")

# --- name + role ------------------------------------------------------------------
d.text("LODGECANARY VELLUMBEAK", "Name", x=500, y=930, size=48,
       font="Virelai Sans", color="#EAE0C6", justify="center")
d.text(" ".join("FILED BEFORE IT WAS SUNG"), "Role", x=500, y=968, size=23,
       font="Virelai Sans", color="#B0A284", justify="center")

d.finish("230.lodgecanary-vellumbeak-V1R00")
