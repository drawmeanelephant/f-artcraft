#!/usr/bin/env python3
"""Meerkat — field-guide plate V1R00. Sentinel duty at one kilogram: upright
on the hind legs, forepaws folded at the chest, dark eye-mask scanning the
Kalahari at dawn. Low sun on the horizon, long shadow thrown across the
sand, a burrow mound and a far second sentinel for depth. Sand floor closes
on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Meerkat — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#2A1808"                    # warm dark ink, never pure black

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

BG_GRAD = lin(0, 0, 0, 1000, (0, "#1C1008"), (1, "#080402"))
PLATE_GRAD = rad((0, "#F4DEAE"), (0.55, "#D9A868"), (1, "#8A5A2C"))
SAND_GRAD = lin(0, 700, 0, 880, (0, "#CE9E58"), (0.6, "#8A5E2C"), (1, "#4A2E14"))
FUR_GRAD = lin(460, 480, 580, 700, (0, "#C69A5E"), (0.6, "#9A6C34"), (1, "#6A4420"))
PALE = "#EBD6AC"
DARK = "#3A2410"                   # mask, ears, paw tips

# --- backdrop + Kalahari dawn plate -------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#D9A868", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A3014", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F8ECD0", strokeWidth=3, opacity=40)

# dawn sun, low over the horizon; glow fades on per-stop opacity before the rim
d.shape("ellipse", "Sun glow", x=550, y=490, width=280, height=220,
        fill=rad((0, "#FBE8B4", 70), (1, "#F4D290", 0)), stroke=NONE)
d.shape("ellipse", "Sun", x=626, y=548, width=110, height=110,
        fill=rad((0, "#FDF3C8"), (0.75, "#F0C878"), (1, "#DEA04E")),
        opacity=95, stroke=NONE)
# heat haze band where the sun meets the dune line
d.path("M560,660 C640,650 720,652 800,660", "Horizon haze", fill=NONE,
       stroke="#F4DCA0", strokeWidth=8, opacity=30, cap="round")

# far dune crest, just above the floor line
d.path("M170,664 C300,640 420,656 560,650 C660,646 740,652 830,644 "
       "L830,700 L170,700 Z", "Dune ridge",
       fill=lin(0, 640, 0, 700, (0, "#B08048"), (1, "#8A5E2C")),
       opacity=45, stroke=NONE)

# a far second sentinel on the dune line — the mob is never off duty
d.path("M318,602 C326,598 336,598 342,604 C346,616 348,640 346,660 "
       "C340,666 324,666 318,660 C314,640 314,614 318,602 Z",
       "Far sentinel body", fill="#6A4420", opacity=55, stroke=NONE)
d.shape("ellipse", "Far sentinel head", x=322, y=590, width=22, height=18,
        fill="#6A4420", opacity=55, stroke=NONE)

# --- sand floor closing on the disc's own arc -----------------------------------
gy = 706
gl, gr = rim_x(gy, side=-1), rim_x(gy, side=1)
d.path(f"M{gl:.1f},{gy} C300,690 420,714 520,706 C620,698 720,700 {gr:.1f},{gy} "
       f"A{R},{R} 0 0 1 {gl:.1f},{gy} Z", "Sand floor", fill=SAND_GRAD, stroke=NONE)
d.path(f"M{gl+8:.0f},{gy} C300,690 420,714 520,706 C620,698 720,700 {gr-8:.0f},{gy}",
       "Floor crest", fill=NONE, stroke="#EBC888", strokeWidth=5, opacity=45, cap="round")

# burrow mound, left of the figure
d.shape("ellipse", "Burrow mound", x=172, y=690, width=170, height=46,
        fill=lin(172, 690, 342, 736, (0, "#9A6C36"), (1, "#5E3A18")),
        opacity=80, stroke=NONE)
d.shape("ellipse", "Burrow mouth", x=222, y=702, width=64, height=22,
        fill="#2E1A0C", opacity=85, stroke=NONE)

# dry grass tufts on the floor
for i, (x, y, s) in enumerate([(248, 742, 1), (356, 752, -1), (646, 748, 1),
                               (724, 742, -1), (788, 730, 1), (180, 752, -1)]):
    for j, (dx, dy) in enumerate([(-7, -22), (0, -30), (7, -20)]):
        d.path(f"M{x},{y} Q{x + dx*0.5},{y + dy*0.6} {x + dx + s*j*3},{y + dy}",
               f"Grass {i+1}.{j+1}", fill=NONE, stroke="#D4B070",
               strokeWidth=3.5, opacity=55, cap="round")

# long dawn shadow thrown left across the sand
d.path("M502,720 C420,736 340,756 284,774 L320,788 C392,766 462,742 522,728 Z",
       "Cast shadow", fill="#3A2410", opacity=25, stroke=NONE)
# contact shadow under the base + tail
d.shape("ellipse", "Contact shadow", x=430, y=712, width=230, height=20,
        fill="#2E1A0C", opacity=45, stroke=NONE)
d.shape("ellipse", "Tail shadow", x=600, y=722, width=170, height=12,
        fill="#2E1A0C", opacity=30, stroke=NONE)

# --- tail: the third leg of the tripod, trailing right along the sand -----------
d.path("M576,664 C630,688 692,704 748,712 C762,714 764,726 752,730 "
       "C694,732 626,722 572,700 C562,690 564,672 576,664 Z",
       "Tail", fill=lin(576, 664, 748, 730, (0, "#9A6C34"), (0.7, "#7A4E24"), (1, "#3A2410")),
       stroke=INK, strokeWidth=4)
d.path("M714,708 C732,710 750,712 752,718 C754,726 746,730 734,730 "
       "C722,728 712,720 714,708 Z", "Tail tip", fill=DARK, stroke=NONE)

# --- body: the upright sentinel column -------------------------------------------
d.path("M474,494 C448,514 438,558 442,606 C446,654 454,692 472,712 "
       "C490,724 550,724 568,712 C586,692 594,654 598,606 "
       "C602,558 592,514 566,494 C552,480 488,480 474,494 Z",
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
# pale belly + chest plane — warm tawny, not white, so the column stays fur
d.path("M486,520 C472,548 470,610 480,658 C488,688 552,688 560,658 "
       "C570,610 568,548 554,520 C542,506 498,506 486,520 Z",
       "Belly", fill="#E6CC9C", opacity=80, stroke=NONE)
# grizzled back bands wrapping the shoulders
for i, dd in enumerate(["M452,540 C470,528 494,522 516,522",
                        "M588,540 C570,528 546,522 524,522",
                        "M446,580 C460,570 478,564 494,564",
                        "M594,580 C580,570 562,564 546,564"]):
    d.path(dd, f"Back band {i+1}", fill=NONE, stroke="#5E3A18",
           strokeWidth=9, opacity=50, cap="round")
# flank shading keeps the column round
d.path("M444,560 C440,610 446,660 460,700", "Flank shade L", fill=NONE,
       stroke="#5E3A18", strokeWidth=10, opacity=35, cap="round")
d.path("M596,560 C600,610 594,660 580,700", "Flank shade R", fill=NONE,
       stroke="#5E3A18", strokeWidth=10, opacity=35, cap="round")

# forearms folded at the chest — the sentinel's hands
d.path("M492,516 C478,540 474,568 480,590 C486,598 498,598 502,588 "
       "C504,562 506,538 508,520 C504,510 496,508 492,516 Z",
       "Forearm L", fill="#7A4E24", stroke=INK, strokeWidth=4)
d.path("M548,516 C562,540 566,568 560,590 C554,598 542,598 538,588 "
       "C536,562 534,538 532,520 C536,510 544,508 548,516 Z",
       "Forearm R", fill="#7A4E24", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Paw L", x=492, y=586, width=20, height=15, fill=DARK, stroke=NONE)
d.shape("ellipse", "Paw R", x=528, y=586, width=20, height=15, fill=DARK, stroke=NONE)

# splayed hind feet at the base
d.path("M456,700 C438,704 426,714 428,724 C442,730 464,730 474,722 "
       "C478,712 470,700 456,700 Z", "Foot L", fill="#8A5E2C",
       stroke=INK, strokeWidth=4)
d.path("M584,700 C602,704 614,714 612,724 C598,730 576,730 566,722 "
       "C562,712 570,700 584,700 Z", "Foot R", fill="#8A5E2C",
       stroke=INK, strokeWidth=4)
for k in range(3):
    d.path(f"M{434 + k*12},{720} L{440 + k*12},{716}", f"Toe L{k+1}",
           fill=NONE, stroke=DARK, strokeWidth=2.5, opacity=70, cap="round")
    d.path(f"M{606 - k*12},{720} L{600 - k*12},{716}", f"Toe R{k+1}",
           fill=NONE, stroke=DARK, strokeWidth=2.5, opacity=70, cap="round")

# --- head: mongoose skull narrowing to the muzzle, dark bandit mask ---------------
d.path("M520,372 C552,372 572,392 574,418 C576,442 566,462 548,472 "
       "C540,484 532,490 520,490 C508,490 500,484 492,472 "
       "C474,462 464,442 466,418 C468,392 488,372 520,372 Z",
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
# pale brow band above the mask
d.path("M482,400 C500,391 540,391 558,400 C560,406 556,410 549,410 "
       "C534,405 506,405 491,410 C484,410 480,406 482,400 Z",
       "Brow band", fill=PALE, opacity=58, stroke=NONE)
# ears: small dark crescents seated low inside the skull line
d.path("M464,392 C452,386 442,392 440,402 C438,412 446,420 456,418 "
       "C464,412 466,402 464,392 Z", "Ear L", fill=DARK, stroke=INK, strokeWidth=3)
d.path("M576,392 C588,386 598,392 600,402 C602,412 594,420 584,418 "
       "C576,412 574,402 576,392 Z", "Ear R", fill=DARK, stroke=INK, strokeWidth=3)
# the signature: large dark teardrop patches angled from brow to cheek
d.path("M498,402 C482,394 466,402 464,418 C462,436 474,450 490,448 "
       "C504,444 510,424 506,410 C504,404 502,402 498,402 Z",
       "Eye patch L", fill=DARK, opacity=95, stroke=NONE)
d.path("M542,402 C558,394 574,402 576,418 C578,436 566,450 550,448 "
       "C536,444 530,424 534,410 C536,404 538,402 542,402 Z",
       "Eye patch R", fill=DARK, opacity=95, stroke=NONE)
# eyes inside the patches, warm amber glints
d.shape("ellipse", "Eye L", x=479, y=418, width=14, height=15,
        fill=rad((0, "#8A5C22"), (0.6, "#4A2E10"), (1, "#1E1206")),
        stroke=INK, strokeWidth=2)
d.shape("ellipse", "Eye R", x=547, y=418, width=14, height=15,
        fill=rad((0, "#8A5C22"), (0.6, "#4A2E10"), (1, "#1E1206")),
        stroke=INK, strokeWidth=2)
d.shape("ellipse", "Glint L", x=483, y=421, width=4, height=4,
        fill="#FFF6DC", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=551, y=421, width=4, height=4,
        fill="#FFF6DC", opacity=85, stroke=NONE)
# muzzle: pale wedge, dark nose, quiet mouth
d.shape("ellipse", "Muzzle", x=500, y=446, width=40, height=26,
        fill="#F4E4C0", opacity=90, stroke=NONE)
d.path("M512,444 C518,440 524,440 529,444 C532,450 527,456 520,456 "
       "C513,456 509,450 512,444 Z", "Nose", fill=DARK, stroke=NONE)
d.path("M512,462 C516,466 524,466 528,462", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
# crown grizzle flecks
for i, (x, y) in enumerate([(490, 380), (520, 374), (552, 382)]):
    d.shape("ellipse", f"Crown fleck {i+1}", x=x, y=y, width=12, height=6,
            fill="#8A5E2C", opacity=50, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#241708", strokeWidth=6)

# --- name -------------------------------------------------------------------------
d.text("MEERKAT", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#F4E2B8", justify="center")

d.finish("meerkat-V1R00")
