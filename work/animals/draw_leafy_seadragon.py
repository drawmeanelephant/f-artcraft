#!/usr/bin/env python3
"""Leafy seadragon — field-guide plate V1R00. Full body in profile drifting
right: banded golden trunk and curling tail, translucent leaf-appendages
layered over and behind the body, a smooth pipe snout and eye. Olive-gold
plate with kelp shadows whose blades root on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Leafy Seadragon — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420


def rim_y(x):
    return CY + math.sqrt(R * R - (x - CX) ** 2)


INK = "#3A2C12"
BG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#1E2410"}, {"offset": 1, "color": "#080A04"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E2D488"}, {"offset": 0.6, "color": "#ADA04C"},
    {"offset": 1, "color": "#5C5622"}]}}
KELP_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#6A6A2C"}, {"offset": 1, "color": "#3A3C16"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#E8C45A"}, {"offset": 0.55, "color": "#C08E32"},
    {"offset": 1, "color": "#86601E"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0D27A"}, {"offset": 0.7, "color": "#C89A3C"},
    {"offset": 1, "color": "#8E6624"}]}}
SNOUT_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#F2D888"}, {"offset": 1, "color": "#B08432"}]}}
LEAF_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E6CC6A"}, {"offset": 0.6, "color": "#B8A040"},
    {"offset": 1, "color": "#C88A50"}]}}
LEAF_FAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A8A3A"}, {"offset": 1, "color": "#6E6228"}]}}
FIN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FFF4C8"}, {"offset": 1, "color": "#E0C878"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A4418", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F6EEC0", strokeWidth=3, opacity=45)
# surface caustics high in the plate
for i, (y, x0, x1) in enumerate([(130, 360, 640), (165, 290, 700), (200, 250, 520)]):
    mid = (x0 + x1) / 2
    d.path(f"M{x0},{y} C{mid - 60},{y - 14} {mid - 20},{y + 14} {mid + 30},{y} "
           f"C{mid + 80},{y - 14} {x1 - 40},{y + 10} {x1},{y}",
           f"Caustic {i+1}", fill=NONE, stroke="#FFF8D0", strokeWidth=4, opacity=22, cap="round")


# kelp shadows: wavy blades rooted on the disc arc
def kelp(xb, height, sway, w, label, op):
    n = 24
    left, right = [], []
    yb = rim_y(xb)
    for i in range(n + 1):
        t = i / n
        y = yb - height * t
        x = xb + sway * math.sin(t * math.pi * 1.6) * t
        ww = w * (1 - 0.65 * t) * (1 + 0.25 * math.sin(t * 9))
        left.append((x - ww / 2, y))
        right.append((x + ww / 2, y))
    rb = right[0][0]
    lb = left[0][0]
    dd = f"M{rb:.1f},{rim_y(rb):.1f} A420,420 0 0 1 {lb:.1f},{rim_y(lb):.1f} "
    dd += " ".join("L%.1f,%.1f" % p for p in left[1:])
    dd += " Q%.1f,%.1f %.1f,%.1f " % (left[-1][0] + w * 0.2, left[-1][1] - w * 0.5, right[-1][0], right[-1][1])
    dd += " ".join("L%.1f,%.1f" % p for p in reversed(right[1:])) + " Z"
    d.path(dd, label, fill=KELP_GRAD, opacity=op, stroke=NONE)


kelp(210, 420, 40, 34, "Kelp 1", 34)
kelp(275, 560, -50, 40, "Kelp 2", 26)
kelp(720, 520, 55, 38, "Kelp 3", 30)
kelp(800, 360, -35, 30, "Kelp 4", 36)
kelp(560, 300, 40, 30, "Kelp 5", 18)
for i, (x, y, w) in enumerate([(190, 300, 6), (780, 250, 7), (160, 470, 6), (840, 470, 7), (230, 700, 6),
                               (760, 700, 7), (420, 110, 6), (600, 108, 5), (330, 830, 5), (660, 830, 6),
                               (880, 380, 5), (130, 560, 5), (480, 760, 5), (720, 160, 5)]):
    d.shape("ellipse", f"Marine snow {i+1}", x=x, y=y, width=w, height=w, fill="#FFFBE0", opacity=45, stroke=NONE)


# --- the animal is drawn in its own frame, scaled up onto the plate -------------
import re
S, OX, OY = 1.20, 508, 548
TX, TY = 500, 466
EXTENT = []


def T(x, y):
    p = (TX + S * (x - OX), TY + S * (y - OY))
    EXTENT.append(p)
    return p


def tf(dd):
    return re.sub(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)",
                  lambda m: "%.1f,%.1f" % T(float(m.group(1)), float(m.group(2))), dd)


class Animal:
    def path(self, dd, label, **kw):
        return d.path(tf(dd), label, **kw)

    def shape(self, kind, label, x, y, width, height, **kw):
        x0, y0 = T(x, y)
        T(x + width, y + height)
        return d.shape(kind, label, x=round(x0, 1), y=round(y0, 1),
                       width=round(width * S, 1), height=round(height * S, 1), **kw)


AN = Animal()

# --- geometry helpers ------------------------------------------------------------
def smooth_closed(pts):
    n = len(pts)
    mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2) for i in range(n)]
    dd = "M%.1f,%.1f " % mids[-1]
    for i in range(n):
        dd += "Q%.1f,%.1f %.1f,%.1f " % (pts[i][0], pts[i][1], mids[i][0], mids[i][1])
    return dd + "Z"


def leaflet(x, y, ang, L, W):
    """A lobed, pointed blade from (x,y) along ang."""
    ux, uy = math.cos(ang), math.sin(ang)
    px, py = -uy, ux
    prof = [(0.0, 0.10), (0.18, 0.75), (0.34, 1.0), (0.48, 0.55), (0.62, 0.85),
            (0.78, 0.45), (0.90, 0.40), (1.0, 0.0)]
    left = [(x + ux * L * t + px * W * k / 2, y + uy * L * t + py * W * k / 2) for t, k in prof]
    right = [(x + ux * L * t - px * W * k * 0.9 / 2, y + uy * L * t - py * W * k * 0.9 / 2) for t, k in prof]
    pts = left + list(reversed(right[1:-1]))
    return smooth_closed(pts), (x + ux * L * 0.85, y + uy * L * 0.85)


def appendage(base, ang_deg, stalk, size, label, far=False, spread=30, n=3):
    a = math.radians(ang_deg)
    bx, by = base
    sx, sy = bx + math.cos(a) * stalk, by + math.sin(a) * stalk
    col = "#6E5420" if far else "#8A6A28"
    AN.path(f"M{bx:.1f},{by:.1f} Q{(bx + sx) / 2 + 6:.1f},{(by + sy) / 2 - 6:.1f} {sx:.1f},{sy:.1f}",
           f"{label} stalk", fill=NONE, stroke=col, strokeWidth=4 if not far else 3, cap="round",
           opacity=80 if not far else 60)
    offs = [(-spread, 0.8), (0, 1.0), (spread, 0.85)] if n == 3 else \
        [(-spread * 1.6, 0.62), (-spread * 0.8, 0.86), (0, 1.0), (spread * 0.8, 0.9), (spread * 1.6, 0.66)]
    for j, (o, k) in enumerate(offs):
        aa = a + math.radians(o)
        dd, tip = leaflet(sx, sy, aa, size * k, size * 0.40 * k)
        AN.path(dd, f"{label} leaf {j+1}", fill=LEAF_FAR_GRAD if far else LEAF_GRAD,
               opacity=60 if far else 70, stroke="#6A4E1A" if not far else NONE, strokeWidth=3)
        if not far:
            AN.path(f"M{sx:.1f},{sy:.1f} L{tip[0]:.1f},{tip[1]:.1f}", f"{label} vein {j+1}",
                   fill=NONE, stroke="#FFF2C0", strokeWidth=3, opacity=45, cap="round")


# --- body spine (head back -> tail tip) ---------------------------------------------
SPINE = [(654, 426), (626, 436), (602, 456), (584, 480), (556, 500), (514, 512), (466, 516),
         (420, 518), (378, 528), (340, 548), (308, 578), (286, 614), (278, 652), (286, 688),
         (306, 712), (332, 718), (352, 704), (354, 682), (340, 670)]
WID = [44, 38, 34, 38, 52, 66, 72, 68, 58, 46, 36, 28, 22, 18, 14, 11, 9, 7, 5]
NRM = []
for i, (x, y) in enumerate(SPINE):
    ax, ay = SPINE[max(i - 1, 0)]
    bx, by = SPINE[min(i + 1, len(SPINE) - 1)]
    dx, dy = bx - ax, by - ay
    ln = math.hypot(dx, dy) or 1
    NRM.append((dy / ln, -dx / ln))     # points to the dorsal (upper) side
DORS = [(x + nx * w / 2, y + ny * w / 2) for (x, y), (nx, ny), w in zip(SPINE, NRM, WID)]
VENT = [(x - nx * w / 2, y - ny * w / 2) for (x, y), (nx, ny), w in zip(SPINE, NRM, WID)]

# far-side appendages, behind the body
appendage(VENT[5], 75, 38, 86, "Far belly leaf", far=True, n=5, spread=22)
appendage(DORS[6], -80, 36, 82, "Far back leaf", far=True, n=5, spread=22)
appendage(VENT[9], 150, 28, 60, "Far tail leaf", far=True)
appendage(DORS[2], -60, 28, 60, "Far neck leaf", far=True)
appendage(DORS[9], -115, 30, 64, "Far rump leaf", far=True)

# dorsal fin: small translucent fan on the back
fx, fy = DORS[7]
AN.path(f"M{fx - 26:.1f},{fy + 4:.1f} C{fx - 30:.1f},{fy - 36:.1f} {fx + 20:.1f},{fy - 40:.1f} {fx + 30:.1f},{fy + 4:.1f} Z",
       "Dorsal fin", fill=FIN_GRAD, opacity=50, stroke="#C8A850", strokeWidth=3)
for j in range(5):
    t = j / 4
    AN.path(f"M{fx - 20 + 44 * t:.1f},{fy + 2:.1f} L{fx - 26 + 52 * t:.1f},{fy - 30 + 6 * abs(t - 0.5):.1f}",
           f"Dorsal fin ray {j+1}", fill=NONE, stroke="#B89440", strokeWidth=3, opacity=45, cap="round")

# trunk + tail
outline = "M%.1f,%.1f " % DORS[0]
for i in range(1, len(DORS) - 1):
    mx, my = (DORS[i][0] + DORS[i + 1][0]) / 2, (DORS[i][1] + DORS[i + 1][1]) / 2
    outline += "Q%.1f,%.1f %.1f,%.1f " % (DORS[i][0], DORS[i][1], mx, my)
tx, ty = SPINE[-1]
outline += "Q%.1f,%.1f %.1f,%.1f " % (tx - 4, ty - 4, VENT[-1][0], VENT[-1][1])
rv = list(reversed(VENT))
for i in range(1, len(rv) - 1):
    mx, my = (rv[i][0] + rv[i + 1][0]) / 2, (rv[i][1] + rv[i + 1][1]) / 2
    outline += "Q%.1f,%.1f %.1f,%.1f " % (rv[i][0], rv[i][1], mx, my)
outline += "L%.1f,%.1f Z" % VENT[0]
AN.path(outline, "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=5)
# belly shade + back light, following the spine
AN.path("M" + " L".join("%.1f,%.1f" % ((x + v[0]) / 2 * 0 + (x * 0.35 + v[0] * 0.65), (y * 0.35 + v[1] * 0.65))
                       for (x, y), v in list(zip(SPINE, VENT))[3:12]),
       "Belly shade", fill=NONE, stroke="#6E4A16", strokeWidth=12, opacity=26, cap="round")
AN.path("M" + " L".join("%.1f,%.1f" % (x * 0.45 + dv[0] * 0.55, y * 0.45 + dv[1] * 0.55)
                       for (x, y), dv in list(zip(SPINE, DORS))[3:11]),
       "Back light", fill=NONE, stroke="#FFF0B8", strokeWidth=8, opacity=30, cap="round")
# bands: pale rings with a dark seam, the bony segments of the trunk and tail
for i in range(2, len(SPINE) - 3):
    for half in (0, 1):
        if half:
            a = ((DORS[i][0] + DORS[i + 1][0]) / 2, (DORS[i][1] + DORS[i + 1][1]) / 2)
            b = ((VENT[i][0] + VENT[i + 1][0]) / 2, (VENT[i][1] + VENT[i + 1][1]) / 2)
            c = ((SPINE[i][0] + SPINE[i + 1][0]) / 2, (SPINE[i][1] + SPINE[i + 1][1]) / 2)
        else:
            a, b, c = DORS[i], VENT[i], SPINE[i]
        nx, ny = NRM[i]
        cx, cy = c[0] + ny * 5, c[1] - nx * 5   # bow the ring toward the tail
        if half:
            AN.path(f"M{a[0]:.1f},{a[1]:.1f} Q{cx:.1f},{cy:.1f} {b[0]:.1f},{b[1]:.1f}",
                   f"Band seam {i+1}", fill=NONE, stroke="#5A3C12", strokeWidth=3, opacity=45, cap="round")
        else:
            w = max(3, WID[i] * 0.12)
            AN.path(f"M{a[0]:.1f},{a[1]:.1f} Q{cx:.1f},{cy:.1f} {b[0]:.1f},{b[1]:.1f}",
                   f"Band pale {i+1}", fill=NONE, stroke="#FFF2C4", strokeWidth=w, opacity=50, cap="round")
# small spines along the back
for i in range(1, len(SPINE) - 5):
    (x, y), (nx, ny) = DORS[i], NRM[i]
    AN.path(f"M{x:.1f},{y:.1f} L{x + nx * 10 - ny * 4:.1f},{y + ny * 10 + nx * 4:.1f}",
           f"Back spine {i+1}", fill=NONE, stroke=INK, strokeWidth=3, opacity=70, cap="round")

# --- head + snout -----------------------------------------------------------------------
AN.path("M690,404 C730,398 770,394 800,390 C808,388 814,392 814,398 C814,404 808,408 800,408 "
       "C770,410 730,418 692,430 Z", "Snout", fill=SNOUT_GRAD, stroke=INK, strokeWidth=4)
AN.path("M700,408 C740,402 774,398 800,396", "Snout sheen", fill=NONE, stroke="#FFFAE0",
       strokeWidth=3, opacity=55, cap="round")
AN.path("M806,393 C810,396 810,402 806,404", "Mouth", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
AN.path("M628,416 C640,394 672,384 700,394 C712,402 712,426 698,436 C676,450 640,452 626,440 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
AN.shape("ellipse", "Head sheen", x=650, y=392, width=42, height=14, fill="#FFFFFF", opacity=25, stroke=NONE)
# eye: the one smooth jewel in the face
AN.shape("ellipse", "Eye ring", x=652, y=402, width=30, height=30, fill="#F6E4A0", opacity=60, stroke=NONE)
AN.shape("ellipse", "Eye", x=656, y=406, width=22, height=22, fill="#C88A2C", stroke=INK, strokeWidth=3)
AN.shape("ellipse", "Pupil", x=662, y=412, width=10, height=10, fill="#1A1206", stroke=NONE)
AN.shape("ellipse", "Eye glint", x=663, y=411, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
# eye stripes radiating back (seadragon facial lines)
for j, dd in enumerate(["M652,412 C642,410 634,412 626,418", "M654,426 C644,432 636,436 628,438",
                        "M680,410 C690,406 698,404 706,404"]):
    AN.path(dd, f"Face line {j+1}", fill=NONE, stroke="#8E5E1E", strokeWidth=3, opacity=55, cap="round")
# pectoral fin: tiny translucent fan behind the head
AN.path("M620,446 C606,452 600,468 606,480 C618,474 626,462 628,450 Z", "Pectoral fin",
       fill=FIN_GRAD, opacity=55, stroke="#C8A850", strokeWidth=3)

# --- near-side appendages, over the body -------------------------------------------------
appendage((652, 396), -70, 22, 52, "Head leaf", spread=26)
appendage(DORS[1], -100, 34, 70, "Neck leaf", n=5, spread=22)
appendage(DORS[4], -118, 44, 92, "Back leaf front", n=5, spread=22)
appendage(VENT[4], 100, 40, 88, "Belly leaf front", n=5, spread=22)
appendage(DORS[8], -140, 38, 80, "Back leaf rear", n=5, spread=22)
appendage(VENT[7], 128, 44, 92, "Belly leaf rear", n=5, spread=22)
appendage(VENT[11], 200, 26, 54, "Tail leaf 1")
appendage(DORS[12], -165, 22, 46, "Tail leaf 2", spread=28)
appendage(VENT[14], 135, 16, 34, "Tail leaf 3", spread=26)

# --- rim redrawn over the kelp roots so the edge stays crisp -------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#4A4418", strokeWidth=6)

# --- name ------------------------------------------------------------------------------------
d.text("LEAFY SEADRAGON", "Name", x=500, y=960, size=46, font="Virelai Sans",
       color="#F2E8B8", justify="center")

far_pt = max(EXTENT, key=lambda p: math.hypot(p[0] - CX, p[1] - CY))
print("animal extent: max r=%.1f at (%.0f,%.0f)" % (math.hypot(far_pt[0] - CX, far_pt[1] - CY), *far_pt))
xs, ys = [p[0] for p in EXTENT], [p[1] for p in EXTENT]
print("bbox x %.0f..%.0f  y %.0f..%.0f" % (min(xs), max(xs), min(ys), max(ys)))

d.finish("leafy-seadragon-V1R00")
