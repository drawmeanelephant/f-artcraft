#!/usr/bin/env python3
"""Bar stool — furniture field plate V1R00. Near-side view with a slight
three-quarter: a diner counter stool — a plump round vinyl seat on four
splayed chrome tube legs joined by a footrest ring, small swivel pan beneath.
Candy-red vinyl on a warm dark plate. 1000x1000. Modelled in 3D (inches) and
projected with a fixed yaw + pitch so every joint lines up.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Bar Stool — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A1A14"   # warm dark, not black
EXTENT = []       # every projected point, checked against the rim


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


# --- projection -------------------------------------------------------------
# x = stool's right, y = up, z = toward the back. Yaw turns the stool, pitch
# looks down onto the seat.
YAW, PITCH = math.radians(24), math.radians(15)
S, OX, OY = 18.0, 506.0, 768.0


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


# --- palette -------------------------------------------------------------------
CHROME = [(0, "#33383E"), (0.32, "#E9EEF2"), (0.55, "#98A1A8"), (1, "#20242A")]

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1B1214"), (1, "#080607")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#5E464A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#4A3A38"), (0.6, "#302624"), (1, "#181212")),
        stroke="#100B0A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8C8BC", strokeWidth=3, opacity=24)
# warm counter light from the upper left
d.shape("ellipse", "Back glow", x=150, y=100, width=560, height=560,
        fill=rad((0, "#F0C8A0", 24), (0.55, "#B8806A", 9), (1, "#7A4A3A", 0)), stroke=NONE)
# faint neon echo low on the right for the diner mood
d.shape("ellipse", "Neon echo", x=560, y=500, width=340, height=220,
        fill=rad((0, "#C85A5A", 14), (1, "#C85A5A", 0)), stroke=NONE)

# floor: a band that closes on the disc's own arc
FY = 702
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#503E3A", 30), (1, "#150F0E", 72)), stroke=NONE)
for i, y in enumerate([742, 788, 840]):
    hw = math.sqrt(PR ** 2 - (y - PCY) ** 2) - 10
    d.path(f"M{PCX - hw:.1f},{y} L{PCX + hw:.1f},{y}", f"Floor seam {i+1}",
           fill=NONE, stroke="#201614", strokeWidth=2, opacity=40)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E0C4B4", strokeWidth=2, opacity=20)

# --- geometry ---------------------------------------------------------------------
SEAT_BOT, SEAT_TOP = 26.4, 30.6
SEAT_R = 7.3
LEG_TOP_Y, LEG_TOP_R = 26.2, 5.4
FOOT_R = 7.6
RING_Y, RING_R = 10.4, 6.6

# legs at four azimuths; the two with a<180 face the viewer
LEG_AZ = [38, 142, 218, 322]


def at(r, az, y):
    return (r * math.cos(math.radians(az)), y, r * math.sin(math.radians(az)))


# floor shadow under the stool
d.shape("ellipse", "Stool shadow", x=330, y=730, width=400, height=96,
        fill=rad((0, "#050303", 66), (0.6, "#050303", 30), (1, "#050303", 0)), stroke=NONE)


def turned(name, a, b, profile, stops_list=None, ink=2.2):
    """A round member between 3D points a and b; profile = [(t, r in)]."""
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
            *(stops_list or CHROME))
    d.path(path, name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return A, B


# footrest ring: a chrome circle; far half first, near half over the legs later
ring = [at(RING_R, a, RING_Y) for a in range(0, 361, 6)]
ring2 = [P(*p) for p in ring]
d.path(smooth(ring2, closed=True), "Footrest ring", fill=NONE,
       stroke="#5A6167", strokeWidth=8, join="round")
d.path(smooth([(x, y - 2.4) for x, y in ring2], closed=True), "Footrest ring light",
       fill=NONE, stroke="#E8EEF2", strokeWidth=2.4, opacity=55)

# legs: far pair first
leg_pts = {}
for i, az in enumerate(sorted(LEG_AZ, key=lambda a: -depth(*at(FOOT_R, a, 0)))):
    a, b = at(FOOT_R, az, 0.4), at(LEG_TOP_R, az, LEG_TOP_Y)
    leg_pts[az] = (a, b)
    turned(f"Leg {i+1}", a, b, [(0.0, 0.34), (0.04, 0.42), (0.5, 0.46), (1.0, 0.52)])
    # rubber foot cap
    fx, fy = P(*at(FOOT_R, az, 0.15))
    d.shape("ellipse", f"Leg {i+1} foot", x=round(fx - 8), y=round(fy - 5), width=16,
            height=10, fill=rad((0, "#3A3532"), (1, "#141110")), stroke=INK, strokeWidth=1.5)
    d.shape("ellipse", f"Leg {i+1} foot shadow", x=round(fx - 14), y=round(fy + 2), width=28,
            height=8, fill=rad((0, "#000000", 50), (1, "#000000", 0)), stroke=NONE)

# swivel pan under the seat: a shallow steel drum
PAN_R, PAN_BOT = 5.6, 24.9
pan_top = [P(PAN_R * math.cos(t), SEAT_BOT - 0.1, PAN_R * math.sin(t))
           for t in [2 * math.pi * i / 48 for i in range(48)]]
pan_bot = [P(PAN_R * 0.94 * math.cos(t), PAN_BOT, PAN_R * 0.94 * math.sin(t))
           for t in [2 * math.pi * i / 48 for i in range(48)]]
d.path(smooth(hull(pan_top + pan_bot), closed=True), "Swivel pan",
       fill=lin((360, 240), (660, 300), (0, "#5A6167"), (0.45, "#B9C2C8"), (1, "#2A2E33")),
       stroke=INK, strokeWidth=2.5, join="round")
# leg-to-pan bolt caps at each leg top
for az in LEG_AZ:
    bx, by = P(*at(LEG_TOP_R, az, LEG_TOP_Y + 0.3))
    d.shape("ellipse", f"Pan bolt {az}", x=round(bx - 4), y=round(by - 3), width=8,
            height=6, fill=rad((0, "#D8DEE2"), (1, "#4A5058")), stroke=INK, strokeWidth=1.2)

# --- seat: vinyl cushion cylinder -------------------------------------------------
rim_top = [P(SEAT_R * math.cos(t), SEAT_TOP, SEAT_R * math.sin(t))
           for t in [2 * math.pi * i / 64 for i in range(64)]]
rim_bot = [P((SEAT_R + 0.25) * math.cos(t), SEAT_BOT, (SEAT_R + 0.25) * math.sin(t))
           for t in [2 * math.pi * i / 64 for i in range(64)]]
# side wall = silhouette of the two rims; deepest fill, then the crown
d.path(smooth(hull(rim_top + rim_bot), closed=True), "Seat side",
       fill=lin((0, 240), (0, 330), (0, "#B33A2E"), (0.55, "#7E241C"), (1, "#46100C")),
       stroke=INK, strokeWidth=3, join="round")
d.path(smooth(rim_top, closed=True), "Seat top",
       fill=rad((0, "#E86A54"), (0.55, "#C04A3A"), (1, "#7E241C")),
       stroke=INK, strokeWidth=2.5, join="round")
# welt piping around the top edge
d.path(smooth(rim_top, closed=True), "Seat welt", fill=NONE,
       stroke="#3E0E0A", strokeWidth=3, opacity=70)
# specular sheen on the vinyl
sheen = [P(-2.6 + 5.4 * math.cos(t), SEAT_TOP + 0.2, -2.4 + 3.4 * math.sin(t))
         for t in [2 * math.pi * i / 40 for i in range(40)]]
d.path(smooth(sheen, closed=True), "Vinyl sheen",
       fill=rad((0, "#FFE0D2", 55), (0.7, "#FFB4A0", 18), (1, "#FFB4A0", 0)), stroke=NONE)
# side-wall highlight strip just under the welt, front-left
hi = [P(SEAT_R * math.cos(t), SEAT_TOP - 0.7, SEAT_R * math.sin(t))
      for t in [math.radians(205 + 75 * i / 24) for i in range(25)]]
d.path(smooth(hi), "Seat side light", fill=NONE, stroke="#F08A72",
       strokeWidth=4, opacity=45, cap="round")

# --- extent check ----------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("stool extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 30, far


# --- caption ----------------------------------------------------------------------------
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
    n = d.text(name, "Name", x=500, y=940, size=56, font="Virelai Sans",
               color="#F2DCCE", justify="center")
    m = d.text(mats, "Materials", x=500, y=972, size=22, font="Virelai Sans",
               color="#C09A8E", justify="center")
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


caption("BAR STOOL", "STEEL · VINYL")
d.finish("bar-stool-V1R00")
