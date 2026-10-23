#!/usr/bin/env python3
"""Arc floor lamp — field plate V1R00. Near-side view: a weighted marble
base at lower left, the long chromed stem sweeping up and over in one
arc, ending in a domed shade over empty space; a warm pool of light on
the disc floor. Dark plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Arc Floor Lamp — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1C1410"   # warm dark, not black
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


# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#17181D"), (1, "#090A0E")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#5A6070", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#484C58"), (0.6, "#33363F"), (1, "#1E2128")),
        stroke="#0D1015", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D0DC", strokeWidth=3, opacity=24)

FY = 708
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#545A66", 32), (1, "#12151B", 70)), stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#D2D8E2", strokeWidth=2, opacity=18)

# --- the arc ----------------------------------------------------------------------
# cubic from base top (272,628) over to the shade socket (742,296)
P0, C1, C2, P1 = (272, 628), (252, 238), (636, 128), (742, 296)


def bez(t):
    mt = 1 - t
    x = mt**3*P0[0] + 3*mt*mt*t*C1[0] + 3*mt*t*t*C2[0] + t**3*P1[0]
    y = mt**3*P0[1] + 3*mt*mt*t*C1[1] + 3*mt*t*t*C2[1] + t**3*P1[1]
    dx = 3*mt*mt*(C1[0]-P0[0]) + 6*mt*t*(C2[0]-C1[0]) + 3*t*t*(P1[0]-C2[0])
    dy = 3*mt*mt*(C1[1]-P0[1]) + 6*mt*t*(C2[1]-C1[1]) + 3*t*t*(P1[1]-C2[1])
    return (x, y), (dx, dy)


N = 44
TS = [i / N for i in range(N + 1)]
pts, tans = [], []
for t in TS:
    p, tn = bez(t)
    pts.append(p); tans.append(tn)
    EXTENT.append(p)

W = [7.2 - 1.4 * t for t in TS]          # stem tapers slightly toward the shade
left, right = [], []
for (x, y), (tx, ty), w in zip(pts, tans, W):
    L = math.hypot(tx, ty)
    nx, ny = -ty / L, tx / L
    left.append((x + nx * w, y + ny * w))
    right.append((x - nx * w, y - ny * w))

CHROME = ((0, "#F4F8FC"), (0.3, "#9AA4B0"), (0.5, "#3E4650"),
          (0.68, "#B8C0CA"), (1, "#4E5660"))
d.path(poly(left + right[::-1]), "Arc stem",
       fill=lin((290, 150), (620, 620), *CHROME), stroke=INK, strokeWidth=2.5, join="round")
# highlight along the upper edge of the arc
d.path(smooth(left[2:-2]), "Stem edge light", fill=NONE, stroke="#F8FBFE",
       strokeWidth=2.2, opacity=45, cap="round")
# shadow ribbon on the underside
under = [(x - (x - right[i][0]) * 0.45, y - (y - right[i][1]) * 0.45)
         for i, (x, y) in enumerate(left)]
d.path(poly(left + under[::-1]), "Stem underside shade",
       fill="#141820", opacity=28, stroke=NONE)

# --- light cone + pool (drawn under the shade, over the floor) ---------------------
cone = [(694, 348), (788, 348), (806, 690), (676, 690)]
for c in cone:
    assert on_disc(c[0], c[1], 10), c
d.path(poly(cone), "Light cone",
       fill=lin((741, 348), (741, 690), (0, "#FFD9A0", 22), (1, "#FFB85C", 6)),
       stroke=NONE)
d.shape("ellipse", "Light pool", x=648, y=676, width=180, height=40,
        fill=rad((0, "#FFCE8A", 52), (0.55, "#E8A05C", 22), (1, "#B06A30", 0)),
        stroke=NONE)

# --- marble base ---------------------------------------------------------------------
# shadow first
d.shape("ellipse", "Base shadow", x=182, y=688, width=196, height=30,
        fill=rad((0, "#04060A", 62), (0.6, "#04060A", 26), (1, "#04060A", 0)), stroke=NONE)
# cylinder body: sides + bottom edge
d.path("M206,648 L206,692 C206,706 244,716 280,716 C316,716 354,706 354,692 L354,648 Z",
       "Base body", fill=lin((206, 0), (354, 0), (0, "#464C58"), (0.35, "#23262E"),
                             (0.72, "#14161C"), (1, "#343945")),
       stroke=INK, strokeWidth=3)
# top face
d.shape("ellipse", "Base top", x=206, y=632, width=148, height=34,
        fill=rad((0, "#585E6C"), (0.65, "#2C2F38"), (1, "#181B21")),
        stroke=INK, strokeWidth=3)
EXTENT += [(206, 632), (354, 632), (280, 716)]
# marble veins on the body
d.path("M222,662 C250,668 268,684 300,688 C322,691 340,686 350,680",
       "Vein 1", fill=NONE, stroke="#8A93A0", strokeWidth=2, opacity=38, cap="round")
d.path("M214,690 C240,696 262,706 296,708", "Vein 2",
       fill=NONE, stroke="#78818E", strokeWidth=1.8, opacity=30, cap="round")
d.path("M248,650 C262,662 270,676 288,684", "Vein 3",
       fill=NONE, stroke="#A0A8B4", strokeWidth=1.6, opacity=26, cap="round")
# polished rim light on the top face
d.path("M222,642 C250,634 310,634 338,642", "Base top light",
       fill=NONE, stroke="#C4CCD8", strokeWidth=2.4, opacity=40, cap="round")
# chrome collar where the stem rises
d.shape("ellipse", "Stem collar", x=258, y=618, width=30, height=18,
        fill=lin((258, 0), (288, 0), *CHROME), stroke=INK, strokeWidth=2)

# --- domed shade ----------------------------------------------------------------------
SX, SY, SR = 742, 336, 62     # rim centre + dome radius
# outer dome: hemisphere shell
d.path(f"M{SX - SR},{SY} A{SR},{SR} 0 0 1 {SX + SR},{SY} "
       f"A{SR},{SR * 0.30:.0f} 0 0 1 {SX - SR},{SY} Z",
       "Shade shell", fill=lin((SX - SR, SY - SR), (SX + SR, SY + 20),
                               (0, "#E8B45C"), (0.35, "#B07A34"), (0.62, "#6A4218"),
                               (0.85, "#C89650"), (1, "#4A2C0E")),
       stroke=INK, strokeWidth=4, join="round")
EXTENT += [(SX - SR, SY), (SX + SR, SY), (SX, SY - SR)]
# rim: the opening ellipse, warm inside
d.shape("ellipse", "Shade rim", x=SX - SR, y=SY - 9, width=2 * SR, height=20,
        fill="#241408", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Shade inner glow", x=SX - SR + 8, y=SY - 6, width=2 * SR - 16, height=15,
        fill=rad((0, "#FFDFA8"), (0.5, "#E8A85C"), (1, "#8A4A18")), stroke=NONE)
# bulb peeking under the dome
d.shape("ellipse", "Bulb", x=SX - 11, y=SY - 2, width=22, height=18,
        fill=rad((0, "#FFF4DC"), (0.7, "#FFC878"), (1, "#C88030")), stroke=NONE)
d.shape("ellipse", "Bulb bloom", x=SX - 26, y=SY - 8, width=52, height=34,
        fill=rad((0, "#FFE8B8", 55), (1, "#FFE8B8", 0)), stroke=NONE)
# socket joint where the stem enters the dome
d.shape("ellipse", "Socket", x=SX - 12, y=SY - SR - 10, width=24, height=18,
        fill=lin((SX - 12, 0), (SX + 12, 0), *CHROME), stroke=INK, strokeWidth=2)
# specular on the dome crown
d.path(f"M{SX - 38},{SY - 40} C{SX - 22},{SY - 56} {SX + 8},{SY - 60} {SX + 30},{SY - 48}",
       "Dome specular", fill=NONE, stroke="#FFEDC4", strokeWidth=3, cap="round", opacity=50)

# --- extent check ----------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("lamp extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far


# --- caption ----------------------------------------------------------------------------
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
               color="#F0E2CE", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#B09C84", justify="center")
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


caption("ARC FLOOR LAMP", "MARBLE · CHROMED STEEL · BRASS")
d.finish("arc-floor-lamp-V1R00")
