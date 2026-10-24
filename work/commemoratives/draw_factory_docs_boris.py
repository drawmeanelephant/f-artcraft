#!/usr/bin/env python3
"""factory-docs-boris — commemorative plate V1R00. The Migration: a flock of
document pages in loose formation, flying from a dissolving mint leaf to a
Boris-graph roost — one leaf becoming two hundred pages mid-flight. Mint
green surrendering to warm paper cream; migration season for documentation.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("factory-docs-boris — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#14201B"   # warm dark, never pure black

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

def hx(h):
    return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

def mix(c0, c1, t):
    return "#%02X%02X%02X" % tuple(round(a + (b - a) * t) for a, b in zip(hx(c0), hx(c1)))

def qbez(p0, p1, p2, t):
    x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0]
    y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1]
    tx = 2*(1-t)*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0])
    ty = 2*(1-t)*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1])
    return (x, y), math.degrees(math.atan2(ty, tx))

MINT_HI, MINT_LO = "#8FE8BC", "#4FA87C"
PAPER_HI, PAPER_LO = "#F4EFDE", "#CFC9B4"
EDGE_MINT, EDGE_PAPER = "#2E6B4E", "#8A8574"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#0D1A1A", "#040B0A", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#22403A"},
                 {"offset": 0.65, "color": "#122720"},
                 {"offset": 1, "color": "#081211"}),
        stroke="#4E6B5E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8DCCB", strokeWidth=3, opacity=26)

# --- night sky: thin moon + migration dust ------------------------------------
d.shape("ellipse", "Moon halo", x=215, y=149, width=82, height=82,
        fill=rad({"offset": 0, "color": "#E8E4D2", "opacity": 0.22},
                 {"offset": 1, "color": "#E8E4D2", "opacity": 0}), stroke=NONE)
d.shape("ellipse", "Moon", x=227, y=161, width=58, height=58,
        fill=rad({"offset": 0, "color": "#F2EEDF"},
                 {"offset": 1, "color": "#B8B49E"}), stroke=NONE)
d.shape("ellipse", "Moon shade", x=247, y=169, width=42, height=42,
        fill="#122720", opacity=60, stroke=NONE)
for i, (x, y, w, o) in enumerate([(340,140,4,32),(450,105,3,26),(585,140,5,30),
                                  (855,430,4,24),(150,470,4,24),(845,600,5,22),
                                  (235,350,3,22),(490,90,4,24)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Star {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#D8E8DE", opacity=o, stroke=NONE)

# --- the ground: a dark mound closing on the disc's own arc --------------------
d.path("M206.1,760 Q500,682 793.9,760 A420,420 0 0 1 206.1,760 Z", "Mound",
       fill=lin("#14201C", "#070D0B", (500, 690), (500, 880)), stroke=NONE)

# --- the mint leaf, dissolving at its tip --------------------------------------
d.shape("ellipse", "Leaf glow", x=180, y=500, width=300, height=240,
        fill=rad({"offset": 0, "color": "#6FD8A8", "opacity": 0.22},
                 {"offset": 1, "color": "#6FD8A8", "opacity": 0}), stroke=NONE)
d.shape("ellipse", "Leaf shadow", x=215, y=705, width=190, height=34,
        fill=rad({"offset": 0, "color": "#000000", "opacity": 0.45},
                 {"offset": 1, "color": "#000000", "opacity": 0}), stroke=NONE)
# leaf body: pointed both ends, stem low-left, tip upper-right
d.path("M246,712 C250,634 296,558 388,544 C384,622 330,700 258,716 "
       "C252,717 248,716 246,712 Z",
       "Mint leaf", fill=lin(MINT_HI, MINT_LO, (250, 545), (390, 715)),
       stroke=EDGE_MINT, strokeWidth=4.5)
# midrib + side veins
d.path("M252,705 Q312,646 382,556", "Leaf midrib", fill=NONE,
       stroke="#2E6B4E", strokeWidth=3.5, opacity=70, cap="round")
for i, (x, y, dx, dy) in enumerate([(288,672,26,4),(318,638,28,2),(346,606,26,-2),
                                    (292,668,-14,16),(322,636,-12,18)]):
    d.path(f"M{x},{y} L{x+dx},{y+dy}", f"Vein {i+1}", fill=NONE,
           stroke="#2E6B4E", strokeWidth=2.5, opacity=45, cap="round")
# torn mint scraps where the tip lets go — the start of the flock
for i, (x, y, w, dg) in enumerate([(408,532,20,-30),(428,512,15,-12),(446,498,11,6)]):
    d.path(rot_rect_path(x, y, w, w*0.6, dg), f"Scrap {i+1}",
           fill=mix(MINT_HI, PAPER_HI, 0.15), stroke=EDGE_MINT, strokeWidth=2)

# --- the flock: pages in formation, mint -> cream along the flight --------------
def page(cx, cy, w, h, deg, label, f):
    """A flying page; f=0 mint-fresh off the leaf, f=1 cream, arrived."""
    t = math.radians(deg); c, s = math.cos(t), math.sin(t)
    def pt(dx, dy): return (cx + dx*c - dy*s, cy + dx*s + dy*c)
    d.path(rot_rect_path(cx, cy, w, h, deg), label,
           fill=lin(mix(MINT_HI, PAPER_HI, f), mix(MINT_LO, PAPER_LO, f),
                    pt(-w/2, -h/2), pt(w/2, h/2)),
           stroke=mix(EDGE_MINT, EDGE_PAPER, f), strokeWidth=2.5)
    # fold mark + two text lines, shrinking for the far/small pages
    fx, fy = pt(w/2 - h*0.22, -h/2)
    c1x, c1y = pt(w/2, -h/2); c2x, c2y = pt(w/2, -h/2 + h*0.22)
    d.path(f"M{fx:.1f},{fy:.1f} L{c1x:.1f},{c1y:.1f} L{c2x:.1f},{c2y:.1f} Z",
           f"{label} fold", fill=mix("#5FC894", "#D8D2C0", f),
           stroke=mix(EDGE_MINT, EDGE_PAPER, f), strokeWidth=1.5)
    if w >= 20:
        for j in range(2):
            y0 = pt(-w/2 + 6, -h/2 + h*0.42 + j*h*0.2)
            y1 = pt(w/2 - 6, -h/2 + h*0.42 + j*h*0.2)
            d.path(f"M{y0[0]:.1f},{y0[1]:.1f} L{y1[0]:.1f},{y1[1]:.1f}",
                   f"{label} line {j+1}", fill=NONE,
                   stroke=mix("#3E8A64", "#8A8574", f), strokeWidth=2,
                   opacity=70, cap="round")

# main arm of the V: leaf tip -> roost, long climb
MAIN = ((405, 545), (545, 385), (745, 295))
for i, t in enumerate((0.06, 0.18, 0.30, 0.43, 0.56, 0.69, 0.81, 0.92)):
    (x, y), dg = qbez(*MAIN, t)
    assert on_disc(x, y, 26), (x, y)
    w = 15 + 14 * t
    page(x, y, w, w * 1.3, dg + (6 if i % 2 else -6), f"Flock {i+1}", t)
# trailing arm, lower and shorter — the V's second leg
TRAIL = ((400, 560), (475, 525), (635, 430))
for i, t in enumerate((0.12, 0.32, 0.52, 0.72, 0.9)):
    (x, y), dg = qbez(*TRAIL, t)
    assert on_disc(x, y, 26), (x, y)
    w = 14 + 10 * t
    page(x, y, w, w * 1.3, dg - 4, f"Trail {i+1}", t * 0.85)

# --- the Boris-graph roost: a bare tree of nodes and edges ----------------------
NODES = {
    "root":  (705, 345), "fork": (748, 298), "low":  (666, 302),
    "top":   (785, 255), "left": (722, 236), "tip":  (830, 280),
    "bud":   (640, 258),
}
EDGES = [("root", "fork"), ("root", "low"), ("fork", "top"),
         ("fork", "left"), ("top", "tip"), ("low", "bud")]
d.shape("ellipse", "Roost glow", x=600, y=190, width=300, height=230,
        fill=rad({"offset": 0, "color": "#46D992", "opacity": 0.18},
                 {"offset": 1, "color": "#46D992", "opacity": 0}), stroke=NONE)
for i, (a, b) in enumerate(EDGES):
    x0, y0 = NODES[a]; x1, y1 = NODES[b]
    mx, my = (x0 + x1) / 2 + 6, (y0 + y1) / 2 - 10
    d.path(f"M{x0},{y0} Q{mx},{my} {x1},{y1}", f"Branch {i+1}", fill=NONE,
           stroke="#3E4A44", strokeWidth=5, cap="round")
for name, (x, y) in NODES.items():
    assert on_disc(x, y, 16), name
    r = 9 if name in ("root", "fork") else 6.5
    d.shape("ellipse", f"Node {name}", x=x - r, y=y - r, width=2*r, height=2*r,
            fill=rad({"offset": 0, "color": "#7CE8B4"},
                     {"offset": 1, "color": "#1E7A4E"}),
            stroke="#0E2A1C", strokeWidth=2.5)
# two pages already roosting, one flaring in to land
page(785, 238, 26, 32, -14, "Perched 1", 1.0)
page(724, 219, 22, 28, 10, "Perched 2", 1.0)
page(852, 322, 20, 25, 35, "Landing", 0.9)

# --- name + role -----------------------------------------------------------------
d.text("FACTORY-DOCS-BORIS", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#F0E8D8", justify="center")
LINE2, SZ2, TRK = "MINTLIFY-TO-BORIS MIGRATION", 22, 280
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#8FD8B4", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
for oid, label in ((r["id"], "second line"),):
    b2 = find(d.call("inspect_document", {}, "inspect")["layers"], oid)["bounds"]
    print(label, "bounds", {k: round(v) for k, v in b2.items()})
    assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("factory-docs-boris-V1R00")
