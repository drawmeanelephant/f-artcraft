#!/usr/bin/env python3
"""Kindness Template — mascot portrait V1R00.
A support reply template, mid-draft: warm boilerplate around cold
violet fill-in fields — [CUSTOMER_NAME], [ISSUE_TYPE],
[INSERT_SYMPATHY_VARIABLE]. Below, the phrase library holds the longer
sympathies, truncated to their cost ceiling. The cursor blinks on.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Kindness Template — Mascot Portrait", 1000, 1000)

INK = "#2C2438"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E1A32"}, {"offset": 1, "color": "#0B0916"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E5680"}, {"offset": 0.7, "color": "#3A3354"},
    {"offset": 1, "color": "#1C1830"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#403858"}, {"offset": 1, "color": "#181228"}]}}
CARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4EEDA"}, {"offset": 1, "color": "#D8CCB0"}]}}
CHIP = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A8CE0"}, {"offset": 1, "color": "#6A56BC"}]}}
CHIP_GLOW = "#8E80D8"
GREEN = "#4EC98A"
BODY = "#4E4460"
MUTE = "#8A80A0"

def chip(x, y, w, label, name):
    """template field chip: violet pill + bracketed token"""
    d.shape("rectangle", name, x=x, y=y, width=w, height=26,
            fill=CHIP, stroke=INK, strokeWidth=3, radius=13)
    d.text(f"[{label}]", f"{name} text", x=x + w/2, y=y + 18, size=12.5,
           font="Virelai Sans", color="#F2EDFF", justify="center")

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8E84B8", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8D0F0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(196,240,8),(798,236,7),(162,524,9),(832,548,8),
                               (250,762,7),(750,746,9),(136,394,6),(862,396,7),
                               (396,114,7),(610,112,8),(336,820,6),(664,816,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#443C66", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0814",
       strokeWidth=4, opacity=70)

# --- the template card -------------------------------------------------------------
d.shape("ellipse", "Card shadow", x=220, y=694, width=560, height=30,
        fill="#060410", opacity=50, stroke=NONE)
d.shape("rectangle", "Card foot L", x=272, y=698, width=56, height=26,
        fill="#221C38", stroke=INK, strokeWidth=4, radius=6)
d.shape("rectangle", "Card foot R", x=672, y=698, width=56, height=26,
        fill="#221C38", stroke=INK, strokeWidth=4, radius=6)
d.shape("rectangle", "Card", x=230, y=238, width=540, height=470,
        fill=CARD, stroke=INK, strokeWidth=5, radius=18)
# titlebar
d.path("M230,288 L770,288", "Titlebar rule", fill=NONE, stroke=INK,
       strokeWidth=3, opacity=45)
for i, c in enumerate(("#E0705E", "#E8C05E", "#6AC88A")):
    d.shape("ellipse", f"Win dot {i+1}", x=250 + i * 24, y=256, width=13, height=13,
            fill=c, stroke=NONE, opacity=85)
d.text("SUPPORT REPLY — TEMPLATE", "Window title", x=346, y=272, size=14,
       font="Virelai Sans", color="#6A5E80")

# body: warm words, cold fields -----------------------------------------------
# line 1: DEAR [CUSTOMER_NAME],
d.text("Dear", "L1 a", x=268, y=330, size=19, font="Source Sans 3", color=BODY)
chip(322, 308, 132, "CUSTOMER_NAME", "Field name")
d.text(",", "L1 b", x=460, y=330, size=19, font="Source Sans 3", color=BODY)
# line 2: We are so sorry about your [ISSUE_TYPE].
d.text("We are so sorry about your", "L2 a", x=268, y=372, size=19,
       font="Source Sans 3", color=BODY)
chip(506, 350, 112, "ISSUE_TYPE", "Field issue")
d.text(".", "L2 b", x=624, y=372, size=19, font="Source Sans 3", color=BODY)
# line 3: Please accept our [INSERT_SYMPATHY_VARIABLE]
d.text("Please accept our", "L3 a", x=268, y=414, size=19,
       font="Source Sans 3", color=BODY)
chip(430, 392, 212, "INSERT_SYMPATHY_VARIABLE", "Field sympathy")
d.shape("ellipse", "Sympathy glow", x=428, y=388, width=216, height=34,
        fill=CHIP_GLOW, opacity=14, stroke=NONE)
# line 4: It lets us [EMOTION_NOUN] with you.
d.text("It lets us", "L4 a", x=268, y=456, size=19,
       font="Source Sans 3", color=BODY)
chip(358, 434, 124, "EMOTION_NOUN", "Field emotion")
d.text("with you.", "L4 b", x=490, y=456, size=19, font="Source Sans 3",
       color=BODY)
# line 5: the deadpan footer of every Empathegy 2.0 reply
d.text("No further action is required.", "L5", x=268, y=498, size=19,
       font="Source Sans 3", color=BODY)
# blinking cursor, still drafting warmth
d.shape("rectangle", "Cursor", x=268, y=516, width=9, height=22,
        fill="#6A56BC", stroke=NONE, opacity=85)

# signature: warmth, unit-supplied
d.text("With warmth,", "Sig 1", x=268, y=566, size=19, font="Source Sans 3",
       color=BODY)
d.path("M398,558 C402,550 412,550 414,558 C416,550 426,550 430,558 "
       "C430,566 420,572 414,576 C408,572 398,566 398,558 Z",
       "Sig heart", fill="#B85A78", stroke=INK, strokeWidth=2, opacity=85)
d.text("AUTOMATED CARE UNIT", "Sig 2", x=268, y=592, size=12,
       font="Virelai Sans", color=MUTE)
# SEND REPLY, always within budget
d.shape("rectangle", "Send pill", x=596, y=558, width=134, height=34,
        fill=GREEN, stroke=INK, strokeWidth=3, radius=17, opacity=90)
d.text("SEND REPLY", "Send text", x=663, y=580, size=13,
       font="Virelai Sans", color="#F0FBF4", justify="center")

# phrase library: the longer sympathies, truncated to the cost ceiling --------
d.path("M230,616 L770,616", "Library rule", fill=NONE, stroke=INK,
       strokeWidth=2, opacity=35)
d.text("PHRASE LIBRARY", "Library label", x=250, y=644, size=12,
       font="Virelai Sans", color=MUTE)
d.text("MAX LENGTH SET BY BUDGET", "Library note", x=750, y=644, size=11,
       font="Virelai Sans", color=MUTE, justify="right")
chip(250, 656, 192, "SINCERITY_PHRASE_LON…", "Lib chip 1")
chip(452, 656, 146, "CLOSING_PLATI…", "Lib chip 2")
chip(608, 656, 128, "WARMTH_TOKEN", "Lib chip 3")

# --- captions ---------------------------------------------------------------------------
d.text("KINDNESS TEMPLATE", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#E4DEF4", justify="center")
r = d.text("SYMPATHY, TRUNCATED TO BUDGET", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A89ECB", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("234.kindness-template-V1R00")
