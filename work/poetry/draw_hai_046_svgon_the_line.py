#!/usr/bin/env python3
"""HAI-0046 Svgon The Line — haiku plate V1R00. Vector purity made visual:
Svgon with golden-ratio staff, validation medallion, anti-aliasing visor,
three haiku stanzas circling a central perfect bezier. Luminous, crisp.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("HAI-0046 Svgon The Line — Haiku Plate", 1000, 1000)

INK = "#101C2C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1626"}, {"offset": 1, "color": "#05080F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#37567E"}, {"offset": 0.7, "color": "#1E3250"},
    {"offset": 1, "color": "#0E1A2C"}]}}
COAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#B4CCE2"}, {"offset": 0.6, "color": "#6E90B0"},
    {"offset": 1, "color": "#3C5670"}]}}
GOLD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F6DC96"}, {"offset": 1, "color": "#C09038"}]}}
VISOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8F2FF"}, {"offset": 1, "color": "#6EB8E8"}]}}
ICE = "#D8ECFC"
SOFT = "#9EC2DE"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E94B8", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8ECFC", strokeWidth=3, opacity=45)
# luminous pool behind the figure
d.shape("ellipse", "Glow pool", x=300, y=330, width=400, height=440,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#7FC4F0", "opacity": 0.25},
            {"offset": 1, "color": "#7FC4F0", "opacity": 0}]}},
        stroke=NONE)
# faint zoom rings — the infinite magnification underfoot
d.shape("ellipse", "Zoom ring 1", x=300, y=660, width=400, height=140,
        fill=NONE, stroke="#8FB8DC", strokeWidth=2, opacity=35)
d.shape("ellipse", "Zoom ring 2", x=370, y=694, width=260, height=92,
        fill=NONE, stroke="#8FB8DC", strokeWidth=2, opacity=25)
d.shape("ellipse", "Zoom ring 3", x=435, y=722, width=130, height=46,
        fill=NONE, stroke="#8FB8DC", strokeWidth=2, opacity=18)

# --- title ----------------------------------------------------------------------
d.text("Zoom in forever", "Title 1", x=500, y=150, size=20,
       font="Virelai Sans", color=ICE, justify="center")
d.text("The curves will never get soft", "Title 2", x=500, y=180,
       size=20, font="Virelai Sans", color=SOFT, justify="center")

# --- the central perfect bezier, drawn like a specimen ----------------------------
CURVE = "M296,668 C390,486 610,620 704,408"
d.path(CURVE, "Bezier glow", fill=NONE, stroke="#7FC4F0", strokeWidth=18,
       opacity=14, cap="round")
d.path(CURVE, "Bezier halo", fill=NONE, stroke="#9ED8F0", strokeWidth=8,
       opacity=35, cap="round")
d.path(CURVE, "Bezier spine", fill=NONE, stroke="#EAF6FF", strokeWidth=3.5,
       cap="round")
# control handles + points (vector-editor furniture)
d.path("M296,668 L390,486 M704,408 L610,620", "Handle lines", fill=NONE,
       stroke="#9EC2DE", strokeWidth=2, opacity=60, dash=[6, 5])
for i, (cx, cy) in enumerate([(390, 486), (610, 620)]):
    d.shape("ellipse", f"Ctrl point {i+1}", x=cx - 5, y=cy - 5, width=10,
            height=10, fill=NONE, stroke="#9EC2DE", strokeWidth=2,
            opacity=80)
for i, (ax, ay) in enumerate([(296, 668), (704, 408)]):
    d.shape("rectangle", f"Anchor {i+1}", x=ax - 6, y=ay - 6, width=12,
            height=12, fill=ICE, stroke=INK, strokeWidth=2)

# --- Svgon: slender sentinel, visor, medallion, staff ------------------------------
d.shape("ellipse", "Svgon shadow", x=415, y=748, width=170, height=24,
        fill="#060A12", opacity=45, stroke=NONE)
# long angular coat
d.path("M458,492 L542,492 L560,748 L520,748 L510,640 L490,640 L480,748 "
       "L440,748 Z",
       "Svgon coat", fill=COAT, stroke=INK, strokeWidth=5, join="round")
d.path("M470,505 L455,720", "Coat sheen", fill=NONE, stroke="#EAF6FF",
       strokeWidth=7, opacity=22, cap="round")
# head: sleek helm, single smooth silhouette
d.path("M462,428 C462,382 538,382 538,428 C538,452 524,468 500,468 "
       "C476,468 462,452 462,428 Z",
       "Svgon helm", fill=COAT, stroke=INK, strokeWidth=5)
# anti-aliasing visor: one perfectly smooth luminous band
d.shape("rectangle", "Visor", x=466, y=424, width=68, height=14, radius=7,
        fill=VISOR, stroke=INK, strokeWidth=2.5)
d.path("M470,431 L530,431", "Visor gleam", fill=NONE, stroke="#FFFFFF",
       strokeWidth=2, opacity=80, cap="round")
# helmet crest ridge
d.path("M500,388 C508,398 508,412 500,420", "Helm ridge", fill=NONE,
       stroke="#EAF6FF", strokeWidth=4, opacity=50, cap="round")
# validation medallion on the chest
d.shape("ellipse", "Medallion", x=474, y=516, width=52, height=52,
        fill=GOLD, stroke=INK, strokeWidth=4)
d.path("M486,542 L496,552 L514,530", "Medallion check", fill=NONE,
       stroke="#1C2E4A", strokeWidth=5, cap="round", join="round")
d.shape("ellipse", "Medallion glint", x=482, y=522, width=16, height=10,
        fill="#FFFFFF", opacity=50, stroke=NONE)
# right arm reaching to the staff
d.path("M540,520 C576,528 596,552 600,588", "Arm R", fill=NONE,
       stroke="#4A6480", strokeWidth=20, cap="round")
d.shape("ellipse", "Hand R", x=588, y=580, width=26, height=24,
        fill="#B4CCE2", stroke=INK, strokeWidth=4)
# golden-ratio staff: shaft + golden-rectangle icon at the top
d.path("M606,356 L606,762", "Staff shaft", fill=NONE, stroke="#D8AC54",
       strokeWidth=6, cap="round")
d.path("M604,762 L608,762 L606,782 Z", "Staff tip", fill="#D8AC54",
       stroke=NONE)
d.shape("rectangle", "Golden rect", x=580, y=298, width=56, height=36,
        radius=3, fill="#16273C", stroke="#F6DC96", strokeWidth=3)
d.path("M614,298 L614,334", "Phi split", fill=NONE, stroke="#F6DC96",
       strokeWidth=2)
d.path("M614,334 A21,21 0 0 0 593,313", "Phi arc", fill=NONE,
       stroke="#F6DC96", strokeWidth=2)
d.path("M627,298 L627,334", "Phi split 2", fill=NONE, stroke="#F6DC96",
       strokeWidth=1.5, opacity=70)
d.shape("ellipse", "Staff glow", x=572, y=290, width=72, height=52,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F6DC96", "opacity": 0.3},
            {"offset": 1, "color": "#F6DC96", "opacity": 0}]}},
        stroke=NONE)

# --- three haiku stanzas circling the curve ----------------------------------------
def stanza(cx, y, lines, idx):
    for j, line in enumerate(lines):
        d.text(line, f"Stanza {idx} line {j+1}", x=cx, y=y + j * 19,
               size=12.5, font="Virelai Sans", color="#CFE8F8",
               justify="center")

stanza(245, 296, ["infinite zoom in", "every anchor holds its place",
                  "no pixel confesses"], 1)
stanza(755, 296, ["golden ratio staff", "measures the unmeasurable",
                  "one point six one eight"], 2)
stanza(500, 792, ["the medallion shines", "validated once, always",
                  "svgon walks the line"], 3)
# small stanza markers
for i, (mx, my) in enumerate([(160, 300), (840, 300), (405, 796)]):
    d.shape("ellipse", f"Stanza mark {i+1}", x=mx - 4, y=my - 4, width=8,
            height=8, fill=GOLD, stroke=NONE, opacity=85)

# --- name + role ------------------------------------------------------------------
d.text("SVGON THE LINE", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color=ICE, justify="center")
r = d.text("HAI-0046 SVGON THE LINE", "Role", x=500, y=968, size=20,
           font="Virelai Sans", color=SOFT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=170)

d.finish("hai-046-svgon-the-line-V1R00")
