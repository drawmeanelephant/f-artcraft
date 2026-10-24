#!/usr/bin/env python3
"""Quagga — field-guide plate V1R00. Standing profile facing left: bold
stripes on head, neck and forequarters that give out mid-flank; the
hindquarters drawn translucent with the low veld sun glowing through, flecks
of rump already drifting off. The front a zebra, the rear a rumor.
Veld plate, faded-stripe mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Quagga — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#241708"
STRIPE = "#33241A"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#18100A"), (1, "#080503"))
PLATE_GRAD = rad((0, "#E0D2AC"), (0.6, "#AC9468"), (1, "#63502F"))
EARTH_GRAD = lin(0, 720, 0, 880, (0, "#9A7C4E"), (0.6, "#6E4E2C"), (1, "#33241A"))
COAT_GRAD = rad((0, "#D8C4A0"), (0.55, "#B09468"), (1, "#74562F"))
RUMP_GRAD = rad((0, "#B09468"), (0.6, "#8A6E44"), (1, "#5E4426"))
PALE = "#E4D8BC"

# --- backdrop + veld plate -------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#AC9468", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E3C22", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E6C8", strokeWidth=3, opacity=45)

# the low pale sun the hindquarters walk into
d.shape("ellipse", "Sun glow", x=606, y=470, width=260, height=230,
        fill=rad((0, "#F4E4B8", 40), (1, "#F4E4B8", 0)), stroke=NONE)
d.shape("ellipse", "Sun", x=662, y=522, width=150, height=130,
        fill="#F4E4B8", opacity=30, stroke=NONE)
# heat shimmer bands
for i, dd in enumerate(["M200,240 C360,224 560,226 730,244",
                        "M250,330 C400,316 580,318 740,334"]):
    d.path(dd, f"Shimmer {i+1}", fill=NONE, stroke="#E8D8B0",
           strokeWidth=6, opacity=13, cap="round")
# drifting veld dust
for i, (x, y, w) in enumerate([(260,200,5),(420,170,4),(600,190,5),(740,260,4),
                               (180,360,4),(840,400,5),(330,300,3),(700,140,4)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0E4C0", opacity=38, stroke=NONE)

# --- dry veld floor, closing on the disc's own arc ----------------------------------
fy = 720
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C320,708 440,724 560,716 C680,708 770,712 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Veld floor", fill=EARTH_GRAD, stroke=NONE)
d.path(f"M{fl+6:.0f},{fy} C320,708 440,724 560,716 C680,708 770,712 {fr-6:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#C4AE7C", strokeWidth=5, opacity=40, cap="round")
# a long pale dust band along the floor
d.shape("ellipse", "Dust band", x=240, y=752, width=380, height=16,
        fill="#D8C49A", opacity=20, stroke=NONE)
# straw tufts
for i, (x, y, s) in enumerate([(200, 726, 1), (252, 740, -1), (330, 730, 1), (700, 736, -1),
                               (770, 726, 1), (630, 744, -1), (450, 732, 1), (560, 736, -1)]):
    for j, (dx, dy) in enumerate([(-8, -24), (0, -32), (8, -22)]):
        tx = x + dx + s * j * 3
        d.path(f"M{x},{y} Q{x + dx*0.5},{y + dy*0.6} {tx},{y + dy}",
               f"Straw {i+1}.{j+1}", fill=NONE, stroke="#C8B06A",
               strokeWidth=3.5, opacity=60, cap="round")
# one dry thornbush silhouette at the left rim
d.path("M186,712 L188,672 L184,656 M188,680 L206,662 M188,688 L172,672",
       "Thornbush", fill=NONE, stroke="#3E2E18", strokeWidth=4.5,
       opacity=55, cap="round")

# contact shadow
d.shape("ellipse", "Contact shadow", x=360, y=706, width=380, height=18,
        fill="#14100A", opacity=40, stroke=NONE)

# === the animal =====================================================================
# --- tail: already half-gone -----------------------------------------------------------
d.path("M782,468 C790,500 790,538 784,568", "Tail", fill=NONE,
       stroke="#5E4426", strokeWidth=9, opacity=32, cap="round")
d.shape("ellipse", "Tail tuft", x=776, y=560, width=18, height=32,
        fill="#3E2E18", opacity=28, stroke=NONE)

# --- hindquarters: the rumor, translucent ------------------------------------------------
d.path("M596,424 C676,418 740,438 772,470 C790,492 792,524 780,550 "
       "C758,582 700,600 634,604 C612,604 596,600 588,590 "
       "C574,556 574,472 590,440 C592,432 594,428 596,424 Z",
       "Hindquarter", fill=RUMP_GRAD, opacity=42, stroke=INK, strokeWidth=4)
# the dappling a real quagga keeps, ghosted
for i, (x, y, w) in enumerate([(640, 460, 14), (690, 480, 12), (740, 470, 12),
                               (660, 520, 12), (716, 530, 10)]):
    d.shape("ellipse", f"Rump dapple {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#33241A", opacity=18, stroke=NONE)
# flecks of rump already drifting off the rim of the body
for i, (x, y, w, o) in enumerate([(800, 470, 10, 22), (824, 502, 8, 18),
                                  (808, 544, 7, 15), (840, 486, 6, 12)]):
    d.shape("ellipse", f"Drift fleck {i+1}", x=x, y=y, width=w, height=w*0.8,
            fill="#8A6E44", opacity=o, stroke=NONE)

# --- far legs ----------------------------------------------------------------------------
d.path("M540,556 C534,592 532,632 538,666 C541,688 540,702 536,710 "
       "C540,718 552,719 560,714 C564,706 564,696 562,688 "
       "C560,660 562,628 568,600 C572,578 572,560 566,550 "
       "C556,544 546,548 540,556 Z",
       "Front leg far", fill="#5E4426", stroke=INK, strokeWidth=4)
d.path("M712,556 C704,592 704,634 712,666 C716,686 716,700 712,708 "
       "C718,714 730,715 738,709 C742,701 741,691 738,682 "
       "C735,654 738,622 746,596 C751,576 750,560 742,551 "
       "C732,545 718,547 712,556 Z",
       "Rear leg far", fill="#5E4426", opacity=30, stroke=NONE)

# --- forebody: the solid half -------------------------------------------------------------
d.path("M420,470 C450,432 512,412 572,414 C602,416 624,426 634,442 "
       "C648,474 648,532 632,568 C602,596 512,604 462,584 "
       "C430,568 414,522 420,470 Z",
       "Forebody", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# pale belly running the length of the underside
d.path("M448,552 C500,578 580,584 640,570 C600,594 510,600 466,582 "
       "C450,574 442,562 448,552 Z", "Belly pale",
       fill=PALE, opacity=55, stroke=NONE)

# --- hind legs near: translucent like the quarters ------------------------------------------
d.path("M668,556 C660,594 660,636 668,670 C672,690 672,704 668,712 "
       "C674,719 688,720 696,714 C700,705 699,695 696,685 "
       "C693,656 696,622 704,594 C709,574 708,558 700,549 "
       "C688,543 674,546 668,556 Z",
       "Rear leg near", fill=RUMP_GRAD, opacity=42, stroke=INK, strokeWidth=4)
d.path("M668,700 C666,709 668,716 676,719 L698,719 C703,715 702,707 696,702 "
       "C686,706 676,706 668,700 Z", "Rear hoof", fill="#3A2C1A",
       opacity=42, stroke=NONE)

# --- front legs near: solid, with the last pale bands --------------------------------------
d.path("M476,556 C470,594 468,636 474,672 C477,692 476,706 472,714 "
       "C476,722 490,724 500,719 C505,712 505,702 503,694 "
       "C500,664 503,630 510,600 C515,578 514,558 506,548 "
       "C494,542 482,546 476,556 Z",
       "Front leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path("M472,702 C470,711 472,719 480,722 L502,722 C507,718 506,709 500,704 "
       "C490,708 480,707 472,702 Z", "Front hoof", fill="#3A2C1A",
       stroke=INK, strokeWidth=4)
# leg bands — the striping gives up before the hoof does
d.path("M476,606 C488,612 500,612 510,606", "Front band 1", fill=NONE,
       stroke=STRIPE, strokeWidth=8, opacity=55, cap="round")
d.path("M476,652 C486,657 496,657 504,652", "Front band 2", fill=NONE,
       stroke=STRIPE, strokeWidth=6, opacity=32, cap="round")

# --- the stripes dying across the shoulder ---------------------------------------------------
for i, (dd, w, o) in enumerate([
        ("M468,434 C458,474 456,518 464,556", 12, 88),
        ("M502,424 C492,468 490,518 498,560", 12, 72),
        ("M538,420 C528,466 527,518 534,560", 11, 48),
        ("M576,422 C568,466 567,514 574,552", 10, 26),
        ("M616,426 C610,468 610,514 616,548", 9, 14)]):
    d.path(dd, f"Flank stripe {i+1}", fill=NONE, stroke=STRIPE,
           strokeWidth=w, opacity=o, cap="round")

# --- neck: the striped column -----------------------------------------------------------------
d.path("M352,352 C390,360 424,384 446,420 C466,454 478,500 482,548 "
       "C484,574 476,596 458,600 C432,604 404,586 388,558 "
       "C368,524 358,480 360,438 C362,408 358,378 352,352 Z",
       "Neck", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# throat shade under the neck
d.path("M370,470 C380,516 402,556 436,584 C410,578 384,556 372,524 "
       "C362,498 360,482 370,470 Z", "Throat shade",
       fill="#74562F", opacity=40, stroke=NONE)
# bold bands wrapping the neck
for i, dd in enumerate([
        "M352,376 C376,400 388,434 392,472",
        "M374,370 C400,398 413,436 417,480",
        "M398,372 C426,404 440,446 444,494",
        "M424,384 C452,420 464,462 468,512"]):
    d.path(dd, f"Neck stripe {i+1}", fill=NONE, stroke=STRIPE,
           strokeWidth=11, opacity=88, cap="round")
# the short erect mane — striped tufts along the crest
for k, (bx, by, tx, ty) in enumerate([
        (352, 356, 336, 318), (372, 362, 362, 322), (394, 372, 388, 332),
        (416, 388, 414, 348), (436, 408, 438, 370), (452, 428, 458, 394)]):
    d.path(f"M{bx-8},{by} Q{(bx+tx)//2 - 4},{(by+ty)//2 - 8} {tx},{ty} "
           f"Q{(bx+tx)//2 + 8},{(by+ty)//2 - 2} {bx+8},{by} Z",
           f"Mane tuft {k+1}", fill=STRIPE if k % 2 == 0 else "#C4AE7C",
           stroke=INK, strokeWidth=2.5)

# --- ears -------------------------------------------------------------------------------------
d.path("M344,340 C334,318 332,296 342,282 C352,272 366,276 372,290 "
       "C376,306 372,326 360,340 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M350,326 C344,310 344,294 352,286 C360,292 362,308 356,322 Z",
       "Inner ear", fill="#74562F", opacity=70, stroke=NONE)
d.path("M348,290 C354,278 362,274 370,276 C366,286 358,292 348,290 Z",
       "Ear tip", fill=STRIPE, opacity=85, stroke=NONE)
d.path("M368,334 C366,314 370,296 382,286 C392,280 402,284 404,296 "
       "C404,312 396,328 384,336 Z", "Ear far", fill="#9A7C4E",
       stroke=INK, strokeWidth=3.5)

# --- head: the long equine wedge ---------------------------------------------------------------
d.path("M352,344 C330,340 306,352 288,374 C268,398 246,428 230,454 "
       "C220,470 218,484 228,492 C240,500 258,498 274,490 "
       "C300,478 322,462 340,442 C358,420 368,392 366,368 "
       "C365,356 360,348 352,344 Z",
       "Head", fill=lin(360, 350, 225, 480, (0, "#D8C4A0"), (0.55, "#AC8A5C"), (1, "#74562F")),
       stroke=INK, strokeWidth=5)
# face stripes converging toward the muzzle
for i, (dd, w) in enumerate([
        ("M306,368 C320,392 328,418 332,444", 8),
        ("M280,392 C294,416 302,442 306,468", 8),
        ("M254,424 C264,442 270,458 272,476", 7)]):
    d.path(dd, f"Face stripe {i+1}", fill=NONE, stroke=STRIPE,
           strokeWidth=w, opacity=85, cap="round")
# dark muzzle
d.path("M230,452 C220,468 218,484 228,492 C240,500 258,498 272,490 "
       "C264,476 252,462 240,454 C236,451 232,450 230,452 Z",
       "Muzzle", fill="#503A28", stroke=NONE)
d.path("M236,468 C232,460 240,452 250,454 C258,456 262,464 258,472 "
       "C252,480 240,478 236,468 Z", "Nostril",
       fill="#140C08", opacity=85, stroke=NONE)
d.path("M238,486 C252,490 268,488 280,480", "Mouth", fill=NONE,
       stroke="#140C08", strokeWidth=3.5, opacity=70, cap="round")
# eye
d.shape("ellipse", "Eye socket", x=302, y=400, width=28, height=22,
        fill="#241708", opacity=35, stroke=NONE)
d.shape("ellipse", "Eye", x=308, y=404, width=15, height=14,
        fill="#140C06", stroke=NONE)
d.shape("ellipse", "Eye glint", x=312, y=407, width=4.5, height=4.5,
        fill="#FFF0D4", opacity=85, stroke=NONE)
# forehead sheen
d.shape("ellipse", "Brow sheen", x=300, y=350, width=60, height=26,
        fill="#FFFFFF", opacity=15, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#3E3018", strokeWidth=6)

# --- name ---------------------------------------------------------------------------------
d.text("QUAGGA", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#EFE4C0", justify="center")

d.finish("quagga-V1R00")
