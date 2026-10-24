#!/usr/bin/env python3
"""Valet stand — field plate V1R00. Three-quarter from the front right:
a mahogany clothes valet — square post on a sledge frame with a shoe
shelf, an arched hanger-shoulder up top with short end drops onto a
trouser bar, brass tie pegs on the post, an open accessory tray below
and a silk tie draped over the bar. Mahogany plate, dressing mood:
warm brown disc, a faint cheval mirror tilted behind, soft lamplight
from the upper left. 1000x1000.
Modelled in inches (x right, y up, +z back), projected with fixed yaw +
pitch; frame bars are 8-corner prisms culled by view normal.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Valet Stand — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#201810"   # warm dark, not black
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
YAW, PITCH = math.radians(24), math.radians(16)
S, OX, OY = 15.6, 506.0, 760.0
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


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def normal(c, f):
    u = sub(c[f[1]], c[f[0]])
    v = sub(c[f[3]], c[f[0]])
    n = cross(u, v)
    l = math.sqrt(sum(k * k for k in n))
    return tuple(k / l for k in n)


def shade(hex1, hex2, b):
    a = [int(hex1[i:i + 2], 16) for i in (1, 3, 5)]
    c = [int(hex2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (c[i] - a[i]) * b) for i in range(3))


FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
TO_VIEWER = (SY * CP, SP, -CY * CP)
LIGHT = (-0.45, 0.78, -0.48)
_l = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / _l for c in LIGHT)

MAHOG_D, MAHOG_L = "#301208", "#8A4E28"     # mahogany ramp
MAHOG_HI = "#B87A48"
BRASS_D, BRASS_L = "#4A3210", "#C89A48"
BRASS_HI = "#F2DC9E"


def prism(name, corners, lo=0.06, hi=0.94, ink=1.8, c1=MAHOG_D, c2=MAHOG_L,
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


def rbox(cx, cz, y0, y1, hw, ht, ang):
    """Box hw x ht in plan, rotated ang about y through (cx,cz)."""
    ca, sa = math.cos(ang), math.sin(ang)
    cs = [(cx + lx * ca + lz * sa, cz - lx * sa + lz * ca)
          for lx, lz in ((-hw, -ht), (hw, -ht), (hw, ht), (-hw, ht))]
    A, B, C, D = cs
    return [(A[0], y0, A[1]), (B[0], y0, B[1]), (B[0], y1, B[1]),
            (A[0], y1, A[1]), (D[0], y0, D[1]), (C[0], y0, C[1]),
            (C[0], y1, C[1]), (D[0], y1, D[1])]


def beam(a, b, w2, h2, stretch=0.0):
    """8 corners of a w x h section bar along a->b (3D), stretched a touch
    along its own axis so chained segments butt without seams."""
    u = sub(b, a)
    L = math.sqrt(sum(k * k for k in u)) or 1.0
    u = tuple(k / L for k in u)
    a = sub(a, tuple(k * stretch for k in u))
    b = tuple(b[k] + u[k] * stretch for k in range(3))
    r = (0, 1, 0) if abs(u[1]) < 0.9 else (1, 0, 0)
    v1 = cross(u, r)
    l1 = math.sqrt(sum(k * k for k in v1))
    v1 = tuple(k / l1 for k in v1)
    v2 = cross(u, v1)

    def q(end, s1, s2):
        return (end[0] + s1 * v1[0] + s2 * v2[0],
                end[1] + s1 * v1[1] + s2 * v2[1],
                end[2] + s1 * v1[2] + s2 * v2[2])
    return [q(a, -w2, -h2), q(b, -w2, -h2), q(b, w2, -h2), q(a, w2, -h2),
            q(a, -w2, h2), q(b, -w2, h2), q(b, w2, h2), q(a, w2, h2)]


def bolt(name, p, r=4.0):
    x, y = P(*p)
    d.shape("ellipse", name, x=round(x - r), y=round(y - r), width=round(2 * r),
            height=round(2 * r),
            fill=rad((0, "#F8ECC8"), (0.55, "#C09A4E"), (1, "#5A3E14")),
            stroke=INK, strokeWidth=1.3)
    d.shape("ellipse", f"{name} glint", x=round(x - r * 0.5), y=round(y - r * 0.7),
            width=round(r * 0.7), height=round(r * 0.5),
            fill="#FFFFFF", opacity=80, stroke=NONE)


def wood(name, corners, **kw):
    kw.setdefault("c1", MAHOG_D)
    kw.setdefault("c2", MAHOG_L)
    return prism(name, corners, **kw)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#170D08"), (1, "#070403")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#A07850", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#66402A"), (0.6, "#40281A"), (1, "#140C08")),
        stroke="#0C0805", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8CCA0", strokeWidth=3, opacity=24)

# cheval mirror ghost in the backdrop, tilted off vertical, upper left
mc, mr_, tlt = (318, 372), (92, 148), math.radians(-11)
mpts = [(mc[0] + mr_[0] * math.cos(t) * math.cos(tlt) - mr_[1] * math.sin(t) * math.sin(tlt),
         mc[1] + mr_[0] * math.cos(t) * math.sin(tlt) + mr_[1] * math.sin(t) * math.cos(tlt))
        for t in [2 * math.pi * i / 40 for i in range(40)]]
d.path(smooth(mpts), "Mirror frame ghost", fill=NONE,
       stroke="#E8CCA0", strokeWidth=4.5, opacity=9)
mpts2 = [(mc[0] + (mr_[0] - 13) * math.cos(t) * math.cos(tlt) - (mr_[1] - 13) * math.sin(t) * math.sin(tlt),
          mc[1] + (mr_[0] - 13) * math.cos(t) * math.sin(tlt) + (mr_[1] - 13) * math.sin(t) * math.cos(tlt))
         for t in [2 * math.pi * i / 40 for i in range(40)]]
d.path(smooth(mpts2), "Mirror glass ghost",
       fill=rad((0, "#E8CCA0", 7), (1, "#E8CCA0", 2)), stroke=NONE)
shear = [(mc[0] - 24 - 0.28 * k, mc[1] - 60 + k * 2.4) for k in range(50)]
d.path(smooth(shear, closed=False), "Mirror sheen", fill=NONE,
       stroke="#F4E4BC", strokeWidth=10, opacity=6, cap="round")

# lamp spot from the upper left
d.shape("ellipse", "Spot", x=150, y=80, width=640, height=580,
        fill=rad((0, "#F2CE96", 15), (0.55, "#C89658", 6), (1, "#C89658", 0)),
        stroke=NONE)

FY = 735
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4E3A24", 44), (1, "#100A06", 78)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#EAD0A0", strokeWidth=2, opacity=18)

# --- valet stand geometry (inches) ---------------------------------------------------
RX, RZ = 6.9, 6.4                     # base frame half-extents
POST_HW = 0.62                        # post half-width
POST_TOP = 44.3
TROUSER_Y = 37.2                      # trouser bar centre height
SH_X = 8.3                            # shoulder half-width
TRAY_Y = 26.0                         # tray bottom top-face level

# grounding shadow
sp_ = [P(x, 0, z) for x, z in [(-8.6, -8.6), (8.6, -8.6), (8.6, 8.6), (-8.6, 8.6)]]
sx0, sx1 = min(p[0] for p in sp_) - 30, max(p[0] for p in sp_) + 30
sy0, sy1 = min(p[1] for p in sp_) - 11, max(p[1] for p in sp_) + 14
d.shape("ellipse", "Stand shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#050302", 64), (0.6, "#050302", 24), (1, "#050302", 0)),
        stroke=NONE)

# --- base: sledge frame + shoe slats, far to near -----------------------------------
wood("Base rail back", rbox(0, RZ, 0.2, 1.15, RX + 0.55, 0.42, 0),
     lo=0.05, hi=0.9, ink=1.6, bias=-0.10)
wood("Base rail left", rbox(-RX, 0, 0.2, 1.15, 0.42, RZ, 0),
     lo=0.05, hi=0.9, ink=1.6, bias=-0.12)

# shoe shelf slats resting in the frame
for i, zz in enumerate((-4.5, -2.2, 0.1, 2.4, 4.7)):
    wood(f"Shoe slat {i+1}", rbox(0, zz, 2.45, 2.8, RX - 0.55, 0.36, 0),
         lo=0.08, hi=0.92, ink=1.5)
# little cleats under the slat ends
for i, sgn in enumerate((-1, 1)):
    wood(f"Cleat {sgn:+}", rbox(sgn * (RX - 0.35), 0, 1.9, 2.45, 0.28, 4.9, 0),
         lo=0.05, hi=0.85, ink=1.4, bias=-0.08)

# --- post (goes down before the near base rails, it stands behind them) --------------
wood("Post", rbox(0, 0, 1.0, POST_TOP, POST_HW, POST_HW, 0),
     lo=0.07, hi=0.95, ink=1.8)
# turning collars on the post
for i, yy in enumerate((7.6, 36.9)):
    wood(f"Post collar {i+1}", rbox(0, 0, yy - 0.28, yy + 0.28,
                                    POST_HW + 0.16, POST_HW + 0.16, 0),
         lo=0.08, hi=0.95, ink=1.5)
# brass ferrule where the shoulder meets the post
prism("Apex ferrule", rbox(0, 0, POST_TOP - 1.35, POST_TOP - 0.75,
                           POST_HW + 0.1, POST_HW + 0.1, 0),
      lo=0.15, hi=1.0, ink=1.4, c1=BRASS_D, c2=BRASS_L)

# near base rails over the post foot
wood("Base rail right", rbox(RX, 0, 0.2, 1.15, 0.42, RZ, 0),
     lo=0.08, hi=0.95, ink=1.6)
wood("Base rail front", rbox(0, -RZ, 0.2, 1.15, RX + 0.55, 0.42, 0),
     lo=0.08, hi=0.95, ink=1.6)
# runner end caps
for i, (xx, zz) in enumerate([(-RX, -RZ), (RX, -RZ), (RX, RZ), (-RX, RZ)]):
    cx, cy = P(xx, 0.62, zz)
    d.shape("ellipse", f"Runner foot {i+1}", x=round(cx - 9), y=round(cy - 4),
            width=18, height=8, fill=rad((0, "#5E3418"), (1, "#1E0E06")),
            stroke=INK, strokeWidth=1.3)

# --- accessory tray on the post front -------------------------------------------------
TZ0, TZ1, TX = -5.7, -0.75, 4.7         # tray z extents and half-width
# back wall first (hugs the post), then floor, felt, side + front walls
wood("Tray wall back", rbox(0, TZ1, TRAY_Y + 0.5, TRAY_Y + 1.75, TX, 0.17, 0),
     lo=0.05, hi=0.85, ink=1.4, bias=-0.08)
wood("Tray floor", rbox(0, (TZ0 + TZ1) / 2, TRAY_Y, TRAY_Y + 0.5, TX, (TZ1 - TZ0) / 2, 0),
     lo=0.08, hi=0.9, ink=1.6)
# felt lining on the tray floor
felt = rbox(0, (TZ0 + TZ1) / 2, TRAY_Y + 0.5, TRAY_Y + 0.62, TX - 0.4, (TZ1 - TZ0) / 2 - 0.4, 0)
prism("Tray felt", felt, lo=0.1, hi=0.8, ink=1.3, c1="#16281C", c2="#3E6248")
for i, sgn in enumerate((-1, 1)):
    wood(f"Tray wall {sgn:+}", rbox(sgn * TX, (TZ0 + TZ1) / 2, TRAY_Y + 0.5,
                                    TRAY_Y + 1.75, 0.17, (TZ1 - TZ0) / 2, 0),
         lo=0.08, hi=0.95, ink=1.5)
wood("Tray wall front", rbox(0, TZ0, TRAY_Y + 0.5, TRAY_Y + 1.75, TX, 0.17, 0),
     lo=0.1, hi=0.97, ink=1.5)
# cleats tying the tray to the post
for i, sgn in enumerate((-1, 1)):
    wood(f"Tray cleat {sgn:+}", rbox(sgn * 2.4, -1.1, TRAY_Y - 0.55, TRAY_Y,
                                     0.55, 0.42, 0), lo=0.05, hi=0.85, ink=1.4,
         bias=-0.06)
# pocket square peeking over the felt, front-left corner
sq = [P(-2.9, TRAY_Y + 0.66, -4.4), P(-1.7, TRAY_Y + 0.66, -4.0),
      P(-2.0, TRAY_Y + 0.66, -2.9), P(-3.2, TRAY_Y + 0.66, -3.3)]
d.path(poly(sq), "Pocket square base",
       fill=lin(sq[0], sq[2], (0, "#8A7A5E"), (1, "#CBB98F")),
       stroke=INK, strokeWidth=1.2)
sq2 = [P(-2.55, TRAY_Y + 0.67, -3.9), P(-2.35, TRAY_Y + 1.35, -3.5),
       P(-1.95, TRAY_Y + 0.67, -3.35)]
d.path(poly(sq2), "Pocket square fold",
       fill=lin(sq2[0], sq2[1], (0, "#D8CBA8"), (1, "#F2EAD2")),
       stroke=INK, strokeWidth=1.2)

# --- hanger group: arched shoulders, end drops, trouser bar ----------------------------
# shoulder arch as one smooth ribbon (segmented prisms read as cogs here)
NSEG = 24
arch = [(x, POST_TOP - 0.15 - 1.95 * (abs(x) / SH_X) ** 1.75, 0.0)
        for x in [-SH_X + 2 * SH_X * i / NSEG for i in range(NSEG + 1)]]
AH, AZ = 0.44, 0.30                   # arch half-height in-plane / half-depth in z


def edge_pts(off, zz):
    out = []
    for i, (x, y, z) in enumerate(arch):
        a = arch[i - 1] if i else arch[i]
        b = arch[i + 1] if i < NSEG else arch[i]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        out.append(P(x + off * -dy / L, y + off * dx / L, zz))
    return out


top_f = edge_pts(AH, -AZ)
top_b = edge_pts(AH, AZ)
bot_f = edge_pts(-AH, -AZ)
# narrow back-top band first (the lit crown of the bar), then the front face
d.path(poly(top_f + top_b[::-1]), "Shoulder crown",
       fill=lin((0, min(p[1] for p in top_f)), (0, max(p[1] for p in top_f)),
                (0, MAHOG_HI), (1, MAHOG_L)),
       stroke=INK, strokeWidth=1.3, join="round")
face = top_f + bot_f[::-1]
d.path(smooth(face), "Shoulder face",
       fill=lin((0, min(p[1] for p in face)), (0, max(p[1] for p in face)),
                (0, "#9A5C30"), (0.5, "#5A2A14"), (1, "#38160A")),
       stroke=INK, strokeWidth=1.8, join="round")
# faint joint ticks along the crown for a built-up shoulder
for i in (5, 11, 13, 19):
    a, b = top_f[i], top_b[i]
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}",
           f"Crown tick {i}", fill=NONE, stroke="#2A1008",
           strokeWidth=1.1, opacity=45)

for i, sgn in enumerate((-1, 1)):
    wood(f"Drop {sgn:+}", beam((sgn * SH_X, arch[0][1] if sgn < 0 else arch[-1][1], 0),
                               (sgn * SH_X, TROUSER_Y, 0), 0.26, 0.36),
         lo=0.07, hi=0.95, ink=1.6)
wood("Trouser bar", beam((-SH_X, TROUSER_Y, 0), (SH_X, TROUSER_Y, 0), 0.30, 0.42),
     lo=0.08, hi=0.97, ink=1.7)
# brass balls where the drops meet the bar
for i, sgn in enumerate((-1, 1)):
    bolt(f"Drop boss {sgn:+}", (sgn * SH_X, TROUSER_Y - 0.15, -0.3), r=4.6)
# small shoulder-tip knobs
for i, sgn in enumerate((-1, 1)):
    e = arch[0] if sgn < 0 else arch[-1]
    cx, cy = P(sgn * (SH_X + 0.15), e[1] - 0.15, 0)
    d.shape("ellipse", f"Shoulder knob {sgn:+}", x=round(cx - 5.5),
            y=round(cy - 4.5), width=11, height=9,
            fill=rad((0, MAHOG_HI), (1, MAHOG_D)), stroke=INK, strokeWidth=1.4)

# --- brass tie pegs on the post sides -------------------------------------------------
for i, sgn in enumerate((-1, 1)):
    prism(f"Tie peg {sgn:+}", beam((sgn * POST_HW, 33.0, -0.1),
                                   (sgn * (POST_HW + 1.5), 34.4, -0.35),
                                   0.16, 0.16),
          lo=0.2, hi=1.0, ink=1.3, c1=BRASS_D, c2=BRASS_L)
    bolt(f"Peg tip {sgn:+}", (sgn * (POST_HW + 1.55), 34.55, -0.37), r=3.4)

# --- silk tie draped over the trouser bar, right end -----------------------------------
def ribbon(name, spine3, w, fill, ink=1.5):
    """Projected ribbon: spine of 3D pts + per-pt half-widths (pt)."""
    s2 = [P(*p) for p in spine3]
    left, right = [], []
    for i, p in enumerate(s2):
        a = s2[i - 1] if i else s2[i]
        b = s2[i + 1] if i < len(s2) - 1 else s2[i]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        left.append((p[0] + nx * w[i], p[1] + ny * w[i]))
        right.append((p[0] - nx * w[i], p[1] - ny * w[i]))
    d.path(smooth(left + right[::-1]), name, fill=fill,
           stroke=INK, strokeWidth=ink, join="round")


TIE_D, TIE_L = "#3E1418", "#8E3830"
# back blade (narrower, darker), hanging behind the bar
back = [(6.7, TROUSER_Y + 0.1, 0.18), (6.55, TROUSER_Y - 1.5, 0.28),
        (6.5, TROUSER_Y - 3.2, 0.3), (6.6, TROUSER_Y - 5.0, 0.28)]
ribbon("Tie back blade", back, [5.0, 5.6, 4.8, 1.8],
       lin((0, 0), (0, 200), (0, "#260C0E"), (1, "#5A2020")))
# front blade over the bar, swinging slightly out as it falls
front = [(6.9, TROUSER_Y + 0.55, -0.34), (7.05, TROUSER_Y - 0.9, -0.5),
         (7.2, TROUSER_Y - 2.9, -0.6), (7.3, TROUSER_Y - 5.2, -0.66),
         (7.35, TROUSER_Y - 7.4, -0.7), (7.25, TROUSER_Y - 8.9, -0.7)]
w_f = [5.6, 6.4, 6.8, 6.4, 4.6, 0.8]
y0f = P(*front[0])[1]
y1f = P(*front[-1])[1]
ribbon("Tie front blade", front, w_f,
       lin((0, y0f), (0, y1f), (0, TIE_L), (0.55, TIE_D), (1, "#2A0E12")))
# blade edge sheen + one subtle rep stripe
sheen = [P(*p) for p in [(7.15, TROUSER_Y - 0.6, -0.52), (7.35, TROUSER_Y - 3.4, -0.62),
                          (7.4, TROUSER_Y - 6.2, -0.68)]]
d.path(smooth(sheen, closed=False), "Tie sheen", fill=NONE,
       stroke="#D88A78", strokeWidth=2.2, opacity=45, cap="round")
st0, st1 = P(6.85, TROUSER_Y - 1.4, -0.5), P(7.6, TROUSER_Y - 2.5, -0.6)
d.path(f"M{st0[0]:.1f},{st0[1]:.1f} L{st1[0]:.1f},{st1[1]:.1f}", "Tie stripe",
       fill=NONE, stroke="#B86A58", strokeWidth=3.2, opacity=55, cap="round")
# knot wrapped over the bar top
knot = [P(6.55, TROUSER_Y + 0.62, -0.3), P(7.35, TROUSER_Y + 0.72, -0.3),
        P(7.2, TROUSER_Y - 0.1, -0.42), P(6.7, TROUSER_Y - 0.25, -0.42)]
d.path(poly(knot), "Tie knot",
       fill=lin(knot[0], knot[2], (0, "#9E5040"), (1, "#44161A")),
       stroke=INK, strokeWidth=1.4, join="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("stand extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F4E4C4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C8AE80", justify="center")
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


caption("VALET STAND", "MAHOGANY · BRASS · FELT")
d.finish("valet-stand-V1R00")
