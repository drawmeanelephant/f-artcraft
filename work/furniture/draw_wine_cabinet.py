#!/usr/bin/env python3
"""Wine cabinet — field plate V1R00. Three-quarter view from front-right-above:
a tall oak cellar cabinet — plinth base, two panelled doors below, and an open
upper bay where a diagonal slat lattice cradles the bottles at their angle,
each one a foil-capped end-on dot in the dim. A crown cap on top carries three
standing bottles. Oak plate, cellar mood. 1000x1000.
Modelled in inches (x right, y up, +z back); face-culled prisms, yaw+pitch.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Wine Cabinet — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#180C04"
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
S, OX, OY = 10.6, 500.0, 694.0
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
    """Tapered prism: wt half-width at top, wb at bottom; optional plan offset
    (sx, sz) at the foot. Same vertex ordering as box()."""
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
OAK_D, OAK_L = "#3E2610", "#96622E"      # oak
OAK_HI = "#C08A50"
BRASS_D, BRASS_L = "#6E4E1E", "#E2BC66"
GLASS_G = ("#12230F", "#4A6E38")         # green bottle glass
GLASS_A = ("#2A1606", "#7E5020")         # amber bottle glass


def prism(name, corners, dark=OAK_D, light=OAK_L, lo=0.06, hi=0.94, ink=1.8):
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
        fill=lin((0, 0), (0, 1000), (0, "#131009"), (1, "#050403")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8A6A3A", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5C4220"), (0.6, "#33200E"), (1, "#100903")),
        stroke="#0E0803", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4C48E", strokeWidth=3, opacity=22)
d.shape("ellipse", "Cellar lamp", x=210, y=140, width=500, height=480,
        fill=rad((0, "#E8BC72", 16), (0.55, "#A87E40", 5), (1, "#6E4A28", 0)),
        stroke=NONE)
d.shape("ellipse", "Cellar cool", x=560, y=150, width=300, height=300,
        fill=rad((0, "#5E7E7A", 9), (1, "#5E7E7A", 0)), stroke=NONE)
for i, (x, y, w) in enumerate([(212, 240, 6), (784, 252, 7), (174, 620, 6), (826, 588, 7),
                               (440, 106, 6), (626, 108, 7), (170, 428, 6), (840, 420, 6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C09A5E", opacity=28, stroke=NONE)

FY = 708
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#3E2E1E", 40), (1, "#100A04", 78)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E0C28A", strokeWidth=2, opacity=18)

# grounding shadow under the cabinet
sh = [P(x, 0, z) for x in (-15.5, 15.5) for z in (-7.5, 7.5)]
sx0, sx1 = min(p[0] for p in sh) - 34, max(p[0] for p in sh) + 34
sy0, sy1 = min(p[1] for p in sh) - 18, max(p[1] for p in sh) + 24
d.shape("ellipse", "Cabinet shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#050302", 64), (0.6, "#050302", 24), (1, "#050302", 0)),
        stroke=NONE)

# --- carcass --------------------------------------------------------------------------
prism("Plinth", box(-14.5, 0, -7.3, 14.5, 6, 7.3),
      dark="#2A1808", light="#6E421E", lo=0.08, hi=0.8, ink=1.8)
seg3("Plinth bevel", [(-14.5, 5.9, -7.35), (14.5, 5.9, -7.35)], "#C08A50", 2.2, 45)
prism("Carcass", box(-15, 6, -7.8, 15, 46, 7.8), lo=0.10, hi=0.98, ink=2.0)

# --- upper bay: open lattice cellar ---------------------------------------------------
OX0, OX1, OY0, OY1 = -13, 13, 24, 43.5
FZ = -7.8 - 0.1                               # just proud of the carcass front
bay = [(OX0, OY0, FZ), (OX1, OY0, FZ), (OX1, OY1, FZ), (OX0, OY1, FZ)]
bq = [P(*p) for p in bay]
by0, by1 = min(p[1] for p in bq), max(p[1] for p in bq)
d.path(poly(bq), "Cellar bay",
       fill=lin((0, by0), (0, by1), (0, "#1C1006"), (1, "#0C0502")),
       stroke="#080302", strokeWidth=2.0, join="round")
# inner shadows: top and right edges read as depth inside the bay
seg3("Bay shade top", [(OX0, OY1 - 0.3, FZ - 0.05), (OX1, OY1 - 0.3, FZ - 0.05)],
     "#050201", 5.0, 60)
seg3("Bay shade right", [(OX1 - 0.3, OY0, FZ - 0.05), (OX1 - 0.3, OY1, FZ - 0.05)],
     "#050201", 4.0, 45)
seg3("Bay light left", [(OX0 + 0.25, OY0 + 0.5, FZ - 0.05), (OX0 + 0.25, OY1 - 0.6, FZ - 0.05)],
     "#8A5628", 2.6, 40)

# diagonal slat lattice: two families at 45 deg, clipped to the bay rect
SLAT_Z = FZ - 0.1


def slat_family(name, mode, consts, col="#7A4A20", sw=4.4):
    """mode 'a': y = x - s ; mode 'b': y = -x + t. Clip to the bay rect."""
    for i, c in enumerate(consts):
        pts = []
        for edge in ("bottom", "top", "left", "right"):
            if mode == "a":                       # x = y + s
                cand = {"bottom": (OY0 + c, OY0), "top": (OY1 + c, OY1),
                        "left": (OX0, OX0 - c), "right": (OX1, OX1 - c)}[edge]
            else:                                 # y = -x + t
                cand = {"bottom": (c - OY0, OY0), "top": (c - OY1, OY1),
                        "left": (OX0, c - OX0), "right": (OX1, c - OX1)}[edge]
            x, y = cand
            if OX0 - 0.01 <= x <= OX1 + 0.01 and OY0 - 0.01 <= y <= OY1 + 0.01:
                pts.append((x, y))
        uniq = sorted(set(pts))
        if len(uniq) >= 2:
            seg3(f"{name} {i+1}", [(uniq[0][0], uniq[0][1], SLAT_Z),
                                   (uniq[-1][0], uniq[-1][1], SLAT_Z)], col, sw, 92)


S_A = [-54 + 6.7 * i for i in range(7)]           # y = x - s
T_B = [12 + 6.8 * i for i in range(7)]            # y = -x + t
slat_family("Slat up", "a", S_A)
slat_family("Slat down", "b", T_B)

# bottles cradled at the diamond cell centres: foil cap, dark glass, glint
FOILS = [("#6E1E24", "#B04048"), ("#8A6420", "#E0B85E"), ("#1E1E24", "#4A4A56"),
         ("#22401E", "#4E7A42"), ("#5E3018", "#A06A38")]
MIDS_A = [(S_A[i] + S_A[i + 1]) / 2 for i in range(len(S_A) - 1)]
MIDS_B = [(T_B[i] + T_B[i + 1]) / 2 for i in range(len(T_B) - 1)]
cells = []
for s in MIDS_A:
    for t in MIDS_B:
        x, y = (s + t) / 2, (t - s) / 2
        if OX0 + 3.4 <= x <= OX1 - 3.4 and OY0 + 2.6 <= y <= OY1 - 2.6:
            cells.append((x, y))
cells.sort(key=lambda c: -depth(c[0], c[1], SLAT_Z))
bi = 0
for cx, cy in cells:
    bx, by = P(cx, cy, SLAT_Z - 0.05)
    g = GLASS_G if bi % 3 else GLASS_A
    f0, f1 = FOILS[bi % len(FOILS)]
    d.shape("ellipse", f"Bottle {bi+1} glass", x=round(bx - 12.5), y=round(by - 12.5),
            width=25, height=25,
            fill=rad((0, g[1]), (0.7, g[0]), (1, "#060302")), stroke="#050302",
            strokeWidth=1.4)
    d.shape("ellipse", f"Bottle {bi+1} cap", x=round(bx - 6.5), y=round(by - 6.5),
            width=13, height=13,
            fill=rad((0, f1), (0.75, f0), (1, f0)), stroke="#050302", strokeWidth=1.2)
    d.path(f"M{bx - 9:.1f},{by - 6:.1f} A11,11 0 0 1 {bx - 3:.1f},{by - 10.4:.1f}",
           f"Bottle {bi+1} glint", fill=NONE, stroke="#E8D8B0", strokeWidth=2.2,
           opacity=55, cap="round")
    bi += 1

# bay frame: four rails over the lattice edges clean the border and read as stiles
for nm, pts in (("top", [(OX0 - 0.4, OY1 + 0.15, FZ + 0.05), (OX1 + 0.4, OY1 + 0.15, FZ + 0.05)]),
                ("bottom", [(OX0 - 0.4, OY0 - 0.15, FZ + 0.05), (OX1 + 0.4, OY0 - 0.15, FZ + 0.05)]),
                ("left", [(OX0 + 0.15, OY0, FZ + 0.05), (OX0 + 0.15, OY1, FZ + 0.05)]),
                ("right", [(OX1 - 0.15, OY0, FZ + 0.05), (OX1 - 0.15, OY1, FZ + 0.05)])):
    seg3(f"Bay rail {nm}", pts, "#7E4E22", 5.2, 90)

# --- lower doors ----------------------------------------------------------------------
for nm, x0, x1 in (("Left", -13.2, -0.7), ("Right", 0.7, 13.2)):
    prism(f"{nm} door", box(x0, 7.6, -7.8 - 0.85, x1, 22.4, -7.8 - 0.05),
          lo=0.14, hi=1.0, ink=1.8)
    # fielded panel inset
    p = 3.2
    seg3(f"{nm} panel light", [(x0 + p, 7.6 + p, -8.8), (x0 + p, 22.4 - p, -8.8),
                               (x1 - p, 22.4 - p, -8.8)], "#C08A50", 2.0, 50)
    seg3(f"{nm} panel shade", [(x1 - p, 22.4 - p, -8.8), (x1 - p, 7.6 + p, -8.8),
                               (x0 + p, 7.6 + p, -8.8)], "#1E0E04", 2.0, 55)
    # brass knob on the inner stile
    kx = x1 - 1.6 if x0 < 0 else x0 + 1.6
    kxp, kyp = P(kx, 14.8, -8.8)
    d.shape("ellipse", f"{nm} knob", x=round(kxp - 3), y=round(kyp - 3), width=6,
            height=6, fill=rad((0, BRASS_L), (1, BRASS_D)), stroke="#241204",
            strokeWidth=1.2)

# --- crown cap --------------------------------------------------------------------------
prism("Crown", box(-16.2, 46, -8.4, 16.2, 47.8, 8.4),
      dark="#4A2C12", light="#A8763E", lo=0.12, hi=1.0, ink=2.2)
seg3("Crown edge light", [(-15.8, 47.9, -7.9), (15.8, 47.9, -7.9)], "#E0AC6A", 2.4, 55)

# --- standing bottles on the crown -----------------------------------------------------
def bottle(nm, cx, cz, body_h, glass):
    """Bottle: straight body + tapered shoulder + neck + capsule on the crown."""
    gd, gl = glass
    top = 47.8 + body_h
    prism(f"{nm} body", box(cx - 1.35, 47.8, cz - 1.35, cx + 1.35, top - 1.6, cz + 1.35),
          dark=gd, light=gl, lo=0.15, hi=0.9, ink=1.6)
    prism(f"{nm} shoulder", taper_box(0.55, 1.35, top - 1.6, top, cx, cz),
          dark=gd, light=gl, lo=0.2, hi=0.9, ink=1.4)
    prism(f"{nm} neck", box(cx - 0.5, top - 0.2, cz - 0.5,
                            cx + 0.5, top + 2.6, cz + 0.5),
          dark=gd, light=gl, lo=0.2, hi=0.9, ink=1.3)
    px, py = P(cx, top + 2.7, cz)
    d.shape("ellipse", f"{nm} capsule", x=round(px - 4.6), y=round(py - 3.4),
            width=9.2, height=6.8,
            fill=lin((px - 4.6, py), (px + 4.6, py), (0, "#C09A48"), (1, "#5E3E14")),
            stroke="#241204", strokeWidth=1.2)
    seg3(f"{nm} glint", [(cx - 0.9, 48.6, cz - 1.4), (cx - 0.9, top - 2.4, cz - 1.4)],
         "#D8C8A0", 2.2, 50)


bottle("Bottle tall", -8.5, 3.6, 6.8, GLASS_G)
bottle("Bottle mid", -3.0, 4.8, 5.6, GLASS_A)
bottle("Bottle short", 4.5, 3.4, 6.2, ("#140C08", "#4A2E14"))

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("wine-cabinet extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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


caption("WINE CABINET", "OAK · GLASS · CORK")
d.finish("wine-cabinet-V1R00")
