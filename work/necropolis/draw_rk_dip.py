#!/usr/bin/env python3
"""rc-dip.sh — The Sorter of Scrolls. Necropolis plate V1R00.
A robed archivist at a long table sorts scrolls into two piles — KEEP and
INTER — while the reliquary shelf behind waits to receive the obsolete.
Every document audited, nothing moved without strong evidence.
1000x1000. Gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("RC-Dip — Necropolis Plate", 1000, 1000)

INK = "#241A10"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A1410"}, {"offset": 1, "color": "#0B0805"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6B5F4E"}, {"offset": 0.7, "color": "#3B332A"},
    {"offset": 1, "color": "#1D1812"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#38302A"}, {"offset": 1, "color": "#16110C"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5C3A"}, {"offset": 1, "color": "#4A3420"}]}}
WOOD_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3420"}, {"offset": 1, "color": "#2C1E10"}]}}
PARCH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EFE3C2"}, {"offset": 1, "color": "#C9B384"}]}}
PARCH_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C9B384"}, {"offset": 1, "color": "#A08B60"}]}}
ROBE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E5A50"}, {"offset": 1, "color": "#2A2620"}]}}
SKIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#CBA87E"}, {"offset": 1, "color": "#96704C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E6455", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8CCB0", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E6250", opacity=35, stroke=NONE)

# --- the reliquary shelf behind, waiting for the obsolete ----------------------
d.path("M230,240 L770,240 L770,254 L230,254 Z", "Shelf", fill=WOOD_DK,
       stroke=INK, strokeWidth=3, join="round")
# vessels on the shelf: urns and boxed records, kept dim
for i, (x, w) in enumerate([(268,36),(330,44),(420,32),(560,38),(640,44)]):
    d.path(f"M{x},240 L{x},{240-40} C{x},{240-52} {x+w},{240-52} {x+w},{240-40} "
           f"L{x+w},240 Z", f"Vessel {i+1}", fill=WOOD_DK, opacity=55,
           stroke=INK, strokeWidth=2)
d.path("M485,240 L485,206 L535,206 L535,240 Z", "Record box", fill=WOOD_DK,
       opacity=60, stroke=INK, strokeWidth=2)
d.path("M495,216 L525,216 M495,228 L525,228", "Box slots", fill=NONE,
       stroke="#8A7454", strokeWidth=2, opacity=40)
# empty niche waiting at the shelf's left end
d.path("M700,240 L700,208 L748,208 L748,240 Z", "Empty niche", fill=NONE,
       stroke="#8A7454", strokeWidth=2, opacity=45)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0A0704",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Table shadow", x=230, y=686, width=540, height=22,
        fill="#040302", opacity=55, stroke=NONE)
d.shape("ellipse", "Keeper shadow", x=360, y=684, width=140, height=16,
        fill="#040302", opacity=45, stroke=NONE)

# --- the archivist's robed body (the table will take the hem) --------------------
d.path("M370,620 L366,430 C366,385 385,345 425,338 C465,332 488,360 490,400 "
       "L496,620 Z", "Robe", fill=ROBE, stroke=INK, strokeWidth=5, join="round")
# robe folds
for i, (x0, y0, x1, y1) in enumerate([(390,430,384,610),(430,420,436,610),
                                      (462,415,472,605)]):
    d.path(f"M{x0},{y0} C{x0+4},{y0+60} {x1-4},{y1-60} {x1},{y1}",
           f"Robe fold {i+1}", fill=NONE, stroke="#1C1812", strokeWidth=3,
           opacity=50)
# hood and shadowed face, bent to the work
d.shape("ellipse", "Head", x=404, y=306, width=52, height=54,
        fill=SKIN, stroke=INK, strokeWidth=4)
d.path("M398,352 C390,318 404,296 432,292 C460,288 478,308 476,338 L462,330 "
       "C450,318 424,316 410,330 Z", "Hood", fill=ROBE, stroke=INK,
       strokeWidth=4, join="round")
# face in hood shadow: a dim plane, one eye catching the lamp
d.path("M414,330 C418,322 442,320 452,330 L450,346 C440,352 420,350 415,344 Z",
       "Face shade", fill="#1E150E", opacity=55, stroke=NONE)
d.shape("ellipse", "Eye", x=440, y=334, width=6, height=6,
        fill="#E8DCBE", opacity=80, stroke=NONE)

# --- the long table -------------------------------------------------------------
d.path("M220,580 L780,580 L806,612 L194,612 Z", "Table top", fill=WOOD,
       stroke=INK, strokeWidth=4, join="round")
d.path("M194,612 L806,612 L806,664 L194,664 Z", "Table front", fill=WOOD_DK,
       stroke=INK, strokeWidth=4, join="round")
# plank seams on the front
for i, x in enumerate([330, 466, 602, 738]):
    d.path(f"M{x},612 L{x},664", f"Seam {i+1}", fill=NONE, stroke="#1E1408",
           strokeWidth=2, opacity=50)
# legs down to the floor
d.path("M230,664 L230,700 L254,700 L254,664 Z", "Leg L", fill=WOOD_DK,
       stroke=INK, strokeWidth=3, join="round")
d.path("M746,664 L746,700 L770,700 L770,664 Z", "Leg R", fill=WOOD_DK,
       stroke=INK, strokeWidth=3, join="round")
# placards naming the verdicts, hung on the table front
d.path("M320,622 L320,612 M440,622 L440,612", "Tag cords", fill=NONE,
       stroke="#8A7454", strokeWidth=2)
d.path(rot_rect_path(380, 634, 92, 30, 0), "KEEP tag", fill=PARCH,
       stroke=INK, strokeWidth=3, join="round")
d.path("M560,622 L560,612 M700,622 L700,612", "Tag cords 2", fill=NONE,
       stroke="#8A7454", strokeWidth=2)
d.path(rot_rect_path(630, 634, 92, 30, 0), "INTER tag", fill=PARCH,
       stroke=INK, strokeWidth=3, join="round")
d.text("KEEP", "KEEP label", x=380, y=641, size=17, font="Virelai Sans",
       color=INK, justify="center")
d.text("INTER", "INTER label", x=630, y=641, size=17, font="Virelai Sans",
       color=INK, justify="center")

# --- the audit sheet between the piles -------------------------------------------
d.path("M462,584 L462,548 L556,548 L556,584 Z", "Audit sheet", fill=PARCH,
       stroke=INK, strokeWidth=3, join="round")
for i, y in enumerate([556, 564, 572]):
    d.path(f"M472,{y} L546,{y}", f"Ruling {i+1}", fill=NONE,
           stroke="#8A7454", strokeWidth=2, opacity=55)
d.path("M524,562 L533,571 L547,553", "Audited check", fill=NONE,
       stroke="#6B4A2A", strokeWidth=3, opacity=80, cap="round")

# --- scroll piles: KEEP neat, INTER heavier and leaning ----------------------------
def scroll(x, y, w, label, angle=0):
    if angle:
        d.path(rot_rect_path(x + w/2, y + 8, w, 16, angle), label,
               fill=PARCH, stroke=INK, strokeWidth=3, join="round")
        return
    d.path(f"M{x},{y} L{x+w},{y} L{x+w},{y+16} L{x},{y+16} Z", label,
           fill=PARCH, stroke=INK, strokeWidth=3, join="round")
    d.shape("ellipse", f"{label} end", x=x+w-8, y=y+1, width=10, height=14,
            fill=PARCH_DK, stroke=INK, strokeWidth=2)
    d.shape("ellipse", f"{label} scroll", x=x-4, y=y+3, width=9, height=10,
            fill="#8A7454", stroke=INK, strokeWidth=2)
    d.path(f"M{x+w*0.55},{y} L{x+w*0.55},{y+16}", f"{label} band", fill=NONE,
           stroke="#6B4A2A", strokeWidth=4)

# KEEP: two below, one above — squared and calm
scroll(322, 562, 62, "Keep s1")
scroll(392, 562, 62, "Keep s2")
scroll(352, 543, 62, "Keep s3")
# INTER: three below, two above, the top one tilted — the pile still being argued
scroll(566, 562, 62, "Inter s1")
scroll(636, 562, 62, "Inter s2")
scroll(706, 562, 56, "Inter s3")
scroll(600, 543, 62, "Inter s4")
scroll(668, 541, 62, "Inter s5", angle=-6)
# wax seal on the top INTER scroll — evidence attached
d.shape("ellipse", "Wax seal", x=714, y=546, width=14, height=14,
        fill="#A03A2C", stroke=INK, strokeWidth=2)

# --- the archivist's arms over the work -------------------------------------------
# left arm cradles the scroll under review against the chest
d.path("M400,420 C388,452 392,486 414,508", "Arm L", fill=NONE,
       stroke="#4A4438", strokeWidth=14, cap="round")
d.shape("ellipse", "Hand L", x=406, y=498, width=20, height=16,
        fill=SKIN, stroke=INK, strokeWidth=3)
scroll(402, 486, 54, "Judged scroll", angle=-18)
# right arm reaches over the table to lay a scroll on INTER
d.path("M480,412 C540,430 590,470 626,512", "Arm R", fill=NONE,
       stroke="#4A4438", strokeWidth=14, cap="round")
d.shape("ellipse", "Hand R", x=618, y=504, width=20, height=16,
        fill=SKIN, stroke=INK, strokeWidth=3)
scroll(600, 492, 58, "Descending scroll", angle=-12)

# --- motes of dust in the lamplight ------------------------------------------------
d.shape("ellipse", "Lamp pool", x=300, y=380, width=400, height=280,
        fill="#E8C87A", opacity=8, stroke=NONE)
for i, (x, y, w) in enumerate([(380,430,4),(520,470,3),(610,440,4),
                               (470,390,3),(700,500,3)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8DCBE", opacity=45, stroke=NONE)

# --- captions ------------------------------------------------------------------
d.text("RC-DIP", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E4DCC8", justify="center")
r = d.text("DOCUMENT IMPROVEMENT", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A89C84", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-dip-V1R00")
