#!/usr/bin/env python3
"""Tyrannosaurus rex — field-guide plate V1R00. Full profile mid-stride facing
left: the massive skull with the jaw dropped open, teeth like pitons, the
ridiculous two-clawed arm, one tree-trunk leg planted and the other folded up
behind, and the counterweight tail tapering to a whip. Badlands plate, dusty
sun, sedimentary strata for a floor — fossil-light mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Tyrannosaurus Rex — Field Plate", 1000, 1000)
rng = random.Random(7)

INK = "#2A1608"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#1C130C"), (1, "#0A0604"))
PLATE_GRAD = rad((0, "#F2E6C8"), (0.65, "#D2B98C"), (1, "#97764E"))
HIDE_GRAD = rad((0, "#9C6B42"), (0.55, "#6B4226"), (1, "#38200F"))
HEAD_GRAD = lin(200, 290, 360, 420, (0, "#A9764A"), (0.6, "#7A4E2A"), (1, "#4A2C14"))
BELLY = "#C9A274"
MOUTH = "#3A1410"
IVORY = lin(0, 340, 0, 400, (0, "#F6EDD6"), (1, "#CBB48A"))
GROUND_GRAD = lin(0, 720, 0, 880, (0, "#E8D5AC"), (1, "#A8845A"))

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

def ribbon_pts(p0, p1, p2, p3, w0, w1, n=24):
    L, R = [], []
    for k in range(n + 1):
        t = k / n
        x, y = cubic(p0, p1, p2, p3, t)
        x0, y0 = cubic(p0, p1, p2, p3, max(0, t - 0.01))
        x1, y1 = cubic(p0, p1, p2, p3, min(1, t + 0.01))
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x - dy/ln * w, y + dx/ln * w))
        R.append((x + dy/ln * w, y - dx/ln * w))
    return L, R

def ribbon(p0, p1, p2, p3, w0, w1, label, n=24, **kw):
    L, R = ribbon_pts(p0, p1, p2, p3, w0, w1, n)
    s = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    s += " " + " ".join("L%.1f,%.1f" % p for p in reversed(R)) + " Z"
    return d.path(s, label, **kw)

def tooth(x, y, w, h, label, flip=False):
    s = -1 if flip else 1
    d.path(f"M{x},{y} L{x+w},{y} L{x+w*0.45},{y+h*s} Z", label,
           fill=IVORY, stroke=INK, strokeWidth=1.5)

# --- backdrop + badlands plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#D2B98C", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E5232", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F8EFD8", strokeWidth=3, opacity=50)

# dusty sun low in the plate's upper right
d.shape("ellipse", "Sun halo", x=586, y=168, width=200, height=200,
        fill="#F8ECD0", opacity=14, stroke=NONE)
d.shape("ellipse", "Sun", x=622, y=204, width=128, height=128,
        fill="#F8ECD0", opacity=42, stroke=NONE)
# heat wisps
for i, dd in enumerate(["M190,330 C340,312 520,314 660,336",
                        "M240,410 C380,394 540,396 690,414"]):
    d.path(dd, f"Dust wisp {i+1}", fill=NONE, stroke="#EAD9B4",
           strokeWidth=5, opacity=18, cap="round")
# high cirrus flecks
for i, (x, y, w, h) in enumerate([(210,200,60,9),(640,140,80,10),(300,130,46,8),(720,250,54,8)]):
    d.shape("ellipse", f"Cirrus {i+1}", x=x, y=y, width=w, height=h,
            fill="#F4E8CC", opacity=20, stroke=NONE)

# --- sedimentary floor, closing on the disc's own arc --------------------------------
d.path("M200,742 C380,722 620,722 800,742 A420,420 0 0 1 200,742 Z",
       "Ground", fill=GROUND_GRAD, stroke="#8A6B44", strokeWidth=4)
# strata seams inside the ground mass
for i, dd in enumerate(["M232,766 C400,752 600,752 768,766",
                        "M272,796 C420,786 580,786 728,796",
                        "M330,824 C440,816 560,816 670,824"]):
    d.path(dd, f"Stratum {i+1}", fill=NONE, stroke="#8A6B44",
           strokeWidth=4, opacity=45, cap="round")
# pebbles
for i, (x, y, w) in enumerate([(300,758,10),(690,756,8),(430,772,7),(580,770,9),(360,806,8),(650,804,7)]):
    d.shape("ellipse", f"Pebble {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#96754C", opacity=55, stroke=NONE)

# === the animal =====================================================================
# --- tail: the counterweight, tapering to a whip --------------------------------------
ribbon((586, 372), (668, 384), (748, 414), (818, 446), 108, 5,
       "Tail", fill=HIDE_GRAD, stroke=INK, strokeWidth=6)

# --- far leg: folded up behind, foot off the ground -----------------------------------
d.path("M560,452 C590,470 610,502 614,536 C617,560 608,584 592,596 "
       "C588,610 588,624 594,636 L572,650 C560,632 558,612 564,594 "
       "C550,576 544,548 546,520 C548,492 552,468 560,452 Z",
       "Far leg", fill="#42280F", stroke=INK, strokeWidth=4)
# far foot dangling
d.path("M596,634 C588,646 574,652 560,654 C552,656 546,650 550,644 "
       "C560,638 572,632 584,628 C590,626 596,628 596,634 Z",
       "Far foot", fill="#4A2C14", stroke=INK, strokeWidth=3)
for i, (x, y) in enumerate([(558,650), (566,656), (575,656)]):
    d.path(f"M{x},{y} l-8,6", f"Far claw {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3, cap="round")

# --- torso -----------------------------------------------------------------------------
d.path("M352,330 C400,318 470,318 530,330 C585,340 625,368 640,404 "
       "C648,432 640,458 616,472 C585,488 520,494 465,486 "
       "C420,480 385,462 365,436 C348,414 342,388 346,364 "
       "C348,348 350,338 352,330 Z",
       "Torso", fill=HIDE_GRAD, stroke=INK, strokeWidth=6)
# belly light along the underside
d.path("M385,448 C430,472 510,480 580,468 C560,486 490,494 440,486 "
       "C412,480 392,466 385,448 Z", "Belly light",
       fill=BELLY, opacity=45, stroke=NONE)
# dorsal shade along the spine
d.path("M370,336 C430,322 520,324 590,344 C560,354 460,352 400,346 "
       "C385,343 375,340 370,336 Z", "Dorsal shade",
       fill="#2A1608", opacity=30, stroke=NONE)
# flank mottle + hip crease
for i, (x, y, w) in enumerate([(450,400,26),(510,415,22),(560,395,20),(480,440,16),(540,445,14)]):
    d.shape("ellipse", f"Flank mottle {i+1}", x=x, y=y, width=w, height=w*0.6,
            fill="#3A2010", opacity=25, stroke=NONE)
d.path("M560,390 C575,415 578,445 568,468", "Hip crease", fill=NONE,
       stroke="#2A1608", strokeWidth=4, opacity=40, cap="round")

# --- near leg: the planted tree-trunk -----------------------------------------------------
d.path("M500,440 C478,462 466,498 470,534 C473,560 484,584 500,600 "
       "C506,616 510,634 512,652 C514,664 528,668 538,660 "
       "C544,636 544,612 538,592 C552,568 558,534 552,502 "
       "C546,472 528,448 500,440 Z",
       "Near leg", fill=HIDE_GRAD, stroke=INK, strokeWidth=5)
# thigh muscle shade
d.path("M486,470 C476,500 476,540 488,570", "Thigh shade", fill=NONE,
       stroke="#2A1608", strokeWidth=8, opacity=30, cap="round")
# near foot: metatarsus angled forward, three toes planted
d.path("M522,650 C514,668 500,692 486,710 C476,722 466,729 456,733 "
       "L474,740 C505,745 540,744 562,737 C574,731 578,722 572,712 "
       "C560,694 546,670 538,654 Z",
       "Near foot", fill=HIDE_GRAD, stroke=INK, strokeWidth=5)
for i, (x, y) in enumerate([(458,735), (480,740), (508,742)]):
    d.path(f"M{x},{y} l-10,5", f"Near claw {i+1}", fill=NONE,
           stroke="#1E1004", strokeWidth=4, cap="round")
# toe creases
for i, (x1, x2) in enumerate([(474, 466), (500, 492), (528, 522)]):
    d.path(f"M{x1},724 L{x2},734", f"Toe crease {i+1}", fill=NONE,
           stroke="#2A1608", strokeWidth=3, opacity=50, cap="round")

# --- neck filling between head and torso ------------------------------------------------
d.path("M320,320 C350,318 380,326 400,346 C412,364 416,388 408,406 "
       "C394,424 372,432 352,426 C332,418 320,398 318,376 "
       "C316,354 316,336 320,320 Z",
       "Neck", fill=HIDE_GRAD, stroke=NONE)

# --- far arm: a claw peeking behind the chest -------------------------------------------
d.path("M408,448 C416,462 420,478 418,494 L404,498 C400,480 400,462 404,448 Z",
       "Far arm", fill="#4A2C14", stroke=INK, strokeWidth=3)

# === head: the great skull, jaw dropped ===================================================
# mouth interior first — the dark gape, open
d.path("M200,342 C240,334 300,340 348,364 C354,372 354,384 350,394 "
       "C330,408 288,410 258,400 C234,392 214,380 204,364 "
       "C198,354 198,348 200,342 Z",
       "Mouth", fill=MOUTH, stroke=NONE)

# lower jaw, dropped open around the hinge
d.path("M216,388 C252,394 306,394 346,380 C358,386 362,400 354,412 "
       "C338,428 300,432 266,424 C238,418 216,402 210,392 "
       "C208,388 211,386 216,388 Z",
       "Lower jaw", fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
d.path("M232,410 C264,420 312,420 344,408", "Jaw shade", fill=NONE,
       stroke="#3A2010", strokeWidth=5, opacity=45, cap="round")

# upper skull
d.path("M196,318 C228,296 266,288 300,291 C326,293 344,302 353,317 "
       "C360,330 358,346 349,358 L344,362 C300,352 254,352 226,354 "
       "C210,356 198,348 194,336 C191,328 191,323 196,318 Z",
       "Upper skull", fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
# snout top highlight
d.path("M206,318 C236,300 272,294 306,297", "Snout light", fill=NONE,
       stroke="#C89868", strokeWidth=6, opacity=50, cap="round")
# brow bump over the eye
d.path("M282,318 C300,310 322,312 334,322", "Brow", fill=NONE,
       stroke=INK, strokeWidth=5, opacity=60, cap="round")

# teeth: uppers hang from the gape edge, lowers rise to meet them
for i, x in enumerate([212, 232, 252, 272, 292, 312, 330]):
    tooth(x, 350 + i % 2 * 2, 12, 17 - i % 3 * 2, f"Tooth U{i+1}")
for i, (x, y) in enumerate([(228, 388), (250, 390), (272, 391), (294, 390), (316, 386)]):
    tooth(x, y, 11, -(14 - i % 2 * 3), f"Tooth L{i+1}")

# nostril + eye
d.shape("ellipse", "Nostril", x=214, y=318, width=16, height=11,
        fill="#241204", opacity=80, stroke=NONE)
d.shape("ellipse", "Eye socket", x=298, y=326, width=30, height=26,
        fill="#2A1608", opacity=45, stroke=NONE)
d.shape("ellipse", "Eye", x=304, y=330, width=16, height=15,
        fill="#140A04", stroke=NONE)
d.shape("ellipse", "Eye glint", x=308, y=333, width=5, height=5,
        fill="#FFE9C0", opacity=85, stroke=NONE)

# --- near arm: the ridiculous little limb ---------------------------------------------------
d.path("M398,444 C410,458 416,476 414,494 C412,504 402,508 394,502 "
       "C390,486 388,468 390,452 Z",
       "Near arm", fill=HIDE_GRAD, stroke=INK, strokeWidth=4)
for i, (x, y, dx, dy) in enumerate([(398, 502, -7, 8), (408, 502, -2, 10)]):
    d.path(f"M{x},{y} l{dx},{dy}", f"Arm claw {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3, cap="round")

# --- skin texture: scale speckles on the flank ----------------------------------------------
for i in range(14):
    x = rng.uniform(400, 620)
    y = rng.uniform(370, 470)
    w = rng.uniform(4, 8)
    d.shape("ellipse", f"Scale {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill=rng.choice(["#C99A6A", "#3A2010"]), opacity=30, stroke=NONE)

# plate rim on top so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#3A2812", strokeWidth=6)

# --- name ------------------------------------------------------------------------------------
d.text("TYRANNOSAURUS REX", "Name", x=500, y=962, size=50, font="Virelai Sans",
       color="#F2E4C2", justify="center")

d.finish("tyrannosaurus-rex-V1R00")
