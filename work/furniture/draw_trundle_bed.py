#!/usr/bin/env python3
"""Trundle bed — field plate V1R00. Three-quarter from the front right:
a low honey-pine frame bed, headboard at the left end, footboard at the
right; the trundle — a shallow drawer of a bed on casters — is rolled out
toward the viewer with its thin pad mattress, a folded quilt and a small
pillow. Pine plate, sleepover mood. 1000x1000.
Modelled in inches (x right, y up, +z back) and projected with a fixed
yaw + pitch; everything is 8-corner prisms, drawn far to near.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Trundle Bed — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241408"   # warm dark, not black
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


def smooth(pts, closed=True, k=1.0):
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
YAW, PITCH = math.radians(26), math.radians(22)
S, OX, OY = 6.0, 502.0, 650.0
CY, SY = math.cos(YAW), math.sin(YAW)
CP, SP = math.cos(PITCH), math.sin(PITCH)


def P(x, y, z):
    xr, zr = x * CY + z * SY, -x * SY + z * CY
    p = (OX + S * xr, OY - S * (y * CP + zr * SP))
    EXTENT.append(p)
    return p


def Pq(x, y, z):
    """Project without registering extent (guides, shadow bounds)."""
    xr, zr = x * CY + z * SY, -x * SY + z * CY
    return (OX + S * xr, OY - S * (y * CP + zr * SP))


def depth(x, y, z):
    """View-space distance; smaller = nearer the viewer (front-right-above)."""
    return -x * SY * CP - y * SP + z * CY * CP


def box(x0, y0, z0, x1, y1, z1):
    return [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]


FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
TO_VIEWER = (SY * CP, SP, -CY * CP)          # normals facing this draw
LIGHT = (-0.40, 0.82, -0.36)
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


PIN_D, PIN_L = "#5E3C1C", "#C89858"        # honey pine ramp
PIN_HI = "#E8C088"
PIN_FAR = ("#3E2810", "#8A6034")           # dimmer pine for far/dim parts
CREAM_D, CREAM_L = "#8A8090", "#F0EADD"


def prism(name, corners, dark=PIN_D, light=PIN_L, lo=0.06, hi=0.94, ink=1.8):
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


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#16120A"), (1, "#070503")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#D8AA60", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#584622"), (0.55, "#3A2C14"), (1, "#1C1206")),
        stroke="#100A04", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EED8A8", strokeWidth=3, opacity=24)
# sleepover lamplight low on the left
d.shape("ellipse", "Lamp bloom", x=110, y=170, width=560, height=480,
        fill=rad((0, "#E8A04C", 0.13), (0.55, "#B87830", 0.05), (1, "#B87830", 0)),
        stroke=NONE)

# --- floor boards closing on the disc arc --------------------------------------------
FYB = 700
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX - hw:.1f},{FYB} L{PCX + hw:.1f},{FYB} A420,420 0 0 1 {PCX - hw:.1f},{FYB} Z",
       "Floor", fill=lin((0, FYB), (0, 880), (0, "#4A3E28", 0.5),
                         (0.5, "#221A0E", 0.75), (1, "#0E0804", 0.92)), stroke=NONE)
d.path(f"M{PCX - hw + 6:.1f},{FYB} L{PCX + hw - 6:.1f},{FYB}", "Floor edge light",
       fill=NONE, stroke="#E8D0A0", strokeWidth=2, opacity=16)
for i, yb in enumerate([752, 792, 832]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Board seam {i+1}",
           fill=NONE, stroke="#5A4A2C", strokeWidth=2, opacity=24)

# grounding shadow under bed + rolled-out trundle
bxs = [Pq(x, 0, z) for x, z in ((-36, -46), (36, -46), (36, 18), (-36, 18))]
sx0, sx1 = min(p[0] for p in bxs) - 16, max(p[0] for p in bxs) + 16
sy0, sy1 = min(p[1] for p in bxs) - 10, max(p[1] for p in bxs) + 24
d.shape("ellipse", "Bed shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#040201", 0.72), (0.6, "#040201", 0.32), (1, "#040201", 0)),
        stroke=NONE)
# darkness in the slot under the frame where the trundle lives
slot = [P(-30, 2, -15.8), P(30, 2, -15.8), P(30, 11.5, -15.8), P(-30, 11.5, -15.8)]
d.path(poly(slot), "Under-bed slot", fill=lin((0, 640), (0, 700),
       (0, "#0A0603", 0.85), (1, "#1A0F06", 0.5)), stroke=NONE)

# --- main bed -------------------------------------------------------------------------
PX = 32.0                              # post centres
POST_W = 1.3


def post(name, cx, cz, ytop, dim=False):
    dk, lt = PIN_FAR if dim else (PIN_D, PIN_L)
    prism(name, box(cx - POST_W, 0, cz - POST_W, cx + POST_W, ytop, cz + POST_W),
          dark=dk, light=lt, lo=0.05, hi=0.95, ink=1.7)
    bx, by = P(cx, ytop + 1.0, cz)
    d.shape("ellipse", f"{name} cap", x=round(bx - 8), y=round(by - 7),
            width=16, height=14,
            fill=rad((0, shade(lt, "#FFFFFF", 0.18)), (0.65, lt), (1, dk)),
            stroke=INK, strokeWidth=1.4)


# far side: back posts, back rail, then the headboard slab
post("Post head far", -PX, 14.5, 42, dim=True)
post("Post foot far", PX, 14.5, 30, dim=True)
prism("Rail far", box(-PX, 11, 13.2, PX, 16, 16.2), dark=PIN_FAR[0], light=PIN_FAR[1],
      lo=0.05, hi=0.85, ink=1.5)
# headboard: tall panel slab at the left end
prism("Headboard", box(-34.5, 16, -14.5, -31.5, 40, 14.5),
      dark=PIN_D, light=PIN_L, lo=0.08, hi=0.9, ink=1.8)
# bead lines on the headboard face
for zz in (-8, 0, 8):
    a, b = P(-31.4, 20, zz), P(-31.4, 38, zz)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Headboard bead {zz:+g}",
           fill=NONE, stroke="#3A2410", strokeWidth=1.8, opacity=50)
hb_rim_a, hb_rim_b = P(-31.4, 40.2, -14.5), P(-31.4, 40.2, 14.5)
d.path(f"M{hb_rim_a[0]:.1f},{hb_rim_a[1]:.1f} L{hb_rim_b[0]:.1f},{hb_rim_b[1]:.1f}",
       "Headboard rim light", fill=NONE, stroke=PIN_HI, strokeWidth=2.2,
       opacity=40, cap="round")

# footboard: lower panel at the right end
prism("Footboard", box(31.5, 16, -14.5, 34.5, 28, 14.5),
      dark=PIN_D, light=PIN_L, lo=0.08, hi=0.95, ink=1.8)
# end rails tying the posts under the mattress line
prism("Head end rail", box(-33.6, 11, -15.8, -30.4, 15.5, 15.8),
      dark=PIN_FAR[0], light=PIN_FAR[1], lo=0.05, hi=0.85, ink=1.6)
prism("Foot end rail", box(30.4, 11, -15.8, 33.6, 15.5, 15.8),
      dark=PIN_D, light=PIN_L, lo=0.06, hi=0.9, ink=1.6)

# mattress + bedding
prism("Mattress", box(-31, 16, -15, 31, 22.5, 15),
      dark=CREAM_D, light=CREAM_L, lo=0.30, hi=1.02, ink=1.7)
pa, pb = P(-30.7, 22.6, -14.7), P(30.7, 22.6, -14.7)
d.path(f"M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}", "Mattress piping",
       fill=NONE, stroke="#A89CA8", strokeWidth=1.7, opacity=50, cap="round")
# duvet over the middle third of the mattress
prism("Duvet", box(-30.5, 22.5, -8, 10, 24.6, 15.2),
      dark="#5E2E22", light="#C06848", lo=0.12, hi=0.95, ink=1.7)
da, db = P(-30.3, 23.6, -7.8), P(9.8, 23.6, -7.8)
d.path(f"M{da[0]:.1f},{da[1]:.1f} L{db[0]:.1f},{db[1]:.1f}", "Duvet fold",
       fill=NONE, stroke="#3A1A10", strokeWidth=2.0, opacity=45, cap="round")

# pillow at the head end
cx_, cy_ = P(-23, 25.4, 2)
pts = [(cx_ - 40, cy_ + 24), (cx_ - 50, cy_ + 4), (cx_ - 16, cy_ - 20),
       (cx_ + 34, cy_ - 28), (cx_ + 52, cy_ - 12), (cx_ + 22, cy_ + 14),
       (cx_ - 14, cy_ + 28)]
d.path(smooth(pts), "Pillow", stroke="#5E5470", strokeWidth=2.2,
       fill=rad((0, "#F6F0E4"), (0.7, "#E0DCE8"), (1, "#B4AEC2")))
d.path(smooth([(cx_ - 28, cy_ + 8), (cx_ - 2, cy_ - 8), (cx_ + 28, cy_ - 18)],
              closed=False), "Pillow crease",
       fill=NONE, stroke="#8C84A4", strokeWidth=2.0, opacity=40, cap="round")

# near posts and the near rail last (front face of the frame)
post("Post head near", -PX, -14.5, 42)
post("Post foot near", PX, -14.5, 30)
prism("Rail near", box(-PX, 11, -16.2, PX, 16, -13.2), lo=0.08, hi=0.95, ink=1.9)
ra, rb = P(-PX, 15.5, -16.4), P(PX, 15.5, -16.4)
d.path(f"M{ra[0]:.1f},{ra[1]:.1f} L{rb[0]:.1f},{rb[1]:.1f}", "Rail bead light",
       fill=NONE, stroke=PIN_HI, strokeWidth=1.9, opacity=40, cap="round")
# the duvet's near edge droops over the rail face
prism("Duvet drape", box(-30.5, 14.5, -17.6, 10, 22.5, -15.4),
      dark="#5E2E22", light="#B85E40", lo=0.10, hi=0.9, ink=1.7)
hem_a, hem_b = P(-30.2, 15.6, -17.7), P(9.8, 15.6, -17.7)
d.path(f"M{hem_a[0]:.1f},{hem_a[1]:.1f} L{hem_b[0]:.1f},{hem_b[1]:.1f}", "Duvet hem",
       fill=NONE, stroke="#2E140C", strokeWidth=2.0, opacity=50, cap="round")
dc_, dd_ = P(-12, 22.6, -16.8), P(-12, 15.0, -17.5)
d.path(f"M{dc_[0]:.1f},{dc_[1]:.1f} L{dd_[0]:.1f},{dd_[1]:.1f}", "Duvet crease",
       fill=NONE, stroke="#3A1A10", strokeWidth=1.8, opacity=40, cap="round")

# --- the trundle, rolled out toward the viewer ------------------------------------------
# rear casters, dim under the bed
for cx2 in (-24, 24):
    prism(f"Caster rear {cx2:+g}", box(cx2 - 1.4, 0, -17.5, cx2 + 1.4, 3.0, -15.0),
          dark="#2A2018", light="#6A5844", lo=0.04, hi=0.7, ink=1.3)
# trundle body: a long shallow drawer
prism("Trundle body", box(-27, 2.5, -44, 27, 9.5, -15.5),
      dark="#4A3014", light="#9A6E38", lo=0.05, hi=0.9, ink=1.8)
# drawer face, a touch proud of the body, with two fielded panels + knobs
prism("Trundle face", box(-28.2, 1.5, -46.2, 28.2, 11.2, -44),
      dark=PIN_D, light=PIN_L, lo=0.08, hi=0.98, ink=1.9)
for hx, tag in ((-14.2, "L"), (14.2, "R")):
    panel = [P(hx - 11.5, 3.4, -46.25), P(hx + 11.5, 3.4, -46.25),
             P(hx + 11.5, 9.8, -46.25), P(hx - 11.5, 9.8, -46.25)]
    d.path(poly(panel), f"Trundle panel {tag}",
           fill=lin((0, min(p[1] for p in panel)), (0, max(p[1] for p in panel)),
                    (0, "#7A5326", None), (1, "#38220E", None)),
           stroke="#1C1006", strokeWidth=1.7, join="round")
for hx, tag in ((-4.5, "L"), (4.5, "R")):
    kx, ky = P(hx, 6.6, -46.6)
    d.shape("ellipse", f"Knob {tag}", x=kx - 4.6, y=ky - 4.6, width=9.2, height=9.2,
            fill=rad((0, "#F0D8A8"), (0.6, "#B8863C"), (1, "#4A3010")),
            stroke=INK, strokeWidth=1.3)

# front casters under the face
for cx2 in (-24, 24):
    prism(f"Caster front {cx2:+g}", box(cx2 - 1.5, 0, -45.5, cx2 + 1.5, 3.2, -43.0),
          dark="#2A2018", light="#7A6648", lo=0.05, hi=0.85, ink=1.4)
    wx, wy = P(cx2, 1.2, -45.7)
    d.shape("ellipse", f"Caster hub {cx2:+g}", x=wx - 3.2, y=wy - 3.2,
            width=6.4, height=6.4, fill="#C8B888", stroke=INK, strokeWidth=1.1)

# thin pad mattress on the trundle + sleepover dressing
prism("Trundle pad", box(-26, 9.5, -43.5, 26, 13.2, -16),
      dark=CREAM_D, light=CREAM_L, lo=0.32, hi=1.02, ink=1.6)
ta, tb = P(-25.7, 13.3, -43.2), P(25.7, 13.3, -43.2)
d.path(f"M{ta[0]:.1f},{ta[1]:.1f} L{tb[0]:.1f},{tb[1]:.1f}", "Pad piping",
       fill=NONE, stroke="#A89CA8", strokeWidth=1.6, opacity=50, cap="round")
# folded guest quilt across the pad's right half
prism("Guest quilt", box(-2, 13.2, -42.5, 26.5, 15.0, -20),
      dark="#2E3E30", light="#7E9A6E", lo=0.14, hi=0.95, ink=1.6)
ga_, gb_ = P(-1.8, 14.2, -42.3), P(-1.8, 14.2, -20.5)
d.path(f"M{ga_[0]:.1f},{ga_[1]:.1f} L{gb_[0]:.1f},{gb_[1]:.1f}", "Guest quilt fold",
       fill=NONE, stroke="#141C14", strokeWidth=2.0, opacity=45, cap="round")
# little guest pillow on the pad's left
tx, ty = P(-15, 14.6, -32)
tpts = [(tx - 30, ty + 15), (tx - 36, ty + 2), (tx - 12, ty - 13),
        (tx + 22, ty - 18), (tx + 34, ty - 6), (tx + 14, ty + 10),
        (tx - 10, ty + 17)]
d.path(smooth(tpts), "Guest pillow", stroke="#5E5470", strokeWidth=2.0,
       fill=rad((0, "#F0EADC"), (0.7, "#D8D2E0"), (1, "#ACA4BC")))

# warm rim light along the near rail and trundle face top
ta2, tb2 = P(-28, 11.4, -46.3), P(28, 11.4, -46.3)
d.path(f"M{ta2[0]:.1f},{ta2[1]:.1f} L{tb2[0]:.1f},{tb2[1]:.1f}", "Trundle rim light",
       fill=NONE, stroke="#FFCE8A", strokeWidth=2.2, opacity=38, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("trundle extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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


caption("TRUNDLE BED", "PINE · IRON · COTTON")
d.finish("trundle-bed-V1R00")
