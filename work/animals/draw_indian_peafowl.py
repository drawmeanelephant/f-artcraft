#!/usr/bin/env python3
"""Indian peafowl — field plate V1R00. Cock in full display on a palace-garden
terrace: the train thrown up as a wall of eye-spotted coverts, electric-blue
neck and crested head centered in the fan. Front view — the ocelli face the
viewer. 1000x1000. House style: gradients + translucent shading, never flat
fills. Plate = circle center (500,460) r420; feather tips stay inside."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Indian Peafowl — Field Plate", 1000, 1000)

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

def spine(p0, p1, p2, p3, n=12):
    return [cubic(p0, p1, p2, p3, i / n) for i in range(n + 1)]

def ribbon(pts, w0, w1, label, fill, stroke=NONE, sw=0, opacity=None):
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
    kw = {"fill": fill}
    if stroke != NONE: kw["stroke"], kw["strokeWidth"] = stroke, sw
    if opacity is not None: kw["opacity"] = opacity
    d.path(dd, label, **kw)

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#1A1410"), (1, "#070503"))
PLATE_GRAD = rad((0, "#C9AC72"), (0.55, "#96794A"), (1, "#54402A"))
FIELD_GRAD = rad((0, "#3A7A50"), (0.6, "#23513A"), (1, "#123122"))
BARB_GRAD  = lin(500, 700, 500, 90, (0, "#4E7A3E"), (1, "#9AA84E"))
BODY_GRAD  = rad((0, "#3E8FE0"), (0.55, "#1E5AA8"), (1, "#0E2E5E"))
NECK_GRAD  = lin(500, 560, 500, 720, (0, "#4EA8E8"), (1, "#1A4E96"))
OC_OUT  = rad((0, "#C89A48"), (0.7, "#9A6E30"), (1, "#6E4A1E"))
OC_MID  = rad((0, "#2A4E38"), (1, "#141E14"))
OC_EYE  = rad((0, "#46D8C4"), (0.6, "#1E8EC0"), (1, "#12486E"))
FLOOR_GRAD = lin(0, 782, 0, 880, (0, "#8A6F44"), (1, "#4A3820"))

# --- backdrop + sandstone plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#8A6E3E", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A3A22", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0DFB4", strokeWidth=3, opacity=40)
d.shape("ellipse", "Patina 1", x=200, y=190, width=240, height=130, fill="#D8BE84", opacity=16, stroke=NONE)
d.shape("ellipse", "Patina 2", x=610, y=560, width=230, height=120, fill="#D8BE84", opacity=14, stroke=NONE)
for i, (x, y, w) in enumerate([(190,350,7),(800,300,8),(160,500,8),(845,470,7),(250,700,7),(755,720,8),
                               (145,610,6),(862,580,6),(395,105,7),(620,112,6),(330,818,6),(700,810,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E4A2C", opacity=38, stroke=NONE)
# low sun glow where the garden sits
d.shape("ellipse", "Sun glow", x=340, y=580, width=330, height=180, fill="#F4D98E", opacity=10, stroke=NONE)

# --- terrace floor, closing on the disc's own arc -----------------------------------
gy = 792
gdx = math.sqrt(R * R - (gy - CY) ** 2)
d.path(f"M{CX-gdx:.1f},{gy} C330,784 420,796 500,792 C590,788 670,796 {CX+gdx:.1f},{gy} "
       f"A{R},{R} 0 0 1 {CX-gdx:.1f},{gy} Z",
       "Terrace", fill=FLOOR_GRAD, opacity=90, stroke=NONE)
# balustrade seam lines on the terrace
for i, x0 in enumerate([300, 430, 570, 700]):
    d.path(f"M{x0},{gy+14} L{x0-6},{gy+58}", f"Baluster {i+1}",
           fill=NONE, stroke="#3E2E18", strokeWidth=3, opacity=45, cap="round")
# garden sprigs
for i, (x0, y0, x1, y1) in enumerate([(268,818,296,806),(724,822,752,810),(648,836,672,826)]):
    d.path(f"M{x0},{y0} Q{(x0+x1)//2},{y0-22} {x1},{y1}", f"Sprig {i+1}",
           fill=NONE, stroke="#7A8A4E", strokeWidth=3, opacity=55, cap="round")

# shadow under the bird
d.shape("ellipse", "Bird shadow", x=390, y=782, width=220, height=18,
        fill="#1E1406", opacity=42, stroke=NONE)

# --- the train: fan field first -----------------------------------------------------
BASE = (500, 688)
def tip_at(deg, rr):
    a = math.radians(deg)
    return (CX + rr * math.sin(a), CY - rr * math.cos(a))

# fan silhouette: edge feathers a touch shorter than center ones
edge_pts = [tip_at(t, 385 - 42 * (abs(t) / 80.0)) for t in range(-80, 81, 10)]
fan_pts = [BASE] + edge_pts + [BASE]
d.path(smooth(fan_pts), "Train field", fill=FIELD_GRAD, opacity=94,
       stroke=INK, strokeWidth=4)
# inner glow low on the fan where light catches the barbs
d.shape("ellipse", "Train glow", x=350, y=430, width=300, height=240,
        fill="#6E9A4E", opacity=16, stroke=NONE)

# --- covert feathers: tapered ribbons along each ray --------------------------------
RAYS = list(range(-78, 79, 12))            # 14 rays
def ray_curve(deg):
    a = math.radians(deg)
    rr = 385 - 42 * (abs(deg) / 80.0)
    tip = tip_at(deg, rr)
    # gentle outward bow through the middle of the feather
    c1 = (CX + rr * 0.35 * math.sin(a * 0.75), CY - rr * 0.35 * math.cos(a * 0.75))
    c2 = (CX + rr * 0.75 * math.sin(a * 0.92), CY - rr * 0.75 * math.cos(a * 0.92))
    return c1, c2, tip

for i, deg in enumerate(RAYS):
    c1, c2, tip = ray_curve(deg)
    ribbon(spine(BASE, c1, c2, tip), 8, 20, f"Covert {i+1}", BARB_GRAD, opacity=55)
    # fine quill line
    dd = "M%d,%d C%d,%d %d,%d %d,%d" % (BASE + c1 + c2 + tip)
    d.path(dd, f"Covert {i+1} quill", fill=NONE, stroke="#2E4E26",
           strokeWidth=2, opacity=55)

# --- ocelli --------------------------------------------------------------------------
def ocellus(cx, cy, s, tag):
    """Eye of the train: gold halo, dark ring, turquoise heart. s = scale."""
    w, h = 62 * s, 74 * s
    d.shape("ellipse", f"Ocellus {tag} halo", x=cx - w / 2, y=cy - h / 2,
            width=w, height=h, fill=OC_OUT, opacity=88, stroke=NONE)
    w2, h2 = 46 * s, 56 * s
    d.shape("ellipse", f"Ocellus {tag} ring", x=cx - w2 / 2, y=cy - h2 / 2,
            width=w2, height=h2, fill=OC_MID, stroke=NONE)
    # turquoise heart: teardrop broader at top, pointed below
    hw, hh = 15 * s, 21 * s
    d.path(f"M{cx},{cy - hh} C{cx + hw},{cy - hh + 4*s} {cx + hw},{cy + 2*s} {cx},{cy + hh} "
           f"C{cx - hw},{cy + 2*s} {cx - hw},{cy - hh + 4*s} {cx},{cy - hh} Z",
           f"Ocellus {tag} heart", fill=OC_EYE, stroke=NONE)
    d.shape("ellipse", f"Ocellus {tag} pupil", x=cx - 4.5 * s, y=cy - 6 * s,
            width=9 * s, height=13 * s, fill="#0E2440", stroke=NONE)

# outer ring: one eye at each ray tip, pulled in a little off the tip
for i, deg in enumerate(RAYS):
    rr = 385 - 42 * (abs(deg) / 80.0)
    x, y = tip_at(deg, rr - 34)
    ocellus(x, y, 1.0 - 0.18 * (abs(deg) / 80.0), f"T{i+1}")
# middle ring, between rays
for i, deg in enumerate(range(-66, 67, 24)):
    x, y = tip_at(deg, 252 - 20 * (abs(deg) / 80.0))
    ocellus(x, y, 0.72, f"M{i+1}")
# inner sparks, smallest
for i, deg in enumerate([-40, 0, 40]):
    x, y = tip_at(deg, 158)
    ocellus(x, y, 0.5, f"I{i+1}")

# --- the bird, standing in front of the fan -------------------------------------------
# legs
for j, x in enumerate([480, 520]):
    d.path(f"M{x},752 L{x-5},794", f"Leg {j+1}", fill=NONE, stroke="#241810",
           strokeWidth=5, cap="round")
for j, x in enumerate([475, 515]):
    for k, dx in enumerate([-9, 0, 9]):
        d.path(f"M{x+dx},794 L{x+dx+(dx if dx else 5)*0.8:.0f},800",
               f"Toe {j+1}.{k+1}", fill=NONE, stroke="#3E2E1C",
               strokeWidth=3.5, cap="round")

# body + neck as one column: narrow neck flaring into the breast
d.path(smooth([(500,578),(521,584),(527,608),(533,638),(548,670),(556,712),
               (552,748),(532,772),(500,780),(468,772),(448,748),(444,712),
               (452,670),(467,638),(473,608),(479,584)]),
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=5)
# breast iridescence
d.shape("ellipse", "Breast light", x=458, y=610, width=84, height=96,
        fill="#5EC4F0", opacity=22, stroke=NONE)
d.shape("ellipse", "Belly shade", x=450, y=734, width=100, height=32,
        fill="#0A2040", opacity=35, stroke=NONE)
# folded wings barred dark at the flanks
for sgn in (-1, 1):
    d.path(smooth([(500+sgn*46,640),(500+sgn*62,668),(500+sgn*58,714),
                   (500+sgn*42,738),(500+sgn*30,726),(500+sgn*34,678)]),
           f"Wing {'L' if sgn<0 else 'R'}", fill="#122A50", opacity=60,
           stroke=INK, strokeWidth=2.5)
    for m, yy in enumerate([668, 692, 714]):
        d.path(f"M{500+sgn*40},{yy} Q{500+sgn*56},{yy+4} {500+sgn*58},{yy+10}",
               f"Wing bar {sgn}.{m}", fill=NONE, stroke="#C89848",
               strokeWidth=3, opacity=55, cap="round")

# head — deep royal, smaller than the neck top so the column reads
d.path(smooth([(500,528),(524,534),(530,556),(522,578),(500,586),
               (478,578),(470,556),(476,534)]),
       "Head", fill=rad((0, "#3A86D8"), (1, "#143E80")), stroke=INK, strokeWidth=4)
d.shape("ellipse", "Head light", x=484, y=536, width=26, height=20,
        fill="#7AD4F4", opacity=25, stroke=NONE)
# eyes + the white facial stripes of the Indian cock
for sgn in (-1, 1):
    d.shape("ellipse", f"Eye {'L' if sgn<0 else 'R'}",
            x=500 + sgn*13 - 4, y=550, width=8, height=9, fill="#0A1626", stroke=NONE)
    d.path(f"M{500+sgn*7},540 Q{500+sgn*15},536 {500+sgn*22},542",
           f"Brow {'L' if sgn<0 else 'R'}", fill=NONE, stroke="#F2F6EE",
           strokeWidth=2.5, opacity=80, cap="round")
    d.path(f"M{500+sgn*8},566 Q{500+sgn*15},570 {500+sgn*21},564",
           f"Cheek {'L' if sgn<0 else 'R'}", fill=NONE, stroke="#F2F6EE",
           strokeWidth=2.5, opacity=70, cap="round")
# beak: small wedge pointing down
d.path("M493,578 L507,578 L500,594 Z", "Beak", fill="#1E1410", stroke=NONE)
# crest: three bare shafts tipped with little fanlets
for k, dx in enumerate([-11, 0, 11]):
    fy = 506 - (4 if dx == 0 else 0)
    d.path(f"M{500+dx*0.35:.0f},528 L{500+dx:.0f},{fy+4}",
           f"Crest shaft {k+1}", fill=NONE, stroke="#123260",
           strokeWidth=3, cap="round")
    d.shape("ellipse", f"Crest fan {k+1}", x=500 + dx - 8, y=fy - 6, width=16, height=12,
            fill="#3A86D8", stroke="#0E2A4E", strokeWidth=2)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#3A2E18", strokeWidth=6)

# --- name -----------------------------------------------------------------------------
d.text("INDIAN PEAFOWL", "Name", x=500, y=962, size=52, font="Virelai Sans",
       color="#EDE3BC", justify="center")

d.finish("indian-peafowl-V1R00")
