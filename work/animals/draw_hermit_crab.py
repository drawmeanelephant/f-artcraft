#!/usr/bin/env python3
"""Hermit crab — field plate V1R00. Shoreline plate, borrowed-shell mood:
a Pagurus in a tilted whelk shell lumbering right across wet dusk sand
toward a second, empty shell — house-hunting, forever. Low moon, foam line,
sand chord closing on the disc arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Hermit Crab — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#2A1510"   # warm near-black
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


def ell(name, cx, cy, rx, ry, **kw):
    return d.shape("ellipse", name, x=round(cx - rx, 1), y=round(cy - ry, 1),
                   width=round(2 * rx, 1), height=round(2 * ry, 1), **kw)


def line(name, x0, y0, x1, y1, w, color, **kw):
    return d.path(f"M{x0:.1f},{y0:.1f} L{x1:.1f},{y1:.1f}", name, fill=NONE,
                  stroke=color, strokeWidth=w, cap="round", **kw)


# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#0A161A"), (1, "#04090B")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#5A7A80", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin((0, 40), (0, 880), (0, "#3A5A5E"), (0.5, "#26424A"),
                 (0.78, "#1A2E36"), (1, "#101E24")),
        stroke="#08141A", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.74, "#000000", 0), (1, "#02080C", 0.5)),
        stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C6D4D0", strokeWidth=3, opacity=26)

# low dusk moon + halo over the water
ell("Moon", 700, 218, 34, 34, fill=rad((0, "#F0E8D2"), (0.8, "#D8CCAC"), (1, "#B8A888")), opacity=85, stroke=NONE)
ell("Moon halo", 700, 218, 74, 74, fill=rad((0, "#E8DCB8", 18), (1, "#E8DCB8", 0)), stroke=NONE)
# moon-glade: dashes stepping down the water
for i, (y, w, op) in enumerate([(290, 46, 30), (330, 60, 26), (375, 78, 22),
                                (425, 66, 19), (480, 88, 16), (545, 70, 13)]):
    line(f"Moon glade {i+1}", 700 - w / 2, y, 700 + w / 2, y, 3, "#D8D4BC", opacity=op)

# scattered water shimmer
for i, (x, y, w, op) in enumerate([(250, 300, 80, 16), (400, 240, 70, 14),
                                   (560, 340, 90, 15), (230, 420, 65, 13),
                                   (340, 520, 80, 12), (830, 330, 55, 14)]):
    line(f"Water shimmer {i+1}", x, y, x + w, y, 2.5, "#7A9AA0", opacity=op)

# --- sand: chord closing on the disc arc ----------------------------------------
ch = 676
hch = math.sqrt(PR ** 2 - (ch - PCY) ** 2)
d.path(f"M{PCX - hch:.1f},{ch} L{PCX + hch:.1f},{ch} A{PR},{PR} 0 0 1 {PCX - hch:.1f},{ch} Z",
       "Sand", fill=lin((0, ch), (0, 880), (0, "#6E5840"), (0.55, "#463626"),
                        (1, "#2A2016")), stroke=NONE)
# damp band under the foam — the tide just left
d.path(f"M{PCX - hch + 14:.1f},{ch + 4} Q{PCX},{ch + 26} {PCX + hch - 14:.1f},{ch + 4} "
       f"L{PCX + hch - 30:.1f},{ch + 34} Q{PCX},{ch + 52} {PCX - hch + 30:.1f},{ch + 34} Z",
       "Damp band", fill="#2E2418", opacity=42, stroke=NONE)
# foam line where the wash stopped
d.path(f"M{PCX - hch + 8:.0f},{ch + 2} Q{PCX - 180},{ch - 12} {PCX - 40},{ch - 2} "
       f"Q{PCX + 90},{ch + 8} {PCX + 200},{ch - 4} Q{PCX + 290},{ch - 10} {PCX + hch - 24:.0f},{ch + 2}",
       "Foam line", fill=NONE, stroke="#D4E2DC", strokeWidth=4, opacity=38, cap="round")
d.path(f"M{PCX - hch + 40:.0f},{ch + 20} Q{PCX - 60},{ch + 30} {PCX + 140},{ch + 18} "
       f"Q{PCX + 250},{ch + 10} {PCX + hch - 60:.0f},{ch + 22}",
       "Foam line 2", fill=NONE, stroke="#D4E2DC", strokeWidth=3, opacity=22, cap="round")

# sand pebbles + speckles — all inside the disc
def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

for i, (x, y, rx, ry, op) in enumerate([(250, 720, 12, 7, 50), (330, 770, 8, 5, 42),
                                        (700, 730, 14, 8, 45), (770, 745, 9, 6, 40),
                                        (235, 750, 10, 6, 38), (620, 800, 11, 6, 36)]):
    assert on_disc(x, y, 8), i
    ell(f"Pebble {i+1}", x, y, rx, ry, fill="#241C12", opacity=op, stroke=NONE)
for i, (x, y) in enumerate([(290, 700), (430, 740), (560, 720), (760, 700),
                            (360, 810), (680, 780), (500, 800), (220, 750)]):
    assert on_disc(x, y, 8), i
    ell(f"Sand fleck {i+1}", x, y, 3.5, 2.5, fill="#8A7454", opacity=50, stroke=NONE)

# --- the empty next shell, waiting -----------------------------------------------
ell("Empty shell shadow", 748, 668, 62, 10, fill="#160E08", opacity=42, stroke=NONE)
d.path(smooth([(706, 646), (694, 616), (706, 586), (736, 566), (768, 566),
               (788, 582), (802, 562), (790, 592), (786, 618), (772, 640),
               (744, 652), (720, 652)]),
       "Empty shell", fill=lin((700, 560), (800, 660), (0, "#D8B88E"),
                               (0.55, "#A87A50"), (1, "#6E4630")),
       stroke=INK, strokeWidth=5)
ext([(802, 562), (694, 616), (720, 652)])
# whorl bands on the little shell
d.path("M706,596 Q744,584 784,600", "Empty band 1", fill=NONE,
       stroke="#7A4E30", strokeWidth=4, opacity=50, cap="round")
d.path("M700,624 Q744,612 780,622", "Empty band 2", fill=NONE,
       stroke="#7A4E30", strokeWidth=4, opacity=45, cap="round")
# its dark aperture turned toward the crab — an open door
d.path("M710,600 Q692,614 698,636 Q714,644 724,628 Q726,610 710,600 Z",
       "Empty aperture", fill="#1E0F08", opacity=75, stroke=NONE)
d.path("M706,598 Q690,612 696,638", "Empty aperture rim", fill=NONE,
       stroke="#E4C49A", strokeWidth=3.5, opacity=60, cap="round")

# --- the hermit crab ---------------------------------------------------------------
ell("Crab shadow", 480, 692, 190, 18, fill="#160E08", opacity=45, stroke=NONE)

# far walking leg, dimmed behind the shell
d.path("M390,596 L362,648", "Leg far upper", fill=NONE, stroke="#5C2818",
       strokeWidth=9, opacity=55, cap="round")
d.path("M362,648 L352,684", "Leg far lower", fill=NONE, stroke="#5C2818",
       strokeWidth=6, opacity=55, cap="round")
ext([(352, 684)])

# the borrowed whelk — fat turban of a body whorl, short stepped spire
shell = [(565, 575), (575, 515), (548, 450), (500, 405), (445, 385),
         (402, 372), (382, 352), (368, 330), (372, 305), (352, 296),
         (338, 315), (328, 345), (322, 372), (305, 408), (293, 470),
         (302, 545), (352, 596), (452, 612)]
d.path(smooth(shell), "Borrowed shell",
       fill=lin((330, 300), (600, 620), (0, "#E8C89E"), (0.5, "#B8834F"),
                (1, "#7A4E34")),
       stroke=INK, strokeWidth=6)
ext(shell)
# spire sutures — two step-shadows under the little turret
d.path("M334,338 Q356,346 374,340", "Suture 1", fill=NONE,
       stroke="#6E4228", strokeWidth=4, opacity=60, cap="round")
d.path("M326,368 Q356,378 386,370", "Suture 2", fill=NONE,
       stroke="#6E4228", strokeWidth=4.5, opacity=55, cap="round")
# growth bands arcing over the body whorl — thin, many, following the dome
for i, (pth, w, op) in enumerate([
        ("M318,418 Q430,438 560,478", 4, 42),
        ("M306,462 Q428,486 566,522", 4, 40),
        ("M302,505 Q430,534 566,562", 3.5, 36),
        ("M310,546 Q430,580 540,596", 3.5, 32),
        ("M330,585 Q420,606 500,610", 3, 28)]):
    d.path(pth, f"Whorl band {i+1}", fill=NONE, stroke="#7A4A2C",
           strokeWidth=w, opacity=op, cap="round")
# dome sheen upper-right — the moon is up that way
ell("Shell sheen", 480, 430, 84, 40, fill=rad((0, "#F4E0C0", 34), (1, "#F4E0C0", 0)),
    stroke=NONE)
# apex tip + spire glint
d.path("M356,300 Q364,312 364,326", "Apex glint", fill=NONE,
       stroke="#F0DCC0", strokeWidth=3.5, opacity=65, cap="round")
# two little barnacles squatting on the old shell
for i, (x, y, r) in enumerate([(370, 430, 9), (345, 460, 7)]):
    ell(f"Barnacle {i+1}", x, y, r, r * 0.8, fill="#D8CBB0", opacity=80,
        stroke=INK, strokeWidth=2.5)
    ell(f"Barnacle mouth {i+1}", x, y - 1, r * 0.4, r * 0.32, fill="#5C4630",
        opacity=85, stroke=NONE)

# the aperture — dark opening low-right where the crab lives
d.path("M540,556 Q578,568 572,600 Q552,614 528,600 Q522,574 540,556 Z",
       "Aperture", fill="#1E0F08", opacity=75, stroke=NONE)
d.path("M536,554 Q574,564 574,592", "Aperture lip", fill=NONE,
       stroke="#E4C49A", strokeWidth=4, opacity=55, cap="round")

# head + thorax emerging right of the aperture
d.path(smooth([(540, 585), (575, 556), (610, 560), (622, 585), (606, 612), (566, 614)]),
       "Head", fill=lin((540, 550), (630, 620), (0, "#B4543C"), (1, "#6E2E1E")),
       stroke=INK, strokeWidth=5)
ext([(622, 585)])

# eyestalks fanning up-forward
d.path("M578,562 L604,524", "Eyestalk 1", fill=NONE, stroke="#8A3C28",
       strokeWidth=6, cap="round")
d.path("M562,568 L580,530", "Eyestalk 2", fill=NONE, stroke="#8A3C28",
       strokeWidth=6, cap="round")
ell("Eye 1", 607, 521, 7.5, 8.5, fill="#140C08", stroke=NONE)
ell("Eye 2", 582, 526, 7, 8, fill="#140C08", stroke=NONE)
ell("Eye glint 1", 609, 518, 2.5, 2.5, fill="#E8DCC8", opacity=80, stroke=NONE)
ell("Eye glint 2", 584, 523, 2.2, 2.2, fill="#E8DCC8", opacity=75, stroke=NONE)
ext([(607, 521)])

# long antennae feeling ahead — thin geometry at >=3pt
d.path("M600,548 Q648,516 692,526", "Antenna 1", fill=NONE, stroke="#9A4630",
       strokeWidth=3.5, cap="round")
d.path("M596,558 Q644,540 686,552", "Antenna 2", fill=NONE, stroke="#9A4630",
       strokeWidth=3.5, cap="round")
ext([(692, 526)])

# the big blocker claw, held up front
claw = [(618, 592), (648, 566), (692, 572), (716, 600), (712, 634),
        (688, 656), (652, 658), (622, 640), (612, 614)]
d.path(smooth(claw), "Big claw",
       fill=lin((620, 560), (720, 660), (0, "#CE6A46"), (0.6, "#9A4630"),
                (1, "#6E2E1C")),
       stroke=INK, strokeWidth=5)
ext(claw)
# pincer split + finger
d.path("M676,574 Q700,580 706,602 Q690,600 676,592 Z", "Claw finger",
       fill=lin((676, 570), (710, 604), (0, "#B4543C"), (1, "#7A3620")),
       stroke=INK, strokeWidth=4)
d.path("M674,580 Q688,592 700,600", "Pincer split", fill=NONE, stroke=INK,
       strokeWidth=3.5, opacity=80, cap="round")
# claw knuckles
for i, (x, y, r) in enumerate([(640, 600, 6), (660, 588, 5), (648, 626, 6.5), (682, 622, 5)]):
    ell(f"Claw knuckle {i+1}", x, y, r, r * 0.7, fill="#E08A5C", opacity=50, stroke=NONE)
# claw sheen
ell("Claw sheen", 652, 590, 34, 16, fill=rad((0, "#F0A87C", 30), (1, "#F0A87C", 0)),
    stroke=NONE)

# small feeding claw tucked under the big one
d.path("M600,622 Q616,636 612,652 Q594,652 588,638 Q588,626 600,622 Z",
       "Small claw", fill="#7A3620", stroke=INK, strokeWidth=4, opacity=95)

# near walking legs — two joints, tips in the sand
for i, (hip, knee, foot) in enumerate([((586, 622), (636, 664), (656, 692)),
                                      ((548, 626), (560, 674), (566, 694)),
                                      ((470, 620), (438, 664), (424, 690))]):
    d.path(f"M{hip[0]},{hip[1]} L{knee[0]},{knee[1]}", f"Leg {i+1} upper",
           fill=NONE, stroke="#7A3620", strokeWidth=10, cap="round")
    d.path(f"M{knee[0]},{knee[1]} L{foot[0]},{foot[1]}", f"Leg {i+1} lower",
           fill=NONE, stroke="#8A3C28", strokeWidth=6.5, cap="round")
    d.path(f"M{foot[0]},{foot[1]} l-4,6", f"Leg {i+1} tip",
           fill=NONE, stroke=INK, strokeWidth=4, cap="round")
    ext([foot])
    # knee joint dot
    ell(f"Leg {i+1} knee", knee[0], knee[1], 5, 5, fill="#9A4630", stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#08141A", strokeWidth=6)

# --- extent check -----------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("hermit-crab extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 26, far


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
    n = d.text(name, "Name", x=500, y=932, size=58, font="Virelai Sans",
               color="#E8D9C0", justify="center")
    m = d.text(mats, "Second line", x=500, y=970, size=22, font="Virelai Sans",
               color="#9FB0AC", justify="center")
    d.cmd("text.setStyle", "Name tracking", ids=[n["id"]], tracking=80)
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


caption("HERMIT CRAB", "PAGURUS BERNHARDUS")
d.finish("hermit-crab-V1R00")
