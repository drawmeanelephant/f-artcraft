#!/usr/bin/env python3
"""Adirondack chair — field plate V1R00. Three-quarter view from the front
right: five fanned back slats over a raked seat, wide flat arms carried on
the front legs, rear legs splayed back to the ground. Weathered-fir plate,
lake-porch mood. 1000x1000. Modelled in inches (x right, y up, +z back)
and projected with a fixed yaw + pitch; every board is an 8-corner prism
drawn far-to-near with per-face wood gradients.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Adirondack Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2E211A"   # warm dark, not black
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
YAW, PITCH = math.radians(30), math.radians(24)
S, OX, OY = 14.8, 446.0, 742.0
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
LIGHT = (-0.52, 0.72, -0.46)
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
    """Mix two wood hex colors at brightness b in [0,1]."""
    a = [int(hex1[i:i + 2], 16) for i in (1, 3, 5)]
    c = [int(hex2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (c[i] - a[i]) * b) for i in range(3))


W_DARK, W_LIGHT = "#3B2F26", "#9C8A6E"   # weathered fir ramp


def prism(name, corners, lo=0.06, hi=0.94):
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
        g = lin((0, y0), (0, y1), (0, shade(W_DARK, W_LIGHT, min(1, b + 0.12))),
                                 (1, shade(W_DARK, W_LIGHT, b)))
        d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=1.8, join="round")


def beam(name, a, b, w, t):
    """Board whose top edge runs a->b in the (y,z) plane, extruded across x
    between a[0] and b[0]; a and b are (x_center, y, z)."""
    corners = [(a[0] - w / 2, a[1], a[2]), (a[0] + w / 2, a[1], a[2]),
               (a[0] + w / 2, a[1] + t, a[2]), (a[0] - w / 2, a[1] + t, a[2]),
               (b[0] - w / 2, b[1], b[2]), (b[0] + w / 2, b[1], b[2]),
               (b[0] + w / 2, b[1] + t, b[2]), (b[0] - w / 2, b[1] + t, b[2])]
    prism(name, corners)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#122023"), (1, "#060D0E")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8A8478", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#6E685E"), (0.6, "#4C4840"), (1, "#28251F")),
        stroke="#14110D", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8D0C0", strokeWidth=3, opacity=26)
d.shape("ellipse", "Porch glow", x=250, y=160, width=520, height=520,
        fill=rad((0, "#E8B87A", 16), (0.6, "#A07A50", 6), (1, "#7A5C40", 0)),
        stroke=NONE)
FY = 668
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#5C564C", 38), (1, "#181510", 74)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#DCD4C4", strokeWidth=2, opacity=20)

# --- chair geometry (inches; x right, y up, +z back) ----------------------------------
SEAT_Y0, SEAT_Y1 = 15.0, 10.5      # seat slope front -> back
SEAT_Z0, SEAT_Z1 = -2.2, 9.8
SEAT_X = 13.0
LEG_X = (10.4, 12.8)               # front leg span across x
ARM_Y0, ARM_Y1 = 20.8, 22.7
ARM_X = (9.0, 16.2)
BACK_Z0 = 11.4
LEAN = 0.30                        # dz per dy of the back slats


def seat_y(z):
    return SEAT_Y0 + (SEAT_Y1 - SEAT_Y0) * (z - SEAT_Z0) / (SEAT_Z1 - SEAT_Z0)


# grounding shadow from the feet before any wood is drawn
feet = [P(sx * 11.6, 0, z) for sx in (-1, 1) for z in (-2.0, 15.6)]
fx0 = min(p[0] for p in feet) - 42
fx1 = max(p[0] for p in feet) + 42
fy0 = min(p[1] for p in feet) - 26
fy1 = max(p[1] for p in feet) + 26
d.shape("ellipse", "Chair shadow", x=round(fx0), y=round(fy0),
        width=round(fx1 - fx0), height=round(fy1 - fy0),
        fill=rad((0, "#04070A", 66), (0.6, "#04070A", 28), (1, "#04070A", 0)),
        stroke=NONE)

# --- back uprights and braces, behind the slats ----------------------------------------
for sx in (-1, 1):
    x0, x1 = sx * 8.6 + (0 if sx > 0 else -2.2), sx * 8.6 + (2.2 if sx > 0 else 0)
    # upright leaning with the back, from just above the seat to near the top
    z0, z1 = BACK_Z0 - 0.4, BACK_Z0 - 0.4 + 26 * LEAN
    corners = [(x0, 8.5, z0), (x1, 8.5, z0), (x1, 34.5, z1), (x0, 34.5, z1),
               (x0, 8.5, z0 + 1.6), (x1, 8.5, z0 + 1.6),
               (x1, 34.5, z1 + 1.6), (x0, 34.5, z1 + 1.6)]
    prism(f"Back upright {sx:+d}", corners, lo=0.02, hi=0.75)
# cross braces showing through the slat gaps
for i, by in enumerate((16.5, 27.5)):
    bz = BACK_Z0 + 0.5 + (by - 8.5) * LEAN
    prism(f"Back brace {i+1}", box(-9.6, by - 1.1, bz, 9.6, by + 1.1, bz + 1.0),
          lo=0.02, hi=0.7)

# --- back slats: five, fanning up and out ----------------------------------------------
SLATS = [(-8.2, -12.6, 33.2), (-4.1, -6.4, 35.6), (0.0, 0.0, 36.6),
         (4.1, 6.4, 35.6), (8.2, 12.6, 33.2)]   # (bottom cx, top cx, top y)
for i, (xb, xt, yt) in enumerate(SLATS):
    zb, zt = BACK_Z0, BACK_Z0 + (yt - 9.0) * LEAN
    w_b, w_t = 3.35, 4.1
    corners = [(xb - w_b / 2, 8.6, zb), (xb + w_b / 2, 8.6, zb),
               (xt + w_t / 2, yt, zt), (xt - w_t / 2, yt, zt),
               (xb - w_b / 2, 8.6, zb + 0.95), (xb + w_b / 2, 8.6, zb + 0.95),
               (xt + w_t / 2, yt, zt + 0.95), (xt - w_t / 2, yt, zt + 0.95)]
    prism(f"Back slat {i+1}", corners, lo=0.10, hi=1.0)

# --- rear legs: boards splayed back to the ground ---------------------------------------
for sx in (-1, 1):
    x0, x1 = (LEG_X[0], LEG_X[1]) if sx > 0 else (-LEG_X[1], -LEG_X[0])
    corners = [(x0, 0.0, 15.6), (x1, 0.0, 15.6), (x1, 0.0, 17.2), (x0, 0.0, 17.2),
               (x0, 12.8, 8.6), (x1, 12.8, 8.6), (x1, 14.4, 10.2), (x0, 14.4, 10.2)]
    prism(f"Rear leg {sx:+d}", corners, lo=0.02, hi=0.8)

# --- seat slats on their rake -----------------------------------------------------------
for i in range(4):
    z0 = SEAT_Z0 + i * 3.05
    z1 = z0 + 2.62
    y0, y1 = seat_y(z0) - 0.95, seat_y(z1) - 0.95
    corners = [(-SEAT_X, y0, z0), (SEAT_X, y0, z0), (SEAT_X, y0 + 0.95, z0),
               (-SEAT_X, y0 + 0.95, z0),
               (-SEAT_X, y1, z1), (SEAT_X, y1, z1), (SEAT_X, y1 + 0.95, z1),
               (-SEAT_X, y1 + 0.95, z1)]
    prism(f"Seat slat {i+1}", corners, lo=0.08, hi=1.0)
# front fascia under the seat lip
prism("Seat fascia", box(-SEAT_X - 0.4, SEAT_Y0 - 3.6, SEAT_Z0 - 1.5,
                        SEAT_X + 0.4, SEAT_Y0 - 0.5, SEAT_Z0 - 0.4), lo=0.02, hi=0.8)

# seat-side stretchers between front leg and rear leg (drawn before the
# legs so their front ends hide behind the leg face)
for sx in (-1, 1):
    x0, x1 = (LEG_X[0] + 0.3, LEG_X[1]) if sx > 0 else (-LEG_X[1], -LEG_X[0] - 0.3)
    corners = [(x0, 8.4, -0.2), (x1, 8.4, -0.2), (x1, 11.2, -0.2), (x0, 11.2, -0.2),
               (x0, 9.6, 8.6), (x1, 9.6, 8.6), (x1, 12.4, 8.6), (x0, 12.4, 8.6)]
    prism(f"Side stretcher {sx:+d}", corners, lo=0.02, hi=0.75)

# --- front legs: wide boards carrying the arms -------------------------------------------
for sx in (-1, 1):
    x0, x1 = (LEG_X[0], LEG_X[1]) if sx > 0 else (-LEG_X[1], -LEG_X[0])
    prism(f"Front leg {sx:+d}", box(x0, 0.0, -2.9, x1, ARM_Y0, -0.7), lo=0.02, hi=0.8)

# --- arm rest brackets behind the front legs ----------------------------------------------
for sx in (-1, 1):
    x0, x1 = (LEG_X[0] + 0.6, LEG_X[1] - 0.2) if sx > 0 else (-LEG_X[1] + 0.2, -LEG_X[0] - 0.6)
    prism(f"Arm post {sx:+d}", box(x0, 13.0, 7.2, x1, ARM_Y0, 9.4), lo=0.02, hi=0.75)

# --- arms: wide flat boards, front edge overhanging ---------------------------------------
for sx in (-1, 1):
    x0, x1 = (ARM_X[0], ARM_X[1]) if sx > 0 else (-ARM_X[1], -ARM_X[0])
    prism(f"Arm {sx:+d}", box(x0, ARM_Y0, -5.4, x1, ARM_Y1, 11.6), lo=0.05, hi=1.0)
    # grain lines along the arm top
    for g in range(2):
        gx = x0 + (x1 - x0) * (0.36 + 0.26 * g)
        ga, gb = P(gx, ARM_Y1 + 0.05, -4.4), P(gx, ARM_Y1 + 0.05, 10.6)
        d.path(f"M{ga[0]:.1f},{ga[1]:.1f} L{gb[0]:.1f},{gb[1]:.1f}",
               f"Arm grain {sx:+d} {g+1}", fill=NONE, stroke=W_DARK,
               strokeWidth=1.3, opacity=30)

# a short tumbler on the left arm — the chair was built to hold a drink
gx, gz = -12.9, -0.6
gbx, gby = P(gx, ARM_Y1, gz)          # base centre on the arm
gtx, gty = P(gx, ARM_Y1 + 4.6, gz)    # rim centre
gr_b, gr_t = S * 1.55, S * 1.75       # base and rim radii (screen x)
gyr_b, gyr_t = gr_b * 0.30, gr_t * 0.30
# tumbler contact shadow on the arm
d.shape("ellipse", "Tumbler shadow", x=round(gbx - gr_b), y=round(gby - gyr_b * 0.6),
        width=round(gr_b * 2), height=round(gyr_b * 1.4),
        fill=rad((0, "#100C08", 55), (1, "#100C08", 0)), stroke=NONE)
# glass body
d.path(f"M{gbx - gr_b:.1f},{gby:.1f} C{gbx - gr_b:.1f},{gby + gyr_b:.1f} "
       f"{gbx + gr_b:.1f},{gby + gyr_b:.1f} {gbx + gr_b:.1f},{gby:.1f} "
       f"L{gtx + gr_t:.1f},{gty:.1f} C{gtx + gr_t:.1f},{gty + gyr_t:.1f} "
       f"{gtx - gr_t:.1f},{gty + gyr_t:.1f} {gtx - gr_t:.1f},{gty:.1f} Z",
       "Tumbler body", fill=lin((gtx, gty), (gbx, gby),
       (0, "#E8DCC2", 34), (0.6, "#C8A060", 55), (1, "#8A6434", 72)),
       stroke="#EADCC0", strokeWidth=2.0, join="round")
# drink surface inside the rim
d.shape("ellipse", "Drink surface", x=round(gtx - gr_t + 3), y=round(gty - gyr_t + 3.5),
        width=round((gr_t - 3) * 2), height=round(gyr_t * 2),
        fill=rad((0, "#F0C87A", 90), (1, "#A06E28", 90)), stroke=NONE)
# rim highlight
d.path(f"M{gtx - gr_t:.1f},{gty:.1f} C{gtx - gr_t:.1f},{gty - gyr_t:.1f} "
       f"{gtx + gr_t:.1f},{gty - gyr_t:.1f} {gtx + gr_t:.1f},{gty:.1f}",
       "Tumbler rim", fill=NONE, stroke="#F4E8CE", strokeWidth=2.4, opacity=85)
# side highlight streak
d.path(f"M{gtx - gr_t + 5:.1f},{gty + 4:.1f} L{gbx - gr_b + 5:.1f},{gby - 4:.1f}",
       "Tumbler streak", fill=NONE, stroke="#FAF0DC", strokeWidth=3, opacity=40)

# peg heads on the front legs
for sx in (-1, 1):
    xm = (LEG_X[0] + LEG_X[1]) / 2 * sx
    px, py = P(xm + (1.4 if sx > 0 else -1.4), 17.5, -2.6)
    d.shape("ellipse", f"Leg peg {sx:+d}", x=round(px - 4.5), y=round(py - 4.5),
            width=9, height=9, fill=rad((0, "#C8B89E"), (1, "#6A5A48")),
            stroke=INK, strokeWidth=1.2)

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
               color="#F0E8DA", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C0B2A2", justify="center")
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


caption("ADIRONDACK CHAIR", "WEATHERED FIR · GALVANIZED IRON")
d.finish("adirondack-chair-V1R00")
