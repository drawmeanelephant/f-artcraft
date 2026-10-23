#!/usr/bin/env python3
"""Monarch — field plate V1R00. Orange panes in a black grid: full dorsal
spread basking on a milkweed umbel, veins thick enough to read, two rows of
white spots along the black margins, the male's scent spot on the hind wing,
one antenna bent. Milkweed-green plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Monarch — Field Plate", 1000, 1000)
rng = random.Random(79)   # fixed seed: florets and specks are the same every run

PCX, PCY, PR = 500, 460, 420
INK = "#24160F"   # warm soot-brown, not black

def lin(c0, c1, start=None, end=None, o0=None, o1=None):
    s0 = {"offset": 0, "color": c0}; s1 = {"offset": 1, "color": c1}
    if o0 is not None: s0["opacity"] = o0
    if o1 is not None: s1["opacity"] = o1
    g = {"kind": "linear", "stops": [s0, s1]}
    if start: g["start"], g["end"] = start, end
    return {"gradient": g}

def rad(*stops):
    n = len(stops) - 1
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": round(i / n, 3), "color": c} for i, c in enumerate(stops)]}}

def smooth(pts, closed=True, k=1.0):
    """Catmull-Rom through pts as cubic Beziers."""
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    rng_ = range(n) if closed else range(n - 1)
    for i in rng_:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

def P(a):
    t = math.radians(a)
    return (PCX + PR * math.cos(t), PCY + PR * math.sin(t))

def arc_to(a_from, a_to):
    """Close along the disc's own arc, the short way round."""
    delta = (a_to - a_from + 540) % 360 - 180
    x, y = P(a_to)
    return f"A420,420 0 0 {1 if delta > 0 else 0} {x:.1f},{y:.1f}"

REACH = []
S, C0 = 0.94, (500, 410)
def sc(p):
    q = (C0[0] + (p[0] - C0[0]) * S, C0[1] + (p[1] - C0[1]) * S)
    REACH.append(q)
    return q

def mir(p):
    return (1000 - p[0], p[1])

def inset(pts, ds):
    """Offset each outline point toward the wing's interior by its own distance."""
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    out = []
    for i, p in enumerate(pts):
        a, b = pts[i - 1], pts[(i + 1) % len(pts)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty) or 1
        nx, ny = -ty / ln, tx / ln
        if nx * (cx - p[0]) + ny * (cy - p[1]) < 0:
            nx, ny = -nx, -ny
        out.append((p[0] + nx * ds[i], p[1] + ny * ds[i]))
    return out

def spot(name, c, w, h, fill, op=95):
    d.shape("ellipse", name, x=round(c[0] - w / 2, 1), y=round(c[1] - h / 2, 1),
            width=w, height=h, fill=fill, stroke=NONE, opacity=op)

# --- palette ------------------------------------------------------------------------------
BG_GRAD = lin("#1B2416", "#070A05", [0, 0], [0, 1000])
PLATE_GRAD = rad("#E4ECCB", "#BECDA0", "#879B6C")
BORDER_FILL = rad("#3A251A", "#1E120C")
SPOT = rad("#FFFFFF", "#ECE6D8")

# --- backdrop + plate ------------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke=NONE)
d.shape("ellipse", "Plate sun", x=200, y=70, width=600, height=380,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FBFBEA", "opacity": 0.45}, {"offset": 1, "color": "#FBFBEA", "opacity": 0}]}},
        stroke=NONE)
for i in range(18):
    while True:
        x, y = rng.uniform(140, 860), rng.uniform(100, 760)
        if math.hypot(x - PCX, y - PCY) < PR - 40:
            break
    w = rng.uniform(5, 9)
    spot(f"Plate fleck {i+1}", (x, y), round(w, 1), round(w, 1), "#7C905F", rng.randint(20, 40))

