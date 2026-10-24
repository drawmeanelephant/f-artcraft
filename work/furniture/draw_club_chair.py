#!/usr/bin/env python3
"""Club chair — field plate V1R00. Three-quarter view from the front right:
a leather cube softened by decades of clubs and cigars — plump rolled arms,
a deep back cushion over a sprung seat, short bun feet, worn sheen on the
arm tops and the back crown. Havana plate, low-lamplight mood. 1000x1000.
Modelled in inches (x right, y up, +z back) and projected with a fixed
yaw + pitch; volumes are 8-corner prisms with per-face leather gradients,
bolsters are swept tubes.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Club Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241410"   # warm dark, not black
EXTENT = []


def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


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


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(28), math.radians(20)
S, OX, OY = 14.8, 484.0, 748.0
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


def box(x0, y0, z0, x1, y1, z1):
    """8 corners of an axis-aligned box, near quad (-z) first, CCW from below-left."""
    return [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]


FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
TO_VIEWER = (SY * CP, SP, -CY * CP)          # normals facing this draw
LIGHT = (-0.45, 0.80, -0.42)
_l = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / _l for c in LIGHT)


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
    """Mix two hex colors at brightness b in [0,1]."""
    a = [int(hex1[i:i + 2], 16) for i in (1, 3, 5)]
    c = [int(hex2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (c[i] - a[i]) * b) for i in range(3))


LTH_D, LTH_L = "#33120C", "#8A4A32"      # aged cigar-leather ramp
LTH_HI = "#B06A48"                       # worn sheen


def prism(name, corners, lo=0.06, hi=0.94, ink=1.8):
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
        b = lo + (hi - lo) * lam ** 0.8
        y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
        g = lin((0, y0), (0, y1), (0, shade(LTH_D, LTH_L, min(1, b + 0.12))),
                                 (1, shade(LTH_D, LTH_L, b)))
        d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return faces


LTH_ROLL = ((0, "#2A0E08"), (0.28, "#A85C40"), (0.45, "#C07A54"),
            (0.62, "#7A3A26"), (1, "#33120C"))


def tube(name, a, b, r=1.1, grad=LTH_ROLL, ink=1.6):
    """Leather bolster between 3D points with rounded ends, lit across width."""
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
    return A, B


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1A1210"), (1, "#0A0605")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#9A6A42", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#6E4E34"), (0.6, "#453023"), (1, "#1E150E")),
        stroke="#120B07", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8C89A", strokeWidth=3, opacity=24)
d.shape("ellipse", "Lamplight", x=230, y=140, width=560, height=560,
        fill=rad((0, "#F0A65A", 20), (0.55, "#A86A36", 7), (1, "#6E4224", 0)),
        stroke=NONE)

FY = 676
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#5C4230", 40), (1, "#160D08", 76)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E8C898", strokeWidth=2, opacity=20)

# --- chair geometry (inches; x right, y up, +z back) ----------------------------------
BACK = (-10.5, 12.0, 4.0, 10.5, 33.0, 10.0)   # tall upholstered back slab
ARM_Y0, ARM_Y1 = 9.0, 21.0
ARM_X = (9.2, 13.6)
ARM_Z = (-5.6, 7.4)
SEAT = (-9.4, 12.2, -4.6, 9.4, 16.6, 6.8)     # cushion between the arms
BASE = (-10.8, 4.4, -5.4, 10.8, 12.6, 7.6)    # carcass below the cushion

# grounding shadow under the bun feet
feet = [P(sx * 9.6, 0, z) for sx in (-1, 1) for z in (-3.6, 6.0)]
fx0 = min(p[0] for p in feet) - 48
fx1 = max(p[0] for p in feet) + 48
fy0 = min(p[1] for p in feet) - 26
fy1 = max(p[1] for p in feet) + 26
d.shape("ellipse", "Chair shadow", x=round(fx0), y=round(fy0),
        width=round(fx1 - fx0), height=round(fy1 - fy0),
        fill=rad((0, "#050302", 70), (0.6, "#050302", 30), (1, "#050302", 0)),
        stroke=NONE)

# --- back slab, then its crown roll -----------------------------------------------------
prism("Back slab", box(*BACK), lo=0.10, hi=1.0, ink=2.0)
tube("Back crown roll", (BACK[0] + 0.4, BACK[4], (BACK[2] + BACK[5]) / 2 - 0.4),
     (BACK[3] - 0.4, BACK[4], (BACK[2] + BACK[5]) / 2 - 0.4), r=1.15)
# soft cushion pad on the back's front face
prism("Back pad", box(BACK[0] + 1.2, BACK[1] + 2.0, BACK[2] - 1.4,
                      BACK[3] - 1.2, BACK[4] - 3.0, BACK[2] - 0.2),
      lo=0.12, hi=1.0, ink=1.6)

# --- back bun feet first (occluded by the carcass), then far arm -----------------------
def bun_foot(sx, z):
    cx, cy = P(sx * 9.6, 2.6, z)
    d.shape("ellipse", f"Bun foot {sx:+d} {z}",
            x=round(cx - 13), y=round(cy - 10), width=26, height=20,
            fill=rad((0, "#6A3A22"), (0.7, "#3A1E10"), (1, "#1C0D06")),
            stroke=INK, strokeWidth=1.6)
    d.shape("ellipse", f"Foot glint {sx:+d} {z}",
            x=round(cx - 5), y=round(cy - 7), width=7, height=5,
            fill="#E8B07A", opacity=50, stroke=NONE)


for sx in (-1, 1):
    bun_foot(sx, 5.8)

# --- far arm (left), then carcass, cushion, near arm ------------------------------------
prism("Arm L", box(-ARM_X[1], ARM_Y0, ARM_Z[0], -ARM_X[0], ARM_Y1, ARM_Z[1]),
      lo=0.06, hi=0.95)
tube("Arm roll L", (-(ARM_X[0] + ARM_X[1]) / 2, ARM_Y1 + 0.2, ARM_Z[1] - 0.6),
     (-(ARM_X[0] + ARM_X[1]) / 2, ARM_Y1 + 0.4, ARM_Z[0] + 0.4), r=1.25)

prism("Carcass", box(*BASE), lo=0.04, hi=0.85)
# front apron seam
pa, pb = P(BASE[0] + 0.3, BASE[4] - 0.4, BASE[2]), P(BASE[3] - 0.3, BASE[4] - 0.4, BASE[2])
d.path(f"M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}", "Apron seam",
       fill=NONE, stroke=INK, strokeWidth=1.6, opacity=55)

# seat cushion, plump, overhanging the carcass
prism("Seat cushion", box(*SEAT), lo=0.10, hi=1.0, ink=2.0)
# cushion piping along the front and near top edge
for lbl, a, b in (("front", (SEAT[0], SEAT[4], SEAT[2]), (SEAT[3], SEAT[4], SEAT[2])),
                  ("side", (SEAT[3], SEAT[4], SEAT[2]), (SEAT[3], SEAT[4], SEAT[5]))):
    qa, qb = P(*a), P(*b)
    d.path(f"M{qa[0]:.1f},{qa[1]:.1f} L{qb[0]:.1f},{qb[1]:.1f}", f"Piping {lbl}",
           fill=NONE, stroke=INK, strokeWidth=2.0, opacity=60)
# worn sheen where the cushion crown has been sat on for decades
scx, scy = P(-1.5, SEAT[4] + 0.1, 0.5)
d.shape("ellipse", "Seat sheen", x=round(scx - 78), y=round(scy - 30),
        width=156, height=60, fill=rad((0, LTH_HI, 26), (1, LTH_HI, 0)), stroke=NONE)
# sag lines where the cushion meets each arm
for sx in (-1, 1):
    cx0 = SEAT[0] + 0.4 if sx < 0 else SEAT[3] - 0.4
    for i in range(3):
        a = P(cx0, SEAT[4] - 0.4 - i * 1.1, SEAT[2] + 1.2 + i * 1.4)
        b = P(cx0 + sx * -0.2, SEAT[4] - 0.8 - i * 1.1, SEAT[2] + 2.6 + i * 1.4)
        d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}",
               f"Crease {sx:+d} {i+1}", fill=NONE, stroke="#1C0C08",
               strokeWidth=1.6, opacity=45)

# near arm over everything at the right
prism("Arm R", box(ARM_X[0], ARM_Y0, ARM_Z[0], ARM_X[1], ARM_Y1, ARM_Z[1]),
      lo=0.06, hi=1.0)
tube("Arm roll R", ((ARM_X[0] + ARM_X[1]) / 2, ARM_Y1 + 0.2, ARM_Z[1] - 0.6),
     ((ARM_X[0] + ARM_X[1]) / 2, ARM_Y1 + 0.4, ARM_Z[0] + 0.4), r=1.25)

# worn sheen where decades of forearms polished the tops
for sx in (-1, 1):
    ax = sx * (ARM_X[0] + ARM_X[1]) / 2
    hx, hy = P(ax, ARM_Y1 + 0.6, -0.5)
    d.shape("ellipse", f"Arm sheen {sx:+d}", x=round(hx - 34), y=round(hy - 20),
            width=68, height=40,
            fill=rad((0, LTH_HI, 34), (1, LTH_HI, 0)), stroke=NONE)
bhx, bhy = P(0, BACK[4] - 1.4, BACK[2] - 1.0)
d.shape("ellipse", "Back sheen", x=round(bhx - 70), y=round(bhy - 26),
        width=140, height=52, fill=rad((0, LTH_HI, 22), (1, LTH_HI, 0)), stroke=NONE)

# --- front bun feet, nearest the viewer --------------------------------------------------
for sx in (-1, 1):
    bun_foot(sx, -3.4)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far


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
               color="#F4E4CE", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C9A582", justify="center")
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


caption("CLUB CHAIR", "CIGAR LEATHER · BEECH · HORSEHAIR")
d.finish("club-chair-V1R00")
