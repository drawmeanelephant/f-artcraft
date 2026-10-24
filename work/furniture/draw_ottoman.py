#!/usr/bin/env python3
"""Ottoman — furniture field plate V1R00. Near-side view with a slight
three-quarter from the front left: a tailored ottoman in deep teal velvet on
turned walnut legs — crowned top with a piped welt and shallow button tufts,
a brass nailhead course above the base, and a hardcover book resting on top
(the footrest that doubles as everything). Warm upholstered plate, feet-up
mood. 1000x1000.
Gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420. Modelled in 3D, oblique projection."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Ottoman — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E140C"


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {}))
                      for s in stops]}}


def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": [
        dict(offset=s[0], color=s[1], **({"opacity": s[2]} if len(s) > 2 else {})) for s in stops]}}


def smooth(pts, closed=False):
    n = len(pts)

    def g(i):
        return pts[i % n] if closed else pts[max(0, min(n - 1, i))]
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


# --- projection: x right, y up, z back (model pt * GS) ----------------------------------
GS = 1.25
CX, FY = 565, 792
TH, PH = math.radians(26), math.radians(14)
CT, ST, CP, SP = math.cos(TH), math.sin(TH), math.cos(PH), math.sin(PH)
BOUNDS = []


def P(x, y, z):
    x, y, z = x * GS, y * GS, z * GS
    depth = x * ST + z * CT
    p = (CX + x * CT - z * ST, FY - (y * CP + depth * SP))
    BOUNDS.append(p)
    return p


def path3(ops):
    out = []
    for op in ops:
        xy = [P(*q) for q in op[1:]]
        out.append(op[0] + " ".join("%.1f,%.1f" % q for q in xy))
    return " ".join(out)


def quad3(pts):
    s = "M%.1f,%.1f " % P(*pts[0])
    return s + " ".join("L%.1f,%.1f" % P(*p) for p in pts[1:]) + " Z"


# --- palette --------------------------------------------------------------------------
VELVET_TOP = rad((0, "#4E8886"), (0.55, "#2E5E5C"), (1, "#1B3A3A"))
VELVET_F = lin(0, 620, 0, 740, (0, "#2E5E5C"), (1, "#163030"))
VELVET_L = lin(430, 620, 430, 740, (0, "#3E7674"), (1, "#1E4240"))
VELVET_R = lin(720, 620, 720, 740, (0, "#234A48"), (1, "#122A28"))
VELVET_HI = "#7FB4AE"
WALNUT = lin(0, 700, 0, 800, (0, "#8A5A30"), (1, "#3E2410"))
WALNUT_DK = lin(0, 700, 0, 800, (0, "#5E3C1E"), (1, "#2A1808"))
BOOK = lin(0, 540, 0, 620, (0, "#B8563E"), (1, "#7E3222"))
PAGES = "#EEDFBF"

# --- backdrop + plate -------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 0, 1000, (0, "#1C1410"), (1, "#080504")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#8A7A5A", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#52402A"), (0.55, "#352413"), (1, "#1B1108")), stroke="#140C05", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D2A8", strokeWidth=3, opacity=26)
d.shape("ellipse", "Lamp glow", x=140, y=90, width=540, height=540,
        fill=rad((0, "#FFC98A", 0.28), (0.55, "#FFB468", 0.08), (1, "#FFB468", 0)), stroke=NONE)
FYB = 700
hw = math.sqrt(PR ** 2 - (FYB - PCY) ** 2)
d.path(f"M{PCX + hw:.1f},{FYB} L{PCX - hw:.1f},{FYB} A420,420 0 0 0 {PCX + hw:.1f},{FYB} Z",
       "Floor", fill=lin(0, FYB, 0, 880, (0, "#36240F", 0), (0.4, "#2A1C0C", 0.55), (1, "#150D05", 0.85)),
       stroke=NONE)
for i, yb in enumerate([744, 790, 838]):
    h = math.sqrt(PR ** 2 - (yb - PCY) ** 2) - 4
    d.path(f"M{PCX - h:.1f},{yb} L{PCX + h:.1f},{yb}", f"Board seam {i+1}",
           fill=NONE, stroke="#5A3C1E", strokeWidth=2, opacity=30)

# --- geometry ----------------------------------------------------------------------------
# legs y 0..62, upholstered box y 62..188, crowned top ~188..214
Y0, Y1, YT = 62, 188, 214
BX, BZ0, BZ1 = 150, 8, 232
sx, sy = P(0, 0, 120)
d.shape("ellipse", "Floor shadow", x=round(sx - 250 * GS), y=round(sy - 46 * GS),
        width=round(500 * GS), height=round(92 * GS),
        fill=rad((0, "#060301", 0.72), (0.7, "#060301", 0.32), (1, "#060301", 0)), stroke=NONE)


def leg(label, x, z, fill):
    """Turned leg: pad foot, ankle taper, collar into the body."""
    prof = [(0, 9), (5, 17), (12, 13), (20, 10), (34, 9.5), (46, 13), (54, 16), (62, 12)]
    L = [P(x - w, y, z) for y, w in prof]
    R = [P(x + w, y, z) for y, w in reversed(prof)]
    pts = L + R
    d.path(smooth(pts, closed=True), label, fill=fill, stroke=INK, strokeWidth=3)
    d.path(smooth([P(x - w * 0.4, y, z) for y, w in prof]), label + " gloss",
           fill=NONE, stroke="#D8A86A", strokeWidth=2.5, opacity=40, cap="round")


# far legs first (body covers their tops)
leg("Leg back R", 124, 200, WALNUT_DK)
leg("Leg back L", -124, 200, WALNUT_DK)

# body sides: front face (z=8), left face (x=-150), right face sliver (x=150)
d.path(quad3([(-BX, Y0, BZ0), (BX, Y0, BZ0), (BX, Y1, BZ0), (-BX, Y1, BZ0)]),
       "Front face", fill=VELVET_F, stroke=INK, strokeWidth=4)
d.path(quad3([(-BX, Y0, BZ0), (-BX, Y0, BZ1), (-BX, Y1, BZ1), (-BX, Y1, BZ0)]),
       "Left face", fill=VELVET_L, stroke=INK, strokeWidth=4)
d.path(quad3([(BX, Y0, BZ0), (BX, Y0, BZ1), (BX, Y1, BZ1), (BX, Y1, BZ0)]),
       "Right face", fill=VELVET_R, stroke=INK, strokeWidth=4)
# fabric softness: soft valleys near the corners, sheen mid-panel
for lab, xx in (("FL", -144), ("FR", 144)):
    d.path(path3([("M", (xx, Y0 + 8, BZ0)), ("C", (xx - 2, 100, BZ0), (xx - 2, 150, BZ0), (xx, Y1 - 4, BZ0))]),
           f"Corner valley {lab}", fill=NONE, stroke="#0E2020", strokeWidth=8, opacity=24, cap="round")
d.path(path3([("M", (-90, Y0 + 20, BZ0)), ("C", (-30, Y0 + 8, BZ0), (40, Y0 + 8, BZ0), (110, Y0 + 22, BZ0))]),
       "Front sheen", fill=NONE, stroke=VELVET_HI, strokeWidth=16, opacity=12, cap="round")
d.path(path3([("M", (-BX, Y0 + 20, 40)), ("C", (-BX, Y0 + 8, 110), (-BX, Y0 + 8, 170), (-BX, Y0 + 24, 210))]),
       "Left sheen", fill=NONE, stroke=VELVET_HI, strokeWidth=14, opacity=12, cap="round")
# welt piping along the visible top edges
for lab, a, b in (("front", (-BX + 2, Y1 + 2, BZ0), (BX - 2, Y1 + 2, BZ0)),
                  ("left", (-BX, Y1 + 2, BZ0 + 4), (-BX, Y1 + 2, BZ1)),
                  ("right", (BX, Y1 + 2, BZ0 + 4), (BX, Y1 + 2, BZ1))):
    d.path(path3([("M", a), ("L", b)]), f"Welt {lab}", fill=NONE, stroke=VELVET_HI,
           strokeWidth=3.5, opacity=60, cap="round")
# low seam + brass nailhead course along front and left
for lab, a, b in (("front", (-BX + 4, Y0 + 18, BZ0), (BX - 4, Y0 + 18, BZ0)),
                  ("left", (-BX, Y0 + 18, BZ0 + 8), (-BX, Y0 + 18, BZ1 - 4))):
    d.path(path3([("M", a), ("L", b)]), f"Low welt {lab}", fill=NONE, stroke="#0E2020",
           strokeWidth=3, opacity=50, cap="round")
for face, a, b, n in (("front", (-140, Y0 + 10, BZ0), (140, Y0 + 10, BZ0), 15),
                      ("left", (-BX, Y0 + 10, BZ0 + 16), (-BX, Y0 + 10, BZ1 - 8), 11)):
    for k in range(n):
        t = k / (n - 1)
        qx, qy = P(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t)
        d.shape("ellipse", f"Nail {face} {k+1}", x=round(qx - 3.4), y=round(qy - 3.4),
                width=6.8, height=6.8,
                fill=rad((0, "#F4DE9A"), (0.6, "#C89644"), (1, "#6E4A16")), stroke=NONE)

# crowned top: edges bow up to a domed centre
top = [("M", (-BX, Y1, BZ0)), ("C", (-70, YT - 14, BZ0 - 2), (70, YT - 14, BZ0 - 2), (BX, Y1, BZ0)),
       ("C", (BX + 6, YT - 22, 110), (BX + 6, YT - 20, 140), (BX, Y1, BZ1)),
       ("C", (70, YT - 14, BZ1 + 2), (-70, YT - 14, BZ1 + 2), (-BX, Y1, BZ1)),
       ("C", (-BX - 6, YT - 20, 140), (-BX - 6, YT - 22, 110), (-BX, Y1, BZ0)), ("Z",)]
d.path(path3(top), "Crowned top", fill=VELVET_TOP, stroke=INK, strokeWidth=4)
# centre dome light
d.path(path3([("M", (-90, YT - 26, 60)), ("C", (-40, YT - 10, 90), (40, YT - 10, 90), (96, YT - 28, 70)),
              ("L", (96, YT - 26, 150)), ("C", (40, YT - 8, 170), (-40, YT - 8, 170), (-90, YT - 26, 150)), ("Z",)]),
       "Top dome light", fill=rad((0, "#9ACCC6", 0.30), (1, "#9ACCC6", 0)), stroke=NONE)
# button tufts: two rows of shallow dimples clear of the book
tufts = [(-95, 55), (-42, 48), (92, 55), (42, 48), (-95, 190), (-42, 198), (92, 190), (42, 198)]
for i, (tx, tz) in enumerate(tufts):
    px, py = P(tx, YT - 20, tz)
    d.shape("ellipse", f"Tuft {i+1} dim", x=round(px - 11), y=round(py - 8), width=22, height=15,
            fill="#0E2020", opacity=40, stroke=NONE)
    d.shape("ellipse", f"Tuft {i+1}", x=round(px - 5.5), y=round(py - 5.5), width=11, height=11,
            fill=rad((0, "#4E8886"), (1, "#1B3A3A")), stroke=INK, strokeWidth=1.5)
    d.path("M%.1f,%.1f L%.1f,%.1f" % (px - 9, py - 3, px - 17, py - 7), f"Tuft {i+1} crease a",
           fill=NONE, stroke="#0E2020", strokeWidth=2, opacity=35, cap="round")
    d.path("M%.1f,%.1f L%.1f,%.1f" % (px + 9, py + 2, px + 16, py + 6), f"Tuft {i+1} crease b",
           fill=NONE, stroke="#0E2020", strokeWidth=2, opacity=35, cap="round")

# front legs last so the tops tuck under the body
leg("Leg front R", 124, 30, WALNUT)
leg("Leg front L", -124, 30, WALNUT)
for x, z in ((124, 30), (-124, 30), (124, 200), (-124, 200)):
    fx2, fy2 = P(x, 0, z)
    d.shape("ellipse", f"Foot shade {x},{z}", x=round(fx2 - 17), y=round(fy2 - 3),
            width=34, height=10, fill=rad((0, "#000000", 0.5), (1, "#000000", 0)), stroke=NONE)

# --- the book: a rust hardcover resting on the crown -------------------------------------
bcx, bcz, bth = 6, 118, math.radians(-17)
cb, sb = math.cos(bth), math.sin(bth)


def book_pt(u, v, y):
    return P(bcx + u * cb - v * sb, y, bcz + u * sb + v * cb)


BW, BH, T0, T1 = 48, 30, 202, 218
A = (-BW - 2, -BH - 2); B = (BW + 2, -BH - 2); C = (BW + 2, BH + 2); D = (-BW - 2, BH + 2)

# soft shadow under the book
sh_pts = [book_pt(u, v, T0) for u, v in (A, B, C, D)]
d.path("M%.1f,%.1f " % sh_pts[0] + " ".join("L%.1f,%.1f" % p for p in sh_pts[1:]) + " Z",
       "Book shadow", fill="#0A1A1A", opacity=45, stroke=NONE)
# page block: front (v=-BH) + right (u=BW) faces with page lines
front_pg = [book_pt(u, v, y) for u, v, y in
            ((-BW + 1, -BH, T0 + 3), (BW - 1, -BH, T0 + 3), (BW - 1, -BH, T1 - 2), (-BW + 1, -BH, T1 - 2))]
d.path("M%.1f,%.1f " % front_pg[0] + " ".join("L%.1f,%.1f" % p for p in front_pg[1:]) + " Z",
       "Pages front", fill=PAGES, stroke=INK, strokeWidth=2.5)
right_pg = [book_pt(u, v, y) for u, v, y in
            ((BW, -BH + 1, T0 + 3), (BW, BH - 1, T0 + 3), (BW, BH - 1, T1 - 2), (BW, -BH + 1, T1 - 2))]
d.path("M%.1f,%.1f " % right_pg[0] + " ".join("L%.1f,%.1f" % p for p in right_pg[1:]) + " Z",
       "Pages fore-edge", fill="#E0CFA8", stroke=INK, strokeWidth=2.5)
for i, yy in enumerate((T0 + 7, T0 + 10, T0 + 13)):
    a_ = book_pt(-BW + 2, -BH - 0.5, yy)
    b_ = book_pt(BW - 2, -BH - 0.5, yy)
    d.path("M%.1f,%.1f L%.1f,%.1f" % (a_ + b_), f"Page line {i+1}", fill=NONE,
           stroke="#8A7A54", strokeWidth=1.6, opacity=60)
# spine face (u=-BW): darker cloth band
spine = [book_pt(u, v, y) for u, v, y in
         ((-BW - 2, -BH - 2, T0), (-BW - 2, BH + 2, T0), (-BW - 2, BH + 2, T1), (-BW - 2, -BH - 2, T1))]
d.path("M%.1f,%.1f " % spine[0] + " ".join("L%.1f,%.1f" % p for p in spine[1:]) + " Z",
       "Book spine", fill=lin(0, 540, 0, 640, (0, "#6E2C1E"), (1, "#4A1A10")), stroke=INK, strokeWidth=2.5)
# top cover
cover = [book_pt(u, v, T1) for u, v in (A, B, C, D)]
d.path("M%.1f,%.1f " % cover[0] + " ".join("L%.1f,%.1f" % p for p in cover[1:]) + " Z",
       "Book cover", fill=BOOK, stroke=INK, strokeWidth=3)
# cover sheen + hinge crease + title panel
sh0 = book_pt(-BW + 8, -BH + 6, T1 + 0.5)
sh1 = book_pt(BW - 18, -BH + 12, T1 + 0.5)
d.path("M%.1f,%.1f L%.1f,%.1f" % (sh0 + sh1), "Cover sheen", fill=NONE,
       stroke="#E8A084", strokeWidth=9, opacity=22, cap="round")
h0 = book_pt(-BW + 6, -BH - 1, T1 + 0.5)
h1 = book_pt(-BW + 6, BH + 1, T1 + 0.5)
d.path("M%.1f,%.1f L%.1f,%.1f" % (h0 + h1), "Hinge crease", fill=NONE,
       stroke="#4A1A10", strokeWidth=2.5, opacity=60)
tp = [book_pt(u, v, T1 + 0.6) for u, v in ((-24, -16), (20, -16), (20, 8), (-24, 8))]
d.path("M%.1f,%.1f " % tp[0] + " ".join("L%.1f,%.1f" % p for p in tp[1:]) + " Z",
       "Title panel", fill="#8A3A28", stroke="#5A2216", strokeWidth=2)

# --- sanity -------------------------------------------------------------------------------
worst = min(PR - math.hypot(x - PCX, y - PCY) for x, y in BOUNDS)
xs, ys = [b[0] for b in BOUNDS], [b[1] for b in BOUNDS]
print("bounds x %.0f..%.0f y %.0f..%.0f" % (min(xs), max(xs), min(ys), max(ys)))
print("min clearance to rim: %.1f" % worst)
assert worst > 20, worst

# --- captions ------------------------------------------------------------------------------
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
               color="#F0E8D4", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C0AA90", justify="center")
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


caption("OTTOMAN", "VELVET · WALNUT · BRASS")
d.finish("ottoman-V1R00")
