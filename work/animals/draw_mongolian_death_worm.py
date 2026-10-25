#!/usr/bin/env python3
"""Mongolian death worm — field plate V1R00. Olgoi-khorkhoi, two feet of
alleged lightning under the Gobi: a fat blunt-bodied worm reared out of a
disturbed sand mound on a dusk dune field, body ringed and wet-sheened,
two faint static sparks off the blunt head — the legend, not a zoological
claim. Dune plate, don't-dig mood.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Mongolian Death Worm — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A120C"   # warm dark, not black
EXTENT = []


def ext(pts):
    EXTENT.extend(pts)


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


def cubic(p0, p1, p2, p3, n=32):
    return [tuple((1 - t) ** 3 * p0[k] + 3 * (1 - t) ** 2 * t * p1[k] +
                  3 * (1 - t) * t * t * p2[k] + t ** 3 * p3[k] for k in (0, 1))
            for t in [i / n for i in range(n + 1)]]


def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(cx - rx, 1), y=round(cy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)


# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#140D0C"), (1, "#080404")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#8A5A34", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin((0, 40), (0, 880), (0, "#3A2418"), (0.5, "#5E3420"),
                 (0.8, "#2E1A12"), (1, "#140C08")),
        stroke="#0C0604", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.72, "#000000", 0), (1, "#0A0504", 0.55)),
        stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D4B8", strokeWidth=3, opacity=28)

# low ember sun settling on the horizon, half-veiled
d.shape("ellipse", "Sun glow", x=240, y=400, width=380, height=260,
        fill=rad((0, "#D8803A", 30), (0.55, "#A85428", 10), (1, "#A85428", 0)),
        stroke=NONE)
d.shape("ellipse", "Sun disc", x=365, y=480, width=130, height=130,
        fill=rad((0, "#E89A50", 75), (0.7, "#C06A30", 50), (1, "#A85428", 0)),
        stroke=NONE)

# --- dune field: sand below the y=648 chord, closing on the rim arc -------------------
ch = 648
hch = math.sqrt(PR ** 2 - (ch - PCY) ** 2)
d.path(f"M{PCX - hch:.1f},{ch} L{PCX + hch:.1f},{ch} A{PR},{PR} 0 0 1 {PCX - hch:.1f},{ch} Z",
       "Dune field", fill=lin((0, ch), (0, 880), (0, "#A8703E"), (0.45, "#6E4424"),
                              (1, "#2E1A0E")), stroke=NONE)
line_l = PCX - hch
# horizon seam light
d.path(f"M{line_l + 36:.0f},{ch + 1} L{PCX + hch - 36:.0f},{ch + 1}", "Horizon seam",
       fill=NONE, stroke="#D8A86A", strokeWidth=2, opacity=30, cap="round")
# dune ridges: long curves sweeping down-left, catching the low sun on their crests
for i, (y0, x0, cx, cy, x1, y1, op) in enumerate([
        (706, 240, 450, 686, 700, 724, 34), (776, 240, 460, 752, 750, 778, 26),
        (828, 300, 520, 806, 700, 830, 18)]):
    d.path(f"M{x0},{y0} Q{cx},{cy} {x1},{y1}", f"Dune ridge {i+1}", fill=NONE,
           stroke="#D8A86A", strokeWidth=5, opacity=op, cap="round")
# wind-combed ripple strokes between the ridges
for i, (x, y, w) in enumerate([(300, 730, 60), (470, 742, 76), (620, 748, 66),
                               (380, 790, 84), (560, 800, 92), (655, 806, 80),
                               (330, 838, 64), (500, 848, 88)]):
    d.path(f"M{x},{y} Q{x + w / 2},{y - 4} {x + w},{y}", f"Wind ripple {i+1}",
           fill=NONE, stroke="#B8875A", strokeWidth=3, opacity=22, cap="round")

# --- the dig: a disturbed mound the worm is climbing out of ---------------------------
ell("Dig shadow", 592, 700, 165, 30, fill=rad((0, "#120804", 60), (1, "#120804", 0)),
    stroke=NONE)
d.path(smooth([(470, 700), (505, 662), (560, 646), (625, 650), (680, 664),
               (715, 694), (700, 712), (640, 724), (560, 726), (495, 716)]),
       "Sand mound", fill=lin((0, 646), (0, 726), (0, "#8A5A30"), (1, "#3E2414")),
       stroke="#241205", strokeWidth=3, join="round")
# scattered clods kicked out of the hole
for i, (x, y, w, op) in enumerate([(505, 668, 12, 60), (672, 682, 14, 55),
                                   (610, 656, 10, 50), (462, 694, 10, 45),
                                   (700, 702, 11, 40), (545, 716, 9, 45)]):
    ell(f"Sand clod {i+1}", x, y, w, w * 0.6, fill="#4A2C14", opacity=op, stroke=NONE)
# the hole the worm comes out of — dark mouth at the mound crest
ell("Burrow mouth", 596, 672, 62, 22,
    fill=rad((0, "#0C0503", 95), (0.7, "#1E0E06", 85), (1, "#3A2210", 30)),
    stroke=NONE)

# --- the worm -------------------------------------------------------------------------
# spine: out of the mound, S-lean, head hooked left. Fat and blunt both ends.
SPINE = cubic((612, 696), (548, 542), (610, 402), (566, 328), 38)
SPINE += cubic(SPINE[-1], (540, 268), (470, 260), (430, 296), 16)[1:]


def ribbon(spine, w0, w1):
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
    return left, right


LEFT, RIGHT = ribbon(SPINE, 44, 30)
body_pts = LEFT + RIGHT[::-1]
ext(body_pts)
d.path(smooth(body_pts), "Worm body",
       fill=lin((SPINE[0][0], 0), (SPINE[-1][0], 0),
                (0, "#6E2418"), (0.35, "#A03824"), (0.62, "#C05232"), (1, "#8E2E1C")),
       stroke=INK, strokeWidth=3, join="round")

# segment rings: curved chords across the ribbon, spacing widens toward the head
n = len(SPINE)
for j, t in enumerate([i / 15 for i in range(1, 15)]):
    i = min(n - 1, int(t * (n - 1)))
    p = SPINE[i]
    q0, q1 = SPINE[max(0, i - 1)], SPINE[min(n - 1, i + 1)]
    tx, ty = q1[0] - q0[0], q1[1] - q0[1]
    L = math.hypot(tx, ty) or 1
    nx, ny = -ty / L, tx / L
    w = 44 + (30 - 44) * i / (n - 1)
    a = (p[0] + nx * w * 0.92, p[1] + ny * w * 0.92)
    b = (p[0] - nx * w * 0.92, p[1] - ny * w * 0.92)
    # rings bow toward the tail end, like wrinkles around the curve
    mx, my = (a[0] + b[0]) / 2 + tx / L * w * 0.18, (a[1] + b[1]) / 2 + ty / L * w * 0.18
    d.path(f"M{a[0]:.1f},{a[1]:.1f} Q{mx:.1f},{my:.1f} {b[0]:.1f},{b[1]:.1f}",
           f"Ring {j+1}", fill=NONE, stroke="#4A140C", strokeWidth=4.5,
           opacity=42, cap="round")

# moist sheen along the lit side
sh0, sh1 = SPINE[int(n * 0.15)], SPINE[int(n * 0.85)]
d.path(f"M{sh0[0] + 10:.1f},{sh0[1]:.1f} Q{(sh0[0] + sh1[0]) / 2 + 26:.1f},"
       f"{(sh0[1] + sh1[1]) / 2:.1f} {sh1[0] + 12:.1f},{sh1[1]:.1f}",
       "Body sheen", fill=NONE, stroke="#F0A880", strokeWidth=9,
       opacity=26, cap="round")
# belly shade down the shadow side
bt0, bt1 = SPINE[int(n * 0.08)], SPINE[int(n * 0.7)]
d.path(f"M{bt0[0] - 14:.1f},{bt0[1]:.1f} Q{(bt0[0] + bt1[0]) / 2 - 24:.1f},"
       f"{(bt0[1] + bt1[1]) / 2:.1f} {bt1[0] - 12:.1f},{bt1[1]:.1f}",
       "Belly shade", fill=NONE, stroke="#3A0E08", strokeWidth=11,
       opacity=32, cap="round")

# blunt head: a small dark mouth slit at the tip, no eyes — it is a worm
tip = SPINE[-1]
tq0, tq1 = SPINE[-4], SPINE[-1]
ttx, tty = tq1[0] - tq0[0], tq1[1] - tq0[1]
tl = math.hypot(ttx, tty) or 1
ttx, tty = ttx / tl, tty / tl
nx, ny = -tty, ttx
m0 = (tip[0] - nx * 7, tip[1] - ny * 7)
m1 = (tip[0] + nx * 7, tip[1] + ny * 7)
d.path(f"M{m0[0]:.1f},{m0[1]:.1f} L{m1[0]:.1f},{m1[1]:.1f}", "Mouth",
       fill=NONE, stroke="#1E0A06", strokeWidth=4, cap="round", opacity=70)

# sand grains clinging to the wet skin just above the burrow mouth
for i, (p, s) in enumerate([(SPINE[4], 6), (SPINE[8], 5), (SPINE[12], 7),
                            (SPINE[16], 5)]):
    ell(f"Clinging sand {i+1}", p[0] - 16, p[1] + 4, s, s * 0.7,
        fill="#3E2414", opacity=55, stroke=NONE)

# the alleged lightning: two faint crackles hugging the head, never antennae
for i, pts in enumerate([[(tip[0] - 18, tip[1] - 2), (tip[0] - 34, tip[1] - 14),
                          (tip[0] - 42, tip[1] - 6), (tip[0] - 54, tip[1] - 20)],
                         [(tip[0] - 4, tip[1] - 16), (tip[0] + 8, tip[1] - 32),
                          (tip[0] + 2, tip[1] - 42), (tip[0] + 12, tip[1] - 54)]]):
    s = "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:])
    d.path(s, f"Static spark {i+1}", fill=NONE, stroke="#F0C878",
           strokeWidth=3, cap="round", join="round", opacity=40)
    ext(pts)

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("death worm extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
    n = d.text(name, "Name", x=500, y=932, size=44, font="Virelai Sans",
               color="#F0E2CC", justify="center")
    m = d.text(mats, "Second line", x=500, y=968, size=22, font="Virelai Sans",
               color="#C8A888", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=40)
    d.cmd("text.setStyle", "Second line tracking", ids=[m["id"]], tracking=240)
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


caption("MONGOLIAN DEATH WORM", "OLGOI-KHORKHOI · GOBI")
d.finish("mongolian-death-worm-V1R00")
