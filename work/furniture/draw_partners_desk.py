#!/usr/bin/env python3
"""Partners desk — field plate V1R00. Front elevation of a kneehole desk two
people can disagree across: a broad mahogany top with a tooled green-leather
writing surface, three frieze drawers, twin pedestals of three graduated
drawers each, and a kneehole that shows the far side's cupboard door and a
sliver of floor beyond. Two opposing book piles stage the argument. Mahogany
plate, chambers mood. 1000x1000.
House style: gradients + translucent shading, never flat.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Partners Desk — Field Plate", 1000, 1000)

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

def linxy(x0, y0, x1, y1, stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
                         "stops": _stops(stops)}}

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

# mahogany: deep red case wood, lit upper-left
MAHOG      = lin([(0, "#8E4A34"), (0.45, "#5E2E1E"), (1, "#2E130C")], DOWN)
MAHOG_X    = linxy(288, 0, 712, 0, [(0, "#9A563A"), (0.45, "#6E3826"), (1, "#321610")])
MAHOG_DK   = lin([(0, "#462417"), (1, "#1E0D06")], DOWN)
DRAWER_ST  = lin([(0, "#965236"), (0.5, "#6E3622"), (1, "#3A1A0E")], DOWN)
LEATHER    = lin([(0, "#334E38"), (0.6, "#223A28"), (1, "#101F14")], DOWN)
BRASS      = rad([(0, "#F0CC7E"), (0.6, "#C89A4E"), (1, "#7A5420")])
RECESS     = lin([(0, "#160A05"), (1, "#080302")], DOWN)

FIT = []
def note(*pts):
    FIT.extend(pts)

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#141014"), (1, "#060405")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#7A4A40", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#5E3B32"), (0.55, "#3C2320"), (1, "#160C0C")]),
        stroke="#0C0506", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.72, "#000000", 0), (1, "#0A0406", 0.5)]), stroke=NONE)
ell("Lamplight", 370, 220, 300, 210,
    fill=rad([(0, "#F0CE8E", 0.18), (0.6, "#C89A58", 0.06), (1, "#C89A58", 0)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CEA998", strokeWidth=3, opacity=28)
for i, (x, y, w) in enumerate([(215, 245, 6), (770, 260, 7), (175, 615, 6), (818, 590, 7),
                               (432, 110, 6), (625, 112, 7), (162, 428, 6), (838, 415, 6)]):
    ell(f"Plate fleck {i+1}", x, y, w / 2, w / 2, fill="#A87E68", opacity=30, stroke=NONE)

# --- floor + contact shadow --------------------------------------------------------
HZN = 784
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin([(0, "#221612", 0.6), (1, "#0C0605", 0.92)], DOWN), stroke=NONE)
ell("Desk shadow", 500, 786, 238, 24,
    fill=rad([(0, "#040404", 0.7), (0.6, "#040404", 0.32), (1, "#040404", 0)]), stroke=NONE)
note((292, 784), (708, 784))

# --- the top: shallow receding surface + edge band ------------------------------------
d.path("M326,292 L674,292 L712,336 L288,336 Z", "Top surface",
       fill=linxy(0, 292, 0, 336, [(0, "#7E452E"), (0.6, "#5E3020"), (1, "#3C1C10")]),
       stroke=INK, strokeWidth=3, join="round")
# leather writing field with gilt tooling border
d.path("M348,298 L652,298 L682,330 L318,330 Z", "Leather field", fill=LEATHER,
       stroke="#0A140C", strokeWidth=2)
d.path("M358,301 L642,301 L668,327 L332,327 Z", "Gilt border", fill=NONE,
       stroke="#C89A4E", strokeWidth=1.8, opacity=65)
ell("Leather sheen", 440, 312, 120, 9,
    fill=rad([(0, "#8AA894", 0.22), (1, "#8AA894", 0)]), stroke=NONE)
# front edge band — the slab's thickness
rect("Top edge band", 288, 336, 712, 368, fill=MAHOG, stroke=INK, strokeWidth=3)
line("Top lip light", 296, 339, 704, 339, 3, "#D89A6A", opacity=55)
note((288, 336), (712, 336), (326, 292), (674, 292))

# opposing book piles on the top: the argument, staged
def bookpile(x0, tag, lean):
    y = 292
    for i, (bw, bh, col) in enumerate([(64, 12, "#4A2E20"), (56, 11, "#5E3A24"), (48, 10, "#3E2A30")]):
        skew = lean * i * 3
        d.path(f"M{x0 + skew},{y - bh} L{x0 + bw + skew},{y - bh} L{x0 + bw + skew - lean},{y} L{x0 + skew - lean},{y} Z",
               f"{tag} book {i+1}", fill=linxy(x0, y - bh, x0, y, [(0, col), (1, "#1E0E08")]),
               stroke=INK, strokeWidth=2)
        line(f"{tag} book {i+1} edge", x0 + 4 + skew - lean * 0.5, y - 2,
             x0 + bw - 6 + skew - lean * 0.5, y - 2, 2, "#E8D8B8", opacity=50)
        y -= bh + 1
    return y

bookpile(344, "Left pile", -1)
bookpile(596, "Right pile", 1)

# --- frieze: three shallow drawers across ---------------------------------------------
for i, (fx0, fx1) in enumerate([(288, 432), (436, 564), (568, 712)]):
    rect(f"Frieze drawer {i+1}", fx0 + 2, 370, fx1 - 2, 402, fill=DRAWER_ST,
         stroke=INK, strokeWidth=2.5)
    line(f"Frieze {i+1} light", fx0 + 10, 374, fx1 - 10, 374, 2.5, "#D89A6A", opacity=45)
    # bail handle: two posts + a hanging arc
    bx = (fx0 + fx1) / 2
    ell(f"Frieze {i+1} post L", bx - 13, 385, 3, 3, fill=BRASS, stroke="#3A2408", strokeWidth=1)
    ell(f"Frieze {i+1} post R", bx + 13, 385, 3, 3, fill=BRASS, stroke="#3A2408", strokeWidth=1)
    d.path(f"M{bx - 13},{385} Q{bx},{398} {bx + 13},{385}", f"Frieze {i+1} bail",
           fill=NONE, stroke="#D9AE5E", strokeWidth=2.4, cap="round")
    ell(f"Frieze {i+1} key", bx, 397, 2.4, 3.4, fill="#140804", stroke=NONE, opacity=85)

# --- pedestals: twin banks of three drawers ---------------------------------------------
def pedestal(x0, x1, tag):
    rect(f"{tag} pedestal", x0, 404, x1, 752, fill=MAHOG_X, stroke=INK, strokeWidth=3)
    for i, (dy0, dy1) in enumerate([(412, 512), (520, 620), (628, 728)]):
        rect(f"{tag} drawer {i+1}", x0 + 8, dy0, x1 - 8, dy1, fill=DRAWER_ST,
             stroke=INK, strokeWidth=2.5)
        # cross-banding: a lighter inset frame line on each drawer face
        rect(f"{tag} drawer {i+1} band", x0 + 15, dy0 + 6, x1 - 15, dy1 - 6,
             fill=NONE, stroke="#B8764E", strokeWidth=1.6, opacity=55)
        line(f"{tag} drawer {i+1} light", x0 + 14, dy0 + 5, x1 - 14, dy0 + 5,
             2.5, "#D89A6A", opacity=40)
        bx = (x0 + x1) / 2
        by = (dy0 + dy1) / 2 + 3
        ell(f"{tag} d{i+1} post L", bx - 15, by - 4, 3.2, 3.2, fill=BRASS,
            stroke="#3A2408", strokeWidth=1.1)
        ell(f"{tag} d{i+1} post R", bx + 15, by - 4, 3.2, 3.2, fill=BRASS,
            stroke="#3A2408", strokeWidth=1.1)
        d.path(f"M{bx - 15},{by - 4} Q{bx},{by + 10} {bx + 15},{by - 4}",
               f"{tag} d{i+1} bail", fill=NONE, stroke="#D9AE5E", strokeWidth=2.6, cap="round")
        ell(f"{tag} d{i+1} esc", bx, by + 10, 2.6, 3.8, fill="#140804",
            stroke=NONE, opacity=85)
    # drawer gaps read as shadow seams
    for gy in (516, 624):
        line(f"{tag} seam {gy}", x0 + 8, gy, x1 - 8, gy, 2, "#120602", opacity=70)

pedestal(288, 434, "Left")
pedestal(566, 712, "Right")

# --- kneehole: recess, far cupboard door, floor sliver -----------------------------------
rect("Kneehole recess", 434, 404, 566, 748, fill=RECESS, stroke=INK, strokeWidth=2.5)
# pedestal inner faces catching a little light at the reveal
rect("Kneehole reveal L", 434, 404, 446, 748, fill=linxy(434, 0, 446, 0, [(0, "#3A1E10"), (1, "#140804")]), stroke=NONE)
rect("Kneehole reveal R", 554, 404, 566, 748, fill=linxy(554, 0, 566, 0, [(0, "#140804"), (1, "#3A1E10")]), stroke=NONE)
# the far side's cupboard door, set back and dimmed — the other partner's face
rect("Far cupboard", 458, 470, 542, 690, fill=lin([(0, "#4A2817"), (1, "#221006")], DOWN),
     stroke="#120704", strokeWidth=2.5)
rect("Far cupboard panel", 468, 482, 532, 678, fill=NONE, stroke="#6E3C24",
     strokeWidth=2, opacity=70)
rect("Far panel inset", 476, 492, 524, 668, fill=lin([(0, "#3E2212"), (1, "#1A0C05")], DOWN),
     stroke="#120704", strokeWidth=1.6)
ell("Far door ring", 500, 500, 5, 5, fill=NONE, stroke="#9A7438", strokeWidth=2.2)
ell("Far door hub", 500, 500, 2.4, 2.4, fill=BRASS, stroke="#3A2408", strokeWidth=1)
# floor sliver under the far door — light through the kneehole
rect("Kneehole floor", 446, 712, 554, 748, fill=lin([(0, "#4E3624", 0.85), (1, "#20130B", 0.95)], DOWN),
     stroke=NONE)
line("Kneehole floor edge", 450, 716, 550, 716, 2, "#8A6038", opacity=45)
# the kneehole's own floor shadow
ell("Kneehole shade", 500, 738, 62, 12, fill=rad([(0, "#050302", 0.6), (1, "#050302", 0)]), stroke=NONE)

# --- plinth base -------------------------------------------------------------------------
rect("Plinth", 288, 752, 712, 782, fill=MAHOG_DK, stroke=INK, strokeWidth=2.5)
line("Plinth light", 294, 755, 434, 755, 2.5, "#B8764E", opacity=40)
line("Plinth light R", 570, 755, 706, 755, 2.5, "#B8764E", opacity=40)
rect("Plinth kneehole", 434, 752, 566, 782, fill="#0E0603", stroke=NONE)
note((288, 782), (712, 782))

# right-side shade over the whole case; left kiss of lamplight
rect("Right shade", 700, 336, 712, 752, fill="#0E0503", stroke=NONE, opacity=40)
rect("Left light", 288, 336, 298, 752, fill="#F0CE8E", stroke=NONE, opacity=15)

# --- sanity: the whole piece inside the disc ------------------------------------------
worst = min(PR - math.hypot(x - PCX, y - PCY) for x, y in FIT)
print("min clearance to rim: %.1f" % worst)
assert worst > 20, worst

# --- captions ---------------------------------------------------------------------------
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o["bounds"]
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit

def caption(name, mats):
    n = d.text(name, "Name", x=500, y=934, size=56, font="Virelai Sans",
               color="#F0E2D4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C8A088", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=240)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "materials")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" %
              (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "materials":
            assert b["width"] <= 760, b["width"]

caption("PARTNERS DESK", "MAHOGANY · LEATHER · BRASS")
d.finish("partners-desk-V1R00")
