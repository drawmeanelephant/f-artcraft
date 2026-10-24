#!/usr/bin/env python3
"""Appendix Silk — mascot portrait V1R00.
A mascot wrapping a data table in lilac silk behind a heavy velvet curtain;
the difficult material preserved in full, set in 9-point type and placed
respectfully at the back of the book. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Appendix Silk — Mascot Portrait", 1000, 1000)

INK = "#2C1E14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1C1424"}, {"offset": 1, "color": "#0A070E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A794B8"}, {"offset": 0.7, "color": "#7D6A92"},
    {"offset": 1, "color": "#4C3E5C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E4258"}, {"offset": 1, "color": "#221A2A"}]}}
CURTAIN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E2540"}, {"offset": 1, "color": "#3C1222"}]}}
CURTAIN_DARK = "#34101E"
CURTAIN_SHEEN = "#9A4560"
SILK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#DEC9F0"}, {"offset": 1, "color": "#A886C8"}]}}
SILK_DARK = "#8E6EAE"
SILK_SHEEN = "#F2E8FA"
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C2AE92"}, {"offset": 0.7, "color": "#9E8A70"},
    {"offset": 1, "color": "#74634E"}]}}
FUR_MID = "#9E8A70"
SHEET_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4EDDA"}, {"offset": 1, "color": "#D8CBAE"}]}}
RULE = "#A89A78"
GOLD = "#C9A85C"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#9C8AB0", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0D4EC", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#54466A", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#181020",
       strokeWidth=4, opacity=70)

# --- the data table: a fine-print sheet, held up to be wrapped ---------------------
d.path(rot_rect_path(608, 470, 210, 258, -6), "Sheet shadow",
       fill="#120C16", opacity=35, stroke=NONE)
d.path(rot_rect_path(600, 462, 210, 258, -6), "Data sheet",
       fill=SHEET_GRAD, stroke=INK, strokeWidth=4)
# table header band + column rules + 9-point text rows
d.path(rot_rect_path(600, 372, 184, 22, -6), "Table head band",
       fill="#C8BA98", opacity=70, stroke=NONE)
for i, (cx, cy, w) in enumerate([(600,404,176),(599,420,176),(598,436,176),
                                 (597,452,176),(596,468,176),(595,484,176),
                                 (594,500,176),(593,516,176),(592,532,176)]):
    d.path(f"M{cx-w/2},{cy} L{cx+w/2},{cy-10}", f"Row rule {i+1}",
           fill=NONE, stroke=RULE, strokeWidth=1.6, opacity=65)
for i, (cx, cy, h) in enumerate([(552,462,120),(644,452,140)]):
    d.path(f"M{cx},{cy-h/2} L{cx-6},{cy+h/2}", f"Col rule {i+1}",
           fill=NONE, stroke=RULE, strokeWidth=1.4, opacity=55)
# 9-point text: hairline double-strokes inside each row
for i, (cx, cy, w) in enumerate([(600,410,150),(599,426,140),(598,442,148),
                                 (597,458,138),(596,474,146),(595,490,136),
                                 (594,506,142),(593,522,128)]):
    d.path(f"M{cx-w/2},{cy} L{cx+w/2},{cy-8.5}", f"9pt line {i+1}a",
           fill=NONE, stroke="#8A7C60", strokeWidth=1, opacity=55)
    d.path(f"M{cx-w/2},{cy+4} L{cx+w/2-14},{cy+4-8}", f"9pt line {i+1}b",
           fill=NONE, stroke="#8A7C60", strokeWidth=1, opacity=45)

# --- the lilac silk, wrapped around the lower sheet and pooling at the hem -----------
d.path("M470,520 C540,486 640,478 716,512 C736,522 740,548 722,566 "
       "C700,588 668,576 650,596 C626,622 640,652 610,668 "
       "C560,690 480,684 448,648 C420,616 430,548 470,520 Z",
       "Silk wrap", fill=SILK_GRAD, stroke=INK, strokeWidth=4)
# silk folds
d.path("M500,540 C540,520 620,512 690,528", "Fold 1", fill=NONE,
       stroke=SILK_DARK, strokeWidth=5, opacity=55, cap="round")
d.path("M480,586 C540,566 610,560 676,576", "Fold 2", fill=NONE,
       stroke=SILK_DARK, strokeWidth=4, opacity=50, cap="round")
d.path("M520,634 C560,650 600,650 636,634", "Fold 3", fill=NONE,
       stroke=SILK_DARK, strokeWidth=4, opacity=45, cap="round")
# sheen along the wrap and the trailing tail
d.path("M492,528 C560,502 640,498 706,520", "Silk sheen", fill=NONE,
       stroke=SILK_SHEEN, strokeWidth=9, opacity=45, cap="round")
d.path("M700,560 C716,620 706,668 668,700 C660,676 668,640 652,606 "
       "C672,590 686,576 700,560 Z", "Silk tail", fill=SILK_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M688,580 C696,626 688,662 672,690", "Tail sheen", fill=NONE,
       stroke=SILK_SHEEN, strokeWidth=5, opacity=40, cap="round")
# a gathered cinch where the wrap is tied shut, ribbon tails hanging
d.path("M556,516 C540,498 514,496 504,514 C496,530 510,544 530,540 "
       "C546,537 552,528 556,516 Z", "Cinch loop L", fill=SILK_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M570,518 C584,498 610,494 622,510 C632,524 620,540 600,538 "
       "C584,536 574,530 570,518 Z", "Cinch loop R", fill=SILK_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M548,536 C540,556 542,576 550,592 L562,588 C556,572 556,552 560,538 Z",
       "Cinch tail L", fill=SILK_GRAD, stroke=INK, strokeWidth=3)
d.path("M576,536 C586,554 588,574 582,592 L570,588 C576,572 574,552 568,538 Z",
       "Cinch tail R", fill=SILK_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Cinch knot", x=550, y=512, width=26, height=20,
        fill=SILK_DARK, stroke=INK, strokeWidth=3)

# --- the mascot, mid-wrap, paws on the silk -----------------------------------------
d.shape("ellipse", "Mascot shadow", x=296, y=684, width=190, height=18,
        fill="#120C16", opacity=35, stroke=NONE)
d.shape("ellipse", "Body", x=306, y=496, width=160, height=192,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Head", x=322, y=370, width=128, height=124,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
for ex in (334, 450):
    d.shape("ellipse", f"Ear {ex}", x=ex-11, y=366, width=26, height=24,
            fill=FUR_MID, stroke=INK, strokeWidth=3.5)
# serene downward gaze at the work
d.path("M356,440 C362,446 370,446 376,440", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M400,440 C406,446 414,446 420,440", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M368,466 C376,472 396,472 404,466", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# arms: one pressing the wrap shut at the cinch, one smoothing its skirt
d.path("M440,528 C470,522 500,522 538,526", "Arm right", fill=NONE,
       stroke=FUR_MID, strokeWidth=16, cap="round")
d.shape("ellipse", "Paw right", x=532, y=516, width=28, height=24,
        fill=FUR_MID, stroke=INK, strokeWidth=3.5)
d.path("M368,560 C400,596 440,624 482,640", "Arm left", fill=NONE,
       stroke=FUR_MID, strokeWidth=16, cap="round")
d.shape("ellipse", "Paw left", x=474, y=630, width=28, height=24,
        fill=FUR_MID, stroke=INK, strokeWidth=3.5)

# --- the velvet curtain, drawn back on gold cords ------------------------------------
# valance swagged along the top of the disc
d.path("M104,140 A420,420 0 0 1 896,140 L896,96 "
       "C760,196 660,196 580,150 C500,196 400,196 320,150 "
       "C240,196 160,190 104,96 Z",
       "Valance", fill=CURTAIN_GRAD, stroke=INK, strokeWidth=4)
d.path("M140,130 C220,170 300,170 360,140", "Valance sheen 1", fill=NONE,
       stroke=CURTAIN_SHEEN, strokeWidth=8, opacity=45, cap="round")
d.path("M430,150 C500,180 570,180 640,150", "Valance sheen 2", fill=NONE,
       stroke=CURTAIN_SHEEN, strokeWidth=8, opacity=45, cap="round")
d.path("M700,140 C770,170 830,164 880,130", "Valance sheen 3", fill=NONE,
       stroke=CURTAIN_SHEEN, strokeWidth=8, opacity=45, cap="round")
# left drape, gathered at a tie-back
d.path("M108,120 C180,140 260,160 300,220 C270,300 262,380 296,470 "
       "C250,540 190,570 150,560 C120,440 104,280 108,120 Z",
       "Curtain L", fill=CURTAIN_GRAD, stroke=INK, strokeWidth=4)
d.path("M140,160 C170,260 160,400 175,520", "Fold L1", fill=NONE,
       stroke=CURTAIN_DARK, strokeWidth=9, opacity=60, cap="round")
d.path("M190,180 C215,280 205,420 225,530", "Fold L2", fill=NONE,
       stroke=CURTAIN_DARK, strokeWidth=8, opacity=55, cap="round")
d.path("M240,200 C255,290 250,400 272,480", "Fold L3", fill=NONE,
       stroke=CURTAIN_DARK, strokeWidth=7, opacity=50, cap="round")
d.path("M165,170 C190,270 180,400 195,515", "Sheen L", fill=NONE,
       stroke=CURTAIN_SHEEN, strokeWidth=7, opacity=40, cap="round")
# right drape, mirror
d.path("M892,120 C820,140 740,160 700,220 C730,300 738,380 704,470 "
       "C750,540 810,570 850,560 C880,440 896,280 892,120 Z",
       "Curtain R", fill=CURTAIN_GRAD, stroke=INK, strokeWidth=4)
d.path("M860,160 C830,260 840,400 825,520", "Fold R1", fill=NONE,
       stroke=CURTAIN_DARK, strokeWidth=9, opacity=60, cap="round")
d.path("M810,180 C785,280 795,420 775,530", "Fold R2", fill=NONE,
       stroke=CURTAIN_DARK, strokeWidth=8, opacity=55, cap="round")
d.path("M760,200 C745,290 750,400 728,480", "Fold R3", fill=NONE,
       stroke=CURTAIN_DARK, strokeWidth=7, opacity=50, cap="round")
d.path("M835,170 C810,270 820,400 805,515", "Sheen R", fill=NONE,
       stroke=CURTAIN_SHEEN, strokeWidth=7, opacity=40, cap="round")
# gold tie-back cords + tassels
for sx, label in [(296, "L"), (704, "R")]:
    d.path(f"M{sx-30},452 C{sx-8},470 {sx+8},470 {sx+30},448",
           f"Tie cord {label}", fill=NONE, stroke=GOLD,
           strokeWidth=6, cap="round")
    d.path(f"M{sx},468 L{sx},496", f"Tassel stem {label}", fill=NONE,
           stroke=GOLD, strokeWidth=4)
    d.path(f"M{sx-9},496 L{sx+9},496 L{sx+5},522 L{sx-5},522 Z",
           f"Tassel {label}", fill=GOLD, stroke=INK, strokeWidth=2.5)

# --- captions -------------------------------------------------------------------------
d.text("APPENDIX SILK", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#EDE2F4", justify="center")
r = d.text("CURATOR OF GRACEFUL DISPLACEMENT", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C6B2D6", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("275.appendix-silk-V1R00")
