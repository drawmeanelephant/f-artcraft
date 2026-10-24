#!/usr/bin/env python3
"""Etagere — field plate V1R00. Three-quarter view from the front right:
a tall brass display stand — four slim posts on little bun feet rising to
ball finials — carrying four glass shelves in brass perimeter frames. The
good objects ride the shelves: bound books, a celadon vase, a small globe,
a pair of letter boxes. Brass-and-glass plate, parlour mood — a deep
teal field with warm cabinet light. 1000x1000. Modelled in inches
(x right, y up, +z back), projected with a fixed yaw + pitch; carcass
parts are 8-corner prisms culled by view normal and shaded by lamp light.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Etagere — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1A140C"   # warm dark, not black
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


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(30), math.radians(22)
S, OX, OY = 9.6, 502.0, 738.0
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
    return [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]


FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
TO_VIEWER = (SY * CP, SP, -CY * CP)          # normals facing this draw
LIGHT = (-0.35, 0.86, -0.30)                  # lamp overhead, slightly left/front
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


def prism(name, corners, ramp=("#4A3010", "#D8A94E"), lo=0.06, hi=0.94, sw=1.8, op=None):
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
        g = lin((0, y0), (0, y1), (0, shade(ramp[0], ramp[1], min(1, b + 0.12))),
                                 (1, shade(ramp[0], ramp[1], b)))
        kw = {}
        if op is not None:
            kw["opacity"] = op
        d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=sw, join="round", **kw)


def flat_ellipse(cx, y, cz, r, label, **kw):
    """Ellipse lying on the horizontal plane y: a circle of model radius r."""
    ex, ey = P(cx, y, cz)
    rx, ry = S * r, S * r * SP
    d.shape("ellipse", label, x=round(ex - rx, 1), y=round(ey - ry, 1),
            width=round(rx * 2, 1), height=round(ry * 2, 1), **kw)


def cylinder(name, cx, y0, y1, cz, r, ramp, sw=1.4):
    """Vertical cylinder: projected side wall + top ellipse."""
    eb = P(cx, y0, cz)
    et = P(cx, y1, cz)
    rx, ry = S * r, S * r * SP
    side = (f"M{eb[0] - rx:.1f},{eb[1]:.1f} L{et[0] - rx:.1f},{et[1]:.1f} "
            f"A{rx:.1f},{ry:.1f} 0 0 1 {et[0] + rx:.1f},{et[1]:.1f} "
            f"L{eb[0] + rx:.1f},{eb[1]:.1f} "
            f"A{rx:.1f},{ry:.1f} 0 0 0 {eb[0] - rx:.1f},{eb[1]:.1f} Z")
    d.path(side, name, fill=lin((0, et[1]), (0, eb[1]),
           (0, ramp[1], None), (1, ramp[0], None)), stroke=INK,
           strokeWidth=sw, join="round")
    flat_ellipse(cx, y1, cz, r, name + " top",
                 fill=rad((0, shade(ramp[1], "#FFFFFF", 0.25), None), (1, ramp[1], None)),
                 stroke=INK, strokeWidth=sw)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#101A16"), (1, "#050807")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#C8AE6A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#2E4038"), (0.55, "#1A2620"), (1, "#0B100D")),
        stroke="#0A0E0A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C89A", strokeWidth=3, opacity=24)

# warm parlour light pooled high behind the stand
d.shape("ellipse", "Parlour glow", x=300, y=170, width=400, height=330,
        fill=rad((0, "#FFC888", 0.14), (0.55, "#B88050", 0.05), (1, "#B88050", 0)),
        stroke=NONE)

# --- floor: dark boards closing on the disc arc ---------------------------------------
FYB = 752
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX - hw:.1f},{FYB} L{PCX + hw:.1f},{FYB} A420,420 0 0 0 {PCX - hw:.1f},{FYB} Z",
       "Floor", fill=lin((0, FYB), (0, 880), (0, "#2E3A30", 0.5), (0.5, "#1A221A", 0.7),
                         (1, "#0A0D09", 0.9)), stroke=NONE)
for i, yb in enumerate([784, 816, 848]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Board seam {i+1}",
           fill=NONE, stroke="#4A5A48", strokeWidth=2, opacity=24)

# --- grounding shadow -------------------------------------------------------------------
fx0, fy0 = P(-12, 0, -7)
fx1, fy1 = P(12, 0, 7)
sx0, sx1 = min(fx0, fx1) - 24, max(fx0, fx1) + 24
sy0, sy1 = min(fy0, fy1) - 12, max(fy0, fy1) + 16
d.shape("ellipse", "Stand shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#030403", 0.7), (0.6, "#030403", 0.3), (1, "#030403", 0)),
        stroke=NONE)

# --- etagere geometry (inches) ---------------------------------------------------------------
BRASS = ("#4A3010", "#D8A94E")
BRASS_HI = ("#6A4A18", "#E8BC66")
GLASS = ("#5E7E78", "#CFE4DE")
PX, PZ = 10.4, 5.9          # post half-spans
SHELFS = [11.0, 24.5, 38.0, 51.5]
TOP_Y = 62.5


def post(sx, sz, tag):
    lx, lz = sx * PX, sz * PZ
    # bun foot
    fb = P(lx, 1.1, lz)
    d.shape("ellipse", f"Bun foot {tag}", x=round(fb[0] - 6.4, 1), y=round(fb[1] - 4.2, 1),
            width=12.8, height=8.4,
            fill=rad((0, "#E8BC66", None), (0.65, "#8A6426", None), (1, "#3A280E", None)),
            stroke=INK, strokeWidth=1.2)
    # slim post, tapering up
    corners = [(lx - 0.55, 0.8, lz - 0.55), (lx + 0.55, 0.8, lz - 0.55),
               (lx + 0.55, 0.8, lz + 0.55), (lx - 0.55, 0.8, lz + 0.55),
               (lx - 0.38, TOP_Y, lz - 0.38), (lx + 0.38, TOP_Y, lz - 0.38),
               (lx + 0.38, TOP_Y, lz + 0.38), (lx - 0.38, TOP_Y, lz + 0.38)]
    prism(f"Post {tag}", corners, ramp=BRASS, lo=0.10, hi=0.95, sw=1.5)
    # collar rings at each shelf line
    for j, sy_ in enumerate(SHELFS):
        cl = P(lx, sy_ + 0.55, lz)
        d.shape("ellipse", f"Collar {tag}{j}", x=round(cl[0] - 3.4, 1), y=round(cl[1] - 1.8, 1),
                width=6.8, height=3.6, fill="#E8BC66", stroke=INK, strokeWidth=0.7)
    # ball finial
    fn = P(lx, TOP_Y + 1.3, lz)
    d.shape("ellipse", f"Finial {tag}", x=round(fn[0] - 5.4, 1), y=round(fn[1] - 5.4, 1),
            width=10.8, height=10.8,
            fill=rad((0, "#F4D48A", None), (0.6, "#C89A4A", None), (1, "#4A3010", None)),
            stroke=INK, strokeWidth=1.1)


# far posts first: they stand behind the shelves
post(-1, 1, "far L")
post(1, 1, "far R")


def shelf(i, sy_):
    # brass perimeter frame holding the glass
    prism(f"Frame near {i}", box(-PX - 0.2, sy_, -PZ - 0.35, PX + 0.2, sy_ + 0.5, -PZ + 0.35),
          ramp=BRASS_HI, lo=0.15, hi=1.0, sw=1.3)
    prism(f"Frame far {i}", box(-PX - 0.2, sy_, PZ - 0.35, PX + 0.2, sy_ + 0.5, PZ + 0.35),
          ramp=BRASS, lo=0.08, hi=0.8, sw=1.3)
    prism(f"Frame L {i}", box(-PX - 0.35, sy_, -PZ - 0.35, -PX + 0.35, sy_ + 0.5, PZ + 0.35),
          ramp=BRASS, lo=0.08, hi=0.85, sw=1.3)
    prism(f"Frame R {i}", box(PX - 0.35, sy_, -PZ - 0.35, PX + 0.35, sy_ + 0.5, PZ + 0.35),
          ramp=BRASS_HI, lo=0.12, hi=0.95, sw=1.3)
    # the glass sheet itself, translucent
    gq = [P(-PX + 0.4, sy_ + 0.25, -PZ + 0.4), P(PX - 0.4, sy_ + 0.25, -PZ + 0.4),
          P(PX - 0.4, sy_ + 0.25, PZ - 0.4), P(-PX + 0.4, sy_ + 0.25, PZ - 0.4)]
    gy0, gy1 = min(p[1] for p in gq), max(p[1] for p in gq)
    d.path(poly(gq), f"Glass {i}", fill=lin((0, gy0), (0, gy1),
           (0, "#D8EAE4", 0.34), (0.6, "#9AB8B0", 0.22), (1, "#5E7E78", 0.30)),
           stroke="#C8E0D8", strokeWidth=1.4, opacity=85, join="round")
    # bright front edge of the glass
    ga, gb = P(-PX + 0.4, sy_ + 0.3, -PZ + 0.4), P(PX - 0.4, sy_ + 0.3, -PZ + 0.4)
    d.path(f"M{ga[0]:.1f},{ga[1]:.1f} L{gb[0]:.1f},{gb[1]:.1f}", f"Glass edge {i}",
           fill=NONE, stroke="#EAF8F2", strokeWidth=2.2, opacity=60, cap="round")


# bottom shelf first, objects riding each deck
shelf(0, SHELFS[0])

# letter boxes on the bottom deck
prism("Letter box L", box(-8.6, SHELFS[0] + 0.5, -2.5, -3.4, SHELFS[0] + 2.2, 2.8),
      ramp=("#3E2E1A", "#8A6A3E"), lo=0.15, hi=0.9, sw=1.2)
prism("Letter box R", box(3.0, SHELFS[0] + 0.5, -2.8, 8.2, SHELFS[0] + 1.9, 2.2),
      ramp=("#2E3A34", "#7E9484"), lo=0.15, hi=0.9, sw=1.2)

shelf(1, SHELFS[1])

# celadon vase on the second deck, slightly left: belly + neck
vbase = SHELFS[1] + 0.45
cylinder("Vase belly", -4.2, vbase, vbase + 3.1, 0.5, 1.7, ("#3E5650", "#9EBEB2"))
cylinder("Vase neck", -4.2, vbase + 3.1, vbase + 5.6, 0.5, 1.05, ("#3E5650", "#9EBEB2"))
vn = P(-4.2, vbase + 6.4, 0.5)
d.shape("ellipse", "Vase lip", x=round(vn[0] - 4.2, 1), y=round(vn[1] - 2.2, 1),
        width=8.4, height=4.4, fill="#3E5650", stroke=INK, strokeWidth=1.0)
# right of the vase: two stacked folios with one leaning
prism("Folio 1", box(2.5, vbase, -3.0, 8.8, vbase + 0.9, 2.6), ramp=("#3A2A16", "#9A7440"),
      lo=0.2, hi=0.95, sw=1.1)
prism("Folio 2", box(2.9, vbase + 0.9, -2.6, 8.5, vbase + 1.7, 2.4), ramp=("#2E2430", "#7A6484"),
      lo=0.2, hi=0.95, sw=1.1)
lean = [P(8.9, vbase, -2.8), P(10.6, vbase + 4.4, -2.8), P(10.6, vbase + 4.4, 2.2),
        P(8.9, vbase, 2.2)]
d.path(poly(lean), "Leaning folio", fill=lin(lean[0], lean[1],
     (0, "#8A3E32", None), (1, "#4A2018", None)), stroke=INK, strokeWidth=1.2, join="round")

shelf(2, SHELFS[2])

# the small globe on the third deck: sphere + meridian arc + stand
gbx, gbz, gby = 1.5, 0.8, SHELFS[2] + 0.5
gb = P(gbx, gby + 3.6, gbz)
gr = S * 2.55
d.shape("ellipse", "Globe shadow", x=round(gb[0] - gr * 0.9, 1), y=round(gb[1] + gr * 0.72, 1),
        width=round(gr * 1.8), height=round(gr * 0.4), fill="#0A0E0A", opacity=35, stroke=NONE)
prism("Globe foot", box(gbx - 1.3, gby, gbz - 1.1, gbx + 1.3, gby + 1.0, gbz + 1.1),
      ramp=BRASS, lo=0.2, hi=1.0, sw=1.0)
d.shape("ellipse", "Globe", x=round(gb[0] - gr, 1), y=round(gb[1] - gr, 1),
        width=round(gr * 2), height=round(gr * 2),
        fill=rad((0, "#7AA8B8", None), (0.55, "#3E6880", None), (1, "#16283A", None)),
        stroke=INK, strokeWidth=1.4)
# landmass hints and the meridian ring
d.shape("ellipse", "Globe land", x=round(gb[0] - gr * 0.55, 1), y=round(gb[1] - gr * 0.35, 1),
        width=round(gr * 0.8), height=round(gr * 0.55), fill="#8AA06A", opacity=55, stroke=NONE)
d.shape("ellipse", "Globe land 2", x=round(gb[0] + gr * 0.15, 1), y=round(gb[1] + gr * 0.2, 1),
        width=round(gr * 0.55), height=round(gr * 0.4), fill="#8AA06A", opacity=50, stroke=NONE)
d.path(f"M{gb[0] + gr * 0.92:.1f},{gb[1] - gr * 0.45:.1f} "
       f"A{gr * 0.5:.1f},{gr * 1.18:.1f} -18 1 0 {gb[0] - gr * 0.5:.1f},{gb[1] + gr * 0.95:.1f}",
       "Globe meridian", fill=NONE, stroke="#E8BC66", strokeWidth=2.0, opacity=80)

shelf(3, SHELFS[3])

# top deck: a tiny bust on a plinth — the prize of the cabinet
bsx, bsz, bsy = -1.0, 0.5, SHELFS[3] + 0.5
prism("Bust plinth", box(bsx - 1.7, bsy, bsz - 1.5, bsx + 1.7, bsy + 1.3, bsz + 1.5),
      ramp=("#8A8478", "#DCD4C4"), lo=0.25, hi=1.0, sw=1.1)
bh = P(bsx, bsy + 3.4, bsz)
d.shape("ellipse", "Bust head", x=round(bh[0] - 11.5, 1), y=round(bh[1] - 13, 1),
        width=23, height=26,
        fill=rad((0, "#F0E8D8", None), (0.6, "#C8BBA4", None), (1, "#7E7260", None)),
        stroke=INK, strokeWidth=1.2)
sh_pts = [P(bsx - 2.0, bsy + 1.3, bsz - 1.0), P(bsx + 2.0, bsy + 1.3, bsz - 1.0),
          P(bsx + 1.3, bsy + 2.6, bsz - 0.2), P(bsx - 1.3, bsy + 2.6, bsz - 0.2)]
d.path(poly(sh_pts), "Bust shoulders", fill=lin((0, sh_pts[2][1]), (0, sh_pts[0][1]),
       (0, "#E0D6C4", None), (1, "#9A8E7A", None)), stroke=INK, strokeWidth=1.1, join="round")

# near posts last: they stand in front of the shelf edges
post(-1, -1, "near L")
post(1, -1, "near R")

# thin stretcher bars low between the near pair, and a crown rail at the top
prism("Low stretcher near", box(-PX, 4.2, -PZ - 0.3, PX, 5.0, -PZ + 0.3),
      ramp=BRASS, lo=0.1, hi=0.9, sw=1.2)
prism("Crown rail near", box(-PX, TOP_Y - 0.6, -PZ - 0.25, PX, TOP_Y, -PZ + 0.25),
      ramp=BRASS_HI, lo=0.15, hi=1.0, sw=1.2)

# warm edge light down the near-right post
ea, eb = P(PX + 0.45, 6, -PZ - 0.1), P(PX + 0.42, TOP_Y - 0.5, -PZ - 0.1)
d.path(f"M{ea[0]:.1f},{ea[1]:.1f} L{eb[0]:.1f},{eb[1]:.1f}", "Post rim light",
       fill=NONE, stroke="#FFCE8A", strokeWidth=2.0, opacity=40, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("etagere extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F0E6CE", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C4B091", justify="center")
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


caption("ETAGERE", "BRASS · GLASS · IVORY")
d.finish("etagere-V1R00")
