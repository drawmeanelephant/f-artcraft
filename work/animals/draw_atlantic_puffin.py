#!/usr/bin/env python3
"""Atlantic puffin — field plate V1R00. Upright profile facing right on a wet
sea-cliff ledge, the great triangular bill closed on a silver catch of sand
eels. Black cap and back, white cheek and belly, banded bill, orange feet.
Sea-cliff plate — grey sea behind, spray at the rock line, the ledge closing
on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Atlantic Puffin — Field Plate", 1000, 1000)
rng = random.Random(53)

PCX, PCY, PR = 500, 460, 420
INK = "#14100E"   # warm near-black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def radO(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def disc_x(y, side):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0A141C"), (1, "#020608"))
PLATE_GRAD = rad((0, "#5E7E88"), (0.55, "#344E58"), (1, "#12242C"))
SEA_GRAD   = lin(0, 560, 0, 880, (0, "#46686F"), (0.5, "#2A444C"), (1, "#14262C"))
ROCK_GRAD  = lin(0, 700, 0, 880, (0, "#3E4145"), (1, "#16181C"))
BLACK_GRAD = rad((0, "#3A3E42"), (0.55, "#1E2124"), (1, "#0C0E10"))
WHITE_GRAD = lin(0, 400, 0, 720, (0, "#F6F8F2"), (0.6, "#E2E8E0"), (1, "#B8C4BC"))
FISH_GRAD  = lin(0, 460, 0, 600, (0, "#E2EAEC"), (0.5, "#AEC0C6"), (1, "#6E8890"))

# --- backdrop + sea-cliff plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#6E8E96", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1E343C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8DCE0", strokeWidth=3, opacity=30)

# pale cold light high in the plate, fading before the rim
d.shape("ellipse", "Sky glow", x=280, y=100, width=420, height=260,
        fill=radO((0, "#C8DCD8", 26), (0.6, "#C8DCD8", 10), (1, "#C8DCD8", 0)), stroke=NONE)
# dark scudding cloud band
for i, dd in enumerate(["M160,220 C360,196 600,202 830,230",
                        "M130,310 C340,292 620,296 860,318"]):
    d.path(dd, f"Cloud band {i+1}", fill=NONE, stroke="#16262C",
           strokeWidth=34, opacity=18, cap="round")
# distant gulls: two small marks kept inside the disc
for i, (x, y) in enumerate([(290, 250), (730, 210)]):
    assert on_disc(x, y, 15), (x, y)
    d.path(f"M{x - 12},{y} Q{x - 4},{y - 7} {x},{y} Q{x + 4},{y - 7} {x + 12},{y}",
           f"Gull {i+1}", fill=NONE, stroke="#1E3238", strokeWidth=3,
           opacity=55, cap="round")

# --- the sea: fills the disc below the horizon curve, closing on the arc -----------
hy = 560
hx0, hx1 = disc_x(hy, -1), disc_x(hy, 1)
d.path(f"M{hx0:.1f},{hy} C330,548 670,548 {hx1:.1f},{hy} "
       f"A{PR},{PR} 0 0 1 {hx0:.1f},{hy} Z", "Sea", fill=SEA_GRAD, stroke=NONE)
# horizon light
d.path(f"M{hx0 + 6:.1f},{hy} C330,548 670,548 {hx1 - 6:.1f},{hy}",
       "Horizon light", fill=NONE, stroke="#A8C8CC", strokeWidth=3, opacity=40, cap="round")
# wave crests running across the sea
for i, dd in enumerate(["M180,610 C300,600 420,606 480,612", "M560,640 C660,632 780,636 850,644",
                        "M140,690 C280,682 400,686 460,692", "M620,700 C720,694 820,698 880,704"]):
    d.path(dd, f"Wave crest {i+1}", fill=NONE, stroke="#9EBCC2",
           strokeWidth=4, opacity=30, cap="round")
# spray rising where the swell meets the rock
for i, (x, y, h) in enumerate([(230, 690, 60), (790, 684, 70), (170, 720, 45), (830, 726, 45)]):
    assert on_disc(x, y - h, 15), (x, y)
    d.path(f"M{x},{y} C{x - 6},{y - h * 0.4} {x + 4},{y - h * 0.7} {x - 4},{y - h}",
           f"Spray {i+1}", fill=NONE, stroke="#C8DEE0", strokeWidth=3.5,
           opacity=35, cap="round")
    d.shape("ellipse", f"Spray bead {i+1}", x=x - 8, y=y - h - 4, width=7, height=7,
            fill="#DCECEE", opacity=40, stroke=NONE)

# --- the ledge: wet rock floor closing on the disc's own arc ------------------------
fy = 745
fx0, fx1 = disc_x(fy, -1), disc_x(fy, 1)
d.path(f"M{fx0:.1f},{fy} C300,724 420,738 540,730 C660,722 760,734 {fx1:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fx0:.1f},{fy} Z", "Rock ledge", fill=ROCK_GRAD, stroke=NONE)
d.path(f"M{fx0 + 6:.1f},{fy} C300,724 420,738 540,730 C660,722 760,734 {fx1 - 6:.1f},{fy}",
       "Rock wet sheen", fill=NONE, stroke="#8E989E", strokeWidth=4, opacity=35, cap="round")
# rock strata + barnacle dots
for i, dd in enumerate(["M250,790 C380,780 560,784 700,792", "M320,830 C440,822 580,824 680,830"]):
    d.path(dd, f"Stratum {i+1}", fill=NONE, stroke="#22262A",
           strokeWidth=5, opacity=50, cap="round")
for i, (x, y) in enumerate([(300, 750), (380, 744), (650, 740), (720, 752)]):
    d.shape("ellipse", f"Barnacle {i+1}", x=x - 4, y=y - 3, width=8, height=6,
            fill="#8E9AA0", opacity=45, stroke=NONE)
# the bird's contact shadow on the ledge
d.shape("ellipse", "Puffin shadow", x=380, y=726, width=270, height=24,
        fill="#0A0C0E", opacity=38, stroke=NONE)

# === the puffin ====================================================================
# tail: the short dark point behind the stance
d.path("M420,650 C404,668 398,690 404,706 C418,700 428,684 432,664 Z",
       "Tail", fill="#14161A", stroke=INK, strokeWidth=3)

# feet: bright orange webs planted on the rock, set far back under the body
for sgn, lab in ((-1, "L"), (1, "R")):
    fx = 478 + sgn * 62
    d.path(f"M{fx - 36},744 C{fx - 32},728 {fx - 18},720 {fx - 2},722 "
           f"C{fx + 18},722 {fx + 34},730 {fx + 40},742 "
           f"C{fx + 24},750 {fx + 2},752 {fx - 14},750 "
           f"C{fx - 26},748 {fx - 34},746 {fx - 36},744 Z",
           f"Foot {lab}", fill=lin(0, 720, 0, 752, (0, "#F08E2E"), (1, "#C45814")),
           stroke=INK, strokeWidth=3)
    for k in (-1, 0, 1):
        d.path(f"M{fx - 4},{726} L{fx + k * 18},{744}", f"Toe web {lab}{k}",
               fill=NONE, stroke="#9E400E", strokeWidth=2, opacity=60, cap="round")

# body: the upright auk pear, black overall
BODY = ("M500,456 C452,458 422,486 410,530 C396,578 400,640 424,686 "
        "C444,722 486,738 530,734 C574,730 610,706 624,664 "
        "C636,626 634,572 618,528 C602,486 556,454 500,456 Z")
d.path(BODY, "Body", fill=BLACK_GRAD, stroke=INK, strokeWidth=6)
# back sheen down the left edge
d.path("M424,520 C410,570 412,630 432,680", "Back sheen", fill=NONE,
       stroke="#5E686E", strokeWidth=9, opacity=30, cap="round")

# white belly washing up the breast and belly
d.path("M510,470 C556,478 592,510 606,556 C618,598 614,650 594,686 "
       "C572,716 534,728 500,722 C520,680 528,620 524,560 "
       "C521,524 516,494 510,470 Z", "Belly", fill=WHITE_GRAD, stroke=NONE)
# a soft shadowed seam where black meets white down the breast
d.path("M522,486 C534,540 534,610 520,668", "Belly seam", fill=NONE,
       stroke="#8E989A", strokeWidth=4, opacity=30, cap="round")

# folded wing: dark teardrop on the back with a pale edge
d.path("M430,530 C452,512 486,512 506,534 C518,568 512,624 492,664 "
       "C474,690 448,694 434,676 C420,634 418,570 430,530 Z",
       "Wing", fill="#16181C", opacity=85, stroke=NONE)
d.path("M438,540 C430,590 434,640 448,672", "Wing sheen", fill=NONE,
       stroke="#5E686E", strokeWidth=5, opacity=30, cap="round")
d.path("M452,520 C478,514 500,524 510,544", "Wing edge", fill=NONE,
       stroke="#8E989E", strokeWidth=3, opacity=30, cap="round")

# --- head ---------------------------------------------------------------------------
HEAD = ("M506,336 C558,336 600,366 612,414 C620,446 614,478 596,500 "
        "C574,522 540,532 506,530 C470,528 442,510 430,482 "
        "C418,454 420,414 436,384 C452,354 476,336 506,336 Z")
d.path(HEAD, "Head", fill=BLACK_GRAD, stroke=INK, strokeWidth=5.5)
# crown sheen
d.shape("ellipse", "Crown sheen", x=452, y=344, width=100, height=36,
        fill="#6E7A80", opacity=25, stroke=NONE)

# the great white cheek: a soft triangle filling the face
d.path("M500,368 C540,362 578,380 596,414 C606,436 604,466 590,486 "
       "C570,506 536,514 508,508 C524,470 524,414 500,368 Z",
       "Cheek", fill=WHITE_GRAD, opacity=95, stroke=NONE)
# cheek shading along its lower edge
d.path("M512,486 C534,496 564,494 584,478", "Cheek shade", fill=NONE,
       stroke="#9EAAA6", strokeWidth=5, opacity=35, cap="round")

# the eye: dark bead in a grey teardrop, red ornament above
d.shape("ellipse", "Eye ring", x=528, y=412, width=30, height=30,
        fill="#8E9AA0", opacity=70, stroke=NONE)
d.shape("ellipse", "Eye", x=534, y=417, width=19, height=19, fill="#0C0E10", stroke=NONE)
d.shape("ellipse", "Eye glint", x=538, y=420, width=5, height=5,
        fill="#FFFFFF", opacity=85, stroke=NONE)
# the little red-orange triangles above and below the eye
d.path("M534,408 L542,398 L550,406 Z", "Eye flag up", fill="#D8562A",
       opacity=85, stroke=NONE)
d.path("M534,446 L542,454 L550,446 Z", "Eye flag down", fill="#D8562A",
       opacity=85, stroke=NONE)

# === the catch: sand eels hanging from the closed bill ==============================
# filled slim fish drawn before the bill so their heads tuck under it
for i, (x, bend, L) in enumerate([(700, -16, 96), (726, 4, 112), (748, 20, 90)]):
    y0 = 466
    tx, ty = x + bend * 0.5, y0 + L
    d.path(f"M{x - 5},{y0} C{x - 4 + bend * 0.4},{y0 + L * 0.35} {tx - 4},{y0 + L * 0.7} {tx},{ty} "
           f"C{tx + 3},{y0 + L * 0.7} {x + 6 + bend * 0.4},{y0 + L * 0.35} {x + 6},{y0} "
           f"C{x + 3},{y0 + 6} {x - 2},{y0 + 6} {x - 5},{y0} Z",
           f"Eel {i+1}", fill=FISH_GRAD, stroke="#4E666E", strokeWidth=2)
    # tail fork
    d.path(f"M{tx},{ty} L{tx - 7},{ty + 13} L{tx},{ty + 8} L{tx + 7},{ty + 13} Z",
           f"Eel tail {i+1}", fill="#7E98A0", stroke="#4E666E", strokeWidth=1.5)
    # eye dot near the head
    d.shape("ellipse", f"Eel eye {i+1}", x=x - 1, y=y0 + 8, width=4, height=4,
            fill="#1E2A2E", opacity=80, stroke=NONE)
    # belly light down each eel
    d.path(f"M{x + 2},{y0 + 12} C{x + 2 + bend * 0.4},{y0 + L * 0.4} {tx + 1},{y0 + L * 0.7} "
           f"{tx + 1},{y0 + L - 8}",
           f"Eel light {i+1}", fill=NONE, stroke="#F2F8F8", strokeWidth=2.5,
           opacity=60, cap="round")

# === the bill: the deep laterally-compressed wedge, banded ===========================
# whole-bill silhouette first for the outline
d.path("M588,392 C630,382 680,394 722,424 C744,440 756,456 754,470 "
       "C736,478 706,480 676,476 C640,470 610,460 592,448 "
       "C584,430 584,410 588,392 Z",
       "Bill", fill="#7E96A4", stroke=INK, strokeWidth=4)
# blue-grey base triangle at the face
d.path("M590,396 C604,392 618,394 632,402 C636,420 634,438 626,452 "
       "C612,452 598,448 590,444 C584,428 584,410 590,396 Z",
       "Bill base", fill="#7E96A4", stroke="#2E3A42", strokeWidth=2.5)
# the soft yellow-orange mid band
d.path("M632,402 C662,398 696,410 722,428 C726,444 722,460 712,468 "
       "C690,466 660,460 626,452 C634,438 636,420 632,402 Z",
       "Bill mid", fill=lin(590, 400, 720, 470, (0, "#F0C23C"), (1, "#D8901E")),
       stroke="#8E5A10", strokeWidth=2)
# the red-orange tip
d.path("M722,428 C740,442 752,456 754,468 C742,474 726,476 712,468 "
       "C722,460 726,444 722,428 Z", "Bill tip", fill="#D84E22",
       stroke="#8E2E0E", strokeWidth=2)
# the gape line where the mandibles meet
d.path("M596,446 C636,456 690,464 738,462", "Gape", fill=NONE,
       stroke="#5E1010", strokeWidth=3, opacity=70, cap="round")
# culmen light along the top edge
d.path("M596,398 C640,388 692,402 734,434", "Culmen light", fill=NONE,
       stroke="#F4E8C0", strokeWidth=4, opacity=45, cap="round")

# spindrift drifting across the whole plate
for i, dd in enumerate(["M150,480 C300,462 480,466 620,486", "M640,340 C740,330 830,336 880,344"]):
    d.path(dd, f"Spindrift {i+1}", fill=NONE, stroke="#C8DEE0",
           strokeWidth=5, opacity=18, cap="round")

# plate rim on top so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#0C1A20", strokeWidth=6)
d.shape("ellipse", "Plate inner ring 2", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8DCE0", strokeWidth=3, opacity=28)

# --- name ---------------------------------------------------------------------------
r1 = d.text("ATLANTIC PUFFIN", "Name", x=500, y=962, size=54, font="Virelai Sans",
            color="#DCE8EA", justify="center")

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
b = find(layers, r1["id"])["bounds"]
print("name bounds", {k: round(v) for k, v in b.items()})
assert b["width"] <= 800 and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("atlantic-puffin-V1R00")
