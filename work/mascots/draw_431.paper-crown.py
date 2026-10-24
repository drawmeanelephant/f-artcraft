#!/usr/bin/env python3
"""Paper Crown — mascot portrait V1R00. HTTP 431, "Request Header Fields
Too Large". Mascot in a badge-covered jacket wearing a folded paper crown,
knees buckling under the weight. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Paper Crown — Mascot Portrait", 1000, 1000)

INK = "#3A2A24"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#241418"}, {"offset": 1, "color": "#0F090C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8D9BE"}, {"offset": 0.7, "color": "#C4A988"},
    {"offset": 1, "color": "#8E7156"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8E7156"}, {"offset": 1, "color": "#5E4836"}]}}
JACKET = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#76845A"}, {"offset": 0.75, "color": "#55633E"},
    {"offset": 1, "color": "#3A4528"}]}}
SLEEVE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E6C44"}, {"offset": 1, "color": "#3A4528"}]}}
TROUSER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#57493C"}, {"offset": 1, "color": "#362B22"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2DAB8"}, {"offset": 1, "color": "#CFA880"}]}}
NEWS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#ECE9DE"}, {"offset": 1, "color": "#BDB8A6"}]}}
SHOE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3A30"}, {"offset": 1, "color": "#241A14"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E5F46", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4EADA", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(210,225,7),(778,210,6),(200,545,6),(812,548,7),
                               (240,755,7),(762,750,7),(140,400,6),(858,398,6),
                               (360,138,7),(630,132,6),(310,810,6),(688,806,7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#7E5F46", opacity=42, stroke=NONE)

# --- floor band closed on the disc's own arc ----------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#4E3A2A",
       strokeWidth=4, opacity=60)

# --- buckling legs + planted feet ---------------------------------------------
d.shape("ellipse", "Figure shadow", x=360, y=726, width=290, height=26,
        fill="#5E4836", opacity=45, stroke=NONE)
d.path("M482,592 C462,622 442,652 436,706", "Leg L",
       fill=NONE, stroke="#4A3E34", strokeWidth=38, cap="round")
d.path("M518,592 C538,622 558,652 564,706", "Leg R",
       fill=NONE, stroke="#4A3E34", strokeWidth=38, cap="round")
# knees bow outward under the load
d.shape("ellipse", "Knee L", x=410, y=636, width=42, height=36,
        fill=TROUSER, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Knee R", x=548, y=636, width=42, height=36,
        fill=TROUSER, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Shoe L", x=394, y=700, width=82, height=34,
        fill=SHOE, stroke=INK, strokeWidth=5, radius=14)
d.shape("rectangle", "Shoe R", x=524, y=700, width=82, height=34,
        fill=SHOE, stroke=INK, strokeWidth=5, radius=14)
# strain wobble marks by the knees
d.path("M396,632 L384,622 M604,636 L616,626 M402,664 L390,660 M598,666 L610,662",
       "Knee wobble", fill=NONE, stroke=INK, strokeWidth=3.5, cap="round", opacity=50)

# --- the badge-covered jacket, slumped ----------------------------------------
d.path("M408,606 C398,512 412,438 448,406 C474,384 526,384 552,406 "
       "C588,438 602,512 592,606 C560,620 440,620 408,606 Z",
       "Jacket", fill=JACKET, stroke=INK, strokeWidth=6, join="round")
# lapel V + button placket
d.path("M472,404 L500,446 L528,404", "Lapels", fill=NONE, stroke=INK,
       strokeWidth=5, join="round")
d.path("M500,446 L500,604", "Placket", fill=NONE, stroke=INK, strokeWidth=4, opacity=60)
# sagging pocket flaps
d.path("M424,540 L470,540 L466,566 L428,566 Z", "Pocket L",
       fill="#4A5734", stroke=INK, strokeWidth=3.5, join="round")
d.path("M530,540 L576,540 L572,566 L534,566 Z", "Pocket R",
       fill="#4A5734", stroke=INK, strokeWidth=3.5, join="round")

# badges: every header field ever sent, pinned on
BADGES = [
    # (x, y, r, color, kind)
    (448, 452, 14, "#C85848", "dot"), (500, 458, 15, "#D8A848", "star"),
    (552, 452, 14, "#4E9A8E", "dot"), (430, 496, 12, "#8A6AA8", "dot"),
    (474, 500, 13, "#5E7EB8", "ring"), (526, 500, 13, "#C85848", "ring"),
    (570, 494, 12, "#D8A848", "dot"), (452, 582, 12, "#4E9A8E", "ring"),
    (500, 586, 13, "#8A6AA8", "star"), (548, 582, 12, "#5E7EB8", "dot"),
]
for i, (x, y, r, col, kind) in enumerate(BADGES):
    d.shape("ellipse", f"Badge {i+1}", x=x-r, y=y-r, width=2*r, height=2*r,
            fill={"gradient": {"kind": "radial", "stops": [
                {"offset": 0, "color": "#FFFFFF"}, {"offset": 0.25, "color": col},
                {"offset": 1, "color": col}]}},
            stroke=INK, strokeWidth=3.5)
    if kind == "dot":
        d.shape("ellipse", f"Badge {i+1} pip", x=x-3.5, y=y-3.5, width=7, height=7,
                fill=INK, opacity=70, stroke=NONE)
    elif kind == "ring":
        d.shape("ellipse", f"Badge {i+1} ring", x=x-6, y=y-6, width=12, height=12,
                fill=NONE, stroke=INK, strokeWidth=3, opacity=60)
    else:
        d.path(f"M{x},{y-5} L{x+2},{y-1} L{x+6},{y-1} L{x+3},{y+2} L{x+4},{y+6} "
               f"L{x},{y+4} L{x-4},{y+6} L{x-3},{y+2} L{x-6},{y-1} L{x-2},{y-1} Z",
               f"Badge {i+1} star", fill=INK, opacity=65, stroke=NONE)
# a badge pops off — headers still arriving
d.shape("ellipse", "Badge falling", x=604, y=598, width=22, height=22,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FFFFFF"}, {"offset": 0.3, "color": "#C85848"},
            {"offset": 1, "color": "#C85848"}]}},
        stroke=INK, strokeWidth=3.5)
d.path("M622,574 L634,566 M632,596 L646,592", "Pop ticks", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round", opacity=60)
d.shape("ellipse", "Badge dropped", x=466, y=730, width=20, height=16,
        fill="#D8A848", stroke=INK, strokeWidth=3, opacity=85)
d.shape("ellipse", "Badge dropped 2", x=548, y=740, width=18, height=14,
        fill="#4E9A8E", stroke=INK, strokeWidth=3, opacity=85)

# --- arms braced on knees, straining ------------------------------------------
d.path("M446,424 C414,458 404,540 418,622", "Sleeve L",
       fill=NONE, stroke="#55633E", strokeWidth=26, cap="round")
d.path("M554,424 C586,458 596,540 582,622", "Sleeve R",
       fill=NONE, stroke="#55633E", strokeWidth=26, cap="round")
# cuff rings
d.path("M412,604 L428,596 M588,604 L572,596", "Cuffs", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=70)
d.shape("ellipse", "Hand L", x=404, y=614, width=34, height=28,
        fill=SKIN, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=562, y=614, width=34, height=28,
        fill=SKIN, stroke=INK, strokeWidth=4)

# --- head tucked low into the shoulders ---------------------------------------
d.shape("ellipse", "Head", x=436, y=290, width=128, height=108,
        fill=SKIN, stroke=INK, strokeWidth=6)
# squeezed-shut eyes
d.path("M452,344 L466,352 L452,360", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round", join="round")
d.path("M548,344 L534,352 L548,360", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round", join="round")
# gritted teeth
d.shape("rectangle", "Teeth", x=470, y=372, width=60, height=20,
        fill="#F4EADA", stroke=INK, strokeWidth=4, radius=5)
d.path("M485,374 L485,390 M500,374 L500,390 M515,374 L515,390",
       "Teeth grit", fill=NONE, stroke=INK, strokeWidth=3, opacity=75)
# sweat
d.path("M432,318 C424,330 424,340 432,344 C440,340 440,330 432,318 Z",
       "Sweat L", fill="#BEE0E8", stroke=INK, strokeWidth=3, opacity=85)
d.path("M570,312 C562,324 562,334 570,338 C578,334 578,324 570,312 Z",
       "Sweat R", fill="#BEE0E8", stroke=INK, strokeWidth=3, opacity=85)

# --- the paper crown, folded newsprint, tipped and heavy ----------------------
# band sits across the head, tilted ~-6 deg
d.path("M434,318 L572,304 L568,268 L440,280 Z", "Crown band",
       fill=NEWS, stroke=INK, strokeWidth=5, join="round")
# zigzag points: four peaks, rightmost flopping over
d.path("M440,280 L446,222 L472,262 L498,206 L524,258 L550,216 L556,270 Z",
       "Crown points", fill=NEWS, stroke=INK, strokeWidth=5, join="round")
d.path("M550,216 C570,224 576,244 568,264", "Flopped tip",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round", opacity=55)
# newsprint column lines on the band and one point
d.path("M448,292 L560,281 M449,302 L561,291", "Print band", fill=NONE,
       stroke="#8F8A7A", strokeWidth=2.5, opacity=70)
d.path("M455,270 L470,240 M462,272 L476,246", "Print point", fill=NONE,
       stroke="#8F8A7A", strokeWidth=2.5, opacity=55)
# crease shadows where it folds
d.path("M498,206 L500,258 M550,216 L552,268", "Crease", fill=NONE,
       stroke="#8F8A7A", strokeWidth=2.5, opacity=45)

# --- name + role ---------------------------------------------------------------
d.text("PAPER CROWN", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#F0E4D2", justify="center")
d.text(" ".join("REQUEST HEADER FIELDS TOO LARGE"), "Role", x=500, y=968, size=23,
       font="Virelai Sans", color="#C9A88E", justify="center")

d.finish("431.paper-crown-V1R00")
