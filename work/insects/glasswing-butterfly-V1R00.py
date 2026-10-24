#!/usr/bin/env python3
"""Glasswing (Greta oto) — field plate V1R00. A living glasswing resting on a
slim leaf, wings held in a relaxed open tilt — not a flat pinned spread:
the whole insect is rotated a touch off-axis and its feet grip the leaf.
Glass panels are true transparency: the plate and the leaf under the right
wings read through the membrane, with faint vein strokes inside. Dark umber
borders, the pale subapical band on each forewing, clubbed antennae.
No pin, no board. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Glasswing Butterfly — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#24160F"   # warm soot-brown, not black

REACH = []
TH = math.radians(-14)          # the whole insect leans left, head high
CX0, CY0 = 500, 445


def tr(p):
    dx, dy = p[0] - CX0, p[1] - CY0
    return (CX0 + dx * math.cos(TH) - dy * math.sin(TH),
            CY0 + dx * math.sin(TH) + dy * math.cos(TH))


def sc(p):
    q = tr(p)
    REACH.append(q)
    return q


def mir(p):
    return (1000 - p[0], p[1])


def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0},
                                     {"offset": 1, "color": c1}]}
    if start:
        g["start"], g["end"] = start, end
    return {"gradient": g}


def rad(*stops):
    n = len(stops) - 1
    return {"gradient": {"kind": "radial", "stops": [
        {"offset": round(i / n, 3), "color": c} for i, c in enumerate(stops)]}}


def smooth(pts, closed=True, k=1.0):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    rng_ = range(n) if closed else range(n - 1)
    for i in rng_:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")


def inset(pts, ds):
    """Offset each outline point toward the wing's interior by its own distance."""
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    out = []
    for i, p in enumerate(pts):
        a, b = pts[i - 1], pts[(i + 1) % len(pts)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty) or 1
        nx, ny = -ty / ln, tx / ln
        if nx * (cx - p[0]) + ny * (cy - p[1]) < 0:
            nx, ny = -nx, -ny
        out.append((p[0] + nx * ds[i], p[1] + ny * ds[i]))
    return out


def spot(name, c, w, h, fill, op=95):
    d.shape("ellipse", name, x=round(c[0] - w / 2, 1), y=round(c[1] - h / 2, 1),
            width=w, height=h, fill=fill, stroke=NONE, opacity=op)


# --- palette ------------------------------------------------------------------------------
BG_GRAD = lin("#10180F", "#050804", [0, 0], [0, 1000])
PLATE_GRAD = rad("#9CB49A", "#5E7A64", "#26382E")
BORDER_FILL = rad("#4A3220", "#2A1A10", "#150D07")
GLASS = "#DCE9EE"
PALE = "#F0E9D4"
BODY = rad("#4A3426", "#2A1A12", "#160D08")

# --- backdrop + plate ------------------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#6E8A6E", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#142018", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#000000", "opacity": 0},
            {"offset": 0.72, "color": "#000000", "opacity": 0},
            {"offset": 1, "color": "#060C08", "opacity": 0.55}]}}, stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE8D4", strokeWidth=3, opacity=40)
# understory light pool, upper left
d.shape("ellipse", "Light pool", x=150, y=90, width=540, height=380,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F0F4DC", "opacity": 0.30},
            {"offset": 1, "color": "#F0F4DC", "opacity": 0}]}}, stroke=NONE)
# one soft out-of-focus leaf shape behind everything
d.path(smooth([(120, 330), (220, 300), (330, 310), (360, 350), (300, 390),
               (180, 390)]), "Ghost leaf", fill="#2A4032", opacity=30,
       stroke=NONE)

