#!/usr/bin/env python3
"""White-nosed coati — field plate V1R00. Costa Rican forest floor: Nasua
narica in profile facing left, long flexible snout down in the leaf litter,
white muzzle and eye-rings against umber fur, darker feet, the long ringed
tail held upright in a loose curl. Muted teal disc, a shaft of green-gold
canopy light. All four feet grounded inside the rim.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("White-Nosed Coati — Field Plate", 1000, 1000)

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


def sample_poly(pts, t):
    """Point and unit tangent at fraction t along a polyline."""
    seg = []
    total = 0.0
    for i in range(len(pts) - 1):
        L = math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
        seg.append(L)
        total += L
    want = t * total
    for i, L in enumerate(seg):
        if want <= L or i == len(seg) - 1:
            f = 0 if L == 0 else want / L
            x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f
            y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f
            tx = (pts[i + 1][0] - pts[i][0]) / L
            ty = (pts[i + 1][1] - pts[i][1]) / L
            return (x, y), (tx, ty)
        want -= L


def tail_outline(pts, hw):
    """Closed outline for a tapered curved tail: offsets along normals."""
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1
        nx, ny = -ty / L, tx / L
        left.append((x + nx * hw[i], y + ny * hw[i]))
        right.append((x - nx * hw[i], y - ny * hw[i]))
    return left + right[::-1]


def band_hw(hw, npts, t):
    return hw[0] + (hw[-1] - hw[0]) * t


# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#0B0F12"), (1, "#05070A")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#4E6A62", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin((0, 40), (0, 880), (0, "#14201F"), (0.5, "#20362F"),
                 (0.78, "#2A3226"), (1, "#12100B")),
        stroke="#0A0C12", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.74, "#000000", 0), (1, "#040805", 0.55)),
        stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8CCC4", strokeWidth=3, opacity=24)

# canopy light: a green-gold shaft upper-left, plus a couple of dust motes
d.shape("ellipse", "Canopy light", x=220, y=180, width=380, height=300,
        fill=rad((0, "#8A9450", 20), (0.6, "#6E7A40", 7), (1, "#6E7A40", 0)),
        stroke=NONE)
for i, (x, y, s) in enumerate([(300, 260, 4), (360, 330, 3), (430, 230, 3.5),
                               (520, 300, 3), (610, 210, 3)]):
    ell(f"Mote {i+1}", x, y, s, s, fill="#C8D8B8", opacity=26, stroke=NONE)

# forest shade behind the animal: darker mass low in the disc
d.shape("ellipse", "Deep shade", x=560, y=420, width=460, height=260,
        fill=rad((0, "#06100C", 55), (1, "#06100C", 0)), stroke=NONE)

# --- forest floor: chord y=712 closing on the disc arc ------------------------------
ch = 712
hch = math.sqrt(PR ** 2 - (ch - PCY) ** 2)
d.path(f"M{PCX - hch:.1f},{ch} L{PCX + hch:.1f},{ch} A{PR},{PR} 0 0 1 {PCX - hch:.1f},{ch} Z",
       "Forest floor",
       fill=lin((0, ch), (0, 880), (0, "#2E2A1E"), (0.5, "#1C1810"),
                (1, "#0C0A06")), stroke=NONE)
line("Floor edge light", PCX - hch + 8, ch, PCX + hch - 8, ch, 3,
     "#6E6444", opacity=40)

# leaf litter: scattered fallen leaves on the floor line, ochre and rust
LEAVES = [
    (240, 726, 26, 10, "#7A5A30", 80), (310, 738, 30, 12, "#8A6A38", 75),
    (392, 730, 24, 9, "#6E4E2C", 80), (470, 742, 28, 11, "#7E6034", 78),
    (560, 736, 26, 10, "#6A4E2E", 80), (640, 744, 30, 12, "#8A6A38", 72),
    (716, 730, 24, 9, "#5E4228", 80), (772, 748, 26, 10, "#7A5A30", 70),
    (350, 758, 24, 9, "#5E4228", 75), (610, 766, 26, 10, "#6E4E2C", 72),
]
for i, (x, y, rx, ry, c, op) in enumerate(LEAVES):
    pts = [(x - rx, y), (x - rx * 0.3, y - ry), (x + rx * 0.4, y - ry * 0.7),
           (x + rx, y), (x + rx * 0.3, y + ry), (x - rx * 0.4, y + ry * 0.6)]
    d.path(smooth(pts), f"Leaf {i+1}", fill=c, opacity=op,
           stroke=INK, strokeWidth=1.5)

# --- the coati: profile facing left, nose to the litter ------------------------------
UM_HI = "#7A5638"
UM_MID = "#4A3020"
UM_LO = "#241610"
CREAM = "#E8DCC4"
FOOT = "#18100C"

# tail first (behind body): upright loose curl, tapering, ringed
tp = [(672, 506), (726, 446), (756, 366), (746, 292), (700, 252), (652, 256)]
thw = [24, 22, 19, 16, 12, 7]
ext(tp)
d.path(smooth(tail_outline(tp, thw)), "Tail",
       fill=lin((660, 250), (760, 500), (0, "#8A6644"), (0.5, "#5A3E28"),
                (1, "#2A1A10")),
       stroke=INK, strokeWidth=3, join="round")
# rings: pale bands across the tail
for i, t in enumerate((0.16, 0.32, 0.48, 0.64, 0.8, 0.93)):
    (x, y), (tx, ty) = sample_poly(tp, t)
    hw = band_hw(thw, len(tp), t) - 1.5
    nx, ny = -ty, tx
    line(f"Tail ring {i+1}", x - nx * hw, y - ny * hw, x + nx * hw, y + ny * hw,
         15, "#C8B490", opacity=72)

# far legs first, darker (all four feet on the ground at y~716)
d.path("M508,606 L502,660 L500,700 L488,712 L514,712 L518,700 L522,646 Z",
       "Far front leg", fill="#221409", opacity=95,
       stroke=INK, strokeWidth=2.5, join="round")
d.path("M618,612 L606,664 L604,700 L592,712 L618,712 L624,698 L634,648 Z",
       "Far rear leg", fill="#221409", opacity=95,
       stroke=INK, strokeWidth=2.5, join="round")

# body: long low trunk, slight arch over the shoulders, rooting stance
body = [(400, 560), (436, 520), (492, 498), (560, 492), (622, 498),
        (668, 512), (686, 540), (678, 584), (650, 630), (600, 656),
        (540, 664), (478, 656), (432, 632), (406, 598)]
ext(body)
d.path(smooth(body), "Body",
       fill=lin((400, 490), (690, 660), (0, UM_HI), (0.5, UM_MID), (1, UM_LO)),
       stroke=INK, strokeWidth=3, join="round")
# grizzled dorsal sheen: pale guard-hair wash along the back
d.path("M440,522 C500,498 580,494 650,512 C590,508 510,512 448,536 Z",
       "Dorsal sheen", fill="#B09468", opacity=38, stroke=NONE)
# belly shade
d.shape("ellipse", "Belly shade", x=470, y=592, width=210, height=80,
        fill=rad((0, "#140C08", 40), (1, "#140C08", 0)), stroke=NONE)

# near legs over the body bottom, dark feet, claws ticked
for nm, pts, foot in (
    ("Near front leg", [(452, 590), (446, 640), (444, 688), (436, 700),
                        (438, 712), (466, 712), (470, 690), (472, 640),
                        (474, 600)], (436, 700, 466, 712)),
    ("Near rear leg", [(636, 596), (662, 630), (664, 668), (656, 692),
                       (646, 700), (648, 712), (676, 712), (678, 690),
                       (676, 648), (662, 606)], (648, 700, 676, 712)),
):
    ext(pts)
    d.path(smooth(pts), nm,
           fill=lin((0, 590), (0, 712), (0, "#3A2414"), (1, FOOT)),
           stroke=INK, strokeWidth=3, join="round")
# claws on the near feet
for i, x in enumerate((442, 452, 462)):
    line(f"Front claw {i+1}", x, 712, x - 3, 716, 2.5, "#0A0604", opacity=90)
for i, x in enumerate((654, 664, 674)):
    line(f"Rear claw {i+1}", x, 712, x - 3, 716, 2.5, "#0A0604", opacity=90)

# neck into the lowered head, rooting down-left
neck = [(400, 560), (374, 566), (354, 588), (352, 612), (370, 628),
        (396, 626), (414, 604), (420, 578)]
ext(neck)
d.path(smooth(neck), "Neck",
       fill=lin((350, 560), (420, 640), (0, "#5E4028"), (1, "#2A1A10")),
       stroke=INK, strokeWidth=3, join="round")

# head + the long mobile snout: separate shape, white muzzle markings
head = [(366, 560), (340, 556), (312, 566), (290, 590), (276, 616),
        (278, 636), (296, 646), (322, 646), (350, 636), (372, 612),
        (382, 584)]
ext(head)
d.path(smooth(head), "Head",
       fill=lin((280, 556), (380, 646), (0, "#6A4A2E"), (0.6, "#42291A"),
                (1, "#241610")),
       stroke=INK, strokeWidth=3, join="round")
# white muzzle: the namesake blaze wrapping the snout tip
muzzle = [(286, 590), (276, 614), (278, 636), (296, 646), (316, 644),
          (310, 624), (306, 602)]
d.path(smooth(muzzle), "White muzzle", fill=CREAM, opacity=92,
       stroke=INK, strokeWidth=2.5, join="round")
# nose pad at the very tip
ell("Nose", 283, 622, 9, 12, fill="#100A06", stroke=NONE)
# white eye-rings above and below the eye
ell("Eye ring hi", 348, 576, 13, 9, fill=CREAM, opacity=80, stroke=NONE)
ell("Eye", 346, 582, 7, 7, fill="#0E0A06", stroke=INK, strokeWidth=2)
ell("Eye glint", 344, 579, 2, 2, fill="#FFFFFF", opacity=85, stroke=NONE)
ell("Eye ring lo", 344, 596, 10, 6, fill=CREAM, opacity=55, stroke=NONE)
# small rounded ear on top
d.path(smooth([(368, 556), (374, 538), (390, 534), (398, 548), (390, 562)]),
       "Ear", fill="#4E3220", stroke=INK, strokeWidth=3, join="round")
ell("Ear inner", 385, 548, 6, 5, fill="#1E120A", opacity=80, stroke=NONE)
# cheek blaze
line("Cheek blaze", 322, 566, 338, 560, 5, CREAM, opacity=50)

# canopy rim light along the back
d.path("M446,516 C510,496 590,492 656,510", "Back rim light", fill=NONE,
       stroke="#A89458", strokeWidth=3.5, opacity=40, cap="round")

# contact shadow under the feet
d.shape("ellipse", "Foot shadow", x=420, y=706, width=270, height=16,
        fill=rad((0, "#000000", 55), (1, "#000000", 0)), stroke=NONE)
# a leaf flipped up by the rooting snout, touching the muzzle tip
d.path(smooth([(262, 634), (278, 624), (298, 630), (294, 648), (274, 652)]),
       "Nosed leaf", fill="#8A6A38", opacity=85,
       stroke=INK, strokeWidth=1.5)

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("coati extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#9AA89E", justify="center")
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


caption("WHITE-NOSED COATI", "NASUA NARICA")
d.finish("white-nosed-coati-V1R00")
