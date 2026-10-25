#!/usr/bin/env python3
"""Irish elk — field plate V1R00. Twelve feet of antler carried into the
peat: a chest-up portrait, head tipped slightly right, the great palmate
rack spread across the upper disc like a second sky. Bog plate — spruce
dusk, standing water, sedge tufts, mist, floor chord on the arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Irish Elk — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E1410"   # warm near-black
EXTENT = []


def ext(pts):
    EXTENT.extend(pts)


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


def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(cx - rx, 1), y=round(cy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)


def line(name, x0, y0, x1, y1, w, color, **kw):
    return d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", name, fill=NONE,
                  stroke=color, strokeWidth=w, cap="round", **kw)


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#0C1412"), (1, "#04080A")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#5A7A6E", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin((0, 40), (0, 880), (0, "#2E4642"), (0.5, "#1E3230"),
                 (0.8, "#142424"), (1, "#0C1818")),
        stroke="#081210", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.74, "#000000", 0), (1, "#040A0A", 0.5)),
        stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BCCAC0", strokeWidth=3, opacity=24)

# dusk glow dying centre-left behind the rack
ell("Sky glow", 370, 330, 240, 140,
    fill=rad((0, "#8A6E50", 16), (1, "#8A6E50", 0)), stroke=NONE)
# far spruce spikes on the skyline, dim and small
for i, (x, w, h, op) in enumerate([(210, 30, 60, 30), (260, 22, 44, 24),
                                   (730, 26, 52, 28), (780, 20, 40, 22),
                                   (660, 16, 34, 18)]):
    d.path(f"M{x},{620} L{x + w / 2},{620 - h} L{x + w},{620} Z",
           f"Spruce {i+1}", fill="#101E1C", opacity=op, stroke=NONE)

# mist — two slow bands across the middle distance
ell("Mist band 1", 420, 560, 300, 26, fill="#9FB4AC", opacity=10, stroke=NONE)
ell("Mist band 2", 560, 610, 320, 22, fill="#9FB4AC", opacity=8, stroke=NONE)

# --- bog water: chord closing on the disc arc ------------------------------------------
ch = 668
hch = math.sqrt(PR ** 2 - (ch - PCY) ** 2)
d.path(f"M{PCX - hch:.1f},{ch} L{PCX + hch:.1f},{ch} A{PR},{PR} 0 0 1 {PCX - hch:.1f},{ch} Z",
       "Bog water", fill=lin((0, ch), (0, 880), (0, "#2E3A34"), (0.5, "#182420"),
                             (1, "#0A1410")), stroke=NONE)
# peat-dark island band along the waterline
d.path(f"M{PCX - hch + 6:.0f},{ch + 2} Q{PCX - 140},{ch - 8} {PCX + 30},{ch} "
       f"Q{PCX + 180},{ch + 6} {PCX + hch - 24:.0f},{ch + 1} "
       f"L{PCX + hch - 20:.0f},{ch + 16} Q{PCX},{ch + 30} {PCX - hch + 10:.0f},{ch + 14} Z",
       "Peat rim", fill="#141E18", opacity=85, stroke=NONE)
# water shimmer — the rack ghosted in the bog
for i, (x, y, w, op) in enumerate([(300, 700, 90, 20), (520, 714, 110, 18),
                                   (680, 700, 70, 16), (400, 746, 80, 14),
                                   (600, 762, 95, 12), (250, 730, 60, 13),
                                   (760, 750, 55, 11)]):
    line(f"Water streak {i+1}", x, y, x + w, y, 2.5, "#7A968C", opacity=op)
# pale reflection of the antlers right under the head — a few broken verticals
for i, (x, h, op) in enumerate([(452, 34, 18), (492, 44, 22), (532, 30, 16),
                                (570, 26, 12)]):
    line(f"Rack reflection {i+1}", x, 692, x + 4, 692 + h, 4, "#A89878", opacity=op)

# --- the rack — spread wide across the upper disc -----------------------------------------
ANT_GRAD = lin((500, 180), (500, 440), (0, "#D8C49A"), (0.6, "#A88A60"), (1, "#6E5236"))
ANT_DIM = lin((500, 180), (500, 440), (0, "#B09878"), (1, "#5E4630"))


def antler(side):
    """One palmate antler: beam, then a broad upright fan of blade. side=-1 left."""
    s = side
    def X(x):
        return PCX + s * (x - PCX)
    # beam — heavy arc from skull out to the palm base
    beam = [(X(478), 436), (X(444), 400), (X(402), 366), (X(372), 352),
            (X(366), 366), (X(396), 384), (X(432), 418), (X(468), 448)]
    d.path(smooth(beam), f"Beam {'L' if s < 0 else 'R'}",
           fill=ANT_DIM if s < 0 else ANT_GRAD, stroke=INK, strokeWidth=5)
    # palm — a broad upright fan, tines ringing the outer-upper edge
    palm = [(X(372), 362), (X(338), 376), (X(296), 380), (X(256), 368),
            (X(218), 346), (X(196), 312),                      # lower edge out
            (X(202), 274), (X(190), 240),                      # outer corner, tine 1
            (X(222), 244), (X(238), 208),                      # dip, tine 2
            (X(268), 218), (X(290), 192),                      # dip, tine 3
            (X(318), 210), (X(342), 198),                      # dip, tine 4
            (X(366), 226), (X(380), 292), (X(378), 342)]       # inner edge home
    d.path(smooth(palm), f"Palm {'L' if s < 0 else 'R'}",
           fill=ANT_DIM if s < 0 else ANT_GRAD, stroke=INK, strokeWidth=5)
    ext(palm)
    # palm finger ridges — soft grooves fanning through the blade
    for j, (x0, y0, x1, y1) in enumerate([(366, 330, 300, 330), (368, 312, 272, 288),
                                          (366, 292, 256, 250), (362, 272, 268, 224)]):
        line(f"Ridge {'L' if s < 0 else 'R'}-{j+1}", X(x0), y0, X(x1), y1,
             3, "#7A5E3E", opacity=45)
    # one brow tine — a small shovel spike dropped in front of the brow
    d.path(smooth([(X(468), 434), (X(452), 452), (X(448), 470),
                   (X(462), 472), (X(468), 454), (X(480), 440)]),
           f"Brow tine {'L' if s < 0 else 'R'}",
           fill=ANT_DIM if s < 0 else ANT_GRAD, stroke=INK, strokeWidth=4)


antler(-1)
antler(1)

# --- the stag: head + neck + shoulder hump, chest-up --------------------------------------
# ears first, tucked under the beam bases
for side in (-1, 1):
    d.path(smooth([(PCX + side * 44, 430), (PCX + side * 66, 420),
                   (PCX + side * 74, 434), (PCX + side * 60, 448),
                   (PCX + side * 46, 444)]),
           f"Ear {'L' if side < 0 else 'R'}", fill="#4E3A28", stroke=INK,
           strokeWidth=4)
    d.path(f"M{PCX + side * 50},436 Q{PCX + side * 62},430 {PCX + side * 68},434",
           f"Ear in {'L' if side < 0 else 'R'}", fill=NONE, stroke="#2E1E12",
           strokeWidth=2.5, opacity=70)

# neck + shoulders falling away to the water
chest = [(PCX - 60, 480), (PCX - 96, 540), (PCX - 120, 610), (PCX - 108, 668),
         (PCX - 40, 690), (PCX + 50, 690), (PCX + 116, 664), (PCX + 124, 606),
         (PCX + 98, 538), (PCX + 62, 480)]
d.path(smooth(chest), "Chest",
       fill=lin((500, 480), (500, 700), (0, "#4A3524"), (0.6, "#332216"),
                (1, "#1E140C")),
       stroke=INK, strokeWidth=6)
ext([(PCX - 120, 610), (PCX + 124, 606), (PCX - 40, 690), (PCX + 50, 690)])
# shoulder hump ridge — the elk's high withers
d.path(f"M{PCX - 60},496 Q{PCX - 10},512 {PCX + 62},500", "Hump ridge",
       fill=NONE, stroke="#5C442C", strokeWidth=5, opacity=55, cap="round")
# throat mane — darker run down the front
d.path(f"M{PCX - 8},492 Q{PCX - 14},560 {PCX - 6},660", "Throat mane",
       fill=NONE, stroke="#241812", strokeWidth=7, opacity=55, cap="round")

# head — long elk face tipped slightly right, muzzle down toward the water
head = [(PCX - 40, 466), (PCX - 50, 426), (PCX - 30, 404), (PCX + 2, 394),
        (PCX + 32, 400), (PCX + 54, 416), (PCX + 62, 444), (PCX + 60, 474),
        (PCX + 50, 496), (PCX + 30, 512), (PCX + 8, 516), (PCX - 14, 506),
        (PCX - 30, 488)]
d.path(smooth(head), "Head",
       fill=lin((460, 400), (560, 520), (0, "#5C422C"), (0.6, "#3E2A1A"),
                (1, "#281A10")), stroke=INK, strokeWidth=5.5)
ext(head)
# muzzle — dark heavy nose pad at the long face's end
d.path(smooth([(PCX + 32, 476), (PCX + 54, 472), (PCX + 62, 484),
               (PCX + 54, 500), (PCX + 36, 504), (PCX + 26, 490)]),
       "Muzzle", fill="#241812", opacity=80, stroke=NONE)
# nostril + mouth line
ell("Nostril", PCX + 50, 486, 4.5, 3.2, fill="#0E0806", opacity=90, stroke=NONE)
d.path(f"M{PCX + 32},498 Q{PCX + 46},504 {PCX + 56},496", "Mouth line",
       fill=NONE, stroke="#120C08", strokeWidth=3, opacity=70, cap="round")
# eyes — dark, level, calm
for side, exx in ((-1, PCX - 24), (1, PCX + 30)):
    ell(f"Eye {'L' if side < 0 else 'R'}", exx, 444, 6.5, 8, fill="#0E0806",
        stroke=NONE)
    ell(f"Eye glint {'L' if side < 0 else 'R'}", exx + 2, 441, 2.2, 2.2,
        fill="#D8E0D4", opacity=70, stroke=NONE)
# brow shading between the eyes
ell("Brow shade", PCX + 2, 432, 26, 12, fill="#1E140C", opacity=35, stroke=NONE)

# --- sedge: dark tufts rising from the waterline ------------------------------------------
def sedge(x, y, h, n, seed):
    for j in range(n):
        dx = (j - (n - 1) / 2) * (8 + seed % 4)
        lean = ((seed * 5 + j * 11) % 15 - 7) / 7.0
        d.path(f"M{x},{y} Q{x + dx * 0.4},{y - h * 0.55} {x + dx + lean * 9:.0f},{y - h:.0f}",
               f"Sedge {seed}-{j+1}", fill=NONE, stroke="#2E3A2A",
               strokeWidth=3.5, cap="round", opacity=85)


for k, (x, h, n) in enumerate([(215, 56, 6), (285, 40, 5), (360, 30, 4),
                               (640, 34, 4), (715, 50, 6), (790, 36, 5),
                               (845, 26, 4)]):
    assert on_disc(x, 668 - h, 14), k
    sedge(x, 674, h, n, k + 21)
# two cotton-grass heads — little pale puffs on thin stalks
for i, (x, h) in enumerate([(268, 96), (742, 88)]):
    assert on_disc(x, 668 - h, 16), i
    line(f"Cotton stalk {i+1}", x, 674, x + 4, 668 - h + 14, 3, "#3A4634", opacity=80)
    ell(f"Cotton head {i+1}", x + 4, 668 - h + 6, 9, 11,
        fill=rad((0, "#E8E4D8", 80), (1, "#E8E4D8", 0)), stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#081210", strokeWidth=6)

# --- extent check -------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("irish-elk extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 20, far


# --- caption ------------------------------------------------------------------------------
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
    n = d.text(name, "Name", x=500, y=932, size=58, font="Virelai Sans",
               color="#DED8C4", justify="center")
    m = d.text(mats, "Second line", x=500, y=970, size=22, font="Virelai Sans",
               color="#96A4A0", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=80)
    d.cmd("text.setStyle", "Second line tracking", ids=[m["id"]], tracking=240)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "second line")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" %
              (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "second line":
            assert b["width"] <= 760, b["width"]


caption("IRISH ELK", "MEGALOCEROS GIGANTEUS")
d.finish("irish-elk-V1R00")
