#!/usr/bin/env python3
"""Wolverine — field-guide plate V1R00. Full body, side profile facing left,
mid-stride: compact, arched, low-slung. Dark chocolate coat, pale masked
brow band, frost-tipped 'glacier' stripe sweeping shoulder to tail, heavy
paws with pale claws. Cold light: icy plate, far peaks, a snow bank that
closes on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Wolverine — Field Plate", 1000, 1000)

INK = "#1A120E"
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def tr(dd, dx, dy):
    """Translate an absolute-coordinate path."""
    out, toks, ex = [], re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd), True
    for t in toks:
        if t.isalpha():
            out.append(t); ex = True
        elif ex:
            out.append(f"{float(t) + dx:g},"); ex = False
        else:
            out[-1] += f"{float(t) + dy:g}"; ex = True
    return " ".join(out)

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#13212F"), (1, "#05090E"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#8FAEC6"), (0.45, "#C9DCE8"), (1, "#EEF5F8"))
SNOW_GRAD = lin(0, 740, 0, 880, (0, "#F6FAFC"), (1, "#B8CCDA"))
COAT_GRAD = lin(0, 450, 0, 640, (0, "#5A3A28"), (0.55, "#3E2618"), (1, "#24160E"))
HEAD_GRAD = rad((0, "#5E3E2C"), (0.7, "#3E2818"), (1, "#22150D"))
LEG_GRAD = lin(0, 560, 0, 750, (0, "#3A2416"), (1, "#140C08"))
LEG_FAR_GRAD = lin(0, 560, 0, 750, (0, "#2A1A10"), (1, "#0C0705"))
TAIL_GRAD = lin(660, 470, 800, 600, (0, "#4A2E1E"), (1, "#1E120A"))
STRIPE_GRAD = lin(380, 0, 700, 0, (0, "#E9DCC2"), (0.6, "#C9AE88"), (1, "#A88A66"))
BROW_GRAD = lin(0, 500, 0, 540, (0, "#D8C4A2"), (1, "#A88C6A"))

# --- backdrop + icy plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(110,140,5),(890,120,4),(60,480,4),(940,420,5),(130,880,4),(880,860,5),(30,720,3),(960,700,4)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w, fill="#CFE2F2", opacity=35, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E6A82", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=55)
d.shape("ellipse", "Cold sun", x=640, y=150, width=120, height=120, fill="#FFFFFF", opacity=40, stroke=NONE)
d.shape("ellipse", "Cold sun halo", x=600, y=110, width=200, height=200, fill="#FFFFFF", opacity=16, stroke=NONE)

# far peaks (every vertex inside the disc)
d.path("M190,640 L270,520 L320,560 L410,430 L470,500 L520,460 L610,560 L680,500 L760,590 L810,640 Z",
       "Far peaks", fill=lin(0, 430, 0, 640, (0, "#9DB6C9"), (1, "#7E99AE")), opacity=60, stroke=NONE)
d.path("M410,430 L440,466 L428,470 L446,492 L470,500 M270,520 L290,548 L320,560 M680,500 L706,534 L730,556",
       "Peak snow lines", fill=NONE, stroke="#FFFFFF", strokeWidth=4, opacity=55, cap="round")
d.path("M180,700 L240,620 L330,670 L420,600 L520,680 L600,630 L700,690 L780,640 L820,700 Z",
       "Near ridge", fill=lin(0, 600, 0, 700, (0, "#B7CCDB"), (1, "#9AB2C4")), opacity=65, stroke=NONE)
# blowing snow
for i, (x, y, w) in enumerate([(200,300,6),(260,240,4),(330,330,5),(560,280,4),(760,360,6),(820,280,4),
                               (180,450,5),(860,480,4),(480,200,4),(380,160,5),(240,560,4),(800,560,5)]):
    d.shape("ellipse", f"Snowflake {i+1}", x=x, y=y, width=w, height=w, fill="#FFFFFF", opacity=70, stroke=NONE)

# snow bank: undulating top edge, bottom closes on the disc arc
gy = 744
gdx = math.sqrt(R*R - (gy - CY)**2)
d.path(f"M{CX-gdx:.1f},{gy} C300,728 420,738 520,734 C620,730 720,736 {CX+gdx:.1f},{gy} "
       f"A{R},{R} 0 0 1 {CX-gdx:.1f},{gy} Z", "Snow bank", fill=SNOW_GRAD, stroke=NONE)
d.path("M210,744 C300,730 420,740 520,736 C620,732 720,738 790,744", "Snow crest light",
       fill=NONE, stroke="#FFFFFF", strokeWidth=4, opacity=80, cap="round")
for i, (x, y, w, h) in enumerate([(250,790,120,10),(560,800,160,12),(400,836,140,10)]):
    d.shape("ellipse", f"Drift shade {i+1}", x=x, y=y, width=w, height=h, fill="#8EA8BC", opacity=30, stroke=NONE)
d.shape("ellipse", "Wolverine shadow", x=290, y=734, width=460, height=28, fill="#6E88A0", opacity=40, stroke=NONE)
# paw prints trailing behind
for i, (x, y) in enumerate([(650,778),(684,792),(640,806)]):
    d.shape("ellipse", f"Print {i+1}", x=x, y=y, width=22, height=10, fill="#8EA8BC", opacity=50, stroke=NONE)

# --- limbs -------------------------------------------------------------------------------
def limb(label, pts, widths, fill, **kw):
    n = len(pts)
    L, Rr = [], []
    for i in range(n):
        ax, ay = pts[max(i - 1, 0)]
        bx, by = pts[min(i + 1, n - 1)]
        dx, dy = bx - ax, by - ay
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = widths[i] / 2
        L.append((pts[i][0] + nx*w, pts[i][1] + ny*w))
        Rr.append((pts[i][0] - nx*w, pts[i][1] - ny*w))
    dd = "M%.1f,%.1f " % L[0]
    for i in range(1, n):          # smooth the outline with midpoint quads
        mx, my = (L[i-1][0] + L[i][0]) / 2, (L[i-1][1] + L[i][1]) / 2
        dd += "Q%.1f,%.1f %.1f,%.1f " % (L[i-1][0], L[i-1][1], mx, my) if i > 1 else "L%.1f,%.1f " % (mx, my)
    dd += "L%.1f,%.1f L%.1f,%.1f " % (L[-1] + Rr[-1])
    for i in range(n - 2, -1, -1):
        dd += "L%.1f,%.1f " % Rr[i]
    d.path(dd + "Z", label, fill=fill, **kw)

def paw(label, cx, fill, claws=True):
    d.path(f"M{cx+24},{746} C{cx+26},{732} {cx+10},{724} {cx-8},{725} "
           f"C{cx-26},{726} {cx-36},{736} {cx-34},{746} Z", label, fill=fill, stroke=INK, strokeWidth=3)
    if claws:
        for j, ox in enumerate([-30, -22, -14]):
            d.path(f"M{cx+ox},{742} Q{cx+ox-8},{744} {cx+ox-10},{750}", f"{label} claw {j+1}",
                   fill=NONE, stroke="#E8DCC8", strokeWidth=3, cap="round")

# far legs (behind the body)
limb("Leg far front", [(430,600),(440,650),(450,700),(458,736)], [54,42,34,32],
     LEG_FAR_GRAD, stroke=INK, strokeWidth=3)
paw("Paw far front", 460, LEG_FAR_GRAD)
limb("Leg far hind", [(600,590),(590,640),(574,690),(560,736)], [60,44,34,32],
     LEG_FAR_GRAD, stroke=INK, strokeWidth=3)
paw("Paw far hind", 558, LEG_FAR_GRAD)

# --- bushy tail (behind the rump) --------------------------------------------------------
d.path("M660,462 C716,460 768,494 792,546 C806,578 800,606 784,612 "
       "C770,618 760,596 748,580 C730,556 700,540 668,536 Z",
       "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M690,488 C730,500 760,526 778,560", "M686,510 C720,520 746,544 762,574",
                        "M776,580 L790,604 M764,586 L774,606"]):
    d.path(dd, f"Tail fur {i+1}", fill=NONE, stroke="#7A5A44", strokeWidth=3, opacity=45, cap="round")
d.path("M700,480 C740,486 774,512 790,544", "Tail rim light", fill=NONE,
       stroke="#D6E8F6", strokeWidth=4, opacity=40, cap="round")

# --- body: low, arched at the hips -------------------------------------------------------
d.path("M318,540 C350,500 420,476 500,460 C560,446 620,432 668,450 "
       "C706,466 724,510 714,556 C706,592 684,618 656,630 "
       "Q644,644 634,636 Q624,648 612,640 Q600,650 588,640 Q576,652 562,642 "
       "Q550,654 536,644 Q522,654 508,644 Q494,654 480,644 Q466,652 452,644 Q438,652 420,648 "
       "C384,652 346,640 328,612 C312,586 306,560 318,540 Z",
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# cold rim light along the back, belly shade
d.path("M344,516 C400,488 470,472 530,460 C590,448 640,440 676,456", "Back rim light",
       fill=NONE, stroke="#CFE4F4", strokeWidth=6, opacity=40, cap="round")
d.path("M420,628 C490,624 560,620 640,618", "Belly shade", fill=NONE,
       stroke="#0E0805", strokeWidth=16, opacity=30, cap="round")

# coat texture
for i, dd in enumerate(["M440,616 L436,630", "M500,620 L497,636", "M560,618 L558,634", "M610,614 L608,630",
                        "M450,590 C470,600 490,606 510,608", "M530,584 C552,594 574,598 596,598",
                        "M600,456 C620,458 640,464 656,474", "M450,486 C470,480 490,476 510,474"]):
    d.path(dd, f"Coat fur {i+1}", fill=NONE, stroke="#7A5440", strokeWidth=3, opacity=40, cap="round")

# --- near legs ------------------------------------------------------------------------------
limb("Leg near front", [(392,556),(390,580),(374,640),(362,692),(338,722),(322,736)], [70,70,52,40,36,34],
     LEG_GRAD, stroke=INK, strokeWidth=4)
paw("Paw near front", 318, LEG_GRAD)
limb("Leg near hind", [(648,530),(652,560),(672,610),(690,660),(708,700),(724,736)], [84,84,60,42,36,34],
     LEG_GRAD, stroke=INK, strokeWidth=4)
paw("Paw near hind", 726, LEG_GRAD)
# shoulder + haunch masses over the leg tops
d.path("M346,540 C390,520 440,540 440,590 C440,626 414,648 392,658 "
       "C368,632 348,594 346,540 Z", "Shoulder", fill=COAT_GRAD, stroke=NONE)
d.path("M598,478 C660,466 718,504 718,556 C718,598 700,626 678,642 "
       "C640,610 600,560 598,478 Z", "Haunch", fill=COAT_GRAD, stroke=NONE)
d.path("M392,658 C414,648 440,626 440,590", "Shoulder edge", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=55, cap="round")
d.path("M678,642 C700,626 718,598 718,556", "Haunch edge", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=55, cap="round")
d.path("M382,606 C372,646 362,680 340,712", "Front leg sheen", fill=NONE,
       stroke="#8A7468", strokeWidth=4, opacity=35, cap="round")
# glacier stripe: frost-tipped band, shoulder sweeping back over the hip to the tail
d.path("M366,556 C424,516 500,496 580,482 C632,474 676,478 704,498 "
       "C700,516 680,512 656,510 C596,510 528,524 466,548 C430,562 400,574 380,584 Z",
       "Glacier stripe", fill=STRIPE_GRAD, opacity=85, stroke=NONE)
d.path("M388,554 C446,522 516,504 584,494 C628,488 668,490 696,502", "Stripe frost",
       fill=NONE, stroke="#FFFFFF", strokeWidth=4, opacity=55, cap="round")
for i, (x, y) in enumerate([(420,560),(470,540),(520,526),(570,516),(620,510),(660,508)]):
    d.path(f"M{x},{y} Q{x-4},{y+8} {x-10},{y+14}", f"Frost tip {i+1}",
           fill=NONE, stroke="#FFF8EC", strokeWidth=3, opacity=35, cap="round")

# --- head: broad, low, masked -----------------------------------------------------------------
HX, HY = -6, 18
# small round ear with a pale rim
d.shape("ellipse", "Ear", x=322+HX, y=490+HY, width=32, height=26, fill=HEAD_GRAD, stroke=INK, strokeWidth=4)
d.path(tr("M326,500 C330,492 342,490 350,496", HX, HY), "Ear rim pale", fill=NONE,
       stroke="#D8C4A2", strokeWidth=4, opacity=75, cap="round")
d.shape("ellipse", "Ear inner", x=331+HX, y=498+HY, width=14, height=11, fill="#140C08", opacity=70, stroke=NONE)

d.path(tr("M352,516 C334,498 302,494 276,504 C254,512 238,530 228,546 C222,556 224,568 236,574 C254,584 272,598 298,604 C324,610 350,600 362,578 C372,556 368,530 352,516 Z", HX, HY),
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=6)
# pale brow band: ear to ear over the mask
d.path(tr("M350,520 C330,504 300,502 278,512 C268,516 262,522 258,528 C276,524 300,520 322,526 C334,530 344,536 352,540 Z", HX, HY),
       "Brow band", fill=BROW_GRAD, opacity=80, stroke=NONE)
# dark mask around the eye + muzzle
d.path(tr("M300,530 C282,524 262,530 248,542 C238,552 236,562 244,568 C262,570 284,566 302,556 C312,548 310,536 300,530 Z", HX, HY),
       "Mask", fill="#120A06", opacity=60, stroke=NONE)
d.path(tr("M232,544 C222,546 218,554 222,560 C228,566 238,562 240,554 Z", HX, HY),
       "Nose", fill=lin(0, 544, 0, 564, (0, "#3A2A22"), (1, "#050303")), stroke=NONE)
d.shape("ellipse", "Nose glint", x=226+HX, y=548+HY, width=5, height=3, fill="#FFFFFF", opacity=45, stroke=NONE)
# small hard eye
d.shape("ellipse", "Eye", x=270+HX, y=532+HY, width=14, height=12, fill="#2A1A10", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Eye glint", x=273+HX, y=534+HY, width=4, height=4, fill="#DDEBF6", opacity=90, stroke=NONE)
d.path(tr("M266,532 C272,526 282,526 288,532", HX, HY), "Brow ridge", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# snarl: lip line + one pale canine
d.path(tr("M236,574 C250,580 266,584 282,584", HX, HY), "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path(tr("M250,577 L254,590 L259,579 Z", HX, HY), "Canine", fill="#F2EADC", stroke=INK, strokeWidth=1.5)
d.path(tr("M298,584 C318,596 342,594 356,580", HX, HY), "Jaw shade", fill=NONE,
       stroke="#0E0805", strokeWidth=10, opacity=30, cap="round")
d.path(tr("M290,506 C312,500 336,504 350,516", HX, HY), "Crown rim light", fill=NONE,
       stroke="#CFE4F4", strokeWidth=4, opacity=45, cap="round")
# --- name -------------------------------------------------------------------------------------
d.text("WOLVERINE", "Name", x=500, y=962, size=56, font="Virelai Sans",
       color="#DCEAF4", justify="center")

d.finish("wolverine-V1R00")
