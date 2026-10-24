#!/usr/bin/env python3
"""Wicker peacock chair — furniture field plate V1R00. Slight three-quarter
from the front: the rattan throne — a huge oval fan of spokes rising behind
a cane seat, scrolled cane arms, and a twisted-skirt hourglass base.
Conservatory mood: cool glasshouse light from the upper right. 1000x1000.
Modelled in inches (x right, y up, +z back), fixed yaw + pitch projection.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Wicker Peacock Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E1A12"   # warm dark, not black
EXTENT = []


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


def catmull(pts, u):
    """Sample a Catmull-Rom spline through 3D control points, u in [0,1]."""
    n = len(pts)
    f = u * (n - 1)
    i = min(n - 2, int(f))
    t = f - i
    g = lambda j: pts[max(0, min(n - 1, j))]
    p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
    out = []
    for k in range(3):
        out.append(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t +
                          (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t * t +
                          (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t ** 3))
    return tuple(out)


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(14), math.radians(15)
S, OX, OY = 9.9, 500.0, 802.0
CY, SY = math.cos(YAW), math.sin(YAW)
CP, SP = math.cos(PITCH), math.sin(PITCH)


def P(x, y, z):
    xr, zr = x * CY + z * SY, -x * SY + z * CY
    p = (OX + S * xr, OY - S * (y * CP + zr * SP))
    EXTENT.append(p)
    return p


def depth(x, y, z):
    return -x * SY * CP - y * SP + z * CY * CP


RATTAN_HI, RATTAN_MID, RATTAN_LO = "#DDB06A", "#A67C40", "#5E3E18"
RATTAN = ((0, RATTAN_LO), (0.3, RATTAN_MID), (0.52, RATTAN_HI),
          (0.74, RATTAN_MID), (1, "#46300F"))


def bar(name, a, b, r=0.5, grad=RATTAN, ink=1.8):
    """Capsule member between two 3D points, lit across its width."""
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
    assert 2 * w >= 3, "member must stay >= 3pt"
    return A, B


def ribbon(name, pts3, w0, w1, grad, ink=1.6):
    """Tapered band along a 3D polyline (screen-space ribbon)."""
    pp = [P(*p) for p in pts3]
    n = len(pp)
    left, right = [], []
    for i, q in enumerate(pp):
        a, b = pp[max(0, i - 1)], pp[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        w = w0 + (w1 - w0) * i / (n - 1)
        left.append((q[0] + nx * w, q[1] + ny * w))
        right.append((q[0] - nx * w, q[1] - ny * w))
    pts = left + right[::-1]
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    d.path(poly(pts), name, fill=lin((0, y0), (0, y1), *grad),
           stroke=INK, strokeWidth=ink, join="round")


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#141C16"), (1, "#060A07")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#5E7A62", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#3E4C40"), (0.6, "#2A362C"), (1, "#101612")),
        stroke="#0A100C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D8BC", strokeWidth=3, opacity=20)
# conservatory light: glasshouse glow from the upper right
d.shape("ellipse", "Glasshouse glow", x=430, y=70, width=560, height=520,
        fill=rad((0, "#E4F0C8", 0.20), (0.55, "#A8BC90", 0.07), (1, "#A8BC90", 0)),
        stroke=NONE)

FY = 738
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#3A4638", 42), (1, "#0C120C", 78)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#D8E4C4", strokeWidth=2, opacity=16)

# --- geometry -----------------------------------------------------------------------
# floor ring / seat ring / twisted skirt
FC = (0.0, 0.0, 5.0)          # base plan centre
RF, YF = 13.2, 1.4            # floor ring radius / height
RS, YS = 9.9, 16.6            # seat ring radius / height
SEAT_Z = 4.0
SWIRL = math.radians(52)      # skirt twist between rings
NROD = 17

# fan: oval rim leaning back LEAN, hub just behind the seat
LEAN = math.radians(10)
HUB = (0.0, 19.0, 9.6)
FAN_VC = 26.0                 # rim-ellipse centre, fan-local v above hub
FRX, FRY = 19.6, 27.0         # outer rim half-extents
FRXI, FRYI = 17.6, 24.6       # inner rim half-extents


def fan_pt(u, v):
    """Fan-local (u right, v up from hub) -> 3D, leaning back LEAN."""
    return (u, HUB[1] + v * math.cos(LEAN), HUB[2] + v * math.sin(LEAN))


def fan_ellipse(rx, ry, t0=0.0, t1=2 * math.pi, n=44):
    return [P(*fan_pt(rx * math.cos(t0 + (t1 - t0) * i / n),
                      FAN_VC + ry * math.sin(t0 + (t1 - t0) * i / n)))
            for i in range(n + 1)]


def ring_pts(cx, cz, y, r, a0=0.0, a1=2 * math.pi, n=40):
    return [P(cx + r * math.cos(a0 + (a1 - a0) * i / n), y,
              cz + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


# grounding shadow
sp = [P(FC[0] + x, 0, FC[2] + z) for x, z in ((-14, -14), (14, -14), (14, 14), (-14, 14))]
sx0, sx1 = min(p[0] for p in sp) - 26, max(p[0] for p in sp) + 26
sy0, sy1 = min(p[1] for p in sp) - 10, max(p[1] for p in sp) + 14
d.shape("ellipse", "Chair shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#030503", 66), (0.6, "#030503", 30), (1, "#030503", 0)),
        stroke=NONE)

# --- the fan: rim torus first, then spokes and weave ----------------------------------
rim_band = fan_ellipse(FRX, FRY) + fan_ellipse(FRXI, FRYI, 2 * math.pi, 0.0)
ry0, ry1 = min(p[1] for p in rim_band), max(p[1] for p in rim_band)
d.path(poly(rim_band), "Fan rim",
       fill=lin((0, ry0), (0, ry1), (0, RATTAN_HI), (0.5, RATTAN_MID),
                (1, "#4A3012")),
       stroke=INK, strokeWidth=2.4, join="round")
# inner face of the rim ring, darker — reads as the rolled edge's underside
inner_face = fan_ellipse(FRXI + 0.55, FRYI + 0.55) + fan_ellipse(FRXI, FRYI, 2 * math.pi, 0.0)
d.path(poly(inner_face), "Rim inner face", fill="#3A240C", opacity=55, stroke=NONE)

# spokes: hub -> inner rim, the fan-tail spread
NSP = 19
spoke_tips = []
for i in range(NSP):
    t = math.radians(8 + 164 * i / (NSP - 1))
    tip = (FRXI * math.cos(t), FAN_VC + FRYI * math.sin(t))
    spoke_tips.append(tip)
for i, tip in enumerate(spoke_tips):
    a = fan_pt(0.0, 1.5)
    b = fan_pt(*tip)
    bar(f"Spoke {i+1}", a, b, r=0.30, ink=1.4)

# weave: concentric arcs across the spokes at four radii fractions
for fi, f in enumerate((0.30, 0.48, 0.66, 0.84)):
    pts = []
    for tip in spoke_tips:
        u = 0.0 + (tip[0] - 0.0) * f
        v = 1.5 + (tip[1] - 1.5) * f
        pts.append(P(*fan_pt(u, v)))
    d.path(smooth(pts, closed=False), f"Weave arc {fi+1}", fill=NONE,
           stroke="#5E3E18", strokeWidth=2.6, opacity=55, cap="round")
# short radial ticks on the rim band — binding wraps
for i in range(15):
    t = math.radians(12 + 156 * i / 14)
    p0 = P(*fan_pt((FRXI + 0.4) * math.cos(t), FAN_VC + (FRYI + 0.4) * math.sin(t)))
    p1 = P(*fan_pt(FRX * math.cos(t), FAN_VC + FRY * math.sin(t)))
    d.path(f"M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}",
           f"Rim wrap {i+1}", fill=NONE, stroke="#3A240C", strokeWidth=1.8,
           opacity=35)

# peacock eyes: two curled loops low in the fan, either side of the spine
for sgn, lbl in ((-1, "L"), (1, "R")):
    ex, ey = P(*fan_pt(sgn * 5.2, 10.5))
    spir = []
    for k in range(40):
        t = k / 39 * 2.2 * math.pi
        rr = 15 * (0.85 - 0.68 * (k / 39))
        spir.append((ex + rr * math.cos(t - 0.5), ey + rr * 0.88 * math.sin(t - 0.5)))
    d.path(smooth(spir, closed=False), f"Fan curl {lbl}", fill=NONE,
           stroke="#8A6434", strokeWidth=3.4, cap="round", opacity=90)
    d.path(smooth([(x - 1.5, y - 2) for x, y in spir], closed=False),
           f"Fan curl light {lbl}", fill=NONE, stroke="#E8C98A", strokeWidth=1.5,
           cap="round", opacity=45)

# fan tail: a bound sheath from the hub down behind the seat, then two struts
ribbon("Tail bundle", [(0, 21.5, 10.0), (0, 18.0, 9.4), (0, 15.2, 8.8)],
       4.5, 8.0, ((0, "#6E4C20"), (0.5, RATTAN_MID), (1, "#4A3012")), ink=1.6)
for i, wy in enumerate((19.8, 17.6, 15.6)):
    wpts = [P(-2.6, wy, 9.3), P(0, wy - 0.5, 9.6), P(2.6, wy, 9.3)]
    d.path(smooth(wpts, closed=False), f"Tail bind {i+1}", fill=NONE,
           stroke="#3A240C", strokeWidth=3.2, opacity=65, cap="round")
for sgn in (-1, 1):
    bar(f"Tail strut {sgn}", fan_pt(0, 1.5), (sgn * 7.5, 14.0, 8.5), r=0.38, ink=1.5)


def arm(sgn, lbl):
    """Arm = the rim frame sweeping off the lower edge, forward into a scroll."""
    a0 = math.radians(-50)
    root = fan_pt(17.8 * math.cos(a0) * sgn, FAN_VC + FRYI * math.sin(a0))
    ctl = [root,
           (sgn * 12.6, 24.2, 8.5), (sgn * 13.4, 22.8, 5.0),
           (sgn * 13.4, 20.8, 1.0), (sgn * 12.9, 20.0, -3.5),
           (sgn * 11.9, 19.6, -6.8), (sgn * 10.9, 19.3, -8.0)]
    pts3 = [catmull(ctl, k / 26) for k in range(27)]
    ribbon(f"Arm {lbl}", pts3, 6.0, 3.4,
           ((0, RATTAN_HI), (0.5, RATTAN_MID), (1, RATTAN_LO)), ink=1.8)
    # cane wraps at the joints
    for k in (7, 14):
        q = P(*catmull(ctl, k / 26))
        d.shape("ellipse", f"Arm wrap {lbl} {k}", x=round(q[0] - 5), y=round(q[1] - 5),
                width=10, height=10, fill=NONE, stroke="#3A240C", strokeWidth=1.8,
                opacity=45)
    # terminal scroll: disc + spiral + eye
    ex, ey = P(*catmull(ctl, 1.0))
    d.shape("ellipse", f"Arm scroll {lbl}", x=round(ex - 15), y=round(ey - 14),
            width=30, height=27, fill=rad((0, "#E8C88A"), (0.55, "#B08648"),
            (1, "#6E4C20")), stroke=INK, strokeWidth=2.4)
    spir = []
    for k in range(36):
        t = k / 35 * 2.1 * math.pi
        rr = 11 * (0.82 - 0.66 * (k / 35))
        spir.append((ex + rr * math.cos(t - 0.6), ey + rr * 0.85 * math.sin(t - 0.6)))
    d.path(smooth(spir, closed=False), f"Arm spiral {lbl}", fill=NONE,
           stroke="#584018", strokeWidth=2.6, cap="round", opacity=85)
    d.shape("ellipse", f"Arm eye {lbl}", x=round(ex - 3.5), y=round(ey - 3.5),
            width=7, height=7, fill=rad((0, "#C8A050"), (1, "#4A3012")),
            stroke=INK, strokeWidth=1.2)

# --- skirt: twisted rods between floor ring and seat ring -----------------------------
rods = []
for i in range(NROD):
    a = 2 * math.pi * i / NROD
    b3 = (FC[0] + RF * math.cos(a), YF + 0.3, FC[2] + RF * math.sin(a))
    t3 = (FC[0] + RS * math.cos(a + SWIRL), YS - 0.4, FC[2] + RS * math.sin(a + SWIRL))
    rods.append((depth((b3[0] + t3[0]) / 2, 9, (b3[2] + t3[2]) / 2), a, b3, t3))
for dep, a, b3, t3 in sorted(r_ for r_ in rods if math.sin(r_[1]) > 0.0):
    bar(f"Rod far {a:.2f}", b3, t3, r=0.40, ink=1.5)
# far arcs of both rings
for nm, r, y in (("Floor ring far", RF, YF), ("Seat ring far", RS, YS)):
    pts = ring_pts(FC[0], FC[2], y, r, math.radians(15), math.radians(165), 26)
    d.path(smooth(pts, closed=False), nm, fill=NONE, stroke="#8A6434",
           strokeWidth=5.5, opacity=85, cap="round")

# far arm before the seat so the seat edge covers its root
arm(-1, "L")

# --- seat: cane pad + rolled rim --------------------------------------------------------
SEAT_RX, SEAT_RZ = 10.9, 8.8
seat = [P(FC[0] + SEAT_RX * math.cos(2 * math.pi * i / 40), YS + 0.6,
          SEAT_Z + SEAT_RZ * math.sin(2 * math.pi * i / 40)) for i in range(40)]
d.path(smooth(seat), "Seat pad",
       fill=rad((0, "#C89A58"), (0.55, "#96682E"), (1, "#523512")),
       stroke=INK, strokeWidth=2.2)
# cane weave: two clipped chord families across the pad
for fam in (-1, 1):
    for i in range(-6, 7):
        u0 = i * 1.55
        half = SEAT_RZ * math.sqrt(max(0.0, 1 - (u0 / SEAT_RX) ** 2))
        p0 = P(FC[0] + u0 + fam * -half * 0.55, YS + 0.7, SEAT_Z - half)
        p1 = P(FC[0] + u0 + fam * half * 0.55, YS + 0.7, SEAT_Z + half)
        d.path(f"M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}",
               f"Cane {fam},{i}", fill=NONE, stroke="#4A3012", strokeWidth=1.7,
               opacity=30)
# rolled seat rim
seat_rim = ([P(FC[0] + 11.6 * math.cos(2 * math.pi * i / 44), YS + 0.5,
               SEAT_Z + 9.4 * math.sin(2 * math.pi * i / 44)) for i in range(44)] +
            [P(FC[0] + 10.6 * math.cos(2 * math.pi * i / 44), YS + 0.5,
               SEAT_Z + 8.4 * math.sin(2 * math.pi * i / 44)) for i in range(44)][::-1])
d.path(poly(seat_rim), "Seat rim",
       fill=lin((0, min(p[1] for p in seat_rim)), (0, max(p[1] for p in seat_rim)),
                (0, RATTAN_HI), (0.55, RATTAN_MID), (1, RATTAN_LO)),
       stroke=INK, strokeWidth=2.0)

# --- skirt: near rods + near ring arcs over the seat edge ------------------------------
for dep, a, b3, t3 in sorted(r_ for r_ in rods if math.sin(r_[1]) <= 0.0):
    bar(f"Rod near {a:.2f}", b3, t3, r=0.40, ink=1.5)
for nm, r, y in (("Seat ring near", RS, YS), ("Floor ring near", RF, YF)):
    pts = ring_pts(FC[0], FC[2], y, r, math.radians(165), math.radians(375), 30)
    d.path(smooth(pts, closed=False), nm, fill=NONE, stroke=RATTAN_MID,
           strokeWidth=5.5, cap="round")
    pts_in = ring_pts(FC[0], FC[2], y, r - 0.6, math.radians(165), math.radians(375), 30)
    d.path(smooth(pts_in, closed=False), f"{nm} inner", fill=NONE,
           stroke="#3A240C", strokeWidth=1.8, opacity=60)

# near arm over everything at the seat's front-right
arm(1, "R")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 22, far


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
               color="#ECF2DC", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#ACC0A4", justify="center")
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


caption("PEACOCK CHAIR", "RATTAN · CANE · REED")
d.finish("wicker-peacock-chair-V1R00")
