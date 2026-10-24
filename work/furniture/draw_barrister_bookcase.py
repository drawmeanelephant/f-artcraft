#!/usr/bin/env python3
"""Barrister bookcase — field plate V1R00. A Globe-Wernicke stack in oak:
four glazed sections, each with its up-and-over door, law-book spines in
leather rows behind the glass, brass bands between the stacks, two books
resting flat on the cornice. Seen from front-right, above. Oak plate,
chambers mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Barrister Bookcase — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#221408"

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

# oak + leather + glass palette
FRONT_ST = [(0, "#B08048"), (1, "#7A5228")]
SIDE_ST  = [(0, "#7A5228"), (1, "#462812")]
TOP_ST   = [(0, "#C08E52"), (0.6, "#9A6834"), (1, "#6E4220")]
DARK_ST  = [(0, "#241608"), (1, "#100802")]
BRASS    = [(0, "#F6DE96"), (0.5, "#CFA04A"), (1, "#8A6224")]
GLASS_ST = [(0, "#D8E4DC", 0.10), (0.5, "#C8D8D0", 0.16), (1, "#A8BCB2", 0.10)]
LEATHERS = ["#6E2A20", "#8A5A2A", "#3E4A34", "#54402C", "#2E3440",
            "#7A3A26", "#5C4A28", "#46342A"]

W, D = 290, 140
FOOT, PLINTH = 22, 20            # bracket feet + plinth
B0 = FOOT + PLINTH               # stack base = 42
SEC = 104                        # section height
NSEC = 4
H = B0 + NSEC * SEC              # 458
CORN = 18                        # cornice overhang band
CO = 12

def mix(c0, c1, t):
    a = [int(c0[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(p + (q - p) * t):02X}" for p, q in zip(a, b))

# --- feet + plinth --------------------------------------------------------------------------------
for nm, fx in [("L", 18), ("R", W - 46)]:
    poly(f"Bracket foot {nm}", front(fx, fx + 28, 0, FOOT, D + 2), sw=2,
         g=((fx, FOOT, D), (fx, 0, D), [(0, "#7A5228"), (1, "#3A200C")]))
poly("Rear foot hint", side(W, D - 50, D - 24, 0, FOOT), stroke=NONE, fill="#2E1A0A")
poly("Plinth front", front(4, W - 4, FOOT, B0, D + 2), sw=2.2,
     g=((4, B0, D), (W - 4, FOOT, D), FRONT_ST))
poly("Plinth right", side(W - 4, 0, D + 2, FOOT, B0), sw=2,
     g=((W - 4, B0, D), (W - 4, FOOT, 0), SIDE_ST))
line("Plinth bead", [(6, B0 - 2, D + 3), (W - 6, B0 - 2, D + 3)], "#E0B880", 2, 60)

# --- right side of the whole stack ------------------------------------------------------------------
poly("Case right side", side(W, 0, D, B0, H), sw=2.5,
     g=((W, H, D), (W, B0, 0), SIDE_ST))
# side reveals between sections
for i in range(1, NSEC):
    line(f"Side seam {i}", [(W, B0 + i * SEC, 8), (W, B0 + i * SEC, D - 8)], "#2E1A0A", 3, 70)

# --- the four glazed sections, bottom to top ----------------------------------------------------------
shelf_seed = [3, 7, 11, 17]
for si in range(NSEC):
    y0, y1 = B0 + si * SEC, B0 + (si + 1) * SEC
    seed = shelf_seed[si]
    # interior darkness + back wall
    poly(f"S{si} interior", front(10, W - 10, y0 + 12, y1 - 16, D - 24), stroke=NONE,
         g=((10, y1, D - 24), (W - 10, y0, D - 24), DARK_ST))
    # the shelf the books stand on
    poly(f"S{si} shelf", top(10, W - 10, D - 26, D - 4, y0 + 14), stroke=NONE, fill="#1A0E04")

    # --- the row of law books -------------------------------------------------------------------
    x = 16
    bi = 0
    while x < W - 30:
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        bw = 9 + (seed % 9)                    # spine width 9..17
        bh = 52 + ((seed >> 8) % 22)           # height 52..73
        col = LEATHERS[(seed >> 4) % len(LEATHERS)]
        lean = (seed >> 12) % 7 == 0           # occasional leaner
        if x + bw > W - 26:
            break
        zb = D - 20
        if lean:
            pts = [(x, y0 + 16, zb), (x + bw + 8, y0 + 16, zb),
                   (x + bw + 12, y0 + 16 + bh * 0.8, zb), (x + 4, y0 + 16 + bh * 0.8, zb)]
        else:
            pts = front(x, x + bw, y0 + 16, y0 + 16 + bh, zb)
        poly(f"S{si} book {bi}", pts, stroke=NONE,
             g=((x, y0 + 16 + bh, zb), (x + bw, y0 + 16, zb),
                [(0, mix(col, "#C8B088", 0.28)), (1, mix(col, "#140A04", 0.25))]))
        # a gilt band or two on the spine
        line(f"S{si} book {bi} band", [(x + 1, y0 + 16 + bh * 0.78, zb + 0.5),
                                       (x + bw - 1, y0 + 16 + bh * 0.78, zb + 0.5)], "#C8A258", 1.6, 75)
        x += bw + 3 if not lean else bw + 12
        bi += 1

    # --- glazed door: wood frame + pane + pull ---------------------------------------------------
    FZ = D + 4
    for nm, (x0, x1, yy0, yy1) in [("left", (0, 12, y0, y1)), ("right", (W - 12, W, y0, y1)),
                                   ("top", (0, W, y1 - 14, y1)), ("bottom", (0, W, y0, y0 + 10))]:
        poly(f"S{si} door {nm}", front(x0, x1, yy0, yy1, FZ), sw=1.8,
             g=((x0, yy1, FZ), (x1, yy0, FZ), FRONT_ST))
    poly(f"S{si} glass", front(12, W - 12, y0 + 10, y1 - 14, FZ - 1), stroke="#C8D8D0", sw=1.6,
         g=((12, y1, FZ), (W - 12, y0, FZ), GLASS_ST))
    # reflection streak across the pane
    poly(f"S{si} glass streak", [(W * 0.30, y0 + 10, FZ + 0.5), (W * 0.44, y0 + 10, FZ + 0.5),
                                 (W * 0.60, y1 - 14, FZ + 0.5), (W * 0.46, y1 - 14, FZ + 0.5)],
         stroke=NONE, fill="#E8F0EA", opacity=12)
    # recessed pull at the bottom rail centre
    px = W / 2
    poly(f"S{si} pull", front(px - 14, px + 14, y0 + 2, y0 + 9, FZ + 2), sw=1.4,
         g=((px - 14, y0 + 9, FZ), (px + 14, y0 + 2, FZ), BRASS))

    # brass band between sections
    if si < NSEC - 1:
        poly(f"Band {si}", front(0, W, y1 - 1, y1 + 3, D + 2), sw=1.4,
             g=((0, y1 + 3, D), (W, y1 - 1, D), BRASS))

# --- cornice + the two resting books ----------------------------------------------------------------
CX0, CX1, CZ0, CZ1 = -CO, W + CO, -CO, D + CO
poly("Cornice front", front(CX0, CX1, H, H + CORN, CZ1), sw=2.4,
     g=((CX0, H + CORN, CZ1), (CX1, H, CZ1), FRONT_ST))
poly("Cornice side", side(CX1, CZ0, CZ1, H, H + CORN), sw=2.4,
     g=((CX1, H + CORN, CZ1), (CX1, H, CZ0), SIDE_ST))
poly("Cornice top", top(CX0, CX1, CZ0, CZ1, H + CORN), sw=2.4,
     g=((CX0, H + CORN, CZ0), (CX1, H + CORN, CZ1), TOP_ST))
line("Cornice light", [(CX0 + 4, H + CORN + 1, CZ1 - 3), (CX1 - 4, H + CORN + 1, CZ1 - 3),
                       (CX1 - 4, H + CORN + 1, CZ0 + 4)], "#E8C890", 2.6, 60)

# two books flat on the cornice, left of centre
def flat_book(nm, x0, x1, z0, z1, y, col):
    poly(f"{nm} cover", top(x0, x1, z0, z1, y), sw=2, stroke="#2A1408",
         g=((x0, y, z0), (x1, y, z1), [(0, mix(col, "#D8C098", 0.3)), (1, col)]))
    poly(f"{nm} pages", side(x1 - 3, z0 + 4, z1 - 4, y - 6, y - 1), stroke=NONE, fill="#E4D8BC")
    line(f"{nm} spine", [(x0 + 3, y - 3, z1 - 4), (x0 + 3, y - 3, z0 + 4)], "#2A1408", 3, 80)

flat_book("Resting book 1", 40, 128, 40, 108, H + CORN + 4, "#54402C")
flat_book("Resting book 2", 52, 122, 52, 100, H + CORN + 12, "#6E2A20")

# --- fit to the disc --------------------------------------------------------------------------------
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

# --- backdrop + plate ------------------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#14100A"), (1, "#060402")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8A7A58", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#6B4A2C"), (0.6, "#402815"), (1, "#170C05")),
        stroke="#100804", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D8B8", strokeWidth=3, opacity=26)
d.shape("ellipse", "Chambers glow", x=240, y=110, width=520, height=460,
        fill=rad((0, "#FFDCA0", 0.14), (0.6, "#FFDCA0", 0.05), (1, "#FFDCA0", 0)), stroke=NONE)
for i, (x, y, w) in enumerate([(208, 215, 6), (782, 245, 7), (168, 615, 6), (830, 590, 7),
                               (428, 102, 6), (648, 108, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#C8AA78", opacity=30, stroke=NONE)

HZN = 700
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z", "Floor",
       fill=lin(0, HZN, 0, 880, (0, "#2E2012", 0.55), (1, "#120A05", 0.9)), stroke=NONE)
d.shape("ellipse", "Bookcase shadow", x=270, y=FOOT_Y - 40, width=480, height=94,
        fill=rad((0, "#060302", 0.65), (1, "#060302", 0)), stroke=NONE)

# --- the bookcase --------------------------------------------------------------------------------------
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

d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE, stroke="#0E0804", strokeWidth=6)

# --- captions ------------------------------------------------------------------------------------------
d.text("BARRISTER BOOKCASE", "Name", x=500, y=940, size=54, font="Virelai Sans",
       color="#F0E4CC", justify="center")
LINE2, SZ2, TRK = "OAK · GLASS · BRASS", 22, 300
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#C8B494", justify="center")
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

d.finish("barrister-bookcase-V1R00")
