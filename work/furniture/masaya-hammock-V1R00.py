#!/usr/bin/env python3
"""Masaya hammock — field plate V1R00. A handwoven cotton hammock in the
Masaya (Nicaragua) tradition: gathered ends with a bridle of cords fanning
to each suspension loop — no spreader bars — the bed hanging empty in a
soft catenary. Calado openwork panels near the ends, a lace cenca edge
with restrained fringe, natural cotton with one muted terracotta band.
Slung on a minimal two-post wood stand; everything inside the rim.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Masaya Hammock — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2E1B0E"


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def rim_x(y, side=-1):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)


def par_y(x, x0, y0, x1, y1, sag):
    """y on the chord-sagging parabola; sag = depth below chord at centre."""
    t = (x - x0) / (x1 - x0)
    return y0 * (1 - t) + y1 * t + sag * 4 * t * (1 - t)


def par_q(x0, y0, x1, y1, sag):
    """quadratic-Bezier control point for the same sagging parabola."""
    return ((x0 + x1) / 2, (y0 + y1) / 2 + 2 * sag)


# --- palette -------------------------------------------------------------------
BG_GRAD = lin(0, 0, 0, 1000, (0, "#181009"), (1, "#070403"))
PLATE_GRAD = rad((0, "#C69A62"), (0.55, "#8A5E36"), (1, "#462A14"))
COTTON = lin(500, 440, 500, 660, (0, "#F4E6C8"), (0.55, "#DCC69E"), (1, "#AD9268"))
CAVITY = lin(500, 430, 500, 560, (0, "#54402A"), (1, "#221505"))
BAND = lin(450, 450, 550, 640, (0, "#A85C42"), (0.6, "#8A4630"), (1, "#6A3220"))
WOOD = lin(210, 300, 210, 760, (0, "#5C3C22"), (1, "#2E1A0C"))
FLOOR = lin(0, 770, 0, 880, (0, "#54402A"), (0.6, "#352412"), (1, "#1C1008"))

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=58, y=18, width=884, height=884, fill="#E8C88A", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#33200F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0DCB0", strokeWidth=3, opacity=40)

# late light pooling upper-left
d.shape("ellipse", "Light pool", x=260, y=150, width=360, height=210,
        fill="#F4DCA8", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(300, 260, 22), (430, 200, 16), (580, 210, 20),
                               (700, 300, 15), (240, 420, 18), (760, 450, 20),
                               (500, 300, 13), (650, 400, 16)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Dust {i+1}", x=x - w / 2, y=y - w / 3, width=w, height=w * 0.66,
            fill="#F4E0B4", opacity=14, stroke=NONE)

# --- floor, closing on the disc arc ----------------------------------------------
fy = 772
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C330,758 420,780 500,772 C580,764 680,768 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C330,758 420,780 500,772 C580,764 680,768 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#D8BC86", strokeWidth=4, opacity=40, cap="round")
# soft shadows: sling hangs over the floor, posts stand on it
d.shape("ellipse", "Hammock shadow", x=330, y=762, width=340, height=26,
        fill="#120A04", opacity=32, stroke=NONE)
d.shape("ellipse", "Post shadow L", x=186, y=758, width=72, height=16,
        fill="#120A04", opacity=38, stroke=NONE)
d.shape("ellipse", "Post shadow R", x=742, y=758, width=72, height=16,
        fill="#120A04", opacity=38, stroke=NONE)

# --- the stand: two slightly splayed wood posts + feet -----------------------------
def post(top, bot, wt, wb, label):
    tx, ty = top; bx, by = bot
    dx, dy = bx - tx, by - ty
    ln = math.hypot(dx, dy); nx, ny = -dy / ln, dx / ln
    pts = [(tx + nx * wt / 2, ty + ny * wt / 2), (tx - nx * wt / 2, ty - ny * wt / 2),
           (bx - nx * wb / 2, by - ny * wb / 2), (bx + nx * wb / 2, by + ny * wb / 2)]
    d.path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" % tuple(sum(pts, ())),
           label, fill=WOOD, stroke=INK, strokeWidth=4)
    # grain
    d.path(f"M{tx + dx * 0.2:.0f},{ty + dy * 0.2:.0f} L{tx + dx * 0.85:.0f},{ty + dy * 0.85:.0f}",
           f"{label} grain", fill=NONE, stroke="#1E1008", strokeWidth=3, opacity=45, cap="round")


post((232, 306), (216, 748), 22, 30, "Post L")
post((768, 306), (784, 748), 22, 30, "Post R")
d.path(rot_rect_path(216, 752, 78, 16, -4), "Foot L", fill=WOOD, stroke=INK, strokeWidth=4)
d.path(rot_rect_path(784, 752, 78, 16, 4), "Foot R", fill=WOOD, stroke=INK, strokeWidth=4)
# pegs the loops hang on
d.shape("ellipse", "Peg L", x=222, y=288, width=20, height=14, fill="#3A2414", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Peg R", x=758, y=288, width=20, height=14, fill="#3A2414", stroke=INK, strokeWidth=3)

# --- suspension: loop ring + bridle fan each end ----------------------------------
# ring at each post top
for side, (rx, ry) in (("L", (240, 296)), ("R", (760, 296))):
    d.shape("ellipse", f"Loop {side}", x=rx - 13, y=ry - 13, width=26, height=26,
            fill=NONE, stroke="#E8D6B0", strokeWidth=5)
# bridle: cords fan from the ring down to the gathered end of the bed
BR_L, BR_R = (240, 296), (760, 296)
land_l = [(296, 416), (300, 428), (303, 440), (305, 452), (306, 464), (306, 476), (302, 486)]
land_r = [(704, 416), (700, 428), (697, 440), (695, 452), (694, 464), (694, 476), (698, 486)]
for i, p in enumerate(land_l):
    d.path(f"M{BR_L[0]},{BR_L[1] + 12} Q{(BR_L[0] + p[0]) / 2 - 4},{(BR_L[1] + p[1]) / 2} {p[0]},{p[1]}",
           f"Bridle L{i+1}", fill=NONE, stroke="#E6D3AA", strokeWidth=3, cap="round")
for i, p in enumerate(land_r):
    d.path(f"M{BR_R[0]},{BR_R[1] + 12} Q{(BR_R[0] + p[0]) / 2 + 4},{(BR_R[1] + p[1]) / 2} {p[0]},{p[1]}",
           f"Bridle R{i+1}", fill=NONE, stroke="#E6D3AA", strokeWidth=3, cap="round")

# --- the bed ----------------------------------------------------------------------
# catenary keylines
FAR = (312, 430, 688, 430, 46)      # far rim: dips to ~476 at centre
NEAR = (310, 458, 690, 458, 110)    # near rim: dips to ~568
BOT = (318, 474, 682, 474, 174)     # bottom hem: dips to ~648

def rim_curve(rim):
    x0, y0, x1, y1, s = rim
    c = par_q(x0, y0, x1, y1, s)
    return f"M{x0},{y0} Q{c[0]:.0f},{c[1]:.0f} {x1},{y1}"

# interior cavity: between far rim and near rim, dark inside the sling
fx0, fy0, fx1, fy1, fs = FAR
nx0, ny0, nx1, ny1, ns = NEAR
fc = par_q(fx0, fy0, fx1, fy1, fs)
nc = par_q(nx1, ny1, nx0, ny0, ns)   # reversed traversal keeps the same sag
d.path(f"M{fx0},{fy0} Q{fc[0]:.0f},{fc[1]:.0f} {fx1},{fy1} "
       f"Q{nc[0]:.0f},{nc[1]:.0f} {nx0},{ny0} Z",
       "Cavity", fill=CAVITY, stroke=NONE)
# far-side fringe hinting inside the cavity — thin strands, barely lit
for i, x in enumerate(range(352, 660, 34)):
    y = par_y(x, *FAR) + 2
    sw = 1 if i % 2 else -1
    d.path(f"M{x},{y:.0f} q{sw * 2},14 {sw * 5},26", f"Far fringe {i+1}", fill=NONE,
           stroke="#C4AA80", strokeWidth=1.8, opacity=42, cap="round")
# lit inner wall of the sling — a pale wash hugging the near rim from inside
nx0, ny0, nx1, ny1, ns = NEAR
inc = par_q(nx0, ny0, nx1, ny1, ns - 26)
d.path(f"M{nx0 + 6},{ny0 + 4} Q{inc[0]:.0f},{inc[1]:.0f} {nx1 - 6},{ny1 + 4}",
       "Inner wall light", fill=NONE, stroke="#8A7350", strokeWidth=12,
       opacity=30, cap="round")
# far rim edge
d.path(rim_curve(FAR), "Far rim", fill=NONE, stroke="#C9B089", strokeWidth=5, cap="round")

# front wall of the sling, between near rim and bottom hem
bx0, by0, bx1, by1, bs = BOT
bc = par_q(bx1, by1, bx0, by0, bs)   # reversed traversal keeps the same sag
d.path(f"{rim_curve(NEAR)} L{bx1},{by0} Q{bc[0]:.0f},{bc[1]:.0f} {bx0},{by0} Z",
       "Bed wall", fill=COTTON, stroke=INK, strokeWidth=5)

# calado openwork panels near each end — translucent depth + diamond lattice
def diamonds(xa, xb, cols, label):
    for i in range(cols):
        x = xa + (xb - xa) * (i + 0.5) / cols
        yt = par_y(x, *NEAR) + 8
        yb = par_y(x, *BOT) - 10
        for j, f in enumerate((0.24, 0.52, 0.8)):
            y = yt + (yb - yt) * f
            d.path(f"M{x},{y - 10:.0f} L{x + 8:.0f},{y:.0f} L{x},{y + 10:.0f} L{x - 8:.0f},{y:.0f} Z",
                   f"{label} diamond {i+1}-{j+1}", fill=NONE, stroke="#F0E0BC",
                   strokeWidth=2.6, opacity=85)

for xa, xb, lbl in ((360, 440, "Calado L"), (560, 640, "Calado R")):
    xmid = (xa + xb) / 2
    yt = par_y(xmid, *NEAR) + 4
    yb = par_y(xmid, *BOT) - 4
    d.path(f"M{xa},{par_y(xa, *NEAR) + 4:.0f} L{xb},{par_y(xb, *NEAR) + 4:.0f} "
           f"L{xb},{par_y(xb, *BOT) - 4:.0f} L{xa},{par_y(xa, *BOT) - 4:.0f} Z",
           f"{lbl} shadow", fill="#3A2A16", opacity=38, stroke=NONE)
    diamonds(xa, xb, 4, lbl)

# one muted colour band across the wall, a slice following the bed's curves
bxa, bxb = 460, 542
d.path(f"M{bxa},{par_y(bxa, *NEAR) + 2:.0f} C{bxa - 7},{par_y(bxa, *NEAR) + 40:.0f} "
       f"{bxa - 9},{par_y(bxa, *BOT) - 40:.0f} {bxa},{par_y(bxa, *BOT) - 2:.0f} "
       f"L{bxb},{par_y(bxb, *BOT) - 2:.0f} C{bxb + 9},{par_y(bxb, *BOT) - 40:.0f} "
       f"{bxb + 7},{par_y(bxb, *NEAR) + 40:.0f} {bxb},{par_y(bxb, *NEAR) + 2:.0f} Z",
       "Colour band", fill=BAND, opacity=92, stroke=NONE)
# cream pinstripes woven at the band edges
for x in (bxa + 4, bxb - 4):
    d.path(f"M{x},{par_y(x, *NEAR) + 3:.0f} C{x - 6},{par_y(x, *NEAR) + 40:.0f} "
           f"{x - 8},{par_y(x, *BOT) - 40:.0f} {x},{par_y(x, *BOT) - 4:.0f}",
           f"Band stripe {x}", fill=NONE, stroke="#EADBB6", strokeWidth=2.4, opacity=80)

# woven weft rows following the wall's form
for j, f in enumerate((0.18, 0.42, 0.66, 0.88)):
    p0 = (330, par_y(330, *NEAR) + (par_y(330, *BOT) - par_y(330, *NEAR)) * f)
    p1 = (670, par_y(670, *NEAR) + (par_y(670, *BOT) - par_y(670, *NEAR)) * f)
    mid = (500, par_y(500, *NEAR) + (par_y(500, *BOT) - par_y(500, *NEAR)) * f)
    d.path(f"M{p0[0]:.0f},{p0[1]:.0f} Q{mid[0]},{mid[1] + 14:.0f} {p1[0]:.0f},{p1[1]:.0f}",
           f"Weft {j+1}", fill=NONE, stroke="#8A7050", strokeWidth=3, opacity=28, cap="round")
# bottom rounding shadow
bx0, by0, bx1, by1, bs = BOT
d.path(f"M{bx0 + 16},{by0 + 18:.0f} Q500,{by0 + bs * 2:.0f} {bx1 - 16},{by0 + 18:.0f}",
       "Bottom shade", fill=NONE, stroke="#6E5638", strokeWidth=14, opacity=30, cap="round")

# near rim binding
d.path(rim_curve(NEAR), "Near rim", fill=NONE, stroke="#F4E6C8", strokeWidth=6, cap="round")

# cenca lace edge — a row of small open diamonds just under the near rim
for i in range(15):
    x = 340 + i * 23
    y = par_y(x, *NEAR) + 15
    d.path(f"M{x},{y - 8:.0f} L{x + 7:.0f},{y:.0f} L{x},{y + 8:.0f} L{x - 7:.0f},{y:.0f} Z",
           f"Lace {i+1}", fill=NONE, stroke="#EADBB6", strokeWidth=2.2, opacity=75)

# restrained fringe hanging from the near rim over the wall
for i in range(34):
    x = 322 + i * 10.6
    y = par_y(x, *NEAR)
    ln = 20 + (i % 3) * 6
    sw = 1 if i % 5 else -1
    d.path(f"M{x:.0f},{y:.0f} q{sw * 2},{ln * 0.55:.0f} {sw * 4},{ln}",
           f"Fringe {i+1}", fill=NONE, stroke="#EADBB6", strokeWidth=2.4,
           opacity=80, cap="round")

# gathered end bundles — wrapped cotton arms the bridle lands on
for side, cx, cy, ang in (("L", 298, 452, -10), ("R", 702, 452, 10)):
    d.path(rot_rect_path(cx, cy, 20, 74, ang), f"Bundle {side}",
           fill=lin(cx - 10, cy - 40, cx + 10, cy + 40, (0, "#EAD9B6"), (1, "#9A805A")),
           stroke=INK, strokeWidth=4)
    for k in (-18, 0, 18):
        d.path(f"M{cx - 9},{cy + k} Q{cx},{cy + k + 6} {cx + 9},{cy + k}",
               f"Wrap {side} {k}", fill=NONE, stroke="#7A6244", strokeWidth=3, opacity=70)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#33200F", strokeWidth=6)

# --- caption ----------------------------------------------------------------------
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
    n = d.text(name, "Name", x=500, y=930, size=56, font="Virelai Sans",
               color="#F2E2C4", justify="center")
    m = d.text(mats, "Materials", x=500, y=966, size=23, font="Virelai Sans",
               color="#C4A982", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=50)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=280)
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


caption("MASAYA HAMMOCK", "COTTON")
d.finish("masaya-hammock-V1R00")
