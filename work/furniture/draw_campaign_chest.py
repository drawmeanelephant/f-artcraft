#!/usr/bin/env python3
"""Campaign chest — field plate V1R00. A dresser that expects to be moved:
two stacking mahogany boxes, brass corner straps, recessed brass pulls,
the upper box's top drawer pulled open showing its empty tray. Near-side
three-quarter view, mahogany on a dark plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Campaign Chest — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241108"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [round(x0, 1), round(y0, 1)],
            "end": [round(x1, 1), round(y1, 1)],
            "stops": [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {}))
                      for s in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

def mix(c0, c1, t):
    a = [int(c0[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(p + (q - p) * t):02X}" for p, q in zip(a, b))

# --- projection: x right, y up, z toward the viewer; seen from front-right, above ---
TH = math.radians(30)
CT, ST = math.cos(TH), math.sin(TH)
K, VC = 0.40, 0.95

def proj(x, y, z):
    return (x * CT - z * ST, (x * ST + z * CT) * K - y * VC)

OPS = []

def poly(label, pts3, fill=None, stroke=INK, sw=2.5, opacity=None, g=None):
    OPS.append(("poly", label, [proj(*p) for p in pts3], fill, stroke, sw, opacity,
                None if g is None else (proj(*g[0]), proj(*g[1]), g[2])))

def line(label, pts3, stroke, sw, opacity=None):
    OPS.append(("line", label, [proj(*p) for p in pts3], NONE, stroke, sw, opacity, None))

def front(x0, x1, y0, y1, z):
    return [(x0, y1, z), (x1, y1, z), (x1, y0, z), (x0, y0, z)]

def side(x, z0, z1, y0, y1):
    return [(x, y1, z1), (x, y1, z0), (x, y0, z0), (x, y0, z1)]

def top(x0, x1, z0, z1, y):
    return [(x0, y, z0), (x1, y, z0), (x1, y, z1), (x0, y, z1)]

# mahogany + brass palette
FRONT_ST  = [(0, "#8E4526"), (1, "#5E2C16")]
DRAWER_ST = [(0, "#9C5030"), (1, "#6E3418")]
SIDE_ST   = [(0, "#5E2E18"), (1, "#381A0C")]
TOP_ST    = [(0, "#A85C36"), (0.6, "#84411F"), (1, "#5E2C16")]
DARK_ST   = [(0, "#2A140A"), (1, "#140A04")]
BRASS     = [(0, "#F6DE96"), (0.5, "#CFA04A"), (1, "#8A6224")]
BRASS_DIM = [(0, "#C8A258"), (1, "#7A5622")]

W, D = 400, 195          # chest width, depth
FOOT_H, PLINTH = 16, 16
B1_0, B1_1 = FOOT_H + PLINTH, 218     # lower box
SEAM = 10
B2_0, B2_1 = B1_1 + SEAM, 414         # upper box
H = B2_1
SLAB = 16
OPEN_DZ = 62                          # how far the open drawer is pulled

def fg(x0, x1, y0, y1, z, st):
    return ((x0, y1, z), (x0 + (x1 - x0) * 0.2, y0, z), st)

def recess_pull(nm, cx, cy, z):
    """Flush campaign pull: brass bezel, dark recess, small bail."""
    poly(f"{nm} bezel", front(cx - 30, cx + 30, cy - 12, cy + 12, z), sw=2.2,
         g=((cx - 30, cy + 12, z), (cx + 30, cy - 12, z), BRASS))
    poly(f"{nm} recess", front(cx - 24, cx + 24, cy - 8, cy + 8, z), sw=1.6, stroke="#3A2410",
         g=((cx, cy + 8, z), (cx, cy - 8, z), [(0, "#1E0E04"), (1, "#4A2E14")]))
    pts = [(cx - 15 * math.cos(a / 8 * math.pi), cy - 1 - 9 * math.sin(a / 8 * math.pi), z + 1) for a in range(9)]
    line(f"{nm} bail", pts, "#8A6224", 4.5)
    line(f"{nm} bail light", pts[1:5], "#F8E2A0", 2.2, 80)

def keyhole(nm, cx, cy, z):
    poly(f"{nm} escutcheon", [(cx + 7 * math.cos(a / 12 * math.tau), cy + 7 * math.sin(a / 12 * math.tau), z)
                              for a in range(12)], sw=1.8,
         g=((cx - 7, cy + 7, z), (cx + 7, cy - 7, z), BRASS))
    poly(f"{nm} hole", [(cx - 1.4, cy + 2.5, z), (cx + 1.4, cy + 2.5, z),
                        (cx + 2, cy - 3.5, z), (cx - 2, cy - 3.5, z)], fill="#1E0E04", stroke=NONE)

def drawer(nm, x0, x1, y0, y1, z, pulls=2):
    poly(f"{nm} front", front(x0, x1, y0, y1, z), sw=2.5, g=fg(x0, x1, y0, y1, z, DRAWER_ST))
    line(f"{nm} bevel light", [(x0 + 3, y0 + 3, z), (x0 + 3, y1 - 3, z), (x1 - 3, y1 - 3, z)], "#E8A870", 2.2, 55)
    line(f"{nm} bevel shade", [(x1 - 3, y1 - 3, z), (x1 - 3, y0 + 3, z), (x0 + 3, y0 + 3, z)], "#3A1808", 2.2, 55)
    if pulls == 2:
        recess_pull(f"{nm} pull L", x0 + (x1 - x0) * 0.28, (y0 + y1) / 2, z)
        recess_pull(f"{nm} pull R", x0 + (x1 - x0) * 0.72, (y0 + y1) / 2, z)
    else:
        recess_pull(f"{nm} pull", (x0 + x1) / 2, (y0 + y1) / 2, z)

def corners(nm, x0, x1, y0, y1, z):
    """Brass corner straps on the box front: plate + stub arms at each corner."""
    for i, (cx, cy, sx, sy) in enumerate([(x0, y0, 1, 1), (x1, y0, -1, 1),
                                         (x0, y1, 1, -1), (x1, y1, -1, -1)]):
        px0, px1 = sorted((cx, cx + sx * 24))
        py0, py1 = sorted((cy, cy + sy * 24))
        poly(f"{nm} corner {i+1}", front(px0, px1, py0, py1, z), sw=2,
             g=((px0, py1, z), (px1, py0, z), BRASS))
        ax0, ax1 = sorted((cx + sx * 24, cx + sx * 58))
        poly(f"{nm} strap h{i+1}", front(ax0, ax1, py0 + 6, py1 - 6, z), sw=1.6,
             g=((ax0, py0, z), (ax1, py1, z), BRASS_DIM))
        ay0, ay1 = sorted((cy + sy * 24, cy + sy * 58))
        poly(f"{nm} strap v{i+1}", front(px0 + 6, px1 - 6, ay0, ay1, z), sw=1.6,
             g=((px0, ay0, z), (px1, ay1, z), BRASS_DIM))
        poly(f"{nm} rivet {i+1}", [(cx + sx * 12 + 4 * math.cos(a / 10 * math.tau),
                                    cy + sy * 12 + 4 * math.sin(a / 10 * math.tau), z) for a in range(10)],
             fill="#5E4218", stroke=NONE)

# --- feet + plinth ----------------------------------------------------------------------
for nm, fx in [("Front L", 26), ("Front R", W - 54)]:
    poly(f"Bun foot {nm}", front(fx, fx + 28, 0, FOOT_H, D), sw=2,
         g=((fx, FOOT_H, D), (fx, 0, D), [(0, "#5E2C16"), (1, "#2A1208")]))
    poly(f"Bun foot {nm} sole", top(fx - 2, fx + 30, D - 6, D + 6, 0), stroke=NONE, fill="#1E0C04")
poly("Rear foot hint", side(W, D - 60, D - 30, 0, FOOT_H), stroke=NONE, fill="#2A1208")
poly("Plinth front", front(4, W - 4, FOOT_H, FOOT_H + PLINTH, D + 2), sw=2.5,
     g=fg(4, W - 4, FOOT_H, FOOT_H + PLINTH, D + 2, [(0, "#7A3A1E"), (1, "#4E2412")]))
poly("Plinth right", side(W - 4, 0, D + 2, FOOT_H, FOOT_H + PLINTH), sw=2,
     g=((W - 4, FOOT_H + PLINTH, D), (W - 4, FOOT_H, 0), SIDE_ST))

# --- boxes ---------------------------------------------------------------------------------
for nm, y0, y1 in [("Lower box", B1_0, B1_1), ("Upper box", B2_0, B2_1)]:
    poly(f"{nm} front", front(0, W, y0, y1, D), sw=2.5, g=fg(0, W, y0, y1, D, FRONT_ST))
    poly(f"{nm} right side", side(W, 0, D, y0, y1), sw=2.5,
         g=((W, y1, D), (W, y0, 0), SIDE_ST))
    # side recessed carry handle (brass, folded into its recess)
    scy = (y0 + y1) / 2
    poly(f"{nm} side handle bezel", side(W, D / 2 - 36, D / 2 + 36, scy - 13, scy + 13), sw=2,
         g=((W, scy + 13, D / 2 - 36), (W, scy - 13, D / 2 + 36), BRASS_DIM))
    poly(f"{nm} side handle recess", side(W, D / 2 - 28, D / 2 + 28, scy - 8, scy + 8), stroke=NONE,
         g=((W, scy + 8, D / 2), (W, scy - 8, D / 2), [(0, "#180C04"), (1, "#3A1E0C")]))
    line(f"{nm} side handle bail", [(W, scy - 4, D / 2 - 18), (W, scy - 16, D / 2), (W, scy - 4, D / 2 + 18)],
         "#8A6224", 5)

# the seam between the two boxes: shadow reveal + brass edge strips
poly("Box seam shadow", front(0, W, B1_1, B2_0, D - 4), stroke=NONE,
     g=((0, B2_0, D - 4), (0, B1_1, D - 4), [(0, "#0E0602"), (1, "#341808")]))
line("Seam lower lip light", [(2, B1_1 - 2, D + 1), (W - 2, B1_1 - 2, D + 1)], "#C87A44", 3, 60)

# drawer layout: two drawers per box, inset
MX = 14
for nm, y0, y1 in [("Lower box", B1_0, B1_1), ("Upper box", B2_0, B2_1)]:
    dh = (y1 - y0 - 3 * 10) / 2
    for k in range(2):
        dy0 = y0 + 10 + k * (dh + 10)
        drawer(f"{nm} drawer {k+1}", MX, W - MX, dy0, dy0 + dh, D)

# --- the open drawer: upper box, top drawer pulled toward the viewer ----------------------
OY0, OY1 = B2_0 + 10 + (B2_1 - B2_0 - 3 * 10) / 2 + 10, B2_1 - 10
OZ = D + OPEN_DZ
# cavity left behind in the upper box
poly("Drawer cavity", front(MX, W - MX, OY0, OY1, D), stroke=NONE,
     g=((0, OY1, D), (0, OY0, D), DARK_ST))
poly("Cavity floor", [(MX, OY0, D), (W - MX, OY0, D), (W - MX, OY0, D - 26), (MX, OY0, D - 26)], stroke=NONE,
     g=((0, OY0, D - 26), (0, OY0, D), [(0, "#1E0E04"), (1, "#5E3418")]))
poly("Cavity right wall", [(W - MX, OY1, D), (W - MX, OY1, D - 22), (W - MX, OY0, D - 22), (W - MX, OY0, D)],
     stroke=NONE, g=((W - MX, OY1, D), (W - MX, OY0, D), [(0, "#3A1E0C"), (1, "#180C04")]))
# drawer box: front pulled proud, side cheeks running back into the cavity, tray floor visible
drawer("Open drawer", MX, W - MX, OY0, OY1, OZ)
for nm, dx in [("L", MX + 4), ("R", W - MX - 14)]:
    poly(f"Open drawer cheek {nm}", side(dx, D - 2, OZ, OY0 + 4, OY1 - 4), sw=2,
         g=((dx, OY1, OZ), (dx, OY0, D), [(0, "#6E3C1C"), (1, "#38180A")]))
poly("Open drawer tray", top(MX + 18, W - MX - 18, D - 2, OZ - 6, OY0 + 6), sw=2,
     g=((MX + 18, OY0 + 6, D - 2), (W - MX - 18, OY0 + 6, OZ - 6), [(0, "#7A4A24"), (1, "#A86838")]))
line("Tray front lip light", [(MX + 18, OY0 + 6, OZ - 6), (W - MX - 18, OY0 + 6, OZ - 6)], "#D89A5C", 3, 60)
keyhole("Open drawer", W / 2, OY0 - 6, OZ)

# --- brass corner straps on all four box front corners ------------------------------------
for nm, y0, y1 in [("Lower box", B1_0, B1_1), ("Upper box", B2_0, B2_1)]:
    corners(nm, 3, W - 3, y0 + 3, y1 - 3, D + 1)
keyhole("Upper box lock", W / 2, B2_0 - 5, D + 1)

# --- top slab + edge brass -----------------------------------------------------------------
TX0, TX1, TZ0, TZ1 = -8, W + 8, -8, D + 8
poly("Top slab", top(TX0, TX1, TZ0, TZ1, H + SLAB), sw=3,
     g=((TX0, H + SLAB, TZ0), (TX1, H + SLAB, TZ1), TOP_ST))
poly("Top slab front edge", front(TX0, TX1, H, H + SLAB, TZ1), sw=3,
     g=fg(TX0, TX1, H, H + SLAB, TZ1, FRONT_ST))
poly("Top slab right edge", side(TX1, TZ0, TZ1, H, H + SLAB), sw=3,
     g=((TX1, H + SLAB, TZ1), (TX1, H, TZ0), SIDE_ST))
line("Top edge highlight", [(TX0 + 4, H + SLAB, TZ1 - 2), (TX1 - 2, H + SLAB, TZ1 - 2), (TX1 - 2, H + SLAB, TZ0 + 4)],
     "#E8A870", 3, 70)
# brass strap stubs on the top's two front corners
for i, (cx, sx) in enumerate([(TX0 + 10, 1), (TX1 - 10, -1)]):
    poly(f"Top corner strap {i+1}", top(min(cx, cx + sx * 50), max(cx, cx + sx * 50), TZ1 - 22, TZ1, H + SLAB + 1),
         sw=1.6, g=((cx, H + SLAB, TZ1 - 22), (cx + sx * 50, H + SLAB, TZ1), BRASS_DIM))

# soft sheen on the chest front
poly("Front sheen", front(40, 150, B1_0 + 20, B2_1 - 30, D + 1), stroke=NONE,
     g=((60, B2_1 - 30, D), (140, B1_0 + 20, D), [(0, "#FFDCB0", 0.16), (1, "#FFDCB0", 0)]))

# --- fit to the disc ----------------------------------------------------------------------
xs = [p[0] for op in OPS for p in op[2]]
ys = [p[1] for op in OPS for p in op[2]]
bw, bh = max(xs) - min(xs), max(ys) - min(ys)
SC = min(560 / bw, 560 / bh)
OX = 500 - SC * (min(xs) + max(xs)) / 2
OY = 480 - SC * (min(ys) + max(ys)) / 2

def S(p):
    return (OX + SC * p[0], OY + SC * p[1])

def path_of(pts, closed):
    q = [S(p) for p in pts]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in q) + (" Z" if closed else "")

screen = [S(p) for op in OPS for p in op[2]]
for x, y in screen:
    assert math.hypot(x - PCX, y - PCY) <= PR - 26, (x, y)
FOOT_Y = max(y for _, y in screen)
print("fit: scale %.3f  bbox x %.0f..%.0f  y %.0f..%.0f" % (
    SC, min(s[0] for s in screen), max(s[0] for s in screen), min(s[1] for s in screen), FOOT_Y))

# --- backdrop + plate ----------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#181410"), (1, "#070605")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#443C34"), (0.6, "#2A2420"), (1, "#141110")), stroke=NONE)
d.shape("ellipse", "Lamplight", x=140, y=80, width=540, height=460,
        fill=rad((0, "#FFD9A0", 0.15), (1, "#FFD9A0", 0)), stroke=NONE)
# faint campaign-map lines on the wall
for i, (x0, y0, x1, y1) in enumerate([(170, 220, 300, 300), (300, 300, 360, 190),
                                      (700, 180, 800, 260), (800, 260, 860, 210)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Map line {i+1}", fill=NONE, stroke="#8A7A5E",
           strokeWidth=3, opacity=16)
for i, (x, y, w) in enumerate([(208, 210, 6), (782, 245, 7), (168, 620, 6), (830, 590, 7),
                               (428, 102, 6), (648, 106, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#9A8A70", opacity=32, stroke=NONE)

HZN = 700
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin(0, HZN, 0, 880, (0, "#3E2E1E", 0.55), (1, "#18100A", 0.9)), stroke=NONE)
d.shape("ellipse", "Chest shadow", x=230, y=FOOT_Y - 60, width=560, height=110,
        fill=rad((0, "#060403", 0.65), (1, "#060403", 0)), stroke=NONE)

# --- the chest ------------------------------------------------------------------------------
for kind, label, pts, fill, stroke, sw, op, g in OPS:
    kw = {}
    if g is not None and kind == "poly":
        s0, s1, stops = g
        a, b = S(s0), S(s1)
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) < 1:
            b = (a[0], a[1] + 1)
        fill = lin(a[0], a[1], b[0], b[1], *stops)
    if op is not None:
        kw["opacity"] = op
    if kind == "poly":
        d.path(path_of(pts, True), label, fill=fill, stroke=stroke,
               **({"strokeWidth": sw, "join": "round"} if stroke != NONE else {}), **kw)
    else:
        d.path(path_of(pts, False), label, fill=NONE, stroke=stroke, strokeWidth=sw, cap="round", join="round", **kw)

d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#0C0A08", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D9C79A", strokeWidth=3, opacity=26)

# --- captions -------------------------------------------------------------------------------
d.text("CAMPAIGN CHEST", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#F0E2C4", justify="center")
LINE2, SZ2, TRK = "MAHOGANY · BRASS", 22, 300
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#C2AE7E", justify="center")
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

d.finish("campaign-chest-V1R00")
