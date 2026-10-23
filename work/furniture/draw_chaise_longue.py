#!/usr/bin/env python3
"""Chaise longue — field plate V1R00. Near-side profile of a scrolled-end
chaise: raised scroll at the left, the seat dipping long to a small foot
roll at the right, button-tufted dusty-rose velvet, four short turned
walnut legs on brass casters. Charcoal plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Chaise Longue — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#33141E"   # warm dark, not black
EXTENT = []


def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def stops(*pairs):
    out = []
    for p in pairs:
        s = {"offset": p[0], "color": p[1]}
        if len(p) > 2:
            s["opacity"] = p[2]
        out.append(s)
    return out


def lin(a, b, *pairs):
    return {"gradient": {"kind": "linear", "start": [round(a[0], 1), round(a[1], 1)],
                         "end": [round(b[0], 1), round(b[1], 1)], "stops": stops(*pairs)}}


def rad(*pairs):
    return {"gradient": {"kind": "radial", "stops": stops(*pairs)}}


def smooth(pts, closed=False, move=True):
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = ("M%.1f,%.1f" if move else "L%.1f,%.1f") % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


def cr_eval(pts, u):
    """Catmull-Rom value at u in [0,1] through control points."""
    n = len(pts) - 1
    f = max(0.0, min(1.0, u)) * n
    i = min(int(f), n - 1)
    t = f - i
    p0 = pts[max(0, i - 1)]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[min(n, i + 2)]
    def axis(k):
        return 0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t +
                      (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t * t +
                      (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t * t * t)
    return (axis(0), axis(1))


# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#181A20"), (1, "#0A0B0F")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#5A6070", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#4C505C"), (0.6, "#363A44"), (1, "#20232B")),
        stroke="#0D1015", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D0DC", strokeWidth=3, opacity=24)
d.shape("ellipse", "Back glow", x=200, y=170, width=520, height=520,
        fill=rad((0, "#E8A0B0", 14), (0.6, "#A06070", 5), (1, "#704050", 0)), stroke=NONE)

FY = 706
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#565C68", 34), (1, "#12151B", 70)), stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#D2D8E2", strokeWidth=2, opacity=18)

# --- upholstery curves ----------------------------------------------------------
TOP = [(312, 438), (380, 466), (480, 494), (575, 497), (660, 478), (704, 452), (730, 428)]
BOT = [(300, 538), (440, 578), (600, 574), (700, 548), (734, 516)]


def top(u):
    return cr_eval(TOP, u)


def bot(u):
    return cr_eval(BOT, u)


def surf(u, v):
    t, b = top(u), bot(u)
    return (t[0] + (b[0] - t[0]) * v, t[1] + (b[1] - t[1]) * v)


# far-side edge: the cushion's back lip peeking over the near top edge (3/4 hint)
FAR = [(x + 26, y - 20) for x, y in TOP]
far_pts = [top(u) for u in [i / 24 for i in range(25)]]
far_edge = [cr_eval(FAR, u) for u in [i / 24 for i in range(25)]]
lip = far_pts + far_edge[::-1]
d.path(smooth(lip, closed=True), "Seat far edge",
       fill=lin((0, 400), (0, 470), (0, "#D89AA6"), (1, "#8E4254")),
       stroke="#5C2836", strokeWidth=2.5, join="round")

# --- shadow ----------------------------------------------------------------------
d.shape("ellipse", "Chaise shadow", x=212, y=664, width=580, height=54,
        fill=rad((0, "#04060A", 62), (0.6, "#04060A", 28), (1, "#04060A", 0)), stroke=NONE)

# --- legs --------------------------------------------------------------------------
WOOD = ((0, "#8A5C3E"), (0.3, "#B98556"), (0.5, "#5C3A24"), (0.78, "#7A4E30"), (1, "#3C2414"))


def leg(cx, y_top, y_foot, scale, name, dark=False):
    """Turned leg: bulged collar, tapered shaft, foot bulb, brass caster."""
    # right-side profile (dy, half-width)
    prof = [(0, 9), (14, 9), (18, 12), (26, 12), (30, 8), (58, 5.5),
            (74, 5), (82, 11), (92, 11), (96, 6)]
    L = y_foot - y_top - 14     # leave room for caster
    s = L / 96.0 * scale
    right = [(cx + w * scale, y_top + dy * s) for dy, w in prof]
    left = [(cx - w * scale, y_top + dy * s) for dy, w in reversed(prof)]
    grad = lin((cx - 12 * scale, 0), (cx + 12 * scale, 0), *WOOD)
    d.path(smooth(right + left, closed=True), f"Leg {name}", fill=grad,
           stroke="#2A1A10", strokeWidth=2.5, join="round",
           opacity=70 if dark else 100)
    # collar ring highlight
    ring_y = y_top + 24 * s
    d.path(f"M{cx - 11 * scale:.1f},{ring_y:.1f} L{cx + 11 * scale:.1f},{ring_y:.1f}",
           f"Leg {name} ring", fill=NONE, stroke="#2A1A10", strokeWidth=2, opacity=45)
    # brass caster: cup + wheel
    cy = y_foot - 6
    d.shape("ellipse", f"Caster cup {name}", x=round(cx - 8), y=round(cy - 12), width=16, height=12,
            fill=rad((0, "#F0D088"), (0.6, "#A87828"), (1, "#5C3C10")),
            stroke="#2A1A10", strokeWidth=1.6, opacity=70 if dark else 100)
    d.shape("ellipse", f"Caster wheel {name}", x=round(cx - 9), y=round(cy - 2), width=18, height=9,
            fill=rad((0, "#3A2C20"), (1, "#14100C")), stroke="#2A1A10", strokeWidth=1.6,
            opacity=70 if dark else 100)
    EXTENT.append((cx, y_foot))
    EXTENT.append((cx - 12 * scale, (y_top + y_foot) / 2))
    EXTENT.append((cx + 12 * scale, (y_top + y_foot) / 2))


# far legs first (behind), then near legs
for u, nm in ((0.16, "far L"), (0.84, "far R")):
    b = bot(u)
    leg(b[0] + 30, b[1] - 26, 692, 0.9, nm, dark=True)
for u, nm in ((0.09, "L"), (0.91, "R")):
    b = bot(u)
    leg(b[0], b[1] - 8, 696, 1.0, nm)

# --- scroll (raised head end) ----------------------------------------------------
# outer roll face
d.shape("ellipse", "Scroll outer", x=196, y=282, width=190, height=184,
        fill=rad((0, "#E4AAB6"), (0.55, "#C07084"), (1, "#7E3346")),
        stroke=INK, strokeWidth=6)
# back lip of the roll (3/4 hint)
d.path("M330,296 C366,304 386,332 388,368 C386,336 366,310 336,300 Z",
       "Scroll depth", fill="#D89AA6", opacity=45, stroke=NONE)
# spiral curl of the scroll
spir = []
for k in range(46):
    t = k / 45 * 2.15 * math.pi
    r = 66 - 58 * (k / 45)
    spir.append((291 + r * math.cos(t + 0.5), 372 + r * math.sin(t + 0.5) * 0.94))
d.path(smooth(spir), "Scroll spiral", fill=NONE, stroke="#5C2836", strokeWidth=5,
       cap="round", opacity=80)
d.path(smooth([(x + 2, y - 3) for x, y in spir]), "Scroll spiral light",
       fill=NONE, stroke="#F0C4CC", strokeWidth=2.5, cap="round", opacity=50)

# --- seat body -------------------------------------------------------------------
seat = [top(i / 30) for i in range(31)] + [bot(i / 30) for i in range(30, -1, -1)]
d.path(smooth(seat, closed=True), "Seat body",
       fill=lin((0, 440), (0, 600), (0, "#D9929E"), (0.45, "#B2607A"), (1, "#6E2C40")),
       stroke=INK, strokeWidth=5, join="round")
EXTENT += seat

# cushion crown: lighter band hugging the top edge
crown = [top(i / 30) for i in range(31)] + [surf(i / 30, 0.22) for i in range(30, -1, -1)]
d.path(smooth(crown, closed=True), "Seat crown light",
       fill=lin((0, 430), (0, 510), (0, "#F0C2CA", 55), (1, "#C87E8E", 0)),
       stroke=NONE)
# rail shade under the seat
rail = [surf(i / 30, 0.72) for i in range(31)] + [bot(i / 30) for i in range(30, -1, -1)]
d.path(smooth(rail, closed=True), "Seat rail shade",
       fill=lin((0, 560), (0, 600), (0, "#541E2E", 0), (1, "#3A1220", 60)), stroke=NONE)

# piping cord along the top edge and the bottom edge
d.path(smooth([top(i / 30) for i in range(31)]), "Top piping",
       fill=NONE, stroke="#571F2E", strokeWidth=5, cap="round")
d.path(smooth([bot(i / 30) for i in range(31)]), "Rail piping",
       fill=NONE, stroke="#571F2E", strokeWidth=4, cap="round", opacity=80)

# --- foot roll (right end) ---------------------------------------------------------
d.shape("ellipse", "Foot roll", x=672, y=396, width=96, height=88,
        fill=rad((0, "#E0A4B0"), (0.6, "#BC6880"), (1, "#7E3346")),
        stroke=INK, strokeWidth=5)
d.path("M704,410 C738,414 754,438 748,466 C752,438 736,418 706,414 Z",
       "Foot roll depth", fill="#8E4254", opacity=55, stroke=NONE)
d.path("M686,420 C700,404 730,402 746,418", "Foot roll highlight",
       fill=NONE, stroke="#F0C4CC", strokeWidth=3, cap="round", opacity=45)

# --- button tufting ------------------------------------------------------------------
rows = [(0.20, [0.10 + i * 0.115 for i in range(8)]),
        (0.50, [0.155 + i * 0.115 for i in range(7)]),
        (0.80, [0.10 + i * 0.115 for i in range(8)])]
btns = []
for v, us in rows:
    for u in us:
        btns.append(surf(u, v))

# diamond seams between neighbouring rows
for (v0, us0), (v1, us1) in zip(rows, rows[1:]):
    for i, u in enumerate(us0[:-1]):
        for u2 in us1[max(0, i - 1):i + 2]:
            a, b = surf(u, v0), surf(u2, v1)
            d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", "Tuft seam",
                   fill=NONE, stroke="#5C2836", strokeWidth=2.2, opacity=30)

for i, (x, y) in enumerate(btns):
    # crease strokes radiating from each dimple
    for a in (-2.5, -0.6, 0.6, 2.5):
        L = 13
        dx, dy = math.cos(a) * L, math.sin(a) * L * 0.55
        d.path(f"M{x + dx * 0.5:.1f},{y + dy * 0.5:.1f} L{x + dx:.1f},{y + dy:.1f}",
               f"Crease {i}", fill=NONE, stroke="#5C2836", strokeWidth=2.4,
               cap="round", opacity=38)
    d.shape("ellipse", f"Button {i}", x=round(x - 5), y=round(y - 4), width=10, height=8,
            fill=rad((0, "#8E4254"), (0.7, "#571F2E"), (1, "#3A1220")),
            stroke="#3A1220", strokeWidth=1.4)
    d.shape("ellipse", f"Button glint {i}", x=round(x - 2), y=round(y - 3), width=3, height=2.4,
            fill="#F0C4CC", opacity=60, stroke=NONE)

# three buttons marching up the scroll
for i, (x, y) in enumerate([(238, 398), (252, 336), (298, 306)]):
    d.shape("ellipse", f"Scroll button {i}", x=x - 5, y=y - 4, width=10, height=8,
            fill=rad((0, "#8E4254"), (0.7, "#571F2E"), (1, "#3A1220")),
            stroke="#3A1220", strokeWidth=1.4)
    d.shape("ellipse", f"Scroll button glint {i}", x=x - 2, y=y - 3, width=3, height=2.4,
            fill="#F0C4CC", opacity=60, stroke=NONE)

# where scroll meets seat: a compression crease
d.path("M342,442 C352,470 352,500 342,528", "Scroll seat crease",
       fill=NONE, stroke="#4A1A28", strokeWidth=5, cap="round", opacity=45)

# --- extent check --------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chaise extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 28, far


# --- caption ---------------------------------------------------------------------------
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
    n = d.text(name, "Name", x=500, y=934, size=56, font="Virelai Sans",
               color="#F0DCDF", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#B29AA0", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=260)
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


caption("CHAISE LONGUE", "WALNUT · VELVET · BRASS")
d.finish("chaise-longue-V1R00")
