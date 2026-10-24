#!/usr/bin/env python3
"""rc-new.sh — The New Plot. Necropolis plate V1R00.
A fresh blank headstone being carried to an empty plot, its face already
stenciled with frontmatter — title, date, draft — waiting for a name to
be written in. Markdown, Textile, or Cooklang: the cemetery accepts all
denominations. Pale stone, hopeful light. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("RC-New — Necropolis Plate", 1000, 1000)

INK = "#232830"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#12161E"}, {"offset": 1, "color": "#080A10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#565E72"}, {"offset": 0.7, "color": "#343A4A"},
    {"offset": 1, "color": "#151824"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A3040"}, {"offset": 1, "color": "#10141E"}]}}
STONE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8DCE6"}, {"offset": 1, "color": "#949CAE"}]}}
STONE_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A92A4"}, {"offset": 1, "color": "#565E70"}]}}
SMOCK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C5244"}, {"offset": 1, "color": "#332C22"}]}}
SOIL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3A28"}, {"offset": 1, "color": "#241A10"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6A4E30"}, {"offset": 1, "color": "#3E2A18"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A8496", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DDE2EC", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5C6478", opacity=35, stroke=NONE)

# --- hopeful light: a soft shaft leaning in from the upper right -----------------
d.path("M645,150 L775,150 L720,700 L540,700 Z", "Light shaft", fill="#E8D9B0",
       opacity=8, stroke=NONE)
d.shape("ellipse", "Light pool", x=540, y=620, width=300, height=90,
        fill="#E8D9B0", opacity=9, stroke=NONE)

# --- ranks of the already-named, fading left --------------------------------------
def old_stone(x, top, w, h, op, tag, cross=False):
    if cross:
        d.path(f"M{x+w/2-6},{top} L{x+w/2+6},{top} L{x+w/2+6},{top+18} "
               f"L{x+w/2+22},{top+18} L{x+w/2+22},{top+30} L{x+w/2+6},{top+30} "
               f"L{x+w/2+6},{top+h} L{x+w/2-6},{top+h} L{x+w/2-6},{top+30} "
               f"L{x+w/2-22},{top+30} L{x+w/2-22},{top+18} L{x+w/2-6},{top+18} Z",
               f"{tag}", fill=STONE_DK, stroke=INK, strokeWidth=3, opacity=op)
    else:
        d.path(f"M{x},{top+h} L{x},{top+16} C{x},{top} {x+w},{top} {x+w},{top+16} "
               f"L{x+w},{top+h} Z", f"{tag}", fill=STONE_DK, stroke=INK,
               strokeWidth=3, opacity=op)
    d.path(f"M{x+8},{top+h-14} L{x+w-8},{top+h-14}", f"{tag} epitaph",
           fill=NONE, stroke="#2A3040", strokeWidth=3, opacity=op)

old_stone(190, 480, 66, 110, 55, "Old stone 1")
old_stone(285, 520, 50, 84, 42, "Old stone 2")
old_stone(360, 500, 58, 96, 48, "Old stone 3", cross=True)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0F16",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Carrier shadow", x=430, y=682, width=200, height=18,
        fill="#030408", opacity=55, stroke=NONE)

# --- the empty plot: dark pit + fresh soil mound + shovel -------------------------
d.shape("ellipse", "Pit", x=658, y=716, width=150, height=34,
        fill="#06080C", stroke=INK, strokeWidth=4)
d.path("M664,716 L802,716", "Pit rim", fill=NONE, stroke="#4A5266",
       strokeWidth=3, opacity=80, cap="round")
d.path("M640,700 C655,660 745,652 772,700 Z", "Soil mound", fill=SOIL,
       stroke=INK, strokeWidth=4, join="round")
d.path("M668,690 C690,672 730,668 752,688", "Mound highlight", fill=NONE,
       stroke="#6A5238", strokeWidth=4, opacity=60, cap="round")
# shovel struck into the mound
d.path("M700,618 L716,672", "Shovel handle", fill=NONE, stroke="#6A4E30",
       strokeWidth=7, cap="round")
d.shape("ellipse", "Shovel grip", x=693, y=606, width=18, height=14,
        fill=NONE, stroke="#6A4E30", strokeWidth=5)
d.path("M710,668 L730,668 L726,694 L714,694 Z", "Shovel blade", fill=STONE_DK,
       stroke=INK, strokeWidth=3, join="round")
# a hopeful sprig beside the plot
d.path("M806,700 C806,688 804,680 802,672 M806,690 C812,684 818,682 824,682 "
       "M806,694 C800,690 795,688 790,688", "Sprig", fill=NONE,
       stroke="#7A9455", strokeWidth=3, cap="round")

# --- the fresh blank headstone, riding a shoulder -----------------------------------
# the sexton, hunched forward mid-stride
d.path("M452,690 C460,660 470,640 488,622", "Leg back", fill=NONE,
       stroke="#3A3228", strokeWidth=16, cap="round")
d.path("M520,690 C520,662 522,646 526,626", "Leg front", fill=NONE,
       stroke="#453B2E", strokeWidth=16, cap="round")
d.path("M438,684 L478,684 L478,694 L438,694 Z", "Boot back", fill="#241C14",
       stroke=INK, strokeWidth=3, join="round")
d.path("M508,684 L548,684 L548,694 L508,694 Z", "Boot front", fill="#241C14",
       stroke=INK, strokeWidth=3, join="round")
# torso leaning under the load
d.path("M470,630 C478,590 500,566 532,556 L560,592 C540,606 528,626 524,650 Z",
       "Smock", fill=SMOCK, stroke=INK, strokeWidth=5, join="round")
# head, tucked forward under the stone's edge
d.shape("ellipse", "Head", x=452, y=560, width=36, height=38,
        fill="#C8A882", stroke=INK, strokeWidth=4)
d.path("M450,572 C448,554 488,552 488,572 L484,566 C476,558 462,558 456,566 Z",
       "Cap", fill=SMOCK, stroke=INK, strokeWidth=3, join="round")
# arms up, hands under the stone's bottom edge
d.path("M496,580 C490,562 490,548 496,534", "Arm L", fill=NONE,
       stroke="#5C5244", strokeWidth=12, cap="round")
d.path("M548,584 C556,566 560,552 562,538", "Arm R", fill=NONE,
       stroke="#5C5244", strokeWidth=12, cap="round")
d.shape("ellipse", "Hand L", x=488, y=524, width=18, height=16,
        fill="#C8A882", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Hand R", x=554, y=528, width=18, height=16,
        fill="#C8A882", stroke=INK, strokeWidth=3)

# the headstone itself — pale, blank, already stenciled
d.path("M486,530 L486,400 C486,352 656,352 656,400 L656,530 Z",
       "Blank stone", fill=STONE, stroke=INK, strokeWidth=5, join="round")
d.path("M496,524 L496,404 C496,364 646,364 646,404 L646,524",
       "Stone bevel", fill=NONE, stroke="#F0F2F8", strokeWidth=3, opacity=70)
# frontmatter stencil: fence, fields, fence
d.path("M508,420 L634,420", "Fence top", fill=NONE, stroke="#4A5266",
       strokeWidth=3, opacity=85)
for i, (ty, lbl) in enumerate([(448, "title:"), (478, "date:"),
                               (508, "draft:")]):
    d.text(lbl, f"Field {lbl}", x=512, y=ty, size=13, font="Virelai Sans",
           color="#39404E", justify="left")
    d.path(f"M560,{ty+4} L630,{ty+4}", f"Blank line {i+1}", fill=NONE,
           stroke="#6E7688", strokeWidth=2, opacity=80)
d.path("M508,526 L634,526", "Fence bottom", fill=NONE, stroke="#4A5266",
       strokeWidth=3, opacity=85)

# --- captions ------------------------------------------------------------------
d.text("RC-NEW", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E2E6F0", justify="center")
r = d.text("SCAFFOLDING THE DEAD", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A4ACC0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-new-V1R00")
