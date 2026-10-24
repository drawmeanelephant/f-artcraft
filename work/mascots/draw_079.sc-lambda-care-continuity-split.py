#!/usr/bin/env python3
"""SC-Λ Care/Continuity Split — mascot portrait V1R00.
The clerk-ghost stands at a lambda junction where one trunk splits into three
directive routes (a suggestion, an order, a metric), every one of them curving
back down into the same case file. 1000x1000 plate format.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("SC-Λ Care/Continuity Split — Mascot Portrait", 1000, 1000)

INK = "#382C44"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#1C1228"}, {"offset": 1, "color": "#08060F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EAE4F0"}, {"offset": 0.65, "color": "#C2B4D0"},
    {"offset": 1, "color": "#8E7CA4"}]}}
ROBE_GRAD = {"gradient": {"kind": "linear", "start": [0, 480], "end": [0, 780], "stops": [
    {"offset": 0, "color": "#B0A2C4"}, {"offset": 0.6, "color": "#86769E"},
    {"offset": 1, "color": "#5E4E76"}]}}
FOLDER_GRAD = {"gradient": {"kind": "linear", "start": [0, 680], "end": [0, 790], "stops": [
    {"offset": 0, "color": "#F0DCAC"}, {"offset": 1, "color": "#C9A96E"}]}}
TRUNK_GRAD = {"gradient": {"kind": "linear", "start": [500, 300], "end": [500, 700], "stops": [
    {"offset": 0, "color": "#6A5A80"}, {"offset": 1, "color": "#4A3C5C"}]}}

SOMA, COMA, CUNTIER = "#7FA87C", "#D9A441", "#6E9CC4"

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#B4A4CC", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E3050", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0EAF6", strokeWidth=3, opacity=38)
d.shape("ellipse", "Patina 1", x=210, y=170, width=220, height=120,
        fill="#9A88B0", opacity=16, stroke=NONE)
d.shape("ellipse", "Patina 2", x=590, y=620, width=230, height=130,
        fill="#9A88B0", opacity=14, stroke=NONE)
for i, (x, y, w) in enumerate([(180, 350, 6), (830, 320, 7), (160, 540, 6), (845, 540, 7),
                               (270, 780, 6), (720, 770, 6), (330, 120, 5), (660, 130, 6)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E5C88", opacity=32, stroke=NONE)
for i, (x, y, w) in enumerate([(70, 140, 4), (920, 110, 5), (50, 540, 4), (945, 600, 4),
                               (130, 890, 4), (870, 900, 5), (500, 32, 4), (760, 50, 3)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8CCE6", opacity=26, stroke=NONE)

# --- the lambda split: one trunk, three directive routes ------------------------
JX, JY = 500, 545          # junction
NL, NC, NR = (350, 275), (500, 232), (650, 275)   # branch end nodes

# return curves first (they pass under the mascot and the branches)
d.path(f"M{NL[0]},{NL[1]+18} C262,400 258,590 438,695", "Return L",
       fill=NONE, stroke=SOMA, strokeWidth=4, opacity=70, cap="round")
d.path(f"M{NC[0]},{NC[1]+18} C588,320 596,540 552,692", "Return C",
       fill=NONE, stroke=COMA, strokeWidth=4, opacity=70, cap="round")
d.path(f"M{NR[0]},{NR[1]+18} C762,400 742,590 568,695", "Return R",
       fill=NONE, stroke=CUNTIER, strokeWidth=4, opacity=70, cap="round")

# trunk: folder up to the junction
d.path(f"M504,700 L{JX},{JY}", "Trunk", fill=NONE, stroke=TRUNK_GRAD,
       strokeWidth=13, cap="round")
# branches: junction fanning up to the three readings
d.path(f"M{JX},{JY} C470,470 400,370 {NL[0]},{NL[1]}", "Branch SOMA",
       fill=NONE, stroke=SOMA, strokeWidth=11, cap="round")
d.path(f"M{JX},{JY} C500,460 500,340 {NC[0]},{NC[1]}", "Branch COMA",
       fill=NONE, stroke=COMA, strokeWidth=11, cap="round")
d.path(f"M{JX},{JY} C530,470 600,370 {NR[0]},{NR[1]}", "Branch CUNTIER",
       fill=NONE, stroke=CUNTIER, strokeWidth=11, cap="round")
# the three readings as document-glyph nodes
for i, (x, y, c) in enumerate([(NL[0], NL[1], SOMA), (NC[0], NC[1], COMA),
                               (NR[0], NR[1], CUNTIER)]):
    d.text("\uE003", f"Node {i+1}", x=x, y=y + 18, size=46,
           font="Virelai Mascots", color=c, justify="center")

# --- case file at the bottom ----------------------------------------------------
d.shape("ellipse", "Shadow", x=360, y=772, width=300, height=26,
        fill="#2E2438", opacity=22, stroke=NONE)
# back panel + tab
d.path("M430,686 L430,680 C430,672 436,668 444,668 L486,668 C492,668 496,671 500,675 "
       "L508,683 L566,683 C576,683 582,689 582,698 L582,724 L430,724 Z",
       "Folder back", fill="#C9A96E", stroke=INK, strokeWidth=4)
# papers peeking out
d.path("M442,700 L570,700 L566,724 L446,724 Z", "Papers", fill="#F4EEE0",
       stroke=INK, strokeWidth=3)
# front panel
d.path("M424,714 C424,706 430,702 438,702 L572,702 C580,702 586,708 586,716 "
       "L590,758 C590,768 584,776 574,776 L438,776 C428,776 422,768 422,758 Z",
       "Folder front", fill=FOLDER_GRAD, stroke=INK, strokeWidth=4)
d.path("M444,744 L566,744", "Folder crease", fill=NONE, stroke="#A08050",
       strokeWidth=3, opacity=60, cap="round")

# --- the clerk beside the trunk, gesturing at the split -----------------------------
d.path("M222,742 C210,646 222,576 256,522 C278,488 370,488 392,522 "
       "C426,576 438,646 426,742 C398,762 362,768 324,768 "
       "C286,768 250,762 222,742 Z",
       "Robe", fill=ROBE_GRAD, stroke=INK, strokeWidth=6)
d.path("M276,600 C270,652 268,706 274,748", "Fold L", fill=NONE,
       stroke="#4E3E62", strokeWidth=4, opacity=55, cap="round")
d.path("M372,600 C378,652 380,706 374,748", "Fold R", fill=NONE,
       stroke="#4E3E62", strokeWidth=4, opacity=55, cap="round")
d.shape("ellipse", "Dome light", x=256, y=505, width=120, height=44,
        fill="#FFFFFF", opacity=16, stroke=NONE)
# raised arm reaching right toward the junction
d.path("M408,596 C448,580 466,568 482,556", "Arm R", fill=NONE,
       stroke="#86769E", strokeWidth=26, cap="round")
d.shape("ellipse", "Hand R", x=474, y=536, width=36, height=32,
        fill="#C4B6D4", stroke=INK, strokeWidth=4)
# face looking up at the fork
d.shape("ellipse", "Eye L", x=278, y=536, width=36, height=44,
        fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye R", x=344, y=536, width=36, height=44,
        fill="#FFFFFF", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=296, y=544, width=15, height=20,
        fill="#241E2C", stroke=NONE)
d.shape("ellipse", "Pupil R", x=362, y=544, width=15, height=20,
        fill="#241E2C", stroke=NONE)
d.shape("ellipse", "Glint L", x=299, y=548, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=365, y=548, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M276,540 C286,526 306,524 316,532", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M342,532 C352,524 372,526 382,540", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.path("M308,606 C320,614 334,614 346,606", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# collar tabs
d.path("M294,634 L324,658 L294,670 Z", "Collar L", fill="#F4EEE0",
       stroke=INK, strokeWidth=3)
d.path("M354,634 L324,658 L354,670 Z", "Collar R", fill="#F4EEE0",
       stroke=INK, strokeWidth=3)

# junction node on top of everything at the fork
d.shape("ellipse", "Junction", x=JX-17, y=JY-17, width=34, height=34,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F0E8F6"}, {"offset": 1, "color": "#8A76A4"}]}},
        stroke=INK, strokeWidth=4)

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

NAME = "SC-Λ CARE/CONTINUITY SPLIT"
d.text(NAME, "Name", x=500, y=930, size=46, font="Virelai Sans",
       color="#EAE4F0", justify="center")
tid = text_id(NAME)
if tid:
    digit_font(tid, NAME)

ROLE = "THREE STORIES ONE CASE NUMBER"
d.text(ROLE, "Role", x=500, y=968, size=23,
       font="Virelai Sans", color="#A89CC0", justify="center")
rid = text_id(ROLE)
if rid:
    d.cmd("text.setStyle", "role tracking", id=rid, tracking=280)

d.finish("079.sc-lambda-care-continuity-split-V1R00")
