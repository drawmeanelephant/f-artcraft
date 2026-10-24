#!/usr/bin/env python3
"""Corner chair — field plate V1R00. The roundabout: a round leather seat
on four legs set in a diamond, a low double bow rail sweeping the back
three-quarters on three turned posts, a vase splat at the back and cross
stretchers between the legs. Drawn diagonally (yaw 45) the way it sits in
a room corner. Mahogany plate, diagonal mood: warm red-brown disc with
diagonal shafts of window light clipped to the plate. 1000x1000.
Modelled in inches (x right, y up, +z back), projected with fixed yaw +
pitch; squared members are 8-corner prisms culled by view normal, round
members are stroke capsules, the bow rails are arc ribbons.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Corner Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E120C"   # warm dark, not black
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


def disc_band(name, p0, p1, w, grad):
    """A straight band of width w along p0->p1 clipped to the plate disc."""
    R = PR - 9
    ux, uy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    nx, ny = -uy, ux

    def hits(off):
        ax, ay = p0[0] + nx * off - PCX, p0[1] + ny * off - PCY
        b = ax * ux + ay * uy
        q = b * b - (ax * ax + ay * ay - R * R)
        if q <= 0:
            return None
        r = math.sqrt(q)
        return [(p0[0] + nx * off + t * ux, p0[1] + ny * off + t * uy)
                for t in (-b - r, -b + r)]

    hp, hm = hits(w / 2), hits(-w / 2)
    if not hp or not hm:
        return

    def arc(a, b, through, n=20):
        TAU = 2 * math.pi
        a0 = math.atan2(a[1] - PCY, a[0] - PCX) % TAU
        a1 = math.atan2(b[1] - PCY, b[0] - PCX) % TAU
        ta = math.atan2(through[1] - PCY, through[0] - PCX) % TAU
        ccw = (a1 - a0) % TAU
        delta = ccw if (ta - a0) % TAU <= ccw else ccw - TAU
        return [(PCX + R * math.cos(a0 + delta * i / n),
                 PCY + R * math.sin(a0 + delta * i / n)) for i in range(1, n)]

    far_t = (PCX + ux * R, PCY + uy * R)
    near_t = (PCX - ux * R, PCY - uy * R)
    pts = [hp[0], hp[1]] + arc(hp[1], hm[1], far_t) + \
        [hm[1], hm[0]] + arc(hm[0], hp[0], near_t)
    d.path(poly(pts), name, fill=grad, stroke=NONE)


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(45), math.radians(20)
S, OX, OY = 15.4, 510.0, 730.0
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
LIGHT = (-0.40, 0.78, -0.48)
_l = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / _l for c in LIGHT)

MAH_D, MAH_L = "#2A120A", "#8A4526"        # mahogany ramp
MAH_HI = "#C07A48"


def prism(name, corners, lo=0.06, hi=0.94, ink=1.8, c1=MAH_D, c2=MAH_L,
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
    plan square rotated ang about y, centre sliding (cx0,cz0)->(cx1,cz1)."""
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


