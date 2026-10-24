#!/usr/bin/env python3
"""African wild dog — field-guide plate V1R00. Frontal portrait: the painted
wolf's two signatures, enormous rounded ears and a calico patchwork coat, at
hunt-dawn on the savanna — low pale sun, acacia on the horizon, dry grass
floor that closes on the disc arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("African Wild Dog — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#1E0F06"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#1A0E06"), (1, "#050201"))
PLATE_GRAD = rad((0, "#F0D08A"), (0.55, "#C9A05E"), (1, "#7E5428"))
FLOOR_GRAD = lin(0, 762, 0, 880, (0, "#6E5630"), (1, "#2C1D0E"))
COAT = lin(0, 280, 0, 800, (0, "#C89A5C"), (0.5, "#A4743C"), (1, "#6E4620"))
DARK = "#2A1A10"                    # the black-brown patches
DARK_GRAD = lin(0, 300, 0, 700, (0, "#3A2718"), (1, "#1C1008"))
CREAM = "#EFE0BE"

# --- backdrop + savanna plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#C9A05E", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E3E1E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0DCA8", strokeWidth=3, opacity=40)
# low dawn sun, left of centre — pale disc with soft halo
d.shape("ellipse", "Sun halo", x=208, y=500, width=150, height=150, fill="#F6E2A8", opacity=14, stroke=NONE)
d.shape("ellipse", "Sun", x=238, y=530, width=90, height=90, fill="#F6E2A8", opacity=55, stroke=NONE)
# heat shimmer lines under the sun
for i, (x0, x1, y) in enumerate([(175, 330, 640), (205, 360, 668), (168, 315, 696)]):
    d.path(f"M{x0},{y} C{(x0+x1)/2-20},{y-6} {(x0+x1)/2+20},{y+6} {x1},{y}",
           f"Shimmer {i+1}", fill=NONE, stroke="#F0DCA8", strokeWidth=3, opacity=25, cap="round")

# --- flat-top acacia on the right horizon --------------------------------------
d.path("M736,724 C734,690 730,660 722,634 M722,634 C728,620 740,612 756,608 "
       "M722,634 C716,622 706,614 692,612",
       "Acacia trunk", fill=NONE, stroke="#3A2412", strokeWidth=7, cap="round")
d.path("M660,600 C690,584 760,580 810,594 C822,598 824,606 812,610 "
       "C764,622 700,622 664,612 C652,608 650,604 660,600 Z",
       "Acacia crown", fill="#3F2E14", opacity=85, stroke=NONE)

# --- dry-grass floor: crest ~y762, bottom closes on the disc arc ----------------
fy = 762
fdx = math.sqrt(R * R - (fy - CY) ** 2)
d.path(f"M{CX-fdx:.1f},{fy} C300,748 430,760 560,752 C650,748 730,756 {CX+fdx:.1f},{fy} "
       f"A{R},{R} 0 0 1 {CX-fdx:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{CX-fdx+8:.1f},{fy-2} C300,746 430,756 560,750 C650,746 730,752 {CX+fdx-8:.1f},{fy-2}",
       "Floor light", fill=NONE, stroke="#E8D8A0", strokeWidth=4, opacity=35, cap="round")

# --- ears first: huge rounded ears behind the skull -----------------------------
def ear(cx, cy, r, label):
    d.shape("ellipse", f"{label} outer", x=cx-r, y=cy-r*0.92, width=2*r, height=2*r*1.0,
            fill=DARK_GRAD, stroke=INK, strokeWidth=6)
    # inner ear: cup sits low and off-centre, not a concentric target
    s = -1 if cx < CX else 1
    d.shape("ellipse", f"{label} inner", x=cx-r*0.52+s*r*0.08, y=cy-r*0.34,
            width=2*r*0.56, height=2*r*0.62,
            fill="#6E4A2E", opacity=75, stroke=NONE)
    d.shape("ellipse", f"{label} shade", x=cx-r*0.38+s*r*0.10, y=cy-r*0.18,
            width=2*r*0.40, height=2*r*0.44, fill="#4A3018", opacity=70, stroke=NONE)
    # rim light on the outer edge — dawn sun from the left
    side = -1 if cx < CX else 1
    d.path(f"M{cx - side*r*0.55},{cy - r*0.62} C{cx - side*r*0.9},{cy - r*0.3} "
           f"{cx - side*r*0.95},{cy + r*0.15} {cx - side*r*0.6},{cy + r*0.55}",
           f"{label} rim", fill=NONE, stroke="#E8C884", strokeWidth=5,
           opacity=55, cap="round")

ear(316, 296, 104, "Ear L")
ear(684, 296, 104, "Ear R")

# --- bust: chest + shoulders as one silhouette closing on the disc arc ---------
by = 800
bdx = math.sqrt(R * R - (by - CY) ** 2)
bxl, bxr = CX - bdx, CX + bdx
d.path(f"M425,640 C380,660 330,700 300,740 C280,766 266,782 {bxl:.1f},{by} "
       f"A{R},{R} 0 0 1 {bxr:.1f},{by} "
       f"C734,782 720,766 700,740 C670,700 620,660 575,640 "
       f"C555,655 445,655 425,640 Z",
       "Bust", fill=DARK_GRAD, stroke=INK, strokeWidth=6)

# --- head + neck silhouette: broad skull, cheeks, slim tapered muzzle ----------
SILH = ("M392,318 C420,292 580,292 608,318 "
        "C646,340 668,382 664,428 "
        "C660,470 640,506 612,536 "
        "C600,548 592,570 584,596 "
        "C572,634 542,662 500,664 "
        "C458,662 428,634 416,596 "
        "C408,570 400,548 388,536 "
        "C360,506 340,470 336,428 "
        "C332,382 354,340 392,318 Z")
d.path(SILH, "Head", fill=COAT, stroke=INK, strokeWidth=6)

# --- calico patches: the painted coat -------------------------------------------
# black mask over the viewer-left eye, running up to the ear base
d.path("M352,400 C356,360 380,330 416,318 C444,308 470,312 486,330 "
       "C470,352 458,382 454,412 C450,440 440,462 420,472 "
       "C396,480 370,472 358,450 C350,434 348,416 352,400 Z",
       "Mask L", fill=DARK, opacity=92, stroke=NONE)
# smaller dark patch at the right temple
d.path("M560,322 C590,326 616,344 630,372 C640,392 642,412 636,430 "
       "C614,424 592,408 578,384 C566,362 560,342 560,322 Z",
       "Mask R", fill=DARK, opacity=85, stroke=NONE)
# cream blaze between the eyes down the nose bridge
d.path("M484,336 C496,330 510,330 520,338 C524,368 522,402 516,436 "
       "C512,458 508,480 504,500 C494,478 488,452 484,424 "
       "C480,394 480,364 484,336 Z",
       "Blaze", fill=CREAM, opacity=80, stroke=NONE)
# cream cheek patch, viewer right
d.path("M590,470 C612,462 632,466 642,482 C646,502 640,522 622,534 "
       "C602,544 580,540 572,522 C566,504 572,482 590,470 Z",
       "Cheek cream", fill=CREAM, opacity=60, stroke=NONE)
# dark muzzle wrap — slim, tapering to the chin
d.path("M438,556 C450,538 470,528 488,526 C494,538 506,538 512,526 "
       "C530,528 550,538 562,556 C568,584 560,616 540,634 "
       "C520,646 480,646 460,634 C440,616 432,584 438,556 Z",
       "Muzzle", fill=DARK, opacity=90, stroke=NONE)
# chest: cream bib inside the bust, tip ending inside the rim
d.path("M430,640 C460,656 540,656 570,640 C584,690 594,742 592,790 "
       "C588,824 560,856 500,874 C440,856 412,824 408,790 "
       "C406,742 416,690 430,640 Z",
       "Chest bib", fill=CREAM, opacity=88, stroke=NONE)
# soft tan shading where the neck meets the dark bust
d.path("M340,650 C370,630 404,626 428,638 C420,676 416,714 422,750 "
       "C400,736 378,712 362,684 C352,668 344,658 340,650 Z",
       "Neck shade L", fill="#8A5E30", opacity=45, stroke=NONE)
d.path("M660,650 C630,630 596,626 572,638 C580,676 584,714 578,750 "
       "C600,736 622,712 638,684 C648,668 656,658 660,650 Z",
       "Neck shade R", fill="#8A5E30", opacity=45, stroke=NONE)
# scattered coat blotches on the neck sides
d.path("M352,690 C366,682 384,684 392,696 C396,712 390,726 376,730 "
       "C360,732 348,722 346,706 C345,698 347,693 352,690 Z",
       "Blotch L1", fill=CREAM, opacity=55, stroke=NONE)
d.path("M632,700 C648,694 664,698 670,712 C672,726 664,738 650,740 "
       "C636,740 626,730 626,716 C626,708 628,703 632,700 Z",
       "Blotch R1", fill=CREAM, opacity=55, stroke=NONE)

# --- face ----------------------------------------------------------------------
# eyes: amber, set wide under the ear line
d.path("M398,448 C408,436 428,432 442,440 C434,456 412,460 398,448 Z",
       "Eye L", fill=rad((0, "#B07A2E"), (0.65, "#6E4714"), (1, "#2E1A08")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil L", x=416, y=441, width=10, height=12, fill="#100A04", stroke=NONE)
d.shape("ellipse", "Glint L", x=418, y=443, width=4, height=4, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M394,444 C404,430 428,426 446,436", "Lid L",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path("M558,440 C572,432 592,436 602,448 C588,460 566,456 558,440 Z",
       "Eye R", fill=rad((0, "#B07A2E"), (0.65, "#6E4714"), (1, "#2E1A08")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil R", x=574, y=441, width=10, height=12, fill="#100A04", stroke=NONE)
d.shape("ellipse", "Glint R", x=576, y=443, width=4, height=4, fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M554,436 C572,426 596,430 606,444", "Lid R",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
# brow shading
d.path("M390,420 C404,408 428,404 448,410", "Brow L",
       fill=NONE, stroke="#4A2E14", strokeWidth=5, opacity=55, cap="round")
d.path("M552,410 C572,404 596,408 610,420", "Brow R",
       fill=NONE, stroke="#4A2E14", strokeWidth=5, opacity=55, cap="round")

# nose: broad dark pad at the muzzle tip
d.path("M472,590 C478,574 522,574 528,590 C532,606 524,622 500,624 "
       "C476,622 468,606 472,590 Z",
       "Nose", fill="#0E0804", stroke=INK, strokeWidth=3)
d.path("M482,596 C486,592 492,592 494,596 M506,596 C508,592 514,592 518,596",
       "Nostrils", fill=NONE, stroke="#3A2A18", strokeWidth=3.5, cap="round")
d.shape("ellipse", "Nose shine", x=484, y=584, width=12, height=7,
        fill="#FFFFFF", opacity=30, stroke=NONE)
# philtrum + mouth line
d.path("M500,624 C500,634 500,642 500,648", "Philtrum",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M500,648 C480,652 458,648 444,638 M500,648 C520,652 542,648 556,638",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# muzzle-side whisker dots
for i, (x, y) in enumerate([(452,592),(446,606),(458,616),(548,592),(554,606),(542,616)]):
    d.shape("ellipse", f"Whisker dot {i+1}", x=x, y=y, width=4, height=4,
            fill="#0E0804", opacity=60, stroke=NONE)

# --- dry grass tufts over the floor crest ---------------------------------------
def tuft(x, y, s, label, lean=0):
    for j, (dx, bend) in enumerate([(-16, -26), (0, 0), (16, 26), (-6, -12), (8, 14)]):
        x2 = x + dx * s + bend * s * 0.4 + lean
        y2 = y - (34 - abs(dx)) * s
        d.path(f"M{x},{y} C{x + dx*s*0.3 + lean},{y - (20-abs(dx)*0.4)*s} "
               f"{x2 - bend*s*0.3},{y2 + 14*s} {x2},{y2}",
               f"{label} blade {j+1}", fill=NONE, stroke="#C8A860",
               strokeWidth=3.5, opacity=75, cap="round")

tuft(280, 790, 0.95, "Tuft L", -6)
tuft(712, 795, 0.85, "Tuft R", 4)
tuft(600, 825, 0.7, "Tuft M")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#140A04", strokeWidth=6)

# --- name ----------------------------------------------------------------------
d.text("AFRICAN WILD DOG", "Name", x=500, y=962, size=48, font="Virelai Sans",
       color="#EED9A2", justify="center")

d.finish("african-wild-dog-V1R00")
