#!/usr/bin/env python3
"""Bergere armchair — furniture field plate V1R00. Near-side view with a
slight three-quarter from the front left: a Louis XV bergere with an arched
caned back in a carved gilt frame, caned side panels under padded
manchettes, a loose rose-silk squab cushion, a serpentine seat rail with a
central shell, and short gilt cabriole legs. Gilt plate, salon mood.
1000x1000. Gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420. The chair is modelled in 3D and drawn
with an oblique projection (affine, so Bezier control points project exactly)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Bergere Armchair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A180C"   # warm umber, never black


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [dict(offset=o, color=c, **({"opacity": a} if a is not None else {}))
                      for o, c, a in stops]}}


def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=o, color=c, **({"opacity": a} if a is not None else {})) for o, c, a in stops]}}


# --- projection: x right, y up, z back (pt) -----------------------------------------
# turned 26 deg so the near (left) side shows, seen from 12 deg above
CX, FY = 528, 768
TH, PH = math.radians(26), math.radians(12)
CT, ST, CP, SP = math.cos(TH), math.sin(TH), math.cos(PH), math.sin(PH)


def P(x, y, z):
    depth = x * ST + z * CT
    return (CX + x * CT - z * ST, FY - (y * CP + depth * SP))


BOUNDS = []


def note(*pts):
    BOUNDS.extend(pts)


def path3(ops):
    """ops: ('M', p) ('L', p) ('C', p1, p2, p3) ('Z',) with 3D points."""
    out = []
    for op in ops:
        k, pts = op[0], op[1:]
        xy = [P(*p) for p in pts]
        note(*xy)
        out.append(k + " ".join("%.1f,%.1f" % q for q in xy))
    return " ".join(out)


def Pback(u, v):
    """Back-plane map: (x, y) -> 3D on the raked back plane."""
    return P(u, v, 256 + (v - 170) * 0.10)


def Pside(x):
    """Side-plane map factory: (z, y) -> 3D on plane x = const."""
    return lambda z, y: P(x, y, z)


def path2(ops, mp):
    out = []
    for op in ops:
        k, pts = op[0], op[1:]
        xy = [mp(*p) for p in pts]
        note(*xy)
        out.append(k + " ".join("%.1f,%.1f" % q for q in xy))
    return " ".join(out)


# --- convex panel weave clipping ---------------------------------------------------
def poly_area(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] -
               poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly))) / 2


def clip_seg(p0, p1, poly):
    """Cyrus-Beck: clip segment to a convex polygon, return (a,b) or None."""
    sgn = 1 if poly_area(poly) > 0 else -1
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    t0, t1 = 0.0, 1.0
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        ex, ey = b[0] - a[0], b[1] - a[1]
        f0 = sgn * (ex * (p0[1] - a[1]) - ey * (p0[0] - a[0]))
        f1 = sgn * (ex * (p1[1] - a[1]) - ey * (p1[0] - a[0]))
        if f0 < 0 and f1 < 0:
            return None
        den = f0 - f1
        if abs(den) < 1e-9:
            continue
        t = f0 / den
        if f0 < 0:
            t0 = max(t0, t)
        elif f1 < 0:
            t1 = min(t1, t)
    if t1 - t0 < 0.02:
        return None
    return ((p0[0] + dx * t0, p0[1] + dy * t0), (p0[0] + dx * t1, p0[1] + dy * t1))


def weave(label, poly, mp, spacing=12.5, sw=2.3, color="#7A5220", op=52):
    """Hex weave: three line families clipped to the (convex) panel."""
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    span = math.hypot(max(xs) - min(xs), max(ys) - min(ys))
    k = 0
    for ang in (0.0, math.radians(58), -math.radians(58)):
        ux, uy = math.cos(ang), math.sin(ang)
        nx, ny = -uy, ux
        off = -span
        while off <= span:
            p0 = (cx + nx * off - ux * span, cy + ny * off - uy * span)
            p1 = (cx + nx * off + ux * span, cy + ny * off + uy * span)
            seg = clip_seg(p0, p1, poly)
            if seg:
                a, b = mp(*seg[0]), mp(*seg[1])
                note(a, b)
                d.path("M%.1f,%.1f L%.1f,%.1f" % (a + b), f"{label} {k+1}",
                       fill=NONE, stroke=color, strokeWidth=sw, opacity=op)
            k += 1
            off += spacing


def polyline(ops, n=14):
    """Flatten M/L/C/Z ops into a polygon for clipping."""
    pts, cur = [], None
    for op in ops:
        if op[0] == "M" or op[0] == "L":
            cur = op[1]
            pts.append(cur)
        elif op[0] == "C":
            p0 = cur
            for i in range(1, n + 1):
                t = i / n
                mt = 1 - t
                x = mt ** 3 * p0[0] + 3 * mt * mt * t * op[1][0] + \
                    3 * mt * t * t * op[2][0] + t ** 3 * op[3][0]
                y = mt ** 3 * p0[1] + 3 * mt * mt * t * op[1][1] + \
                    3 * mt * t * t * op[2][1] + t ** 3 * op[3][1]
                pts.append((x, y))
            cur = op[3]
    return pts


# --- palette -------------------------------------------------------------------------
BG_GRAD = lin(0, 0, 0, 1000, (0, "#1E140A", None), (1, "#070403", None))
PLATE_GRAD = rad((0, "#5A4324", None), (0.55, "#3A2812", None), (1, "#1D1207", None))
GILT = lin(0, 300, 0, 660, (0, "#E8C268", None), (0.45, "#B8862E", None), (1, "#7A5318", None))
GILT_DK = lin(0, 300, 0, 720, (0, "#A87830", None), (1, "#573A10", None))
GILT_HI = "#F4DE9A"
CANE = rad((0, "#F2D8A2", None), (0.6, "#D2AA60", None), (1, "#9E7434", None))
SILK_TOP = lin(0, 540, 0, 660, (0, "#EFB4A6", None), (0.55, "#C9796C", None), (1, "#9C5248", None))
SILK_FACE = lin(0, 620, 0, 720, (0, "#B06A5C", None), (1, "#6E3630", None))
SILK_PAD = lin(0, 480, 0, 560, (0, "#E4A89C", None), (1, "#A05A50", None))
WELT = "#F2CFC0"

# --- backdrop + plate ----------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#B08A48", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke="#140C05", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8C88A", strokeWidth=3, opacity=26)
# salon sconce glow, upper left
d.shape("ellipse", "Sconce glow", x=110, y=80, width=560, height=560,
        fill=rad((0, "#FFC27A", 0.32), (0.55, "#FFB060", 0.09), (1, "#FFB060", 0)), stroke=NONE)
# floor band closes on the disc's own arc
FYB = 700
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX + hw:.1f},{FYB} L{PCX - hw:.1f},{FYB} A420,420 0 0 0 {PCX + hw:.1f},{FYB} Z",
       "Floor", fill=lin(0, FYB, 0, 880, (0, "#38240F", 0), (0.4, "#2C1C0C", 0.55), (1, "#150D05", 0.85)),
       stroke=NONE)
# parquet seams + wainscot line
for i, yb in enumerate([744, 790, 838]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Parquet seam {i+1}",
           fill=NONE, stroke="#5A3C1E", strokeWidth=2, opacity=30)
h = math.sqrt(PR ** 2 - (520 - PCY) ** 2) - 6
d.path(f"M{PCX - h:.1f},520 L{PCX + h:.1f},520", "Wainscot rail",
       fill=NONE, stroke="#8A6234", strokeWidth=3, opacity=22)

# --- floor shadow ----------------------------------------------------------------------
sx, sy = P(0, 0, 150)
d.shape("ellipse", "Floor shadow", x=round(sx - 290), y=round(sy - 50), width=580, height=100,
        fill=rad((0, "#060301", 0.75), (0.7, "#060301", 0.35), (1, "#060301", 0)), stroke=NONE)

# --- legs: back pair first --------------------------------------------------------------
def leg(label, x, z, fill, front=True):
    """Short cabriole leg: knee swells toward the viewer, ankle pinches, pad foot."""
    tx, ty = P(x, 132, z)
    bx, by = P(x, 0, z)
    note((tx, ty), (bx, by))
    s = (1 if x > 0 else -1) if front else -(1 if x > 0 else -1)
    w0, w1 = 24, 12
    dpath = ("M%.1f,%.1f L%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f "
             "C%.1f,%.1f %.1f,%.1f %.1f,%.1f L%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f "
             "C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z") % (
        tx - w0 / 2, ty, tx + w0 / 2, ty,
        tx + w0 / 2 + s * 8, ty + 24, tx + w1 / 2 - s * 5, by - 24, bx + w1 / 2, by - 6,
        bx + w1 / 2 + 3, by - 2, bx + w1 / 2 + 3, by, bx + w1 / 2 + 2, by,
        bx - w1 / 2 - 2, by,
        bx - w1 / 2 - 3, by, bx - w1 / 2 - 3, by - 2, bx - w1 / 2, by - 6,
        tx - w1 / 2 - s * 5, by - 24, tx - w0 / 2 + s * 8, ty + 24, tx - w0 / 2, ty)
    d.path(dpath, label, fill=fill, stroke=INK, strokeWidth=3)
    d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
        tx - w0 / 2 + 6, ty + 4, tx - w0 / 2 + 8 + s * 5, ty + 24, tx - 2, by - 26, bx - 2, by - 8),
        label + " gloss", fill=NONE, stroke=GILT_HI, strokeWidth=3, opacity=45, cap="round")


leg("Leg back right", 160, 240, GILT_DK, front=False)
leg("Leg back left", -160, 240, GILT_DK, front=False)

# --- back frame + caned panel -----------------------------------------------------------
BACK_OUT = [("M", (-165, 172)), ("L", (-165, 335)),
            ("C", (-165, 412), (-95, 462), (0, 462)),
            ("C", (95, 462), (165, 412), (165, 335)),
            ("L", (165, 172)), ("Z",)]
BACK_IN = [("M", (-139, 196)), ("L", (-139, 335)),
           ("C", (-139, 394), (-78, 436), (0, 436)),
           ("C", (78, 436), (139, 394), (139, 335)),
           ("L", (139, 196)), ("Z",)]

# gilt frame (outer silhouette) — the back is thicker at the rail, ~14pt of depth
d.path(path2(BACK_OUT, Pback), "Back frame", fill=GILT, stroke=INK, strokeWidth=4)
# top edge of the crest rail seen from above: a thin gilt-dark crescent
crest_top = [("M", (-165, 335)), ("C", (-165, 412), (-95, 462), (0, 462)),
             ("C", (95, 462), (165, 412), (165, 335))]
d.path(path2(crest_top, lambda u, v: P(u, v, 256 + (v - 170) * 0.10 + 12)),
       "Crest top edge", fill=NONE, stroke="#6E4A16", strokeWidth=7, opacity=70, cap="round")
d.path(path2(crest_top, lambda u, v: P(u, v, 256 + (v - 170) * 0.10 + 4)),
       "Crest crown light", fill=NONE, stroke=GILT_HI, strokeWidth=4, opacity=60, cap="round")

# cane panel + weave + molding + sheen
d.path(path2(BACK_IN, Pback), "Back cane", fill=CANE, stroke="#5C3C14", strokeWidth=3)
back_poly = polyline(BACK_IN)
weave("Back weave", back_poly, Pback, spacing=13)
# gilt molding line just inside the frame
d.path(path2(BACK_IN, Pback), "Back molding", fill=NONE, stroke=GILT_HI, strokeWidth=4, opacity=55)
# lamp sheen on the cane's upper left
d.path(path2([("M", (-120, 300)), ("C", (-120, 380), (-60, 420), (0, 424)),
              ("C", (30, 426), (60, 418), (80, 404)), ("L", (60, 320)), ("Z",)],
             Pback),
       "Back cane sheen", fill=rad((0, "#FFF0C8", 0.30), (1, "#FFF0C8", 0)), stroke=NONE)

# crest carving: a small rocaille shell at the apex
cx0, cy0 = Pback(0, 464)
note((cx0, cy0))
d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" % (
    cx0 - 22, cy0 + 6, cx0 - 20, cy0 - 14, cx0 - 8, cy0 - 20, cx0, cy0 - 20,
    cx0 + 8, cy0 - 20, cx0 + 20, cy0 - 14, cx0 + 22, cy0 + 6),
    "Crest shell", fill=GILT, stroke=INK, strokeWidth=2.5)
for k, dx in enumerate((-13, -6.5, 0, 6.5, 13)):
    d.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (cx0 + dx, cy0 + 4, cx0 + dx * 0.4, cy0 - 8, cx0, cy0 - 17),
           f"Crest rib {k+1}", fill=NONE, stroke="#6E4A16", strokeWidth=1.6, opacity=70, cap="round")

# --- far (right) side: caned panel + arm ------------------------------------------------
SIDE_PANEL = [(78, 176), (236, 176), (236, 244), (88, 244)]
sideR = Pside(158)
d.path(path2([("M", p) for p in SIDE_PANEL[:1]] + [("L", p) for p in SIDE_PANEL[1:]] + [("Z",)],
             sideR), "Right side cane", fill=CANE, stroke="#5C3C14", strokeWidth=3)
weave("Right weave", SIDE_PANEL, sideR, spacing=12, sw=2.1, op=48)
# frame sticks round the right panel
for lab, a, b in (("rail", (80, 170), (238, 170)), ("stile", (240, 172), (240, 246)),
                  ("post", (74, 172), (88, 246))):
    pa, pb = sideR(*a), sideR(*b)
    note(pa, pb)
    d.path("M%.1f,%.1f L%.1f,%.1f" % (pa + pb), f"Right side {lab}",
           fill=NONE, stroke="#8A5E1E", strokeWidth=8, cap="round")

# right arm: gilt rail + crowned silk pad (inner face + top strip shown)
RAIL = [("M", (60, 250)), ("L", (242, 250)), ("L", (242, 234)), ("L", (68, 234)),
        ("C", (58, 234), (52, 240), (54, 248)), ("Z",)]
PAD = [("M", (66, 250)),
       ("C", (54, 250), (48, 258), (50, 265)),
       ("C", (52, 272), (60, 276), (70, 276)),
       ("C", (110, 281), (170, 281), (216, 274)),
       ("C", (230, 272), (238, 266), (240, 256)),
       ("L", (240, 250)), ("Z",)]
PAD_TOP = [("M", (70, 276)), ("C", (110, 281), (170, 281), (216, 274)),
           ("C", (230, 272), (238, 266), (240, 256))]
CONSOLE = [("M", (58, 236)), ("C", (36, 228), (28, 204), (42, 186)),
           ("C", (50, 176), (64, 171), (80, 171)), ("L", (84, 176)),
           ("C", (70, 178), (58, 184), (52, 196)), ("C", (45, 210), (50, 228), (68, 238)), ("Z",)]


def pad_top_strip(x_in, x_out, label, col):
    ops = [("M", (x_in, 276, 70)), ("C", (x_in, 281, 110), (x_in, 281, 170), (x_in, 274, 216)),
           ("C", (x_in, 272, 230), (x_in, 266, 238), (x_in, 256, 240)),
           ("L", (x_out, 256, 240)),
           ("C", (x_out, 266, 238), (x_out, 272, 230), (x_out, 274, 216)),
           ("C", (x_out, 281, 170), (x_out, 281, 110), (x_out, 275, 70)), ("Z",)]
    d.path(path3(ops), label, fill=col, stroke=INK, strokeWidth=3)


def pad_cap(x0, x1, label):
    """Rounded front face of the manchette pad in the plane z = 52."""
    z = 52
    ops = [("M", (x0, 258, z)), ("L", (x0, 268, z)),
           ("C", (x0, 272, z), (x0 + 4, 275, z), (x0 + 8, 275, z)),
           ("L", (x1 - 8, 275, z)),
           ("C", (x1 - 4, 275, z), (x1, 272, z), (x1, 268, z)),
           ("L", (x1, 258, z)),
           ("C", (x1, 254, z), (x1 - 4, 252, z), (x1 - 8, 252, z)),
           ("L", (x0 + 8, 252, z)),
           ("C", (x0 + 4, 252, z), (x0, 254, z), (x0, 258, z)), ("Z",)]
    d.path(path3(ops), label,
           fill=lin(0, 500, 0, 560, (0, "#E8AFA4", None), (1, "#A85E52", None)),
           stroke=INK, strokeWidth=3)


# far arm: console peeking under the pad front, rail inner face, pad inner + top
d.path(path2(CONSOLE, Pside(162)), "Right console", fill=GILT_DK, stroke=INK, strokeWidth=3)
d.path(path2(RAIL, Pside(160)), "Right arm rail", fill=GILT_DK, stroke=INK, strokeWidth=3)
d.path(path2(PAD, Pside(138)), "Right manchette inner",
       fill=lin(0, 480, 0, 560, (0, "#D8948A", None), (1, "#9C5A50", None)),
       stroke=INK, strokeWidth=3)
pad_top_strip(138, 208, "Right manchette top", SILK_PAD)
d.path(path2([("M", (80, 268)), ("L", (200, 274))], Pside(141)),
       "Right manchette welt", fill=NONE, stroke=WELT, strokeWidth=2.5, opacity=50, cap="round")

# --- seat deck hint behind the cushion ---------------------------------------------------
d.path(path3([("M", (-150, 172, 240)), ("L", (150, 172, 240)), ("L", (150, 186, 240)),
              ("L", (-150, 186, 240)), ("Z",)]), "Seat back rail", fill=GILT_DK, stroke=INK, strokeWidth=3)

# --- loose squab cushion ------------------------------------------------------------------
# top face: front edge sags a touch at centre; back corners tuck under the manchettes
cush_top = [("M", (-146, 196, 246)), ("L", (146, 196, 246)),
            ("L", (150, 208, 60)), ("C", (120, 216, 8), (-120, 216, 8), (-150, 208, 60)), ("Z",)]
d.path(path3(cush_top), "Cushion top", fill=SILK_TOP, stroke=INK, strokeWidth=3.5)
# front face: a soft bow over the rail
cush_front = [("M", (-150, 208, 60)), ("C", (-120, 216, 8), (120, 216, 8), (150, 208, 60)),
              ("L", (152, 186, 20)), ("C", (100, 172, 4), (-100, 172, 4), (-152, 186, 20)), ("Z",)]
d.path(path3(cush_front), "Cushion front", fill=SILK_FACE, stroke=INK, strokeWidth=3.5)
# welt cord along the top front edge + sit sheen + creases
d.path(path3([("M", (-150, 209, 58)), ("C", (-120, 217, 7), (120, 217, 7), (150, 209, 58))]),
       "Cushion welt", fill=NONE, stroke=WELT, strokeWidth=3, opacity=70, cap="round")
d.path(path3([("M", (-110, 206, 150)), ("C", (-40, 214, 170), (50, 214, 170), (110, 204, 150))]),
       "Cushion sheen", fill=NONE, stroke="#F8D8CC", strokeWidth=14, opacity=16, cap="round")
for lab, x in (("L", -132), ("R", 132)):
    d.path(path3([("M", (x, 210, 55)), ("C", (x * 0.98, 200, 34), (x * 0.96, 190, 22), (x * 0.95, 182, 14))]),
           f"Cushion crease {lab}", fill=NONE, stroke="#6E3630", strokeWidth=3, opacity=45, cap="round")

# --- seat rail: serpentine apron + central shell ------------------------------------------
rail_top = 176
d.path(path3([("M", (-172, rail_top, 0)), ("L", (172, rail_top, 0)), ("L", (172, 142, 0)),
              ("C", (100, 122, 0), (-100, 122, 0), (-172, 142, 0)), ("Z",)]),
       "Apron", fill=GILT, stroke=INK, strokeWidth=4)
# apron moulding line + shade under the cushion's overhang
d.path(path3([("M", (-168, rail_top - 4, 1)), ("L", (168, rail_top - 4, 1))]),
       "Apron moulding", fill=NONE, stroke=GILT_HI, strokeWidth=3, opacity=55, cap="round")
d.path(path3([("M", (-170, rail_top, 0)), ("L", (170, rail_top, 0)), ("L", (170, rail_top - 14, 0)),
              ("L", (-170, rail_top - 14, 0)), ("Z",)]), "Apron top shade",
       fill="#1A0E04", opacity=26, stroke=NONE)
# shell cartouche at the rail's centre
shx, shy = P(0, 138, 0)
note((shx, shy))
d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f Z" % (
    shx - 20, shy + 2, shx - 16, shy - 12, shx - 7, shy - 16, shx, shy - 16,
    shx + 7, shy - 16, shx + 16, shy - 12, shx + 20, shy + 2),
    "Rail shell", fill=GILT_DK, stroke=INK, strokeWidth=2)
for k, dx in enumerate((-11, -5.5, 0, 5.5, 11)):
    d.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (shx + dx, shy, shx + dx * 0.4, shy - 6, shx, shy - 14),
           f"Rail rib {k+1}", fill=NONE, stroke=GILT_HI, strokeWidth=1.5, opacity=65, cap="round")

# front legs last: knees kick toward the viewer
leg("Leg front right", 160, 10, GILT)
leg("Leg front left", -160, 10, GILT)

# --- near (left) side: caned panel over the seat -----------------------------------------
sideL = Pside(-158)
d.path(path2([("M", SIDE_PANEL[0])] + [("L", p) for p in SIDE_PANEL[1:]] + [("Z",)], sideL),
       "Left side cane", fill=CANE, stroke="#5C3C14", strokeWidth=3)
weave("Left weave", SIDE_PANEL, sideL, spacing=12, sw=2.1, op=52)
for lab, a, b in (("rail", (80, 170), (238, 170)), ("stile", (240, 172), (240, 246)),
                  ("post", (74, 172), (88, 246))):
    pa, pb = sideL(*a), sideL(*b)
    note(pa, pb)
    d.path("M%.1f,%.1f L%.1f,%.1f" % (pa + pb), f"Left side {lab}",
           fill=NONE, stroke="#8A5E1E", strokeWidth=8, cap="round")
    d.path("M%.1f,%.1f L%.1f,%.1f" % (pa[0], pa[1] - 3, pb[0], pb[1] - 3),
           f"Left side {lab} light", fill=NONE, stroke=GILT_HI, strokeWidth=2.5, opacity=45, cap="round")

# near arm: gilt rail outer face, console scroll, crowned pad, rounded front cap
d.path(path2(RAIL, Pside(-206)), "Left arm rail", fill=GILT, stroke=INK, strokeWidth=3)
d.path(path2([("M", (70, 247)), ("L", (238, 247))], Pside(-207)),
       "Left rail light", fill=NONE, stroke=GILT_HI, strokeWidth=2.5, opacity=55, cap="round")
d.path(path2(CONSOLE, Pside(-200)), "Left console", fill=GILT, stroke=INK, strokeWidth=3)
d.path(path2([("M", (60, 232)), ("C", (42, 224), (36, 204), (46, 190))], Pside(-201)),
       "Left console light", fill=NONE, stroke=GILT_HI, strokeWidth=3, opacity=55, cap="round")
# volute where the console meets the rail front
vx, vy = P(-201, 240, 56)
d.shape("ellipse", "Left volute", x=round(vx - 9), y=round(vy - 9), width=18, height=18,
        fill=rad((0, "#F4DE9A", None), (0.6, "#B8862E", None), (1, "#6E4A16", None)),
        stroke=INK, strokeWidth=2.5)

d.path(path2(PAD, Pside(-208)), "Left manchette outer", fill=SILK_FACE, stroke=INK, strokeWidth=3)
pad_top_strip(-138, -208, "Left manchette top", SILK_PAD)
d.path(path2([("M", (80, 269)), ("L", (200, 275))], Pside(-205)),
       "Left manchette welt", fill=NONE, stroke=WELT, strokeWidth=2.5, opacity=55, cap="round")
d.path(path2([("M", (90, 275)), ("L", (190, 279))], Pside(-200)),
       "Left manchette sheen", fill=NONE, stroke="#F8D8CC", strokeWidth=7, opacity=22, cap="round")

# contact shadows under the front feet
for x, z in ((160, 10), (-160, 10), (160, 240), (-160, 240)):
    fx, fy = P(x, 0, z)
    d.shape("ellipse", f"Foot shadow {x},{z}", x=round(fx - 15), y=round(fy - 3),
            width=30, height=9, fill=rad((0, "#000000", 0.5), (1, "#000000", 0)), stroke=NONE)

# --- sanity: whole chair well inside the disc ------------------------------------------------
worst = min(PR - math.hypot(x - PCX, y - PCY) for x, y in BOUNDS)
xs, ys = [b[0] for b in BOUNDS], [b[1] for b in BOUNDS]
print("bounds x %.0f..%.0f y %.0f..%.0f" % (min(xs), max(xs), min(ys), max(ys)))
print("min clearance to rim: %.1f" % worst)
assert worst > 20, worst

# --- captions ---------------------------------------------------------------------------------
def find(node, oid):
    if isinstance(node, dict):
        if node.get("id") == oid and "bounds" in node:
            return node["bounds"]
        for v in node.values():
            r = find(v, oid)
            if r:
                return r
    elif isinstance(node, list):
        for v in node:
            r = find(v, oid)
            if r:
                return r
    return None


def caption(name, mats):
    n = d.text(name, "Name", x=500, y=934, size=56, font="Virelai Sans",
               color="#F4E4C4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#CCA888", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=260)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "materials")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" % (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "materials":
            assert b["width"] <= 760, b["width"]


caption("BERGERE ARMCHAIR", "GILT BEECH · CANE · SILK")
d.finish("bergere-armchair-V1R00")
