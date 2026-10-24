#!/usr/bin/env python3
"""Spring-arm desk lamp — furniture field plate V1R00. Anglepoise type in
near-side view with a slight three-quarter: a stepped steel base, twin
parallel arm bars with bright extension springs, and a green enamel bell
shade tilted over the work, warm light pooling on the desk below. A flex
cord droops from the head back to the base. Draughtsman mood: slate-teal
plate, tungsten pool. 1000x1000. Modelled in inches (x lateral, y up,
+z toward the front of the desk), projected with a fixed yaw + pitch;
rounded parts are convex hulls of projected ring samples.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Spring-Arm Desk Lamp — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1C140C"   # warm dark, never black
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
YAW, PITCH = math.radians(31), math.radians(15)
S, OX, OY = 14.2, 498.0, 762.0
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


def vlen(a):
    return math.sqrt(sum(c * c for c in a))


def vunit(a):
    l = vlen(a)
    return tuple(c / l for c in a)


def ring(c, u, r, n=42):
    """Sample a 3D circle of radius r centred on c in the plane normal to u."""
    ref = (1, 0, 0) if abs(u[0]) < 0.9 else (0, 1, 0)
    a = vunit(cross3(u, ref))
    b = cross3(u, a)
    return [tuple(c[i] + r * (math.cos(2 * math.pi * k / n) * a[i] +
                            math.sin(2 * math.pi * k / n) * b[i]) for i in range(3))
            for k in range(n)]


def hull(pts):
    """2D convex hull (monotonic chain) of projected points."""
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


STEEL = ((0, "#39424A"), (0.3, "#8A98A2"), (0.52, "#C8D2D8"), (0.72, "#5A646C"), (1, "#2A3036"))
ENAMEL = ((0, "#2E8A58"), (0.35, "#17603C"), (0.7, "#0C3822"), (1, "#062014"))


def tube(name, a, b, r=0.5, grad=STEEL, sw=2.0):
    """Round bar between 3D endpoints: hull of two end rings, lit across."""
    u = vunit(sub(b, a))
    pts = [P(*p) for p in ring(a, u, r) + ring(b, u, r)]
    h = hull(pts)
    # gradient axis = screen perpendicular of the bar
    pa, pb = P(*a), P(*b)
    dx, dy = pb[0] - pa[0], pb[1] - pa[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    w = r * S * 1.05
    cx, cy = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
    g = lin((cx + nx * w, cy + ny * w), (cx - nx * w, cy - ny * w), *grad)
    d.path(poly(h), name, fill=g, stroke=INK, strokeWidth=sw, join="round")
    return pa, pb


def spring(name, a, b, coils=11, amp=0.75, lead=0.14):
    """Extension spring: bright zigzag coil over an ink under-stroke."""
    pa, pb = P(*a), P(*b)
    dx, dy = pb[0] - pa[0], pb[1] - pa[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    A = amp * S
    pts = [pa, (pa[0] + ux * L * lead, pa[1] + uy * L * lead)]
    n = coils * 2
    for k in range(1, n):
        t = lead + (1 - 2 * lead) * k / n
        off = A if k % 2 else -A
        px, py = pa[0] + ux * L * t + nx * off, pa[1] + uy * L * t + ny * off
        pts.append((px, py))
        if k in (1, n - 1):
            ext(px, py)
    pts.append((pa[0] + ux * L * (1 - lead), pa[1] + uy * L * (1 - lead)))
    pts.append(pb)
    dd = "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:])
    d.path(dd, name + " edge", fill=NONE, stroke=INK, strokeWidth=5.4, join="round", cap="round")
    d.path(dd, name, fill=NONE, stroke="#C8D2DA", strokeWidth=3.0, join="round", cap="round")
    d.path(dd, name + " sheen", fill=NONE, stroke="#F2F8FA", strokeWidth=1.2,
           opacity=55, join="round", cap="round")


def cyl(name, cx, cz, r, y0, y1, grad, sw=2.0):
    """Vertical-axis cylinder silhouette + top face."""
    pts = [P(*p) for p in ring((cx, y0, cz), (0, 1, 0), r) + ring((cx, y1, cz), (0, 1, 0), r)]
    h = hull(pts)
    x0 = min(p[0] for p in h)
    x1 = max(p[0] for p in h)
    d.path(poly(h), name, fill=lin((x0, 0), (x1, 0), *grad),
           stroke=INK, strokeWidth=sw, join="round")
    return h


def topring(name, cx, cz, r, y, grad, sw=1.8):
    """Visible top face of a horizontal cylinder."""
    pts = [P(*p) for p in ring((cx, y, cz), (0, 1, 0), r)]
    d.path(poly(pts), name, fill=grad, stroke=INK, strokeWidth=sw, join="round")


def disc3(name, c, u, r, grad, sw=0):
    """Filled disc in an arbitrary plane: projected ring polygon."""
    pts = [P(*p) for p in ring(c, u, r)]
    kw = {"fill": grad, "join": "round"}
    if sw:
        kw.update(stroke=INK, strokeWidth=sw)
    else:
        kw["stroke"] = NONE
    d.path(poly(pts), name, **kw)


# --- backdrop + plate ------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#101E20"), (1, "#050A0B")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7A9090", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#46584F"), (0.55, "#2C3A34"), (1, "#141D19")),
        stroke="#0C1410", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8DAD0", strokeWidth=3, opacity=24)

# desk surface: band closing on the disc's own arc
FYB = 706
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX - hw:.1f},{FYB} L{PCX + hw:.1f},{FYB} A420,420 0 0 0 {PCX - hw:.1f},{FYB} Z",
       "Desk", fill=lin((0, FYB), (0, 880), (0, "#3E3A2C", 0.42), (0.5, "#26221A", 0.72),
                        (1, "#12100A", 0.9)), stroke=NONE)
d.path(f"M{PCX - hw + 6:.1f},{FYB} L{PCX + hw - 6:.1f},{FYB}", "Desk edge light",
       fill=NONE, stroke="#B8C4AE", strokeWidth=2, opacity=16)
for i, yb in enumerate([748, 792, 836]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Desk seam {i+1}",
           fill=NONE, stroke="#4E4A38", strokeWidth=2, opacity=24)

# --- lamp geometry (inches) -------------------------------------------------------------
# base stack: two stepped tiers + socket dome, centred z=0
BASE_Z = 0.5
cyl("Base tier", 0, BASE_Z, 6.6, 0, 1.5,
    ((0, "#5A646C"), (0.4, "#9AA8B0"), (0.75, "#3E464E"), (1, "#22282E")))
topring("Base tier top", 0, BASE_Z, 6.6, 1.5,
        rad((0, "#8A98A2"), (0.7, "#5A646C"), (1, "#3A424A")))
cyl("Base step", 0, BASE_Z, 4.6, 1.3, 2.7,
    ((0, "#6E7A82"), (0.45, "#B4C0C6"), (0.75, "#4A545C"), (1, "#2A3238")))
topring("Base step top", 0, BASE_Z, 4.6, 2.7,
        rad((0, "#AEBAC0"), (0.7, "#6E7A82"), (1, "#454F56")))
cyl("Socket dome", 0, BASE_Z - 0.4, 2.9, 2.5, 3.6,
    ((0, "#7E8A92"), (0.5, "#C2CCD2"), (1, "#3A444C")))
# switch knob standing on the base step top, near side
kn = P(-2.4, 3.1, BASE_Z + 3.2)
d.shape("ellipse", "Switch knob", x=round(kn[0] - 7), y=round(kn[1] - 9), width=14, height=18,
        fill=rad((0, "#F0D08A"), (0.6, "#B08030"), (1, "#5A3C12")), stroke=INK, strokeWidth=1.6)

# shadow under the base
feet = [P(sx * 6.6, 0, BASE_Z + sz * 6.6) for sx in (-1, 1) for sz in (-1, 1)]
fx0, fx1 = min(p[0] for p in feet) - 26, max(p[0] for p in feet) + 26
fy0, fy1 = min(p[1] for p in feet) - 14, max(p[1] for p in feet) + 18
d.shape("ellipse", "Base shadow", x=round(fx0), y=round(fy0), width=round(fx1 - fx0),
        height=round(fy1 - fy0),
        fill=rad((0, "#030503", 0.66), (0.6, "#030503", 0.3), (1, "#030503", 0)), stroke=NONE)

# arm joints (side view: z,y)
PV = (-2.0, 6.0)      # base pivot
EL = (11.0, 22.4)     # elbow
HP = (4.6, 32.8)      # head pivot
ARMX = 1.35           # lateral half-spacing of the twin bars

# pivot post on the base
tube("Pivot post", (0, 2.8, PV[0] + 0.4), (0, PV[1] + 0.6, PV[0]), r=1.05)

# far arm bars first (drawn under), then springs, then near bars
for sx in (1, -1):
    tube(f"Lower arm bar {sx:+d}", (sx * ARMX, PV[1], PV[0]), (sx * ARMX, EL[1], EL[0]), r=0.48)
    tube(f"Upper arm bar {sx:+d}", (sx * ARMX, EL[1], EL[0]), (sx * ARMX, HP[1], HP[0]), r=0.44)

# extension springs: lower pair from base anchor to lower arm, upper from
# elbow bracket back along the upper arm
for sx, tag in ((-1, "near"), (1, "far")):
    xa = sx * (ARMX + 0.15)
    spring(f"Lower spring {tag}", (xa, 4.4, -3.6),
           (xa, PV[1] + 0.68 * (EL[1] - PV[1]), PV[0] + 0.68 * (EL[0] - PV[0])),
           coils=10, amp=0.62)
    spring(f"Upper spring {tag}", (xa, EL[1] - 1.6, EL[0] + 1.9),
           (xa, EL[1] + 0.62 * (HP[1] - EL[1]), EL[0] + 0.62 * (HP[0] - EL[0])),
           coils=8, amp=0.55)
# spring anchor lugs
for sx in (-1, 1):
    lu = P(sx * ARMX, 4.6, -3.4)
    d.shape("ellipse", f"Spring lug {sx:+d}", x=round(lu[0] - 6), y=round(lu[1] - 6),
            width=12, height=12, fill=rad((0, "#8A98A2"), (1, "#3A424A")),
            stroke=INK, strokeWidth=1.6)

# joint knuckles + brass bolts
for nm, (z, y), rr in (("Pivot knuckle", PV, 1.5), ("Elbow knuckle", EL, 1.7),
                       ("Head knuckle", HP, 1.35)):
    kp = P(0, y, z)
    d.shape("ellipse", nm, x=round(kp[0] - rr * S), y=round(kp[1] - rr * S),
            width=round(2 * rr * S), height=round(2 * rr * S),
            fill=rad((0, "#8A98A2"), (0.6, "#4E585F"), (1, "#262C32")),
            stroke=INK, strokeWidth=2.2)
    bp = P(-ARMX - 0.55, y, z)
    d.shape("ellipse", nm + " bolt", x=round(bp[0] - 6.5), y=round(bp[1] - 6.5),
            width=13, height=13, fill=rad((0, "#FFF0B8"), (0.55, "#D2A24A"), (1, "#7A5418")),
            stroke=INK, strokeWidth=1.6)

# --- the enamel bell shade ------------------------------------------------------------------
# frustum: neck at the head pivot, mouth tilted down over the work
NECK = (0, HP[1] + 0.3, HP[0] + 0.35)
AXIS = vunit(sub((0, 25.2, 8.4), NECK))     # neck -> mouth centre
MLEN = 6.8
MOUTH = tuple(NECK[i] + MLEN * AXIS[i] for i in range(3))
RN, RM = 1.35, 4.7
neckr = ring(NECK, AXIS, RN)
mouthr = ring(MOUTH, AXIS, RM)
bell = hull([P(*p) for p in neckr + mouthr])
np2, mp2 = P(*NECK), P(*MOUTH)
# shell: gradient keyed neck->mouth, bright enamel shoulder to dark rim
d.path(poly(bell), "Shade shell",
       fill=lin(np2, mp2, *ENAMEL), stroke=INK, strokeWidth=2.6, join="round")
# enamel specular streak along the shoulder
sx0 = tuple(NECK[i] + 1.6 * AXIS[i] for i in range(3))
sx1 = tuple(NECK[i] + 4.4 * AXIS[i] for i in range(3))
sa, sb = P(sx0[0] - RN * 0.55, sx0[1], sx0[2]), P(sx1[0] - RM * 0.5, sx1[1], sx1[2])
d.path(f"M{sa[0]:.1f},{sa[1]:.1f} L{sb[0]:.1f},{sb[1]:.1f}", "Shade streak",
       fill=NONE, stroke="#9AE0B4", strokeWidth=4.5, opacity=38, cap="round")
# mouth interior: warm reflector, then the rolled rim over its edge
disc3("Shade mouth", MOUTH, AXIS, RM * 0.985,
      rad((0, "#FFF0C0"), (0.45, "#F2C878"), (0.8, "#A06A28"), (1, "#5E3A14")))
# rolled rim: re-stroke the mouth ring
pts_m = [P(*p) for p in mouthr]
d.path(poly(pts_m), "Shade rim", fill=NONE, stroke=INK, strokeWidth=3.0, join="round")
d.path(poly(pts_m), "Rim edge light", fill=NONE, stroke="#7AD8A2", strokeWidth=1.4,
       opacity=50, join="round")
# brass neck ring where the shade meets the head knuckle
disc3("Neck collar", NECK, AXIS, RN * 1.02,
      rad((0, "#D8AC58"), (0.6, "#9A6E26"), (1, "#503610")), sw=1.6)
# bulb peeking inside the mouth
bulb = P(*tuple(MOUTH[i] - 1.0 * AXIS[i] for i in range(3)))
d.shape("ellipse", "Bulb", x=round(bulb[0] - 13), y=round(bulb[1] - 13), width=26, height=26,
        fill=rad((0, "#FFF8E2"), (0.55, "#FFE0A0"), (1, "#E8A84E", 0)), stroke=NONE)
ext(bulb[0] - 13, bulb[1] - 13); ext(bulb[0] + 13, bulb[1] + 13)

# --- light thrown by the lamp ----------------------------------------------------------------
# beam cone from the mouth ring down to the desk pool
mxl = [P(*p) for p in mouthr]
mleft = min(mxl, key=lambda p: p[0])
mright = max(mxl, key=lambda p: p[0])
pool_c = P(0, 0.05, MOUTH[2] + 4.2)
pcx, pcy = pool_c
ext(pcx - 150, pcy); ext(pcx + 150, pcy)
d.path(f"M{mleft[0]:.1f},{mleft[1]:.1f} L{mright[0]:.1f},{mright[1]:.1f} "
       f"L{pcx + 150:.1f},{pcy + 10:.1f} L{pcx - 150:.1f},{pcy + 10:.1f} Z",
       "Beam", fill=lin((0, mleft[1]), (0, pcy),
                        (0, "#FFCE8A", 0.20), (0.55, "#FFB464", 0.07), (1, "#FFB464", 0)),
       stroke=NONE)
d.shape("ellipse", "Light pool", x=round(pcx - 150), y=round(pcy - 34), width=300, height=88,
        fill=rad((0, "#F2C878", 0.42), (0.55, "#B08A48", 0.16), (1, "#7A5E28", 0)),
        stroke=NONE)
ext(pcx - 150, pcy - 34); ext(pcx + 150, pcy + 54)
# warm bloom round the head
bx0, by0 = mp2
d.shape("ellipse", "Head bloom", x=round(bx0 - 120), y=round(by0 - 110), width=240, height=210,
        fill=rad((0, "#FFCE8A", 0.14), (0.6, "#C88A44", 0.05), (1, "#C88A44", 0)), stroke=NONE)
ext(bx0 - 120, by0 - 110); ext(bx0 + 120, by0 + 100)
# dust motes in the beam
for i, (mx_, my_, mr_) in enumerate([(0.32, 0.38, 1.8), (0.5, 0.52, 1.4), (0.62, 0.45, 2.0),
                                     (0.42, 0.66, 1.5), (0.55, 0.74, 1.8), (0.72, 0.6, 1.3)]):
    mx = mleft[0] + (mright[0] - mleft[0]) * mx_ + (pcx - (mleft[0] + mright[0]) / 2) * my_
    my = mleft[1] + (pcy - mleft[1]) * my_
    ext(mx, my)
    d.shape("ellipse", f"Mote {i+1}", x=round(mx - mr_), y=round(my - mr_),
            width=round(mr_ * 2), height=round(mr_ * 2), fill="#FFE8C0", opacity=26, stroke=NONE)

# --- flex cord: from the head pivot, drooping back to the base ----------------------------
cord = [P(0.6, HP[1] - 0.4, HP[0] - 0.5), P(1.0, 28, -1.5), P(1.2, 20, -5.2),
        P(1.0, 12, -6.6), P(0.6, 5.5, -5.6), P(0.2, 3.0, BASE_Z - 3.2)]
d.path(smooth(cord), "Cord edge", fill=NONE, stroke=INK, strokeWidth=5.0, cap="round")
d.path(smooth(cord), "Cord", fill=NONE, stroke="#3A3230", strokeWidth=3.2, cap="round")
d.path(smooth([(x, y - 1) for x, y in cord[:4]]), "Cord sheen", fill=NONE,
       stroke="#8A8078", strokeWidth=1.4, opacity=45, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("lamp extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#E8F0EA", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#A8BEB4", justify="center")
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


caption("SPRING-ARM DESK LAMP", "ENAMELLED STEEL · SPRINGS · BRASS")
d.finish("spring-arm-desk-lamp-V1R00")
