#!/usr/bin/env python3
"""Svgon The Line — mascot portrait V1R00. Vector Supremacist:
a robed precisionist holding a golden-ratio staff, wearing a validation
medallion and an anti-aliasing visor. Crisp at any size. Ego-fueled.
Regal indigo plate on a plum-night backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Svgon The Line — Mascot Plate", 1000, 1000)

INK = "#221A14"   # warm dark ink, never black
PHI = (1 + math.sqrt(5)) / 2
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#150F1C"}, {"offset": 1, "color": "#08060C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E5678"}, {"offset": 0.62, "color": "#3C3654"},
    {"offset": 1, "color": "#1A1626"}]}}
ROBE_GRAD = {"gradient": {"kind": "linear", "start": [0, 400], "end": [0, 780], "stops": [
    {"offset": 0, "color": "#4A4380"}, {"offset": 0.55, "color": "#332C5E"},
    {"offset": 1, "color": "#1C1838"}]}}
SKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E6CCA8"}, {"offset": 0.75, "color": "#C9A888"},
    {"offset": 1, "color": "#A8846A"}]}}
VISOR_GRAD = {"gradient": {"kind": "linear", "start": [0, 345], "end": [0, 390], "stops": [
    {"offset": 0, "color": "#2A3E5E"}, {"offset": 0.5, "color": "#16203A"},
    {"offset": 1, "color": "#0C1224"}]}}
GOLD = "#D4AC52"
GOLD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0D488"}, {"offset": 1, "color": "#A8842E"}]}}
MEDAL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4DC96"}, {"offset": 0.7, "color": "#D4AC52"},
    {"offset": 1, "color": "#9A782A"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def log_spiral(cx, cy, r0, turns, label, steps=64, start_deg=0):
    """Log spiral r = r0 * phi^(-2*theta/pi): the golden spiral."""
    pts = []
    for i in range(steps + 1):
        t = math.radians(start_deg) + turns * 2 * math.pi * i / steps
        r = r0 * PHI ** (-2 * (t - math.radians(start_deg)) / math.pi)
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return path

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#7A70A0", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#100C18", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8C0E0", strokeWidth=3, opacity=26)
# patina + flecks
d.shape("ellipse", "Patina 1", x=195, y=330, width=235, height=150,
        fill="#4E4668", opacity=24, stroke=NONE)
d.shape("ellipse", "Patina 2", x=615, y=570, width=235, height=140,
        fill="#262040", opacity=32, stroke=NONE)
for i, (x, y, w) in enumerate([(218,348,5),(792,342,6),(182,548,5),(850,568,5),
                               (262,762,5),(732,768,6),(160,452,5),(852,632,5),
                               (432,128,5),(598,140,6),(340,162,4),(702,202,5),
                               (252,652,4),(658,722,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#DCD4F0", opacity=30, stroke=NONE)
# ghost arcs on the dark backdrop
d.path("M930,158 A105,105 0 0 0 848,64", "Ghost arc TR",
       fill=NONE, stroke="#6A5E90", strokeWidth=14, opacity=10, cap="round")
d.path("M78,778 A118,118 0 0 0 186,880", "Ghost arc BL",
       fill=NONE, stroke="#6A5E90", strokeWidth=10, opacity=8, cap="round")

# --- golden-ratio ghost diagram, upper left of the plate --------------------------
gx, gy, gs = 208, 200, 150   # origin + unit
# nested golden rects: W x W/phi, recursing three deep
rw, rh = gs, gs / PHI
for j in range(3):
    d.shape("rectangle", f"Golden rect {j+1}", x=gx, y=gy, width=rw,
            height=rh, fill=NONE, stroke=GOLD, strokeWidth=2.5, opacity=24)
    gx += rw - rh        # carve off the square, next rect beside it
    rw, rh = rh, rw - rh if j % 2 == 0 else rh / PHI
d.path(log_spiral(285, 248, 48, 1.3, "ghost"), "Ghost spiral",
       fill=NONE, stroke=GOLD, strokeWidth=3, opacity=30, cap="round")

# --- pen-tool motif: a perfect bezier with anchor handles, floating right ---------
d.path("M700,640 C730,560 800,540 846,586", "Specimen curve",
       fill=NONE, stroke="#B8AEE0", strokeWidth=4, opacity=55, cap="round")
for j, (x, y) in enumerate([(700, 640), (846, 586)]):
    d.shape("rectangle", f"Anchor {j+1}", x=x - 7, y=y - 7, width=14,
            height=14, fill="#E8E2F4", stroke="#3A3256", strokeWidth=2)
# tangent handle off the first anchor
d.path("M700,640 L756,596", "Handle line",
       fill=NONE, stroke="#8A80B8", strokeWidth=2, opacity=60)
d.shape("ellipse", "Handle knob", x=750, y=590, width=12, height=12,
        fill="#B8AEE0", stroke="#3A3256", strokeWidth=2)

# --- the golden-ratio staff ------------------------------------------------------------
sx = 668
d.path(f"M{sx},252 L{sx},742", "Staff rod",
       fill=NONE, stroke="#8A6E34", strokeWidth=8, cap="round")
d.path(f"M{sx - 1},268 L{sx - 1},720", "Staff rod sheen",
       fill=NONE, stroke="#C8A85A", strokeWidth=2.5, opacity=60, cap="round")
# staff cap: a disc bearing the spiral
d.shape("ellipse", "Staff cap glow", x=sx - 52, y=158, width=104, height=104,
        fill=GOLD, opacity=14, stroke=NONE)
d.shape("ellipse", "Staff cap", x=sx - 38, y=172, width=76, height=76,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#3A3252"}, {"offset": 1, "color": "#1A1428"}]}},
        stroke=GOLD, strokeWidth=5)
d.path(log_spiral(sx + 14, 224, 30, 1.35, "cap", start_deg=90),
       "Cap spiral", fill=NONE, stroke=GOLD, strokeWidth=3.5, cap="round")

# --- the supremacist --------------------------------------------------------------------
# sleeves: left arm folded in, right arm out to the staff
d.path("M410,500 C388,556 382,624 392,688 C402,702 420,702 430,690 "
       "C424,626 432,562 448,514 Z",
       "Sleeve L", fill=ROBE_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand L", x=388, y=684, width=30, height=26,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=3)
# robe: crisp bell silhouette
d.path("M500,428 C556,428 596,466 612,534 C626,594 634,676 628,746 "
       "C578,772 422,772 372,746 C366,676 374,594 388,534 "
       "C404,466 444,428 500,428 Z",
       "Robe", fill=ROBE_GRAD, stroke=INK, strokeWidth=5)
# robe shading: right side + hem
d.path("M566,470 C596,528 614,636 610,738 C588,750 564,758 540,762 "
       "C566,692 574,560 566,470 Z",
       "Robe shade", fill="#100C28", opacity=45, stroke=NONE)
d.path("M374,714 C430,734 570,734 626,714 L628,746 C578,772 422,772 372,746 Z",
       "Hem shade", fill="#0E0A24", opacity=40, stroke=NONE)
# geometric gold trim: center line + angular chevrons
d.path("M500,462 L500,748", "Robe trim",
       fill=NONE, stroke=GOLD, strokeWidth=5, opacity=85)
for j, yy in enumerate((530, 600, 670)):
    d.path(f"M{466 - j * 6},{yy} L500,{yy + 18} L{534 + j * 6},{yy}",
           f"Chevron {j+1}", fill=NONE, stroke=GOLD, strokeWidth=3,
           opacity=55)
# high collar
d.path("M462,428 C466,398 482,384 500,384 C518,384 534,398 538,428 "
       "C526,416 512,410 500,410 C488,410 474,416 462,428 Z",
       "Collar", fill="#2A2450", stroke=INK, strokeWidth=3.5)
# right arm extended, gripping the staff
d.path("M596,470 C628,478 654,496 668,522 C672,536 664,548 650,544 "
       "C636,522 616,508 594,500 Z",
       "Sleeve R", fill=ROBE_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=650, y=512, width=34, height=30,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=3)
d.path("M668,506 L668,540", "Grip marks",
       fill=NONE, stroke=INK, strokeWidth=2.5, cap="round", opacity=70)

# --- the validation medallion -----------------------------------------------------------
mx, my = 500, 600
d.path(f"M{mx - 16},{my + 30} L{mx - 26},{my + 58} L{mx - 8},{my + 44} Z",
       "Ribbon L", fill="#8A2E2E", stroke=INK, strokeWidth=2)
d.path(f"M{mx + 16},{my + 30} L{mx + 26},{my + 58} L{mx + 8},{my + 44} Z",
       "Ribbon R", fill="#8A2E2E", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Medal glow", x=mx - 44, y=my - 44, width=88, height=88,
        fill=GOLD, opacity=15, stroke=NONE)
d.shape("ellipse", "Medal", x=mx - 33, y=my - 33, width=66, height=66,
        fill=MEDAL_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Medal ring", x=mx - 24, y=my - 24, width=48, height=48,
        fill=NONE, stroke="#8A6820", strokeWidth=2.5, opacity=80)
d.path(f"M{mx - 13},{my + 1} L{mx - 3},{my + 11} L{mx + 15},{my - 11}",
       "Valid check", fill=NONE, stroke="#4A3A10", strokeWidth=6,
       cap="round")

# --- the head + the anti-aliasing visor ---------------------------------------------------
d.path("M500,282 C546,282 578,314 578,362 C578,410 544,442 500,442 "
       "C456,442 422,410 422,362 C422,314 454,282 500,282 Z",
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=4.5)
# serene, superior mouth + chin shade
d.path("M472,412 C486,421 514,421 528,410", "Smile",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
d.path("M456,414 C476,432 524,432 544,414 C536,436 520,442 500,442 "
       "C480,442 464,436 456,414 Z",
       "Chin shade", fill="#9A7A5C", opacity=30, stroke=NONE)
# nose
d.path("M498,392 C496,400 494,406 491,412 C497,416 505,416 510,412",
       "Nose", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
# the visor: one smooth band, infinitely resolvable
d.path("M424,344 C424,330 440,322 500,322 C560,322 576,330 576,344 "
       "L576,366 C576,380 560,388 500,388 C440,388 424,380 424,366 Z",
       "Visor", fill=VISOR_GRAD, stroke=INK, strokeWidth=4)
# sheen sweep + perfectly crisp edge light
d.path("M436,346 C460,336 540,336 564,346", "Visor sheen",
       fill=NONE, stroke="#9FC4E8", strokeWidth=3.5, opacity=65,
       cap="round")
d.path("M440,372 C470,380 530,380 560,372", "Visor edge light",
       fill=NONE, stroke="#5E7AA8", strokeWidth=2, opacity=50,
       cap="round")
# temple studs where the visor seats
d.shape("ellipse", "Visor stud L", x=418, y=348, width=14, height=16,
        fill=GOLD_GRAD, stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Visor stud R", x=568, y=348, width=14, height=16,
        fill=GOLD_GRAD, stroke=INK, strokeWidth=2.5)

# --- name + role ----------------------------------------------------------------------
d.text("SVGON THE LINE", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#E2DCF4", justify="center")
r = d.text("VECTOR SUPREMACIST", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#AEA0D4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("046.svgon-the-line-V1R00")
