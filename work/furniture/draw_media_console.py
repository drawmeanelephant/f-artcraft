#!/usr/bin/env python3
"""Media console — field plate V1R00. Three-quarter view from front-right-above:
a long low walnut credenza sized to the black wall-mounted screen above it —
two fluted doors flanking an open centre bay (record spines, a small amp),
slab top, splayed tapered legs with brass ferrules. A soundbar, a book stack
and a little potted plant dress the top. Walnut plate, living-room mood.
1000x1000. Modelled in inches (x right, y up, +z back); face-culled prisms,
yaw+pitch. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Media Console — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E0E05"
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


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(28), math.radians(22)
S, OX, OY = 9.3, 500.0, 690.0
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


def taper_box(wt, wb, ht0, ht1, cx, cz, sx=0.0, sz=0.0):
    """Tapered splayed leg: wt half-width at top, wb at bottom; splay offsets
    the foot outward by (sx, sz). Same vertex ordering as box()."""
    return [(cx - wb + sx, ht0, cz - wb + sz), (cx + wb + sx, ht0, cz - wb + sz),
            (cx + wt, ht1, cz - wt), (cx - wt, ht1, cz - wt),
            (cx - wb + sx, ht0, cz + wb + sz), (cx + wb + sx, ht0, cz + wb + sz),
            (cx + wt, ht1, cz + wt), (cx - wt, ht1, cz + wt)]


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


# palettes: (dark, light) ramps per material
WAL_D, WAL_L = "#38200E", "#8A5628"      # walnut
WAL_HI = "#C08A50"
BRASS_D, BRASS_L = "#6E4E1E", "#E2BC66"
EBONY_D, EBONY_L = "#0E0E12", "#3C3C48"  # screen / soundbar
POT_D, POT_L = "#5A2C18", "#B86838"      # terracotta


def prism(name, corners, dark=WAL_D, light=WAL_L, lo=0.06, hi=0.94, ink=1.8):
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


def seg3(name, pts3, stroke, sw, opacity=None, dash=None):
    """Polyline through 3D points, no culling."""
    kw = {"fill": NONE, "stroke": stroke, "strokeWidth": sw, "cap": "round"}
    if opacity is not None:
        kw["opacity"] = opacity
    if dash is not None:
        kw["dash"] = dash
    q = [P(*p) for p in pts3]
    d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in q), name, **kw)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#18100A"), (1, "#070402")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#A8763F", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#6B4A2C"), (0.6, "#3E2716"), (1, "#140B05")),
        stroke="#100A05", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EEC89A", strokeWidth=3, opacity=24)
d.shape("ellipse", "Lamplight", x=170, y=130, width=560, height=520,
        fill=rad((0, "#F2C880", 18), (0.55, "#B8864A", 6), (1, "#6E4A28", 0)),
        stroke=NONE)
for i, (x, y, w) in enumerate([(214, 236, 6), (776, 258, 7), (176, 626, 6), (824, 592, 7),
                               (436, 108, 6), (630, 104, 7), (172, 424, 6), (838, 434, 6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C89A5E", opacity=30, stroke=NONE)

FY = 708
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#463322", 42), (1, "#120A05", 78)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E8CC92", strokeWidth=2, opacity=20)

# grounding shadow under the console
sh = [P(x, 0, z) for x in (-32, 32) for z in (-7.5, 7.5)]
sx0, sx1 = min(p[0] for p in sh) - 34, max(p[0] for p in sh) + 34
sy0, sy1 = min(p[1] for p in sh) - 18, max(p[1] for p in sh) + 24
d.shape("ellipse", "Console shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#060302", 64), (0.6, "#060302", 24), (1, "#060302", 0)),
        stroke=NONE)

# --- wall screen: the black rectangle the console is sized to -------------------------
prism("Screen", box(-22, 33, 10.3, 22, 54, 11.3),
      dark=EBONY_D, light=EBONY_L, lo=0.14, hi=0.62, ink=2.4)
seg3("Screen sheen 1", [(-19.5, 50.5, 10.2), (-7, 38, 10.2)], "#6E6E82", 4.5, 30)
seg3("Screen sheen 2", [(-14, 53, 10.2), (-3, 42, 10.2)], "#5A5A6E", 3.0, 22)
seg3("Screen edge light", [(-21, 33.4, 10.2), (18, 33.4, 10.2)], "#8A8A9E", 2.0, 30)
lx, ly = P(20.6, 33.6, 10.2)
d.shape("ellipse", "Screen standby dot", x=round(lx - 1.8), y=round(ly - 1.8),
        width=3.6, height=3.6, fill="#7AE08A", opacity=75, stroke=NONE)

# --- legs: splayed tapers, back pair first ---------------------------------------------
def leg(nm, cx, cz, sx, sz, ferrule=True):
    if ferrule:
        prism(f"{nm} ferrule", taper_box(1.05, 0.92, 0, 1.7, cx, cz, sx, sz),
              dark=BRASS_D, light=BRASS_L, lo=0.15, hi=1.0, ink=1.5)
        prism(f"{nm} leg", taper_box(1.15, 0.95, 1.7, 7.0, cx, cz, sx * 0.4, sz * 0.4),
              lo=0.08, hi=0.95, ink=1.7)
    else:
        prism(f"{nm} leg", taper_box(1.1, 0.9, 0, 7.0, cx, cz, sx * 0.4, sz * 0.4),
              dark="#1E1006", light="#5A3618", lo=0.05, hi=0.7, ink=1.7)


LX, LZ = 29.0, 4.6
leg("Back left", -26, LZ, -0.9, 0.5, ferrule=False)
leg("Back right", 26, LZ, 0.9, 0.5, ferrule=False)

# --- carcass ----------------------------------------------------------------------------
CX, CY0, CY1, CZ = 31.5, 7.0, 21.2, 6.5
prism("Carcass", box(-CX, CY0, -CZ, CX, CY1, CZ), lo=0.10, hi=0.98, ink=2.0)

# centre open bay: a dark recess quad on the front face, then its contents
BX = 10.0                                    # bay half-width
FZ = -CZ - 0.12                              # just in front of the front face
bay = [(-BX, 8.2, FZ), (BX, 8.2, FZ), (BX, 20.2, FZ), (-BX, 20.2, FZ)]
bq = [P(*p) for p in bay]
by0, by1 = min(p[1] for p in bq), max(p[1] for p in bq)
d.path(poly(bq), "Open bay",
       fill=lin((0, by0), (0, by1), (0, "#241408"), (1, "#0E0602")),
       stroke="#0A0402", strokeWidth=2.0, join="round")
# shelf line inside the bay
seg3("Bay shelf", [(-BX + 0.4, 14.4, FZ - 0.05), (BX - 0.4, 14.4, FZ - 0.05)],
     "#4A2E14", 2.6, 80)
# record spines standing on the bay floor, left half
recs = [(-8.6, 10.8, "#6E3A28"), (-7.4, 11.4, "#8A5A32"), (-6.1, 10.2, "#4E5A3A"),
        (-4.9, 11.0, "#7A6A48"), (-3.6, 10.6, "#3E4E5E"), (-2.4, 9.6, "#8A4A30")]
for i, (rx, rh, rc) in enumerate(recs):
    seg3(f"Record {i+1}", [(rx, 8.5, FZ - 0.15), (rx, 8.5 + rh * 0.8, FZ - 0.15)],
         rc, 6.5, 92)
# small amp on the shelf, right half of the bay
prism("Amp", box(2.0, 14.6, FZ - 0.9, 8.4, 18.2, FZ - 0.1),
      dark="#141018", light="#4A3E30", lo=0.2, hi=0.85, ink=1.4)
seg3("Amp slot", [(2.8, 16.4, FZ - 0.95), (6.2, 16.4, FZ - 0.95)], "#C8A860", 2.2, 70)
ax, ay = P(7.6, 16.4, FZ - 0.95)
d.shape("ellipse", "Amp lamp", x=round(ax - 1.6), y=round(ay - 1.6), width=3.2,
        height=3.2, fill="#F0C86A", opacity=85, stroke=NONE)

# doors over the side bays, slightly proud of the front
for nm, x0, x1 in (("Left", -30.6, -10.9), ("Right", 10.9, 30.6)):
    prism(f"{nm} door", box(x0, 8.0, -CZ - 0.9, x1, 20.4, -CZ - 0.05),
          lo=0.14, hi=1.0, ink=1.8)
    # fluting: vertical grooves down the door face
    fr = -CZ - 1.0
    n_fl = 6
    for k in range(n_fl):
        fx = x0 + (x1 - x0) * (k + 1) / (n_fl + 1)
        seg3(f"{nm} flute {k+1}", [(fx, 9.0, fr), (fx, 19.4, fr)],
             "#2A1608", 2.8, 55)
        seg3(f"{nm} flute hi {k+1}", [(fx + 0.42, 9.0, fr), (fx + 0.42, 19.4, fr)],
             "#B87A42", 1.4, 40)
    # slim vertical pull on the inner edge
    px = x1 - 1.1 if x0 < 0 else x0 + 1.1
    seg3(f"{nm} pull", [(px, 15.4, fr - 0.1), (px, 19.6, fr - 0.1)],
         BRASS_L, 4.2, 90)

# --- top slab -----------------------------------------------------------------------------
TX0, TX1, TY0, TY1, TZ0, TZ1 = -33.0, 33.0, 21.2, 22.6, -7.3, 7.3
prism("Top slab", box(TX0, TY0, TZ0, TX1, TY1, TZ1),
      dark="#45280F", light="#A06832", lo=0.12, hi=1.05, ink=2.2)
seg3("Top edge light", [(TX0 + 1, TY1 + 0.08, TZ0 + 0.5), (TX1 - 1, TY1 + 0.08, TZ0 + 0.5)],
     "#E8B878", 2.6, 60)
# faint grain on the top surface
seg3("Grain 1", [(-28, TY1 + 0.05, 2.6), (-14, TY1 + 0.05, 1.8), (0, TY1 + 0.05, 2.8)],
     "#2E1A0A", 1.6, 45)
seg3("Grain 2", [(6, TY1 + 0.05, -2.6), (18, TY1 + 0.05, -1.6), (28, TY1 + 0.05, -2.4)],
     "#2E1A0A", 1.6, 40)

# --- front legs after the carcass ------------------------------------------------------------
leg("Front left", -LX, -LZ, -1.3, -0.9)
leg("Front right", LX, -LZ, 1.3, -0.9)

# --- soundbar, centred under the screen ----------------------------------------------------------
prism("Soundbar", box(-13.5, TY1, 2.6, 13.5, TY1 + 1.9, 4.6),
      dark=EBONY_D, light=EBONY_L, lo=0.16, hi=0.8, ink=1.6)
seg3("Soundbar grill", [(-12.6, TY1 + 1.0, 2.45), (12.6, TY1 + 1.0, 2.45)],
     "#0A0A0E", 2.0, 60)
for k in range(9):
    sx = -10 + k * 2.5
    seg3(f"Grill dot {k+1}", [(sx, TY1 + 1.0, 2.4), (sx + 0.6, TY1 + 1.0, 2.4)],
         "#565664", 1.6, 70)

# --- book stack, left end of the top ---------------------------------------------------------------
prism("Book lower", box(-30, TY1, -0.6, -22, TY1 + 1.1, 5.6),
      dark="#5E2A18", light="#A8542E", lo=0.2, hi=0.95, ink=1.6)
seg3("Book lower pages", [(-29.6, TY1 + 0.55, -0.75), (-22.5, TY1 + 0.55, -0.75)],
     "#E8DCC0", 2.6, 80)
prism("Book upper", box(-28.8, TY1 + 1.1, 0.2, -22.6, TY1 + 1.95, 4.8),
      dark="#2E4452", light="#6E8EA0", lo=0.2, hi=0.95, ink=1.5)
seg3("Book upper pages", [(-28.4, TY1 + 1.52, 0.05), (-23.0, TY1 + 1.52, 0.05)],
     "#E0D8C4", 2.2, 80)

# --- potted plant, right end of the top --------------------------------------------------------------
pot = taper_box(2.3, 1.7, TY1, TY1 + 3.4, 27.5, 2.4)
prism("Plant pot", pot, dark=POT_D, light=POT_L, lo=0.18, hi=1.0, ink=1.7)
leaf_c = [("#4E6E34", -14, 8.5), ("#5E7A3C", -6, 9.6), ("#6E8A48", 0, 10.2),
          ("#4E6E34", 7, 9.4), ("#5E7A3C", 14, 8.2)]
for i, (col, dx, h) in enumerate(leaf_c):
    bx, by = P(27.5 + dx * 0.08, TY1 + 3.3, 2.4)
    tx, ty = P(27.5 + dx * 0.42, TY1 + 3.3 + h, 2.4)
    mx, my = P(27.5 + dx * 0.22, TY1 + 3.3 + h * 0.55, 2.4)
    d.path(f"M{bx:.1f},{by:.1f} Q{mx:.1f},{my:.1f} {tx:.1f},{ty:.1f}",
           f"Leaf {i+1}", fill=NONE, stroke=col, strokeWidth=4.2, cap="round", opacity=95)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("media-console extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F4E6C8", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#D2B078", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=240)
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


caption("MEDIA CONSOLE", "WALNUT · BRASS · GLASS")
d.finish("media-console-V1R00")
