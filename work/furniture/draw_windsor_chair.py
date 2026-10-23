#!/usr/bin/env python3
"""Windsor chair — field plate V1R00. Three-quarter view of a hoop-back
Windsor side chair: a bent bow filled with a comb of thin spindles, a scooped
saddle seat, splayed vase-and-ring turned legs on an H-stretcher. Honey wood
on a dark plate. 1000x1000. The chair is modelled in 3D (inches) and projected
with a fixed yaw + pitch so every joint lines up.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Windsor Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#3A2212"   # warm umber, not black
EXTENT = []       # every projected point of the chair, checked against the rim


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
    """Catmull-Rom through pts as cubic Beziers."""
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


# --- projection -----------------------------------------------------------------
# x = chair's right, y = up, z = toward the back. Yaw swings the chair's right
# side toward the viewer; pitch looks down onto the seat.
YAW, PITCH = math.radians(38), math.radians(17)
S, OX, OY = 15.0, 492.0, 768.0


def P(x, y, z):
    c, s = math.cos(YAW), math.sin(YAW)
    xr, zr = x * c + z * s, -x * s + z * c
    p = (OX + S * xr, OY - S * (y * math.cos(PITCH) + zr * math.sin(PITCH)))
    EXTENT.append(p)
    return p


def depth(x, y, z):
    return -x * math.sin(YAW) + z * math.cos(YAW)


def hull(pts):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in pts))

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


WOOD = (("#6A3C18",), ("#F7D594",), ("#D99C50",), ("#7E4A1E",))


def turned(name, a, b, profile, ink=2.2, light=0.30):
    """A turned member between 3D points a and b; profile = [(t, radius in)]."""
    A, B = P(*a), P(*b)
    dx, dy = B[0] - A[0], B[1] - A[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    left, right = [], []
    for t, r in profile:
        cx, cy = A[0] + dx * t, A[1] + dy * t
        w = r * S
        left.append((cx + nx * w, cy + ny * w))
        right.append((cx - nx * w, cy - ny * w))
    path = smooth(left) + " " + smooth(right[::-1], move=False) + " Z"
    wmax = max(r for _, r in profile) * S
    mx, my = A[0] + dx * 0.5, A[1] + dy * 0.5
    # gradient runs across the member so it reads as a cylinder lit from the left
    if nx > 0:
        nx, ny = -nx, -ny
    g = lin((mx + nx * wmax, my + ny * wmax), (mx - nx * wmax, my - ny * wmax),
            (0, "#7A4A20"), (light, "#F8D898"), (0.62, "#D2954A"), (1, "#6A3A16"))
    d.path(path, name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return A, B, (nx, ny)


def rings(name, a, b, ts, r, opacity=45):
    """Incised turning lines across a member at fractions ts."""
    A, B = P(*a), P(*b)
    dx, dy = B[0] - A[0], B[1] - A[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    for i, t in enumerate(ts):
        cx, cy = A[0] + dx * t, A[1] + dy * t
        w = r[i] * S if isinstance(r, list) else r * S
        d.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (cx + nx * w, cy + ny * w, cx + dx / L * 2,
                                                   cy + dy / L * 2, cx - nx * w, cy - ny * w),
               f"{name} ring {i+1}", fill=NONE, stroke=INK, strokeWidth=1.6, opacity=opacity)


# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#16120F"), (1, "#060504")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#5A4630", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#3E3830"), (0.62, "#2A2621"), (1, "#181512")), stroke="#0C0A08", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C9A877", strokeWidth=3, opacity=30)
# warm lamp-glow behind the chair so honey wood separates from the dark plate
d.shape("ellipse", "Back glow", x=250, y=120, width=500, height=560,
        fill=rad((0, "#E8B66A", 30), (0.55, "#B9823E", 12), (1, "#8A5A28", 0)), stroke=NONE)

# floor: a band that closes on the disc's own arc
FY = 676
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#5A4630", 34), (1, "#1A1511", 70)), stroke=NONE)
for i, y in enumerate([712, 760, 818]):
    hw = math.sqrt(PR ** 2 - (y - PCY) ** 2) - 14
    d.path(f"M{PCX - hw:.1f},{y} L{PCX + hw:.1f},{y}", f"Floorboard seam {i+1}",
           fill=NONE, stroke="#0E0B08", strokeWidth=2, opacity=40)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#D8B27A", strokeWidth=2, opacity=22)

# --- the chair: dimensions in inches ----------------------------------------------
SEAT_Y, SEAT_T = 17.5, 1.8


def seat_pt(a, k=1.0, y=SEAT_Y):
    """Seat outline in plan: rounded back (sin a > 0), flatter front."""
    c, s = math.cos(a), math.sin(a)
    x = 9.4 * k * math.copysign(abs(c) ** 0.72, c)
    z = (8.4 if s > 0 else 7.6) * k * math.copysign(abs(s) ** (1.0 if s > 0 else 0.55), s)
    return (x, y, z)


SEAT_N = 72
top = [seat_pt(2 * math.pi * i / SEAT_N) for i in range(SEAT_N)]
bot = [seat_pt(2 * math.pi * i / SEAT_N, 0.94, SEAT_Y - SEAT_T) for i in range(SEAT_N)]

# shadow under the chair, kept well inside the disc
d.shape("ellipse", "Chair shadow", x=268, y=716, width=470, height=118,
        fill=rad((0, "#050403", 70), (0.6, "#050403", 34), (1, "#050403", 0)), stroke=NONE)
for t in range(0, 360, 10):
    ex = 268 + 235 + 235 * math.cos(math.radians(t))
    ey = 716 + 59 + 59 * math.sin(math.radians(t))
    assert on_disc(ex, ey, 12), (ex, ey)

# legs: seat underside -> floor, splayed out and back/forward
LEG = [(0.0, 0.46), (0.05, 0.56), (0.17, 0.80), (0.28, 0.66), (0.33, 0.47), (0.37, 0.70),
       (0.40, 0.47), (0.47, 0.58), (0.56, 0.78), (0.64, 0.64), (0.82, 0.55), (1.0, 0.40)]
legs = {
    "FL": ((-6.2, SEAT_Y - SEAT_T, -4.6), (-8.6, 0, -8.0)),
    "FR": ((6.2, SEAT_Y - SEAT_T, -4.6), (8.6, 0, -8.0)),
    "BL": ((-6.0, SEAT_Y - SEAT_T, 4.4), (-8.2, 0, 8.6)),
    "BR": ((6.0, SEAT_Y - SEAT_T, 4.4), (8.2, 0, 8.6)),
}
ST_T = 0.56   # stretcher height as a fraction down each leg


def along(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


sideL = (along(*legs["FL"], ST_T), along(*legs["BL"], ST_T))
sideR = (along(*legs["FR"], ST_T), along(*legs["BR"], ST_T))
midL, midR = along(*sideL, 0.5), along(*sideR, 0.5)
STR = [(0.0, 0.34), (0.12, 0.40), (0.22, 0.36), (0.5, 0.58), (0.78, 0.36), (0.88, 0.40), (1.0, 0.34)]

parts = []
for k, (a, b) in legs.items():
    parts.append((depth(*along(a, b, 0.5)), "leg", k, a, b))
parts.append((depth(*midL) + 0.01, "str", "Side stretcher L", *sideL))
parts.append((depth(*midR) + 0.01, "str", "Side stretcher R", *sideR))
parts.append((depth(*along(midL, midR, 0.5)), "str", "Cross stretcher", midL, midR))
for dep, kind, name, a, b in sorted(parts, key=lambda p: -p[0]):
    if kind == "leg":
        turned(f"Leg {name}", a, b, LEG)
        rings(f"Leg {name}", a, b, [0.33, 0.40], 0.47)
        # foot: a soft contact shadow
        fx, fy = P(*b)
        d.shape("ellipse", f"Leg {name} foot shadow", x=round(fx - 14), y=round(fy - 3), width=28,
                height=8, fill=rad((0, "#000000", 55), (1, "#000000", 0)), stroke=NONE)
    else:
        turned(name, a, b, STR, ink=2.0)
        rings(name, a, b, [0.22, 0.78], 0.36, opacity=40)

# --- seat ---------------------------------------------------------------------------------
top2 = [P(*p) for p in top]
bot2 = [P(*p) for p in bot]
edge = hull(top2 + bot2)
d.path(smooth(edge, closed=True), "Seat edge",
       fill=lin((300, 520), (690, 640), (0, "#8A5424"), (0.45, "#C78640"), (1, "#5E3414")),
       stroke=INK, strokeWidth=2.5, join="round")
d.path(smooth(top2, closed=True), "Seat top",
       fill=rad((0, "#F6CF88"), (0.65, "#E2A65A"), (1, "#B97A38")), stroke=INK, strokeWidth=2.5)
# saddle scoop: two shallow dishes either side of a pommel ridge
for side, nm in ((-1, "L"), (1, "R")):
    dish = [P(side * 3.7 + 3.5 * math.cos(t), SEAT_Y, -0.6 + 4.6 * math.sin(t))
            for t in [2 * math.pi * i / 40 for i in range(40)]]
    d.path(smooth(dish, closed=True), f"Seat dish {nm}",
           fill=rad((0, "#7A4418", 55), (0.7, "#9A5E28", 26), (1, "#A86A30", 0)), stroke=NONE)
pom = [P(0, SEAT_Y, -7.4), P(0.9, SEAT_Y, -4.6), P(0.5, SEAT_Y, -1.8), P(-0.5, SEAT_Y, -1.8),
       P(-0.9, SEAT_Y, -4.6)]
d.path(smooth(pom, closed=True), "Pommel highlight",
       fill=rad((0, "#FFF0C8", 60), (1, "#FFE2A0", 0)), stroke=NONE)
# grain following the seat outline
for i, k in enumerate([0.86, 0.70, 0.52]):
    g = [P(*seat_pt(2 * math.pi * j / 48 + 0.3 * i, k)) for j in range(48)]
    d.path(smooth(g, closed=True), f"Seat grain {i+1}", fill=NONE, stroke="#8A5424",
           strokeWidth=1.4, opacity=22)
# spindle channel incised around the back
chan = [P(*seat_pt(a, 0.84)) for a in [0.05 + (math.pi - 0.1) * j / 30 for j in range(31)]]
d.path(smooth(chan), "Spindle channel", fill=NONE, stroke="#6A3A16", strokeWidth=2, opacity=55)
front_lip = [P(*seat_pt(a, 0.96)) for a in [math.pi + 0.35 + (math.pi - 0.7) * j / 24 for j in range(25)]]
d.path(smooth(front_lip), "Seat front lip light", fill=NONE, stroke="#FFE7B4", strokeWidth=3,
       opacity=45, cap="round")

# --- hoop + spindles ------------------------------------------------------------------------
H, RAKE, A0 = 21.5, 0.30, 0.55


def bow_pt(a):
    """The hoop follows the spindle channel in plan, rises, and leans back."""
    u = (a - A0) / (math.pi - 2 * A0)
    v = H * max(0.0, math.sin(math.pi * u)) ** 0.42
    x, _, z = seat_pt(a, 0.84)
    flare = 1.0 + 0.10 * math.sin(math.pi * u) ** 2
    return (x * flare, SEAT_Y + v, z + v * RAKE)


N_SP = 9
xs = [-5.5 + 11.0 * i / (N_SP - 1) for i in range(N_SP)]


def a_for_x(x):
    lo, hi = A0 + 0.02, math.pi - A0 - 0.02
    for _ in range(50):
        mid = (lo + hi) / 2
        if seat_pt(mid, 0.84)[0] > x:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


spindles = []
for i, x in enumerate(xs):
    a = a_for_x(x)
    base = seat_pt(a, 0.84)
    tip = bow_pt(a)
    spindles.append((depth(*base), i, base, tip))
SP = [(0.0, 0.30), (0.10, 0.34), (0.32, 0.38), (0.60, 0.31), (1.0, 0.24)]
for dep, i, base, tip in sorted(spindles, key=lambda s: -s[0]):
    A, B, n = turned(f"Spindle {i+1}", base, tip, SP, ink=1.6, light=0.28)
    assert min(r for _, r in SP) * S * 2 >= 3, "spindles must stay >= 3pt"
    # tenon shadow where the spindle enters the seat
    d.shape("ellipse", f"Spindle {i+1} socket", x=round(A[0] - 7), y=round(A[1] - 3), width=14,
            height=6, fill="#4A2810", opacity=45, stroke=NONE)

bow = [bow_pt(A0 + (math.pi - 2 * A0) * j / 60) for j in range(61)]
bow2 = [P(*p) for p in bow]
# hoop as a ribbon: outer and inner edges offset in screen space
BW = 0.85 * S
outer, inner = [], []
for j, p in enumerate(bow2):
    q0 = bow2[max(0, j - 1)]
    q1 = bow2[min(len(bow2) - 1, j + 1)]
    tx, ty = q1[0] - q0[0], q1[1] - q0[1]
    L = math.hypot(tx, ty) or 1
    nx, ny = ty / L, -tx / L
    outer.append((p[0] + nx * BW / 2, p[1] + ny * BW / 2))
    inner.append((p[0] - nx * BW / 2, p[1] - ny * BW / 2))
top_y = min(p[1] for p in bow2)
d.path(smooth(outer) + " " + smooth(inner[::-1], move=False) + " Z", "Hoop",
       fill=lin((0, top_y - 10), (0, bow2[0][1]), (0, "#F6D08C"), (0.5, "#D2944A"), (1, "#8A5424")),
       stroke=INK, strokeWidth=2.2, join="round")
hl = [((o[0] * 2 + c[0]) / 3, (o[1] * 2 + c[1]) / 3) for o, c in zip(outer, bow2)]
d.path(smooth(hl[6:-6]), "Hoop highlight", fill=NONE, stroke="#FFF0C8", strokeWidth=2.5,
       opacity=55, cap="round")
sh = [((i_[0] * 2 + c[0]) / 3, (i_[1] * 2 + c[1]) / 3) for i_, c in zip(inner, bow2)]
d.path(smooth(sh[10:-10]), "Hoop inner shade", fill=NONE, stroke="#5A3212", strokeWidth=2.5,
       opacity=35, cap="round")
for end, nm in ((bow[0], "R"), (bow[-1], "L")):
    ex, ey = P(*end)
    d.shape("ellipse", f"Hoop {nm} socket", x=round(ex - 9), y=round(ey - 4), width=18, height=8,
            fill="#4A2810", opacity=50, stroke=NONE)

# --- extent check ----------------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 30, far


# --- caption ------------------------------------------------------------------------------------------
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
               color="#F2DDB4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#B89A70", justify="center")
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


caption("WINDSOR CHAIR", "ELM · ASH · BEECH")
d.finish("windsor-chair-V1R00")