# --- milkweed: leaves and stalk rise off the disc's own arc ------------------------------------
def leaf(name, a_lo, a_hi, tip, bulge, fill):
    p0, p1 = P(a_lo), P(a_hi)
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    vx, vy = tip[0] - mx, tip[1] - my
    ln = math.hypot(vx, vy); nx, ny = -vy / ln, vx / ln
    # the edge leaving p0 bulges out on p0's own side of the midrib
    sg = 1 if (p0[0] - mx) * nx + (p0[1] - my) * ny > 0 else -1
    e0 = [(mx + vx * t + sg * nx * b, my + vy * t + sg * ny * b) for t, b in ((0.35, bulge), (0.85, bulge * 0.6))]
    e1 = [(mx + vx * t - sg * nx * b, my + vy * t - sg * ny * b) for t, b in ((0.85, bulge * 0.6), (0.35, bulge))]
    s = (f"M{p0[0]:.1f},{p0[1]:.1f} C{e0[0][0]:.1f},{e0[0][1]:.1f} {e0[1][0]:.1f},{e0[1][1]:.1f} {tip[0]:.1f},{tip[1]:.1f} "
         f"C{e1[0][0]:.1f},{e1[0][1]:.1f} {e1[1][0]:.1f},{e1[1][1]:.1f} {p1[0]:.1f},{p1[1]:.1f} "
         + arc_to(ang(p1), ang(p0)) + " Z")
    d.path(s, name, fill=fill, stroke="#3E5230", strokeWidth=4, opacity=92)
    d.path(f"M{mx:.1f},{my:.1f} Q{mx + vx*0.5 + nx*bulge*0.15:.1f},{my + vy*0.5 + ny*bulge*0.15:.1f} "
           f"{tip[0] - vx*0.06:.1f},{tip[1] - vy*0.06:.1f}", name + " midrib",
           fill=NONE, stroke="#F2F4E2", strokeWidth=4, opacity=55, cap="round")

def ang(p):
    return math.degrees(math.atan2(p[1] - PCY, p[0] - PCX)) % 360

leaf("Milkweed leaf L", 122, 138, (176, 610), 52, lin("#86A866", "#4C6E3E", [150, 600], [300, 820]))
leaf("Milkweed leaf R", 42, 58, (824, 610), 52, lin("#86A866", "#4C6E3E", [850, 600], [700, 820]))
p0, p1 = P(88.6), P(91.4)
d.path(f"M{p0[0]:.1f},{p0[1]:.1f} C506,800 506,760 504,712 L496,712 C494,760 494,800 {p1[0]:.1f},{p1[1]:.1f} "
       + arc_to(91.4, 88.6) + " Z", "Milkweed stalk", fill=lin("#7E9A5C", "#4C663A"), stroke="#3E5230", strokeWidth=3)
# the umbel: a dome of reflexed pink florets peeking out under the hind wings
FLORET = rad("#FBD4DE", "#E89AB2", "#B8607E")
fl = []
for ring, (rr, nn) in enumerate([(0, 1), (26, 7), (50, 12), (72, 15)]):
    for k in range(nn):
        a = 2 * math.pi * k / nn + ring * 0.4
        fl.append((500 + rr * math.cos(a) * 1.25, 704 + rr * math.sin(a) * 0.7 + rng.uniform(-3, 3)))
for i, (x, y) in sorted(enumerate(fl), key=lambda t: t[1][1]):
    d.path(f"M500,{712} L{x:.1f},{y:.1f}", f"Pedicel {i+1}", fill=NONE, stroke="#8AA06A",
           strokeWidth=3, opacity=60, cap="round")
for i, (x, y) in sorted(enumerate(fl), key=lambda t: t[1][1]):
    d.shape("star", f"Floret {i+1}", cx=round(x, 1), cy=round(y, 1), points=5, radius1=11, radius2=5,
            rotation=rng.uniform(0, 72), fill=FLORET, stroke="#9A4E6A", strokeWidth=1.5, opacity=95)
    spot(f"Floret hood {i+1}", (x, y), 7, 7, "#FFF2F4", 80)

