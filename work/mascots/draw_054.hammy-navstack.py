#!/usr/bin/env python3
"""Hammy Navstack — mascot portrait V1R00.
A hamburger whose physical layers map to navigation routes: top bun
HOME, ketchup STORMS, patty MASCOTS, lettuce FORMS, bottom bun PDF
(the overstacked dropdown that rendered as a standalone document).
Route tags with leader lines, one breadcrumb trail chewed. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Hammy Navstack — Mascot Portrait", 1000, 1000)

INK = "#2E1E18"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#161014"}, {"offset": 1, "color": "#0A0608"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A5A66"}, {"offset": 0.7, "color": "#584049"},
    {"offset": 1, "color": "#33262D"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#443239"}, {"offset": 1, "color": "#221A1E"}]}}
BUN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0C878"}, {"offset": 0.65, "color": "#D89E4E"},
    {"offset": 1, "color": "#A86E30"}]}}
BUN_LO_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8A050"}, {"offset": 1, "color": "#9E6A2E"}]}}
PATTY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5238"}, {"offset": 1, "color": "#4A2E20"}]}}
LETTUCE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9EC86A"}, {"offset": 1, "color": "#5E8A3E"}]}}
CHEESE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0C84A"}, {"offset": 1, "color": "#C8982E"}]}}
KETCHUP = "#B83E32"
CHIP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8DCC0"}, {"offset": 1, "color": "#C8B898"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6A76", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C4CC", strokeWidth=3, opacity=35)
for i, (x, y, w) in enumerate([(190,240,8),(802,234,7),(152,522,9),(842,540,8),
                               (254,768,7),(748,754,9),(130,392,6),(864,398,7),
                               (390,110,7),(618,112,8),(338,822,6),(664,824,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E3A44", opacity=50, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#181014",
       strokeWidth=4, opacity=70)

# --- the hamburger-menu glyph, floated like a route beacon ------------------------
d.shape("ellipse", "Menu shadow", x=690, y=672, width=90, height=14,
        fill="#140E10", opacity=50, stroke=NONE)
d.path(rot_rect_path(722, 380, 86, 86, 6), "Menu chip",
       fill=CHIP_GRAD, stroke=INK, strokeWidth=4, join="round")
for j, dy in enumerate([-18, 0, 18]):
    d.path(rot_rect_path(722, 380+dy, 52, 8, 6), f"Menu bar {j+1}",
           fill="#5E4638", stroke=NONE)
d.text("MENU", "Menu label", x=722, y=436, size=10,
       font="Virelai Sans", color="#5E4638", justify="center")

# --- Hammy Navstack: the burger itself ---------------------------------------------
d.shape("ellipse", "Burger shadow", x=340, y=676, width=330, height=26,
        fill="#140E10", opacity=55, stroke=NONE)

# bottom bun: shallow dome, routes to a standalone PDF
d.path("M380,600 C376,652 430,680 500,680 C570,680 624,652 620,600 Z",
       "Bottom bun", fill=BUN_LO_GRAD, stroke=INK, strokeWidth=6,
       join="round")

# lettuce: frill spilling past both edges — it controls the forms
d.path("M366,560 C380,540 400,566 420,548 C440,530 460,560 480,546 "
       "C500,532 520,560 540,546 C560,532 580,560 600,548 "
       "C620,536 634,556 640,566 L634,596 C600,606 400,606 366,596 Z",
       "Lettuce", fill=LETTUCE_GRAD, stroke=INK, strokeWidth=5,
       join="round")
for j, lx in enumerate([400, 460, 520, 580]):
    d.path(f"M{lx},566 C{lx+8},574 {lx+16},578 {lx+24},580",
           f"Lettuce vein {j+1}", fill=NONE, stroke="#4E7030",
           strokeWidth=2, cap="round", opacity=60)

# patty: thick slab, governs mascots
d.path("M368,508 C364,536 372,556 380,564 L620,564 C628,556 636,536 632,508 "
       "C632,500 624,494 612,494 L388,494 C376,494 368,500 368,508 Z",
       "Patty", fill=PATTY_GRAD, stroke=INK, strokeWidth=6, join="round")
for j, (px, py) in enumerate([(420,520),(480,532),(560,518),(590,540),(440,548)]):
    d.shape("ellipse", f"Patty char {j+1}", x=px, y=py, width=14, height=7,
            fill="#38221A", opacity=60, stroke=NONE)

# cheese: melted square, corners drooping over the patty
d.path("M386,466 L614,466 L614,482 C614,492 600,494 596,486 "
       "C592,478 588,496 576,494 C566,492 570,480 560,482 "
       "L386,482 Z", "Cheese", fill=CHEESE_GRAD, stroke=INK,
       strokeWidth=4, join="round")

# ketchup: drippy band over the cheese — that's storms
d.path("M392,446 L608,446 L608,462 C600,472 592,458 584,468 "
       "C576,478 566,458 556,468 C546,478 536,460 526,468 "
       "C516,476 506,458 496,466 C486,474 474,458 464,466 "
       "C454,474 442,458 432,466 C422,474 410,458 400,466 "
       "C394,470 392,464 392,458 Z",
       "Ketchup", fill=KETCHUP, stroke=INK, strokeWidth=3.5, join="round")

# top bun: the dome, routes to HOME — and carries the face
d.path("M500,280 C596,280 646,344 644,430 L644,446 L356,446 L356,430 "
       "C354,344 404,280 500,280 Z",
       "Top bun", fill=BUN_GRAD, stroke=INK, strokeWidth=6, join="round")
d.shape("ellipse", "Bun hi", x=408, y=306, width=110, height=54,
        fill="#FFFFFF", opacity=18, stroke=NONE)
# sesame seeds
for i, (sx, sy, r) in enumerate([(430,330,-14),(500,310,6),(566,332,18),
                                 (462,366,-6),(548,368,10),(610,352,-20),
                                 (396,368,24),(500,352,-12),(584,318,4)]):
    d.path(rot_rect_path(sx, sy, 16, 8, r), f"Seed {i+1}",
           fill="#F4E4BC", stroke="#C89A50", strokeWidth=1.5)

# face on the bun: calm, nested three menus deep
for side, ex in [("L", 452), ("R", 522)]:
    d.shape("ellipse", f"Eye {side}", x=ex, y=372, width=26, height=30,
            fill=INK, stroke=NONE)
    d.shape("ellipse", f"Glint {side}", x=ex+6, y=376, width=8, height=8,
            fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M486,418 C496,426 512,426 522,418", "Smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Cheek L", x=424, y=408, width=28, height=13,
        fill="#C87058", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=550, y=408, width=28, height=13,
        fill="#C87058", opacity=45, stroke=NONE)

# --- route tags: chips with leader lines to their layers ----------------------------
def tag(x, y, label, tx, ty):
    """Chip at (x,y) — its right/left edge nearest the burger leads to (tx,ty)."""
    w = 30 + len(label) * 9.5
    d.shape("ellipse", f"{label} lead dot", x=tx-4, y=ty-4, width=8, height=8,
            fill="#E8DCC0", stroke=INK, strokeWidth=2)
    ex = x + w/2 if x < tx else x - w/2
    d.path(f"M{ex:.0f},{y} L{tx-6 if x<tx else tx+6:.0f},{ty}",
           f"{label} leader", fill=NONE, stroke="#E8DCC0",
           strokeWidth=2.5, cap="round", opacity=85)
    d.path(rot_rect_path(x, y, w, 26, 0), f"{label} chip",
           fill=CHIP_GRAD, stroke=INK, strokeWidth=3, join="round")
    d.text(label, f"{label} txt", x=x, y=y+6, size=12,
           font="Virelai Sans", color="#4E3A30", justify="center")

tag(240, 300, "HOME", 400, 330)      # -> top bun
tag(736, 480, "STORMS", 610, 462)    # -> ketchup
tag(214, 524, "MASCOTS", 372, 530)   # -> patty
tag(748, 590, "FORMS", 636, 580)     # -> lettuce
tag(252, 646, "PDF", 396, 622)       # -> bottom bun

# --- breadcrumb trail, literally chewed, leading to the burger ---------------------
d.text("HOME / MASCOTS / FORMS / ??", "Crumbs", x=176, y=732, size=13,
       font="Virelai Sans", color="#B09A8A", justify="left")
for i, (cx, cy) in enumerate([(208,714),(236,706),(266,712),(298,704)]):
    d.shape("ellipse", f"Crumb {i+1}", x=cx, y=cy, width=7, height=5,
            fill="#C89A50", stroke=NONE, opacity=80)
# one crumb bitten
d.path("M330,700 C334,696 342,697 344,702 C346,708 340,712 335,710 "
       "C330,708 328,704 330,700 Z M336,699 L340,703",
       "Bitten crumb", fill="#C89A50", stroke=INK, strokeWidth=1.5,
       opacity=80)

# --- captions ----------------------------------------------------------------------
d.text("HAMMY NAVSTACK", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F0E4DC", justify="center")
r = d.text("LAYERED FOR EVERY ROUTE · STACKED FOR EVERY MOOD", "Role",
           x=500, y=968, size=20, font="Virelai Sans", color="#C4ACB4",
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=120)

d.finish("054.hammy-navstack-V1R00")
