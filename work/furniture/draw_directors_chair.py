#!/usr/bin/env python3
"""Director's chair — field plate V1R00. Three-quarter from the front
right: beech scissor side-frames crossed at pivot bolts, flat arms on top,
a natural canvas seat slung between front and back rungs, and a canvas
backrest band between the tall rear posts. A strip of gaffer tape marks
the spot on the floor. Canvas plate, backlot mood: warm tan disc with a
soft studio spot from the upper left. 1000x1000.
Modelled in inches (x right, y up, +z back), projected with fixed yaw +
pitch; frame bars are 8-corner prisms culled by view normal.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Director's Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#201810"   # warm dark, not black
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


def smooth(pts, closed=True):
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = "M%.1f,%.1f" % pts[0]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(33), math.radians(19)
S, OX, OY = 13.4, 502.0, 728.0
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


FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
TO_VIEWER = (SY * CP, SP, -CY * CP)
LIGHT = (-0.42, 0.80, -0.44)
_l = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / _l for c in LIGHT)

BEECH_D, BEECH_L = "#3A2412", "#B0824A"     # beech ramp
BEECH_HI = "#D8AC70"


def prism(name, corners, lo=0.06, hi=0.94, ink=1.8, c1=BEECH_D, c2=BEECH_L,
          bias=0.0):
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
        b = lo + (hi - lo) * max(0.0, lam + bias) ** 0.8
        b = max(0.0, min(1.0, b))
        y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
        g = lin((0, y0), (0, y1), (0, shade(c1, c2, min(1, b + 0.12))),
                                 (1, shade(c1, c2, b)))
        d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return faces


def rbox(cx, cz, y0, y1, hw, ht, ang):
    """Box hw x ht in plan, rotated ang about y through (cx,cz)."""
    ca, sa = math.cos(ang), math.sin(ang)
    cs = [(cx + lx * ca + lz * sa, cz - lx * sa + lz * ca)
          for lx, lz in ((-hw, -ht), (hw, -ht), (hw, ht), (-hw, ht))]
    A, B, C, D = cs
    return [(A[0], y0, A[1]), (B[0], y0, B[1]), (B[0], y1, B[1]),
            (A[0], y1, A[1]), (D[0], y0, D[1]), (C[0], y0, C[1]),
            (C[0], y1, C[1]), (D[0], y1, D[1])]


def barbox(sx, a, b, tx=0.38, tp=0.46):
    """8 corners of a square-section bar from (z,y) a to b on plane x=sx.
    End caps are rectangles tx in x by tp along the in-plane normal."""
    az, ay = a
    bz, by = b
    dz, dy = bz - az, by - ay
    L = math.hypot(dz, dy)
    pz, py = -dy / L, dz / L          # in-plane normal

    def cap(zz, yy):
        q = [((sx - tx), (yy - tp * py), (zz - tp * pz)),
             ((sx + tx), (yy - tp * py), (zz - tp * pz)),
             ((sx + tx), (yy + tp * py), (zz + tp * pz)),
             ((sx - tx), (yy + tp * py), (zz + tp * pz))]
        return [(x, y, z) for x, y, z in q]
    A0, B0, C0, D0 = cap(az, ay)
    A1, B1, C1, D1 = cap(bz, by)
    return [A0, B0, B1, A1, D0, C0, C1, D1]


def bolt(name, p, r=4.5):
    x, y = P(*p)
    d.shape("ellipse", name, x=round(x - r), y=round(y - r), width=round(2 * r),
            height=round(2 * r),
            fill=rad((0, "#F8ECC8"), (0.55, "#C09A4E"), (1, "#6A4A18")),
            stroke=INK, strokeWidth=1.4)
    d.shape("ellipse", f"{name} glint", x=round(x - r * 0.5), y=round(y - r * 0.7),
            width=round(r * 0.7), height=round(r * 0.5),
            fill="#FFFFFF", opacity=80, stroke=NONE)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#141009"), (1, "#060403")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#A08858", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#6E5A3E"), (0.6, "#463620"), (1, "#161009")),
        stroke="#0C0805", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D4A8", strokeWidth=3, opacity=24)
# canvas weave hint: a few faint warp/weft lines inside the disc, low alpha
for i, y in enumerate(range(160, 820, 66)):
    h = math.sqrt(PR ** 2 - (y - PCY) ** 2) - 14
    d.path(f"M{PCX - h:.1f},{y} L{PCX + h:.1f},{y}", f"Weft {i+1}",
           fill=NONE, stroke="#E8D4A8", strokeWidth=1.6, opacity=5)
# studio spot from the upper left
d.shape("ellipse", "Spot", x=170, y=90, width=620, height=560,
        fill=rad((0, "#F4DCAC", 16), (0.55, "#C8A468", 6), (1, "#C8A468", 0)),
        stroke=NONE)

FY = 712
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#54432A", 42), (1, "#120C06", 78)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#EAD6A8", strokeWidth=2, opacity=18)

# --- chair geometry (inches) ----------------------------------------------------------
FX = 10.6                        # side-frame plane x
PIVOT = (0.0, 12.4)              # (z, y) of the scissor pivot
SEAT_Y, SEAT_Z = 17.3, 6.9       # rung height / rung z extent
ARM_Y = 24.3
POST_TOP = 33.6

# grounding shadow
sp = [P(x, 0, z) for x, z in [(-12.4, -11), (12.4, -11), (12.4, 11), (-12.4, 11)]]
sx0, sx1 = min(p[0] for p in sp) - 32, max(p[0] for p in sp) + 32
sy0, sy1 = min(p[1] for p in sp) - 13, max(p[1] for p in sp) + 15
d.shape("ellipse", "Chair shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#050302", 66), (0.6, "#050302", 25), (1, "#050302", 0)),
        stroke=NONE)

# gaffer tape marks on the floor, out front of the feet
for i, (tx, tz, ang) in enumerate([(-4.5, -12.5, 24), (-1.4, -12.9, 24)]):
    cx, cy = P(tx, 0.15, tz)
    L, W = 46, 13
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    q = [(cx + (-L / 2) * ca - (-W / 2) * sa, cy + (-L / 2) * sa + (-W / 2) * ca),
         (cx + (L / 2) * ca - (-W / 2) * sa, cy + (L / 2) * sa + (-W / 2) * ca),
         (cx + (L / 2) * ca - (W / 2) * sa, cy + (L / 2) * sa + (W / 2) * ca),
         (cx + (-L / 2) * ca - (W / 2) * sa, cy + (-L / 2) * sa + (W / 2) * ca)]
    d.path(poly(q), f"Tape {i+1}", fill="#D8C47E", opacity=38, stroke=NONE)


def frame(sx, near):
    """One scissor side-frame at x=sx."""
    # bar rising to the back: front foot -> arm top -> back post to POST_TOP
    prism(f"Scissor fwd {sx:+}", barbox(sx, (-8.4, 0.7), (8.2, ARM_Y)),
          lo=0.05, hi=0.95, ink=1.6, bias=(-0.06 if near else -0.18))
    prism(f"Back post {sx:+}", barbox(sx, (8.2, ARM_Y - 0.4), (8.9, POST_TOP)),
          lo=0.05, hi=0.95, ink=1.6, bias=(-0.06 if near else -0.18))
    # bar rising to the front: back foot -> arm front
    prism(f"Scissor bak {sx:+}", barbox(sx, (8.4, 0.7), (-8.2, ARM_Y)),
          lo=0.05, hi=0.95, ink=1.6, bias=(-0.06 if near else -0.18))
    # foot pads
    for zz in (-8.4, 8.4):
        fx, fy = P(sx, 0.35, zz)
        d.shape("ellipse", f"Foot {sx:+},{zz:+}", x=round(fx - 10), y=round(fy - 4),
                width=20, height=9, fill=rad((0, "#5E3A1C"), (1, "#200F06")),
                stroke=INK, strokeWidth=1.4)


# far frame first (x=-FX is the far side at this yaw)
frame(-FX, near=False)

# seat rungs + foot stretchers spanning the width between the frames
prism("Seat rung front", rbox(0, -SEAT_Z, SEAT_Y - 0.5, SEAT_Y + 0.5,
                              FX - 0.6, 0.5, 0), lo=0.1, hi=0.9, ink=1.5)
prism("Seat rung back", rbox(0, SEAT_Z, SEAT_Y - 0.5, SEAT_Y + 0.5,
                             FX - 0.6, 0.5, 0), lo=0.1, hi=0.9, ink=1.5)
prism("Stretcher front", rbox(0, -8.4, 2.6, 4.0, FX - 0.2, 0.55, 0),
      lo=0.06, hi=0.9, ink=1.5)
prism("Stretcher back", rbox(0, 8.4, 2.6, 4.0, FX - 0.2, 0.55, 0),
      lo=0.06, hi=0.9, ink=1.5)

# --- canvas seat: slung between the rungs, sagging toward z=0 ---------------------------
CW = 9.7                                # canvas half-width in x
SAG = 2.6


def seat_y(z):
    return SEAT_Y - SAG * math.sin(math.pi * (z + SEAT_Z) / (2 * SEAT_Z))


NB = 9
xs = [-CW + 2 * CW * j / NB for j in range(NB + 1)]
ZS = [-SEAT_Z + 2 * SEAT_Z * i / 22 for i in range(23)]
for j in range(NB):
    pts = [P(xs[j], seat_y(z), z) for z in ZS] + \
          [P(xs[j + 1], seat_y(z), z) for z in ZS[::-1]]
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    d.path(poly(pts), f"Seat strip {j+1}",
           fill=lin((0, y0), (0, y1), (0, "#8A7A58"), (0.45, "#CDB98E"),
                    (1, "#E4D4AC")), stroke=NONE)

# seat outline + sag shade + stitching
edge_f = [P(x, seat_y(-SEAT_Z), -SEAT_Z) for x in xs]
edge_b = [P(x, seat_y(SEAT_Z), SEAT_Z) for x in xs]
edge_l = [P(-CW, seat_y(z), z) for z in ZS]
edge_r = [P(CW, seat_y(z), z) for z in ZS]
loop = edge_l + edge_b[1:] + edge_r[::-1][1:] + edge_f[::-1][1:]
d.path(poly(loop), "Seat outline", fill=NONE, stroke=INK, strokeWidth=2.6,
       join="round")
dip = [P(x, seat_y(-0.6) + 0.15, -0.6) for x in xs]
d.path(smooth(dip, closed=False), "Seat dip shade", fill=NONE,
       stroke="#2A1E10", strokeWidth=17, opacity=20, cap="round")
d.path(smooth([(x, y + 4) for x, y in edge_f], closed=False), "Seat front hem",
       fill=NONE, stroke="#F0E4C0", strokeWidth=1.8, opacity=55,
       dash=[4, 3.5], cap="round")

# --- backrest canvas between the posts -------------------------------------------------
BY0, BY1 = 27.6, 31.9
BWX = 9.7
bz = 8.55
xs2 = [-BWX + 2 * BWX * j / 20 for j in range(21)]
top_e = [P(x, BY1 + 0.28 * math.cos(math.pi * x / BWX) - 0.28, bz) for x in xs2]
bot_e = [P(x, BY0 - 0.15 + 0.15 * math.cos(math.pi * x / BWX), bz) for x in xs2]
back_pts = top_e + bot_e[::-1]
d.path(poly(back_pts), "Backrest",
       fill=lin((0, min(p[1] for p in back_pts)), (0, max(p[1] for p in back_pts)),
                (0, "#E4D4AC"), (0.55, "#C4AE80"), (1, "#8A7A58")),
       stroke=INK, strokeWidth=2.4, join="round")
# top hem, side hems, a faint horizontal crease where the film fades
d.path(smooth([(x, y - 4) for x, y in top_e], closed=False), "Back top hem",
       fill=NONE, stroke="#8A7A58", strokeWidth=2.2, opacity=65)
for s_ in (-1, 1):
    ex = s_ * (BWX - 0.35)
    e0, e1 = P(ex, BY0 - 0.1, bz), P(ex, BY1 - 0.1, bz)
    d.path(f"M{e0[0]:.1f},{e0[1]:.1f} L{e1[0]:.1f},{e1[1]:.1f}",
           f"Back side hem {s_:+}", fill=NONE, stroke="#8A7A58",
           strokeWidth=2.0, opacity=60, dash=[4, 3])

# near frame over the canvas edges
frame(FX, near=True)

# arms over the scissor tops
for s_ in (-1, 1):
    prism(f"Arm {s_:+}", rbox(s_ * FX, 0, ARM_Y - 0.1, ARM_Y + 1.05, 0.62, 9.9, 0),
          lo=0.08, hi=0.97, ink=1.7)
# pivot bolts
for s_ in (-1, 1):
    bolt(f"Pivot bolt {s_:+}", (s_ * (FX + 0.42), PIVOT[1], PIVOT[0]))
# post caps
for s_ in (-1, 1):
    cx, cy = P(s_ * FX, POST_TOP + 0.35, 8.9)
    d.shape("ellipse", f"Post cap {s_:+}", x=round(cx - 6), y=round(cy - 5),
            width=12, height=10, fill=rad((0, BEECH_HI), (1, BEECH_D)),
            stroke=INK, strokeWidth=1.5)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F4E4C4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C8AE80", justify="center")
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


caption("DIRECTORS CHAIR", "BEECH · CANVAS · STEEL")
d.finish("directors-chair-V1R00")