# --- wings ----------------------------------------------------------------------------------
FW = [(512, 338), (560, 300), (630, 262), (710, 232), (770, 216), (808, 222), (814, 252),
      (802, 300), (784, 350), (762, 400), (740, 446), (690, 454), (620, 442), (560, 420), (516, 398)]
FW_D = [6, 6, 8, 10, 56, 70, 60, 30, 30, 30, 30, 26, 10, 8, 6]
HW = [(514, 394), (580, 388), (660, 400), (730, 430), (772, 470), (788, 520), (778, 575),
      (750, 625), (706, 662), (650, 684), (600, 686), (560, 664), (534, 620), (520, 560), (514, 480)]
HW_D = [6, 6, 8, 22, 32, 32, 32, 32, 32, 32, 32, 30, 22, 10, 6]
FW_CELL = [(524, 352), (600, 322), (668, 312), (678, 352), (642, 386), (566, 390)]
HW_CELL = [(528, 420), (600, 430), (660, 470), (652, 518), (600, 522), (546, 482)]
FW_VEINS = [((524, 350), 3), ((668, 312), 4), ((670, 318), 5), ((676, 334), 6), ((678, 350), 7),
            ((668, 364), 8), ((652, 378), 9), ((618, 388), 10), ((586, 390), 11), ((520, 394), 12)]
HW_VEINS = [((520, 398), 2), ((600, 430), 3), ((660, 470), 4), ((660, 492), 5), ((656, 512), 6),
            ((638, 520), 7), ((614, 522), 8), ((590, 520), 9), ((566, 506), 10), ((546, 484), 11),
            ((522, 450), 12), ((516, 420), 13)]

def margin_spots(name, pts, i0, i1, rows, flip):
    cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts)
    n = 0
    for i in range(i0, i1):
        a, b = pts[i], pts[i + 1]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty); nx, ny = -ty / ln, tx / ln
        if nx * (cx - a[0]) + ny * (cy - a[1]) < 0:
            nx, ny = -nx, -ny
        for t in (0.25, 0.75):
            mx, my = a[0] + tx * t, a[1] + ty * t
            for off, sz in rows:
                q = (mx + nx * off, my + ny * off)
                if flip: q = mir(q)
                n += 1
                spot(f"{name} spot {n}", q, sz, sz * 0.8, SPOT, 92)

def wing(name, outline, ds, cell, veins, vein_w, spots, flip, extra=None):
    o = [sc(p) for p in outline]
    c = [sc(p) for p in cell]
    if flip:
        o = [mir(p) for p in o]; c = [mir(p) for p in c]
    ins = inset(o, ds)
    cx = sum(p[0] for p in o) / len(o); cy = sum(p[1] for p in o) / len(o)
    root = o[0]
    d.path(smooth(ins), f"{name} panes", fill={"gradient": {"kind": "radial",
           "center": [round(root[0], 1), round(root[1], 1)], "stops": [
           {"offset": 0, "color": "#F7AC46"}, {"offset": 0.6, "color": "#F39A34"},
           {"offset": 1, "color": "#E0761F"}]}},
           stroke=NONE, opacity=90)
    d.path(smooth(ins), f"{name} pane glow", fill={"gradient": {"kind": "radial", "stops": [
           {"offset": 0, "color": "#FFE2A0", "opacity": 0.35}, {"offset": 1, "color": "#FFE2A0", "opacity": 0}]}},
           stroke=NONE)
    # black border band: outline + reversed inset, a compound path with a hole
    d.path(smooth(o) + " " + smooth(list(reversed(ins))), f"{name} border", fill=BORDER_FILL,
           stroke=INK, strokeWidth=3, opacity=95)
    for j, (start, k) in enumerate(veins):
        a = sc(start)
        if flip: a = mir(a)
        b = o[k]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        bx, by = (mx - cx) * 0.06, (my - cy) * 0.06
        d.path(f"M{a[0]:.1f},{a[1]:.1f} Q{mx + bx:.1f},{my + by:.1f} {b[0]:.1f},{b[1]:.1f}",
               f"{name} vein {j+1}", fill=NONE, stroke=INK, strokeWidth=vein_w, cap="round", opacity=95)
    d.path(smooth(c), f"{name} discal cell", fill=NONE, stroke=INK, strokeWidth=vein_w, opacity=95)
    if extra: extra(flip)
    for (i0, i1, rows) in spots:
        margin_spots(name, [sc(p) for p in outline], i0, i1, rows, flip)

