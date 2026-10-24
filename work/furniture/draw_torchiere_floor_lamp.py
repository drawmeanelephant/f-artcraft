#!/usr/bin/env python3
"""Torchiere floor lamp — field plate V1R00. Near-side view in a corner:
a stepped three-tier base, a slim bronzed pole with collar rings, an
upward-flared bowl with a hot alabaster liner, and the cone of glow it
throws up the walls to wash the ceiling. Deco plate — faint sunburst
rays inside the cone, a corner seam behind. 1000x1000.
Drawn in screen space as lathe profiles mirrored on the lamp axis.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Torchiere Floor Lamp — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
AX = 502            # lamp axis
INK = "#1E140E"     # warm dark, not black
EXTENT = []


def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


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


def lathe(profile):
    """Right-half profile [(x,y)...] bottom->top -> closed symmetric silhouette."""
    left = [(2 * AX - x, y) for x, y in reversed(profile)]
    for p in profile + left:
        EXTENT.append(p)
    return smooth(profile + left)


def mark(x, y):
    EXTENT.append((x, y))


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#14161A"), (1, "#07080B")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8A7A50", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#3E3C30"), (0.55, "#2A2820"), (1, "#12100A")),
        stroke="#0C0A06", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C890", strokeWidth=3, opacity=24)

# corner mood: the walls meet behind the lamp — a soft seam + tonal split
d.path("M508,84 L516,84 L524,708 L508,708 Z", "Corner shade",
       fill=lin((508, 0), (524, 0), (0, "#0A0A08", 0), (0.5, "#080706", 0.35),
                (1, "#080706", 0)), stroke=NONE)
d.path(f"M516,100 L520,700", "Corner seam", fill=NONE, stroke="#060503",
       strokeWidth=3.0, opacity=45)

# the light itself: ceiling wash, then the cone, then bowl bloom
d.shape("ellipse", "Ceiling wash", x=200, y=52, width=600, height=200,
        fill=rad((0, "#FFDC9A", 0.30), (0.55, "#E8A850", 0.10), (1, "#E8A850", 0)),
        stroke=NONE)
d.path("M424,262 L580,262 L688,74 L316,74 Z", "Light cone",
       fill=lin((502, 262), (502, 74), (0, "#FFCE84", 0.22), (0.55, "#F0A850", 0.09),
                (1, "#F0A850", 0.02)), stroke=NONE)
# deco sunburst rays inside the cone, fading up
RAYS = [(424, 262, 356, 104), (456, 258, 424, 88), (502, 254, 502, 76),
        (548, 258, 580, 88), (580, 262, 648, 104)]
for i, (x0, y0, x1, y1) in enumerate(RAYS):
    mark(x1, y1)
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Ray {i+1}", fill=NONE,
           stroke="#FFDC9A", strokeWidth=2.4, opacity=26, cap="round")
# faint ray fan echoed on the upper walls
for i, (x0, y0, x1, y1) in enumerate([(424, 262, 340, 136), (580, 262, 664, 136)]):
    mark(x1, y1)
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Wall ray {i+1}", fill=NONE,
           stroke="#F0C880", strokeWidth=1.8, opacity=14, cap="round")

# --- floor boards closing on the disc arc --------------------------------------------
FYB = 708
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX - hw:.1f},{FYB} L{PCX + hw:.1f},{FYB} A420,420 0 0 1 {PCX - hw:.1f},{FYB} Z",
       "Floor", fill=lin((0, FYB), (0, 880), (0, "#3C3628", 0.5),
                         (0.5, "#1E1A10", 0.75), (1, "#0C0806", 0.92)), stroke=NONE)
d.path(f"M{PCX - hw + 6:.1f},{FYB} L{PCX + hw - 6:.1f},{FYB}", "Floor edge light",
       fill=NONE, stroke="#D8C890", strokeWidth=2, opacity=16)
# skirting line where the walls meet the floor
d.path(f"M{PCX - hw + 2:.1f},{FYB - 14} L{PCX + hw - 2:.1f},{FYB - 14}",
       "Skirting", fill=NONE, stroke="#0A0806", strokeWidth=4, opacity=50)
# lamp shadow + faint upcast light on the floor
d.shape("ellipse", "Lamp shadow", x=396, y=682, width=212, height=34,
        fill=rad((0, "#030201", 0.7), (0.65, "#030201", 0.3), (1, "#030201", 0)),
        stroke=NONE)
d.shape("ellipse", "Floor catch", x=420, y=668, width=170, height=26,
        fill=rad((0, "#C8924A", 0.14), (1, "#C8924A", 0)), stroke=NONE)

# --- the lamp -------------------------------------------------------------------------
BR_D, BR_L = "#3A2410", "#B8863C"          # bronze ramp
BR_HI = "#F0C880"
ST_D, ST_L = "#1A1A1C", "#5A5852"          # blackened steel


def metal(y0, y1, dk=BR_D, lt=BR_L, hi=BR_HI):
    return lin((0, y0), (0, y1),
               (0, dk), (0.42, lt), (0.58, hi), (0.78, shade_(lt, dk, 0.5)), (1, dk))


def shade_(hex1, hex2, b):
    a = [int(hex1[i:i + 2], 16) for i in (1, 3, 5)]
    c = [int(hex2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (c[i] - a[i]) * b) for i in range(3))


# stepped base: three tiers shrinking upward (ziggurat foot)
base_profile = [(408, 700), (408, 692), (424, 686), (438, 680),
                (438, 674), (456, 668), (462, 660),
                (462, 654), (478, 648), (484, 640),
                (484, 634), (494, 628), (496, 618), (492, 610)]
d.path(lathe(base_profile), "Base", fill=metal(610, 700, ST_D, ST_L, "#9A9488"),
       stroke=INK, strokeWidth=2.2, join="round")
# tier edge lights
for i, (y, rx) in enumerate([(686, 30), (660, 40), (634, 44)]):
    d.shape("ellipse", f"Base tier light {i+1}", x=AX - rx, y=y - 3,
            width=2 * rx, height=6, fill=NONE, stroke="#C8BCA0",
            strokeWidth=1.8, opacity=30)

# pole: slim taper from the base neck to the bowl socket
pole_profile = [(492, 610), (494, 560), (495, 500), (496, 420), (497, 340)]
d.path(lathe(pole_profile), "Pole", fill=metal(340, 610),
       stroke=INK, strokeWidth=2.0, join="round")
# pole sheen
d.path("M495.5,600 C494,540 493.5,470 495,380", "Pole sheen", fill=NONE,
       stroke=BR_HI, strokeWidth=2.6, opacity=32, cap="round")
# collar rings on the pole: the deco beat
for i, (y, hw, hh) in enumerate([(556, 15, 7), (468, 13, 6), (392, 15, 7)]):
    d.shape("ellipse", f"Collar {i+1}", x=AX - hw, y=y, width=2 * hw, height=hh * 2,
            fill=lin((AX - hw, 0), (AX + hw, 0), (0, BR_D), (0.5, BR_HI), (1, BR_D)),
            stroke=INK, strokeWidth=1.4)
    d.shape("ellipse", f"Collar groove {i+1}", x=AX - hw, y=y + hh - 2,
            width=2 * hw, height=4, fill=NONE, stroke="#2A1808",
            strokeWidth=1.4, opacity=55)

# bowl: flared shade, bronze outside — profile runs socket out to the lip
bowl_profile = [(494, 342), (488, 336), (484, 330), (486, 322),
                (496, 312), (516, 302), (542, 296), (566, 292),
                (578, 288), (580, 280), (576, 274)]
d.path(lathe(bowl_profile), "Bowl", fill=metal(274, 342),
       stroke=INK, strokeWidth=2.2, join="round")
# flute lines on the bowl belly
for i, fx in enumerate([518, 538, 554]):
    fy = {518: 306, 538: 300, 554: 296}[fx]
    d.path(f"M{fx},{342 - (fx - 494) * 0.55:.1f} L{fx + 6},{fy}", f"Flute R{i+1}",
           fill=NONE, stroke="#241608", strokeWidth=1.8, opacity=45)
    lx = 2 * AX - fx
    d.path(f"M{lx},{342 - (fx - 494) * 0.55:.1f} L{lx - 6},{fy}", f"Flute L{i+1}",
           fill=NONE, stroke="#241608", strokeWidth=1.8, opacity=45)

# alabaster liner: the glowing inside of the bowl, sitting proud of the rim
d.shape("ellipse", "Liner", x=AX - 76, y=268, width=152, height=26,
        fill=rad((0, "#FFF2D4"), (0.6, "#F0C884"), (1, "#B87A34")),
        stroke="#6A4014", strokeWidth=1.6)
d.shape("ellipse", "Liner core", x=AX - 52, y=272, width=104, height=15,
        fill=rad((0, "#FFFDF4"), (1, "#FFD894")), stroke=NONE)
# bloom hovering just above the rim
d.shape("ellipse", "Rim bloom", x=AX - 110, y=236, width=220, height=70,
        fill=rad((0, "#FFE2A8", 0.42), (0.6, "#F0B060", 0.14), (1, "#F0B060", 0)),
        stroke=NONE)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("torchiere extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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


caption("TORCHIERE", "BRONZE · ALABASTER · STEEL")
d.finish("torchiere-floor-lamp-V1R00")
