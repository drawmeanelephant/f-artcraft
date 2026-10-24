#!/usr/bin/env python3
"""Nightstand — field plate V1R00. Three-quarter view from the front right:
a walnut bedside stand, one drawer over an open cubby of books, a brass
lamp burning warm against the blue night and one glass of water on top.
Slate plate, 3 a.m. mood. 1000x1000.
Modelled in inches (x right, y up, +z back) and projected with a fixed
yaw + pitch; the carcass is face-framed slabs so the cubby reads real,
horizontal circles project to ellipses for the lamp foot and glass rims.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Nightstand — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1A0E10"   # warm dark, not black
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
YAW, PITCH = math.radians(28), math.radians(20)
S, OX, OY = 16.0, 515.0, 648.0
CY, SY = math.cos(YAW), math.sin(YAW)
CP, SP = math.cos(PITCH), math.sin(PITCH)


def P(x, y, z):
    xr, zr = x * CY + z * SY, -x * SY + z * CY
    p = (OX + S * xr, OY - S * (y * CP + zr * SP))
    EXTENT.append(p)
    return p


def ell(x, y, z, r):
    """A horizontal circle of radius r at (x,y,z) -> screen (cx, cy, rx, ry)."""
    cx, cy = P(x, y, z)
    return cx, cy, r * S, r * S * SP


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


WAL_D, WAL_L = "#241410", "#7E4C30"      # walnut ramp
WAL_HI = "#B8804F"                       # lamplight sheen
BRASS_D, BRASS_L = "#6E4E1E", "#D9B25E"


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


def quad3(name, pts3, fill, stroke=NONE, sw=1.6, opacity=None):
    kw = {"fill": fill, "stroke": NONE}
    if stroke != NONE:
        kw.update(stroke=stroke, strokeWidth=sw, join="round")
    if opacity is not None:
        kw["opacity"] = opacity
    d.path(poly([P(*p) for p in pts3]), name, **kw)


# --- lamp geometry first, so its glow lands on the plate --------------------------
LX, LZ = -4.8, 2.0                    # lamp position on the top slab
SH_B, SH_T = 30.6, 34.4               # shade bottom/top heights
scx, scy = P(LX, (SH_B + SH_T) / 2, LZ)

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#161420"), (1, "#070709")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7E7490", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#3E3850"), (0.6, "#262034"), (1, "#12101A")),
        stroke="#0C0A12", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#A898C0", strokeWidth=3, opacity=20)
# the lamp is the only light: wide glow, then a hot core around the shade
d.shape("ellipse", "Lamp glow", x=round(scx - 330), y=round(scy - 290),
        width=660, height=580,
        fill=rad((0, "#F0B060", 26), (0.5, "#C88040", 9), (1, "#6E4224", 0)),
        stroke=NONE)
d.shape("ellipse", "Lamp core", x=round(scx - 150), y=round(scy - 130),
        width=300, height=260,
        fill=rad((0, "#FFE0A0", 40), (1, "#FFE0A0", 0)), stroke=NONE)

FY = 596
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#38344A", 45), (1, "#100E18", 80)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#B8A8D8", strokeWidth=2, opacity=18)

# grounding shadow under the stand
sh = [P(x, 0, z) for x in (-9.3, 9.3) for z in (-6.3, 6.3)]
sx0, sx1 = min(p[0] for p in sh) - 60, max(p[0] for p in sh) + 60
sy0, sy1 = min(p[1] for p in sh) - 18, max(p[1] for p in sh) + 26
d.shape("ellipse", "Stand shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#040308", 72), (0.6, "#040308", 30), (1, "#040308", 0)),
        stroke=NONE)

# --- nightstand geometry (inches; x right, y up, +z back) -----------------------------
X0, X1 = -9.5, 9.5
Z0, Z1 = -6.5, 6.5
CY0, CY1 = 5.0, 22.5                 # carcass y range
OX0, OX1, OY0, OY1, OZ1 = -7.4, 7.4, 6.6, 13.9, 4.2   # cubby opening / interior

def leg(name, cx, cz):
    """Tapered leg: narrower at the floor."""
    b, t = 0.5, 0.8
    corners = [(cx - b, 0, cz - b), (cx + b, 0, cz - b), (cx + t, CY0 + 1.2, cz - t),
               (cx - t, CY0 + 1.2, cz - t), (cx - b, 0, cz + b), (cx + b, 0, cz + b),
               (cx + t, CY0 + 1.2, cz + t), (cx - t, CY0 + 1.2, cz + t)]
    prism(name, corners, dark="#1E0E08", light="#5E3620", lo=0.10, hi=0.9, ink=1.6)


for nm, (cx, cz) in {"Back L": (-8.3, 5.3), "Back R": (8.3, 5.3)}.items():
    leg(f"Leg {nm}", cx, cz)

# cubby interior: floor, back wall, then the books resting inside
quad3("Cubby floor", [(-7.2, 6.7, -6.4), (7.2, 6.7, -6.4), (7.2, 6.7, 4.1), (-7.2, 6.7, 4.1)],
      lin((0, 600), (0, 640), (0, "#8A5C3A"), (1, "#5E3822")))
quad3("Cubby back", [(-7.2, 6.7, 4.15), (7.2, 6.7, 4.15), (7.2, 13.8, 4.15), (-7.2, 13.8, 4.15)],
      lin((0, 430), (0, 560), (0, "#7A4E30"), (1, "#3E2414")))
quad3("Cubby left wall", [(-7.4, 6.7, -6.4), (-7.4, 6.7, 4.15), (-7.4, 13.8, 4.15), (-7.4, 13.8, -6.4)],
      lin((430, 500), (600, 620), (0, "#5E3822"), (1, "#3A2010")))
# ceiling shadow inside the opening
quad3("Cubby ceiling shade", [(-7.3, 13.8, -6.4), (7.3, 13.8, -6.4), (7.3, 13.8, 4.15), (-7.3, 13.8, 4.15)],
      lin((0, 430), (0, 470), (0, "#0C0603", 80), (1, "#0C0603", 0)), stroke=NONE)
# two books lying flat, muted cloth colors
prism("Book 1", box(-6.6, 6.7, -5.6, 4.4, 8.1, 2.6),
      dark="#2E1A16", light="#9C4C44", lo=0.25, hi=0.9, ink=1.4)
prism("Book 2", box(-5.4, 8.1, -4.4, 5.8, 9.3, 3.4),
      dark="#1E2830", light="#6E8CA4", lo=0.20, hi=0.9, ink=1.4)
# page-block slivers on the books' front edges
pa, pb = P(-6.2, 7.9, -5.62), P(3.9, 7.9, -5.62)
d.path(f"M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}", "Book 1 pages",
       fill=NONE, stroke="#E8DCC0", strokeWidth=2.2, opacity=55, cap="round")
pa, pb = P(-5.0, 9.0, -4.42), P(5.2, 9.0, -4.42)
d.path(f"M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}", "Book 2 pages",
       fill=NONE, stroke="#E8DCC0", strokeWidth=2.0, opacity=55, cap="round")

# face frame: side walls, stiles, rails — then the drawer above
prism("Left wall", box(X0, CY0, Z0, -7.4, CY1, Z1), dark="#2A1810", light="#6E442A", lo=0.08, hi=0.9)
prism("Right wall", box(7.4, CY0, Z0, X1, CY1, Z1), lo=0.06, hi=0.9)
prism("Left stile", box(X0, CY0, Z0 - 0.9, -7.4, OY1 + 0.1, Z0), lo=0.10, hi=0.95)
prism("Right stile", box(7.4, CY0, Z0 - 0.9, X1, OY1 + 0.1, Z0), lo=0.10, hi=0.95)
prism("Bottom rail", box(-7.4, CY0, Z0 - 0.9, 7.4, 6.6, Z0), lo=0.08, hi=0.9)
prism("Mid rail", box(-7.4, OY1, Z0 - 0.9, 7.4, 14.4, Z0), lo=0.08, hi=0.9)
prism("Drawer face", box(-8.6, 14.4, Z0 - 0.5, 8.6, 22.2, Z0 + 0.1),
      dark="#2E1A10", light="#8A5638", lo=0.12, hi=1.0, ink=2.0)
# drawer bevel lights
for nm, a, b in (("L", (-8.1, 21.6, Z0 - 0.55), (-8.1, 15.0, Z0 - 0.55)),
                 ("T", (-8.1, 21.6, Z0 - 0.55), (8.1, 21.6, Z0 - 0.55))):
    qa, qb = P(*a), P(*b)
    d.path(f"M{qa[0]:.1f},{qa[1]:.1f} L{qb[0]:.1f},{qb[1]:.1f}", f"Drawer bevel {nm}",
           fill=NONE, stroke="#DCA878", strokeWidth=1.8, opacity=45, cap="round")
# brass drawer knob
kx, ky = P(0, 18.3, Z0 - 0.6)
d.shape("ellipse", "Drawer knob", x=round(kx - 5.5), y=round(ky - 5.5), width=11, height=11,
        fill=rad((0, "#F2DA94"), (0.6, "#C89A46"), (1, "#6E4E1E")),
        stroke="#3A280C", strokeWidth=1.5)
d.shape("ellipse", "Knob glint", x=round(kx - 2.4), y=round(ky - 3.2), width=4, height=4,
        fill="#FFF2C8", opacity=80, stroke=NONE)

# top slab, slightly proud
prism("Top slab", box(X0 - 0.9, CY1, Z0 - 0.9, X1 + 0.9, CY1 + 1.7, Z1 + 0.9),
      dark="#2A180E", light="#8E5A3A", lo=0.10, hi=1.0, ink=2.0)
# lamplight pooling on the top surface
lx, ly = P(LX, CY1 + 1.75, LZ - 1)
d.shape("ellipse", "Lamp pool", x=round(lx - 110), y=round(ly - 34), width=220, height=68,
        fill=rad((0, "#F0BE7A", 30), (1, "#F0BE7A", 0)), stroke=NONE)

for nm, (cx, cz) in {"Front L": (-8.3, -5.3), "Front R": (8.3, -5.3)}.items():
    leg(f"Leg {nm}", cx, cz)

# --- the lamp ---------------------------------------------------------------------------
# brass foot disc
fx, fy, frx, fry = ell(LX, CY1 + 1.75, LZ, 1.7)
d.shape("ellipse", "Lamp foot", x=round(fx - frx), y=round(fy - fry),
        width=round(2 * frx), height=round(2 * fry),
        fill=rad((0, "#F2DA94"), (0.55, "#C89A46"), (1, "#6E4E1E")),
        stroke="#3A280C", strokeWidth=1.6)
# stem
sa, sb = P(LX - 0.28, CY1 + 1.8, LZ), P(LX - 0.28, SH_B + 0.4, LZ)
sa2, sb2 = P(LX + 0.28, CY1 + 1.8, LZ), P(LX + 0.28, SH_B + 0.4, LZ)
d.path(f"M{sa[0]:.1f},{sa[1]:.1f} L{sb[0]:.1f},{sb[1]:.1f} L{sb2[0]:.1f},{sb2[1]:.1f} L{sa2[0]:.1f},{sa2[1]:.1f} Z",
       "Lamp stem", fill=lin((sa[0], 0), (sa2[0], 0), (0, "#8A6224"), (0.5, "#E8C06A"), (1, "#6E4E1E")),
       stroke="#3A280C", strokeWidth=1.2)
# shade: glowing frustum — trapezoid + bottom-rim arc
bcx, bcy, brx, bry = ell(LX, SH_B, LZ, 3.4)
tcx, tcy, trx, try_ = ell(LX, SH_T, LZ, 2.3)
sh_pts = [(bcx - brx, bcy + bry * 0.25), (bcx + brx, bcy + bry * 0.25),
          (tcx + trx, tcy + try_ * 0.6), (tcx - trx, tcy + try_ * 0.6)]
d.path(poly(sh_pts), "Lamp shade", stroke="#4A2C10", strokeWidth=1.8, join="round",
       fill=lin((0, tcy), (0, bcy), (0, "#C8803C"), (0.55, "#F0B45E"), (1, "#FFE4A8")))
# shade bottom opening: warm dark underside arc
d.path(f"M{bcx - brx:.1f},{bcy + bry * 0.25:.1f} A{brx:.1f},{bry:.1f} 0 0 0 {bcx + brx:.1f},{bcy + bry * 0.25:.1f}",
       "Shade underside", fill=NONE, stroke="#9A5C22", strokeWidth=3.5, opacity=80, cap="round")
# shade top rim
d.shape("ellipse", "Shade top rim", x=round(tcx - trx), y=round(tcy - try_),
        width=round(2 * trx), height=round(2 * try_),
        fill=lin((0, tcy - try_), (0, tcy + try_), (0, "#8A5424"), (1, "#C8803C")),
        stroke="#4A2C10", strokeWidth=1.5)
# bulb glint peeking under the shade
d.shape("ellipse", "Bulb glint", x=round(bcx - 6), y=round(bcy + bry * 0.2), width=12, height=6,
        fill=rad((0, "#FFF4D0", 85), (1, "#FFF4D0", 0)), stroke=NONE)

# --- the glass of water ------------------------------------------------------------------
GX, GZ, GR, GH = 5.4, -2.6, 1.05, 3.6
gbx, gby, gb_rx, gb_ry = ell(GX, CY1 + 1.8, GZ, GR * 0.9)
gtx, gty, gt_rx, gt_ry = ell(GX, CY1 + 1.8 + GH, GZ, GR)
gwx, gwy, gw_rx, gw_ry = ell(GX, CY1 + 1.8 + GH * 0.62, GZ, GR * 0.96)
# glass body, translucent
body = [(gbx - gb_rx, gby), (gbx + gb_rx, gby),
        (gtx + gt_rx, gty), (gtx - gt_rx, gty)]
d.path(poly(body), "Glass body", stroke="#C8DCE8", strokeWidth=1.6, join="round",
       fill=lin((0, gty), (0, gby), (0, "#B8D4E0", 10), (0.6, "#A8C4D4", 22), (1, "#8AA8B8", 30)),
       opacity=90)
# water inside
wbx, wby, wb_rx, wb_ry = ell(GX, CY1 + 2.0, GZ, GR * 0.82)
water = [(wbx - wb_rx, wby), (wbx + wb_rx, wby),
         (gwx + gw_rx, gwy), (gwx - gw_rx, gwy)]
d.path(poly(water), "Water", stroke=NONE,
       fill=lin((0, gwy), (0, wby), (0, "#7A9CB0", 30), (1, "#5E7E92", 45)))
d.shape("ellipse", "Waterline", x=round(gwx - gw_rx), y=round(gwy - gw_ry),
        width=round(2 * gw_rx), height=round(2 * gw_ry),
        fill=NONE, stroke="#D8ECF4", strokeWidth=1.8, opacity=55)
# rim + base ellipses
d.shape("ellipse", "Glass rim", x=round(gtx - gt_rx), y=round(gty - gt_ry),
        width=round(2 * gt_rx), height=round(2 * gt_ry),
        fill=NONE, stroke="#D8ECF4", strokeWidth=1.8, opacity=60)
# long highlight down the glass's left edge
d.path(f"M{gtx - gt_rx * 0.55:.1f},{gty + 3:.1f} L{gbx - gb_rx * 0.55:.1f},{gby - 4:.1f}",
       "Glass highlight", fill=NONE, stroke="#F0F8FC", strokeWidth=2.2, opacity=45, cap="round")

# warm rim light on the stand's left edge where the lamp reaches
re0, re1 = P(X0 - 0.9, CY1 + 1.4, Z0 - 0.6), P(X0 - 0.9, CY0 + 1.0, Z0 - 0.6)
d.path(f"M{re0[0]:.1f},{re0[1]:.1f} L{re1[0]:.1f},{re1[1]:.1f}", "Left edge lamplight",
       fill=NONE, stroke="#E8B070", strokeWidth=2.5, opacity=30, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("nightstand extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#EEE4F4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#B0A2C4", justify="center")
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


caption("NIGHTSTAND", "WALNUT · BRASS · GLASS")
d.finish("nightstand-V1R00")
