#!/usr/bin/env python3
"""Rigid airship — field plate V1R00. Near-profile of a zeppelin at night,
nose to the right: long envelope with panel bands reading as gradient strips,
four tail fins with a blank rudder, control car slung under the bow third,
two engine cars, and a single searchlight reaching up from the hills to catch
the hull. 1000x1000. House style: gradients + translucent shading, never flat
fills. Plate = circle center (500,460) r420; ground closes on the disc arc."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Rigid Airship — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1C1620"
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

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin([(0, "#0E1220"), (1, "#05060C")], DOWN), stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#7A8AC8", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin([(0, "#1A2450"), (0.45, "#2E3A6E"), (0.75, "#1E2246"), (1, "#0C0E22")], DOWN),
        stroke="#0A0D1C", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad([(0, "#000000", 0), (0.75, "#000000", 0), (1, "#060818", 0.55)]), stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8C8F0", strokeWidth=3, opacity=35)
# star field
stars = [(210, 215, 2.2), (260, 140, 1.6), (330, 170, 2.6), (430, 110, 1.8), (540, 140, 2.2),
         (640, 100, 1.6), (740, 150, 2.4), (810, 215, 1.8), (160, 320, 1.8), (845, 340, 2.0),
         (230, 400, 1.4), (790, 420, 1.5), (150, 470, 1.6), (860, 505, 1.4), (340, 110, 1.5),
         (680, 200, 1.4), (480, 90, 1.4), (760, 250, 1.6)]
for i, (x, y, r) in enumerate(stars):
    assert on_disc(x, y, 10), (x, y)
    ell(f"Star {i+1}", x, y, r, r, fill="#FFF8E8", opacity=75, stroke=NONE)
for i, (x, y) in enumerate([(330, 170), (740, 150), (210, 215)]):
    ell(f"Star glow {i+1}", x, y, 9, 9, fill=rad([(0, "#FFF8E8", 0.5), (1, "#FFF8E8", 0)]), stroke=NONE)
# crescent moon, upper right
d.path("M790,296 A30,30 0 1 1 762,344 A24,24 0 1 0 790,296 Z", "Moon",
       fill=lin([(0, "#FFF6DC"), (1, "#E0CE9E")], DOWN), stroke=NONE, opacity=90)
ell("Moon glow", 768, 330, 56, 56, fill=rad([(0, "#FFF2CE", 0.3), (1, "#FFF2CE", 0)]), stroke=NONE)
# thin night clouds
for i, (cx, cy, rx, ry, op) in enumerate([(280, 260, 110, 18, 22), (660, 330, 130, 20, 18),
                                         (420, 210, 80, 13, 16)]):
    assert on_disc(cx - rx, cy, 8) and on_disc(cx + rx, cy, 8)
    ell(f"Cloud {i+1}", cx, cy, rx, ry, fill=lin([(0, "#6E7AAC"), (1, "#3A4068")], DOWN),
        opacity=op, stroke=NONE)

# --- ground: dark hills closing on the disc arc ----------------------------------------
GY = 788
gl, gr = chord(GY)
d.path(f"M{gl:.1f},{GY} Q300,756 420,772 Q560,790 680,764 Q780,748 {gr:.1f},{GY} "
       f"A420,420 0 0 1 {gl:.1f},{GY} Z", "Hills",
       fill=lin([(0, "#161B34"), (1, "#0A0C1C")], DOWN), stroke=NONE)
# a few lit windows and a beacon on the hills
for i, (x, y, op) in enumerate([(310, 776, 60), (352, 780, 45), (610, 772, 55), (660, 770, 40),
                                (430, 780, 50), (720, 776, 45)]):
    assert on_disc(x, y, 6)
    rect(f"Ground light {i+1}", x, y, 5, 6, fill="#FFD88E", opacity=op, stroke=NONE)
ell("Beacon glow", 690, 762, 22, 10, fill=rad([(0, "#FFC87A", 0.5), (1, "#FFC87A", 0)]), stroke=NONE)

# --- searchlight: one beam from the hills up to the hull ---------------------------------
# source sits on the right-hand hill
SX, SY = 690, 764
BX0, BY0 = 592, 502          # where the beam meets the hull (lower edge)
BX1, BY1 = 664, 508
d.path(f"M{SX},{SY} L{BX0},{BY0} L{BX1},{BY1} Z", "Searchlight beam",
       fill=lin([(0, "#FFF4CC", 0.02), (1, "#FFF0BE", 0.4)], DOWN), stroke=NONE)
d.path(f"M{SX},{SY} L{BX0 + 10},{BY0} L{BX1 - 8},{BY1} Z", "Searchlight core",
       fill=lin([(0, "#FFFCE8", 0.05), (1, "#FFF8D8", 0.5)], DOWN), stroke=NONE)
ell("Searchlight source", SX, SY, 12, 8, fill=rad([(0, "#FFFCE8"), (1, "#F0B85E")]), stroke=NONE)
ell("Source flare", SX, SY, 30, 18, fill=rad([(0, "#FFF4CC", 0.6), (1, "#FFF4CC", 0)]), stroke=NONE)

# --- tail fins (behind the envelope): cruciform, upper + lower visible, side fins hinted ---
FIN = lin([(0, "#8E9AC4"), (0.5, "#5A6494"), (1, "#2C3152")], DOWN)
FIN_DARK = lin([(0, "#6A749E"), (1, "#242844")], DOWN)
# far side fins, slightly darker and offset, peeking out
d.path("M238,404 L168,332 Q158,322 172,320 L252,318 Q268,320 268,336 L264,404 Z",
       "Far fin top", fill=FIN_DARK, stroke=INK, strokeWidth=2.5, opacity=85)
d.path("M238,462 L168,534 Q158,544 172,546 L252,548 Q268,546 268,530 L264,462 Z",
       "Far fin bottom", fill=FIN_DARK, stroke=INK, strokeWidth=2.5, opacity=85)
# near fins: upper and lower, blank rudders
d.path("M268,402 L196,298 Q186,284 204,282 L292,282 Q310,284 310,302 L304,402 Z",
       "Upper fin", fill=FIN, stroke=INK, strokeWidth=3)
d.path("M268,464 L196,568 Q186,582 204,584 L292,584 Q310,582 310,564 L304,464 Z",
       "Lower fin", fill=FIN, stroke=INK, strokeWidth=3)
for nm, (ya, yb) in [("upper", (300, 398)), ("lower", (566, 468))]:
    line(f"{nm} fin rib 1", 226, ya, 262, yb, 3, "#20243C", opacity=45)
    line(f"{nm} fin rib 2", 262, ya + 4, 288, yb - 6, 3, "#20243C", opacity=45)
line("Upper rudder hinge", 286, 288, 296, 400, 3, "#1C2036", opacity=55)
line("Lower rudder hinge", 286, 578, 296, 466, 3, "#1C2036", opacity=55)
line("Upper fin sheen", 210, 296, 280, 296, 3, "#E8EEFA", opacity=30)

# --- envelope ------------------------------------------------------------------------------
# silhouette: tail tip at x=150, nose at x=884, vertical centre y=435, beam B=78
X0, X1, YC, B = 150, 884, 435, 78
d.path(f"M{X0},436 C240,372 340,358 500,358 C660,358 800,382 868,420 "
       f"C886,430 886,442 868,450 C800,486 660,510 500,510 C340,510 240,496 {X0},436 Z",
       "Envelope", fill=lin([(0, "#C4CCE8"), (0.4, "#8E98C4"), (0.75, "#4E5680"), (1, "#2A2E4E")], DOWN),
       stroke=INK, strokeWidth=3.5)
# panel bands: transverse strips, alternating lighter/darker, following the hull curve
def env_h(x):
    s = (x - X0) / (X1 - X0)
    return B * math.pow(math.sin(math.pi * min(max(s, 0), 1)), 0.72)
band_i = 0
for xb in range(196, 860, 40):
    band_i += 1
    h = env_h(xb) - 4
    yc = YC + 2 * math.sin((xb - X0) / (X1 - X0) * math.pi - 0.4)  # centreline droop
    light = band_i % 2 == 0
    d.path(f"M{xb - 9},{yc - h:.1f} Q{xb},{yc - h - 6:.1f} {xb + 9},{yc - h:.1f} "
           f"L{xb + 9},{yc + h:.1f} Q{xb},{yc + h + 6:.1f} {xb - 9},{yc + h:.1f} Z",
           f"Panel band {band_i}",
           fill=lin([(0, "#FFFFFF" if light else "#141A34", 0.16 if light else 0.14),
                     (1, "#FFFFFF" if light else "#141A34", 0.05 if light else 0.3)], DOWN),
           stroke=NONE)
# longitudinal seams
for frac, nm, op in [(0.45, "upper", 40), (0.62, "lower", 35)]:
    pts = []
    for x in range(X0 + 30, X1 - 26, 24):
        h = env_h(x)
        pts.append((x, YC - h + 2 * h * frac))
    d.path("M" + " L".join(f"{x},{y:.1f}" for x, y in pts), f"Seam {nm}",
           fill=NONE, stroke="#181C34", strokeWidth=2.5, opacity=op)
# nose cap + rim light on the leading edge
ell("Nose cap", 866, 434, 16, 20, fill=rad([(0, "#E8EEFA"), (1, "#8E98C4")]), stroke=INK, strokeWidth=2)
d.path("M806,392 Q852,406 872,428", "Nose rim light", fill=NONE, stroke="#F2F6FF",
       strokeWidth=3.5, opacity=50, cap="round")
# searchlight splash on the belly
ell("Beam splash", 628, 502, 60, 16, fill=rad([(0, "#FFF6D8", 0.85), (0.6, "#FFE49A", 0.4), (1, "#FFE49A", 0)]),
    stroke=NONE)
ell("Beam splash hot", 634, 503, 24, 8, fill=rad([(0, "#FFFCEE", 0.95), (1, "#FFFCEE", 0)]), stroke=NONE)
# nose pennant mast + blank station marks
line("Nose mast", 872, 434, 892, 434, 3, "#2A2E4E")
ell("Nose tip light", 893, 434, 4, 4, fill=rad([(0, "#FFE9B0"), (1, "#E89A3A")]), stroke=NONE)

# --- cars slung beneath ----------------------------------------------------------------------
def car(name, cx, top, w, h, lit):
    for k, (sx, sw) in enumerate([(cx - w * 0.3, 4), (cx + w * 0.3, 4)]):
        line(f"{name} strut {k+1}", sx, env_h(sx) * -1 + YC if False else YC + env_h(sx) - 2,
             sx, top + 4, sw, "#3A3E5C", opacity=85)
    d.path(f"M{cx - w / 2},{top + h / 2} Q{cx - w / 2},{top} {cx - w / 2 + 12},{top} "
           f"L{cx + w / 2 - 10},{top} Q{cx + w / 2 + 4},{top + h / 2} {cx + w / 2 - 10},{top + h} "
           f"L{cx - w / 2 + 12},{top + h} Q{cx - w / 2},{top + h} {cx - w / 2},{top + h / 2} Z",
           name, fill=lin([(0, "#AEB6DA"), (0.5, "#6A729E"), (1, "#30345A")], DOWN),
           stroke=INK, strokeWidth=2.5)
    line(f"{name} sheen", cx - w / 2 + 14, top + 3, cx + w / 2 - 14, top + 3, 2.5, "#FFFFFF", opacity=35)
    if lit:
        for i in range(3):
            rect(f"{name} window {i+1}", cx - w / 2 + 18 + i * 22, top + h * 0.28, 14, h * 0.4,
                 fill=lin([(0, "#FFEDB4", 0.9), (1, "#F0A94E", 0.75)], DOWN),
                 stroke="#3A3020", strokeWidth=1.5, radius=3)
    else:
        rect(f"{name} louvre", cx - w / 2 + 14, top + h * 0.3, w - 28, h * 0.36,
             fill="#1A1E38", stroke=NONE, radius=3)
        for i in range(3):
            line(f"{name} louvre {i+1}", cx - w / 2 + 18, top + h * 0.36 + i * 4,
                 cx + w / 2 - 18, top + h * 0.36 + i * 4, 2.5, "#4A5078", opacity=70)

# control car under the bow third, windows lit
car("Control car", 668, 518, 108, 34, lit=True)
ell("Control car glow", 668, 535, 70, 20, fill=rad([(0, "#FFC87A", 0.25), (1, "#FFC87A", 0)]), stroke=NONE)
# two engine cars amidships, dark louvres + prop stubs
car("Engine car aft", 330, 520, 72, 26, lit=False)
car("Engine car fore", 480, 524, 72, 26, lit=False)
for nm, cx in [("aft", 330), ("fore", 480)]:
    line(f"Prop stub {nm}", cx - 42, 533, cx - 56, 533, 3, "#3A3E5C")
    ell(f"Prop {nm}", cx - 60, 533, 5, 16, fill=rad([(0, "#D8DEF2", 0.55), (1, "#D8DEF2", 0.1)]),
        stroke="#D8DEF2", strokeWidth=1.5, opacity=70)
# small tail fins' running light
ell("Tail light", 152, 436, 4, 4, fill=rad([(0, "#FFD9B0"), (1, "#E8763A")]), stroke=NONE)
ell("Tail light glow", 152, 436, 10, 10, fill=rad([(0, "#FF9A5A", 0.5), (1, "#FF9A5A", 0)]), stroke=NONE)

# --- sanity: everything stays inside the plate ----------------------------------------------
for x, y in [(150, 436), (884, 435), (204, 282), (196, 568), (310, 584), (668, 552),
             (272, 533), (690, 764), (790, 296)]:
    assert on_disc(x, y, 8), (x, y)

# --- name ------------------------------------------------------------------------------------
d.text("RIGID AIRSHIP", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#DCE4F8", justify="center")
LINE2, SZ2, TRK = "1936 · DIESEL · HYDROGEN LIFT", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#9AACC8", justify="center")
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

d.finish("rigid-airship-V1R00")
