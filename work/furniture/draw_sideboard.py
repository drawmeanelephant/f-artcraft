#!/usr/bin/env python3
"""Sideboard — field plate V1R00. A long low breakfront cabinet for the
silver and the good bottles: two tapered-leg bays flanking a proud centre,
stringing on every edge, and on the top a pair of candlesticks, a ship's
decanter and two claret glasses. Seen from front-right, above.
Mahogany plate, dining-room mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Sideboard — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#200E06"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [round(x0, 1), round(y0, 1)],
            "end": [round(x1, 1), round(y1, 1)],
            "stops": [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {}))
                      for s in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

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

# mahogany + brass + silver palette
FRONT_ST = [(0, "#8E4526"), (1, "#5E2C16")]
PROUD_ST = [(0, "#9C5030"), (1, "#6E3418")]
SIDE_ST  = [(0, "#5E2E18"), (1, "#381A0C")]
TOP_ST   = [(0, "#B06038"), (0.6, "#8A4020"), (1, "#5E2C16")]
LEG_ST   = [(0, "#7A3A1E"), (1, "#4E2412")]
LEG_SIDE = [(0, "#3E1E0E"), (1, "#201008")]
INLAY    = "#E8C890"
BRASS    = [(0, "#F6DE96"), (0.5, "#CFA04A"), (1, "#8A6224")]
SILVER   = [(0, "#E8ECF0"), (0.5, "#A8B0BA"), (1, "#5C6470")]

W, D = 560, 170          # long, low
B0, B1 = 100, 310        # carcass bottom / top (legs below)
SLAB = 16
TY = B1 + SLAB           # top surface
CB0, CB1 = W * 0.34, W * 0.66   # proud centre bay
PROUD = 10

# --- legs: six, square tapered — the two rear first ------------------------------------------
def leg(nm, x, z, sx=1):
    """Tapered leg: 22 wide at the apron, 13 at the foot."""
    xt, xb, zt, zb = x, x + sx * 2.5, z, z + 2
    poly(f"{nm} front", [(xb, 0, zb + 13), (xb + 13, 0, zb + 13),
                         (xt + 22, B0, zt + 22), (xt, B0, zt + 22)],
         sw=2, g=((xt, B0, zt), (xb, 0, zb), LEG_ST))
    poly(f"{nm} side", [(xb + 13, 0, zb + 13), (xb + 13, 0, zb),
                        (xt + 22, B0, zt), (xt + 22, B0, zt + 22)],
         sw=2, g=((xt, B0, zt), (xb, 0, zb), LEG_SIDE))

leg("Rear left leg", 14, 14)
leg("Rear right leg", W - 36, 14)
leg("Front left leg", 14, D - 36)
leg("Front mid leg", CB0 + (CB1 - CB0) / 2 - 11, D + PROUD - 36)
leg("Front right leg", W - 36, D - 36)

# --- carcass: side bays at z=D, proud centre at z=D+PROUD -------------------------------------
poly("Right side", side(W, 0, D, B0, B1), sw=2.5,
     g=((W, B1, D), (W, B0, 0), SIDE_ST))
# side bays
poly("Left bay front", front(0, CB0, B0, B1, D), sw=2.4,
     g=((0, B1, D), (CB0, B0, D), FRONT_ST))
poly("Right bay front", front(CB1, W, B0, B1, D), sw=2.4,
     g=((CB1, B1, D), (W, B0, D), FRONT_ST))
# centre bay proud face + its little return cheeks
poly("Centre bay front", front(CB0, CB1, B0, B1, D + PROUD), sw=2.4,
     g=((CB0, B1, D + PROUD), (CB1, B0, D + PROUD), PROUD_ST))
poly("Centre bay left cheek", side(CB0, D, D + PROUD, B0, B1), sw=1.8,
     g=((CB0, B1, D + PROUD), (CB0, B0, D), SIDE_ST))
poly("Centre bay right cheek", side(CB1, D, D + PROUD, B0, B1), sw=1.8,
     g=((CB1, B1, D + PROUD), (CB1, B0, D), SIDE_ST))
# arched apron cut between the legs — a shallow arc rising at centre
apron = []
for t in range(25):
    u = t / 24
    apron.append((u * W, B0 - 14 - 16 * math.sin(math.pi * u) ** 1.3, D + 2))
poly("Apron", [(0, B0 + 2, D + 2), (W, B0 + 2, D + 2)] + list(reversed(apron)),
     sw=2.2, g=((0, B0 + 2, D), (W, B0 - 30, D), [(0, "#6E3418"), (1, "#4A1E0C")]))

# --- left cupboard door + right cupboard door ---------------------------------------------------
def cupboard(nm, x0, x1, y0, y1, z):
    m = 10
    poly(f"{nm} door", front(x0 + m, x1 - m, y0 + m, y1 - m, z), sw=2,
         g=((x0 + m, y1 - m, z), (x1 - m, y0 + m, z), PROUD_ST))
    # fielded panel
    p = m + 8
    poly(f"{nm} panel", front(x0 + m + p, x1 - m - p, y0 + m + p, y1 - m - p, z + 1), sw=1.6,
         g=((x0 + m + p, y1 - m - p, z), (x1 - m - p, y0 + m + p, z), FRONT_ST))
    line(f"{nm} mould light", [(x0 + m + p - 3, y0 + m + p - 3, z + 1),
                               (x0 + m + p - 3, y1 - m - p + 3, z + 1),
                               (x1 - m - p + 3, y1 - m - p + 3, z + 1)], "#E8A870", 2, 55)
    line(f"{nm} mould shade", [(x0 + m + p - 3, y0 + m + p - 3, z + 1),
                               (x1 - m - p + 3, y0 + m + p - 3, z + 1),
                               (x1 - m - p + 3, y1 - m - p + 3, z + 1)], "#381606", 2, 55)
    # oval escutcheon mid-inner edge
    ex = x1 - m - 12 if x0 < W / 2 else x0 + m + 12
    ey = (y0 + y1) / 2
    poly(f"{nm} escutcheon", [(ex + 5 * math.cos(a / 12 * math.tau),
                               ey + 8 * math.sin(a / 12 * math.tau), z + 2) for a in range(12)],
         sw=1.4, g=((ex - 5, ey + 8, z), (ex + 5, ey - 8, z), BRASS))

cupboard("Left cupboard", 8, CB0 - 8, B0 + 6, B1 - 6, D + 2)
cupboard("Right cupboard", CB1 + 8, W - 8, B0 + 6, B1 - 6, D + 2)

# --- centre: drawer over a deep cellarette drawer ------------------------------------------------
CDR_Z = D + PROUD + 2
def drawer(nm, x0, x1, y0, y1, z):
    m = 8
    poly(f"{nm} face", front(x0 + m, x1 - m, y0 + m, y1 - m, z), sw=2,
         g=((x0 + m, y1 - m, z), (x1 - m, y0 - m, z), FRONT_ST))
    line(f"{nm} bevel light", [(x0 + m + 4, y0 + m + 4, z + 1), (x0 + m + 4, y1 - m - 4, z + 1),
                               (x1 - m - 4, y1 - m - 4, z + 1)], "#E8A870", 2.2, 55)
    line(f"{nm} bevel shade", [(x1 - m - 4, y1 - m - 4, z + 1), (x1 - m - 4, y0 + m + 4, z + 1),
                               (x0 + m + 4, y0 + m + 4, z + 1)], "#381606", 2.2, 55)
    # ring pull: small plate + ring
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    poly(f"{nm} plate", [(cx + 7 * math.cos(a / 10 * math.tau), cy + 9 * math.sin(a / 10 * math.tau),
                          z + 1) for a in range(10)], sw=1.5,
         g=((cx - 7, cy + 9, z), (cx + 7, cy - 9, z), BRASS))
    ring = [(cx + 9 * math.cos(a / 12 * math.tau), cy - 4 - 11 * math.sin(a / 12 * math.tau),
             z + 2) for a in range(12)]
    line(f"{nm} ring", ring + [ring[0]], "#CFA04A", 3)

drawer("Top drawer", CB0 + 6, CB1 - 6, B1 - 62, B1 - 8, CDR_Z)
drawer("Cellarette", CB0 + 6, CB1 - 6, B0 + 6, B1 - 70, CDR_Z)

# --- stringing: a fine light inlay tracing each bay ----------------------------------------------
for nm, x0, x1, z in [("Left", 14, CB0 - 14, D + 3), ("Right", CB1 + 14, W - 14, D + 3),
                      ("Centre", CB0 + 12, CB1 - 12, CDR_Z + 1)]:
    line(f"Stringing {nm}", [(x0, B0 + 12, z), (x0, B1 - 12, z), (x1, B1 - 12, z),
                             (x1, B0 + 12, z), (x0, B0 + 12, z)], INLAY, 1.6, 70)

# --- top slab --------------------------------------------------------------------------------------
TX0, TX1, TZ0, TZ1 = -10, W + 10, -8, D + PROUD + 8
poly("Top slab right edge", side(TX1, TZ0, TZ1, B1, TY), sw=2.6,
     g=((TX1, TY, TZ1), (TX1, B1, TZ0), SIDE_ST))
poly("Top slab front edge", front(TX0, TX1, B1, TY, TZ1), sw=2.6,
     g=((TX0, TY, TZ1), (TX1, B1, TZ1), FRONT_ST))
poly("Top surface", top(TX0, TX1, TZ0, TZ1, TY), sw=2.6,
     g=((TX0, TY, TZ0), (TX1, TY, TZ1), TOP_ST))
line("Top edge light", [(TX0 + 4, TY + 1, TZ1 - 3), (TX1 - 4, TY + 1, TZ1 - 3),
                        (TX1 - 4, TY + 1, TZ0 + 4)], "#E8A870", 3, 65)
# serving glow across the middle of the top
poly("Top sheen", top(140, 420, 30, 130, TY + 1), stroke=NONE,
     g=((180, TY, 40), (400, TY, 120), [(0, "#FFD8A0", 0.10), (1, "#FFD8A0", 0)]))

# --- fit to the disc (props live above the top, so leave headroom) -------------------------------
xs = [p[0] for op in OPS for p in op[2]]
ys = [p[1] for op in OPS for p in op[2]] + [proj(W / 2, TY + 120, D / 2)[1]]
bw, bh = max(xs) - min(xs), max(ys) - min(ys)
SC = min(600 / bw, 540 / bh)
OX = 500 - SC * (min(xs) + max(xs)) / 2
OY = 500 - SC * (min(ys) + max(ys)) / 2

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

# --- backdrop + plate -----------------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#150C08"), (1, "#060302")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8A6A50", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5E2E22"), (0.6, "#381812"), (1, "#140806")),
        stroke="#100604", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D0B8", strokeWidth=3, opacity=26)
d.shape("ellipse", "Dining glow", x=230, y=110, width=540, height=460,
        fill=rad((0, "#FFDCA8", 0.16), (0.6, "#FFDCA8", 0.05), (1, "#FFDCA8", 0)), stroke=NONE)
for i, (x, y, w) in enumerate([(208, 215, 6), (782, 245, 7), (168, 615, 6), (830, 590, 7),
                               (428, 102, 6), (648, 108, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#C89878", opacity=30, stroke=NONE)

HZN = 700
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin(0, HZN, 0, 880, (0, "#322014", 0.55), (1, "#140A06", 0.9)), stroke=NONE)
d.shape("ellipse", "Sideboard shadow", x=200, y=FOOT_Y - 40, width=620, height=92,
        fill=rad((0, "#060302", 0.65), (1, "#060302", 0)), stroke=NONE)

# --- the sideboard ----------------------------------------------------------------------------------
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

# --- silver + glass on the top (screen space, bases projected) ---------------------------------------
def candlestick(nm, mx, mz):
    bx, by = S(proj(mx, TY + 1, mz))
    u = SC
    # contact shadow
    d.shape("ellipse", f"{nm} shadow", x=round(bx - 13 * u), y=round(by - 3 * u),
            width=round(26 * u), height=round(7 * u),
            fill=rad((0, "#0A0503", 0.5), (1, "#0A0503", 0)), stroke=NONE)
    # base disc, stem, knop, nozzle, candle, flame
    d.shape("ellipse", f"{nm} base", x=round(bx - 11 * u), y=round(by - 9 * u),
            width=round(22 * u), height=round(9 * u),
            fill=lin(bx - 11 * u, by, bx + 11 * u, by, *SILVER), stroke="#3C424C", strokeWidth=1.6)
    d.path(f"M{bx - 3.4 * u:.0f},{by - 5 * u:.0f} "
           f"C{bx - 7 * u:.0f},{by - 16 * u:.0f} {bx - 5 * u:.0f},{by - 26 * u:.0f} {bx - 3.4 * u:.0f},{by - 34 * u:.0f} "
           f"L{bx + 3.4 * u:.0f},{by - 34 * u:.0f} "
           f"C{bx + 5 * u:.0f},{by - 26 * u:.0f} {bx + 7 * u:.0f},{by - 16 * u:.0f} {bx + 3.4 * u:.0f},{by - 5 * u:.0f} Z",
           f"{nm} stem", fill=lin(bx - 6 * u, by - 20 * u, bx + 6 * u, by - 20 * u, *SILVER),
           stroke="#3C424C", strokeWidth=1.4)
    d.shape("ellipse", f"{nm} knop", x=round(bx - 6 * u), y=round(by - 30 * u),
            width=round(12 * u), height=round(8 * u),
            fill=lin(bx - 6 * u, by - 26 * u, bx + 6 * u, by - 26 * u, *SILVER), stroke="#3C424C", strokeWidth=1.4)
    d.shape("ellipse", f"{nm} nozzle", x=round(bx - 5 * u), y=round(by - 42 * u),
            width=round(10 * u), height=round(7 * u),
            fill=lin(bx - 5 * u, by - 38 * u, bx + 5 * u, by - 38 * u, *SILVER), stroke="#3C424C", strokeWidth=1.4)
    d.path(f"M{bx - 2.6 * u:.0f},{by - 38 * u:.0f} L{bx - 2.6 * u:.0f},{by - 58 * u:.0f} "
           f"L{bx + 2.6 * u:.0f},{by - 58 * u:.0f} L{bx + 2.6 * u:.0f},{by - 38 * u:.0f} Z",
           f"{nm} candle", fill=lin(bx, by - 58 * u, bx, by - 38 * u, (0, "#F4ECD8"), (1, "#D8CCAF")),
           stroke="#8A8274", strokeWidth=1.2)
    fx, fy = bx, by - 60 * u
    d.path(f"M{fx:.0f},{fy - 7 * u:.0f} C{fx - 3.4 * u:.0f},{fy - 3 * u:.0f} {fx - 2.4 * u:.0f},{fy + 1 * u:.0f} {fx:.0f},{fy + 2 * u:.0f} "
           f"C{fx + 2.4 * u:.0f},{fy + 1 * u:.0f} {fx + 3.4 * u:.0f},{fy - 3 * u:.0f} {fx:.0f},{fy - 7 * u:.0f} Z",
           f"{nm} flame", fill=rad((0, "#FFF2C8"), (0.7, "#F0A838"), (1, "#C06818")),
           stroke=NONE)
    d.shape("ellipse", f"{nm} flame glow", x=round(fx - 9 * u), y=round(fy - 12 * u),
            width=round(18 * u), height=round(16 * u),
            fill=rad((0, "#FFDC90", 0.5), (1, "#FFDC90", 0)), stroke=NONE)

candlestick("Left candlestick", 92, 66)
candlestick("Right candlestick", W - 82, 58)

# ship's decanter, centre-back — wide base, short neck, disc stopper
DX, DZp = W * 0.5 + 30, 60
dbx, dby = S(proj(DX, TY + 1, DZp))
u = SC
d.shape("ellipse", "Decanter shadow", x=round(dbx - 20 * u), y=round(dby - 4 * u),
        width=round(40 * u), height=round(9 * u),
        fill=rad((0, "#0A0503", 0.5), (1, "#0A0503", 0)), stroke=NONE)
d.path(f"M{dbx - 19 * u:.0f},{dby:.0f} "
       f"C{dbx - 19 * u:.0f},{dby - 14 * u:.0f} {dbx - 13 * u:.0f},{dby - 22 * u:.0f} {dbx - 5 * u:.0f},{dby - 30 * u:.0f} "
       f"L{dbx - 4 * u:.0f},{dby - 44 * u:.0f} L{dbx + 4 * u:.0f},{dby - 44 * u:.0f} "
       f"C{dbx + 13 * u:.0f},{dby - 22 * u:.0f} {dbx + 19 * u:.0f},{dby - 14 * u:.0f} {dbx + 19 * u:.0f},{dby:.0f} Z",
       "Decanter body", fill=lin(dbx, dby - 44 * u, dbx, dby,
       (0, "#E8D8B8", 0.22), (0.55, "#C08A3C", 0.55), (1, "#8A5420", 0.7)),
       stroke="#EADCC0", strokeWidth=1.8, join="round")
# wine inside, low shoulder
d.path(f"M{dbx - 16 * u:.0f},{dby - 1 * u:.0f} "
       f"C{dbx - 16 * u:.0f},{dby - 10 * u:.0f} {dbx - 11 * u:.0f},{dby - 16 * u:.0f} {dbx - 6 * u:.0f},{dby - 20 * u:.0f} "
       f"L{dbx + 6 * u:.0f},{dby - 20 * u:.0f} "
       f"C{dbx + 11 * u:.0f},{dby - 16 * u:.0f} {dbx + 16 * u:.0f},{dby - 10 * u:.0f} {dbx + 16 * u:.0f},{dby - 1 * u:.0f} Z",
       "Wine", fill=lin(dbx, dby - 20 * u, dbx, dby, (0, "#7A2418", 0.85), (1, "#4A1008", 0.85)), stroke=NONE)
d.shape("ellipse", "Decanter stopper", x=round(dbx - 7 * u), y=round(dby - 52 * u),
        width=round(14 * u), height=round(9 * u),
        fill=lin(dbx - 7 * u, dby - 48 * u, dbx + 7 * u, dby - 48 * u,
                 (0, "#F8F0DC", 0.9), (1, "#B09868", 0.9)), stroke="#C8B890", strokeWidth=1.4)
d.path(f"M{dbx - 12 * u:.0f},{dby - 8 * u:.0f} C{dbx - 12 * u:.0f},{dby - 16 * u:.0f} {dbx - 8 * u:.0f},{dby - 24 * u:.0f} {dbx - 5 * u:.0f},{dby - 30 * u:.0f}",
       "Decanter light", fill=NONE, stroke="#FAF0DC", strokeWidth=2.4, opacity=50)

# two claret glasses beside the decanter
for i, (gx, gz) in enumerate([(DX - 62, 88), (DX + 60, 96)]):
    cx, cy = S(proj(gx, TY + 1, gz))
    d.shape("ellipse", f"Glass {i+1} shadow", x=round(cx - 8 * u), y=round(cy - 2.4 * u),
            width=round(16 * u), height=round(5 * u),
            fill=rad((0, "#0A0503", 0.5), (1, "#0A0503", 0)), stroke=NONE)
    d.shape("ellipse", f"Glass {i+1} foot", x=round(cx - 6 * u), y=round(cy - 5 * u),
            width=round(12 * u), height=round(5 * u),
            fill=lin(cx - 6 * u, cy - 3 * u, cx + 6 * u, cy - 3 * u,
                     (0, "#F0E8D8", 0.75), (1, "#9A9078", 0.75)), stroke="#B0A890", strokeWidth=1.2)
    d.path(f"M{cx - 1.4 * u:.0f},{cy - 3 * u:.0f} L{cx - 1.4 * u:.0f},{cy - 16 * u:.0f} "
           f"L{cx + 1.4 * u:.0f},{cy - 16 * u:.0f} L{cx + 1.4 * u:.0f},{cy - 3 * u:.0f} Z",
           f"Glass {i+1} stem", fill=lin(cx, cy - 16 * u, cx, cy - 3 * u,
           (0, "#F0E8D8", 0.7), (1, "#9A9078", 0.7)), stroke="#B0A890", strokeWidth=1)
    d.path(f"M{cx - 7.5 * u:.0f},{cy - 30 * u:.0f} "
           f"C{cx - 8.5 * u:.0f},{cy - 20 * u:.0f} {cx - 6 * u:.0f},{cy - 14 * u:.0f} {cx:.0f},{cy - 14 * u:.0f} "
           f"C{cx + 6 * u:.0f},{cy - 14 * u:.0f} {cx + 8.5 * u:.0f},{cy - 20 * u:.0f} {cx + 7.5 * u:.0f},{cy - 30 * u:.0f} Z",
           f"Glass {i+1} bowl", fill=lin(cx, cy - 30 * u, cx, cy - 14 * u,
           (0, "#E8D8B8", 0.18), (1, "#C09858", 0.4)), stroke="#EADCC0", strokeWidth=1.4)
    d.path(f"M{cx - 5.4 * u:.0f},{cy - 24 * u:.0f} "
           f"C{cx - 5 * u:.0f},{cy - 18 * u:.0f} {cx + 5 * u:.0f},{cy - 18 * u:.0f} {cx + 5.4 * u:.0f},{cy - 24 * u:.0f} Z",
           f"Glass {i+1} wine", fill="#6E1E14", opacity=80, stroke=NONE)

# --- plate rim + captions ----------------------------------------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#0E0604", strokeWidth=6)

d.text("SIDEBOARD", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#F0E2CC", justify="center")
LINE2, SZ2, TRK = "MAHOGANY · SILVER · GLASS", 22, 300
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#C8AC94", justify="center")
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

d.finish("sideboard-V1R00")
