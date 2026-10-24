#!/usr/bin/env python3
"""Klismos chair — furniture field plate V1R00. Three-quarter from the front
right: the ancient Greek form — four sabre legs bowing outward, a leather-strap
seat in a trapezoid frame, rear uprights sweeping back into a wide curved
shoulder tablet. Painted-wood plate, classical mood: a pale shaft of
atrium light. 1000x1000.
Modelled in inches (x right, y up, +z back), fixed yaw + pitch projection;
legs and uprights are tapered ribbons along splines.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Klismos Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#181210"   # warm dark, not black
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


def catmull(pts, u):
    """Sample a Catmull-Rom spline through 3D control points, u in [0,1]."""
    n = len(pts)
    f = u * (n - 1)
    i = min(n - 2, int(f))
    t = f - i
    g = lambda j: pts[max(0, min(n - 1, j))]
    p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
    out = []
    for k in range(3):
        out.append(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t +
                          (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t * t +
                          (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t ** 3))
    return tuple(out)


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(22), math.radians(14)
S, OX, OY = 13.6, 502.0, 788.0
CY, SY = math.cos(YAW), math.sin(YAW)
CP, SP = math.cos(PITCH), math.sin(PITCH)


def P(x, y, z):
    xr, zr = x * CY + z * SY, -x * SY + z * CY
    p = (OX + S * xr, OY - S * (y * CP + zr * SP))
    EXTENT.append(p)
    return p


def depth(x, y, z):
    return -x * SY * CP - y * SP + z * CY * CP


PAINT_HI, PAINT_MID, PAINT_LO = "#5E6890", "#3A4058", "#1A1C28"
PAINT = ((0, PAINT_LO), (0.32, PAINT_MID), (0.55, PAINT_HI),
         (0.76, "#2E3450"), (1, "#12141E"))
LEATHER_HI, LEATHER_MID, LEATHER_LO = "#A87C44", "#7C5626", "#3E280C"


def ribbon(name, pts3, w0, w1, grad, ink=1.8, edge=None):
    """Tapered band along a 3D polyline (screen-space ribbon)."""
    pp = [P(*p) for p in pts3]
    n = len(pp)
    left, right = [], []
    for i, q in enumerate(pp):
        a, b = pp[max(0, i - 1)], pp[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        w = w0 + (w1 - w0) * i / (n - 1)
        left.append((q[0] + nx * w, q[1] + ny * w))
        right.append((q[0] - nx * w, q[1] - ny * w))
    pts = left + right[::-1]
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    d.path(poly(pts), name, fill=lin((0, y0), (0, y1), *grad),
           stroke=INK, strokeWidth=ink, join="round")
    if edge:
        # catch-light along the ribbon's upper-left edge
        d.path(smooth(left[:max(3, n * 2 // 3)], closed=False), name + " edge",
               fill=NONE, stroke=edge, strokeWidth=1.8, opacity=40, cap="round")
    return pts


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#161A20"), (1, "#07090C")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#6E7688", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#46434C"), (0.6, "#2E2C34"), (1, "#131118")),
        stroke="#0C0A10", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8D4E0", strokeWidth=3, opacity=20)
# classical mood: a pale shaft of light leaning in from upper left
d.path("M300,60 L520,60 L640,700 L420,700 Z", "Light shaft",
       fill=lin((380, 60), (530, 700), (0, "#E8E4D8", 0.10), (1, "#E8E4D8", 0.02)),
       stroke=NONE)

FY = 722
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#3E3A42", 42), (1, "#100E14", 78)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#DCD8CC", strokeWidth=2, opacity=15)

# --- geometry -----------------------------------------------------------------------
YS = 17.2                     # seat frame top
# seat frame corners (trapezoid: wide front, narrow back)
SFL = (-9.2, YS, -6.6)
SFR = (9.2, YS, -6.6)
SBL = (-7.8, YS, 6.2)
SBR = (7.8, YS, 6.2)

# sabre legs: spline from seat corner sweeping outward to the foot
LEGS = {
    "front-right": [SFR, (10.4, 12.5, -8.6), (11.3, 6.5, -10.2), (11.6, 0.5, -11.0)],
    "front-left":  [SFL, (-10.4, 12.5, -8.6), (-11.3, 6.5, -10.2), (-11.6, 0.5, -11.0)],
    "back-right":  [SBR, (9.0, 12.5, 8.4), (10.0, 6.5, 10.2), (10.3, 0.5, 10.8)],
    "back-left":   [SBL, (-9.0, 12.5, 8.4), (-10.0, 6.5, 10.2), (-10.3, 0.5, 10.8)],
}

# grounding shadow
sp = [P(x, 0, z) for x, z in ((-11, -10), (11, -10), (11, 11), (-11, 11))]
sx0, sx1 = min(p[0] for p in sp) - 30, max(p[0] for p in sp) + 30
sy0, sy1 = min(p[1] for p in sp) - 12, max(p[1] for p in sp) + 15
d.shape("ellipse", "Chair shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#030205", 66), (0.6, "#030205", 30), (1, "#030205", 0)),
        stroke=NONE)

# --- far legs first (left side is away from this viewer) --------------------------------
for nm in ("back-left", "front-left"):
    pts3 = [catmull(LEGS[nm], k / 18) for k in range(19)]
    ribbon(f"Leg {nm}", pts3, 11.0, 5.0, PAINT, edge=PAINT_HI)

# rear uprights sweep up-and-back from the back-leg tops to the tablet
UPR = {
    -1: [(-7.9, YS + 0.4, 6.4), (-7.8, 24.0, 8.0), (-7.3, 31.5, 9.6),
         (-6.9, 37.6, 10.3)],
    1: [(7.9, YS + 0.4, 6.4), (7.8, 24.0, 8.0), (7.3, 31.5, 9.6),
        (6.9, 37.6, 10.3)],
}
ribbon("Upright L", [catmull(UPR[-1], k / 16) for k in range(17)], 8.5, 5.0, PAINT,
       edge=PAINT_HI)

# --- seat: a slung leather pad sagging in the frame -------------------------------------
def seat_pt(u, z):
    """Seat surface: u in [-1,1] across, z along depth; sags mid-span."""
    f = (z + 6.4) / 12.4                     # 0 at front rail, 1 at back rail
    x = u * (9.0 - 1.2 * f)                  # trapezoid narrows toward the back
    return (x, YS - 0.15 - 0.9 * 4 * f * (1 - f) * (1 - u * u), z)


rows = []
for j, zz in enumerate([-6.3, -3.0, 0.2, 3.4, 6.0]):
    rows.append([P(*seat_pt(-1 + 0.25 * i, zz)) for i in range(9)])
pad = rows[0] + [r[-1] for r in rows[1:]] + rows[-1][::-1] + [r[0] for r in rows[1:-1]][::-1]
d.path(smooth(pad), "Seat pad",
       fill=lin((0, min(p[1] for p in pad)), (0, max(p[1] for p in pad)),
                (0, LEATHER_HI), (0.55, LEATHER_MID), (1, LEATHER_LO)),
       stroke=INK, strokeWidth=1.8)
# strap seams front-to-back
for i in range(1, 6):
    u = -1 + 2 * i / 6
    pts = [P(*seat_pt(u, -6.3 + 12.3 * k / 10)) for k in range(11)]
    d.path(smooth(pts, closed=False), f"Strap seam {i}", fill=NONE,
           stroke="#3E280C", strokeWidth=1.6, opacity=45)
# two lateral seams
for i, zz in enumerate((-2.6, 2.0)):
    pts = [P(*seat_pt(-0.96 + 1.92 * k / 10, zz)) for k in range(11)]
    d.path(smooth(pts, closed=False), f"Strap lat {i+1}", fill=NONE,
           stroke="#3E280C", strokeWidth=1.5, opacity=35)

# seat rails: painted frame — back and sides first, front last
def rail(name, a, b, w=7.0):
    ribbon(name, [a, b], w / 2, w / 2, PAINT, ink=1.8, edge=PAINT_HI)


rail("Back rail", (-8.2, YS + 0.4, 6.6), (8.2, YS + 0.4, 6.6), 6.0)
rail("Side rail L", (-9.0, YS, -6.3), (-7.9, YS + 0.4, 6.4), 6.5)
rail("Side rail R", (9.0, YS, -6.3), (7.9, YS + 0.4, 6.4), 6.5)
# front rail bows forward — the klismos seat-front curve
frail = [catmull([(-9.5, YS + 0.2, -6.8), (0, YS - 0.2, -8.1), (9.5, YS + 0.2, -6.8)],
                 k / 12) for k in range(13)]
ribbon("Front rail", frail, 4.0, 4.0, PAINT, ink=1.8, edge=PAINT_HI)

# --- stretchers ---------------------------------------------------------------------------
def leg_pt(nm, y0):
    """Point on a leg spline at height y0 (bisect the spline parameter)."""
    lo, hi = 0.0, 1.0
    for _ in range(24):
        mid = (lo + hi) / 2
        if catmull(LEGS[nm], mid)[1] > y0:
            lo = mid
        else:
            hi = mid
    return catmull(LEGS[nm], mid)


# front stretcher ties the front legs, sagging slightly between them
fr = [leg_pt("front-left", 7.4), (0, 6.4, -9.9), leg_pt("front-right", 7.4)]
ribbon("Stretcher front", [catmull(fr, k / 10) for k in range(11)], 4.6, 4.6, PAINT,
       ink=1.5)
for sgn, lbl in ((-1, "L"), (1, "R")):
    sd = [leg_pt("front-left" if sgn < 0 else "front-right", 7.2),
          (sgn * 10.2, 6.3, 0.4),
          leg_pt("back-left" if sgn < 0 else "back-right", 7.2)]
    ribbon(f"Stretcher {lbl}", [catmull(sd, k / 12) for k in range(13)], 4.4, 4.4,
           PAINT, ink=1.5)

# --- near legs over the straps ---------------------------------------------------------------
for nm in ("back-right", "front-right"):
    pts3 = [catmull(LEGS[nm], k / 18) for k in range(19)]
    ribbon(f"Leg {nm}", pts3, 11.0, 5.0, PAINT, edge=PAINT_HI)
ribbon("Upright R", [catmull(UPR[1], k / 16) for k in range(17)], 8.5, 5.0, PAINT,
       edge=PAINT_HI)

# --- the shoulder tablet: a broad panel concave toward the sitter -----------------------
# plan arc: ends wrap forward around the shoulders; top edge reclines a touch
def tablet_edge(x, top):
    z = 10.4 - 0.052 * x * x + (0.9 if top else 0.0)
    y = 38.4 - 0.028 * x * x if top else 33.9 - 0.028 * x * x
    return (x, y, z)


NXT = 30
top_e = [P(*tablet_edge(-8.9 + 17.8 * i / NXT, True)) for i in range(NXT + 1)]
bot_e = [P(*tablet_edge(-8.9 + 17.8 * i / NXT, False)) for i in range(NXT + 1)]
tablet = top_e + bot_e[::-1]
d.path(smooth(tablet), "Tablet",
       fill=lin((0, min(p[1] for p in tablet)), (0, max(p[1] for p in tablet)),
                (0, PAINT_HI), (0.45, PAINT_MID), (1, "#141620")),
       stroke=INK, strokeWidth=2.2, join="round")
# incised border just inside the tablet edge
inset = [(x, y - 1.1, z + 0.12) if top else (x, y + 1.1, z + 0.12)
         for (x, y, z), top in
         zip([tablet_edge(-8.4 + 16.8 * i / NXT, True) for i in range(NXT + 1)] +
             [tablet_edge(-8.4 + 16.8 * i / NXT, False) for i in range(NXT + 1)][::-1],
             [True] * (NXT + 1) + [False] * (NXT + 1))]
d.path(smooth([P(*p) for p in inset]), "Tablet inset", fill=NONE,
       stroke="#0C0E14", strokeWidth=1.8, opacity=60)
# a small palmette at the tablet's centre — five short strokes fanning up
cx, cy = P(*tablet_edge(0.0, False))
for i, a in enumerate((-32, -16, 0, 16, 32)):
    aa = math.radians(a - 90)
    x1, y1 = cx + 3.0 * math.cos(aa), cy - 8
    x2, y2 = cx + 26.0 * math.cos(aa), cy - 8 + 26.0 * math.sin(aa)
    d.path(f"M{x1:.1f},{y1:.1f} Q{(x1 + x2) / 2 + 2 * math.sin(aa):.1f},{(y1 + y2) / 2:.1f} {x2:.1f},{y2:.1f}",
           f"Palmette {i+1}", fill=NONE, stroke="#8890B0", strokeWidth=2.2,
           opacity=50, cap="round")
d.path(f"M{cx - 14:.1f},{cy - 7:.1f} L{cx + 14:.1f},{cy - 7:.1f}", "Palmette base",
       fill=NONE, stroke="#8890B0", strokeWidth=2.4, opacity=50, cap="round")

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
               color="#ECE8F0", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#B0ACC0", justify="center")
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


caption("KLISMOS CHAIR", "PAINTED WOOD · LEATHER")
d.finish("klismos-chair-V1R00")
