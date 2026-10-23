#!/usr/bin/env python3
"""Rocking chair — field plate V1R00. Near-side profile with a slight
three-quarter: a fan-back rocker on long curved runners, the seat's shallow
dish, turned arm posts, and the near arm's hand-end worn pale where palms
have rested on it for years. Cherry with hickory spindles on a deep blue
plate. 1000x1000. Modelled in 3D (inches) and projected with a fixed yaw +
pitch so every joint lines up.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Rocking Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2E160C"   # warm umber, not black
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


# --- projection ------------------------------------------------------------------
# x = chair's right, y = up, z = toward the back. Negative yaw turns the front
# toward screen-right and shows the chair's left flank; pitch looks down a little.
YAW, PITCH = math.radians(-58), math.radians(13)
S, OX, OY = 12.2, 548.0, 778.0


def P(x, y, z):
    c, s = math.cos(YAW), math.sin(YAW)
    xr, zr = x * c + z * s, -x * s + z * c
    p = (OX + S * xr, OY - S * (y * math.cos(PITCH) + zr * math.sin(PITCH)))
    EXTENT.append(p)
    return p


def depth(x, y, z):
    return -x * math.sin(YAW) + z * math.cos(YAW)


CHERRY = ("#6A2A12", "#F2B07C", "#BF6A36", "#5A220E")
HICKORY = ("#7A5430", "#F6DDB2", "#CFA46E", "#6A4422")


def turned(name, a, b, profile, pal=CHERRY, ink=2.0, light=0.30):
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
    if nx > 0:
        nx, ny = -nx, -ny
    g = lin((mx + nx * wmax, my + ny * wmax), (mx - nx * wmax, my - ny * wmax),
            (0, pal[0]), (light, pal[1]), (0.62, pal[2]), (1, pal[3]))
    d.path(path, name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return A, B


def rings(name, a, b, ts, r, opacity=45):
    A, B = P(*a), P(*b)
    dx, dy = B[0] - A[0], B[1] - A[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    for i, t in enumerate(ts):
        cx, cy = A[0] + dx * t, A[1] + dy * t
        w = r * S
        d.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (cx + nx * w, cy + ny * w, cx + dx / L * 2,
                                                   cy + dy / L * 2, cx - nx * w, cy - ny * w),
               f"{name} ring {i+1}", fill=NONE, stroke=INK, strokeWidth=1.5, opacity=opacity)


def along(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#0A1224"), (1, "#03060E")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#3A5E9A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#2A4C86"), (0.6, "#1A3462"), (1, "#0E1D3C")), stroke="#081226", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#A8C2EA", strokeWidth=3, opacity=28)
d.shape("ellipse", "Window light", x=230, y=110, width=520, height=560,
        fill=rad((0, "#9EC0F0", 22), (0.6, "#6A90CC", 8), (1, "#4A70AC", 0)), stroke=NONE)

FY = 668
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#2E4E84", 40), (1, "#081428", 75)), stroke=NONE)
for i, y in enumerate([706, 756, 816]):
    hw = math.sqrt(PR ** 2 - (y - PCY) ** 2) - 14
    d.path(f"M{PCX - hw:.1f},{y} L{PCX + hw:.1f},{y}", f"Floorboard seam {i+1}",
           fill=NONE, stroke="#050C1A", strokeWidth=2, opacity=40)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#B8D0F4", strokeWidth=2, opacity=20)

# --- dimensions (inches) ---------------------------------------------------------------
SEAT_Y, SEAT_T = 16.5, 1.7
RX, R_RAD, R_ZC, R_H, R_W = 9.4, 36.0, 2.0, 1.8, 1.1
RZ0, RZ1 = -15.0, 22.0


def runner_y(z):
    """Bottom of a runner: a circular arc touching the floor at z = R_ZC."""
    return R_RAD - math.sqrt(R_RAD ** 2 - (z - R_ZC) ** 2)


def seat_pt(a, k=1.0, y=SEAT_Y):
    c, s = math.cos(a), math.sin(a)
    x = 9.6 * k * math.copysign(abs(c) ** 0.75, c)
    z = (8.6 if s > 0 else 8.0) * k * math.copysign(abs(s) ** (1.0 if s > 0 else 0.6), s)
    return (x, y, z)


# shadow: computed from the runners' floor footprint
foot = [P(sx, 0, z) for sx in (-RX, RX) for z in (RZ0 + 6, R_ZC, RZ1 - 7)]
fx0, fx1 = min(p[0] for p in foot) - 30, max(p[0] for p in foot) + 30
fy0, fy1 = min(p[1] for p in foot) - 20, max(p[1] for p in foot) + 22
d.shape("ellipse", "Chair shadow", x=round(fx0), y=round(fy0), width=round(fx1 - fx0),
        height=round(fy1 - fy0),
        fill=rad((0, "#02050C", 70), (0.6, "#02050C", 32), (1, "#02050C", 0)), stroke=NONE)
for t in range(0, 360, 10):
    ex = (fx0 + fx1) / 2 + (fx1 - fx0) / 2 * math.cos(math.radians(t))
    ey = (fy0 + fy1) / 2 + (fy1 - fy0) / 2 * math.sin(math.radians(t))
    assert on_disc(ex, ey, 10), (ex, ey)


def runner(name, x, outward):
    """A curved rocker: side face as a ribbon, plus the thin top face."""
    zs = [RZ0 + (RZ1 - RZ0) * i / 48 for i in range(49)]
    # ends sweep up a little more than the arc, like a hand-shaped rocker
    def lift(z):
        u = (z - RZ0) / (RZ1 - RZ0)
        return 0.9 * max(0, 0.12 - u) / 0.12 + 1.2 * max(0, u - 0.86) / 0.14
    bot = [(x, runner_y(z) + lift(z), z) for z in zs]
    top = [(x, runner_y(z) + lift(z) + R_H * (0.75 + 0.25 * math.sin(math.pi * (z - RZ0) / (RZ1 - RZ0))), z)
           for z in zs]
    # thickness seen from above: the top edge is doubled inward by the runner's width
    top_in = [(x - outward * R_W, p[1], p[2]) for p in top]
    face = [P(*p) for p in top] + [P(*p) for p in bot[::-1]]
    ty = min(p[1] for p in face)
    by = max(p[1] for p in face)
    # closed Catmull-Rom rounds the two ends like a hand-shaped rocker tip
    d.path(smooth([P(*p) for p in top_in][2:-2] + [P(*p) for p in top[::-1]][2:-2], closed=True),
           f"{name} top", fill=lin((0, ty - 4), (0, by), (0, "#F2B07C"), (1, "#B8642E")),
           stroke=INK, strokeWidth=1.8, join="round")
    d.path(smooth(face, closed=True),
           f"{name}", fill=lin((0, ty), (0, by + 6), (0, "#C8743C"), (0.5, "#8E4420"), (1, "#4E1C0A")),
           stroke=INK, strokeWidth=2.2, join="round")
    hl = [P(x, p[1] - 0.35, p[2]) for p in top[4:-4]]
    d.path(smooth(hl), f"{name} edge light", fill=NONE, stroke="#FFD2A6", strokeWidth=2.2,
           opacity=45, cap="round")
    return top


def runner_top(z):
    u = (z - RZ0) / (RZ1 - RZ0)
    return runner_y(z) + R_H * (0.75 + 0.25 * math.sin(math.pi * u))


LEG = [(0.0, 0.50), (0.06, 0.58), (0.20, 0.78), (0.32, 0.60), (0.37, 0.46), (0.41, 0.66),
       (0.44, 0.46), (0.55, 0.62), (0.72, 0.70), (0.90, 0.56), (1.0, 0.52)]
STR = [(0.0, 0.32), (0.15, 0.40), (0.5, 0.55), (0.85, 0.40), (1.0, 0.32)]
legs = {}
for side, sx in (("L", -1), ("R", 1)):
    for end, (zs, zf) in (("F", (-6.0, -7.0)), ("B", (5.4, 6.4))):
        legs[end + side] = ((sx * 7.2, SEAT_Y - SEAT_T, zs), (sx * RX, runner_top(zf) - 0.2, zf))

# far side (chair's right, +x) first
runner("Far runner", RX, 1)
for k in ("BR", "FR"):
    turned(f"Leg {k}", *legs[k], LEG)
    rings(f"Leg {k}", *legs[k], [0.37, 0.44], 0.46)
sR = (along(*legs["FR"], 0.6), along(*legs["BR"], 0.6))
turned("Side stretcher R", *sR, STR)
fS = (along(*legs["FL"], 0.45), along(*legs["FR"], 0.45))
bS = (along(*legs["BL"], 0.45), along(*legs["BR"], 0.45))
turned("Back stretcher", *bS, STR)
turned("Front stretcher", *fS, STR)
rings("Front stretcher", *fS, [0.15, 0.85], 0.40, opacity=40)
for k in ("BL", "FL"):
    turned(f"Leg {k}", *legs[k], LEG)
    rings(f"Leg {k}", *legs[k], [0.37, 0.44], 0.46)
sL = (along(*legs["FL"], 0.6), along(*legs["BL"], 0.6))
turned("Side stretcher L", *sL, STR)
rings("Side stretcher L", *sL, [0.15, 0.85], 0.40, opacity=40)
runner("Near runner", -RX, -1)

# --- back + arm geometry ------------------------------------------------------------------
RAKE = 0.40
CREST_Y0, CREST_H = 41.5, 3.4


def crest_z(x):
    return 7.2 + (CREST_Y0 - SEAT_Y) * RAKE + 2.4 * (1 - (x / 11.5) ** 2)


def crest_bot(x):
    return CREST_Y0 + 0.6 * (x / 11.5) ** 2


def crest_top(x):
    u = abs(x) / 11.5
    e = min(1.0, max(0.0, (u - 0.70) / 0.30))
    return CREST_Y0 + CREST_H + 0.5 * (1 - u ** 2) + 0.9 * e * e * (3 - 2 * e)


POST_X0, POST_Z0 = 7.4, 5.6
post_base = {s: (s * POST_X0, SEAT_Y, POST_Z0) for s in (-1, 1)}
post_top = {s: (s * 11.0, crest_bot(11.0) + 0.6, crest_z(11.0)) for s in (-1, 1)}
ARM_Y = 25.0
arm_back = {}
for s in (-1, 1):
    t = (ARM_Y - SEAT_Y) / (post_top[s][1] - SEAT_Y)
    arm_back[s] = along(post_base[s], post_top[s], t)
arm_post_base = {s: (s * 8.0, SEAT_Y, -6.6) for s in (-1, 1)}
arm_post_top = {s: (s * 10.0, ARM_Y - 0.9, -8.2) for s in (-1, 1)}
POST = [(0.0, 0.55), (0.08, 0.62), (0.22, 0.48), (0.30, 0.70), (0.36, 0.48), (0.55, 0.56),
        (0.80, 0.48), (1.0, 0.40)]
APOST = [(0.0, 0.52), (0.10, 0.62), (0.30, 0.84), (0.48, 0.58), (0.54, 0.44), (0.60, 0.66),
         (0.66, 0.44), (0.85, 0.50), (1.0, 0.44)]
SP = [(0.0, 0.28), (0.12, 0.32), (0.35, 0.36), (0.65, 0.30), (1.0, 0.24)]


def arm(s, worn):
    """Arm board: a plank from the back post forward over the arm post,
    flaring into a rounded hand-end."""
    bx, _, bz = arm_back[s]
    n = 28
    cl = []
    for i in range(n + 1):
        t = i / n
        x = bx + (s * 10.4 - bx) * t + s * 0.8 * math.sin(math.pi * t)
        z = bz + (-10.0 - bz) * t
        w = 1.2 + 0.9 * t ** 1.6
        cl.append((x, z, w))
    outl, inl = [], []
    for i, (x, z, w) in enumerate(cl):
        x0, z0, _ = cl[max(0, i - 1)]
        x1, z1, _ = cl[min(n, i + 1)]
        tx, tz = x1 - x0, z1 - z0
        L = math.hypot(tx, tz)
        nx, nz = tz / L, -tx / L
        outl.append((x + nx * w, z + nz * w))
        inl.append((x - nx * w, z - nz * w))
    ex, ez, ew = cl[-1]
    cap = [(ex + s * 0 + ew * math.cos(a) * 1.0, ez + ew * math.sin(a) * -1.0 - 0.0)
           for a in [math.pi * j / 10 for j in range(1, 10)]]
    # order the cap so it runs from outl[-1] to inl[-1]
    if math.hypot(cap[0][0] - outl[-1][0], cap[0][1] - outl[-1][1]) > \
       math.hypot(cap[-1][0] - outl[-1][0], cap[-1][1] - outl[-1][1]):
        cap = cap[::-1]
    ring = outl + cap + inl[::-1]
    topp = [P(x, ARM_Y, z) for x, z in ring]
    botp = [P(x, ARM_Y - 1.0, z) for x, z in ring]
    nm = "Near arm" if s < 0 else "Far arm"
    d.path(smooth(hull(topp + botp), closed=True), f"{nm} edge",
           fill=lin(P(bx, ARM_Y, bz), P(ex, ARM_Y, ez), (0, "#6A2A12"), (1, "#A8582A")),
           stroke=INK, strokeWidth=2, join="round")
    hand = P(ex, ARM_Y, ez)
    back = P(bx, ARM_Y, bz)
    if worn:
        # finish rubbed off at the hand-end: cherry fades to pale raw wood
        g = lin(back, hand, (0, "#C06C38"), (0.55, "#D89060"), (0.82, "#EEC9A0"), (1, "#F6DEC0"))
    else:
        g = lin(back, hand, (0, "#A8582A"), (1, "#D08048"))
    d.path(smooth(topp, closed=True), nm, fill=g, stroke=INK, strokeWidth=2, join="round")
    mid = [P(x, ARM_Y, z) for x, z, _ in cl[3:-2]]
    d.path(smooth(mid), f"{nm} sheen", fill=NONE, stroke="#FFE0C0", strokeWidth=3,
           opacity=40 if worn else 25, cap="round")
    if worn:
        hx_, hy_ = hand
        d.shape("ellipse", "Near arm worn patch", x=round(hx_ - 26), y=round(hy_ - 9), width=48,
                height=18, fill=rad((0, "#FFF4E2", 55), (1, "#FFF4E2", 0)), stroke=NONE)


# --- seat ------------------------------------------------------------------------------------
SEAT_N = 72
top = [seat_pt(2 * math.pi * i / SEAT_N) for i in range(SEAT_N)]
bot = [seat_pt(2 * math.pi * i / SEAT_N, 0.95, SEAT_Y - SEAT_T) for i in range(SEAT_N)]
top2 = [P(*p) for p in top]
bot2 = [P(*p) for p in bot]
ex0 = min(p[0] for p in top2)
ex1 = max(p[0] for p in top2)
d.path(smooth(hull(top2 + bot2), closed=True), "Seat edge",
       fill=lin((ex0, 0), (ex1, 0), (0, "#5A220E"), (0.5, "#A8552A"), (1, "#7A3416")),
       stroke=INK, strokeWidth=2.4, join="round")
d.path(smooth(top2, closed=True), "Seat top",
       fill=rad((0, "#E89A62"), (0.65, "#C26C36"), (1, "#8E4420")), stroke=INK, strokeWidth=2.4)
dish = [P(1.6 * math.cos(t) * 4.3, SEAT_Y, -0.4 + 5.6 * math.sin(t)) for t in
        [2 * math.pi * i / 40 for i in range(40)]]
d.path(smooth(dish, closed=True), "Seat dish",
       fill=rad((0, "#5A220E", 50), (0.7, "#7A3416", 22), (1, "#7A3416", 0)), stroke=NONE)
for i, k in enumerate([0.84, 0.66]):
    g = [P(*seat_pt(2 * math.pi * j / 48 + 0.4 * i, k)) for j in range(48)]
    d.path(smooth(g, closed=True), f"Seat grain {i+1}", fill=NONE, stroke="#6A2A12",
           strokeWidth=1.3, opacity=24)
front_lip = [P(*seat_pt(a, 0.95)) for a in [math.pi + 0.4 + (math.pi - 0.8) * j / 24 for j in range(25)]]
d.path(smooth(front_lip), "Seat front lip light", fill=NONE, stroke="#FFD0A4", strokeWidth=3,
       opacity=40, cap="round")

# --- things rising from the seat, far to near --------------------------------------------------
turned("Far arm post", arm_post_base[1], arm_post_top[1], APOST)
turned("Far back post", post_base[1], post_top[1], POST)
arm(1, False)

N_SP = 9
spindles = []
for i in range(N_SP):
    f = i / (N_SP - 1)
    xb = -4.8 + 9.6 * f
    # base sits on the seat's back arc
    lo, hi = 0.05, math.pi - 0.05
    for _ in range(50):
        m = (lo + hi) / 2
        if seat_pt(m, 0.84)[0] > xb:
            lo = m
        else:
            hi = m
    base = seat_pt((lo + hi) / 2, 0.84)
    xt = -8.6 + 17.2 * f
    tip = (xt, crest_bot(xt) + 0.4, crest_z(xt))
    spindles.append((depth(*base), i, base, tip))
for dep, i, base, tip in sorted(spindles, key=lambda s: -s[0]):
    A, B = turned(f"Spindle {i+1}", base, tip, SP, pal=HICKORY, ink=1.5, light=0.28)
    assert min(r for _, r in SP) * S * 2 >= 3, "spindles must stay >= 3pt"
    d.shape("ellipse", f"Spindle {i+1} socket", x=round(A[0] - 6), y=round(A[1] - 3), width=12,
            height=6, fill="#3A140A", opacity=45, stroke=NONE)

# crest rail: top face sliver, then the front face
xs = [-11.5 + 23.0 * i / 40 for i in range(41)]
front_top = [P(x, crest_top(x), crest_z(x)) for x in xs]
back_top = [P(x * 0.96, crest_top(x) - 0.25, crest_z(x * 0.96) + 1.1) for x in xs]
front_bot = [P(x, crest_bot(x), crest_z(x)) for x in xs]
ty = min(p[1] for p in back_top)
by = max(p[1] for p in front_bot)
d.path(smooth(back_top) + " " + smooth(front_top[::-1], move=False) + " Z", "Crest rail top",
       fill=lin((0, ty), (0, ty + 30), (0, "#F2B07C"), (1, "#B8642E")), stroke=INK, strokeWidth=2)
# the far end grain shows because the rail's thickness turns toward screen-left
x0 = xs[0]
end = [front_top[0], back_top[0], P(x0 * 0.96, crest_bot(x0), crest_z(x0 * 0.96) + 1.1), front_bot[0]]
d.path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f L%.1f,%.1f Z" % (end[0] + end[1] + end[2] + end[3]),
       "Crest rail end", fill=lin(end[1], end[3], (0, "#A8582A"), (1, "#4E1C0A")), stroke=INK,
       strokeWidth=2, join="round")
d.path(smooth(front_top) + " " + smooth(front_bot[::-1], move=False) + " Z", "Crest rail",
       fill=lin((0, ty), (0, by), (0, "#E08E56"), (0.45, "#B05C2C"), (1, "#5E2410")),
       stroke=INK, strokeWidth=2.2, join="round")
d.path(smooth([P(x, crest_top(x) - 0.45, crest_z(x) - 0.02) for x in xs[3:-3]]), "Crest rail sheen",
       fill=NONE, stroke="#FFD6AE", strokeWidth=2.5, opacity=45, cap="round")
d.path(smooth([P(x, crest_bot(x) + 0.5, crest_z(x) - 0.02) for x in xs[4:-4]]), "Crest rail bead",
       fill=NONE, stroke="#3A140A", strokeWidth=1.6, opacity=40, cap="round")

turned("Near back post", post_base[-1], post_top[-1], POST)
rings("Near back post", post_base[-1], post_top[-1], [0.22, 0.36], 0.5)
turned("Near arm post", arm_post_base[-1], arm_post_top[-1], APOST)
rings("Near arm post", arm_post_base[-1], arm_post_top[-1], [0.54, 0.66], 0.46)
arm(-1, True)

# --- extent check -------------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("chair extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 30, far


# --- caption -----------------------------------------------------------------------------------
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
               color="#E2ECFA", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#9EB4D6", justify="center")
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


caption("ROCKING CHAIR", "CHERRY · HICKORY · BEESWAX")
d.finish("rocking-chair-V1R00")
