#!/usr/bin/env python3
"""Lionell Pancake Auditor — mascot portrait V1R00.
The examiner at the crowded luncheon table, holding up the syrup-marked
minutes: the same moment entered twice, once as atmosphere and once as
commitment. Warmly received is not a motion. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Lionell Pancake Auditor — Mascot Portrait", 1000, 1000)

INK = "#2A1A12"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E1410"}, {"offset": 1, "color": "#150F0C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E4634"}, {"offset": 0.7, "color": "#3E2C20"},
    {"offset": 1, "color": "#1E1410"}]}}
CLOTH_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2E6D0"}, {"offset": 1, "color": "#C4AC88"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DCAE72"}, {"offset": 0.7, "color": "#B07F4C"},
    {"offset": 1, "color": "#7C5832"}]}}
MANE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9A6636"}, {"offset": 0.75, "color": "#6E4522"},
    {"offset": 1, "color": "#4A2C14"}]}}
CAKE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8B96E"}, {"offset": 1, "color": "#B88340"}]}}
SYRUP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#A85E22"}, {"offset": 1, "color": "#5E2E0E"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4EAD2"}, {"offset": 1, "color": "#D8C8A4"}]}}
CUP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A4A3A"}, {"offset": 1, "color": "#5A2C22"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6A50", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D2BC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(198,238,8),(800,234,7),(162,530,9),(836,550,8),
                               (252,766,7),(750,752,9),(140,398,6),(862,394,7),
                               (396,116,7),(612,112,8),(338,824,6),(664,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E3A2C", opacity=45, stroke=NONE)

# --- the luncheon table, cloth hanging to the disc's own arc -------------------
d.path("M210,596 L790,596 L844,704 A420,420 0 0 1 156,704 Z", "Tablecloth",
       fill=CLOTH_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M210,596 L790,596", "Table edge", fill=NONE, stroke="#FFF6E4",
       strokeWidth=4, opacity=60, cap="round")
# cloth fold shadows
for fx in (330, 500, 670):
    d.path(f"M{fx},604 C{fx-8},660 {fx-10},700 {fx-6},740", f"Fold {fx}",
           fill=NONE, stroke="#A08A66", strokeWidth=3, opacity=45,
           cap="round")

# --- crowded-table hints: the neighbours' places, cropped by the rim ------------
for side, px in (("L", 196), ("R", 804)):
    d.shape("ellipse", f"Place {side}", x=px - 48, y=546, width=96, height=44,
            fill="#E4D4B6", stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Place inner {side}", x=px - 34, y=554, width=68,
            height=28, fill=NONE, stroke="#B09C7C", strokeWidth=2.5,
            opacity=70)
    # fork laid beside the plate
    d.path(f"M{px + (58 if side == 'L' else -58)},552 "
           f"L{px + (66 if side == 'L' else -66)},582", f"Fork {side}",
           fill=NONE, stroke="#C8C0B0", strokeWidth=4, cap="round")

# --- the pancake stack, still glossy with the stuff that bound us ----------------
for i, (w, y) in enumerate([(150, 552), (140, 534), (130, 517), (120, 500)]):
    d.shape("ellipse", f"Pancake {i+1}", x=290 - w/2, y=y, width=w, height=26,
            fill=CAKE_GRAD, stroke=INK, strokeWidth=3.5)
# syrup poured over the crown, running down the left flank
d.path("M262,498 C240,502 226,512 224,528 C222,544 230,556 236,566 "
       "L246,560 C240,548 238,536 242,524 C246,512 256,504 268,500 Z",
       "Syrup run", fill=SYRUP_GRAD, opacity=85, stroke=NONE)
d.shape("ellipse", "Syrup pool", x=238, y=494, width=64, height=20,
        fill=SYRUP_GRAD, stroke=INK, strokeWidth=3)
d.path("M272,498 C282,510 286,524 284,540", "Syrup drip", fill=NONE,
       stroke="#8A4A18", strokeWidth=5, cap="round", opacity=80)
# the pat of butter, melting into evidence
d.shape("rectangle", "Butter", x=270, y=486, width=34, height=16,
        fill="#F6DE8E", stroke=INK, strokeWidth=3, radius=4)
d.shape("ellipse", "Butter melt", x=258, y=498, width=58, height=10,
        fill="#F0D684", opacity=60, stroke=NONE)

# --- a coffee gone cold while the warmth was audited -------------------------------
d.shape("ellipse", "Cup shadow", x=690, y=576, width=96, height=18,
        fill="#1A0E08", opacity=45, stroke=NONE)
d.path("M712,514 L782,514 L774,580 L720,580 Z", "Cup", fill=CUP_GRAD,
       stroke=INK, strokeWidth=4, join="round")
d.path("M782,528 C800,526 806,542 800,556 C795,566 784,568 776,564",
       "Cup handle", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Coffee", x=718, y=512, width=58, height=14,
        fill="#3A2010", stroke=INK, strokeWidth=3)
d.path("M736,494 C730,482 740,476 736,464 M758,496 C752,484 762,478 758,466",
       "Steam", fill=NONE, stroke="#D8C8B4", strokeWidth=3, opacity=50,
       cap="round")

# --- Lionell himself: lion-mane ruff, good-natured suspicion ----------------------
d.shape("ellipse", "Body", x=415, y=560, width=190, height=130,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# the mane: a ring of scallop lobes behind the head
for i in range(14):
    a = math.radians(i * (360 / 14))
    cx, cy = 510 + 96 * math.cos(a), 418 + 96 * math.sin(a)
    d.shape("ellipse", f"Mane lobe {i+1}", x=cx - 26, y=cy - 26, width=52,
            height=52, fill=MANE_GRAD, stroke=INK, strokeWidth=3)
# ears tucked into the mane
for ex in (452, 568):
    d.shape("ellipse", f"Ear {ex}", x=ex - 13, y=330, width=26, height=24,
            fill="#B07F4C", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Head", x=430, y=338, width=160, height=148,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# muzzle and warm cheek shading
d.shape("ellipse", "Muzzle", x=472, y=424, width=76, height=50,
        fill="#E8C08A", opacity=70, stroke=NONE)
d.shape("ellipse", "Nose", x=498, y=414, width=24, height=16,
        fill="#5E3A20", stroke=INK, strokeWidth=3)
# the eyes: kindly, and counting
d.shape("ellipse", "Eye L", x=466, y=386, width=15, height=18,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=540, y=386, width=15, height=18,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=470, y=390, width=5, height=5,
        fill="#FFF6E4", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=544, y=390, width=5, height=5,
        fill="#FFF6E4", opacity=85, stroke=NONE)
# one brow raised over the minutes
d.path("M458,368 C468,361 480,360 488,364", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M534,360 C546,358 556,361 562,367", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M492,450 C500,455 512,455 520,450", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")

# --- the syrup-marked minutes, held up for the record -------------------------------
# arm reaching up on the viewer's right, gripping the page
d.path("M585,560 C620,540 640,512 652,486", "Arm papers", fill=NONE,
       stroke="#B07F4C", strokeWidth=17, cap="round")
# the page itself, tilted as held
d.path("M588,336 L734,322 L748,478 L602,492 Z", "Minutes page",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=4, join="round")
# the two columns: what the room felt | what the room committed
d.path("M664,330 L676,484", "Column rule", fill=NONE, stroke="#B8A880",
       strokeWidth=2.5, opacity=80)
for i, y in enumerate(range(352, 430, 14)):
    d.path(f"M600,{y} L652,{y - 2}", f"Felt line {i+1}", fill=NONE,
           stroke="#8A7A5E", strokeWidth=2.5, cap="round", opacity=80)
for i, y in enumerate(range(350, 424, 14)):
    d.path(f"M680,{y - 2} L730,{y - 4}", f"Committed line {i+1}", fill=NONE,
           stroke="#9A4A3A", strokeWidth=2.5, cap="round", opacity=85)
# the syrup ring: the pledge line's true signature
d.shape("ellipse", "Syrup ring", x=606, y=430, width=52, height=46,
        fill=NONE, stroke="#9A5A1E", strokeWidth=9, opacity=55)
d.shape("ellipse", "Syrup blot", x=652, y=462, width=16, height=12,
        fill="#9A5A1E", opacity=50, stroke=NONE)
# the paw on the page corner
d.shape("ellipse", "Paw grip", x=636, y=472, width=34, height=28,
        fill="#DCAE72", stroke=INK, strokeWidth=4)
# the other paw resting flat, doing nothing incriminating
d.path("M445,556 C430,568 424,580 424,590", "Arm rest", fill=NONE,
       stroke="#B07F4C", strokeWidth=16, cap="round")
d.shape("ellipse", "Paw rest", x=400, y=574, width=34, height=26,
        fill="#DCAE72", stroke=INK, strokeWidth=4)

# --- crumbs, motes, the smell of procedural regret ----------------------------------
for i, (x, y, w) in enumerate([(252,428,5),(330,300,6),(664,250,5),(820,480,6),
                               (240,700,5),(780,660,5),(380,240,5),(740,360,4)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8B894", opacity=35, stroke=NONE)

# --- captions ---------------------------------------------------------------------
d.text("LIONELL PANCAKE AUDITOR", "Name", x=500, y=930, size=52,
       font="Virelai Sans", color="#F0E4D2", justify="center")
r = d.text("LUNCHEON ASSENT EXAMINER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#D2A88E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("310.lionell-pancake-auditor-V1R00")
