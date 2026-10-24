#!/usr/bin/env python3
"""SI-9 Interval Witness — mascot portrait V1R00.
A solemn little clerk-ghost standing under a timeline with one blank stretch
hollowed out of it, holding a minutes book open to an empty entry while a
pencil hovers, never quite filing. 1000x1000 plate format.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("SI-9 Interval Witness — Mascot Portrait", 1000, 1000)

INK = "#332E3E"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#121C30"}, {"offset": 1, "color": "#05080F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E6EEF0"}, {"offset": 0.65, "color": "#B4C9D2"},
    {"offset": 1, "color": "#7896A4"}]}}
BAR_GRAD = {"gradient": {"kind": "linear", "start": [0, 190], "end": [0, 226], "stops": [
    {"offset": 0, "color": "#3C4E5C"}, {"offset": 1, "color": "#26374A"}]}}
ROBE_GRAD = {"gradient": {"kind": "linear", "start": [0, 400], "end": [0, 750], "stops": [
    {"offset": 0, "color": "#A8BECA"}, {"offset": 0.6, "color": "#7E94A4"},
    {"offset": 1, "color": "#586C7C"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "start": [0, 648], "end": [0, 770], "stops": [
    {"offset": 0, "color": "#F6F0E0"}, {"offset": 1, "color": "#DCD2B8"}]}}
BEAM_GRAD = {"gradient": {"kind": "linear", "start": [0, 232], "end": [0, 580], "stops": [
    {"offset": 0, "color": "#EAF6FA", "opacity": 0.22},
    {"offset": 1, "color": "#EAF6FA", "opacity": 0}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#9DBBC8", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2C4652", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EDF5F6", strokeWidth=3, opacity=38)
# quiet patina + dust on the plate
d.shape("ellipse", "Patina 1", x=200, y=580, width=240, height=130,
        fill="#8AA6B2", opacity=18, stroke=NONE)
d.shape("ellipse", "Patina 2", x=580, y=150, width=200, height=110,
        fill="#8AA6B2", opacity=15, stroke=NONE)
for i, (x, y, w) in enumerate([(170, 330, 6), (840, 300, 7), (150, 520, 7), (850, 560, 6),
                               (250, 770, 6), (740, 760, 7), (300, 130, 5), (690, 120, 6)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E7E8C", opacity=35, stroke=NONE)
# faint dust on the dark margin outside the plate
for i, (x, y, w) in enumerate([(60, 120, 4), (930, 90, 5), (45, 560, 4), (950, 620, 4),
                               (120, 900, 4), (880, 910, 5), (520, 30, 4), (240, 45, 3)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#C9DAE2", opacity=28, stroke=NONE)

# --- timeline band with the silent interval hollowed out ----------------------
d.shape("rectangle", "Timeline", x=180, y=190, width=640, height=36, radius=18,
        fill=BAR_GRAD, stroke="#1E2E3A", strokeWidth=4)
# ticks along the bar — everywhere EXCEPT the blank stretch 430..640
for i, x in enumerate(range(196, 816, 31)):
    if 424 < x < 646:
        continue
    d.path(f"M{x},198 L{x},218", f"Tick {i}", fill=NONE,
           stroke="#8FB0BE", strokeWidth=3, opacity=55, cap="round")
# the hollowed span: darker notch + dashed boundary brackets
d.shape("rectangle", "Silent interval", x=430, y=194, width=210, height=28, radius=14,
        fill="#0C141F", opacity=85, stroke=NONE)
for i, x in enumerate((430, 640)):
    d.path(f"M{x},180 L{x},236", f"Interval bracket {i+1}", fill=NONE,
           stroke="#A9C6D2", strokeWidth=3, dash=[5, 5], opacity=70, cap="round")
# three faint ellipsis dots inside the void — the unlogged minutes
for i, x in enumerate((508, 535, 562)):
    d.shape("ellipse", f"Void dot {i+1}", x=x, y=204, width=8, height=8,
            fill="#7E9CA8", opacity=45, stroke=NONE)
# beam of attention: the blank space people point at
d.path("M445,232 L655,232 L640,560 L400,560 Z", "Beam",
       fill=BEAM_GRAD, stroke=NONE)

# --- ground shadow -------------------------------------------------------------
d.shape("ellipse", "Shadow", x=360, y=742, width=280, height=30,
        fill="#1E2E3A", opacity=22, stroke=NONE)

# --- the witness: robed clerk-ghost ----------------------------------------------
d.path("M368,724 C354,610 372,520 412,452 C440,404 560,404 588,452 "
       "C628,520 646,610 632,724 C600,748 552,756 500,756 "
       "C448,756 400,748 368,724 Z",
       "Robe", fill=ROBE_GRAD, stroke=INK, strokeWidth=6)
# robe folds + hem shade
d.path("M448,560 C440,620 438,680 444,734", "Fold L", fill=NONE,
       stroke="#4E6272", strokeWidth=4, opacity=60, cap="round")
d.path("M552,560 C560,620 562,680 556,734", "Fold R", fill=NONE,
       stroke="#4E6272", strokeWidth=4, opacity=60, cap="round")
d.path("M392,700 C430,724 570,724 608,700 C580,738 420,738 392,700 Z",
       "Hem shade", fill="#3E5060", opacity=30, stroke=NONE)
# dome highlight
d.shape("ellipse", "Dome light", x=430, y=428, width=140, height=54,
        fill="#FFFFFF", opacity=16, stroke=NONE)

# face: calm half-lidded eyes
d.shape("ellipse", "Eye L", x=446, y=486, width=38, height=46,
        fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye R", x=516, y=486, width=38, height=46,
        fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=459, y=504, width=16, height=22,
        fill="#241E2C", stroke=NONE)
d.shape("ellipse", "Pupil R", x=529, y=504, width=16, height=22,
        fill="#241E2C", stroke=NONE)
d.shape("ellipse", "Glint L", x=463, y=508, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=533, y=508, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M444,492 C456,478 476,476 486,484", "Lid L", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M514,484 C524,476 544,478 556,492", "Lid R", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M482,562 C494,568 506,568 518,562", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")

# clerk collar + tie
d.path("M468,594 L500,622 L468,634 Z", "Collar L", fill="#F4EEE0",
       stroke=INK, strokeWidth=3)
d.path("M532,594 L500,622 L532,634 Z", "Collar R", fill="#F4EEE0",
       stroke=INK, strokeWidth=3)
d.path("M500,622 L490,640 L500,664 L510,640 Z", "Tie", fill="#4E3A54",
       stroke=INK, strokeWidth=3)

# --- open minutes book held in front --------------------------------------------
# hands first (book covers their inner edge)
d.shape("ellipse", "Hand L", x=382, y=694, width=48, height=40,
        fill="#9DB4C0", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=570, y=694, width=48, height=40,
        fill="#9DB4C0", stroke=INK, strokeWidth=4)
# cover, then pages
d.path("M500,664 L398,640 L398,752 L500,776 Z", "Cover L", fill="#5E4E40",
       stroke=INK, strokeWidth=3)
d.path("M500,664 L602,640 L602,752 L500,776 Z", "Cover R", fill="#5E4E40",
       stroke=INK, strokeWidth=3)
d.path("M500,672 L410,652 L410,742 L500,764 Z", "Page L", fill=PAGE_GRAD,
       stroke=INK, strokeWidth=3)
d.path("M500,672 L590,652 L590,742 L500,764 Z", "Page R", fill=PAGE_GRAD,
       stroke=INK, strokeWidth=3)
d.path("M500,672 L500,764", "Spine", fill=NONE, stroke=INK,
       strokeWidth=3, opacity=60)
# left page: minuted lines (the logged past)
for i, y in enumerate((676, 694, 712, 730)):
    d.path(f"M424,{y} L488,{y + 10}", f"Line L{i+1}", fill=NONE,
           stroke="#8A8272", strokeWidth=3, opacity=65, cap="round")
# right page: a header rule, then the empty entry — dashed box where it should be
d.path("M514,676 L578,666", "Line R head", fill=NONE,
       stroke="#8A8272", strokeWidth=3, opacity=65, cap="round")
d.path("M516,694 L576,686 L576,724 L516,734 Z", "Empty entry", fill=NONE,
       stroke="#8A8272", strokeWidth=2.5, dash=[4, 4], opacity=55)
# pencil hovering over the blank entry, never quite filing
d.path(rot_rect_path(560, 636, 64, 12, -28), "Pencil body", fill="#E8B23C",
       stroke=INK, strokeWidth=3)
d.path("M533,651 L522,662 L538,660 Z", "Pencil tip", fill="#3A2E24",
       stroke=INK, strokeWidth=2)
d.path(rot_rect_path(589, 622, 12, 12, -28), "Pencil eraser", fill="#C97E8C",
       stroke=INK, strokeWidth=2)

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

NAME = "SI-9 INTERVAL WITNESS"
d.text(NAME, "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#DCE8EE", justify="center")
tid = text_id(NAME)
if tid:
    digit_font(tid, NAME)

ROLE = "KEEPS THE BLANK ON RECORD"
d.text(ROLE, "Role", x=500, y=968, size=23,
       font="Virelai Sans", color="#8BA8B4", justify="center")
rid = text_id(ROLE)
if rid:
    d.cmd("text.setStyle", "role tracking", id=rid, tracking=280)

d.finish("078.si-9-interval-witness-V1R00")
