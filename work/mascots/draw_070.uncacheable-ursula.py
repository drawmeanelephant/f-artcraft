#!/usr/bin/env python3
"""Uncacheable Ursula — mascot portrait V1R00.
Hooded oracle wandering between CDN edge nodes, counting clicks like
rosary beads while two header plates argue FRESH vs STALE over her head.
1000x1000. Gradients + translucent shading, never flat."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Uncacheable Ursula — Mascot Portrait", 1000, 1000)

INK = "#1E1814"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1A20"}, {"offset": 1, "color": "#060C10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E5A5E"}, {"offset": 0.7, "color": "#26393E"},
    {"offset": 1, "color": "#141E22"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A3436"}, {"offset": 1, "color": "#10181A"}]}}
CLOAK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E5E78"}, {"offset": 0.65, "color": "#28425A"},
    {"offset": 1, "color": "#16283A"}]}}
HOOD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A6E88"}, {"offset": 0.7, "color": "#2E4A60"},
    {"offset": 1, "color": "#182E40"}]}}
NODE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#46545C"}, {"offset": 1, "color": "#242E34"}]}}
BEAD = "#8FD8C8"
GOLD = "#D8C078"
PAPER_FRESH = "#BFE8CC"
PAPER_STALE = "#E8C890"
MIST = "#9FC4BE"

def rot_pt(cx, cy, x, y, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * s,
            cy + (x - cx) * s + (y - cy) * c)

# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E7A80", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8D4CE", strokeWidth=3, opacity=35)
# plate patina
d.shape("ellipse", "Patina 1", x=200, y=200, width=230, height=140,
        fill="#557A78", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=580, y=620, width=250, height=140,
        fill="#557A78", opacity=18, stroke=NONE)

# --- the edge network: CDN nodes on a wandering dashed route --------------------
# node tiles placed well inside the plate arc (r<=330 from 500,460)
NODES = [(300, 200), (690, 185), (795, 415), (715, 648), (285, 640), (205, 415)]
for i in range(len(NODES)):
    x1, y1 = NODES[i]; x2, y2 = NODES[(i + 1) % len(NODES)]
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Edge hop {i+1}", fill=NONE,
           stroke="#6E8E8A", strokeWidth=2.5, dash=[7, 7], opacity=55)
for i, (x, y) in enumerate(NODES):
    d.shape("rectangle", f"CDN node {i+1}", x=x - 26, y=y - 18,
            width=52, height=36, fill=NODE_GRAD, stroke="#7E969C",
            strokeWidth=3, radius=5, opacity=95)
    for j in range(3):
        d.shape("ellipse", f"Node {i+1} light {j+1}", x=x - 16 + j * 12,
                y=y - 5, width=7, height=7,
                fill=BEAD if (i + j) % 3 else "#E8A86A",
                opacity=85, stroke=NONE)
# ttl tick-marks drifting off the route
for i, (x, y, s) in enumerate([(430, 250, 4), (560, 300, 3), (350, 350, 4),
                               (640, 480, 3), (480, 590, 4), (620, 620, 3)]):
    d.shape("ellipse", f"Drift tick {i+1}", x=x, y=y, width=s, height=s,
            fill=MIST, opacity=45, stroke=NONE)

# --- conflicting headers, arguing over her head ----------------------------------
d.path(rot_rect_path(330, 330, 168, 52, -9), "Header card FRESH",
       fill=PAPER_FRESH, stroke=INK, strokeWidth=4, join="round", opacity=95)
t = d.text("ETag: FRESH", "Fresh label", x=330, y=337, size=19,
           font="Source Sans 3", color="#2E5640", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "fresh tilt", ids=[t["id"]], angle=-9,
          origin=[330, 330])
d.path(rot_rect_path(672, 316, 168, 52, 8), "Header card STALE",
       fill=PAPER_STALE, stroke=INK, strokeWidth=4, join="round", opacity=95)
t = d.text("ETag: STALE", "Stale label", x=672, y=323, size=19,
           font="Source Sans 3", color="#7A4A20", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "stale tilt", ids=[t["id"]], angle=8,
          origin=[672, 316])
# opposed arrows between them — the conflict
d.path("M428,318 L470,318 M470,318 L458,308 M470,318 L458,328",
       "Arrow out", fill=NONE, stroke="#C8A86A", strokeWidth=4,
       cap="round", join="round", opacity=80)
d.path("M588,306 L548,306 M548,306 L560,296 M548,306 L560,316",
       "Arrow in", fill=NONE, stroke="#C8A86A", strokeWidth=4,
       cap="round", join="round", opacity=80)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#080E10",
       strokeWidth=4, opacity=70)

# --- Ursula: the oracle between nodes -------------------------------------------
d.shape("ellipse", "Ursula shadow", x=390, y=688, width=240, height=24,
        fill="#04080A", opacity=55, stroke=NONE)
# cloak: hooded robe flaring to the hem
d.path("M500,398 C564,398 604,448 616,520 C626,584 646,652 668,700 "
       "C596,722 404,722 332,700 C354,652 374,584 384,520 "
       "C396,448 436,398 500,398 Z",
       "Cloak", fill=CLOAK_GRAD, stroke=INK, strokeWidth=6, join="round")
# cloak fold lines + hem shade
d.path("M430,540 C436,600 424,660 408,694", "Fold L", fill=NONE,
       stroke="#0E1E2C", strokeWidth=4, cap="round", opacity=55)
d.path("M576,540 C570,600 582,660 598,694", "Fold R", fill=NONE,
       stroke="#0E1E2C", strokeWidth=4, cap="round", opacity=55)
d.path("M340,686 C420,706 580,706 660,686 C580,698 420,698 340,686 Z",
       "Hem shade", fill="#0C1822", opacity=50, stroke=NONE)
# hood dome over a shadowed face
d.path("M500,368 C556,368 592,410 592,462 C592,498 566,522 500,522 "
       "C434,522 408,498 408,462 C408,410 444,368 500,368 Z",
       "Hood", fill=HOOD_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Face shadow", x=438, y=418, width=124, height=88,
        fill="#101C26", stroke=NONE)
# the pale eyes that have seen every expiry
d.shape("ellipse", "Eye L", x=462, y=448, width=20, height=24,
        fill=BEAD, opacity=95, stroke=NONE)
d.shape("ellipse", "Eye R", x=518, y=448, width=20, height=24,
        fill=BEAD, opacity=95, stroke=NONE)
d.shape("ellipse", "Pupil L", x=468, y=456, width=8, height=10,
        fill="#0C2020", stroke=NONE)
d.shape("ellipse", "Pupil R", x=524, y=456, width=8, height=10,
        fill="#0C2020", stroke=NONE)
d.path("M486,492 C494,498 506,498 514,492", "Oracle mouth", fill=NONE,
       stroke="#5E7E78", strokeWidth=3.5, cap="round", opacity=80)
# hood rim highlight
d.path("M430,420 C450,392 550,392 572,420", "Hood rim light", fill=NONE,
       stroke="#7EA8B8", strokeWidth=4, cap="round", opacity=50)

# --- raised right arm blessing a header ------------------------------------------
d.path("M560,540 C610,510 640,470 652,424", "Arm R ink", fill=NONE,
       stroke=INK, strokeWidth=34, cap="round")
d.path("M560,540 C610,510 640,470 652,424", "Arm R", fill=NONE,
       stroke="#2E4A60", strokeWidth=24, cap="round")
d.shape("ellipse", "Hand R", x=636, y=398, width=36, height=30,
        fill="#C9B79A", stroke=INK, strokeWidth=3.5)
# two raised fingers: freshness declared, twice, differently
d.path("M646,402 L640,382 M658,400 L658,378", "Fingers", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")

# --- rosary of clicks, counted in the left hand -----------------------------------
d.path("M442,560 C400,580 376,610 372,646", "Arm L ink", fill=NONE,
       stroke=INK, strokeWidth=30, cap="round")
d.path("M442,560 C400,580 376,610 372,646", "Arm L", fill=NONE,
       stroke="#2E4A60", strokeWidth=20, cap="round")
d.shape("ellipse", "Hand L", x=352, y=632, width=34, height=28,
        fill="#C9B79A", stroke=INK, strokeWidth=3.5)
# bead loop hanging from the hand: string ellipse + beads along it
d.path("M366,650 C330,700 340,760 392,778 C452,796 520,772 522,722 "
       "C524,680 480,660 430,664", "Rosary string", fill=NONE,
       stroke="#B8A888", strokeWidth=3, opacity=75)
def ell_pt(cx, cy, rx, ry, deg):
    a = math.radians(deg)
    return (cx + rx * math.cos(a), cy + ry * math.sin(a))
for i, adeg in enumerate([195, 225, 255, 285, 315, 345, 15, 45, 75, 105, 135]):
    bx, by = ell_pt(436, 716, 92, 58, adeg)
    glow = (i % 4 == 0)
    d.shape("ellipse", f"Bead {i+1}", x=bx - 7, y=by - 7, width=14,
            height=14, fill=BEAD if glow else "#D8C8A0",
            stroke=INK, strokeWidth=2, opacity=95)
    if glow:
        d.shape("ellipse", f"Bead {i+1} glow", x=bx - 3, y=by - 4,
                width=5, height=5, fill="#FFFFFF", opacity=80, stroke=NONE)
# pendant: the little refresh charm at the bottom of the loop
d.shape("ellipse", "Charm ring", x=428, y=766, width=26, height=26,
        fill=NONE, stroke=GOLD, strokeWidth=5)
d.path("M452,772 L462,772 M462,772 L456,766 M462,772 L456,778",
       "Charm arrow", fill=NONE, stroke=GOLD, strokeWidth=4,
       cap="round", join="round")

# --- captions ----------------------------------------------------------------------
d.text("UNCACHEABLE URSULA", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#DCE8E4", justify="center")
r = d.text("ORACLE OF CONTESTED FRESHNESS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9AB8B2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("070.uncacheable-ursula-V1R00")
