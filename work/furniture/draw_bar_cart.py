#!/usr/bin/env python3
"""Bar cart — field plate V1R00. Three-quarter view from front-right-above:
a two-tier serving trolley in brass — tube corner posts on caster wheels,
teak tray shelves with a gallery rail at the back and ends, a hoop push
handle on the far end, and the good stock on parade: a tall decanter, a
round cognac bottle, a cocktail shaker and a poured tumbler up top; an ice
bucket and two coupes below. Brass plate, cocktail-hour mood. 1000x1000.
Modelled in inches (x right, y up, +z back); face-culled prisms, yaw+pitch.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Bar Cart — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241304"
EXTENT = []


def stops(*pairs):
    out = []
    for p in pairs:
        s = {"offset": p[0], "color": p[1]}
        if len(p) > 2 and p[2] is not None:
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
YAW, PITCH = math.radians(30), math.radians(20)
S, OX, OY = 14.3, 502.0, 706.0
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
    a = [int(hex1[i:i + 2], 16) for i in (1, 3, 5)]
    c = [int(hex2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(a[i] + (c[i] - a[i]) * b) for i in range(3))


FACES = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
         (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
TO_VIEWER = (SY * CP, SP, -CY * CP)
LIGHT = (-0.42, 0.80, -0.44)
_l = math.sqrt(sum(c * c for c in LIGHT))
LIGHT = tuple(c / _l for c in LIGHT)

BRASS_D, BRASS_L = "#4A2E0C", "#D8A84E"
BRASS_HI = "#F4DCA0"
TEAK_D, TEAK_L = "#3A1E0C", "#9A6634"
GLASS = "#C8DCE0"
AMBER_D, AMBER_L = "#5E2E08", "#E8963C"


def prism(name, corners, dark=BRASS_D, light=BRASS_L, lo=0.10, hi=0.95,
          ink=1.5, bias=0.0):
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
        b = lo + (hi - lo) * max(0.0, lam + bias) ** 0.8
        b = max(0.0, min(1.0, b))
        y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
        g = lin((0, y0), (0, y1), (0, shade(dark, light, min(1, b + 0.12))),
                                 (1, shade(dark, light, b)))
        d.path(poly(pts), name, fill=g, stroke=INK, strokeWidth=ink, join="round")
    return faces


def box(x0, y0, z0, x1, y1, z1):
    return [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
            (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]


def rbox(cx, cz, y0, y1, hw, ht, ang):
    """Box hw x ht in plan, rotated ang about y through (cx,cz)."""
    ca, sa = math.cos(ang), math.sin(ang)
    cs = [(cx + lx * ca + lz * sa, cz - lx * sa + lz * ca)
          for lx, lz in ((-hw, -ht), (hw, -ht), (hw, ht), (-hw, ht))]
    A, B, C, D = cs
    return [(A[0], y0, A[1]), (B[0], y0, B[1]), (B[0], y1, B[1]),
            (A[0], y1, A[1]), (D[0], y0, D[1]), (C[0], y0, C[1]),
            (C[0], y1, C[1]), (D[0], y1, D[1])]


def quad3(name, pts3, fill, stroke=NONE, sw=1.6, opacity=None):
    kw = {"fill": fill}
    if stroke != NONE:
        kw.update(stroke=stroke, strokeWidth=sw, join="round")
    else:
        kw["stroke"] = NONE
    if opacity is not None:
        kw["opacity"] = opacity
    d.path(poly([P(*p) for p in pts3]), name, **kw)


def dot3(name, x, y, z, rx, ry=None, **kw):
    sx, sy = P(x, y, z)
    ry = rx if ry is None else ry
    kw.setdefault("stroke", INK)
    kw.setdefault("strokeWidth", 1.2)
    return d.shape("ellipse", name, x=round(sx - rx, 1), y=round(sy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)


def axis2d(cx, cz):
    """Screen anchor of the vertical axis through (cx,cz)."""
    xr, zr = cx * CY + cz * SY, -cx * SY + cz * CY
    return (OX + S * xr, OY - S * zr * SP)


def turned(name, cx, cz, profile, fill=None, stroke=INK, sw=1.6,
           opacity=None, glint=True):
    """Surface of revolution about the vertical axis at (cx,cz): profile is
    [(r, y)] bottom->top; the silhouette edge projects at xr +/- r."""
    ax, ay = axis2d(cx, cz)
    edge_l = [(ax - S * r, ay - S * CP * y) for r, y in profile]
    edge_r = [(ax + S * r, ay - S * CP * y) for r, y in profile]
    pts = edge_l + edge_r[::-1]
    EXTENT.extend(pts)
    kw = {"fill": fill}
    if stroke != NONE:
        kw.update(stroke=stroke, strokeWidth=sw, join="round")
    else:
        kw["stroke"] = NONE
    if opacity is not None:
        kw["opacity"] = opacity
    d.path(smooth(pts), name, **kw)
    if glint:
        r_max = max(r for r, _ in profile)
        y0, y1 = profile[0][1], profile[-1][1]
        d.path(f"M{ax - S * r_max * 0.55:.1f},{ay - S * CP * (y0 + (y1 - y0) * 0.22):.1f} "
               f"L{ax - S * r_max * 0.45:.1f},{ay - S * CP * (y0 + (y1 - y0) * 0.72):.1f}",
               name + " glint", fill=NONE, stroke="#F8F2E0",
               strokeWidth=max(2.0, S * r_max * 0.13), opacity=32, cap="round")


def bottle(name, cx, cz, profile, liq_h, glass_st, liq_st, sw=1.7):
    """Turned bottle: glass envelope, liquid inside up to liq_h, neck glint."""
    ax, ay = axis2d(cx, cz)
    # liquid first: same profile clipped at liq_h, slightly narrower
    lp = [(r * 0.82, y) for r, y in profile if y <= liq_h]
    if lp and lp[-1][1] < liq_h:
        lp.append((lp[-1][0], liq_h))
    edge_l = [(ax - S * r, ay - S * CP * y) for r, y in lp]
    edge_r = [(ax + S * r, ay - S * CP * y) for r, y in lp]
    pts = edge_l + edge_r[::-1]
    EXTENT.extend(pts)
    d.path(smooth(pts), name + " liquid",
           fill=lin((ax - S, ay - S * CP * liq_h), (ax + S, ay), *liq_st),
           stroke=NONE, opacity=92)
    turned(name, cx, cz, profile, stroke=sw and "#241304" or INK, sw=sw,
           fill=lin((ax - S * 2, ay - S * CP * profile[-1][1]), (ax + S * 2, ay),
                    *glass_st), glint=True)


# --- backdrop + plate: brass hour -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#160D07"), (1, "#060302")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#A8884A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#6B5232"), (0.6, "#443014"), (1, "#140C05")),
        stroke="#0C0704", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8CF9A", strokeWidth=3, opacity=24)
# cocktail-hour spot, low and warm from the left
d.shape("ellipse", "Spot", x=160, y=100, width=620, height=560,
        fill=rad((0, "#F0C87E", 18), (0.55, "#B0803E", 7), (1, "#8A5E28", 0)),
        stroke=NONE)
for i, (x, y, w) in enumerate([(236, 218, 6), (770, 240, 7), (182, 596, 6),
                               (826, 570, 7), (418, 118, 6), (648, 116, 7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C9A869", opacity=26, stroke=NONE)

FY = 712
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#4A3A20", 42), (1, "#100A04", 80)),
       stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#EAD6A8", strokeWidth=2, opacity=18)

# --- geometry (inches): a two-tier trolley ---------------------------------------
HX, HZ = 13.0, 7.0            # half-width x, half-depth z
TOP0, TOP1 = 24.6, 26.2       # top tray slab
LOW0, LOW1 = 6.6, 8.2         # lower tray slab
POST_T = 26.2                  # posts carry the top tray
HANDLE_T = 34.0                # push-hoop top
RAIL_Y = 28.4                  # gallery rail height on the top tray

# grounding shadow
sh = [P(x, 0, z) for x in (-HX - 1, HX + 1) for z in (-HZ - 1, HZ + 1)]
sx0, sx1 = min(p[0] for p in sh) - 34, max(p[0] for p in sh) + 34
sy0, sy1 = min(p[1] for p in sh) - 12, max(p[1] for p in sh) + 16
d.shape("ellipse", "Cart shadow", x=round(sx0), y=round(sy0),
        width=round(sx1 - sx0), height=round(sy1 - sy0),
        fill=rad((0, "#050302", 66), (0.6, "#050302", 25), (1, "#050302", 0)),
        stroke=NONE)


def caster(name, x, z, far=False):
    """Small swivel wheel under a post: fork, tyre disc, brass hub."""
    wx, wy = P(x, 0.95, z)
    wr = S * 1.05
    al = 55 if far else 95
    # fork: short strut from post bottom to the wheel axle
    quad3(name + " fork", [(x - 0.4, 1.6, z), (x + 0.4, 1.6, z),
                           (x + 0.28, 0.8, z), (x - 0.28, 0.8, z)],
          lin((wx - 6, wy - wr), (wx + 6, wy), (0, BRASS_L), (1, BRASS_D)),
          stroke=INK, sw=1.2, opacity=min(100, al))
    d.shape("ellipse", name + " tyre", x=round(wx - wr * 0.62), y=round(wy - wr),
            width=round(wr * 1.24), height=round(wr * 2),
            fill=rad((0, "#3E2A14"), (0.7, "#1E1108"), (1, "#0C0604")),
            stroke=INK, strokeWidth=1.4, opacity=min(100, al - 10))
    d.shape("ellipse", name + " hub", x=round(wx - wr * 0.22), y=round(wy - wr * 0.22),
            width=round(wr * 0.44), height=round(wr * 0.44),
            fill=rad((0, BRASS_HI), (1, BRASS_D)), stroke=INK, strokeWidth=1.1,
            opacity=min(100, al))


def post(name, x, z, far=False):
    """Upright brass corner post; the far pair carries the push hoop."""
    prism(name, box(x - 0.45, 1.4, z - 0.45, x + 0.45, POST_T, z + 0.45),
          lo=0.14, hi=0.98, ink=1.5, bias=(-0.12 if far else 0))
    caster(name + " caster", x, z, far=far)


def hoop():
    """Push handle at the far (-x) end: two risers + a swept crossbar."""
    pts3 = [(-HX, POST_T - 0.4, -HZ), (-HX, HANDLE_T - 0.6, -HZ),
            (-HX, HANDLE_T + 0.5, -HZ * 0.5), (-HX, HANDLE_T + 0.8, 0),
            (-HX, HANDLE_T + 0.5, HZ * 0.5), (-HX, HANDLE_T - 0.6, HZ),
            (-HX, POST_T - 0.4, HZ)]
    pts = [P(*p) for p in pts3]
    d.path(smooth(pts, closed=False), "Push handle", fill=NONE,
           stroke="#5E3C12", strokeWidth=8.5, cap="round", join="round")
    d.path(smooth(pts, closed=False), "Push handle brass", fill=NONE,
           stroke=BRASS_L, strokeWidth=4.6, cap="round", join="round")
    up = [(x, y - 1.6) for x, y in pts[1:-1]]
    d.path(smooth(up, closed=False), "Handle glint", fill=NONE,
           stroke=BRASS_HI, strokeWidth=1.8, opacity=70, cap="round")


def tray(name, y0, y1):
    """Teak tray slab across the full plan + darker inset top panel."""
    prism(name + " slab", box(-HX, y0, -HZ, HX, y1, HZ),
          dark=TEAK_D, light=TEAK_L, lo=0.16, hi=0.98, ink=2.0)
    # rolled brass edge on the front rim
    a, b = P(-HX, y1 - 0.12, -HZ - 0.28), P(HX, y1 - 0.12, -HZ - 0.28)
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", name + " rim",
           fill=NONE, stroke=BRASS_L, strokeWidth=3.2, opacity=90, cap="round")
    # end caps of the slab that culling leaves open
    for s_ in (-1, 1):
        cap = [(s_ * HX, y0, -HZ), (s_ * HX, y0, HZ),
               (s_ * HX, y1, HZ), (s_ * HX, y1, -HZ)]
        ys = [P(*p)[1] for p in cap]
        quad3(name + f" end {s_:+}", cap,
              lin((0, min(ys)), (0, max(ys)), (0, "#6E421E"), (1, "#2E1608")),
              stroke=INK, sw=1.5)


def rail():
    """Gallery rail on the top tray: back edge + both ends (front stays open)."""
    bars = [("back", [(-HX + 0.5, RAIL_Y - 0.5, HZ - 0.35), (HX - 0.5, RAIL_Y - 0.5, HZ - 0.35),
                      (HX - 0.5, RAIL_Y, HZ - 0.35), (-HX + 0.5, RAIL_Y, HZ - 0.35),
                      (-HX + 0.5, RAIL_Y - 0.5, HZ + 0.05), (HX - 0.5, RAIL_Y - 0.5, HZ + 0.05),
                      (HX - 0.5, RAIL_Y, HZ + 0.05), (-HX + 0.5, RAIL_Y, HZ + 0.05)])]
    for s_ in (-1, 1):
        bars.append((f"end {s_:+}", rbox(s_ * (HX - 0.3), 0, RAIL_Y - 0.5, RAIL_Y,
                                         0.22, HZ - 0.4, 0)))
    for nm, c in bars:
        prism(f"Rail {nm}", c, lo=0.18, hi=1.0, ink=1.2)


def coupe(name, cx, cz):
    """Coupe glass: stem, foot, and a shallow bowl with a charge of amber."""
    ax, ay = axis2d(cx, cz)
    y0 = LOW1
    foot = [(0.9, y0), (0.95, y0 + 0.18), (0.3, y0 + 0.5)]
    stem = [(0.16, y0 + 0.4), (0.16, y0 + 2.6)]
    bowl = [(1.35, y0 + 3.4), (1.45, y0 + 4.05), (1.1, y0 + 4.3)]
    prof = foot + stem + bowl
    edge_l = [(ax - S * r, ay - S * CP * y) for r, y in prof]
    edge_r = [(ax + S * r, ay - S * CP * y) for r, y in prof]
    pts = edge_l + edge_r[::-1]
    EXTENT.extend(pts)
    d.path(smooth(pts), name, fill=lin((ax - S, ay - S * CP * (y0 + 4.3)),
                                       (ax + S, ay - S * CP * y0),
                                       (0, GLASS, 55), (0.6, GLASS, 28), (1, "#8AA0A4", 45)),
           stroke="#3A2A14", strokeWidth=1.4, join="round")
    # charge line inside the bowl
    ch = [(ax - S * 1.15, ay - S * CP * (y0 + 3.55)),
          (ax + S * 1.15, ay - S * CP * (y0 + 3.55)),
          (ax + S * 1.0, ay - S * CP * (y0 + 4.0)),
          (ax - S * 1.0, ay - S * CP * (y0 + 4.0))]
    d.path(poly(ch), name + " charge", fill=AMBER_L, opacity=70, stroke=NONE)


# === far end first =========================================================
hoop()
post("Post far back", -HX, HZ, far=True)
post("Post far front", -HX, -HZ, far=True)

# lower tray + its stock, seen through the gap
tray("Lower tray", LOW0, LOW1)
# ice bucket: tapered brass cylinder, domed lid, ring handle
ax, ay = axis2d(-5.5, 0.6)
turned("Ice bucket", -5.5, 0.6, [(1.7, LOW1), (1.95, LOW1 + 0.5), (1.8, LOW1 + 4.4)],
       fill=lin((ax - S * 2, ay - S * CP * (LOW1 + 4.4)), (ax + S * 2, ay - S * CP * LOW1),
                (0, "#E8B968"), (0.55, "#B08038"), (1, "#4A2E0C")),
       sw=1.7, glint=False)
d.shape("ellipse", "Ice bucket lid", x=round(ax - S * 1.7), y=round(ay - S * CP * (LOW1 + 4.4) - S * 0.55),
        width=round(S * 3.4), height=round(S * 1.1),
        fill=rad((0, BRASS_HI), (0.7, BRASS_L), (1, BRASS_D)),
        stroke=INK, strokeWidth=1.4)
dot3("Ice bucket knob", -5.5, LOW1 + 5.0, 0.6, 4.2, 3.4,
     fill=rad((0, BRASS_HI), (1, BRASS_D)))
# two coupes, one behind the other
coupe("Coupe back", 4.6, 2.6)
coupe("Coupe front", 6.8, -0.8)
# a slim jigger standing between them
jx, jy = axis2d(1.8, -1.4)
turned("Jigger", 1.8, -1.4, [(0.55, LOW1), (0.75, LOW1 + 2.2), (0.5, LOW1 + 2.9)],
       fill=lin((jx - S, jy - S * CP * (LOW1 + 2.9)), (jx + S, jy - S * CP * LOW1),
                (0, BRASS_HI), (1, BRASS_D)), sw=1.3, glint=False)

# near-side posts over the lower tier
post("Post near back", HX, HZ)
post("Post near front", HX, -HZ)

# top tray + gallery rail
tray("Top tray", TOP0, TOP1)
# rail back edge only runs behind the bottles; end rails after
rail()

# === top-shelf stock, far to near =========================================
# tall square-shouldered decanter, far left
bottle("Decanter", -8.6, 2.4,
       [(1.45, TOP1), (1.6, TOP1 + 0.5), (1.6, TOP1 + 3.4), (0.95, TOP1 + 4.8),
        (0.55, TOP1 + 5.2), (0.55, TOP1 + 6.6), (0.75, TOP1 + 6.9)],
       TOP1 + 3.2,
       [(0, GLASS, 28), (0.6, GLASS, 14), (1, "#8AA0A4", 26)],
       [(0, "#E8963C"), (0.7, "#B86818"), (1, "#6E3808")])
dot3("Decanter stopper", -8.6, TOP1 + 7.05, 2.4, 5.4, 5.2,
     fill=rad((0, "#F0E8D8"), (0.6, "#B8C4C6"), (1, "#5E6E72")))
# round cognac bottle, centre-back
bottle("Cognac", -2.2, 3.6,
       [(1.55, TOP1), (1.85, TOP1 + 0.8), (1.75, TOP1 + 2.6), (1.1, TOP1 + 3.8),
        (0.5, TOP1 + 4.4), (0.48, TOP1 + 5.8), (0.62, TOP1 + 6.1)],
       TOP1 + 3.4,
       [(0, GLASS, 30), (0.6, GLASS, 16), (1, "#8AA0A4", 28)],
       [(0, "#D88428"), (0.7, "#9E520F"), (1, "#5A2C06")])
# cocktail shaker, right of centre: a tapered steel cobbler shaker
sx_, sy_ = axis2d(3.6, 1.6)
turned("Shaker", 3.6, 1.6,
       [(1.2, TOP1), (1.4, TOP1 + 0.4), (1.3, TOP1 + 4.6), (0.95, TOP1 + 5.5),
        (0.8, TOP1 + 6.4), (0.95, TOP1 + 7.1), (0.6, TOP1 + 7.6)],
       fill=lin((sx_ - S * 1.4, sy_ - S * CP * (TOP1 + 7.6)), (sx_ + S * 1.4, sy_ - S * CP * TOP1),
                (0, "#D8D0C0"), (0.4, "#9AA8AC"), (0.75, "#5E6E74"), (1, "#324042")),
       sw=1.7, glint=False)
d.path(f"M{sx_ - S * 1.28:.1f},{sy_ - S * CP * (TOP1 + 4.5):.1f} "
       f"L{sx_ - S * 0.98:.1f},{sy_ - S * CP * (TOP1 + 6.2):.1f}",
       "Shaker glint", fill=NONE, stroke="#F8F4E8", strokeWidth=3.4,
       opacity=45, cap="round")
d.path(f"M{axis2d(3.6, 1.6)[0] - S * 1.05:.1f},{axis2d(3.6, 1.6)[1] - S * CP * (TOP1 + 5.1):.1f} "
       f"L{axis2d(3.6, 1.6)[0] + S * 1.05:.1f},{axis2d(3.6, 1.6)[1] - S * CP * (TOP1 + 5.1):.1f}",
       "Shaker seam", fill=NONE, stroke="#3A2A14", strokeWidth=1.4, opacity=60)
# small bitters bottle behind the shaker
bottle("Bitters", 8.8, 3.8,
       [(0.8, TOP1), (0.95, TOP1 + 0.3), (0.9, TOP1 + 3.4), (0.4, TOP1 + 4.0),
        (0.36, TOP1 + 5.6)],
       TOP1 + 3.2,
       [(0, GLASS, 50), (1, "#8AA0A4", 42)],
       [(0, "#8A3810"), (1, "#4A1C04")])
# a poured tumbler up front on the tray
tx, ty = axis2d(8.0, -1.2)
EXTENT.extend([(tx - S * 1.3, ty), (tx + S * 1.3, ty - S * CP * (TOP1 + 3.6))])
d.path(poly([(tx - S * 0.95, ty - S * CP * (TOP1 + 0.4)),
             (tx + S * 0.95, ty - S * CP * (TOP1 + 0.4)),
             (tx + S * 1.08, ty - S * CP * (TOP1 + 3.3)),
             (tx - S * 1.08, ty - S * CP * (TOP1 + 3.3))]), "Tumbler pour",
       fill=lin((0, ty - S * CP * (TOP1 + 3.3)), (0, ty - S * CP * (TOP1 + 0.4)),
                (0, "#E8963C", 80), (0.6, "#B86818", 85), (1, "#6E3808", 90)),
       stroke="#3A2A14", strokeWidth=1.2, join="round", opacity=85)
# whisky sphere in the tumbler
d.shape("ellipse", "Tumbler ice", x=round(tx - S * 0.5), y=round(ty - S * CP * (TOP1 + 2.6) - S * 0.4),
        width=round(S * 1.0), height=round(S * 0.85),
        fill=rad((0, "#F4FAFA", 75), (1, "#A8C4C8", 50)), stroke="#E8F0F0",
        strokeWidth=1.0, opacity=75)
# glass outline over the pour
d.path(f"M{tx - S * 1.15:.1f},{ty - S * CP * TOP1:.1f} "
       f"L{tx - S * 1.25:.1f},{ty - S * CP * (TOP1 + 0.35):.1f} "
       f"L{tx - S * 1.15:.1f},{ty - S * CP * (TOP1 + 3.2):.1f} "
       f"L{tx - S * 1.28:.1f},{ty - S * CP * (TOP1 + 3.55):.1f} "
       f"L{tx + S * 1.28:.1f},{ty - S * CP * (TOP1 + 3.55):.1f} "
       f"L{tx + S * 1.15:.1f},{ty - S * CP * (TOP1 + 3.2):.1f} "
       f"L{tx + S * 1.25:.1f},{ty - S * CP * (TOP1 + 0.35):.1f} "
       f"L{tx + S * 1.15:.1f},{ty - S * CP * TOP1:.1f} Z", "Tumbler glass",
       fill=lin((tx - S, ty - S * CP * (TOP1 + 3.5)), (tx + S, ty - S * CP * TOP1),
                (0, GLASS, 30), (0.6, GLASS, 14), (1, "#8AA0A4", 26)),
       stroke="#3A2A14", strokeWidth=1.5, join="round")

# end rails drawn over the near stock edges for depth
# post caps: brass finials on all four corners
for i, (px, pz) in enumerate([(-HX, -HZ), (-HX, HZ), (HX, -HZ), (HX, HZ)]):
    dot3(f"Post cap {i+1}", px, POST_T + 0.25, pz, 4.2, 3.4,
         fill=rad((0, BRASS_HI), (1, BRASS_D)))

# --- extent check ----------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("bar cart extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 24, far


# --- caption ----------------------------------------------------------------------
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
               color="#F4E2C0", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C9A869", justify="center")
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


caption("BAR CART", "BRASS · TEAK · GLASS")
d.finish("bar-cart-V1R00")