# --- the perch: one slim lance leaf on a rising diagonal --------------------------------------
# midrib M0 -> M1; blade bulges below the rib, tip slips under the right wings
M0, M1 = (250, 650), (746, 394)
leaf_top = [(250, 650), (330, 606), (450, 552), (580, 490), (680, 432), (746, 394)]
leaf_bot = [(732, 416), (656, 474), (538, 530), (418, 586), (308, 636)]
leaf_pts = leaf_top + leaf_bot
d.path(smooth(leaf_pts), "Perch leaf",
       fill=lin("#6E9A68", "#28503A", [280, 640], [740, 400]),
       stroke="#16281C", strokeWidth=3.5, join="round")
d.path(f"M{M0[0]},{M0[1]} Q490,522 {M1[0] - 8},{M1[1] + 6}", "Leaf midrib",
       fill=NONE, stroke="#C8DCB4", strokeWidth=3, opacity=65, cap="round")
# a short bare stem trailing off the leaf base
d.path(f"M{M0[0]},{M0[1]} Q226,672 208,702", "Leaf stem", fill=NONE,
       stroke="#2E4A34", strokeWidth=5, cap="round")
# soft shadow the insect throws along the leaf
d.shape("ellipse", "Leaf shadow", x=340, y=512, width=290, height=32,
        fill=rad("#0A140C", "#0A140C"), opacity=30, stroke=NONE)

# --- legs: drawn before the wings so they emerge from behind onto the leaf -------------------
LEAF = lambda x: 650 + (394 - 650) * (x - 250) / (746 - 250)
for i, (ax, ay, fx) in enumerate([(492, 430, 452), (490, 452, 516), (488, 474, 580)]):
    for flip in (False, True):
        a = sc((ax, ay))
        if flip:
            a = mir(a)
        f = (fx, LEAF(fx) + 8)
        knee = ((a[0] + f[0]) / 2 + 8, (a[1] + f[1]) / 2 - 6)
        d.path(f"M{a[0]:.1f},{a[1]:.1f} Q{knee[0]:.1f},{knee[1]:.1f} {f[0]:.1f},{f[1]:.1f}",
               f"Leg {i+1} {'R' if not flip else 'L'}", fill=NONE, stroke=INK,
               strokeWidth=3.5, cap="round", opacity=90)

# --- wing data (local frame: body vertical, head up; R side, mirrored for L) -------------------
FW = [(512, 338), (556, 302), (620, 270), (695, 246), (758, 236), (795, 244),
      (802, 272), (792, 318), (774, 364), (752, 406), (726, 436), (682, 444),
      (622, 436), (564, 416), (520, 396)]
FW_D = [10, 10, 11, 14, 28, 36, 36, 33, 28, 22, 15, 11, 9, 8, 8]
FW_VEINS = [((524, 352), 2), ((524, 352), 4), ((526, 360), 7), ((526, 366), 8),
            ((528, 372), 9), ((526, 382), 10), ((524, 388), 11)]

HW = [(514, 392), (576, 386), (652, 394), (714, 420), (756, 462), (768, 514),
      (756, 564), (724, 606), (678, 638), (628, 650), (582, 642), (548, 614),
      (528, 566), (518, 500), (512, 442)]
HW_D = [7, 8, 10, 15, 20, 22, 22, 22, 20, 17, 13, 9, 7, 6, 6]
HW_VEINS = [((522, 398), 2), ((524, 404), 3), ((526, 410), 5), ((528, 418), 6),
            ((526, 424), 8), ((524, 430), 9), ((522, 436), 11)]


