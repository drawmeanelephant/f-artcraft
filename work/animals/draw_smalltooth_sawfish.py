#!/usr/bin/env python3
"""Smalltooth sawfish — field plate V1R00. Estuary murk: Pristis pectinata
in profile swimming right, the long flat rostrum leading — a saw edged with
evenly spaced teeth — over a muddy bottom, light shafts dropping through
tannin-green water. Olive-brown back, pale ventral band, gill slits under
the head, pectoral flap swept back, dorsals far aft, small caudal.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Smalltooth Sawfish — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#140D0A"   # warm near-black
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


# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#0A0E0C"), (1, "#040705")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#5A6A56", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin((0, 40), (0, 880), (0, "#1E2A1E"), (0.45, "#2C3A28"),
                 (0.75, "#33341F"), (1, "#12100A")),
        stroke="#0A0C12", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.74, "#000000", 0), (1, "#040804", 0.55)),
        stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B4C4A8", strokeWidth=3, opacity=24)

# light shafts dropping through the water from upper right
for i, (x0, x1, y1, op) in enumerate([(560, 640, 700, 14), (660, 720, 660, 10),
                                      (470, 530, 640, 9)]):
    d.path(f"M{x0},110 L{x0 + 34},110 L{x1},{y1} L{x1 - 40},{y1} Z",
           f"Light shaft {i+1}",
           fill=lin((0, 110), (0, y1), (0, "#C8D89A", op), (1, "#C8D89A", 0)),
           stroke=NONE)
# suspended particles drifting in the murk
for i, (x, y, s) in enumerate([(300, 260, 4), (420, 200, 3), (560, 300, 3.5),
                               (680, 240, 3), (250, 400, 3.5), (740, 360, 4),
                               (360, 480, 3), (620, 480, 3), (480, 380, 4)]):
    ell(f"Mote {i+1}", x, y, s, s, fill="#C8D4A8", opacity=22, stroke=NONE)

# --- mud bottom: chord y=748 closing on the disc arc --------------------------------
ch = 748
hch = math.sqrt(PR ** 2 - (ch - PCY) ** 2)
d.path(f"M{PCX - hch:.1f},{ch} L{PCX + hch:.1f},{ch} A{PR},{PR} 0 0 1 {PCX - hch:.1f},{ch} Z",
       "Mud bottom",
       fill=lin((0, ch), (0, 880), (0, "#3A3222"), (0.5, "#221C12"),
                (1, "#0E0A06")), stroke=NONE)
line("Mud edge light", PCX - hch + 8, ch, PCX + hch - 8, ch, 3,
     "#6E6244", opacity=40)
# mud ripples + debris flecks
for i, (x, y, w) in enumerate([(260, 762, 50), (420, 776, 60), (600, 768, 55),
                               (730, 756, 44), (330, 800, 46), (540, 812, 52)]):
    line(f"Mud ripple {i+1}", x, y, x + w, y - 3, 4, "#14100A", opacity=60)
for i, (x, y, w) in enumerate([(370, 762, 14), (660, 784, 16), (300, 780, 12)]):
    line(f"Debris {i+1}", x, y, x + w, y - 6, 3, "#7A6A44", opacity=55)

# silt cloud stirred at the tail
d.shape("ellipse", "Silt cloud", x=160, y=560, width=160, height=110,
        fill=rad((0, "#6E6244", 22), (1, "#6E6244", 0)), stroke=NONE)

# --- the sawfish: profile swimming right, saw leading ----------------------------------
OLIVE_HI = "#7A7458"
OLIVE_MID = "#4E4A36"
OLIVE_LO = "#26241A"
CREAM = "#D8CCAC"

# caudal fin first, small and notched, upper lobe dominant (sawfish trait)
d.path(smooth([(252, 500), (214, 474), (208, 496), (226, 512), (210, 532),
               (236, 548), (254, 534)]),
       "Caudal",
       fill=lin((205, 474), (255, 548), (0, "#5A5440"), (1, "#201C12")),
       stroke=INK, strokeWidth=3, join="round")

# body: long ray-shark trunk — deep at the head (right), tapering smoothly
# aft into the tail peduncle (left), one continuous silhouette
body = [(252, 512), (296, 486), (360, 452), (430, 424), (500, 412),
        (548, 416), (578, 434), (588, 452), (584, 474), (562, 496),
        (516, 522), (448, 540), (378, 544), (314, 538), (266, 526)]
ext(body)
d.path(smooth(body), "Body",
       fill=lin((0, 412), (0, 544), (0, OLIVE_HI), (0.5, OLIVE_MID),
                (1, OLIVE_LO)),
       stroke=INK, strokeWidth=3, join="round")
# pale ventral band along the belly — countershading
d.path("M300,530 C380,548 480,544 556,504 C500,534 400,556 316,542 Z",
       "Ventral band", fill=CREAM, opacity=55, stroke=NONE)
# dorsal shading: darker cast down the spine
d.path("M296,486 C370,444 460,418 560,428 C470,420 380,448 306,494 Z",
       "Dorsal shade", fill="#1A1810", opacity=45, stroke=NONE)

# two dorsals far aft on the tail — swept triangles, not blobs
d.path(smooth([(318, 480), (296, 432), (312, 428), (340, 470), (336, 486)]),
       "Dorsal 1",
       fill=lin((0, 428), (0, 486), (0, "#5A5440"), (1, "#201C12")),
       stroke=INK, strokeWidth=3, join="round")
d.path(smooth([(268, 492), (252, 456), (266, 452), (288, 484), (284, 498)]),
       "Dorsal 2",
       fill=lin((0, 452), (0, 498), (0, "#4E4A36"), (1, "#1C1A12")),
       stroke=INK, strokeWidth=3, join="round")

# pectoral fin: the broad ray flap swept back under the head, translucent
pect = [(560, 496), (516, 520), (478, 556), (462, 592), (490, 608),
        (534, 588), (566, 548), (574, 514)]
ext(pect)
d.path(smooth(pect), "Pectoral fin",
       fill=lin((460, 496), (575, 608), (0, "#8A8462", 80), (1, "#3E3A28", 80)),
       stroke=INK, strokeWidth=3, join="round", opacity=85)
# faint ribs in the fin
for i, (x0, x1) in enumerate([(556, 500), (540, 512), (522, 526)]):
    d.path(f"M{x0},508 Q{(x0 + x1) / 2},552 {x1},596", f"Pect rib {i+1}",
           fill=NONE, stroke="#2A2618", strokeWidth=2.5, opacity=55, cap="round")
# pelvic fin: small flap further aft under the belly
d.path(smooth([(392, 534), (366, 558), (362, 582), (390, 586), (412, 562),
               (414, 542)]), "Pelvic fin",
       fill=lin((0, 534), (0, 586), (0, "#5E5A42"), (1, "#242018")),
       stroke=INK, strokeWidth=2.5, join="round")

# head top: eye + spiracle just behind, set on the flat of the head
ell("Eye", 556, 424, 8, 7, fill=rad((0, "#3E3A28"), (1, "#141210")),
    stroke=INK, strokeWidth=2)
ell("Eye glint", 553, 421, 2, 2, fill="#E8E4D0", opacity=80, stroke=NONE)
ell("Spiracle", 576, 430, 9, 5, fill="#1C1A12", opacity=80, stroke=NONE)
# five gill slits under the head
for i in range(5):
    x = 500 + i * 14
    d.path(f"M{x},492 Q{x + 3},504 {x + 1},516", f"Gill slit {i+1}",
           fill=NONE, stroke="#14120C", strokeWidth=3, opacity=75, cap="round")

# the rostrum: long flat blade leading right, tapering slightly
rostrum = [(584, 434), (630, 420), (720, 420), (780, 426), (784, 438),
           (726, 448), (636, 450), (588, 458)]
ext(rostrum)
d.path(smooth(rostrum), "Rostrum",
       fill=lin((0, 420), (0, 458), (0, "#8A8468"), (0.55, "#5E5A42"),
                (1, "#2E2A1E")),
       stroke=INK, strokeWidth=3, join="round")
# pale lateral ridge down the blade
line("Rostrum ridge", 606, 438, 770, 436, 3, "#B8AE8A", opacity=50)

# saw teeth: evenly spaced triangles on both edges — the smalltooth's even rank
NX = 11
for side, (edge_y, diry) in enumerate(((422, -1), (448, 1))):
    for i in range(NX):
        t = i / (NX - 1)
        bx = 622 + t * 146          # teeth stop short of tip and base
        by = edge_y - t * 1.5       # follow the slight taper
        hgt = 11 - t * 3            # shorter toward the tip
        w = 9                       # base width of the tooth
        pts = [(bx, by), (bx + w, by),
               (bx + w * 0.55, by + diry * hgt)]
        d.path(f"M{bx:.1f},{by:.1f} L{bx + w:.1f},{by:.1f} "
               f"L{bx + w * 0.55:.1f},{by + diry * hgt:.1f} Z",
               f"Tooth {'T' if side == 0 else 'B'}{i+1}",
               fill="#E4DABE", stroke=INK, strokeWidth=1.2, join="round")
        ext([(bx + w * 0.5, by + diry * hgt)])

# ventral mouth: small arc under the head base
d.path("M540,478 Q562,486 582,476", "Mouth", fill=NONE, stroke="#14110B",
       strokeWidth=4, opacity=80, cap="round")

# water-light rim along the spine
d.path("M300,478 C380,434 470,412 552,420", "Spine light", fill=NONE,
       stroke="#A8B078", strokeWidth=3.5, opacity=40, cap="round")

# soft shadow under the fish on the water column
d.shape("ellipse", "Fish shade", x=340, y=580, width=340, height=60,
        fill=rad((0, "#000000", 30), (1, "#000000", 0)), stroke=NONE)

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("sawfish extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far


# --- caption ---------------------------------------------------------------------------
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
               color="#E8E4DA", justify="center")
    m = d.text(mats, "Second line", x=500, y=970, size=22, font="Virelai Sans",
               color="#A0AC94", justify="center")
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


caption("SMALLTOOTH SAWFISH", "PRISTIFORMES · PRISTIS PECTINATA")
d.finish("smalltooth-sawfish-V1R00")
