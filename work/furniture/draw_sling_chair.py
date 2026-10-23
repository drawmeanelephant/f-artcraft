#!/usr/bin/env python3
"""Sling chair — field plate V1R00. Three-quarter view of a folding sling
chair: two crossed chrome X-frames joined by a front and a back rail, a
rust-orange canvas sling hung between the rails and dipping deep between
them, its back hem seam stitched across the top. Slate plate. 1000x1000.
Modelled in 3D (inches) and projected with a fixed yaw + pitch; the sling's
fold line is where the fabric turns edge-on to the eye.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Sling Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A1A14"   # warm dark, not black
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


def smooth(pts, closed=False, move=True):
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = ("M%.1f,%.1f" if move else "L%.1f,%.1f") % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


def poly(pts):
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(36), math.radians(18)
S, OX, OY = 14.2, 498.0, 752.0


def P(x, y, z):
    c, s = math.cos(YAW), math.sin(YAW)
    xr, zr = x * c + z * s, -x * s + z * c
    p = (OX + S * xr, OY - S * (y * math.cos(PITCH) + zr * math.sin(PITCH)))
    EXTENT.append(p)
    return p


CHROME = ((0, "#3A424C"), (0.22, "#F2F6FA"), (0.36, "#A6B0BC"), (0.52, "#323A44"),
          (0.74, "#C4CCD6"), (1, "#4E5662"))


def tube(name, a, b, r=0.44, ink=1.6, grad=CHROME, ink_col=INK):
    """Chrome tube between 3D points with rounded ends, lit across its width."""
    A, B = P(*a), P(*b)
    dx, dy = B[0] - A[0], B[1] - A[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    w = r * S
    pts = []
    for k in range(9):
        t = math.pi * k / 8
        pts.append((B[0] + nx * w * math.cos(t) + ux * w * math.sin(t),
                    B[1] + ny * w * math.cos(t) + uy * w * math.sin(t)))
    for k in range(9):
        t = math.pi * k / 8
        pts.append((A[0] - nx * w * math.cos(t) - ux * w * math.sin(t),
                    A[1] - ny * w * math.cos(t) - uy * w * math.sin(t)))
    mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
    if nx > 0:
        nx, ny = -nx, -ny
    g = lin((mx + nx * w, my + ny * w), (mx - nx * w, my - ny * w), *grad)
    d.path(poly(pts), name, fill=g, stroke=ink_col, strokeWidth=ink, join="round")
    assert 2 * w >= 3, "tube must stay >= 3pt"
    return A, B


def bolt(name, p):
    x, y = P(*p)
    d.shape("ellipse", name, x=round(x - 8), y=round(y - 8), width=16, height=16,
            fill=rad((0, "#FFF0B8"), (0.55, "#D2A24A"), (1, "#7A5418")), stroke=INK, strokeWidth=1.6)
    d.shape("ellipse", f"{name} glint", x=round(x - 4), y=round(y - 5), width=5, height=4,
            fill="#FFFFFF", opacity=80, stroke=NONE)


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#14181D"), (1, "#06080A")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#6A7684", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#56626E"), (0.6, "#3A444F"), (1, "#232A32")), stroke="#0E1216", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4CED8", strokeWidth=3, opacity=26)
d.shape("ellipse", "Back glow", x=240, y=150, width=520, height=520,
        fill=rad((0, "#E8A070", 18), (0.6, "#B07050", 6), (1, "#805040", 0)), stroke=NONE)

FY = 672
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#5A6672", 36), (1, "#141A20", 72)), stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#D0D8E2", strokeWidth=2, opacity=20)

# --- frame geometry (inches) ----------------------------------------------------------
FX = 11.0
A_FOOT, A_TOP = (0.0, 10.5), (17.0, -10.0)     # (y, z): back foot -> front rail
B_FOOT, B_TOP = (0.0, -9.5), (34.0, 14.5)      # front foot -> back rail


def rod(side, foot, top):
    return (side * FX, foot[0], foot[1]), (side * FX, top[0], top[1])


def cross_pt():
    (y0, z0), (y1, z1) = A_FOOT, A_TOP
    (y2, z2), (y3, z3) = B_FOOT, B_TOP
    # solve A(t) = B(s) in the (y, z) plane
    a11, a12, b1 = y1 - y0, -(y3 - y2), y2 - y0
    a21, a22, b2 = z1 - z0, -(z3 - z2), z2 - z0
    det = a11 * a22 - a12 * a21
    t = (b1 * a22 - a12 * b2) / det
    return y0 + (y1 - y0) * t, z0 + (z1 - z0) * t


PIV = cross_pt()

# shadow from the four feet
feet = [P(sx * FX, 0, z) for sx in (-1, 1) for z in (A_FOOT[1], B_FOOT[1])]
fx0, fx1 = min(p[0] for p in feet) - 34, max(p[0] for p in feet) + 34
fy0, fy1 = min(p[1] for p in feet) - 22, max(p[1] for p in feet) + 24
d.shape("ellipse", "Chair shadow", x=round(fx0), y=round(fy0), width=round(fx1 - fx0),
        height=round(fy1 - fy0),
        fill=rad((0, "#05070A", 66), (0.6, "#05070A", 30), (1, "#05070A", 0)), stroke=NONE)
for t in range(0, 360, 10):
    ex = (fx0 + fx1) / 2 + (fx1 - fx0) / 2 * math.cos(math.radians(t))
    ey = (fy0 + fy1) / 2 + (fy1 - fy0) / 2 * math.sin(math.radians(t))
    assert on_disc(ex, ey, 10), (ex, ey)


# --- sling surface ------------------------------------------------------------------------
def sling(u, xf):
    sn = math.sin(math.pi * u)
    xe = 10.3 - 0.8 * sn                     # free side hems pull inward under load
    y = A_TOP[0] + 0.55 + (B_TOP[0] - A_TOP[0]) * u - 14.5 * sn ** 0.9 - 1.2 * (1 - xf * xf) * sn
    z = A_TOP[1] + (B_TOP[1] - A_TOP[1]) * u + 2.2 * sn
    return (xf * xe, y, z)


NU, NXF = 40, 9
US = [i / NU for i in range(NU + 1)]
XFS = [-1 + 2 * j / (NXF - 1) for j in range(NXF)]


def fold_u(xf):
    """Where the fabric turns edge-on: the lowest screen point along u."""
    best = max(US, key=lambda u: P(*sling(u, xf))[1])
    return best


FOLD = [fold_u(xf) for xf in XFS]

# --- far side of the frame, rails ---------------------------------------------------------
far_a, far_b = rod(-1, A_FOOT, A_TOP), rod(-1, B_FOOT, B_TOP)
tube("Far rod A", *far_a)
tube("Far rod B", *far_b)
bolt("Far pivot", (-FX - 0.4, PIV[0], PIV[1]))
tube("Back foot rail", (-FX, 0.35, A_FOOT[1]), (FX, 0.35, A_FOOT[1]))
tube("Back rail", (-FX - 0.3, B_TOP[0], B_TOP[1]), (FX + 0.3, B_TOP[0], B_TOP[1]), r=0.42)
tube("Front rail", (-FX - 0.3, A_TOP[0], A_TOP[1]), (FX + 0.3, A_TOP[0], A_TOP[1]), r=0.42)

# --- sling: inner face first, then the front fall's outer face over it -------------------
inner = [P(*sling(u, -1)) for u in US] + [P(*sling(1, xf)) for xf in XFS[1:]] + \
        [P(*sling(u, 1)) for u in US[::-1]] + [P(*sling(0, xf)) for xf in XFS[::-1][1:]]
hi_y = min(p[1] for p in inner)
lo_y = max(p[1] for p in inner)
d.path(poly(inner), "Sling inner face",
       fill=lin((0, hi_y), (0, lo_y), (0, "#F0A06A"), (0.45, "#D06A34"), (1, "#8A3414")),
       stroke="#4A1A08", strokeWidth=2, join="round")

# lambert strips: darken where the cloth turns from the light
LIGHT = (-0.35, 0.75, -0.55)
ln_ = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / ln_ for c in LIGHT)
for i in range(NU):
    u0, u1 = US[i], US[i + 1]
    a0, a1 = sling(u0, 0), sling(u1, 0)
    dy, dz = a1[1] - a0[1], a1[2] - a0[2]
    L = math.hypot(dy, dz)
    n = (0, dz / L, -dy / L)
    lam = sum(n[k] * LIGHT[k] for k in range(3))
    strip = [P(*sling(u0, xf)) for xf in XFS] + [P(*sling(u1, xf)) for xf in XFS[::-1]]
    if lam < 0.55:
        d.path(poly(strip), f"Sling shade {i+1}", fill="#3A1206",
               opacity=round(min(48, (0.55 - lam) * 70)), stroke=NONE)
    elif lam > 0.75:
        d.path(poly(strip), f"Sling light {i+1}", fill="#FFD6B0",
               opacity=round(min(26, (lam - 0.75) * 110)), stroke=NONE)

# canvas weave: faint warp threads along the hang
for j, xf in enumerate([-0.66, -0.33, 0.0, 0.33, 0.66]):
    th = [P(*sling(u, xf)) for u in US[2:-2]]
    d.path(smooth(th), f"Warp thread {j+1}", fill=NONE, stroke="#FFE2C8", strokeWidth=1.4, opacity=14)
# tension folds from the back rail corners into the seat
for side in (-1, 1):
    fold = [P(*sling(u, side * (0.92 - 0.9 * (1 - u) ** 1.4))) for u in [0.92 - 0.06 * k for k in range(9)]]
    d.path(smooth(fold), f"Tension fold {'L' if side < 0 else 'R'}", fill=NONE, stroke="#5A1E0A",
           strokeWidth=3, opacity=28, cap="round")
# side hems: a darker doubled edge
for side, nm in ((-1, "L"), (1, "R")):
    hem = [P(*sling(u, side * 0.96)) for u in US[1:-1]]
    d.path(smooth(hem), f"Side hem {nm}", fill=NONE, stroke="#7A2C10", strokeWidth=3, opacity=50,
           cap="round")

# back hem seam: the one visible stitch line, where the pocket round the back rail is sewn
seam_u = 0.93
seam = [P(*sling(seam_u, xf * 0.94)) for xf in [-1 + 2 * k / 16 for k in range(17)]]
d.path(smooth(seam), "Back hem fold", fill=NONE, stroke="#5A1E0A", strokeWidth=2.4, opacity=55)
d.path(smooth([(x, y + 3) for x, y in seam]), "Back hem seam", fill=NONE, stroke="#FFE4C4",
       strokeWidth=1.8, opacity=80, dash=[5, 4], cap="round")

# outer face of the front fall, from the front rail down to the fold line
front = [P(*sling(u, -1)) for u in US if u <= FOLD[0]]
front += [P(*sling(FOLD[j], xf)) for j, xf in enumerate(XFS)][1:-1]
front += [P(*sling(u, 1)) for u in US[::-1] if u <= FOLD[-1]]
front += [P(*sling(0, xf)) for xf in XFS[::-1][1:]]
fy_hi = min(p[1] for p in front)
fy_lo = max(p[1] for p in front)
d.path(poly(front), "Sling front fall",
       fill=lin((0, fy_hi), (0, fy_lo), (0, "#B4542A"), (0.6, "#8A3616"), (1, "#5A200A")),
       stroke="#4A1A08", strokeWidth=2, join="round")
d.path(smooth([P(*sling(FOLD[j], xf)) for j, xf in enumerate(XFS)][1:-1]), "Fold edge light",
       fill=NONE, stroke="#F4A878", strokeWidth=2.4, opacity=45, cap="round")

# fabric wrapped over each rail
for nm, (ry, rz), r in (("Front", A_TOP, 0.42), ("Back", B_TOP, 0.42)):
    # canvas pocket round the rail: a soft capsule a little fatter than the tube
    w = (r + 0.16) * S
    a, b = tube(f"{nm} rail wrap", (-10.0, ry, rz), (10.0, ry, rz), r=r + 0.16, ink=2,
                grad=((0, "#7A3012"), (0.3, "#F4AE7C"), (0.6, "#C8602C"), (1, "#5A200A")),
                ink_col="#4A1A08")
    d.path(f"M{a[0]:.1f},{a[1] - w * 0.35:.1f} L{b[0]:.1f},{b[1] - w * 0.35:.1f}", f"{nm} wrap sheen",
           fill=NONE, stroke="#FFE0C4", strokeWidth=2.2, opacity=45, cap="round")

# --- near side of the frame ------------------------------------------------------------
tube("Front foot rail", (-FX, 0.35, B_FOOT[1]), (FX, 0.35, B_FOOT[1]))
near_a, near_b = rod(1, A_FOOT, A_TOP), rod(1, B_FOOT, B_TOP)
tube("Near rod A", *near_a)
tube("Near rod B", *near_b)
bolt("Near pivot", (FX + 0.4, PIV[0], PIV[1]))
for nm, p in (("rail L", (-FX - 0.3, A_TOP[0], A_TOP[1])), ("rail R", (FX + 0.3, A_TOP[0], A_TOP[1])),
              ("back L", (-FX - 0.3, B_TOP[0], B_TOP[1])), ("back R", (FX + 0.3, B_TOP[0], B_TOP[1]))):
    x, y = P(*p)
    d.shape("ellipse", f"Rail cap {nm}", x=round(x - 5), y=round(y - 5), width=10, height=10,
            fill=rad((0, "#F4F8FC"), (1, "#5A626C")), stroke=INK, strokeWidth=1.2)
for sx in (-1, 1):
    for z in (A_FOOT[1], B_FOOT[1]):
        x, y = P(sx * FX, 0, z)
        d.shape("ellipse", f"Foot shadow {sx}{z}", x=round(x - 14), y=round(y - 3), width=28, height=8,
                fill=rad((0, "#000000", 55), (1, "#000000", 0)), stroke=NONE)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 30, far


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
               color="#F0E4DA", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#B8A49A", justify="center")
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


caption("SLING CHAIR", "CHROMED STEEL · CANVAS · BRASS")
d.finish("sling-chair-V1R00")
