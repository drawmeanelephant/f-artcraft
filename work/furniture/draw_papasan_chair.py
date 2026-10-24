#!/usr/bin/env python3
"""Papasan chair — furniture field plate V1R00. Three-quarter from the front
right: a big tilted rattan bowl nested in a small splayed-slat base, its huge
tufted cushion puffing inside the rim. Dorm mood: warm amber lamp light low
in the left corner. 1000x1000.
Modelled in inches (x right, y up, +z back), fixed yaw + pitch projection;
the bowl is a paraboloid shell in a plane tilted toward the viewer.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Papasan Chair — Field Plate", 1000, 1000)

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
YAW, PITCH = math.radians(24), math.radians(17)
S, OX, OY = 13.0, 500.0, 762.0
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


RATTAN_HI, RATTAN_MID, RATTAN_LO = "#DDB06A", "#A67C40", "#5E3E18"
RATTAN = ((0, RATTAN_LO), (0.3, RATTAN_MID), (0.52, RATTAN_HI),
          (0.74, RATTAN_MID), (1, "#46300F"))


def bar(name, a, b, r=0.5, grad=RATTAN, ink=1.8):
    """Capsule member between two 3D points, lit across its width."""
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
    d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    assert 2 * w >= 3, "member must stay >= 3pt"
    return A, B


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1C1418"), (1, "#080608")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8A6A4A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#4C3A38"), (0.6, "#332624"), (1, "#140E0E")),
        stroke="#0C0808", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8CCA8", strokeWidth=3, opacity=20)
# dorm mood: a warm lamp glow pooled low-left
d.shape("ellipse", "Lamp glow", x=80, y=430, width=520, height=430,
        fill=rad((0, "#E8A44E", 0.24), (0.5, "#B4743A", 0.09), (1, "#B4743A", 0)),
        stroke=NONE)

FY = 706
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4E3A30", 40), (1, "#120A08", 75)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#F0CCA0", strokeWidth=2, opacity=16)

# --- geometry --------------------------------------------------------------------------
# bowl: rim circle in a plane tilted TILT from vertical toward the viewer (-z)
TILT = math.radians(38)
AX = (0.0, math.cos(TILT), -math.sin(TILT))      # bowl axis: up + forward
U1 = (1.0, 0.0, 0.0)                            # rim-plane basis: across
U2 = (0.0, -math.sin(TILT), -math.cos(TILT))    # rim-plane basis: down + forward
RC = (0.0, 25.5, -1.0)                          # rim centre
RR = 17.6                                       # rim radius
BOWLD = 18.0                                    # shell depth along -AX
BASE_C = (0.0, 0.0, 11.0)                       # base plan centre (under the belly)
RTOP, RBOT = 8.8, 10.6                          # base ring radii
YTOP, YBOT = 13.2, 1.1


def tilt_pt(u, v, lift=0.0):
    """u along U1, v along U2 in the rim plane; lift along the bowl axis."""
    return (RC[0] + u * U1[0] + v * U2[0] + lift * AX[0],
            RC[1] + u * U1[1] + v * U2[1] + lift * AX[1],
            RC[2] + u * U1[2] + v * U2[2] + lift * AX[2])


def shell_pt(t, k):
    """Point on the bowl shell: rim-angle t, radius fraction k (paraboloid)."""
    return tilt_pt(k * RR * math.cos(t), k * RR * math.sin(t),
                   -BOWLD * (1 - k * k))


def rim_arc(k, t0, t1, n=26, lift=0.0):
    return [P(*tilt_pt(k * RR * math.cos(t0 + (t1 - t0) * i / n),
                       k * RR * math.sin(t0 + (t1 - t0) * i / n), lift))
            for i in range(n + 1)]


def shell_arc(t0, t1, k, n=26):
    return [P(*shell_pt(t0 + (t1 - t0) * i / n, k)) for i in range(n + 1)]


def ring_pts(cx, cz, y, r, a0=0.0, a1=2 * math.pi, n=40):
    return [P(cx + r * math.cos(a0 + (a1 - a0) * i / n), y,
              cz + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


# grounding shadow under the base
sp = [P(BASE_C[0] + x, 0, BASE_C[2] + z)
      for x, z in ((-13, -13), (13, -13), (13, 13), (-13, 13))]
sx0, sx1 = min(p[0] for p in sp) - 30, max(p[0] for p in sp) + 30
sy0, sy1 = min(p[1] for p in sp) - 12, max(p[1] for p in sp) + 16
d.shape("ellipse", "Chair shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#040202", 68), (0.6, "#040202", 30), (1, "#040202", 0)),
        stroke=NONE)

# --- base: slatted drum, far half first ---------------------------------------------
for nm, r, y in (("Bottom ring far", RBOT, YBOT), ("Top ring far", RTOP, YTOP)):
    pts = ring_pts(BASE_C[0], BASE_C[2], y, r, math.radians(20), math.radians(160), 26)
    d.path(smooth(pts, closed=False), nm, fill=NONE, stroke="#8A6434",
           strokeWidth=5, opacity=85, cap="round")
# slats, far half (sin a > 0 sits toward +z/back)
slats = []
NROD = 18
for i in range(NROD):
    a = 2 * math.pi * i / NROD
    bx, bz = BASE_C[0] + RBOT * math.cos(a), BASE_C[2] + RBOT * math.sin(a)
    tx, tz = BASE_C[0] + RTOP * math.cos(a), BASE_C[2] + RTOP * math.sin(a)
    slats.append((depth((bx + tx) / 2, (YBOT + YTOP) / 2, (bz + tz) / 2), a,
                  (bx, YBOT, bz), (tx, YTOP, tz)))
for dep, a, b_, t_ in sorted(s_ for s_ in slats if math.sin(s_[1]) > 0.05):
    bar(f"Slat far {a:.2f}", b_, t_, r=0.34, ink=1.5)

# cane wrap band between the rings, far arc
wrap = (ring_pts(BASE_C[0], BASE_C[2], 6.6, 9.9, math.radians(15), math.radians(165), 24) +
        ring_pts(BASE_C[0], BASE_C[2], 8.0, 9.7, math.radians(165), math.radians(15), 24))
d.path(poly(wrap), "Wrap band far", fill="#3A2812", opacity=55, stroke=NONE)

# --- bowl shell: exterior below the rim ----------------------------------------------
# band: rim front arc (t 0..pi) down to the equator ring — poly, not smooth:
# the two ends are real corners, and Catmull-Rom overshoot spikes them.
band = shell_arc(0, math.pi, 1.0, 30) + shell_arc(math.pi, 0, 0.5, 30)
sh_y0 = min(p[1] for p in band)
sh_y1 = max(p[1] for p in band)
d.path(poly(band), "Bowl shell",
       fill=lin((sh_y0 - 40, sh_y0), (sh_y1, sh_y1 + 30),
                (0, RATTAN_HI), (0.45, RATTAN_MID), (1, "#4A3012")),
       stroke=INK, strokeWidth=2.2, join="round")
# belly disc closing the shell below the equator
nub = shell_arc(0, 2 * math.pi, 0.5, 36)
d.path(smooth(nub), "Bowl belly", fill=rad((0, "#96682E"), (0.6, "#684520"),
        (1, "#4A3012")), stroke=INK, strokeWidth=2.0)
# weave: latitude arcs on the visible shell
for i, k in enumerate((0.86, 0.72, 0.58)):
    pts = shell_arc(math.radians(4), math.radians(176), k, 24)
    d.path(smooth(pts, closed=False), f"Weave lat {i+1}", fill=NONE,
           stroke="#3A240C", strokeWidth=2.2, opacity=40, cap="round")
# weave: spokes converging on the belly
for i in range(9):
    t = math.radians(8 + 164 * i / 8)
    pts = [P(*shell_pt(t, k)) for k in [0.98 - 0.44 * j / 7 for j in range(8)]]
    d.path(smooth(pts, closed=False), f"Weave spoke {i+1}", fill=NONE,
           stroke="#4A3012", strokeWidth=2.0, opacity=30, cap="round")

# rim torus: full ellipse band — the rattan ring the cushion sits inside
rim_band = rim_arc(1.0, 0, 2 * math.pi, 48) + rim_arc(0.88, 2 * math.pi, 0, 48)
d.path(smooth(rim_band), "Rim", fill=lin((0, min(p[1] for p in rim_band)),
        (0, max(p[1] for p in rim_band)),
        (0, "#8A6434"), (0.4, RATTAN_HI), (0.7, RATTAN_MID), (1, RATTAN_LO)),
        stroke=INK, strokeWidth=2.2)
# rim wrap hints: short strokes across the band at intervals
for i in range(14):
    t = 2 * math.pi * i / 14 + 0.12
    p0 = P(*tilt_pt(0.9 * RR * math.cos(t), 0.9 * RR * math.sin(t)))
    p1 = P(*tilt_pt(1.0 * RR * math.cos(t), 1.0 * RR * math.sin(t)))
    d.path(f"M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}",
           f"Rim wrap {i+1}", fill=NONE, stroke="#3A240C", strokeWidth=1.8,
           opacity=35)

# bowl interior wall: a crescent of inside shell between rim and cushion
wall = shell_arc(math.pi, 2 * math.pi, 0.94, 26) + shell_arc(2 * math.pi, math.pi, 0.74, 26)
d.path(poly(wall), "Interior wall", fill=lin((0, min(p[1] for p in wall)),
        (0, max(p[1] for p in wall)), (0, "#3A2410"), (1, "#5E3E18")),
        stroke=NONE)

# --- cushion: tufted disc puffing out of the bowl --------------------------------------
CR = 15.4


def cush_edge(t):
    """Squishy pillow silhouette: slight droop toward the front lip."""
    overhang = 0.045 * max(0.0, math.sin(t)) ** 2
    lump = 0.016 * math.sin(7 * t + 1.2) + 0.011 * math.sin(3 * t - 0.6)
    return CR * (1 + overhang + lump)


cpts = [P(*tilt_pt(cush_edge(t) * math.cos(t), cush_edge(t) * math.sin(t), 2.2))
        for t in [2 * math.pi * i / 56 for i in range(56)]]
cx0 = min(p[0] for p in cpts)
cx1 = max(p[0] for p in cpts)
cy0 = min(p[1] for p in cpts)
cy1 = max(p[1] for p in cpts)
d.path(smooth(cpts), "Cushion",
       fill={"gradient": {"kind": "radial",
                          "center": [round((cx0 + cx1) / 2 - 55, 1),
                                     round(cy0 + (cy1 - cy0) * 0.28, 1)],
                          "stops": stops((0, "#E8B96A"), (0.45, "#C89050"),
                                         (0.78, "#96642E"), (1, "#6E4520"))}},
       stroke=INK, strokeWidth=2.6, join="round")
# soft pad of lamp light on the upper face
d.path(smooth([P(*tilt_pt(u, v, 2.6)) for u, v in
               [(-12, -4), (-6, -9), (2, -8), (8, -3), (5, 1), (-6, 2)]]),
       "Cushion sheen", fill="#FFE8B8", opacity=11, stroke=NONE)
# welt piping just inside the edge
wpts = [P(*tilt_pt((cush_edge(t) * 0.925) * math.cos(t),
                   (cush_edge(t) * 0.925) * math.sin(t), 2.35))
        for t in [2 * math.pi * i / 52 for i in range(52)]]
d.path(smooth(wpts), "Cushion welt", fill=NONE, stroke="#5E3E18",
      strokeWidth=2.4, opacity=55)

# tuft buttons: centre + ring of 8, each a dimple with a crease pull
BTN = [(0.0, 0.0)] + [(0.48 * CR * math.cos(2 * math.pi * i / 8 + 0.4),
                       0.48 * CR * math.sin(2 * math.pi * i / 8 + 0.4))
                      for i in range(8)]
for i, (bu, bv) in enumerate(BTN):
    bx, by = P(*tilt_pt(bu, bv, 2.9))
    d.shape("ellipse", f"Button shadow {i+1}", x=round(bx - 5.2), y=round(by - 3.6),
            width=11, height=8, fill="#3A2008", opacity=55, stroke=NONE)
    d.shape("ellipse", f"Button {i+1}", x=round(bx - 4.2), y=round(by - 5.4),
            width=9, height=7, fill=rad((0, "#E8B96A"), (1, "#96642E")),
            stroke=INK, strokeWidth=1.4)
    for j, dt in enumerate((-0.5, 0.5)):
        rr = math.hypot(bu, bv)
        tt = math.atan2(bv, bu) + dt
        c0 = P(*tilt_pt((rr + 0.6) * math.cos(tt), (rr + 0.6) * math.sin(tt), 2.7))
        c1 = P(*tilt_pt((rr + 2.4) * math.cos(tt), (rr + 2.4) * math.sin(tt), 2.6))
        d.path(f"M{c0[0]:.1f},{c0[1]:.1f} L{c1[0]:.1f},{c1[1]:.1f}",
               f"Crease {i+1}.{j+1}", fill=NONE, stroke="#5E3E18",
               strokeWidth=1.6, opacity=26, cap="round")
# fabric bunching where the cushion presses the front rim
for i, t in enumerate((math.radians(58), math.radians(76), math.radians(94),
                       math.radians(112), math.radians(130))):
    b0 = P(*tilt_pt(0.99 * CR * math.cos(t), 0.99 * CR * math.sin(t), 2.0))
    b1 = P(*tilt_pt(0.86 * CR * math.cos(t), 0.86 * CR * math.sin(t), 2.4))
    d.path(f"M{b0[0]:.1f},{b0[1]:.1f} L{b1[0]:.1f},{b1[1]:.1f}",
           f"Bunch {i+1}", fill=NONE, stroke="#4A2A0E", strokeWidth=2.0,
           opacity=32, cap="round")

# --- base: near half over the bowl belly ---------------------------------------------
for dep, a, b_, t_ in sorted(s_ for s_ in slats if math.sin(s_[1]) <= 0.05):
    bar(f"Slat near {a:.2f}", b_, t_, r=0.34, ink=1.5)
for nm, r, y in (("Bottom ring near", RBOT, YBOT), ("Top ring near", RTOP, YTOP)):
    pts = ring_pts(BASE_C[0], BASE_C[2], y, r, math.radians(160), math.radians(380), 30)
    d.path(smooth(pts, closed=False), nm, fill=NONE, stroke=RATTAN_MID,
           strokeWidth=5, cap="round")
    pts_in = ring_pts(BASE_C[0], BASE_C[2], y, r - 0.55, math.radians(160),
                      math.radians(380), 30)
    d.path(smooth(pts_in, closed=False), f"{nm} inner", fill=NONE,
           stroke="#3A240C", strokeWidth=1.8, opacity=60)
# cane wrap band, near arc
wrap_n = (ring_pts(BASE_C[0], BASE_C[2], 6.6, 9.9, math.radians(175),
                   math.radians(365), 22) +
          ring_pts(BASE_C[0], BASE_C[2], 8.0, 9.7, math.radians(365),
                   math.radians(175), 22))
d.path(poly(wrap_n), "Wrap band near",
       fill=lin((0, min(p[1] for p in wrap_n)), (0, max(p[1] for p in wrap_n)),
                (0, "#8A6434"), (1, "#4A3012")),
       stroke=INK, strokeWidth=1.4)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F4E4C4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C8A884", justify="center")
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


caption("PAPASAN CHAIR", "RATTAN · COTTON · FOAM")
d.finish("papasan-chair-V1R00")
