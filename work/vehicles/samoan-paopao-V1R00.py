#!/usr/bin/env python3
"""Samoan paopao — field plate V1R00. A small everyday fishing canoe:
dugout hull with decked ends and an open waist, single tapered outrigger
float (ama) held on two gently arched booms (kiato) with sennit lashings.
Slight elevated profile from the outrigger side so the float reads clear of
the hull across a strip of lagoon; a paddle rests across the afterdeck with
its blade dipped at the stern quarter. Warm timber over an indigo lagoon
at last light; a low motu with palms closes the far horizon. No sail, no
ornament — the brief is a working boat.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; water chord y=510."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Samoan Paopao — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241812"
EXTENT = []


def ext(pts):
    EXTENT.extend(pts)


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def chord(y):
    h = math.sqrt(PR ** 2 - (y - PCY) ** 2)
    return PCX - h, PCX + h


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


def smooth(pts, closed=True, move=True):
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = ("M%.1f,%.1f" if move else "L%.1f,%.1f") % pts[0]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


def cubic(p0, p1, p2, p3, n=20):
    return [tuple((1 - t) ** 3 * p0[k] + 3 * (1 - t) ** 2 * t * p1[k] +
                  3 * (1 - t) * t * t * p2[k] + t ** 3 * p3[k] for k in (0, 1))
            for t in [i / n for i in range(n + 1)]]


def ribbon(name, spine, w0, w1, fill, ink=2.0):
    """Tapered filled ribbon along a spine polyline (half-width w0->w1)."""
    n = len(spine)
    left, right = [], []
    for i, p in enumerate(spine):
        q0 = spine[max(0, i - 1)]
        q1 = spine[min(n - 1, i + 1)]
        tx, ty = q1[0] - q0[0], q1[1] - q0[1]
        L = math.hypot(tx, ty) or 1
        nx, ny = -ty / L, tx / L
        w = w0 + (w1 - w0) * i / (n - 1)
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    ext(left + right)
    d.path(smooth(left, closed=False) + " " + smooth(right[::-1], closed=False, move=False) + " Z",
           name, fill=fill, stroke=INK, strokeWidth=ink, join="round")
    return left, right


def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(cx - rx, 1), y=round(cy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)


def line(name, x0, y0, x1, y1, w, color, **kw):
    return d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", name, fill=NONE,
                  stroke=color, strokeWidth=w, cap="round", **kw)


HULL = lin((0, 440), (0, 570),
           (0, "#B9825A"), (0.45, "#8A5A34"), (0.8, "#5A3A20"), (1, "#3E2712"))
HULL_TOP = lin((0, 452), (0, 500), (0, "#D0A06C"), (1, "#96683E"))
INTERIOR = lin((0, 470), (0, 510), (0, "#2E1E12"), (1, "#120B06"))
FLOAT_W = lin((0, 650), (0, 695), (0, "#C9A26E"), (0.55, "#8A6238"), (1, "#4E3319"))
BOOM_W = lin((0, 480), (0, 680), (0, "#B98A58"), (0.6, "#7A4E2A"), (1, "#503018"))
SEAT_W = lin((0, 490), (0, 505), (0, "#C1945F"), (1, "#7C5228"))
PADDLE_W = lin((0, 460), (0, 600), (0, "#A57A4E"), (1, "#54371F"))

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#0B0F22"), (1, "#04060F")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#4A5C9E", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin((0, 40), (0, 880), (0, "#26305C"), (0.55, "#2E3A6B"),
                 (0.78, "#1B2347"), (1, "#0E1330")),
        stroke="#080C1E", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.72, "#000000", 0), (1, "#060A18", 0.55)),
        stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C6D2E8", strokeWidth=3, opacity=30)

# last light: warm ember low over the lagoon, slightly left of centre
d.shape("ellipse", "Sunset glow", x=170, y=270, width=600, height=330,
        fill=rad((0, "#E8963C", 22), (0.55, "#B4642E", 6), (1, "#B4642E", 0)),
        stroke=NONE)
d.shape("ellipse", "Sunset core", x=350, y=380, width=240, height=130,
        fill=rad((0, "#F0B45C", 36), (0.55, "#D8843C", 10), (1, "#D8843C", 0)),
        stroke=NONE)

# --- far motu on the horizon, port side -------------------------------------------
# low islet mass sitting on the water chord
motu = [(128, 508), (150, 494), (196, 486), (248, 490), (300, 496), (330, 508)]
d.path(smooth(motu), "Motu", fill="#0D1330", opacity=82, stroke=NONE)
# coconut palms: thin leaning trunks, frond fans
for i, (tx, ty, lean, h) in enumerate([(172, 492, -14, 58), (222, 488, 6, 66),
                                       (272, 492, 16, 52)]):
    top = (tx + lean, ty - h)
    line(f"Palm trunk {i+1}", tx, ty + 4, top[0], top[1], 3.2, "#0A0F28", opacity=85)
    for j, (dx, dy) in enumerate([(-26, 2), (-18, -9), (-6, -14), (8, -13),
                                  (20, -7), (26, 3)]):
        d.path(f"M{top[0]},{top[1]} Q{top[0] + dx * 0.6},{top[1] + dy * 0.7 - 4} "
               f"{top[0] + dx},{top[1] + dy}",
               f"Palm {i+1} frond {j+1}", fill=NONE, stroke="#0A0F28",
               strokeWidth=3.0, cap="round", opacity=85)
    ext([top, (top[0] - 26, top[1]), (top[0] + 26, top[1])])

# --- lagoon: chord segment closing on the rim arc ----------------------------------
wx0, wx1 = chord(510)
d.path(f"M{wx0:.1f},510 L{wx1:.1f},510 A{PR},{PR} 0 0 1 {wx0:.1f},510 Z",
       "Lagoon", fill=lin((0, 510), (0, 880), (0, "#3A4C8E"), (0.35, "#222E5E"),
                          (0.75, "#121A3E"), (1, "#090D22")), stroke=NONE)
# horizon line: last light catching the water seam
line("Horizon light", wx0 + 30, 511, wx1 - 30, 511, 2.0, "#8A96C8", opacity=30)
# warm path the ember throws across the water
for i, (cx, cy, rx, op) in enumerate([(460, 522, 200, 26), (470, 545, 150, 20),
                                      (480, 575, 110, 15), (490, 615, 80, 10)]):
    ell(f"Glow path {i+1}", cx, cy, rx, 7 + i * 2,
        fill=rad((0, "#E8A04A", 0.5), (1, "#E8A04A", 0)), stroke=NONE, opacity=op)
# a few cool swell bands, all inside the chord
for i, (cx, cy, rx, op) in enumerate([(250, 600, 130, 16), (640, 640, 160, 13),
                                      (360, 720, 190, 11), (700, 760, 150, 9)]):
    if on_disc(cx - rx, cy, 4) and on_disc(cx + rx, cy, 4):
        ell(f"Swell {i+1}", cx, cy, rx, 8,
            fill=rad((0, "#5C6EB0", 0.4), (1, "#5C6EB0", 0)), stroke=NONE, opacity=op)

# --- reflections, under everything that floats --------------------------------------
ell("Hull reflection", 505, 592, 225, 15,
    fill=rad((0, "#120A06", 0.5), (0.7, "#120A06", 0.22), (1, "#120A06", 0)),
    stroke=NONE)
ell("Float reflection", 430, 716, 185, 10,
    fill=rad((0, "#0E0A06", 0.45), (1, "#0E0A06", 0)), stroke=NONE)

# --- hull ---------------------------------------------------------------------------
# sheer profile: blunt rising ends, gentle sag amidships, deep dugout body
hull = [(234, 470), (310, 480), (420, 487), (505, 490), (600, 488),
        (700, 478), (778, 458),          # sheer, bow -> stern (stern raised)
        (772, 496),                       # stern face, slight inward run
        (700, 528), (560, 552), (420, 558), (300, 540), (238, 512)]
ext(hull)
d.path(smooth(hull), "Hull", fill=HULL, stroke=INK, strokeWidth=3.5, join="round")
# rubbing strake: a low seam running the hull side below the sheer
line("Rubbing strake", 244, 496, 776, 470, 2.4, "#2E1D10", opacity=38)
line("Rubbing strake 2", 258, 502, 764, 478, 2.0, "#1E1208", opacity=24)

# dugout cavity: far lip -> dark interior -> near sheer (decked ends cover it)
d.path("M262,480 Q500,506 748,464 L752,480 Q500,540 268,498 Z",
       "Interior", fill=INTERIOR, stroke=NONE)
# far gunwale lip catching the light
d.path("M262,480 Q500,506 748,464", "Far gunwale", fill=NONE,
       stroke=HULL_TOP, strokeWidth=4.5, cap="round")
# decked ends: solid covers bow and stern of the open waist
d.path(smooth([(234, 470), (290, 477), (336, 483), (338, 494),
               (292, 489), (238, 482)]), "Fore deck",
       fill=HULL_TOP, stroke=INK, strokeWidth=1.8, join="round")
d.path(smooth([(672, 480), (726, 470), (778, 458), (772, 476),
               (722, 486), (676, 490)]), "After deck",
       fill=HULL_TOP, stroke=INK, strokeWidth=1.8, join="round")
# faint coaming line where each deck meets the open waist
line("Fore deck seam", 336, 483, 340, 494, 2.4, "#241608", opacity=55)
line("After deck seam", 672, 480, 676, 490, 2.4, "#241608", opacity=55)
# thwart seat plank spanning the cavity, just aft of midships
d.path(smooth([(520, 494), (598, 498), (600, 506), (522, 502)]),
       "Thwart seat", fill=SEAT_W, stroke=INK, strokeWidth=1.6, join="round")
# near gunwale edge
d.path("M234,470 Q505,494 778,458", "Near gunwale", fill=NONE,
       stroke="#3A2616", strokeWidth=4.5, cap="round")
# weathered grain on the topside
for i, (x0, y0, x1, y1, op) in enumerate([(300, 512, 430, 520, 28),
                                          (470, 522, 610, 514, 24),
                                          (560, 540, 690, 526, 20),
                                          (290, 528, 400, 536, 20)]):
    line(f"Grain {i+1}", x0, y0, x1, y1, 2.2, "#2E1D10", opacity=op)

# --- paddle across the afterdeck, blade dipped at the stern quarter -------------------
line("Paddle shaft", 668, 466, 828, 566, 6.5, PADDLE_W)
line("Paddle grip", 668, 466, 656, 458, 7.5, "#8A6238")
d.path(smooth([(820, 552), (838, 566), (846, 584), (842, 600),
               (830, 602), (818, 588), (812, 570)]),
       "Paddle blade", fill=PADDLE_W, stroke=INK, strokeWidth=2.4, join="round")
ext([(656, 458), (846, 584), (842, 600)])

# --- outrigger float (ama): tapered log, ends ticking up, clear of the hull -----------
float_pts = [(248, 678), (300, 670), (380, 666), (460, 666), (540, 672),
             (612, 682),                       # top edge, fore -> aft
             (608, 692), (540, 690), (460, 688), (380, 686), (300, 686),
             (252, 688)]
ext(float_pts)
d.path(smooth(float_pts), "Ama float", fill=FLOAT_W,
       stroke=INK, strokeWidth=2.8, join="round")
# pointed tip caps read as carved ends
d.path("M248,678 Q244,682 252,688", "Ama fore tip", fill=NONE,
       stroke="#3A2616", strokeWidth=2.2, cap="round")
d.path("M612,682 Q616,686 608,692", "Ama aft tip", fill=NONE,
       stroke="#3A2616", strokeWidth=2.2, cap="round")
line("Ama sheen", 300, 672, 560, 676, 2.6, "#E8CDA0", opacity=40)

# --- booms (kiato): two arched spars, gunwale -> float --------------------------------
BOOMS = [((388, 486), (352, 556), (338, 616), (352, 664)),
         ((556, 490), (524, 562), (512, 622), (530, 670))]
for i, (p0, p1, p2, p3) in enumerate(BOOMS):
    spine = cubic(p0, p1, p2, p3)
    ribbon(f"Boom {i+1}", spine, 9.5, 6.5, BOOM_W, ink=2.2)

# sennit lashings: crisscross wraps at gunwale and at the float
def lash(name, cx, cy, dx, dy, n=3, gap=5.5, w=3.2):
    for j in range(n):
        off = (j - (n - 1) / 2) * gap
        line(f"{name} {j+1}", cx - dx + off, cy - dy, cx + dx + off, cy + dy,
             w, "#1E1208", opacity=80)
    for j in range(n - 1):
        off = (j - (n - 2) / 2) * gap
        line(f"{name} x{j+1}", cx + dx + off, cy - dy, cx - dx + off, cy + dy,
             w, "#2E1D10", opacity=60)


lash("Boom1 gunwale lash", 386, 487, 10, 7)
lash("Boom2 gunwale lash", 554, 491, 10, 7)
lash("Boom1 float lash", 352, 666, 11, 8)
lash("Boom2 float lash", 530, 672, 11, 8)

# --- water dressing -------------------------------------------------------------------
for i, (cx, cy, rx, op) in enumerate([(252, 540, 50, 40), (330, 548, 34, 30),
                                      (756, 528, 55, 42), (700, 534, 36, 32)]):
    ell(f"Hull ripple {i+1}", cx, cy, rx, 6,
        fill=rad((0, "#8FA2D8", 0.5), (1, "#8FA2D8", 0)), stroke=NONE, opacity=op)
for i, (cx, cy, rx, op) in enumerate([(262, 694, 55, 42), (590, 702, 60, 40),
                                      (430, 700, 90, 26)]):
    ell(f"Float ripple {i+1}", cx, cy, rx, 5.5,
        fill=rad((0, "#8FA2D8", 0.5), (1, "#8FA2D8", 0)), stroke=NONE, opacity=op)
ell("Blade wash", 838, 604, 30, 7,
    fill=rad((0, "#9CB2E2", 0.5), (1, "#9CB2E2", 0)), stroke=NONE)

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("paopao extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far


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
    n = d.text(name, "Name", x=500, y=932, size=58, font="Virelai Sans",
               color="#EDEBE2", justify="center")
    m = d.text(mats, "Materials", x=500, y=968, size=22, font="Virelai Sans",
               color="#AEB8D0", justify="center")
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


caption("PAOPAO", "DUGOUT · OUTRIGGER")
d.finish("samoan-paopao-V1R00")
