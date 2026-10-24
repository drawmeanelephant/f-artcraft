#!/usr/bin/env python3
"""Bad Request Bob — mascot portrait V1R00.
Bob at the intake desk, stamp already coming down on a request whose
mandatory fields were never filled in. The in-tray leans with more of
them. Apologetically careless; the stamp says FINE. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Bad Request Bob — Mascot Portrait", 1000, 1000)

INK = "#33261C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#221C16"}, {"offset": 1, "color": "#181410"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A7C66"}, {"offset": 0.7, "color": "#605646"},
    {"offset": 1, "color": "#2C2720"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4C4236"}, {"offset": 1, "color": "#1E1A14"}]}}
BOB_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D4BF9C"}, {"offset": 0.72, "color": "#AC9A76"},
    {"offset": 1, "color": "#70604A"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E5238"}, {"offset": 1, "color": "#382A1E"}]}}
PAPER = "#F0E6CC"
RED = "#B04838"
BRASS = "#C9A85E"
TRAY = "#4A4038"

# --- backdrop + plate --------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#9A8A70", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4DAC4", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(190,234,8),(806,232,7),(158,520,9),(838,544,8),
                               (252,764,7),(750,750,9),(134,392,6),(864,394,7),
                               (394,112,7),(612,112,8),(334,822,6),(668,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#564C3E", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#161009",
       strokeWidth=4, opacity=70)

# --- the intake counter ------------------------------------------------------------------
d.shape("ellipse", "Desk shadow", x=170, y=688, width=660, height=22,
        fill="#120C08", opacity=40, stroke=NONE)
d.path("M186,596 L814,596 L798,700 L202,700 Z", "Counter", fill=DESK_GRAD,
       stroke=INK, strokeWidth=6, join="round")
d.path("M186,596 L814,596", "Counter edge", fill=NONE, stroke="#96744C",
       strokeWidth=5, opacity=80)
d.path("M236,640 L764,640 M230,672 L770,672", "Counter grain", fill=NONE,
       stroke="#241A12", strokeWidth=3, opacity=40)
# the intake sign, hanging slightly crooked like everything else here
d.path("M676,620 L760,616 L764,652 L680,656 Z", "Intake sign", fill=BRASS,
       stroke=INK, strokeWidth=4, join="round")
d.text("INTAKE", "Sign text", x=722, y=645, size=18, font="Virelai Sans",
       color="#3E2E18", justify="center")

# --- the in-tray: a queue of almost-requests ----------------------------------------------
d.shape("ellipse", "Tray shadow", x=196, y=640, width=140, height=16,
        fill="#120C08", opacity=40, stroke=NONE)
d.path("M206,560 L336,560 L326,644 L216,644 Z", "Tray", fill=TRAY,
       stroke=INK, strokeWidth=5, join="round")
d.path("M206,560 L336,560 L332,586 L210,586 Z", "Tray rim", fill="#5C5148",
       stroke=INK, strokeWidth=4, join="round")
# forms leaning out at every angle, none of them complete
d.path("M222,556 L252,472 L292,478 L268,558 Z", "Form lean L", fill=PAPER,
       stroke=INK, strokeWidth=4, join="round")
d.path("M232,496 L266,500 M236,514 L268,518", "Form L lines", fill=NONE,
       stroke="#A89468", strokeWidth=2.5, opacity=80)
d.path("M282,558 L296,462 L338,468 L330,560 Z", "Form lean R", fill="#E4D6B4",
       stroke=INK, strokeWidth=4, join="round")
d.path("M298,486 L328,490 M300,504 L330,508 M302,522 L328,526", "Form R lines",
       fill=NONE, stroke="#A89468", strokeWidth=2.5, opacity=80)
d.path("M282,462 L296,448 L338,454 L338,468 Z", "Form R dogear",
       fill="#CDBC98", stroke=INK, strokeWidth=3, join="round")

# --- Bob: apologetically careless ---------------------------------------------------------
d.shape("ellipse", "Bob shadow", x=380, y=686, width=250, height=24,
        fill="#120C08", opacity=45, stroke=NONE)
# body: soft bell, one shoulder already shrugging
d.path("M500,392 C576,392 622,452 630,548 C634,620 626,660 612,686 "
       "L382,686 C368,660 362,620 366,548 C372,452 424,392 500,392 Z",
       "Bob body", fill=BOB_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body hi", x=420, y=424, width=96, height=44,
        fill="#FFFFFF", opacity=14, stroke=NONE)
# collar and the tie that gave up
d.path("M462,560 L500,586 L538,560 L528,548 L500,566 L472,548 Z",
       "Collar", fill="#EDE3C8", stroke=INK, strokeWidth=4, join="round")
d.path("M496,566 L512,566 L520,640 L504,656 L488,640 Z", "Tie",
       fill="#7A4A44", stroke=INK, strokeWidth=4, join="round")
d.path("M494,600 L516,600", "Tie crease", fill=NONE, stroke="#4E2E2A",
       strokeWidth=3, opacity=70)
# the name tag: handwritten, slightly crooked
d.path("M432,596 L490,592 L492,620 L434,624 Z", "Name tag", fill=PAPER,
       stroke=INK, strokeWidth=3, join="round")
d.text("BOB", "Tag text", x=461, y=615, size=16, font="Virelai Sans",
       color="#4A3820", justify="center")

# left arm: open palm of helpless welcome — every request deserves a chance
d.path("M382,520 C352,542 338,568 336,592", "Arm L", fill=NONE,
       stroke="#AC9A76", strokeWidth=20, cap="round")
d.path("M318,584 C318,572 332,566 346,570 C360,566 372,574 370,586 "
       "C368,598 354,602 344,600 C330,602 318,596 318,584 Z",
       "Palm L", fill="#D4BF9C", stroke=INK, strokeWidth=4)

# right arm: raised, the stamp already committed to its answer
d.path("M594,470 C636,444 660,420 676,392", "Arm R", fill=NONE,
       stroke="#AC9A76", strokeWidth=20, cap="round")
# the rubber stamp in the fist: wooden grip, red business end
d.path("M652,392 C648,378 658,368 674,370 C690,368 700,378 696,392 "
       "C694,404 682,408 672,406 C660,408 654,402 652,392 Z",
       "Fist R", fill="#D4BF9C", stroke=INK, strokeWidth=4)
d.path("M668,370 L664,340 C662,330 670,324 680,326 C690,324 696,332 694,342 "
       "L690,368 Z", "Stamp grip", fill="#8A6438", stroke=INK,
       strokeWidth=4, join="round")
d.shape("ellipse", "Grip top", x=664, y=316, width=30, height=16,
        fill="#A87C48", stroke=INK, strokeWidth=4)
d.path("M646,368 L706,368 L712,396 L640,396 Z", "Stamp base", fill=RED,
       stroke=INK, strokeWidth=4, join="round")
d.path("M644,386 L710,386", "Base edge", fill=NONE, stroke="#6E2820",
       strokeWidth=3, opacity=80)
# motion ticks: the stamp is mid-fall
d.path("M716,330 L736,316 M724,356 L748,348 M724,384 L748,388",
       "Stamp motion", fill=NONE, stroke=INK, strokeWidth=4,
       opacity=55, cap="round")

# face: the crooked smile of a man about to say "we'll fix it in processing"
d.shape("ellipse", "Eye L", x=442, y=466, width=26, height=26,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye L glint", x=448, y=470, width=8, height=8,
        fill="#FFFFFF", stroke=NONE)
d.shape("ellipse", "Eye R", x=528, y=462, width=26, height=26,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R glint", x=534, y=466, width=8, height=8,
        fill="#FFFFFF", stroke=NONE)
# eyebrows: one asking, one apologizing
d.path("M432,436 C444,428 460,428 470,434", "Brow L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M522,432 C534,424 550,424 562,430", "Brow R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# lopsided grin
d.path("M464,528 C478,540 508,542 530,526", "Grin", fill=NONE, stroke=INK,
       strokeWidth=6, cap="round")
d.path("M528,522 L536,516", "Grin tail", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.shape("ellipse", "Cheek L", x=426, y=508, width=26, height=13,
        fill="#B09878", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=540, y=504, width=26, height=13,
        fill="#B09878", opacity=45, stroke=NONE)
# the sweat bead of structural leniency
d.path("M408,462 C402,474 400,480 400,486 C400,494 407,498 412,494 "
       "C417,498 424,494 424,486 C424,478 416,468 412,458 Z",
       "Sweat", fill="#B8D4DC", stroke=INK, strokeWidth=3, opacity=85)

# --- the request being stamped: mandatory fields, all of them blank ------------------------
d.path("M420,600 L620,592 L626,660 L426,668 Z", "The request", fill=PAPER,
       stroke=INK, strokeWidth=4, join="round")
# header line + empty field boxes with dashed outlines
d.path("M440,606 L540,602", "Form header", fill=NONE, stroke="#8A7A54",
       strokeWidth=5, opacity=90)
for i, (fx, fw) in enumerate([(440, 88), (540, 62)]):
    d.path(f"M{fx},{620 + i*2} L{fx + fw},{618 + i*2} L{fx + fw + 2},{634 + i*2} "
           f"L{fx + 2},{636 + i*2} Z", f"Blank field {i+1}", fill=NONE,
           stroke="#8A7A54", strokeWidth=2.5, dash=[4, 3], opacity=85)
d.path("M444,646 L520,642 M444,656 L556,652", "Form lines", fill=NONE,
       stroke="#A89468", strokeWidth=2.5, opacity=70)
# the red corner stamp already landed once: FINE
d.path("M552,606 L616,600 L620,632 L556,638 Z", "FINE box", fill=NONE,
       stroke=RED, strokeWidth=4, join="round", opacity=85)
d.text("FINE", "FINE text", x=586, y=627, size=20, font="Virelai Sans",
       color=RED, justify="center")
# a second form half-off the desk, drifting toward the floor it will become
d.path("M300,618 L384,612 L388,660 L304,666 Z", "Spare form", fill="#E4D6B4",
       stroke=INK, strokeWidth=4, join="round")
d.path("M314,628 L370,624 M316,640 L372,636", "Spare lines", fill=NONE,
       stroke="#A89468", strokeWidth=2.5, opacity=70)

# --- captions ---------------------------------------------------------------------------
d.text("BAD REQUEST BOB", "Name", x=500, y=930, size=54, font="Virelai Sans",
       color="#F0E4CC", justify="center")
r = d.text("INPUT MISCLASSIFICATION WARDEN", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C4AE8E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("400.bad-request-bob-V1R00")
