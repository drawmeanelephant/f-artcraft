#!/usr/bin/env python3
"""Loveseat — furniture field plate V1R00. Front-near view of a small parlor
settee: arched upholstered back with a carved rosewood crest, two plump back
cushions, two seat cushions with a centre seam, scrolled arms and short
turned rosewood legs on brass casters. Peacock velvet with gimp piping and
brass nailheads against a warm plum plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Loveseat — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#22180F"   # warm umber, never black
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


# --- palette ----------------------------------------------------------------------
VEL_HI, VEL_MID, VEL_LO = "#8AD2C2", "#4B9C8E", "#22544C"
VEL_DARK, VEL_CREASE = "#163B35", "#0F2A25"
PIPE = "#12332E"

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#1B1A20"), (1, "#0B090D")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#5C5258", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad((0, "#4E4248"), (0.6, "#362B32"), (1, "#1E181D")),
        stroke="#120D11", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C8D0", strokeWidth=3, opacity=22)
d.shape("ellipse", "Warm glow", x=190, y=150, width=540, height=520,
        fill=rad((0, "#E8B070", 14), (0.6, "#A06848", 5), (1, "#704038", 0)), stroke=NONE)

FY = 706
hx = math.sqrt(PR ** 2 - (FY - PCY) ** 2)
d.path(f"M{PCX - hx:.1f},{FY} L{PCX + hx:.1f},{FY} A420,420 0 0 1 {PCX - hx:.1f},{FY} Z",
       "Floor", fill=lin((0, FY), (0, 880), (0, "#514754", 34), (1, "#141016", 70)), stroke=NONE)
d.path(f"M{PCX - hx + 6:.1f},{FY} L{PCX + hx - 6:.1f},{FY}", "Floor edge light",
       fill=NONE, stroke="#DCCEDA", strokeWidth=2, opacity=18)

# --- rear legs (peek out under the rail, mostly shadow) -----------------------------
WOOD = ((0, "#6E3F2C"), (0.3, "#9A6242"), (0.5, "#3F2114"), (0.78, "#57321E"), (1, "#2A140C"))
BRASS = rad((0, "#F4D890"), (0.6, "#A87828"), (1, "#5C3C10"))


def leg(cx, y_top, y_foot, scale, name, dark=False):
    """Turned leg: collar, tapered shaft, foot bulb, brass caster."""
    prof = [(0, 9), (14, 9), (18, 12), (26, 12), (30, 8), (58, 5.5),
            (74, 5), (82, 11), (92, 11), (96, 6)]
    L = y_foot - y_top - 14
    s = L / 96.0 * scale
    right = [(cx + w * scale, y_top + dy * s) for dy, w in prof]
    left = [(cx - w * scale, y_top + dy * s) for dy, w in reversed(prof)]
    d.path(smooth(right + left, closed=True), f"Leg {name}",
           fill=lin((cx - 12 * scale, 0), (cx + 12 * scale, 0), *WOOD),
           stroke="#1E0E08", strokeWidth=2.5, join="round",
           opacity=62 if dark else 100)
    cy = y_foot - 6
    d.shape("ellipse", f"Caster cup {name}", x=round(cx - 8), y=round(cy - 12), width=16, height=12,
            fill=BRASS, stroke="#1E0E08", strokeWidth=1.6, opacity=62 if dark else 100)
    d.shape("ellipse", f"Caster wheel {name}", x=round(cx - 9), y=round(cy - 2), width=18, height=9,
            fill=rad((0, "#3A2C20"), (1, "#14100C")), stroke="#1E0E08", strokeWidth=1.6,
            opacity=62 if dark else 100)
    EXTENT.extend([(cx, y_foot), (cx - 12 * scale, y_top), (cx + 12 * scale, y_top)])


leg(392, 606, 694, 0.9, "rear L", dark=True)
leg(608, 606, 694, 0.9, "rear R", dark=True)

# --- shadow ------------------------------------------------------------------------
d.shape("ellipse", "Settee shadow", x=206, y=660, width=590, height=58,
        fill=rad((0, "#050308", 62), (0.6, "#050308", 28), (1, "#050308", 0)), stroke=NONE)

# --- back panel: arched upholstered back, mostly hidden behind cushions -------------
BACK = [(292, 560), (286, 480), (296, 428), (356, 388), (430, 362), (500, 352),
        (570, 362), (644, 388), (704, 428), (714, 480), (708, 560)]
back_pts = [smooth(BACK)]
d.path(back_pts[0] + " L708,560 L292,560 Z", "Back panel",
       fill=lin((0, 355), (0, 560), (0, "#5FB4A4"), (0.45, "#3A8478"), (1, "#1E4A44")),
       stroke=INK, strokeWidth=5, join="round")
EXTENT += BACK
# arch piping follows the top edge
d.path(smooth(BACK[1:10]), "Back arch piping", fill=NONE, stroke=PIPE, strokeWidth=5, cap="round")
# soft light pooling on the upper left of the arch
d.shape("ellipse", "Back panel light", x=330, y=375, width=260, height=110,
        fill=rad((0, "#A8E4D6", 40), (1, "#A8E4D6", 0)), stroke=NONE)
# side shade where the arms throw the panel into shadow
d.shape("ellipse", "Back shade L", x=288, y=430, width=90, height=150,
        fill=rad((0, "#0E2622", 55), (1, "#0E2622", 0)), stroke=NONE)
d.shape("ellipse", "Back shade R", x=622, y=430, width=90, height=150,
        fill=rad((0, "#0E2622", 60), (1, "#0E2622", 0)), stroke=NONE)
# stitched channels fanning up the visible arch
for i, (u0, u1) in enumerate([(0.28, 0.38), (0.46, 0.50), (0.64, 0.72)]):
    a = BACK[1][0] + (BACK[9][0] - BACK[1][0]) * u0
    b = BACK[1][0] + (BACK[9][0] - BACK[1][0]) * u1
    d.path(f"M{a:.0f},470 C{a + 8:.0f},430 {b - 8:.0f},410 {b:.0f},382",
           f"Back channel {i+1}", fill=NONE, stroke=PIPE, strokeWidth=3, opacity=35, cap="round")

# --- carved crest: rosewood medallion astride the arch -------------------------------
d.shape("ellipse", "Crest", x=466, y=330, width=68, height=48,
        fill=lin((466, 330), (534, 378), *WOOD), stroke="#1E0E08", strokeWidth=3)
d.shape("ellipse", "Crest inset", x=478, y=338, width=44, height=32,
        fill=rad((0, "#8A5336"), (1, "#3C1E10")), stroke="#1E0E08", strokeWidth=2)
d.path("M500,344 C492,350 492,360 500,364 C508,360 508,350 500,344 Z", "Crest carve",
       fill="#2A140C", opacity=65, stroke=NONE)
for sgn in (-1, 1):
    d.path(f"M{500 + sgn * 34},352 C{500 + sgn * 46},348 {500 + sgn * 52},354 {500 + sgn * 56},362",
           f"Crest leaf {'L' if sgn < 0 else 'R'}", fill=NONE, stroke="#1E0E08",
           strokeWidth=5, cap="round")
EXTENT += [(466, 330), (534, 378)]

# --- arm bodies: upholstered columns the scrolls sit on -------------------------------
def arm_body(sgn):
    """sgn -1 left arm, +1 right arm."""
    xo, xi = (228, 330) if sgn < 0 else (772, 670)
    pts = [(xo + 6, 440), (xo + 2, 500), (xo + 8, 575), (xo + 22, 666),
           (xi - 18, 666), (xi - 2, 575), (xi + 2, 500), (xi - 2, 440)]
    d.path(smooth(pts, closed=True), f"Arm body {'L' if sgn < 0 else 'R'}",
           fill=lin((xo, 0), (xi, 0), (0, "#3E887B"), (0.55, "#2A675E"), (1, "#163B35")),
           stroke=INK, strokeWidth=4.5, join="round")
    EXTENT.extend(pts)
    # inside face sliver catching light between scroll and cushion
    inn = [(xi - 2, 448), (xi + 2, 505), (xi - 4, 570), (xi - 16, 616),
           (xi - 30, 612), (xi - 20, 545), (xi - 22, 490)]
    lit = sgn < 0
    d.path(smooth(inn, closed=True), f"Arm inner {'L' if sgn < 0 else 'R'}",
           fill=lin((xi - 30, 0), (xi, 0), (0, "#5FB4A4" if lit else "#2A675E"),
                    (1, "#3A8478" if lit else "#1E4A44")),
           stroke=INK, strokeWidth=3, join="round", opacity=96)


arm_body(-1)
arm_body(1)

# --- back cushions: two plump pillows ------------------------------------------------
def back_cushion(x0, x1, label, lean):
    """Plump pillow from y~414 to ~566, crowned top, squashed bottom."""
    cx = (x0 + x1) / 2
    pts = [(x0 + 6, 548), (x0 + 2, 480), (x0 + 14, 432), (x0 + 52, 414 + lean),
           (cx, 408 + lean), (x1 - 52, 414 + lean), (x1 - 14, 432), (x1 - 2, 480),
           (x1 - 6, 548), (x1 - 30, 560), (cx, 566), (x0 + 30, 560)]
    d.path(smooth(pts, closed=True), label,
           fill=lin((0, 410), (0, 566), (0, VEL_HI), (0.5, VEL_MID), (1, VEL_LO)),
           stroke=INK, strokeWidth=4, join="round")
    EXTENT.extend(pts)
    # crown sheen along the top
    top = pts[1:7]
    d.path(smooth([(x, y + 10) for x, y in top]), label + " sheen",
           fill=NONE, stroke="#C4EFE4", strokeWidth=7, cap="round", opacity=32)
    # piping along the outer edge
    d.path(smooth([pts[2], pts[3], pts[4], pts[5], pts[6]]), label + " piping",
           fill=NONE, stroke=PIPE, strokeWidth=3.5, cap="round", opacity=75)
    # small dimpled gather where the pillow meets the seat
    d.shape("ellipse", label + " gather", x=round(cx - 34), y=548, width=68, height=14,
            fill=rad((0, VEL_DARK, 55), (1, VEL_DARK, 0)), stroke=NONE)


back_cushion(340, 502, "Back cushion L", -6)
back_cushion(498, 660, "Back cushion R", 0)
# centre slit shadow between the pillows
d.path("M500,430 C496,480 496,520 501,556", "Back cushion gap",
       fill=NONE, stroke=VEL_CREASE, strokeWidth=6, cap="round", opacity=70)

# --- seat cushions: two crowned pads --------------------------------------------------
def seat_cushion(x0, x1, label):
    pts = [(x0 + 4, 558), (x0 + 26, 540), (x0 + 78, 530), ((x0 + x1) / 2, 528),
           (x1 - 78, 530), (x1 - 26, 540), (x1 - 4, 558), (x1 - 8, 600),
           (x1 - 16, 626), ((x0 + x1) / 2, 632), (x0 + 16, 626), (x0 + 8, 600)]
    d.path(smooth(pts, closed=True), label,
           fill=lin((0, 528), (0, 632), (0, "#7CC8B8"), (0.45, VEL_MID), (1, "#1E4A44")),
           stroke=INK, strokeWidth=4, join="round")
    EXTENT.extend(pts)
    # crown light band hugging the top edge
    d.path(smooth([(x, y + 9) for x, y in pts[1:6]]), label + " crown",
           fill=NONE, stroke="#C4EFE4", strokeWidth=8, cap="round", opacity=38)
    # front piping along the bottom edge
    d.path(smooth([pts[10], pts[9], pts[8]]), label + " piping",
           fill=NONE, stroke=PIPE, strokeWidth=3.5, cap="round", opacity=80)


seat_cushion(330, 502, "Seat cushion L")
seat_cushion(498, 670, "Seat cushion R")
# centre seam: shadow under the join plus a piping pair
d.path("M501,540 C498,575 499,606 502,628", "Seat centre seam",
       fill=NONE, stroke=VEL_CREASE, strokeWidth=5, cap="round", opacity=75)
# deck shadow between back cushions and seat cushions
d.shape("ellipse", "Seat deck shade", x=330, y=540, width=340, height=26,
        fill=rad((0, VEL_DARK, 60), (1, VEL_DARK, 0)), stroke=NONE)

# --- front rail ----------------------------------------------------------------------
d.path("M296,606 L704,606 Q714,606 714,616 L714,648 Q714,666 696,668 "
       "L304,668 Q286,666 286,648 L286,616 Q286,606 296,606 Z", "Front rail",
       fill=lin((0, 604), (0, 664), (0, "#469587"), (0.5, "#2A675E"), (1, "#122E2A")),
       stroke=INK, strokeWidth=4.5, join="round")
# gimp braid along the rail's top edge
d.path("M296,612 L704,612", "Rail gimp", fill=NONE, stroke=PIPE, strokeWidth=4, cap="round")
d.path("M296,610 L704,610", "Rail gimp light", fill=NONE, stroke="#7CC8B8",
       strokeWidth=1.8, cap="round", opacity=50)
# brass nailheads under the gimp
for i in range(17):
    x = 310 + i * 23.6
    d.shape("ellipse", f"Rail nail {i+1}", x=round(x - 3), y=618, width=6.4, height=6.4,
            fill=BRASS, stroke="#1E0E08", strokeWidth=1)

# --- front legs ----------------------------------------------------------------------
leg(332, 630, 700, 1.0, "front L")
leg(668, 630, 700, 1.0, "front R")

# --- arm scrolls ----------------------------------------------------------------------
def scroll(cx, cy, r, label, lit):
    d.shape("ellipse", label, x=round(cx - r), y=round(cy - r * 0.94), width=round(2 * r),
            height=round(2 * r * 0.94),
            fill=rad((0, "#8AD2C2" if lit else "#5FB4A4"), (0.55, "#4FA496"), (1, "#1E4A44")),
            stroke=INK, strokeWidth=5)
    EXTENT.extend([(cx - r, cy - r), (cx + r, cy + r)])
    # spiral curl inward
    spir = []
    for k in range(44):
        t = k / 43 * 2.05 * math.pi
        rr = r * (0.78 - 0.66 * (k / 43))
        spir.append((cx + rr * math.cos(t - 0.4), cy + rr * 0.9 * math.sin(t - 0.4)))
    d.path(smooth(spir), label + " spiral", fill=NONE, stroke=PIPE, strokeWidth=4.5,
           cap="round", opacity=80)
    d.path(smooth([(x - 2, y - 3) for x, y in spir]), label + " spiral light",
           fill=NONE, stroke="#B4E8DC", strokeWidth=2, cap="round", opacity=45)
    d.shape("ellipse", label + " eye", x=round(cx - 4), y=round(cy - 4), width=9, height=9,
            fill=rad((0, "#5FB4A4"), (1, "#122E2A")), stroke=INK, strokeWidth=1.5)
    # rim light on the upper edge
    d.path(f"M{cx - r * 0.7:.0f},{cy - r * 0.62:.0f} A{r * 0.92:.0f},{r * 0.86:.0f} 0 0 1 {cx + r * 0.35:.0f},{cy - r * 0.85:.0f}",
           label + " rim light", fill=NONE, stroke="#C4EFE4", strokeWidth=4, cap="round", opacity=50)


scroll(276, 472, 56, "Scroll L", lit=True)
scroll(724, 472, 56, "Scroll R", lit=False)
# where the scrolls meet the seat: compression creases
d.path("M330,470 C340,510 340,560 332,600", "Scroll crease L",
       fill=NONE, stroke=VEL_CREASE, strokeWidth=5, cap="round", opacity=50)
d.path("M670,470 C660,510 660,560 668,600", "Scroll crease R",
       fill=NONE, stroke=VEL_CREASE, strokeWidth=5, cap="round", opacity=50)

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("loveseat extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#EAE2DC", justify="center")
    m = d.text(mats, "Materials", x=500, y=970, size=22, font="Virelai Sans",
               color="#C2AE9C", justify="center")
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


caption("LOVESEAT", "ROSEWOOD · VELVET · BRASS")
d.finish("loveseat-V1R00")
