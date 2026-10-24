#!/usr/bin/env python3
"""Chimpanzee — field-guide plate V1R00. Seated in profile under the fig tree,
elbow on knee, holding one ripe fig up to the light — ninety-eight percent of
us, holding the rest in its hand. Lobed fig leaves droop in from the canopy,
figs hang on short stems, dappled light on a leaf-litter floor that closes on
the disc arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Chimpanzee — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#120905"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0D140C"), (1, "#030602"))
PLATE_GRAD = rad((0, "#C0D0A4"), (0.55, "#86A06C"), (1, "#48603E"))
FLOOR_GRAD = lin(0, 758, 0, 880, (0, "#465A38"), (1, "#1C2614"))
FUR = lin(0, 300, 0, 750, (0, "#3C2C20"), (0.5, "#26190F"), (1, "#140C07"))
FUR_DARK = "#1A100A"
FACE = rad((0, "#B08A64"), (1, "#7A5A3C"))
HAND = rad((0, "#4A3424"), (1, "#241508"))
FIG = rad((0, "#8A5064"), (1, "#3E1E30"))
LEAF = "#2E4426"
LEAF_DK = "#22341C"

# --- backdrop + forest plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#86A06C", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#364A2E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4EAC8", strokeWidth=3, opacity=40)
# canopy light shafts, top-right, very soft — starting inside the rim
d.path("M620,95 L500,470", "Shaft 1", fill=NONE, stroke="#E8DCA0",
       strokeWidth=85, opacity=9, cap="round")
d.path("M730,155 L620,430", "Shaft 2", fill=NONE, stroke="#E8DCA0",
       strokeWidth=55, opacity=7, cap="round")
# dappled sun-spots on the plate
for i, (x, y, w) in enumerate([(250,300,44),(620,180,38),(740,470,30),(300,560,26),(520,160,22)]):
    assert on_disc(x, y, 20), (x, y)
    d.shape("ellipse", f"Dapple {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#EAE4B8", opacity=14, stroke=NONE)

# --- fig canopy: a limb reaching in from the upper-left, lobed leaves and
# figs hanging off it — everything rooted inside the rim -----------------------
d.path("M185,225 C270,215 360,228 445,258 C495,276 540,286 585,288",
       "Fig limb", fill=NONE, stroke="#2A1E12", strokeWidth=14, cap="round")
d.path("M185,225 C270,215 360,228 445,258", "Limb light",
       fill=NONE, stroke="#5A4830", strokeWidth=4, opacity=50, cap="round")

def figleaf(x, y, s, label, fill=LEAF):
    """Three-lobed fig leaf hanging from a stem point at (x,y), scale s."""
    p = (f"M{x},{y} "
         f"C{x-14*s},{y+8*s} {x-26*s},{y+24*s} {x-30*s},{y+44*s} "
         f"C{x-33*s},{y+60*s} {x-28*s},{y+74*s} {x-18*s},{y+82*s} "
         f"C{x-12*s},{y+74*s} {x-8*s},{y+66*s} {x-6*s},{y+58*s} "
         f"C{x-8*s},{y+74*s} {x-6*s},{y+88*s} {x+2*s},{y+96*s} "
         f"C{x+8*s},{y+84*s} {x+10*s},{y+70*s} {x+8*s},{y+56*s} "
         f"C{x+16*s},{y+64*s} {x+26*s},{y+62*s} {x+30*s},{y+50*s} "
         f"C{x+33*s},{y+36*s} {x+28*s},{y+22*s} {x+16*s},{y+10*s} "
         f"C{x+8*s},{y+4*s} {x+4*s},{y+1*s} {x},{y} Z")
    d.path(p, label, fill=fill, stroke=INK, strokeWidth=3)
    for j, (dx, dy) in enumerate([(-16, 60), (0, 74), (18, 44)]):
        d.path(f"M{x},{y+6*s} C{x+dx*s*0.4},{y+dy*s*0.5} {x+dx*s*0.8},{y+dy*s*0.85} {x+dx*s},{y+dy*s}",
               f"{label} vein {j+1}", fill=NONE, stroke="#5A7A4C", strokeWidth=2, opacity=60, cap="round")

figleaf(280, 226, 1.15, "Leaf 1")
figleaf(200, 218, 0.9, "Leaf 2", LEAF_DK)
figleaf(400, 242, 0.85, "Leaf 3")
figleaf(490, 268, 0.7, "Leaf 4", LEAF_DK)
# hanging figs under the limb — short stem, purple tear-drop
def hangfig(x, y, s, label):
    d.path(f"M{x},{y-26*s} C{x},{y-16*s} {x},{y-8*s} {x},{y}", f"{label} stem",
           fill=NONE, stroke="#3A2E1A", strokeWidth=2.5, cap="round")
    d.path(f"M{x-9*s},{y} C{x-11*s},{y+12*s} {x-6*s},{y+22*s} {x},{y+24*s} "
           f"C{x+6*s},{y+22*s} {x+11*s},{y+12*s} {x+9*s},{y} C{x+5*s},{y-5*s} {x-5*s},{y-5*s} {x-9*s},{y} Z",
           label, fill=FIG, stroke=INK, strokeWidth=2.5)

hangfig(330, 258, 1.0, "Fig 1")
hangfig(440, 288, 0.85, "Fig 2")
hangfig(214, 243, 0.8, "Fig 3")

# --- leaf-litter floor: crest at y758, bottom closes on the disc arc ------------
fy = 758
fdx = math.sqrt(R * R - (fy - CY) ** 2)
d.path(f"M{CX-fdx:.1f},{fy} C300,744 420,754 540,748 C640,744 720,752 {CX+fdx:.1f},{fy} "
       f"A{R},{R} 0 0 1 {CX-fdx:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{CX-fdx+8:.1f},{fy-2} C300,742 420,750 540,744 C640,740 720,748 {CX+fdx-8:.1f},{fy-2}",
       "Floor light", fill=NONE, stroke="#D8DCA8", strokeWidth=4, opacity=35, cap="round")
# fallen leaves + a dropped fig on the litter
for i, (x, y, w, c) in enumerate([(270,786,30,"#5A6A3A"),(330,806,24,"#4A5C32"),(660,796,28,"#5A6A3A"),
                                  (740,776,22,"#4A5C32"),(420,800,26,"#546436")]):
    assert on_disc(x, y, 14), (x, y)
    d.shape("ellipse", f"Litter {i+1}", x=x, y=y, width=w, height=w*0.4,
            fill=c, opacity=70, stroke=NONE)
# a dropped fig on the litter — squashed, no standing stem
d.path("M694,786 C690,798 696,810 706,814 C716,818 728,814 732,804 "
       "C736,794 732,784 722,780 C712,776 698,778 694,786 Z",
       "Fallen fig", fill=FIG, stroke=INK, strokeWidth=2.5)
d.path("M706,780 C710,776 716,774 722,775", "Fallen fig scar",
       fill=NONE, stroke="#2A1418", strokeWidth=2, cap="round")

# --- chimpanzee: seated profile, elbow on knee, fig held to the light -----------
# resting arm first — its shoulder tucks into the silhouette
d.path("M512,486 C552,536 584,596 600,660 C608,694 612,720 610,740",
       "Resting arm", fill=NONE, stroke=FUR_DARK, strokeWidth=46, cap="round")
# knuckle fist on the floor
d.path("M580,724 C576,700 586,684 606,680 C626,676 642,688 644,708 "
       "C646,726 634,742 614,744 C598,746 584,738 580,724 Z",
       "Knuckles", fill=HAND, stroke=INK, strokeWidth=4)
d.path("M590,712 C598,706 610,704 622,708 M592,724 C600,718 612,716 622,720",
       "Knuckle ridges", fill=NONE, stroke="#6B4E32", strokeWidth=3, opacity=70, cap="round")

# ear before the silhouette so its root buries in the skull
d.path("M444,352 C464,344 486,352 494,370 C500,386 494,404 478,412 "
       "C462,418 444,410 438,394 C432,378 434,360 444,352 Z",
       "Ear", fill=FUR_DARK, stroke=INK, strokeWidth=4)
d.path("M452,366 C462,362 474,366 480,376 C484,386 480,398 470,402 "
       "C460,406 450,400 446,390 C444,380 446,370 452,366 Z",
       "Ear inner", fill="#6B4E32", opacity=60, stroke=NONE)

# one silhouette: forehead → crown → neck → back → rump → seat → foot →
# folded leg with the knee up → belly → chest → throat → chin → face front
SILH = ("M322,352 C330,330 352,314 380,308 C408,302 438,308 458,322 "
        "C478,336 490,354 496,374 C528,394 556,428 578,470 "
        "C606,524 630,594 640,660 C644,692 644,718 638,738 "
        "C600,744 560,746 520,744 C490,742 462,740 440,736 "
        "C430,724 428,708 432,692 C420,676 414,656 418,636 "
        "C422,614 434,600 452,594 C446,570 436,546 420,524 "
        "C404,504 386,492 366,484 C356,472 348,458 342,444 "
        "C328,432 318,416 314,400 C312,384 314,366 322,352 Z")
d.path(SILH, "Chimp", fill=FUR, stroke=INK, strokeWidth=6)

# face plate: bare tan skin — brow, flat nose, wide lips, small chin
d.path("M322,352 C332,342 348,336 366,336 C384,336 398,344 406,356 "
       "C412,368 414,382 410,396 C418,404 422,416 420,428 "
       "C414,442 400,450 384,450 C368,450 354,444 344,434 "
       "C330,424 320,410 316,396 C312,382 314,366 322,352 Z",
       "Face", fill=FACE, opacity=95, stroke=NONE)
# brow ridge shadow — the heavy bar over the eye
d.path("M326,368 C342,356 366,352 388,356 C398,358 406,364 410,372 "
       "C394,364 372,362 352,366 C342,368 332,372 326,378 Z",
       "Brow ridge", fill="#6B4E32", opacity=80, stroke=NONE)
# eye: deep-set under the brow, dark amber, quiet
d.path("M340,382 C350,372 368,370 380,378 C372,390 352,392 340,382 Z",
       "Eye", fill=rad((0, "#8A6238"), (0.6, "#543618"), (1, "#2A1A0A")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=358, y=376, width=9, height=11, fill="#0E0A04", stroke=NONE)
d.shape("ellipse", "Glint", x=360, y=378, width=4, height=4, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M336,378 C348,366 370,364 384,374", "Lid",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
# nose: flat, wide nostrils low on the face
d.path("M336,410 C342,404 352,402 360,406 C356,412 346,414 338,412 Z",
       "Nostril", fill="#2A1A0E", stroke=NONE)
d.path("M362,412 C368,406 378,406 384,410 C380,416 370,418 364,416 Z",
       "Nostril far", fill="#2A1A0E", stroke=NONE)
# mouth: the long thin thoughtful line
d.path("M334,428 C352,436 374,440 396,440 C404,440 410,438 414,434",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M338,436 C354,442 372,445 390,445", "Lower lip",
       fill=NONE, stroke="#6B4E32", strokeWidth=3, opacity=60, cap="round")
# whisker stubble / cheek shading
d.path("M350,398 C368,394 388,396 402,404", "Cheek crease",
       fill=NONE, stroke="#8A6848", strokeWidth=3, opacity=55, cap="round")

# coat shading: crown cap darker, back darker, flank lighter at the belly
d.path("M322,352 C336,332 362,318 392,314 C420,310 448,316 466,330 "
       "C448,322 420,320 394,324 C368,328 344,338 330,352 Z",
       "Crown cap", fill=FUR_DARK, opacity=60, stroke=NONE)
d.path("M496,380 C532,400 560,432 582,472 C610,524 630,588 638,650 "
       "C632,590 614,530 586,480 C562,438 532,406 496,388 Z",
       "Back shade", fill=FUR_DARK, opacity=65, stroke=NONE)
for i, dd in enumerate(["M520,440 C544,480 562,530 572,584",
                        "M556,470 C578,512 592,562 598,616",
                        "M600,530 C614,570 624,618 626,660"]):
    d.path(dd, f"Back fur {i+1}", fill=NONE, stroke="#120A06", strokeWidth=4, opacity=45, cap="round")
# belly light
d.path("M436,560 C452,590 462,624 464,656 C466,686 462,712 452,730 "
       "C446,700 442,664 442,630 C442,604 440,580 436,560 Z",
       "Belly light", fill="#4A3424", opacity=50, stroke=NONE)
# folded leg: knee cap shading + shin line
d.path("M418,640 C428,620 444,606 464,602 C456,618 450,638 450,660 "
       "C450,684 444,706 436,722 C424,700 416,668 418,640 Z",
       "Knee", fill=FUR_DARK, opacity=55, stroke=NONE)
d.path("M424,650 C432,676 434,702 430,726", "Shin line",
       fill=NONE, stroke="#120A06", strokeWidth=4, opacity=50, cap="round")

# raised arm: elbow resting on the knee, forearm up — thick stroked limb
d.path("M478,452 C438,492 410,540 398,590 C388,566 360,508 330,458",
       "Raised arm", fill=NONE, stroke="#2A1C12", strokeWidth=50, cap="round")
d.path("M478,452 C438,492 410,540 398,590 C388,566 360,508 330,458",
       "Raised arm shade", fill=NONE, stroke=FUR_DARK, strokeWidth=50, cap="round", opacity=45)
# forearm fur strokes along the raised forearm
for i, dd in enumerate(["M392,576 C382,548 364,514 348,486",
                        "M404,584 C394,552 376,516 356,486"]):
    d.path(dd, f"Forearm fur {i+1}", fill=NONE, stroke="#120A06", strokeWidth=4, opacity=40, cap="round")

# the hand at the wrist: long dark fingers gently pinching the fig
d.path("M316,436 C306,424 306,408 316,398 C326,388 342,388 352,396 "
       "C342,398 334,404 330,412 C338,410 348,412 354,420 "
       "C346,420 340,424 336,430 C334,438 326,442 316,436 Z",
       "Hand", fill=HAND, stroke=INK, strokeWidth=4)
# finger ridges over the fig
for i, dd in enumerate(["M320,404 C328,398 338,396 346,398",
                        "M318,418 C326,412 336,410 344,412"]):
    d.path(dd, f"Finger {i+1}", fill=NONE, stroke="#6B4E32", strokeWidth=3, opacity=70, cap="round")
# the fig: held up between thumb and fingertips, catching the light
d.path("M296,404 C292,418 298,432 310,438 C322,444 336,440 342,428 "
       "C348,416 344,402 332,396 C320,390 304,392 296,404 Z",
       "Held fig", fill=FIG, stroke=INK, strokeWidth=3)
d.path("M310,394 C314,390 320,388 326,389", "Fig stem scar",
       fill=NONE, stroke="#2A1418", strokeWidth=2.5, cap="round")
d.shape("ellipse", "Fig light", x=302, y=404, width=8, height=10, fill="#C88A9A", opacity=60, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0A140A", strokeWidth=6)

# --- name ----------------------------------------------------------------------
d.text("CHIMPANZEE", "Name", x=500, y=962, size=52, font="Virelai Sans",
       color="#DEE6C4", justify="center")

d.finish("chimpanzee-V1R00")
