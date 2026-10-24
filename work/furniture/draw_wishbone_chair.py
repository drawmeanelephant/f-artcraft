#!/usr/bin/env python3
"""Wishbone chair — furniture field plate V1R00. Near-side view with a slight
three-quarter from the front left: a beech chair with a steam-bent horseshoe
rail sweeping around the back into low arms, the Y-shaped splat beneath it,
a woven paper-cord seat and splayed tapered legs on rungs. Pale nordic wood
on a warm grey plate. 1000x1000. Modelled in 3D (inches) and projected with a
fixed yaw + pitch so every joint lines up.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Wishbone Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2E2013"   # warm umber, not black
EXTENT = []       # every projected point of the chair, checked against the rim


def stops(*pairs):
    out = []
    for p in pairs:
        s = {"offset": p[0], "color": p[1]}
        if len(p) > 2:
            s["opacity"] = p[2]
        out.append(s)
    return out


def lin(a, b, *pairs):
    return {"gradient": {"kind": "linear", "start": [round(a[0], 1), round(a[1], 1)],
                         "end": [round(b[0], 1), round(b[1], 1)], "stops": stops(*pairs)}}


def rad(*pairs):
    return {"gradient": {"kind": "radial", "stops": stops(*pairs)}}


def smooth(pts, closed=False, move=True):
    """Catmull-Rom through pts as cubic Beziers."""
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = ("M%.1f,%.1f" if move else "L%.1f,%.1f") % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


# --- projection -------------------------------------------------------------
# x = chair's right, y = up, z = toward the back. Yaw swings the chair's right
# side toward the viewer; pitch looks down onto the seat.
YAW, PITCH = math.radians(27), math.radians(13)
S, OX, OY = 17.6, 506.0, 766.0


def P(x, y, z):
    c, s = math.cos(YAW), math.sin(YAW)
    xr, zr = x * c + z * s, -x * s + z * c
    p = (OX + S * xr, OY - S * (y * math.cos(PITCH) + zr * math.sin(PITCH)))
    EXTENT.append(p)
    return p


def depth(x, y, z):
    return -x * math.sin(YAW) + z * math.cos(YAW)


# --- convex clipping (Cyrus-Beck) --------------------------------------------
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


def grid_weave(label, poly, mp, spx, spz, color, sw=3.2, op=48):
    """Paper-cord weave: two strand families clipped to the seat trapezoid.
    poly = [(x,z)...] in seat-plane coords; mp maps (x,z) -> screen."""
    xs = [p[0] for p in poly]
    zs = [p[1] for p in poly]
    k = 0
    x = min(xs) - 4
    while x <= max(xs) + 4:
        seg = clip_seg((x, min(zs) - 4), (x, max(zs) + 4), poly)
        if seg:
            a, b = mp(*seg[0]), mp(*seg[1])
            EXTENT.extend([a, b])
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
            EXTENT.extend([a, b])
            d.path("M%.1f,%.1f L%.1f,%.1f" % (a + b), f"{label} h{k+1}",
                   fill=NONE, stroke=color, strokeWidth=sw, opacity=op)
        k += 1
        z += spz


# --- palette -------------------------------------------------------------------
BEECH = lin((0, 220), (0, 780), (0, "#EACB92"), (0.5, "#C79B5E"), (1, "#8A6132"))
BEECH_DK = lin((0, 220), (0, 780), (0, "#B98D52"), (1, "#6E4A24"))
BEECH_HI = "#F6E2B4"
CORD = "#DCC8A0"

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#171310"), (1, "#070606")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#6A5A48", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#4C4238"), (0.6, "#332B24"), (1, "#1B1612")),
        stroke="#0E0B09", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4CFA8", strokeWidth=3, opacity=26)
# soft window light behind the chair, slightly left of centre
d.shape("ellipse", "Back glow", x=170, y=110, width=560, height=560,
        fill=rad((0, "#F0DCB8", 26), (0.55, "#C8A878", 9), (1, "#8A6A46", 0)), stroke=NONE)

# floor: a band that closes on the disc's own arc
FY = 700
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#55483A", 32), (1, "#161210", 72)), stroke=NONE)
for i, y in enumerate([738, 784, 836]):
    hw = math.sqrt(PR ** 2 - (y - PCY) ** 2) - 10
    d.path(f"M{PCX - hw:.1f},{y} L{PCX + hw:.1f},{y}", f"Floorboard seam {i+1}",
           fill=NONE, stroke="#241C14", strokeWidth=2, opacity=40)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E2CCA6", strokeWidth=2, opacity=20)

# --- geometry ---------------------------------------------------------------------
SEAT_Y, SEAT_T = 17.5, 1.4
# seat trapezoid in plan: front wide, back narrower (cord wraps the four rails)
SEAT = [(-8.9, -7.2), (8.9, -7.2), (7.9, 6.6), (-7.9, 6.6)]   # FL FR BR BL


def seat_map(x, z):
    return P(x, SEAT_Y - 0.35 * math.sin(math.pi * ((z + 7.2) / 13.8)), z)


# shadow under the chair, kept well inside the disc
d.shape("ellipse", "Chair shadow", x=286, y=724, width=448, height=104,
        fill=rad((0, "#050403", 68), (0.6, "#050403", 32), (1, "#050403", 0)), stroke=NONE)


def along(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def turned(name, a, b, profile, ink=2.2, fill_lo="#8A6132", fill_hi="#F2D9A4"):
    """A tapered round member between 3D points a and b; profile = [(t, r in)]."""
    A, B = P(*a), P(*b)
    dx, dy = B[0] - A[0], B[1] - A[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    left, right = [], []
    for t, r in profile:
        cx, cy = A[0] + dx * t, A[1] + dy * t
        w = r * S
        left.append((cx + nx * w, cy + ny * w))
        right.append((cx - nx * w, cy - ny * w))
    path = smooth(left) + " " + smooth(right[::-1], move=False) + " Z"
    wmax = max(r for _, r in profile) * S
    mx, my = A[0] + dx * 0.5, A[1] + dy * 0.5
    if nx > 0:
        nx, ny = -nx, -ny
    g = lin((mx + nx * wmax, my + ny * wmax), (mx - nx * wmax, my - ny * wmax),
            (0, fill_lo), (0.38, fill_hi), (0.66, "#C99B5C"), (1, "#6E4A24"))
    d.path(path, name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return A, B


def rung(name, a, b, r, ink=2.0):
    """Plain dowel rung between 3D points."""
    turned(name, a, b, [(0.0, r * 0.9), (0.08, r), (0.5, r * 1.15), (0.92, r), (1.0, r * 0.9)],
           ink=ink)


LEG = [(0.0, 0.40), (0.06, 0.48), (0.5, 0.55), (1.0, 0.68)]
POST = [(0.0, 0.40), (0.06, 0.48), (0.42, 0.55), (0.72, 0.60), (0.88, 0.52), (1.0, 0.44)]

# legs: foot -> top (front legs carry the arm ends, back legs rake to the rail)
legs = {
    "FL": ((-9.1, 0, -8.6), (-8.4, 25.55, -6.9)),
    "FR": ((9.1, 0, -8.6), (8.4, 25.55, -6.9)),
    "BL": ((-9.3, 0, 9.0), (-8.2, 27.7, 4.4)),
    "BR": ((9.3, 0, 9.0), (8.2, 27.7, 4.4)),
}
order = sorted(legs.items(), key=lambda kv: -depth(*kv[1][0]))
for k, (a, b) in order:
    turned(f"Leg {k}", a, b, POST if k[0] == "B" else LEG,
           fill_lo="#7A5528" if depth(*a) < 2 else "#8A6132")
    fx, fy = P(*a)
    d.shape("ellipse", f"Leg {k} foot shadow", x=round(fx - 13), y=round(fy - 3), width=26,
            height=8, fill=rad((0, "#000000", 52), (1, "#000000", 0)), stroke=NONE)

# rungs: front dowel rides a little higher than the sides and back
def leg_pt(k, y):
    a, b = legs[k]
    t = y / b[1]
    return along(a, b, t)


rung("Rung front", leg_pt("FL", 6.8), leg_pt("FR", 6.8), 0.30)
rung("Rung back", leg_pt("BL", 5.4), leg_pt("BR", 5.4), 0.30)
rung("Rung left", leg_pt("FL", 5.2), leg_pt("BL", 5.2), 0.30)
rung("Rung right", leg_pt("FR", 5.2), leg_pt("BR", 5.2), 0.30)

# --- seat --------------------------------------------------------------------------
# side + back rails peek out past the cord; front rail carries the weave
def rail_face(p3a, p3b, drop, name, fill):
    A, B = P(*p3a), P(*p3b)
    EXTENT.append((B[0], B[1] + drop))
    d.path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" %
           (A[0], A[1], B[0], B[1], B[0], B[1] + drop, A[0], A[1] + drop),
           name, fill=fill, stroke=INK, strokeWidth=2.5, join="round")


rail_face((-8.9, SEAT_Y - 0.4, -7.2), (8.9, SEAT_Y - 0.4, -7.2), SEAT_T * S * 0.8,
          "Seat rail front", BEECH)
rail_face((7.9, SEAT_Y - 0.5, -6.4), (7.2, SEAT_Y - 0.5, 6.2), SEAT_T * S * 0.7,
          "Seat rail right", BEECH_DK)
rail_face((-7.9, SEAT_Y - 0.5, -6.4), (-7.2, SEAT_Y - 0.5, 6.2), SEAT_T * S * 0.7,
          "Seat rail left", BEECH)
rail_face((-7.9, SEAT_Y - 0.5, 6.4), (7.9, SEAT_Y - 0.5, 6.4), SEAT_T * S * 0.85,
          "Seat rail back", BEECH_DK)

# cord field: slightly domed trapezoid inside the rails
cord_poly = [(-8.2, -6.6), (8.2, -6.6), (7.3, 5.9), (-7.3, 5.9)]
top_pts = [seat_map(x, z) for x, z in cord_poly]
d.path(smooth(top_pts, closed=True), "Cord field",
       fill=rad((0, "#EAD7AC"), (0.7, "#C9AB74"), (1, "#9A7844")),
       stroke="#5E4218", strokeWidth=2.5)
grid_weave("Cord", cord_poly, seat_map, 1.05, 1.05, CORD, sw=3.4, op=52)
# soft sheen across the weave
d.path(smooth([seat_map(x, z) for x, z in
               [(-5.4, -4.6), (-2.0, -1.0), (1.6, 1.4), (4.6, 4.2)]]),
       "Cord sheen", fill=NONE, stroke="#FFF2D2", strokeWidth=14, opacity=13, cap="round")
d.path(smooth([seat_map(x, -6.4) for x in (-7.6, -3, 3, 7.6)]),
       "Cord front wrap", fill=NONE, stroke="#7A5A28", strokeWidth=4, opacity=42, cap="round")

# --- Y splat ------------------------------------------------------------------------
# one outline: up the stem's left edge, around the left arm to its tip, back
# down the inner edge to the notch, up the right arm, down the right stem edge.
Z_SPLAT = 7.05
splat = [(-1.28, 16.9), (-1.18, 18.6), (-1.08, 21.0), (-1.0, 22.9),
         (-1.3, 24.2), (-2.15, 25.5), (-3.25, 26.5), (-4.25, 27.3), (-4.8, 27.65),
         (-4.45, 27.85), (-3.7, 27.65), (-2.55, 26.6), (-1.45, 25.3), (-0.55, 23.7),
         (0.0, 23.15),
         (0.55, 23.7), (1.45, 25.3), (2.55, 26.6), (3.7, 27.65), (4.45, 27.85),
         (4.8, 27.65), (4.25, 27.3), (3.25, 26.5), (2.15, 25.5), (1.3, 24.2),
         (1.0, 22.9), (1.08, 21.0), (1.18, 18.6), (1.28, 16.9)]
splat2 = [P(x, y, Z_SPLAT + 0.055 * (y - 16.9)) for x, y in splat]
d.path(smooth(splat2, closed=True), "Y splat",
       fill=lin((360, 270), (560, 520), (0, "#EFD49C"), (0.5, "#CDA468"), (1, "#8A6132")),
       stroke=INK, strokeWidth=3, join="round")
# splat shading: shade the inner faces of the fork
d.path(smooth([P(-0.42, 23.6, Z_SPLAT + 0.4), P(-1.6, 25.2, Z_SPLAT + 0.55),
               P(-2.9, 26.8, Z_SPLAT + 0.7), P(-3.9, 27.6, Z_SPLAT + 0.75)]),
       "Splat inner shade L", fill=NONE, stroke="#6E4A24", strokeWidth=3.5, opacity=35, cap="round")
d.path(smooth([P(0.42, 23.6, Z_SPLAT + 0.4), P(1.6, 25.2, Z_SPLAT + 0.55),
               P(2.9, 26.8, Z_SPLAT + 0.7), P(3.9, 27.6, Z_SPLAT + 0.75)]),
       "Splat inner shade R", fill=NONE, stroke="#6E4A24", strokeWidth=3.5, opacity=35, cap="round")
d.path(smooth([P(-0.72, 17.3, Z_SPLAT), P(-0.66, 19.8, Z_SPLAT + 0.2), P(-0.6, 22.3, Z_SPLAT + 0.35)]),
       "Splat light", fill=NONE, stroke=BEECH_HI, strokeWidth=2.5, opacity=40, cap="round")

# --- the bent rail -------------------------------------------------------------------
# horseshoe in plan: arm tips over the front legs, sweeping around the back;
# height falls from ~28.6 at the back apex to ~26.2 at the arm ends.
RAIL_PLAN = [(-8.4, -6.9), (-9.15, -4.6), (-9.6, -1.8), (-9.8, 1.0), (-9.55, 3.6),
             (-8.8, 5.2), (-7.2, 6.4), (-5.0, 7.15), (-2.6, 7.55), (0.0, 7.7),
             (2.6, 7.55), (5.0, 7.15), (7.2, 6.4), (8.8, 5.2), (9.55, 3.6),
             (9.8, 1.0), (9.6, -1.8), (9.15, -4.6), (8.4, -6.9)]


def rail_h(x, z):
    # apex height at the back centre, easing down toward the arm tips
    t = min(1.0, max(0.0, (z + 6.9) / 14.6))
    return 25.95 + 2.65 * math.sin(math.pi * t * 0.82) ** 0.9


rail3 = [(x, rail_h(x, z), z) for x, z in RAIL_PLAN]
rail2 = [P(*p) for p in rail3]
BW = 0.52 * S
outer, inner = [], []
for j, p in enumerate(rail2):
    q0 = rail2[max(0, j - 1)]
    q1 = rail2[min(len(rail2) - 1, j + 1)]
    tx, ty = q1[0] - q0[0], q1[1] - q0[1]
    L = math.hypot(tx, ty) or 1
    nx, ny = ty / L, -tx / L
    outer.append((p[0] + nx * BW / 2, p[1] + ny * BW / 2))
    inner.append((p[0] - nx * BW / 2, p[1] - ny * BW / 2))
top_y = min(p[1] for p in rail2)
d.path(smooth(outer) + " " + smooth(inner[::-1], move=False) + " Z", "Arm rail",
       fill=lin((0, top_y - 12), (0, rail2[9][1] + 60),
                (0, "#F4DCA8"), (0.45, "#D3AA6C"), (1, "#8A6132")),
       stroke=INK, strokeWidth=3, join="round")
hl = [(o[0] * 0.62 + c[0] * 0.38, o[1] * 0.62 + c[1] * 0.38) for o, c in zip(outer, rail2)]
d.path(smooth(hl[2:-2]), "Rail top light", fill=NONE, stroke="#FFF2CE",
       strokeWidth=3, opacity=55, cap="round")
sh2 = [(i_[0] * 0.62 + c[0] * 0.38, i_[1] * 0.62 + c[1] * 0.38) for i_, c in zip(inner, rail2)]
d.path(smooth(sh2[4:-4]), "Rail under shade", fill=NONE, stroke="#6E4A24",
       strokeWidth=3.5, opacity=38, cap="round")
# rounded caps where the rail ends rest on the front legs
for end, nm in ((rail3[0], "L"), (rail3[-1], "R")):
    ex, ey = P(*end)
    d.shape("ellipse", f"Rail {nm} joint shade", x=round(ex - 9), y=round(ey + 5),
            width=18, height=8, fill="#5E4218", opacity=45, stroke=NONE)

# --- extent check ----------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 30, far


# --- caption ----------------------------------------------------------------------------
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
    n = d.text(name, "Name", x=500, y=940, size=56, font="Virelai Sans",
               color="#F2E2C2", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C4AA86", justify="center")
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


caption("WISHBONE CHAIR", "BEECH · PAPER CORD")
d.finish("wishbone-chair-V1R00")
