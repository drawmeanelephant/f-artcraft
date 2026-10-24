#!/usr/bin/env python3
"""Cssandra Cascade — mascot portrait V1R00. Visual Chaos Harmonizer:
a figure assembled from reset.css box fragments (solid, dashed, dotted
borders, each casting a box-shadow), held in devtools-orange margin bands
that visibly collapse where they overlap; the last fragment still floats
in above. A tarsier with enormous eyes watches over a weathered manual,
footnoted as a warning. Rebeccapurple palette. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Cssandra Cascade — Mascot Plate", 1000, 1000)

INK = "#33244A"   # warm violet ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#1B1230"}, {"offset": 1, "color": "#080511"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D9CFEB"}, {"offset": 0.62, "color": "#A88BD0"},
    {"offset": 1, "color": "#6D4FA0"}]}}
BOX_A = {"gradient": {"kind": "linear", "start": [0, 300], "end": [0, 430], "stops": [
    {"offset": 0, "color": "#F2EBF8"}, {"offset": 1, "color": "#D4C2E8"}]}}
BOX_B = {"gradient": {"kind": "linear", "start": [0, 420], "end": [0, 545], "stops": [
    {"offset": 0, "color": "#E2D4F2"}, {"offset": 1, "color": "#B99EDA"}]}}
BOX_C = {"gradient": {"kind": "linear", "start": [0, 540], "end": [0, 660], "stops": [
    {"offset": 0, "color": "#D0BEE6"}, {"offset": 1, "color": "#A586CC"}]}}
TARSIER_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8AE82"}, {"offset": 0.7, "color": "#B98A5E"},
    {"offset": 1, "color": "#8A5F3E"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E6D8B4"}, {"offset": 1, "color": "#C4AF82"}]}}
IRIS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2C96E"}, {"offset": 1, "color": "#B97E2E"}]}}
MARGIN = "#E8A33D"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def frag(cx, cy, w, h, deg, fill, label, dash=None, shadow=True):
    """One reset.css fragment: a rotated box + its offset box-shadow."""
    if shadow:
        d.path(rot_rect_path(cx + 9, cy + 12, w, h, deg), f"{label} shadow",
               fill="#3A2454", opacity=22, stroke=NONE)
    kw = {} if dash is None else {"dash": dash}
    d.path(rot_rect_path(cx, cy, w, h, deg), label,
           fill=fill, stroke=INK, strokeWidth=3.5, **kw)

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#8A6AB8", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#241640", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4DBF2", strokeWidth=3, opacity=40)
# patina + flecks
d.shape("ellipse", "Patina 1", x=180, y=150, width=250, height=160, fill="#C4B2E2", opacity=16, stroke=NONE)
d.shape("ellipse", "Patina 2", x=580, y=620, width=260, height=150, fill="#7E5EAE", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(200,340,6),(800,320,5),(170,560,7),(840,560,6),(240,760,5),
                               (748,768,6),(140,450,5),(870,430,4),(440,120,5),(620,140,6),
                               (330,150,4),(710,210,5),(640,800,4),(190,660,4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#EAE2F6", opacity=45, stroke=NONE)
# stray selectors drifting down the right margin
for i, (x, y, op) in enumerate([(700, 300, 20), (730, 430, 14), (705, 560, 9)]):
    d.text("}", f"Cascade brace {i+1}", x=x, y=y, size=30, font="Source Sans 3",
           color="#D8CCEE")
    doc = d.call("inspect_document", {"kind": "Type"}, f"inspect brace {i+1}")
    for n in (doc or {}).get("nodes", []):
        if str(n.get("name", "")) == f"Cascade brace {i+1}":
            d.call("run_command", {"command": "object.setProps",
                   "params": {"id": n["id"], "opacity": op}}, f"brace {i+1} opacity")

# --- collapsing margins (devtools orange, overlapping = collapsed) ----------------
# outer margins: above the stack, below the stack
d.shape("rectangle", "Margin top", x=368, y=262, width=224, height=26,
        fill=MARGIN, opacity=28, stroke=NONE)
d.shape("rectangle", "Margin bottom", x=372, y=652, width=220, height=26,
        fill=MARGIN, opacity=28, stroke=NONE)
# collapsed pair between head and torso: two bands meeting in one seam
d.shape("rectangle", "Margin head bottom", x=350, y=418, width=290, height=18,
        fill=MARGIN, opacity=40, stroke=NONE)
d.shape("rectangle", "Margin torso top", x=352, y=408, width=286, height=18,
        fill=MARGIN, opacity=40, stroke=NONE)
# and between torso and base
d.shape("rectangle", "Margin torso bottom", x=356, y=530, width=270, height=18,
        fill=MARGIN, opacity=40, stroke=NONE)
d.shape("rectangle", "Margin base top", x=358, y=520, width=266, height=18,
        fill=MARGIN, opacity=40, stroke=NONE)
# collapse indicator: two arrows squeezing the seam shut
d.path("M636,392 L636,410 L628,410 L642,424 L656,410 L648,410 L648,392 Z",
       "Collapse arrow dn", fill=MARGIN, opacity=75, stroke=NONE)
d.path("M636,470 L636,452 L628,452 L642,438 L656,452 L648,452 L648,470 Z",
       "Collapse arrow up", fill=MARGIN, opacity=75, stroke=NONE)
d.text("margin: 0;", "Margin label", x=404, y=282, size=14, font="Source Sans 3",
       color="#8A5F1E")

# --- the floating fragment, mid-assembly ------------------------------------------
for i, (dx, dy) in enumerate([(-56, -30), (0, -42), (56, -30)]):
    d.path(f"M{478+dx},{238+dy} L{478+dx},{222+dy}", f"Arrive tick {i+1}",
           fill=NONE, stroke=INK, strokeWidth=3, opacity=55, cap="round")
frag(478, 246, 92, 52, 10, BOX_A, "Floating fragment", dash=[6, 4])
d.text("* {", "Reset snippet", x=416, y=252, size=15, font="Source Sans 3",
       color="#5A4370")

# --- Cssandra: stacked fragments ---------------------------------------------------
frag(468, 598, 200, 108, -2, BOX_C, "Base box", dash=[2, 5])
frag(458, 476, 230, 112, 3, BOX_B, "Torso box", dash=[9, 5])
frag(480, 364, 192, 104, -4, BOX_A, "Head box")
# arm fragments: one shrugs off-axis, one floats half-attached
frag(330, 508, 84, 34, -18, BOX_B, "Arm L")
frag(622, 452, 90, 34, 14, BOX_B, "Arm R")
# feet
frag(424, 664, 58, 26, -6, BOX_C, "Foot L", shadow=False)
frag(528, 662, 58, 26, 5, BOX_C, "Foot R", shadow=False)

# torso embroidery: a tiny declaration that never applied
d.text("!important", "Declaration", x=486, y=520, size=15, font="Source Sans 3",
       color="#6A4F92")

# face on the head box: mismatched eyes, elegantly unstable
d.shape("ellipse", "Eye L", x=424, y=346, width=40, height=40,
        fill="#F6F1FA", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Iris L", x=432, y=354, width=20, height=20,
        fill="#6D4FA0", stroke=NONE)
d.shape("ellipse", "Pupil L", x=438, y=360, width=9, height=9, fill="#241640", stroke=NONE)
d.shape("ellipse", "Glint L", x=440, y=362, width=4, height=4, fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Eye R", x=504, y=350, width=32, height=32,
        fill="#F6F1FA", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Iris R", x=510, y=356, width=16, height=16,
        fill="#6D4FA0", stroke=NONE)
d.shape("ellipse", "Pupil R", x=515, y=361, width=7, height=7, fill="#241640", stroke=NONE)
d.shape("ellipse", "Glint R", x=517, y=362, width=3.5, height=3.5, fill="#FFFFFF", opacity=85, stroke=NONE)
# one sceptical brow, slightly off-register like an unoverridden rule
d.path("M420,332 C436,324 452,324 464,330", "Brow",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# flat tilted mouth: rendered, not consulted
d.path("M456,398 L508,393", "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")

# --- the tarsier, watching from a weathered manual ---------------------------------
TX, TY = 322, 682
# ears first (behind head): thin rounded bat ears
d.path(f"M{TX-40},{TY-38} C{TX-58},{TY-72} {TX-52},{TY-92} {TX-30},{TY-66} Z",
       "Ear L", fill="#B98A5E", stroke=INK, strokeWidth=3)
d.path(f"M{TX+40},{TY-38} C{TX+58},{TY-72} {TX+52},{TY-92} {TX+30},{TY-66} Z",
       "Ear R", fill="#B98A5E", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Head", x=TX - 46, y=TY - 44, width=92, height=92,
        fill=TARSIER_GRAD, stroke=INK, strokeWidth=4)
# the enormous eyes, nearly touching
for ex in (-22, 22):
    d.shape("ellipse", f"T-eye {ex}", x=TX + ex - 21, y=TY - 30, width=42, height=42,
            fill="#F8F0DC", stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"T-iris {ex}", x=TX + ex - 14, y=TY - 22, width=28, height=28,
            fill=IRIS_GRAD, stroke=NONE)
    d.shape("ellipse", f"T-pupil {ex}", x=TX + ex - 7, y=TY - 14, width=14, height=14,
            fill="#1E1408", stroke=NONE)
    d.shape("ellipse", f"T-glint {ex}", x=TX + ex - 3, y=TY - 16, width=6, height=6,
            fill="#FFFFFF", opacity=90, stroke=NONE)
# tiny nose + mouth peeking over the book
d.path(f"M{TX-6},{TY+16} L{TX+6},{TY+16} L{TX},{TY+24} Z", "T-nose",
       fill="#7A4E30", stroke=NONE)

# the manual: open, weathered, footnoted as a warning
d.path("M264,720 L328,714 L330,784 L260,778 Z", "Page L",
       fill=PAGE_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M336,714 L404,720 L410,778 L334,784 Z", "Page R",
       fill=PAGE_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M328,714 L336,714 L334,784 L330,784 Z", "Spine",
       fill="#8A5F3C", stroke=NONE)
# cover edges peeking out
d.path("M260,778 L410,778 L412,788 L258,788 Z", "Cover edge",
       fill="#8A5F3C", stroke=INK, strokeWidth=3)
# faded text lines + a coffee ring of provenance
for i, y in enumerate([730, 742, 754]):
    d.path(f"M274,{y} L318,{y-3}", f"Text L {i+1}", fill=NONE,
           stroke="#7A6440", strokeWidth=2.5, opacity=45, cap="round")
    d.path(f"M346,{y-3} L394,{y}", f"Text R {i+1}", fill=NONE,
           stroke="#7A6440", strokeWidth=2.5, opacity=45, cap="round")
d.shape("ellipse", "Coffee ring", x=352, y=742, width=34, height=26,
        fill=NONE, stroke="#8A5F3C", strokeWidth=3, opacity=30)
# tarsier fingers curled over the top edge
for i, fx in enumerate([TX - 30, TX - 18, TX + 16, TX + 28]):
    d.shape("ellipse", f"Finger {i+1}", x=fx, y=700 + (i % 2) * 3, width=10, height=18,
            fill="#C89B72", stroke=INK, strokeWidth=2.5)
for x, y in [(260, 720), (410, 720), (258, 788), (412, 788)]:
    assert on_disc(x, y, 10), (x, y)

# --- name + role --------------------------------------------------------------------
d.text("CSSANDRA CASCADE", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E2D8F2", justify="center")
d.text("VISUAL CHAOS HARMONIZER", "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#B49EDA", justify="center")
doc = d.call("inspect_document", {"kind": "Type"}, "inspect type")
for n in (doc or {}).get("nodes", []):
    if str(n.get("name", "")) == "Role":
        d.call("run_command", {"command": "text.setStyle",
               "params": {"id": n["id"], "tracking": 260}}, "track role")

d.finish("008.cssandra-cascade-V1R00")
