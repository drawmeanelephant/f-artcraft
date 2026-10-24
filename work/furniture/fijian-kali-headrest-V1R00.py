#!/usr/bin/env python3
"""Fijian kali headrest — field plate V1R00. Low three-quarter view of the
Te Papa OL002079 type: one long wooden beam — the neck rest — carried on a
pair of short legs at each end, carved from a single piece. Straight,
slightly waisted beam with rounded lugs; warm wood on an ocean-night disc,
contact shadow kept inside the rim. No invented carving, no Tongan/Samoan
forms. 1000x1000. House style: gradients + translucent shading, never flat.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Fijian Kali Headrest — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2E1E12"
DOWN = -90                    # linear gradient angle: first stop at the top

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

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

WOOD = lin([(0, "#9A6B3E"), (0.45, "#6E4526"), (1, "#3C2412")], DOWN)
WOOD_TOP = lin([(0, "#C89458"), (1, "#7E5630")], DOWN)
WOOD_DK = lin([(0, "#54371E"), (1, "#281708")], DOWN)

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#0A121A"), (1, "#04070C")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#4A6E8A", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin([(0, "#16283A"), (0.5, "#23425A"), (0.78, "#365E72"), (1, "#16202E")], DOWN),
        stroke="#080E16", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.75, "#000000", 0), (1, "#080E16", 0.55)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BCD0DC", strokeWidth=3, opacity=35)
# moonlit glow, upper right
ell("Moon glow", 660, 270, 180, 150, fill=rad([(0, "#D4E2EA", 0.32), (0.55, "#9AB4C4", 0.13), (1, "#9AB4C4", 0)]),
    stroke=NONE)
ell("Moon", 668, 268, 20, 20, fill=rad([(0, "#F2F8FA"), (1, "#B4CCD8")]), stroke=NONE, opacity=90)
# a handful of small stars
for i, (x, y, r) in enumerate([(300, 200, 2.6), (380, 150, 2.0), (520, 190, 2.4), (760, 330, 2.0),
                               (220, 330, 2.2), (830, 250, 1.8)]):
    ell(f"Star {i+1}", x, y, r, r, fill="#D8E6EC", opacity=55, stroke=NONE)

# --- kali: beam on four legs, long axis receding right ----------------------------------
# contact shadow, long and low, hugging the feet
ell("Shadow", 500, 592, 255, 32, fill=rad([(0, "#04070C", 0.7), (0.6, "#04070C", 0.3), (1, "#04070C", 0)]),
    stroke=NONE)

# far-side legs first (drawn before the beam's underside)
d.path("M300,468 L316,466 L312,560 L298,562 Z", "Far left leg", fill=WOOD_DK, stroke=INK, strokeWidth=2.5)
d.path("M676,452 L694,450 L694,552 L680,554 Z", "Far right leg", fill=WOOD_DK, stroke=INK, strokeWidth=2.5)

# the beam: slight waist, rounded lugs at each end
d.path("M238,452 Q262,438 292,436 Q500,414 706,416 Q744,418 758,432 "
       "Q768,444 760,456 Q746,470 712,470 Q500,486 296,484 Q258,482 244,470 Q234,460 238,452 Z",
       "Beam", fill=WOOD, stroke=INK, strokeWidth=3.5)
# polished rest surface along the top of the beam
d.path("M252,450 Q300,440 400,434 Q560,424 706,424 Q736,426 748,434 Q736,440 700,440 "
       "Q500,440 320,452 Q274,456 252,450 Z",
       "Rest sheen", fill=WOOD_TOP, stroke=NONE, opacity=85)
# end lug shading: slightly swollen, darker ends
ell("Left lug", 260, 462, 24, 14, fill=rad([(0, "#3C2412", 0), (1, "#2A1608", 0.4)]), stroke=NONE)
ell("Right lug", 736, 444, 26, 15, fill=rad([(0, "#3C2412", 0), (1, "#2A1608", 0.4)]), stroke=NONE)
# grain lines along the beam length
for i, (x0, y0, x1, y1, op) in enumerate([(280, 462, 560, 446, 26), (320, 472, 620, 452, 22),
                                          (430, 440, 700, 430, 22), (250, 458, 420, 448, 20),
                                          (540, 466, 730, 452, 20)]):
    line(f"Grain {i+1}", x0, y0, x1, y1, 2, "#3C2412", opacity=op)

# near-side legs: splayed in the view, with a shoulder where each meets the beam
d.path("M266,480 L290,478 L276,574 L254,576 Z", "Left leg", fill=WOOD, stroke=INK, strokeWidth=3)
d.path("M706,468 L732,466 L748,566 L726,568 Z", "Right leg", fill=WOOD, stroke=INK, strokeWidth=3)
# leg shoulders: a hard join line under the beam edge, >=3pt
line("Left shoulder", 260, 484, 296, 482, 4, INK, opacity=80)
line("Right shoulder", 700, 472, 738, 470, 4, INK, opacity=80)
# feet flares
d.path("M254,576 L276,574 L282,588 L248,588 Z", "Left foot", fill=WOOD_DK, stroke=INK, strokeWidth=2.5)
d.path("M726,568 L748,566 L756,580 L722,582 Z", "Right foot", fill=WOOD_DK, stroke=INK, strokeWidth=2.5)

# --- sanity: everything stays inside the plate ---------------------------------------------
for x, y in [(238, 452), (758, 432), (296, 484), (248, 588), (756, 580), (230, 618),
             (770, 618), (500, 648), (668, 268)]:
    assert on_disc(x, y, 6), (x, y)

# --- name -----------------------------------------------------------------------------------
r1 = d.text("KALI HEADREST", "Name", x=500, y=930, size=56, font="Virelai Sans",
            color="#EFE3CC", justify="center")
d.cmd("text.setStyle", "Name tracking", id=r1["id"], tracking=60)
LINE2, SZ2, TRK = "WOOD", 22, 260
r2 = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
            color="#B4C4CE", justify="center")
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

d.finish("fijian-kali-headrest-V1R00")
