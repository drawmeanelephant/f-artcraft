#!/usr/bin/env python3
"""Pendant lamp — field plate V1R00. Straight-on workshop corner:
a single green-enamel dome shade on a cloth cord, hanging over the edge
of a workbench; a cone of warm light pooling on the bench top where a
jar, a folded rag and a small tool rest. Enamel plate — deep green disc,
pale ring. 1000x1000.
Drawn in screen space: lathe profiles for shade + canopy, quads for the
bench, strokes for the cord.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Pendant Lamp — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
AX = 500            # lamp axis
INK = "#141C16"     # warm dark green-ink, not black
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


def smooth(pts, closed=True, k=1.0):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


def poly(pts):
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"


def lathe(profile, ax=AX):
    """Right-half profile [(x,y)...] bottom->top -> closed symmetric silhouette."""
    left = [(2 * ax - x, y) for x, y in reversed(profile)]
    for p in profile + left:
        EXTENT.append(p)
    return smooth(profile + left)


def mark(x, y):
    EXTENT.append((x, y))


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#0E1410"), (1, "#050705")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7A9A80", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#3A5248"), (0.55, "#26382F"), (1, "#0F1A14")),
        stroke="#0A100C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E2C8", strokeWidth=3, opacity=24)

# workshop wall: two faint shelf lines high on the plate
for i, (y, x0, x1, op) in enumerate([(230, 232, 356, 30), (238, 644, 768, 24)]):
    mark(x0, y); mark(x1, y)
    d.path(f"M{x0},{y} L{x1},{y}", f"Wall line {i+1}", fill=NONE,
           stroke="#0E1A14", strokeWidth=3.4, opacity=op + 20)
    d.path(f"M{x0},{y-3} L{x1},{y-3}", f"Wall line {i+1} light", fill=NONE,
           stroke="#8AA88E", strokeWidth=1.6, opacity=op)

# --- the cord + canopy (drawn first; the shade caps its foot) --------------------------
# small ceiling canopy dome
canopy = lathe([(478, 96), (478, 88), (486, 80), (496, 76), (500, 74)])
mark(478, 96)
d.path(canopy, "Canopy", fill=lin((478, 0), (500, 0),
       (0, "#3A3018"), (0.5, "#A8843E"), (1, "#2A2210")),
       stroke=INK, strokeWidth=1.6, join="round")
# cloth cord: soft S-curve down to the socket
cord = [(500, 94), (497, 160), (503, 230), (499, 300), (500, 330)]
d.path(smooth(cord, closed=False), "Cord", fill=NONE, stroke="#3A2E1E",
       strokeWidth=5.0, cap="round")
d.path(smooth([(x - 1.6, y) for x, y in cord], closed=False), "Cord sheen",
       fill=NONE, stroke="#8A7040", strokeWidth=1.6, opacity=55, cap="round")

# --- light: cone from the shade mouth down to the bench -------------------------------
d.path("M386,372 L614,372 L688,668 L312,668 Z", "Light cone",
       fill=lin((500, 372), (500, 668), (0, "#FFCE84", 0.20), (0.5, "#F0A850", 0.08),
                (1, "#F0A850", 0.02)), stroke=NONE)
d.shape("ellipse", "Cone bloom", x=360, y=340, width=280, height=120,
        fill=rad((0, "#FFDC9A", 0.28), (0.6, "#F0B060", 0.10), (1, "#F0B060", 0)),
        stroke=NONE)
# dust motes hanging in the beam
for i, (mx, my, mr, mo) in enumerate([(452, 430, 2.2, 30), (520, 470, 1.8, 24),
                                     (480, 520, 2.4, 28), (560, 550, 1.7, 22),
                                     (430, 580, 1.9, 22), (530, 610, 1.5, 18),
                                     (600, 500, 1.6, 20), (410, 470, 1.4, 18)]):
    d.shape("ellipse", f"Mote {i+1}", x=mx, y=my, width=mr * 2, height=mr * 2,
            fill="#FFE8C0", opacity=mo, stroke=NONE)

# --- floor boards closing on the disc arc --------------------------------------------
FYB = 726
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX - hw:.1f},{FYB} L{PCX + hw:.1f},{FYB} A420,420 0 0 1 {PCX - hw:.1f},{FYB} Z",
       "Floor", fill=lin((0, FYB), (0, 880), (0, "#2E332A", 0.5),
                         (0.5, "#171B14", 0.78), (1, "#0A0C08", 0.92)), stroke=NONE)
d.path(f"M{PCX - hw + 6:.1f},{FYB} L{PCX + hw - 6:.1f},{FYB}", "Floor edge light",
       fill=NONE, stroke="#C8D4B8", strokeWidth=2, opacity=14)

# --- the workbench ---------------------------------------------------------------------
BENCH_Y0, BENCH_Y1 = 636, 668
bx0, bx1 = 296, 712
# bench shadow first
for bx_, by_ in [(282, 680), (726, 680), (324, 776), (676, 776)]:
    mark(bx_, by_)
d.shape("ellipse", "Bench shadow", x=290, y=746, width=440, height=60,
        fill=rad((0, "#030402", 0.66), (0.6, "#030402", 0.3), (1, "#030402", 0)),
        stroke=NONE)
# legs behind the top
d.path("M320,668 L348,668 L344,776 L324,776 Z", "Leg L",
       fill=lin((320, 0), (348, 0), (0, "#4A3418"), (0.5, "#8A6030"), (1, "#2E1E0C")),
       stroke=INK, strokeWidth=1.8, join="round")
d.path("M652,668 L680,668 L676,776 L656,776 Z", "Leg R",
       fill=lin((652, 0), (680, 0), (0, "#4A3418"), (0.5, "#8A6030"), (1, "#2E1E0C")),
       stroke=INK, strokeWidth=1.8, join="round")
d.path("M344,742 L656,742 L656,752 L344,752 Z", "Stretcher",
       fill=lin((0, 742), (0, 752), (0, "#6A4A24"), (1, "#3A2812")),
       stroke=INK, strokeWidth=1.5)
# top slab: a shallow trapezoid, slightly deeper on the right (perspective lean)
d.path(poly([(bx0, BENCH_Y0), (bx1, BENCH_Y0), (bx1 + 14, BENCH_Y1), (bx0 - 14, BENCH_Y1)]),
       "Bench top", fill=lin((0, BENCH_Y0), (0, BENCH_Y1),
       (0, "#7A5628"), (0.6, "#5E3E1C"), (1, "#3A2610")),
       stroke=INK, strokeWidth=2.0, join="round")
# front edge band
d.path(poly([(bx0 - 14, BENCH_Y1), (bx1 + 14, BENCH_Y1), (bx1 + 14, BENCH_Y1 + 12),
             (bx0 - 14, BENCH_Y1 + 12)]),
       "Bench edge", fill=lin((0, BENCH_Y1), (0, BENCH_Y1 + 12),
       (0, "#4A3014"), (1, "#241606")), stroke=INK, strokeWidth=1.8, join="round")
# the pool of light on the bench
d.shape("ellipse", "Light pool", x=330, y=622, width=340, height=48,
        fill=rad((0, "#FFDC9A", 0.48), (0.55, "#E0A050", 0.22), (1, "#E0A050", 0)),
        stroke=NONE)

# bench props: a jar, a folded rag, a small stubby tool
# jar: glass cylinder catching the light
d.path("M566,584 L566,624 Q566,632 576,632 L600,632 Q610,632 610,624 L610,584 Z",
       "Jar", fill=lin((566, 0), (610, 0), (0, "#A8C8BC", 0.35), (0.45, "#E4F0E8", 0.55),
                       (0.7, "#9AB8AC", 0.3), (1, "#5E7E72", 0.4)),
       stroke=INK, strokeWidth=1.8, join="round")
d.shape("ellipse", "Jar mouth", x=566, y=578, width=44, height=12,
        fill=lin((566, 0), (610, 0), (0, "#4A5A50"), (0.5, "#8A9A8E"), (1, "#38473E")),
        stroke=INK, strokeWidth=1.6)
d.path("M570,590 L570,622", "Jar sheen", fill=NONE, stroke="#F0FAF4",
       strokeWidth=3.0, opacity=55, cap="round")
# folded rag: low soft lump left of the pool
rag = [(370, 632), (364, 622), (372, 612), (392, 606), (414, 608), (426, 616),
       (428, 626), (416, 634), (390, 636)]
d.path(smooth(rag), "Rag", fill=rad((0, "#A8B4BC"), (0.7, "#74808C"), (1, "#46505C")),
       stroke=INK, strokeWidth=1.8)
d.path(smooth([(378, 622), (394, 616), (412, 620)], closed=False), "Rag fold",
       fill=NONE, stroke="#38404A", strokeWidth=1.6, opacity=55, cap="round")
# a stubby tool handle lying in the light: driver with a brass collar
d.path("M462,640 L540,628 L542,636 L464,648 Z", "Tool",
       fill=lin((462, 640), (542, 632), (0, "#5E3A20"), (0.5, "#9A6E3A"), (1, "#3A2410")),
       stroke=INK, strokeWidth=1.4, join="round")
d.path("M540,628 L558,625 L560,632 L542,636 Z", "Tool collar",
       fill=lin((540, 0), (560, 0), (0, "#6A4A1E"), (0.5, "#D8AA58"), (1, "#4A3414")),
       stroke=INK, strokeWidth=1.2)

# --- the shade --------------------------------------------------------------------------
# socket + brass collar at the cord's foot
d.shape("rectangle", "Socket", x=AX - 13, y=326, width=26, height=26,
        fill=lin((AX - 13, 0), (AX + 13, 0), (0, "#2E2618"), (0.45, "#8A6E38"),
                (0.6, "#C8A050"), (1, "#241C0E")),
        stroke=INK, strokeWidth=1.6)
d.shape("ellipse", "Socket ring", x=AX - 15, y=342, width=30, height=8,
        fill=lin((AX - 15, 0), (AX + 15, 0), (0, "#3A2C14"), (0.5, "#D8AA58"), (1, "#2E2210")),
        stroke=INK, strokeWidth=1.2)

# enamel dome: warehouse shade, right-half profile socket -> rolled rim
EN_D, EN_L, EN_HI = "#0E2A20", "#2E6B4C", "#6FB088"
shade_profile = [(487, 352), (482, 356), (470, 362), (452, 372),
                 (432, 386), (416, 402), (406, 420), (402, 436),
                 (400, 446)]
d.path(lathe(shade_profile), "Shade",
       fill=lin((AX - 100, 0), (AX + 100, 0),
                (0, EN_D), (0.35, EN_L), (0.5, EN_HI), (0.65, EN_L), (1, EN_D)),
       stroke=INK, strokeWidth=2.4, join="round")
# enamel specular sweep on the dome's left shoulder
d.path("M416,420 C424,398 442,378 466,366", "Enamel gloss", fill=NONE,
       stroke="#C8E8D4", strokeWidth=6, opacity=38, cap="round")
d.path("M424,424 C431,406 446,388 466,378", "Enamel gloss 2", fill=NONE,
       stroke="#FFFFFF", strokeWidth=2.4, opacity=50, cap="round")
# rolled rim: a pale ring at the mouth
d.shape("ellipse", "Rim roll", x=AX - 100, y=438, width=200, height=18,
        fill=lin((AX - 100, 0), (AX + 100, 0), (0, "#12291E"), (0.5, "#4E8A66"), (1, "#0E2018")),
        stroke=INK, strokeWidth=1.8)
# the hot underside: white enamel mouth + bulb glow
d.shape("ellipse", "Shade mouth", x=AX - 92, y=440, width=184, height=26,
        fill=rad((0, "#FFF6E0"), (0.62, "#F0D8A0"), (1, "#B8884A")),
        stroke="#3A2A12", strokeWidth=1.4)
d.shape("ellipse", "Bulb", x=AX - 26, y=444, width=52, height=22,
        fill=rad((0, "#FFFDF4"), (1, "#FFD894")), stroke=NONE)
# bloom spilling out under the mouth
d.shape("ellipse", "Mouth bloom", x=AX - 120, y=436, width=240, height=80,
        fill=rad((0, "#FFE2A8", 0.36), (0.55, "#F0B060", 0.12), (1, "#F0B060", 0)),
        stroke=NONE)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("pendant extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F0E6CE", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C4B091", justify="center")
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


caption("PENDANT LAMP", "STEEL · ENAMEL · BRASS")
d.finish("pendant-lamp-V1R00")
