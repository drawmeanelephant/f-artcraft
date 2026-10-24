#!/usr/bin/env python3
"""Secretary desk — field plate V1R00. Bookcase-on-bureau: glazed two-door
cabinet over a fall-front folded down to show the pigeonhole gallery and
a tooled-leather writing surface; three graduated drawers, bracket feet.
Walnut on an aubergine library-dark disc. Front view, 1000x1000.
House style: gradients + translucent shading, never flat.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Secretary Desk — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E0E06"
DOWN = -90

def _stops(stops):
    return [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]

def lin(stops, angle=None):
    g = {"kind": "linear", "stops": _stops(stops)}
    if angle is not None:
        g["angle"] = angle
    return {"gradient": g}

def rad(stops):
    return {"gradient": {"kind": "radial", "stops": _stops(stops)}}

def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(cx - rx, 1), y=round(cy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)

def line(name, x0, y0, x1, y1, w, color, **kw):
    return d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", name, fill=NONE, stroke=color,
                  strokeWidth=w, cap="round", **kw)

def rect(name, x0, y0, x1, y1, **kw):
    return d.shape("rectangle", name, x=round(x0, 1), y=round(y0, 1),
                   width=round(x1 - x0, 1), height=round(y1 - y0, 1), **kw)

# walnut: reddish-brown case wood, lit upper-left
WALNUT     = lin([(0, "#8A5636"), (0.45, "#5E3820"), (1, "#2E1808")], DOWN)
WALNUT_X   = {"gradient": {"kind": "linear", "start": [362, 0], "end": [638, 0], "stops": [
    {"offset": 0, "color": "#9A6238"}, {"offset": 0.4, "color": "#6E4224"},
    {"offset": 1, "color": "#2A1408"}]}}
WALNUT_DK  = lin([(0, "#4A2C16"), (1, "#221004")], DOWN)
BRASS      = rad([(0, "#F0CC7E"), (0.6, "#C89A4E"), (1, "#7A5420")])
INTERIOR   = rad([(0, "#E8B96A"), (0.55, "#8A5426"), (1, "#2A1406")])
GLASS      = lin([(0, "#9AA8BC", 0.30), (0.5, "#6E7C92", 0.14), (1, "#3E4A5E", 0.22)], DOWN)
LEATHER    = lin([(0, "#3E5C40"), (0.6, "#2A4230"), (1, "#16241A")], DOWN)

FIT = []
def note(*pts):
    FIT.extend(pts)

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#100C12"), (1, "#050406")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#6E5A72", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#4E3A50"), (0.55, "#33243A"), (1, "#140E1A")]),
        stroke="#0A060E", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.72, "#000000", 0), (1, "#080410", 0.5)]), stroke=NONE)
ell("Lamplight", 390, 220, 300, 210,
    fill=rad([(0, "#F0CE8E", 0.2), (0.6, "#C89A58", 0.07), (1, "#C89A58", 0)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8B4CE", strokeWidth=3, opacity=30)
for i, (x, y, w) in enumerate([(215, 240, 6), (765, 255, 7), (178, 610, 6), (815, 585, 7),
                               (435, 112, 6), (620, 115, 7), (165, 425, 6), (840, 410, 6)]):
    ell(f"Plate fleck {i+1}", x, y, w / 2, w / 2, fill="#9A82A2", opacity=30, stroke=NONE)

# --- floor + contact shadow --------------------------------------------------------
HZN = 782
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin([(0, "#221A14", 0.6), (1, "#0C0806", 0.92)], DOWN), stroke=NONE)
ell("Desk shadow", 500, 784, 215, 26,
    fill=rad([(0, "#040404", 0.7), (0.6, "#040404", 0.34), (1, "#040404", 0)]), stroke=NONE)
note((290, 782), (710, 782))

X0, X1 = 362, 638        # case sides

# --- cornice -------------------------------------------------------------------------
rect("Cornice crown", 352, 182, 648, 197, fill=lin([(0, "#A06838"), (1, "#4A2A12")], DOWN),
     stroke=INK, strokeWidth=2.5)
rect("Cornice cove", 356, 197, 644, 209, fill=WALNUT_DK, stroke=INK, strokeWidth=2)
line("Cove light", 360, 199, 640, 199, 3, "#C89458", opacity=55)
rect("Head rail", 360, 209, 640, 219, fill=WALNUT, stroke=INK, strokeWidth=2)
note((352, 182), (648, 182))

# --- upper case + glazed doors -------------------------------------------------------
rect("Upper case", 368, 219, 632, 432, fill=WALNUT_X, stroke=INK, strokeWidth=3)

BOOKS = ["#5A3A48", "#3A4A5C", "#4A5A3A", "#6A4A26", "#4E3A56", "#5C4A30", "#3C5450", "#66402E"]
def door(x0, x1, tag):
    rect(f"{tag} door frame", x0, 226, x1, 424, fill=WALNUT, stroke=INK, strokeWidth=2.5)
    # dark interior behind the glazing
    rect(f"{tag} interior", x0 + 12, 238, x1 - 12, 412,
         fill=lin([(0, "#24160C"), (1, "#0E0703")], DOWN), stroke=NONE)
    # book spines on two shelves
    k = 0
    for si, (sy0, sy1) in enumerate([(262, 318), (340, 396)]):
        bx = x0 + 16
        while bx < x1 - 24:
            bw = 11 + (k * 7 + si * 3) % 9
            bh = (sy1 - sy0 - 4) - (k * 5 % 10)
            rect(f"{tag} book {si+1}-{k+1}", bx, sy1 - bh, min(bx + bw, x1 - 14), sy1,
                 fill=BOOKS[(k + si * 3) % len(BOOKS)], opacity=62, stroke="#160C04", strokeWidth=1)
            bx += bw + 2 + (k % 3)
            k += 1
        line(f"{tag} shelf {si+1}", x0 + 13, sy1 + 2, x1 - 13, sy1 + 2, 4, "#5E3820", opacity=90)
    # glazing sheet + diagonal sheen
    rect(f"{tag} glazing", x0 + 12, 238, x1 - 12, 412, fill=GLASS, stroke=NONE)
    d.path(f"M{x0 + 30},{238} L{x0 + 60},{238} L{x0 + 20},{412} L{x0 + 4},{412} Z",
           f"{tag} glass sheen", fill="#DCE8F0", opacity=10, stroke=NONE)
    # mullions: mid stile + two cross rails, >=8pt
    xm = (x0 + x1) / 2
    rect(f"{tag} mullion V", xm - 4.5, 238, xm + 4.5, 412, fill=WALNUT_DK, stroke=INK, strokeWidth=1.5)
    for yy in (304, 372):
        rect(f"{tag} mullion {yy}", x0 + 12, yy - 4, x1 - 12, yy + 4, fill=WALNUT_DK, stroke=INK, strokeWidth=1.5)
    # bevel light on the frame's top-left
    line(f"{tag} bevel top", x0 + 3, 230, x1 - 3, 230, 3, "#C89458", opacity=50)
    line(f"{tag} bevel left", x0 + 3, 230, x0 + 3, 420, 3, "#C89458", opacity=35)
    # brass pull at the meeting stile
    px = x1 - 10 if x0 < PCX else x0 + 10
    ell(f"{tag} pull", px, 330, 4.5, 4.5, fill=BRASS, stroke="#3A2408", strokeWidth=1.2)

door(374, 498, "Left")
door(502, 626, "Right")
# meeting stile shadow between the doors
rect("Meeting stile", 498, 226, 502, 424, fill="#1E0E06", stroke=NONE, opacity=70)

# --- waist: open fall cavity with pigeonhole gallery ---------------------------------
rect("Waist case", X0, 432, X1, 608, fill=WALNUT_X, stroke=INK, strokeWidth=3)
# cavity recess
rect("Cavity", 378, 444, 622, 548, fill=lin([(0, "#120802"), (1, "#050201")], DOWN),
     stroke=INK, strokeWidth=2.5)
# warm interior back panel
rect("Interior back", 384, 450, 616, 542, fill=INTERIOR, stroke=NONE)

# pigeonhole banks: 3 cells x 2 rows each side + centre cupboard + tiny drawer strip
GRID_INK = "#3A1E0C"
def bank(x0, x1, tag):
    for r, (ry0, ry1) in enumerate([(456, 482), (486, 512)]):
        for c in range(3):
            cx0 = x0 + c * (x1 - x0) / 3
            cx1 = x0 + (c + 1) * (x1 - x0) / 3
            rect(f"{tag} hole {r+1}-{c+1}", cx0 + 1.5, ry0, cx1 - 1.5, ry1,
                 fill=rad([(0, "#5E3818"), (1, "#2A1404")]), stroke=GRID_INK, strokeWidth=3)
bank(390, 464, "Left bank")
bank(536, 610, "Right bank")
# centre cupboard with a tiny knob
rect("Cupboard", 468, 456, 532, 512, fill=WALNUT, stroke=GRID_INK, strokeWidth=3)
ell("Cupboard knob", 500, 484, 3.5, 3.5, fill=BRASS, stroke="#3A2408", strokeWidth=1)
# tiny drawer strip along the bottom of the gallery
for c in range(4):
    dx0 = 390 + c * 55
    rect(f"Tiny drawer {c+1}", dx0 + 1.5, 516, dx0 + 53.5, 536,
         fill=lin([(0, "#8A5636"), (1, "#4A2810")], DOWN), stroke=GRID_INK, strokeWidth=3)
    ell(f"Tiny pull {c+1}", dx0 + 27.5, 526, 3, 3, fill=BRASS, stroke="#3A2408", strokeWidth=1)

# the fall flap, folded down toward the viewer
d.path("M372,548 L628,548 L650,598 L350,598 Z", "Fall flap", fill=WALNUT, stroke=INK, strokeWidth=3)
d.path("M388,556 L612,556 L626,586 L374,586 Z", "Leather inset", fill=LEATHER,
       stroke="#0E180E", strokeWidth=2)
# gilt border inside the leather
d.path("M396,560 L604,560 L616,582 L384,582 Z", "Gilt border", fill=NONE,
       stroke="#C89A4E", strokeWidth=2, opacity=70)
ell("Leather sheen", 470, 566, 90, 10, fill=rad([(0, "#9AB4A0", 0.3), (1, "#9AB4A0", 0)]), stroke=NONE)
# flap edge thickness + hinge barrels
d.path("M350,598 L650,598 L650,606 L350,606 Z", "Flap edge", fill=WALNUT_DK, stroke=INK, strokeWidth=2)
for hx_, tag in [(392, "L"), (608, "R")]:
    ell(f"Hinge {tag}", hx_, 550, 5, 5, fill=BRASS, stroke="#3A2408", strokeWidth=1.5)
note((350, 606), (650, 606))

# --- drawer stack ----------------------------------------------------------------------
rect("Drawer case", X0, 608, X1, 750, fill=WALNUT_X, stroke=INK, strokeWidth=3)
for i, (dy0, dy1) in enumerate([(614, 654), (658, 698), (702, 742)]):
    rect(f"Drawer {i+1}", 372, dy0, 628, dy1, fill=WALNUT, stroke=INK, strokeWidth=2.5)
    line(f"Drawer {i+1} light", 378, dy0 + 4, 622, dy0 + 4, 3, "#C89458", opacity=45)
    for j, kx in enumerate((440, 560)):
        ell(f"Drawer {i+1} pull {j+1}", kx, (dy0 + dy1) / 2 + 2, 5.5, 5.5,
            fill=BRASS, stroke="#3A2408", strokeWidth=1.4)
    # key escutcheon
    ell(f"Drawer {i+1} key", 500, (dy0 + dy1) / 2 + 2, 3, 4.5, fill="#1E0E06", stroke=NONE, opacity=80)

# --- base, apron, bracket feet ---------------------------------------------------------
rect("Base molding", 356, 750, 644, 760, fill=WALNUT_DK, stroke=INK, strokeWidth=2)
line("Base light", 360, 752, 640, 752, 3, "#C89458", opacity=45)
# shallow shaped apron between the feet
d.path("M398,760 L602,760 L602,764 Q500,782 398,764 Z", "Apron", fill=WALNUT_DK,
       stroke=INK, strokeWidth=2)
d.path("M364,760 L404,760 L398,782 L366,782 Q361,770 364,760 Z", "Left foot", fill=WALNUT,
       stroke=INK, strokeWidth=2.5)
d.path("M596,760 L636,760 L634,782 L602,782 Q596,770 596,760 Z", "Right foot", fill=WALNUT,
       stroke=INK, strokeWidth=2.5)
note((364, 782), (636, 782))

# right-side shade over the whole case; left kiss of lamplight
rect("Right shade", 628, 219, 638, 750, fill="#100802", stroke=NONE, opacity=45)
rect("Left light", 362, 219, 370, 750, fill="#F0CE8E", stroke=NONE, opacity=18)

# --- sanity: the whole piece inside the disc ------------------------------------------
worst = min(PR - math.hypot(x - PCX, y - PCY) for x, y in FIT)
print("min clearance to rim: %.1f" % worst)
assert worst > 24, worst

# --- rim + captions ---------------------------------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#080410", strokeWidth=6)
d.shape("ellipse", "Plate inner edge", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D0BCD6", strokeWidth=3, opacity=26)

r1 = d.text("SECRETARY DESK", "Name", x=500, y=936, size=58, font="Virelai Sans",
            color="#F0E2D4", justify="center")
LINE2, SZ2, TRK = "WALNUT · BRASS", 22, 280
r2 = d.text(LINE2, "Second line", x=500, y=972, size=SZ2, font="Virelai Sans",
            color="#C4AAC6", justify="center")
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

d.finish("secretary-desk-V1R00")
