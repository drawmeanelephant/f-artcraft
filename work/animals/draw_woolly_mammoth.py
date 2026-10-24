#!/usr/bin/env python3
"""Woolly mammoth — field-guide plate V1R00. Full profile facing left, the
silhouette doing the talking: high shoulder hump, domed head, long sloping
back, a shaggy skirt of guard hair, the trunk hanging straight, and two huge
tusks that sweep down, out and curl back up like sled runners. Glacial plate,
faint aurora, blowing snow, breath fog at the trunk tip. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Woolly Mammoth — Field Plate", 1000, 1000)
rng = random.Random(23)

INK = "#241510"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0C1722"), (1, "#04080D"))
PLATE_GRAD = rad((0, "#E6EFF4"), (0.7, "#B0C7D3"), (1, "#6D8A9B"))
FUR_GRAD = rad((0, "#8A6240"), (0.6, "#54381F"), (1, "#28180C"))
TUSK_GRAD = lin(300, 520, 300, 700, (0, "#F7EFDC"), (0.6, "#E4D3AC"), (1, "#C3A87C"))
TUSK_FAR = lin(320, 500, 320, 660, (0, "#D8C8A4"), (1, "#9C8460"))
SNOW_GRAD = lin(0, 720, 0, 880, (0, "#F6FBFE"), (1, "#B4CCDB"))
TRUNK_GRAD = lin(300, 440, 320, 670, (0, "#7A5638"), (1, "#3A2412"))

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

def ribbon_pts(p0, p1, p2, p3, w0, w1, n=24):
    """Edge points of a tapered strip along a cubic bezier."""
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

# --- backdrop + glacial plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#AFC7D3", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#42657A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0F8FC", strokeWidth=3, opacity=55)

# faint aurora bands high in the plate (endpoints kept inside the disc)
A1 = [(196, 210), (360, 150), (560, 155), (730, 175)]
A2 = [(210, 265), (380, 215), (580, 220), (750, 240)]
assert all(on_disc(x, y, 20) for x, y in A1 + A2), (A1, A2)
d.path("M%d,%d C%d,%d %d,%d %d,%d C770,180 795,195 806,215" % tuple(p for pt in A1 for p in pt),
       "Aurora 1", fill=NONE, stroke="#8FE0BC", strokeWidth=26, opacity=13, cap="round")
assert on_disc(806, 215, 20)
d.path("M%d,%d C%d,%d %d,%d %d,%d" % tuple(p for pt in A2 for p in pt),
       "Aurora 2", fill=NONE, stroke="#9AD8E8", strokeWidth=16, opacity=11, cap="round")
# blowing snow streaks
for i, dd in enumerate(["M170,300 C330,278 520,278 700,302",
                        "M240,365 C400,344 580,344 740,368"]):
    d.path(dd, f"Wind streak {i+1}", fill=NONE, stroke="#EAF5FB",
           strokeWidth=5, opacity=20, cap="round")
# distant flakes behind the animal
for i, (x, y, w) in enumerate([(200,300,7),(770,260,6),(160,470,8),(830,440,7),(250,170,6),(720,160,7),
                               (400,130,6),(600,125,7),(140,580,6),(860,560,6),(330,215,5),(680,235,5)]):
    assert on_disc(x + w / 2, y + w / 2, 8), (x, y)
    d.shape("ellipse", f"Back flake {i+1}", x=x, y=y, width=w, height=w,
            fill="#F4FAFD", opacity=55, stroke=NONE)

# --- snowdrift floor, closing on the disc's own arc --------------------------------
d.path("M194,748 C380,730 620,730 806,748 A420,420 0 0 1 194,748 Z",
       "Snowdrift", fill=SNOW_GRAD, stroke="#8FACC0", strokeWidth=4)
d.path("M240,760 C380,750 620,750 760,762", "Drift shade", fill=NONE,
       stroke="#9FBDD0", strokeWidth=5, opacity=40, cap="round")

# --- far tusk: the wider, darker sweep behind --------------------------------------
ribbon((365, 500), (212, 552), (176, 690), (262, 606), 27, 5,
       "Tusk far", fill=TUSK_FAR, stroke=INK, strokeWidth=4)

# --- far legs (darker, tucked under the skirt) --------------------------------------
d.path("M436,640 C432,680 432,724 436,764 C438,774 452,776 458,768 "
       "C462,724 462,682 458,646 Z", "Front leg far", fill="#2C1C0E", stroke=NONE)
d.path("M648,646 C646,684 646,726 650,766 C652,776 666,778 672,770 "
       "C676,726 674,686 670,650 Z", "Hind leg far", fill="#2C1C0E", stroke=NONE)

# === body mass: hump, dome head, sloping back, ragged hem ============================
BODY = ("M314,432 "
        "C300,402 308,368 334,348 "        # brow rising to the dome
        "C372,322 420,312 466,318 "        # dome into the shoulder hump
        "C540,320 612,352 664,394 "        # long back sloping to the rump
        "C702,424 722,474 720,524 "        # rump rounding down
        "C718,578 710,616 698,640 "        # rear edge into the hem
        "L682,632 L670,662 L654,640 L638,670 L620,646 L604,674 L586,650 "
        "L570,678 L550,654 L534,680 L514,658 L498,682 L478,660 L462,684 "
        "L442,662 L428,680 L410,658 L396,674 L380,652 L366,668 L352,648 L340,662 "
        "C334,640 334,610 340,586 "        # chest front rising
        "C318,570 306,546 302,518 "        # throat under the jaw
        "C296,488 298,458 314,432 Z")      # face front, gently convex, to the brow
d.path(BODY, "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=7)

# snow dusting along the hump and back
for i, dd in enumerate(["M360,332 C420,314 500,312 560,326",
                        "M330,352 C360,340 400,332 440,330",
                        "M580,340 C620,356 656,382 682,414"]):
    d.path(dd, f"Back snow {i+1}", fill=NONE, stroke="#F4FAFD",
           strokeWidth=7, opacity=32, cap="round")

# long guard-hair strands falling from mid-body to the hem
for i in range(30):
    x = 370 + i * 11 + rng.uniform(-3, 3)
    y0 = rng.uniform(470, 540)
    y1 = rng.uniform(640, 680)
    col = rng.choice(["#160D06", "#160D06", "#6E5238", "#442E1A"])
    d.path(f"M{x:.0f},{y0:.0f} C{x+rng.uniform(-6,6):.0f},{(y0+y1)/2:.0f} "
           f"{x+rng.uniform(-8,8):.0f},{y1-30:.0f} {x+rng.uniform(-6,6):.0f},{y1:.0f}",
           f"Hair strand {i+1}", fill=NONE, stroke=col,
           strokeWidth=3, opacity=rng.randint(28, 48), cap="round")
# flank shade + hump light
d.shape("ellipse", "Flank shade", x=560, y=480, width=170, height=190,
        fill="#120A04", opacity=22, stroke=NONE)
d.shape("ellipse", "Hump light", x=390, y=330, width=180, height=80,
        fill="#B98A5C", opacity=20, stroke=NONE)

# --- near legs under the skirt -------------------------------------------------------
d.path("M378,644 C372,684 372,726 376,764 C378,776 398,778 408,768 "
       "C414,724 414,682 410,648 Z", "Front leg", fill="#38220F",
       stroke=INK, strokeWidth=4)
d.path("M594,650 C590,688 590,728 596,766 C598,777 618,779 628,770 "
       "C632,726 630,686 626,652 Z", "Hind leg", fill="#38220F",
       stroke=INK, strokeWidth=4)
# toes sink into the snow
d.shape("ellipse", "Front foot drift", x=376, y=760, width=44, height=14,
        fill="#E9F3F9", opacity=40, stroke=NONE)
d.shape("ellipse", "Hind foot drift", x=594, y=762, width=46, height=14,
        fill="#E9F3F9", opacity=40, stroke=NONE)

# --- near tusk: the sled-runner curl --------------------------------------------------
TUSK_P = [(358, 515), (225, 580), (196, 718), (300, 585)]
ribbon(*TUSK_P, 40, 6, "Tusk near", fill=TUSK_GRAD, stroke=INK, strokeWidth=5)
# ivory growth lines
TL, TR = ribbon_pts(*TUSK_P, 40, 6)
for i, t in enumerate([0.22, 0.4, 0.58, 0.74]):
    k = round(t * 24)
    d.path(f"M{TL[k][0]:.0f},{TL[k][1]:.0f} L{TR[k][0]:.0f},{TR[k][1]:.0f}",
           f"Tusk band {i+1}", fill=NONE, stroke="#A98F60",
           strokeWidth=3, opacity=30, cap="round")
# tusk tip glint
d.path("M282,610 C288,600 295,592 300,585", "Tusk tip light", fill=NONE,
       stroke="#FDF8EA", strokeWidth=4, opacity=55, cap="round")

# --- trunk: hanging from the face, tip curling inward --------------------------------
ribbon((334, 442), (302, 536), (304, 630), (340, 660), 38, 15,
       "Trunk", fill=TRUNK_GRAD, stroke=INK, strokeWidth=5)
# trunk ridges
for i, t in enumerate([0.3, 0.5, 0.68, 0.85]):
    x, y = cubic((334, 442), (302, 536), (304, 630), (340, 660), t)
    d.path(f"M{x-14:.0f},{y:.0f} C{x-4:.0f},{y+5:.0f} {x+8:.0f},{y+5:.0f} {x+14:.0f},{y-2:.0f}",
           f"Trunk ridge {i+1}", fill=NONE, stroke="#241408",
           strokeWidth=3, opacity=50, cap="round")

# --- head details ----------------------------------------------------------------------
# ear: a small flap behind the eye, half-buried in hair
d.path("M436,408 C460,398 484,406 490,424 C482,442 456,446 444,434 "
       "C436,426 434,416 436,408 Z", "Ear", fill="#3E2812",
       stroke=INK, strokeWidth=3.5)
for i, dd in enumerate(["M432,402 C426,420 426,436 432,450",
                        "M446,398 C442,416 442,432 448,444",
                        "M462,396 C458,412 458,428 464,438"]):
    d.path(dd, f"Ear hair {i+1}", fill=NONE, stroke="#241408",
           strokeWidth=4, opacity=55, cap="round")
# eye: deep-set, watchful
d.shape("ellipse", "Eye socket", x=378, y=416, width=40, height=38,
        fill="#1C1008", opacity=55, stroke=NONE)
d.shape("ellipse", "Eye", x=388, y=424, width=20, height=19,
        fill="#0E0804", stroke=NONE)
d.shape("ellipse", "Eye glint", x=392, y=428, width=6, height=6,
        fill="#FFFFFF", opacity=80, stroke=NONE)
# brow hair spilling over the eye
for i, dd in enumerate(["M356,398 C352,416 354,434 362,448",
                        "M378,392 C376,410 380,428 388,440"]):
    d.path(dd, f"Brow hair {i+1}", fill=NONE, stroke="#1C1006",
           strokeWidth=5, opacity=50, cap="round")
# mouth hint under the tusk root
d.path("M330,548 C346,556 364,556 378,548", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, opacity=70, cap="round")

# --- breath fog at the trunk tip -------------------------------------------------------
d.shape("ellipse", "Breath 1", x=290, y=660, width=64, height=40,
        fill="#F0F7FB", opacity=20, stroke=NONE)
d.shape("ellipse", "Breath 2", x=258, y=684, width=84, height=48,
        fill="#F0F7FB", opacity=14, stroke=NONE)

# --- foreground flakes ------------------------------------------------------------------
for i, (x, y, w) in enumerate([(300,260,8),(660,310,7),(240,660,7),(760,630,8),(480,340,6),
                               (180,690,6),(820,340,7),(560,150,6),(380,790,5),(640,790,6)]):
    assert on_disc(x + w / 2, y + w / 2, 6), (x, y)
    d.shape("ellipse", f"Front flake {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=70, stroke=NONE)

# plate rim on top so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#1B2E3A", strokeWidth=6)

# --- name ------------------------------------------------------------------------------
d.text("WOOLLY MAMMOTH", "Name", x=500, y=962, size=56, font="Virelai Sans",
       color="#E4EFF6", justify="center")

d.finish("woolly-mammoth-V1R00")
