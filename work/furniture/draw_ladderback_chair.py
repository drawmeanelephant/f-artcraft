#!/usr/bin/env python3
"""Ladderback chair — furniture field plate V1R00. Near-side view with a
slight three-quarter from the front left: a country ladderback with turned
ash posts and ball finials, four arched slats, a woven rush seat in a
flared trapezoid, turned stretchers and pad feet. Warm ember light from the
right; hearth mood. 1000x1000.
Gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420. The chair is modelled in 3D and drawn
with an oblique projection (affine, so Bezier control points project exactly)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Ladderback Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241408"   # warm umber, never black


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [dict(offset=o, color=c, **({"opacity": a} if a is not None else {}))
                      for o, c, a in stops]}}


def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=o, color=c, **({"opacity": a} if a is not None else {})) for o, c, a in stops]}}


def smooth(pts, closed=False):
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


# --- projection: x right, y up, z back (pt) -----------------------------------------
CX, FY = 560, 772
TH, PH = math.radians(26), math.radians(12)
CT, ST, CP, SP = math.cos(TH), math.sin(TH), math.cos(PH), math.sin(PH)


def P(x, y, z):
    depth = x * ST + z * CT
    return (CX + x * CT - z * ST, FY - (y * CP + depth * SP))


BOUNDS = []


def note(*pts):
    BOUNDS.extend(pts)


def path3(ops):
    out = []
    for op in ops:
        k, pts = op[0], op[1:]
        xy = [P(*p) for p in pts]
        note(*xy)
        out.append(k + " ".join("%.1f,%.1f" % q for q in xy))
    return " ".join(out)


def path2(ops, mp):
    out = []
    for op in ops:
        k, pts = op[0], op[1:]
        xy = [mp(*p) for p in pts]
        note(*xy)
        out.append(k + " ".join("%.1f,%.1f" % q for q in xy))
    return " ".join(out)


# --- convex clipping (Cyrus-Beck) ----------------------------------------------------
def poly_area(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] -
               poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly))) / 2


def clip_seg(p0, p1, poly):
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


def grid_weave(label, poly, mp, spx, spz, color="#7A5A28", sw=3.4, op=50):
    """Rush seat: two families of strands clipped to the seat trapezoid.
    poly = [(x,z)...] in seat-plane coords."""
    xs = [p[0] for p in poly]
    zs = [p[1] for p in poly]
    k = 0
    x = min(xs) - 4
    while x <= max(xs) + 4:
        seg = clip_seg((x, min(zs) - 4), (x, max(zs) + 4), poly)
        if seg:
            a, b = mp(*seg[0]), mp(*seg[1])
            note(a, b)
            d.path("M%.1f,%.1f L%.1f,%.1f" % (a + b), f"{label} v{k+1}",
                   fill=NONE, stroke=color, strokeWidth=sw, opacity=op)
        k += 1
        x += spx
    k = 0
    z = min(zs) - 4
    while z <= max(zs) + 4:
        seg = clip_seg((min(xs) - 4, z), (max(xs) + 4, z), poly)
        if seg:
            a, b = mp(*seg[0]), mp(*seg[1])
            d.path("M%.1f,%.1f L%.1f,%.1f" % (a + b), f"{label} h{k+1}",
                   fill=NONE, stroke=color, strokeWidth=sw, opacity=op)
        k += 1
        z += spz


# --- palette --------------------------------------------------------------------------
BG_GRAD = lin(0, 0, 0, 1000, (0, "#1B1209", None), (1, "#070403", None))
PLATE_GRAD = rad((0, "#54401F", None), (0.55, "#35240F", None), (1, "#1B1106", None))
ASH = lin(0, 280, 0, 780, (0, "#C09458", None), (0.5, "#8A5E2E", None), (1, "#553713", None))
ASH_DK = lin(0, 280, 0, 780, (0, "#8A6234", None), (1, "#422A10", None))
SLAT = lin(300, 300, 720, 480, (0, "#D2A868", None), (1, "#96682E", None))
ASH_HI = "#E8C88A"
RUSH = rad((0, "#E2C48C", None), (0.6, "#B89452", None), (1, "#82612E", None))

# --- backdrop + plate ------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#B08A48", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke="#140C05", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8C88A", strokeWidth=3, opacity=26)
# hearth ember pool low on the right + cool lamp from the upper left
d.shape("ellipse", "Ember glow", x=500, y=540, width=440, height=300,
        fill=rad((0, "#FF8A3C", 0.30), (0.55, "#C85A20", 0.10), (1, "#C85A20", 0)), stroke=NONE)
d.shape("ellipse", "Lamp glow", x=110, y=80, width=520, height=520,
        fill=rad((0, "#FFC27A", 0.26), (0.55, "#FFB060", 0.07), (1, "#FFB060", 0)), stroke=NONE)
# floor band closes on the disc's own arc
FYB = 705
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX + hw:.1f},{FYB} L{PCX - hw:.1f},{FYB} A420,420 0 0 0 {PCX + hw:.1f},{FYB} Z",
       "Floor", fill=lin(0, FYB, 0, 880, (0, "#3A2812", 0), (0.4, "#2C1C0C", 0.55), (1, "#150D05", 0.85)),
       stroke=NONE)
for i, yb in enumerate([748, 792, 840]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Board seam {i+1}",
           fill=NONE, stroke="#5A3C1E", strokeWidth=2, opacity=30)
# hearth stones at the right edge of the floor (kept inside the disc arc)
for i, (hx_, hy_, hw_) in enumerate([(700, 716, 44), (678, 748, 36), (748, 706, 30)]):
    note((hx_, hy_), (hx_ + hw_, hy_ + 26))
    d.path(f"M{hx_},{hy_} L{hx_ + hw_},{hy_} L{hx_ + hw_ - 8},{hy_ + 26} L{hx_ + 6},{hy_ + 26} Z",
           f"Hearth stone {i+1}", fill="#3A2812", stroke="#1A0E04", strokeWidth=2, opacity=80)
# ember dots among the stones
for i, (ex, ey, ew) in enumerate([(706, 730, 8), (730, 748, 7), (688, 738, 6), (750, 714, 8), (714, 756, 6)]):
    note((ex, ey), (ex + ew, ey + ew))
    d.shape("ellipse", f"Ember {i+1}", x=ex, y=ey, width=ew, height=ew,
            fill=rad((0, "#FFCF7A", None), (0.5, "#FF7A2E", None), (1, "#8A2E08", None)), stroke=NONE)

# --- floor shadow ----------------------------------------------------------------------
sx, sy = P(0, 0, 140)
d.shape("ellipse", "Floor shadow", x=round(sx - 240), y=round(sy - 44), width=480, height=88,
        fill=rad((0, "#060301", 0.72), (0.7, "#060301", 0.32), (1, "#060301", 0)), stroke=NONE)

# --- geometry ---------------------------------------------------------------------------
# rear posts rake back: z(y) at the post plane
POST_X = 140
def zb(y):
    return 244 + y * 0.058

# back stretcher first (deepest)
def rod(label, a, b, w, col=ASH_DK, hi=ASH_HI, hiop=40):
    """Round rung between 3D points: stroked line + a thinner light line."""
    A, B = P(*a), P(*b)
    note(A, B)
    d.path("M%.1f,%.1f L%.1f,%.1f" % (A + B), label, fill=NONE,
           stroke=col, strokeWidth=w, cap="round")
    mx = (A[0] + B[0]) / 2
    d.path("M%.1f,%.1f L%.1f,%.1f" % (A[0] * 0.7 + mx * 0.3, A[1] - w * 0.28,
                                      B[0] * 0.7 + mx * 0.3, B[1] - w * 0.28),
           label + " light", fill=NONE, stroke=hi, strokeWidth=max(1.6, w * 0.3),
           opacity=hiop, cap="round")


rod("Back stretcher", (-POST_X, 96, 246), (POST_X, 96, 246), 10)

# slats between the posts, arched; drawn before the posts so ends tuck in
SLATS = [(258, 284), (308, 334), (358, 384), (410, 436)]
for i, (y0, y1) in enumerate(SLATS):
    ym = (y0 + y1) / 2
    def slat_map(u, v, _y0=y0, _y1=y1):
        return P(u, v, zb(v) + 2)
    slat = [("M", (-143, y0 + 3)),
            ("C", (-70, y0 - 1), (70, y0 - 1), (143, y0 + 3)),
            ("L", (143, y1 - 3)),
            ("C", (70, y1 + 9), (-70, y1 + 9), (-143, y1 - 3)),
            ("Z",)]
    d.path(path2(slat, slat_map), f"Slat {i+1}", fill=SLAT, stroke=INK, strokeWidth=3)
    # lower-edge shade makes each slat read as a curved board
    d.path(path2([("M", (-138, y0 + 5)), ("C", (-70, y0 + 1), (70, y0 + 1), (138, y0 + 5))], slat_map),
           f"Slat {i+1} shade", fill=NONE, stroke="#553713", strokeWidth=3, opacity=45, cap="round")
    d.path(path2([("M", (-130, y1 - 4)), ("C", (-70, y1 + 4), (70, y1 + 4), (130, y1 - 4))], slat_map),
           f"Slat {i+1} light", fill=NONE, stroke=ASH_HI, strokeWidth=2.5, opacity=45, cap="round")

# rear posts: turned profile up the whole height, ball finial on top
def turned(label, x, profile, fill, sw=3):
    """profile: [(y, halfwidth)...] bottom -> top; silhouette via smooth()."""
    L = [P(x - w, y, zb(y)) for y, w in profile]
    R = [P(x + w, y, zb(y)) for y, w in reversed(profile)]
    pts = L + R
    d.path(smooth(pts, closed=True), label, fill=fill, stroke=INK, strokeWidth=sw)
    note(*pts)
    mid = [P(x - w * 0.35, y, zb(y)) for y, w in profile]
    d.path(smooth(mid), label + " light", fill=NONE, stroke=ASH_HI,
           strokeWidth=2.5, opacity=30, cap="round")


REAR_POST = [(0, 11), (8, 14), (15, 10), (30, 9), (60, 8.5), (88, 10),
             (95, 13), (101, 9), (140, 9), (178, 11), (188, 14), (196, 9.5),
             (250, 9), (300, 8.5), (350, 8.5), (410, 9), (432, 10),
             (440, 15), (447, 17), (454, 15), (461, 9), (467, 4)]
turned("Rear post R", POST_X, REAR_POST, ASH_DK)
turned("Rear post L", -POST_X, REAR_POST, ASH)

# side stretchers: far one (right) is deeper, draw it first
rod("Side stretcher R", (POST_X - 4, 92, 30), (POST_X - 4, 92, 238), 10)
rod("Side stretcher L", (-POST_X + 4, 92, 30), (-POST_X + 4, 92, 238), 10)

# --- rush seat -----------------------------------------------------------------------------
# rails: front band + two side bands (the rush wraps over them)
d.path(path3([("M", (-136, 186, 14)), ("L", (136, 186, 14)), ("L", (136, 168, 14)),
              ("L", (-136, 168, 14)), ("Z",)]), "Seat rail front", fill=ASH, stroke=INK, strokeWidth=3)
d.path(path3([("M", (140, 186, 16)), ("L", (128, 186, 240)), ("L", (128, 168, 240)),
              ("L", (140, 168, 16)), ("Z",)]), "Seat rail right", fill=ASH_DK, stroke=INK, strokeWidth=3)
d.path(path3([("M", (-140, 186, 16)), ("L", (-128, 186, 240)), ("L", (-128, 168, 240)),
              ("L", (-140, 168, 16)), ("Z",)]), "Seat rail left", fill=ASH, stroke=INK, strokeWidth=3)
d.path(path3([("M", (-134, 188, 16)), ("L", (134, 188, 16))]),
       "Seat rail lip", fill=NONE, stroke=ASH_HI, strokeWidth=3, opacity=55, cap="round")

# rush panel: trapezoid flaring to the front, slight sag under the weave
seat_poly = [(-130, 22), (130, 22), (124, 236), (-124, 236)]
seat_map = lambda x, z: P(x, 183 - 3 * math.sin(math.pi * (x / 260 + 0.5)) , z)
d.path(path2([("M", seat_poly[0])] + [("L", p) for p in seat_poly[1:]] + [("Z",)], seat_map),
       "Rush seat", fill=RUSH, stroke="#4E3410", strokeWidth=3)
grid_weave("Rush", seat_poly, seat_map, 11, 11)
# sheen + front-edge wrap shade
d.path(path2([("M", (-100, 60)), ("C", (-40, 48), (40, 48), (100, 64))], seat_map),
       "Rush sheen", fill=NONE, stroke="#FFF0C8", strokeWidth=16, opacity=14, cap="round")
d.path(path2([("M", (-128, 30)), ("L", (128, 30))], seat_map),
       "Rush front wrap", fill=NONE, stroke="#4E3410", strokeWidth=5, opacity=40, cap="round")

# front stretcher: bigger turned rung with a central swell
rod("Front stretcher", (-128, 108, 18), (128, 108, 18), 13, col=ASH)
fx, fy = P(0, 108, 18)
d.shape("ellipse", "Front stretcher swell", x=round(fx - 17), y=round(fy - 9), width=34, height=18,
        fill=lin(fx - 17, 0, fx + 17, 0, (0, "#8A5E2E", None), (0.5, "#C09458", None), (1, "#553713", None)),
        stroke=INK, strokeWidth=2.5)

# front legs: short turned posts with pad feet
FRONT_LEG = [(0, 8), (6, 13), (13, 10), (26, 9), (55, 8.5), (80, 9),
             (92, 12), (100, 9), (140, 9.5), (170, 10), (178, 11), (182, 8)]
def front_leg(label, x, fill):
    Lp = [P(x - w, y, 16) for y, w in FRONT_LEG]
    Rp = [P(x + w, y, 16) for y, w in reversed(FRONT_LEG)]
    pts = Lp + Rp
    d.path(smooth(pts, closed=True), label, fill=fill, stroke=INK, strokeWidth=3)
    note(*pts)
    mid = [P(x - w * 0.35, y, 16) for y, w in FRONT_LEG]
    d.path(smooth(mid), label + " light", fill=NONE, stroke=ASH_HI,
           strokeWidth=2.5, opacity=30, cap="round")


front_leg("Front leg R", 130, ASH_DK)
front_leg("Front leg L", -130, ASH)

# ember rim-light on the right-hand edges
for lab, pts3 in (("post", [(POST_X + 8, y, zb(y)) for y in (200, 300, 400, 430)]),
                  ("leg", [(138, y, 16) for y in (30, 90, 150)])):
    edge = [P(*p) for p in pts3]
    d.path(smooth(edge), f"Ember rim {lab}", fill=NONE, stroke="#FF9A50",
           strokeWidth=3, opacity=30, cap="round")

# contact shadows
for x, z, w in ((130, 16, 30), (-130, 16, 30), (POST_X, 244, 30), (-POST_X, 244, 30)):
    fx2, fy2 = P(x, 0, z)
    d.shape("ellipse", f"Foot shadow {x}", x=round(fx2 - w / 2), y=round(fy2 - 3),
            width=w, height=9, fill=rad((0, "#000000", 0.5), (1, "#000000", 0)), stroke=NONE)

# --- sanity: whole chair well inside the disc ---------------------------------------------
worst = min(PR - math.hypot(x - PCX, y - PCY) for x, y in BOUNDS)
xs, ys = [b[0] for b in BOUNDS], [b[1] for b in BOUNDS]
print("bounds x %.0f..%.0f y %.0f..%.0f" % (min(xs), max(xs), min(ys), max(ys)))
print("min clearance to rim: %.1f" % worst)
assert worst > 20, worst

# --- captions ------------------------------------------------------------------------------
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


caption("LADDERBACK CHAIR", "ASH · RUSH")
d.finish("ladderback-chair-V1R00")
