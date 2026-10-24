#!/usr/bin/env python3
"""Red fox — field-guide plate V1R00. Seated in profile on a drift, the brush
wrapped around its feet: rust-red punctuation in a field of snow. Behind it a
first-frost hedgerow — bare hawthorn canes hung with red haws and rime — under
a cold dawn plate. Breath ghosting from the muzzle. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Red Fox — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#2A140A"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def quad(p0, p1, p2, t):
    u = 1 - t
    return (u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0],
            u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1])

def ribbon_pts(p0, p1, p2, w0, w1, n=20):
    """Edge points of a tapered strip along a quadratic."""
    L, Rr = [], []
    for k in range(n + 1):
        t = k / n
        x, y = quad(p0, p1, p2, t)
        xa, ya = quad(p0, p1, p2, max(0, t - 0.01))
        xb, yb = quad(p0, p1, p2, min(1, t + 0.01))
        dx, dy = xb - xa, yb - ya
        ln = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x - dy/ln * w, y + dx/ln * w))
        Rr.append((x + dy/ln * w, y - dx/ln * w))
    return L, Rr

def ribbon(p0, p1, p2, w0, w1, label, n=20, **kw):
    L, Rr = ribbon_pts(p0, p1, p2, w0, w1, n)
    s = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    s += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    return d.path(s, label, **kw)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0E1826"), (1, "#04070D"))
PLATE_GRAD = rad((0, "#DCE6EE"), (0.55, "#AABCCD"), (1, "#53667E"))
SNOW_GRAD = lin(0, 730, 0, 880, (0, "#EEF3F8"), (1, "#AFBDCC"))
COAT = lin(0, 340, 0, 750, (0, "#CC7C3C"), (0.5, "#A85422"), (1, "#6B2E12"))
DARKFUR = lin(0, 280, 0, 700, (0, "#57301C"), (1, "#2E1608"))
CREAM = rad((0, "#F8EFDE"), (1, "#D8C4A2"))

# --- backdrop + first-frost plate ---------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#AABCCD", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#33445A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EAF0F6", strokeWidth=3, opacity=40)
# thin dawn band low on the left horizon — first light through the hedge
d.path("M140,600 C230,588 330,588 420,598 C330,608 230,610 140,600 Z",
       "Dawn band", fill="#F0C898", opacity=15, stroke=NONE)
# falling snow
for i, (x, y, w) in enumerate([(215,250,4),(330,170,5),(455,140,4),(585,132,5),(710,185,4),
                               (800,275,4),(170,355,5),(845,405,4),(255,455,4),(690,315,3),
                               (370,320,3),(545,215,3),(190,520,4),(855,525,3),(430,545,3),
                               (620,420,4),(765,470,3),(300,600,3)]):
    assert on_disc(x, y, 14), (x, y)
    d.shape("ellipse", f"Snow {i+1}", x=x, y=y, width=w, height=w, fill="#FFFFFF", opacity=70, stroke=NONE)

# drift floor: soughing top edge, bottom closes on the disc arc
ly = 745
ldx = math.sqrt(R * R - (ly - CY) ** 2)
d.path(f"M{CX-ldx:.1f},{ly} C310,726 430,740 530,734 C630,728 710,738 {CX+ldx:.1f},{ly} "
       f"A{R},{R} 0 0 1 {CX-ldx:.1f},{ly} Z", "Drift", fill=SNOW_GRAD, stroke=NONE)
d.path(f"M{CX-ldx+8:.1f},{ly-2} C310,724 430,736 530,730 C630,724 710,734 {CX+ldx-8:.1f},{ly-2}",
       "Drift light", fill=NONE, stroke="#FFFFFF", strokeWidth=4, opacity=45, cap="round")

# --- hedgerow: bare hawthorn canes, rime on the tops, red haws -----------------
HEDGE_INK = "#241812"
def cane(pts, w, label, op=88):
    d.path("M{} ,{}".format(*pts[0]).replace(" ", "") +
           " " + " ".join(f"L{x},{y}" for x, y in pts[1:]),
           label, fill=NONE, stroke=HEDGE_INK, strokeWidth=w, opacity=op, cap="round")

# left tangle, well below the muzzle line
cane([(176,748),(184,700),(178,652),(196,608)], 7, "L cane 1")
cane([(196,608),(216,582),(244,570)], 4, "L twig 1a")
cane([(196,608),(182,584),(168,566)], 4, "L twig 1b")
cane([(216,748),(222,706),(238,668),(262,640)], 6, "L cane 2")
cane([(262,640),(290,624),(316,622)], 4, "L twig 2a")
cane([(262,640),(252,614),(238,598)], 4, "L twig 2b")
cane([(258,748),(264,714),(282,684)], 5, "L cane 3")
cane([(282,684),(306,668),(330,668)], 3.5, "L twig 3a")
# right tangle, beside the rump
cane([(780,748),(776,700),(786,648),(772,600)], 7, "R cane 1")
cane([(772,600),(754,576),(732,568)], 4, "R twig 1a")
cane([(772,600),(792,578),(810,566)], 4, "R twig 1b")
cane([(742,748),(738,712),(722,678),(700,656)], 6, "R cane 2")
cane([(700,656),(676,644),(654,646)], 4, "R twig 2a")
cane([(700,656),(708,630),(704,608)], 4, "R twig 2b")
cane([(818,748),(822,712),(836,682),(830,650)], 5, "R cane 3")
cane([(830,650),(848,634),(862,634)], 3.5, "R twig 3a")
cane([(758,748),(768,724),(788,704),(812,696)], 4, "R cross twig")
# hedge foot: a dark welt along the drift crest behind the fox
d.path(f"M{CX-ldx+6},742 C260,726 330,720 400,724 C470,728 560,722 640,726 C700,729 {CX+ldx-8},736 {CX+ldx-4},740",
       "Hedge foot", fill=NONE, stroke=HEDGE_INK, strokeWidth=10, opacity=60, cap="round")
# rime on the branch tops
for i, dd in enumerate(["M178,652 C186,636 192,622 196,610",
                        "M238,668 C250,654 262,644 274,636",
                        "M776,648 C780,632 780,616 772,602",
                        "M722,678 C712,668 704,660 700,656"]):
    d.path(dd, f"Rime {i+1}", fill=NONE, stroke="#EAF2F8", strokeWidth=3.5, opacity=55, cap="round")
# haws: clusters of red berries on the twigs — little echoes of the fox
for i, (x, y, w) in enumerate([(214,586,9),(228,578,8),(172,570,8),(252,618,8),(268,628,9),
                               (306,664,8),(322,662,7),(750,566,9),(736,560,7),(806,570,8),
                               (794,578,7),(704,650,8),(720,642,7),(852,630,8),(840,640,7)]):
    assert on_disc(x, y, 16), (x, y)
    d.shape("ellipse", f"Haw {i+1}", x=x, y=y, width=w, height=w*1.15,
            fill=rad((0, "#C44830"), (1, "#7C1F10")), stroke=NONE)
# frost glints in the hedge
for i, (x, y) in enumerate([(200,640),(240,690),(290,700),(720,690),(760,640),(800,700)]):
    d.shape("ellipse", f"Frost glint {i+1}", x=x, y=y, width=4, height=4,
            fill="#FFFFFF", opacity=80, stroke=NONE)

# --- fox: seated in profile, nose left, brush wrapped round the feet -----------
# ears first: bases get buried by the silhouette so they grow out of the skull
d.path("M452,358 C458,326 468,300 482,280 C496,302 506,326 512,352 "
       "C494,362 470,364 452,358 Z",
       "Ear far", fill=DARKFUR, stroke=INK, strokeWidth=5)
d.path("M390,368 C398,328 410,294 428,262 C444,288 458,318 468,346 "
       "C448,362 418,370 390,368 Z",
       "Ear near", fill=COAT, stroke=INK, strokeWidth=5)

# the brush first: its root end tucks behind the rump so it reads as the tail
# sweeping round onto the floor in front of the feet — a hand-drawn plump
# crescent, not a ribbon, so there are no cap edges to hide
d.path("M676,724 C640,736 590,748 548,756 C520,762 496,768 478,776 "
       "C468,782 468,792 480,798 C500,808 540,814 590,814 "
       "C636,814 676,806 700,786 C714,772 712,750 700,738 "
       "C694,728 684,724 676,724 Z",
       "Brush", fill=COAT, stroke=INK, strokeWidth=5)
# white tag hugging the brush outline, scalloped parting where the rust gives
d.path("M574,748 C564,760 560,774 566,788 C572,800 584,808 598,812 "
       "C566,816 528,810 506,798 C492,790 482,782 478,776 "
       "C486,768 498,762 512,758 C532,754 554,750 574,748 Z",
       "Brush tag", fill=CREAM, opacity=95, stroke=NONE)
# guard strokes following the brush
for i, dd in enumerate(["M600,752 C630,744 656,738 678,736",
                        "M620,780 C644,790 664,790 682,782",
                        "M530,786 C548,792 566,792 580,786"]):
    d.path(dd, f"Brush fur {i+1}", fill=NONE, stroke="#5A2A10", strokeWidth=3.5, opacity=45, cap="round")

# one silhouette: nose tip → crown → neck → back → haunch → seat → paws → chest → jaw
SILH = ("M308,418 C322,400 344,386 372,376 C390,368 408,361 426,357 "
        "C444,354 460,357 472,366 C488,376 502,386 516,398 "
        "C560,414 612,462 648,540 C676,604 686,664 674,708 "
        "C668,730 650,742 628,746 C600,750 568,749 546,745 "
        "C516,743 482,744 456,741 C444,747 430,747 422,741 "
        "C413,734 411,724 414,712 L417,696 "
        "C412,656 411,616 418,578 C422,548 430,520 442,498 "
        "C432,478 410,462 386,454 C364,448 344,444 330,436 "
        "C319,430 312,425 308,418 Z")
d.path(SILH, "Fox", fill=COAT, stroke=INK, strokeWidth=6)
# shadow where the brush tucks under the rump
d.path("M662,742 C674,756 682,772 684,788", "Brush root shade",
       fill=NONE, stroke="#3A1C0C", strokeWidth=6, opacity=40, cap="round")
# ear details on the visible part
d.path("M414,348 C418,322 424,300 432,282 C441,300 448,320 452,338 "
       "C440,348 424,350 414,348 Z",
       "Ear inner", fill="#1E0F08", opacity=80, stroke=NONE)
d.path("M402,344 C407,318 415,294 427,272", "Ear frost rim",
       fill=NONE, stroke="#EAF2F8", strokeWidth=3, opacity=45, cap="round")
d.path("M462,326 C468,308 474,294 482,284", "Ear far rim",
       fill=NONE, stroke="#EAF2F8", strokeWidth=2.5, opacity=35, cap="round")

# dark saddle down the back and over the haunch
d.path("M506,392 C556,410 610,458 644,534 C670,596 680,656 668,700 "
       "C664,646 650,590 622,534 C594,480 552,434 500,406 Z",
       "Saddle", fill=DARKFUR, opacity=65, stroke=NONE)
for i, dd in enumerate(["M560,450 C584,488 606,534 620,584",
                        "M596,500 C616,542 630,588 634,632",
                        "M526,440 C552,474 574,516 588,560"]):
    d.path(dd, f"Guard hair {i+1}", fill=NONE, stroke="#3A1C0C", strokeWidth=4, opacity=40, cap="round")

# cream shirtfront: chin → throat → down the chest, dissolving at the foreleg
d.path("M378,456 C368,478 372,502 390,520 C382,540 382,566 396,586 "
       "C412,606 434,612 452,604 C466,596 472,578 468,558 "
       "C462,532 448,508 428,490 C412,474 394,462 378,456 Z",
       "Shirtfront", fill=CREAM, opacity=92, stroke=NONE)
for i, dd in enumerate(["M398,540 C414,548 432,550 446,544",
                        "M394,576 C412,586 432,588 448,582"]):
    d.path(dd, f"Bib fur {i+1}", fill=NONE, stroke="#B89C76", strokeWidth=3.5, opacity=50, cap="round")

# foreleg stockings: dark columns, the far leg hinted behind
d.path("M424,690 C428,660 430,630 428,604 C440,612 448,630 448,652 "
       "C448,672 444,692 436,706 C431,702 426,696 424,690 Z",
       "Far foreleg", fill=DARKFUR, opacity=70, stroke=NONE)
d.path("M414,712 L417,696 C413,660 412,624 418,590 C424,584 432,584 438,590 "
       "C434,624 433,660 437,696 L438,720 C437,734 430,742 422,741 "
       "C414,736 412,724 414,712 Z",
       "Near foreleg", fill=DARKFUR, opacity=85, stroke=NONE)
d.path("M414,724 C420,730 430,730 437,724", "Paw line",
       fill=NONE, stroke=INK, strokeWidth=3, opacity=70, cap="round")

# muzzle shading: darker bridge, pale lower jaw
d.path("M314,414 C332,398 356,386 382,380 C372,394 356,408 340,418 "
       "C330,424 318,422 314,414 Z",
       "Muzzle bridge", fill=DARKFUR, opacity=45, stroke=NONE)
# nose leather, tucked onto the muzzle tip
d.path("M298,416 C294,405 300,396 311,394 C322,392 331,399 331,410 "
       "C331,421 322,429 311,428 C304,427 300,423 298,416 Z",
       "Nose", fill=rad((0, "#3A2A22"), (1, "#120906")), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose glint", x=303, y=399, width=8, height=5, fill="#FFFFFF", opacity=40, stroke=NONE)
# mouth + lip line
d.path("M318,436 C336,446 356,452 376,454", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M320,428 C326,432 332,434 338,434", "Lip corner",
       fill=NONE, stroke=INK, strokeWidth=3, cap="round")
# whisker dots
for i, (x, y) in enumerate([(330,430),(340,426),(336,436)]):
    d.shape("ellipse", f"Whisker dot {i+1}", x=x, y=y, width=3, height=3, fill=INK, opacity=60, stroke=NONE)

# the eye: amber, level, a little wary — set low and forward
d.path("M364,410 C376,396 400,394 416,404 C404,420 378,424 364,410 Z",
       "Eye", fill=rad((0, "#EBB040"), (0.6, "#B27E20"), (1, "#6E4A10")),
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil", x=390, y=401, width=10, height=14, fill="#0E0A04", stroke=NONE)
d.shape("ellipse", "Glint", x=393, y=404, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M362,407 C376,393 402,391 418,401", "Upper lid",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path("M368,422 C382,428 400,426 412,418", "Lower lid light",
       fill=NONE, stroke="#F2E6CE", strokeWidth=3, opacity=50, cap="round")
d.path("M358,394 C378,382 404,380 424,388", "Brow",
       fill=NONE, stroke="#3A1C0C", strokeWidth=7, opacity=35, cap="round")

# breath ghosting from the muzzle — first-frost air
for i, (dd, op) in enumerate([("M296,422 C272,414 256,402 250,386 C246,374 250,362 260,356", 13),
                              ("M294,436 C272,434 256,426 246,412", 9)]):
    d.path(dd, f"Breath {i+1}", fill=NONE, stroke="#FFFFFF", strokeWidth=7, opacity=op, cap="round")

# haunch fur texture
for i, dd in enumerate(["M640,560 C652,590 656,624 650,656",
                        "M610,600 C622,630 626,664 618,694",
                        "M580,640 C590,668 592,698 584,722"]):
    d.path(dd, f"Haunch fur {i+1}", fill=NONE, stroke="#3A1C0C", strokeWidth=4, opacity=35, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0A1220", strokeWidth=6)

# --- name ---------------------------------------------------------------------
d.text("RED FOX", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#E8EEF4", justify="center")

d.finish("red-fox-V1R00")
