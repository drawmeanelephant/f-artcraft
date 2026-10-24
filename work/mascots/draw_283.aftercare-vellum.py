#!/usr/bin/env python3
"""Aftercare Vellum — mascot portrait V1R00.
A soft vellum-sheet mascot presenting a carefully worded follow-up letter
on even softer stock. Behind it, ghosted on the wall: the procedural first
contact the letter answers for. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Aftercare Vellum — Mascot Portrait", 1000, 1000)

INK = "#4A2E22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1C1410"}, {"offset": 1, "color": "#0B0705"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A5C40"}, {"offset": 0.7, "color": "#463323"},
    {"offset": 1, "color": "#1E140C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#34241A"}, {"offset": 1, "color": "#160E08"}]}}
VELLUM = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F6ECD4"}, {"offset": 0.72, "color": "#E4CFA4"},
    {"offset": 1, "color": "#C4A478"}]}}
LETTER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FBF4E2"}, {"offset": 1, "color": "#EEDFBF"}]}}
SEAL = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C86A50"}, {"offset": 1, "color": "#8E3A28"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#B08A62", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D4AE", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E5238", opacity=45, stroke=NONE)

# --- floor --------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#120C08",
       strokeWidth=4, opacity=70)

# --- the first contact: a procedural form letter, ghosted on the wall -----------
# tilted grey notice, already filed and fading — the vellum answers for it
d.path(rot_rect_path(292, 272, 190, 148, 8), "First contact", fill="#6E6256",
       stroke="#3E342C", strokeWidth=4, join="round", opacity=42)
for i in range(4):
    y = 230 + i*24
    w = 136 if i < 3 else 88
    d.path(rot_rect_path(292, y, w, 7, 8), f"Ghost line {i+1}",
           fill="#9E9484", stroke=NONE, opacity=38)
# its stamp: RECEIVED, already cold
d.path(rot_rect_path(290, 310, 80, 26, 8), "Ghost stamp", fill=NONE,
       stroke="#8E5A4C", strokeWidth=3, opacity=45)
t = d.text("RECEIVED", "Ghost stamp text", x=258, y=318, size=12,
           font="Virelai Sans", color="#8E5A4C", justify="left")
if t and t.get("id"):
    d.cmd("object.setProps", "stamp fade", ids=[t["id"]], opacity=45)

# --- inkwell + quill at floor right ----------------------------------------------
d.shape("ellipse", "Inkwell shadow", x=688, y=676, width=92, height=16,
        fill="#0C0805", opacity=50, stroke=NONE)
d.path("M714,676 C714,644 726,636 736,634 C750,631 766,640 768,676 Z",
       "Inkwell", fill="#2E1E16", stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Ink surface", x=728, y=630, width=30, height=10,
        fill="#17100E", stroke=INK, strokeWidth=3)
# quill, still wet
d.path("M742,632 C752,586 770,548 796,522", "Quill shaft", fill=NONE,
       stroke="#E4CFA4", strokeWidth=5, cap="round")
d.path("M796,522 C814,530 814,562 792,580 C786,560 788,536 796,522 Z",
       "Quill feather", fill="#E8D8B4", stroke=INK, strokeWidth=3,
       join="round", opacity=90)
d.path("M794,534 C800,548 798,562 792,574", "Feather vein", fill=NONE,
       stroke="#8E7452", strokeWidth=2, opacity=60)

# --- warm glow the letter carries -------------------------------------------------
d.shape("ellipse", "Letter glow", x=370, y=520, width=260, height=190,
        fill="#F0C878", opacity=12, stroke=NONE)
d.shape("ellipse", "Letter glow core", x=420, y=555, width=160, height=120,
        fill="#F0D08A", opacity=14, stroke=NONE)

# --- the mascot: a vellum sheet with deckled edges ----------------------------------
def deckle():
    # gentle wavy edges — paper, not a panel
    return ("M350,318 C430,304 560,322 650,312 "
            "C664,410 656,540 662,680 "
            "C560,696 430,680 350,686 "
            "C336,560 346,420 350,318 Z")

d.path(deckle(), "Vellum body", fill=VELLUM, stroke=INK, strokeWidth=6,
       join="round")
# deckle fringe hints along the bottom + left
d.path("M352,684 C430,678 560,694 660,678", "Deckle bottom", fill=NONE,
       stroke="#8E6E48", strokeWidth=3, opacity=50)
d.path("M350,320 C346,420 338,560 352,682", "Deckle left", fill=NONE,
       stroke="#8E6E48", strokeWidth=3, opacity=40)
# top sheen + faint laid lines (vellum's tooth)
d.shape("ellipse", "Vellum sheen", x=390, y=330, width=190, height=56,
        fill="#FFFFFF", opacity=18, stroke=NONE)
for i in range(6):
    y = 398 + i*44
    d.path(f"M372,{y} C470,{y+4} 560,{y-4} 634,{y+2}", f"Laid line {i+1}",
           fill=NONE, stroke="#B89468", strokeWidth=2, opacity=25)

# face: composed, gentle — the second contact is always calmer
d.path("M424,412 C432,420 446,420 454,412", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M546,412 C554,420 568,420 576,412", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M478,452 C490,462 510,462 522,452", "Smile", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.shape("ellipse", "Blush L", x=408, y=428, width=28, height=13,
        fill="#C88A62", opacity=38, stroke=NONE)
d.shape("ellipse", "Blush R", x=564, y=428, width=28, height=13,
        fill="#C88A62", opacity=38, stroke=NONE)

# --- arms presenting the letter forward ---------------------------------------------
d.path("M352,576 C324,592 322,624 348,644", "Arm L", fill=NONE,
       stroke=INK, strokeWidth=13, cap="round")
d.path("M658,572 C684,588 686,620 662,640", "Arm R", fill=NONE,
       stroke=INK, strokeWidth=13, cap="round")

# --- the follow-up letter itself ------------------------------------------------------
CX, CY, ANG = 500, 606, -6

def rp(x, y):
    a = math.radians(ANG); c, s = math.cos(a), math.sin(a)
    return (CX + (x-CX)*c - (y-CY)*s, CY + (x-CX)*s + (y-CY)*c)

d.path(rot_rect_path(CX, CY, 236, 132, ANG), "The letter", fill=LETTER,
       stroke=INK, strokeWidth=5, join="round")
# deckled hint on the letter's lower edge
p1, p2 = rp(390, 664), rp(610, 664)
d.path(f"M{p1[0]:.0f},{p1[1]:.0f} C{p1[0]+60:.0f},{p1[1]+6:.0f} "
       f"{p2[0]-60:.0f},{p2[1]-6:.0f} {p2[0]:.0f},{p2[1]:.0f}",
       "Letter deckle", fill=NONE, stroke="#B08A5E", strokeWidth=2.5,
       opacity=60)
# carefully worded lines — deliberate, even, unhurried
for i, (x1, x2) in enumerate([(408,592),(408,578),(408,592),(408,512)]):
    q1, q2 = rp(x1, 566+i*19), rp(x2, 566+i*19)
    d.path(f"M{q1[0]:.0f},{q1[1]:.0f} L{q2[0]:.0f},{q2[1]:.0f}",
           f"Letter line {i+1}", fill=NONE, stroke="#7A5E42",
           strokeWidth=4, cap="round", opacity=75)
# the closing flourish — the only stroke with feeling in it
q1, q2 = rp(430, 646), rp(500, 650)
d.path(f"M{q1[0]:.0f},{q1[1]:.0f} C{q1[0]+22:.0f},{q1[1]-10:.0f} "
       f"{q2[0]-22:.0f},{q2[1]+8:.0f} {q2[0]:.0f},{q2[1]:.0f}",
       "Sign-off", fill=NONE, stroke="#6E4E34", strokeWidth=3.5,
       cap="round", opacity=80)
# wax seal, bottom right — pressed after everything else was fixed
sx, sy = rp(572, 648)
d.shape("ellipse", "Wax seal", x=sx-13, y=sy-13, width=26, height=26,
        fill=SEAL, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Seal mark", x=sx-6, y=sy-6, width=12, height=12,
        fill=NONE, stroke="#F0C8A8", strokeWidth=2, opacity=80)

# hands resting on the letter's edges
hx1, hy1 = rp(392, 640); hx2, hy2 = rp(610, 636)
d.shape("ellipse", "Hand L", x=hx1-13, y=hy1-10, width=26, height=20,
        fill=VELLUM, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=hx2-13, y=hy2-10, width=26, height=20,
        fill=VELLUM, stroke=INK, strokeWidth=4)

# --- captions ---------------------------------------------------------------------
d.text("AFTERCARE VELLUM", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F0E2C8", justify="center")
r = d.text("SECOND-CONTACT STATIONER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8A888", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("283.aftercare-vellum-V1R00")