def scent_spot(flip):
    q = sc((612, 578))
    if flip: q = mir(q)
    spot("Scent spot " + ("L" if flip else "R"), q, 16, 11, BORDER_FILL, 95)

def apex_spots(flip):
    for i, (x, y, w, h, col) in enumerate([(752, 252, 16, 11, "#F5A548"), (766, 276, 14, 10, "#F5A548"),
                                           (734, 244, 12, 9, "#F5A548"), (716, 246, 9, 7, "#FFFFFF"),
                                           (780, 236, 9, 7, "#FFFFFF"), (790, 262, 8, 6, "#FFFFFF")]):
        q = sc((x, y))
        if flip: q = mir(q)
        spot(f"Apex spot {'L' if flip else 'R'} {i+1}", q, w, h, rad("#FFFFFF", col) if col != "#FFFFFF" else SPOT, 92)

for flip in (False, True):
    sd = "L" if flip else "R"
    wing(f"Hind wing {sd}", HW, HW_D, HW_CELL, HW_VEINS, 6, [(3, 12, [(9, 7), (22, 8)])], flip, scent_spot)
for flip in (False, True):
    sd = "L" if flip else "R"
    wing(f"Fore wing {sd}", FW, FW_D, FW_CELL, FW_VEINS, 7, [(6, 11, [(9, 6), (21, 7)])], flip, apex_spots)
    # a soft sheen across the fore wing
    a, b = sc((600, 330)), sc((720, 300))
    if flip: a, b = mir(a), mir(b)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} Q{(a[0]+b[0])/2:.1f},{(a[1]+b[1])/2 - 14:.1f} {b[0]:.1f},{b[1]:.1f}",
           f"Fore wing sheen {sd}", fill=NONE, stroke="#FFF4D8", strokeWidth=10, opacity=16, cap="round")

# --- legs gripping the umbel -------------------------------------------------------------------
for i, pts in enumerate([[(490, 400), (470, 430), (462, 470)], [(492, 420), (476, 470), (472, 520)]]):
    for flip in (False, True):
        q = [mir(p) if flip else p for p in pts]
        q = [sc(p) for p in q]
        d.path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" % (q[0] + q[1] + q[2]), f"Leg {i+1} {'R' if flip else 'L'}",
               fill=NONE, stroke=INK, strokeWidth=4, cap="round", join="round", opacity=90)

# --- body: dotted thorax, slim abdomen, small head --------------------------------------------
BODY = rad("#4A3426", "#2A1A12", "#160D08")
a = sc((500, 412)); b = sc((500, 600))
d.path(f"M{a[0]-16:.1f},{a[1]:.1f} C{a[0]-18:.1f},{a[1]+60:.1f} {b[0]-10:.1f},{b[1]-40:.1f} {b[0]:.1f},{b[1]:.1f} "
       f"C{b[0]+10:.1f},{b[1]-40:.1f} {a[0]+18:.1f},{a[1]+60:.1f} {a[0]+16:.1f},{a[1]:.1f} Z",
       "Abdomen", fill=BODY, stroke=INK, strokeWidth=3)
for i in range(7):
    y = a[1] + 18 + i * 22
    w = 14 - i * 1.4
    d.path(f"M{500 - w:.1f},{y:.1f} Q500,{y + 5:.1f} {500 + w:.1f},{y:.1f}", f"Abdomen ring {i+1}",
           fill=NONE, stroke="#8C7A6A", strokeWidth=3, opacity=35, cap="round")
