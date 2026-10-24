#!/usr/bin/env python3
"""Lyrebird — field plate V1R00. Male in full display: the tail thrown up
and forward into a full lyre — two dark frame feathers bookend the fan,
pale filament feathers laced over the bird like a veil. Small brown body
low on the forest floor, head peering out from under the lace.
Forest-floor browns, soft and layered. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; feather tips stay inside."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Lyrebird — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#241812"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def smooth(pts, closed=True, k=1.0):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

def spine(p0, p1, p2, p3, n=14):
    return [cubic(p0, p1, p2, p3, i / n) for i in range(n + 1)]

def ribbon(pts, w0, w1, label, fill, stroke=INK, sw=4):
    """Tapered closed ribbon along a sampled spine."""
    n = len(pts)
    L, Rp = [], []
    for i, (x, y) in enumerate(pts):
        ax, ay = pts[max(i - 1, 0)]; bx, by = pts[min(i + 1, n - 1)]
        dx, dy = bx - ax, by - ay
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        L.append((x + nx * w, y + ny * w)); Rp.append((x - nx * w, y - ny * w))
    tw = max(w1 / 2, 2)
    dd = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    dd += " A%.1f,%.1f 0 0 0 %.1f,%.1f " % (tw, tw, Rp[-1][0], Rp[-1][1])
    dd += " ".join("L%.1f,%.1f" % p for p in reversed(Rp[:-1])) + " Z"
    d.path(dd, label, fill=fill, stroke=stroke, strokeWidth=sw)

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#15130E"), (1, "#060503"))
PLATE_GRAD = rad((0, "#C2B288"), (0.6, "#8C7C56"), (1, "#4E432B"))
FRAME_GRAD = lin(580, 690, 320, 250, (0, "#4E3524"), (1, "#7A5840"))
BODY_GRAD  = rad((0, "#5E4028"), (0.6, "#46301E"), (1, "#2C1C10"))
HEAD_GRAD  = rad((0, "#6A4A30"), (1, "#3A2614"))
FIL  = "#D8CBA8"          # pale filament lace
FIL2 = "#B8A67E"
LITTER_GRAD = lin(0, 762, 0, 880, (0, "#6E5A36"), (1, "#3E3018"))

# --- backdrop + forest-floor plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#7A6848", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#443A24", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EDE4C6", strokeWidth=3, opacity=45)
d.shape("ellipse", "Patina 1", x=220, y=180, width=230, height=120, fill="#C8B98E", opacity=18, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=540, width=220, height=110, fill="#C8B98E", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(200,340,7),(790,290,8),(165,480,8),(840,460,7),(245,710,7),(760,730,8),
                               (150,600,6),(858,570,6),(400,108,7),(612,118,6),(330,824,6),(695,815,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#665739", opacity=38, stroke=NONE)
# dappled light where the display happens
d.shape("ellipse", "Dapple", x=380, y=200, width=260, height=130, fill="#EFE6C8", opacity=12, stroke=NONE)

# --- litter floor, closing on the disc's own arc -------------------------------------
gy = 782
gdx = math.sqrt(R * R - (gy - CY) ** 2)
d.path(f"M{CX-gdx:.1f},{gy} C330,774 420,786 500,782 C590,778 670,786 {CX+gdx:.1f},{gy} "
       f"A{R},{R} 0 0 1 {CX-gdx:.1f},{gy} Z",
       "Forest floor", fill=LITTER_GRAD, opacity=88, stroke=NONE)
for i, (x0, y0, x1, y1) in enumerate([(300,800,330,790),(620,806,650,796),(740,792,770,800)]):
    d.path(f"M{x0},{y0} Q{(x0+x1)//2},{y0-26} {x1},{y1}", f"Grass {i+1}",
           fill=NONE, stroke="#8A7A4E", strokeWidth=3, opacity=50, cap="round")

# shadow under the bird
d.shape("ellipse", "Bird shadow", x=370, y=762, width=260, height=20,
        fill="#221806", opacity=40, stroke=NONE)

# --- the fan: filaments first (behind the frame feathers) ----------------------------
BASE = (578, 676)
# (ctrl1, ctrl2, tip) for each filament — fanning from low-right up and over to the left
FILAMENTS = [
    ((700,600), (810,540), (846,486)),
    ((720,560), (820,470), (836,404)),
    ((730,510), (810,410), (800,326)),
    ((720,470), (780,340), (744,262)),
    ((700,430), (730,300), (668,208)),
    ((660,380), (660,270), (578,168)),
    ((620,350), (585,255), (480,156)),
    ((575,325), (505,235), (388,180)),
    ((530,305), (435,240), (315,240)),
    ((500,300), (390,270), (265,315)),
    ((480,320), (370,330), (250,395)),
]
def ctan(p0, p1, p2, p3, t):
    u = 1 - t
    return (3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0]),
            3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1]))

for i, (c1, c2, tip) in enumerate(FILAMENTS):
    dd = "M%d,%d C%d,%d %d,%d %d,%d" % (BASE + c1 + c2 + tip)
    col = FIL if i % 2 == 0 else FIL2
    # pale under-stroke, then a hairline core — reads as lace, not sticks
    d.path(dd, f"Filament {i+1} lace", fill=NONE, stroke=col,
           strokeWidth=7, opacity=55, cap="round")
    d.path(dd, f"Filament {i+1} core", fill=NONE, stroke="#7A6242",
           strokeWidth=2.2, opacity=60, cap="round")
    # loose barbs along the quill — lyrebird filaments never zip closed
    for j, t in enumerate([0.45, 0.65, 0.85]):
        x, y = cubic(BASE, c1, c2, tip, t)
        tx, ty = ctan(BASE, c1, c2, tip, t)
        ln = math.hypot(tx, ty) or 1
        nx, ny = -ty / ln * (9 if j % 2 == 0 else -9), tx / ln * (9 if j % 2 == 0 else -9)
        d.path(f"M{x:.0f},{y:.0f} L{x+nx:.0f},{y+ny:.0f}", f"Filament {i+1} barb {j+1}",
               fill=NONE, stroke=col, strokeWidth=1.6, opacity=40, cap="round")

# --- the two frame feathers: thick ribbons bookending the fan -----------------------
ribbon(spine((586,682), (700,610), (800,540), (852,470)), 18, 6,
       "Frame feather R", FRAME_GRAD, sw=4)
d.path("M586,682 C700,610 800,540 852,470", "Frame rib R", fill=NONE,
       stroke="#8A6A48", strokeWidth=2.5, opacity=70)
ribbon(spine((586,672), (560,470), (420,300), (300,212)), 18, 6,
       "Frame feather L", FRAME_GRAD, sw=4)
d.path("M586,672 C560,470 420,300 300,212", "Frame rib L", fill=NONE,
       stroke="#8A6A48", strokeWidth=2.5, opacity=70)

# --- bird: one flowing silhouette — head, chest, belly, raised rump ---------------------
d.path(smooth([(358,712),(370,692),(392,684),(414,692),
               (470,690),(545,676),(598,668),(628,684),
               (626,712),(588,738),(530,756),(466,758),
               (414,748),(382,734),(360,722)]),
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Body shade", x=430, y=740, width=150, height=22,
        fill="#221408", opacity=40, stroke=NONE)
d.shape("ellipse", "Breast glow", x=430, y=700, width=120, height=44,
        fill="#9A7248", opacity=20, stroke=NONE)
# folded wing lying along the flank
d.path(smooth([(438,712),(480,704),(530,708),(560,722),(548,738),
               (505,746),(458,738),(436,724)]),
       "Wing", fill="#33200F", opacity=55, stroke=INK, strokeWidth=2)
for i, (x0, y0, x1, y1) in enumerate([(520,712,540,730),(540,716,556,732)]):
    d.path(f"M{x0},{y0} Q{(x0+x1)//2+4},{(y0+y1)//2} {x1},{y1}",
           f"Wing feather {i+1}", fill=NONE, stroke="#8A6A48",
           strokeWidth=2.5, opacity=50, cap="round")
# rump fluff where the fan springs
for i, (x, y, dx, dy) in enumerate([(586,678,-8,-12),(604,672,-2,-14),(618,680,6,-10)]):
    d.path(f"M{x},{y} q{dx},{dy} {dx*2},{dy+5}", f"Covert fluff {i+1}",
           fill=NONE, stroke="#8A6A48", strokeWidth=3, opacity=55, cap="round")
# head detail: beak, crown sweep, eye
d.path("M362,706 L338,712 L361,719 Z", "Beak", fill="#1E1208", stroke=NONE)
d.path("M408,690 q-9,-9 -20,-9", "Crown sweep", fill=NONE,
       stroke="#5E4028", strokeWidth=4, cap="round")
d.shape("ellipse", "Eye", x=388, y=698, width=10, height=11, fill="#160C06", stroke=NONE)
d.shape("ellipse", "Eye glint", x=390, y=700, width=3.5, height=3.5, fill="#FFFFFF", opacity=90, stroke=NONE)
# legs: sturdy scratcher's legs planted in the litter
for j, x in enumerate([462, 516]):
    d.path(f"M{x},750 L{x-6},781 L{x+8},781 L{x+5},750 Z", f"Leg {j+1}",
           fill="#5E4630", stroke=INK, strokeWidth=2.5)
    for k, dx in enumerate([-10, 0, 10]):
        d.path(f"M{x + dx},781 L{x + dx + (dx if dx else 4) * 0.6:.0f},787",
               f"Toe {j+1}.{k+1}", fill=NONE, stroke="#4A3624",
               strokeWidth=3.5, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#362C1A", strokeWidth=6)

# --- name ------------------------------------------------------------------------------
d.text("LYREBIRD", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#E4D8B4", justify="center")
LINE2, SZ2, TRK = "MENURA NOVAEHOLLANDIAE", 20, 230
r = d.text(LINE2, "Second line", x=500, y=973, size=SZ2, font="Virelai Sans",
           color="#B0A078", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("lyrebird-V1R00")
