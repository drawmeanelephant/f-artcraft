#!/usr/bin/env python3
"""Monarch — field plate V2R00, a rendition of V1R00.

V1 was the straight dorsal spread on a pale green ground. This take is the
animal at dusk: perched on a milkweed umbel, wings half-raised, lit from
behind so the membranes glow and the veins read as silhouette. Deep plum sky,
a low burnt-orange horizon, grass and milkweed leaves in silhouette on the
disc's arc. 1000x1000. House style: gradients + translucent shading.
"""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Monarch — Field Plate V2", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#241018"


def rim_y(x):
    return CY + math.sqrt(max(R * R - (x - CX) ** 2, 0))


def cr(pts, closed=False, tension=1.0):
    n = len(pts)
    if n < 2:
        return ""
    ext = ([pts[-1]] + list(pts) + [pts[0], pts[1]]) if closed else \
          ([pts[0]] + list(pts) + [pts[-1]])
    dd = "M%.1f,%.1f " % pts[0]
    for i in range(1, n if closed else n - 1):
        p0, p1, p2, p3 = ext[i], ext[i + 1], ext[i + 2], ext[i + 3]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * tension, p1[1] + (p2[1] - p0[1]) / 6 * tension)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * tension, p2[1] - (p3[1] - p1[1]) / 6 * tension)
        dd += "C%.1f,%.1f %.1f,%.1f %.1f,%.1f " % (c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    return dd + ("Z" if closed else "")


NUM = re.compile(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)")


def wing_transform(bx, by, s, deg, mirror):
    t = math.radians(deg)
    c, sn = math.cos(t), math.sin(t)

    def T(x, y):
        if mirror:
            x = -x
        return (bx + s * (x * c - y * sn), by + s * (x * sn + y * c))
    return T


def place(dd, T):
    return NUM.sub(lambda m: "%.1f,%.1f" % T(float(m.group(1)), float(m.group(2))), dd)


BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#120A18"}, {"offset": 0.5, "color": "#0C0610"},
    {"offset": 1, "color": "#050306"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A2334"}, {"offset": 0.45, "color": "#2E1226"},
    {"offset": 1, "color": "#170A16"}]}}
SKY_GRAD = {"gradient": {"kind": "linear", "start": [0, 60], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#241030"}, {"offset": 0.42, "color": "#6E2838"},
    {"offset": 0.72, "color": "#C4653C"}, {"offset": 1, "color": "#E89A56"}]}}
WING_GRAD = {"gradient": {"kind": "linear", "start": [0, 300], "end": [520, 620], "stops": [
    {"offset": 0, "color": "#FFD79A"}, {"offset": 0.5, "color": "#F0993F"},
    {"offset": 1, "color": "#C25A28"}]}}
WING_FAR = {"gradient": {"kind": "linear", "start": [0, 300], "end": [500, 620], "stops": [
    {"offset": 0, "color": "#C2794E"}, {"offset": 0.6, "color": "#9C4E2E"},
    {"offset": 1, "color": "#6E2E22"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [470, 380], "end": [540, 560], "stops": [
    {"offset": 0, "color": "#3E2630"}, {"offset": 0.5, "color": "#221119"},
    {"offset": 1, "color": "#120A0E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2A0F1E", strokeWidth=6)
# dusk sky inside the disc, clipped to the arc by construction
d.shape("ellipse", "Sky", x=80, y=40, width=840, height=840, fill=SKY_GRAD, stroke=NONE)
# horizon band and low sun bloom
d.shape("ellipse", "Sun bloom", x=290, y=300, width=420, height=340,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FFE0A8", "opacity": 0.85},
            {"offset": 0.45, "color": "#FFB36A", "opacity": 0.45},
            {"offset": 1, "color": "#FF9A50", "opacity": 0}]}}, stroke=NONE, opacity=80)
d.shape("ellipse", "Sun core", x=452, y=404, width=96, height=96,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FFF6DC", "opacity": 0.95},
            {"offset": 1, "color": "#FFD79A", "opacity": 0}]}}, stroke=NONE)
