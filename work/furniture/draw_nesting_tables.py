#!/usr/bin/env python3
"""Nesting tables — field plate V1R00. Three walnut tables of one design in
three sizes, three-quarter view from the front-right and a little above.
The two smaller tables are pulled forward out of the largest so the three
tops step down toward the viewer like a staircase. Thin tapered legs with
brass sabots; warm dark plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Nesting Tables — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A170E"   # warm umber, not black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [round(x0, 1), round(y0, 1)],
            "end": [round(x1, 1), round(y1, 1)],
            "stops": [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {}))
                      for s in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}

# --- projection: x right, y up, z toward the viewer; seen from front-right, above -------
TH = math.radians(28)
CT, ST = math.cos(TH), math.sin(TH)
K, VC = 0.42, 0.90          # floor foreshortening, vertical scale

def proj(x, y, z):
    return (x * CT - z * ST, (x * ST + z * CT) * K - y * VC)

# Geometry is collected in local screen space first, then scaled + centred on the
# disc, so the three tables can be tuned in world units without hand-placing.
OPS = []

def poly(label, pts3, fill, stroke=INK, sw=2.5, opacity=None, g=None):
    """g = (p3_start, p3_end, stops) for a linear gradient in world coordinates."""
    OPS.append(("poly", label, [proj(*p) for p in pts3], fill, stroke, sw, opacity,
                None if g is None else (proj(*g[0]), proj(*g[1]), g[2])))

def line(label, pts3, stroke, sw, opacity=None):
    OPS.append(("line", label, [proj(*p) for p in pts3], NONE, stroke, sw, opacity, None))

# walnut palette
TOP_ST = [(0, "#A06B45"), (0.55, "#7E4F31"), (1, "#5C3720")]
FRONT_ST = [(0, "#6E4329"), (1, "#45291A")]
SIDE_ST = [(0, "#52311F"), (1, "#301C11")]
LEG_F = [(0, "#7A4B2E"), (1, "#4A2C1A")]
LEG_S = [(0, "#4C2D1B"), (1, "#2E1B10")]
BRASS_F = [(0, "#F1D58C"), (0.5, "#C99A45"), (1, "#8C6424")]
BRASS_S = [(0, "#B78B3C"), (1, "#6E4C1C")]

T_TOP = 16        # top thickness
APRON = 22        # side/back apron height under the top
LEG_A, LEG_B = 10, 5.5   # leg half-width at top / at floor
INSET = 15        # leg centre inset from the top's edge
SABOT = 26        # brass shoe height

def leg(nm, cx, cz, ytop):
    def hw(y): return LEG_B + (LEG_A - LEG_B) * y / ytop
    a, b = LEG_A, LEG_B
    front = [(cx - a, ytop, cz + a), (cx + a, ytop, cz + a), (cx + b, 0, cz + b), (cx - b, 0, cz + b)]
    side = [(cx + a, ytop, cz + a), (cx + a, ytop, cz - a), (cx + b, 0, cz - b), (cx + b, 0, cz + b)]
    poly(f"{nm} front", front, None, g=((cx - a, 0, cz), (cx + a, 0, cz), LEG_F))
    poly(f"{nm} side", side, None, g=((cx, ytop, cz), (cx, 0, cz), LEG_S))
    # a lit arris down the leading corner
    line(f"{nm} arris", [(cx + a - 1, ytop - 4, cz + a), (cx + b - 1, SABOT + 2, cz + b)], "#C99068", 2.2, 55)
    c = hw(SABOT)
    poly(f"{nm} sabot front", [(cx - c, SABOT, cz + c), (cx + c, SABOT, cz + c), (cx + b, 0, cz + b), (cx - b, 0, cz + b)],
         None, sw=2, g=((cx - c, 0, cz), (cx + c, 0, cz), BRASS_F))
    poly(f"{nm} sabot side", [(cx + c, SABOT, cz + c), (cx + c, SABOT, cz - c), (cx + b, 0, cz - b), (cx + b, 0, cz + b)],
         None, sw=2, g=((cx, SABOT, cz), (cx, 0, cz), BRASS_S))
    line(f"{nm} sabot glint", [(cx - c + 3, SABOT - 5, cz + c), (cx - b + 2, 5, cz + b)], "#FFF4CC", 2.4, 75)

def table(nm, x0, z0, W, D, H, inner=None):
    x1, z1 = x0 + W, z0 + D
    yb = H - T_TOP                      # underside of top
    lx, rx = x0 + INSET, x1 - INSET
    bz, fz = z0 + INSET, z1 - INSET
    # far side first
    leg(f"{nm} leg back-left", lx, bz, yb)
    leg(f"{nm} leg back-right", rx, bz, yb)
    poly(f"{nm} back apron", [(lx + LEG_A, yb, bz), (rx - LEG_A, yb, bz), (rx - LEG_A, yb - APRON, bz), (lx + LEG_A, yb - APRON, bz)],
         None, sw=2, g=((0, yb, bz), (0, yb - APRON, bz), [(0, "#3A2214"), (1, "#24150C")]))
    poly(f"{nm} left apron inner face", [(lx + LEG_A - 6, yb, bz + LEG_A), (lx + LEG_A - 6, yb, fz - LEG_A),
                                         (lx + LEG_A - 6, yb - APRON, fz - LEG_A), (lx + LEG_A - 6, yb - APRON, bz + LEG_A)],
         None, sw=2, g=((lx, yb, bz), (lx, yb, fz), [(0, "#3A2214"), (1, "#5A3520")]))
    leg(f"{nm} leg front-left", lx, fz, yb)
    if inner:
        inner()
        # this top throws a soft shadow across the step below it
        _, _, iz0, iw, idd, ih, ix0 = inner.dims
        poly(f"{nm} shadow on next top", [(ix0, ih, z1), (ix0 + iw, ih, z1), (ix0 + iw, ih, z1 + 34), (ix0, ih, z1 + 34)],
             None, stroke=NONE, g=((0, ih, z1), (0, ih, z1 + 34), [(0, "#1A0D06", 0.55), (1, "#1A0D06", 0)]))
    # the top: upper face, front edge, right edge
    poly(f"{nm} top", [(x0, H, z0), (x1, H, z0), (x1, H, z1), (x0, H, z1)], None, sw=3,
         g=((x0, H, z0), (x1, H, z1), TOP_ST))
    # grain: long soft waves running the width
    for i in range(9):
        zz = z0 + D * (i + 0.6) / 9.4
        amp, ph = 2.2 + (i % 3), i * 1.7
        pts = [(x0 + 6 + W * t / 24 * (W - 12) / W, H, zz + amp * math.sin(t * 0.55 + ph)) for t in range(25)]
        line(f"{nm} grain {i+1}", pts, "#3E2213" if i % 2 else "#C68B5E", 2, 26 if i % 2 else 20)
    # one figured knot-swirl per top
    kx, kz = x0 + W * 0.62, z0 + D * 0.42
    ring = [(kx + 34 * math.cos(a / 18 * math.tau), H, kz + 9 * math.sin(a / 18 * math.tau)) for a in range(19)]
    line(f"{nm} grain figure", ring, "#3E2213", 2, 22)
    # sheen from the window: a translucent diagonal band
    poly(f"{nm} top sheen", [(x0 + W * 0.12, H, z0), (x0 + W * 0.34, H, z0), (x0 + W * 0.20, H, z1), (x0 + W * 0.02, H, z1)],
         None, stroke=NONE, g=((x0, H, z0), (x0, H, z1), [(0, "#FFF1DC", 0.20), (1, "#FFF1DC", 0.04)]))
    poly(f"{nm} top front edge", [(x0, H, z1), (x1, H, z1), (x1, yb, z1), (x0, yb, z1)], None, sw=3,
         g=((x0, H, z1), (x0, yb, z1), FRONT_ST))
    poly(f"{nm} top right edge", [(x1, H, z1), (x1, H, z0), (x1, yb, z0), (x1, yb, z1)], None, sw=3,
         g=((x1, H, z1), (x1, H, z0), SIDE_ST))
    line(f"{nm} top edge highlight", [(x0 + 4, H, z1), (x1 - 2, H, z1), (x1, H, z0 + 4)], "#E3B387", 2.4, 70)
    # near side
    poly(f"{nm} right apron", [(rx + LEG_A, yb, fz - LEG_A), (rx + LEG_A, yb, bz + LEG_A),
                               (rx + LEG_A, yb - APRON, bz + LEG_A), (rx + LEG_A, yb - APRON, fz - LEG_A)],
         None, sw=2, g=((rx, yb, fz), (rx, yb, bz), SIDE_ST))
    leg(f"{nm} leg front-right", rx, fz, yb)

class Tbl:
    def __init__(self, nm, x0, z0, W, D, H, inner=None):
        self.a = (nm, x0, z0, W, D, H, inner)
        self.dims = (nm, None, z0, W, D, H, x0)
    def __call__(self):
        table(*self.a)

# Each smaller table fits inside the legs of the next and under its aprons,
# pulled forward so the tops read as a staircase.
small = Tbl("Small table", 56, 180, 288, 196, 248)
medium = Tbl("Medium table", 28, 90, 344, 218, 294, small)
large = Tbl("Large table", 0, 0, 400, 240, 340, medium)

# floor contact: a soft footprint under each table, drawn first
for nm, x0, z0, W, D in [("Large", 0, 0, 400, 240), ("Medium", 28, 90, 344, 218), ("Small", 56, 180, 288, 196)]:
    poly(f"{nm} floor shade", [(x0 - 10, 0, z0 - 6), (x0 + W + 14, 0, z0 - 6), (x0 + W + 18, 0, z0 + D + 12), (x0 - 8, 0, z0 + D + 12)],
         None, stroke=NONE, opacity=38, g=((x0, 0, z0), (x0 + W, 0, z0 + D), [(0, "#120804", 0.15), (1, "#120804", 0.55)]))
FLOOR_N = len(OPS)
large()

# --- fit to the disc ----------------------------------------------------------------
xs = [p[0] for op in OPS[FLOOR_N:] for p in op[2]]
ys = [p[1] for op in OPS[FLOOR_N:] for p in op[2]]
bw, bh = max(xs) - min(xs), max(ys) - min(ys)
SC = min(560 / bw, 500 / bh)
OX = 500 - SC * (min(xs) + max(xs)) / 2
OY = 478 - SC * (min(ys) + max(ys)) / 2

def S(p):
    return (OX + SC * p[0], OY + SC * p[1])

def path_of(pts, closed):
    q = [S(p) for p in pts]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in q) + (" Z" if closed else "")

screen = [S(p) for op in OPS for p in op[2]]
for x, y in screen:
    assert math.hypot(x - PCX, y - PCY) <= PR - 30, (x, y)
FOOT_Y = max(y for _, y in screen)
print("fit: scale %.3f  bbox x %.0f..%.0f  y %.0f..%.0f" % (
    SC, min(s[0] for s in screen), max(s[0] for s in screen), min(s[1] for s in screen), FOOT_Y))

# --- backdrop + plate -----------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#22160F"), (1, "#0B0705")), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#5A4030"), (0.6, "#3C2A1F"), (1, "#22170F")), stroke=NONE)
# warm light falling from an upper-left window
d.path("M250,150 L400,82 L760,700 L520,800 Z", "Window light",
       fill=lin(250, 100, 640, 760, (0, "#FFE2B8", 0.16), (1, "#FFE2B8", 0)), stroke=NONE)
for i, (x, y, w, h) in enumerate([(170, 220, 200, 120), (630, 150, 190, 110)]):
    d.shape("ellipse", f"Plate patina {i+1}", x=x, y=y, width=w, height=h,
            fill=rad((0, "#7A5A44", 0.22), (1, "#7A5A44", 0)), stroke=NONE)
for i, (x, y, w) in enumerate([(210, 300, 7), (780, 260, 6), (160, 540, 8), (830, 520, 7), (420, 110, 6),
                               (600, 100, 7), (300, 170, 5), (720, 170, 6), (140, 420, 6), (860, 400, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#7A5A42", opacity=40, stroke=NONE)

# floor: a lighter band that closes on the disc's own arc
HZ = 590
hx = math.sqrt(PR ** 2 - (HZ - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZ} L{PCX + hx:.1f},{HZ} A420,420 0 0 1 {PCX - hx:.1f},{HZ} Z", "Floor",
       fill=lin(0, HZ, 0, 880, (0, "#6B4E3A", 0.55), (1, "#2A1C14", 0.85)), stroke=NONE)
for i, yy in enumerate([640, 700, 770, 840]):
    xx = math.sqrt(PR ** 2 - (yy - PCY) ** 2) - 6
    d.path(f"M{PCX - xx:.1f},{yy} L{PCX + xx:.1f},{yy}", f"Floorboard seam {i+1}",
           fill=NONE, stroke="#1E130C", strokeWidth=3, opacity=30)
# the shadow ellipse the set sits on
d.shape("ellipse", "Set shadow", x=230, y=FOOT_Y - 70, width=560, height=120,
        fill=rad((0, "#0E0704", 0.6), (1, "#0E0704", 0)), stroke=NONE)

# --- the tables -------------------------------------------------------------------------
for kind, label, pts, fill, stroke, sw, op, g in OPS:
    kw = {}
    if g is not None:
        (s0, s1, stops) = g
        a, b = S(s0), S(s1)
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) < 1:
            b = (a[0], a[1] + 1)
        fill = lin(a[0], a[1], b[0], b[1], *stops) if kind == "poly" else fill
    if op is not None:
        kw["opacity"] = op
    if kind == "poly":
        d.path(path_of(pts, True), label, fill=fill, stroke=stroke,
               **({"strokeWidth": sw, "join": "round"} if stroke != NONE else {}), **kw)
    else:
        d.path(path_of(pts, False), label, fill=NONE, stroke=stroke, strokeWidth=sw, cap="round", join="round", **kw)

# rim drawn last so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#140C07", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8C9A2", strokeWidth=3, opacity=26)

# --- name + second line -----------------------------------------------------------------
d.text("NESTING TABLES", "Name", x=500, y=940, size=58, font="Virelai Sans", color="#F1DEC4", justify="center")
LINE2, SZ2, TRK = "WALNUT · BRASS", 22, 300
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans", color="#C9A27C", justify="center")
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

d.finish("nesting-tables-V1R00")
