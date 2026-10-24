#!/usr/bin/env python3
"""APH-003 Blamey McTypoface — aphorism plate V1R00. A routing-slip form
stamped mid-impression on its ROOT CAUSE field while papers fly between
two filing cabinets toward the wrong department; a scapegoat badge pinned
on the corner. Bureaucratic warm dark ink, translucent document layers.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-003 Blamey McTypoface — Aphorism Plate", 1000, 1000)

INK = "#33200F"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#241812"}, {"offset": 1, "color": "#0F0805"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5A3B22"}, {"offset": 0.7, "color": "#33200F"},
    {"offset": 1, "color": "#1A0E07"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E2C4"}, {"offset": 0.65, "color": "#DCC79E"},
    {"offset": 1, "color": "#B99F72"}]}}
METAL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6B6A58"}, {"offset": 0.55, "color": "#4E4D3E"},
    {"offset": 1, "color": "#2E2D24"}]}}
DRAWER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C5B4A"}, {"offset": 1, "color": "#3A392E"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A4E2A"}, {"offset": 0.6, "color": "#543318"},
    {"offset": 1, "color": "#33200F"}]}}
STAMP_RED = "#A63A2E"
CREAM = "#F0E2C4"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A5230", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8C890", strokeWidth=3, opacity=40)
# plate patina
d.shape("ellipse", "Patina 1", x=200, y=170, width=200, height=120,
        fill="#6E4A2C", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=600, width=220, height=130,
        fill="#6E4A2C", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(210, 260, 7), (790, 250, 8), (160, 480, 6),
                               (840, 470, 7), (250, 640, 6), (750, 650, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A6A42", opacity=35, stroke=NONE)

# --- filing cabinets ----------------------------------------------------------
def cabinet(cx, label, dept):
    # cx = left edge
    d.shape("rectangle", f"{label} body", x=cx, y=300, width=110, height=240,
            radius=6, fill=METAL_GRAD, stroke=INK, strokeWidth=4)
    d.shape("rectangle", f"{label} top lip", x=cx - 4, y=292, width=118,
            height=14, radius=4, fill="#7A7962", stroke=INK, strokeWidth=3)
    for j, dy in enumerate([314, 402]):
        d.shape("rectangle", f"{label} drawer {j+1}", x=cx + 10, y=dy,
                width=90, height=76, radius=4, fill=DRAWER_GRAD,
                stroke=INK, strokeWidth=3)
        # label holder
        d.shape("rectangle", f"{label} label {j+1}", x=cx + 30, y=dy + 12,
                width=50, height=18, radius=2, fill="#C9BD96",
                stroke=INK, strokeWidth=2)
        # pull handle
        d.path(f"M{cx + 38},{dy + 50} L{cx + 72},{dy + 50}",
               f"{label} handle {j+1}", fill=NONE, stroke="#8A8970",
               strokeWidth=6, cap="round")
    # department tag on top drawer label
    d.text(dept, f"{label} dept", x=cx + 55, y=326, size=9,
           font="Virelai Sans", color=INK, justify="center")
    # feet shadow
    d.shape("ellipse", f"{label} shadow", x=cx - 8, y=540, width=126,
            height=18, fill="#000000", opacity=30, stroke=NONE)

cabinet(150, "Cabinet A", "DEPT A")
cabinet(740, "Cabinet B", "DEPT B")

# --- papers in flight, left cabinet to right cabinet ---------------------------
# dashed trajectory arc
d.path("M265,315 Q500,130 735,315", "Paper route", fill=NONE,
       stroke="#E8C890", strokeWidth=2.5, opacity=35, dash=[8, 10])

def flying_paper(cx, cy, w, h, deg, label):
    d.path(rot_rect_path(cx, cy, w, h, deg), f"{label} sheet",
           fill=PAPER_GRAD, stroke=INK, strokeWidth=2.5, opacity=92)
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    for k in range(3):
        lw = w * (0.62 - k * 0.08)
        ly = -h * 0.22 + k * h * 0.2
        lx = cx - ly * s
        lyy = cy + ly * c
        # ink line as a thin rotated rect
        d.path(rot_rect_path(lx, lyy, lw, 3.5, deg), f"{label} line {k+1}",
               fill=INK, opacity=55, stroke=NONE)

flying_paper(330, 268, 58, 76, -16, "Paper 1")
flying_paper(445, 212, 62, 82, -6, "Paper 2")
flying_paper(575, 208, 60, 80, 9, "Paper 3")
flying_paper(688, 258, 56, 74, 17, "Paper 4")
# one sheet slipping off the wrong side, falling toward Dept B's slot
flying_paper(795, 380, 50, 66, 42, "Stray paper")

# --- desk ----------------------------------------------------------------------
d.shape("ellipse", "Desktop", x=185, y=645, width=630, height=55,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Desk sheen", x=260, y=652, width=480, height=18,
        fill="#9A6A3E", opacity=45, stroke=NONE)

# --- the form -------------------------------------------------------------------
d.shape("rectangle", "Form shadow", x=343, y=330, width=330, height=380,
        radius=4, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Routing form", x=335, y=322, width=330, height=380,
        radius=4, fill=PAPER_GRAD, stroke=INK, strokeWidth=4)
# dog-ear fold, top right
d.path("M635,322 L665,352 L635,352 Z", "Dog ear", fill="#C9B183",
       stroke=INK, strokeWidth=3)
d.text("ROUTING SLIP 88-B", "Form header", x=365, y=352,
       size=14, font="Virelai Sans", color=INK, justify="left")
d.path("M365,368 L635,368", "Header rule", fill=NONE, stroke=INK,
       strokeWidth=2, opacity=70)
# faint ruled rows
for k, ry in enumerate([560, 585, 640]):
    d.path(f"M365,{ry} L635,{ry}", f"Form rule {k+1}", fill=NONE,
           stroke=INK, strokeWidth=1.5, opacity=30)

# scapegoat badge pinned on the form, upper left
d.shape("ellipse", "Badge shadow", x=361, y=392, width=56, height=56,
        fill="#000000", opacity=25, stroke=NONE)
d.shape("ellipse", "Scapegoat badge", x=356, y=386, width=56, height=56,
        fill="#E8D6B0", stroke=STAMP_RED, strokeWidth=4)
d.shape("ellipse", "Badge pin", x=381, y=389, width=7, height=7,
        fill=INK, stroke=NONE)
# goat head inside the badge: skull + horns + ears
d.shape("ellipse", "Goat head", x=376, y=408, width=16, height=20,
        fill=INK, stroke=NONE)
d.path("M378,410 Q372,396 366,394", "Goat horn L", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
d.path("M390,410 Q396,396 402,394", "Goat horn R", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
d.path("M374,416 L368,422", "Goat ear L", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
d.path("M394,416 L400,422", "Goat ear R", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")

# --- the stamp, mid-impression over the ROOT CAUSE field -----------------------
# grip + stem rise above the form top edge — the stamp descends from off-page
d.shape("ellipse", "Stamp grip", x=516, y=252, width=88, height=44,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Grip sheen", x=532, y=258, width=40, height=14,
        fill="#A8763E", opacity=60, stroke=NONE)
d.shape("rectangle", "Stamp neck", x=542, y=292, width=36, height=24,
        fill="#543318", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Stamp stem", x=550, y=312, width=20, height=130,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=3)
# motion lines: the stamp is still coming down
for i, (mx, mh) in enumerate([(515, 26), (605, 26), (530, 18), (590, 18)]):
    d.path(f"M{mx},{228 - mh} L{mx},228", f"Stamp motion {i+1}", fill=NONE,
           stroke=CREAM, strokeWidth=3.5, opacity=55, cap="round")
# metal collar + rubber base pressed onto the field
d.shape("rectangle", "Stamp collar", x=512, y=436, width=96, height=18,
        radius=3, fill="#8A8970", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Stamp base", x=504, y=452, width=112, height=34,
        radius=4, fill="#7E2B22", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Base sheen", x=510, y=456, width=100, height=10,
        fill="#B8543E", opacity=55, stroke=NONE)

# --- form fields ------------------------------------------------------------------
d.text("ROOT CAUSE:", "Field label", x=370, y=522, size=15,
       font="Virelai Sans", color=INK, justify="left")
d.shape("rectangle", "Field box", x=370, y=534, width=260, height=52,
        fill=NONE, stroke=INK, strokeWidth=2, opacity=75)
# fresh REASSIGNED impression slammed into the box — ring + ghost offset
d.shape("ellipse", "Impression ghost", x=491, y=518, width=150, height=76,
        fill=NONE, stroke=STAMP_RED, strokeWidth=4, opacity=25)
d.shape("ellipse", "Impression ring", x=485, y=512, width=150, height=76,
        fill=NONE, stroke=STAMP_RED, strokeWidth=5, opacity=80)
r = d.text("REASSIGNED", "Impression text", x=560, y=558, size=16,
           font="Virelai Sans", color=STAMP_RED, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "impression tracking", ids=[r["id"]], tracking=45)
# forwarded-to line: the wrong department
d.text("FORWARDED TO:", "Fwd label", x=370, y=615, size=13,
       font="Virelai Sans", color=INK, justify="left")
d.text("DEPT. B — NOT OURS", "Fwd value", x=500, y=615, size=13,
       font="Virelai Sans", color=STAMP_RED, justify="left")
# signature squiggle + date line
d.path("M370,668 Q390,652 408,666 Q424,678 440,664 Q454,654 468,666",
       "Signature", fill=NONE, stroke=INK, strokeWidth=2.5, opacity=80)
d.path("M560,672 L640,672", "Date line", fill=NONE, stroke=INK,
       strokeWidth=1.5, opacity=60)
# coffee ring, lower left of the form
d.shape("ellipse", "Coffee ring", x=352, y=676, width=44, height=26,
        fill=NONE, stroke="#6B4423", strokeWidth=4, opacity=30)

# slide motion: the form was pushed from the left
for i, (my, mw) in enumerate([(470, 44), (500, 58), (530, 40)]):
    d.path(f"M{322 - mw},{my} L322,{my}", f"Slide motion {i+1}", fill=NONE,
           stroke=CREAM, strokeWidth=3.5, opacity=45, cap="round")

# --- aphorism line + name + role --------------------------------------------------
r = d.text("THE SYSTEM KEPT THE RITUAL", "Key line 1", x=500, y=738,
           size=22, font="Virelai Sans", color="#E8C890", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key1 tracking", ids=[r["id"]], tracking=110)
r = d.text("AND MISPLACED THE FUNCTION.", "Key line 2", x=500, y=772,
           size=22, font="Virelai Sans", color="#E8C890", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key2 tracking", ids=[r["id"]], tracking=110)

d.text("BLAMEY MCTYPOFACE", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color="#F0E2C4", justify="center")
r = d.text("ROOT CAUSE REASSIGNED", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color="#C9906A", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-003-blamey-mctypoface-V1R00")
