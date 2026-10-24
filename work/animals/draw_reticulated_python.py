#!/usr/bin/env python3
"""Reticulated python — field plate V1R00. Malayopython reticulatus in the
ambush coil: three stacked loops on a muddy riverbank, the neck rising out
of the mound to the left, head level, tongue mid-flick. The skin is the
net — a chain of dark-margined diamonds linked by a cream reticulum cast
over every coil. Jungle-river plate, deep green dusk, water glint behind
the bank. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Reticulated Python — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E140A"   # warm dark ink, never pure black
rng = random.Random(1107)

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = start, end
    return {"gradient": g}

def lin3(c0, c1, c2, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0},
         {"offset": 0.5, "color": c1}, {"offset": 1, "color": c2}]}
    if start: g["start"], g["end"] = start, end
    return {"gradient": g}

def rad(*stops):
    n = len(stops) - 1
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": round(i / n, 3), "color": c} for i, c in enumerate(stops)]}}

def rad_o(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

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

def qpt(p0, p1, p2, t):
    u = 1 - t
    return (u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0], u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1])

def qtan(p0, p1, p2, t):
    u = 1 - t
    return (2*u*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0]), 2*u*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1]))

def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

BG_GRAD    = lin("#101812", "#040705", [0, 0], [0, 1000])
PLATE_GRAD = rad("#5E7A5C", "#39543E", "#1B2E20", "#0E1A12")
FLOOR_GRAD = lin("#6E5838", "#332414", [0, 660], [0, 880])
COIL_GRAD  = lin("#C2A25E", "#7A5C30", [0, 430], [0, 690])
COIL_DARK  = lin("#96783E", "#54401E", [0, 430], [0, 690])
NET_DARK   = "#32200E"
NET_CREAM  = "#EADAAC"
CELL_MID   = "#B08D4E"

# --- backdrop + jungle-river plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#5E7A5C", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke=NONE)
# humid dusk glow low behind the coils
d.shape("ellipse", "Dusk glow", x=200, y=380, width=600, height=280,
        fill=rad_o((0, "#D8B878", 0.26), (0.6, "#B89058", 0.10), (1, "#B89058", 0)), stroke=NONE)
# the river: a pale glint strip behind the bank, fading before the rim
d.shape("ellipse", "River glint", x=170, y=622, width=660, height=26,
        fill={"gradient": {"kind": "linear", "start": [170, 635], "end": [830, 635], "stops": [
            {"offset": 0, "color": "#9FC4B2", "opacity": 0},
            {"offset": 0.18, "color": "#9FC4B2", "opacity": 0.28},
            {"offset": 0.82, "color": "#9FC4B2", "opacity": 0.28},
            {"offset": 1, "color": "#9FC4B2", "opacity": 0}]}}, stroke=NONE)
# far bank dark mass behind the water
d.path("M170,640 C300,608 700,606 830,638 L830,668 C700,652 300,652 170,668 Z",
       "Far bank", fill="#24382A", opacity=55, stroke=NONE)

# --- muddy bank, closed on the disc arc ------------------------------------------------
GY = 664
gx = math.sqrt(PR**2 - (GY - PCY)**2)
d.path(f"M{PCX - gx:.1f},{GY} Q{PCX},{GY - 12} {PCX + gx:.1f},{GY} A420,420 0 0 1 {PCX - gx:.1f},{GY} Z",
       "Mud bank", fill=FLOOR_GRAD, stroke=NONE)
# leaf litter + grit
for i in range(24):
    x, y = rng.uniform(200, 800), rng.uniform(690, 850)
    r = rng.uniform(3, 8)
    if not on_disc(x, y, 14): continue
    d.shape("ellipse", f"Litter {i+1}", x=x - r, y=y - r * 0.5, width=2 * r, height=r,
            fill=rng.choice(("#7A6238", "#5A4A2C", "#8A7040")), opacity=rng.choice((40, 55)), stroke=NONE)

# fallen philodendron leaf at the right edge
leaf = [(716, 700), (760, 690), (798, 702), (806, 726), (782, 744), (740, 744), (712, 726)]
d.path(smooth(leaf), "Fallen leaf", fill=lin("#4E6A3C", "#243A20", [716, 700], [806, 744]),
       opacity=85, stroke=NONE)
d.path("M722,706 C750,712 780,724 796,736", "Leaf vein", fill=NONE,
       stroke="#8AA468", strokeWidth=3, opacity=50, cap="round")

# === the python =============================================================================
def coil(name, pts, shade_y0, shade_y1):
    """One loop of the mound: closed blob, cylinder shading, net chain on the spine."""
    d.path(smooth(pts), name, fill=COIL_GRAD, stroke=INK, strokeWidth=4)
    ys = [p[1] for p in pts]
    hi, lo = min(ys), max(ys)
    # cylinder: light crown, shadowed under-roll
    top_pts = sorted(pts, key=lambda p: p[1])[:len(pts)//2]
    bot_pts = sorted(pts, key=lambda p: -p[1])[:len(pts)//2]
    d.path(smooth(sorted(top_pts, key=lambda p: p[0]), closed=False), f"{name} crown light",
           fill=NONE, stroke="#F0DCA8", strokeWidth=10, opacity=22, cap="round")
    d.path(smooth(sorted(bot_pts, key=lambda p: p[0]), closed=False), f"{name} under shade",
           fill=NONE, stroke="#241608", strokeWidth=16, opacity=30, cap="round")

def net_chain(name, spine, half_w, n, skip=()):
    """The reticulum: dark diamond cells on a cream net, chained along the spine."""
    cells = []
    for i in range(n):
        t = 0.06 + 0.88 * i / (n - 1)
        x, y = qpt(*spine, t)
        tx, ty = qtan(*spine, t)
        ln = math.hypot(tx, ty) or 1
        ux, uy = tx / ln, ty / ln
        nx, ny = -uy, ux
        w = half_w * (0.9 + 0.2 * math.sin(math.pi * t))
        L = w * 1.15
        # kite: nose and tail along the spine, wings across it
        kite = [(x + ux * L * 0.62, y + uy * L * 0.62),
                (x + nx * w * 0.78, y + ny * w * 0.78),
                (x - ux * L * 0.62, y - uy * L * 0.62),
                (x - nx * w * 0.78, y - ny * w * 0.78)]
        cells.append((x, y, ux, uy, nx, ny, w))
        if i in skip: continue
        d.path(smooth(kite, k=0.7), f"{name} cell {i+1}", fill=NET_DARK,
               opacity=88, stroke=NONE)
        inner = [lerp(c, (x, y), 0.42) for c in kite]
        d.path(smooth(inner, k=0.7), f"{name} cell mid {i+1}", fill=CELL_MID,
               opacity=80, stroke=NONE)
    # cream net strands between cell corners + across the coil edges
    for i in range(n - 1):
        x, y, ux, uy, nx, ny, w = cells[i]
        x2, y2, ux2, uy2, nx2, ny2, w2 = cells[i + 1]
        for s in (1, -1):
            a = (x + nx * w * 0.72 * s, y + ny * w * 0.72 * s)
            b = (x2 + nx2 * w2 * 0.72 * s, y2 + ny2 * w2 * 0.72 * s)
            mx, my = (a[0] + b[0]) / 2 + nx * 6 * s, (a[1] + b[1]) / 2 + ny * 6 * s
            d.path(f"M{a[0]:.1f},{a[1]:.1f} Q{mx:.1f},{my:.1f} {b[0]:.1f},{b[1]:.1f}",
                   f"{name} net {i+1}{'a' if s > 0 else 'b'}", fill=NONE,
                   stroke=NET_CREAM, strokeWidth=4, opacity=65, cap="round")
    # scale speckle in the lanes between cells
    for i in range(n - 1):
        t = 0.06 + 0.88 * (i + 0.5) / (n - 1)
        x, y = qpt(*spine, t)
        for s in (-0.45, 0.0, 0.45):
            tx, ty = qtan(*spine, t)
            ln = math.hypot(tx, ty) or 1
            d.shape("ellipse", f"{name} scale {i}{s}", x=x - ty / ln * half_w * s - 3,
                    y=y + tx / ln * half_w * s - 2.5, width=6, height=5,
                    fill="#8A6C38", opacity=55, stroke=NONE)

# tail tip: a tapered stub peeking out at the right of the bottom coil
T0, T1, T2 = (700, 640), (782, 630), (806, 668)
tl, tr = [], []
NT = 12
for k in range(NT + 1):
    t = k / NT
    x, y = qpt(T0, T1, T2, t)
    tx, ty = qtan(T0, T1, T2, t)
    ln = math.hypot(tx, ty)
    nx, ny = -ty / ln, tx / ln
    w = (34 * (1 - t) ** 0.8 + 4) / 2
    tl.append((x + nx * w, y + ny * w)); tr.append((x - nx * w, y - ny * w))
d.path(smooth(tl + list(reversed(tr))), "Tail tip", fill=COIL_DARK, stroke=INK, strokeWidth=4)
for j, t in enumerate((0.25, 0.55)):
    x, y = qpt(T0, T1, T2, t)
    tx, ty = qtan(T0, T1, T2, t)
    ln = math.hypot(tx, ty)
    nx, ny = -ty / ln, tx / ln
    w = (34 * (1 - t) ** 0.8 + 4) / 2
    d.path(f"M{x + nx * w:.1f},{y + ny * w:.1f} L{x - nx * w:.1f},{y - ny * w:.1f}",
           f"Tail band {j+1}", fill=NONE, stroke=NET_CREAM, strokeWidth=4,
           opacity=60, cap="round")

# contact shadow under the mound
d.shape("ellipse", "Mound shadow", x=250, y=640, width=520, height=56,
        fill=rad_o((0, "#080C06", 0.55), (0.7, "#080C06", 0.22), (1, "#080C06", 0)), stroke=NONE)

# --- the coil mound, bottom to top -------------------------------------------------------------
# bottom coil: broad flat loop sitting on the bank
bottom = [(308, 604), (336, 560), (430, 542), (560, 546), (668, 566),
          (716, 606), (700, 644), (600, 664), (430, 666), (330, 640)]
coil("Bottom coil", bottom, 540, 668)
net_chain("Bottom", ((330, 618), (505, 588), (696, 616)), 46, 11)

# middle coil, staggered right so the mound spirals rather than stacks
middle = [(368, 524), (402, 486), (486, 470), (600, 478), (670, 508),
          (680, 544), (636, 570), (496, 574), (386, 556)]
coil("Middle coil", middle, 466, 576)
net_chain("Middle", ((384, 532), (521, 502), (668, 526)), 42, 10)

# top coil, tightest, tipped forward
top = [(402, 448), (436, 420), (510, 414), (578, 430), (600, 458),
       (570, 486), (482, 494), (414, 478)]
coil("Top coil", top, 410, 496)
net_chain("Top", ((414, 452), (505, 434), (588, 448)), 38, 8)

# --- neck + head, rising left out of the mound --------------------------------------------
# neck: a thick stroke curving up-left
neck = [(452, 452), (408, 428), (368, 402), (342, 378)]
d.path(smooth(neck, closed=False), "Neck ink", fill=NONE, stroke=INK, strokeWidth=62, cap="round")
d.path(smooth(neck, closed=False), "Neck", fill=NONE, stroke=COIL_GRAD, strokeWidth=54, cap="round")
# net chain down the neck
net_pts = []
for i in range(9):
    u = i / 8
    # piecewise along the 4-point neck polyline
    seg = min(2, int(u * 3))
    tt = u * 3 - seg
    p = lerp(neck[seg], neck[seg + 1], tt)
    q = lerp(neck[seg], neck[seg + 1], min(1, tt + 0.02))
    tx, ty = q[0] - p[0], q[1] - p[1]
    ln = math.hypot(tx, ty) or 1
    net_pts.append((p[0], p[1], -ty / ln, tx / ln))
for i, (x, y, nx, ny) in enumerate(net_pts):
    w = 24 - i * 1.2
    d.path(f"M{x + nx * w:.1f},{y + ny * w:.1f} L{x - nx * w:.1f},{y - ny * w:.1f}",
           f"Neck net {i+1}", fill=NONE, stroke=NET_DARK if i % 3 == 1 else NET_CREAM,
           strokeWidth=6 if i % 3 == 1 else 4, opacity=70, cap="round")

# head: elongated wedge, level, facing left
head = [(352, 366), (320, 348), (284, 344), (254, 356), (238, 372),
        (244, 388), (268, 398), (306, 402), (340, 396), (358, 382)]
d.path(smooth(head), "Head", fill=lin("#B8965A", "#6E5226", [250, 350], [360, 400]),
       stroke=INK, strokeWidth=4)
# crown plates: the python's big symmetrical head shields
d.path("M300,352 C322,346 344,354 352,366", "Crown sheen", fill=NONE,
       stroke="#F0DCA8", strokeWidth=6, opacity=30, cap="round")
# dark temporal stripe through the eye to the neck
d.path("M330,368 C348,372 360,380 366,392", "Temporal stripe", fill=NONE,
       stroke=NET_DARK, strokeWidth=8, opacity=75, cap="round")
# eye: orange iris, vertical pupil
d.shape("ellipse", "Eye rim", x=288, y=358, width=24, height=20,
        fill=rad("#8A6C38", "#4E3A18"), stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Eye", x=293, y=361, width=15, height=13,
        fill=rad("#D89238", "#6E3A10"), stroke=NONE)
d.shape("ellipse", "Pupil", x=299, y=362, width=5, height=11, fill="#120A04", stroke=NONE)
d.shape("ellipse", "Eye glint", x=296, y=362, width=4, height=3, fill="#FFF6D8", opacity=85, stroke=NONE)
# mouth + labial pits (heat-sensing dots along the upper lip)
d.path("M240,384 C262,394 300,400 334,396", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
for i, (x, y) in enumerate([(252, 386), (266, 391), (281, 394), (297, 396)]):
    d.shape("ellipse", f"Lip pit {i+1}", x=x - 2.5, y=y - 2, width=5, height=4,
            fill=INK, opacity=75, stroke=NONE)
d.shape("ellipse", "Nostril", x=250, y=368, width=6, height=5, fill=INK, opacity=70, stroke=NONE)
# rostral net marks
for i, (x, y, w) in enumerate([(262, 364, 5), (276, 360, 5), (250, 376, 4)]):
    d.path(f"M{x},{y} L{x + 8},{y - 6}", f"Head net {i+1}", fill=NONE,
           stroke=NET_CREAM, strokeWidth=3.5, opacity=55, cap="round")
# forked tongue mid-flick
d.path("M238,382 C222,384 210,390 200,398", "Tongue stem", fill=NONE,
       stroke="#B44A3A", strokeWidth=4, cap="round")
d.path("M200,398 L188,392 M200,398 L186,402", "Tongue forks", fill=NONE,
       stroke="#B44A3A", strokeWidth=3, cap="round")

# hanging liana, upper right, thin but >=3pt
for i, (x0, sway) in enumerate([(762, 24), (790, -18)]):
    pts = [(x0, 190), (x0 + sway * 0.4, 240), (x0 + sway, 298), (x0 + sway * 0.7, 350)]
    for p in pts: assert on_disc(*p, 10), p
    d.path(smooth(pts, closed=False), f"Liana {i+1}", fill=NONE,
           stroke="#2E4428", strokeWidth=4, opacity=70, cap="round")
    for j, t in enumerate((0.3, 0.62, 0.9)):
        u = t * 3
        seg = min(2, int(u))
        p = lerp(pts[seg], pts[seg + 1], u - seg)
        d.shape("ellipse", f"Liana {i+1} leaf {j}", x=p[0] - 4, y=p[1] - 8,
                width=9, height=16, fill=lin("#5E7A44", "#33482A"), opacity=75, stroke=NONE)

# plate rim over everything
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0C140C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8DCA8", strokeWidth=3, opacity=22)

# --- name (long — smaller point) --------------------------------------------------------------
r1 = d.text("RETICULATED PYTHON", "Name", x=500, y=962, size=48, font="Virelai Sans",
            color="#E4D8AE", justify="center")

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
b = find(layers, r1["id"])["bounds"]
print("name bounds", {k: round(v) for k, v in b.items()})
assert b["width"] <= 800 and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("reticulated-python-V1R00")
