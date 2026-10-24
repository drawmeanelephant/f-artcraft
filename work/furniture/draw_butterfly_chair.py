#!/usr/bin/env python3
"""Butterfly chair — furniture field plate V1R00. Near-side three-quarter of
a BKF-type folding chair: two black-iron rod Xs joined by low spreader bars,
a cognac leather cover hung from the four rod tips — its top hem draping in
a deep catenary between the high back ears, the front ears wider and lower.
Canvas plate, mid-century mood. 1000x1000.
Modelled in 3D (inches) and projected with a fixed yaw + pitch.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Butterfly Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241812"   # warm dark, not black
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
YAW, PITCH = math.radians(34), math.radians(26)
S, OX, OY = 12.0, 500.0, 764.0


def P(x, y, z):
    c, s = math.cos(YAW), math.sin(YAW)
    xr, zr = x * c + z * s, -x * s + z * c
    p = (OX + S * xr, OY - S * (y * math.cos(PITCH) + zr * math.sin(PITCH)))
    EXTENT.append(p)
    return p


IRON = ((0, "#4E565C"), (0.25, "#8A929A"), (0.42, "#3A4046"), (0.62, "#22262A"),
        (0.8, "#565E66"), (1, "#181C20"))


def tube(name, a, b, r=0.30, ink=1.8, grad=IRON, ink_col=INK):
    """Iron rod between 3D points with rounded ends, lit across its width."""
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
    assert 2 * w >= 3, "rod must stay >= 3pt"
    return A, B


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#181510"), (1, "#080705")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7A6E54", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#6E6248"), (0.6, "#4A4230"), (1, "#26211A")),
        stroke="#12100B", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8CCB0", strokeWidth=3, opacity=25)
d.shape("ellipse", "Back glow", x=220, y=150, width=540, height=540,
        fill=rad((0, "#F0B878", 18), (0.6, "#A87848", 6), (1, "#6E4C30", 0)), stroke=NONE)

FY = 690
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#685C46", 34), (1, "#16130D", 72)), stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E4D8BC", strokeWidth=2, opacity=20)

# --- frame geometry (inches) ----------------------------------------------------------
# each side: rod A front-foot -> back-top tip; rod B back-foot -> front-top tip
# front ears splay wider than the back ears, as on the real frame
FX = 10.6
A_FOOT = (10.4, 0.0, 11.0)                   # (x, y, z) front foot
A_TIP = (10.0, 33.5, -7.0)                   # back ear (rod A's top)
B_FOOT = (11.4, 0.0, -11.0)                  # back foot
B_TIP = (11.9, 23.0, 9.0)                   # front ear (rod B's top)


def cross_pt():
    (y0, z0), (y1, z1) = A_FOOT[1:], A_TIP[1:]
    (y2, z2), (y3, z3) = B_FOOT[1:], B_TIP[1:]
    a11, a12, b1 = y1 - y0, -(y3 - y2), y2 - y0
    a21, a22, b2 = z1 - z0, -(z3 - z2), z2 - z0
    det = a11 * a22 - a12 * a21
    t = (b1 * a22 - a12 * b2) / det
    return y0 + (y1 - y0) * t, z0 + (z1 - z0) * t


PIV = cross_pt()

# shadow from the four feet
feet = [P(-A_FOOT[0], 0, A_FOOT[2]), P(A_FOOT[0], 0, A_FOOT[2]),
        P(-B_FOOT[0], 0, B_FOOT[2]), P(B_FOOT[0], 0, B_FOOT[2])]
fx0, fx1 = min(p[0] for p in feet) - 40, max(p[0] for p in feet) + 40
fy0, fy1 = min(p[1] for p in feet) - 20, max(p[1] for p in feet) + 26
d.shape("ellipse", "Chair shadow", x=round(fx0), y=round(fy0), width=round(fx1 - fx0),
        height=round(fy1 - fy0),
        fill=rad((0, "#050403", 66), (0.6, "#050403", 30), (1, "#050403", 0)), stroke=NONE)

# --- far frame: rods, spreaders, pivot --------------------------------------------------
tube("Far rod A", (-A_FOOT[0], A_FOOT[1], A_FOOT[2]), (-A_TIP[0], A_TIP[1], A_TIP[2]))
tube("Far rod B", (-B_FOOT[0], B_FOOT[1], B_FOOT[2]), (-B_TIP[0], B_TIP[1], B_TIP[2]))
tube("Front spreader", (-A_FOOT[0] - 0.4, 2.6, A_FOOT[2] - 1.5),
     (A_FOOT[0] + 0.4, 2.6, A_FOOT[2] - 1.5), r=0.26)
tube("Back spreader", (-B_FOOT[0] - 0.4, 2.6, B_FOOT[2] + 1.5),
     (B_FOOT[0] + 0.4, 2.6, B_FOOT[2] + 1.5), r=0.26)


# --- leather sling surface -------------------------------------------------------------
# cover(u, xf): u 0 at back ears -> 1 at front ears, xf -1..1 across.
# hems dip between their own two ears; the bowl sinks between them.
def cover(u, xf):
    edge_dip = 3.2 * (1 - xf * xf) ** 0.8 * math.exp(-(u / 0.38) ** 2) \
             + 4.2 * (1 - xf * xf) ** 0.9 * math.exp(-((u - 1) / 0.32) ** 2)
    bowl = 11.5 * math.sin(math.pi * min(1.0, u * 1.04)) ** 1.1 * (1 - 0.45 * xf * xf)
    y = 33.5 + (23.0 - 33.5) * u - edge_dip - bowl
    z = A_TIP[2] + (B_TIP[2] - A_TIP[2]) * u ** 2.6 - 0.8 * math.sin(math.pi * u)
    half = (A_TIP[0] + (B_TIP[0] - A_TIP[0]) * u) * (1 - 0.08 * math.sin(math.pi * u))
    return (xf * half, y, z)


NU, NXF = 36, 9
US = [i / NU for i in range(NU + 1)]
XFS = [-1 + 2 * j / (NXF - 1) for j in range(NXF)]

skin = [P(*cover(u, -1)) for u in US] + [P(*cover(1, xf)) for xf in XFS[1:]] + \
       [P(*cover(u, 1)) for u in US[::-1]] + [P(*cover(0, xf)) for xf in XFS[::-1][1:]]
hi_y = min(p[1] for p in skin)
lo_y = max(p[1] for p in skin)
d.path(poly(skin), "Sling",
       fill=lin((0, hi_y), (0, lo_y), (0, "#D89A5C"), (0.4, "#B47844"), (0.75, "#8A5428"), (1, "#6E3C1A")),
       stroke="#3A1E0A", strokeWidth=2.5, join="round")

# lambert strips: shade where the hide turns from the light
LIGHT = (-0.35, 0.8, -0.5)
ln_ = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / ln_ for c in LIGHT)
for i in range(NU):
    u0, u1 = US[i], US[i + 1]
    a0, a1 = cover(u0, 0), cover(u1, 0)
    dy, dz = a1[1] - a0[1], a1[2] - a0[2]
    L = math.hypot(dy, dz)
    n = (0, dz / L, -dy / L)
    lam = sum(n[k] * LIGHT[k] for k in range(3))
    strip = [P(*cover(u0, xf)) for xf in XFS] + [P(*cover(u1, xf)) for xf in XFS[::-1]]
    if lam < 0.35:
        d.path(poly(strip), f"Sling shade {i+1}", fill="#2E1404",
               opacity=round(min(38, (0.35 - lam) * 70)), stroke=NONE)
    elif lam > 0.72:
        d.path(poly(strip), f"Sling light {i+1}", fill="#FFD8AC",
               opacity=round(min(32, (lam - 0.72) * 110)), stroke=NONE)

# bowl catch-light: the seat pocket faces up into the light
bx_, by_ = P(0, 33.5 + (23.0 - 33.5) * 0.52 - 9.0, A_TIP[2] + (B_TIP[2] - A_TIP[2]) * 0.52)
d.shape("ellipse", "Bowl light", x=round(bx_ - 120), y=round(by_ - 66), width=240, height=132,
        fill=rad((0, "#F0B878", 34), (0.7, "#C08048", 12), (1, "#C08048", 0)), stroke=NONE)

# grain creases radiating from the seat bowl toward the ears
for xf0, nm in [(-0.55, "L"), (-0.25, "Lm"), (0.25, "Rm"), (0.55, "R")]:
    crease = [P(*cover(u, xf0 + 0.35 * (1 - u) * (1 if xf0 < 0 else -1))) for u in
              [0.18, 0.32, 0.48, 0.62]]
    d.path(smooth(crease), f"Hide crease {nm}", fill=NONE, stroke="#4E2810",
           strokeWidth=3, opacity=34, cap="round")
# edge hems: doubled leather along both free sides + the draped hems
for side, nm in ((-1, "L"), (1, "R")):
    hem = [P(*cover(u, side * 0.985)) for u in US[1:-1]]
    d.path(smooth(hem), f"Side hem {nm}", fill=NONE, stroke="#3A1E0A",
           strokeWidth=3.5, opacity=55, cap="round")
for u_end, nm, wu in ((0, "Back", 0.965), (1, "Front", 0.97)):
    hem = [P(*cover(u_end, xf * wu)) for xf in [-1 + 2 * k / 20 for k in range(21)]]
    d.path(smooth(hem), f"{nm} hem", fill=NONE, stroke="#3A1E0A",
           strokeWidth=3.5, opacity=60, cap="round")
    d.path(smooth([(x, y - 3.5) for x, y in hem]), f"{nm} hem light", fill=NONE,
           stroke="#F4C894", strokeWidth=2, opacity=45, cap="round")

# corner pockets: the folded sleeves the rod tips thread through
for sx, tip, nm in ((-1, A_TIP, "back L"), (1, A_TIP, "back R"),
                    (-1, B_TIP, "front L"), (1, B_TIP, "front R")):
    x, y = P(sx * tip[0], tip[1], tip[2])
    d.shape("ellipse", f"Pocket {nm}", x=round(x - 13), y=round(y - 9), width=26, height=18,
            fill=rad((0, "#B87C44"), (0.6, "#8A5424"), (1, "#4E2810")),
            stroke="#3A1E0A", strokeWidth=2)

# --- near frame over the leather ------------------------------------------------------
tube("Near rod B", B_FOOT, B_TIP)
tube("Near rod A", A_FOOT, A_TIP)
# rod tips standing proud of the pockets
for sx, tip, nm in ((1, A_TIP, "near back"), (-1, A_TIP, "far back"),
                    (1, B_TIP, "near front"), (-1, B_TIP, "far front")):
    tube(f"Tip {nm}", (sx * tip[0], tip[1] + 0.4, tip[2]),
         (sx * tip[0], tip[1] + 2.0, tip[2]), r=0.30)
# pivots
for sx, nm in ((-1, "far"), (1, "near")):
    x, y = P(sx * (FX + 0.35), PIV[0], PIV[1])
    d.shape("ellipse", f"Pivot {nm}", x=round(x - 6.5), y=round(y - 6.5), width=13, height=13,
            fill=rad((0, "#9AA2AC"), (0.6, "#4A525A"), (1, "#1E2226")),
            stroke=INK, strokeWidth=1.5)
# feet caps + contact shadows
for sx in (-1, 1):
    for foot in (A_FOOT, B_FOOT):
        x, y = P(sx * foot[0], 0, foot[2])
        d.shape("ellipse", f"Foot shadow {sx}{foot[2]}", x=round(x - 13), y=round(y - 2), width=26, height=7,
                fill=rad((0, "#000000", 55), (1, "#000000", 0)), stroke=NONE)
        d.shape("ellipse", f"Foot cap {sx}{foot[2]}", x=round(x - 4), y=round(y - 5), width=8, height=6,
                fill=rad((0, "#6E767E"), (1, "#22262A")), stroke=INK, strokeWidth=1.2)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("butterfly extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F4E8D4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C2B298", justify="center")
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


caption("BUTTERFLY CHAIR", "IRON · LEATHER")
d.finish("butterfly-chair-V1R00")
