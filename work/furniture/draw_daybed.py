#!/usr/bin/env python3
"""Daybed — field plate V1R00. Three-quarter view from the front right:
an iron daybed with matching end frames — posts with brass ball finials,
top rail and slim spindles — long side rails, a striped ticking mattress,
one pillow against the far end and a throw slumped over the front edge.
Iron-frame plate, nap mood. 1000x1000.
Modelled in inches (x right, y up, +z back) and projected with a fixed
yaw + pitch; every board is an 8-corner prism drawn far-to-near with
per-face gradients.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Daybed — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241A14"   # warm dark, not black
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
YAW, PITCH = math.radians(30), math.radians(22)
S, OX, OY = 8.0, 500.0, 610.0
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
LIGHT = (-0.50, 0.74, -0.45)
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


IR_D, IR_L = "#1E1B1C", "#6E645C"       # wrought iron ramp
TIK_D, TIK_L = "#8E8468", "#EFE7D2"     # cotton ticking ramp
THR_D, THR_L = "#4E5A42", "#96A47E"     # sage wool throw ramp
PIL_D, PIL_L = "#9E8F74", "#E8DCC2"     # pillow linen ramp


def prism(name, corners, lo=0.06, hi=0.94, ramp=(IR_D, IR_L), ink=1.8):
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
        d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")


def lean_box(x0, x1, yb, zb, yt, zt, t):
    """Slab leaning in the (y,z) plane: front quad at (yb,zb)-(yt,zt),
    extruded t in +z. Backrests and reclined cushions."""
    return [(x0, yb, zb), (x1, yb, zb), (x1, yt, zt), (x0, yt, zt),
            (x0, yb, zb + t), (x1, yb, zb + t), (x1, yt, zt + t), (x0, yt, zt + t)]


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#181420"), (1, "#0A080E")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7A6E80", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5C5462"), (0.6, "#3E3746"), (1, "#211D28")),
        stroke="#120E18", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8CCDE", strokeWidth=3, opacity=24)
d.shape("ellipse", "Lamp glow", x=230, y=140, width=520, height=520,
        fill=rad((0, "#EFC98E", 16), (0.6, "#A8886A", 6), (1, "#6A5442", 0)),
        stroke=NONE)

FY = 503
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#564E5C", 36), (1, "#141018", 72)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#D6CADA", strokeWidth=2, opacity=18)

# --- daybed geometry (inches; x right, y up, +z back) ----------------------------------
# footprint: 78 long (x +/-39), 36 deep (z +/-18), ends 40 tall, mattress top ~17.5
POST = (36.8, 39.0)                  # end-post x span
FZ, BZ = (-18.0, -15.8), (15.8, 18.0)  # front/back post z spans
TOP_Y0, TOP_Y1 = 38.0, 40.0          # end-frame top rail
MID_Y0, MID_Y1 = 21.0, 23.0          # end-frame mid rail
RAIL_Y0, RAIL_Y1 = 8.0, 10.2         # long side rails
MAT_Y0, MAT_Y1 = 10.4, 17.5          # mattress
SPIN = (-12.0, -6.0, 0.0, 6.0, 12.0) # spindle z positions in each end frame

# grounding shadow under all feet
feet = [P(sx * 37.9, 0, z) for sx in (-1, 1) for z in (FZ[0], BZ[1])]
fx0 = min(p[0] for p in feet) - 60
fx1 = max(p[0] for p in feet) + 60
fy0 = min(p[1] for p in feet) - 8
fy1 = max(p[1] for p in feet) + 34
d.shape("ellipse", "Bed shadow", x=round(fx0), y=round(fy0),
        width=round(fx1 - fx0), height=round(fy1 - fy0),
        fill=rad((0, "#060408", 64), (0.6, "#060408", 26), (1, "#060408", 0)),
        stroke=NONE)


def end_frame(sx):
    """One iron end frame: two posts, top + mid rails, spindles, finials."""
    x0, x1 = (POST[0], POST[1]) if sx > 0 else (-POST[1], -POST[0])
    tag = "R" if sx > 0 else "L"
    # back post drawn before spindles (farther), front post after
    prism(f"Back post {tag}", box(x0, 0, BZ[0], x1, TOP_Y1, BZ[1]), lo=0.02, hi=0.75)
    prism(f"Mid rail {tag}", box(x0, MID_Y0, FZ[1], x1, MID_Y1, BZ[0]), lo=0.02, hi=0.7)
    for i, zc in enumerate(SPIN):
        prism(f"Spindle {tag} {i+1}", box(x0 + 0.75, MID_Y1, zc - 0.35,
                                        x1 - 0.75, TOP_Y0, zc + 0.35), lo=0.02, hi=0.7)
    prism(f"Front post {tag}", box(x0, 0, FZ[0], x1, TOP_Y1, FZ[1]), lo=0.02, hi=0.8)
    prism(f"Top rail {tag}", box(x0, TOP_Y0, FZ[0], x1, TOP_Y1, BZ[1]), lo=0.05, hi=0.95)


# far end (left) first
end_frame(-1)

# long side rails connecting the ends — back rail behind the mattress
prism("Back side rail", box(-POST[0], RAIL_Y0, BZ[0] - 0.4,
                            POST[0], RAIL_Y1, BZ[1] + 0.4), lo=0.02, hi=0.7)

# --- mattress ----------------------------------------------------------------------
prism("Mattress", box(-37.4, MAT_Y0, -17.4, 37.4, MAT_Y1, 17.4),
      lo=0.10, hi=1.0, ramp=(TIK_D, TIK_L), ink=2.2)
# ticking stripes down the front face (z = -17.45), spaced in x
for i in range(17):
    sx = -36.0 + i * 4.5
    a, b = P(sx, MAT_Y0 + 0.3, -17.46), P(sx, MAT_Y1 - 0.2, -17.46)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}",
           f"Ticking stripe {i+1}", fill=NONE, stroke="#6A7A88",
           strokeWidth=2.6, opacity=55)
# piping along the front top edge of the mattress
pa, pb = P(-37.2, MAT_Y1, -17.4), P(37.2, MAT_Y1, -17.4)
d.path(f"M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}", "Mattress piping",
       fill=NONE, stroke="#7A705A", strokeWidth=2.4, opacity=75)

# --- pillow slumped against the far (left) end frame ----------------------------------
# drawn after the far frame so its left edge laps the post and reads propped
prism("Pillow", lean_box(-37.2, -13.0, MAT_Y1 + 0.2, -6.0, 27.5, 3.5, 7.0),
      lo=0.08, hi=0.92, ramp=(PIL_D, PIL_L), ink=2.0)
# pillow crease
pa, pb = P(-35.5, 25.6, -4.4), P(-15.0, 26.2, -2.4)
d.path(f"M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}", "Pillow crease",
       fill=NONE, stroke=PIL_D, strokeWidth=2.0, opacity=55)
# seam inset on the pillow's front face keeps it reading soft, not slab
_pc = (-25.1, 22.6, -1.25)
_seam = []
for cx, cy, cz in [(-37.2, MAT_Y1 + 0.2, -6.0), (-13.0, MAT_Y1 + 0.2, -6.0),
                   (-13.0, 27.5, 3.5), (-37.2, 27.5, 3.5)]:
    _seam.append(P(cx + (_pc[0] - cx) * 0.09, cy + (_pc[1] - cy) * 0.09,
                   cz + (_pc[2] - cz) * 0.09))
d.path(poly(_seam), "Pillow seam", fill=NONE, stroke=PIL_D,
       strokeWidth=2.0, opacity=50, join="round")

# --- throw over the near (front) edge, right of centre ---------------------------------
prism("Throw top", box(4.0, MAT_Y1 - 0.3, -18.2, 31.0, MAT_Y1 + 1.9, 3.0),
      lo=0.08, hi=1.0, ramp=(THR_D, THR_L), ink=2.0)
prism("Throw skirt", box(4.0, 6.2, -19.6, 31.0, MAT_Y1 - 0.1, -17.0),
      lo=0.04, hi=0.9, ramp=(THR_D, THR_L), ink=2.0)
# fold lines down the skirt
for i, fx in enumerate((9.5, 16.5, 24.0)):
    a, b = P(fx, 6.8, -19.7), P(fx + 1.2, MAT_Y1 - 0.6, -18.0)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}",
           f"Throw fold {i+1}", fill=NONE, stroke=THR_D, strokeWidth=2.2, opacity=60)

# --- front side rail + near end (right) ------------------------------------------------
prism("Front side rail", box(-POST[0], RAIL_Y0, FZ[0] - 0.4,
                             POST[0], RAIL_Y1, FZ[1] + 0.4), lo=0.02, hi=0.8)
# the skirt's front fold lines sit over the rail — redrawn after it
for i, fx in enumerate((9.5, 16.5, 24.0)):
    a, b = P(fx, 6.8, -19.7), P(fx + 1.2, MAT_Y1 - 0.6, -18.0)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}",
           f"Throw fold front {i+1}", fill=NONE, stroke="#3A4630",
           strokeWidth=2.4, opacity=70)
end_frame(1)

# brass ball finials on all four post tops
for sx in (-1, 1):
    for z in (FZ[0] + 1.1, BZ[1] - 1.1):
        px, py = P(sx * 37.9, TOP_Y1 + 1.0, z)
        d.shape("ellipse", f"Finial {sx:+d} {int(z)}", x=round(px - 7), y=round(py - 7),
                width=14, height=14, fill=rad((0, "#E8C87E"), (1, "#7A5622")),
                stroke=INK, strokeWidth=1.4)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("daybed extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#EFE6DC", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#B2A8BC", justify="center")
    d.cmd("text.setStyle", "Name tracking", id=n["id"], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", id=m["id"], tracking=260)
    doc = d.m.call("inspect_document", {})
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


caption("DAYBED", "IRON · COTTON · BRASS")
d.finish("daybed-V1R00")
