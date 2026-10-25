#!/usr/bin/env python3
"""Blue-footed booby — field plate V1R00. Galapagos dusk: the bird mid
courtship dance on black volcanic rock, head thrown up, bill to the sky,
one turquoise foot lifted to show off the sea's best blue. Amber horizon
over a dark sea; basalt takes the bottom of the disc on the rim arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Blue-Footed Booby — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#140D0A"   # warm near-black
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


# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#0B0E14"), (1, "#05060A")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#5A6478", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin((0, 40), (0, 880), (0, "#1B2434"), (0.5, "#243040"),
                 (0.72, "#4A3A28"), (1, "#14100C")),
        stroke="#0A0C12", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.74, "#000000", 0), (1, "#04060C", 0.55)),
        stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C6D0DC", strokeWidth=3, opacity=26)

# dusk glow on the horizon, warm off-center right where the bird looks
d.shape("ellipse", "Horizon glow", x=430, y=520, width=420, height=190,
        fill=rad((0, "#C8803E", 26), (0.6, "#8A5428", 9), (1, "#8A5428", 0)),
        stroke=NONE)
# faint stars, cold
for i, (x, y, s) in enumerate([(280, 180, 4), (660, 150, 3), (740, 250, 3.5),
                               (230, 290, 3), (560, 120, 3)]):
    ell(f"Star {i+1}", x, y, s, s, fill="#D8E0EA", opacity=30, stroke=NONE)

# --- sea: chord y=636 closing on the disc arc --------------------------------------
ch = 636
hch = math.sqrt(PR ** 2 - (ch - PCY) ** 2)
d.path(f"M{PCX - hch:.1f},{ch} L{PCX + hch:.1f},{ch} A{PR},{PR} 0 0 1 {PCX - hch:.1f},{ch} Z",
       "Sea", fill=lin((0, ch), (0, 880), (0, "#1C2A38"), (0.5, "#12202E"),
                       (1, "#080D16")), stroke=NONE)
# horizon line: thin warm light where sea meets sky
line("Horizon light", PCX - hch + 6, ch, PCX + hch - 6, ch, 2.5, "#C08850",
     opacity=38)
# water shimmer: short horizontal dashes
for i, (x, y, w, op) in enumerate([(220, 662, 70, 24), (400, 678, 90, 20),
                                   (610, 668, 80, 22), (740, 696, 60, 18),
                                   (300, 716, 100, 15), (560, 730, 110, 14),
                                   (680, 756, 90, 12)]):
    line(f"Sea shimmer {i+1}", x, y, x + w, y, 2.5, "#5A6E8C", opacity=op)

# distant islet silhouette right of the horizon glow
d.path(smooth([(640, 636), (668, 612), (712, 606), (756, 614), (788, 636)]),
       "Islet", fill="#0E141C", opacity=80, stroke=NONE)

# --- volcanic rock: chord y=766 closing on the disc arc -----------------------------
ch2 = 766
hch2 = math.sqrt(PR ** 2 - (ch2 - PCY) ** 2)
d.path(f"M{PCX - hch2:.1f},{ch2} L{PCX + hch2:.1f},{ch2} A{PR},{PR} 0 0 1 {PCX - hch2:.1f},{ch2} Z",
       "Basalt", fill=lin((0, ch2), (0, 880), (0, "#2A2420"), (0.5, "#181210"),
                          (1, "#0C0806")), stroke=NONE)
# lit top edge where the bird stands
line("Rock edge light", PCX - hch2 + 8, ch2, PCX + hch2 - 8, ch2, 3,
     "#5E4E3C", opacity=42)
# basalt cracks
for i, (x0, y0, x1, y1) in enumerate([(300, 776, 330, 806), (560, 780, 540, 816),
                                      (690, 774, 716, 800), (420, 790, 448, 822)]):
    line(f"Rock crack {i+1}", x0, y0, x1, y1, 2.5, "#000000", opacity=40)

# --- the bird: mid-dance, facing right, head up -------------------------------------
WHITE_HI = "#F4EFE4"
WHITE_LO = "#CDBFAA"
BROWN_HI = "#5A4434"
BROWN_MID = "#38271E"
BROWN_LO = "#1E140E"
BLUE_HI = "#5CC6E8"
BLUE_MID = "#2E9CC8"
BLUE_LO = "#176A96"
BILL = "#6E8494"

# far wing lifted behind, darker
farwing = [(486, 452), (430, 420), (392, 432), (388, 470), (414, 520),
           (452, 560), (486, 566)]
ext(farwing)
d.path(smooth(farwing), "Far wing",
       fill=lin((0, 420), (0, 570), (0, BROWN_MID), (1, "#150E0A")),
       stroke=INK, strokeWidth=3, join="round", opacity=92)

# tail: long narrow wedge cocked up behind, brown with pale shaft
tail = [(462, 600), (428, 628), (330, 520), (350, 502), (446, 548), (478, 578)]
ext(tail)
d.path(smooth(tail), "Tail",
       fill=lin((330, 500), (480, 630), (0, "#4E3A2C"), (1, "#1C120C")),
       stroke=INK, strokeWidth=3, join="round")
line("Tail shaft", 348, 516, 436, 584, 3.5, "#8A7058", opacity=55)

# planted leg: from belly down to the rock at y~756
d.path("M512,640 L508,706 L522,706 L528,642 Z", "Planted leg",
       fill=lin((0, 640), (0, 706), (0, "#3A6E8A"), (1, BLUE_LO)),
       stroke=INK, strokeWidth=2.5, join="round")

# planted foot: webbed, flat on the rock, toes spread — bright blue
foot_pts = [(506, 706), (524, 706), (534, 728), (560, 748), (556, 760),
            (532, 752), (520, 762), (508, 752), (490, 762), (482, 750),
            (494, 730), (496, 714)]
ext(foot_pts)
d.path(smooth(foot_pts), "Planted foot",
       fill=lin((0, 706), (0, 762), (0, BLUE_HI), (0.6, BLUE_MID), (1, BLUE_LO)),
       stroke=INK, strokeWidth=3, join="round")
# toe creases
for i, (x0, y0, x1, y1) in enumerate([(516, 716, 500, 752), (522, 716, 522, 752),
                                      (528, 718, 548, 748)]):
    line(f"Toe crease {i+1}", x0, y0, x1, y1, 2.2, "#0E4A68", opacity=65)

# body: upright pear, breast forward, in the dance lean
body = [(560, 452), (596, 480), (606, 540), (596, 610), (566, 660),
        (528, 686), (496, 686), (466, 660), (446, 612), (440, 552),
        (452, 496), (496, 458), (530, 446)]
ext(body)
d.path(smooth(body), "Body",
       fill=lin((440, 460), (610, 680), (0, WHITE_HI), (0.55, "#E4DAC8"),
                (1, WHITE_LO)),
       stroke=INK, strokeWidth=3, join="round")
# belly shade, translucent
d.shape("ellipse", "Belly shade", x=452, y=560, width=140, height=120,
        fill=rad((0, "#8A7458", 26), (1, "#8A7458", 0)), stroke=NONE)

# neck rising to the thrown-back head
neck = [(528, 452), (548, 392), (566, 348), (596, 340), (610, 372),
        (598, 420), (574, 452)]
ext(neck)
d.path(smooth(neck), "Neck",
       fill=lin((540, 340), (610, 452), (0, WHITE_HI), (1, "#D8CCB6")),
       stroke=INK, strokeWidth=3, join="round")

# head: oval tilted up, brown-streaked nape
head = [(562, 344), (574, 318), (602, 306), (628, 314), (636, 338),
        (626, 362), (600, 370), (574, 364)]
ext(head)
d.path(smooth(head), "Head",
       fill=rad((0, WHITE_HI), (0.7, "#E6DCC8"), (1, "#C4B49A")),
       stroke=INK, strokeWidth=3, join="round")
# brown crown/nape streaks — the booby's tousled cap
for i, (x0, y0, x1, y1) in enumerate([(584, 316, 596, 340), (598, 310, 606, 338),
                                      (612, 312, 616, 338), (624, 322, 622, 344)]):
    line(f"Nape streak {i+1}", x0, y0, x1, y1, 4, "#7A5C40", opacity=60)

# bill: long tapered cone pointing sky-right, slightly open in the call
bill_top = [(600, 322), (662, 282), (706, 268), (664, 296), (612, 336)]
ext(bill_top)
d.path(smooth(bill_top), "Bill upper",
       fill=lin((600, 270), (700, 300), (0, "#8CA2B2"), (1, "#4A5E6C")),
       stroke=INK, strokeWidth=3, join="round")
d.path(smooth([(612, 340), (664, 300), (700, 288), (660, 314), (618, 350)]),
       "Bill lower",
       fill=lin((610, 300), (690, 330), (0, "#5E7484"), (1, "#3A4A56")),
       stroke=INK, strokeWidth=2.5, join="round")
# gape line
line("Gape", 610, 336, 660, 306, 2.5, "#241A14", opacity=80)

# eye: pale yellow, small and bright under the crown
ell("Eye", 608, 332, 8, 8, fill=rad((0, "#F2E2A0"), (1, "#C8A840")),
    stroke=INK, strokeWidth=2)
ell("Pupil", 609, 332, 3.5, 3.5, fill="#100C08", stroke=NONE)
ell("Eye glint", 606, 329, 1.8, 1.8, fill="#FFFFFF", opacity=85, stroke=NONE)

# near wing: folded long on the flank, tip sweeping back past the tail base
nearwing = [(512, 470), (462, 442), (424, 448), (406, 474), (396, 520),
            (390, 566), (404, 598), (436, 608), (478, 600), (516, 570),
            (534, 528), (530, 492)]
ext(nearwing)
d.path(smooth(nearwing), "Near wing",
       fill=lin((390, 440), (540, 610), (0, BROWN_HI), (0.55, BROWN_MID),
                (1, BROWN_LO)),
       stroke=INK, strokeWidth=3, join="round")
# covert scallops: short strokes running along the wing
for i, (x0, y0, x1, y1) in enumerate([(430, 480, 478, 492), (420, 514, 474, 528),
                                      (414, 550, 470, 560)]):
    line(f"Covert {i+1}", x0, y0, x1, y1, 3.5, "#241812", opacity=55)
# white wing-bar flash where the primaries part
line("Wing bar", 406, 588, 480, 600, 5, "#E8DEC8", opacity=45)

# raised leg + display foot: the money shot, toes spread toward the viewer
d.path("M560,636 C586,610 606,592 616,570 L632,580 C622,606 600,628 574,650 Z",
       "Raised leg",
       fill=lin((560, 640), (630, 570), (0, "#3A6E8A"), (1, BLUE_MID)),
       stroke=INK, strokeWidth=2.5, join="round")
# webbed foot fan: three front toes splayed, bright blue
disp = [(616, 570), (634, 576), (656, 556), (672, 540), (678, 552),
        (664, 574), (680, 578), (676, 594), (652, 598), (656, 614),
        (644, 620), (626, 602), (610, 596), (606, 580)]
ext(disp)
d.path(smooth(disp), "Display foot",
       fill=lin((610, 540), (680, 620), (0, BLUE_HI), (0.55, BLUE_MID),
                (1, BLUE_LO)),
       stroke=INK, strokeWidth=3, join="round")
# toe creases + a rim glint on the lifted foot
for i, (x0, y0, x1, y1) in enumerate([(636, 578, 664, 552), (644, 584, 672, 586),
                                      (640, 592, 648, 610)]):
    line(f"Disp toe {i+1}", x0, y0, x1, y1, 2.2, "#0E4A68", opacity=65)
line("Foot glint", 620, 576, 654, 552, 3, "#C8F0FF", opacity=55)

# dusk rim light on the bird's left edge
d.path("M452,520 C444,560 448,610 468,648", "Rim light", fill=NONE,
       stroke="#C89058", strokeWidth=3.5, opacity=42, cap="round")

# contact shadow under the planted foot on the rock
d.shape("ellipse", "Foot shadow", x=474, y=752, width=104, height=18,
        fill=rad((0, "#000000", 55), (1, "#000000", 0)), stroke=NONE)

# --- extent check ---------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("booby extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#E8E4DA", justify="center")
    m = d.text(mats, "Second line", x=500, y=970, size=22, font="Virelai Sans",
               color="#98A2B2", justify="center")
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


caption("BLUE-FOOTED BOOBY", "SULIFORMES · SULA NEBOUXII")
d.finish("blue-footed-booby-V1R00")
