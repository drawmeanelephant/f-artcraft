#!/usr/bin/env python3
"""Murphy bed — field plate V1R00. Three-quarter from the front right:
a tall oak wall cabinet with its bay open, the bed folded down out of it
toward the viewer — mattress, pillow, quilt folded across the foot, a pair
of swing-down legs, pull handles on the foot face. The lift spring and
pivot arm show inside the bay's left wall. Cabinet plate, studio-flat
mood. 1000x1000. Modelled in inches (x right, y up, +z back), projected
with a fixed yaw + pitch; carcass parts are 8-corner prisms culled by
view normal and shaded by lamplight.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Murphy Bed — Field Plate", 1000, 1000)

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
YAW, PITCH = math.radians(26), math.radians(20)
S, OX, OY = 5.0, 502.0, 656.0
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
LIGHT = (-0.38, 0.84, -0.34)                  # lamp overhead, slightly left/front
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


def prism(name, corners, dark="#241408", light="#7A4E26", lo=0.06, hi=0.94, ink=1.8):
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


def face_quad(name, pts3, fill, **kw):
    """A flat 4-corner plate on a model plane."""
    d.path(poly([P(*p) for p in pts3]), name, fill=fill, **kw)


OAK_D, OAK_L = "#241208", "#7E5028"        # cabinet oak
OAK2_D, OAK2_L = "#3A2410", "#B5824A"      # bed-frame oak, a step lighter
CREAM_D, CREAM_L = "#8A8090", "#F0EADD"


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#181009"), (1, "#070402")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#C89A58", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#54402A"), (0.55, "#3A2A18"), (1, "#1C1208")),
        stroke="#120A05", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D0A0", strokeWidth=3, opacity=24)
# room warmth pooling over the cabinet top
d.shape("ellipse", "Wall glow", x=330, y=88, width=420, height=220,
        fill=rad((0, "#D89A50", 0.12), (0.6, "#B07838", 0.05), (1, "#B07838", 0)),
        stroke=NONE)

# --- floor boards closing on the disc arc --------------------------------------------
FYB = 706
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX - hw:.1f},{FYB} L{PCX + hw:.1f},{FYB} A420,420 0 0 1 {PCX - hw:.1f},{FYB} Z",
       "Floor", fill=lin((0, FYB), (0, 880), (0, "#4A3A24", 0.5),
                         (0.5, "#241A0E", 0.75), (1, "#0E0804", 0.92)), stroke=NONE)
d.path(f"M{PCX - hw + 6:.1f},{FYB} L{PCX + hw - 6:.1f},{FYB}", "Floor edge light",
       fill=NONE, stroke="#E0C890", strokeWidth=2, opacity=16)
for i, yb in enumerate([758, 796, 834]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Board seam {i+1}",
           fill=NONE, stroke="#5A4526", strokeWidth=2, opacity=24)

# rug ears peeking out from under the bed, studio-flat colour
rug = [P(-34, 0.15, -56), P(34, 0.15, -56), P(34, 0.15, -16), P(-34, 0.15, -16)]
d.path(poly(rug), "Rug", fill=lin((0, 620), (0, 780),
       (0, "#7E4434", None), (1, "#46221A", None)), stroke=NONE)
rug_i = [P(-31, 0.15, -52), P(31, 0.15, -52), P(31, 0.15, -20), P(-31, 0.15, -20)]
d.path(poly(rug_i), "Rug border", fill=NONE, stroke="#D89A60",
       strokeWidth=2.4, opacity=50)

# grounding shadow under bed + cabinet
bxs = [Pq(x, 0, z) for x, z in ((-34, -66), (34, -66), (34, 26), (-34, 26))]
sx0, sx1 = min(p[0] for p in bxs) - 18, max(p[0] for p in bxs) + 18
sy0, sy1 = min(p[1] for p in bxs) - 10, max(p[1] for p in bxs) + 26
d.shape("ellipse", "Bed shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#040201", 0.72), (0.6, "#040201", 0.32), (1, "#040201", 0)),
        stroke=NONE)

# --- the cabinet ---------------------------------------------------------------------
# interior back panel first (deepest face), then the carcass prisms over its edges
face_quad("Bay back panel",
          [(-27, 14, 27.2), (27, 14, 27.2), (27, 78, 27.2), (-27, 78, 27.2)],
          fill=lin((0, 300), (0, 620), (0, "#2E1C0E", None), (1, "#160C05", None)),
          stroke=NONE)
# soft shadow washing the top and right of the cavity
face_quad("Bay top shadow",
          [(-27, 66, 27.0), (27, 66, 27.0), (27, 78, 27.0), (-27, 78, 27.0)],
          fill=lin((0, 300), (0, 380), (0, "#0A0503", 0), (1, "#0A0503", 0.55)),
          stroke=NONE)
# faint vertical seams on the bay back: the bed's underside panels live here when up
for sx in (-9, 9):
    a, b = P(sx, 18, 27.1), P(sx, 76, 27.1)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Bay seam {sx:+g}",
           fill=NONE, stroke="#0E0703", strokeWidth=2.0, opacity=55)

# side stiles, header, toe plinth, crown
prism("Stile L", box(-31, 0, 12, -27, 78, 28), dark=OAK_D, light=OAK_L, lo=0.04, hi=0.85)
prism("Stile R", box(27, 0, 12, 31, 78, 28), dark=OAK_D, light=OAK_L, lo=0.04, hi=0.85)
prism("Header", box(-31, 78, 12, 31, 84, 28), dark=OAK_D, light=OAK_L, lo=0.05, hi=0.9)
prism("Plinth", box(-31.5, 0, 11.5, 31.5, 4.5, 28), dark=OAK_D, light=OAK_L, lo=0.03, hi=0.7)
prism("Crown", box(-33, 84, 11, 33, 87.5, 28.5), dark=OAK_D, light=OAK_L, lo=0.08, hi=0.95)
# crown lip
prism("Crown lip", box(-33.5, 83.2, 10.5, 33.5, 84.6, 28.8),
      dark=OAK_D, light=OAK_L, lo=0.06, hi=0.8, ink=1.5)

# cabinet face-frame beads along the stile fronts
for sx in (-31, 31):
    a, b = P(sx, 5, 12), P(sx, 77, 12)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Stile bead {sx:+g}",
           fill=NONE, stroke="#E8C890", strokeWidth=1.8, opacity=30, cap="round")

# lift hardware on the bay's left wall: coil spring above a pivot strut
sp0, sp1 = P(-26.8, 74, 21), P(-26.8, 34, 21)
zig = []
n_coil = 9
for i in range(n_coil * 2 + 1):
    t = i / (n_coil * 2)
    zz = 21 + (1.6 if i % 2 else -1.6) * (1 if 0 < i < n_coil * 2 else 0)
    zig.append(P(-26.8, 74 + (34 - 74) * t, zz))
d.path("M%.1f,%.1f " % zig[0] + " ".join("L%.1f,%.1f" % p for p in zig[1:]),
       "Lift spring", fill=NONE, stroke="#8A8A92", strokeWidth=2.4,
       opacity=80, cap="round", join="round")
# spring anchors
for i, p in enumerate((sp0, sp1)):
    d.shape("ellipse", f"Spring anchor {i+1}", x=p[0] - 4, y=p[1] - 4,
            width=8, height=8, fill="#B8B4AC", stroke=INK, strokeWidth=1.2)
# pivot strut from the wall down to the rail head
sa_, sb_ = P(-26.8, 46, 19), P(-26.8, 12, 7)
sdx, sdy = sb_[0] - sa_[0], sb_[1] - sa_[1]
sl = math.hypot(sdx, sdy)
snx, sny = -sdy / sl * 3.4, sdx / sl * 3.4
d.path(poly([(sa_[0] + snx, sa_[1] + sny), (sa_[0] - snx, sa_[1] - sny),
             (sb_[0] - snx * 0.7, sb_[1] - sny * 0.7), (sb_[0] + snx * 0.7, sb_[1] + sny * 0.7)]),
       "Pivot strut", fill=lin(sa_, sb_, (0, "#9A9690", None), (1, "#4E4A44", None)),
       stroke=INK, strokeWidth=1.4, join="round")
d.shape("ellipse", "Strut pivot", x=sb_[0] - 4.6, y=sb_[1] - 4.6, width=9.2, height=9.2,
        fill="#C8C4BC", stroke=INK, strokeWidth=1.3)

# --- the bed, folded down ------------------------------------------------------------
# far side rail (left) first; the head rail ties the pivot end
prism("Rail far", box(-28, 8, 12, -25, 15, -62), dark=OAK2_D, light=OAK2_L, lo=0.05, hi=0.85)
prism("Head rail", box(-28, 8, 10, 28, 15, 13.5), dark=OAK2_D, light=OAK2_L, lo=0.04, hi=0.8)

# mattress on the frame
prism("Mattress", box(-25.5, 15, -59, 25.5, 21.5, 9.5),
      dark=CREAM_D, light=CREAM_L, lo=0.30, hi=1.02, ink=1.7)
pa, pb = P(-25.2, 21.6, -58.7), P(25.2, 21.6, -58.7)
d.path(f"M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}",
       "Mattress piping", fill=NONE, stroke="#A89CA8", strokeWidth=1.7,
       opacity=50, cap="round")
pe = P(-25.2, 21.6, 9.2)
d.path(f"M{pa[0]:.1f},{pa[1]:.1f} L{pe[0]:.1f},{pe[1]:.1f}", "Mattress piping L",
       fill=NONE, stroke="#A89CA8", strokeWidth=1.7, opacity=40, cap="round")

# quilt folded across the foot half
prism("Quilt", box(-25.7, 21.5, -48, 25.7, 23.4, -26),
      dark="#26313E", light="#6E8AA0", lo=0.12, hi=0.95, ink=1.7)
qa, qb = P(-25.5, 22.5, -47.8), P(25.5, 22.5, -47.8)
d.path(f"M{qa[0]:.1f},{qa[1]:.1f} L{qb[0]:.1f},{qb[1]:.1f}", "Quilt fold",
       fill=NONE, stroke="#141C24", strokeWidth=2.2, opacity=50, cap="round")
qc, qd = P(-25.5, 22.5, -33), P(25.5, 22.5, -33)
d.path(f"M{qc[0]:.1f},{qc[1]:.1f} L{qd[0]:.1f},{qd[1]:.1f}", "Quilt seam",
       fill=NONE, stroke="#141C24", strokeWidth=1.6, opacity=35, cap="round")

# pillow at the head, screen-space blob over the mattress
cx_, cy_ = P(-7, 23.8, 3)
pts = [(cx_ - 44, cy_ + 22), (cx_ - 52, cy_ + 4), (cx_ - 20, cy_ - 18),
       (cx_ + 30, cy_ - 30), (cx_ + 54, cy_ - 16), (cx_ + 26, cy_ + 12),
       (cx_ - 12, cy_ + 26)]
d.path(smooth(pts), "Pillow", stroke="#5E5470", strokeWidth=2.2,
       fill=rad((0, "#F6F0E4"), (0.7, "#E0DCE8"), (1, "#B4AEC2")))
d.path(smooth([(cx_ - 30, cy_ + 8), (cx_ - 4, cy_ - 10), (cx_ + 30, cy_ - 20)],
              closed=False), "Pillow crease",
       fill=NONE, stroke="#8C84A4", strokeWidth=2.0, opacity=40, cap="round")

# webbing straps holding the mattress for the fold
for i, sz in enumerate((-14, -52)):
    prism(f"Mattress strap {i+1}", box(-25.6, 21.4, sz - 1.1, 25.6, 22.2, sz + 1.1),
          dark="#4A3420", light="#9A7648", lo=0.15, hi=0.9, ink=1.4)
    buck = P(0, 22.3, sz)
    d.shape("ellipse", f"Strap buckle {i+1}", x=buck[0] - 5, y=buck[1] - 4,
            width=10, height=8, fill=NONE, stroke="#C8C4BC", strokeWidth=2.0)

# near side rail over the mattress edge
prism("Rail near", box(25, 8, 12, 28, 15, -62), dark=OAK2_D, light=OAK2_L, lo=0.06, hi=0.95, ink=1.9)
ra, rb = P(28.1, 14.4, 10), P(28.1, 14.4, -60)
d.path(f"M{ra[0]:.1f},{ra[1]:.1f} L{rb[0]:.1f},{rb[1]:.1f}", "Rail bead light",
       fill=NONE, stroke="#F0C888", strokeWidth=2.0, opacity=38, cap="round")
# pivot plate where the near rail enters the cabinet
pvx, pvy = P(28.15, 11.5, 9)
d.shape("ellipse", "Pivot plate", x=pvx - 7, y=pvy - 7, width=14, height=14,
        fill=rad((0, "#C8C4BC"), (0.7, "#8A867E"), (1, "#4E4A44")),
        stroke=INK, strokeWidth=1.4)
d.shape("ellipse", "Pivot bolt", x=pvx - 2.4, y=pvy - 2.4, width=4.8, height=4.8,
        fill="#3A3630", stroke=NONE)

# swing-down legs at the foot, then the foot rail with its pull handles
for lx, tag in ((-22.5, "L"), (22.5, "R")):
    prism(f"Leg {tag}", box(lx - 2.6, 0, -61, lx + 2.6, 8.6, -56.5),
          dark=OAK2_D, light=OAK2_L, lo=0.04, hi=0.8)
prism("Leg stretcher", box(-22.5, 2.2, -59.8, 22.5, 4.6, -56.9),
      dark=OAK2_D, light=OAK2_L, lo=0.03, hi=0.7, ink=1.5)
prism("Foot rail", box(-28, 6, -65.5, 28, 17, -62),
      dark=OAK2_D, light=OAK2_L, lo=0.06, hi=0.95, ink=2.0)

# the foot face is the false cabinet front when the bed is up: two inset panels + handles
for hx, tag in ((-15.5, "L"), (15.5, "R")):
    panel = [P(hx - 10.5, 8, -65.55), P(hx + 10.5, 8, -65.55),
             P(hx + 10.5, 15.6, -65.55), P(hx - 10.5, 15.6, -65.55)]
    d.path(poly(panel), f"Foot panel {tag}",
           fill=lin((0, min(p[1] for p in panel)), (0, max(p[1] for p in panel)),
                    (0, "#54371C", None), (1, "#2A180A", None)),
           stroke="#160C04", strokeWidth=1.7, join="round")
# handles on the foot face
for hx, tag in ((-4.5, "L"), (4.5, "R")):
    prism(f"Handle {tag}", box(hx - 1.6, 9.5, -67.6, hx + 1.6, 14.5, -65.5),
          dark="#4A3418", light="#C8A050", lo=0.1, hi=1.0, ink=1.3)

# rim light along the crown and the foot rail's top edge
ca_, cb_ = P(-32, 87.6, 27.5), P(32, 87.6, 27.5)
d.path(f"M{ca_[0]:.1f},{ca_[1]:.1f} L{cb_[0]:.1f},{cb_[1]:.1f}", "Crown rim light",
       fill=NONE, stroke="#FFCE8A", strokeWidth=2.2, opacity=30, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("murphy extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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


caption("MURPHY BED", "OAK · STEEL · LINEN")
d.finish("murphy-bed-V1R00")
