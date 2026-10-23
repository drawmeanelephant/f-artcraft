#!/usr/bin/env python3
"""Wombat — field-guide plate V1R00. Full body in three-quarter view facing
left, low to the ground: the rump a squared-off block, short thick legs,
broad blunt nose, heavy brows set in mild offence. Eucalyptus grey-green
plate with gum sprigs, a dusty bank with one burrow mouth behind.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Wombat — Field Plate", 1000, 1000)

INK = "#2A211B"
CX, CY, R = 500, 460, 420          # plate disc centre + radius
random.seed(62)

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rim(y):
    dx = math.sqrt(R*R - (y - CY)**2)
    return CX - dx, CX + dx

BG_GRAD = lin(0, 0, 0, 1000, (0, "#1C2620"), (1, "#080C0A"))
PLATE_GRAD = rad((0, "#E2EADB"), (0.65, "#B4C4AE"), (1, "#7C9279"))
GROUND = lin(0, 520, 0, 880, (0, "#CDB48E"), (0.45, "#B49872"), (1, "#8C7354"))
BURROW = rad((0, "#0E0905"), (0.7, "#261A10"), (1, "#4A3622"))
BODY = lin(0, 440, 0, 690, (0, "#9A8A74"), (0.5, "#766653"), (1, "#4A3E33"))
HEAD = rad((0, "#A49480"), (0.7, "#7E6E5A"), (1, "#56493C"))
RUMP = lin(730, 0, 790, 0, (0, "#8E7E69"), (1, "#5C4E40"))
LEG = lin(0, 600, 0, 710, (0, "#6A5A49"), (1, "#3A3028"))
LEG_FAR = lin(0, 600, 0, 710, (0, "#4E4237"), (1, "#2A221C"))
LEAF = lin(0, 140, 0, 330, (0, "#A9BFB3"), (1, "#6E8A7C"))
LEAF_DARK = lin(0, 140, 0, 330, (0, "#8DA79A"), (1, "#56705F"))

# --- backdrop + eucalyptus plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(110,150,4),(880,110,5),(50,500,4),(950,430,4),(120,880,4),(890,880,5),(30,740,3),(960,700,4)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w, fill="#DCE6D8", opacity=28, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E6250", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F2F6EE", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=600, y=200, width=220, height=130, fill="#9DB09A", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=170, y=330, width=200, height=120, fill="#9DB09A", opacity=20, stroke=NONE)
# far scrub line of gum trunks, faint
for i, (x, h, w) in enumerate([(220, 150, 12), (300, 190, 14), (610, 170, 12), (690, 210, 16), (770, 150, 10)]):
    d.path(f"M{x-w/2},{560} L{x-w/4},{560-h} L{x+w/4},{560-h} L{x+w/2},{560} Z", f"Far trunk {i+1}",
           fill=lin(0, 560 - h, 0, 560, (0, "#C8D3C2"), (1, "#9BAE98")), opacity=45, stroke=NONE)
    d.shape("ellipse", f"Far crown {i+1}", x=x-70, y=560-h-60, width=140, height=80,
            fill="#94A992", opacity=30, stroke=NONE)

# --- gum sprigs hanging into the plate (every point well inside the rim) ------------------------
def sickle(x, y, ln, ang, w, label, fill):
    t = math.radians(ang); ux, uy = math.cos(t), math.sin(t); nx, ny = -uy, ux
    tip = (x + ux*ln + nx*ln*0.18, y + uy*ln + ny*ln*0.18)
    a = (x + ux*ln*0.5 + nx*(w + ln*0.12), y + uy*ln*0.5 + ny*(w + ln*0.12))
    b = (x + ux*ln*0.5 - nx*(w - ln*0.08), y + uy*ln*0.5 - ny*(w - ln*0.08))
    d.path(f"M{x:.1f},{y:.1f} Q{a[0]:.1f},{a[1]:.1f} {tip[0]:.1f},{tip[1]:.1f} "
           f"Q{b[0]:.1f},{b[1]:.1f} {x:.1f},{y:.1f} Z", label, fill=fill, stroke="#3E5446", strokeWidth=3)
    d.path(f"M{x:.1f},{y:.1f} Q{(x + tip[0])/2 + nx*ln*0.06:.1f},{(y + tip[1])/2 + ny*ln*0.06:.1f} "
           f"{tip[0]:.1f},{tip[1]:.1f}", f"{label} midrib", fill=NONE, stroke="#E4EDE6",
           strokeWidth=3, opacity=40, cap="round")

def sprig(pts, leaves, tag):
    (x0, y0), (x1, y1), (x2, y2) = pts
    d.path(f"M{x0},{y0} Q{x1},{y1} {x2},{y2}", f"{tag} twig", fill=NONE,
           stroke=lin(x0, y0, x2, y2, (0, "#8A5A3E"), (1, "#B07A54")), strokeWidth=6, cap="round")
    for k, (t, ln, ang) in enumerate(leaves):
        x = (1-t)**2*x0 + 2*(1-t)*t*x1 + t*t*x2
        y = (1-t)**2*y0 + 2*(1-t)*t*y1 + t*t*y2
        sickle(x, y, ln, ang, 9, f"{tag} leaf {k+1}", LEAF if k % 2 else LEAF_DARK)
    # gumnuts
    for k, t in enumerate([0.55, 0.62]):
        x = (1-t)**2*x0 + 2*(1-t)*t*x1 + t*t*x2
        y = (1-t)**2*y0 + 2*(1-t)*t*y1 + t*t*y2
        d.shape("ellipse", f"{tag} gumnut {k+1}", x=x-8+k*12, y=y+6, width=14, height=16,
                fill=lin(0, y + 6, 0, y + 22, (0, "#9A8A6A"), (1, "#5E5238")), stroke="#3E3424", strokeWidth=3)

sprig([(240, 180), (330, 140), (440, 176)],
      [(0.12, 92, 100), (0.3, 104, 84), (0.48, 96, 72), (0.7, 88, 96), (0.88, 80, 64), (1.0, 70, 40)], "Sprig L")
sprig([(770, 210), (700, 172), (612, 196)],
      [(0.15, 86, 80), (0.38, 96, 104), (0.62, 84, 88), (0.85, 74, 120), (1.0, 64, 140)], "Sprig R")

# --- dusty bank with the burrow, closing on the disc arc ----------------------------------------
gyl, gyr = 612, 490
xl, _ = rim(gyl); _, xr = rim(gyr)
d.path(f"M{xl:.1f},{gyl} C260,604 420,600 560,598 C620,596 660,540 720,500 "
       f"C760,474 820,462 860,466 C880,468 896,474 {xr:.1f},{gyr} "
       f"A{R},{R} 0 0 1 {xl:.1f},{gyl} Z", "Ground", fill=GROUND, stroke=NONE)
d.path("M190,610 C260,604 420,600 560,598 C620,596 660,540 720,500 C760,474 820,462 860,466",
       "Bank crest light", fill=NONE, stroke="#EADCC2", strokeWidth=4, opacity=60, cap="round")
# grass tufts on the bank top
for i, (x, y) in enumerate([(744, 486), (870, 470), (660, 548)]):
    for k, dx in enumerate([-12, -6, 0, 6, 12]):
        d.path(f"M{x},{y} Q{x+dx*0.5},{y-14} {x+dx},{y-24+abs(dx)}", f"Bank grass {i+1}-{k+1}",
               fill=NONE, stroke="#8C9A6A", strokeWidth=3, opacity=80, cap="round")
# burrow mouth: dark arch, packed rim, spoil fan spilling forward
d.path("M776,548 C776,506 802,486 832,486 C862,486 888,506 888,548 C866,556 798,556 776,548 Z",
       "Burrow rim", fill=lin(0, 540, 0, 610, (0, "#A88A64"), (1, "#7A6044")), stroke=NONE)
d.path("M788,546 C788,514 808,498 832,498 C856,498 876,514 876,546 C858,552 806,552 788,546 Z",
       "Burrow mouth", fill=BURROW, stroke="#3A2A1A", strokeWidth=3)
d.path("M796,528 C802,512 816,502 832,502", "Burrow lip light", fill=NONE, stroke="#D8C2A0",
       strokeWidth=3, opacity=45, cap="round")
d.path("M764,550 C786,572 850,578 884,560 C874,584 820,594 786,586 C772,580 764,566 764,550 Z",
       "Spoil fan", fill=lin(0, 606, 0, 650, (0, "#C2A47C"), (1, "#9C7E5A")), stroke=NONE)
for i, (x, y, w) in enumerate([(784,566,8),(806,576,6),(832,572,9),(856,566,7),(870,560,5),(820,584,5)]):
    d.shape("ellipse", f"Spoil clod {i+1}", x=x, y=y, width=w*1.3, height=w,
            fill=lin(0, y, 0, y + w, (0, "#B39570"), (1, "#7E6446")), stroke=NONE)
# ground shading, scuffs, pebbles
for i, (x, y, w, h) in enumerate([(220,690,180,16),(520,730,200,18),(300,790,200,14),(470,818,150,12)]):
    d.shape("ellipse", f"Ground shade {i+1}", x=x, y=y, width=w, height=h, fill="#7E6648", opacity=22, stroke=NONE)
for i, dd in enumerate(["M230,740 C280,734 330,736 380,744", "M600,760 C650,752 700,754 740,762",
                        "M340,826 C400,820 450,822 500,830"]):
    d.path(dd, f"Scuff {i+1}", fill=NONE, stroke="#8C7354", strokeWidth=3, opacity=40, cap="round")
for i, (x, y, w) in enumerate([(250,720,10),(680,710,9),(420,800,8),(620,800,10),(340,760,6)]):
    d.shape("ellipse", f"Pebble {i+1}", x=x, y=y, width=w*1.4, height=w,
            fill=lin(0, y, 0, y + w, (0, "#C8B494"), (1, "#7E6A50")), stroke=NONE)

# --- wombat -------------------------------------------------------------------------------------
d.shape("ellipse", "Wombat shadow", x=228, y=676, width=560, height=44, fill="#4A3826", opacity=34, stroke=NONE)

def foot(x, y, w, fill, tag, n=4):
    d.path(f"M{x-w/2},{y} C{x-w/2},{y-18} {x-w/4},{y-24} {x},{y-24} C{x+w/4},{y-24} {x+w/2},{y-18} {x+w/2},{y} Z",
           f"{tag} foot", fill=fill, stroke=INK, strokeWidth=3)
    for k in range(n):
        cx = x - w/2 + 6 + k*(w - 12)/(n - 1)
        d.path(f"M{cx:.1f},{y-4} Q{cx-3:.1f},{y+2} {cx-7:.1f},{y+4}", f"{tag} claw {k+1}",
               fill=NONE, stroke="#E8DCC6", strokeWidth=3, cap="round")

# far legs (behind)
d.path("M290,610 C286,640 284,668 288,690 L332,690 C334,666 334,636 330,612 Z", "Leg far front",
       fill=LEG_FAR, stroke=INK, strokeWidth=3)
foot(306, 694, 46, LEG_FAR, "Far front")
d.path("M626,620 C624,646 626,668 630,688 L670,688 C672,664 672,640 668,620 Z", "Leg far hind",
       fill=LEG_FAR, stroke=INK, strokeWidth=3)
foot(648, 692, 44, LEG_FAR, "Far hind")

# body: low barrel ending in a squared rump block
BODY_D = ("M392,486 C470,446 600,436 700,448 C740,454 762,470 768,500 "
          "C774,540 774,600 768,640 C764,666 748,678 724,680 "
          "C640,684 520,684 440,676 C400,672 372,640 368,600 C364,550 370,510 392,486 Z")
d.path(BODY_D, "Body", fill=BODY, stroke=INK, strokeWidth=6)
# rump facet: the flat back end turned slightly toward us
d.path("M716,452 C744,458 762,472 768,500 C774,540 774,600 768,640 C764,666 748,678 724,680 "
       "C732,640 736,560 728,500 C726,480 722,464 716,452 Z", "Rump facet", fill=RUMP, stroke=NONE)
d.path("M716,452 C722,464 726,480 728,500 C736,560 732,640 724,680", "Rump edge", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=25, cap="round")
d.path("M742,500 C748,540 748,600 742,640", "Rump light", fill=NONE, stroke="#C8BAA4",
       strokeWidth=5, opacity=30, cap="round")
# back light, belly shade, flank volume
d.path("M410,484 C480,454 600,446 700,456", "Back rim light", fill=NONE, stroke="#E6DCCB",
       strokeWidth=8, opacity=32, cap="round")
d.path("M430,662 C520,672 640,672 716,666", "Belly shade", fill=NONE, stroke="#2A211B",
       strokeWidth=18, opacity=26, cap="round")
d.path("M420,520 C500,486 600,478 690,486", "Flank light", fill=NONE, stroke="#D8CCB8",
       strokeWidth=26, opacity=10, cap="round")
d.path("M400,630 C480,650 600,654 700,646", "Lower flank shade", fill=NONE, stroke="#2A211B",
       strokeWidth=30, opacity=14, cap="round")
# coarse coat texture
for i in range(34):
    x, y = random.uniform(420, 712), random.uniform(476, 660)
    ln = random.uniform(10, 18)
    d.path(f"M{x:.0f},{y:.0f} q{-ln*0.3:.0f},{ln*0.5:.0f} {-ln*0.25:.0f},{ln:.0f}", f"Coat {i+1}",
           fill=NONE, stroke=random.choice(["#4A3E33", "#B8A890"]), strokeWidth=3,
           opacity=random.choice([28, 36, 44]), cap="round")

# near legs: short, thick
d.path("M664,616 C660,640 660,664 664,690 L716,690 C720,664 722,636 716,610 Z", "Leg near hind",
       fill=LEG, stroke=INK, strokeWidth=4)
d.path("M620,560 C660,540 712,556 724,600 C732,632 720,650 704,656 C680,640 640,608 620,560 Z",
       "Haunch", fill=BODY, stroke=NONE)
d.path("M704,656 C720,650 732,632 724,600", "Haunch edge", fill=NONE, stroke=INK, strokeWidth=3,
       opacity=45, cap="round")
foot(690, 694, 56, LEG, "Near hind")
d.path("M384,606 C380,636 380,664 384,692 L438,692 C442,664 444,634 438,604 Z", "Leg near front",
       fill=LEG, stroke=INK, strokeWidth=4)
foot(410, 696, 58, LEG, "Near front")

# --- head: broad, blunt, mildly offended ---------------------------------------------------------
# ears
d.path("M262,448 C252,424 260,404 276,400 C292,402 300,424 296,448 Z", "Ear far",
       fill=HEAD, stroke=INK, strokeWidth=4)
d.path("M372,446 C370,418 384,398 402,398 C418,402 420,428 408,452 Z", "Ear near",
       fill=HEAD, stroke=INK, strokeWidth=4)
d.path("M380,440 C380,422 390,410 400,410 C408,416 406,432 400,446 Z", "Ear near inner",
       fill="#4A3C30", opacity=60, stroke=NONE)
d.path("M270,444 C266,426 270,414 278,412 C286,416 288,430 286,446 Z", "Ear far inner",
       fill="#4A3C30", opacity=60, stroke=NONE)
d.path("M240,512 C238,466 280,436 336,434 C392,434 432,462 436,512 C440,560 428,600 404,626 "
       "C376,654 304,660 270,636 C242,616 242,560 240,512 Z", "Head", fill=HEAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Brow light", x=280, y=446, width=120, height=44, fill="#E2D6C2", opacity=18, stroke=NONE)
d.path("M408,620 C428,596 438,560 436,516", "Cheek shade", fill=NONE, stroke="#3A3028",
       strokeWidth=14, opacity=28, cap="round")
for i, dd in enumerate(["M410,480 q8,10 10,22", "M420,520 q6,10 6,22", "M252,500 q-4,10 -4,20",
                        "M300,452 q6,-4 14,-4", "M350,450 q8,0 14,4"]):
    d.path(dd, f"Head fur {i+1}", fill=NONE, stroke="#4A3E33", strokeWidth=3, opacity=40, cap="round")
# muzzle + broad blunt nose
d.path("M262,566 C264,546 290,536 320,536 C352,536 378,548 380,570 C382,598 356,616 320,616 "
       "C288,616 260,596 262,566 Z", "Muzzle", fill=lin(0, 536, 0, 616, (0, "#A89884"), (1, "#7A6A58")),
       stroke=NONE)
d.path("M272,560 C272,540 296,532 320,532 C346,532 370,540 370,560 C370,584 348,596 320,596 "
       "C292,596 272,584 272,560 Z", "Nose", fill=lin(0, 532, 0, 596, (0, "#4A3E36"), (1, "#16110D")),
       stroke=INK, strokeWidth=3)
for i, (x, y) in enumerate([(290,548),(304,544),(320,542),(336,544),(350,548),(296,562),(312,560),
                            (328,560),(344,562),(306,576),(322,578),(338,576)]):
    d.shape("ellipse", f"Nose grain {i+1}", x=x, y=y, width=4, height=4, fill="#6A5C52", opacity=50, stroke=NONE)
d.path("M286,546 C300,538 326,536 346,542", "Nose sheen", fill=NONE, stroke="#C8BEB4",
       strokeWidth=4, opacity=40, cap="round")
d.path("M294,574 C298,566 306,566 308,574 Z", "Nostril L", fill="#050302", stroke=NONE)
d.path("M334,574 C336,566 344,566 348,574 Z", "Nostril R", fill="#050302", stroke=NONE)
# mildly offended mouth: a short flat downturn
d.path("M298,606 C310,600 330,600 344,606", "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M320,596 L320,603", "Philtrum", fill=NONE, stroke=INK, strokeWidth=3, opacity=70, cap="round")
# small eyes under heavy, low-slung brows
for tag, (ex, ey, w) in [("far", (282, 506, 12)), ("near", (366, 506, 14))]:
    d.shape("ellipse", f"Eye socket {tag}", x=ex-4, y=ey-3, width=w+8, height=w+4, fill="#3A2E24", opacity=40, stroke=NONE)
    d.shape("ellipse", f"Eye {tag}", x=ex, y=ey, width=w, height=w - 1,
            fill=rad((0, "#3A2618"), (1, "#0A0604")), stroke=NONE)
    d.shape("ellipse", f"Eye glint {tag}", x=ex + w*0.55, y=ey + 2, width=4, height=4, fill="#F4F0E6", opacity=85, stroke=NONE)
# heavy lids pressing down toward the nose = offence
# half-lowered lids and a faint inward tilt: unimpressed rather than angry
d.path("M276,506 C280,503 288,503 296,509 L296,512 L276,511 Z", "Lid far", fill="#806F5C", stroke=NONE)
d.path("M362,505 C368,503 376,503 382,507 L382,512 L362,512 Z", "Lid near", fill="#806F5C", stroke=NONE)
d.path("M274,507 C282,504 290,505 298,510", "Lid line far", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M384,507 C376,504 368,505 360,510", "Lid line near", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M272,492 C282,490 292,492 300,496", "Brow far", fill=NONE, stroke="#3A2E24", strokeWidth=4, opacity=60, cap="round")
d.path("M388,490 C378,488 366,490 356,494", "Brow near", fill=NONE, stroke="#3A2E24", strokeWidth=4, opacity=60, cap="round")

# dust kicked up around the hind feet
for i, (x, y, w, h, op) in enumerate([(700,664,80,40,26),(740,640,60,34,18),(640,676,70,30,20),(212,676,60,26,16)]):
    d.shape("ellipse", f"Dust puff {i+1}", x=x, y=y, width=w, height=h, fill="#E6D6BA", opacity=op, stroke=NONE)
for i in range(18):
    x, y = random.uniform(680, 820), random.uniform(600, 690)
    w = random.choice([3, 4, 5])
    d.shape("ellipse", f"Dust mote {i+1}", x=x, y=y, width=w, height=w, fill="#D6C29E", opacity=70, stroke=NONE)

# --- name ---------------------------------------------------------------------------------------
d.text("WOMBAT", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#DCE6D6", justify="center")

d.finish("wombat-V1R00")
