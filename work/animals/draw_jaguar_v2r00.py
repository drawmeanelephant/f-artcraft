#!/usr/bin/env python3
"""Jaguar — psychedelic poster rendition V2R00. 60s concert-poster idiom:
rosettes become radiating concentric neon rings, the coat is a gradient
field, backdrop a pulsing purple/green wash. Three-quarter view, shoulder
toward viewer, amber eyes. Lettering warped on an arc letter-by-letter.
Rendition rules: no plate disc, no house dark ink; everything inside the
60pt safe margin, field runs edge to edge. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Jaguar — Psychedelic Poster V2R00", 1000, 1000)

CX, CY = 500, 470
VIOLET = "#2A0A3E"
PINK   = "#FF2E9A"
PINK_L = "#FF8FC8"
CYAN   = "#1FD8E0"
TEAL   = "#1FD8C0"
YELLOW = "#FFDE3A"
LIME   = "#A8F03A"
AMBER  = "#FFB42E"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def radO(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

def wavy_ring(r0, amp, lobes, phase=0.0, steps=120):
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        r = r0 + amp * math.sin(lobes * t + phase)
        pts.append((CX + r * math.cos(t), CY + r * math.sin(t)))
    dd = "M%.1f,%.1f " % pts[0]
    for i in range(steps):
        p = pts[(i + 1) % steps]
        q = pts[(i + 2) % steps]
        dd += "Q%.1f,%.1f %.1f,%.1f " % (p[0], p[1], (p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    return dd + "Z"

def arc_pts(cx, cy, r, a0, a1, n=16):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / (n - 1))),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / (n - 1))))
            for i in range(n)]

def poly(pts, closed=False):
    dd = "M%.1f,%.1f " % pts[0]
    for p in pts[1:]:
        dd += "L%.1f,%.1f " % p
    return dd + ("Z" if closed else "")

# --- field: purple-to-green wash, pulsing --------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin(0, 0, 1000, 1000, (0, "#36085E"), (0.5, "#1C0438"), (1, "#07220F")),
        stroke=NONE)
# pulsing colour-wash blobs behind the cat
d.shape("ellipse", "Wash magenta", x=150, y=120, width=700, height=640,
        fill=radO((0, "#C8128C", 42), (0.6, "#7E0E78", 22), (1, "#7E0E78", 0)), stroke=NONE)
d.shape("ellipse", "Wash green", x=560, y=480, width=380, height=380,
        fill=radO((0, "#2EE86A", 26), (1, "#2EE86A", 0)), stroke=NONE)
d.shape("ellipse", "Wash cyan", x=80, y=500, width=340, height=340,
        fill=radO((0, "#1FD8E0", 22), (1, "#1FD8E0", 0)), stroke=NONE)

# radiating colour-wave bands — pink/yellow/teal, the rosette rings scaled up
RING_COLS = [PINK, YELLOW, TEAL, PINK, CYAN, YELLOW, PINK, TEAL, "#B13AFF", YELLOW]
for i, r0 in enumerate(range(150, 406, 27)):
    d.path(wavy_ring(r0, 11, 8, i * 1.9), f"Wave band {i+1}", fill=NONE,
           stroke=RING_COLS[i % len(RING_COLS)], strokeWidth=21, opacity=85)

# sparkles inside the margin
for i, (x, y, s, col) in enumerate([
        (110, 118, 15, YELLOW), (886, 110, 14, CYAN), (104, 874, 15, PINK),
        (892, 868, 16, LIME), (74, 492, 12, TEAL), (926, 500, 12, YELLOW),
        (830, 216, 9, "#FFFFFF"), (176, 790, 10, CYAN)]):
    d.path(f"M{x},{y - s} L{x + s * 0.28},{y - s * 0.28} L{x + s},{y} "
           f"L{x + s * 0.28},{y + s * 0.28} L{x},{y + s} "
           f"L{x - s * 0.28},{y + s * 0.28} L{x - s},{y} "
           f"L{x - s * 0.28},{y - s * 0.28} Z",
           f"Sparkle {i+1}", fill=col, opacity=90, stroke=NONE)

# drips into the lower third, sliding past the shoulder
def drip(x, y0, y1, sway, w, col, label):
    xm = x + sway
    d.path(f"M{x},{y0} C{xm},{y0 + (y1 - y0) * 0.35} {x - sway},{y0 + (y1 - y0) * 0.7} {x + sway * 0.4:.1f},{y1}",
           f"{label} run", fill=NONE, stroke=col, strokeWidth=w, cap="round", opacity=92)
    d.shape("ellipse", f"{label} bulb", x=x + sway * 0.4 - w * 0.85, y=y1 - w * 0.55,
            width=w * 1.7, height=w * 1.5, fill=col, opacity=92, stroke=NONE)

for i, (x, y0, y1, sw, w, col) in enumerate([
        (250, 600, 806, 24, 14, TEAL), (318, 640, 772, -18, 12, PINK),
        (720, 630, 840, 20, 14, YELLOW), (786, 596, 780, -22, 12, CYAN)]):
    drip(x, y0, y1, sw, w, col, f"Drip {i+1}")

# === the jaguar, three-quarter view ============================================
COAT = lin(430, 300, 560, 830, (0, "#FF5FAE"), (0.45, "#FF9A3E"), (1, "#1FD8C0"))

def rosette(cx, cy, r, label, seed=0.0):
    """Rosette as broken concentric neon rings around a hot core."""
    cols = [PINK, CYAN, YELLOW]
    for k, rr in enumerate((r, r * 0.62)):
        a0 = seed * 40 + k * 140
        pts = arc_pts(cx, cy, rr, a0, a0 + 235)
        d.path(poly(pts), f"{label} ring {k+1}", fill=NONE, stroke=cols[k % 3],
               strokeWidth=max(3.2, r * 0.24), cap="round", opacity=90)
    d.shape("ellipse", f"{label} core", x=cx - r * 0.18, y=cy - r * 0.16,
            width=r * 0.36, height=r * 0.32, fill=cols[2], opacity=85, stroke=NONE)

# chest and shoulder mass first — the shoulder rolls toward the viewer; the
# bottom closes in a shallow curve so the bust sits in the field, not on a desk
d.path("M330,818 C322,742 348,668 412,628 C452,604 548,600 596,624 "
       "C668,660 700,730 694,818 C690,858 610,884 512,884 "
       "C414,884 334,858 330,818 Z",
       "Chest", fill=lin(500, 620, 500, 880, (0, "#FF9A3E"), (1, "#12B8A0")),
       stroke=VIOLET, strokeWidth=7)
# near shoulder swelling over the chest edge
d.path("M330,818 C318,740 344,664 416,624 C436,614 452,610 470,608 "
       "C430,646 408,712 412,780 C416,820 448,856 496,866 "
       "C420,862 344,848 330,818 Z",
       "Near shoulder", fill=lin(360, 620, 440, 860, (0, "#FF7AB8"), (1, "#FF9A3E")),
       stroke=VIOLET, strokeWidth=6)

# ears: near ear larger and lower on the skull corner, far ear tucked higher
d.path("M352,330 C322,314 310,278 322,248 C332,222 362,212 386,226 "
       "C408,238 414,270 404,296 C394,320 374,336 352,330 Z",
       "Ear near", fill=lin(360, 220, 370, 330, (0, "#FF5FAE"), (1, "#C81E78")),
       stroke=VIOLET, strokeWidth=6)
d.path("M360,312 C344,300 338,278 346,262 C354,248 372,244 384,254 "
       "C394,264 394,284 386,298 C378,310 370,316 360,312 Z",
       "Inner ear near", fill=CYAN, opacity=85, stroke=NONE)
d.path("M592,318 C616,300 624,268 612,244 C602,224 576,218 556,230 "
       "C538,242 534,270 544,292 C554,312 574,326 592,318 Z",
       "Ear far", fill=lin(580, 225, 575, 320, (0, "#E84E9E"), (1, "#A81268")),
       stroke=VIOLET, strokeWidth=6)
d.path("M584,300 C596,290 600,272 594,260 C588,248 572,246 562,256 "
       "C554,266 556,282 564,294 C570,302 578,306 584,300 Z",
       "Inner ear far", fill=CYAN, opacity=70, stroke=NONE)

# skull: broad crown, heavy jaw; the muzzle drifts a touch left for the 3/4
d.path("M470,292 C560,286 630,330 658,404 C682,468 674,548 640,612 "
       "C612,664 556,696 488,698 C414,700 356,668 330,612 "
       "C300,548 296,470 322,404 C350,330 386,298 470,292 Z",
       "Head", fill=COAT, stroke=VIOLET, strokeWidth=8)
# crown sheen + cheek shadow keep the volume round under the flat colours
d.shape("ellipse", "Crown sheen", x=400, y=312, width=180, height=64,
        fill="#FFFFFF", opacity=18, stroke=NONE)
d.path("M336,430 C330,496 342,556 372,604", "Cheek edge shade", fill=NONE,
       stroke="#C81E78", strokeWidth=15, opacity=35, cap="round")
d.path("M636,430 C646,492 640,552 614,600", "Far cheek shade", fill=NONE,
       stroke="#8A0E60", strokeWidth=13, opacity=30, cap="round")

# rosettes: neon ring clusters wrapping crown, cheeks and shoulder
for i, (x, y, r, s) in enumerate([
        (430, 336, 17, 1), (502, 330, 15, 3), (570, 344, 16, 5),
        (388, 386, 14, 2), (468, 380, 13, 4), (548, 388, 14, 6), (614, 400, 13, 0),
        (360, 480, 15, 3), (352, 546, 14, 5), (382, 606, 15, 1),
        (636, 486, 14, 2), (628, 548, 13, 4), (600, 608, 14, 6)]):
    rosette(x, y, r, f"Head rosette {i+1}", seed=i)
for i, (x, y, r, s) in enumerate([
        (392, 668, 18, 2), (452, 700, 16, 4), (524, 706, 17, 1),
        (592, 686, 16, 5), (640, 726, 15, 3), (368, 742, 16, 0),
        (452, 776, 17, 5), (540, 780, 16, 2), (616, 792, 15, 4)]):
    rosette(x, y, r, f"Chest rosette {i+1}", seed=i)

# --- face ----------------------------------------------------------------------
# pale mask: muzzle patch drifting left of centre
d.path("M418,540 C428,514 456,500 482,500 C514,500 544,516 554,544 "
       "C564,574 554,612 528,630 C510,642 462,642 444,628 "
       "C420,610 410,574 418,540 Z",
       "Muzzle pad", fill=radO((0, "#FFE8C8", 88), (1, "#FFD8A8", 70)), stroke=NONE)
# eyes: amber, level stare; far eye slightly narrower
d.path("M382,470 C398,448 434,442 456,458 C452,484 424,496 398,490 "
       "C388,486 382,480 382,470 Z",
       "Eye near", fill=radO((0, AMBER, 100), (0.6, "#E08A12", 100), (1, "#8A5206", 100)),
       stroke=VIOLET, strokeWidth=5)
d.path("M398,458 C408,452 422,454 430,462 C432,478 424,488 412,488 "
       "C400,486 394,472 398,458 Z", "Pupil near", fill="#12060E", stroke=NONE)
d.shape("ellipse", "Glint near", x=404, y=460, width=8, height=8,
        fill="#FFF4D8", opacity=90, stroke=NONE)
d.path("M540,464 C552,448 580,444 598,456 C596,478 574,488 554,484 "
       "C546,480 540,474 540,464 Z",
       "Eye far", fill=radO((0, AMBER, 100), (0.6, "#E08A12", 100), (1, "#8A5206", 100)),
       stroke=VIOLET, strokeWidth=5)
d.path("M554,456 C562,451 574,453 580,460 C582,473 576,482 566,482 "
       "C556,480 551,468 554,456 Z", "Pupil far", fill="#12060E", stroke=NONE)
d.shape("ellipse", "Glint far", x=559, y=458, width=7, height=7,
        fill="#FFF4D8", opacity=90, stroke=NONE)
# radiating ringlets behind each eye — the hypnotic stare
for k in range(2):
    d.path(poly(arc_pts(419, 470, 62 + k * 18, 150, 320)),
           f"Eye halo near {k+1}", fill=NONE, stroke=CYAN if k == 0 else PINK,
           strokeWidth=4, opacity=55, cap="round")
    d.path(poly(arc_pts(569, 464, 56 + k * 16, 210, 380)),
           f"Eye halo far {k+1}", fill=NONE, stroke=CYAN if k == 0 else PINK,
           strokeWidth=4, opacity=50, cap="round")
# brow folds
d.path("M374,448 C394,428 436,424 460,442", "Brow near", fill=NONE,
       stroke="#C81E78", strokeWidth=9, opacity=70, cap="round")
d.path("M534,444 C550,428 584,426 602,440", "Brow far", fill=NONE,
       stroke="#C81E78", strokeWidth=8, opacity=60, cap="round")
# nose, philtrum, the level mouth
d.path("M452,516 C464,508 496,508 510,516 C518,532 514,550 500,558 "
       "C488,564 470,564 458,558 C444,550 444,532 452,516 Z",
       "Nose", fill=lin(452, 508, 510, 562, (0, "#E83E6E"), (1, "#8A0E48")),
       stroke=VIOLET, strokeWidth=4.5)
d.path("M458,546 C454,538 458,530 466,528 C472,530 474,538 470,544 "
       "C466,549 460,549 458,546 Z", "Nostril n", fill="#3E0A28", stroke=NONE)
d.path("M502,546 C506,538 502,530 494,528 C488,530 486,538 490,544 "
       "C494,549 500,549 502,546 Z", "Nostril f", fill="#3E0A28", stroke=NONE)
d.path("M480,564 L480,580", "Philtrum", fill=NONE, stroke=VIOLET,
       strokeWidth=4.5, cap="round")
d.path("M480,580 C456,588 432,588 414,584 M480,580 C504,588 528,588 546,584",
       "Mouth", fill=NONE, stroke=VIOLET, strokeWidth=5, cap="round")
# whisker pits + sparse glowing whiskers
for i, (x, y) in enumerate([(434, 552), (428, 570), (436, 588), (450, 562),
                            (446, 580), (528, 552), (534, 570), (526, 588),
                            (514, 562), (518, 580)]):
    d.shape("ellipse", f"Whisker pit {i+1}", x=x - 3, y=y - 2.5,
            width=6, height=5, fill="#8A0E48", opacity=60, stroke=NONE)
for i, (x1, y1, x2, y2) in enumerate([(428, 556, 322, 536), (426, 574, 314, 574),
                                      (430, 590, 328, 610), (532, 556, 640, 536),
                                      (534, 574, 648, 574), (530, 590, 634, 610)]):
    d.path(f"M{x1},{y1} Q{(x1+x2)/2},{min(y1,y2)-8} {x2},{y2}", f"Whisker {i+1}",
           fill=NONE, stroke="#C8F8F0", strokeWidth=2.5, opacity=45, cap="round")

# --- lettering -------------------------------------------------------------------
def arc_text(word, cx, cy, radius, span_deg, size, font, label):
    n = len(word)
    for i, ch in enumerate(word):
        th = math.radians(-90 + (i - (n - 1) / 2) * span_deg)
        x = cx + radius * math.cos(th)
        y = cy + radius * math.sin(th)
        rot = math.degrees(th) + 90
        ghost = d.text(ch, f"{label} ghost {i+1}", x=x + 5, y=y + 5, size=size,
                       font=font, color=CYAN, justify="center")
        if ghost:
            d.cmd("object.rotate", f"{label} ghost rot {i+1}",
                  ids=[ghost["id"]], angle=rot, origin=[x + 5, y + 5])
        r = d.text(ch, f"{label} {i+1}", x=x, y=y, size=size, font=font,
                   color=YELLOW, justify="center")
        if r:
            d.call("set_paint", {"ids": [r["id"]], "stroke": PINK,
                                 "strokeWidth": 3.5}, f"{label} stroke {i+1}")
            d.cmd("object.rotate", f"{label} rot {i+1}",
                  ids=[r["id"]], angle=rot, origin=[x, y])

arc_text("JAGUAR", 500, 780, 620, 9.4, 120, "Virelai Sans", "Title")

sub = d.text("PANTHERA ONCA", "Subline", x=500, y=916, size=30,
             font="Source Sans 3", color="#BFEBF5", justify="center")
if sub:
    d.cmd("text.setStyle", "Subline tracking", ids=[sub["id"]], tracking=240)

d.finish("jaguar-V2R00")