# thin cloud bands
for i, (y, w, op) in enumerate([(232, 420, 22), (286, 300, 16), (344, 360, 12)]):
    d.shape("ellipse", f"Cloud {i+1}", x=500 - w / 2, y=y, width=w, height=18,
            fill="#FFC48C", opacity=op, stroke=NONE)

# --- silhouette ground, rooted on the disc arc --------------------------------
GY = 690
cap = [(CX + R * math.cos(math.radians(a)), CY + R * math.sin(math.radians(a)))
       for a in [146 - i * (112 / 40) for i in range(41)]]
d.path(cr(cap + [(CX + R * math.cos(math.radians(34)), GY + 6),
                 (CX - R * math.cos(math.radians(34)), GY + 6)], closed=True),
       "Ground", fill="#1B0C14", opacity=94, stroke=NONE)
d.path(f"M166,{GY} C250,{GY - 14} 400,{GY - 6} 540,{GY - 11} C660,{GY - 16} 790,{GY - 4} 834,{GY}",
       "Ground crest", fill=NONE, stroke="#4A2230", strokeWidth=4, opacity=55, cap="round")
# grass blades, all inside the disc
for i, (xb, h, sway, w) in enumerate([(206, 150, -46, 11), (234, 214, 26, 10), (264, 132, 52, 9),
                                      (736, 168, -38, 11), (768, 210, 22, 10), (800, 140, -30, 9),
                                      (330, 96, 18, 8), (676, 88, -20, 8)]):
    tipx = xb + sway
    d.path(f"M{xb - w / 2},{GY} Q{xb + sway * 0.35:.1f},{GY - h * 0.6:.1f} {tipx:.1f},{GY - h:.1f} "
           f"Q{xb + sway * 0.5 + w:.1f},{GY - h * 0.5:.1f} {xb + w / 2},{GY} Z",
           f"Grass {i+1}", fill="#150A10", opacity=92, stroke=NONE)

# --- milkweed: stem, leaves, umbel ----------------------------------------------
STEM = "#3A1E22"
d.path("M500,706 C494,672 506,650 500,626", "Milkweed stem", fill=NONE, stroke=STEM,
       strokeWidth=9, cap="round", opacity=95)
for i, (x0, y0, x1, y1, cx, cy_) in enumerate([(498, 668, 386, 630, 442, 604),
                                               (502, 656, 626, 610, 570, 594)]):
    dd = (f"M{x0},{y0} C{cx},{cy_} {cx},{cy_} {x1},{y1} "
          f"C{cx + 14},{cy_ + 26} {cx - 8},{cy_ + 28} {x0},{y0} Z")
    d.path(dd, f"Milkweed leaf {i+1}", fill="#2C1620", stroke="#4A2430", strokeWidth=3, opacity=94)
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Milkweed leaf vein {i+1}", fill=NONE,
           stroke="#5E303A", strokeWidth=2.6, opacity=55, cap="round")

# umbel: florets on short pedicels around a dome above the stem
UMB = (500, 596)
for i in range(17):
    a = math.radians(-172 + i * 11.4)
    rr = 58 if i % 2 else 46
    fx, fy = UMB[0] + math.cos(a) * rr, UMB[1] + math.sin(a) * rr * 0.56
    d.path(f"M{UMB[0]},{UMB[1] + 26} Q{(UMB[0] + fx) / 2:.1f},{(UMB[1] + fy) / 2 + 12:.1f} {fx:.1f},{fy:.1f}",
           f"Pedicel {i+1}", fill=NONE, stroke="#4A2430", strokeWidth=3, opacity=80, cap="round")
    for k in range(5):
        pa = math.radians(-90 + k * 72 + i * 7)
        px, py = fx + math.cos(pa) * 9, fy + math.sin(pa) * 7
        d.shape("ellipse", f"Floret {i+1} petal {k+1}", x=px - 6.5, y=py - 5.6, width=13, height=11.2,
                fill="#F2C7B4" if i % 3 else "#F8DCC8", opacity=94, stroke=NONE)
    d.shape("ellipse", f"Floret {i+1} centre", x=fx - 3, y=fy - 3, width=6, height=6,
            fill="#C9736F", stroke=NONE)
