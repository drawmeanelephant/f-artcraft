#!/usr/bin/env python3
"""Sleigh bed — field plate V1R00. Three-quarter view down the bed's length:
a cherry sleigh bed, headboard and footboard scrolled like a winter
conveyance, a snow-drift of white bedding between them with a grey wool
throw folded at the foot. Blue night plate, snow-drift mood. 1000x1000.
The scrolled boards are cross-section polygons extruded along the bed's
width: their near end-caps carry the true scroll profile to the viewer.
Boxy parts (rails, mattress, throw) are 8-corner prisms.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Sleigh Bed — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#22100C"   # warm dark, not black
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


def smooth(pts, closed=True, k=1.0):
    """Catmull-Rom through pts as cubic Beziers."""
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(28), math.radians(20)
S, OX, OY = 10.8, 518.0, 640.0
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
    a = [int(hex1[i:i + 2], 16) for i in (1, 3, 5)]
    c = [int(hex2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (c[i] - a[i]) * b) for i in range(3))


CH_D, CH_L = "#38160E", "#A05230"        # cherry ramp
CH_HI = "#C87A50"


def vgrad_for(pts, dark, light, b):
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    return lin((0, y0), (0, y1), (0, shade(dark, light, min(1, b + 0.12))),
                                (1, shade(dark, light, b)))


def prism(name, corners, dark=CH_D, light=CH_L, lo=0.06, hi=0.94, ink=1.8):
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
        d.path(poly(pts), name, fill=vgrad_for(pts, dark, light, b),
               stroke=INK, strokeWidth=ink, join="round")
    return faces


def shell(name, sect, z0, z1, dark=CH_D, light=CH_L, lo=0.05, hi=0.95, ink=1.8):
    """A curved board: closed (x,y) cross-section extruded z0..z1.
    Emits one quad per profile edge plus the NEAR (z0) end cap — the cap
    carries the true scroll silhouette to the viewer. The cross-section may
    be wound either way; signed area decides which way normals point."""
    n = len(sect)
    area = sum(sect[i][0] * sect[(i + 1) % n][1] - sect[(i + 1) % n][0] * sect[i][1]
               for i in range(n))
    winding = 1.0 if area > 0 else -1.0      # CCW polygon => outward = (ey,-ex)
    faces = []
    for i in range(n):
        a, b = sect[i], sect[(i + 1) % n]
        ex, ey = b[0] - a[0], b[1] - a[1]
        L = math.hypot(ex, ey) or 1
        nrm = (winding * ey / L, -winding * ex / L, 0.0)
        if nrm[0] * TO_VIEWER[0] + nrm[1] * TO_VIEWER[1] <= 0.02:
            continue
        lam = max(0.0, sum(nrm[k] * LIGHT[k] for k in range(3)))
        quad = [(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1), (a[0], a[1], z1)]
        dep = sum(depth(*p) for p in quad) / 4
        faces.append((dep, [P(*p) for p in quad], lam, False))
    # near end cap: the scroll silhouette, always facing -z toward the viewer
    cap = [(x, y, z0) for x, y in sect]
    lam = max(0.0, -LIGHT[2])
    dep = sum(depth(*p) for p in cap) / len(cap)
    faces.append((dep - 0.01, [P(*p) for p in cap], lam, True))
    for dep, pts, lam, is_cap in sorted(faces, key=lambda t: -t[0]):
        b = lo + (hi - lo) * lam ** 0.8
        if is_cap:
            d.path(poly(pts), name, fill=vgrad_for(pts, dark, light, b * 0.9),
                   stroke=INK, strokeWidth=ink, join="round")
        else:
            d.path(poly(pts), name, fill=vgrad_for(pts, dark, light, b),
                   stroke=NONE, join="round")


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#131420"), (1, "#060608")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#6E7A9C", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#3C4258"), (0.6, "#262A3C"), (1, "#111218")),
        stroke="#0C0A12", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8C4E0", strokeWidth=3, opacity=20)
# cold moonlit wash, high left
d.shape("ellipse", "Moonlight", x=170, y=90, width=560, height=520,
        fill=rad((0, "#B8C8E8", 16), (0.55, "#6E7EA8", 6), (1, "#3A4468", 0)),
        stroke=NONE)

FY = 562
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#3A3E52", 45), (1, "#0E0E16", 80)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#C0CCE8", strokeWidth=2, opacity=18)

# grounding shadow under the bed
sh = [P(x, 0, z) for x in (-25.5, 25.5) for z in (-9.5, 9.5)]
sx0, sx1 = min(p[0] for p in sh) - 55, max(p[0] for p in sh) + 55
sy0, sy1 = min(p[1] for p in sh) - 20, max(p[1] for p in sh) + 26
d.shape("ellipse", "Bed shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#040308", 70), (0.6, "#040308", 30), (1, "#040308", 0)),
        stroke=NONE)

# --- sleigh bed geometry (inches; bed length along x, head at -x) --------------------
ZW = (-8.0, 8.0)                     # board depth across the bed width

# scrolled headboard: x-y cross-section, CCW from inner-face bottom.
# Inner face (the side pillows lean on) runs up and rolls back at the top;
# outer face returns down the back; the tip tucks into the curl.
HEAD = [(-23.4, 4.0), (-23.4, 15.0), (-23.6, 21.0), (-24.6, 26.0),
        (-26.6, 29.8), (-29.0, 31.6), (-30.6, 31.4), (-31.4, 30.4),
        (-31.6, 29.2), (-30.9, 28.8), (-30.6, 27.6), (-29.6, 26.6),
        (-28.0, 25.8), (-26.2, 24.4), (-25.4, 21.5), (-25.4, 4.0)]
shell("Headboard", HEAD, *ZW)

# scrolled footboard: mirror of the headboard, lower, curling toward +x
FOOT = [(23.4, 4.0), (23.4, 12.5), (23.6, 17.0), (24.6, 21.0),
        (26.6, 24.2), (29.0, 25.6), (30.4, 25.2), (31.0, 24.2),
        (31.1, 23.2), (30.4, 22.8), (30.1, 21.7), (29.2, 20.9),
        (27.7, 20.3), (26.0, 19.0), (25.4, 16.5), (25.4, 4.0)]
shell("Footboard", FOOT, *ZW)

# far side rail (mostly hidden behind the mattress)
prism("Far side rail", box(-23.4, 6.5, 8.0, 23.4, 11.5, 9.4), lo=0.04, hi=0.7)

# mattress, ivory ticking
prism("Mattress", box(-23.0, 11.5, -8.0, 23.0, 16.6, 8.0),
      dark="#8A8494", light="#F0EBDD", lo=0.30, hi=1.02, ink=1.6)
# piping along the mattress's near top edge
pa, pb = P(-22.6, 16.5, -7.9), P(22.6, 16.5, -7.9)
d.path(f"M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}", "Mattress piping",
       fill=NONE, stroke="#A89CA8", strokeWidth=1.8, opacity=60, cap="round")

# pillows propped against the headboard's inner face
for i, (px, pz) in enumerate([(-19.5, -3.6), (-19.0, 3.0)]):
    c = P(px, 18.2, pz)
    pts = [(c[0] - 40, c[1] + 26), (c[0] - 47, c[1] + 8), (c[0] - 16, c[1] - 24),
           (c[0] + 28, c[1] - 38), (c[0] + 50, c[1] - 24), (c[0] + 22, c[1] + 10),
           (c[0] - 12, c[1] + 30)]
    d.path(smooth(pts), f"Pillow {i+1}",
           fill=rad((0, "#F8F4EC"), (0.7, "#E4E2EE"), (1, "#B8B6CC")),
           stroke="#5E5470", strokeWidth=2.5)
    d.path(smooth([(c[0] - 30, c[1] + 8), (c[0] - 2, c[1] - 14), (c[0] + 28, c[1] - 26)],
                  closed=False), f"Pillow {i+1} crease",
           fill=NONE, stroke="#8C84A4", strokeWidth=2.2, opacity=40, cap="round")

# duvet over the foot two-thirds, snow-white, draping slightly over the near rail
prism("Duvet", box(-14.0, 11.5, -8.6, 23.4, 18.2, 8.6),
      dark="#9A96AC", light="#F6F2EA", lo=0.35, hi=1.05, ink=1.6)
# snow-drift mounds on the duvet top
for i, (mx, mz, w, h, o) in enumerate([(-4, -2, 120, 34, 20), (10, 3, 150, 42, 24),
                                       (18, -4, 100, 30, 18)]):
    c = P(mx, 18.4, mz)
    d.shape("ellipse", f"Drift {i+1}", x=round(c[0] - w / 2), y=round(c[1] - h / 2),
            width=w, height=h, fill=rad((0, "#FFFFFF", o), (1, "#FFFFFF", 0)), stroke=NONE)
# duvet hem: a soft drop over the near side rail
hm = [P(x, 12.0, -8.7) for x in (-14, -6, 2, 10, 18, 23.2)]
hem_top = [(p[0], p[1]) for p in hm]
hem_bot = [(p[0], p[1] + 26 + (6 if i % 2 else 0)) for i, p in enumerate(hm)]
dd = "M%.1f,%.1f " % hem_top[0] + " ".join("L%.1f,%.1f" % p for p in hem_top[1:])
dd += " " + smooth(hem_bot[::-1], closed=False, k=1.2)[1:] + " Z"
d.path(dd, "Duvet drop", stroke="#4A4258", strokeWidth=2.0, join="round",
       fill=lin((0, hem_top[0][1]), (0, hem_bot[0][1] + 20),
                (0, "#E8E6F0"), (1, "#A8A2BC")))
# folded grey wool throw across the foot
prism("Wool throw", box(14.5, 18.0, -8.9, 21.5, 19.6, 8.9),
      dark="#3A3E4A", light="#8A92A6", lo=0.15, hi=0.95, ink=1.8)
for i in range(3):
    a = P(14.6 + i * 2.3, 19.7, -8.9)
    b = P(14.6 + i * 2.3, 19.7, 8.9)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Throw stripe {i+1}",
           fill=NONE, stroke="#5A4A56", strokeWidth=2.2, opacity=40, cap="round")

# near side rail, in front of the mattress
prism("Near side rail", box(-23.4, 6.5, -9.6, 23.4, 11.5, -8.0), lo=0.08, hi=0.95, ink=2.0)
ra, rb = P(-22.8, 11.2, -9.7), P(22.8, 11.2, -9.7)
d.path(f"M{ra[0]:.1f},{ra[1]:.1f} L{rb[0]:.1f},{rb[1]:.1f}", "Rail bead light",
       fill=NONE, stroke="#D89A70", strokeWidth=2.0, opacity=45, cap="round")

# bracket feet under the four board corners
for i, (fx, fz) in enumerate([(-24.4, -8.6), (-24.4, 8.6), (24.4, -8.6), (24.4, 8.6)]):
    prism(f"Foot {i+1}", box(fx - 1.6, 0, fz - 1.2, fx + 1.6, 6.5, fz + 1.2),
          dark="#1E0C06", light="#5E2E18", lo=0.06, hi=0.85, ink=1.6)

# moonlight catching the scroll tips
for nm, p in (("Head", (-30.6, 31.4, -6)), ("Foot", (30.4, 25.2, -6))):
    hxp, hyp = P(*p)
    d.shape("ellipse", f"{nm} scroll sheen", x=round(hxp - 26), y=round(hyp - 14),
            width=52, height=28, fill=rad((0, CH_HI, 30), (1, CH_HI, 0)), stroke=NONE)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("bed extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#ECF0F8", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#AEA8C8", justify="center")
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


caption("SLEIGH BED", "CHERRY · LINEN · WOOL")
d.finish("sleigh-bed-V1R00")
