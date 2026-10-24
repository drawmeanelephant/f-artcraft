#!/usr/bin/env python3
"""Cradle — field plate V1R00. A rocking box for the smallest sleeper: two
crescent end panels carry the crib, a bonnet hood leans over the pillow, the
near side is a wall of slim spindles, and a small blanket is folded over the
top rail. A maple crescent-and-star inlay on the head panel is the lullaby.
Cherry plate, lullaby mood. 1000x1000. Modelled in 3D (inches), projected
with fixed yaw + pitch so every joint lines up.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Cradle — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#26120A"   # warm umber, not black
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
# x = cradle's left/right (rocker direction), y = up, z = head(-) to foot(+).
# Negative yaw turns the head end toward screen-right and shows the cradle's
# left flank; pitch looks down a little so the bedding reads.
YAW, PITCH = math.radians(-58), math.radians(13)
S, OX, OY = 13.0, 498.0, 762.0


def P(x, y, z):
    c, s = math.cos(YAW), math.sin(YAW)
    xr, zr = x * c + z * s, -x * s + z * c
    p = (OX + S * xr, OY - S * (y * math.cos(PITCH) + zr * math.sin(PITCH)))
    EXTENT.append(p)
    return p


def depth(x, y, z):
    return -x * math.sin(YAW) + z * math.cos(YAW)


CHERRY = ("#6A2A12", "#F2B07C", "#BF6A36", "#5A220E")
PINE = ("#8A6032", "#F6DCAE", "#D2A468", "#7A5228")


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


def along(a, b, t):
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#180C0A"), (1, "#060303")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8A5A46", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#582A26"), (0.6, "#341618"), (1, "#130708")),
        stroke="#0E0506", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4C6AE", strokeWidth=3, opacity=26)
d.shape("ellipse", "Nursery light", x=200, y=100, width=560, height=560,
        fill=rad((0, "#FFC896", 20), (0.6, "#D89A6C", 7), (1, "#A06848", 0)), stroke=NONE)

FY = 785
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#3A241C", 45), (1, "#120806", 78)), stroke=NONE)
for i, y in enumerate([812, 846]):
    hw = math.sqrt(PR ** 2 - (y - PCY) ** 2) - 14
    d.path(f"M{PCX - hw:.1f},{y} L{PCX + hw:.1f},{y}", f"Floorboard seam {i+1}",
           fill=NONE, stroke="#0A0404", strokeWidth=2, opacity=40)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#F0CEB0", strokeWidth=2, opacity=18)

# --- dimensions (inches) ---------------------------------------------------------------
# end panels: crescent rockers that also are the head/foot boards
R_ARC = 38.0          # rocker arc radius
TIP = 9.5             # rocker half-span along x
PZ = 13.5             # panel centre z (head -PZ, foot +PZ)
PT = 1.1              # panel thickness
BOX_Y0, BOX_Y1 = 11.5, 22.5       # crib walls
TOPR0, TOPR1 = 20.8, 22.3         # top rail band
BOTR0, BOTR1 = 11.5, 13.6         # bottom rail band
WX = 6.6                          # side wall face x
WZ = 12.4                         # side wall half-length


def arc_y(x):
    """Rocker bottom edge: circle sagging to y=0 at centre, tips hand-lifted."""
    lift = 1.15 * max(0.0, (abs(x) - 7.6) / 1.9) ** 2
    return R_ARC - math.sqrt(max(0.1, R_ARC ** 2 - x ** 2)) + lift


def crest_top(x, kind):
    if kind == "head":
        return 26.6 + 1.8 * (1 - (x / 8.2) ** 2)
    return 23.2 + 1.3 * (1 - (x / 8.2) ** 2)


def panel_pts(kind):
    """Rocker end-panel outline (x,y): crest left->right, right flank flaring
    out to the tip, bottom arc right->left, left flank back up."""
    top = [(x, crest_top(x, kind)) for x in [-8 + 16 * i / 24 for i in range(25)]]
    side = []
    for i in range(1, 8):
        t = i / 8
        y = crest_top(8, kind) - (crest_top(8, kind) - 2.6) * t
        side.append((8 + 1.5 * t ** 1.4, y))
    bot = [(x, arc_y(x)) for x in [9.5 - 19 * i / 36 for i in range(37)]]
    lside = []
    for i in range(1, 8):
        t = i / 8
        y = 2.6 + (crest_top(-8, kind) - 2.6) * t
        lside.append((-9.5 + 1.5 * t ** 0.7, y))
    return top + side + bot + lside


def end_panel(name, zc, kind, face_pal, edge_pal):
    """Rocker end panel: front face + left thickness edge + crest sheen +
    bottom-arc edge light."""
    face_z = zc - math.copysign(PT / 2, zc)     # face toward the viewer
    pts = [P(x, y, face_z) for x, y in panel_pts(kind)]
    # thickness edge on the -x flank (drawn first, face overlaps its seam)
    edge = [P(-9.5, arc_y(-9.5), face_z), P(-8.4, 12.0, face_z),
            P(-8.0, 21.0, face_z), P(-8.0, 21.0, zc + math.copysign(PT / 2, zc)),
            P(-8.4, 12.0, zc + math.copysign(PT / 2, zc)), P(-9.5, arc_y(-9.5),
            zc + math.copysign(PT / 2, zc))]
    d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in edge) + " Z",
           name + " edge", fill=lin(edge[0], edge[3], (0, edge_pal[0]), (1, edge_pal[1])),
           stroke=INK, strokeWidth=1.8, join="round")
    ty = min(p[1] for p in pts)
    by = max(p[1] for p in pts)
    lx = min(p[0] for p in pts)
    rx = max(p[0] for p in pts)
    d.path(smooth(pts, closed=True), name,
           fill=lin((lx, ty), (rx, by), *face_pal),
           stroke=INK, strokeWidth=2.4, join="round")
    # crest sheen along the shaped top
    sheen = [P(x, crest_top(x, kind) - 0.4, face_z - math.copysign(0.06, zc))
             for x in [-7 + 14 * i / 20 for i in range(21)]]
    d.path(smooth(sheen), name + " crest sheen", fill=NONE, stroke="#FFD6AE",
           strokeWidth=2.4, opacity=42, cap="round")
    # edge light following the rocker arc
    epts = [P(x, arc_y(x) + 0.55, face_z - math.copysign(0.06, zc))
            for x in [-8.6 + 17.2 * i / 28 for i in range(29)]]
    d.path(smooth(epts), name + " arc light", fill=NONE, stroke="#FFC896",
           strokeWidth=2.2, opacity=38, cap="round")
    # grain echoing the arc
    for k, off in enumerate((2.2, 4.2)):
        g = [P(x, arc_y(x) + off, face_z) for x in [-7.6 + 15.2 * i / 26 for i in range(27)]]
        d.path(smooth(g), f"{name} grain {k+1}", fill=NONE, stroke="#4A1E0C",
               strokeWidth=1.4, opacity=28, cap="round")


# --- ground shadow from the two rockers' footprint ------------------------------------
# rockers touch the floor only near x=0 — shadow hugs the two contact zones
foot = [P(x, 0, z) for x in (-6, 0, 6) for z in (-PZ, PZ)]
fx0, fx1 = min(p[0] for p in foot) - 34, max(p[0] for p in foot) + 34
fy0, fy1 = min(p[1] for p in foot) - 14, max(p[1] for p in foot) + 20
d.shape("ellipse", "Cradle shadow", x=round(fx0), y=round(fy0), width=round(fx1 - fx0),
        height=round(fy1 - fy0),
        fill=rad((0, "#050202", 68), (0.6, "#050202", 30), (1, "#050202", 0)), stroke=NONE)
# hard contact darks where each rocker kisses the floor
for i, z in enumerate((-PZ, PZ)):
    cx, cy = P(0, 0.4, z)
    d.shape("ellipse", f"Rocker contact {i+1}", x=round(cx - 74), y=round(cy - 12),
            width=148, height=26,
            fill=rad((0, "#030101", 80), (0.6, "#030101", 40), (1, "#030101", 0)),
            stroke=NONE)
for t in range(0, 360, 10):
    ex = (fx0 + fx1) / 2 + (fx1 - fx0) / 2 * math.cos(math.radians(t))
    ey = (fy0 + fy1) / 2 + (fy1 - fy0) / 2 * math.sin(math.radians(t))
    assert on_disc(ex, ey, 8), (ex, ey)

# --- far end panel (foot) ---------------------------------------------------------------
end_panel("Foot panel", PZ, "foot",
          [(0, "#A25430"), (0.45, "#7E3A20"), (1, "#3E180A")], ("#4A1E0C", "#2E1208"))

# finials on the foot panel's top corners
FIN = [(0.0, 0.42), (0.28, 0.40), (0.42, 0.52), (0.55, 0.30), (0.62, 0.72),
       (0.74, 0.62), (0.82, 0.34), (0.90, 0.22), (1.0, 0.04)]
for sgn in (-1, 1):
    turned(f"Foot finial {sgn:+d}", (sgn * 8.0, crest_top(8, "foot") - 0.5, PZ - PT / 2),
           (sgn * 8.0, crest_top(8, "foot") + 2.4, PZ - PT / 2), FIN, ink=1.8)

# --- far side wall ------------------------------------------------------------------------
def side_wall(xface, name, rail_st, spindle_pal):
    """Spindle side wall at |x|=xface: bottom rail, top rail, 8 spindles."""
    # rails as boards spanning z, thin in x
    for nm, y0, y1, st in ((f"{name} bottom rail", BOTR0, BOTR1, rail_st),
                           (f"{name} top rail", TOPR0, TOPR1, rail_st)):
        # face = z-y plane at xface; top sliver for the top rail
        f = [P(xface, y1, -WZ), P(xface, y1, WZ), P(xface, y0, WZ), P(xface, y0, -WZ)]
        ty = min(p[1] for p in f)
        by = max(p[1] for p in f)
        d.path("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in f) + " Z", nm,
               fill=lin((0, ty), (0, by), *st), stroke=INK, strokeWidth=2, join="round")
    tx = 1.0 if xface < 0 else -1.0
    topf = [P(xface, TOPR1, -WZ), P(xface, TOPR1, WZ), P(xface + tx * 0.9, TOPR1 + 0.35, WZ),
            P(xface + tx * 0.9, TOPR1 + 0.35, -WZ)]
    d.path("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in topf) + " Z", f"{name} top rail cap",
           fill=lin(topf[0], topf[2], (0, "#E0965E"), (1, "#9A4C26")), stroke=INK,
           strokeWidth=1.6, join="round")
    SP = [(0.0, 0.30), (0.10, 0.36), (0.30, 0.42), (0.44, 0.34), (0.50, 0.46),
          (0.58, 0.34), (0.78, 0.38), (1.0, 0.28)]
    for i, z in enumerate((-9.4, -6.7, -4.0, -1.3, 1.4, 4.1, 6.8, 9.5)):
        turned(f"{name} spindle {i+1}", (xface, BOTR1 - 0.3, z),
               (xface, TOPR0 + 0.3, z), SP, pal=spindle_pal, ink=1.6, light=0.30)
    # rail sheen on the top rail's face
    hl = [P(xface - math.copysign(0.06, xface), TOPR0 + 1.0, -WZ + 1 + (2 * WZ - 2) * i / 20)
          for i in range(21)]
    d.path(smooth(hl), f"{name} rail sheen", fill=NONE, stroke="#FFD0A4",
           strokeWidth=2.4, opacity=34, cap="round")


side_wall(WX, "Far wall", [(0, "#8E4426"), (1, "#4E1E0E")], CHERRY)

# --- interior: mattress + quilt + pillow (seen through spindles, over the rail) -----------
QX = 5.8
quilt = [P(-QX, 16.2, -12.0), P(QX, 16.2, -12.0), P(QX, 16.2, 12.0), P(-QX, 16.2, 12.0)]
d.path("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in quilt) + " Z", "Quilt",
       fill=rad((0, "#EAD9BC"), (0.55, "#C4AC8C"), (1, "#8A7458")), stroke=NONE)
# quilt edge faces so the loft reads through the spindle gaps
for nm, qpts, st in (
        ("Quilt near edge", [(-QX, 16.2, -12), (-QX, 16.2, 12), (-QX, 13.8, 12), (-QX, 13.8, -12)],
         [(0, "#B09478"), (1, "#6E5840")]),
        ("Quilt foot edge", [(-QX, 16.2, 12), (QX, 16.2, 12), (QX, 13.8, 12), (-QX, 13.8, 12)],
         [(0, "#A08468"), (1, "#5E4834")])):
    f = [P(x, y, z) for x, y, z in qpts]
    d.path("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in f) + " Z", nm,
           fill=lin(f[0], f[2], *st), stroke=NONE)
# quilt stitch channels
for i, zx in enumerate((-6, 0, 6)):
    st = [P(-QX + 0.4, 16.25, zx + i * 0.0), P(QX - 0.4, 16.25, zx)]
    d.path(f"M{st[0][0]:.1f},{st[0][1]:.1f} L{st[1][0]:.1f},{st[1][1]:.1f}",
           f"Quilt channel {i+1}", fill=NONE, stroke="#8A7054", strokeWidth=1.6, opacity=30)

# pillow under the hood: a soft blob at the head end
pil = []
cx_, cy_, cz_ = 0.0, 17.0, -8.6
for i in range(20):
    a = math.tau * i / 20
    pil.append(P(cx_ + 4.4 * math.cos(a) * 1.0, cy_ + 1.5 * math.sin(a) *
                 (0.8 + 0.2 * math.cos(a)), cz_ + 2.0 * math.sin(a) * 0.5))
d.path(smooth(hull(pil), closed=True), "Pillow",
       fill=rad((0, "#F6ECD6"), (0.6, "#D8C4A4"), (1, "#9A8468")), stroke="#8A7458",
       strokeWidth=1.6, join="round")

# --- near side wall ----------------------------------------------------------------------
side_wall(-WX, "Near wall", [(0, "#B05C2E"), (0.5, "#7E3A1C"), (1, "#461C0C")],
          CHERRY)

# --- head end panel -----------------------------------------------------------------------
end_panel("Head panel", -PZ, "head",
          [(0, "#C06838"), (0.4, "#8E4424"), (0.75, "#642A14"), (1, "#3A160A")],
          ("#5E2410", "#361408"))

# head finials
for sgn in (-1, 1):
    turned(f"Head finial {sgn:+d}", (sgn * 8.0, crest_top(8, "head") - 0.5, -PZ - PT / 2),
           (sgn * 8.0, crest_top(8, "head") + 2.4, -PZ - PT / 2), FIN, ink=1.8)

# --- lullaby inlay: maple crescent moon + star on the head panel face ----------------------
FZ = -PZ - PT / 2 - 0.08
MCX, MCY, MR = 0.0, 24.4, 1.5
cres = []
for i in range(26):
    a = math.radians(52 + 256 * i / 25)
    cres.append(P(MCX + MR * math.cos(a), MCY + MR * math.sin(a), FZ))
for i in range(20):
    a = math.radians(300 - 240 * i / 19)
    cres.append(P(MCX + 0.75 + 1.12 * math.cos(a), MCY + 0.35 + 1.12 * math.sin(a), FZ))
d.path("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in cres) + " Z", "Moon inlay",
       fill=lin(cres[0], cres[len(cres) // 2], (0, "#F2DCA8"), (1, "#C8A468")),
       stroke="#8A6234", strokeWidth=1.4, join="round")
st_pts = []
for i in range(8):
    r = 0.85 if i % 2 == 0 else 0.32
    a = -math.pi / 2 + math.tau * i / 8
    st_pts.append(P(2.6 + r * math.cos(a), 25.5 + r * math.sin(a), FZ))
d.path("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in st_pts) + " Z", "Star inlay",
       fill="#F2DCA8", stroke="#8A6234", strokeWidth=1.2, join="round")

# --- hood: shell + near cheek + front rail -------------------------------------------------
def hood_arc(t):
    """Hood crown curve in (z,y): springs off the head crest, over, and rolls
    to the front edge."""
    z = -WZ - 0.6 + (-4.2 - (-WZ - 0.6)) * t
    y = (1 - t) ** 2 * 27.8 + 2 * (1 - t) * t * 34.4 + t ** 2 * 24.6
    return z, y


HX = 6.9           # hood shell half width
CHX = 7.8          # cheek face x (proud of the shell edge)
arc = [hood_arc(i / 30) for i in range(31)]

# hood underside (visible inside the open edge, over the pillow)
inner = [P(-HX + 0.3, y - 0.5, z) for z, y in arc[18:]] + \
        [P(HX - 0.3, y - 0.5, z) for z, y in reversed(arc[18:])]
d.path("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in inner) + " Z", "Hood lining",
       fill=lin(inner[0], inner[-1], (0, "#6E3A22"), (1, "#301408")), stroke=NONE)
glow = P(0, 24.0, -8.5)
d.shape("ellipse", "Hood nightlight glow", x=round(glow[0] - 120), y=round(glow[1] - 46),
        width=240, height=92,
        fill=rad((0, "#FFC88A", 30), (0.7, "#FFC88A", 10), (1, "#FFC88A", 0)), stroke=NONE)

# shell: near edge + far edge joined through the arc
shell = [P(-HX, y, z) for z, y in arc] + [P(HX, y, z) for z, y in reversed(arc)]
shell_g = lin(P(-HX, hood_arc(0)[1], hood_arc(0)[0]), P(-HX, hood_arc(1)[1], hood_arc(1)[0]),
              (0, "#6E2E16"), (0.35, "#D08048"), (0.55, "#E8A066"), (0.8, "#9A4A28"), (1, "#58240F"))
d.path(smooth(shell, closed=True), "Hood shell", fill=shell_g,
       stroke=INK, strokeWidth=2.2, join="round")
# shell plank seams across the crown
for k, tt in enumerate((0.3, 0.55, 0.8)):
    z, y = hood_arc(tt)
    d.path(f"M{P(-HX, y, z)[0]:.1f},{P(-HX, y, z)[1]:.1f} L{P(HX, y, z)[0]:.1f},{P(HX, y, z)[1]:.1f}",
           f"Hood seam {k+1}", fill=NONE, stroke="#3A160A", strokeWidth=1.6, opacity=32)
# sheen along the near crown edge
nsheen = [P(-HX - 0.05, y - 0.3, z) for z, y in arc[8:26]]
d.path(smooth(nsheen), "Hood sheen", fill=NONE, stroke="#FFD2A6", strokeWidth=3,
       opacity=42, cap="round")

# near cheek: solid board — arc top (rear->front) then straight bottom back
ctop = [P(-CHX, y + 0.5, z) for z, y in arc]
cbot = [P(-CHX, BOX_Y1 - 0.4, z) for z, y in reversed(arc)]
d.path(smooth(ctop) + " " + smooth(cbot, move=False) + " Z", "Hood cheek",
       fill=lin(P(-CHX, 33, -8), P(-CHX, 22.5, -8), (0, "#A8552C"), (0.6, "#6E2E16"), (1, "#3E180A")),
       stroke=INK, strokeWidth=2.2, join="round")
# cheek grain + a carved scroll hint
cg = [P(-CHX - 0.05, y - 1.6, z + 0.4) for z, y in arc[6:24]]
d.path(smooth(cg), "Hood cheek grain", fill=NONE, stroke="#4A1E0C", strokeWidth=1.5,
       opacity=35, cap="round")
# cheek front edge thickness (the open edge turns toward the viewer)
fz, fy = hood_arc(1.0)
ef = [P(-CHX, fy + 0.5, fz), P(-HX, fy + 0.3, fz), P(-HX, BOX_Y1 - 0.4, fz),
      P(-CHX, BOX_Y1 - 0.4, fz)]
d.path("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in ef) + " Z", "Cheek edge",
       fill=lin(ef[0], ef[2], (0, "#8E4626"), (1, "#3A160A")), stroke=INK,
       strokeWidth=1.8, join="round")

# front rail across the hood's open edge: face frame with a small crown arch
fy0, fy1 = 23.6, 25.9
fr = [P(-HX, fy1, fz), P(0, fy1 + 0.7, fz), P(HX, fy1, fz), P(HX, fy0, fz),
      P(0, fy0 - 0.5, fz), P(-HX, fy0, fz)]
d.path(smooth(fr, closed=True), "Hood front rail",
       fill=lin(P(0, fy1 + 0.7, fz), P(0, fy0 - 0.5, fz), (0, "#D88C50"), (0.55, "#8E4222"), (1, "#4A1C0C")),
       stroke=INK, strokeWidth=2.2, join="round")
d.path(smooth([P(-HX + 0.6, fy1 - 0.35, fz - 0.05), P(0, fy1 + 0.3, fz - 0.05),
               P(HX - 0.6, fy1 - 0.35, fz - 0.05)]), "Hood rail sheen",
       fill=NONE, stroke="#FFD6AE", strokeWidth=2.2, opacity=40, cap="round")

# --- blanket folded over the near top rail -------------------------------------------------
BZ0, BZ1 = 2.6, 9.0
bx_out, bx_in = -WX - 0.75, -WX + 0.9
# outer face hanging down the wall
bout = [P(bx_out, TOPR1 + 0.15, BZ0), P(bx_out, TOPR1 + 0.15, BZ1)]
for i in range(1, 9):
    t = i / 8
    z = BZ1 + (BZ0 - BZ1) * t
    sag = 1.0 * math.sin(math.pi * t) ** 0.7
    bout.append(P(bx_out - 0.25 - sag * 0.3, 17.6 - sag, z))
d.path(smooth(bout, closed=True), "Blanket",
       fill=lin(bout[0], bout[-1], (0, "#C9D4E2"), (0.55, "#8FA0B8"), (1, "#5A6C84")),
       stroke=INK, strokeWidth=1.8, join="round")
# fold over the rail top
fold = [P(bx_out, TOPR1 + 0.15, BZ0), P(bx_in, TOPR1 - 0.4, BZ0), P(bx_in, TOPR1 - 0.4, BZ1),
        P(bx_out, TOPR1 + 0.15, BZ1)]
d.path("M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in fold) + " Z", "Blanket fold",
       fill=lin(fold[0], fold[1], (0, "#E4ECF6"), (1, "#A8B8CC")), stroke=INK,
       strokeWidth=1.6, join="round")
# inside flap
flap = [P(bx_in, TOPR1 - 0.4, BZ0), P(bx_in, TOPR1 - 0.4, BZ1), P(bx_in - 0.3, 19.6, BZ1 - 0.6),
        P(bx_in - 0.3, 19.9, BZ0 + 0.6)]
d.path(smooth(flap, closed=True), "Blanket inside",
       fill=lin(flap[0], flap[2], (0, "#9AAEC4"), (1, "#647690")), stroke=INK,
       strokeWidth=1.4, join="round")
# a couple of woven stripes on the outer face, roughly following the hem
for i, yv in enumerate((18.9, 19.9)):
    st = [P(bx_out - 0.42, yv, BZ0 + 0.6), P(bx_out - 0.42, yv - 1.5, BZ1 - 0.6)]
    d.path(f"M{st[0][0]:.1f},{st[0][1]:.1f} L{st[1][0]:.1f},{st[1][1]:.1f}",
           f"Blanket stripe {i+1}", fill=NONE, stroke="#E6EEFA", strokeWidth=2.0,
           opacity=45, cap="round")
# stitch dashes along the hem
d.path(smooth([P(bx_out - 0.42, 18.15, BZ1 - (BZ1 - BZ0) * i / 12) for i in range(13)]),
       "Blanket hem", fill=NONE, stroke="#5A6C84", strokeWidth=1.6, opacity=60,
       cap="round", dash=[3, 2])

# --- extent check --------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("cradle extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 28, far


# --- caption --------------------------------------------------------------------------------
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
               color="#F2E4D4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#CBA498", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=60)
    d.cmd("text.setStyle", "Materials tracking", ids=[m["id"]], tracking=260)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "materials")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" %
              (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "materials":
            assert b["width"] <= 760, b["width"]


caption("CRADLE", "CHERRY · PINE · LINEN")
d.finish("cradle-V1R00")
