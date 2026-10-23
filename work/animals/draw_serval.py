#!/usr/bin/env python3
"""Serval — field-guide plate V1R00. Full-body standing profile facing
left: the tall-cat silhouette, all legs and radar — enormous oval ears,
a long slender neck, a small narrow face, and crisp black spots over a
gradient gold coat. The far ear shows its black back with a pale ocellus
bar. Warm savanna-gold plate; dry grass by the arc-closing ground band.
1000x1000. House style: gradients + translucent shading, never flat."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Serval — Field Plate", 1000, 1000)

INK = "#33220F"
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def spot(x, y, w, h, label, rot=0, color="#241610", op=88):
    """Crisp dark coat mark (ellipse, optionally squashed/tilted)."""
    d.shape("ellipse", label, x=x - w/2, y=y - h/2, width=w, height=h,
            fill=color, opacity=op, stroke=NONE)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#26200F"), (1, "#0C0805"))
PLATE_GRAD = rad((0, "#FAE8BC"), (0.66, "#E8C07A"), (1, "#AE7C3C"))
COAT_GRAD = rad((0, "#EDBE6E"), (0.64, "#D29A4E"), (1, "#9E6C30"))
NECK_GRAD = lin(360, 330, 470, 540, (0, "#E4B464"), (1, "#B8853E"))
FAR_GRAD = lin(0, 540, 0, 800, (0, "#A8793C"), (1, "#7C5626"))
EAR_GRAD = lin(390, 330, 440, 210, (0, "#D8A85C"), (1, "#C2904A"))
EAR_FAR_GRAD = lin(430, 340, 480, 240, (0, "#8A6230"), (1, "#5E4020"))
INNER_EAR_GRAD = lin(400, 320, 435, 230, (0, "#F0D2A0"), (1, "#E0B988"))
EYE_GRAD = rad((0, "#5A3E20"), (1, "#160D06"))
GRASS = "#8E7434"
PALE = "#FBF0D6"

# --- backdrop + savanna-gold plate ----------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6430", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFF4DC", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=600, y=160, width=230, height=120, fill="#E8CC90", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=170, y=430, width=190, height=110, fill="#E8CC90", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(770,300,7),(830,470,8),(200,330,6),(160,500,8),(250,720,7),(750,690,8),
                               (855,560,6),(400,110,7),(610,118,6),(330,810,6),(690,240,5),(150,400,6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#A8843C", opacity=38, stroke=NONE)

# faint heat shimmer + a far flat-top acacia, all inside the disc
d.path("M200,420 C300,408 420,406 540,414", "Heat shimmer", fill=NONE,
       stroke="#C89858", strokeWidth=8, opacity=18, cap="round")
d.path("M762,480 L766,442 L756,428 M766,442 L780,426", "Acacia trunk", fill=NONE,
       stroke="#8A6230", strokeWidth=5, opacity=30, cap="round")
d.path("M726,432 C742,416 776,412 804,418 C818,422 824,430 818,436 "
       "C790,444 750,444 726,432 Z", "Acacia canopy", fill="#8A6230", opacity=28, stroke=NONE)

# --- savanna band, closing on the disc's own arc ------------------------------------
gy = 792
gdx = math.sqrt(R*R - (gy - CY)**2)
d.path(f"M{CX-gdx:.1f},{gy} C320,780 410,789 500,783 C590,777 680,785 {CX+gdx:.1f},{gy} "
       f"A{R},{R} 0 0 1 {CX-gdx:.1f},{gy} Z",
       "Savanna band", fill=lin(0, 780, 0, 880, (0, "#C2985A"), (1, "#84602E")), opacity=80, stroke=NONE)
d.shape("ellipse", "Paw shadow", x=360, y=792, width=320, height=22,
        fill="#4A3414", opacity=30, stroke=NONE)
# dry grass tufts beside the legs
for j, (x, y, dx) in enumerate([(700,776,12),(716,780,20),(688,782,4),(268,772,-12),(282,776,-4)]):
    d.path(f"M{x},{y} Q{x+dx},{y-30} {x+dx*2},{y-44}", f"Grass {j+1}",
           fill=NONE, stroke=GRASS, strokeWidth=3, opacity=50, cap="round")

# --- far legs (behind the body) ---------------------------------------------------------
d.path("M470,545 C474,620 472,700 468,788 L456,788 C458,700 456,622 452,548 Z",
       "Front leg far", fill=FAR_GRAD, stroke=NONE)
d.path("M616,545 C634,600 644,680 636,788 L624,788 C630,690 624,610 604,552 Z",
       "Hind leg far", fill=FAR_GRAD, stroke=NONE)
for i, (x0, x1) in enumerate([(454,470),(622,638)]):
    d.path(f"M{x0},786 L{x1},786 C{x1+3},794 {x1-1},799 {x1-5},799 C{x0+2},799 {x0-3},793 {x0},786 Z",
           f"Paw far {i+1}", fill="#1C1208", stroke=NONE)

# --- tail: short, black-tipped, hanging off the rump --------------------------------------
d.path("M636,502 C656,512 668,534 668,560 C668,578 662,592 654,600 "
       "C648,594 646,580 648,562 C650,540 644,518 632,508 Z",
       "Tail", fill=COAT_GRAD, stroke=INK, strokeWidth=4)
d.path("M654,592 C662,588 666,576 666,562 C660,570 654,580 654,592 Z",
       "Tail tip", fill="#1C1208", stroke=NONE)

# --- neck: long and slender -----------------------------------------------------------------
d.path("M382,338 C402,392 424,452 446,506 C456,528 478,540 502,536 "
       "C478,492 456,438 436,380 C426,350 402,334 382,338 Z",
       "Neck", fill=NECK_GRAD, stroke=INK, strokeWidth=5)
d.path("M394,352 C412,404 432,458 454,504", "Throat light", fill=NONE,
       stroke=PALE, strokeWidth=7, opacity=35, cap="round")
d.path("M416,368 C432,420 450,474 470,516", "Nape shade", fill=NONE,
       stroke="#8A5E2C", strokeWidth=7, opacity=25, cap="round")
# neck stripes breaking into spots (serval signature)
for j, (x, y, dx, dy) in enumerate([(402,392,18,26),(414,424,20,28),(428,458,20,30)]):
    d.path(f"M{x},{y} Q{x+dx},{y+dy/2} {x+dx+4},{y+dy}", f"Neck stripe {j+1}",
           fill=NONE, stroke="#241610", strokeWidth=5, opacity=70, cap="round")

# --- body: lean, high-shouldered -------------------------------------------------------------
d.path("M446,478 C486,458 550,454 600,470 C632,478 648,498 646,522 "
       "C642,548 612,562 574,562 C530,562 486,554 462,534 "
       "C444,518 436,494 446,478 Z",
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
d.path("M452,500 C466,520 484,532 506,538", "Shoulder blend", fill=NONE,
       stroke="#B8853E", strokeWidth=10, opacity=35, cap="round")
d.path("M466,480 C504,464 556,460 598,472", "Back sheen", fill=NONE,
       stroke=PALE, strokeWidth=8, opacity=30, cap="round")
d.path("M500,540 C544,552 596,552 630,534", "Flank shade", fill=NONE,
       stroke="#7C5626", strokeWidth=14, opacity=22, cap="round")
d.path("M470,536 C506,548 560,552 606,544 C566,560 500,558 476,544 Z",
       "Belly pale", fill=PALE, opacity=45, stroke=NONE)

# crisp spot field over the gradient body — irregular rows
SPOTS = [(492,486,13,9),(524,478,11,8),(556,478,12,9),(588,484,10,8),(618,494,9,7),
         (478,506,10,8),(510,498,14,10),(542,496,12,9),(574,502,11,8),(606,510,9,7),
         (494,524,9,7),(526,518,12,9),(560,520,11,8),(592,526,10,7),
         (512,540,8,6),(546,540,9,7),(578,538,8,6),
         (470,494,8,6),(632,508,8,6),(638,528,7,5)]
for j, (x, y, w, h) in enumerate(SPOTS):
    spot(x, y, w, h, f"Spot {j+1}")

# --- near legs: the famous stilts --------------------------------------------------------------
d.path("M448,540 C452,620 450,700 446,788 L434,788 C436,700 434,622 430,544 Z",
       "Front leg near", fill=NECK_GRAD, stroke=NONE)
d.path("M444,560 C446,636 444,712 441,780", "Front leg light", fill=NONE,
       stroke=PALE, strokeWidth=3, opacity=40, cap="round")
d.path("M588,548 C606,590 614,650 608,706 C605,740 600,766 597,790 L585,790 "
       "C590,760 594,730 592,700 C588,650 580,600 570,556 Z",
       "Hind leg near", fill=NECK_GRAD, stroke=NONE)
d.path("M590,570 C600,614 604,660 600,702", "Hock shade", fill=NONE,
       stroke="#8A5E2C", strokeWidth=6, opacity=30, cap="round")
# leg spots: small, fading out below the knee/hock
for j, (x, y) in enumerate([(440,566),(446,596),(438,626),(444,656),
                             (580,580),(592,606),(596,636),(600,668)]):
    spot(x, y, 7, 5, f"Leg spot {j+1}", op=70)
for i, (x0, x1) in enumerate([(432,448),(583,599)]):
    d.path(f"M{x0},786 L{x1},786 C{x1+3},794 {x1-1},799 {x1-5},799 C{x0+2},799 {x0-3},793 {x0},786 Z",
           f"Paw near {i+1}", fill="#1C1208", stroke=NONE)

# --- far ear: turned, showing its black back + pale ocellus bar -------------------------------
d.path("M414,318 C428,270 452,232 486,214 C504,230 506,272 492,308 "
       "C482,330 456,342 434,336 C420,330 410,322 414,318 Z",
       "Ear far", fill=EAR_FAR_GRAD, stroke=INK, strokeWidth=5)
d.path("M436,292 C452,262 468,240 486,226", "Ocellus bar", fill=NONE,
       stroke=PALE, strokeWidth=7, opacity=85, cap="round")

# --- head: small, narrow, all ears --------------------------------------------------------------
HEAD = ("M370,318 C392,312 412,320 422,340 C430,356 430,376 420,390 "
        "C410,404 392,410 374,406 C354,402 336,402 326,394 "
        "C316,388 314,378 320,368 C328,358 342,346 356,334 "
        "C360,326 364,320 370,318 Z")
d.path(HEAD, "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
d.path("M338,362 C350,348 366,336 384,330", "Forehead light", fill=NONE,
       stroke=PALE, strokeWidth=6, opacity=35, cap="round")
# white muzzle + chin
d.path("M322,372 C330,384 346,394 362,398 C350,404 332,400 324,390 "
       "C318,384 318,378 322,372 Z", "Muzzle pale", fill=PALE, opacity=75, stroke=NONE)
# nose + mouth + tear mark
d.path("M322,368 C315,374 315,384 322,390 C328,386 330,376 328,370 Z",
       "Nose pad", fill="#241610", stroke=NONE)
d.path("M330,392 C342,398 356,400 368,398", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M362,360 C356,372 352,384 350,394", "Tear mark", fill=NONE,
       stroke="#241610", strokeWidth=4, opacity=80, cap="round")
# eyes + pale spectacle
d.shape("ellipse", "Eye ring", x=368, y=342, width=34, height=30, fill=PALE, opacity=75, stroke=NONE)
d.shape("ellipse", "Eye", x=375, y=346, width=22, height=21, fill=EYE_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye glint", x=380, y=350, width=7, height=7, fill="#FFFFFF", opacity=92, stroke=NONE)
d.path("M370,348 C378,340 390,338 400,344", "Upper lid", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# whiskers
for j, (x1, y1, x2, y2) in enumerate([(340,378,296,368),(342,384,298,388),(346,390,304,404)]):
    d.path(f"M{x1},{y1} Q{(x1+x2)/2},{min(y1,y2)-5} {x2},{y2}", f"Whisker {j+1}",
           fill=NONE, stroke="#FFFFFF", strokeWidth=2, opacity=70, cap="round")

# --- near ear: the enormous oval, upright --------------------------------------------------------
d.path("M382,322 C374,266 386,212 420,186 C448,178 468,204 466,246 "
       "C464,290 444,326 412,336 C398,334 386,328 382,322 Z",
       "Ear near", fill=EAR_GRAD, stroke=INK, strokeWidth=5)
d.path("M398,312 C394,268 404,226 428,204 C444,202 452,222 450,250 "
       "C448,284 432,312 412,320 Z",
       "Inner ear", fill=INNER_EAR_GRAD, opacity=88, stroke=NONE)
d.path("M390,300 C388,258 398,220 420,198", "Ear rim light", fill=NONE,
       stroke=PALE, strokeWidth=4, opacity=45, cap="round")

# --- rim redrawn so the plate edge stays crisp ----------------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#8A6430", strokeWidth=6)

# --- name ------------------------------------------------------------------------------------------
d.text("SERVAL", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#F0DCAC", justify="center")

d.finish("serval-V1R00")