def wing(name, outline, ds, veins, flip, extras=None):
    o = [sc(p) for p in outline]
    if flip:
        o = [mir(p) for p in o]
    ins = inset(o, ds)
    cx = sum(p[0] for p in o) / len(o)
    cy = sum(p[1] for p in o) / len(o)
    # glass panel first: a real window, the plate and leaf show through
    d.path(smooth(ins), f"{name} glass", fill=GLASS, stroke=NONE, opacity=22)
    # faint sheen sweeping the panel so the membrane catches light
    c0, c1 = ins[2], ins[6]
    d.path(f"M{c0[0]:.1f},{c0[1]:.1f} Q{(c0[0]+c1[0])/2:.1f},{(c0[1]+c1[1])/2 - 12:.1f} "
           f"{c1[0]:.1f},{c1[1]:.1f}", f"{name} sheen", fill=NONE,
           stroke="#FFFFFF", strokeWidth=9, opacity=14, cap="round")
    # umber border: compound path, outline + reversed inset leaves the window
    d.path(smooth(o) + " " + smooth(list(reversed(ins))), f"{name} border",
           fill=BORDER_FILL, stroke=INK, strokeWidth=3, opacity=96, join="round")
    # veins inside the glass, kept quiet
    for j, (start, k) in enumerate(veins):
        a = sc(start)
        if flip:
            a = mir(a)
        b = o[k]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        bx, by = (mx - cx) * 0.06, (my - cy) * 0.06
        d.path(f"M{a[0]:.1f},{a[1]:.1f} Q{mx + bx:.1f},{my + by:.1f} {b[0]:.1f},{b[1]:.1f}",
               f"{name} vein {j+1}", fill=NONE, stroke="#2A1A10",
               strokeWidth=3, cap="round", opacity=50)
    if extras:
        extras(o, ins, flip)


def fw_extras(o, ins, flip):
    """Greta oto tells: pale subapical band across the dark apex, small dark
    dash closing the discal cell inside the glass."""
    sd = "L" if flip else "R"
    # the cream band slices the apical border between outline pts 5 and 7
    a, b = o[5], o[7]
    ia, ib = ins[5], ins[7]
    band = [(a[0] * 0.72 + ia[0] * 0.28, a[1] * 0.72 + ia[1] * 0.28),
            (b[0] * 0.72 + ib[0] * 0.28, b[1] * 0.72 + ib[1] * 0.28),
            (b[0] * 0.30 + ib[0] * 0.70, b[1] * 0.30 + ib[1] * 0.70),
            (a[0] * 0.30 + ia[0] * 0.70, a[1] * 0.30 + ia[1] * 0.70)]
    d.path(smooth(band), f"Apical band {sd}", fill=PALE, stroke=NONE, opacity=90)
    # discal cell bar: short dark stroke inside the panel near the costa
    p0, p1 = sc((622, 316)), sc((652, 330))
    if flip:
        p0, p1 = mir(p0), mir(p1)
    d.path(f"M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}", f"Cell bar {sd}",
           fill=NONE, stroke="#2A1A10", strokeWidth=5, cap="round", opacity=80)


def hw_extras(o, ins, flip):
    """Pale marginal thread running the inside of the hindwing border."""
    sd = "L" if flip else "R"
    seg = ins[4:10]
    d.path(smooth(seg, closed=False), f"Margin thread {sd}", fill=NONE,
           stroke=PALE, strokeWidth=3, opacity=45, cap="round")


for flip in (False, True):
    sd = "L" if flip else "R"
    wing(f"Hind wing {sd}", HW, HW_D, HW_VEINS, flip, hw_extras)
for flip in (False, True):
    sd = "L" if flip else "R"
    wing(f"Fore wing {sd}", FW, FW_D, FW_VEINS, flip, fw_extras)

# --- body: fuzzy thorax, banded abdomen, small head ---------------------------------------------
ab_a, ab_b = sc((500, 414)), sc((500, 598))
d.path(f"M{ab_a[0]-15:.1f},{ab_a[1]:.1f} C{ab_a[0]-17:.1f},{ab_a[1]+58:.1f} "
       f"{ab_b[0]-9:.1f},{ab_b[1]-38:.1f} {ab_b[0]:.1f},{ab_b[1]:.1f} "
       f"C{ab_b[0]+9:.1f},{ab_b[1]-38:.1f} {ab_a[0]+17:.1f},{ab_a[1]+58:.1f} "
       f"{ab_a[0]+15:.1f},{ab_a[1]:.1f} Z",
       "Abdomen", fill=BODY, stroke=INK, strokeWidth=3)
