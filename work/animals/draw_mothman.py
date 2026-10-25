#!/usr/bin/env python3
"""Mothman — field plate V1R00. Point Pleasant, December 1967: a headless
winged figure perched on the eyebars of a suspension-bridge tower, wings
mantled like a high collar, two red eyes doing all the talking. The bridge
reads behind him — deck, tower, sagging main cables — and the river takes
the bottom of the disc on the rim arc, with a thin red glint under him.
River-town dusk, industrial murk on the horizon.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Mothman — Field Plate", 1000, 1000)

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
        fill=lin((0, 0), (0, 1000), (0, "#0A0D14"), (1, "#04060A")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#5A6A80", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin((0, 40), (0, 880), (0, "#1E2532"), (0.55, "#2C3244"),
                 (0.8, "#3A322C"), (1, "#14100C")),
        stroke="#0A0C12", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.74, "#000000", 0), (1, "#04060C", 0.55)),
        stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C6D0DC", strokeWidth=3, opacity=26)

# river-town murk: a low amber smear off to the left, sodium light
d.shape("ellipse", "Town glow", x=160, y=430, width=380, height=180,
        fill=rad((0, "#B4763C", 22), (0.6, "#8A5428", 8), (1, "#8A5428", 0)),
        stroke=NONE)
# faint stars, cold
for i, (x, y, s) in enumerate([(300, 200, 4), (640, 170, 3), (720, 260, 3.5),
                               (250, 300, 3), (560, 140, 3)]):
    ell(f"Star {i+1}", x, y, s, s, fill="#D8E0EA", opacity=30, stroke=NONE)

# --- river: chord y=640 closing on the disc arc ---------------------------------------
ch = 640
hch = math.sqrt(PR ** 2 - (ch - PCY) ** 2)
d.path(f"M{PCX - hch:.1f},{ch} L{PCX + hch:.1f},{ch} A{PR},{PR} 0 0 1 {PCX - hch:.1f},{ch} Z",
       "River", fill=lin((0, ch), (0, 880), (0, "#1A2232"), (0.5, "#101625"),
                         (1, "#070B14")), stroke=NONE)
# water shimmer: short horizontal dashes
for i, (x, y, w, op) in enumerate([(200, 668, 70, 26), (390, 684, 90, 22),
                                   (600, 676, 80, 24), (740, 700, 60, 20),
                                   (300, 730, 100, 16), (520, 742, 110, 15),
                                   (660, 770, 90, 13), (410, 800, 120, 11)]):
    line(f"River shimmer {i+1}", x, y, x + w, y, 2.5, "#5A6E8C", opacity=op)
# thin red glint in the water under the tower — the eyes, reflected
line("Eye glint on water", 298, 668, 298, 712, 4, "#B02424", opacity=32)
line("Eye glint far", 262, 676, 262, 700, 3, "#B02424", opacity=22)

# --- the bridge: left tower, deck, sagging main cable ----------------------------------
DK = "#12151C"
# deck band across the span
d.path("M138,566 L872,560 L872,572 L138,578 Z", "Bridge deck",
       fill=lin((0, 556), (0, 580), (0, "#232A36"), (1, DK)), stroke=NONE)
line("Deck edge light", 140, 566, 870, 560, 2.2, "#4A5668", opacity=40)
# tower: a real portal-frame pier — two legs, cap beam, mothman perches on top
tower = [(236, 452), (240, 428), (298, 428), (302, 452),
         (306, 566), (232, 568)]
d.path(smooth(tower), "Bridge tower", fill=lin((236, 0), (306, 0),
          (0, "#323C4C"), (0.5, "#1C222E"), (1, DK)), stroke=NONE)
# portal opening between the legs: darker void with a crossbar
d.path("M252,458 L286,458 L288,566 L250,566 Z", "Tower portal",
       fill="#0C1018", opacity=85, stroke=NONE)
line("Portal crossbar", 250, 512, 288, 512, 7, "#1E242E", opacity=90)
line("Tower cap light", 238, 430, 300, 430, 3.5, "#566274", opacity=45)
# main cable: anchored off-frame left, over the tower, sagging to midspan right
d.path(f"M140,470 Q210,452 258,436 Q400,480 560,538 Q720,576 872,562",
       "Main cable", fill=NONE, stroke="#1E242E", strokeWidth=4.5, cap="round")
d.path(f"M140,470 Q210,452 258,436", "Anchor cable", fill=NONE,
       stroke="#1E242E", strokeWidth=4.5, cap="round")
# suspenders: sparse verticals cable -> deck, right of the tower
for i, x in enumerate([340, 410, 480, 550, 620, 690, 760, 830]):
    t = (x - 258) / (872 - 258)
    cy = 436 + t * (562 - 436) + 60 * math.sin(t * math.pi) * 0.8
    line(f"Suspender {i+1}", x, cy - 4, x, 566 - t * 6, 2.6, "#1A2028", opacity=80)
# far tower ghost on the right edge, hazier
d.path(smooth([(816, 480), (822, 464), (836, 464), (842, 480), (844, 560), (814, 562)]),
       "Far tower", fill="#161C26", opacity=60, stroke=NONE)
d.path(f"M258,436 Q540,474 826,466", "Far cable", fill=NONE,
       stroke="#161C26", strokeWidth=3.5, cap="round", opacity=55)

# --- the mothman: perched on the tower cap ---------------------------------------------
# figure centre x=267; wings spread wide and drooping — a mantled cloak, not ears
FIG = "#1E1614"
FIG_EDGE = "#3E3228"
wingL = [(258, 304), (222, 278), (196, 262), (184, 272), (186, 300),
         (194, 332), (210, 360), (230, 380), (246, 368)]
wingR = [(276, 304), (312, 278), (338, 262), (350, 272), (348, 300),
         (340, 332), (324, 360), (304, 380), (288, 368)]
body = [(267, 452), (246, 448), (232, 428), (226, 398), (226, 356),
        (234, 330), (250, 316), (267, 310), (284, 316), (300, 330),
        (308, 356), (308, 398), (302, 428), (288, 448)]

# wings first (behind the body), slightly scalloped trailing edges
for nm, wpts in (("L", wingL), ("R", wingR)):
    ext(wpts)
    d.path(smooth(wpts), f"Wing {nm}",
           fill=lin((267, 170), (267, 320), (0, "#241A18"), (1, "#120C0A")),
           stroke=INK, strokeWidth=3, join="round")
    # folded primaries: long soft strokes fanning from the shoulder
    sx, sy = (254, 310) if nm == "L" else (280, 310)
    sgn = -1 if nm == "L" else 1
    for j, (ex, ey) in enumerate([(sx + sgn * 56, 278), (sx + sgn * 62, 310),
                                  (sx + sgn * 54, 344)]):
        d.path(f"M{sx},{sy} Q{(sx + ex) / 2},{(sy + ey) / 2 - 6} {ex},{ey}",
               f"Wing {nm} fold {j+1}", fill=NONE, stroke="#0E0806",
               strokeWidth=3.4, cap="round", opacity=55)

# body: broad shoulders melting into a headless column, perched on the cap
ext(body)
d.path(smooth(body), "Mothman body",
       fill=lin((0, 300), (0, 455), (0, "#2C201C"), (0.5, "#1E1614"), (1, "#0E0A08")),
       stroke=INK, strokeWidth=3, join="round")
# rim light on the town-lit left edge
d.path("M232,428 C228,398 230,360 240,336", "Left rim light", fill=NONE,
       stroke="#7A5A3C", strokeWidth=3.5, opacity=40, cap="round")
# chest fuzz suggestion: short broken strokes across the torso
for i, (x0, y0, x1, y1) in enumerate([(248, 352, 288, 356), (244, 380, 290, 384),
                                      (246, 408, 286, 410)]):
    line(f"Chest fuzz {i+1}", x0, y0, x1, y1, 3, "#0C0806", opacity=45)

# the eyes: bloom first, then the two coals
d.shape("ellipse", "Eye bloom", x=222, y=278, width=90, height=44,
        fill=rad((0, "#D83030", 34), (0.55, "#A81E1E", 12), (1, "#A81E1E", 0)),
        stroke=NONE)
ell("Eye L", 252, 298, 10, 6.5, fill=rad((0, "#F04838"), (1, "#B01818")),
    stroke="#5A0E0C", strokeWidth=1.5)
ell("Eye R", 282, 298, 10, 6.5, fill=rad((0, "#F04838"), (1, "#B01818")),
    stroke="#5A0E0C", strokeWidth=1.5)
ell("Eye glint L", 250, 296, 2.4, 2.0, fill="#FFD8C8", opacity=80, stroke=NONE)
ell("Eye glint R", 280, 296, 2.4, 2.0, fill="#FFD8C8", opacity=80, stroke=NONE)
# a faint red cast on the chest below the eyes
d.shape("ellipse", "Eye cast", x=244, y=310, width=46, height=26,
        fill=rad((0, "#C82828", 18), (1, "#C82828", 0)), stroke=NONE)

# feet gripping the tower cap: two talons over the edge
for i, x in enumerate((246, 288)):
    d.path(f"M{x},448 q-8,10 -4,18 q5,6 12,3", f"Foot {i+1}", fill=NONE,
           stroke=INK, strokeWidth=5, cap="round")

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("mothman extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#98A2B2", justify="center")
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


caption("MOTHMAN", "POINT PLEASANT · SILVER BRIDGE")
d.finish("mothman-V1R00")
