#!/usr/bin/env python3
"""Chandelier — field plate V1R00. Front view, symmetric: a gilt-brass
stem bolted to a ceiling canopy, six S-curved arms ending in candles,
bead swags sagging between the arm tips, crystal drops hanging off
every ledge and a big pendant under the stem. Crystal plate, ballroom
mood. 1000x1000, drawn in screen space.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Chandelier — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1C1420"   # warm dark, not black
EXTENT = []


def ext(x, y):
    EXTENT.append((x, y))
    return (x, y)


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


def quad(p0, p1, p2, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])


GIL_D, GIL_L = "#6A4A18", "#D8AE5E"     # gilt brass ramp
GIL_HI = "#F4DC9A"
CRY_D, CRY_L = "#7E96B4", "#E8F2FC"     # crystal ramp
FLM = "#FFE9A8"


def ellipse(name, cx, cy, w, h, fill, stroke=NONE, sw=1.5, opacity=None):
    kw = {}
    if opacity is not None:
        kw["opacity"] = opacity
    d.shape("ellipse", name, x=round(cx - w / 2), y=round(cy - h / 2),
            width=round(w), height=round(h), fill=fill, stroke=stroke,
            strokeWidth=sw, **kw)
    ext(cx - w / 2, cy - h / 2)
    ext(cx + w / 2, cy + h / 2)


def drop(name, cx, cy, s, fill=None, stroke="#DCEAF6", sw=1.6, opacity=None):
    """Crystal pendalogue: faceted kite — shoulder, waist, long point."""
    f = fill or lin((cx - s, cy), (cx + s, cy + 3.2 * s),
                    (0, CRY_L), (0.55, "#B8CCE2"), (1, CRY_D))
    kw = {}
    if opacity is not None:
        kw["opacity"] = opacity
    d.path(f"M{cx:.1f},{cy:.1f} L{cx + 0.85 * s:.1f},{cy + 0.9 * s:.1f} "
           f"L{cx:.1f},{cy + 3.1 * s:.1f} L{cx - 0.85 * s:.1f},{cy + 0.9 * s:.1f} Z",
           name, fill=f, stroke=stroke, strokeWidth=sw, join="round", **kw)
    ext(cx - s, cy)
    ext(cx + s, cy + 3.1 * s)


def sparkle(name, cx, cy, s, opacity=70):
    d.path(f"M{cx - s},{cy} L{cx + s},{cy} M{cx},{cy - s} L{cx},{cy + s}",
           name, fill=NONE, stroke="#FFFFFF", strokeWidth=1.6,
           opacity=opacity, cap="round")


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#141224"), (1, "#080612")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#7A6E9A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#524C6E"), (0.6, "#342E4A"), (1, "#181426")),
        stroke="#100C1C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8D4EC", strokeWidth=3, opacity=24)
# warm halo behind the fixture
d.shape("ellipse", "Ballroom glow", x=230, y=170, width=540, height=540,
        fill=rad((0, "#EFC88E", 16), (0.6, "#9A7E52", 6), (1, "#5E4A2E", 0)),
        stroke=NONE)

# ceiling chord: segment above CY_TOP, closing on the disc's own arc
CY_TOP = 148
tx = math.sqrt(PR ** 2 - (CY_TOP - PCY) ** 2)
d.path(f"M{PCX - tx:.1f},{CY_TOP} L{PCX + tx:.1f},{CY_TOP} "
       f"A420,420 0 0 0 {PCX - tx:.1f},{CY_TOP} Z",
       "Ceiling", fill=lin((0, 40), (0, CY_TOP), (0, "#0E0C1A", 78), (1, "#423A58", 30)),
       stroke=NONE)
d.path(f"M{PCX - tx + 6:.1f},{CY_TOP} L{PCX + tx - 6:.1f},{CY_TOP}", "Cornice line",
       fill=NONE, stroke="#CFC8E4", strokeWidth=2, opacity=16)

# ballroom floor far below + the fixture's light pool
FY = 742
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4E4662", 30), (1, "#120E1E", 70)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#D2CCE6", strokeWidth=2, opacity=16)
ellipse("Light pool", 500, 768, 340, 84,
        rad((0, "#EFC88E", 20), (0.6, "#9A7E52", 8), (1, "#5E4A2E", 0)))

# --- canopy + chain ------------------------------------------------------------------
ellipse("Canopy", 500, 152, 74, 22,
        lin((463, 140), (537, 164), (0, GIL_HI), (0.5, GIL_L), (1, GIL_D)),
        stroke=INK, sw=2.0)
ellipse("Canopy lip", 500, 160, 52, 12,
        lin((474, 154), (526, 166), (0, GIL_L), (1, GIL_D)), stroke=INK, sw=1.6)
# chain links: alternating orientation ellipses, drawn as interlocked rings
for i in range(4):
    cy = 172 + i * 13
    ellipse(f"Chain link {i+1}", 500, cy, 9, 14 if i % 2 == 0 else 8,
            NONE, stroke=GIL_L, sw=3.0)

# --- central stem ---------------------------------------------------------------------
d.path("M494,224 L494,596 L506,596 L506,224 Z", "Stem",
       fill=lin((494, 0), (506, 0), (0, GIL_D), (0.45, GIL_HI), (0.75, GIL_L), (1, GIL_D)),
       stroke=INK, strokeWidth=1.8, join="round")
# turned knops down the stem
for i, (cy, w, h) in enumerate([(236, 30, 16), (300, 40, 22), (368, 26, 14),
                                (452, 46, 26), (520, 58, 30), (560, 34, 18)]):
    ellipse(f"Knop {i+1}", 500, cy, w, h,
            lin((500 - w / 2, 0), (500 + w / 2, 0), (0, GIL_D), (0.5, GIL_HI), (1, GIL_D)),
            stroke=INK, sw=1.7)

# --- six arms, mirrored ---------------------------------------------------------------
# tips: (x offset, candle top y); arms leave the low knop, dip, then rise
TIPS = [(118, 452), (206, 436), (282, 462)]
for i, (dx, ty) in enumerate(TIPS):
    for sx in (-1, 1):
        tx_, ty_ = 500 + sx * dx, ty
        bx = 500 + sx * 26                    # root at the low knop
        # ribbon: upper edge and lower edge of one S-curve
        p0 = (bx, 528)
        c1 = (500 + sx * (dx * 0.55), 566)
        c2 = (500 + sx * (dx - 34), ty_ + 74)
        p1 = (tx_, ty_ + 30)
        # offset the curve ~4.5pt down for the lower edge
        q0 = (bx, 536)
        qc1 = (c1[0], c1[1] + 9)
        qc2 = (c2[0], c2[1] + 9)
        q1 = (tx_, ty_ + 38)
        d.path(f"M{p0[0]:.1f},{p0[1]:.1f} C{c1[0]:.1f},{c1[1]:.1f} "
               f"{c2[0]:.1f},{c2[1]:.1f} {p1[0]:.1f},{p1[1]:.1f} "
               f"L{q1[0]:.1f},{q1[1]:.1f} C{qc2[0]:.1f},{qc2[1]:.1f} "
               f"{qc1[0]:.1f},{qc1[1]:.1f} {q0[0]:.1f},{q0[1]:.1f} Z",
               f"Arm {i+1} {'LR'[sx > 0]}",
               fill=lin(p0, p1, (0, GIL_L), (0.5, GIL_HI), (1, GIL_D)),
               stroke=INK, strokeWidth=1.6, join="round")
        # curled flourish inside each arm bend
        d.path(f"M{bx + sx * 6:.1f},534 C{500 + sx * dx * 0.5:.1f},556 "
               f"{tx_ - sx * 40:.1f},{ty_ + 66:.1f} {tx_ - sx * 8:.1f},{ty_ + 34:.1f}",
               f"Arm vein {i+1} {'LR'[sx > 0]}", fill=NONE, stroke=GIL_HI,
               strokeWidth=1.4, opacity=55)
        # drip pan + candle + flame
        ellipse(f"Bobeche {i+1} {'LR'[sx > 0]}", tx_, ty_ + 30, 30, 10,
                lin((tx_ - 15, 0), (tx_ + 15, 0), (0, GIL_D), (0.5, GIL_HI), (1, GIL_D)),
                stroke=INK, sw=1.6)
        d.path(f"M{tx_ - 7:.1f},{ty_ + 30} L{tx_ - 7:.1f},{ty_} "
               f"L{tx_ + 7:.1f},{ty_} L{tx_ + 7:.1f},{ty_ + 30} Z",
               f"Candle {i+1} {'LR'[sx > 0]}",
               fill=lin((tx_ - 7, 0), (tx_ + 7, 0), (0, "#C8B890"), (0.5, "#F4ECD8"), (1, "#A89878")),
               stroke=INK, strokeWidth=1.4, join="round")
        # flame: teardrop + halo
        ellipse(f"Flame halo {i+1} {'LR'[sx > 0]}", tx_, ty_ - 16, 34, 34,
                rad((0, "#FFDFA0", 55), (1, "#F2A84E", 0)), stroke=NONE)
        d.path(f"M{tx_:.1f},{ty_ - 30} C{tx_ + 5:.1f},{ty_ - 22} {tx_ + 4:.1f},{ty_ - 12} "
               f"{tx_:.1f},{ty_ - 6} C{tx_ - 4:.1f},{ty_ - 12} {tx_ - 5:.1f},{ty_ - 22} "
               f"{tx_:.1f},{ty_ - 30} Z",
               f"Flame {i+1} {'LR'[sx > 0]}",
               fill=rad((0, "#FFF6D8"), (0.7, "#F2B65E"), (1, "#D8802A")), stroke=NONE)
        # crystal drop under each bobeche
        drop(f"Tip drop {i+1} {'LR'[sx > 0]}", tx_, ty_ + 38, 6)
        ext(tx_, ty_ - 34)

# --- bead swags between neighbouring tips ----------------------------------------------
tip_pts = [(500 - 282, 500), (500 - 206, 474), (500 - 118, 490),
           (500 + 118, 490), (500 + 206, 474), (500 + 282, 500)]
# anchor each swag at the drip pans (tip y + 34)
anchors = [(x, y + 34 - 8) for x, y in
           [(500 - 282, 462), (500 - 206, 436), (500 - 118, 452),
            (500 + 118, 452), (500 + 206, 436), (500 + 282, 462)]]
# stem-side swag anchors on the low knop
stem_lo, stem_hi = (500, 468), (500, 502)
swags = [(anchors[0], anchors[1], 26), (anchors[1], anchors[2], 24),
         (anchors[3], anchors[4], 24), (anchors[4], anchors[5], 26)]
for i, (a, b, sag) in enumerate(swags):
    mid = ((a[0] + b[0]) / 2, max(a[1], b[1]) + sag)
    n = int(math.hypot(b[0] - a[0], b[1] - a[1]) / 13)
    for j in range(n + 1):
        x, y = quad(a, mid, b, j / n)
        ellipse(f"Swag {i+1} bead {j+1}", x, y, 5, 5,
                rad((0, "#F4FAFE"), (1, "#8AA4C0")), stroke=NONE)
        if j in (1, n - 2):
            drop(f"Swag {i+1} drop {j}", x, y + 4, 4.5, opacity=92)
# swags from the outer tips up to the stem
for i, (a, sag) in enumerate([(anchors[0], 30), (anchors[5], 30)]):
    b = stem_lo if a[0] < 500 else stem_lo
    mid = ((a[0] + b[0]) / 2, max(a[1], b[1]) + sag)
    n = int(math.hypot(b[0] - a[0], b[1] - a[1]) / 13)
    for j in range(n + 1):
        x, y = quad(a, mid, b, j / n)
        ellipse(f"Stem swag {i+1} bead {j+1}", x, y, 5, 5,
                rad((0, "#F4FAFE"), (1, "#8AA4C0")), stroke=NONE)
    mx, my = quad(a, mid, b, 0.5)
    drop(f"Stem swag {i+1} drop", mx, my + 4, 5.5, opacity=95)

# --- crystal skirt: a ring of drops hung on threads under the arm roots -----------------
for i, ang in enumerate(range(-62, 63, 31)):
    a = math.radians(ang)
    cx = 500 + 150 * math.sin(a)
    cy = 566 + 26 * (1 - math.cos(a))
    d.path(f"M{cx:.1f},{cy - 6:.1f} L{cx:.1f},{cy + 17:.1f}", f"Skirt thread {i+1}",
           fill=NONE, stroke="#B8CCE2", strokeWidth=1.5, opacity=45)
    drop(f"Skirt drop {i+1}", cx, cy + 18, 6.5)

# --- bottom finial + the big pendant ----------------------------------------------------
ellipse("Bottom knop", 500, 606, 40, 18,
        lin((480, 0), (520, 0), (0, GIL_D), (0.5, GIL_HI), (1, GIL_D)),
        stroke=INK, sw=1.7)
drop("Grand pendant", 500, 616, 11)
sparkle("Pendant star", 506, 636, 7)

# sparkles only on crystals — a glint with nothing under it reads as a stray plus
for i, (sx_, sy_, ss) in enumerate([(224, 508, 6), (776, 508, 6), (706, 482, 5),
                                    (577, 602, 5), (430, 606, 5)]):
    sparkle(f"Glint {i+1}", sx_, sy_, ss, opacity=65)

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chandelier extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far


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
               color="#EDEAF8", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#AEA8CE", justify="center")
    d.cmd("text.setStyle", "Name tracking", id=n["id"], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", id=m["id"], tracking=260)
    doc = d.m.call("inspect_document", {})
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


caption("CHANDELIER", "GILT BRASS · CRYSTAL")
d.finish("chandelier-V1R00")
