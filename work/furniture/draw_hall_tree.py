#!/usr/bin/env python3
"""Hall tree — field plate V1R00. Three-quarter from the front right:
an oak hallstand — two deep posts joined by a crest rail, a tall mirror
between them, four cast-iron double hooks, a bench seat, and under the
seat an open bay with an iron drip tray holding two wet boots and a
leaning umbrella. A damp coat hangs off the far post's top hook.
Mud-season mood: cold grey light, rain streaks high on the plate.
1000x1000.
Modelled in inches (x right, y up, +z back), fixed yaw + pitch projection;
frame members are 8-corner prisms, mirror/hooks/props in the front plane.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Hall Tree — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E140C"   # warm dark, not black
EXTENT = []


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


def poly(pts):
    return "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"


def smooth(pts, closed=True):
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = "M%.1f,%.1f" % pts[0]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


# --- projection ------------------------------------------------------------------
YAW, PITCH = math.radians(18), math.radians(10)
S, OX, OY = 7.4, 502.0, 712.0
CY, SY = math.cos(YAW), math.sin(YAW)
CP, SP = math.cos(PITCH), math.sin(PITCH)


def P(x, y, z):
    xr, zr = x * CY + z * SY, -x * SY + z * CY
    p = (OX + S * xr, OY - S * (y * CP + zr * SP))
    EXTENT.append(p)
    return p


def depth(x, y, z):
    """View-space distance; smaller = nearer the viewer (front-right-above)."""
    return -x * SY * CP - y * SP + z * CY * CP


def box(x0, y0, z0, x1, y1, z1):
    """8 corners of an axis-aligned box, near quad (-z) first, CCW from below-left."""
    return [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]


FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
TO_VIEWER = (SY * CP, SP, -CY * CP)          # normals facing this draw
LIGHT = (-0.48, 0.80, -0.36)
_l = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / _l for c in LIGHT)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def normal(c, f):
    u = sub(c[f[1]], c[f[0]])
    v = sub(c[f[3]], c[f[0]])
    n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2],
         u[0] * v[1] - u[1] * v[0])
    l = math.sqrt(sum(k * k for k in n))
    return tuple(k / l for k in n)


def shade(hex1, hex2, b):
    """Mix two hex colors at brightness b in [0,1]."""
    a = [int(hex1[i:i + 2], 16) for i in (1, 3, 5)]
    c = [int(hex2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (c[i] - a[i]) * b) for i in range(3))


OAK_D, OAK_L = "#2A1808", "#7C5020"        # hallway oak, a little sober
OAK_HI = "#B8894C"


def prism(name, corners, lo=0.06, hi=0.94, ink=1.8, c1=OAK_D, c2=OAK_L):
    """Draw the viewer-facing faces of an 8-corner prism, far to near."""
    faces = []
    for f in FACES:
        n = normal(corners, f)
        if n[0] * TO_VIEWER[0] + n[1] * TO_VIEWER[1] + n[2] * TO_VIEWER[2] <= 0.02:
            continue
        lam = max(0.0, sum(n[i] * LIGHT[i] for i in range(3)))
        dep = sum(depth(*corners[i]) for i in f) / len(f)
        pts = [P(*corners[i]) for i in f]
        faces.append((dep, pts, lam))
    for dep, pts, lam in sorted(faces, key=lambda t: -t[0]):
        b = lo + (hi - lo) * lam ** 0.8
        y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
        g = lin((0, y0), (0, y1), (0, shade(c1, c2, min(1, b + 0.12))),
                                 (1, shade(c1, c2, b)))
        d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return faces


def fquad(x0, y0, x1, y1, z):
    return [P(x0, y0, z), P(x1, y0, z), P(x1, y1, z), P(x0, y1, z)]


IRON_D, IRON_L = "#14120E", "#3E3A30"      # cast iron ramp


def iron(pts):
    y0 = min(p[1] for p in pts)
    y1 = max(p[1] for p in pts)
    return lin((0, y0), (0, y1), (0, IRON_D), (0.55, IRON_L), (1, IRON_D))


# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#14191A"), (1, "#070A0A")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#5E6E62", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#3A4038"), (0.6, "#282E28"), (1, "#10140F")),
        stroke="#0A0D09", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8DECB", strokeWidth=3, opacity=20)
# cold daylight from the left — the door just opened
d.shape("ellipse", "Door light", x=120, y=120, width=560, height=560,
        fill=rad((0, "#D8E4DC", 16), (0.5, "#8A9A8E", 6), (1, "#8A9A8E", 0)),
        stroke=NONE)
# rain streaks, high left — mud season outside
for i, (rx, ry, rl) in enumerate([(300, 150, 60), (350, 120, 74), (405, 155, 56),
                                  (268, 210, 48), (445, 205, 44)]):
    d.path(f"M{rx},{ry} L{rx - rl * 0.22:.0f},{ry + rl}", f"Rain {i + 1}",
           fill=NONE, stroke="#C8D8D0", strokeWidth=2.2, opacity=14, cap="round")

FY = 712
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#40463C", 30), (1, "#0D100A", 72)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#DCE2CC", strokeWidth=2, opacity=15)

# --- frame geometry (inches; x right, y up, +z back) -----------------------------------
# hallstand: 34 wide, 79 to the crest, 16 deep; posts carry seat + back
XW, ZD = 17.0, 8.0
POST_X0, POST_X1 = 14.5, 17.0

shadow_pts = [P(-XW, 0, -ZD), P(XW, 0, -ZD), P(XW, 0, ZD), P(-XW, 0, ZD)]
sx0 = min(p[0] for p in shadow_pts) - 40
sx1 = max(p[0] for p in shadow_pts) + 40
sy0 = min(p[1] for p in shadow_pts) - 12
sy1 = max(p[1] for p in shadow_pts) + 22
d.shape("ellipse", "Hallstand shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#040503", 70), (0.6, "#040503", 28), (1, "#040503", 0)),
        stroke=NONE)

# far post first, then shared members, near post last
prism("Far post", box(-POST_X1, 0, -ZD, -POST_X0, 76, ZD), lo=0.05, hi=0.85)

# back panel between the posts: stiles + mirror rail, recessed behind post faces
BP = -ZD + 0.5                       # back-panel front plane
prism("Panel stile L", box(-14.5, 20, -ZD, -12.5, 74, BP), lo=0.06, hi=0.9)
prism("Panel stile R", box(12.5, 20, -ZD, 14.5, 74, BP), lo=0.06, hi=0.9)
prism("Panel rail B", box(-14.5, 20, -ZD, 14.5, 24, BP), lo=0.06, hi=0.9)
prism("Panel rail T", box(-14.5, 70, -ZD, 14.5, 74, BP), lo=0.06, hi=0.9)

# mirror glass inside the frame, slightly deeper still
mir = fquad(-12.0, 24.5, 12.0, 69.5, -ZD - 0.1)
d.path(poly(mir), "Mirror glass",
       fill=lin((0, mir[0][1]), (0, mir[2][1]),
                (0, "#7E948A", 90), (0.45, "#4A6056", 88), (1, "#6E847A", 90)),
       stroke=NONE)
# a faint reflected doorway: pale upright quad off-centre
rq = fquad(-9.5, 30, -4.0, 62, -ZD - 0.16)
d.path(poly(rq), "Mirror doorway", fill="#B8CCC2", opacity=14, stroke=NONE)
rq2 = fquad(-8.7, 31.5, -4.8, 60, -ZD - 0.18)
d.path(poly(rq2), "Mirror doorway inner", fill="#7C8E84", opacity=18, stroke=NONE)
# long diagonal sheen across the glass
s0, s1 = P(-11.0, 66, -ZD - 0.2), P(-6.0, 66, -ZD - 0.2)
s2, s3 = P(3.0, 28, -ZD - 0.2), P(8.0, 28, -ZD - 0.2)
d.path(poly([s0, s1, s3, s2]), "Mirror sheen", fill="#E8F2EC", opacity=10,
       stroke=NONE)
# mirror bevel: a fine bright line inside the frame's top-left edges
ba, bb = P(-11.8, 69.2, -ZD - 0.14), P(11.8, 69.2, -ZD - 0.14)
d.path(f"M{ba[0]:.1f},{ba[1]:.1f} L{bb[0]:.1f},{bb[1]:.1f}", "Bevel top",
       fill=NONE, stroke="#DCEAE0", strokeWidth=1.6, opacity=40)
bc, bd = P(-11.8, 69.2, -ZD - 0.14), P(-11.8, 25.0, -ZD - 0.14)
d.path(f"M{bc[0]:.1f},{bc[1]:.1f} L{bd[0]:.1f},{bd[1]:.1f}", "Bevel left",
       fill=NONE, stroke="#DCEAE0", strokeWidth=1.6, opacity=30)

# crest rail + small centre crest between the post tops
prism("Crest rail", box(-XW, 76, -ZD, XW, 79, ZD), lo=0.06, hi=0.95, ink=2.0)
prism("Crest", box(-3.0, 79, -ZD + 1.5, 3.0, 82, ZD - 1.5), lo=0.08, hi=1.0, ink=1.9)
# little turned cap on each post top
for i, tx in enumerate((-POST_X0 - 1.25, POST_X0 + 1.25)):
    tcx, tcy = P(tx, 79.6, 0)
    d.shape("ellipse", f"Post cap {i + 1}", x=round(tcx - 8), y=round(tcy - 7),
            width=16, height=14,
            fill=rad((0, "#C89A58"), (0.55, "#7C5020"), (1, "#2A1808")),
            stroke=INK, strokeWidth=1.5)

# --- seat + under-seat bay --------------------------------------------------------------
# seat slab spanning the posts, front edge proud and rounded by a lip prism
prism("Seat", box(-POST_X0 - 0.6, 16.5, -ZD - 0.8, POST_X0 + 0.6, 19.5, ZD),
      lo=0.08, hi=1.0, ink=2.0)
# seat-front sheen
fa, fb = P(-14.5, 19.1, -ZD - 0.85), P(14.5, 19.1, -ZD - 0.85)
d.path(f"M{fa[0]:.1f},{fa[1]:.1f} L{fb[0]:.1f},{fb[1]:.1f}", "Seat edge light",
       fill=NONE, stroke=OAK_HI, strokeWidth=2.4, opacity=45, cap="round")
# low front rail closing the bay
prism("Bay rail", box(-POST_X0, 2.0, -ZD - 0.3, POST_X0, 5.0, -ZD + 1.0),
      lo=0.05, hi=0.85, ink=1.8)

# drip tray in the bay: shallow iron pan, faint wet glint on its rim
tray = [P(-10.5, 5.2, -ZD + 1.2), P(10.5, 5.2, -ZD + 1.2),
        P(11.5, 6.6, -ZD + 0.6), P(-11.5, 6.6, -ZD + 0.6)]
d.path(poly(tray), "Drip tray rim", fill=iron(tray), stroke=INK,
       strokeWidth=1.8, join="round")
pan = fquad(-11.5, 4.2, 11.5, 5.4, -ZD + 1.0)
d.path(poly(pan), "Drip tray pan",
       fill=lin((0, pan[0][1]), (0, pan[2][1]), (0, "#0E0C08"), (1, "#241F16")),
       stroke=INK, strokeWidth=1.6, join="round")
wet = fquad(-8.5, 4.6, 8.5, 5.1, -ZD + 0.9)
d.path(poly(wet), "Tray water", fill="#5E6E68", opacity=35, stroke=NONE)

# two wet boots standing on the tray, dark leather
def boot(name, bx, hgt, flip):
    """L-silhouette: foot forward (+flip*dir), shaft up, in plane z=-6."""
    z = -6.0
    fw = 3.4 * flip
    pts = smooth([P(bx, 6.2, z), P(bx - 0.2, 10.5, z), P(bx + 0.6 * flip, hgt, z),
                  P(bx + 2.4 * flip, hgt - 0.2, z), P(bx + 2.2 * flip, 9.2, z),
                  P(bx + 2.0 * flip, 7.4, z), P(bx + fw, 7.2, z),
                  P(bx + fw + 0.6 * flip, 6.4, z), P(bx + fw * 0.85, 5.9, z)])
    d.path(pts, name,
           fill=lin((0, P(bx, hgt, z)[1]), (0, P(bx, 6, z)[1]),
                    (0, "#4A3A26"), (0.6, "#2C1F10"), (1, "#140D06")),
           stroke=INK, strokeWidth=1.8, join="round")
    # sole line + damp highlight down the shaft
    sa_, sb_ = P(bx + 0.2, 6.5, z - 0.05), P(bx + fw + 0.3 * flip, 6.6, z - 0.05)
    d.path(f"M{sa_[0]:.1f},{sa_[1]:.1f} L{sb_[0]:.1f},{sb_[1]:.1f}",
           f"{name} sole", fill=NONE, stroke="#0C0804", strokeWidth=2.2,
           opacity=80, cap="round")
    hx_, hy_ = P(bx + 0.7 * flip, hgt - 1.4, z - 0.05)
    d.path(f"M{hx_:.1f},{hy_:.1f} L{hx_ + 3:.1f},{hy_ + 16:.1f}",
           f"{name} damp", fill=NONE, stroke="#7C8C82", strokeWidth=2.4,
           opacity=32, cap="round")


boot("Boot L", -8.6, 14.0, 1)
boot("Boot R", -3.4, 13.4, 1)

# umbrella leaning against the bay's right side: rolled canopy + handle
uz = -5.2
u0, u1 = P(5.6, 5.6, uz), P(10.4, 16.8, uz)          # tip -> handle base
ux, uy = u1[0] - u0[0], u1[1] - u0[1]
ul = math.hypot(ux, uy)
nx_, ny_ = -uy / ul, ux / ul
canopy = [(u0[0] - nx_ * 1.2, u0[1] - ny_ * 1.2),
          (u1[0] - ux / ul * 2.4 - nx_ * 5.2, u1[1] - uy / ul * 2.4 - ny_ * 5.2),
          (u1[0] - ux / ul * 2.4 + nx_ * 5.2, u1[1] - uy / ul * 2.4 + ny_ * 5.2),
          (u0[0] + nx_ * 1.2, u0[1] + ny_ * 1.2)]
d.path(poly(canopy), "Umbrella canopy",
       fill=lin(u0, u1, (0, "#241A12"), (0.5, "#4E4030"), (1, "#1E140C")),
       stroke=INK, strokeWidth=2.0, join="round")
# ferrule + wet glint down the canopy
d.path(f"M{u0[0] - nx_ * 1.0:.1f},{u0[1] - ny_ * 1.0:.1f} "
       f"L{u0[0] - ux / ul * 2.4:.1f},{u0[1] - uy / ul * 2.4:.1f}",
       "Umbrella ferrule", fill=NONE, stroke="#9AA49C", strokeWidth=2.6,
       cap="round")
d.path(f"M{(u0[0] + u1[0]) / 2 - nx_ * 2.6:.1f},{(u0[1] + u1[1]) / 2 - ny_ * 2.6:.1f} "
       f"L{u1[0] - ux / ul * 3.2 - nx_ * 3.4:.1f},{u1[1] - uy / ul * 3.2 - ny_ * 3.4:.1f}",
       "Umbrella glint", fill=NONE, stroke="#8A96A0", strokeWidth=2.2,
       opacity=40, cap="round")
# handle: short stick past the canopy + a J-hook
d.path(f"M{u1[0] - ux / ul * 2.4:.1f},{u1[1] - uy / ul * 2.4:.1f} "
       f"L{u1[0]:.1f},{u1[1]:.1f}", "Umbrella stick", fill=NONE,
       stroke="#6A4A22", strokeWidth=3.0, cap="round")
d.path(smooth([u1, (u1[0] + ux / ul * 2.2, u1[1] + uy / ul * 2.2),
               (u1[0] + ux / ul * 3.6 - nx_ * 2.4, u1[1] + uy / ul * 3.6 - ny_ * 2.4)],
              closed=False), "Umbrella handle", fill=NONE,
       stroke="#6A4A22", strokeWidth=3.4, cap="round")

# near post over the seat/bay junctions, before the hooks mount on it
prism("Near post", box(POST_X0, 0, -ZD, POST_X1, 76, ZD), lo=0.08, hi=1.0)

# --- hooks: four cast-iron doubles on the posts -----------------------------------------
def hook(name, hx, hy, sgn):
    """Mount plate on the post face + two big curls — the classic double hook."""
    z = -ZD - 0.5
    mp = fquad(hx - 1.3, hy - 2.6, hx + 1.3, hy + 2.6, z)
    d.path(poly(mp), f"{name} mount", fill=iron(mp), stroke=INK,
           strokeWidth=1.6, join="round")
    for mx, my in ((hx - 0.7, hy + 1.7), (hx - 0.7, hy - 1.7)):
        mpx, mpy = P(mx, my, z - 0.05)
        d.shape("ellipse", f"{name} screw", x=round(mpx - 3), y=round(mpy - 3),
                width=6, height=6, fill=rad((0, "#8A8478"), (1, "#181410")),
                stroke=INK, strokeWidth=0.9)
    # upper arm sweeps up and out; lower arm dips and hooks under
    for j, (dy, rise, sw) in enumerate(((1.8, 3.2, 5.2), (-0.9, 1.4, 4.4))):
        a = P(hx, hy + dy, z - 0.1)
        b = P(hx + sgn * 1.2, hy + dy + 1.2, z - 0.4)
        c = P(hx + sgn * 2.9, hy + dy + 1.9, z - 0.6)
        e = P(hx + sgn * 3.5, hy + dy + rise, z - 0.5)
        d.path(smooth([a, b, c, e], closed=False), f"{name} arm {j + 1}",
               fill=NONE, stroke="#2E2A22", strokeWidth=sw + 1.4, cap="round")
        d.path(smooth([a, b, c, e], closed=False), f"{name} arm {j + 1} lit",
               fill=NONE, stroke=IRON_L, strokeWidth=sw, cap="round")
        tx, ty = e
        d.shape("ellipse", f"{name} tip {j + 1}", x=round(tx - 5), y=round(ty - 5),
                width=10, height=10, fill=rad((0, "#6E6858"), (1, "#181410")),
                stroke=INK, strokeWidth=1.2)


hook("Hook FL hi", -POST_X0 - 0.2, 66, -1)
hook("Hook FL lo", -POST_X0 - 0.2, 56, -1)
hook("Hook NR hi", POST_X0 + 0.2, 66, 1)
hook("Hook NR lo", POST_X0 + 0.2, 56, 1)

# --- the damp coat on the far top hook ---------------------------------------------------
# shoulders over the hook, body tapering to a wet hem — olive oilskin
cz = -ZD - 0.55
coat = smooth([P(-16.4, 63.5, cz), P(-17.6, 61.5, cz), P(-18.6, 57.0, cz),
               P(-19.4, 51.0, cz), P(-19.8, 44.5, cz), P(-19.4, 40.0, cz),
               P(-14.6, 38.6, cz), P(-11.8, 39.4, cz), P(-10.6, 42.0, cz),
               P(-11.0, 48.0, cz), P(-11.6, 55.0, cz), P(-12.8, 60.0, cz),
               P(-14.2, 62.8, cz), P(-15.2, 63.6, cz)])
d.path(coat, "Wet coat",
       fill=lin((0, P(-15, 64, cz)[1]), (0, P(-15, 38, cz)[1]),
                (0, "#4E5A40"), (0.45, "#39432E"), (1, "#202618")),
       stroke=INK, strokeWidth=2.2, join="round")
# collar + fold lines + a darker wet hem band
col = smooth([P(-16.2, 63.2, cz - 0.05), P(-15.6, 62.0, cz - 0.05),
              P(-14.4, 62.4, cz - 0.05), P(-13.9, 63.2, cz - 0.05)])
d.path(col, "Coat collar", fill="#2A301E", stroke=INK, strokeWidth=1.6)
for i, fx_ in enumerate((-17.4, -15.0, -12.9)):
    fpts = smooth([P(fx_, 58, cz - 0.05), P(fx_ - 0.6, 50, cz - 0.05),
                   P(fx_ - 0.2, 43, cz - 0.05)], closed=False)
    d.path(fpts, f"Coat fold {i + 1}", fill=NONE, stroke="#1C2214",
           strokeWidth=1.8, opacity=55)
hem = smooth([P(-19.4, 42.5, cz - 0.05), P(-15.5, 41.2, cz - 0.05),
              P(-11.6, 43.2, cz - 0.05)], closed=False)
d.path(hem, "Coat wet hem", fill=NONE, stroke="#161C10", strokeWidth=4.5,
       opacity=60, cap="round")

# grain: two long soft strokes on the near post's lit face
for i, gz in enumerate((-6.0, -3.0)):
    gpts = smooth([P(POST_X1 + 0.03, 4 + i * 2, gz - 1.4),
                   P(POST_X1 + 0.03, 30, gz),
                   P(POST_X1 + 0.03, 55, gz + 1.0),
                   P(POST_X1 + 0.03, 74, gz + 0.4)], closed=False)
    d.path(gpts, f"Post grain {i + 1}", fill=NONE, stroke="#1C0F04",
           strokeWidth=1.6, opacity=26)
# near post edge sheen
ea, eb = P(POST_X1 - 0.25, 4, -ZD - 0.05), P(POST_X1 - 0.25, 74, -ZD - 0.05)
d.path(f"M{ea[0]:.1f},{ea[1]:.1f} L{eb[0]:.1f},{eb[1]:.1f}", "Post sheen",
       fill=NONE, stroke=OAK_HI, strokeWidth=2.6, opacity=30, cap="round")

# --- extent check ---------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("hall tree extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 20, far


# --- caption ----------------------------------------------------------------------------------
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
               color="#E6EADA", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#B4BCA2", justify="center")
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


caption("HALL TREE", "OAK · IRON · GLASS")
d.finish("hall-tree-V1R00")
