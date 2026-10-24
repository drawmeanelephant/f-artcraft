#!/usr/bin/env python3
"""Workbench — field plate V1R00. Three-quarter view from the front right:
a Roubo-style bench with a thick maple slab top, a beech face vise holding
a standing board, a tail-vise wagon and a row of dog holes, a low plank
shelf between the leg pairs, a hand plane resting on the top and curls of
shaving under the vise. Maple plate, woodshop mood — a warm window shaft
from the upper left with dust in it. 1000x1000.
Modelled in inches (x right, y up, +z back), projected with a fixed
yaw + pitch; carcass parts are 8-corner prisms culled by view normal and
shaded by the window light. House style: gradients + translucent shading,
never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Workbench — Field Plate", 1000, 1000)

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


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(30), math.radians(27)
S, OX, OY = 5.9, 502.0, 732.0
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
LIGHT = (-0.55, 0.72, -0.42)                  # window light from the upper left
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


def prism(name, corners, ramp=("#241408", "#7A4E26"), lo=0.06, hi=0.94, sw=1.8):
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
        d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=sw, join="round")


def flat_ellipse(cx, y, cz, r, label, **kw):
    """Ellipse lying on the horizontal plane y: a circle of model radius r."""
    ex, ey = P(cx, y, cz)
    rx, ry = S * r, S * r * SP
    d.shape("ellipse", label, x=round(ex - rx, 1), y=round(ey - ry, 1),
            width=round(rx * 2, 1), height=round(ry * 2, 1), **kw)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1A130C"), (1, "#0A0603")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#C09458", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5C4526"), (0.55, "#3A2A14"), (1, "#1A1107")),
        stroke="#120C05", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0C08A", strokeWidth=3, opacity=24)

# window shaft from the upper left + warm glow — kept inside the disc
d.path("M280,120 L460,120 L640,660 L330,660 Z", "Window shaft",
       fill=lin((340, 120), (520, 660), (0, "#FFCF8E", 0.13), (0.6, "#E8A860", 0.05),
                (1, "#E8A860", 0)), stroke=NONE)
d.shape("ellipse", "Window glow", x=200, y=100, width=360, height=360,
        fill=rad((0, "#FFC27A", 0.20), (0.6, "#C8853E", 0.06), (1, "#C8853E", 0)),
        stroke=NONE)

# --- floor chord: computed so every foot lands inside the band ------------------------
feet_screen = [P(37, 0, -9.5), P(-37, 0, -9.5), P(37, 0, 9.5), P(-37, 0, 9.5)]
FYB = min(p[1] for p in feet_screen) - 8
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX - hw:.1f},{FYB:.1f} L{PCX + hw:.1f},{FYB:.1f} A420,420 0 0 0 {PCX - hw:.1f},{FYB:.1f} Z",
       "Floor", fill=lin((0, FYB), (0, 880), (0, "#4A3820", 0.45), (0.5, "#2A1C0C", 0.7),
                         (1, "#100A04", 0.9)), stroke=NONE)
for i, yb in enumerate([FYB + 44, FYB + 92, FYB + 148]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb:.1f} L{PCX + h:.1f},{yb:.1f}", f"Board seam {i+1}",
           fill=NONE, stroke="#6A4E28", strokeWidth=2, opacity=26)

# --- grounding shadow under the bench ---------------------------------------------------
sh_a, sh_b = P(-39, 0, -10.5), P(39, 0, 10.5)
sx0, sx1 = min(sh_a[0], sh_b[0]) - 30, max(sh_a[0], sh_b[0]) + 30
sy0, sy1 = min(sh_a[1], sh_b[1]) - 14, max(sh_a[1], sh_b[1]) + 20
d.shape("ellipse", "Bench shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#050302", 0.7), (0.6, "#050302", 0.3), (1, "#050302", 0)),
        stroke=NONE)

# --- bench geometry (inches) ---------------------------------------------------------------
MAPLE = ("#5A3A18", "#C89A5C")
MAPLE_HI = ("#6E4A22", "#DDB472")
BEECH = ("#6A4A24", "#D8AE72")
IRON = ("#1A1A1E", "#4A4A52")

# understructure first so legs overpaint the joint ends: end stretchers
# along z joining each leg pair, then plank shelf along x
for sx, tag in ((-1, "L"), (1, "R")):
    lx = sx * 37
    prism(f"End stretcher {tag}", box(lx - 2.6, 4.5, -10.5, lx + 2.6, 10.5, 10.5),
          ramp=MAPLE, lo=0.03, hi=0.8)
for i in range(4):
    z0 = -8.0 + i * 4.1
    prism(f"Shelf plank {i+1}", box(-33.2, 9.6, z0, 33.2, 10.9, z0 + 3.7),
          ramp=("#3A2410", "#8A6234"), lo=0.02, hi=0.7)

# legs: chunky squares joined to the slab, far pair first
for sx, sz, tag in ((-1, 1, "far L"), (1, 1, "far R"), (-1, -1, "near L"), (1, -1, "near R")):
    lx, lz = sx * 37, sz * 9.5
    prism(f"Leg {tag}", box(lx - 3.3, 0, lz - 3.3, lx + 3.3, 32, lz + 3.3),
          ramp=MAPLE, lo=0.04, hi=0.85)

# the standing board held in the face vise, drawn before the jaw and top
# (a wide pale maple plank rising from between the vise jaw and the bench front)
prism("Clamped board", box(-41, 26, -16.4, -28.5, 57, -15.4),
      ramp=("#8A6A38", "#E8C88E"), lo=0.2, hi=1.0)
# board edges: a pale top end-grain line and a soft shadow cast onto the top
ba, bb = P(-41, 57.2, -16.4), P(-28.5, 57.2, -16.4)
d.path(f"M{ba[0]:.1f},{ba[1]:.1f} L{bb[0]:.1f},{bb[1]:.1f}", "Board top edge",
       fill=NONE, stroke="#F4DCA8", strokeWidth=2.0, opacity=60)

# top slab: 4in thick, blunt prism ends
prism("Top", box(-44, 32, -15, 44, 36, 15), ramp=MAPLE_HI, lo=0.1, hi=1.0)
# long grain lines along the top
for g in range(3):
    ga, gb = P(-40, 36.1, -8 + g * 7), P(40, 36.1, -8 + g * 7)
    d.path(f"M{ga[0]:.1f},{ga[1]:.1f} L{gb[0]:.1f},{gb[1]:.1f}", f"Top grain {g+1}",
           fill=NONE, stroke="#8A5E2E", strokeWidth=1.4, opacity=30)
# front edge wear: vise-zone scuffs and saw marks on the near face
wa, wb = P(-40, 33.2, -15.1), P(-24, 33.2, -15.1)
d.path(f"M{wa[0]:.1f},{wa[1]:.1f} L{wb[0]:.1f},{wb[1]:.1f}", "Vise wear",
       fill=NONE, stroke="#3A2410", strokeWidth=3.4, opacity=35)

# tail vise wagon: a slightly different-toned block at the right end of the top
prism("Tail wagon", box(37.5, 35.2, -8, 42.5, 36.4, 8), ramp=BEECH, lo=0.08, hi=0.95)
ta, tb = P(37.5, 36.45, -8), P(37.5, 36.45, 8)
d.path(f"M{ta[0]:.1f},{ta[1]:.1f} L{tb[0]:.1f},{tb[1]:.1f}", "Wagon seam",
       fill=NONE, stroke="#3A2410", strokeWidth=2.0, opacity=50)

# dog holes along the front edge of the top, plus one popped bench dog
for i in range(9):
    hx = -28 + i * 8
    flat_ellipse(hx, 36.15, -11.5, 0.6, f"Dog hole {i+1}", fill="#1A0E04", stroke=NONE)
prism("Bench dog", box(-8.6, 36, -12.1, -7.4, 38.6, -10.9), ramp=BEECH, lo=0.1, hi=1.0, sw=1.2)

# --- face vise on the near-left corner ----------------------------------------------------
# parallel guide rails sunk into the bench front
for gy in (28.4, 31.2):
    ga, gb = P(-37.5, gy, -15.05), P(-28.5, gy, -15.05)
    d.path(f"M{ga[0]:.1f},{ga[1]:.1f} L{gb[0]:.1f},{gb[1]:.1f}", f"Vise rail {gy}",
           fill=NONE, stroke="#0E0803", strokeWidth=2.6, opacity=60)
# the jaw: a beech board on the bench face
prism("Vise jaw", box(-40.5, 25.5, -17.6, -27, 34, -15.6), ramp=BEECH, lo=0.08, hi=1.0)
# screw barrel through the jaw, axis along z
sa, sb = P(-33.7, 29.8, -15.2), P(-33.7, 29.8, -19.6)
d.path(f"M{sa[0]:.1f},{sa[1]:.1f} L{sb[0]:.1f},{sb[1]:.1f}", "Vise screw",
       fill=NONE, stroke=shade(IRON[0], IRON[1], 0.55), strokeWidth=6.5, cap="round")
d.path(f"M{sa[0]:.1f},{sa[1] - 2.2:.1f} L{sb[0]:.1f},{sb[1] - 2.2:.1f}", "Screw light",
       fill=NONE, stroke="#8A8A92", strokeWidth=1.8, opacity=45, cap="round")
# tommy bar through the screw end, along x, with knob ends
tba, tbb = P(-37.5, 31.6, -19.6), P(-29.9, 28.0, -19.6)
d.path(f"M{tba[0]:.1f},{tba[1]:.1f} L{tbb[0]:.1f},{tbb[1]:.1f}", "Tommy bar",
       fill=NONE, stroke="#4A2E14", strokeWidth=3.4, cap="round")
for tp, tl in ((tba, "L"), (tbb, "R")):
    d.shape("ellipse", f"Tommy knob {tl}", x=round(tp[0] - 3.4), y=round(tp[1] - 3.4),
            width=6.8, height=6.8, fill=rad((0, "#C89A5C", None), (1, "#5A3A18", None)),
            stroke=INK, strokeWidth=1.0)

# --- props on the top ----------------------------------------------------------------------
# hand plane resting mid-top: body, front knob, rear tote, blade iron
prism("Plane body", box(10, 36, 2, 21, 38, 5), ramp=("#1E1208", "#4A3018"), lo=0.05, hi=0.85)
d.shape("ellipse", "Plane knob", x=round(P(12.2, 39.3, 3.4)[0] - 4.6),
        y=round(P(12.2, 39.3, 3.4)[1] - 4.6), width=9.2, height=9.2,
        fill=rad((0, "#7A4E26", None), (1, "#2A1810", None)), stroke=INK, strokeWidth=1.2)
tote = [P(17.5, 38, 2.6), P(20, 38, 2.9), P(19.4, 40.8, 3.6), P(18.2, 40.4, 4.2)]
d.path(poly(tote), "Plane tote", fill=shade(MAPLE[0], MAPLE[1], 0.45),
       stroke=INK, strokeWidth=1.4, join="round")
blade = [P(14.2, 38, 3.0), P(16.2, 38, 3.0), P(15.8, 40.4, 3.6), P(14.6, 40.4, 3.6)]
d.path(poly(blade), "Plane iron", fill=lin(P(14.2, 38, 3.0), P(15.8, 40.4, 3.6),
       (0, "#3A3A42", None), (1, "#8A8A96", None)), stroke=INK, strokeWidth=1.0)
# a thin shaving curl still riding the plane mouth
curl = smooth([P(15.2, 38.4, 2.2), P(15.8, 39.6, 1.6), P(15.0, 40.4, 1.4), P(14.6, 39.8, 1.8)])
d.path(curl, "Plane shaving", fill=NONE, stroke="#E8C88E", strokeWidth=1.6, opacity=75)

# wood shavings on the top near the vise and on the floor below it
for i, (cx_, cy_, cz_, k) in enumerate([(-24, 36.3, -9, 1), (-20, 36.3, -12, -1),
                                      (-33, 0.4, -13, 1), (-28, 0.4, -16, -1)]):
    pts = []
    for j in range(7):
        a = j * 0.9 * k
        pts.append(P(cx_ + 2.2 * math.sin(a), cy_ + 0.5 * j / 6, cz_ + 1.1 * math.cos(a)))
    d.path(smooth(pts), f"Shaving {i+1}", fill=NONE, stroke="#D8AE72",
           strokeWidth=1.6, opacity=70)

# sawdust specks around the vise on the floor and top
for i, (mx_, my_, mz_, mo_) in enumerate([
        (-30, 0.3, -12, 35), (-34, 0.3, -15, 30), (-27, 0.3, -17, 28), (-31, 0.3, -19, 25),
        (-36, 36.2, -12, 30), (-33, 36.2, -9, 26), (-29, 36.2, -13, 30),
        (-25, 36.2, -10, 24), (-38, 36.2, -11, 22)]):
    e = P(mx_, my_, mz_)
    d.shape("ellipse", f"Dust {i+1}", x=round(e[0] - 1.4, 1), y=round(e[1] - 1.4, 1),
            width=2.8, height=2.8, fill="#E8C88E", opacity=mo_, stroke=NONE)

# dust motes in the window shaft (screen space)
for i, (mx_, my_, mr_, mo_) in enumerate([
        (300, 240, 2.0, 28), (360, 300, 1.6, 22), (430, 280, 2.2, 26), (390, 370, 1.7, 20),
        (320, 420, 1.9, 22), (470, 400, 1.5, 18), (520, 470, 2.0, 20), (440, 500, 1.6, 16)]):
    EXTENT.append((mx_, my_))
    d.shape("ellipse", f"Mote {i+1}", x=mx_, y=my_, width=mr_ * 2, height=mr_ * 2,
            fill="#FFE0B0", opacity=mo_, stroke=NONE)

# window rim light on the top's near-left edge
ra, rb = P(-44, 36.2, -14), P(-14, 36.2, -14.6)
d.path(f"M{ra[0]:.1f},{ra[1]:.1f} L{rb[0]:.1f},{rb[1]:.1f}", "Top rim light",
       fill=NONE, stroke="#FFDCA8", strokeWidth=2.6, opacity=40, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("bench extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F0E2C4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C8AC84", justify="center")
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


caption("WORKBENCH", "MAPLE · BEECH · IRON")
d.finish("workbench-V1R00")
