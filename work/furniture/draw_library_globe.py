#!/usr/bin/env python3
"""Library globe — furniture field plate V1R00. An antique terrestrial globe
on a mahogany four-leg stand: varnished-amber oceans, parchment continents,
engraved graticule, tilted brass meridian ring with hour circle, the engraved
horizon ring band wrapping the ball, tapered legs to brass casters and a
compass-rose stretcher. Old-world map, Africa and Eurasia to the front.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420. Modelled in 3D (x right, y up, z toward
viewer), orthographic projection with a slight downward view; occlusion is
handled by draw order."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Library Globe — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A1406"


def lin(x0, y0, x1, y1, *ss):
    return {"gradient": {"kind": "linear", "start": [round(x0, 1), round(y0, 1)],
            "end": [round(x1, 1), round(y1, 1)],
            "stops": [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {}))
                      for s in ss]}}


def rad(*ss):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in ss]}}


def mix(c0, c1, t):
    a = [int(c0[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(p + (q - p) * t):02X}" for p, q in zip(a, b))


# --- projection: view slightly from above -----------------------------------------------------
CX, CY = 500, 355            # sphere centre on screen
V = math.radians(12)         # view elevation
CV, SV = math.cos(V), math.sin(V)
BOUNDS = []


def P(x, y, z):
    return (CX + x, CY - (y * CV - z * SV))


def path_of(pts, closed=True, track=True):
    q = list(pts)
    if track:
        BOUNDS.extend(q)
    s = "M%.1f,%.1f " % q[0] + " ".join("L%.1f,%.1f" % p for p in q[1:])
    return s + (" Z" if closed else "")


def strip(pts3, w0, w1, n=20):
    """Tapered ribbon along a 3D polyline, widened across the screen
    perpendicular; returns outline points in screen space."""
    pts = [P(*p) for p in pts3]
    n = max(n, len(pts) * 8)
    # resample the polyline
    seg, acc = [], [pts[0]]
    for a, b in zip(pts, pts[1:]):
        seg.append(math.hypot(b[0] - a[0], b[1] - a[1]))
    tot = sum(seg)
    for i in range(1, n):
        t = i * tot / n
        j = 0
        while j < len(seg) - 1 and t > seg[j]:
            t -= seg[j]
            j += 1
        r = 0 if seg[j] == 0 else t / seg[j]
        acc.append((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * r,
                    pts[j][1] + (pts[j + 1][1] - pts[j][1]) * r))
    acc.append(pts[-1])
    left, right = [], []
    for i, p in enumerate(acc):
        a = acc[max(i - 1, 0)]
        b = acc[min(i + 1, len(acc) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = w0 + (w1 - w0) * i / (len(acc) - 1)
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    return left + right[::-1]


# --- globe frame ------------------------------------------------------------------------------
RS = 170                     # sphere radius (world)
TA = math.radians(18)        # axis tilt, top pole leaning right
AX = (math.sin(TA), math.cos(TA), 0)      # north axis
MX = (0.0, 0.0, 1.0)                      # lon 0 faces viewer
NX = (math.cos(TA), -math.sin(TA), 0)     # lon +90 lands toward +x


def sph3(lon, lat):
    lo, la = math.radians(lon), math.radians(lat)
    cl = math.cos(la)
    return (cl * math.cos(lo) * MX[0] + cl * math.sin(lo) * NX[0] + math.sin(la) * AX[0],
            cl * math.cos(lo) * MX[1] + cl * math.sin(lo) * NX[1] + math.sin(la) * AX[1],
            cl * math.cos(lo) * MX[2] + cl * math.sin(lo) * NX[2] + math.sin(la) * AX[2])


def front_runs(pts3, zmin=2.0, closed=False):
    """Split a 3D polyline into runs of visible (near-hemisphere) screen points."""
    runs, cur = [], []
    n = len(pts3)
    rng = range(n + 1) if closed else range(n)
    prev = None
    for i in rng:
        p = pts3[i % n]
        vis = p[2] > zmin
        if vis:
            if prev is not None and prev[2] <= zmin:
                t = (zmin - prev[2]) / (p[2] - prev[2])
                cur.append(P(prev[0] + (p[0] - prev[0]) * t,
                             prev[1] + (p[1] - prev[1]) * t,
                             zmin))
            cur.append(P(*p))
        elif cur:
            if prev is not None and prev[2] > zmin:
                t = (zmin - prev[2]) / (p[2] - prev[2])
                cur.append(P(prev[0] + (p[0] - prev[0]) * t,
                             prev[1] + (p[1] - prev[1]) * t,
                             zmin))
            if len(cur) > 1:
                runs.append(cur)
            cur = []
        prev = p
    if len(cur) > 1:
        runs.append(cur)
    return runs


def clip_front(poly3):
    """Sutherland-Hodgman clip of a 3D polygon to the near hemisphere z>0."""
    out = []
    for i, a in enumerate(poly3):
        b = poly3[(i + 1) % len(poly3)]
        ain, bin_ = a[2] > 0, b[2] > 0
        if ain:
            out.append(a)
        if ain != bin_:
            t = a[2] / (a[2] - b[2])
            out.append((a[0] + (b[0] - a[0]) * t,
                        a[1] + (b[1] - a[1]) * t, 0.0))
    return out


LON0 = 25.0  # real longitude facing the viewer (East Africa / Indian Ocean)


def land(lonlat):
    """Densify a lon/lat coast, clip to the near hemisphere, project."""
    pts = []
    n = len(lonlat)
    for i in range(n):
        a, b = lonlat[i], lonlat[(i + 1) % n]
        dl = max(abs(b[0] - a[0]), abs(b[1] - a[1]))
        k = max(1, int(dl / 4))
        for j in range(k):
            t = j / k
            pts.append(sph3(a[0] + (b[0] - a[0]) * t - LON0,
                            a[1] + (b[1] - a[1]) * t))
    vis = clip_front(pts)
    return [P(x * RS, y * RS, z * RS) for x, y, z in vis]


# --- palette ------------------------------------------------------------------------------------
OCEAN = rad((0, "#E2B25E"), (0.45, "#A5712C"), (0.8, "#6A3E12"), (1, "#3C2008"))
LAND = lin(340, 240, 660, 480, (0, "#D8BE8C"), (0.6, "#B08A50"), (1, "#84602F"))
MAHOG = lin(0, 330, 0, 760, (0, "#6B4220"), (0.5, "#46260F"), (1, "#261105"))
MAHOG_DK = lin(0, 330, 0, 760, (0, "#462810"), (0.6, "#2A1407"), (1, "#170A03"))
BRASS = "#C8973E"
BRASS_HI = "#F2DC96"

# ================================================================================================
# backdrop + plate
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#1B1710"), (1, "#070503")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#9A8458", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#6B563A"), (0.6, "#41311D"), (1, "#150D06")),
        stroke="#0E0804", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E0BE", strokeWidth=3, opacity=24)
# low lamplight from the upper left — library mood
d.shape("ellipse", "Lamplight", x=140, y=80, width=540, height=540,
        fill=rad((0, "#F0D2A0", 0.13), (0.6, "#D8B07C", 0.05), (1, "#D8B07C", 0)),
        stroke=NONE)
for i, (x, y, w) in enumerate([(208, 228, 6), (786, 236, 7), (166, 602, 6), (832, 580, 7),
                               (430, 108, 6), (650, 106, 7), (320, 826, 6), (668, 824, 6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#D0B47E", opacity=30, stroke=NONE)

# floor: a chord of the plate + the arc home, per house rule
HZN = 770
hx = math.sqrt(PR ** 2 - (HZN - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{HZN} L{PCX + hx:.1f},{HZN} A420,420 0 0 1 {PCX - hx:.1f},{HZN} Z",
       "Floor", fill=lin(0, HZN, 0, 880, (0, "#3A2E1C", 0.55), (1, "#130C05", 0.9)),
       stroke=NONE)
for i, yy in enumerate([792, 828]):
    xx = math.sqrt(PR ** 2 - (yy - PCY) ** 2) - 6
    d.path(f"M{PCX - xx:.1f},{yy} L{PCX + xx:.1f},{yy}", f"Floor seam {i+1}",
           fill=NONE, stroke="#100A04", strokeWidth=3, opacity=28)

# --- the stand: coordinates in world units ------------------------------------------------------
AZF, AZB = math.radians(52), math.radians(140)   # front / back leg azimuths
RRING, RFOOT = 250.0, 332.0
YLEG_T, YFOOT = -22.0, -362.0


def leg_pts(az):
    """Tapered, gently bowed leg from ring underside to caster."""
    x0, z0 = RRING * math.sin(az), RRING * math.cos(az)
    x1, z1 = RFOOT * math.sin(az), RFOOT * math.cos(az)
    bow = 16 * (1 if math.sin(az) > 0 else -1)
    return [(x0, YLEG_T, z0),
            ((x0 + x1) / 2 + bow * 0.4, (YLEG_T + YFOOT) / 2, (z0 + z1) / 2 - 10),
            (x1, YFOOT, z1)]


# floor shadow first
shx, shy = P(0, YFOOT - 6, 10)
d.shape("ellipse", "Globe shadow", x=round(shx - 250), y=round(shy - 26),
        width=500, height=52, fill=rad((0, "#060302", 0.7), (1, "#060302", 0)),
        stroke=NONE)

# back legs (behind everything of the stand)
for az, lbl in [(AZB, "L"), (math.pi * 2 - AZB, "R")]:
    d.path(path_of(strip(leg_pts(az), 9, 13)), f"Back leg {lbl}",
           fill=MAHOG_DK, stroke=INK, strokeWidth=1.6, join="round")
    fx, fy = P(RFOOT * math.sin(az), YFOOT, RFOOT * math.cos(az))
    d.shape("ellipse", f"Back caster {lbl}", x=round(fx - 7), y=round(fy - 4),
            width=14, height=12, fill=rad((0, "#8A5E22"), (1, "#382008")),
            stroke=INK, strokeWidth=1.2)

# stretcher ring between the legs + compass medallion
ystretch = -250.0
rxs = 224.0
sx, sy = P(0, ystretch, 0)
rys = rxs * SV / CV
pts_st = [P(rxs * math.cos(t), ystretch, rxs * math.sin(t))
          for t in [2 * math.pi * k / 60 for k in range(61)]]
d.path(path_of(pts_st, False), "Stretcher", fill=NONE, stroke="#3A2210",
       strokeWidth=7, cap="round")
pts_hi = [P(rxs * math.cos(t), ystretch, rxs * math.sin(t))
          for t in [math.pi * 0.08 + 0.02 * k for k in range(45)]]
d.path(path_of(pts_hi, False), "Stretcher light", fill=NONE, stroke="#8A5E30",
       strokeWidth=2.5, cap="round", opacity=60)
# compass medallion at the stretcher centre
d.shape("ellipse", "Compass disc", x=round(sx - 34), y=round(sy - 22), width=68,
        height=44, fill=rad((0, "#E4BE6E"), (0.65, "#A87A30"), (1, "#5C3A10")),
        stroke=INK, strokeWidth=2)
for i in range(8):
    t = math.pi * i / 4
    x0, y0 = sx + 6 * math.cos(t), sy + 4 * math.sin(t)
    x1, y1 = sx + 28 * math.cos(t), sy + 18 * math.sin(t)
    d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", f"Rose ray {i+1}",
           fill=NONE, stroke=INK if i % 2 == 0 else "#7A5424",
           strokeWidth=3 if i % 2 == 0 else 1.8, cap="round", opacity=80)
d.shape("ellipse", "Rose hub", x=round(sx - 5), y=round(sy - 5), width=10,
        height=10, fill="#2A1406", stroke=NONE)

# horizon ring band — full annulus as a wide stroked ellipse, behind the ball
RB_MID = 236.0
band = [P(RB_MID * math.cos(t), 0, RB_MID * math.sin(t))
        for t in [2 * math.pi * k / 96 for k in range(97)]]
d.path(path_of(band, False), "Horizon band", fill=NONE, stroke="#3A2210",
       strokeWidth=46)
band_out = [P(262 * math.cos(t), 0, 262 * math.sin(t))
            for t in [2 * math.pi * k / 96 for k in range(97)]]
d.path(path_of(band_out, False), "Band outer rim", fill=NONE, stroke="#5A3A1E",
       strokeWidth=3)

# meridian ring, far half — a great circle through the tilted axis
RM = 208.0
PHI = math.radians(60)    # ring plane: contains AX, tilted PHI from face-on
PX = (math.cos(TA), -math.sin(TA), 0)     # perp to axis in screen plane
BX = (math.cos(PHI) * PX[0], math.cos(PHI) * PX[1], math.sin(PHI))
ring3 = [(RM * (math.cos(t) * AX[0] + math.sin(t) * BX[0]),
          RM * (math.cos(t) * AX[1] + math.sin(t) * BX[1]),
          RM * (math.cos(t) * AX[2] + math.sin(t) * BX[2]))
         for t in [2 * math.pi * k / 96 for k in range(97)]]
ring_far = [P(*p) for p in ring3 if p[2] <= 0]
if ring_far:
    d.path(path_of(ring_far + [ring_far[0]], False), "Meridian far",
           fill=NONE, stroke="#6E4C1C", strokeWidth=12, cap="round")

# axis rod stubs past the poles
for sgn, lbl in [(1, "N"), (-1, "S")]:
    a = P(*(sgn * (RS - 4) * c for c in AX))
    b = P(*(sgn * (RM + 4) * c for c in AX))
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Axis stub {lbl}",
           fill=NONE, stroke="#8A6224", strokeWidth=5, cap="round")

# --- the ball -----------------------------------------------------------------------------------
d.shape("ellipse", "Sphere", x=CX - RS, y=CY - RS, width=2 * RS, height=2 * RS,
        fill=OCEAN, stroke=INK, strokeWidth=3)

# graticule: parallels then meridians, near hemisphere only
for la in (-60, -30, 0, 30, 60):
    pts = [tuple(c * RS for c in sph3(lo, la)) for lo in range(0, 361, 4)]
    for j, run in enumerate(front_runs(pts, zmin=3.0, closed=True)):
        d.path(path_of(run, False), f"Parallel {la} {j}", fill=NONE,
               stroke="#3A1E08", strokeWidth=2.2, opacity=48, cap="round")
for lo in range(0, 180, 30):
    pts = []
    for k in range(91):
        t = 2 * math.pi * k / 90
        mx = (math.cos(math.radians(lo)) * MX[0] + math.sin(math.radians(lo)) * NX[0],
              math.cos(math.radians(lo)) * MX[1] + math.sin(math.radians(lo)) * NX[1],
              math.cos(math.radians(lo)) * MX[2] + math.sin(math.radians(lo)) * NX[2])
        pts.append((RS * (math.cos(t) * mx[0] + math.sin(t) * AX[0]),
                    RS * (math.cos(t) * mx[1] + math.sin(t) * AX[1]),
                    RS * (math.cos(t) * mx[2] + math.sin(t) * AX[2])))
    for j, run in enumerate(front_runs(pts, zmin=3.0, closed=True)):
        d.path(path_of(run, False), f"Meridian ln {lo} {j}", fill=NONE,
               stroke="#3A1E08", strokeWidth=2.2, opacity=42, cap="round")

# continents — rough antique coasts, lon frame: true lon minus 20 faces viewer
LANDS = {
    "Africa": [(-17, 15), (-10, 4), (6, 4), (9, -1), (12, -8), (14, -16),
               (19, -30), (26, -34), (32, -28), (35, -21), (40, -11),
               (41, -3), (46, 3), (51, 11), (46, 11), (43, 12), (39, 16),
               (37, 21), (32, 31), (25, 32), (19, 33), (11, 37), (3, 37),
               (-6, 36), (-11, 33), (-16, 28), (-17, 21)],
    "Eurasia": [(-10, 37), (-9, 43), (-2, 44), (-4, 48), (2, 50), (6, 54),
                (12, 55), (18, 56), (24, 56), (28, 60), (30, 66), (26, 71),
                (18, 70), (24, 68), (32, 70), (45, 68), (60, 69), (75, 72),
                (95, 75), (110, 74), (125, 72), (140, 72), (155, 70),
                (168, 67), (178, 65), (170, 60), (162, 60), (158, 55),
                (150, 60), (142, 55), (142, 48), (136, 44), (128, 38),
                (122, 34), (121, 30), (115, 24), (110, 20), (108, 14),
                (105, 9), (103, 2), (100, 6), (97, 12), (94, 17), (90, 21),
                (86, 20), (80, 14), (76, 8), (74, 14), (72, 19), (66, 24),
                (60, 25), (56, 26), (52, 28), (48, 30), (44, 32), (42, 36),
                (36, 36), (30, 36), (24, 37), (18, 40), (12, 44), (8, 44),
                (4, 43), (-2, 42)],
    "N-America": [(-58, 46), (-62, 50), (-60, 56), (-66, 60), (-70, 63),
                  (-78, 66), (-86, 67), (-92, 66), (-96, 62), (-94, 57),
                  (-90, 52), (-84, 46), (-80, 42), (-76, 40), (-74, 44),
                  (-68, 44), (-64, 44)],
    "S-America": [(-80, 8), (-76, 10), (-70, 11), (-62, 10), (-55, 6),
                  (-50, 1), (-44, -3), (-38, -6), (-35, -9), (-38, -14),
                  (-41, -20), (-46, -24), (-52, -30), (-58, -34), (-62, -39),
                  (-65, -45), (-66, -52), (-70, -55), (-73, -50), (-73, -42),
                  (-71, -33), (-70, -25), (-70, -18), (-75, -14), (-78, -8),
                  (-80, -3), (-81, 2)],
    "Australia": [(114, -22), (113, -26), (116, -33), (122, -34), (129, -32),
                  (133, -32), (137, -35), (140, -38), (146, -39), (150, -37),
                  (153, -30), (153, -26), (148, -20), (143, -11), (137, -12),
                  (135, -15), (131, -12), (126, -14), (122, -17), (117, -21)],
    "Madagascar": [(44, -16), (47, -15), (50, -16), (50, -21), (46, -25),
                   (44, -24), (43, -20)],
    "Britain": [(-5, 50), (-3, 53), (-2, 57), (-4, 58), (-6, 55), (-5, 52)],
    "Japan": [(130, 31), (133, 34), (137, 35), (140, 36), (141, 39),
              (141, 42), (138, 39), (135, 36), (131, 34)],
    "Borneo-etc": [(110, 0), (114, 3), (118, 2), (119, -2), (115, -4),
                   (111, -3)],
}
for name, coast in LANDS.items():
    pts = land(coast)
    if len(pts) > 2:
        d.path(path_of(pts), f"Land {name}", fill=LAND, stroke=INK,
               strokeWidth=2.2, join="round", opacity=94)

# limb shading + sheen on the varnish
d.shape("ellipse", "Limb shade", x=CX - RS, y=CY - RS, width=2 * RS,
        height=2 * RS, fill=rad((0, "#1E0E04", 0), (0.72, "#1E0E04", 0.06),
        (0.92, "#1E0E04", 0.38), (1, "#140A02", 0.62)), stroke=NONE)
d.shape("ellipse", "Sphere sheen", x=CX - 118, y=CY - 138, width=170,
        height=130, fill=rad((0, "#FFE8B8", 0.34), (1, "#FFE8B8", 0)),
        stroke=NONE)
# scattered islands, antique-map flavour: a few specks in the open ocean
for i, (lo, la, rr) in enumerate([(-58, -8, 4), (-64, -14, 3), (66, -20, 4),
                                  (72, -28, 3), (80, -12, 3), (-80, -20, 3)]):
    px, py = P(*[c * RS for c in sph3(lo, la)])
    d.shape("ellipse", f"Island {i+1}", x=round(px - rr), y=round(py - rr),
            width=2 * rr, height=2 * rr, fill="#C8A468", stroke=NONE,
            opacity=80)
# cartouche: a faint oval label cartouche low on the ocean, antique-map flavour
ctx, cty = P(*[c * RS for c in sph3(52, -32)])
d.shape("ellipse", "Cartouche", x=round(ctx - 26), y=round(cty - 13), width=52,
        height=26, fill=NONE, stroke="#E8D2A0", strokeWidth=2, opacity=40)
d.path(f"M{ctx - 14:.0f},{cty - 2:.0f} L{ctx + 14:.0f},{cty - 2:.0f}",
       "Cartouche line 1", fill=NONE, stroke="#E8D2A0", strokeWidth=1.6,
       opacity=38, cap="round")
d.path(f"M{ctx - 10:.0f},{cty + 4:.0f} L{ctx + 10:.0f},{cty + 4:.0f}",
       "Cartouche line 2", fill=NONE, stroke="#E8D2A0", strokeWidth=1.6,
       opacity=38, cap="round")

# --- in front of the ball -----------------------------------------------------------------------
# near half of the horizon band + engraved ticks + rims
for lo_kind, r_, col, w_, op in [("band near", RB_MID, "#4A2C14", 46, 100),
                                 ("band rim out", 262, "#7A5226", 3, 85),
                                 ("band rim in", 210, "#241204", 3, 80)]:
    run = [P(r_ * math.cos(t), 0, r_ * math.sin(t))
           for t in [math.pi * k / 96 for k in range(97)]]
    d.path(path_of(run, False), f"Horizon {lo_kind}", fill=NONE, stroke=col,
           strokeWidth=w_, cap="round", **({"opacity": op} if op < 100 else {}))
for k in range(19):
    t = math.pi * (k + 0.5) / 19
    a = P(214 * math.cos(t), 0, 214 * math.sin(t))
    b = P(258 * math.cos(t), 0, 258 * math.sin(t))
    d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", f"Band tick {k+1}",
           fill=NONE, stroke="#C8985A", strokeWidth=2.4, opacity=55, cap="round")

# near half of the meridian ring: brass arc sweeping over the face
near = [P(*p) for p in ring3 if p[2] > 0]
if near:
    d.path(path_of(near, False), "Meridian ring", fill=NONE, stroke=BRASS,
           strokeWidth=13, cap="round")
    d.path(path_of(near[4:-4], False), "Meridian light", fill=NONE,
           stroke=BRASS_HI, strokeWidth=3.5, cap="round", opacity=70)

# hour circle at the north pole + finials
hc_c = [c * (RS + 8) for c in AX]
hc = [P(hc_c[0] + 24 * (math.cos(t) * PX[0] + math.sin(t) * 0),
        hc_c[1] + 24 * (math.cos(t) * PX[1] + math.sin(t) * 0),
        hc_c[2] + 24 * math.sin(t))
      for t in [2 * math.pi * k / 40 for k in range(41)]]
d.path(path_of(hc, False), "Hour circle", fill=NONE, stroke=BRASS,
       strokeWidth=4, opacity=90)
for sgn, lbl in [(1, "N"), (-1, "S")]:
    fx, fy = P(*(sgn * (RM + 10) * c for c in AX))
    d.shape("ellipse", f"Finial {lbl}", x=round(fx - 7), y=round(fy - 7),
            width=14, height=14, fill=rad((0, BRASS_HI), (0.7, BRASS), (1, "#6E4A16")),
            stroke=INK, strokeWidth=1.4)

# front legs + collars + casters
for az, lbl in [(AZF, "L"), (math.pi * 2 - AZF, "R")]:
    pts = strip(leg_pts(az), 10, 14)
    d.path(path_of(pts), f"Front leg {lbl}", fill=MAHOG, stroke=INK,
           strokeWidth=2, join="round")
    # turned collar where the leg meets the ring
    cx0, cy0 = P(RRING * math.sin(az), YLEG_T - 8, RRING * math.cos(az))
    d.shape("ellipse", f"Collar {lbl}", x=round(cx0 - 13), y=round(cy0 - 6),
            width=26, height=15, fill=rad((0, "#E4BE6E"), (1, "#7A5220")),
            stroke=INK, strokeWidth=1.6)
    fx, fy = P(RFOOT * math.sin(az), YFOOT, RFOOT * math.cos(az))
    d.shape("ellipse", f"Caster {lbl}", x=round(fx - 9), y=round(fy - 5),
            width=18, height=14, fill=rad((0, "#E4BE6E"), (0.7, "#9A6A26"),
            (1, "#4A2C0C")), stroke=INK, strokeWidth=1.4)

# maker's brass plate on the stretcher medallion front edge — empire detail
d.path(f"M{sx - 40:.0f},{sy + 16:.0f} L{sx + 40:.0f},{sy + 16:.0f} "
       f"L{sx + 34:.0f},{sy + 26:.0f} L{sx - 34:.0f},{sy + 26:.0f} Z",
       "Maker plate", fill=lin(sx - 40, sy + 16, sx + 40, sy + 26,
       (0, "#E4BE6E"), (1, "#7A5220")), stroke=INK, strokeWidth=1.4)

# plate rim over everything
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#0C0603", strokeWidth=6)

# --- captions -------------------------------------------------------------------------------------
d.text("LIBRARY GLOBE", "Name", x=500, y=938, size=56, font="Virelai Sans",
       color="#F4EAD2", justify="center")
LINE2 = "MAHOGANY · BRASS · VARNISHED GESSO"
r = d.text(LINE2, "Second line", x=500, y=974, size=22, font="Virelai Sans",
           color="#CFB88E", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=260)


def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o:
            return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit:
                return hit


b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

# subject stays inside the rim
for x, y in BOUNDS:
    assert math.hypot(x - PCX, y - PCY) <= PR - 12, (x, y)
print("subject points:", len(BOUNDS))

d.finish("library-globe-V1R00")
