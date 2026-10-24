#!/usr/bin/env python3
"""Caballito de totora — field plate V1R00. Huanchaco north-coast Peru form:
two lashed totora-reed bundles, the inner longer one drawn up into the narrow
upturned prow, broad blunt stern. Near-profile with a little top surface
visible; a simple paddle rests beside it, blade in a small contained water
patch. Warm straw on a sea-green disc. Not a Titicaca balsa, no sail, no
carved prow head. 1000x1000. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Caballito de Totora — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#33241A"
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

STRAW = lin([(0, "#DDBE7E"), (0.45, "#C09A58"), (1, "#7E5B2E")], DOWN)
STRAW_HI = lin([(0, "#EDD9A2"), (1, "#B08A4E")], DOWN)
LASH = "#5C3E20"
SEA = lin([(0, "#3D6B5C"), (0.5, "#1E4038"), (1, "#0B1B22")], DOWN)
PADDLE_WOOD = lin([(0, "#A57A4E"), (1, "#5C3D22")], DOWN)

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#101B19"), (1, "#060B0C")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#4E8A7A", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin([(0, "#2A4A48"), (0.5, "#43705F"), (0.78, "#6E8A6C"), (1, "#2E3A44")], DOWN),
        stroke="#0A1418", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.75, "#000000", 0), (1, "#0A1214", 0.5)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E4D4", strokeWidth=3, opacity=35)
# low warm sun off the sea, upper left
ell("Sun glow", 270, 300, 190, 150, fill=rad([(0, "#FFE2B0", 0.4), (0.55, "#E8B878", 0.16), (1, "#E8B878", 0)]),
    stroke=NONE)
ell("Sun", 262, 306, 24, 24, fill=rad([(0, "#FFF6DC"), (1, "#F0C078")]), stroke=NONE, opacity=90)

# --- small contained water patch under the hull --------------------------------------
ell("Water patch", 500, 610, 330, 46, fill=SEA, stroke=NONE, opacity=92)
for i, (cx, cy, rx, op) in enumerate([(330, 600, 90, 30), (640, 622, 110, 24)]):
    ell(f"Swell {i+1}", cx, cy, rx, 7, fill=lin([(0, "#6AA08C"), (1, "#2A5048")], 0),
        opacity=op, stroke=NONE)

# --- reed hull: main bundle with upturned prow, prow to the right -----------------------
# outer (front + bottom) edge then rounded tip then inner deck edge back to stern
d.path("M250,586 Q480,584 620,572 Q700,560 736,502 Q758,454 752,402 "
       "Q754,390 766,394 Q778,400 772,414 "
       "Q762,456 730,500 Q682,552 560,562 L262,562 Q248,572 250,586 Z",
       "Main bundle", fill=STRAW, stroke=INK, strokeWidth=3.5)
# secondary bundle strip visible along the top of the body (a little top surface)
d.path("M272,548 Q440,536 560,528 Q614,522 652,516 Q662,514 660,524 Q652,532 636,534 "
       "Q520,546 400,552 L278,558 Z",
       "Second bundle", fill=STRAW_HI, stroke=INK, strokeWidth=2)

# reed texture: longitudinal strokes following the body and the prow curve
for i, (x0, y0, x1, y1, op) in enumerate([(280, 566, 560, 560, 30), (300, 574, 580, 566, 26),
                                          (420, 548, 640, 540, 24), (560, 552, 700, 520, 24),
                                          (660, 540, 720, 480, 26), (700, 500, 744, 432, 24),
                                          (724, 478, 754, 414, 22), (280, 550, 520, 540, 20),
                                          (742, 452, 762, 412, 20)]):
    line(f"Reed line {i+1}", x0, y0, x1, y1, 2, "#8A6A38", opacity=op)

# lashings: bands across the bundle, perpendicular to its axis, stern to prow base
for i, (cx, top, bot) in enumerate([(310, (306, 548), (314, 584)), (390, (386, 543), (392, 582)),
                                    (470, (468, 540), (470, 580)), (550, (552, 538), (548, 578)),
                                    (625, (630, 534), (618, 572)), (690, (700, 524), (682, 560))]):
    line(f"Lashing {i+1}", top[0], top[1], bot[0], bot[1], 4.5, LASH)
    line(f"Lashing edge {i+1}", top[0] + 5, top[1] + 2, bot[0] + 5, bot[1] - 2, 2, "#8A6238", opacity=70)
# prow throat lashing where the neck narrows
line("Throat lashing", 714, 532, 740, 486, 4.5, LASH)
line("Throat lashing edge", 721, 534, 746, 490, 2, "#8A6238", opacity=70)
# stern end: blunt bound cap
line("Stern binding", 258, 556, 256, 580, 5, LASH)

# --- paddle resting beside the stern, blade in the water --------------------------------
line("Paddle shaft", 208, 440, 238, 636, 6, PADDLE_WOOD)
d.path("M238,636 Q228,662 232,684 Q236,700 248,702 Q256,696 252,674 Q248,652 238,636 Z",
       "Paddle blade", fill=PADDLE_WOOD, stroke=INK, strokeWidth=2.5)

# --- water dressing ----------------------------------------------------------------------
for i, (cx, cy, rx, op) in enumerate([(700, 596, 60, 40), (300, 604, 55, 36), (560, 612, 70, 26)]):
    ell(f"Ripple {i+1}", cx, cy, rx, 6, fill=rad([(0, "#9CC8B4", 0.45), (1, "#9CC8B4", 0)]),
        stroke=NONE, opacity=op)
ell("Blade wash", 244, 700, 26, 7, fill=rad([(0, "#9CC8B4", 0.5), (1, "#9CC8B4", 0)]), stroke=NONE)
ell("Hull reflection", 470, 634, 190, 13, fill=rad([(0, "#8A6A38", 0.3), (1, "#8A6A38", 0)]), stroke=NONE)

# --- sanity: everything stays inside the plate --------------------------------------------
for x, y in [(250, 582), (752, 402), (778, 400), (772, 414), (208, 440), (248, 702),
             (170, 610), (830, 610), (500, 656), (262, 306)]:
    assert on_disc(x, y, 6), (x, y)

# --- name ----------------------------------------------------------------------------------
r1 = d.text("CABALLITO DE TOTORA", "Name", x=500, y=930, size=44, font="Virelai Sans",
            color="#F2E4C8", justify="center")
LINE2, SZ2, TRK = "REED BUNDLES · PADDLE", 22, 200
r2 = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
            color="#C9C2A8", justify="center")
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

d.finish("caballito-de-totora-V1R00")
