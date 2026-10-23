#!/usr/bin/env python3
"""Collection navigation map — site equity plate V1R00. The eleven collection
trunks as nodes on a ring around the archive's ◈ hub, joined by translucent
connectors, each labelled in caps. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Collection Map — Site Equity", 1000, 1000)

INK = "#3A2418"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A1C10"}, {"offset": 1, "color": "#100904"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4E8CC"}, {"offset": 0.7, "color": "#D9BE92"},
    {"offset": 1, "color": "#A9845A"}]}}
MARK_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4CE72"}, {"offset": 0.6, "color": "#D9A03C"},
    {"offset": 1, "color": "#9C6218"}]}}
NODE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F8EFD8"}, {"offset": 0.7, "color": "#E2C89A"},
    {"offset": 1, "color": "#B8905E"}]}}
CORE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E3A20"}, {"offset": 1, "color": "#2A1608"}]}}

PCX, PCY, PR = 500, 460, 420
def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def diamond(cx, cy, r):
    return f"M{cx},{cy-r} L{cx+r},{cy} L{cx},{cy+r} L{cx-r},{cy} Z"

CX, CY, RING = 500, 450, 255
NODES = ["HOME", "MASCOTS", "LORELOG", "REFERENCE", "POSTS", "CHANGELOG",
         "RELEASES", "APHORISMS", "HAIKUS", "LIMERICKS", "GUIDES"]

# --- backdrop + plate -------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#D9BE92", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2E1C0E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F8F0DC", strokeWidth=3, opacity=40)
d.shape("ellipse", "Patina 1", x=190, y=640, width=240, height=130, fill="#B08C5E", opacity=18, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=150, width=220, height=120, fill="#B08C5E", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(200,330,7),(790,290,6),(170,540,8),(830,520,7),(250,730,6),
                               (740,720,8),(145,430,6),(855,410,7),(420,120,7),(600,130,6),
                               (300,170,5),(700,180,6),(330,810,5),(660,800,6),(500,105,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#8A6844", opacity=35, stroke=NONE)

# --- connectors + orbit ring -------------------------------------------------
pts = []
for i in range(11):
    a = math.radians(-90 + i * 360 / 11)
    pts.append((CX + RING * math.cos(a), CY + RING * math.sin(a)))
for i, (x, y) in enumerate(pts):
    d.path(f"M{CX},{CY} L{x:.1f},{y:.1f}", f"Spoke {i+1}", fill=NONE,
           stroke="#6E4A24", strokeWidth=3.5, opacity=38, cap="round")
d.shape("ellipse", "Orbit ring", x=CX-RING, y=CY-RING, width=RING*2, height=RING*2,
        fill=NONE, stroke="#8A6844", strokeWidth=2, opacity=30)
d.shape("ellipse", "Orbit ring inner", x=CX-RING+14, y=CY-RING+14, width=(RING-14)*2, height=(RING-14)*2,
        fill=NONE, stroke="#F4E8CC", strokeWidth=1.5, opacity=30)

# --- nodes --------------------------------------------------------------------
for i, (x, y) in enumerate(pts):
    big = (i == 0)
    r = 40 if big else 31
    assert on_disc(x, y, 60), (i, x, y)
    d.shape("ellipse", f"Node shadow {i+1}", x=x-r, y=y-r+7, width=r*2, height=r*2,
            fill="#3A2418", opacity=15, stroke=NONE)
    d.shape("ellipse", f"Node {NODES[i]}", x=x-r, y=y-r, width=r*2, height=r*2,
            fill=NODE_GRAD, stroke=INK, strokeWidth=5)
    if big:
        d.path(diamond(x, y, 17), "Home glyph", fill=MARK_GRAD, stroke=INK, strokeWidth=3, join="round")
        d.path(diamond(x, y, 7), "Home core", fill=CORE_GRAD, stroke=NONE)
    else:
        d.shape("ellipse", f"Node pip {i+1}", x=x-7, y=y-7, width=14, height=14,
                fill="#B8905E", opacity=75, stroke=NONE)

# --- hub: the archive mark -----------------------------------------------------
d.path(diamond(CX, CY+8, 66), "Hub shadow", fill="#3A2418", opacity=18, stroke=NONE)
d.path(diamond(CX, CY, 62), "Hub outer", fill=MARK_GRAD, stroke=INK, strokeWidth=9, join="round")
d.path(diamond(CX, CY, 36), "Hub field", fill={"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E9D6AC"}, {"offset": 1, "color": "#C6A472"}]}},
    stroke=INK, strokeWidth=4, join="round")
d.path(diamond(CX, CY, 18), "Hub core", fill=CORE_GRAD, stroke="#F0C96A", strokeWidth=2, join="round")

# --- labels ---------------------------------------------------------------------
# clearance past each node = node radius + gap + projection of the text's
# half-extents onto the radial direction (horizontal text, centre-justified)
for i, (x, y) in enumerate(pts):
    a = math.radians(-90 + i * 360 / 11)
    ca, sa = abs(math.cos(a)), abs(math.sin(a))
    hw, hh = 5.4 * len(NODES[i]), 9            # ~16pt caps, centre-justified
    node_r = 40 if i == 0 else 31
    off = node_r + 8 + hw * ca + hh * sa
    lx, ly = CX + (RING + off) * math.cos(a), CY + (RING + off) * math.sin(a)
    for cx_ in (lx - hw, lx + hw):
        for cy_ in (ly - hh, ly + hh):
            assert on_disc(cx_, cy_, 18), (i, round(cx_), round(cy_))
    d.text(NODES[i], f"Label {NODES[i]}", x=round(lx), y=round(ly) + 6, size=16,
           font="Virelai Sans", color="#3A2418", justify="center")

# --- name + role ------------------------------------------------------------------
d.text("COLLECTION MAP", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#F0E2C4", justify="center")
d.text(" ".join("ELEVEN TRUNKS"), "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#C6A472", justify="center")

d.finish("site-collection-map-V1R00")
