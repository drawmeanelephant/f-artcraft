#!/usr/bin/env python3
"""Sanctioned Quilt — mascot portrait V1R00.
A heavy committee-assembled quilt standing folded like a sentry: off-cut
squares, triple-stitched compliance seams, button eyes that give no opinion,
and one loose thread on the third quadrant that nobody may pull. A second
quilt waits folded beside it, already issued. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Sanctioned Quilt — Mascot Portrait", 1000, 1000)

INK = "#3A2822"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#181016"}, {"offset": 1, "color": "#0A0608"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4C3A3A"}, {"offset": 0.7, "color": "#2C2024"},
    {"offset": 1, "color": "#161014"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#332627"}, {"offset": 1, "color": "#141011"}]}}
BINDING = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#54403A"}, {"offset": 1, "color": "#32241F"}]}}
CUFF = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A6E7E"}, {"offset": 1, "color": "#37444F"}]}}
THREAD = "#C9A24C"

# patch palette: sincere fragments, committee-muted
PATCHES = [("#9A6A6A", "#7A4E50"), ("#7E7A52", "#5E5A3C"),
           ("#B08A50", "#8A6838"), ("#5A6E80", "#3E5060"),
           ("#8A5240", "#663A2C"), ("#B0A48A", "#8A7E66")]

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6A5E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C4AE", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A3A38", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E0A08",
       strokeWidth=4, opacity=70)

# --- the second quilt, already issued ---------------------------------------------
d.shape("ellipse", "Spare shadow", x=700, y=676, width=140, height=18,
        fill="#080606", opacity=50, stroke=NONE)
for i, (y, c) in enumerate([(652, "#5A6E80"), (630, "#7E7A52"), (608, "#9A6A6A")]):
    d.shape("rectangle", f"Spare fold {i+1}", x=716, y=y, width=112, height=26,
            fill=c, stroke=INK, strokeWidth=4, radius=10)
    d.path(f"M716,{y+13} L828,{y+13}", f"Spare seam {i+1}", fill=NONE,
           stroke=THREAD, strokeWidth=2, dash=[6, 5], opacity=70)

# --- the quilt body -----------------------------------------------------------------
d.shape("ellipse", "Quilt shadow", x=300, y=668, width=400, height=34,
        fill="#080606", opacity=55, stroke=NONE)
# binding silhouette: the dark backing every square was pasted onto
d.shape("rectangle", "Quilt body", x=308, y=300, width=384, height=398,
        fill=BINDING, stroke=INK, strokeWidth=7, radius=36)

# --- off-cut squares ---------------------------------------------------------------
cols = [332, 416, 500, 584]
rows = [418, 483, 548, 613]
rota = [1.6, -1.2, 1.0, -1.7]
k = 0
for r, y in enumerate(rows):
    for c, x in enumerate(cols):
        hi, lo = PATCHES[(r * 4 + c) % len(PATCHES)]
        ang = rota[(r + c) % 4]
        d.path(rot_rect_path(x + 36, y + 28, 72, 56, ang),
               f"Patch {r+1}-{c+1}",
               fill={"gradient": {"kind": "linear", "stops": [
                   {"offset": 0, "color": hi}, {"offset": 1, "color": lo}]}},
               stroke=INK, strokeWidth=3, join="round")
        # one honest stitch row across each fragment
        d.path(f"M{x+8},{y+28} L{x+64},{y+28}", f"Patch stitch {r+1}-{c+1}",
               fill=NONE, stroke=THREAD, strokeWidth=2.5,
               dash=[6, 5], opacity=65)
        k += 1

# worn corners where earlier initiatives show through
d.shape("ellipse", "Wear 1", x=356, y=560, width=40, height=22,
        fill="#2E2020", opacity=30, stroke=NONE)
d.shape("ellipse", "Wear 2", x=580, y=430, width=34, height=20,
        fill="#2E2020", opacity=25, stroke=NONE)

# the APPROVED stamp, third quadrant-adjacent, slightly crooked
d.path(rot_rect_path(600, 644, 78, 36, -7), "Approval stamp",
       fill=NONE, stroke="#7E3630", strokeWidth=3.5, join="round")
d.text("APPROVED", "Stamp text", x=572, y=652, size=10,
       font="Virelai Sans", color="#7E3630", justify="left")

# --- triple-stitched compliance seams -------------------------------------------------
# three rows of gold thread where the cuff meets the field
for i, y in enumerate([394, 403, 412]):
    d.path(f"M322,{y} L678,{y}", f"Compliance seam top {i+1}", fill=NONE,
           stroke=THREAD, strokeWidth=2.5, dash=[7, 5], opacity=85)
# and binding the hem, left and right
for i, y in enumerate([676, 685, 694]):
    d.path(f"M328,{y} L672,{y}", f"Compliance seam hem {i+1}", fill=NONE,
           stroke=THREAD, strokeWidth=2.5, dash=[7, 5], opacity=80)
for i, x in enumerate([318, 327, 336]):
    d.path(f"M{x},410 L{x},664", f"Compliance seam L {i+1}", fill=NONE,
           stroke=THREAD, strokeWidth=2.5, dash=[7, 5], opacity=75)
for i, x in enumerate([664, 673, 682]):
    d.path(f"M{x},410 L{x},664", f"Compliance seam R {i+1}", fill=NONE,
           stroke=THREAD, strokeWidth=2.5, dash=[7, 5], opacity=75)

# --- the folded cuff -------------------------------------------------------------------
d.shape("rectangle", "Cuff", x=294, y=288, width=412, height=100,
        fill=CUFF, stroke=INK, strokeWidth=6, radius=30)
d.shape("ellipse", "Cuff sheen", x=330, y=298, width=200, height=30,
        fill="#FFFFFF", opacity=12, stroke=NONE)
# cuff quilting stitches
for i, y in enumerate([322, 340, 358]):
    d.path(f"M312,{y} L688,{y}", f"Cuff stitch {i+1}", fill=NONE,
           stroke=THREAD, strokeWidth=2.5, dash=[8, 6], opacity=75)
# the fold's underside shadow
d.shape("rectangle", "Cuff underside", x=308, y=376, width=384, height=14,
        fill="#241A16", opacity=55, stroke=NONE, radius=6)

# --- the face: button eyes, the stitching gives no opinion -----------------------------
for i, cx in enumerate([452, 548]):
    d.shape("ellipse", f"Button {i+1}", x=cx - 15, y=436, width=30, height=30,
            fill="#241A18", stroke=INK, strokeWidth=3)
    d.path(f"M{cx-7},445 L{cx+7},457 M{cx+7},445 L{cx-7},457",
           f"Button thread {i+1}", fill=NONE, stroke=THREAD,
           strokeWidth=2.5, cap="round")
# a mouth that is technically a seam
d.path("M470,506 L530,506", "Mouth seam", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round", dash=[9, 7])
# blush rendered as darning
for i, cx in enumerate([408, 592]):
    for j in range(3):
        d.path(f"M{cx-10+j*8},484 L{cx-10+j*8},498", f"Darn {i+1}-{j+1}",
               fill=NONE, stroke="#8A5A52", strokeWidth=2.5,
               cap="round", opacity=60)

# --- the single loose thread on the third quadrant --------------------------------------
d.path("M500,640 C492,668 512,690 500,712 C490,730 506,742 518,736",
       "Loose thread", fill=NONE, stroke=THREAD, strokeWidth=3,
       cap="round", opacity=90)
d.shape("ellipse", "Thread coil", x=512, y=730, width=22, height=10,
        fill=NONE, stroke=THREAD, strokeWidth=2.5, opacity=70)
# the redacted incident report, pinned to a hem — permanently
d.path(rot_rect_path(648, 566, 46, 56, 6), "Incident tag",
       fill="#C9BCA4", stroke=INK, strokeWidth=3, join="round")
d.path("M634,556 L664,552 M636,566 L664,562 M638,576 L662,572",
       "Tag lines", fill=NONE, stroke="#8A7460", strokeWidth=2,
       opacity=80)
d.path("M632,586 L668,580", "Redaction", fill=NONE, stroke="#4A3230",
       strokeWidth=6, cap="round")

# --- plate-side motifs: two stray patch scraps ------------------------------------------
d.path(rot_rect_path(206, 616, 54, 54, -10), "Stray scrap 1",
       fill="#5A6E80", stroke=INK, strokeWidth=3, join="round", opacity=80)
d.path(rot_rect_path(782, 330, 44, 44, 14), "Stray scrap 2",
       fill="#8A5240", stroke=INK, strokeWidth=3, join="round", opacity=75)

# --- captions -------------------------------------------------------------------------
d.text("SANCTIONED QUILT", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#EDDCC6", justify="center")
r = d.text("KEEPER OF THE COVERAGE MAP", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C9A98E", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("295.sanctioned-quilt-V1R00")
