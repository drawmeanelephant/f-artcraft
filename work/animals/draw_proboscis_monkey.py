#!/usr/bin/env python3
"""Proboscis monkey — field-guide plate V1R00. The nose is the portrait:
head and shoulders in half-profile to the viewer's left so the long
pendulous nose reads, cream collar, rusty-orange coat against grey arms,
pot belly cropped by the disc. Warm swamp plate: hazy sun, mangrove line,
still water; everything near the lower edge closes on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Proboscis Monkey — Field Plate", 1000, 1000)

INK = "#2A170C"
SUN = "#FFE0A0"                    # hazy sun, upper right
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(deg):
    t = math.radians(deg)
    return CX + R*math.cos(t), CY + R*math.sin(t)

def P(deg):
    x, y = on_disc(deg)
    return f"{x:.1f},{y:.1f}"

ARC = f"A{R},{R} 0 0 1"

BG_GRAD = lin(0, 0, 0, 1000, (0, "#2C2412"), (1, "#0C0904"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#E8C98A"), (0.55, "#C49A58"), (1, "#7A5A2E"))
TREE_GRAD = lin(0, 420, 0, 620, (0, "#6A5A30"), (1, "#3E3418"))
WATER_GRAD = lin(0, 600, 0, 880, (0, "#D8B878"), (0.5, "#9C7C46"), (1, "#5A4422"))
COAT_GRAD = lin(0, 420, 0, 880, (0, "#E08A48"), (0.5, "#C0602A"), (1, "#7E3A16"))
BELLY_GRAD = rad((0, "#F4DEB0"), (0.7, "#DDB678"), (1, "#B48448"))
LIMB_GRAD = lin(0, 520, 0, 880, (0, "#BDB8AE"), (1, "#6E6A62"))
COLLAR_GRAD = lin(0, 420, 0, 560, (0, "#FBF2DC"), (1, "#D8C49C"))
HEAD_GRAD = rad((0, "#E8A060"), (0.7, "#C0682E"), (1, "#8A4218"))
SKIN_GRAD = rad((0, "#F2C8A6"), (1, "#C88E68"))
NOSE_GRAD = rad((0, "#F6B08A"), (0.6, "#DE845E"), (1, "#A8503A"))

# --- backdrop + swamp plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w, o) in enumerate([(70,100,5,35),(150,40,4,25),(40,400,5,30),(930,90,6,30),
                                  (955,380,4,25),(60,830,5,25),(935,840,5,25)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w, fill="#E8C98A", opacity=o, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A3618", strokeWidth=6)
# hazy sun, upper right
for k, (r, op) in enumerate([(120, 10), (90, 14), (64, 22), (42, 45)]):
    d.shape("ellipse", f"Sun haze {k+1}", x=680 - r, y=240 - r, width=2*r, height=2*r,
            fill=SUN, opacity=op, stroke=NONE)
for i, (x, y, w) in enumerate([(220,170,90),(250,262,130),(590,170,90)]):
    d.shape("ellipse", f"Haze cloud {i+1}", x=x, y=y, width=w*1.8, height=w*0.3, fill="#FFF4DA", opacity=16, stroke=NONE)
# mangrove treeline, closing on the disc arc
d.path(f"M{P(170)} C130,500 150,470 190,474 C210,440 250,430 280,452 C300,420 350,416 372,448 "
       f"C400,428 440,432 452,460 L560,460 C580,428 630,424 650,450 C672,420 720,420 740,446 "
       f"C770,430 812,436 828,466 C860,462 890,490 {P(10)} {ARC} {P(170)} Z",
       "Mangrove line", fill=TREE_GRAD, opacity=70, stroke=NONE)
for i, x in enumerate([190, 260, 330, 690, 760, 830]):
    d.path(f"M{x},{480} L{x},{560}", f"Trunk {i+1}", fill=NONE, stroke="#3A2E14", strokeWidth=5, opacity=50, cap="round")
    d.path(f"M{x - 24},{602} C{x - 24},{572} {x - 8},{558} {x},{558} C{x + 8},{558} {x + 24},{572} {x + 24},{602}",
           f"Prop roots {i+1}", fill=NONE, stroke="#3A2E14", strokeWidth=4, opacity=45, cap="round")
# still water, closing on the arc
d.path(f"M{P(160)} L{on_disc(20)[0]:.1f},{on_disc(160)[1]:.1f} {ARC} {P(160)} Z",
       "Water", fill=WATER_GRAD, stroke=NONE)
d.path(f"M{on_disc(160)[0] + 6:.1f},{on_disc(160)[1] + 2:.1f} L{on_disc(20)[0] - 6:.1f},{on_disc(20)[1] + 2:.1f}",
       "Waterline glint", fill=NONE, stroke="#FFF0C8", strokeWidth=3, opacity=55, cap="round")
for i, (x0, y, ln) in enumerate([(150,640,90),(700,630,120),(760,676,80),(180,700,70),(660,720,110),
                                 (620,780,90),(230,760,60),(600,830,60)]):
    hw = math.sqrt(R*R - (y - CY)**2) - 24
    x0, x1 = max(x0, CX - hw), min(x0 + ln, CX + hw)
    d.path(f"M{x0:.1f},{y} L{x1:.1f},{y}", f"Ripple {i+1}", fill=NONE, stroke="#FFE8B0",
           strokeWidth=3, opacity=35, cap="round")
d.shape("ellipse", "Sun reflection", x=690, y=620, width=60, height=180, fill=SUN, opacity=14, stroke=NONE)
# reeds on the right, rooted inside the disc
for i, (x, top, lean) in enumerate([(800, 520, 18), (820, 560, -10), (838, 600, 14), (770, 600, -16)]):
    base = CY + math.sqrt(R*R - (x - CX)**2) - 30
    d.path(f"M{x},{base:.1f} C{x + lean*0.3:.1f},{(base + top)/2:.1f} {x + lean:.1f},{top + 40} {x + lean:.1f},{top}",
           f"Reed {i+1}", fill=NONE, stroke=lin(0, top, 0, base, (0, "#8A7A3A"), (1, "#4A3E1C")),
           strokeWidth=5, cap="round")

# --- body: rusty shoulders, closing on the disc arc -------------------------------------------
d.path(f"M{P(132)} C236,650 296,560 380,516 C444,484 520,436 604,436 "
       f"C704,436 772,560 {P(48)} {ARC} {P(132)} Z", "Shoulders", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
d.path("M620,446 C690,452 744,520 764,610", "Shoulder sun rim", fill=NONE, stroke=SUN,
       strokeWidth=7, opacity=55, cap="round")
for i, dd in enumerate(["M660,520 C690,560 706,610 712,660", "M700,500 C730,540 748,590 754,640",
                        "M630,600 C650,640 660,690 662,740"]):
    d.path(dd, f"Coat fur {i+1}", fill=NONE, stroke="#7A3614", strokeWidth=4, opacity=40, cap="round")
# far arm (grey) hanging behind the belly, closing on the arc
d.path(f"M{P(140)} C216,690 250,620 310,600 C350,612 356,700 {P(118)} {ARC} {P(140)} Z",
       "Far arm", fill=LIMB_GRAD, stroke=INK, strokeWidth=6)
d.path("M266,660 C254,700 250,740 254,790", "Far arm shade", fill=NONE, stroke="#4E4A44",
       strokeWidth=8, opacity=30, cap="round")
# pot belly, cropped by the disc
d.path(f"M{P(118)} C300,700 330,616 412,602 C482,590 540,630 556,690 "
       f"C570,750 572,810 {P(80)} {ARC} {P(118)} Z", "Belly", fill=BELLY_GRAD, stroke=INK, strokeWidth=6)
d.path("M330,700 C346,650 380,620 420,614", "Belly light", fill=NONE, stroke="#FFF4DA",
       strokeWidth=8, opacity=40, cap="round")
d.path("M540,660 C556,720 562,790 560,850", "Belly shade", fill=NONE, stroke="#9A6A34",
       strokeWidth=12, opacity=30, cap="round")
for i, dd in enumerate(["M380,710 C400,728 420,736 444,740", "M350,790 C370,806 392,816 416,820"]):
    d.path(dd, f"Belly fur {i+1}", fill=NONE, stroke="#B08048", strokeWidth=4, opacity=40, cap="round")
# near arm (grey): down the side, forearm forward, hand resting on the belly
def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])
arm = [cubic((630,500), (672,580), (690,690), (640,752), i/20) for i in range(21)]
arm += [cubic((640,752), (604,794), (548,800), (500,790), i/14) for i in range(1, 15)]
Lp, Rp, n = [], [], len(arm)
for i, (x, y) in enumerate(arm):
    ax, ay = arm[max(i - 1, 0)]; bx, by = arm[min(i + 1, n - 1)]
    ln = math.hypot(bx - ax, by - ay) or 1
    nx, ny = -(by - ay)/ln, (bx - ax)/ln
    w = (76 - 30*i/(n - 1)) / 2
    Lp.append((x + nx*w, y + ny*w)); Rp.append((x - nx*w, y - ny*w))
dd = "M%.1f,%.1f " % Lp[0] + " ".join("L%.1f,%.1f" % p for p in Lp[1:])
dd += " A23,23 0 0 0 %.1f,%.1f " % Rp[-1] + " ".join("L%.1f,%.1f" % p for p in reversed(Rp[:-1])) + " Z"
d.path(dd, "Near arm", fill=LIMB_GRAD, stroke=INK, strokeWidth=6)
d.path("M" + " L".join("%.1f,%.1f" % ((a[0] + b[0])/2 + (b[0] - a[0])*0.25, (a[1] + b[1])/2 + (b[1] - a[1])*0.25)
                       for a, b in list(zip(Rp, Lp))[3:18]), "Near arm sun rim", fill=NONE, stroke=SUN,
       strokeWidth=5, opacity=50, cap="round")
d.path("M650,560 C664,620 664,680 640,730", "Near arm shade", fill=NONE, stroke="#4E4A44",
       strokeWidth=10, opacity=22, cap="round")
d.shape("ellipse", "Elbow light", x=652, y=690, width=30, height=40, fill="#FFFFFF", opacity=12, stroke=NONE)
d.path("M496,770 C478,770 462,780 460,794 C458,808 476,816 496,812 Z", "Hand",
       fill=lin(0, 768, 0, 816, (0, "#9A968E"), (1, "#5E5A54")), stroke=INK, strokeWidth=5)
for k, y in enumerate([780, 792, 804]):
    d.path(f"M476,{y} C468,{y + 1} 462,{y + 3} 458,{y + 6}", f"Finger {k+1}", fill=NONE,
           stroke=INK, strokeWidth=3, opacity=70, cap="round")

# --- cream collar ------------------------------------------------------------------------------
d.path("M420,470 C424,516 440,546 476,558 C544,570 610,548 640,500 "
       "C656,474 652,444 636,424 C600,470 540,492 480,494 C456,492 436,484 420,470 Z",
       "Collar", fill=COLLAR_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M450,520 C460,532 470,540 484,544", "M510,540 C536,544 562,538 586,526",
                        "M600,500 C612,490 622,478 628,466"]):
    d.path(dd, f"Collar fur {i+1}", fill=NONE, stroke="#B8A47A", strokeWidth=4, opacity=50, cap="round")

# --- head: half-profile to the viewer's left ----------------------------------------------------
d.shape("ellipse", "Ear", x=574, y=318, width=40, height=50, fill=lin(574, 0, 614, 0, (0, "#C88A68"), (1, "#8A5236")),
        stroke=INK, strokeWidth=5)
HEAD = ("M520,212 C604,212 652,272 650,342 C648,410 610,470 540,488 "
        "C490,500 430,490 402,446 C376,404 370,334 382,292 C402,238 452,212 520,212 Z")
d.path(HEAD, "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
d.path("M560,222 C610,236 644,280 648,334", "Head sun rim", fill=NONE, stroke=SUN,
       strokeWidth=7, opacity=60, cap="round")
for i, dd in enumerate(["M470,224 C490,214 512,210 534,212", "M430,240 C446,226 462,218 480,214",
                        "M556,220 C576,226 594,236 606,248", "M600,300 C612,320 618,344 618,368",
                        "M560,430 C580,420 598,404 610,386"]):
    d.path(dd, f"Crown fur {i+1}", fill=NONE, stroke="#7E3A16", strokeWidth=4, opacity=55, cap="round")
d.shape("ellipse", "Ear inner", x=584, y=330, width=18, height=26, fill="#6E3A22", opacity=50, stroke=NONE)
# bare face, pinkish-tan
d.path("M446,286 C492,280 520,310 522,352 C524,410 506,470 470,488 "
       "C430,500 396,470 388,420 C380,350 404,292 446,286 Z", "Face", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
d.path("M400,318 C420,300 460,292 500,304", "Brow ridge", fill=NONE, stroke="#9A5A38", strokeWidth=8,
       opacity=45, cap="round")
d.shape("ellipse", "Eye near", x=468, y=326, width=20, height=15, fill=rad((0, "#8A5A2A"), (1, "#2A160A")),
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye far", x=410, y=332, width=13, height=12, fill=rad((0, "#8A5A2A"), (1, "#2A160A")),
        stroke=INK, strokeWidth=3)
d.shape("ellipse", "Glint near", x=473, y=329, width=6, height=6, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint far", x=413, y=334, width=4, height=4, fill="#FFFFFF", opacity=80, stroke=NONE)
d.path("M468,348 C476,354 488,354 494,348", "Under-eye", fill=NONE, stroke="#A86A48", strokeWidth=3,
       opacity=60, cap="round")
# mouth + chin, tucked under the nose
d.path("M462,466 C476,474 494,472 506,462", "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M462,484 C476,492 492,490 504,480", "Chin", fill=NONE, stroke="#A86A48", strokeWidth=4,
       opacity=60, cap="round")

# --- THE nose -------------------------------------------------------------------------------------
NOSE = ("M448,340 C432,346 420,368 414,396 C406,428 386,452 378,486 "
        "C370,520 388,546 418,548 C450,550 466,526 464,496 C462,466 466,436 468,404 "
        "C470,374 464,346 448,340 Z")
d.path(NOSE, "Nose", fill=NOSE_GRAD, stroke=INK, strokeWidth=6)
d.path("M440,360 C430,390 420,420 400,460", "Nose ridge light", fill=NONE, stroke="#FFE0C8",
       strokeWidth=6, opacity=55, cap="round")
d.path("M458,430 C458,466 456,500 446,530", "Nose shade", fill=NONE, stroke="#8A3E2A",
       strokeWidth=8, opacity=35, cap="round")
d.shape("ellipse", "Nose tip glint", x=390, y=490, width=20, height=12, fill="#FFFFFF", opacity=35, stroke=NONE)
d.shape("ellipse", "Nostril", x=386, y=528, width=22, height=10, fill="#4A1E12", opacity=75, stroke=NONE)
d.path("M392,544 C410,550 434,548 450,536", "Nose underside", fill=NONE, stroke="#7A3424",
       strokeWidth=4, opacity=55, cap="round")

# --- name -----------------------------------------------------------------------------------------
d.text("PROBOSCIS MONKEY", "Name", x=500, y=960, size=46, font="Virelai Sans",
       color="#F2DDB0", justify="center")

d.finish("proboscis-monkey-V1R00")
