#!/usr/bin/env python3
"""Folding screen — furniture field plate V1R00. Three-panel byōbu type in
near-side view with a slight three-quarter: black lacquer frames folded
into a shallow bay toward the viewer, deep red fields carrying a gold-leaf
scene that continues across the panels — a moon, drifting cloud bands and
grass tufts at the foot. Brass hinge barrels at the seams, bracket feet.
Lacquer plate, partition mood. 1000x1000. Modelled in inches
(x right, y up, +z back), projected with a fixed yaw + pitch; carcass
parts are 8-corner prisms culled by view normal.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Folding Screen — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#160C08"   # warm dark, not black
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


def ext(x, y):
    EXTENT.append((x, y))
    return (x, y)


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(28), math.radians(14)
S, OX, OY = 8.3, 512.0, 748.0
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
TO_VIEWER = (SY * CP, SP, -CY * CP)
LIGHT = (-0.30, 0.88, -0.36)
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


def prism(name, corners, ramp=("#160A06", "#5E2418"), lo=0.08, hi=0.94, sw=1.8):
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


# --- panel model -------------------------------------------------------------------
# a panel: bottom-left corner BL, width dir w (unit, in plan), decorated-face
# normal n (unit, in plan, pointing at the viewer side), slab thickness T
W, H, T = 22.0, 62.0, 1.1


def slab(BL, w, n, u0, u1, v0, v1, t0=0.0, t1=T):
    """8-corner box in panel coords, matching box() vertex order."""
    return [(BL[0] + w[0] * u + n[0] * t, v, BL[1] + w[1] * u + n[1] * t)
            for t in (t0, t1) for u, v in ((u0, v0), (u1, v0), (u1, v1), (u0, v1))]


def pface(BL, w, n, u, v):
    """Point on the decorated face: u along the width, v up from the floor."""
    return P(BL[0] + n[0] * T + w[0] * u, v,
             BL[1] + n[1] * T + w[1] * u)


PANELS = [
    # far-to-near draw order: right wing folds away back-right, centre panel,
    # then the left wing folded toward the viewer — the screen's S-zigzag
    dict(tag="Right", BL=(11.0, -0.2), w=(math.cos(math.radians(40)), math.sin(math.radians(40))),
         n=(math.sin(math.radians(40)), -math.cos(math.radians(40)))),
    dict(tag="Centre", BL=(-11.0, 0.6), w=(1.0, 0.0), n=(0.0, -1.0)),
    dict(tag="Left", BL=(-11.0, -0.2), w=(-math.cos(math.radians(40)), -math.sin(math.radians(40))),
         n=(math.sin(math.radians(40)), -math.cos(math.radians(40)))),
]

# --- backdrop + plate ------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1A0E0C"), (1, "#080404")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8A4A3A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5E382A"), (0.55, "#3A211A"), (1, "#180E0A")),
        stroke="#100804", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0C4A8", strokeWidth=3, opacity=24)

# floor: dark boards closing on the disc arc
FYB = 724
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX - hw:.1f},{FYB} L{PCX + hw:.1f},{FYB} A420,420 0 0 0 {PCX - hw:.1f},{FYB} Z",
       "Floor", fill=lin((0, FYB), (0, 880), (0, "#3E2A20", 0.5), (0.5, "#241812", 0.75),
                         (1, "#0E0805", 0.92)), stroke=NONE)
d.path(f"M{PCX - hw + 6:.1f},{FYB} L{PCX + hw - 6:.1f},{FYB}", "Floor edge light",
       fill=NONE, stroke="#C8A488", strokeWidth=2, opacity=16)
for i, yb in enumerate([764, 800, 836]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Board seam {i+1}",
           fill=NONE, stroke="#4E3424", strokeWidth=2, opacity=24)

# shadow under the whole screen
se = [P(-28, 0, -16), P(28, 0, -16), P(-28, 0, 2), P(28, 0, 2)]
sx0, sx1 = min(p[0] for p in se) - 20, max(p[0] for p in se) + 20
sy0, sy1 = min(p[1] for p in se) - 12, max(p[1] for p in se) + 16
d.shape("ellipse", "Screen shadow", x=round(sx0), y=round(sy0), width=round(sx1 - sx0),
        height=round(sy1 - sy0),
        fill=rad((0, "#040202", 0.62), (0.6, "#040202", 0.28), (1, "#040202", 0)),
        stroke=NONE)

LACQ = ("#140806", "#6E2E1E")        # black-red lacquer ramp
LACQ_HI = ("#1E0C08", "#8A4030")
FIELD = ((0, "#7E3222"), (0.45, "#5E2018"), (1, "#2E0F0C"))
GOLD = ((0, "#F4D98E"), (0.5, "#D8A94E"), (1, "#8A5E1E"))

for pn in PANELS:
    tag, BL, w, n = pn["tag"], pn["BL"], pn["w"], pn["n"]
    # feet under the slab, nosing out past the face
    for uu in (2.2, W - 3.6):
        prism(f"Foot {tag} {uu}", slab(BL, w, n, uu, uu + 1.4, 0, 1.6, -0.4, T * 1.5),
              ramp=LACQ, lo=0.05, hi=0.8, sw=1.4)
    # the panel slab
    prism(f"Panel {tag}", slab(BL, w, n, 0, W, 0, H), ramp=LACQ, lo=0.06, hi=0.9, sw=2.2)
    # top cap rail, slightly proud of the slab
    prism(f"Cap {tag}", slab(BL, w, n, -0.5, W + 0.5, H, H + 1.6, -0.3, T + 0.6),
          ramp=LACQ_HI, lo=0.1, hi=1.0, sw=1.8)
    # decorated field, inset from the frame edges
    FU, FV0, FV1 = 2.0, 2.6, H - 3.2
    fq = [pface(BL, w, n, uu, vv) for uu, vv in
          ((FU, FV0), (W - FU, FV0), (W - FU, FV1), (FU, FV1))]
    y0, y1 = min(p[1] for p in fq), max(p[1] for p in fq)
    d.path(poly(fq), f"Field {tag}",
           fill=lin((0, y1), (0, y0), *FIELD), stroke="#0E0604",
           strokeWidth=1.8, join="round")
    # thin gold keyline inside the field
    kq = [pface(BL, w, n, uu, vv) for uu, vv in
          ((FU + 0.9, FV0 + 0.9), (W - FU - 0.9, FV0 + 0.9),
           (W - FU - 0.9, FV1 - 0.9), (FU + 0.9, FV1 - 0.9))]
    d.path(poly(kq), f"Keyline {tag}", fill=NONE, stroke="#B8863A",
           strokeWidth=1.4, opacity=55, join="round")

# --- the gold-leaf scene, continuous across the three faces ----------------------------
def cloud(name, panel, u0, v0, w_):
    """Gold cloud band on one field: flat-bottomed blob with scalloped top."""
    BL, w, n = panel["BL"], panel["w"], panel["n"]
    uv = [(u0, v0), (u0 + w_ * 0.22, v0 + 2.6), (u0 + w_ * 0.38, v0 + 2.0),
          (u0 + w_ * 0.55, v0 + 3.4), (u0 + w_ * 0.72, v0 + 2.4),
          (u0 + w_ * 0.88, v0 + 3.0), (u0 + w_, v0 + 1.6), (u0 + w_, v0)]
    pts = [pface(BL, w, n, uu, vv) for uu, vv in uv]
    g0, g1 = min(p[1] for p in pts), max(p[1] for p in pts)
    d.path(smooth(pts, closed=True), name,
           fill=lin((0, g0), (0, g1), *GOLD), stroke="#3A2408",
           strokeWidth=1.6, opacity=92, join="round")


L, C, R = PANELS[2], PANELS[1], PANELS[0]
# moon on the centre face, upper left — a ring of field points
mc = [pface(C["BL"], C["w"], C["n"], 8.2 + 4.6 * math.cos(t),
            49 + 4.6 * math.sin(t)) for t in [2 * math.pi * k / 36 for k in range(36)]]
d.path(poly(mc), "Moon",
       fill=rad((0, "#F8E8B0"), (0.6, "#E8C878"), (1, "#C09038")),
       stroke="#4A3008", strokeWidth=1.6)
# cloud bands drifting across all three faces at matching heights
cloud("Cloud L1", L, 2.5, 47.5, 15)
cloud("Cloud C1", C, 4.0, 44.5, 16.5)
cloud("Cloud R1", R, 3.0, 46.5, 15)
cloud("Cloud L2", L, 4.5, 34.0, 13)
cloud("Cloud C2", C, 3.0, 31.5, 15)
cloud("Cloud R2", R, 5.0, 33.0, 12.5)
# grass tufts rising from the field bottoms
for pn, tufts in ((L, (4.5, 9.5, 15.5)), (C, (5.0, 11.0, 17.0)), (R, (5.0, 11.5, 16.5))):
    for j, uu in enumerate(tufts):
        for k in range(3):
            uu2 = uu + (k - 1) * 1.1
            top_v = 6.5 + ((j * 3 + k) % 4) * 2.6 + (0 if k == 1 else -1.5)
            uv = [(uu2, 3.2), (uu2 + (k - 1) * 0.7, 3.2 + top_v * 0.55),
                  (uu2 + (k - 1) * 1.8, 3.2 + top_v)]
            pts = [pface(pn["BL"], pn["w"], pn["n"], a, b) for a, b in uv]
            d.path(smooth(pts), f"Grass {pn['tag']} {j} {k}", fill=NONE,
                   stroke=("#C89A4A" if k == 1 else "#8A6428"),
                   strokeWidth=3.0, opacity=80, cap="round")

# two little birds high on the right face
for bi, (bu, bv, bs) in enumerate([(14.5, 54.5, 1.5), (17.5, 52.0, 1.1)]):
    for sgn in (-1, 1):
        pts = [pface(R["BL"], R["w"], R["n"], bu + sgn * t, bv + 0.5 * abs(t - bs))
               for t in (0, bs * 0.6, bs)]
        d.path(smooth(pts), f"Bird {bi+1} {sgn:+d}", fill=NONE, stroke="#3A2408",
               strokeWidth=2.4, opacity=70, cap="round")

# brass hinge barrels at the two seams
for si, (hx_, hz_) in enumerate(((-11.0, -0.6), (11.0, -0.6))):
    for hi, hv in enumerate((10.0, 30.0, 50.0)):
        hp = P(hx_, hv, hz_)
        d.shape("ellipse", f"Hinge {si+1}.{hi+1}", x=round(hp[0] - 4.5),
                y=round(hp[1] - 7), width=9, height=14,
                fill=rad((0, "#F0D08A"), (0.6, "#B08030"), (1, "#5A3C12")),
                stroke=INK, strokeWidth=1.4)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("screen extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 20, far


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
               color="#F0E4D2", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C8A88E", justify="center")
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


caption("FOLDING SCREEN", "LACQUERED WOOD · SILK · BRASS")
d.finish("folding-screen-V1R00")