# a few florets lit from behind
for i, (fx, fy) in enumerate([(462, 566), (540, 562), (500, 550)]):
    d.shape("ellipse", f"Floret glow {i+1}", x=fx - 14, y=fy - 12, width=28, height=24,
            fill={"gradient": {"kind": "radial", "stops": [
                {"offset": 0, "color": "#FFD9A8", "opacity": 0.75},
                {"offset": 1, "color": "#FFD9A8", "opacity": 0}]}}, stroke=NONE, opacity=75)

# --- wings ----------------------------------------------------------------------
FORE = ("M0,0 C50,-46 150,-86 246,-96 C286,-99 304,-80 298,-54 "
        "C286,-8 246,32 192,56 C146,74 92,70 54,52 C18,34 0,18 0,0 Z")
FORE_VEINS = ["M6,-2 L294,-58", "M6,0 L262,-34", "M6,2 L240,4", "M6,4 L214,28",
              "M6,6 L182,46", "M6,8 L136,58", "M4,10 L84,60"]
FORE_CELL = ("M22,2 C40,-18 74,-30 106,-30 C118,-18 114,2 96,14 "
             "C74,28 38,24 22,2 Z")
FORE_SPOTS = [(286, -60), (272, -40), (256, -18), (238, 4), (218, 24), (196, 42),
              (170, 54), (144, 62), (116, 64), (88, 60), (60, 52), (38, 42)]
HIND = ("M0,0 C58,12 128,36 176,74 C212,104 208,142 174,152 "
        "C128,166 68,142 32,106 C10,82 0,42 0,0 Z")
HIND_VEINS = ["M6,2 L166,66", "M6,6 L172,96", "M6,10 L156,124", "M6,12 L124,142", "M6,14 L86,146"]
HIND_SPOTS = [(180, 78), (186, 100), (180, 120), (166, 136), (146, 146), (122, 150), (98, 148)]


def draw_wing(outline, veins, spots, cell, bx, by, s, deg, mirror, far=False, spots_n=12):
    T = wing_transform(bx, by, s, deg, mirror)
    d.path(place(outline, T), "Wing" + (" far" if far else ""),
           fill=WING_FAR if far else WING_GRAD, stroke="#1A0A12", strokeWidth=4, opacity=97)
    # black margin band: a thick stroke along the outer contour, then the inner edge cleaned up
    d.path(place(outline, T), "Wing margin", fill=NONE, stroke="#1E0C14",
           strokeWidth=26 * s, opacity=88)
    if cell:
        d.path(place(cell, T), "Discal cell", fill=NONE, stroke="#1E0C14",
               strokeWidth=5 * s, opacity=88)
    for i, v in enumerate(veins):
        d.path(place(v, T), f"Vein {i+1}", fill=NONE, stroke="#220E16",
               strokeWidth=4.2 * s, opacity=90, cap="round")
    for i, sp in enumerate(spots[:spots_n]):
        sx, sy = T(*sp)
        r = (5.4 if i % 2 == 0 else 4.2) * s
        d.shape("ellipse", f"Spot {i+1}", x=sx - r, y=sy - r, width=2 * r, height=2 * r,
                fill="#FFF0DE", opacity=72 if far else 90, stroke=NONE)


# far pair first (behind the body), smaller and smoke-dimmed
draw_wing(FORE, FORE_VEINS, FORE_SPOTS, FORE_CELL, 486, 424, 0.94, -6, True, far=True, spots_n=9)
draw_wing(HIND, HIND_VEINS, HIND_SPOTS, None, 484, 448, 0.92, 6, True, far=True, spots_n=5)

# --- body ------------------------------------------------------------------------
# abdomen, tapering to the umbel
d.path("M486,432 C484,472 488,520 492,556 C496,570 504,570 508,556 "
       "C512,520 516,472 514,432 Z", "Abdomen", fill=BODY_GRAD, stroke=INK, strokeWidth=3)
for i in range(5):
    y = 448 + i * 22
    d.path(f"M488,{y} C496,{y + 4} 504,{y + 4} 512,{y}", f"Abdomen band {i+1}",
           fill=NONE, stroke="#0E060A", strokeWidth=3, opacity=70, cap="round")
