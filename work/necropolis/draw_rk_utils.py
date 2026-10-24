#!/usr/bin/env python3
"""rc-utils.sh — The Sexton's Toolkit. Necropolis plate V1R00.
An open toolkit on a workbench: rk_init_script as the master key, rk_load_env
the lamp, validate_layout_alignment the brass caliper, the traps as coiled
rope — every instrument worn smooth because every worker in the necropolis
borrows from this box. Worn leather, shared brass.
1000x1000. Gradients + translucent shading."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("RC-Utils — Necropolis Plate", 1000, 1000)

INK = "#241812"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#150E08"}, {"offset": 1, "color": "#080503"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#514334"}, {"offset": 0.7, "color": "#261D13"},
    {"offset": 1, "color": "#110B06"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#352B1D"}, {"offset": 1, "color": "#150F08"}]}}
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#54402A"}, {"offset": 1, "color": "#241708"}]}}
WOOD_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3C2C1C"}, {"offset": 1, "color": "#1A1006"}]}}
LEATHER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E4C2E"}, {"offset": 1, "color": "#38240F"}]}}
LEATHER_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#523722"}, {"offset": 1, "color": "#241505"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EAC56E"}, {"offset": 1, "color": "#9A782E"}]}}
ROPE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#BC9E6E"}, {"offset": 1, "color": "#7A6440"}]}}
PARCH = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EAE0C4"}, {"offset": 1, "color": "#B8A87E"}]}}
LAMP_GLASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4ECDF"}, {"offset": 1, "color": "#9AA894"}]}}
FLAME = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FAE8A8"}, {"offset": 1, "color": "#E0A040"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A6248", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0D0B0", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E5A40", opacity=35, stroke=NONE)

# --- crypt wall: seam + the peg rail of borrowed things ---------------------------
d.path("M150,368 C350,360 650,360 850,368", "Wall seam", fill=NONE,
       stroke="#0C0804", strokeWidth=4, opacity=40)
# peg rail
d.path("M220,296 L520,296 L520,308 L220,308 Z", "Peg rail", fill=WOOD_DK,
       stroke=INK, strokeWidth=3, join="round")
for i, px in enumerate([252, 340, 428]):
    d.path(f"M{px},308 L{px},332", f"Peg {i+1}", fill=NONE, stroke="#3E2E1C",
           strokeWidth=6, cap="round")
# peg one: a spare skeleton key hanging — the next borrower will take it
d.path("M252,332 C244,340 244,352 252,356 C260,352 260,340 252,332 Z",
       "Spare key bow", fill=NONE, stroke="#B8924A", strokeWidth=4)
d.path("M252,356 L252,392", "Spare key stem", fill=NONE, stroke="#B8924A",
       strokeWidth=4, cap="round")
d.path("M252,380 L262,380 M252,388 L260,388", "Spare key bit", fill=NONE,
       stroke="#B8924A", strokeWidth=3)
# peg two: a hanging leather strap, off a borrowed belt
d.path("M340,332 C332,352 332,376 342,394 C350,378 350,352 344,334",
       "Strap loop", fill=NONE, stroke="#7A5636", strokeWidth=7, cap="round")
d.shape("rectangle", "Strap buckle", x=335, y=360, width=12, height=10,
        fill=NONE, stroke="#B8924A", strokeWidth=2)
# peg three: bare — out on loan
d.shape("ellipse", "Peg shine", x=427, y=330, width=3, height=3,
        fill="#D8C49A", opacity=70, stroke=NONE)

# --- lamp glow (ambient, behind the bench scene) ------------------------------------
d.shape("ellipse", "Lamp glow", x=205, y=330, width=300, height=300,
        fill="#F0C868", opacity=11, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0804",
       strokeWidth=4, opacity=70)
d.shape("ellipse", "Bench shadow", x=270, y=686, width=560, height=20,
        fill="#050302", opacity=55, stroke=NONE)

# --- the workbench -------------------------------------------------------------------
d.path("M306,582 L334,582 L334,696 L306,696 Z", "Bench leg L", fill=WOOD_DK,
       stroke=INK, strokeWidth=4, join="round")
d.path("M744,582 L772,582 L772,696 L744,696 Z", "Bench leg R", fill=WOOD_DK,
       stroke=INK, strokeWidth=4, join="round")
d.path("M318,644 L758,644 L758,658 L318,658 Z", "Stretcher", fill=WOOD_DK,
       stroke=INK, strokeWidth=3, join="round")
d.path("M282,548 L798,548 L798,582 L282,582 Z", "Bench slab", fill=WOOD,
       stroke=INK, strokeWidth=5, join="round")
d.path("M288,554 L792,554", "Slab edge light", fill=NONE, stroke="#96774E",
       strokeWidth=3, opacity=55)
# scars of shared work along the slab edge
for i, (x0, x1) in enumerate([(340,360),(470,478),(640,652),(720,734)]):
    d.path(f"M{x0},572 L{x1},570", f"Scar {i+1}", fill=NONE,
           stroke="#2A1C0E", strokeWidth=2, opacity=60)

# --- the lamp (rk_load_env): brass base, glass chimney, live flame ---------------------
d.path("M326,548 C326,538 338,532 354,532 C370,532 382,538 382,548 Z",
       "Lamp base", fill=BRASS, stroke=INK, strokeWidth=3, join="round")
d.path("M348,532 L348,504 L360,504 L360,532", "Lamp stem", fill=BRASS,
       stroke=INK, strokeWidth=3, join="round")
d.shape("ellipse", "Oil font", x=336, y=496, width=36, height=24,
        fill=BRASS, stroke=INK, strokeWidth=3)
# glass chimney — translucent so the backdrop reads through
d.path("M338,504 C332,478 334,452 344,438 L364,438 C374,452 376,478 370,504 Z",
       "Chimney", fill=LAMP_GLASS, opacity=28, stroke="#C8D0BC",
       strokeWidth=3, join="round")
d.shape("ellipse", "Chimney mouth", x=344, y=432, width=20, height=8,
        fill="#2A2018", stroke=INK, strokeWidth=3)
# the flame, burning steady
d.shape("ellipse", "Flame core", x=349, y=452, width=10, height=20,
        fill=FLAME, opacity=95, stroke=NONE)
d.shape("ellipse", "Flame glow", x=330, y=438, width=48, height=48,
        fill="#F0C868", opacity=22, stroke=NONE)
# the bail handle, folded down against the glass
d.path("M336,506 C322,492 320,470 330,456", "Bail L", fill=NONE,
       stroke="#8A6A34", strokeWidth=3, cap="round")
d.path("M372,506 C386,492 388,470 378,456", "Bail R", fill=NONE,
       stroke="#8A6A34", strokeWidth=3, cap="round")

# --- the toolkit: open leather case, lid thrown back -----------------------------------
# dark mouth of the open box
d.path("M452,472 L628,472 L618,456 L462,456 Z", "Box mouth", fill="#0E0803",
       stroke=INK, strokeWidth=3, join="round")
# the lid, hinged at the back edge and leaning open
d.path("M462,456 L618,456 L600,404 L480,404 Z", "Box lid", fill=LEATHER_DK,
       stroke=INK, strokeWidth=4, join="round")
d.path("M472,448 L608,448 L596,412 L484,412 Z", "Lid lining", fill=LEATHER,
       opacity=60, stroke=NONE, join="round")
# hinges + lid handle resting up
d.path("M492,458 L492,450 M588,458 L588,450", "Hinges", fill=NONE,
       stroke="#B8924A", strokeWidth=4)
d.path("M526,404 C526,394 554,394 554,404", "Lid handle", fill=NONE,
       stroke="#B8924A", strokeWidth=5, cap="round")
# box front: worn leather over wood, straps, brass corners, hasp
d.path("M450,472 L630,472 L630,548 L450,548 Z", "Box front", fill=LEATHER,
       stroke=INK, strokeWidth=4, join="round")
for i, sx in enumerate([478, 594]):
    d.path(f"M{sx},472 L{sx},548", f"Strap {i+1}", fill=NONE,
           stroke="#4E3220", strokeWidth=10)
    d.shape("rectangle", f"Strap stud {i+1}", x=sx-4, y=498, width=8,
            height=8, fill=BRASS, stroke=INK, strokeWidth=2)
for i, (cx, cy) in enumerate([(450,472),(630,472),(450,548),(630,548)]):
    d.shape("ellipse", f"Corner {i+1}", x=cx-6, y=cy-6, width=12, height=12,
            fill=BRASS, stroke=INK, strokeWidth=2)
d.shape("rectangle", "Hasp", x=534, y=466, width=14, height=22, fill=BRASS,
        stroke=INK, strokeWidth=2, radius=2)
# a folded chamois draped over the front edge — mid-borrow
d.path("M450,500 C468,502 484,502 498,498 L502,548 C484,554 466,552 452,548 Z",
       "Draped cloth", fill=PARCH, opacity=85, stroke=INK, strokeWidth=3,
       join="round")
d.path("M462,512 L490,510 M462,526 L492,524", "Cloth folds", fill=NONE,
       stroke="#8A7A58", strokeWidth=2, opacity=60)

# --- the master key (rk_init_script), laid out on the slab -------------------------------
d.path("M500,566 L606,556", "Key shaft", fill=NONE, stroke="#D8AE54",
       strokeWidth=8, cap="round")
d.shape("ellipse", "Key bow", x=602, y=540, width=34, height=30, fill=NONE,
        stroke="#D8AE54", strokeWidth=7)
d.shape("ellipse", "Key bow heart", x=610, y=548, width=10, height=10,
        fill=NONE, stroke="#D8AE54", strokeWidth=3)
# bit: two teeth at the shaft's far end
d.path("M500,566 L498,578 M512,565 L510,576 M490,568 L488,580", "Key teeth",
       fill=NONE, stroke="#D8AE54", strokeWidth=5)
d.path("M524,560 L596,554", "Key shine", fill=NONE, stroke="#F4DFA0",
       strokeWidth=2, opacity=70)
# the loan tag tied to the bow — every worker signs it out
d.path("M622,566 C628,576 630,586 628,596", "Tag string", fill=NONE,
       stroke="#8A7454", strokeWidth=2)
d.shape("rectangle", "Loan tag", x=614, y=596, width=30, height=18,
        fill=PARCH, stroke=INK, strokeWidth=2, radius=2)
d.path("M620,606 L636,606", "Tag line", fill=NONE, stroke="#6A5B40",
       strokeWidth=2, opacity=80)

# --- the brass caliper (validate_layout_alignment) ----------------------------------------
d.shape("ellipse", "Caliper hinge", x=674, y=452, width=18, height=18,
        fill=BRASS, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Hinge screw", x=679, y=457, width=8, height=8,
        fill="#6E5222", stroke=NONE)
d.path("M682,466 L644,546", "Caliper leg L", fill=NONE, stroke="#D8AE54",
       strokeWidth=7, cap="round")
d.path("M686,468 L726,546", "Caliper leg R", fill=NONE, stroke="#D8AE54",
       strokeWidth=7, cap="round")
d.path("M644,546 L640,556 M726,546 L730,556", "Caliper points", fill=NONE,
       stroke="#D8AE54", strokeWidth=4, cap="round")
# the measuring arc between the legs
d.path("M652,528 C670,540 700,540 718,528", "Caliper arc", fill=NONE,
       stroke="#B8924A", strokeWidth=2, opacity=80)
for i, t in enumerate([0.2, 0.5, 0.8]):
    x = 652 + (718 - 652) * t
    y = 528 + (540 - 528) * (1 - abs(t - 0.5) * 2)
    d.path(f"M{x:.0f},{y:.0f} L{x:.0f},{y+6:.0f}", f"Arc tick {i+1}",
           fill=NONE, stroke="#B8924A", strokeWidth=2)

# --- the coiled rope (the traps), with a tail over the edge -------------------------------
for i, (x, y, w, h) in enumerate([(726,516,70,36),(733,522,56,28),
                                  (740,528,42,20)]):
    d.shape("ellipse", f"Coil {i+1}", x=x, y=y, width=w, height=h,
            fill=NONE, stroke="#A98A5C", strokeWidth=7)
# coil shading
d.path("M730,548 C748,556 772,556 790,548", "Coil shadow", fill=NONE,
       stroke="#5E4A2E", strokeWidth=4, opacity=60)
# the tail: over the slab edge and down
d.path("M792,536 C806,556 806,584 794,606 C786,622 784,640 790,656",
       "Rope tail", fill=NONE, stroke="#A98A5C", strokeWidth=6, cap="round")
d.path("M788,652 L800,664", "Tail whipping", fill=NONE, stroke="#A98A5C",
       strokeWidth=6, cap="round")
# frayed end
d.path("M792,660 C790,666 788,670 786,674 M796,662 C796,668 797,672 798,676",
       "Fray", fill=NONE, stroke="#8A6F44", strokeWidth=2, cap="round")

# --- captions ------------------------------------------------------------------
d.text("RC-UTILS", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E8DEC8", justify="center")
r = d.text("EVERYONE BORROWS THESE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B4A488", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("rk-utils-V1R00")
