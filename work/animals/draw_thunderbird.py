#!/usr/bin/env python3
"""Thunderbird — field plate V1R00. Wingspan enough to make its own
weather: a great dark raptor front-on in soaring dihedral, wings stretched
rim to rim over the mesas, storm bank closing on the top arc with an
amber-lit underbelly, one bolt licking down off the wing. Mesa plate,
storm-front mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Thunderbird — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#18100C"   # warm near-black
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
        fill=lin((0, 0), (0, 1000), (0, "#0E1218"), (1, "#06080C")), stroke=NONE)
d.shape("ellipse", "Plate halo", x=78, y=38, width=844, height=844,
        fill="#5C6E80", opacity=9, stroke=NONE)
# storm sky — dark slate up top burning amber at the horizon band
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=lin((0, 40), (0, 880), (0, "#131C26"), (0.42, "#24303C"),
                 (0.62, "#4A3E30"), (0.72, "#5E4226"), (0.85, "#2E2218"),
                 (1, "#14100E")),
        stroke="#080C12", strokeWidth=6)
d.shape("ellipse", "Plate vignette", x=80, y=40, width=840, height=840,
        fill=rad((0, "#000000", 0), (0.74, "#000000", 0), (1, "#040608", 0.5)),
        stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8C4CC", strokeWidth=3, opacity=22)

# amber horizon band — the last light under the front
ell("Horizon fire", 560, 585, 300, 70,
    fill=rad((0, "#C8843C", 26), (0.6, "#8A5426", 10), (1, "#8A5426", 0)),
    stroke=NONE)

# --- the storm bank: closes on the TOP arc ----------------------------------------------
# on-rim points: left (166,220) right (836,214) — compute on circle
def rim_top(x):
    return PCY - math.sqrt(max(0, PR * PR - (x - PCX) ** 2))

lx, rx = 166, 836
d.path(f"M{lx},{rim_top(lx):.0f} "
       f"Q260,300 340,284 Q420,268 500,292 Q580,316 660,296 "
       f"Q740,276 {rx},{rim_top(rx):.0f} "
       f"A{PR},{PR} 0 0 0 {lx},{rim_top(lx):.0f} Z",
       "Storm bank", fill=lin((0, 60), (0, 330), (0, "#0C1218"),
                              (0.7, "#182028"), (1, "#232A32")), stroke=NONE)
# lit underbelly — soft amber washes tucked under the bank's billows
for i, (cx, cy, rx2, ry2, op) in enumerate([(330, 320, 130, 26, 34),
                                            (560, 340, 150, 28, 30),
                                            (720, 310, 90, 22, 26)]):
    ell(f"Underbelly {i+1}", cx, cy, rx2, ry2,
        fill=rad((0, "#C8843C", op), (1, "#C8843C", 0)), stroke=NONE)
# low scud — a second thin cloud dragging under the bank, left
d.path("M190,392 Q280,368 370,388 Q430,400 470,392 L470,404 Q400,418 320,404 "
       "Q250,392 196,404 Z", "Scud", fill="#141C24", opacity=80, stroke=NONE)

# rain curtain veils under the left flank of the front
for i, (x, ln) in enumerate([(230, 150), (262, 170), (296, 160), (330, 140),
                             (210, 120)]):
    d.path(f"M{x},{410} q-8,{ln / 2:.0f} -14,{ln}", f"Rain {i+1}", fill=NONE,
           stroke="#7A8C9C", strokeWidth=3, opacity=14, cap="round")

# lightning — one bolt off the right flank, forking to the mesa
d.path("M742,330 L716,420 L736,424 L700,528 L726,532 L688,636",
       "Bolt main", fill=NONE, stroke="#E8E0C8", strokeWidth=5,
       opacity=75, cap="round")
d.path("M716,420 L690,470 L700,474 L672,540", "Bolt fork", fill=NONE,
       stroke="#E8E0C8", strokeWidth=3.5, opacity=55, cap="round")
ell("Bolt bloom", 742, 336, 30, 14, fill=rad((0, "#E8E0C8", 40), (1, "#E8E0C8", 0)),
    stroke=NONE)
# a distant dimmer flicker left
d.path("M268,336 L252,392 L264,396 L242,452", "Bolt far", fill=NONE,
       stroke="#D8D4C0", strokeWidth=3, opacity=30, cap="round")

# --- mesas and desert floor ---------------------------------------------------------------
ch = 700
hch = math.sqrt(PR ** 2 - (ch - PCY) ** 2)
d.path(f"M{PCX - hch:.1f},{ch} L{PCX + hch:.1f},{ch} A{PR},{PR} 0 0 1 {PCX - hch:.1f},{ch} Z",
       "Desert floor", fill=lin((0, ch), (0, 880), (0, "#4E3424"), (0.5, "#2E1E12"),
                                (1, "#181009")), stroke=NONE)
# far mesa — long flat top, dim, right side
d.path("M560,700 L566,632 L586,624 L586,604 L748,604 L748,622 L770,630 L776,700 Z",
       "Mesa far", fill=lin((660, 600), (660, 700), (0, "#54382A"),
                            (1, "#2A1A10")), opacity=85, stroke=NONE)
ext([(748, 604), (586, 604)])
# near mesa — left, taller, warmer face
d.path("M180,700 L186,640 L206,632 L206,596 L318,596 L318,626 L340,634 L346,700 Z",
       "Mesa near", fill=lin((260, 590), (260, 700), (0, "#6E4830"),
                             (1, "#2E1C10")), stroke=INK, strokeWidth=4)
ext([(206, 596), (318, 596)])
# strata seams on the near mesa
for i, (y, w0, w1) in enumerate([(614, 210, 314), (636, 210, 322), (660, 212, 334)]):
    d.path(f"M{w0},{y} Q{(w0 + w1) / 2},{y + 4} {w1},{y}", f"Strata {i+1}",
           fill=NONE, stroke="#3A2414", strokeWidth=3, opacity=60, cap="round")
# mesa rim light on the flat tops
line("Mesa rim L", 206, 598, 318, 598, 3.5, "#C8843C", opacity=45)
line("Mesa rim R", 586, 606, 748, 606, 3, "#C8843C", opacity=35)

# --- the thunderbird ----------------------------------------------------------------------
BIRD = lin((500, 300), (500, 660), (0, "#3A2A1E"), (0.5, "#241812"), (1, "#140D08"))
BIRD_HI = "#4E3826"

def wing(side):
    s = side
    def X(x):
        return PCX + s * (x - PCX)
    # one wing: shoulder -> leading edge out -> primary fingers -> trailing home
    pts = [(X(478), 410), (X(404), 330), (X(316), 288), (X(244), 272),
           (X(196), 286),                                          # tip approach
           (X(180), 312),                                          # primary 1 (outermost)
           (X(210), 326), (X(214), 358),                            # notch, primary 2
           (X(260), 356), (X(268), 390),                            # notch, primary 3
           (X(318), 386), (X(334), 418),                            # notch, primary 4
           (X(392), 412), (X(406), 438),                            # notch, innermost
           (X(468), 448)]                                          # trailing to body
    d.path(smooth(pts), f"Wing {'L' if s < 0 else 'R'}", fill=BIRD,
           stroke=INK, strokeWidth=5)
    ext(pts)
    # feather flow lines arcing out to the fingers
    for j, (x1, y1) in enumerate([(200, 310), (218, 350), (266, 382),
                                  (330, 410), (400, 430)]):
        d.path(f"M{X(452)},{424} Q{X(360)},{350 + j * 8} {X(x1)},{y1}",
               f"Feather {'L' if s < 0 else 'R'}-{j+1}", fill=NONE,
               stroke=BIRD_HI, strokeWidth=3, opacity=45, cap="round")
    # storm-light on the leading edge
    d.path(f"M{X(470)},404 Q{X(360)},{310} {X(210)},{282}",
           f"Leading light {'L' if s < 0 else 'R'}", fill=NONE,
           stroke="#C89050", strokeWidth=4, opacity=40, cap="round")


wing(-1)
wing(1)

# tail fan — five broad feathers spread below the body
for i, (dx, ln, w) in enumerate([(-56, 116, 15), (-28, 130, 16), (0, 136, 17),
                                 (28, 128, 16), (54, 112, 15)]):
    bx, by = PCX + dx * 0.25, 548
    tx, ty = PCX + dx, 548 + ln
    d.path(f"M{bx - w / 2:.0f},{by} L{tx - w / 2:.0f},{ty} "
           f"Q{tx},{ty + 10} {tx + w / 2:.0f},{ty} L{bx + w / 2:.0f},{by} Z",
           f"Tail feather {i+1}", fill="#1E1410", stroke=INK, strokeWidth=3.5)
ext([(PCX + 56, 680), (PCX - 56, 680)])

# body — the hanging keel between the wings
body = [(PCX - 26, 420), (PCX - 40, 462), (PCX - 36, 520), (PCX - 20, 556),
        (PCX + 20, 556), (PCX + 36, 520), (PCX + 40, 462), (PCX + 26, 420)]
d.path(smooth(body), "Body", fill=BIRD, stroke=INK, strokeWidth=5)
# chest — a faint ember of storm-light on the breast
ell("Chest ember", PCX, 480, 24, 48,
    fill=rad((0, "#8A5426", 30), (1, "#8A5426", 0)), stroke=NONE)

# head — frontal raptor: brow ridge, down-hooked beak, eye pits
head = [(PCX - 30, 398), (PCX - 34, 366), (PCX - 20, 344), (PCX, 336),
        (PCX + 20, 344), (PCX + 34, 366), (PCX + 30, 398), (PCX + 14, 420),
        (PCX - 14, 420)]
d.path(smooth(head), "Head", fill=lin((470, 330), (530, 430), (0, "#4A3626"),
                                      (1, "#241812")), stroke=INK, strokeWidth=5)
ext(head)
# hooked beak dropping down the middle
d.path(smooth([(PCX - 10, 372), (PCX, 380), (PCX + 10, 372), (PCX + 8, 396),
               (PCX + 2, 408), (PCX - 4, 412), (PCX - 2, 398), (PCX - 8, 390)]),
       "Beak", fill="#D8C498", stroke=INK, strokeWidth=4)
# brow shadow band
d.path(f"M{PCX - 26},368 Q{PCX},356 {PCX + 26},368", "Brow band",
       fill=NONE, stroke="#141008", strokeWidth=6, opacity=70, cap="round")
# eyes — two pale fierce pits under the brow
for s in (-1, 1):
    ell(f"Eye {'L' if s < 0 else 'R'}", PCX + s * 16, 376, 5, 5.5,
        fill="#0C0804", stroke=NONE)
    ell(f"Eye fire {'L' if s < 0 else 'R'}", PCX + s * 16, 375, 2, 2,
        fill="#E8C878", opacity=90, stroke=NONE)
# crown hackles — a short swept crest off the back of the head
for i, (x0, y0, x1, y1) in enumerate([(PCX - 12, 342, PCX - 24, 318),
                                      (PCX - 2, 336, PCX - 8, 310),
                                      (PCX + 10, 340, PCX + 14, 314)]):
    line(f"Hackle {i+1}", x0, y0, x1, y1, 5, "#3A2A1E", opacity=95)

# talons tucked under the breast
for s in (-1, 1):
    d.path(f"M{PCX + s * 14},556 q{s * 6},10 {s * 4},16 q{-s * 8},2 {-s * 10},-4",
           f"Foot {'L' if s < 0 else 'R'}", fill=NONE, stroke="#0E0A06",
           strokeWidth=4.5, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#080C12", strokeWidth=6)

# --- extent check -------------------------------------------------------------------------
far = max(math.hypot(x - PCX, y - PCY) for x, y in EXTENT)
print("thunderbird extent: farthest point %.0f from centre (rim %d)" % (far, PR))
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
               color="#E4DCC4", justify="center")
    m = d.text(mats, "Second line", x=500, y=970, size=22, font="Virelai Sans",
               color="#9AA4AC", justify="center")
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


caption("THUNDERBIRD", "THE STORM-BRINGER")
d.finish("thunderbird-V1R00")
