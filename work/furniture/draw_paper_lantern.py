#!/usr/bin/env python3
"""Paper lantern — field plate V1R00. A hanging festival ball: a wire rib
cage skinned in rice paper, a low flame inside breathing warm light through
the skin, bamboo mouth and base rings, a cord up out of the light and a red
tassel below. Rice-paper plate, festival mood — warm glow against a night
dark. 1000x1000. Screen-space construction like the other lit subjects.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Paper Lantern — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A1008"   # warm dark, not black
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
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


# --- backdrop + rice-paper plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#0B0E16"), (1, "#04050A")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#C8A668", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#EBDDB6"), (0.55, "#D3C196"), (0.85, "#A99066"), (1, "#7A6440")),
        stroke="#4A3A22", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#8A6E44", strokeWidth=3, opacity=30)
# rice-paper fibres: a handful of faint short strokes on the disc
for i, (x0, y0, x1, y1) in enumerate([(220, 300, 262, 312), (730, 200, 762, 216),
                                      (250, 640, 288, 654), (690, 700, 726, 692),
                                      (170, 470, 208, 478), (780, 520, 818, 512),
                                      (420, 160, 452, 172), (560, 760, 596, 752)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Fibre {i+1}", fill=NONE,
           stroke="#7A6240", strokeWidth=1.4, opacity=10, cap="round")
# festival bokeh: soft far-off lights on the paper dark
for i, (bx, by, br, bo) in enumerate([(296, 208, 13, 26), (714, 250, 17, 22),
                                      (646, 168, 9, 28), (372, 164, 8, 20),
                                      (762, 420, 10, 16), (248, 380, 8, 14)]):
    assert math.hypot(bx - PCX, by - PCY) < PR - 40
    d.shape("ellipse", f"Bokeh {i+1}", x=bx - br, y=by - br, width=2 * br, height=2 * br,
            fill=rad((0, "#F0A840", bo), (0.6, "#D07828", bo // 2), (1, "#D07828", 0)),
            stroke=NONE)

# the lantern's own light pooling on the paper behind it
d.shape("ellipse", "Lantern light pool", x=280, y=230, width=440, height=420,
        fill=rad((0, "#F0A040", 30), (0.5, "#D87A28", 12), (1, "#C06018", 0)),
        stroke=NONE)

FY = 800
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#6A5638", 40), (1, "#2A1E10", 70)),
       stroke=NONE)
# soft cast shadow the hanging lantern throws below-right
d.shape("ellipse", "Lantern cast shadow", x=500, y=782, width=240, height=34,
        fill=rad((0, "#1E1408", 55), (0.65, "#1E1408", 24), (1, "#1E1408", 0)),
        stroke=NONE)

# --- geometry ---------------------------------------------------------------------------
LX, LY = 500, 430          # body centre
RX, RY = 188, 170          # body radii
RIB_V = [-0.80 + i * 0.16 for i in range(11)]   # rib rows, normalised


def rib_span(v):
    """Half-chord of the body ellipse at normalised height v."""
    return RX * math.sqrt(max(0.0, 1 - v * v))


# hanging cord first: it must sit behind the body glow edges
cord = [(500, LY - RY + 2), (503, LY - RY - 40), (512, LY - RY - 95), (524, LY - RY - 140)]
for p in cord:
    EXTENT.append(p)
d.path(smooth(cord), "Hanging cord", fill=NONE, stroke="#1E1410", strokeWidth=3.2,
       cap="round")
# wire bail over the mouth ring
bail = [P for P in [(476, LY - RY + 8), (488, LY - RY - 18), (500, LY - RY - 24),
                    (512, LY - RY - 18), (524, LY - RY + 8)]]
d.path(smooth(bail), "Wire bail", fill=NONE, stroke="#241812", strokeWidth=3.4,
       cap="round")

# paper skin: silhouette with a small pillow between rib rows and pinched poles
pts = []
for i in range(72):
    a = math.tau * i / 72
    v = math.sin(a)
    # nearest rib distance -> pillow bump between rows
    dmin = min(abs(v - r) for r in RIB_V)
    band = max(0.0, 1 - dmin / 0.09)
    pinch = 1 - 0.05 * abs(v) ** 6
    r = (1 + 0.022 * band * band) * pinch
    pts.append((LX + RX * r * math.cos(a), LY + RY * r * v))
for p in pts:
    EXTENT.append(p)
d.path(smooth(pts, closed=True), "Paper skin",
       fill=rad((0, "#FFD98C"), (0.35, "#F09A40"), (0.7, "#D05420"), (1, "#8A2C12")),
       stroke=INK, strokeWidth=2.4, join="round")
# inner flame: the breath of light, low centre
d.shape("ellipse", "Flame heart", x=LX - 90, y=LY + 10, width=180, height=150,
        fill=rad((0, "#FFF0C0", 70), (0.55, "#FFC060", 30), (1, "#FFC060", 0)),
        stroke=NONE)
# paper grain: two long translucent strokes on the skin
d.path(f"M{LX - 120},{LY - 60} q-30,60 -6,140", "Skin fibre L", fill=NONE,
       stroke="#FBE6B8", strokeWidth=6, opacity=12, cap="round")
d.path(f"M{LX + 96},{LY - 90} q26,70 8,160", "Skin fibre R", fill=NONE,
       stroke="#8A2C12", strokeWidth=5, opacity=10, cap="round")

# ribs: front arcs of each hoop, darker where the light thins at the edge
for i, v in enumerate(RIB_V):
    w = rib_span(v)
    if w < 24:
        continue
    y = LY + v * RY
    arc = [(LX - w * 0.985, y), (LX - w * 0.55, y + w * 0.075),
           (LX, y + w * 0.10), (LX + w * 0.55, y + w * 0.075), (LX + w * 0.985, y)]
    edge = abs(v)
    op = 30 + int(34 * edge)
    d.path(smooth(arc), f"Rib {i+1}", fill=NONE, stroke="#4A1408",
           strokeWidth=2.6, opacity=op, cap="round")
    EXTENT.extend(arc)

# painted guard bands near the caps
for nm, v0, v1, op in (("Top guard", -0.93, -0.84, 55), ("Bottom guard", 0.84, 0.93, 55)):
    # filled band between two latitude arcs
    top_e = [(LX - rib_span(v0) * math.cos(math.pi * j / 24), LY + v0 * RY)
             for j in range(25)]
    bot_e = [(LX - rib_span(v1) * math.cos(math.pi * j / 24), LY + v1 * RY)
             for j in range(25)]
    d.path(smooth(top_e + bot_e[::-1], closed=True), nm, fill="#5A1808",
           stroke=NONE, opacity=op)

# --- mouth + base rings: turned bamboo ---------------------------------------------------
def ring_cap(nm, cy, rw, rh):
    d.shape("ellipse", f"{nm} rim", x=round(LX - rw), y=round(cy - rh / 2),
            width=round(2 * rw), height=round(rh),
            fill=lin((LX - rw, cy), (LX + rw, cy), (0, "#3A2410"), (0.45, "#8A6234"),
                     (0.6, "#B0824E"), (1, "#2E1C0C")), stroke=INK, strokeWidth=1.8)
    d.shape("ellipse", f"{nm} dark", x=round(LX - rw * 0.72), y=round(cy - rh * 0.18),
            width=round(rw * 1.44), height=round(rh * 0.42), fill="#1E1208",
            opacity=70, stroke=NONE)


ring_cap("Mouth ring", LY - RY + 4, 56, 26)
ring_cap("Base ring", LY + RY - 4, 46, 22)

# --- tassel: cord, knot, red brush -------------------------------------------------------
tc = [(500, LY + RY + 8), (501, LY + RY + 26), (500, LY + RY + 44)]
for p in tc:
    EXTENT.append(p)
d.path(smooth(tc), "Tassel cord", fill=NONE, stroke="#1E1410", strokeWidth=2.6,
       cap="round")
d.shape("ellipse", "Tassel knot", x=494, y=LY + RY + 40, width=13, height=12,
        fill=rad((0, "#B03020"), (1, "#5A1408")), stroke=INK, strokeWidth=1.4)
brush = [(500, LY + RY + 52), (509, LY + RY + 58), (513, LY + RY + 82),
         (506, LY + RY + 106), (501, LY + RY + 112), (496, LY + RY + 106),
         (488, LY + RY + 82), (492, LY + RY + 58)]
for p in brush:
    EXTENT.append(p)
d.path(smooth(brush, closed=True), "Tassel", fill=lin((488, LY + RY + 52),
       (513, LY + RY + 112), (0, "#C03828"), (0.6, "#7A1C10"), (1, "#3E0C06")),
       stroke=INK, strokeWidth=1.8, join="round")
for j, dx in enumerate((-4, 0, 4)):
    d.path(f"M{500 + dx},{LY + RY + 62} q{dx * 0.5},{26} {dx * 0.8},46",
           f"Tassel strand {j+1}", fill=NONE, stroke="#3E0C06", strokeWidth=1.4,
           opacity=55, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("lantern extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#F0E2C8", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C8A87A", justify="center")
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


caption("PAPER LANTERN", "RICE PAPER · BAMBOO · WIRE")
d.finish("paper-lantern-V1R00")