def bar(name, a, b, r, grad=None, ink=2.0):
    """Round-ended member between 3D points, lit across its width."""
    grad = grad or ((0, MAH_L), (0.4, MAH_HI), (0.62, MAH_L), (1, MAH_D))
    A, B = P(*a), P(*b)
    dx, dy = B[0] - A[0], B[1] - A[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    w = r * S
    pts = []
    for k in range(9):
        t = math.pi * k / 8
        pts.append((B[0] + nx * w * math.cos(t) + ux * w * math.sin(t),
                    B[1] + ny * w * math.cos(t) + uy * w * math.sin(t)))
    for k in range(9):
        t = math.pi * k / 8
        pts.append((A[0] - nx * w * math.cos(t) - ux * w * math.sin(t),
                    A[1] - ny * w * math.cos(t) - uy * w * math.sin(t)))
    mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
    if nx > 0:
        nx, ny = -nx, -ny
    g = lin((mx + nx * w, my + ny * w), (mx - nx * w, my - ny * w), *grad)
    d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    assert 2 * w >= 3, "bar must stay >= 3pt"
    return A, B


def arc_pts(r, y, a0, a1, n=24, c=(0, 0)):
    """Points on the seat-axis cylinder: a=0 is straight back (+z)."""
    return [P(c[0] + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)), y,
              c[1] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def band(r, y0, y1, a0, a1, name, n=28, c=(0, 0), tone=None, ink=1.6):
    """Vertical ribbon on a cylinder wall between y0 and y1."""
    pts = arc_pts(r, y1, a0, a1, n, c) + arc_pts(r, y0, a1, a0, n, c)
    y0s, y1s = min(p[1] for p in pts), max(p[1] for p in pts)
    g = lin((0, y0s), (0, y1s), *(tone or ((0, MAH_HI), (0.5, MAH_L), (1, MAH_D))))
    d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return pts


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#180E0C"), (1, "#080404")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7A4228", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5E3A28"), (0.6, "#3E2418"), (1, "#160C08")),
        stroke="#0E0604", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0B088", strokeWidth=3, opacity=22)
# diagonal window light, clipped to the disc — the diagonal mood
disc_band("Light shaft", (120, -40), (640, 920), 150,
          lin((300, 60), (540, 860), (0, "#F0C890", 18), (0.6, "#D8A468", 7),
              (1, "#D8A468", 0)))
disc_band("Light shaft 2", (560, -20), (960, 800), 55,
          lin((590, 60), (880, 760), (0, "#F0C890", 9), (1, "#D8A468", 0)))
# warm glow low-left where the shafts land
d.shape("ellipse", "Glow pool", x=370, y=600, width=360, height=230,
        fill=rad((0, "#D89050", 10), (0.6, "#A06038", 5), (1, "#A06038", 0)),
        stroke=NONE)

FY = 706
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4A2E1E", 40), (1, "#120806", 76)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E8B98A", strokeWidth=2, opacity=18)

# --- chair geometry (inches) ----------------------------------------------------------
# diamond plan: legs at back (+z), left/right (x), front (-z); seat r~9.6
SEAT_R, SEAT_Y, SEAT_T = 9.6, 16.4, 2.6
LEG_P = {"front": (0, -8.6), "back": (0, 8.6), "left": (-8.6, 0), "right": (8.6, 0)}
FOOT_R = 10.1
RAIL_LO, RAIL_HI = 27.4, 32.0
RBOW = 9.7
A_END = 128

# grounding shadow
sp = [P(x, 0, z) for x, z in [(-11.8, -11.8), (11.8, -11.8), (11.8, 11.8), (-11.8, 11.8)]]
sx0, sx1 = min(p[0] for p in sp) - 34, max(p[0] for p in sp) + 34
sy0, sy1 = min(p[1] for p in sp) - 14, max(p[1] for p in sp) + 16
d.shape("ellipse", "Chair shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#050302", 68), (0.6, "#050302", 26), (1, "#050302", 0)),
        stroke=NONE)

# legs: tapered prisms splaying from seat rim to the floor
for nm in ("back", "left", "right", "front"):
    cx, cz = LEG_P[nm]
    fx, fz = cx / 8.6 * FOOT_R, cz / 8.6 * FOOT_R
    prism(f"Leg {nm}", taper(cx, cz, fx, fz, SEAT_Y - 0.4, 0.6, 0.72, 0.5,
                             ang=math.radians(45)),
          lo=0.05, hi=0.92, ink=1.7)
    ex, ey = P(fx, 0.35, fz)
    d.shape("ellipse", f"Pad foot {nm}", x=round(ex - 10), y=round(ey - 4),
            width=20, height=9, fill=rad((0, "#5E3018"), (1, "#241008")),
            stroke=INK, strokeWidth=1.5)

# cross stretchers between neighbouring legs, low and quiet
STRET_Y = 4.6
pairs = [("front", "left"), ("front", "right"), ("back", "left"), ("back", "right")]
for a, b in sorted(pairs,
                   key=lambda t: -depth((LEG_P[t[0]][0] + LEG_P[t[1]][0]) / 2,
                                        STRET_Y,
                                        (LEG_P[t[0]][1] + LEG_P[t[1]][1]) / 2)):
    ax, az = LEG_P[a]
    bx, bz = LEG_P[b]
    f = FOOT_R / 8.6 * 0.95          # stretcher ends meet the legs' floor positions
    bar(f"Stretcher {a}-{b}", (ax * f, STRET_Y, az * f), (bx * f, STRET_Y, bz * f),
        r=0.38, ink=1.6,
        grad=((0, "#4A2414"), (0.45, "#7A4524"), (1, "#241008")))

# --- seat: mahogany rim band + leather pad ----------------------------------------------
seat_pts = band(SEAT_R + 0.3, SEAT_Y - SEAT_T, SEAT_Y + 0.2, -180, 180, "Seat rail",
                n=40, ink=1.8)
seat_top = [P(SEAT_R * math.sin(math.radians(t)), SEAT_Y + 0.45,
              SEAT_R * math.cos(math.radians(t))) for t in range(0, 360, 10)]