c = sc((500, 372))
d.shape("ellipse", "Thorax", x=round(c[0] - 24, 1), y=round(c[1] - 46, 1), width=48, height=92,
        fill=BODY, stroke=INK, strokeWidth=3)
for i, (dx, dy) in enumerate([(-12, -22), (12, -22), (-15, 0), (15, 0), (-10, 22), (10, 22), (0, -34)]):
    spot(f"Thorax dot {i+1}", (c[0] + dx, c[1] + dy), 6, 6, SPOT, 85)
d.shape("ellipse", "Thorax sheen", x=round(c[0] - 12, 1), y=round(c[1] - 36, 1), width=12, height=50,
        fill="#FFFFFF", opacity=12, stroke=NONE)
h = sc((500, 318))
d.shape("ellipse", "Head", x=round(h[0] - 17, 1), y=round(h[1] - 15, 1), width=34, height=30,
        fill=BODY, stroke=INK, strokeWidth=3)
for sd, dx in (("L", -11), ("R", 11)):
    d.shape("ellipse", f"Eye {sd}", x=round(h[0] + dx - 8, 1), y=round(h[1] - 8, 1), width=16, height=16,
            fill=rad("#5A4E44", "#1E1610"), stroke=INK, strokeWidth=2)
    spot(f"Eye glint {sd}", (h[0] + dx - 2, h[1] - 3), 4, 4, "#FFFFFF", 70)
    spot(f"Head dot {sd}", (h[0] + dx * 0.4, h[1] + 9), 4, 4, SPOT, 85)

# --- antennae: one straight, one bent at the middle -----------------------------------------------
la = [sc((494, 306)), sc((470, 250)), sc((438, 190))]
ra = [sc((506, 306)), sc((534, 250)), sc((600, 222))]
for nm, pts in (("Antenna L", la), ("Antenna R", ra)):
    d.path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" % (pts[0] + pts[1] + pts[2]), nm, fill=NONE, stroke=INK,
           strokeWidth=4, cap="round", join="round")
    tx, ty = pts[2][0] - pts[1][0], pts[2][1] - pts[1][1]
    ln = math.hypot(tx, ty)
    cx_, cy_ = pts[2][0] + tx / ln * 6, pts[2][1] + ty / ln * 6
    rot = math.degrees(math.atan2(ty, tx))
    k = 0.5523; rx, ry = 13, 6
    ca, sa = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    def R(x, y): return (cx_ + x * ca - y * sa, cy_ + x * sa + y * ca)
    e = [R(rx, 0), R(rx, ry*k), R(rx*k, ry), R(0, ry), R(-rx*k, ry), R(-rx, ry*k), R(-rx, 0),
         R(-rx, -ry*k), R(-rx*k, -ry), R(0, -ry), R(rx*k, -ry), R(rx, -ry*k)]
    s = "M%.1f,%.1f " % e[0] + " ".join("C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (e[i] + e[i+1] + e[(i+2) % 12])
                                       for i in (1, 4, 7, 10))
    d.path(s + " Z", nm + " club", fill=rad("#5A4A3E", "#1E1610"), stroke=INK, strokeWidth=2)
    spot(nm + " tip", R(5, 0), 4, 3, "#F2E6D0", 70)

# --- rim drawn last so everything inside closes under it -----------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#5E7048", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4F6E4", strokeWidth=3, opacity=45)

far = max(math.hypot(x - PCX, y - PCY) for x, y in REACH)
print(f"butterfly reach from disc center: {far:.0f} (inner ring 396)")
assert far < 392, far

# --- name + second line ------------------------------------------------------------------------
d.text("MONARCH", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#F3E2C2", justify="center")
r = d.text("LEPIDOPTERA", "Second line", x=500, y=975, size=22, font="Virelai Sans",
           color="#B8C99A", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=300)
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

d.finish("monarch-V1R00")
