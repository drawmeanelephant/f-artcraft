#!/usr/bin/env python3
"""Silla matera — field plate V1R00. A low Argentine matera chair in slight
three-quarter view: a rustic frame of debarked poles — short splayed legs,
low stretchers, two rear posts rising into a modest two-rail backrest — and
a seat handwoven from pale tiento rawhide strips, front-to-back strips laid
continuous, left-to-right strips tucked segment by segment between them.
Warm wood, pale rawhide, dusk plum disc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Silla Matera — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A1A16"   # warm dark ink, never pure black
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

def smooth(pts, closed=True, k=1.0):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

def poly(pts):
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"

# --- projection: model in inches, fixed yaw + pitch ------------------------------------
YAW, PITCH = math.radians(34), math.radians(17)
S, OX, OY = 14.7, 500.0, 730.0

def P(x, y, z):
    c, s = math.cos(YAW), math.sin(YAW)
    xr, zr = x * c + z * s, -x * s + z * c
    p = (OX + S * xr, OY - S * (y * math.cos(PITCH) + zr * math.sin(PITCH)))
    EXTENT.append(p)
    return p

WOOD = ((0, "#A8743E"), (0.3, "#8A5A2E"), (0.6, "#6A4020"), (1, "#3E2412"))
WOOD_FAR = ((0, "#7A522C"), (0.5, "#5E3C1E"), (1, "#38200E"))

def pole(name, pts3, r=0.42, grad=WOOD, ink=2.2):
    """A slightly irregular debarked pole: capsule ribbon along a 3D polyline."""
    pts = [P(*p) for p in pts3]
    w = r * S
    # offset normals per joint (screen-space)
    left, right = [], []
    for i, p in enumerate(pts):
        a = pts[max(0, i - 1)]; b = pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    d.path(smooth(left + right[::-1] + [left[0]]), name,
           fill=lin(left[0], right[-1], *grad), stroke=INK, strokeWidth=ink, join="round")
    assert 2 * w >= 3, "pole must stay >= 3pt"
    return pts

def strap(name, pts, w, grad, ink=1.6, shade=False):
    """A rawhide tiento strip: ribbon along 2D points, width w in pt."""
    left, right = [], []
    for i, p in enumerate(pts):
        a = pts[max(0, i - 1)]; b = pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        left.append((p[0] + nx * w / 2, p[1] + ny * w / 2))
        right.append((p[0] - nx * w / 2, p[1] - ny * w / 2))
    d.path(smooth(left + right[::-1] + [left[0]]), name,
           fill=grad, stroke="#5E4020" if not shade else "#3E2812",
           strokeWidth=ink, join="round")
    return left, right

# --- backdrop + dusk plum plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#16121C"), (1, "#070509")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#6E5A76", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#6E5A76"), (0.6, "#463450"), (1, "#241A2E")),
        stroke="#120C18", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CBB8D4", strokeWidth=3, opacity=25)
d.shape("ellipse", "Back glow", x=260, y=170, width=480, height=480,
        fill=rad((0, "#C89078", 16), (0.6, "#8A5A58", 6), (1, "#6A4050", 0)), stroke=NONE)

# floor, closed on the disc arc
FY = 668
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#5E4A62", 34), (1, "#1A1220", 70)), stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#D4C4DE", strokeWidth=2, opacity=18)

# === chair model (inches) ================================================================
SEAT_Y, SEAT_X, SEAT_Z = 11.0, 8.6, 7.4
BACK_TOP = 27.5

# shadow from the four feet
feet = [P(sx * (SEAT_X + 0.9), 0, sz * (SEAT_Z + 1.0)) for sx in (-1, 1) for sz in (-1, 1)]
fx0, fx1 = min(p[0] for p in feet) - 40, max(p[0] for p in feet) + 40
fy0, fy1 = min(p[1] for p in feet) - 20, max(p[1] for p in feet) + 22
d.shape("ellipse", "Chair shadow", x=round(fx0), y=round(fy0), width=round(fx1 - fx0),
        height=round(fy1 - fy0),
        fill=rad((0, "#0A060E", 62), (0.6, "#0A060E", 28), (1, "#0A060E", 0)), stroke=NONE)

# far side first: rear-left members sit deeper in the yaw
# leg layout: x +-SEAT_X (left/right), z +-SEAT_Z (back/front, +z = front)
def leg_pts(sx, sz, splay=0.9):
    top = (sx * SEAT_X, SEAT_Y, sz * SEAT_Z)
    mid = (sx * (SEAT_X + splay * 0.5), SEAT_Y * 0.45, sz * (SEAT_Z + splay * 0.5))
    foot = (sx * (SEAT_X + splay), 0, sz * (SEAT_Z + splay))
    return [foot, mid, top]

# far legs (back-left depth order): draw rear leg + far front leg darker
pole("Far back leg", leg_pts(-1, -1), r=0.40, grad=WOOD_FAR)
pole("Far front leg", leg_pts(-1, 1), r=0.40, grad=WOOD_FAR)
# far stretcher between far legs
pole("Far stretcher", [(-SEAT_X - 0.5, 4.6, SEAT_Z + 0.4), (-SEAT_X - 0.5, 4.4, -SEAT_Z - 0.4)],
     r=0.28, grad=WOOD_FAR, ink=1.8)
# back posts rise from the rear legs; far post first
for sx, nm in ((-1, "Far"), (1, "Near")):
    pole(f"{nm} back post",
         [(sx * (SEAT_X + 0.6), 0.5, -SEAT_Z - 0.7),
          (sx * SEAT_X, SEAT_Y, -SEAT_Z),
          (sx * (SEAT_X - 0.3), 19.5, -SEAT_Z - 0.4),
          (sx * (SEAT_X - 0.7), BACK_TOP, -SEAT_Z - 0.8)],
         r=0.42 if sx > 0 else 0.40, grad=WOOD if sx > 0 else WOOD_FAR)
# backrest rails: two irregular slats between the posts
pole("Back rail upper", [(-SEAT_X + 0.4, 24.6, -SEAT_Z - 0.55), (0, 24.2, -SEAT_Z - 0.5),
                         (SEAT_X - 0.5, 24.7, -SEAT_Z - 0.6)], r=0.34)
pole("Back rail lower", [(-SEAT_X + 0.6, 18.6, -SEAT_Z - 0.4), (0.2, 18.2, -SEAT_Z - 0.35),
                         (SEAT_X - 0.3, 18.7, -SEAT_Z - 0.45)], r=0.30)

# seat frame rails: front, back, then the near side rail
pole("Back seat rail", [(-SEAT_X, SEAT_Y, -SEAT_Z), (0, SEAT_Y + 0.25, -SEAT_Z - 0.1),
                        (SEAT_X, SEAT_Y, -SEAT_Z)], r=0.34)
pole("Near side rail", [(SEAT_X, SEAT_Y, -SEAT_Z), (SEAT_X + 0.2, SEAT_Y - 0.1, 0),
                        (SEAT_X, SEAT_Y, SEAT_Z)], r=0.34)
pole("Far side rail", [(-SEAT_X, SEAT_Y, -SEAT_Z), (-SEAT_X - 0.2, SEAT_Y - 0.1, 0),
                       (-SEAT_X, SEAT_Y, SEAT_Z)], r=0.30, grad=WOOD_FAR)

# --- the tiento weave ----------------------------------------------------------------------
# seat plane between the rails; strips sag 0.5" at mid
def seat_pt(x, z, sag=0.0):
    return P(x, SEAT_Y + 0.28 - sag, z)

TIENTO = lin((0, 0), (0, 0), (0, "#E0C69C"))  # placeholder, replaced per strip

def tiento_grad(a, b, tone=0):
    pal = [("#EAD3A8", "#C4A374", "#96754C"), ("#E4CC9E", "#BC9968", "#8E6E44"),
           ("#F0DBB2", "#CBA97B", "#9C7A50")]
    c = pal[tone % 3]
    return lin(a, b, (0, c[0]), (0.5, c[1]), (1, c[2]))

NX, NZ = 7, 6
xs = [-SEAT_X + 1.15 + i * (2 * (SEAT_X - 1.15) / (NX - 1)) for i in range(NX)]
zs = [-SEAT_Z + 1.15 + i * (2 * (SEAT_Z - 1.15) / (NZ - 1)) for i in range(NZ)]

# under-seat shadow: the dark bed the strips lie over
bed = [seat_pt(-SEAT_X + 0.6, -SEAT_Z + 0.6), seat_pt(SEAT_X - 0.6, -SEAT_Z + 0.6),
       seat_pt(SEAT_X - 0.6, SEAT_Z - 0.6), seat_pt(-SEAT_X + 0.6, SEAT_Z - 0.6)]
d.path(poly(bed), "Seat under-bed", fill="#3A2414", opacity=92, stroke=NONE)

# front-to-back strips: continuous, laid over the crossings
fb_lr = []
for i, x in enumerate(xs):
    pts = [seat_pt(x, -SEAT_Z + 0.2), seat_pt(x + 0.15 * math.sin(i * 2.1), 0, 0.55),
           seat_pt(x - 0.1, SEAT_Z - 0.2)]
    fb_lr.append(pts)
# left-to-right strips: drawn first in the gaps (tucked under FB strips)
for j, z in enumerate(zs):
    row_pts = []
    for i in range(NX - 1):
        x0, x1 = xs[i] + 0.55, xs[i + 1] - 0.55
        seg = [seat_pt(x0, z), seat_pt((x0 + x1) / 2, z, 0.3), seat_pt(x1, z)]
        g = tiento_grad(P(x0, SEAT_Y, z), P(x1, SEAT_Y, z), tone=(i + j) % 3)
        strap(f"LR strip {j+1}.{i+1}", seg, 4.6, g, ink=1.4)
# then the continuous FB strips over them
for i, pts in enumerate(fb_lr):
    g = tiento_grad(pts[0], pts[-1], tone=i % 3)
    strap(f"FB strip {i+1}", pts, 5.2, g, ink=1.5)
    # a leather sheen down the strip's lit flank
    a, b = pts[0], pts[-1]
    d.path(f"M{a[0] + 1.5:.1f},{a[1]:.1f} Q{(a[0] + b[0]) / 2 + 1.5:.1f},{(a[1] + b[1]) / 2 - 3:.1f} {b[0] + 1.5:.1f},{b[1]:.1f}",
           f"FB sheen {i+1}", fill=NONE, stroke="#FFF2D8", strokeWidth=1.8,
           opacity=40, cap="round")

# front seat rail wraps the strip ends, then near legs over everything
pole("Front seat rail", [(-SEAT_X, SEAT_Y, SEAT_Z), (0, SEAT_Y - 0.15, SEAT_Z + 0.25),
                         (SEAT_X, SEAT_Y, SEAT_Z)], r=0.38)
pole("Near front leg", leg_pts(1, 1), r=0.44)
pole("Near back leg", leg_pts(1, -1), r=0.44)
# near stretcher
pole("Near stretcher", [(SEAT_X + 0.6, 4.8, -SEAT_Z - 0.3), (SEAT_X + 0.7, 4.5, SEAT_Z + 0.4)],
     r=0.30)
# front stretcher between the front legs
pole("Front stretcher", [(-SEAT_X - 0.7, 4.9, SEAT_Z + 0.75), (0, 4.7, SEAT_Z + 0.9),
                         (SEAT_X + 0.7, 4.9, SEAT_Z + 0.75)], r=0.28)

for nm, p3 in (("post L", (-SEAT_X - 0.6, 0.4, -SEAT_Z - 0.7)),
               ("post R", (SEAT_X + 0.6, 0.4, -SEAT_Z - 0.7)),
               ("leg LF", (-SEAT_X - 0.9, 0.3, SEAT_Z + 0.9)),
               ("leg RF", (SEAT_X + 0.9, 0.3, SEAT_Z + 0.9))):
    x, y = P(*p3)
    d.shape("ellipse", f"Foot pad {nm}", x=round(x - 12), y=round(y - 3), width=24, height=7,
            fill=rad((0, "#000000", 50), (1, "#000000", 0)), stroke=NONE)

# --- extent check -----------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far

# plate rim over everything
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#120C18", strokeWidth=6)
d.shape("ellipse", "Plate inner ring 2", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CBB8D4", strokeWidth=3, opacity=22)

# --- caption -----------------------------------------------------------------------------------
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
               color="#E8DCCE", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#BCA8C2", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=260)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "materials")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" % (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "materials":
            assert b["width"] <= 760, b["width"]

caption("SILLA MATERA", "WOOD · RAWHIDE")
d.finish("silla-matera-V1R00")
