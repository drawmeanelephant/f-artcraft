#!/usr/bin/env python3
"""Consent Murmur — mascot portrait V1R00.
A translucent wisp-clerk bent over the minutes, transcribing the room's
silence into a record of unanimous approval. The table is empty; the
chairs were never asked. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Consent Murmur — Mascot Portrait", 1000, 1000)

INK = "#232A30"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#12161C"}, {"offset": 1, "color": "#07090C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E4A58"}, {"offset": 0.7, "color": "#232C36"},
    {"offset": 1, "color": "#10161C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#242E3A"}, {"offset": 1, "color": "#0E1418"}]}}
WISP = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8E4F0"}, {"offset": 0.7, "color": "#9DB2C8"},
    {"offset": 1, "color": "#64788C"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3A2C"}, {"offset": 1, "color": "#241C14"}]}}
PAGE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2ECD8"}, {"offset": 1, "color": "#D6CCAC"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A8CA0", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C2D2E0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A4854", opacity=45, stroke=NONE)

# --- floor --------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C1214",
       strokeWidth=4, opacity=70)

# --- emptied chairs, pushed back at the angles people leave at -------------------
def chair(cx, cy, lean, flip):
    # simple meeting chair: back slab + seat, one silhouette, slightly leaned
    p = rot_rect_path(cx, cy-58, 62, 86, lean)
    d.path(p, "Chair back", fill="#2A3644", stroke=INK, strokeWidth=5,
           join="round")
    s = rot_rect_path(cx, cy+18, 78, 26, lean)
    d.path(s, "Chair seat", fill="#364456", stroke=INK, strokeWidth=5,
           join="round")
    # legs hinted, never finished — they stopped mattering first
    d.path(f"M{cx-24},{cy+30} L{cx-26},{cy+62} M{cx+24},{cy+30} "
           f"L{cx+26},{cy+62}", "Chair legs", fill=NONE, stroke=INK,
           strokeWidth=4, cap="round", opacity=70)

chair(250, 560, -8, 1)
chair(372, 580, 4, 1)
chair(640, 578, -5, 1)
chair(758, 556, 9, 1)

# --- the table: one long dark slab the silence sat at ------------------------------
d.path("M318,472 L682,472 L756,612 L244,612 Z", "Tabletop", fill=WOOD,
       stroke=INK, strokeWidth=6, join="round")
d.path("M244,612 L756,612 L756,634 L244,634 Z", "Table edge", fill="#2A2018",
       stroke=INK, strokeWidth=4, join="round")
d.path("M300,634 L316,700 M700,634 L684,700", "Table legs", fill=NONE,
       stroke=INK, strokeWidth=9, cap="round")
# vacant name-tents — dashes where attendees would be
for i, (x, y) in enumerate([(390,520),(560,514),(480,556)]):
    d.path(rot_rect_path(x, y, 56, 26, -4 if i == 1 else 3), f"Tent {i+1}",
           fill="#CBC4AE", stroke=INK, strokeWidth=3, join="round",
           opacity=80)
    d.path(rot_rect_path(x, y, 24, 4, -4 if i == 1 else 3),
           f"Tent dash {i+1}", fill="#6E6858", stroke=NONE, opacity=70)
# cold coffee the silence left behind
d.shape("ellipse", "Cup", x=618, y=540, width=30, height=22,
        fill="#3A4654", stroke=INK, strokeWidth=3)
d.path("M646,546 C656,546 656,556 646,556", "Cup handle", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")

# --- the murmur: a speakerless register over the table -------------------------------
# concentric wavy arcs, louder in hindsight — opacity rises toward the pen
for i, (y, w, op) in enumerate([(268, 300, 18), (300, 260, 26),
                                (330, 218, 34), (358, 176, 44)]):
    x0, x1 = 500 - w, 500 + w
    d.path(f"M{x0},{y} C{x0+w*0.7},{y-26} {x1-w*0.7},{y-26} {x1},{y} "
           f"C{x1-w*0.7},{y+22} {x0+w*0.7},{y+22} {x0},{y} Z",
           f"Murmur band {i+1}", fill="#AEC4D8", opacity=op, stroke=NONE)
# motes of consensus drifting down into the ledger
for i, (x, y, r) in enumerate([(452,392,5),(512,382,4),(548,398,6),
                               (488,404,3),(566,378,3)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill="#D8E4F0", opacity=40-i*5, stroke=NONE)

# --- the wisp-clerk: the only attendee never listed ---------------------------------
d.shape("ellipse", "Wisp glow", x=380, y=300, width=240, height=300,
        fill="#AEC4D8", opacity=12, stroke=NONE)
# body: a tapering register, no feet — it hovers where the answer was not
d.path("M500,308 C560,308 588,352 586,402 C584,448 566,478 560,516 "
       "C554,548 566,576 552,596 C540,612 520,604 512,586 "
       "C500,610 478,616 464,598 C450,580 462,552 456,522 "
       "C448,480 420,452 420,404 C420,352 448,308 500,308 Z",
       "Wisp body", fill=WISP, stroke=INK, strokeWidth=5, opacity=88)
# inner translucency — you can nearly see the table through it
d.shape("ellipse", "Wisp hollow", x=452, y=400, width=96, height=140,
        fill="#3E4A58", opacity=22, stroke=NONE)
d.shape("ellipse", "Wisp sheen", x=448, y=322, width=90, height=44,
        fill="#FFFFFF", opacity=20, stroke=NONE)
# face: downcast, serene, mid-transcription
d.path("M456,392 C463,399 474,399 481,392", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M519,392 C526,399 537,399 544,392", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M486,424 L516,424", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round", opacity=70)
# ear-fins catching the register
d.path("M420,372 C400,366 392,348 398,330", "Ear L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=60)
d.path("M582,368 C602,360 608,342 600,326", "Ear R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=60)

# --- arm + quill reaching the ledger ---------------------------------------------------
d.path("M560,470 C584,486 596,506 592,528", "Writing arm", fill=NONE,
       stroke="#8AA0B4", strokeWidth=14, cap="round")
d.shape("ellipse", "Writing hand", x=580, y=516, width=26, height=20,
        fill=WISP, stroke=INK, strokeWidth=4)
d.path("M598,522 L626,492", "Quill", fill=NONE, stroke="#D8E4F0",
       strokeWidth=5, cap="round")
d.path("M626,492 C642,494 646,512 634,524 C628,512 626,500 626,492 Z",
       "Quill tip feather", fill="#C2D2E0", stroke=INK, strokeWidth=2.5,
       opacity=85)

# --- the minutes: open ledger recording a room that was never asked -------------------
d.path("M404,584 L500,568 L596,584 L596,660 L500,644 L404,660 Z",
       "Ledger", fill=PAGE, stroke=INK, strokeWidth=5, join="round")
d.path("M500,568 L500,644", "Ledger spine", fill=NONE, stroke="#8E8264",
       strokeWidth=3, opacity=60)
# left page: the attendance grid — every box ticked by nobody
for i in range(4):
    y = 592 + i*13
    d.shape("rectangle", f"Tick box {i+1}", x=416, y=y, width=9, height=9,
            fill=NONE, stroke="#6E5E42", strokeWidth=2)
    d.path(f"M417,{y+5} L420,{y+8} L426,{y+1}", f"Tick {i+1}", fill=NONE,
           stroke="#5E7A54", strokeWidth=2.5, cap="round")
    d.path(f"M432,{y+5} L480,{y+3}", f"Attendee {i+1}", fill=NONE,
           stroke="#8E8264", strokeWidth=3, cap="round", opacity=60)
# right page: the finding, in full
d.text("UNANIMOUS", "The finding", x=506, y=618, size=14,
       font="Virelai Sans", color="#5E4E36", justify="left")
d.path("M510,630 L584,626", "Finding rule", fill=NONE, stroke="#8E8264",
       strokeWidth=3, cap="round", opacity=60)
# fresh ink shine on the word that signs nothing
d.shape("ellipse", "Ink shine", x=518, y=600, width=70, height=14,
        fill="#FFFFFF", opacity=25, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("CONSENT MURMUR", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#DCE6EF", justify="center")
r = d.text("AMBIENT CONSENSUS CLERK", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9DB4C8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("284.consent-murmur-V1R00")
