#!/usr/bin/env python3
"""Drum table — field plate V1R00. Three-quarter from the front right:
a round mahogany top overhanging a deep drum apron studded with little
drawer fronts and brass knobs, a turned column, and four downswept legs
landing in pad feet. Mahogany plate, library mood: deep red-brown disc
with a low lamplight pool. 1000x1000.
Modelled in inches (x right, y up, +z back), projected with fixed yaw +
pitch; the drum and column are arc-ribbon cylinder walls, legs are swept
tapered ribbons on radial planes.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Drum Table — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1C100B"   # warm dark, not black
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
YAW, PITCH = math.radians(30), math.radians(24)
S, OX, OY = 11.8, 502.0, 738.0
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


def cyl(r, y, a0=0, a1=360, n=30, c=(0, 0)):
    """Ring of projected points on a horizontal circle (a=0 -> +z)."""
    return [P(c[0] + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)), y,
              c[1] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def wall(r, y0, y1, a0, a1, name, n=30, c=(0, 0), tone=None, ink=1.7):
    pts = cyl(r, y1, a0, a1, n, c) + cyl(r, y0, a1, a0, n, c)
    y0s, y1s = min(p[1] for p in pts), max(p[1] for p in pts)
    g = lin((0, y0s), (0, y1s), *(tone or ((0, MAH_HI), (0.5, MAH_L), (1, MAH_D))))
    d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return pts


def swept(name, pts3, w0, w1, tone, ink=1.7):
    """Tapered ribbon along a 3D polyline; width interpolates w0->w1."""
    sp = [P(*p) for p in pts3]
    n = len(sp)
    left, right = [], []
    for i, p in enumerate(sp):
        j0, j1 = max(0, i - 1), min(n - 1, i + 1)
        dx, dy = sp[j1][0] - sp[j0][0], sp[j1][1] - sp[j0][1]
        L = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * i / (n - 1)) * S
        left.append((p[0] - dy / L * w, p[1] + dx / L * w))
        right.append((p[0] + dy / L * w, p[1] - dx / L * w))
    pts = left + right[::-1]
    y0s, y1s = min(p[1] for p in pts), max(p[1] for p in pts)
    d.path(poly(pts), name,
           fill=lin((0, y0s), (0, y1s), *tone),
           stroke=INK, strokeWidth=ink, join="round")


# --- palette ---------------------------------------------------------------------------
MAH_D, MAH_L = "#26110A", "#84431F"
MAH_HI = "#BC7940"
BRASS = ((0, "#F4D488"), (0.6, "#B8862E"), (1, "#5E3C10"))

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#150D0A"), (1, "#060303")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7A4022", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#55321F"), (0.6, "#372012"), (1, "#130A06")),
        stroke="#0D0604", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCAE7E", strokeWidth=3, opacity=22)
# lamplight pool, warm from the left
d.shape("ellipse", "Lamplight", x=180, y=110, width=560, height=540,
        fill=rad((0, "#E8A45C", 15), (0.55, "#A06030", 5), (1, "#A06030", 0)),
        stroke=NONE)

FY = 694
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#462A18", 38), (1, "#100704", 78)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E0B284", strokeWidth=2, opacity=18)

# --- table geometry (inches) -------------------------------------------------------------
TOP_R = 15.0            # top radius
DRUM_R = 13.6           # apron radius
AP_Y0, AP_Y1 = 23.6, 27.6
TOP_Y = 29.2            # top face height (edge band above apron)

# grounding shadow
sp = [P(x, 0, z) for x, z in [(-14, -14), (14, -14), (14, 14), (-14, 14)]]
sx0, sx1 = min(p[0] for p in sp) - 30, max(p[0] for p in sp) + 30
sy0, sy1 = min(p[1] for p in sp) - 12, max(p[1] for p in sp) + 14
d.shape("ellipse", "Table shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#040202", 66), (0.6, "#040202", 24), (1, "#040202", 0)),
        stroke=NONE)

# --- legs: four downswept ribbons, far ones first -------------------------------------------
def leg_pts(a):
    """Centreline of the down-swept leg at azimuth a, column base -> pad foot."""
    pts = []
    for i in range(10):
        t = i / 9
        r = 4.3 + 8.9 * (t ** 1.35)
        y = 9.8 - 8.6 * t
        pts.append((r * math.sin(math.radians(a)), y,
                    r * math.cos(math.radians(a))))
    return pts


for i, a in enumerate(sorted((45, 135, 225, 315),
                             key=lambda t: -depth(12 * math.sin(math.radians(t)),
                                                  4, 12 * math.cos(math.radians(t))))):
    swept(f"Leg {i+1}", leg_pts(a), 0.74, 0.42,
          ((0, MAH_L), (0.55, "#5E2E14"), (1, MAH_D)), ink=1.6)
    tip = leg_pts(a)[-1]
    fx, fy = P(tip[0], 1.0, tip[2])
    d.shape("ellipse", f"Pad foot {i+1}", x=round(fx - 12), y=round(fy - 5),
            width=24, height=10, fill=rad((0, "#5E3018"), (1, "#1E0D06")),
            stroke=INK, strokeWidth=1.5)

# --- column: a single turned baluster profile, revolved -------------------------------------
# (y, r) pairs bottom -> top: plinth foot, shaft, urn swell, neck, collar
PROF = [(8.4, 5.5), (9.2, 5.5), (9.9, 4.4), (10.5, 3.9), (11.4, 3.3),
        (13.2, 3.05), (14.6, 3.2), (15.4, 4.4), (16.4, 5.0), (17.4, 5.0),
        (18.3, 4.2), (19.0, 3.4), (20.0, 3.2), (21.0, 3.4), (21.9, 4.5),
        (22.7, 4.95), (23.55, 5.1)]
col_l = [P(-r, y, 0) for y, r in PROF]
col_r = [P(r, y, 0) for y, r in PROF[::-1]]
col_pts = col_l + col_r
x0s, x1s = min(p[0] for p in col_pts), max(p[0] for p in col_pts)
d.path(poly(col_pts), "Pedestal",
       fill=lin((x0s, 0), (x1s, 0),
                (0, "#200D05"), (0.3, "#6E3A1C"), (0.46, MAH_HI),
                (0.62, MAH_L), (1, "#1E0C05")),
       stroke=INK, strokeWidth=2.0, join="round")
# sheen up the urn's left shoulder
shx, shy = P(-2.1, 16.9, 0)
d.shape("ellipse", "Urn sheen", x=round(shx - 26), y=round(shy - 34),
        width=52, height=68, fill=rad((0, "#F0C088", 32), (1, "#F0C088", 0)),
        stroke=NONE)
# bead line where the pedestal meets the apron
bd = cyl(5.15, 23.5, -180, 180, 26)
d.path(smooth(bd, closed=False), "Pedestal bead", fill=NONE, stroke=INK,
       strokeWidth=1.8, opacity=60)

# --- drum apron + drawer fronts --------------------------------------------------------------
wall(DRUM_R, AP_Y0, AP_Y1, -180, 180, "Drum apron", n=44,
     tone=((0, "#A86836"), (0.45, MAH_L), (0.8, "#4A2210"), (1, "#2A120A")),
     ink=2.0)
# apron bead lines top and bottom
for yy, lbl in ((AP_Y0 + 0.35, "low"), (AP_Y1 - 0.3, "high")):
    pts = cyl(DRUM_R + 0.04, yy, 108, 252, 26)
    d.path(smooth(pts, closed=False), f"Apron bead {lbl}", fill=NONE,
           stroke="#1E0D06", strokeWidth=2.0, opacity=55)

# drawer fronts across the front of the drum: 5 fronts, knobs on each
for i, ac in enumerate((113, 146.5, 180, 213.5, 247)):
    pts = cyl(DRUM_R + 0.14, AP_Y1 - 0.62, ac - 13.5, ac + 13.5, 8) + \
          cyl(DRUM_R + 0.14, AP_Y0 + 0.62, ac + 13.5, ac - 13.5, 8)
    y0s, y1s = min(p[1] for p in pts), max(p[1] for p in pts)
    d.path(poly(pts), f"Drawer front {i+1}",
           fill=lin((0, y0s), (0, y1s), (0, "#B87A44"), (0.6, "#8A4E26"),
                    (1, "#3A1B0C")),
           stroke=INK, strokeWidth=1.7, join="round")
    # two tiny brass knobs per drawer
    for ka in (ac - 6, ac + 6):
        kx, ky = P((DRUM_R + 0.3) * math.sin(math.radians(ka)),
                   (AP_Y0 + AP_Y1) / 2, (DRUM_R + 0.3) * math.cos(math.radians(ka)))
        d.shape("ellipse", f"Knob {i+1}.{ka:.0f}", x=round(kx - 3.4), y=round(ky - 2.9),
                width=6.8, height=5.8, fill=rad(*BRASS), stroke=INK, strokeWidth=1.0)

# --- top: edge band + face with tooled inset -------------------------------------------------
wall(TOP_R, AP_Y1 - 0.2, TOP_Y, -180, 180, "Top edge", n=44,
     tone=((0, "#B0763E"), (0.5, "#6E3A1C"), (1, "#2A120A")), ink=2.0)
top_pts = [P(TOP_R * math.sin(math.radians(t)), TOP_Y,
             TOP_R * math.cos(math.radians(t))) for t in range(0, 360, 9)]
d.path(smooth(top_pts), "Table top",
       fill=rad((0, "#9A5E30"), (0.55, "#6E3B1C"), (1, "#33170C")),
       stroke=INK, strokeWidth=2.2, join="round")
# tooled leather inset ring on the top face
inset = [P(11.6 * math.sin(math.radians(t)), TOP_Y + 0.02,
           11.6 * math.cos(math.radians(t))) for t in range(0, 360, 9)]
d.path(smooth(inset), "Top inset ring", fill=NONE, stroke="#3A1B0C",
       strokeWidth=1.8, opacity=50)
inset2 = [P(10.9 * math.sin(math.radians(t)), TOP_Y + 0.02,
            10.9 * math.cos(math.radians(t))) for t in range(0, 360, 9)]
d.path(smooth(inset2), "Top inset ring 2", fill=NONE, stroke="#C08A54",
       strokeWidth=1.2, opacity=30)
# sheen sweeping the top's near-left
txx, tyy = P(-5, TOP_Y, -3)
d.shape("ellipse", "Top sheen", x=round(txx - 105), y=round(tyy - 46),
        width=210, height=92, fill=rad((0, "#F0C088", 18), (1, "#F0C088", 0)),
        stroke=NONE)
# rim light along the top's far edge
rim = cyl(TOP_R - 0.2, TOP_Y + 0.1, -80, 80, 22)
d.path(smooth(rim, closed=False), "Top rim light", fill=NONE, stroke="#F0C890",
       strokeWidth=2.2, opacity=30, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("table extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F2DCBE", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C89870", justify="center")
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


caption("DRUM TABLE", "MAHOGANY · LEATHER · BRASS")
d.finish("drum-table-V1R00")
