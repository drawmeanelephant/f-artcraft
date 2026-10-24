#!/usr/bin/env python3
"""Steamer trunk — field plate V1R00. A flat-top ocean trunk: canvas-covered
carcass ribbed with oak slats, iron corner caps, two leather straps thrown
over the lid, brass lock and a leather grab handle on the near end. Two
blank paper labels — no line names — say where it has been. Seen from
front-right, above. Slate plate, boarding mood. 1000x1000.
Modelled in inches (x right, y up, +z back), fixed yaw + pitch.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Steamer Trunk — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1C1208"
EXTENT = []


def stops(*pairs):
    return [{"offset": p[0], "color": p[1], **({"opacity": p[2]} if len(p) > 2 else {})}
            for p in pairs]


def lin(a, b, *pairs):
    return {"gradient": {"kind": "linear", "start": [round(a[0], 1), round(a[1], 1)],
                         "end": [round(b[0], 1), round(b[1], 1)], "stops": stops(*pairs)}}


def rad(*pairs):
    return {"gradient": {"kind": "radial", "stops": stops(*pairs)}}


def poly(pts):
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(26), math.radians(22)
S, OX, OY = 11.5, 505.0, 630.0
CY, SY = math.cos(YAW), math.sin(YAW)
CP, SP = math.cos(PITCH), math.sin(PITCH)


def P(x, y, z):
    xr, zr = x * CY + z * SY, -x * SY + z * CY
    p = (OX + S * xr, OY - S * (y * CP + zr * SP))
    EXTENT.append(p)
    return p


def depth(x, y, z):
    return -x * SY * CP - y * SP + z * CY * CP


def box(x0, y0, z0, x1, y1, z1):
    return [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]


FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
TO_VIEWER = (SY * CP, SP, -CY * CP)
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
    a = [int(hex1[i:i + 2], 16) for i in (1, 3, 5)]
    c = [int(hex2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (c[i] - a[i]) * b) for i in range(3))


# palettes: (dark, light) ramps per material
CAN_D, CAN_L = "#4E4A30", "#98905E"      # drab canvas
OAK_D, OAK_L = "#4A2C14", "#A87B44"      # oak slats
LEA_D, LEA_L = "#3A1E10", "#8A5430"      # leather straps
IRON_D, IRON_L = "#26241F", "#5E5A4E"    # corner caps, banding
BRASS_D, BRASS_L = "#8A6224", "#F6DE96"


def prism(name, corners, dark=CAN_D, light=CAN_L, lo=0.06, hi=0.94, ink=1.8):
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
        g = lin((0, y0), (0, y1), (0, shade(dark, light, min(1, b + 0.12))),
                                 (1, shade(dark, light, b)))
        d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return faces


def quad3(name, pts3, fill, stroke=NONE, sw=1.6, opacity=None):
    kw = {"fill": fill}
    if stroke != NONE:
        kw.update(stroke=stroke, strokeWidth=sw, join="round")
    else:
        kw["stroke"] = NONE
    if opacity is not None:
        kw["opacity"] = opacity
    d.path(poly([P(*p) for p in pts3]), name, **kw)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#101214"), (1, "#050607")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#5E6A66", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#4A5450"), (0.6, "#2E3834"), (1, "#121816")),
        stroke="#0A0E0C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D4C8", strokeWidth=3, opacity=22)
d.shape("ellipse", "Dock light", x=190, y=110, width=600, height=560,
        fill=rad((0, "#F0D89A", 14), (0.55, "#A89050", 5), (1, "#6E5A30", 0)),
        stroke=NONE)

FY = 645
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#3A4038", 42), (1, "#0C0E0A", 78)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#D8DCC8", strokeWidth=2, opacity=20)

# grounding shadow
sh = [P(x, 0, z) for x in (-20, 20) for z in (-11, 11)]
sx0, sx1 = min(p[0] for p in sh) - 44, max(p[0] for p in sh) + 44
sy0, sy1 = min(p[1] for p in sh) - 22, max(p[1] for p in sh) + 28
d.shape("ellipse", "Trunk shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#040505", 66), (0.6, "#040505", 26), (1, "#040505", 0)),
        stroke=NONE)

# --- geometry (inches) -----------------------------------------------------------------
X0, X1 = -19.0, 19.0
Z0, Z1 = -10.0, 10.0
Y0, Y1 = 1.6, 20.5          # carcass; small foot rail below
LT = 1.6                    # lid band thickness

# --- carcass: canvas shell --------------------------------------------------------------
prism("Carcass", box(X0, Y0, Z0, X1, Y1, Z1), dark=CAN_D, light=CAN_L,
      lo=0.12, hi=1.0, ink=2.0)
# canvas weave hint: faint horizontal seams on the front face
for i, sy_ in enumerate((Y0 + 4.5, Y0 + 9.5, Y0 + 14.5)):
    a, b = P(X0 + 1.5, sy_, Z0 - 0.05), P(X1 - 1.5, sy_ + 0.3, Z0 - 0.05)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Canvas seam {i+1}",
           fill=NONE, stroke="#3A3820", strokeWidth=1.6, opacity=35, cap="round")

# --- lid band: a slab capping the carcass ------------------------------------------------
prism("Lid band", box(X0 - 0.4, Y1, Z0 - 0.4, X1 + 0.4, Y1 + LT, Z1 + 0.4),
      dark="#5E5233", light="#B0A468", lo=0.10, hi=1.0, ink=2.0)
# seam between lid and body along the front + right
a, b = P(X0 - 0.4, Y1 - 0.15, Z0 - 0.45), P(X1 + 0.4, Y1 - 0.15, Z0 - 0.45)
d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", "Lid seam front",
       fill=NONE, stroke="#14100A", strokeWidth=3.2, opacity=60, cap="round")

# --- oak slats: vertical ribs on the front face, continuing over the lid -----------------
for i, sx_ in enumerate((-15.0, -9.0, -3.0, 3.0, 9.0, 15.0)):
    prism(f"Slat front {i+1}", box(sx_ - 0.75, Y0, Z0 - 0.55, sx_ + 0.75, Y1, Z0 - 0.05),
          dark=OAK_D, light=OAK_L, lo=0.15, hi=1.0, ink=1.5)
    prism(f"Slat top {i+1}", box(sx_ - 0.75, Y1 + LT, Z0 - 0.4, sx_ + 0.75, Y1 + LT + 0.55, Z1 + 0.4),
          dark=OAK_D, light=OAK_L, lo=0.15, hi=1.0, ink=1.5)
# matching slats on the right end face (+x)
for i, sz_ in enumerate((-5.5, 0.5, 6.5)):
    prism(f"Slat end {i+1}", box(X1 - 0.05, Y0, sz_ - 0.75, X1 + 0.55, Y1, sz_ + 0.75),
          dark=OAK_D, light=OAK_L, lo=0.15, hi=1.0, ink=1.5)

# --- iron corner posts: full-height bound posts at the three near corners ------------------
for nm, cx0, cx1, cz0, cz1 in (("FL", X0 - 0.35, X0 + 1.6, Z0 - 0.55, Z0 + 1.6),
                              ("FR", X1 - 1.6, X1 + 0.35, Z0 - 0.55, Z0 + 1.6),
                              ("BR", X1 - 1.6, X1 + 0.35, Z1 - 1.6, Z1 + 0.35)):
    prism(f"Corner {nm}", box(cx0, Y0 - 0.3, cz0, cx1, Y1 + LT + 0.2, cz1),
          dark=IRON_D, light=IRON_L, lo=0.15, hi=1.0, ink=1.7)
# rivets along the slat fronts
for i, sx_ in enumerate((-15.0, -9.0, -3.0, 3.0, 9.0, 15.0)):
    for j, ry in enumerate((Y0 + 1.2, Y1 - 1.2)):
        rx, ry2 = P(sx_, ry, Z0 - 0.6)
        d.shape("ellipse", f"Rivet {i+1}.{j+1}", x=round(rx - 2.2), y=round(ry2 - 2.2),
                width=4.4, height=4.4,
                fill=rad((0, "#E8E4D4"), (1, "#6E6A58")), stroke="#1C1A14", strokeWidth=0.8)

# --- leather straps: two, running over the lid and down the front ------------------------
for i, sx_ in enumerate((-10.5, 10.5)):
    # strap down the front face
    prism(f"Strap front {i+1}", box(sx_ - 1.15, Y0 - 0.4, Z0 - 0.85, sx_ + 1.15, Y1 + LT, Z0 - 0.6),
          dark=LEA_D, light=LEA_L, lo=0.12, hi=1.0, ink=1.7)
    # strap over the lid
    prism(f"Strap top {i+1}", box(sx_ - 1.15, Y1 + LT + 0.5, Z0 - 0.4, sx_ + 1.15,
                                  Y1 + LT + 1.05, Z1 + 0.4),
          dark=LEA_D, light=LEA_L, lo=0.12, hi=1.0, ink=1.7)
    # buckle on the front strap
    bx, by = P(sx_, Y0 + 5.2, Z0 - 0.95)
    d.path(f"M{bx - 7:.1f},{by - 5:.1f} L{bx + 7:.1f},{by - 5:.1f} L{bx + 7:.1f},{by + 5:.1f} L{bx - 7:.1f},{by + 5:.1f} Z",
           f"Buckle {i+1}", fill=NONE, stroke="#D8B25E", strokeWidth=2.6, join="round")
    d.path(f"M{bx - 7:.1f},{by:.1f} L{bx + 7:.1f},{by:.1f}", f"Buckle bar {i+1}",
           fill=NONE, stroke="#D8B25E", strokeWidth=2.0)

# --- brass lock + hasp at the lid front centre ---------------------------------------------
hx_, hy = P(0, Y1 - 1.2, Z0 - 0.95)
d.path(f"M{hx_ - 8:.1f},{hy - 9:.1f} L{hx_ + 8:.1f},{hy - 9:.1f} L{hx_ + 8:.1f},{hy + 7:.1f} L{hx_ - 8:.1f},{hy + 7:.1f} Z",
       "Lock plate", fill=lin((hx_ - 8, hy), (hx_ + 8, hy), (0, "#F2DA94"), (1, "#9A7028")),
       stroke="#4A340E", strokeWidth=1.6)
d.shape("ellipse", "Keyhole", x=round(hx_ - 2.2), y=round(hy - 1), width=4.4, height=6,
        fill="#1E0E04", stroke=NONE)
# hasp tab above the lock, over the lid seam
ha = P(0, Y1 + 0.6, Z0 - 0.9)
d.path(f"M{ha[0] - 5:.1f},{ha[1] - 6:.1f} L{ha[0] + 5:.1f},{ha[1] - 6:.1f} L{ha[0] + 5:.1f},{ha[1] + 4:.1f} L{ha[0] - 5:.1f},{ha[1] + 4:.1f} Z",
       "Hasp", fill=lin((ha[0], ha[1] - 6), (ha[0], ha[1] + 4), (0, "#C8A04A"), (1, "#7A5420")),
       stroke="#4A340E", strokeWidth=1.4)

# --- leather grab handle on the right end face ----------------------------------------------
# two brackets + a sagging grip across the +x end
for i, hz in enumerate((-4.0, 3.6)):
    prism(f"Handle mount {i+1}", box(X1 + 0.05, Y0 + 9.0, hz, X1 + 0.9, Y0 + 11.4, hz + 1.4),
          dark=IRON_D, light=IRON_L, lo=0.2, hi=1.0, ink=1.4)
h0 = P(X1 + 0.9, Y0 + 10.2, -3.6)
h1 = P(X1 + 0.9, Y0 + 10.2, 4.0)
hm = P(X1 + 2.2, Y0 + 8.6, 0.2)
d.path(f"M{h0[0]:.1f},{h0[1]:.1f} Q{hm[0]:.1f},{hm[1]:.1f} {h1[0]:.1f},{h1[1]:.1f}",
       "Handle grip", fill=NONE, stroke="#4A2A16", strokeWidth=6.5, cap="round")
d.path(f"M{h0[0]:.1f},{h0[1] - 1:.1f} Q{hm[0]:.1f},{hm[1] - 2:.1f} {h1[0]:.1f},{h1[1] - 1:.1f}",
       "Handle light", fill=NONE, stroke="#8A5430", strokeWidth=2.4, cap="round", opacity=70)

# --- travel labels: two blank paper labels on the canvas front ------------------------------
lab = [(-13.5, Y0 + 11.5, 5.5, 3.6, -6), (-6.0, Y0 + 7.8, 4.6, 3.2, 9)]
for i, (lx, ly, lw, lh, rot) in enumerate(lab):
    t = math.radians(rot)
    c0 = P(lx, ly, Z0 - 0.62)
    ux = (math.cos(t) * lw / 2 * S, math.sin(t) * lw / 2 * S)
    uy = (-math.sin(t) * lh / 2 * S, math.cos(t) * lh / 2 * S)
    pts = [(c0[0] - ux[0] - uy[0], c0[1] - ux[1] - uy[1]),
           (c0[0] + ux[0] - uy[0], c0[1] + ux[1] - uy[1]),
           (c0[0] + ux[0] + uy[0], c0[1] + ux[1] + uy[1]),
           (c0[0] - ux[0] + uy[0], c0[1] - ux[1] + uy[1])]
    d.path(poly(pts), f"Label {i+1}",
           fill=lin((pts[0][0], pts[0][1]), (pts[2][0], pts[2][1]),
                    (0, "#E4DCC0"), (1, "#B0A680")), stroke="#6E6244", strokeWidth=1.5)
    # two scribble lines — no words
    for j in range(2):
        ly_ = c0[1] + uy[1] * (-0.4 + 0.5 * j)
        lx_ = c0[0] + uy[0] * (-0.4 + 0.5 * j)
        d.path(f"M{lx_ - ux[0] * 0.55:.1f},{ly_ - ux[1] * 0.55:.1f} L{lx_ + ux[0] * 0.55:.1f},{ly_ + ux[1] * 0.55:.1f}",
               f"Label {i+1} line {j+1}", fill=NONE, stroke="#8A8060", strokeWidth=1.6,
               opacity=60, cap="round")

# worn scuffs along the bottom rail
for i, (sx_, sw_) in enumerate(((-16, 2.8), (-4, 3.6), (7, 2.2), (15.5, 3.0))):
    a, b = P(sx_, Y0 + 1.1, Z0 - 0.06), P(sx_ + sw_, Y0 + 1.4, Z0 - 0.06)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Scuff {i+1}",
           fill=NONE, stroke="#B8AE7C", strokeWidth=2.4, opacity=30, cap="round")

# top sheen where dock light grazes the lid
gx, gy = P(-4, Y1 + LT + 0.4, -3)
d.shape("ellipse", "Lid sheen", x=round(gx - 100), y=round(gy - 28), width=200, height=56,
        fill=rad((0, "#D8CC90", 20), (1, "#D8CC90", 0)), stroke=NONE)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("trunk extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#EAE8D8", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#A8B4A8", justify="center")
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


caption("STEAMER TRUNK", "CANVAS · OAK · BRASS")
d.finish("steamer-trunk-V1R00")
