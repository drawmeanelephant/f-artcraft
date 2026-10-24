#!/usr/bin/env python3
"""Morris chair — field plate V1R00. Three-quarter view from the front
right: square oak posts, broad flat arms over side spindles, a reclined
backrest on the pegged adjustment bar sticking out behind, loose leather
cushions on seat and back. Oak plate, arts-and-crafts mood. 1000x1000.
Modelled in inches (x right, y up, +z back) and projected with a fixed
yaw + pitch; every board is an 8-corner prism drawn far-to-near with
per-face gradients.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Morris Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A1C12"   # warm dark, not black
EXTENT = []


def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


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
S, OX, OY = 14.4, 462.0, 738.0
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


OAK_D, OAK_L = "#3A2612", "#B08A52"      # quartersawn oak ramp
LTH_D, LTH_L = "#4A1E14", "#A4563A"      # aged russet leather ramp


def prism(name, corners, lo=0.06, hi=0.94, ramp=(OAK_D, OAK_L), ink=1.8):
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
        fill=lin((0, 0), (0, 1000), (0, "#141C14"), (1, "#070B07")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8A744E", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#7A6248"), (0.6, "#4E3E2C"), (1, "#262015")),
        stroke="#161009", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E2D2B4", strokeWidth=3, opacity=26)
d.shape("ellipse", "Hearth glow", x=250, y=160, width=520, height=520,
        fill=rad((0, "#F0B46E", 15), (0.6, "#A87A48", 6), (1, "#7A5834", 0)),
        stroke=NONE)

FY = 672
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#5E503C", 38), (1, "#181208", 74)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E0D0B0", strokeWidth=2, opacity=20)

# --- chair geometry (inches; x right, y up, +z back) ----------------------------------
POST_X = (9.4, 11.6)               # leg/post span across x
FRONT_Z = (-3.4, -1.2)             # front post depth span
BACK_Z = (6.4, 8.6)                # back post depth span
ARM_Y0, ARM_Y1 = 21.6, 23.4
SEAT_Y0, SEAT_Y1 = 12.6, 15.4      # seat rail
HINGE_Y, HINGE_Z = 16.2, 7.9       # backrest pivot
BK_YB, BK_ZB = 16.0, 8.4           # backrest base
BK_YT, BK_ZT = 38.0, 15.2          # backrest top (reclined ~20 deg)

# grounding shadow under all four feet
feet = [P(sx * 10.5, 0, z) for sx in (-1, 1) for z in (FRONT_Z[0], BACK_Z[1] + 1.5)]
fx0 = min(p[0] for p in feet) - 46
fx1 = max(p[0] for p in feet) + 46
fy0 = min(p[1] for p in feet) - 26
fy1 = max(p[1] for p in feet) + 26
d.shape("ellipse", "Chair shadow", x=round(fx0), y=round(fy0),
        width=round(fx1 - fx0), height=round(fy1 - fy0),
        fill=rad((0, "#050705", 66), (0.6, "#050705", 28), (1, "#050705", 0)),
        stroke=NONE)

# --- pegged adjustment hardware -------------------------------------------------------
# the notched rack behind the seat back plus round hinge pegs on the stiles
# read the reclining mechanism without a loose prop hanging off the silhouette
# notched rack across the rear posts, barely visible behind the seat back
prism("Notch rack", box(-9.6, 14.8, 9.8, 9.6, 16.2, 10.9), lo=0.02, hi=0.7)
for i in range(4):
    nx = -7.0 + i * 4.6
    d.path(poly([P(nx, 16.2, 9.9), P(nx + 1.4, 16.2, 9.9),
                 P(nx + 1.4, 15.3, 9.9), P(nx, 15.3, 9.9)]),
           f"Rack notch {i+1}", fill="#241608", stroke=NONE)
# hinge pegs where the backrest pivots
for sx in (-1, 1):
    px, py = P(sx * 8.8, HINGE_Y + 0.8, HINGE_Z - 0.4)
    d.shape("ellipse", f"Hinge peg {sx:+d}", x=round(px - 5), y=round(py - 5),
            width=10, height=10, fill=rad((0, "#D8BC84"), (1, "#6A4A20")),
            stroke=INK, strokeWidth=1.4)

# --- backrest: frame stiles + rails, then the leather pad on the front ----------------
for sx in (-1, 1):
    x0, x1 = (7.9, 9.7) if sx > 0 else (-9.7, -7.9)
    prism(f"Back stile {sx:+d}", lean_box(x0, x1, BK_YB - 1.6, BK_ZB - 0.4,
                                          BK_YT + 0.6, BK_ZT + 0.4, 1.5),
          lo=0.02, hi=0.75)
# top rail joining the stiles
prism("Back top rail", lean_box(-9.7, 9.7, BK_YT - 1.4, BK_ZT + 0.4,
                                BK_YT + 0.6, BK_ZT + 0.4, 1.5), lo=0.02, hi=0.8)
# bottom rail, mostly hidden by the pad
prism("Back bottom rail", lean_box(-9.7, 9.7, BK_YB - 1.6, BK_ZB - 0.4,
                                   BK_YB + 0.6, BK_ZB + 0.4, 1.5), lo=0.02, hi=0.7)
# loose back cushion resting on the frame
prism("Back cushion", lean_box(-7.7, 7.7, BK_YB + 0.6, BK_ZB - 2.0,
                               BK_YT - 0.8, BK_ZT - 2.0, 2.9),
      lo=0.08, hi=1.0, ramp=(LTH_D, LTH_L), ink=2.0)

# --- far side (left): posts, spindles, arm ----------------------------------------------
for sx in (-1,):
    x0, x1 = (-POST_X[1], -POST_X[0])
    prism("Back post L", box(x0, 0.0, BACK_Z[0], x1, ARM_Y0 + 1.2, BACK_Z[1]), lo=0.02, hi=0.75)
    prism("Front post L", box(x0, 0.0, FRONT_Z[0], x1, ARM_Y0, FRONT_Z[1]), lo=0.02, hi=0.75)
    for i in range(4):
        z0 = FRONT_Z[1] + 0.9 + i * 1.9
        prism(f"Spindle L {i+1}", box(x0 + 0.45, SEAT_Y1 - 0.6, z0,
                                    x1 - 0.45, ARM_Y0, z0 + 0.75), lo=0.02, hi=0.7)
    prism("Arm L", box(-13.4, ARM_Y0, -4.6, -9.0, ARM_Y1, 9.4), lo=0.05, hi=1.0)

# --- seat frame, rails and stretchers -----------------------------------------------------
prism("Rear seat rail", box(-9.4, SEAT_Y0, 6.2, 9.4, SEAT_Y1, 8.2), lo=0.02, hi=0.7)
prism("Seat deck", box(-9.4, SEAT_Y0 + 1.6, -3.0, 9.4, SEAT_Y1, 7.8), lo=0.02, hi=0.75)
prism("Front apron", box(-10.4, SEAT_Y0 - 1.4, -3.6, 10.4, SEAT_Y1, -2.4), lo=0.02, hi=0.8)
# low stretchers between the posts
prism("Front stretcher", box(-9.4, 4.6, -2.9, 9.4, 7.0, -1.7), lo=0.02, hi=0.7)
for sx in (-1, 1):
    x0, x1 = (POST_X[0], POST_X[1]) if sx > 0 else (-POST_X[1], -POST_X[0])
    prism(f"Side stretcher {sx:+d}", box(x0 + 0.3, 4.6, -1.2, x1 - 0.3, 7.0, 7.0),
          lo=0.02, hi=0.7)

# --- seat cushion, overhanging the apron -----------------------------------------------
prism("Seat cushion", box(-10.2, SEAT_Y1 - 0.1, -4.1, 10.2, SEAT_Y1 + 3.0, 8.4),
      lo=0.08, hi=1.0, ramp=(LTH_D, LTH_L), ink=2.0)
# cushion seam piping along the front top edge
pa, pb = P(-10.0, SEAT_Y1 + 3.0, -4.0), P(10.0, SEAT_Y1 + 3.0, -4.0)
d.path(f"M{pa[0]:.1f},{pa[1]:.1f} L{pb[0]:.1f},{pb[1]:.1f}", "Cushion piping",
       fill=NONE, stroke="#5A2418", strokeWidth=2.2, opacity=70)

# --- near side (right): posts, spindles, arm — drawn last, nearest ----------------------
x0, x1 = POST_X
prism("Back post R", box(x0, 0.0, BACK_Z[0], x1, ARM_Y0 + 1.2, BACK_Z[1]), lo=0.02, hi=0.8)
for i in range(4):
    z0 = FRONT_Z[1] + 0.9 + i * 1.9
    prism(f"Spindle R {i+1}", box(x0 + 0.45, SEAT_Y1 - 0.6, z0,
                                x1 - 0.45, ARM_Y0, z0 + 0.75), lo=0.02, hi=0.75)
prism("Front post R", box(x0, 0.0, FRONT_Z[0], x1, ARM_Y0, FRONT_Z[1]), lo=0.02, hi=0.85)
prism("Arm R", box(9.0, ARM_Y0, -4.6, 13.4, ARM_Y1, 9.4), lo=0.05, hi=1.0)
# grain lines along the near arm top
for g in range(2):
    gxa = 9.0 + (13.4 - 9.0) * (0.35 + 0.3 * g)
    ga, gb = P(gxa, ARM_Y1 + 0.05, -3.8), P(gxa, ARM_Y1 + 0.05, 8.6)
    d.path(f"M{ga[0]:.1f},{ga[1]:.1f} L{gb[0]:.1f},{gb[1]:.1f}",
           f"Arm grain R {g+1}", fill=NONE, stroke=OAK_D, strokeWidth=1.3, opacity=30)
# corbels under the front of each arm
for sx in (-1, 1):
    cx0, cx1 = (POST_X[0] + 0.2, POST_X[1]) if sx > 0 else (-POST_X[1], -POST_X[0] - 0.2)
    prism(f"Arm corbel {sx:+d}", box(cx0, ARM_Y0 - 2.6, -3.6, cx1, ARM_Y0, -2.2),
          lo=0.02, hi=0.7)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F2E8D4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C4AE8E", justify="center")
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


caption("MORRIS CHAIR", "OAK · LEATHER · IRON PEGS")
d.finish("morris-chair-V1R00")
