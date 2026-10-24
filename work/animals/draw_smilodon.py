#!/usr/bin/env python3
"""Smilodon — field-guide plate V1R00. Saber teeth long enough to be a
liability: tar-pit plate, Pleistocene mood. Heavy-shouldered cat in left
profile picking its way along a glossy tar seep, sabers hanging past the
jaw, half-sunk bones and a far mammoth line on the dusk ridge. The tar
pool closes on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Smilodon — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#2E1A0C"                    # warm dark ink, never pure black

def lin(x0, y0, x1, y1, *stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": ss}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#140D06"), (1, "#070402"))
PLATE_GRAD = rad((0, "#C9AE7C"), (0.5, "#8A6E44"), (1, "#3C2C18"))
CAT_GRAD = lin(380, 420, 620, 700, (0, "#B9925A"), (0.5, "#8E6A3C"), (1, "#5C4022"))
TAR_GRAD = lin(0, 730, 0, 890, (0, "#241A10"), (0.5, "#120C08"), (1, "#0A0604"))
BONE = "#D8C9A4"
SABER = "#EDE2C0"
RIDGE = "#4A361C"

# --- backdrop + tar-pit plate ------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#8A6E44", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2A1E10", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D4AE", strokeWidth=3, opacity=40)

# the low Pleistocene sun, drowning in dust
d.shape("ellipse", "Sun halo", x=560, y=230, width=300, height=300,
        fill=rad((0, "#E8D8A8", 28), (0.6, "#E8D8A8", 10), (1, "#E8D8A8", 0)),
        stroke=NONE)
d.shape("ellipse", "Sun", x=634, y=304, width=150, height=150,
        fill=rad((0, "#F0E2B4"), (0.8, "#E0CD9C"), (1, "#B89C62")), stroke=NONE)
# dust hanging in the air
for i, (x, y, w) in enumerate([(220, 240, 4), (330, 170, 5), (470, 300, 4),
                               (180, 400, 5), (820, 380, 4), (720, 170, 5),
                               (600, 140, 4), (150, 560, 4), (850, 560, 5),
                               (390, 120, 3), (770, 470, 4), (260, 640, 4)]):
    d.shape("ellipse", f"Dust {i+1}", x=x, y=y, width=w, height=w,
            fill="#E4D4AE", opacity=30, stroke=NONE)

# the far ridge — a mammoth line trailing across the dusk
d.path("M130,648 C260,628 400,636 520,632 C640,628 760,624 868,640 "
       "L868,668 L130,668 Z", "Far ridge", fill=RIDGE, opacity=55, stroke=NONE)
for i, (x, s) in enumerate([(668, 1.0), (740, 0.82), (800, 0.66)]):
    y = 640 - 4 * s
    d.path(f"M{x},{y} C{x-14*s},{y-26*s} {x+4*s},{y-38*s} {x+22*s},{y-36*s} "
           f"C{x+38*s},{y-34*s} {x+46*s},{y-20*s} {x+44*s},{y-8*s} "
           f"L{x+40*s},{y} L{x+34*s},{y} L{x+33*s},{y-8*s} "
           f"L{x+18*s},{y-8*s} L{x+17*s},{y} L{x+11*s},{y} L{x+10*s},{y-8*s} "
           f"L{x-4*s},{y-8*s} L{x-5*s},{y} L{x-11*s},{y} Z "
           f"M{x-14*s},{y-22*s} C{x-20*s},{y-16*s} {x-22*s},{y-8*s} {x-18*s},{y-2*s} "
           f"L{x-14*s},{y-4*s} C{x-17*s},{y-10*s} {x-16*s},{y-16*s} {x-12*s},{y-19*s} Z",
           f"Mammoth {i+1}", fill=RIDGE, opacity=70, stroke=NONE)

# cracked dry flats between ridge and tar
for i, (x0, y0, x1, y1) in enumerate([(170, 690, 250, 706), (430, 678, 500, 690),
                                      (590, 692, 660, 682), (760, 676, 830, 688),
                                      (320, 700, 360, 714)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Crack {i+1}", fill=NONE,
           stroke="#3A2A14", strokeWidth=3, opacity=40, cap="round")

# --- the tar seep, closing on the disc's own arc --------------------------------------
fy = 736
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C300,720 420,744 560,738 C660,734 760,730 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Tar pool", fill=TAR_GRAD, stroke=NONE)
d.path(f"M{fl+8:.0f},{fy} C300,720 420,744 560,738 C660,734 760,730 {fr-8:.0f},{fy}",
       "Tar crest", fill=NONE, stroke="#C9AE7C", strokeWidth=4, opacity=35, cap="round")
# glossy sheen — the sky coming back off the tar
for i, (x, y, w) in enumerate([(330, 770, 190), (560, 794, 240), (720, 758, 130)]):
    d.shape("ellipse", f"Tar sheen {i+1}", x=x - w/2, y=y, width=w, height=10,
            fill="#E8C890", opacity=13, stroke=NONE)
# a bubble mid-bloop
d.shape("ellipse", "Tar bubble", x=596, y=762, width=16, height=10,
        fill=NONE, stroke="#C9AE7C", strokeWidth=3, opacity=30)

# bones the seep already claimed — a ribcage off the left shoulder,
# one long bone adrift at right
for k in range(5):
    x = 210 + k * 22
    d.path(f"M{x},{746 + k*2} C{x-4},{722} {x+2},{698} {x+16},{684}",
           f"Rib {k+1}", fill=NONE, stroke=BONE, strokeWidth=6,
           opacity=70 - k * 6, cap="round")
d.path("M186,752 C226,744 286,742 330,748", "Ribcage spine", fill=NONE,
       stroke=BONE, strokeWidth=5, opacity=55, cap="round")
d.path("M706,764 L792,742 L798,752 L712,774 Z", "Long bone", fill=BONE,
       opacity=55, stroke=NONE)
for i, (x, y) in enumerate([(706, 758), (794, 746)]):
    d.shape("ellipse", f"Bone end {i+1}", x=x, y=y, width=16, height=14,
            fill=BONE, opacity=55, stroke=NONE)

# contact shadow under the cat
d.shape("ellipse", "Cat shadow", x=330, y=720, width=420, height=22,
        fill="#100A06", opacity=40, stroke=NONE)

# --- the cat --------------------------------------------------------------------------
# tapered multi-joint limbs, same idiom as the wolverine plate
def limb(label, pts, widths, fill, **kw):
    n = len(pts)
    L, Rr = [], []
    for i in range(n):
        ax, ay = pts[max(i - 1, 0)]
        bx, by = pts[min(i + 1, n - 1)]
        dx, dy = bx - ax, by - ay
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = widths[i] / 2
        L.append((pts[i][0] + nx * w, pts[i][1] + ny * w))
        Rr.append((pts[i][0] - nx * w, pts[i][1] - ny * w))
    dd = "M%.1f,%.1f " % L[0]
    for i in range(1, n):
        mx, my = (L[i - 1][0] + L[i][0]) / 2, (L[i - 1][1] + L[i][1]) / 2
        dd += ("Q%.1f,%.1f %.1f,%.1f " % (L[i-1][0], L[i-1][1], mx, my)) if i > 1 else ("L%.1f,%.1f " % (mx, my))
    dd += "L%.1f,%.1f L%.1f,%.1f " % (L[-1] + Rr[-1])
    for i in range(n - 2, -1, -1):
        dd += "L%.1f,%.1f " % Rr[i]
    d.path(dd + "Z", label, fill=fill, **kw)

def paw(label, cx, cy, fill):
    d.path(f"M{cx+22},{cy} C{cx+24},{cy-14} {cx+8},{cy-20} {cx-10},{cy-19} "
           f"C{cx-28},{cy-18} {cx-36},{cy-8} {cx-34},{cy} Z",
           label, fill=fill, stroke=INK, strokeWidth=3.5)
    for j, ox in enumerate([-30, -21, -12]):
        d.path(f"M{cx+ox},{cy-4} Q{cx+ox-8},{cy-1} {cx+ox-9},{cy+6}",
               f"{label} claw {j+1}", fill=NONE, stroke="#E8DCC8",
               strokeWidth=3, opacity=70, cap="round")

# far legs (behind the body), a half-pace back
limb("Foreleg far", [(462, 560), (468, 620), (472, 680), (474, 730)],
     [58, 48, 38, 32], "#5C4022", stroke=INK, strokeWidth=3.5)
paw("Forepaw far", 474, 736, "#4A3018")
limb("Hindleg far", [(556, 570), (566, 630), (572, 686), (566, 730)],
     [62, 50, 38, 32], "#5C4022", stroke=INK, strokeWidth=3.5)
paw("Hindpaw far", 560, 736, "#4A3018")

# the bob tail — a stub hugging the rump
d.path("M682,486 C696,490 704,502 702,516 C700,528 690,534 682,530 "
       "C676,522 676,504 678,490 Z", "Bobtail", fill="#8E6A3C",
       stroke=INK, strokeWidth=4)

# torso — withers peak over the shoulders, back sloping to a low rump,
# brisket dipping under the belly line; the head overlaps its front
d.path("M392,452 C376,466 368,486 370,508 "                    # throatlatch front
       "C372,536 380,560 398,576 "                            # chest to brisket
       "C424,592 470,598 528,596 "                            # belly
       "C580,594 630,584 656,566 "                            # rump bottom
       "C676,552 686,530 682,504 "                            # rear curve
       "C678,478 660,458 630,446 "                            # rump top
       "C580,430 524,416 478,412 "                            # back to withers
       "C444,410 416,414 398,426 "                            # neck top dip
       "C394,434 392,444 392,452 Z",
       "Body", fill=CAT_GRAD, stroke=INK, strokeWidth=6)
# muscle + mood shading laid over the torso
d.shape("ellipse", "Withers mass", x=404, y=416, width=150, height=110,
        fill="#D8B87E", opacity=22, stroke=NONE)
d.path("M398,556 C460,580 560,586 640,566 C596,592 480,598 430,582 "
       "C412,576 400,568 398,556 Z", "Belly shade", fill="#4A3018",
       opacity=42, stroke=NONE)
# faint flank barring, ghosts of kitten spots
for i, (x, y, h) in enumerate([(500, 460, 40), (538, 468, 38), (574, 480, 32)]):
    d.path(f"M{x},{y} C{x+6},{y+14} {x+6},{y+26} {x+2},{y+h}",
           f"Flank bar {i+1}", fill=NONE, stroke="#5C4022",
           strokeWidth=6, opacity=30, cap="round")

# near legs — massive forelimb reaching a half-step forward
limb("Foreleg near", [(412, 540), (404, 596), (392, 656), (380, 700), (366, 734)],
     [72, 62, 48, 38, 32], CAT_GRAD, stroke=INK, strokeWidth=4.5)
paw("Forepaw near", 362, 738, "#8E6A3C")
limb("Hindleg near", [(632, 540), (648, 590), (662, 646), (668, 696), (682, 732)],
     [84, 68, 50, 38, 32], CAT_GRAD, stroke=INK, strokeWidth=4.5)
paw("Hindpaw near", 686, 738, "#8E6A3C")
# haunch mass over the hip
d.path("M600,470 C656,458 700,496 700,540 C700,576 684,600 664,614 "
       "C630,586 604,534 600,470 Z", "Haunch", fill=CAT_GRAD,
       stroke=NONE)
d.path("M664,614 C684,600 700,576 700,540", "Haunch edge", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=50, cap="round")

# head — square deep muzzle, blunt jaw, set low and forward off the chest
d.path("M236,500 C232,512 232,524 240,534 "                    # nose front
       "C252,546 268,554 288,558 "                            # chin
       "C314,564 344,560 362,546 "                            # jaw underside
       "C382,532 392,512 392,488 "                            # throatlatch back
       "C392,462 384,442 368,430 "                            # neck to poll
       "C348,420 324,422 304,432 "                            # skull top
       "C282,440 266,454 254,468 "                            # forehead
       "C248,476 240,486 236,500 Z",                          # stop + bridge
       "Head", fill=CAT_GRAD, stroke=INK, strokeWidth=6)
# neck mass closing over the head-torso seam
d.path("M340,440 C380,432 416,438 438,458 C452,484 452,524 442,560 "
       "C426,580 396,584 368,570 C348,548 338,492 340,440 Z",
       "Neck mass", fill=CAT_GRAD, stroke=NONE)
d.shape("ellipse", "Jowl mass", x=282, y=494, width=70, height=58,
        fill="#D8B87E", opacity=20, stroke=NONE)
# ear — small, rounded, laid back over the poll
d.path("M342,432 C344,410 358,396 376,398 C386,408 384,426 372,436 "
       "C360,440 348,440 342,432 Z", "Ear", fill="#8E6A3C",
       stroke=INK, strokeWidth=4)
d.path("M352,426 C356,416 366,410 374,412", "Ear inner", fill=NONE,
       stroke="#4A3018", strokeWidth=3.5, opacity=60, cap="round")

# face — nose leather, brow ridge, mouth line shut on the teeth
d.path("M230,496 C226,506 228,516 236,522 C244,526 254,522 258,514 "
       "C258,504 250,496 240,494 Z", "Nose", fill="#1E1008", stroke=NONE)
d.path("M276,448 C300,438 332,436 354,446", "Brow ridge", fill=NONE,
       stroke="#5C4022", strokeWidth=6, opacity=50, cap="round")
d.path("M246,540 C270,550 300,552 324,546", "Mouth", fill=NONE,
       stroke="#1E1008", strokeWidth=4, opacity=80, cap="round")
d.path("M290,470 C300,464 312,464 320,470 C312,478 300,478 290,470 Z",
       "Eye", fill="#1E1008", stroke=NONE)
d.shape("ellipse", "Eye glint", x=302, y=467, width=4.5, height=4.5,
        fill="#F0E2B4", opacity=85, stroke=NONE)
# whiskers — three fine sweeps off the muzzle
for i, dy in enumerate((0, 8, 16)):
    d.path(f"M246,{516+dy} C216,{510+dy} 188,{508+dy} 166,{514+dy}",
           f"Whisker {i+1}", fill=NONE, stroke="#E4D4AE",
           strokeWidth=2.6, opacity=55, cap="round")

# the liability — blades rooted back on the top jaw, tapering to a point,
# the far saber a sliver behind the near blade
d.path("M316,534 C320,572 328,614 340,644 C344,656 354,652 354,640 "
       "C346,602 342,564 344,532 C336,526 324,526 316,534 Z",
       "Saber far", fill="#C9B88E", stroke=INK, strokeWidth=4)
d.path("M288,524 C280,558 278,614 290,672 C293,688 304,688 306,674 "
       "C300,630 300,580 308,536 C302,526 294,522 288,524 Z",
       "Saber near", fill=SABER, stroke=INK, strokeWidth=4.5)
d.path("M295,540 C292,584 294,630 301,664", "Saber sheen", fill=NONE,
       stroke="#FFF6DC", strokeWidth=3, opacity=60, cap="round")
d.path("M284,516 C294,508 310,508 318,518 C316,528 306,534 294,532 "
       "C286,528 282,522 284,516 Z", "Saber root", fill=CAT_GRAD,
       stroke=INK, strokeWidth=3.5)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#140C06", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
d.text("SMILODON", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#E4D4AE", justify="center")

d.finish("smilodon-V1R00")
