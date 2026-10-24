#!/usr/bin/env python3
"""Ocelot — field-guide plate V1R00. A leopard in miniature, painted in commas.
Understory plate, night-prowl mood: moonlight straining through canopy onto a
slim tawny head, big amber eyes, comma-spots chaining down the cheeks and
shoulders, the paired black cheek stripes that name the species. Leaf-litter
floor closes on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Ocelot — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#1C1208"                    # warm dark ink, never pure black
SPOT = "#201204"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

def mirror(dd):
    out, toks, ex = [], re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd), True
    for t in toks:
        if t.isalpha():
            out.append(t); ex = True
        elif ex:
            out.append(f"{1000 - float(t):g},"); ex = False
        else:
            out[-1] += f"{float(t):g}"; ex = True
    return " ".join(out)

def pair(dd, label, **kw):
    d.path(dd, f"{label} L", **kw)
    d.path(mirror(dd), f"{label} R", **kw)

def comma(p0, p1, p2, w0, w1, label, fill=SPOT, samples=14, **kw):
    """A comma spot: tapered filled stroke along a quadratic — the ocelot's
    elongated open spot, chained in rows across the coat."""
    Lp, Rp = [], []
    for i in range(samples + 1):
        t = i / samples
        x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0]
        y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1]
        dx = 2*(1-t)*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0])
        dy = 2*(1-t)*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1])
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0)*t) / 2
        Lp.append((x + nx*w, y + ny*w)); Rp.append((x - nx*w, y - ny*w))
    dd = "M%.1f,%.1f " % Lp[0] + " ".join("L%.1f,%.1f" % p for p in Lp[1:])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rp)) + " Z"
    d.path(dd, label, fill=fill, **kw)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0A1410"), (1, "#030705"))
PLATE_GRAD = rad((0, "#567664"), (0.52, "#2C4A3C"), (1, "#0C1C16"))
COAT_GRAD = rad((0, "#E4B264"), (0.55, "#BC8238"), (1, "#6E4014"))
PALE_GRAD = rad((0, "#F4E8CA"), (1, "#D2B484"))
MUZZLE_GRAD = rad((0, "#EDD9AE"), (1, "#B8925A"))

# --- backdrop + understory plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0A1810", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C2D4AE", strokeWidth=3, opacity=30)

# moonlight in a canopy gap, upper-left of the disc
d.shape("ellipse", "Canopy gap glow", x=278, y=128, width=244, height=170,
        fill="#DCEAD2", opacity=13, stroke=NONE)
d.shape("ellipse", "Moon core", x=336, y=154, width=140, height=110,
        fill="#F0F4DE", opacity=16, stroke=NONE)
# leaf edge cutting across the gap so the light reads as canopy-filtered
d.path("M300,300 q40,-26 92,-18 q-30,26 -92,18 Z", "Gap leaf",
       fill="#0E241A", opacity=75, stroke=NONE)

# canopy leaves hanging into the disc from the top rim — pointed silhouettes
for i, (x, y, a, s) in enumerate([(238,158,-32,1.0),(268,128,-8,0.8),(212,196,-52,0.85),
                                  (742,158,32,1.0),(712,128,8,0.8),(788,196,52,0.85),
                                  (168,276,-70,0.75),(832,276,70,0.75)]):
    t = math.radians(a); c, s_ = math.cos(t), math.sin(t)
    L, W = 95*s, 30*s
    d.path(f"M{x},{y} q{L*0.4*c - W*0.5*s_:.0f},{L*0.4*s_ + W*0.5*c:.0f} {L*c:.0f},{L*s_:.0f} "
           f"q{-L*0.55*c - W*0.5*s_:.0f},{-L*0.55*s_ + W*0.5*c:.0f} {-L*c:.0f},{-L*s_:.0f} Z",
           f"Canopy leaf {i+1}", fill="#0E241A", opacity=80, stroke=NONE)
# a few mid-veins
for i, (x, y, a) in enumerate([(238,158,-32),(742,158,32)]):
    t = math.radians(a)
    d.path(f"M{x},{y} L{x+88*math.cos(t):.0f},{y+88*math.sin(t):.0f}",
           f"Leaf vein {i+1}", fill=NONE, stroke="#1E3A2A", strokeWidth=3, opacity=60, cap="round")

# fireflies drifting in the understory murk
for i, (x, y, w) in enumerate([(252,388,7),(300,452,5),(762,332,6),(804,560,5),
                               (196,524,6),(728,450,5),(346,220,5),(660,238,6),
                               (420,150,4),(586,168,5)]):
    d.shape("ellipse", f"Firefly {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8D878", opacity=75, stroke=NONE)
    d.shape("ellipse", f"Firefly halo {i+1}", x=x-w*0.8, y=y-w*0.8, width=w*2.6, height=w*2.6,
            fill="#E8D878", opacity=18, stroke=NONE)

# --- leaf-litter floor, closing on the disc arc ------------------------------------
fy = 752
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C320,736 400,760 480,752 C560,744 660,740 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Litter floor",
       fill=lin(0, 740, 0, 880, (0, "#223626"), (0.6, "#12221A"), (1, "#081410")),
       stroke=NONE)
d.path(f"M{fl+10:.0f},{fy} C320,736 400,760 480,752 C560,744 660,740 {fr-10:.0f},{fy}",
       "Floor line", fill=NONE, stroke="#8EA87E", strokeWidth=4, opacity=40, cap="round")
# fallen leaves on the litter — pale undersides catching moonlight
for i, (x, y, a) in enumerate([(300,795,-20),(420,824,15),(560,806,-35),(500,844,-8)]):
    t = math.radians(a); c, s_ = math.cos(t), math.sin(t)
    d.path(f"M{x},{y} q{20*c - 5*s_:.0f},{20*s_ + 5*c:.0f} {38*c:.0f},{38*s_:.0f} "
           f"q{-16*c - 9*s_:.0f},{-16*s_ + 9*c:.0f} {-38*c:.0f},{-38*s_:.0f} Z",
           f"Fallen leaf {i+1}", fill="#3A4A30", opacity=60, stroke=NONE)

# --- chest and shoulders rising out of the litter -----------------------------------
d.path("M304,738 C304,648 344,578 412,548 L588,548 C656,578 696,648 696,738 "
       "C696,768 656,786 500,786 C344,786 304,768 304,738 Z",
       "Chest", fill=lin(0, 548, 0, 786, (0, "#B8823A"), (1, "#5C3410")),
       stroke=INK, strokeWidth=6)
# comma chains across the shoulders — rows slanting toward the spine
for i, (p0, p1, p2) in enumerate([
        ((360,608),(392,616),(424,610)), ((448,600),(478,596),(508,600)),
        ((368,660),(404,672),(438,668)), ((466,652),(498,650),(528,656)),
        ((352,712),(392,720),(428,714)), ((456,706),(490,702),(522,708)),
        ((580,608),(612,616),(640,610)), ((580,660),(616,672),(648,668)),
        ((586,712),(622,720),(656,714))]):
    comma(p0, p1, p2, 17, 5, f"Chest comma {i+1}", opacity=88)
# chest shadow under the jaw
d.path("M380,560 C420,600 580,600 620,560 C600,640 560,672 500,672 C440,672 400,640 380,560 Z",
       "Chest shade", fill="#6E4014", opacity=30, stroke=NONE)

# --- ears: rounded, dark-backed, seated wide on the skull corners ---------------------
EAR = ("M352,382 C322,366 312,326 328,296 C342,268 376,260 400,276 "
       "C424,290 430,326 418,354 C406,378 378,394 352,382 Z")
pair(EAR, "Ear", fill=rad((0, "#5C3410"), (1, "#241205")),
     stroke=INK, strokeWidth=5)
pair("M360,360 C344,346 342,322 354,306 C366,292 386,292 398,304 "
     "C410,316 408,338 396,350 C386,360 372,366 360,360 Z",
     "Inner ear", fill="#2A1808", opacity=85, stroke=NONE)
pair("M352,300 C344,318 344,340 352,358", "Ear rim light", fill=NONE,
     stroke="#E8C890", strokeWidth=4, opacity=35, cap="round")

# --- head: slim and gracile, smaller-cat proportions ----------------------------------
HEAD = ("M500,318 C584,318 650,364 670,442 C684,505 670,568 634,622 "
        "C604,662 552,686 500,686 C448,686 396,662 366,622 "
        "C330,568 316,505 330,442 C350,364 416,318 500,318 Z")
d.path(HEAD, "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Crown light", x=424, y=330, width=152, height=56,
        fill="#F0C868", opacity=22, stroke=NONE)
pair("M344,470 C336,520 344,566 366,604", "Cheek edge shade", fill=NONE,
     stroke="#6E4014", strokeWidth=14, opacity=32, cap="round")

# --- comma spots on the crown and temples, chained in rows -----------------------------
for i, (p0, p1, p2) in enumerate([
        ((410,352),(438,346),(466,350)), ((498,342),(524,342),(550,348)),
        ((560,352),(586,348),(612,356)),
        ((376,398),(404,392),(430,396)), ((470,384),(496,380),(522,384)),
        ((556,388),(584,384),(610,392)),
        ((352,452),(378,446),(402,452)), ((610,452),(634,446),(654,454))]):
    comma(p0, p1, p2, 13, 4, f"Crown comma {i+1}", opacity=85)
# small solid spots between brow and eyes
for i, (x, y) in enumerate([(456,432),(488,424),(520,424),(550,432),
                            (472,452),(528,452)]):
    d.shape("ellipse", f"Brow spot {i+1}", x=x - 4, y=y - 3,
            width=8, height=6, fill=SPOT, opacity=85, stroke=NONE)

# --- the ocelot signature: bold black cheek stripes + forehead bands -------------------
# two stripes each side, from the eye sweeping back and down across the cheek
pair("M444,496 C428,540 410,580 386,614", "Cheek stripe upper", fill=NONE,
     stroke="#140C04", strokeWidth=11, opacity=90, cap="round")
pair("M404,512 C388,548 372,584 352,612", "Cheek stripe lower", fill=NONE,
     stroke="#140C04", strokeWidth=9, opacity=85, cap="round")
# forehead bands converging between the ears
pair("M452,340 C456,372 458,400 456,428", "Forehead band outer", fill=NONE,
     stroke="#140C04", strokeWidth=8, opacity=80, cap="round")
pair("M480,336 C482,366 483,394 482,420", "Forehead band inner", fill=NONE,
     stroke="#140C04", strokeWidth=6, opacity=65, cap="round")
# white spectacles around the eyes + pale muzzle field
pair("M372,486 C378,522 404,548 440,560 C462,567 470,588 462,610 "
     "C450,640 410,650 382,632 C358,616 350,580 356,546 "
     "C360,522 364,502 372,486 Z",
     "Cheek pale", fill=PALE_GRAD, opacity=80, stroke=NONE)
d.path("M434,600 C444,640 464,668 500,672 C536,668 556,640 566,600 "
       "C572,646 556,682 500,686 C444,682 428,646 434,600 Z",
       "Throat pale", fill=PALE_GRAD, opacity=90, stroke=NONE)

# --- eyes: large, level, amber — the night-prowl stare ----------------------------------
pair("M390,478 C408,454 446,448 468,464 C464,492 432,504 404,496 "
     "C394,492 388,486 390,478 Z",
     "Eye", fill=rad((0, "#E8C85C"), (0.6, "#AC8226"), (1, "#5E4E12")),
     stroke=INK, strokeWidth=5)
pair("M408,466 C420,458 438,460 446,470 C448,486 440,498 424,496 "
     "C410,494 402,480 408,466 Z",
     "Pupil", fill="#120C06", stroke=NONE)
d.shape("ellipse", "Glint L", x=414, y=468, width=8, height=8,
        fill="#FFF4D8", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=578, y=468, width=8, height=8,
        fill="#FFF4D8", opacity=90, stroke=NONE)
# upper lid line + pale brow
pair("M384,458 C404,440 448,436 472,454", "Upper lid", fill=NONE,
     stroke=INK, strokeWidth=6, cap="round")
d.path("M488,436 C493,450 493,464 490,476 M512,436 C507,450 507,464 510,476",
       "Forehead furrow", fill=NONE, stroke="#8A5018", strokeWidth=5,
       opacity=55, cap="round")

# --- muzzle: pale pad, brick nose, heavy whisker dots -----------------------------------
d.path("M434,542 C444,518 472,506 500,506 C528,506 556,518 566,542 "
       "C576,572 566,606 542,624 C526,634 474,634 458,624 "
       "C434,606 424,572 434,542 Z",
       "Muzzle pad", fill=MUZZLE_GRAD, stroke=NONE)
for i, (x, y) in enumerate([(448,558),(442,576),(450,594),(464,568),
                            (460,586),(552,558),(558,576),(550,594),
                            (536,568),(540,586)]):
    d.shape("ellipse", f"Whisker pit {i+1}", x=x - 3, y=y - 2.5,
            width=6, height=5, fill=SPOT, opacity=60, stroke=NONE)
# nose: brick-pink, small-cat narrow
d.path("M472,522 C484,514 516,514 528,522 C534,538 530,554 518,562 "
       "C508,567 492,567 482,562 C470,554 466,538 472,522 Z",
       "Nose", fill=lin(472,514,528,568,(0,"#A85A40"),(1,"#5C2818")),
       stroke=INK, strokeWidth=4)
pair("M482,548 C478,541 482,534 489,532 C495,534 497,541 493,547 "
     "C489,551 484,551 482,548 Z",
     "Nostril", fill="#2E1008", stroke=NONE)
d.path("M500,566 L500,580", "Philtrum", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M500,580 C476,587 452,587 436,582 M500,580 C524,587 548,587 564,582",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# whiskers — long, pale, drooping into the dark
for i, (x1, y1, x2, y2) in enumerate([(440,560,318,536),(438,580,308,580),(442,596,326,616),
                                      (560,560,682,536),(562,580,692,580),(558,596,674,616)]):
    d.path(f"M{x1},{y1} Q{(x1+x2)/2},{min(y1,y2)-8} {x2},{y2}", f"Whisker {i+1}",
           fill=NONE, stroke="#E8D8B8", strokeWidth=2.5, opacity=58, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#081410", strokeWidth=6)

# --- name -----------------------------------------------------------------------------
d.text("OCELOT", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#D4E2C4", justify="center")

d.finish("ocelot-V1R00")
