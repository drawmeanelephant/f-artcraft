#!/usr/bin/env python3
"""Benevolence Spacer — mascot portrait V1R00.
A mascot fluffing a chair in a furnished waiting room: motivational poster
on the wall, tea and newsletters on offer. Care expressed; relief pending.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Benevolence Spacer — Mascot Portrait", 1000, 1000)

INK = "#2C1E14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#201419"}, {"offset": 1, "color": "#0D080A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C2A098"}, {"offset": 0.7, "color": "#947068"},
    {"offset": 1, "color": "#583F3A"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#58443E"}, {"offset": 1, "color": "#241A16"}]}}
CHAIR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#84A89E"}, {"offset": 1, "color": "#4E6E64"}]}}
CHAIR_DARK = "#3C584F"
CUSHION_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4EAD2"}, {"offset": 0.75, "color": "#DECFAE"},
    {"offset": 1, "color": "#BFA87E"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C2AE92"}, {"offset": 0.7, "color": "#9E8A70"},
    {"offset": 1, "color": "#74634E"}]}}
FUR_MID = "#9E8A70"
WOOD = "#5A4030"
POSTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E4C8"}, {"offset": 1, "color": "#D2BE9C"}]}}
SUN = "#D9A44E"
TEA = "#7A4A2E"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#AE8E80", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D4C8", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5C443C", opacity=45, stroke=NONE)

# --- floor + rug ------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#1C1210",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Rug", x=330, y=660, width=440, height=70,
        fill="#8A5E54", opacity=45, stroke=NONE)
d.shape("ellipse", "Rug inner", x=370, y=668, width=360, height=54,
        fill=NONE, stroke="#D8B4A4", strokeWidth=3, opacity=40)

# --- the motivational poster, hung at standing eye level ------------------------------
d.path("M676,200 L820,200 L820,336 L676,336 Z", "Poster frame",
       fill=POSTER_GRAD, stroke=INK, strokeWidth=4)
d.path("M686,210 L810,210 L810,326 L686,326 Z", "Poster inner",
       fill="#F8EFDC", stroke="#A8906C", strokeWidth=2)
# rising sun over a horizon + motto rules beneath
d.path("M700,282 A46,46 0 0 1 792,282 Z", "Poster sun", fill=SUN,
       opacity=85, stroke=NONE)
for i, (x0, y0, x1, y1) in enumerate([(746,232,746,256),(710,242,722,262),
                                       (782,242,770,262),(698,258,714,268),
                                       (794,258,780,268)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Ray {i+1}", fill=NONE,
           stroke=SUN, strokeWidth=4, cap="round")
d.path("M696,282 L796,282", "Poster horizon", fill=NONE, stroke=INK,
       strokeWidth=2.5)
for i, (y, w) in enumerate([(298,92),(310,76)]):
    d.path(f"M{746-w/2},{y} L{746+w/2},{y}", f"Motto line {i+1}",
           fill=NONE, stroke="#9A8468", strokeWidth=3, opacity=70)
# nail + wire shadow above frame
d.path("M692,200 L748,184 L804,200", "Poster wire", fill=NONE,
       stroke=INK, strokeWidth=2.5, opacity=60)

# --- side table: tea and newsletters on offer ------------------------------------------
d.shape("ellipse", "Table shadow", x=166, y=686, width=120, height=12,
        fill="#140D0A", opacity=30, stroke=NONE)
d.shape("ellipse", "Table top", x=160, y=520, width=120, height=16,
        fill=WOOD, stroke=INK, strokeWidth=3)
d.path("M214,536 L214,676", "Table stem", fill=NONE, stroke=WOOD,
       strokeWidth=8)
d.path("M214,676 L186,694 M214,676 L242,694", "Table feet", fill=NONE,
       stroke=WOOD, strokeWidth=6, cap="round")
# teacup + saucer with a steam curl
d.shape("ellipse", "Saucer", x=176, y=506, width=52, height=10,
        fill="#EFE6D0", stroke=INK, strokeWidth=2.5)
d.path("M184,484 L218,484 L214,506 L188,506 Z", "Cup",
       fill="#F4ECDA", stroke=INK, strokeWidth=2.5)
d.path("M218,488 C228,486 230,496 220,498", "Cup handle", fill=NONE,
       stroke=INK, strokeWidth=2.5)
d.path("M196,476 C192,468 198,462 194,454", "Steam", fill=NONE,
       stroke="#E8DCC8", strokeWidth=3, opacity=70, cap="round")
d.path("M186,492 L216,492 L214,500 L188,500 Z", "Tea", fill=TEA,
       opacity=55, stroke=NONE)
# newsletter fan leaning on the table leg
for i, (deg, label) in enumerate([(-18, "NL 1"), (-8, "NL 2"), (2, "NL 3")]):
    d.path(rot_rect_path(246, 620, 64, 88, deg), label,
           fill=POSTER_GRAD, stroke=INK, strokeWidth=2.5)
    d.path(rot_rect_path(246, 610, 48, 4, deg), f"{label} masthead",
           fill="#8A7660", opacity=60, stroke=NONE)
    d.path(rot_rect_path(246, 640, 46, 3, deg), f"{label} column",
           fill="#A89478", opacity=55, stroke=NONE)

# --- the armchair, mid-fluff --------------------------------------------------------------
d.shape("ellipse", "Chair shadow", x=470, y=680, width=270, height=18,
        fill="#140D0A", opacity=35, stroke=NONE)
# back + rolled arms + base
d.path("M496,560 C496,470 540,424 606,424 C672,424 716,470 716,560 "
       "L716,640 L496,640 Z",
       "Chair back", fill=CHAIR_GRAD, stroke=INK, strokeWidth=5)
# button tufts on the back
for i, (x, y) in enumerate([(552,492),(606,478),(660,492),(580,540),(634,540)]):
    d.shape("ellipse", f"Tuft {i+1}", x=x, y=y, width=10, height=10,
            fill=CHAIR_DARK, opacity=70, stroke=NONE)
    d.path(f"M{x-8},{y+5} C{x-2},{y+10} {x+8},{y+10} {x+14},{y+4}",
           f"Tuft crease {i+1}", fill=NONE, stroke=CHAIR_DARK,
           strokeWidth=2, opacity=45)
# rolled arms
d.path("M472,560 C472,522 496,502 522,510 C544,518 548,550 536,574 "
       "C526,594 498,600 484,588 C472,578 472,570 472,560 Z",
       "Arm L", fill=CHAIR_GRAD, stroke=INK, strokeWidth=4)
d.path("M740,560 C740,522 716,502 690,510 C668,518 664,550 676,574 "
       "C686,594 714,600 728,588 C740,578 740,570 740,560 Z",
       "Arm R", fill=CHAIR_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Arm L scroll", x=486, y=530, width=30, height=30,
        fill=NONE, stroke=CHAIR_DARK, strokeWidth=3, opacity=60)
d.shape("ellipse", "Arm R scroll", x=696, y=530, width=30, height=30,
        fill=NONE, stroke=CHAIR_DARK, strokeWidth=3, opacity=60)
# seat + skirt + feet
d.path("M508,600 L704,600 L704,640 L508,640 Z", "Seat band",
       fill=CHAIR_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M500,640 L712,640 L712,668 L500,668 Z", "Skirt",
       fill=CHAIR_DARK, stroke=INK, strokeWidth=3.5)
d.path("M520,668 L514,692 M692,668 L698,692", "Chair feet", fill=NONE,
       stroke=WOOD, strokeWidth=7, cap="round")

# --- the cushion, lifted and patted ------------------------------------------------------
d.path(rot_rect_path(606, 566, 168, 74, -9), "Cushion",
       fill=CUSHION_GRAD, stroke=INK, strokeWidth=4)
d.path(rot_rect_path(606, 566, 140, 46, -9), "Cushion welt",
       fill=NONE, stroke="#A8906C", strokeWidth=2.5, opacity=60)
d.shape("ellipse", "Cushion button", x=596, y=556, width=14, height=14,
        fill="#A8906C", stroke=INK, strokeWidth=2)
# fluff marks: poof arcs + dust motes off the rising edge
for i, (x0, y0, x1, y1, x2, y2) in enumerate([
        (700,516,722,506,738,516),(668,502,684,488,704,492),
        (528,540,506,536,494,550)]):
    d.path(f"M{x0},{y0} Q{x1},{y1} {x2},{y2}", f"Poof {i+1}", fill=NONE,
           stroke="#E8D8B8", strokeWidth=4, opacity=75, cap="round")
for i, (x, y, w) in enumerate([(712,540,7),(690,478,6),(516,516,6),(740,560,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8D8B8", opacity=55, stroke=NONE)

# --- the mascot, mid-pat -----------------------------------------------------------------
d.shape("ellipse", "Mascot shadow", x=250, y=686, width=180, height=16,
        fill="#140D0A", opacity=35, stroke=NONE)
d.shape("ellipse", "Body", x=272, y=500, width=150, height=188,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Head", x=284, y=376, width=124, height=120,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
for ex in (294, 396):
    d.shape("ellipse", f"Ear {ex}", x=ex-10, y=372, width=25, height=23,
            fill=FUR_MID, stroke=INK, strokeWidth=3.5)
# warm, busy expression
d.shape("ellipse", "Eye L", x=318, y=436, width=10, height=10,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=360, y=436, width=10, height=10,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=320, y=438, width=3, height=3,
        fill="#F4EAD2", stroke=NONE)
d.shape("ellipse", "Glint R", x=362, y=438, width=3, height=3,
        fill="#F4EAD2", stroke=NONE)
d.path("M324,464 C332,470 352,470 360,464", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Blush L", x=304, y=450, width=14, height=8,
        fill="#C88E7E", opacity=45, stroke=NONE)
d.shape("ellipse", "Blush R", x=368, y=450, width=14, height=8,
        fill="#C88E7E", opacity=45, stroke=NONE)
# arms up on the cushion: one steadying, one patting
d.path("M410,528 C440,520 472,518 500,522", "Arm steady", fill=NONE,
       stroke=FUR_MID, strokeWidth=15, cap="round")
d.shape("ellipse", "Paw steady", x=492, y=512, width=26, height=22,
        fill=FUR_MID, stroke=INK, strokeWidth=3.5)
d.path("M402,570 C440,566 478,570 508,580", "Arm pat", fill=NONE,
       stroke=FUR_MID, strokeWidth=15, cap="round")
d.shape("ellipse", "Paw pat", x=502, y=570, width=26, height=22,
        fill=FUR_MID, stroke=INK, strokeWidth=3.5)
# pat motion marks off the upper paw
d.path("M540,596 C556,600 568,594 574,582", "Pat mark", fill=NONE,
       stroke=FUR_MID, strokeWidth=4, opacity=70, cap="round")

# --- captions -------------------------------------------------------------------------
d.text("BENEVOLENCE SPACER", "Name", x=500, y=930, size=52,
       font="Virelai Sans", color="#F0DFD2", justify="center")
r = d.text("AFFECTIVE DELAY ENTITY", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#CBAE9E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("278.benevolence-spacer-V1R00")
