#!/usr/bin/env python3
"""LC-04 Soft Green Seal — mascot portrait V1R00.
A soft green wax-seal creature with a scalloped, drippy base, settled
contentedly onto a filed record — the stamp is the mascot. The record sits
inside faint screenshot chrome: window frame, dots, scanlines, a cursor.
1000x1000 plate format.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LC-04 Soft Green Seal — Mascot Portrait", 1000, 1000)

INK = "#2E3A2C"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#12201A"}, {"offset": 1, "color": "#060D09"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E2EBDD"}, {"offset": 0.65, "color": "#B2C5AC"},
    {"offset": 1, "color": "#75906F"}]}}
REC_GRAD = {"gradient": {"kind": "linear", "start": [0, 270], "end": [0, 730], "stops": [
    {"offset": 0, "color": "#F4EFDD"}, {"offset": 1, "color": "#DCD2B4"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [0, 430], "end": [0, 680], "stops": [
    {"offset": 0, "color": "#A4D8AC"}, {"offset": 0.6, "color": "#74B57C"},
    {"offset": 1, "color": "#4E8256"}]}}
GLOW_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8F0DC", "opacity": 0.35},
    {"offset": 1, "color": "#D8F0DC", "opacity": 0}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#A8C4A8", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E4A34", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EEF5EA", strokeWidth=3, opacity=38)
d.shape("ellipse", "Patina 1", x=180, y=580, width=240, height=130,
        fill="#8EA884", opacity=16, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=150, width=200, height=110,
        fill="#8EA884", opacity=14, stroke=NONE)
for i, (x, y, w) in enumerate([(185, 355, 6), (822, 335, 7), (170, 550, 7), (838, 585, 6),
                               (268, 782, 6), (728, 778, 7), (318, 140, 5), (672, 133, 6)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E7E5C", opacity=35, stroke=NONE)
for i, (x, y, w) in enumerate([(68, 155, 4), (918, 125, 5), (58, 585, 4), (942, 655, 4),
                               (145, 912, 4), (868, 922, 5), (548, 24, 4), (258, 38, 3)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8DCC4", opacity=28, stroke=NONE)

# --- screenshot chrome: a window frame holding the record -----------------------
d.shape("rectangle", "Window frame", x=312, y=232, width=376, height=516,
        radius=10, fill=NONE, stroke="#4E6252", strokeWidth=3, opacity=80)
d.shape("rectangle", "Title bar", x=312, y=232, width=376, height=30,
        radius=10, fill="#4E6252", opacity=22, stroke=NONE)
d.path("M312,262 L688,262", "Title bar rule", fill=NONE,
       stroke="#4E6252", strokeWidth=2, opacity=60)
for i, x in enumerate((330, 348, 366)):
    d.shape("ellipse", f"Win dot {i+1}", x=x, y=241, width=10, height=10,
            fill="#4E6252", opacity=65, stroke=NONE)
# scanlines over the whole window — the artifact's age
for i, y in enumerate((292, 340, 388, 436, 484, 532, 580, 628, 676, 724)):
    d.path(f"M318,{y} L682,{y}", f"Scanline {i+1}", fill=NONE,
           stroke="#3E5244", strokeWidth=1.5, opacity=10)

# --- the filed record -------------------------------------------------------------
d.shape("rectangle", "Record", x=336, y=278, width=328, height=452,
        fill=REC_GRAD, stroke="#7A684A", strokeWidth=4)
# FILED tab + hole punch + ruling
d.shape("rectangle", "Filed tab", x=352, y=266, width=88, height=28,
        radius=6, fill="#C98A6E", stroke="#7A4A38", strokeWidth=3)
d.text("FILED", "Tab text", x=396, y=285, size=14, font="Virelai Sans",
       color="#F8F0DC", justify="center")
d.shape("ellipse", "Hole punch", x=610, y=296, width=20, height=20,
        fill="#9A8A6A", opacity=45, stroke="#7A684A", strokeWidth=2)
d.text("RECORD", "Rec header", x=500, y=324, size=18, font="Virelai Sans",
       color="#7A684A", justify="center")
for i, y in enumerate((352, 376, 400, 424, 448)):
    d.path(f"M372,{y} L628,{y}", f"Rec line {i+1}", fill=NONE,
           stroke="#9A8A6A", strokeWidth=4, opacity=55, cap="round")
# faint red-pencil query someone stopped asking
d.path("M372,472 L520,472", "Rec line faded", fill=NONE,
       stroke="#9A8A6A", strokeWidth=4, opacity=30, cap="round")
d.path("M586,470 C586,448 606,438 622,446 C638,454 640,474 626,486 "
       "C616,494 612,502 612,514", "Query mark", fill=NONE,
       stroke="#B56A52", strokeWidth=6, opacity=55, cap="round")
d.shape("ellipse", "Query dot", x=606, y=528, width=12, height=12,
        fill="#B56A52", opacity=55, stroke=NONE)

# --- the stamped imprint the creature sits in --------------------------------------
d.shape("ellipse", "Imprint outer", x=415, y=592, width=170, height=130,
        fill=NONE, stroke="#5E9E6A", strokeWidth=9, opacity=50)
d.shape("ellipse", "Imprint inner", x=437, y=610, width=126, height=94,
        fill=NONE, stroke="#5E9E6A", strokeWidth=5, opacity=40)
for i, (x1, y1, x2, y2) in enumerate([(455, 648, 480, 648), (490, 660, 545, 660),
                                      (455, 672, 505, 672)]):
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Imprint line {i+1}", fill=NONE,
           stroke="#5E9E6A", strokeWidth=4, opacity=45, cap="round")

# --- ground shadow -----------------------------------------------------------------
d.shape("ellipse", "Shadow", x=380, y=676, width=240, height=26,
        fill="#2E4A34", opacity=22, stroke=NONE)

# --- the soft green seal creature ---------------------------------------------------
# halo of archival comfort
d.shape("ellipse", "Glow", x=370, y=400, width=260, height=260,
        fill=GLOW_GRAD, stroke=NONE)
# scalloped wax body — dome rising off the imprint
d.path("M418,648 C414,560 432,486 470,450 C490,430 510,430 530,450 "
       "C568,486 586,560 582,648 "
       "L574,664 Q560,646 545,664 Q530,646 515,664 Q500,646 485,664 "
       "Q470,646 455,664 Q440,646 426,664 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# dome light + lower shade
d.shape("ellipse", "Dome light", x=440, y=452, width=120, height=52,
        fill="#FFFFFF", opacity=20, stroke=NONE)
d.path("M432,610 C460,632 540,632 568,610 C548,640 452,640 432,610 Z",
       "Base shade", fill="#3E6B46", opacity=30, stroke=NONE)

# serene face: eyes gently shut, small smile — nothing left to argue aloud
d.path("M438,548 C452,560 470,560 482,548", "Lid L", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.path("M518,548 C530,560 548,560 562,548", "Lid R", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.path("M482,590 C492,598 508,598 518,590", "Smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Blush L", x=430, y=566, width=26, height=14,
        fill="#4E8256", opacity=35, stroke=NONE)
d.shape("ellipse", "Blush R", x=544, y=566, width=26, height=14,
        fill="#4E8256", opacity=35, stroke=NONE)

# --- a cursor that never clicked resolve ---------------------------------------------
d.path("M640,700 L640,668 L658,684 L666,680 L648,664 L664,662 Z",
       "Cursor", fill="#4E6252", stroke="#2E4A34", strokeWidth=2, opacity=75)

# --- name + role ------------------------------------------------------------------
def text_id(text):
    # point-type nodes are named after their content, not the layer label
    doc = d.call("inspect_document", {"kind": "Type"}, "inspect type") or {}
    for nd in doc.get("nodes", []):
        if nd.get("name") == text:
            return nd["id"]
    return None

FALLBACK = set("0123456789Λ/™")
def digit_font(tid, text):
    b = 0
    for ch in text:
        n = len(ch.encode("utf-8"))
        if ch in FALLBACK:
            d.cmd("text.setStyle", f"fallback {ch}@{b}",
                  id=tid, font="Source Sans 3", start=b, end=b + n)
        b += n

NAME = "LC-04 SOFT GREEN SEAL"
d.text(NAME, "Name", x=500, y=930, size=52, font="Virelai Sans",
       color="#DDEAD8", justify="center")
tid = text_id(NAME)
if tid:
    digit_font(tid, NAME)

ROLE = "PROOF OF PROCEDURAL ABANDONMENT"
d.text(ROLE, "Role", x=500, y=968, size=23,
       font="Virelai Sans", color="#94B08E", justify="center")
rid = text_id(ROLE)
if rid:
    d.cmd("text.setStyle", "role tracking", id=rid, tracking=280)

d.finish("084.lc-04-soft-green-seal-V1R00")
