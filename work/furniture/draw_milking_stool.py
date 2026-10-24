#!/usr/bin/env python3
"""Milking stool — field plate V1R00. Three-quarter from the front right,
a touch higher than usual so the dish reads: a round ash seat, edge-rolled,
on three splayed and tapered legs — the tripod that stays level on any
floor — plus a leather carry strap hanging off the near side. Ash plate,
dairy-barn mood: pale grey-tan disc, a scatter of straw on the floor,
soft morning light. 1000x1000.
Modelled in inches (x right, y up, +z back), projected with fixed yaw +
pitch; legs are tapered 8-corner prisms culled by view normal.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Milking Stool — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E1710"   # warm dark, not black
EXTENT = []


def stops(*pairs):
    out = []
    for p in pairs:
        s = {"offset": p[0], "color": p[1]}
        if len(p) > 2 and p[2] is not None:
            s["opacity"] = p[2]
        out.append(s)
    return out


def lin(a, b, *pairs):
    return {"gradient": {"kind": "linear", "start": [round(a[0], 1), round(a[1], 1)],
                         "end": [round(b[0], 1), round(b[1], 1)], "stops": stops(*pairs)}}


def rad(*pairs):
    return {"gradient": {"kind": "radial", "stops": stops(*pairs)}}


def poly(pts):
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"


def smooth(pts, closed=True):
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = "M%.1f,%.1f" % pts[0]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(16), math.radians(26)
S, OX, OY = 23.4, 500.0, 706.0
CY, SY = math.cos(YAW), math.sin(YAW)
CP, SP = math.cos(PITCH), math.sin(PITCH)


def P(x, y, z):
    xr, zr = x * CY + z * SY, -x * SY + z * CY
    p = (OX + S * xr, OY - S * (y * CP + zr * SP))
    EXTENT.append(p)
    return p


def depth(x, y, z):
    """View-space distance; smaller = nearer the viewer (front-right-above)."""
    return -x * SY * CP - y * SP + z * CY * CP


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def normal(c, f):
    u = sub(c[f[1]], c[f[0]])
    v = sub(c[f[3]], c[f[0]])
    n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2],
         u[0] * v[1] - u[1] * v[0])
    l = math.sqrt(sum(k * k for k in n))
    return tuple(k / l for k in n)


def shade(hex1, hex2, b):
    a = [int(hex1[i:i + 2], 16) for i in (1, 3, 5)]
    c = [int(hex2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (c[i] - a[i]) * b) for i in range(3))


FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
TO_VIEWER = (SY * CP, SP, -CY * CP)
LIGHT = (-0.38, 0.82, -0.42)
_l = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / _l for c in LIGHT)

ASH_D, ASH_L = "#33291C", "#9E8A66"        # ash ramp
ASH_HI = "#C9B58A"


def prism(name, corners, lo=0.06, hi=0.94, ink=1.8, c1=ASH_D, c2=ASH_L,
          bias=0.0):
    """Draw the viewer-facing faces of an 8-corner prism, far to near."""
    faces = []
    for f in FACES:
        n = normal(corners, f)
        if n[0] * TO_VIEWER[0] + n[1] * TO_VIEWER[1] + n[2] * TO_VIEWER[2] <= 0.02:
            continue
        lam = max(0.0, sum(n[i] * LIGHT[i] for i in range(3)))
        dep = sum(depth(*corners[i]) for i in f) / len(f)
        pts = [P(*corners[i]) for i in f]
        faces.append((dep, pts, lam))
    for dep, pts, lam in sorted(faces, key=lambda t: -t[0]):
        b = lo + (hi - lo) * max(0.0, lam + bias) ** 0.8
        b = max(0.0, min(1.0, b))
        y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
        g = lin((0, y0), (0, y1), (0, shade(c1, c2, min(1, b + 0.12))),
                                 (1, shade(c1, c2, b)))
        d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return faces


def taper(cx0, cz0, cx1, cz1, y0, y1, hw0, hw1, ang=0.0):
    """8 corners of a box tapering from half-width hw0 at y0 to hw1 at y1;
    plan square rotated ang, centre sliding (cx0,cz0)->(cx1,cz1)."""
    ca, sa = math.cos(ang), math.sin(ang)

    def sq(cx, cz, hw):
        return [(cx + lx * ca + lz * sa, cz - lx * sa + lz * ca)
                for lx, lz in ((-hw, -hw), (hw, -hw), (hw, hw), (-hw, hw))]
    b = sq(cx0, cz0, hw0)
    t = sq(cx1, cz1, hw1)
    A, B, C, D = b
    At, Bt, Ct, Dt = t
    return [(A[0], y0, A[1]), (B[0], y0, B[1]), (Bt[0], y1, Bt[1]),
            (At[0], y1, At[1]), (D[0], y0, D[1]), (C[0], y0, C[1]),
            (Ct[0], y1, Ct[1]), (Dt[0], y1, Dt[1])]


def cyl(r, y, a0=0, a1=360, n=28, c=(0, 0)):
    """Ellipse-ish ring of projected points on a horizontal circle."""
    return [P(c[0] + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)), y,
              c[1] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def wall(r, y0, y1, a0, a1, name, n=30, c=(0, 0), tone=None, ink=1.7):
    pts = cyl(r, y1, a0, a1, n, c) + cyl(r, y0, a1, a0, n, c)
    y0s, y1s = min(p[1] for p in pts), max(p[1] for p in pts)
    g = lin((0, y0s), (0, y1s), *(tone or ((0, ASH_HI), (0.5, ASH_L), (1, ASH_D))))
    d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return pts


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#131210"), (1, "#050505")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8A8060", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#6E6250"), (0.6, "#484036"), (1, "#17130E")),
        stroke="#0D0A07", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4DCC4", strokeWidth=3, opacity=24)
# morning light, high and cool-warm
d.shape("ellipse", "Morning light", x=230, y=80, width=560, height=520,
        fill=rad((0, "#F0E4C0", 15), (0.55, "#C8B88E", 5), (1, "#C8B88E", 0)),
        stroke=NONE)

FY = 628
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4E4230", 36), (1, "#131008", 80)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E4D6AE", strokeWidth=2, opacity=18)
# straw scatter on the barn floor
import random
random.seed(7)
for i in range(18):
    tx = PCX + random.uniform(-210, 210)
    ty = random.uniform(FY + 26, FY + 170)
    if math.hypot(tx - PCX, ty - PCY) > PR - 44:
        continue
    tl = random.uniform(14, 34)
    ta = math.radians(random.uniform(-24, 24))
    d.path(f"M{tx - tl / 2 * math.cos(ta):.1f},{ty - tl / 2 * math.sin(ta):.1f} "
           f"L{tx + tl / 2 * math.cos(ta):.1f},{ty + tl / 2 * math.sin(ta):.1f}",
           f"Straw {i+1}", fill=NONE, stroke="#C9A968", strokeWidth=1.7,
           opacity=random.randint(18, 34), cap="round")

# --- stool geometry (inches) ------------------------------------------------------------
SEAT_R, SEAT_Y, SEAT_T = 5.3, 13.2, 1.7
# azimuth convention: point = (r*sin(a), r*cos(a)); a=0 is back, a=180 front
# legs at seat underside r=3.9 splaying to r=6.4 at floor
LEG_TOP_R, LEG_BOT_R = 3.9, 6.4
LEG_TOP_Y, LEG_BOT_Y = SEAT_Y - 0.2, 0.5

# grounding shadow
sp = [P(x, 0, z) for x, z in [(-8.4, -8.4), (8.4, -8.4), (8.4, 8.4), (-8.4, 8.4)]]
sx0, sx1 = min(p[0] for p in sp) - 30, max(p[0] for p in sp) + 30
sy0, sy1 = min(p[1] for p in sp) - 12, max(p[1] for p in sp) + 14
d.shape("ellipse", "Stool shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#040404", 64), (0.6, "#040404", 24), (1, "#040404", 0)),
        stroke=NONE)

# legs far to near: a=0 sits at +z (back of the stool), a=180 at -z (front)
legs = [("A", 0), ("B", 120), ("C", 240)]
for nm, a in sorted(legs, key=lambda t: -depth(LEG_TOP_R * math.sin(math.radians(t[1])),
                                               7, LEG_TOP_R * math.cos(math.radians(t[1])))):
    tx = LEG_TOP_R * math.sin(math.radians(a))
    tz = LEG_TOP_R * math.cos(math.radians(a))
    bx = LEG_BOT_R * math.sin(math.radians(a))
    bz = LEG_BOT_R * math.cos(math.radians(a))
    prism(f"Leg {nm}", taper(bx, bz, tx, tz, LEG_BOT_Y, SEAT_Y - 0.15,
                             0.42, 0.62, ang=math.radians(22)),
          lo=0.06, hi=0.95, ink=1.6)
    # foot tip darkened
    fx, fy = P(bx, 0.35, bz)
    d.shape("ellipse", f"Foot {nm}", x=round(fx - 9), y=round(fy - 3.5),
            width=18, height=8, fill=rad((0, "#54452E"), (1, "#221A0E")),
            stroke=INK, strokeWidth=1.3)
    # wedge end grain: the leg tenon shows through the seat's top face
    ex, ey = P(tx * 0.76, SEAT_Y + 0.31, tz * 0.76)
    d.shape("ellipse", f"Wedge {nm}", x=round(ex - 6), y=round(ey - 2.2),
            width=12, height=4.4, fill=rad((0, "#C0AC82"), (1, "#4E3F2A")),
            stroke=INK, strokeWidth=1.1)

# seat: rolled-edge cylinder wall + dished top
wall(SEAT_R, SEAT_Y - SEAT_T, SEAT_Y + 0.25, -180, 180, "Seat wall", n=40)
top_pts = [P(SEAT_R * math.sin(math.radians(t)), SEAT_Y + 0.28,
             SEAT_R * math.cos(math.radians(t))) for t in range(0, 360, 9)]
d.path(smooth(top_pts), "Seat top",
       fill=rad((0, "#B09A70"), (0.62, "#8A7452"), (1, "#4E3F2A")),
       stroke=INK, strokeWidth=1.9, join="round")
# the dish: a shallow darker bowl centre inside the top
dish_pts = [P((SEAT_R - 1.15) * math.sin(math.radians(t)), SEAT_Y + 0.30,
              (SEAT_R - 1.15) * math.cos(math.radians(t))) for t in range(0, 360, 12)]
d.path(smooth(dish_pts), "Seat dish",
       fill=rad((0, "#6E5A3E"), (0.7, "#7E6A4A", 55), (1, "#8A7452", 0)),
       stroke=NONE)
# carry hole bored through the seat wall, front-left of centre
hx0, hy0 = P((SEAT_R + 0.02) * math.sin(math.radians(206)), SEAT_Y - 0.75,
             (SEAT_R + 0.02) * math.cos(math.radians(206)))
d.path(f"M{hx0 - 17:.1f},{hy0 + 2:.1f} Q{hx0:.1f},{hy0 - 7:.1f} {hx0 + 17:.1f},{hy0 - 2:.1f} "
       f"Q{hx0:.1f},{hy0 + 7:.1f} {hx0 - 17:.1f},{hy0 + 2:.1f} Z",
       "Carry hole", fill="#160E08", stroke=INK, strokeWidth=1.3)
d.path(f"M{hx0 - 15:.1f},{hy0 + 1:.1f} Q{hx0:.1f},{hy0 - 5:.1f} {hx0 + 15:.1f},{hy0 - 2:.1f}",
       "Hole lip", fill=NONE, stroke="#C9B58A", strokeWidth=1.6, opacity=45,
       cap="round")

# leather carry strap hanging off the near edge, right of the handhold
sx0, sz0 = SEAT_R * math.sin(math.radians(160)), SEAT_R * math.cos(math.radians(160))
sx1, sz1 = SEAT_R * math.sin(math.radians(140)), SEAT_R * math.cos(math.radians(140))
sp0 = P(sx0 * 0.98, SEAT_Y + 0.1, sz0 * 0.98)
sp1 = P(sx1 * 0.98, SEAT_Y + 0.1, sz1 * 0.98)
loop_pts = [sp0,
            P(sx0 * 1.02, SEAT_Y - 2.6, sz0 * 1.02),
            P((sx0 + sx1) / 2 * 1.04, SEAT_Y - 3.6, (sz0 + sz1) / 2 * 1.04),
            P(sx1 * 1.02, SEAT_Y - 2.6, sz1 * 1.02), sp1]
d.path(smooth(loop_pts, closed=False), "Strap ink", fill=NONE, stroke=INK,
       strokeWidth=9.5, cap="round", opacity=50)
d.path(smooth(loop_pts, closed=False), "Carry strap", fill=NONE,
       stroke="#5E3A20", strokeWidth=6.5, cap="round")
for p_, lbl in ((sp0, "a"), (sp1, "b")):
    d.shape("ellipse", f"Strap tack {lbl}", x=round(p_[0] - 3.2), y=round(p_[1] - 2.6),
            width=6.4, height=5.4, fill=rad((0, "#D8B068"), (1, "#6A4A18")),
            stroke=INK, strokeWidth=0.9)

# top rim light along the far edge of the seat
rim = cyl(SEAT_R - 0.15, SEAT_Y + 0.42, -60, 60, 18)
d.path(smooth(rim, closed=False), "Seat rim light", fill=NONE, stroke="#F0E2B8",
       strokeWidth=2.0, opacity=34, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("stool extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 24, far


# --- caption ----------------------------------------------------------------------------------
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
               color="#F0E8D4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C4B68E", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=260)
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


caption("MILKING STOOL", "ASH · LEATHER")
d.finish("milking-stool-V1R00")