d.shape("ellipse", "Thorax", x=482, y=404, width=36, height=44, fill=BODY_GRAD,
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Thorax fur", x=486, y=404, width=28, height=16, fill="#5A3A3E",
        opacity=55, stroke=NONE)
d.shape("ellipse", "Head", x=486, y=380, width=28, height=26, fill=BODY_GRAD,
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye L", x=482, y=384, width=11, height=12, fill="#0C0608", stroke=NONE)
d.shape("ellipse", "Eye R", x=505, y=384, width=11, height=12, fill="#0C0608", stroke=NONE)
d.shape("ellipse", "Eye glint L", x=483, y=385, width=4, height=4, fill="#FFE6C0", opacity=90, stroke=NONE)
d.shape("ellipse", "Eye glint R", x=506, y=385, width=4, height=4, fill="#FFE6C0", opacity=90, stroke=NONE)
# antennae with clubs, and the coiled proboscis
d.path("M492,378 C470,354 452,334 444,318", "Antenna L", fill=NONE, stroke="#1E0C14",
       strokeWidth=3.6, cap="round")
d.shape("ellipse", "Antenna club L", x=437, y=311, width=14, height=13, fill="#2A121A",
        stroke=NONE, opacity=95)
d.path("M508,378 C530,352 548,332 556,316", "Antenna R", fill=NONE, stroke="#1E0C14",
       strokeWidth=3.6, cap="round")
d.shape("ellipse", "Antenna club R", x=550, y=309, width=14, height=13, fill="#2A121A",
        stroke=NONE, opacity=95)
d.path("M500,398 C508,404 508,414 500,414 C494,414 492,408 496,404", "Proboscis",
       fill=NONE, stroke="#2A121A", strokeWidth=3.4, cap="round")
# legs reaching down to the umbel
for i, (x0, y0, x1, y1, xm, ym) in enumerate([(488, 424, 468, 566, 462, 500),
                                               (492, 428, 486, 582, 480, 506),
                                               (508, 428, 518, 582, 524, 510),
                                               (512, 424, 536, 566, 544, 502)]):
    d.path(f"M{x0},{y0} Q{xm},{ym} {x1},{y1}", f"Leg {i+1}", fill=NONE, stroke="#241016",
           strokeWidth=4.6, cap="round")
    d.path(f"M{x1},{y1} l{-6 if x1 < 500 else 6},10", f"Leg claw {i+1}", fill=NONE,
           stroke="#241016", strokeWidth=3.4, cap="round")

# near pair over the body
draw_wing(FORE, FORE_VEINS, FORE_SPOTS, FORE_CELL, 514, 418, 1.04, -15, False)
draw_wing(HIND, HIND_VEINS, HIND_SPOTS, None, 512, 444, 1.02, 8, False)

# --- front rim light on the body edges -------------------------------------------
d.path("M486,436 C484,478 488,522 492,552", "Body rim L", fill=NONE, stroke="#FFC98C",
       strokeWidth=3, opacity=45, cap="round")
d.path("M516,430 C518,474 514,520 508,552", "Body rim R", fill=NONE, stroke="#FFE0B0",
       strokeWidth=2.6, opacity=35, cap="round")

# --- plate rim over everything ----------------------------------------------------
# nothing may show outside the disc: repaint the backdrop over the ring,
# then the rim gets drawn back on top of it
d.shape("ellipse", "Backdrop mask", x=-200, y=-240, width=1400, height=1400,
        fill=NONE, stroke=BG_GRAD, strokeWidth=560)

d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#2A0F1E", strokeWidth=6)
d.shape("ellipse", "Rim light", x=96, y=56, width=808, height=808,
        fill=NONE, stroke="#FFC48C", strokeWidth=2, opacity=20)

d.text("MONARCH", "Name", x=500, y=946, size=52, font="Virelai Sans",
       color="#FFE8CE", justify="center")
d.text("LEPIDOPTERA", "Order", x=500, y=976, size=22, font="Virelai Sans",
       color="#F0B98E", justify="center")

d.finish("monarch-V2R00")
