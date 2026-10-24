#!/usr/bin/env python3
"""Cheval mirror — furniture field plate V1R00. Near-side view with a slight
three-quarter: an oval full-length glass in a slim mahogany frame, tilted a
few degrees back on its pivots, swung between two turned posts that stand on
splayed trestle feet with a low stretcher between them. Brass pivot screws,
a cool window sheen sliding down the glass. Mahogany plate, dressing-room
mood. 1000x1000. Modelled in inches (x right, y up, +z back), projected
with a fixed yaw + pitch; turned posts are hulls of ring samples.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Cheval Mirror — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1A0E08"   # warm dark, not black
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


def ext(x, y):
    EXTENT.append((x, y))
    return (x, y)


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(26), math.radians(13)
S, OX, OY = 9.0, 502.0, 758.0
CY, SY = math.cos(YAW), math.sin(YAW)
CP, SP = math.cos(PITCH), math.sin(PITCH)


def P(x, y, z):
    xr, zr = x * CY + z * SY, -x * SY + z * CY
    p = (OX + S * xr, OY - S * (y * CP + zr * SP))
    EXTENT.append(p)
    return p


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross3(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def vunit(a):
    l = math.sqrt(sum(c * c for c in a))
    return tuple(c / l for c in a)


def ring(c, u, r, n=36):
    ref = (1, 0, 0) if abs(u[0]) < 0.9 else (0, 1, 0)
    a = vunit(cross3(u, ref))
    b = cross3(u, a)
    return [tuple(c[i] + r * (math.cos(2 * math.pi * k / n) * a[i] +
                            math.sin(2 * math.pi * k / n) * b[i]) for i in range(3))
            for k in range(n)]


def hull(pts):
    pts = sorted(set((round(x, 1), round(y, 1)) for x, y in pts))
    if len(pts) <= 2:
        return pts

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo = []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


MAH = ((0, "#8A4E2E"), (0.3, "#5E3018"), (0.55, "#8A4E28"), (0.8, "#3E1E0E"), (1, "#5E3418"))
MAH_D = ((0, "#5E3018"), (0.5, "#7E4224"), (1, "#2E1408"))


def tube(name, a, b, r, grad=MAH, sw=2.0):
    """Round bar between 3D endpoints: hull of two end rings, lit across."""
    u = vunit(sub(b, a))
    pts = [P(*p) for p in ring(a, u, r) + ring(b, u, r)]
    h = hull(pts)
    pa, pb = P(*a), P(*b)
    dx, dy = pb[0] - pa[0], pb[1] - pa[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    w = r * S * 1.05
    cx, cy = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
    d.path(poly(h), name, fill=lin((cx + nx * w, cy + ny * w),
                                   (cx - nx * w, cy - ny * w), *grad),
           stroke=INK, strokeWidth=sw, join="round")
    return pa, pb


def turn(name, x, z, profile, grad=MAH, sw=2.0):
    """Turned post: hull of horizontal ring samples along a (y, r) profile."""
    pts = []
    for y, r in profile:
        pts += [P(*p) for p in ring((x, y, z), (0, 1, 0), r, n=26)]
    h = hull(pts)
    x0, x1 = min(p[0] for p in h), max(p[0] for p in h)
    d.path(poly(h), name, fill=lin((x0, 0), (x1, 0), *grad),
           stroke=INK, strokeWidth=sw, join="round")


def collar(x, z, y, r, name):
    """Thin dark ring round a turned post — a cove line of the turning."""
    pts = [P(*p) for p in ring((x, y, z), (0, 1, 0), r, n=26)]
    d.path(poly(pts), name, fill=NONE, stroke="#241008", strokeWidth=1.8,
           opacity=70, join="round")


def ribbon(name, pts, w0, w1, grad, sw=1.8):
    """Filled band along a screen-space polyline, width tapering w0->w1."""
    n = len(pts)
    left, right = [], []
    for i, p in enumerate(pts):
        t = i / (n - 1)
        w = w0 + (w1 - w0) * t
        a = pts[max(0, i - 1)]
        b = pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L * w / 2, dx / L * w / 2
        left.append((p[0] + nx, p[1] + ny))
        right.append((p[0] - nx, p[1] - ny))
    ext(*left[0]); ext(*right[-1])
    d.path(smooth(left + right[::-1], closed=True), name, fill=grad,
           stroke=INK, strokeWidth=sw, join="round")


def ell3(name, c, eu, ev, ru, rv, n=44):
    """Points of a 3D ellipse: centre c, axis dirs eu/ev, radii ru/rv."""
    return [P(c[0] + ru * math.cos(t) * eu[0] + rv * math.sin(t) * ev[0],
              c[1] + ru * math.cos(t) * eu[1] + rv * math.sin(t) * ev[1],
              c[2] + ru * math.cos(t) * eu[2] + rv * math.sin(t) * ev[2])
            for t in [2 * math.pi * k / n for k in range(n)]]


# --- backdrop + plate ------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1C1210"), (1, "#080505")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#9A6248", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5A3A2C"), (0.55, "#38221A"), (1, "#180E0A")),
        stroke="#120806", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8CDB2", strokeWidth=3, opacity=24)
# a faint cool glimmer from the glass side of the room
d.shape("ellipse", "Window glimmer", x=170, y=120, width=420, height=480,
        fill=rad((0, "#8AA8B8", 0.10), (0.6, "#6A8898", 0.04), (1, "#6A8898", 0)),
        stroke=NONE)

# floor: dark boards closing on the disc arc + a muted rug band under the stand
FYB = 726
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX - hw:.1f},{FYB} L{PCX + hw:.1f},{FYB} A420,420 0 0 0 {PCX - hw:.1f},{FYB} Z",
       "Floor", fill=lin((0, FYB), (0, 880), (0, "#3E2C22", 0.5), (0.5, "#241812", 0.78),
                         (1, "#0E0805", 0.92)), stroke=NONE)
d.path(f"M{PCX - hw + 6:.1f},{FYB} L{PCX + hw - 6:.1f},{FYB}", "Floor edge light",
       fill=NONE, stroke="#C8A488", strokeWidth=2, opacity=14)
for i, yb in enumerate([766, 802, 838]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Board seam {i+1}",
           fill=NONE, stroke="#4E3424", strokeWidth=2, opacity=22)
# rug arc: an ellipse band hugging the floor
d.shape("ellipse", "Rug", x=318, y=700, width=364, height=86,
        fill=rad((0, "#6E2E26", 0.5), (0.7, "#4E1E18", 0.28), (1, "#381410", 0)),
        stroke="#8A4A3A", strokeWidth=2, opacity=70)

# --- the stand ---------------------------------------------------------------------------
# two trestle ends at x=+-PX; each = turned post + a z-splayed foot
PX = 15.2
PIV_Y = 38.0          # pivot height
POST = [(1.6, 1.5), (3.4, 1.05), (5.2, 1.5), (9.0, 1.05), (11.5, 1.35),
        (30.0, 1.05), (33.0, 1.35), (52.0, 1.05), (54.6, 1.4), (56.2, 1.1)]

# grounding shadow
se = [P(-PX - 3, 0, -11), P(PX + 3, 0, -11), P(-PX - 3, 0, 11), P(PX + 3, 0, 11)]
sx0, sx1 = min(p[0] for p in se) - 16, max(p[0] for p in se) + 16
sy0, sy1 = min(p[1] for p in se) - 10, max(p[1] for p in se) + 14
d.shape("ellipse", "Stand shadow", x=round(sx0), y=round(sy0), width=round(sx1 - sx0),
        height=round(sy1 - sy0),
        fill=rad((0, "#030202", 0.6), (0.6, "#030202", 0.26), (1, "#030202", 0)),
        stroke=NONE)

# stretcher between the posts, low
tube("Stretcher", (-PX - 0.4, 5.4, 0), (PX + 0.4, 5.4, 0), r=0.55, grad=MAH_D)
for sx in (-1, 1):
    kn = P(sx * (PX - 0.5), 5.4, 0)
    d.shape("ellipse", f"Stretcher boss {sx:+d}", x=round(kn[0] - 5), y=round(kn[1] - 5),
            width=10, height=10, fill=rad((0, "#8A4E2E"), (1, "#2E1408")),
            stroke=INK, strokeWidth=1.4)

# far trestle (x=+PX) first, then the mirror, then the near trestle over it
def trestle(tag, x):
    # splayed foot: an S-curve board in the post's side plane, toe out each end
    centre = [P(x, 2.2, -10.5), P(x, 1.1, -6.0), P(x, 0.9, -1.5),
              P(x, 1.0, 3.5), P(x, 1.6, 7.0), P(x, 2.6, 10.5)]
    ribbon(f"Foot {tag}", centre, 11, 11,
           lin((0, min(p[1] for p in centre)), (0, max(p[1] for p in centre) + 14), *MAH_D))
    # toe caps: little upward scrolls
    for tz in (-10.5, 10.5):
        tp = P(x, 3.1, tz)
        d.shape("ellipse", f"Toe {tag} {tz:+g}", x=round(tp[0] - 5), y=round(tp[1] - 5.5),
                width=10, height=11, fill=rad((0, "#7E4224"), (1, "#2E1408")),
                stroke=INK, strokeWidth=1.4)
    turn(f"Post {tag}", x, 0, POST)
    for cy, cr in ((3.4, 1.55), (9.0, 1.4), (33.0, 1.5), (52.0, 1.35)):
        collar(x, 0, cy, cr, f"Collar {tag} {cy}")
    # finial: ball + spike on top
    fp = P(x, 57.3, 0)
    d.shape("ellipse", f"Finial {tag}", x=round(fp[0] - 8), y=round(fp[1] - 9),
            width=16, height=18, fill=rad((0, "#9A5A34"), (0.6, "#5E3018"), (1, "#241008")),
            stroke=INK, strokeWidth=1.6)
    sp = P(x, 59.6, 0)
    d.shape("ellipse", f"Finial tip {tag}", x=round(sp[0] - 3.5), y=round(sp[1] - 5),
            width=7, height=9, fill=rad((0, "#8A4E2E"), (1, "#2E1408")),
            stroke=INK, strokeWidth=1.2)
    ext(fp[0] - 8, fp[1] - 9); ext(sp[0], sp[1] - 5)


trestle("far", PX)
trestle("near", -PX)

# --- the glass, tilted back a few degrees ---------------------------------------------------
BETA = math.radians(9)
EU = (1, 0, 0)                          # lateral axis
EV = (0, math.cos(BETA), math.sin(BETA))  # vertical axis of the tilted plane
MC = (0, 36.0, 1.2)                     # mirror centre, hung just ahead of the posts
RO_X, RO_Y = 12.4, 27.5                 # frame outer radii
RI_X, RI_Y = 10.6, 25.7                 # glass radii

# frame: outer ellipse ring in mahogany
fo = ell3("frame outer", MC, EU, EV, RO_X, RO_Y)
fx0, fx1 = min(p[0] for p in fo), max(p[0] for p in fo)
fy0, fy1 = min(p[1] for p in fo), max(p[1] for p in fo)
d.path(poly(fo), "Mirror frame",
       fill=lin((fx0, fy0), (fx1, fy1), *MAH), stroke=INK, strokeWidth=2.6,
       join="round")
# carved bead just inside the frame edge
bd = ell3("bead", MC, EU, EV, RO_X - 0.75, RO_Y - 0.75)
d.path(poly(bd), "Frame bead", fill=NONE, stroke="#2A1208", strokeWidth=1.6,
       opacity=65, join="round")
# the glass
gl = ell3("glass", MC, EU, EV, RI_X, RI_Y)
gx0, gx1 = min(p[0] for p in gl), max(p[0] for p in gl)
gy0, gy1 = min(p[1] for p in gl), max(p[1] for p in gl)
d.path(poly(gl), "Glass",
       fill=lin((gx0, gy0), (gx1, gy1),
                (0, "#B8C8CC", 0.85), (0.35, "#7E9299", 0.8), (0.7, "#4E5E64", 0.85),
                (1, "#323E42", 0.9)), stroke="#0E0805", strokeWidth=2.2, join="round")
# sheen band sliding down the glass — a diagonal stripe inside the oval,
# plus a dimmer second band
def gplane(u, v):
    return P(MC[0] + u * EU[0] + v * EV[0],
             MC[1] + u * EU[1] + v * EV[1],
             MC[2] + u * EU[2] + v * EV[2])


sh = [gplane(u, 0.5 * u + c) for u, c in ((-9, -6), (5, -6), (5, 3), (-9, 3))]
d.path(poly(sh), "Glass sheen", fill="#E8F2F4", opacity=20, stroke=NONE)
sh2 = [gplane(u, 0.5 * u + c) for u, c in ((3, -9), (9, -9), (9, -5.5), (3, -5.5))]
d.path(poly(sh2), "Glass sheen 2", fill="#E8F2F4", opacity=12, stroke=NONE)
# hint of a reflected window: soft bright pane high on the glass
wx = [gplane(u, v) for u, v in ((-4.5, 16.5), (4.5, 16.5), (4.5, 6.0), (-4.5, 6.0))]
d.path(poly(wx), "Reflected window", fill="#D8E6EA", opacity=16, stroke=NONE)
wl = [gplane(u, v) for u, v in ((-0.6, 16.0), (0.6, 16.0), (0.6, 6.5), (-0.6, 6.5))]
d.path(poly(wl), "Window mullion", fill="#4E5E64", opacity=20, stroke=NONE)

# short swing arms from the posts into the frame's pivot line
for sx in (-1, 1):
    tube(f"Swing arm {sx:+d}", (sx * (PX - 0.4), PIV_Y, 0.8), (sx * 12.2, PIV_Y, 1.5),
         r=0.4, grad=MAH_D, sw=1.6)

# brass pivot screws at the frame's widest point, over the posts
for sx in (-1, 1):
    pp = P(sx * PX, PIV_Y, 0)
    d.shape("ellipse", f"Pivot {sx:+d}", x=round(pp[0] - 8), y=round(pp[1] - 8),
            width=16, height=16,
            fill=rad((0, "#FFF0B8"), (0.5, "#D2A24A"), (1, "#6E4A16")),
            stroke=INK, strokeWidth=1.8)
    d.shape("ellipse", f"Pivot slot {sx:+d}", x=round(pp[0] - 4.5), y=round(pp[1] - 1.6),
            width=9, height=3.2, fill="#3A2408", stroke=NONE)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("mirror extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 20, far


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
               color="#F0E2D0", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#CAA88C", justify="center")
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


caption("CHEVAL MIRROR", "MAHOGANY · GLASS · BRASS")
d.finish("cheval-mirror-V1R00")
