#!/usr/bin/env python3
"""Alibi Seal — mascot portrait V1R00.
The mascot presses a heavy wax-seal stamp onto a signature-covered memo.
A first impression already sits on the sheet, glossy and still wet; the
exoneration predates the charge it answers. 1000x1000.
Gradients + translucent shading, no flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Alibi Seal — Mascot Portrait", 1000, 1000)

INK = "#2A1B16"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#181016"}, {"offset": 1, "color": "#0A0709"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E4E44"}, {"offset": 0.7, "color": "#4C362E"},
    {"offset": 1, "color": "#2B1E1B"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#43302A"}, {"offset": 1, "color": "#201613"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DCB894"}, {"offset": 0.7, "color": "#B58C64"},
    {"offset": 1, "color": "#896746"}]}}
WAX_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E05A4C"}, {"offset": 0.65, "color": "#AE2E2B"},
    {"offset": 1, "color": "#6E1818"}]}}
PARCH_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E3C4"}, {"offset": 1, "color": "#D8C69E"}]}}
BRASS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E2B45C"}, {"offset": 0.7, "color": "#B07F33"},
    {"offset": 1, "color": "#6E4C1C"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#52392D"}, {"offset": 1, "color": "#33221A"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A5F3C"}, {"offset": 1, "color": "#573B24"}]}}

def scallop(cx, cy, r, bumps=9, wob=0.13):
    pts = [(cx + r * (1 + (wob if i % 2 else -wob)) * math.cos(2 * math.pi * i / (2 * bumps)),
            cy + r * (1 + (wob if i % 2 else -wob)) * math.sin(2 * math.pi * i / (2 * bumps)))
           for i in range(2 * bumps)]
    m = [((pts[i][0] + pts[(i + 1) % len(pts)][0]) / 2,
          (pts[i][1] + pts[(i + 1) % len(pts)][1]) / 2) for i in range(len(pts))]
    out = f"M{m[0][0]:.1f},{m[0][1]:.1f} "
    for i in range(len(pts)):
        p = pts[(i + 1) % len(pts)]
        mm = m[(i + 1) % len(m)]
        out += f"Q{p[0]:.1f},{p[1]:.1f} {mm[0]:.1f},{mm[1]:.1f} "
    return out + "Z"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6248", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4CBA6", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,230,8),(800,225,7),(160,520,9),(838,540,8),
                               (250,764,7),(752,746,9),(135,390,6),(864,392,7),
                               (390,112,7),(610,110,8),(335,822,6),(664,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#503A30", opacity=45, stroke=NONE)

# --- prior exonerations: memos already sealed, pinned on the back wall ---------
for i, (cx, cy, w, h, deg) in enumerate([(240, 282, 140, 100, -7),
                                         (730, 240, 140, 100, 6)]):
    d.path(rot_rect_path(cx, cy, w, h, deg), f"Old memo {i+1}",
           fill=PARCH_GRAD, stroke=INK, strokeWidth=3, opacity=45)
    d.path(scallop(cx - 20, cy + 12, 22, 8, 0.12), f"Old wax {i+1}",
           fill=WAX_GRAD, stroke=NONE, opacity=50)
    d.path(f"M{cx-45},{cy-22} C{cx-30},{cy-30} {cx-15},{cy-16} {cx-2},{cy-24}",
           f"Old signature {i+1}", fill=NONE, stroke=INK, strokeWidth=2.5,
           opacity=40)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#140D0B",
       strokeWidth=4, opacity=70)

# --- warm glow over the seal ---------------------------------------------------
d.shape("ellipse", "Seal glow", x=350, y=440, width=330, height=250,
        fill="#E8A86A", opacity=10, stroke=NONE)

# --- the mascot, behind the desk ------------------------------------------------
d.shape("ellipse", "Body", x=585, y=425, width=185, height=215,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# head + ears
for ex in (608, 748):
    d.shape("ellipse", f"Ear {ex}", x=ex - 11, y=296, width=26, height=24,
            fill="#B58C64", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Head", x=604, y=298, width=148, height=136,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# serene closed eyes — it never asks what it is absolving
d.path("M636,368 C644,376 656,376 664,368", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M694,368 C702,376 714,376 722,368", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# a small satisfied smirk
d.path("M664,404 C674,412 692,412 700,402", "Smirk", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Cheek L", x=624, y=388, width=22, height=14,
        fill="#D08A7A", opacity=35, stroke=NONE)
d.shape("ellipse", "Cheek R", x=714, y=388, width=22, height=14,
        fill="#D08A7A", opacity=35, stroke=NONE)

# --- the desk -------------------------------------------------------------------
d.shape("ellipse", "Desk shadow", x=230, y=752, width=540, height=22,
        fill="#0E0806", opacity=45, stroke=NONE)
for x in (288, 696):
    d.shape("rectangle", f"Desk leg {x}", x=x, y=640, width=16, height=116,
            fill="#3A281E", stroke=INK, strokeWidth=3, radius=4)
d.path("M285,545 L715,545 L756,625 L244,625 Z", "Desk top",
       fill=DESK_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M244,625 L756,625 L744,648 L256,648 Z", "Desk edge",
       fill="#3E2B20", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Desk sheen", x=300, y=556, width=180, height=20,
        fill="#8A6A4E", opacity=25, stroke=NONE)

# --- the memo, signature-covered --------------------------------------------------
d.path("M330,552 L560,548 L576,614 L340,620 Z", "Memo",
       fill=PARCH_GRAD, stroke=INK, strokeWidth=3.5, join="round")
# signature squiggles — names already dry
d.path("M348,566 C360,559 370,571 382,565 C394,559 404,571 418,564 "
       "C428,559 436,567 446,563", "Signature 1", fill=NONE,
       stroke="#4A3828", strokeWidth=2.5, cap="round")
d.path("M348,581 C364,574 374,588 390,580 C400,575 410,586 424,580 "
       "C436,575 446,584 458,579", "Signature 2", fill=NONE,
       stroke="#4A3828", strokeWidth=2.5, cap="round", opacity=85)
d.path("M350,596 C358,590 366,600 376,594 C384,589 392,598 402,593",
       "Signature 3", fill=NONE, stroke="#4A3828", strokeWidth=2.5,
       cap="round", opacity=75)
# a flourish under the top signature
d.path("M344,572 C380,578 430,575 452,568 C448,576 420,582 344,572 Z",
       "Flourish", fill="#4A3828", opacity=55, stroke=NONE)
# ruled line at the memo's foot
d.path("M346,606 L560,602", "Ruled line", fill=NONE, stroke="#B8A27E",
       strokeWidth=2, opacity=70)

# --- the fresh impression, still wet -----------------------------------------------
d.path(scallop(455, 592, 34, 10, 0.12), "Wax impression",
       fill=WAX_GRAD, stroke="#5E1414", strokeWidth=3)
d.path(scallop(455, 592, 22, 10, 0.10), "Wax inner",
       fill=NONE, stroke="#7E1E1C", strokeWidth=3, opacity=80)
d.text("A", "Seal mark", x=455, y=602, size=26, font="Virelai Sans",
       color="#F0C0A8", justify="center")
# wet gloss — the ink has not dried
d.shape("ellipse", "Wet gloss 1", x=438, y=574, width=16, height=9,
        fill="#FFD8C8", opacity=75, stroke=NONE)
d.shape("ellipse", "Wet gloss 2", x=470, y=582, width=9, height=5,
        fill="#FFD8C8", opacity=60, stroke=NONE)
# a stray tacky droplet
d.shape("ellipse", "Wax droplet", x=496, y=604, width=8, height=6,
        fill="#B8322C", opacity=85, stroke=NONE)

# --- the arm holding the memo flat ---------------------------------------------------
d.path("M596,520 C560,528 540,540 522,550", "Memo arm", fill=NONE,
       stroke="#B58C64", strokeWidth=20, cap="round")
d.shape("ellipse", "Memo paw", x=508, y=540, width=36, height=26,
        fill="#DCB894", stroke=INK, strokeWidth=4)

# --- the seal press, mid-stamp ---------------------------------------------------------
# fresh wax sliver peeking from under the head
d.path("M564,588 C576,584 588,586 594,592 C586,596 572,596 564,592 Z",
       "Wax sliver", fill="#C03830", stroke=NONE)
d.shape("ellipse", "Seal contact shadow", x=542, y=588, width=70, height=12,
        fill="#3A2418", opacity=50, stroke=NONE)
# brass head tilted forward onto the paper
d.shape("ellipse", "Seal head", x=542, y=566, width=66, height=30,
        fill=BRASS_GRAD, stroke=INK, strokeWidth=4)
d.path("M554,570 L556,548 L594,548 L596,570 Z", "Seal collar",
       fill=BRASS_GRAD, stroke=INK, strokeWidth=3.5, join="round")
# wooden handle + knob
d.shape("rectangle", "Handle", x=564, y=480, width=22, height=70,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=3.5, radius=8)
d.shape("ellipse", "Knob", x=554, y=456, width=44, height=30,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Knob sheen", x=562, y=462, width=16, height=8,
        fill="#C89868", opacity=60, stroke=NONE)
# arm from body to the press
d.path("M680,470 C654,466 626,464 602,466", "Press arm", fill=NONE,
       stroke="#B58C64", strokeWidth=20, cap="round")
# the pressing paw over the knob
d.shape("ellipse", "Press paw", x=552, y=450, width=50, height=40,
        fill="#DCB894", stroke=INK, strokeWidth=4)
d.path("M566,462 L566,478 M578,462 L578,478 M590,462 L590,478",
       "Paw toes", fill=NONE, stroke=INK, strokeWidth=2.5, cap="round",
       opacity=70)

# --- the ink pot ---------------------------------------------------------------------
d.shape("ellipse", "Ink pot shadow", x=278, y=606, width=52, height=10,
        fill="#2A1A12", opacity=50, stroke=NONE)
d.path("M284,566 C284,556 292,550 302,550 C312,550 320,556 320,566 "
       "L320,602 C320,608 284,608 284,602 Z", "Ink pot",
       fill="#1E1410", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Ink surface", x=290, y=552, width=24, height=9,
        fill="#3A1E20", stroke=NONE)
d.shape("ellipse", "Ink sheen", x=294, y=554, width=9, height=4,
        fill="#8A4E50", opacity=80, stroke=NONE)
# a quill resting against the pot
d.path("M318,588 C330,566 344,548 360,540", "Quill shaft", fill=NONE,
       stroke="#D8C69E", strokeWidth=3.5, cap="round")
d.path("M344,548 C354,532 372,526 382,530 C378,544 362,554 344,548 Z",
       "Quill feather", fill="#E4D6B4", stroke=INK, strokeWidth=2.5,
       opacity=90)

# --- motes ------------------------------------------------------------------------------
for i, (x, y, w) in enumerate([(262,420,6),(244,560,5),(640,240,5),(836,470,6),
                               (224,640,6),(812,300,5),(548,212,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8B46A", opacity=40, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("ALIBI SEAL", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#F0E2CE", justify="center")
r = d.text("ABSOLVED BEFORE THE ASKING", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8A884", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("271.alibi-seal-V1R00")
