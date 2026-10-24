#!/usr/bin/env python3
"""Chono dalca — field plate V1R00. Slight elevated near-profile of the
three-plank sewn canoe of the southern Chilean archipelagos (per the Museo
Chileno de Arte Precolombino reconstruction: two side planks bent with fire
and sewn with culeu-bark cordage to a longer central plank). Pointed rising
ends, one seam with lashing stitches along the near side, a single plain
paddle resting beside the hull, cold green water closing on the disc arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; water chord y=580."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Chono Dalca — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A1E16"
DOWN = -90                    # linear gradient angle: first stop at the top

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def chord(y):
    h = math.sqrt(PR**2 - (y - PCY)**2)
    return PCX - h, PCX + h

def _stops(stops):
    return [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]

def lin(stops, angle=None):
    g = {"kind": "linear", "stops": _stops(stops)}
    if angle is not None:
        g["angle"] = angle
    return {"gradient": g}

def rad(stops):
    return {"gradient": {"kind": "radial", "stops": _stops(stops)}}

def rect(name, x, y, w, h, **kw):
    return d.shape("rectangle", name, x=round(x, 1), y=round(y, 1), width=round(w, 1), height=round(h, 1), **kw)

def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(cx - rx, 1), y=round(cy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)

def line(name, x0, y0, x1, y1, w, color, **kw):
    return d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", name, fill=NONE, stroke=color,
                  strokeWidth=w, cap="round", **kw)

def quad(p0, p1, p2, t):
    x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0]
    y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1]
    tx = 2*(1-t)*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0])
    ty = 2*(1-t)*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1])
    return (x, y), (tx, ty)

SIDE_PLANK = lin([(0, "#B08858"), (0.5, "#8A6238"), (1, "#54371F")], DOWN)
KEEL_PLANK = lin([(0, "#96694A"), (0.55, "#6B472E"), (1, "#3B2514")], DOWN)
INTERIOR = lin([(0, "#3E2C1C"), (1, "#150E08")], DOWN)
FAR_LIP = lin([(0, "#C9A26E"), (1, "#8A6238")], DOWN)
SEA = lin([(0, "#3D6B5C"), (0.45, "#1E4038"), (1, "#0B1B22")], DOWN)
PADDLE_WOOD = lin([(0, "#A57A4E"), (1, "#5C3D22")], DOWN)

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#0E1A18"), (1, "#050B0C")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#4E8A7A", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin([(0, "#233F46"), (0.45, "#3E6158"), (0.72, "#6A8570"), (1, "#2E3A44")], DOWN),
        stroke="#0A1418", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.75, "#000000", 0), (1, "#0A1214", 0.5)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D4E4DA", strokeWidth=3, opacity=35)
# cold overcast glow, high left
ell("Sky glow", 300, 260, 210, 160, fill=rad([(0, "#D8E4D2", 0.4), (0.55, "#A8BCA8", 0.18), (1, "#A8BCA8", 0)]),
    stroke=NONE)
# distant archipelago headlands, low and translucent above the water chord
for i, (x, y, w, h, op) in enumerate([(255, 545, 150, 42, 40), (665, 530, 185, 50, 34)]):
    assert on_disc(x - w / 2, y - h / 2, 6) or on_disc(x + w / 2, y - h / 2, 6)
    ell(f"Headland {i+1}", x, y, w / 2, h / 2, fill=lin([(0, "#22403A"), (1, "#0E1E20")], DOWN),
        opacity=op, stroke=NONE)
# two small gulls
for i, (x, y, s) in enumerate([(610, 240, 1.0), (660, 268, 0.75)]):
    d.path(f"M{x-14*s:.0f},{y:.0f} Q{x-5*s:.0f},{y-7*s:.0f} {x:.0f},{y:.0f} Q{x+5*s:.0f},{y-7*s:.0f} {x+14*s:.0f},{y:.0f}",
           f"Gull {i+1}", fill=NONE, stroke="#C8D4C4", strokeWidth=2.5, cap="round", opacity=55)

# --- water: disc segment below the y=566 chord, closed on the rim arc ---------------
wx0, wx1 = chord(566)
d.path(f"M{wx0:.0f},566 L{wx1:.0f},566 A{PR},{PR} 0 0 1 {wx0:.0f},566 Z",
       "Water", fill=SEA, stroke=NONE)
# faint swell bands contained on the chord
for i, (cx, cy, rx, op) in enumerate([(300, 640, 120, 20), (560, 690, 160, 16), (430, 760, 200, 12)]):
    if on_disc(cx - rx, cy, 4) and on_disc(cx + rx, cy, 4):
        ell(f"Swell {i+1}", cx, cy, rx, 8 + i, fill=lin([(0, "#6AA08C"), (1, "#2A5048")], 0),
            opacity=op, stroke=NONE)

# --- dalca hull ---------------------------------------------------------------------
# hull exterior: sheer -> stem face -> keel curve -> stern face
d.path("M208,500 Q500,562 792,482 L782,528 Q500,640 214,532 Z",
       "Hull", fill=KEEL_PLANK, stroke=INK, strokeWidth=3.5)
# side plank band between sheer and seam
d.path("M212,504 Q500,564 788,486 L784,502 Q500,578 218,518 Z",
       "Side plank", fill=SIDE_PLANK, stroke=NONE)
# interior opening between far gunwale and near sheer
d.path("M230,504 Q500,522 772,486 L776,498 Q500,556 238,520 Z",
       "Interior", fill=INTERIOR, stroke=NONE)
# far gunwale lip
d.path("M230,504 Q500,522 772,486", "Far gunwale", fill=NONE,
       stroke=FAR_LIP, strokeWidth=4, cap="round")
# near gunwale edge
d.path("M212,504 Q500,564 788,486", "Near gunwale", fill=NONE,
       stroke="#3A2616", strokeWidth=4, cap="round")

# seam curve between side plank and central plank, with culeu-cord stitches
SEAM = [(222, 520), (500, 582), (780, 504)]
d.path(f"M{SEAM[0][0]},{SEAM[0][1]} Q{SEAM[1][0]},{SEAM[1][1]} {SEAM[2][0]},{SEAM[2][1]}",
       "Seam", fill=NONE, stroke="#301E10", strokeWidth=4.5, cap="round", opacity=90)
for i, t in enumerate([0.05, 0.125, 0.20, 0.275, 0.35, 0.425, 0.50, 0.575, 0.65, 0.725, 0.80, 0.875, 0.95]):
    (x, y), (tx, ty) = quad(*[tuple(p) for p in SEAM], t)
    ln = math.hypot(tx, ty) or 1
    tx, ty = tx / ln, ty / ln
    nx, ny = -ty, tx
    # stitches run diagonal: mostly across the seam, slightly along it
    dx, dy = nx * 0.82 + tx * 0.57, ny * 0.82 + ty * 0.57
    d.path(f"M{x - dx*9:.0f},{y - dy*9:.0f} L{x + dx*9:.0f},{y + dy*9:.0f}",
           f"Stitch {i+1}", fill=NONE, stroke="#241608", strokeWidth=3.4, cap="round")
# converging end seams where the three planks meet at each tip
for i, ((x0, y0), (x1, y1)) in enumerate([((222, 506), (238, 528)), ((230, 500), (252, 522)),
                                          ((778, 490), (758, 514)), ((770, 496), (748, 518))]):
    line(f"End lashing {i+1}", x0, y0, x1, y1, 3.2, "#241608")

# weathered grain streaks on the planks
for i, (x0, y0, x1, y1, op) in enumerate([(300, 512, 430, 516, 30), (470, 520, 620, 510, 26),
                                          (560, 556, 700, 542, 24), (290, 548, 420, 552, 22),
                                          (380, 596, 540, 600, 20), (560, 592, 680, 578, 20)]):
    line(f"Grain {i+1}", x0, y0, x1, y1, 2.2, "#2E1D10", opacity=op)

# --- paddle resting beside the hull, blade in the water -------------------------------
line("Paddle shaft", 318, 428, 372, 612, 6.5, PADDLE_WOOD)
d.path("M372,612 Q360,640 364,664 Q368,682 380,686 Q390,680 386,656 Q382,632 372,612 Z",
       "Paddle blade", fill=PADDLE_WOOD, stroke=INK, strokeWidth=2.5)
line("Paddle grip", 318, 428, 312, 414, 7.5, "#8A6238")

# --- water dressing -------------------------------------------------------------------
# ripple where the hull meets the water, bow and stern
for i, (cx, cy, rx, op) in enumerate([(722, 570, 60, 45), (668, 574, 40, 35),
                                     (278, 574, 55, 40), (330, 576, 34, 30)]):
    ell(f"Ripple {i+1}", cx, cy, rx, 6 + i, fill=rad([(0, "#9CC8B4", 0.5), (1, "#9CC8B4", 0)]),
        stroke=NONE, opacity=op)
# paddle blade wash
ell("Blade wash", 380, 686, 30, 8, fill=rad([(0, "#9CC8B4", 0.5), (1, "#9CC8B4", 0)]), stroke=NONE)
# hull reflection
ell("Hull reflection", 500, 652, 210, 15, fill=rad([(0, "#5A3A26", 0.35), (1, "#5A3A26", 0)]), stroke=NONE)

# --- sanity: everything stays inside the plate ----------------------------------------
for x, y in [(208, 500), (792, 482), (214, 532), (782, 528), (500, 640), (230, 504),
             (312, 414), (380, 686), (105, 550), (895, 555)]:
    assert on_disc(x, y, 6), (x, y)

# --- name ----------------------------------------------------------------------------
d.text("DALCA", "Name", x=500, y=930, size=58, font="Virelai Sans", color="#EDE4D2", justify="center")
LINE2, SZ2, TRK = "PLANK-BUILT · PADDLE", 22, 200
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans", color="#B9C6B4", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("chono-dalca-V1R00")
