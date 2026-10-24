#!/usr/bin/env python3
"""Camelback sofa — furniture field plate V1R00. Front-near view of a
Chippendale-style camelback: tight upholstered back sweeping up to a single
central hump, low outscrolled arms, a long tight seat, and exposed mahogany —
a serpentine show-wood rail with a carved shell and four cabriole legs on
ball-and-claw feet. Champagne damask on a warm umber plate, brass nailheads
where fabric meets wood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Camelback Sofa — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241209"   # warm umber, never black
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


# --- palette ----------------------------------------------------------------------
DAM_HI, DAM_MID, DAM_LO = "#F2E4C2", "#D4BA8C", "#9C8256"
DAM_DARK, DAM_CREASE = "#6E5A38", "#584628"
MAHOG = ((0, "#8A4A2E"), (0.35, "#5E2A16"), (0.7, "#7A3E22"), (1, "#2E130A"))
BRASS = rad((0, "#F4D890"), (0.6, "#A87828"), (1, "#5C3C10"))

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1D1815"), (1, "#0C0907")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#5C4A42", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#4E3A32"), (0.6, "#372720"), (1, "#1E1410")),
        stroke="#120C09", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C4B2", strokeWidth=3, opacity=22)
d.shape("ellipse", "Warm glow", x=180, y=140, width=540, height=520,
        fill=rad((0, "#F0C080", 15), (0.6, "#A06848", 5), (1, "#704038", 0)), stroke=NONE)

FY = 706
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4E3F3A", 34), (1, "#141010", 70)), stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E2D2C4", strokeWidth=2, opacity=18)

# --- rear legs: plain tapered backs, mostly in shadow -------------------------------
def rear_leg(cx, name):
    pts = [(cx - 8, 600), (cx + 8, 600), (cx + 6, 672), (cx + 10, 690),
           (cx - 10, 690), (cx - 6, 672)]
    d.path(smooth(pts, closed=True), name,
           fill=lin((cx - 10, 0), (cx + 10, 0), *MAHOG), stroke="#180A05",
           strokeWidth=2.5, join="round", opacity=60)
    EXTENT.extend([(cx - 10, 690), (cx + 10, 690)])


rear_leg(372, "Rear leg L")
rear_leg(628, "Rear leg R")

# --- shadow ------------------------------------------------------------------------
d.shape("ellipse", "Sofa shadow", x=210, y=662, width=580, height=56,
        fill=rad((0, "#060302", 62), (0.6, "#060302", 28), (1, "#060302", 0)), stroke=NONE)

# --- tight upholstered back: the hump -------------------------------------------------
# silhouette: up from left arm shoulder, steep rise, central hump, down to right arm
BACK = [(302, 560), (296, 480), (302, 430), (330, 402), (372, 372), (424, 352),
        (468, 344), (500, 342), (532, 344), (576, 352), (628, 372), (670, 402),
        (698, 430), (704, 480), (698, 560)]
d.path(smooth(BACK, closed=True), "Back",
       fill=lin((0, 345), (0, 560), (0, DAM_HI), (0.45, DAM_MID), (1, DAM_LO)),
       stroke=INK, strokeWidth=5, join="round")
EXTENT += BACK
# welt cord following the serpentine top edge
d.path(smooth(BACK[1:14]), "Back welt cord", fill=NONE, stroke="#584628",
       strokeWidth=5, cap="round")
d.path(smooth([(x, y - 3) for x, y in BACK[2:13]]), "Back welt light",
       fill=NONE, stroke="#FAEFD8", strokeWidth=2.2, cap="round", opacity=55)
# light pooling on the hump's left shoulder, shade at both ends
d.shape("ellipse", "Hump light", x=360, y=360, width=220, height=110,
        fill=rad((0, "#FCF4E2", 45), (1, "#FCF4E2", 0)), stroke=NONE)
d.shape("ellipse", "Back end shade L", x=290, y=430, width=80, height=140,
        fill=rad((0, DAM_DARK, 50), (1, DAM_DARK, 0)), stroke=NONE)
d.shape("ellipse", "Back end shade R", x=630, y=430, width=80, height=140,
        fill=rad((0, DAM_DARK, 55), (1, DAM_DARK, 0)), stroke=NONE)

# --- damask sprigs inside the back (stays inside the silhouette) ----------------------
def sprig(cx, cy, s, name, op=26):
    """Small four-point damask motif."""
    d.path(f"M{cx},{cy - s} C{cx + s * 0.4},{cy - s * 0.4} {cx + s * 0.4},{cy - s * 0.4} {cx + s},{cy} "
           f"C{cx + s * 0.4},{cy + s * 0.4} {cx + s * 0.4},{cy + s * 0.4} {cx},{cy + s} "
           f"C{cx - s * 0.4},{cy + s * 0.4} {cx - s * 0.4},{cy + s * 0.4} {cx - s},{cy} "
           f"C{cx - s * 0.4},{cy - s * 0.4} {cx - s * 0.4},{cy - s * 0.4} {cx},{cy - s} Z",
           name, fill="#8A7040", opacity=op, stroke=NONE)
    d.shape("ellipse", name + " dot", x=round(cx - s * 0.16), y=round(cy - s * 0.16),
            width=round(s * 0.32), height=round(s * 0.32), fill="#6E5A38", opacity=op + 12, stroke=NONE)


n = 0
for row, ys in enumerate([392, 434, 476, 518]):
    for col in range(7):
        cx = 348 + col * 51 + (26 if row % 2 else 0)
        cy = ys
        # keep motifs inside the back silhouette's rough bounds
        if 345 < cx < 655 and math.hypot(cx - 500, cy - 470) < 150:
            n += 1
            sprig(cx, cy, 11, f"Damask sprig {n}")

# --- arms: low outscrolled rolls -------------------------------------------------------
def arm(sgn):
    """Outscrolled arm: body column + scroll face + inner panel."""
    lbl = "L" if sgn < 0 else "R"
    xo, xi = (232, 336) if sgn < 0 else (768, 664)
    pts = [(xo + 8, 436), (xo + 2, 505), (xo + 10, 585), (xo + 24, 652),
           (xi - 20, 652), (xi - 4, 585), (xi + 0, 505), (xi - 4, 436)]
    d.path(smooth(pts, closed=True), f"Arm body {lbl}",
           fill=lin((xo, 0), (xi, 0), (0, "#DCC294"), (0.55, "#B09468"), (1, "#7A643C")),
           stroke=INK, strokeWidth=4.5, join="round")
    EXTENT.extend(pts)
    # inside arm face: wedge from under the scroll sloping down to the seat
    inn = [(xi - 4, 452), (xi + 0, 510), (xi - 6, 570), (xi - 22, 606),
           (xi - 36, 600), (xi - 26, 540), (xi - 26, 486)]
    d.path(smooth(inn, closed=True), f"Arm inner {lbl}",
           fill=lin((xi - 34, 0), (xi, 0),
                    (0, "#E8D4AA" if sgn < 0 else "#A8905E"), (1, "#C0A476" if sgn < 0 else "#7A643C")),
           stroke=INK, strokeWidth=3, join="round", opacity=96)
    # scroll face
    cx, cy, r = (xo + xi) / 2 + sgn * 6, 484, 48
    d.shape("ellipse", f"Scroll {lbl}", x=round(cx - r), y=round(cy - r * 0.94),
            width=round(2 * r), height=round(2 * r * 0.94),
            fill=rad((0, "#F2E4C2" if sgn < 0 else "#D4BA8C"), (0.55, "#C8AC7C"), (1, "#8A7040")),
            stroke=INK, strokeWidth=5)
    EXTENT.extend([(cx - r, cy - r), (cx + r, cy + r)])
    spir = []
    for k in range(44):
        t = k / 43 * 2.0 * math.pi
        rr = r * (0.76 - 0.64 * (k / 43))
        spir.append((cx + rr * math.cos(t - 0.4), cy + rr * 0.9 * math.sin(t - 0.4)))
    d.path(smooth(spir), f"Scroll spiral {lbl}", fill=NONE, stroke="#584628",
           strokeWidth=4.5, cap="round", opacity=80)
    d.path(smooth([(x - 2, y - 3) for x, y in spir]), f"Scroll spiral light {lbl}",
           fill=NONE, stroke="#FAEFD8", strokeWidth=2, cap="round", opacity=45)
    d.shape("ellipse", f"Scroll eye {lbl}", x=round(cx - 4), y=round(cy - 4), width=9, height=9,
            fill=rad((0, "#C8AC7C"), (1, "#6E5A38")), stroke=INK, strokeWidth=1.5)
    d.path(f"M{cx - r * 0.7:.0f},{cy - r * 0.62:.0f} A{r * 0.92:.0f},{r * 0.86:.0f} 0 0 1 {cx + r * 0.35:.0f},{cy - r * 0.85:.0f}",
           f"Scroll rim light {lbl}", fill=NONE, stroke="#FCF4E2", strokeWidth=4, cap="round", opacity=50)


arm(-1)
arm(1)

# --- tight seat ------------------------------------------------------------------------
seat = [(310, 568), (340, 548), (430, 540), (500, 538), (570, 540), (660, 548),
        (690, 568), (694, 604), (680, 632), (500, 642), (320, 632), (306, 604)]
d.path(smooth(seat, closed=True), "Seat",
       fill=lin((0, 538), (0, 642), (0, "#E8D4AA"), (0.5, "#C0A476"), (1, "#8A7040")),
       stroke=INK, strokeWidth=4.5, join="round")
EXTENT += seat
d.path(smooth([(x, y + 8) for x, y in seat[1:6]]), "Seat crown",
       fill=NONE, stroke="#FAEFD8", strokeWidth=8, cap="round", opacity=40)
d.path(smooth([seat[10], seat[9], seat[8]]), "Seat front welt",
       fill=NONE, stroke="#584628", strokeWidth=4, cap="round", opacity=80)
# deck shadow where the seat meets the back
d.shape("ellipse", "Seat deck shade", x=320, y=536, width=360, height=24,
        fill=rad((0, DAM_DARK, 55), (1, DAM_DARK, 0)), stroke=NONE)
# two seat sprigs
sprig(430, 586, 10, "Seat sprig L", 22)
sprig(572, 588, 10, "Seat sprig R", 22)

# --- cabriole legs with ball-and-claw feet ---------------------------------------------
def cabriole(cx, mirror, name):
    """S-curved leg: knee swells out, ankle sweeps back to a ball foot."""
    m = -1 if mirror else 1
    pts = [(cx - 12 * m, 648), (cx - 19 * m, 664), (cx - 22 * m, 678),
           (cx - 20 * m, 692), (cx - 14 * m, 702), (cx - 5 * m, 708),
           (cx + 8 * m, 708), (cx + 13 * m, 700), (cx + 14 * m, 682),
           (cx + 12 * m, 664), (cx + 9 * m, 648)]
    d.path(smooth(pts, closed=True), name,
           fill=lin((cx - 20, 0), (cx + 15, 0), *MAHOG), stroke="#180A05",
           strokeWidth=3, join="round")
    # knee highlight
    d.path(f"M{cx - 18 * m},668 C{cx - 21 * m},678 {cx - 18 * m},692 {cx - 9 * m},700",
           name + " knee light", fill=NONE, stroke="#C8825A", strokeWidth=3,
           cap="round", opacity=50)
    # ball-and-claw: sphere gripped by two talon arcs
    bx, by = cx + 2 * m, 714
    d.shape("ellipse", name + " ball", x=round(bx - 9), y=round(by - 9), width=18, height=16,
            fill=rad((0, "#9A5A36"), (0.6, "#5E2A16"), (1, "#2A1208")),
            stroke="#180A05", strokeWidth=2.5)
    d.path(f"M{bx - 10 * m},{by - 8} C{bx - 16 * m},{by - 2} {bx - 14 * m},{by + 4} {bx - 9 * m},{by + 7}",
           name + " claw", fill=NONE, stroke="#180A05", strokeWidth=3.5, cap="round")
    EXTENT.extend([(cx - 22, 708), (cx + 14, 708), (bx, by + 7)])


cabriole(326, False, "Leg front L")
cabriole(674, True, "Leg front R")


# --- exposed mahogany serpentine rail --------------------------------------------------
rail = [(284, 634), (400, 630), (500, 638), (600, 630), (716, 634),
        (722, 654), (702, 668), (500, 672), (298, 668), (278, 654)]
d.path(smooth(rail, closed=True), "Mahogany rail",
       fill=lin((0, 630), (0, 672), *MAHOG), stroke="#180A05", strokeWidth=4, join="round")
EXTENT += rail
# rail sheen and lower edge light
d.path("M300,642 L700,642", "Rail sheen", fill=NONE, stroke="#C8825A",
       strokeWidth=3.5, cap="round", opacity=45)
d.path("M310,662 L690,662", "Rail edge light", fill=NONE, stroke="#3E1E10",
       strokeWidth=3, cap="round", opacity=60)
# center shell carving on the rail
d.shape("ellipse", "Rail shell", x=480, y=636, width=40, height=26,
        fill=rad((0, "#A86038"), (0.7, "#5E2A16"), (1, "#3A1A0C")),
        stroke="#180A05", strokeWidth=2.5)
for i, a in enumerate([-2.4, -1.9, -1.3, -0.8]):
    d.path(f"M500,658 L{500 + 15 * math.cos(a):.0f},{644 + 12 * math.sin(a) + 12:.0f}",
           f"Shell rib {i+1}", fill=NONE, stroke="#2A1208", strokeWidth=2, cap="round", opacity=60)
# brass nailheads trimming fabric against the show wood
for i in range(15):
    x = 314 + i * 26.6
    d.shape("ellipse", f"Rail nail {i+1}", x=round(x - 3), y=628, width=6.4, height=6.4,
            fill=BRASS, stroke="#180A05", strokeWidth=1)

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("camelback extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 28, far


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
    n = d.text(name, "Name", x=500, y=934, size=56, font="Virelai Sans",
               color="#F0E6D8", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C4A88E", justify="center")
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


caption("CAMELBACK SOFA", "MAHOGANY · DAMASK · BRASS")
d.finish("camelback-sofa-V1R00")
