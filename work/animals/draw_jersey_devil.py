#!/usr/bin/env python3
"""Jersey devil — field plate V1R00. Hooves, wings and a Pine Barrens
mailing address: the thing reared on a peat hummock in a cedar swamp,
head thrown back mid-shriek at a drowned moon, bat wings mantled wide,
cloven hooves dug in, whippy tail forked. Cedar-swamp plate, shriek mood.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Jersey Devil — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1C100C"   # warm near-black
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


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin((0, 0), (0, 1000), (0, "#0C120E"), (1, "#040806")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#5A6E58", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin((0, 40), (0, 880), (0, "#27362C"), (0.5, "#1A2620"),
                 (0.8, "#121C16"), (1, "#0A120C")),
        stroke="#060C08", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.74, "#000000", 0), (1, "#040804", 0.5)),
        stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8C4AC", strokeWidth=3, opacity=24)

# a drowned moon, high-left, misted over
ell("Moon", 330, 205, 36, 36,
    fill=rad((0, "#D8DCC4"), (0.75, "#B0B89C"), (1, "#8A9478")), opacity=60,
    stroke=NONE)
ell("Moon murk", 330, 205, 92, 66,
    fill=rad((0, "#9AA88E", 16), (1, "#9AA88E", 0)), stroke=NONE)
ell("Mist veil", 400, 260, 260, 40, fill="#8AA090", opacity=9, stroke=NONE)

# cedar trunks — dark verticals that ENTER through the rim, tops cut by the arc
# left cedar: top edge is a rim chord between (160,213) and (186,181)
d.path(f"M160,213 Q166,440 172,690 L196,690 Q190,440 186,181 "
       f"A{PR},{PR} 0 0 0 160,213 Z",
       "Cedar left", fill=lin((178, 180), (184, 690), (0, "#2A241C"),
                              (1, "#14100C")), opacity=92, stroke=NONE)
# right cedar: rim chord between (826,195) and (852,231)
d.path(f"M826,195 Q822,440 818,690 L840,690 Q846,440 852,231 "
       f"A{PR},{PR} 0 0 1 826,195 Z",
       "Cedar right", fill=lin((832, 195), (830, 690), (0, "#2A241C"),
                               (1, "#14100C")), opacity=92, stroke=NONE)
# a dead snag deeper in — fully inside, top rounded off
d.path("M756,300 Q754,480 758,668 L772,668 Q770,480 770,300 Q763,290 756,300 Z",
       "Snag", fill="#1A1710", opacity=85, stroke=NONE)
# hanging moss off the trunks
for i, (mx, my, ln) in enumerate([(180, 240, 50), (184, 330, 62), (176, 430, 44),
                                  (832, 260, 56), (836, 370, 48), (826, 470, 40),
                                  (764, 320, 42), (766, 420, 36)]):
    d.path(f"M{mx},{my} q-4,{ln / 2:.0f} -2,{ln}", f"Moss {i+1}", fill=NONE,
           stroke="#3E4632", strokeWidth=3, opacity=55, cap="round")

# --- swamp water: chord closing on the disc arc -----------------------------------------
ch = 684
hch = math.sqrt(PR ** 2 - (ch - PCY) ** 2)
d.path(f"M{PCX - hch:.1f},{ch} L{PCX + hch:.1f},{ch} A{PR},{PR} 0 0 1 {PCX - hch:.1f},{ch} Z",
       "Swamp water", fill=lin((0, ch), (0, 880), (0, "#223028"), (0.5, "#121E18"),
                               (1, "#080F0C")), stroke=NONE)
# tannin-dark slick + duckweed flecks
for i, (x, y, w, op) in enumerate([(280, 706, 90, 20), (520, 720, 110, 17),
                                   (690, 708, 70, 15), (390, 752, 80, 13),
                                   (600, 768, 95, 12), (240, 736, 60, 12)]):
    line(f"Water streak {i+1}", x, y, x + w, y, 2.5, "#5E7A68", opacity=op)
for i, (x, y) in enumerate([(330, 700), (480, 712), (640, 700), (740, 730),
                            (280, 760), (560, 780), (430, 735)]):
    if on_disc(x, y, 8):
        ell(f"Duckweed {i+1}", x, y, 3.5, 2, fill="#4E6A48", opacity=50, stroke=NONE)
# cedar knees — little spikes poking out of the water
for i, (x, h) in enumerate([(238, 34), (762, 40), (806, 26), (196, 22)]):
    if on_disc(x, 684 - h, 12):
        d.path(f"M{x - 7},{690} L{x},{690 - h} L{x + 7},{690} Z",
               f"Cedar knee {i+1}", fill="#161F18", stroke=INK, strokeWidth=3)
# will-o-wisps — three cold motes over the water
for i, (x, y, s) in enumerate([(300, 640, 5), (700, 620, 4.5), (590, 655, 3.5)]):
    ell(f"Wisp {i+1}", x, y, s, s, fill=rad((0, "#C8E8C0", 70), (1, "#C8E8C0", 0)),
        stroke=NONE)

# --- the devil ---------------------------------------------------------------------------
WING_MEM = lin((500, 260), (500, 480), (0, "#4E2E28", 82), (1, "#2A1814", 70))
WING_FAR = lin((500, 260), (500, 480), (0, "#38211C", 78), (1, "#1E100E", 64))

# far wing (right), dimmer, spread a touch higher
d.path(smooth([(545, 425), (615, 315), (645, 282), (778, 262), (738, 330),
               (784, 344), (726, 388), (744, 424), (648, 452), (545, 462)]),
       "Wing far", fill=WING_FAR, stroke=INK, strokeWidth=5)
ext([(778, 262), (784, 344)])
for j, (x1, y1) in enumerate([(778, 262), (784, 344), (744, 424)]):
    line(f"Wing far rib {j+1}", 645, 282, x1, y1, 4, "#241410", opacity=70)

# tail — a whippy line curling right along the ground, forked tip up
d.path(smooth([(508, 585), (560, 630), (620, 660), (676, 668), (716, 648)],
              closed=False),
       "Tail", fill=NONE, stroke="#3A1F16", strokeWidth=9, cap="round")
d.path(smooth([(716, 648), (736, 624), (748, 602), (742, 596), (728, 612),
               (708, 634)]),
       "Tail fork", fill="#3A1F16", stroke=INK, strokeWidth=4)
ext([(748, 602)])

# hind legs — digitigrade, bent under the rear-up body
# far leg, dimmer
d.path(smooth([(488, 560), (462, 596), (448, 632), (456, 662), (470, 676),
               (478, 668), (470, 640), (478, 610), (500, 580)]),
       "Leg far", fill="#321E14", stroke=INK, strokeWidth=4.5)
# near leg — haunch, shin, cloven hoof dug into the hummock
d.path(smooth([(512, 545), (482, 585), (470, 624), (478, 660), (494, 678),
               (506, 672), (498, 642), (506, 610), (528, 578)]),
       "Leg near", fill=lin((480, 540), (530, 680), (0, "#4E2C1C"),
                            (1, "#2A160E")), stroke=INK, strokeWidth=5)
ext([(478, 660)])
# hooves — two-toed dark wedges
for i, (hx) in enumerate((492, 470)):
    d.path(f"M{hx - 8},678 L{hx},668 L{hx + 8},676 L{hx + 2},684 Z",
           f"Hoof toe {i+1}", fill="#14100C", stroke=NONE)

# torso — the thrown-back barrel, chest to the left
torso = [(470, 610), (438, 575), (425, 520), (432, 465), (452, 425),
         (478, 405), (498, 415), (514, 455), (520, 510), (514, 565)]
d.path(smooth(torso), "Torso",
       fill=lin((420, 400), (530, 620), (0, "#5C3420"), (0.55, "#3E2214"),
                (1, "#26140C")), stroke=INK, strokeWidth=6)
ext(torso)
# belly rib-shade
d.path("M455,470 Q448,520 462,566", "Belly shade", fill=NONE,
       stroke="#241208", strokeWidth=6, opacity=45, cap="round")

# neck ribbon up-left into the thrown-back head
d.path(smooth([(464, 438), (436, 412), (416, 382), (428, 364), (456, 390),
               (484, 420)]),
       "Neck", fill=lin((420, 360), (480, 440), (0, "#542E1C"), (1, "#301A0E")),
       stroke=INK, strokeWidth=5)

# head — horse-like, flung up-left, jaws wide on the shriek
d.path(smooth([(432, 372), (410, 356), (392, 334), (378, 308), (390, 298),
               (410, 306), (426, 322), (442, 334), (450, 350)]),
       "Head", fill=lin((390, 300), (450, 370), (0, "#5C3420"), (1, "#321C10")),
       stroke=INK, strokeWidth=5)
ext([(378, 308)])
# dropped lower jaw — the scream is the open gap between the two
d.path(smooth([(434, 372), (412, 374), (392, 372), (378, 366), (376, 356),
               (388, 356), (404, 362), (424, 360)]),
       "Lower jaw", fill="#42240F", stroke=INK, strokeWidth=4)
ext([(376, 356)])
# mouth interior — a hot little cave under the open upper jaw
d.path("M388,340 Q402,352 420,354 Q410,340 396,334 Z", "Mouth glow",
       fill="#B0482E", opacity=80, stroke=NONE)
# ear spike + brow horn buds
d.path("M420,326 Q414,308 420,296 Q428,308 428,322 Z", "Ear spike",
       fill="#4E2C1A", stroke=INK, strokeWidth=3.5)
d.path("M404,318 Q398,304 402,294 Q410,304 410,314 Z", "Horn bud",
       fill="#3A2212", stroke=INK, strokeWidth=3)
# eye — wild, pale
ell("Eye", 428, 338, 6, 7, fill="#0E0806", stroke=NONE)
ell("Eye glint", 430, 335, 2.4, 2.4, fill="#F0E0B0", opacity=85, stroke=NONE)
ell("Nostril", 390, 314, 3.5, 2.8, fill="#0E0806", opacity=85, stroke=NONE)

# near wing — the mantled fan, spread up-left over the moon side
d.path(smooth([(455, 425), (385, 318), (358, 288), (228, 266), (264, 330),
               (220, 346), (272, 386), (262, 428), (352, 454), (455, 462)]),
       "Wing near", fill=WING_MEM, stroke=INK, strokeWidth=5)
ext([(228, 266), (220, 346)])
for j, (x1, y1) in enumerate([(228, 266), (220, 346), (262, 428)]):
    line(f"Wing near rib {j+1}", 358, 288, x1, y1, 4, "#241410", opacity=75)
# wing shoulder cap
ell("Wing shoulder", 455, 432, 18, 14, fill="#3A2118", stroke=INK, strokeWidth=4)

# small forelimbs lifted, clawed fingers spread
for i, (pts) in enumerate([[(446, 478), (424, 452), (408, 428), (416, 420),
                            (430, 442), (452, 462)],
                           [(466, 486), (448, 466), (436, 446), (444, 440),
                            (456, 460), (472, 476)]]):
    d.path(smooth(pts), f"Arm {i+1}", fill="#42240F", stroke=INK, strokeWidth=4)
for i, (x0, y0, x1, y1) in enumerate([(410, 424, 396, 406), (414, 426, 404, 404),
                                      (418, 428, 414, 402), (440, 444, 428, 428),
                                      (444, 446, 436, 426)]):
    line(f"Finger {i+1}", x0, y0, x1, y1, 3.5, "#5C3420")

# peat hummock the devil stands on — a dark mound on the waterline
ell("Hummock", 490, 692, 120, 16, fill="#181410", opacity=90, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#060C08", strokeWidth=6)

# --- extent check -------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("jersey-devil extent: farthest point %.0f from centre (rim %d)" % (far, PR))
assert far < PR - 20, far


# --- caption ------------------------------------------------------------------------------
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
               color="#DDD8BE", justify="center")
    m = d.text(mats, "Second line", x=500, y=970, size=22, font="Virelai Sans",
               color="#92A294", justify="center")
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


caption("JERSEY DEVIL", "PINE BARRENS · LEEDS POINT")
d.finish("jersey-devil-V1R00")
