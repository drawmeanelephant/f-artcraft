#!/usr/bin/env python3
"""Honey badger — field-guide plate V1R00. The animal the hive, the snake
and the leopard all declined to argue with: low-slung profile walking flat
out, pale mantle over black everything-else, long foreclaws out. Thornveld
plate, no-fear mood — flat-top acacia, a hanging log hive it has already
forgotten, thorn scrub on dusty ground. Floor closes on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Honey Badger — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#201408"                    # warm dark ink, never pure black

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

def on_disc(x, y, pad=0, r=R):
    return math.hypot(x - CX, y - CY) <= r - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#181108"), (1, "#070402"))
PLATE_GRAD = rad((0, "#EAD9AE"), (0.55, "#B8945A"), (1, "#60451E"))
DUST_GRAD = lin(0, 690, 0, 880, (0, "#B08C4E"), (0.6, "#6E4C20"), (1, "#38260E"))
FUR_GRAD = lin(400, 440, 560, 600, (0, "#33291F"), (0.6, "#1E1710"), (1, "#0E0906"))
MANTLE_GRAD = lin(0, 430, 0, 540, (0, "#E2DCCB"), (0.6, "#B4AC98"), (1, "#8A8270"))

# --- backdrop + thornveld plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#B8945A", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#42300F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4E8C4", strokeWidth=3, opacity=40)

# late-afternoon light pool, high right
d.shape("ellipse", "Light pool", x=580, y=140, width=280, height=220,
        fill=rad((0, "#F8ECC0", 45), (1, "#F8ECC0", 0)), stroke=NONE)

# flat-top acacia on the horizon — the thornveld itself
d.path("M168,566 C210,548 300,542 372,548 C420,552 448,560 452,568 "
       "C446,578 390,584 310,584 C240,584 180,578 168,566 Z",
       "Acacia canopy", fill="#3E2C10", opacity=70, stroke=NONE)
d.path("M306,584 C302,620 300,660 302,694 L314,694 C314,660 312,620 314,584 Z",
       "Acacia trunk", fill="#3E2C10", opacity=70, stroke=NONE)
d.path("M240,584 C236,610 234,640 236,668 M380,582 C384,606 386,634 384,660",
       "Acacia boughs", fill=NONE, stroke="#3E2C10", strokeWidth=5, opacity=70, cap="round")
# the log hive hanging under the canopy — already argued with, already lost
d.path("M258,592 C248,594 242,604 244,616 C246,628 254,636 264,634 "
       "C274,630 278,616 274,604 C271,595 266,590 258,592 Z",
       "Log hive", fill="#2E2010", opacity=80, stroke=NONE)
d.path("M258,592 C260,586 264,582 268,580", "Hive rope", fill=NONE,
       stroke="#3E2C10", strokeWidth=3, opacity=70, cap="round")
for i, (x, y) in enumerate([(234, 610), (282, 606), (252, 648), (292, 640), (228, 636)]):
    d.shape("ellipse", f"Bee {i+1}", x=x, y=y, width=5, height=5,
            fill="#2E2010", opacity=60, stroke=NONE)
# two tick birds crossing the hot sky
for i, (x, y) in enumerate([(690, 300), (750, 268)]):
    d.path(f"M{x},{y} Q{x+8},{y-7} {x+16},{y} Q{x+8},{y-3} {x},{y} Z",
           f"Bird {i+1}", fill="#4A3618", opacity=55, stroke=NONE)

# --- dusty floor closing on the disc's own arc -------------------------------------
dy = 692
dl, dr = rim_x(dy, side=-1), rim_x(dy, side=1)
d.path(f"M{dl:.1f},{dy} C320,676 430,700 540,694 C640,688 720,690 {dr:.1f},{dy} "
       f"A{R},{R} 0 0 1 {dl:.1f},{dy} Z", "Dust floor", fill=DUST_GRAD, stroke=NONE)
d.path(f"M{dl+8:.0f},{dy} C320,676 430,700 540,694 C640,688 720,690 {dr-8:.0f},{dy}",
       "Floor crest", fill=NONE, stroke="#E4C68A", strokeWidth=5, opacity=45, cap="round")
# thorn scrub on the floor — angular zigzags, not grass
for i, (x, y, s) in enumerate([(200, 730, 1), (770, 724, -1), (830, 738, 1),
                               (300, 748, -1), (700, 746, 1), (160, 716, -1)]):
    d.path(f"M{x},{y} L{x + 12*s},{y - 16} L{x + 8*s},{y - 26} M{x + 12*s},{y - 16} L{x + 22*s},{y - 22}",
           f"Thorn {i+1}", fill=NONE, stroke="#5E4218", strokeWidth=3.5,
           opacity=65, cap="round")
# dust puffs at the heels — the pace is the attitude
for i, (x, y, w, o) in enumerate([(300, 650, 50, 26), (262, 668, 64, 30),
                                  (330, 676, 44, 22), (226, 686, 52, 20)]):
    d.shape("ellipse", f"Dust {i+1}", x=x - w/2, y=y - w/4, width=w, height=w/2,
            fill="#D8BC78", opacity=o, stroke=NONE)
# contact shadow, wide and low like the animal
d.shape("ellipse", "Contact shadow", x=380, y=680, width=340, height=18,
        fill="#241708", opacity=45, stroke=NONE)

# --- the badger: black underneath, mantle over the top ------------------------------
# far legs first — darker, planted a half-pace back
d.path("M382,556 C376,592 374,632 378,662 C386,670 402,670 408,662 "
       "C410,628 408,588 404,556 C398,548 386,548 382,556 Z",
       "Rear leg far", fill="#14100A", stroke=INK, strokeWidth=4)
d.path("M690,548 C684,584 682,624 686,656 C694,664 710,664 716,656 "
       "C718,622 716,582 712,548 C706,540 694,540 690,548 Z",
       "Front leg far", fill="#14100A", stroke=INK, strokeWidth=4)
d.path("M378,656 L366,676 M392,658 L386,678 M404,658 L402,678",
       "Rear claws far", fill=NONE, stroke="#14100A", strokeWidth=3, opacity=60, cap="round")

# tail: short and bushy, carried low off the rump
d.path("M330,486 C302,492 284,512 278,538 C274,558 284,570 300,568 "
       "C318,562 330,542 336,518 C340,502 338,490 330,486 Z",
       "Tail", fill=FUR_GRAD, stroke=INK, strokeWidth=5)

# body silhouette — the long low slab, shoulders heavy, head carried level
d.path("M330,470 C360,446 430,436 505,438 C575,440 636,438 660,448 "
       "C700,452 726,466 744,490 C756,504 760,518 754,528 "
       "C746,540 726,544 708,538 C700,556 686,572 664,580 "
       "C558,600 438,598 376,572 C348,562 330,540 324,512 "
       "C320,494 322,480 330,470 Z",
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
# belly sag + rear shading
d.path("M376,556 C444,576 560,578 636,562 C596,584 480,590 404,574 "
       "C388,570 380,564 376,556 Z", "Belly shade", fill="#0A0604",
       opacity=50, stroke=NONE)

# the mantle: pale saddle draped from crown to rump, wrapping the flanks
d.path("M334,470 C364,446 432,436 502,438 C572,440 636,438 660,448 "
       "C696,452 716,464 732,486 C738,496 734,504 724,506 "
       "C682,500 620,492 540,490 C460,488 390,494 346,512 "
       "C336,498 332,484 334,470 Z",
       "Mantle", fill=MANTLE_GRAD, stroke=INK, strokeWidth=4)
# mantle edge: ragged wisps where the grizzle frays into black
for i, (x, y) in enumerate([(392, 500), (468, 490), (546, 490), (620, 492)]):
    d.path(f"M{x},{y} C{x+8},{y+8} {x+12},{y+16} {x+10},{y+24}",
           f"Mantle fray {i+1}", fill=NONE, stroke="#C9C1AC",
           strokeWidth=5, opacity=45, cap="round")

# near legs — thick columns, front paw mid-stride reaching forward
d.path("M412,560 C404,596 402,636 408,668 C418,676 438,676 446,668 "
       "C450,634 448,594 444,560 C436,550 418,550 412,560 Z",
       "Rear leg near", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.path("M408,662 C396,668 390,678 398,684 C410,688 428,686 438,678 "
       "C440,670 430,662 418,660 Z", "Rear paw", fill="#1A130C",
       stroke=INK, strokeWidth=4)
d.path("M652,552 C646,588 640,628 642,660 C650,670 670,672 680,664 "
       "C688,634 690,594 688,556 C682,546 660,542 652,552 Z",
       "Front leg near", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.path("M640,656 C628,660 620,670 628,678 C640,684 660,682 670,674 "
       "C672,666 662,656 650,654 Z", "Front paw", fill="#1A130C",
       stroke=INK, strokeWidth=4)
# the digging claws — pale, long, unbothered
for k, (x, y, dx) in enumerate([(630, 676, -16), (644, 680, -9), (658, 681, -2)]):
    d.path(f"M{x},{y} Q{x + dx*0.6},{y + 9} {x + dx},{y + 14}",
           f"Foreclaw {k+1}", fill=NONE, stroke="#D8D2C4",
           strokeWidth=4, opacity=85, cap="round")

# ear — barely a crease inside the crown line (they are famously vestigial)
d.path("M664,458 C668,451 676,449 684,453", "Ear crease", fill=NONE,
       stroke="#0A0604", strokeWidth=3.5, opacity=60, cap="round")
# nose + set jaw under the mantle's brow line
d.shape("ellipse", "Nose", x=738, y=512, width=20, height=15,
        fill="#0A0604", stroke=INK, strokeWidth=3)
d.path("M708,534 C722,541 738,540 750,530", "Jaw line", fill=NONE,
       stroke="#0A0604", strokeWidth=4, opacity=80, cap="round")
# the eye — small, dark, forward, just under the pale brow
d.shape("ellipse", "Eye", x=710, y=508, width=13, height=12,
        fill="#0A0604", stroke=NONE)
d.shape("ellipse", "Eye glint", x=714, y=510, width=3.5, height=3.5,
        fill="#FFF6DC", opacity=80, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#241708", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
d.text("HONEY BADGER", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#F4E6BC", justify="center")

d.finish("honey-badger-V1R00")
