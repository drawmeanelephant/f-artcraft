#!/usr/bin/env python3
"""Cantilever chair — furniture field plate V1R00. Cesca type in near-side
view with a slight three-quarter: one continuous chrome tube runs the sled
base, bends up at the front to seat height, runs back under the cane seat
and rises to carry the cane back — a seat with no back legs. Beech frames,
honey cane webbing, rubber glides under the sled. Bauhaus mood: cool slate
plate, bright chrome. 1000x1000. Modelled in inches (x right, y up,
+z back), projected with a fixed yaw + pitch; the tube is a stroked path in
each side plane, panels are quads on their own planes.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Cantilever Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#18120C"   # warm dark, not black
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
YAW, PITCH = math.radians(30), math.radians(14)
S, OX, OY = 14.6, 502.0, 748.0
CY, SY = math.cos(YAW), math.sin(YAW)
CP, SP = math.cos(PITCH), math.sin(PITCH)


def P(x, y, z):
    xr, zr = x * CY + z * SY, -x * SY + z * CY
    p = (OX + S * xr, OY - S * (y * CP + zr * SP))
    EXTENT.append(p)
    return p


def sp(x, y, z):
    """Project without recording extent (interior points only)."""
    xr, zr = x * CY + z * SY, -x * SY + z * CY
    return (OX + S * xr, OY - S * (y * CP + zr * SP))


# --- backdrop + plate ------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#12181E"), (1, "#06080A")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7A8A96", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#4E5658"), (0.55, "#30383A"), (1, "#141A1C")),
        stroke="#0C1214", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D2DCD8", strokeWidth=3, opacity=24)

# floor: pale boards closing on the disc arc — the bauhaus studio
FYB = 720
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX - hw:.1f},{FYB} L{PCX + hw:.1f},{FYB} A420,420 0 0 0 {PCX - hw:.1f},{FYB} Z",
       "Floor", fill=lin((0, FYB), (0, 880), (0, "#4A4438", 0.5), (0.5, "#2A261E", 0.75),
                         (1, "#12100A", 0.92)), stroke=NONE)
d.path(f"M{PCX - hw + 6:.1f},{FYB} L{PCX + hw - 6:.1f},{FYB}", "Floor edge light",
       fill=NONE, stroke="#D8D2BE", strokeWidth=2, opacity=15)
for i, yb in enumerate([762, 798, 834]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Board seam {i+1}",
           fill=NONE, stroke="#585244", strokeWidth=2, opacity=22)

# grounding shadow under the sled
se = [P(-10, 0, -10), P(10, 0, -10), P(-10, 0, 11), P(10, 0, 11)]
sx0, sx1 = min(p[0] for p in se) - 24, max(p[0] for p in se) + 24
sy0, sy1 = min(p[1] for p in se) - 12, max(p[1] for p in se) + 16
d.shape("ellipse", "Chair shadow", x=round(sx0), y=round(sy0), width=round(sx1 - sx0),
        height=round(sy1 - sy0),
        fill=rad((0, "#030405", 0.62), (0.6, "#030405", 0.28), (1, "#030405", 0)),
        stroke=NONE)

# --- the tube ----------------------------------------------------------------------------
# side profile (z,y): sled on the floor -> front bend up to seat height ->
# run back under the seat -> rise to the back top. One continuous line.
TX = 9.2                       # lateral offset of each side tube


def tube_path(x):
    """Screen-space polyline of the frame profile at lateral offset x.

    One continuous line: down the back face, forward under the seat,
    down the front bend to the floor, back along the sled, then up the
    rear riser to join behind the back — the whole chair on one bend.
    """
    zy = [(10.2, 33.8), (9.8, 30.0), (9.2, 25.0), (8.6, 20.5), (8.2, 17.4),
          (5.5, 16.9), (-6.6, 16.9),
          (-8.2, 14.5), (-9.2, 10.0), (-9.6, 5.5), (-9.0, 2.4), (-7.4, 1.1),
          (7.6, 1.0),
          (9.2, 1.4), (10.2, 3.2), (10.7, 6.5), (10.9, 10.0), (10.9, 13.5)]
    pts = [P(x, y, z) for z, y in zy]
    ext(max(p[0] for p in pts) + 5, min(p[1] for p in pts))
    ext(min(p[0] for p in pts) - 5, max(p[1] for p in pts))
    return smooth(pts)


def chrome(name, path_d):
    d.path(path_d, name + " edge", fill=NONE, stroke=INK, strokeWidth=9.6,
           join="round", cap="round")
    d.path(path_d, name, fill=NONE, stroke="#9AAAB4", strokeWidth=6.0,
           join="round", cap="round")
    d.path(path_d, name + " core", fill=NONE, stroke="#DDE8EC", strokeWidth=2.6,
           opacity=85, join="round", cap="round")
    d.path(path_d, name + " dark", fill=NONE, stroke="#3A464E", strokeWidth=1.4,
           opacity=50, join="round", cap="round")


chrome("Far tube", tube_path(TX))

# rubber glides on the sled's floor run
for sx, tag in ((-1, "near"), (1, "far")):
    for gz in (-5.5, 7.5):
        gp = P(sx * TX, 0.35, gz)
        d.shape("ellipse", f"Glide {tag} {gz:+g}", x=round(gp[0] - 6), y=round(gp[1] - 3.5),
                width=12, height=7, fill=rad((0, "#3A3E42"), (1, "#101214")),
                stroke=INK, strokeWidth=1.2)

# --- cane seat in its beech frame -----------------------------------------------------------
# seat slab: x +-8.4, y 17.2..18.6, z -7.4..7.6
def quad(name, corners, grad, sw=2.0, opacity=None, stroke=INK):
    pts = [P(*c) for c in corners]
    kw = {"fill": grad, "stroke": stroke, "strokeWidth": sw, "join": "round"}
    if opacity is not None:
        kw["opacity"] = opacity
    d.path(poly(pts), name, **kw)
    return pts


BEECH = ((0, "#D8AC6E"), (0.5, "#A8783E"), (1, "#6E4A20"))
CANE = ((0, "#EED9A8"), (0.6, "#D8B878"), (1, "#B08A4A"))

# seat slab drawn as three faces: front edge, top, side
seat_top = quad("Seat beech edge", [(-8.4, 17.2, -7.6), (8.4, 17.2, -7.6),
                                    (8.4, 17.2, 7.6), (-8.4, 17.2, 7.6)],
                lin((0, 600), (0, 660), *BEECH))
seat_f = quad("Seat front edge", [(-8.4, 17.2, -7.6), (8.4, 17.2, -7.6),
                                  (8.4, 18.7, -7.6), (-8.4, 18.7, -7.6)],
              lin((0, 600), (0, 660), (0, "#8A5E2E"), (1, "#4E3012")))
seat_s = quad("Seat side edge", [(8.4, 17.2, -7.6), (8.4, 17.2, 7.6),
                                 (8.4, 18.7, 7.6), (8.4, 18.7, -7.6)],
              lin((0, 600), (0, 660), (0, "#7A5226"), (1, "#3E240E")))
# cane field inset on the seat top
seat_cane = quad("Seat cane", [(-7.6, 18.62, -6.8), (7.6, 18.62, -6.8),
                               (7.6, 18.62, 6.8), (-7.6, 18.62, 6.8)],
                 lin((0, 560), (0, 640), *CANE), sw=1.4)
# cane weave: fine grid on the seat plane
for k in range(1, 8):
    u = -7.6 + 15.2 * k / 8
    a, b = sp(u, 18.63, -6.8), sp(u, 18.63, 6.8)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Seat weave u{k}",
           fill=NONE, stroke="#8A6428", strokeWidth=1.5, opacity=35)
for k in range(1, 7):
    zz = -6.8 + 13.6 * k / 7
    a, b = sp(-7.6, 18.63, zz), sp(7.6, 18.63, zz)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Seat weave z{k}",
           fill=NONE, stroke="#8A6428", strokeWidth=1.5, opacity=35)

# --- cane back, reclining slightly ----------------------------------------------------------
# back frame: x +-8.4, v 19.5..34.2, tilted so the top sits further back
ZB0, ZB1 = 8.4, 10.6
back_f = quad("Back frame", [(-8.4, 18.8, ZB0), (8.4, 18.8, ZB0),
                             (8.4, 34.4, ZB1), (-8.4, 34.4, ZB1)],
              lin((0, 240), (0, 330), *BEECH))
back_cane = quad("Back cane", [(-7.4, 19.8, ZB0 + 0.12), (7.4, 19.8, ZB0 + 0.12),
                               (7.4, 33.4, ZB1 - 0.12), (-7.4, 33.4, ZB1 - 0.12)],
                 lin((0, 250), (0, 320), *CANE), sw=1.4)
# weave on the back
for k in range(1, 8):
    u = -7.4 + 14.8 * k / 8
    t = (u + 7.4) / 14.8
    a = sp(u, 20.4, ZB0 + 0.14)
    b = sp(u, 33.4, ZB1 - 0.14)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Back weave u{k}",
           fill=NONE, stroke="#8A6428", strokeWidth=1.5, opacity=35)
for k in range(1, 6):
    v = 20.4 + 13.0 * k / 6
    zz = ZB0 + 0.14 + (ZB1 - ZB0 - 0.28) * (v - 20.4) / 13.0
    a, b = sp(-7.4, v, zz), sp(7.4, v, zz)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Back weave v{k}",
           fill=NONE, stroke="#8A6428", strokeWidth=1.5, opacity=35)

chrome("Near tube", tube_path(-TX))

# cross run across the top of the back — the same tube, bent over
top_a, top_b = P(-TX, 33.8, 10.2), P(TX, 33.8, 10.2)
topd = f"M{top_a[0]:.1f},{top_a[1]:.1f} L{top_b[0]:.1f},{top_b[1]:.1f}"
chrome("Back top run", topd)

# chrome glints at the bends
for sx, tag in ((-1, "near"), (1, "far")):
    for gz, gy in ((-8.8, 8.0), (8.2, 21.5)):
        gp = sp(sx * TX, gy, gz)
        d.shape("ellipse", f"Glint {tag} {gz:+g}", x=round(gp[0] - 3), y=round(gp[1] - 5),
                width=6, height=10, fill="#FFFFFF", opacity=60, stroke=NONE)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#ECF0EC", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#B4C2BC", justify="center")
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


caption("CANTILEVER CHAIR", "CHROME · CANE · BEECH")
d.finish("cantilever-chair-V1R00")