for i in range(6):
    y = 436 + i * 24
    w = 13 - i * 1.5
    p0, p1 = sc((500 - w, y)), sc((500 + w, y))
    d.path(f"M{p0[0]:.1f},{p0[1]:.1f} Q{(p0[0]+p1[0])/2:.1f},{p0[1]+5:.1f} {p1[0]:.1f},{p1[1]:.1f}",
           f"Abdomen ring {i+1}", fill=NONE, stroke="#8C7A6A", strokeWidth=3,
           opacity=35, cap="round")
th = [(500, 330), (524, 336), (530, 372), (524, 410), (500, 418),
      (476, 410), (470, 372), (476, 336)]
th = [sc(p) for p in th]
d.path(smooth(th), "Thorax", fill=BODY, stroke=INK, strokeWidth=3)
for i, (dx, dy) in enumerate([(-11, -18), (11, -18), (-14, 2), (14, 2), (-9, 20), (9, 20)]):
    spot(f"Thorax dot {i+1}", sc((500 + dx, 372 + dy)), 5, 5, PALE, 80)
h = [sc((500, 306)), sc((516, 310)), sc((518, 324)), sc((500, 332)),
     sc((482, 324)), sc((484, 310))]
d.path(smooth(h), "Head", fill=BODY, stroke=INK, strokeWidth=3)
for sd, dx in (("L", -10), ("R", 10)):
    e = sc((500 + dx, 314))
    d.shape("ellipse", f"Eye {sd}", x=round(e[0] - 7, 1), y=round(e[1] - 7, 1),
            width=14, height=14, fill=rad("#5A4E44", "#1E1610"),
            stroke=INK, strokeWidth=2)
    spot(f"Eye glint {sd}", (e[0] - 2, e[1] - 3), 4, 4, "#FFFFFF", 70)

# --- antennae: slim clubs, spread in a shallow V --------------------------------------------------
ANT = {"L": [sc((492, 300)), sc((462, 246)), sc((428, 196))],
       "R": [sc((508, 300)), sc((542, 244)), sc((586, 198))]}
for nm, pts in ANT.items():
    d.path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" % (pts[0] + pts[1] + pts[2]),
           f"Antenna {nm}", fill=NONE, stroke=INK, strokeWidth=3.5,
           cap="round", join="round")
    tip = pts[2]
    d.shape("ellipse", f"Antenna {nm} club", x=round(tip[0] - 6, 1),
            y=round(tip[1] - 5, 1), width=13, height=9,
            fill=rad("#5A4A3E", "#1E1610"), stroke=INK, strokeWidth=2)

# --- rim drawn last so everything inside closes under it -----------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#33473A", strokeWidth=6)

far = max(math.hypot(x - PCX, y - PCY) for x, y in REACH)
print(f"butterfly reach from disc centre: {far:.0f} (rim 420)")
assert far < 392, far


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
    n = d.text(name, "Name", x=500, y=932, size=58, font="Virelai Sans",
               color="#F0E8D2", justify="center")
    m = d.text(mats, "Second line", x=500, y=970, size=22, font="Virelai Sans",
               color="#B8C8AE", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=80)
    d.cmd("text.setStyle", "Second line tracking", ids=[m["id"]], tracking=300)
    doc = d.m.call("doc_inspect", {})
    for oid, label in ((n["id"], "name"), (m["id"], "second line")):
        b = find(doc, oid)
        nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
                   min(max(PCY, b["y"]), b["y"] + b["height"]))
        clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
        print("%s: %.0fx%.0f at y %.0f, clears rim by %.1f" %
              (label, b["width"], b["height"], b["y"], clear))
        assert clear > 0 and b["x"] >= 10 and b["x"] + b["width"] <= 990, label
        if label == "second line":
            assert b["width"] <= 760, b["width"]


caption("GLASSWING", "LEPIDOPTERA")
d.finish("glasswing-butterfly-V1R00")
