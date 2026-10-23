#!/usr/bin/env python3
"""Dik-dik — field-guide plate V1R00. Full-body side profile facing left:
a miniature antelope no taller than a rabbit — huge dark eye, oversized
ears, the tiny elongated proboscis snout, a scruffy forehead crest hiding
two pin horns, and legs tapered to near-line weight. Warm tawny plate,
dusk-blue shadowing on the coat; the ground band closes on the disc's own
arc. 1000x1000. House style: gradients + translucent shading, never flat."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Dik-dik — Field Plate", 1000, 1000)

INK = "#3E2A1C"
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#241C2E"), (1, "#0D0908"))
PLATE_GRAD = rad((0, "#FBEDD0"), (0.68, "#E9C893"), (1, "#B08350"))
COAT_GRAD = rad((0, "#DCAE72"), (0.66, "#BC8850"), (1, "#8A5E34"))
NECK_GRAD = lin(440, 430, 540, 570, (0, "#D6A668"), (1, "#A06E3C"))
FAR_GRAD = lin(0, 600, 0, 800, (0, "#96683A"), (1, "#6E4826"))
EAR_GRAD = lin(455, 415, 535, 280, (0, "#C89458"), (1, "#DDB07A"))
EAR_FAR_GRAD = lin(480, 410, 555, 315, (0, "#A8794A"), (1, "#8A5E34"))
INNER_EAR_GRAD = lin(470, 400, 520, 300, (0, "#E8C39C"), (1, "#F6E4CC"))
EYE_GRAD = rad((0, "#4A3022"), (1, "#150C07"))
DUSK = "#4E5E80"                    # dusk-blue shadow accent
PALE = "#F6E8CC"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6438", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFF6E2", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=600, y=160, width=230, height=120, fill="#D9B47E", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=170, y=430, width=180, height=110, fill="#D9B47E", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(770,300,7),(830,470,8),(200,330,6),(160,500,8),(250,730,7),(740,690,8),
                               (855,560,6),(400,110,7),(610,118,6),(330,810,6),(690,240,5),(140,400,6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#A47A48", opacity=38, stroke=NONE)

# faint dusk-blue far hills + a tiny acacia, all inside the disc
d.path("M170,560 C240,540 320,536 400,548 C470,556 540,552 610,542",
       "Far hills", fill=NONE, stroke=DUSK, strokeWidth=10, opacity=20, cap="round")
d.path("M742,540 L746,500 L736,482 M746,500 L760,480", "Acacia trunk", fill=NONE,
       stroke="#7E5C38", strokeWidth=6, opacity=30, cap="round")
d.path("M700,486 C716,468 752,462 782,468 C800,472 806,482 800,490 "
       "C770,498 724,498 700,486 Z", "Acacia canopy", fill="#7E5C38", opacity=26, stroke=NONE)
for i, (x, y) in enumerate([(360,240),(390,224),(640,200)]):
    d.shape("ellipse", f"Dusk cloud {i+1}", x=x, y=y, width=120, height=22,
            fill="#E8D0AA", opacity=18, stroke=NONE)

# --- ground band, closing on the disc's own arc --------------------------------
gy = 792
gdx = math.sqrt(R*R - (gy - CY)**2)
d.path(f"M{CX-gdx:.1f},{gy} C330,778 420,788 500,782 C580,776 670,784 {CX+gdx:.1f},{gy} "
       f"A{R},{R} 0 0 1 {CX-gdx:.1f},{gy} Z",
       "Ground band", fill=lin(0, 780, 0, 880, (0, "#B5875A"), (1, "#7E5A36")), opacity=80, stroke=NONE)
d.path("M260,800 C360,790 460,796 560,790 C640,786 710,792 748,796", "Ground shade",
       fill=NONE, stroke="#5E422A", strokeWidth=8, opacity=30, cap="round")

# hoof shadow + two grass sprigs (well inside the disc)
d.shape("ellipse", "Hoof shadow", x=430, y=794, width=300, height=22,
        fill="#3A2818", opacity=30, stroke=NONE)
for j, (x, y, dx) in enumerate([(330,782,-14),(345,786,-6),(752,762,10),(766,766,16)]):
    d.path(f"M{x},{y} Q{x+dx},{y-26} {x+dx*2},{y-38}", f"Grass {j+1}",
           fill=NONE, stroke="#6E5A34", strokeWidth=3, opacity=45, cap="round")

# --- far legs (behind the body) --------------------------------------------------
d.path("M532,650 C536,700 536,748 532,790 L524,790 C526,744 524,696 520,652 Z",
       "Front leg far", fill=FAR_GRAD, stroke=NONE)
d.path("M676,660 C692,690 700,730 694,790 L684,790 C688,742 684,700 668,668 Z",
       "Hind leg far", fill=FAR_GRAD, stroke=NONE)
for i, (x0, x1) in enumerate([(523,535),(683,697)]):
    d.path(f"M{x0},788 L{x1},788 C{x1+3},796 {x1-2},801 {x1-6},801 C{x0+1},801 {x0-2},795 {x0},788 Z",
           f"Hoof far {i+1}", fill="#2E1E12", stroke=NONE)

# --- neck (drawn before body+head so both junctions tuck under) -------------------
d.path("M452,430 C470,478 492,528 516,564 C526,572 540,568 546,556 "
       "C524,516 502,468 482,420 C468,412 456,418 452,430 Z",
       "Neck", fill=NECK_GRAD, stroke=INK, strokeWidth=5)
d.path("M466,446 C482,492 500,532 520,560", "Throat light", fill=NONE,
       stroke="#F2DCB8", strokeWidth=8, opacity=35, cap="round")
d.path("M488,432 C506,478 524,522 540,552", "Nape shade", fill=NONE,
       stroke=DUSK, strokeWidth=8, opacity=28, cap="round")

# --- body: compact hunched barrel ------------------------------------------------
d.path("M498,552 C536,514 606,500 668,522 C704,536 716,574 702,612 "
       "C686,652 638,674 586,672 C542,670 506,654 486,624 "
       "C470,599 476,570 498,552 Z",
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# back sheen, dusk-blue flank shade, pale belly
d.path("M516,536 C560,516 620,514 662,532", "Back sheen", fill=NONE,
       stroke="#F2DCB8", strokeWidth=10, opacity=30, cap="round")
d.path("M540,640 C580,656 630,656 670,636", "Flank shade", fill=NONE,
       stroke=DUSK, strokeWidth=16, opacity=22, cap="round")
d.path("M660,548 C684,566 694,592 686,616", "Rump shade", fill=NONE,
       stroke=DUSK, strokeWidth=14, opacity=18, cap="round")
d.path("M500,632 C540,652 600,660 650,650 C612,668 548,668 514,652 "
       "C502,646 498,638 500,632 Z", "Belly pale", fill=PALE, opacity=55, stroke=NONE)
d.path("M505,560 C512,590 512,616 506,640", "Chest shade", fill=NONE,
       stroke="#6E4826", strokeWidth=10, opacity=25, cap="round")
# grizzled coat ticks
for j, (x, y, a) in enumerate([(560,540,-20),(596,532,-15),(632,540,-10),(575,585,8),(618,592,12),(555,610,15)]):
    t = math.radians(a)
    d.path(f"M{x},{y} L{x+16*math.cos(t):.0f},{y+16*math.sin(t):.0f}", f"Coat tick {j+1}",
           fill=NONE, stroke="#8A5E34", strokeWidth=3, opacity=35, cap="round")
# tiny tail
d.path("M698,552 C714,556 721,570 716,586 C707,584 699,575 696,564 Z",
       "Tail", fill="#6E4826", stroke=INK, strokeWidth=3)

# --- near legs: tapered to near-line weight --------------------------------------
d.path("M506,640 C510,690 508,742 502,792 L497,792 C499,742 498,692 495,642 Z",
       "Front leg near", fill=NECK_GRAD, stroke=NONE)
d.path("M503,660 C505,706 504,748 501,786", "Front leg light", fill=NONE,
       stroke="#F2DCB8", strokeWidth=3, opacity=40, cap="round")
d.path("M636,650 C662,672 678,700 676,726 C674,752 666,775 660,795 L652,795 "
       "C656,772 660,748 658,724 C656,700 646,675 630,660 Z",
       "Hind leg near", fill=NECK_GRAD, stroke=NONE)
d.path("M640,664 C658,684 668,706 666,726", "Hock shade", fill=NONE,
       stroke=DUSK, strokeWidth=6, opacity=30, cap="round")
for i, (x0, x1) in enumerate([(495,504),(650,663)]):
    d.path(f"M{x0},790 L{x1},790 C{x1+3},798 {x1-1},803 {x1-5},803 C{x0+2},803 {x0-2},797 {x0},790 Z",
           f"Hoof near {i+1}", fill="#2E1E12", stroke=NONE)

# --- far ear (behind the head) -----------------------------------------------------
d.path("M478,400 C492,362 516,330 546,314 C560,330 556,368 538,394 "
       "C524,410 500,414 486,408 Z",
       "Ear far", fill=EAR_FAR_GRAD, stroke=INK, strokeWidth=5)

# --- head: the long proboscis snout is the star --------------------------------------
HEAD = ("M448,384 C470,392 478,412 474,432 C470,450 458,462 440,468 "
        "C414,474 388,472 366,462 C344,452 322,452 310,458 "
        "C300,462 292,462 288,456 C284,448 288,440 296,436 "
        "C306,430 326,416 352,402 C390,384 424,378 448,384 Z")
d.path(HEAD, "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# snout-top ridge light + under-jaw dusk shade
d.path("M330,424 C360,406 400,392 436,388", "Snout ridge light", fill=NONE,
       stroke="#F6E4C4", strokeWidth=7, opacity=40, cap="round")
d.path("M330,458 C360,468 404,472 436,464", "Under-jaw shade", fill=NONE,
       stroke=DUSK, strokeWidth=8, opacity=25, cap="round")
d.path("M446,392 C458,404 464,420 460,438", "Cheek shade", fill=NONE,
       stroke="#6E4826", strokeWidth=8, opacity=22, cap="round")
# pale chin + lower snout: a soft wash along the whole jaw line
d.path("M292,456 C312,464 344,466 372,462 C352,474 316,474 298,464 Z",
       "Chin pale", fill=PALE, opacity=48, stroke=NONE)
# nose pad + slit nostril + mouth
d.path("M296,436 C287,441 284,451 291,459 C298,456 302,447 300,440 Z",
       "Nose pad", fill="#3A281C", stroke=NONE)
d.shape("ellipse", "Nostril", x=290, y=446, width=7, height=5, fill="#150C07", stroke=NONE)
d.path("M300,462 C316,468 334,468 348,464", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# preorbital gland: the dark teardrop below the eye line
d.path("M368,446 C375,450 377,461 371,468 C364,465 362,454 368,446 Z",
       "Preorbital gland", fill="#3A281C", opacity=60, stroke=NONE)

# --- the huge eye ------------------------------------------------------------------
d.shape("ellipse", "Eye ring", x=394, y=402, width=46, height=44, fill=PALE, opacity=80, stroke=NONE)
d.shape("ellipse", "Eye", x=402, y=408, width=34, height=32, fill=EYE_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye glint", x=409, y=413, width=9, height=9, fill="#FFFFFF", opacity=92, stroke=NONE)
d.shape("ellipse", "Eye glint small", x=423, y=428, width=5, height=5, fill="#FFFFFF", opacity=65, stroke=NONE)
d.path("M398,412 C408,402 424,400 436,408", "Upper lid", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
for i, (a, b) in enumerate([((402,408),(396,400)), ((412,404),(410,394))]):
    d.path(f"M{a[0]},{a[1]} L{b[0]},{b[1]}", f"Lash {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3, cap="round")

# --- near ear: oversized leaf, base sunk into the crown -------------------------------
d.path("M446,424 C438,366 456,308 500,280 C524,274 540,298 536,328 "
       "C528,374 498,412 466,428 C456,428 448,426 446,424 Z",
       "Ear near", fill=EAR_GRAD, stroke=INK, strokeWidth=5)
d.path("M466,396 C464,354 476,314 504,294 C518,294 526,314 522,338 "
       "C516,368 494,392 472,402 Z",
       "Inner ear", fill=INNER_EAR_GRAD, opacity=90, stroke=NONE)
d.path("M458,380 C462,340 476,306 500,288", "Ear rim light", fill=NONE,
       stroke="#F6DDB6", strokeWidth=4, opacity=45, cap="round")

# --- forehead crest + pin horns ---------------------------------------------------------
for i, (x0, x1) in enumerate([(452,447),(464,461)]):
    d.path(f"M{x0},384 L{x1},352 L{x0+6},382 Z", f"Horn {i+1}",
           fill="#4A3020", stroke=NONE)
for i, (a, b, c2) in enumerate([((438,388),(430,362),(438,344)),
                                 ((448,386),(446,358),(452,340)),
                                 ((458,386),(462,360),(468,346)),
                                 ((434,390),(424,372),(424,358))]):
    d.path(f"M{a[0]},{a[1]} Q{b[0]},{b[1]} {c2[0]},{c2[1]}", f"Crest {i+1}",
           fill=NONE, stroke="#7E532E", strokeWidth=4, cap="round")

# --- rim redrawn so the plate edge stays crisp -------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#8A6438", strokeWidth=6)

# --- name -----------------------------------------------------------------------------
d.text("DIK-DIK", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#EEDDBE", justify="center")

d.finish("dik-dik-V1R00")
