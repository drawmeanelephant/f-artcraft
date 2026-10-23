#!/usr/bin/env python3
"""Wrong Door Finch — mascot portrait V1R00. HTTP 421, "Misdirected Request".
Finch perched on a window sill, beak tapping the glass pane. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Wrong Door Finch — Mascot Portrait", 1000, 1000)

INK = "#3E2B33"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#241C33"}, {"offset": 1, "color": "#0E0A16"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DDE4EE"}, {"offset": 0.7, "color": "#A9B5C9"},
    {"offset": 1, "color": "#6F7C99"}]}}
GLASS_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FFDF96"}, {"offset": 0.55, "color": "#F2B45C"},
    {"offset": 1, "color": "#C8813C"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F7D77A"}, {"offset": 0.6, "color": "#E8AC44"},
    {"offset": 1, "color": "#B97A28"}]}}
WING_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A5A34"}, {"offset": 1, "color": "#5E3B22"}]}}

# --- backdrop + plate --------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5C6B8C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E9EFF6", strokeWidth=3, opacity=55)
# dusk speckles on the plate
for i, (x, y, w) in enumerate([(200,200,7),(790,190,6),(240,700,7),(740,720,6),(160,430,6),
                               (840,450,7),(330,140,6),(660,130,7),(450,810,6),(590,815,6)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5C6B8C", opacity=40, stroke=NONE)
# a few early stars
for i, (x, y) in enumerate([(255,255),(755,265),(210,540),(800,590),(500,170)]):
    d.path(f"M{x-8},{y} L{x+8},{y} M{x},{y-8} L{x},{y+8}", f"Star {i+1}",
           fill=NONE, stroke="#EAF0F8", strokeWidth=3.5, opacity=45, cap="round")

# --- window --------------------------------------------------------------------
# glow halo behind the frame
d.shape("rectangle", "Window glow", x=370, y=180, width=330, height=470,
        radius=14, fill="#F2B45C", opacity=28, stroke=NONE)
# frame
d.shape("rectangle", "Window frame", x=385, y=195, width=300, height=440,
        radius=8, fill="#5E4632", stroke=INK, strokeWidth=5)
# glass, two panes with muntin cross
d.shape("rectangle", "Glass", x=405, y=215, width=260, height=400,
        fill=GLASS_GRAD, stroke=INK, strokeWidth=4)
d.path("M535,215 L535,615 M405,415 L665,415", "Muntins",
       fill=NONE, stroke="#5E4632", strokeWidth=10)
d.path("M535,215 L535,615 M405,415 L665,415", "Muntin ink",
       fill=NONE, stroke=INK, strokeWidth=3, opacity=60)
# glass sheen
d.path("M430,240 L500,240 L450,400 L420,400 Z", "Sheen", fill="#FFFFFF", opacity=18, stroke=NONE)
# curtains hinted at top corners
d.path("M405,215 C430,240 432,280 405,300 Z", "Curtain L", fill="#8A4438", opacity=70, stroke=NONE)
d.path("M665,215 C640,240 638,280 665,300 Z", "Curtain R", fill="#8A4438", opacity=70, stroke=NONE)
# sill
d.shape("rectangle", "Sill", x=355, y=635, width=360, height=30,
        radius=6, fill="#6E5238", stroke=INK, strokeWidth=5)
d.shape("rectangle", "Sill shadow", x=365, y=665, width=340, height=18,
        radius=8, fill="#2C1E14", opacity=35, stroke=NONE)

# --- tap ripples on the glass, centered on the beak's contact point -------------
for i, r in enumerate([13, 24, 35]):
    d.path(f"M{406+r},{497-r*0.8} A{r},{r} 0 0 1 {406+r},{497+r*0.8}", f"Tap ripple {i+1}",
           fill=NONE, stroke="#FFF2CF", strokeWidth=4, opacity=75 - i*15, cap="round")

# --- finch (on the sill, facing the glass) ---------------------------------------
# tail, angled down-left
d.path("M286,610 C268,632 252,664 246,700 L236,716 C234,724 244,728 250,722 "
       "C272,700 292,668 302,632 Z", "Tail", fill=WING_GRAD, stroke=INK, strokeWidth=5, join="round")
# body
d.shape("ellipse", "Body", x=270, y=505, width=130, height=118,
        fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# belly
d.shape("ellipse", "Belly", x=292, y=548, width=82, height=62,
        fill="#FBEBBE", opacity=85, stroke=NONE)
# wing
d.path("M292,540 C272,556 270,590 292,608 C318,624 352,614 360,590 "
       "C366,566 348,544 320,536 C310,533 300,534 292,540 Z",
       "Wing", fill=WING_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M296,586 C312,598 336,598 348,586", "Wing bar",
       fill=NONE, stroke="#F2D98C", strokeWidth=6, cap="round", opacity=80)
# head
d.shape("ellipse", "Head", x=342, y=452, width=104, height=96,
        fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# cap
d.path("M352,478 C360,452 384,438 408,444 C394,460 380,472 370,488 Z",
       "Cap", fill="#7A4A28", stroke=NONE)
# cheek blush
d.shape("ellipse", "Cheek", x=382, y=510, width=30, height=14, fill="#E07840", opacity=45, stroke=NONE)
# beak pressed to the glass (tip overlaps the pane edge at x=406)
d.path("M436,484 L404,496 L436,510 C444,499 444,491 436,484 Z",
       "Beak", fill="#D96A3A", stroke=INK, strokeWidth=4, join="round")
# eye, slightly anxious — looking at the pane
d.shape("ellipse", "Eye", x=388, y=472, width=22, height=26, fill="#33222A", stroke=NONE)
d.shape("ellipse", "Glint", x=393, y=477, width=7, height=7, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M384,462 C392,456 402,455 410,459", "Brow",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round", opacity=70)
# legs + feet gripping sill edge
d.path("M316,620 L314,638 M356,620 L358,638", "Legs",
       fill=NONE, stroke="#8A5A34", strokeWidth=5, cap="round")
d.path("M304,638 L326,638 M346,638 L370,638", "Feet",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")

# --- name + role ------------------------------------------------------------------
d.text("WRONG DOOR FINCH", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E0E8F2", justify="center")
d.text(" ".join("MISDIRECTED REQUEST"), "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#9AACC6", justify="center")

d.finish("421.wrong-door-finch-V1R00")