d.path(smooth(seat_top), "Leather seat",
       fill=rad((0, "#7A4030"), (0.55, "#542A1C"), (1, "#2A100A")),
       stroke=INK, strokeWidth=2.0, join="round")
sx, sy = P(-2.5, SEAT_Y + 0.5, 2.0)
d.shape("ellipse", "Seat sheen", x=round(sx - 90), y=round(sy - 40), width=180, height=80,
        fill=rad((0, "#E8A878", 16), (1, "#E8A878", 0)), stroke=NONE)
# stitched welt + brass nails on the front half of the rim
welt = arc_pts(SEAT_R - 0.7, SEAT_Y + 0.55, 140, 40, 22)
d.path(smooth(welt, closed=False), "Seat welt", fill=NONE, stroke="#1E0C06",
       strokeWidth=2.2, opacity=60)
for i, a in enumerate(range(150, 31, -12)):
    px, py = P((SEAT_R - 0.55) * math.sin(math.radians(a)), SEAT_Y + 0.45,
               (SEAT_R - 0.55) * math.cos(math.radians(a)))
    d.shape("ellipse", f"Nail {i+1}", x=round(px - 2.6), y=round(py - 2.2), width=5.2, height=4.4,
            fill=rad((0, "#F4D488"), (0.6, "#B8862E"), (1, "#5E3C10")),
            stroke=INK, strokeWidth=0.8)

# --- bow: two rails wrapping the back ~250 degrees ---------------------------------------
# azimuth a: 0 = back (+z); the opening faces the front (-z)
band(RBOW, RAIL_LO, RAIL_LO + 1.1, -A_END, A_END, "Bow lower",
     tone=((0, "#6E3A1E"), (1, "#381A0C")), ink=1.5)
band(RBOW, RAIL_HI - 1.7, RAIL_HI, -A_END, A_END, "Bow top", ink=1.7)
# arm ends: a short turned stub joins the two rails where the bow stops
for a_end, lbl in ((-A_END, "L"), (A_END, "R")):
    px = RBOW * math.sin(math.radians(a_end))
    pz = RBOW * math.cos(math.radians(a_end))
    c0 = P(px, RAIL_LO + 0.35, pz)
    c1 = P(px, RAIL_HI + 0.05, pz)
    d.path(f"M{c0[0]:.1f},{c0[1]:.1f} L{c1[0]:.1f},{c1[1]:.1f}",
           f"Bow end ink {lbl}", fill=NONE, stroke=INK, strokeWidth=10,
           cap="round", opacity=50)
    d.path(f"M{c0[0]:.1f},{c0[1]:.1f} L{c1[0]:.1f},{c1[1]:.1f}",
           f"Bow end {lbl}", fill=NONE, stroke="#6E3A1E", strokeWidth=7,
           cap="round")

# posts over the rails: three turned uprights at the leg tops' radius
POST = {"left": (-8.6, 0), "right": (8.6, 0), "back": (0, 8.6)}
for nm in sorted(POST, key=lambda k: -depth(POST[k][0], 25, POST[k][1])):
    cx, cz = POST[nm]
    prism(f"Post {nm}", taper(cx, cz, cx * 9.4 / 8.6, cz * 9.4 / 8.6,
                              SEAT_Y + 0.1, RAIL_HI + 0.9, 0.46, 0.38,
                              ang=math.radians(45)),
          lo=0.05, hi=0.95, ink=1.5)
    prism(f"Post swell {nm}", taper(cx * 9.05 / 8.6, cz * 9.05 / 8.6,
                                    cx * 9.25 / 8.6, cz * 9.25 / 8.6,
                                    21.4, 24.2, 0.54, 0.42, ang=math.radians(45)),
          lo=0.05, hi=0.95, ink=1.4)
    ex, ey = P(cx * 9.4 / 8.6, RAIL_HI + 1.15, cz * 9.4 / 8.6)
    d.shape("ellipse", f"Post cap {nm}", x=round(ex - 5), y=round(ey - 4), width=10, height=8,
            fill=rad((0, MAH_HI), (1, MAH_D)), stroke=INK, strokeWidth=1.4)

# top-edge light along the bow's back run
rim = arc_pts(RBOW - 0.5, RAIL_HI - 0.1, -105, 105, 26)
d.path(smooth(rim, closed=False), "Bow rim light", fill=NONE, stroke="#F0C890",
       strokeWidth=2.2, opacity=30, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F2DCBE", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C89A72", justify="center")
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


caption("CORNER CHAIR", "MAHOGANY · LEATHER · BRASS")
d.finish("corner-chair-V1R00")
