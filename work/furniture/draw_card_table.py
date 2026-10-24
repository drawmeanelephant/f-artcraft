#!/usr/bin/env python3
"""Card table — field plate V1R00. Bridge-night still life: a square
mahogany table on its folding legs, green baize top carrying a fanned
hand — ace of spades up — a waiting deck and a whisky tumbler. Seen
from front-right, above. Baize plate, bridge-night mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Card Table — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E120A"

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

# palette: mahogany + baize + brass
FRONT_ST = [(0, "#8E4526"), (1, "#5E2C16")]
SIDE_ST  = [(0, "#5E2E18"), (1, "#381A0C")]
TOP_ST   = [(0, "#A85C36"), (0.6, "#84411F"), (1, "#5E2C16")]
LEG_ST   = [(0, "#7A3A1E"), (1, "#4E2412")]
LEG_SIDE = [(0, "#3E1E0E"), (1, "#201008")]
FELT_ST  = [(0, "#4E9A66"), (0.65, "#357A4C"), (1, "#22583A")]
BRASS    = [(0, "#F6DE96"), (0.5, "#CFA04A"), (1, "#8A6224")]
IVORY    = [(0, "#F8F2E4"), (1, "#DCD2B8")]
RED      = "#B03028"
BLACK    = "#2A2620"

W, D = 360, 360            # square top
LEG = 262                  # leg height / underside of apron
APRON = 48
SLAB = 20
TY = LEG + APRON + SLAB    # top surface = 330
SPLAY = 9                  # outward drift of each foot

def leg(nm, x0, x1, z0, z1, sxd, szd):
    """Slightly splayed square leg: top rect under the apron, foot drifted
    out by (sxd*SPLAY, szd*SPLAY). Draws the two viewer-facing faces."""
    x0b, x1b = x0 + sxd * SPLAY, x1 + sxd * SPLAY
    z0b, z1b = z0 + szd * SPLAY, z1 + szd * SPLAY
    poly(f"{nm} front", [(x0b, 0, z1b), (x1b, 0, z1b), (x1, LEG, z1), (x0, LEG, z1)],
         sw=2.2, g=((x0b, LEG, z1b), (x1b, 0, z1b), LEG_ST))
    if sxd > 0:   # right leg: outer face is x1
        xf = [(x1b, 0, z0b), (x1b, 0, z1b), (x1, LEG, z1), (x1, LEG, z0)]
        ga, gb = (x1b, LEG, z1b), (x1b, 0, z0b)
    else:         # left leg: outer face is x0
        xf = [(x0b, 0, z1b), (x0b, 0, z0b), (x0, LEG, z0), (x0, LEG, z1)]
        ga, gb = (x0b, LEG, z0b), (x0b, 0, z1b)
    poly(f"{nm} outer", xf, sw=2.2, g=(ga, gb, LEG_SIDE))

LX0, LZ0 = 20, 20          # leg inset
LW = 26                    # leg width
leg("Back left leg",  LX0, LX0 + LW, LZ0, LZ0 + LW, -1, -1)
leg("Back right leg", W - LX0 - LW, W - LX0, LZ0, LZ0 + LW, 1, -1)
leg("Front left leg",  LX0, LX0 + LW, D - LZ0 - LW, D - LZ0, -1, 1)
leg("Front right leg", W - LX0 - LW, W - LX0, D - LZ0 - LW, D - LZ0, 1, 1)

# side stretchers between leg pairs, low — the folding-table brace; each bar
# runs from inside the back leg into the front leg so no end shows
for nm, x0, x1 in [("L", LX0 - 2, LX0 + 10), ("R", W - LX0 - 10, W - LX0 + 2)]:
    z_a, z_b = LZ0 + LW - 8, D - LZ0 - 4
    poly(f"Stretcher {nm} top", top(x0, x1, z_a, z_b, 70), stroke=NONE, fill="#4E2412")
    if x0 < W / 2:
        poly(f"Stretcher {nm} outer", [(x0, 44, z_b), (x0, 44, z_a), (x0, 70, z_a), (x0, 70, z_b)],
             sw=1.8, g=((x0, 70, z_a), (x0, 44, z_b), LEG_SIDE))
    else:
        poly(f"Stretcher {nm} outer", [(x1, 44, z_a), (x1, 44, z_b), (x1, 70, z_b), (x1, 70, z_a)],
             sw=1.8, g=((x1, 70, z_a), (x1, 44, z_b), LEG_SIDE))

# --- apron: shallow skirt inset under the slab ---------------------------------------------
AI = 8
poly("Apron right", side(W - AI, AI, D - AI, LEG, LEG + APRON), sw=2.4,
     g=((W - AI, LEG + APRON, D - AI), (W - AI, LEG, AI), SIDE_ST))
poly("Apron front", front(AI, W - AI, LEG, LEG + APRON, D - AI), sw=2.4,
     g=((AI, LEG + APRON, D - AI), (W - AI, LEG, D - AI), FRONT_ST))
line("Apron lower light", [(AI + 4, LEG + 3, D - AI + 1), (W - AI - 4, LEG + 3, D - AI + 1)],
     "#C87A44", 2.4, 55)
# folding brackets: small brass hinge plates on the apron above each front leg
for i, hx in enumerate([LX0 + LW / 2, W - LX0 - LW / 2]):
    poly(f"Hinge {i+1}", front(hx - 12, hx + 12, LEG + 10, LEG + APRON - 10, D - AI + 1), sw=1.8,
         g=((hx - 12, LEG + APRON - 10, D - AI + 1), (hx + 12, LEG + 10, D - AI + 1), BRASS))
    line(f"Hinge {i+1} knuckle", [(hx - 12, LEG + 24, D - AI + 2), (hx + 12, LEG + 24, D - AI + 2)],
         "#5E4218", 2, 80)

# --- top slab + baize ----------------------------------------------------------------------
TX0, TX1, TZ0, TZ1 = -6, W + 6, -6, D + 6
poly("Top slab", top(TX0, TX1, TZ0, TZ1, TY), sw=3,
     g=((TX0, TY, TZ0), (TX1, TY, TZ1), TOP_ST))
poly("Top slab right edge", side(TX1, TZ0, TZ1, TY - SLAB, TY), sw=3,
     g=((TX1, TY, TZ1), (TX1, TY - SLAB, TZ0), SIDE_ST))
poly("Top slab front edge", front(TX0, TX1, TY - SLAB, TY, TZ1), sw=3,
     g=((TX0, TY, TZ1), (TX1, TY - SLAB, TZ1), FRONT_ST))
line("Top edge highlight", [(TX0 + 4, TY + 1, TZ1 - 3), (TX1 - 3, TY + 1, TZ1 - 3),
                            (TX1 - 3, TY + 1, TZ0 + 4)], "#E8A870", 3, 65)
# baize inset
FB = 26
poly("Baize", top(TX0 + FB, TX1 - FB, TZ0 + FB, TZ1 - FB, TY + 1), sw=2, stroke="#173A26",
     g=((TX0 + FB, TY, TZ0 + FB), (TX1 - FB, TY, TZ1 - FB), FELT_ST))
poly("Baize light pool", top(90, 300, 70, 250, TY + 1.5), stroke=NONE,
     g=((150, TY, 120), (290, TY, 230), [(0, "#8ED8A4", 0.22), (1, "#8ED8A4", 0)]))
# felt edge stitch: a dashed inset line
stitch = []
for t in range(25):
    u = TX0 + FB + 10 + (TX1 - TX0 - 2 * FB - 20) * t / 24
    stitch.append((u, TY + 2, TZ0 + FB + 10))
line("Baize stitch front", stitch, "#9AD4AE", 2, 45)

# --- playing cards on the felt ---------------------------------------------------------------
CARD_W, CARD_L = 46, 64

def card_pts(cx, cz, ang, u, v):
    ca, sa = math.cos(ang), math.sin(ang)
    return (cx + u * ca - v * sa, cz + u * sa + v * ca)

def card(nm, cx, cz, ang, back=False):
    cs = [card_pts(cx, cz, ang, u, v) for u, v in
          [(-CARD_W / 2, -CARD_L / 2), (CARD_W / 2, -CARD_L / 2),
           (CARD_W / 2, CARD_L / 2), (-CARD_W / 2, CARD_L / 2)]]
    if back:
        poly(f"{nm} back", [(x, TY + 2, z) for x, z in cs], sw=2, stroke="#7A2A22",
             g=(card_pts(cx, cz, ang, -CARD_W / 2, -CARD_L / 2)[:1] + (TY,) + card_pts(cx, cz, ang, -CARD_W / 2, -CARD_L / 2)[1:],
                card_pts(cx, cz, ang, CARD_W / 2, CARD_L / 2)[:1] + (TY,) + card_pts(cx, cz, ang, CARD_W / 2, CARD_L / 2)[1:],
                [(0, "#B84A3E"), (1, "#8A2E24")]))
        ib = [card_pts(cx, cz, ang, u, v) for u, v in
              [(-CARD_W / 2 + 5, -CARD_L / 2 + 5), (CARD_W / 2 - 5, -CARD_L / 2 + 5),
               (CARD_W / 2 - 5, CARD_L / 2 - 5), (-CARD_W / 2 + 5, CARD_L / 2 - 5)]]
        lift = lambda p: (p[0], TY + 2.2, p[1])
        line(f"{nm} back border", [lift(p) for p in ib + [ib[0]]], "#F0E2C4", 2.2, 75)
        line(f"{nm} back cross", [lift(ib[0]), lift(ib[2])], "#F0E2C4", 1.8, 45)
        line(f"{nm} back cross 2", [lift(ib[1]), lift(ib[3])], "#F0E2C4", 1.8, 45)
        return
    poly(f"{nm} face", [(x, TY + 2, z) for x, z in cs], sw=2, stroke="#8A8274",
         g=(card_pts(cx, cz, ang, -CARD_W / 2, -CARD_L / 2)[:1] + (TY,) + card_pts(cx, cz, ang, -CARD_W / 2, -CARD_L / 2)[1:],
            card_pts(cx, cz, ang, CARD_W / 2, CARD_L / 2)[:1] + (TY,) + card_pts(cx, cz, ang, CARD_W / 2, CARD_L / 2)[1:],
            IVORY))

def heart_body(s, n, flip):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        u = 16 * math.sin(t) ** 3
        v = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        if flip:
            v = -v
        pts.append((u * s / 17.0, v * s / 17.0))
    return pts

def pip(nm, cx, cz, ang, u, v, s, suit, up=True):
    """Suit mark lying on the felt, in card-local (u,v) at scale s."""
    if suit == "diamond":
        body = [(0, -s), (0.62 * s, 0), (0, s), (-0.62 * s, 0)]
        stem = []
    elif suit == "heart":
        body = heart_body(s, 22, flip=not up)
        stem = []
    else:  # spade: flipped heart + stem
        body = heart_body(s, 22, flip=up)
        st = [(0.16 * s, -0.30 * s), (-0.16 * s, -0.30 * s), (0, -0.80 * s)]
        stem = [card_pts(cx, cz, ang, u + (a if up else -a), v + (b if up else -b)) for a, b in st]
    pts = [card_pts(cx, cz, ang, u + (a if up else -a), v + (b if up else -b)) for a, b in body]
    col = RED if suit in ("diamond", "heart") else BLACK
    poly(nm, [(x, TY + 2.4, z) for x, z in pts], stroke=NONE, fill=col)
    if stem:
        poly(f"{nm} stem", [(x, TY + 2.4, z) for x, z in stem], stroke=NONE, fill=col)

# the fanned hand, front-left of centre: diamond left, ace of spades up middle, heart right
card("Hand card L", 128, 236, math.radians(-21))
pip("Hand L pip", 128, 236, math.radians(-21), 0, 0, 11, "diamond")
pip("Hand L idx", 128, 236, math.radians(-21), -14, -22, 5, "diamond")
card("Hand card R", 220, 236, math.radians(21))
pip("Hand R pip", 220, 236, math.radians(21), 0, 0, 11, "heart")
pip("Hand R idx", 220, 236, math.radians(21), -14, -22, 5, "heart")
card("Hand card C", 174, 212, math.radians(-2))
pip("Ace body", 174, 212, math.radians(-2), 0, 0, 17, "spade")
pip("Ace idx", 174, 212, math.radians(-2), -14, -22, 5.5, "spade")
pip("Ace idx 2", 174, 212, math.radians(-2), 14, 22, 5.5, "spade", up=False)

# the waiting deck: three cards stacked, face down, drifting right-back
for i in range(3):
    card(f"Deck card {i+1}", 248 + i * 3, 112 - i * 2, math.radians(-8), back=(i == 2))

# --- fit to the disc ----------------------------------------------------------------------
xs = [p[0] for op in OPS for p in op[2]] + [proj(300, TY + 80, 178)[0]]
ys = [p[1] for op in OPS for p in op[2]] + [proj(300, TY + 80, 178)[1]]
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
        fill=lin(0, 0, 0, 1000, (0, "#0C1613"), (1, "#040806")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#5A7A66", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#2F6B4A"), (0.6, "#1B4630"), (1, "#0A2016")),
        stroke="#081410", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8E0CE", strokeWidth=3, opacity=26)
d.shape("ellipse", "Lamplight", x=240, y=130, width=520, height=460,
        fill=rad((0, "#FFE8B0", 0.14), (0.6, "#FFE8B0", 0.05), (1, "#FFE8B0", 0)), stroke=NONE)
for i, (x, y, w) in enumerate([(208, 215, 6), (782, 245, 7), (168, 615, 6), (830, 590, 7),
                               (428, 102, 6), (648, 108, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#8AB89E", opacity=30, stroke=NONE)

HZN = 700
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin(0, HZN, 0, 880, (0, "#1E2E24", 0.55), (1, "#0A120C", 0.9)), stroke=NONE)
d.shape("ellipse", "Table shadow", x=230, y=FOOT_Y - 34, width=560, height=96,
        fill=rad((0, "#040806", 0.62), (1, "#040806", 0)), stroke=NONE)

# --- the table -------------------------------------------------------------------------------
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

# --- the tumbler, back-right of the felt (screen space, like the adirondack's) ---------------
gbx, gby = S(proj(300, TY + 2, 178))
gr_b, gr_t = SC * 8.2, SC * 9.2
gty = gby - SC * 22
gyr_b, gyr_t = gr_b * 0.32, gr_t * 0.32
d.shape("ellipse", "Tumbler shadow", x=round(gbx - gr_b * 1.4), y=round(gby - gyr_b),
        width=round(gr_b * 2.8), height=round(gyr_b * 2.4),
        fill=rad((0, "#06100A", 0.55), (1, "#06100A", 0)), stroke=NONE)
d.path(f"M{gbx - gr_b:.1f},{gby:.1f} C{gbx - gr_b:.1f},{gby + gyr_b:.1f} "
       f"{gbx + gr_b:.1f},{gby + gyr_b:.1f} {gbx + gr_b:.1f},{gby:.1f} "
       f"L{gbx + gr_t:.1f},{gty:.1f} C{gbx + gr_t:.1f},{gty + gyr_t:.1f} "
       f"{gbx - gr_t:.1f},{gty + gyr_t:.1f} {gbx - gr_t:.1f},{gty:.1f} Z",
       "Tumbler body", fill=lin(gbx, gty, gbx, gby,
       (0, "#E8DCC2", 0.30), (0.6, "#C8A060", 0.55), (1, "#8A6434", 0.72)),
       stroke="#EADCC0", strokeWidth=2.0, join="round")
d.shape("ellipse", "Drink surface", x=round(gbx - gr_t + 3), y=round(gty - gyr_t + 3.5),
        width=round((gr_t - 3) * 2), height=round(gyr_t * 2),
        fill=rad((0, "#F0C87A", 0.9), (1, "#A06E28", 0.9)), stroke=NONE)
d.path(f"M{gbx - gr_t:.1f},{gty:.1f} C{gbx - gr_t:.1f},{gty - gyr_t:.1f} "
       f"{gbx + gr_t:.1f},{gty - gyr_t:.1f} {gbx + gr_t:.1f},{gty:.1f}",
       "Tumbler rim", fill=NONE, stroke="#F4E8CE", strokeWidth=2.4, opacity=85)
d.path(f"M{gbx - gr_t + 5:.1f},{gty + 4:.1f} L{gbx - gr_b + 5:.1f},{gby - 4:.1f}",
       "Tumbler streak", fill=NONE, stroke="#FAF0DC", strokeWidth=3, opacity=40)

d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#06100C", strokeWidth=6)

# --- captions -------------------------------------------------------------------------------
d.text("CARD TABLE", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#F0E8D2", justify="center")
LINE2, SZ2, TRK = "BAIZE · MAHOGANY · BRASS", 22, 300
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#A8C8B0", justify="center")
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

d.finish("card-table-V1R00")
