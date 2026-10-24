#!/usr/bin/env python3
"""Slipper chair — furniture field plate V1R00. Front-near view with a slight
three-quarter: a low, armless boudoir chair — tall shield back easing into a
deep seat, button-tufted teal velvet, a welted apron, short turned mahogany
legs on brass casters. Deep plum plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Slipper Chair — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#331222"   # warm dark aubergine, not black
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


# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1A1018"), (1, "#0A0609")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#6E5468", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#50384A"), (0.6, "#362632"), (1, "#1E141C")),
        stroke="#100A0F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DACAD6", strokeWidth=3, opacity=24)
d.shape("ellipse", "Back glow", x=210, y=150, width=540, height=540,
        fill=rad((0, "#E8B0C0", 16), (0.6, "#A06878", 5), (1, "#6E4654", 0)), stroke=NONE)

FY = 706
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#584452", 34), (1, "#140D13", 70)), stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#E0D2DC", strokeWidth=2, opacity=18)

# --- chair parametrics --------------------------------------------------------
# Back: u across [0..1], v down [0..1]; arched crest, sides tapering to the seat.
def back(u, v):
    ax = abs(2 * u - 1)
    y_top = 182 + 40 * ax ** 1.7          # crest rises in the middle
    y_bot = 542 + 18 * (1 - ax ** 2)      # seat line sags toward centre
    half = 116 - 26 * v + 10 * math.sin(math.pi * v)
    x = 500 + (u * 2 - 1) * half
    return (x, y_top + (y_bot - y_top) * v)


def back_top(u):
    return back(u, 0)


def back_side(u, v):
    """Right-hand side face of the back, peeled off toward the viewer."""
    x, y = back(u, v)
    return (x + 30 * u ** 1.6, y + 10 * u)


# --- shadow ---------------------------------------------------------------------
d.shape("ellipse", "Chair shadow", x=270, y=660, width=470, height=54,
        fill=rad((0, "#060409", 64), (0.6, "#060409", 28), (1, "#060409", 0)), stroke=NONE)

# --- legs -------------------------------------------------------------------------
WOOD = ((0, "#6E4428"), (0.3, "#9A6A44"), (0.5, "#4A2A16"), (0.78, "#623C22"), (1, "#2C170C"))


def leg(cx, y_top, y_foot, scale, name, dark=False):
    """Short turned leg: collar bead, tapered shaft, bun foot, brass caster."""
    prof = [(0, 10), (10, 10), (14, 13), (20, 13), (24, 8), (44, 5.5),
            (56, 5), (62, 10), (70, 10), (74, 6)]
    L = y_foot - y_top - 12
    s = L / 74.0 * scale
    right = [(cx + w * scale, y_top + dy * s) for dy, w in prof]
    left = [(cx - w * scale, y_top + dy * s) for dy, w in reversed(prof)]
    d.path(smooth(right + left, closed=True), f"Leg {name}",
           fill=lin((cx - 11 * scale, 0), (cx + 11 * scale, 0), *WOOD),
           stroke="#241208", strokeWidth=2.5, join="round",
           opacity=66 if dark else 100)
    ring_y = y_top + 18 * s
    d.path(f"M{cx - 10 * scale:.1f},{ring_y:.1f} L{cx + 10 * scale:.1f},{ring_y:.1f}",
           f"Leg {name} bead", fill=NONE, stroke="#241208", strokeWidth=2, opacity=45)
    cy = y_foot - 5
    d.shape("ellipse", f"Caster cup {name}", x=round(cx - 7), y=round(cy - 10), width=14, height=11,
            fill=rad((0, "#F0D088"), (0.6, "#A87828"), (1, "#5C3C10")),
            stroke="#241208", strokeWidth=1.5, opacity=66 if dark else 100)
    d.shape("ellipse", f"Caster wheel {name}", x=round(cx - 8), y=round(cy - 1), width=16, height=8,
            fill=rad((0, "#3A2C20"), (1, "#120E0A")), stroke="#241208", strokeWidth=1.5,
            opacity=66 if dark else 100)
    EXTENT.append((cx, y_foot))


# far legs first, then the near pair
leg(398, 596, 690, 0.88, "far L", dark=True)
leg(622, 596, 690, 0.88, "far R", dark=True)
leg(372, 606, 698, 1.0, "L")
leg(646, 606, 698, 1.0, "R")

# --- seat + apron -------------------------------------------------------------------
# apron: upholstered rail under the cushion, drawn before the seat
apron_top = [(352, 592), (430, 606), (560, 606), (652, 592)]
apron_bot = [(358, 646), (430, 656), (560, 656), (646, 646)]
apron = apron_top + apron_bot[::-1]
d.path(smooth(apron, closed=True), "Apron",
       fill=lin((0, 590), (0, 658), (0, "#2E5848"), (0.6, "#1E3C30"), (1, "#12241C")),
       stroke=INK, strokeWidth=4, join="round")
EXTENT += apron
d.path(smooth(apron_bot), "Apron welt", fill=NONE, stroke="#0E1C16",
       strokeWidth=4, cap="round", opacity=80)

# seat cushion: deep and plump, overhanging the apron
seat_top = [(344, 556), (420, 546), (500, 544), (580, 546), (660, 558)]
seat_bot = [(340, 596), (420, 616), (500, 620), (580, 616), (664, 598)]
seat = seat_top + seat_bot[::-1]
d.path(smooth(seat, closed=True), "Seat cushion",
       fill=lin((0, 540), (0, 622), (0, "#7FB49A"), (0.45, "#4E8068"), (1, "#26483A")),
       stroke=INK, strokeWidth=4.5, join="round")
EXTENT += seat
# crown light along the cushion top
crown = [seat_top[0], seat_top[1], seat_top[2], seat_top[3], seat_top[4],
         (580, 566), (500, 564), (420, 566)]
d.path(smooth(crown, closed=True), "Seat crown light",
       fill=lin((0, 540), (0, 578), (0, "#BCDCC8", 50), (1, "#8FBCA2", 0)), stroke=NONE)
# cushion welt cord
d.path(smooth(seat_top), "Seat top welt", fill=NONE, stroke="#16302A",
       strokeWidth=4, cap="round", opacity=85)
d.path(smooth(seat_bot), "Seat bottom welt", fill=NONE, stroke="#16302A",
       strokeWidth=3.5, cap="round", opacity=70)
# a soft compression crease where cushion meets back
d.path("M386,560 C430,576 570,576 618,560", "Seat back crease", fill=NONE,
       stroke="#14281F", strokeWidth=5, cap="round", opacity=45)

# --- back: side face first, then the front -------------------------------------------
side_pts = [back_side(u, v) for u, v in
            [(0.55, 0), (0.8, 0), (1, 0), (1, 0.4), (1, 0.8), (1, 1),
             (0.82, 1), (0.82, 0.5), (0.55, 0.06)]]
d.path(smooth(side_pts, closed=True), "Back side face",
       fill=lin((0, 190), (0, 560), (0, "#3E6856"), (0.6, "#27483A"), (1, "#16281F")),
       stroke=INK, strokeWidth=4, join="round")
EXTENT += side_pts

front = [back(u, 0) for u in [i / 24 for i in range(25)]] + \
        [back(1, v) for v in (0.2, 0.4, 0.6, 0.8)] + \
        [back(u, 1) for u in [i / 24 for i in range(24, -1, -1)]] + \
        [back(0, v) for v in (0.8, 0.6, 0.4, 0.2)]
d.path(smooth(front, closed=True), "Back front",
       fill=lin((0, 180), (0, 560), (0, "#86BAA0"), (0.4, "#548672"), (0.75, "#356052"), (1, "#1E3A2E")),
       stroke=INK, strokeWidth=5, join="round")
EXTENT += front

# crest roll: a padded band just inside the top edge, ends tucked in
US_C = [0.03 + 0.94 * i / 24 for i in range(25)]
crest = [back(u, 0) for u in US_C]
crest_lo = [(x, y + 26 - 8 * abs(2 * u - 1)) for u, (x, y) in zip(US_C, crest)]
d.path(smooth(crest + crest_lo[::-1], closed=True), "Crest roll",
       fill=lin((0, 176), (0, 240), (0, "#A8D2BC"), (0.6, "#6A9A82"), (1, "#3E6856")),
       stroke=NONE)
d.path(smooth(crest), "Crest welt", fill=NONE, stroke="#14302A",
       strokeWidth=4, cap="round", opacity=80)

# --- button tufting ------------------------------------------------------------------
rows = [(0.30, [0.16 + i * 0.17 for i in range(5)]),
        (0.56, [0.075 + i * 0.17 for i in range(6)]),
        (0.80, [0.16 + i * 0.17 for i in range(5)])]
btns = []
for v, us in rows:
    for u in us:
        btns.append(back(u, v))

for (v0, us0), (v1, us1) in zip(rows, rows[1:]):
    for i, u in enumerate(us0[:-1]):
        for u2 in us1[max(0, i - 1):i + 2]:
            a, b = back(u, v0), back(u2, v1)
            d.path(f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}", "Tuft seam",
                   fill=NONE, stroke="#1C3830", strokeWidth=2.2, opacity=32)

for i, (x, y) in enumerate(btns):
    for a in (-2.4, -0.7, 0.7, 2.4):
        L = 13
        dx, dy = math.cos(a) * L, math.sin(a) * L * 0.6
        d.path(f"M{x + dx * 0.5:.1f},{y + dy * 0.5:.1f} L{x + dx:.1f},{y + dy:.1f}",
               f"Crease {i}", fill=NONE, stroke="#1C3830", strokeWidth=2.4,
               cap="round", opacity=38)
    d.shape("ellipse", f"Button {i}", x=round(x - 5), y=round(y - 4), width=10, height=8,
            fill=rad((0, "#4E8068"), (0.7, "#2A5040"), (1, "#16281F")),
            stroke="#14281F", strokeWidth=1.4)
    d.shape("ellipse", f"Button glint {i}", x=round(x - 2), y=round(y - 3), width=3, height=2.4,
            fill="#C8E4D4", opacity=60, stroke=NONE)

# velvet nap: broad soft sheen up the left of the back
d.path("M430,240 C410,330 408,430 430,510 C452,430 452,330 470,244 C456,240 442,238 430,240 Z",
       "Velvet sheen", fill=rad((0, "#C8E8D6", 26), (1, "#C8E8D6", 0)), stroke=NONE)

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("slipper extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 28, far


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
    n = d.text(name, "Name", x=500, y=934, size=56, font="Virelai Sans",
               color="#F0E2EA", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#BAA6B2", justify="center")
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


caption("SLIPPER CHAIR", "MAHOGANY · VELVET · BRASS")
d.finish("slipper-chair-V1R00")
