#!/usr/bin/env python3
"""LIM-0441 Predictive Pete — limerick plate V1R00. Predictive policing:
a small child silhouette walks toward a schoolhouse while a database
tag the size of his torso stays wired to his wrist; the record never
expires, and a dashed loop of circular logic closes around the tag.
Institutional slate-khaki palette, warm dark ink. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LIM-0441 Predictive Pete — Limerick Plate", 1000, 1000)

INK = "#20201A"
CREAM = "#F0E4C8"
TAN = "#B0A888"
RED = "#B8402E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#14160F"}, {"offset": 1, "color": "#090A06"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5C6050"}, {"offset": 0.7, "color": "#363A2C"},
    {"offset": 1, "color": "#1A1C12"}]}}
COAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#565044"}, {"offset": 1, "color": "#2E2A20"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E0CCA6"}, {"offset": 0.75, "color": "#B69C74"},
    {"offset": 1, "color": "#806C4C"}]}}
TAGPAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4D8BC"}, {"offset": 1, "color": "#BCAF90"}]}}
STEEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#525A54"}, {"offset": 1, "color": "#2C322C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E7050", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D8B8", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(175, 230, 8), (815, 210, 7), (145, 540, 9),
                               (850, 590, 8), (250, 750, 7), (720, 745, 8),
                               (125, 400, 6), (865, 430, 7), (360, 135, 7),
                               (640, 145, 8)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#464830", opacity=40, stroke=NONE)

# --- the gang database: a steel cylinder of records, top right ----------------------
d.shape("ellipse", "DB top", x=640, y=270, width=170, height=44,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#6A7268"}, {"offset": 1, "color": "#3E463E"}]}},
        stroke=INK, strokeWidth=4)
d.path("M640,292 L640,470 A85,22 0 0 0 810,470 L810,292",
       "DB body", fill=STEEL, stroke=INK, strokeWidth=4)
for i, ry in enumerate([340, 395]):
    d.path(f"M640,{ry} A85,22 0 0 0 810,{ry}", f"DB seam {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3, opacity=70)
d.text("GANG DB", "DB label", x=725, y=378, size=19, font="Virelai Sans",
       color="#C9C4A8", justify="center")
d.text("JUVENILE FILE", "DB sub", x=725, y=404, size=11,
       font="Virelai Sans", color="#8E8A70", justify="center")
# record card sticking out — it never comes all the way out
d.shape("rectangle", "Record card", x=678, y=216, width=96, height=64,
        radius=4, fill=TAGPAPER, stroke=INK, strokeWidth=3)
d.path("M688,232 L764,232 M688,246 L748,246 M688,260 L756,260",
       "Card lines", fill=NONE, stroke=INK, strokeWidth=2.5, opacity=65)
d.path("M688,232 L764,232", "Card redact", fill=NONE, stroke=RED,
       strokeWidth=5, opacity=85)
# cold-storage snowflakes on the cylinder — the record goes cold, never dies
for i, (sx, sy) in enumerate([(664, 430), (700, 445), (672, 460)]):
    d.path(f"M{sx},{sy} l8,8 M{sx + 8},{sy} l-8,8", f"Cold mark {i+1}",
           fill=NONE, stroke="#9AB0B8", strokeWidth=2.5, opacity=70,
           cap="round")

# --- the tag: database label the size of the child ------------------------------------
d.shape("ellipse", "Tag shadow", x=180, y=730, width=230, height=18,
        fill="#0E0F08", opacity=40, stroke=NONE)
# luggage-tag body, slightly tilted
d.path("M210,540 L330,505 L395,570 L395,730 L210,730 Z",
       "Tag body", fill=TAGPAPER, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Tag hole", x=338, y=536, width=22, height=22,
        fill="#1A1C12", stroke=INK, strokeWidth=3)
d.path("M214,545 L334,510", "Tag top edge", fill=NONE, stroke=INK,
       strokeWidth=2, opacity=40)
d.text("GANG DB", "Tag header", x=302, y=592, size=24,
       font="Virelai Sans", color=INK, justify="center")
d.path("M240,604 L364,604", "Tag rule", fill=NONE, stroke=INK,
       strokeWidth=2.5, opacity=60)
d.text("SUBJECT: MINOR", "Tag line 1", x=302, y=632, size=14,
       font="Virelai Sans", color="#3E3428", justify="center")
d.text("STATUS: ACTIVE", "Tag line 2", x=302, y=658, size=14,
       font="Virelai Sans", color="#3E3428", justify="center")
d.text("EXPIRES: NEVER", "Tag line 3", x=302, y=684, size=14,
       font="Virelai Sans", color=RED, justify="center")
# barcode along the tag bottom
for i, bx in enumerate([232, 240, 248, 258, 264, 276, 284, 292, 304, 312,
                        322, 330, 342, 350]):
    w = 2 if i % 3 else 3.5
    d.path(f"M{bx},700 L{bx},718", f"Tag bar {i+1}", fill=NONE, stroke=INK,
           strokeWidth=w)
# circular logic: a dashed orbit that closes back on the tag
d.path("M302,470 A150,60 0 1 1 300,470", "Logic loop", fill=NONE,
       stroke="#C9C4A8", strokeWidth=3, dash=[9, 7], opacity=55)
d.path("M300,470 L316,462 L314,480 Z", "Loop arrowhead", fill="#C9C4A8",
       opacity=70, stroke=NONE)

# --- Pete: small, backpack on, walking right toward school -----------------------------
d.shape("ellipse", "Pete shadow", x=470, y=722, width=150, height=16,
        fill="#0E0F08", opacity=45, stroke=NONE)
# long shadow reaching toward the schoolhouse
d.path("M540,726 L760,700 L760,724 L540,738 Z", "Long shadow",
       fill="#0E0F08", opacity=30, stroke=NONE)
# backpack
d.shape("rectangle", "Backpack", x=452, y=580, width=34, height=52,
        radius=8, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#7A4A34"},
            {"offset": 1, "color": "#4A2C1E"}]}},
        stroke=INK, strokeWidth=4)
d.path("M486,592 L496,592", "Pack strap", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
# body — smaller than the tag
d.path("M486,566 L544,566 L556,720 L474,720 Z", "Pete coat", fill=COAT,
       stroke=INK, strokeWidth=5, join="round")
d.path("M496,580 L490,700", "Coat sheen", fill=NONE, stroke="#E4D8B8",
       strokeWidth=5, opacity=14, cap="round")
# legs mid-stride
d.path("M494,720 L488,748", "Leg back", fill=NONE, stroke=INK,
       strokeWidth=11, cap="round")
d.path("M534,720 L546,748", "Leg front", fill=NONE, stroke=INK,
       strokeWidth=11, cap="round")
# head, tipped down under the weight of the label
d.shape("ellipse", "Pete head", x=488, y=512, width=52, height=52,
        fill=SKIN, stroke=INK, strokeWidth=5)
# baseball cap
d.path("M490,528 A26,22 0 0 1 540,526 L556,530 L540,538 Z",
       "Cap", fill=COAT, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Cap button", x=512, y=506, width=8, height=8,
        fill=INK, stroke=NONE)
# downcast eye
d.shape("ellipse", "Pete eye", x=506, y=538, width=8, height=9,
        fill=INK, stroke=NONE)
d.path("M504,556 Q514,551 524,556", "Small frown", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
# left arm trailing back — the wire to the tag ties at the wrist
d.path("M488,584 C470,600 458,616 448,634", "Pete arm", fill=NONE,
       stroke="#3A3428", strokeWidth=16, cap="round")
d.shape("ellipse", "Pete hand", x=438, y=626, width=20, height=19,
        fill=SKIN, stroke=INK, strokeWidth=3.5)
# the wire: tag hole to wrist, slightly taut
d.path("M349,548 C390,570 420,600 444,630", "Tag wire", fill=NONE,
       stroke=RED, strokeWidth=3.5, cap="round", dash=[7, 5])

# --- the schoolhouse, small and far -------------------------------------------------
d.path("M700,668 L700,724 L800,724 L800,668", "School walls", fill=NONE,
       stroke="#8E8A70", strokeWidth=4, opacity=80)
d.path("M692,670 L750,632 L808,670", "School roof", fill=NONE,
       stroke="#8E8A70", strokeWidth=4, opacity=80)
d.path("M742,724 L742,694 L758,694 L758,724", "School door", fill=NONE,
       stroke="#8E8A70", strokeWidth=3, opacity=70)
d.path("M750,632 L750,612 L766,619 L750,626", "School flag", fill=NONE,
       stroke="#8E8A70", strokeWidth=3, opacity=70)

# --- key line + name + role ---------------------------------------------------------
r = d.text("A LABEL THAT NOTHING CAN SOLDER.", "Key line", x=500, y=782,
           size=22, font="Virelai Sans", color=CREAM, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key line tracking", ids=[r["id"]], tracking=60)
d.text("PREDICTIVE PETE", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("NEVER CHARGED, NEVER TOLD", "Role", x=500, y=967, size=20,
           font="Virelai Sans", color=TAN, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=170)

d.finish("lim-0441-predictive-pete-V1R00")
