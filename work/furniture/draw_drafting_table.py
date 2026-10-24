#!/usr/bin/env python3
"""Drafting table — field plate V1R00. A maple board tilted toward the
viewer on a pair of steel trestles: vellum sheet with ruled lines and a
title block, T-square resting across, pencil ledge on the near edge,
footrest between the A-frames. Slate-dark atelier plate. Near-side view,
1000x1000. House style: gradients + translucent shading, never flat.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Drafting Table — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#14181E"
DOWN = -90

def _stops(stops):
    return [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]

def lin(stops, angle=None):
    g = {"kind": "linear", "stops": _stops(stops)}
    if angle is not None:
        g["angle"] = angle
    return {"gradient": g}

def lin_pts(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [round(x0, 1), round(y0, 1)],
            "end": [round(x1, 1), round(y1, 1)], "stops": _stops(stops)}}

def rad(stops):
    return {"gradient": {"kind": "radial", "stops": _stops(stops)}}

def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(cx - rx, 1), y=round(cy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)

def line(name, x0, y0, x1, y1, w, color, **kw):
    return d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", name, fill=NONE, stroke=color,
                  strokeWidth=w, cap="round", **kw)

STEEL   = lin([(0, "#B4BEC8"), (0.45, "#78828E"), (1, "#38414C")], 0)
STEEL_F = lin([(0, "#8A94A0"), (1, "#2C343E")], 0)          # far/dimmer steel
STEEL_D = lin([(0, "#4E5864"), (1, "#1E242C")], DOWN)
MAPLE   = lin_pts(500, 548, 500, 388, (0, "#C49A5C"), (0.5, "#E0C088"), (1, "#F0D6A2"))
MAPLE_D = lin([(0, "#8A6434"), (1, "#4A3012")], DOWN)
PAPER   = lin_pts(500, 537, 500, 397, (0, "#DCD4C0"), (1, "#F0EBDC"))

FIT = []
def note(*pts):
    FIT.extend(pts)

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#0C1016"), (1, "#04060A")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#4E5E72", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#3C4A58"), (0.55, "#263240"), (1, "#0E151E")]),
        stroke="#070B10", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.72, "#000000", 0), (1, "#04080E", 0.5)]), stroke=NONE)
# cool north-light glow, upper left — the draughtsman's window
ell("North light", 380, 220, 320, 220,
    fill=rad([(0, "#D8E4EE", 0.2), (0.6, "#9AB2C4", 0.07), (1, "#9AB2C4", 0)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#AEBECA", strokeWidth=3, opacity=30)
for i, (x, y, w) in enumerate([(212, 235, 6), (768, 252, 7), (175, 605, 6), (818, 580, 7),
                               (432, 110, 6), (626, 113, 7), (162, 422, 6), (842, 405, 6)]):
    ell(f"Plate fleck {i+1}", x, y, w / 2, w / 2, fill="#78889A", opacity=30, stroke=NONE)

# --- floor + contact shadow --------------------------------------------------------
HZN = 760
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin([(0, "#1C2026", 0.6), (1, "#0A0C10", 0.92)], DOWN), stroke=NONE)
ell("Table shadow", 500, 760, 235, 28,
    fill=rad([(0, "#040608", 0.7), (0.6, "#040608", 0.34), (1, "#040608", 0)]), stroke=NONE)
note((268, 760), (732, 760))

# --- steel trestles ---------------------------------------------------------------
# each trestle splays in depth: front leg to the floor line, rear leg shorter/higher
def trestle(ax, tag):
    # rear leg first (farther, dimmer)
    d.path(f"M{ax - 7},592 L{ax + 5},592 L{ax + 40},722 L{ax + 28},722 Z",
           f"{tag} rear leg", fill=STEEL_F, stroke=INK, strokeWidth=2.5)
    ell(f"{tag} rear pad", ax + 34, 724, 14, 5, fill="#1E242C", stroke=INK, strokeWidth=1.5)
    # front leg
    d.path(f"M{ax - 7},592 L{ax + 5},592 L{ax - 20},745 L{ax - 34},745 Z",
           f"{tag} front leg", fill=STEEL, stroke=INK, strokeWidth=2.5)
    line(f"{tag} leg light", ax - 9, 610, ax - 28, 735, 3, "#DCE4EA", opacity=50)
    ell(f"{tag} front pad", ax - 27, 748, 15, 5, fill="#1E242C", stroke=INK, strokeWidth=1.5)
    # cross brace inside the A
    ly = 678
    x_back = ax + 5 + (ax + 40 - ax - 5) * (ly - 592) / (722 - 592) + 3
    x_front = ax - 7 + (ax - 34 - ax + 7) * (ly - 592) / (745 - 592) - 3
    line(f"{tag} brace", x_front, ly, x_back, ly - 4, 9, "#5C6672")

trestle(392, "Left trestle")
trestle(608, "Right trestle")

# rear stretcher linking the rear legs
d.path("M432,690 L640,688 L640,699 L432,701 Z", "Rear stretcher", fill=STEEL_F, stroke=INK, strokeWidth=2)
# footrest between the front legs
d.path("M362,694 L578,692 L578,704 L362,706 Z", "Footrest", fill=STEEL_D, stroke=INK, strokeWidth=2)
line("Footrest light", 366, 695, 574, 693, 3, "#C8D2DC", opacity=55)

# board bearer rail under the near edge
d.path("M300,556 L700,556 L700,571 L300,571 Z", "Bearer rail", fill=MAPLE_D, stroke=INK, strokeWidth=2.5)
# pivot discs where the board rides the trestle apexes
for ax, tag in [(392, "L"), (608, "R")]:
    ell(f"Pivot {tag}", ax, 574, 12, 12, fill=STEEL, stroke=INK, strokeWidth=2.5)
    ell(f"Pivot {tag} bolt", ax, 574, 3.5, 3.5, fill="#1A2028", stroke=NONE)

# --- the tilted board ---------------------------------------------------------------
BL, BR, TR, TL = (280, 548), (720, 548), (680, 376), (320, 376)
# left edge thickness
d.path("M280,548 L320,376 L313,370 L273,542 Z", "Board left edge", fill=MAPLE_D,
       stroke=INK, strokeWidth=2)
# board face
d.path(f"M{BL[0]},{BL[1]} L{BR[0]},{BR[1]} L{TR[0]},{TR[1]} L{TL[0]},{TL[1]} Z",
       "Board face", fill=MAPLE, stroke=INK, strokeWidth=3)
note(BL, BR, TR, TL)
# grain lines running with the tilt
for i, t in enumerate([0.2, 0.4, 0.6, 0.8]):
    x0 = BL[0] + (BR[0] - BL[0]) * t
    x1 = TL[0] + (TR[0] - TL[0]) * t
    line(f"Board grain {i+1}", x0, 542, x1, 394, 2, "#8A6434", opacity=18)

# vellum sheet, inset toward the board's centroid
BC = (500, 462)
def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
PBL = lerp(BL, BC, .13); PBR = lerp(BR, BC, .13)
PTR = lerp(TR, BC, .13); PTL = lerp(TL, BC, .13)
d.path(f"M{PBL[0]},{PBL[1]} L{PBR[0]},{PBR[1]} L{PTR[0]},{PTR[1]} L{PTL[0]},{PTL[1]} Z",
       "Vellum", fill=PAPER, stroke="#7A7260", strokeWidth=2)
# sheet border, inset each corner toward the sheet centroid
cc = (500, 467)
q = [(p[0] + (cc[0] - p[0]) * .06, p[1] + (cc[1] - p[1]) * .06) for p in [PBL, PBR, PTR, PTL]]
d.path(f"M{q[0][0]:.0f},{q[0][1]:.0f} L{q[1][0]:.0f},{q[1][1]:.0f} L{q[2][0]:.0f},{q[2][1]:.0f} "
       f"L{q[3][0]:.0f},{q[3][1]:.0f} Z", "Sheet border", fill=NONE, stroke="#8A8270",
       strokeWidth=2, opacity=75)
# ruled horizontals — the lines that had to be perfect
for i, t in enumerate([0.28, 0.42, 0.56, 0.70]):
    xa = PBL[0] + (PTL[0] - PBL[0]) * t + 14
    xb = PBR[0] + (PTR[0] - PBR[0]) * t - 14
    y = PBL[1] + (PTL[1] - PBL[1]) * t
    line(f"Rule {i+1}", xa, y, xb, y, 2.5, "#5A6E84", opacity=65)
# title block, lower right of the sheet
d.path("M560,498 L642,498 L639,524 L557,524 Z", "Title block", fill="#E4DECA",
       stroke="#8A8270", strokeWidth=2)
line("Title rule 1", 564, 507, 638, 507, 2, "#8A8270", opacity=80)
line("Title rule 2", 564, 516, 636, 516, 2, "#8A8270", opacity=80)

# pencil ledge along the near edge
d.path("M283,540 L717,540 L720,549 L280,549 Z", "Pencil ledge", fill=MAPLE_D,
       stroke=INK, strokeWidth=2)
line("Ledge light", 290, 541.5, 710, 541.5, 2.5, "#E8C88E", opacity=60)

# T-square: steel blade across the board, maple head over the left edge
d.path("M322,494 L694,458 L695,471 L323,507 Z", "T-square blade",
       fill=lin([(0, "#DCE2E8"), (0.5, "#A8B4C0"), (1, "#5E6A78")], DOWN),
       stroke="#20262E", strokeWidth=2)
line("Blade light", 330, 497, 688, 462, 2.5, "#F2F6FA", opacity=70)
d.path("M304,478 L346,473 L351,510 L309,516 Z", "T-square head", fill=MAPLE_D,
       stroke=INK, strokeWidth=2.5)
ell("T-square bolt", 328, 494, 4, 4, fill="#20262E", stroke="#0C1014", strokeWidth=1)
note((304, 478), (694, 458))

# --- sanity: the whole piece inside the disc ------------------------------------------
worst = min(PR - math.hypot(x - PCX, y - PCY) for x, y in FIT)
print("min clearance to rim: %.1f" % worst)
assert worst > 24, worst

# --- rim + captions ---------------------------------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#060A0E", strokeWidth=6)
d.shape("ellipse", "Plate inner edge", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B4C4D0", strokeWidth=3, opacity=26)

r1 = d.text("DRAFTING TABLE", "Name", x=500, y=936, size=58, font="Virelai Sans",
            color="#E8ECEA", justify="center")
LINE2, SZ2, TRK = "MAPLE · STEEL", 22, 280
r2 = d.text(LINE2, "Second line", x=500, y=972, size=SZ2, font="Virelai Sans",
            color="#A2B4C0", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r2["id"], tracking=TRK)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit

layers = d.call("inspect_document", {}, "inspect")["layers"]
for label, rr in [("name", r1), ("second line", r2)]:
    b = find(layers, rr["id"])["bounds"]
    print(label, "bounds", {k: round(v) for k, v in b.items()})
    assert b["width"] <= 780 and b["x"] >= 96 and b["y"] + b["height"] <= 990, b

d.finish("drafting-table-V1R00")
