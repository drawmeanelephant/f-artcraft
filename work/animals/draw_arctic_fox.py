#!/usr/bin/env python3
"""Arctic fox — field-guide plate V1R00. A white comma against the snow: the
fox curled nose-to-tail on a tundra night, tail wrapped over its paws, muzzle
tucked; summer-brown guard hair dusting the back and the dark undercoat
showing where the curl meets the drift. Aurora overhead, a lemming's dotted
trail crossing the snowfield that closes on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Arctic Fox — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#1E2632"                    # cold dark ink, never pure black

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

def ribbon(p0, p1, p2, w0, w1, label, fill, samples=18, **kw):
    """Tapered filled stroke along a quadratic — aurora curtains, the tail."""
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

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0C1220"), (1, "#04060C"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#17243F"), (0.45, "#33486E"),
                 (0.72, "#7C92AE"), (1, "#C9D6E2"))
FUR_GRAD = rad((0, "#FFFFFF"), (0.6, "#EDF2F6"), (1, "#C2D0DC"))
TAIL_GRAD = lin(0, 600, 0, 780, (0, "#F4F8FA"), (0.7, "#D8E2EA"), (1, "#AEC0CE"))
BROWN_GRAD = lin(0, 470, 0, 780, (0, "#7A5E40"), (1, "#4A3826"))
SNOW_GRAD = lin(0, 690, 0, 880, (0, "#F2F6F8"), (0.55, "#D8E2EA"), (1, "#A4B6C4"))

# --- backdrop + tundra-night plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#131F36", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D8E8", strokeWidth=3, opacity=35)

# stars scattered across the night half of the disc
for i, (x, y, w) in enumerate([(300,105,4),(705,112,5),(210,210,4),(790,235,4),
                               (385,150,3),(615,135,4),(255,320,4),(745,335,3),
                               (170,430,3),(830,430,4),(500,90,4),(430,240,3)]):
    d.shape("ellipse", f"Plate star {i+1}", x=x, y=y, width=w, height=w,
            fill="#E4ECF4", opacity=60, stroke=NONE)

# aurora curtains — translucent ribbons sagging across the upper disc
ribbon((268,150),(480,330),(742,140), 66, 34, "Aurora 1",
       lin(268,150,742,140,(0,"#6FE0A0"),(0.6,"#8FE8B4"),(1,"#5CC890")),
       opacity=30)
ribbon((310,120),(520,270),(730,170), 40, 20, "Aurora 2",
       lin(310,120,730,170,(0,"#9AECBE"),(1,"#66D09A")),
       opacity=22)
ribbon((350,200),(560,360),(720,250), 26, 12, "Aurora 3",
       lin(350,200,720,250,(0,"#C0F0D4"),(1,"#7CD8AA")),
       opacity=18)

# --- snowfield closing on the disc arc ---------------------------------------------
sy = 688
sl, sr = rim_x(sy, side=-1), rim_x(sy, side=1)
d.path(f"M{sl:.1f},{sy} C320,676 410,700 500,694 C590,688 690,682 {sr:.1f},{sy} "
       f"A{R},{R} 0 0 1 {sl:.1f},{sy} Z", "Snowfield",
       fill=SNOW_GRAD, stroke=NONE)
d.path(f"M{sl+10:.0f},{sy} C320,676 410,700 500,694 C590,688 690,682 {sr-10:.0f},{sy}",
       "Snow line", fill=NONE, stroke="#FFFFFF", strokeWidth=4, opacity=55, cap="round")
# drift contours
for i, (x, y, w) in enumerate([(280,798,120),(560,828,130),(420,858,100)]):
    d.path(f"M{x},{y} q{w/2},-{6+i*2} {w},0", f"Drift {i+1}", fill=NONE,
           stroke="#8EA2B2", strokeWidth=4, opacity=40, cap="round")
# a lemming's trail: fine paired dots hopping across the left snow
for i, (x, y, s) in enumerate([(205,742,1.0),(250,760,0.95),(295,776,0.9)]):
    for j, (ox, oy) in enumerate([(0,0),(10,-5),(21,1),(30,-4)]):
        d.shape("ellipse", f"Lemming {i+1}.{j+1}", x=x+ox*s, y=y+oy*s,
                width=7*s, height=4.5*s, fill="#4A5C6C", opacity=62, stroke=NONE)

# soft shadow pooling under the curl
d.shape("ellipse", "Fox shadow", x=330, y=730, width=360, height=70,
        fill="#5E7288", opacity=45, stroke=NONE)

# --- summer-brown undercoat: the dark side of the curl, laid before the white body ---
d.path("M368,706 C352,640 380,560 440,516 C390,580 392,660 424,716 C404,716 384,712 368,706 Z",
       "Undercoat L", fill=BROWN_GRAD, opacity=80, stroke=NONE)
d.path("M600,724 C640,706 660,660 652,610 C676,660 666,712 620,736 C612,732 604,728 600,724 Z",
       "Undercoat R", fill=BROWN_GRAD, opacity=70, stroke=NONE)

# --- the curled body: one white comma ----------------------------------------------
BODY = ("M352,700 C338,596 390,492 496,472 C594,454 668,516 670,608 "
        "C671,672 636,722 566,740 C488,760 396,748 352,700 Z")
d.path(BODY, "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=7)
# hollow of the curl in cool shadow
d.shape("ellipse", "Curl shadow", x=540, y=640, width=110, height=80,
        fill="#8CA2B4", opacity=25, stroke=NONE)
# back ridge highlight
d.path("M420,540 C460,498 540,486 600,514", "Back light", fill=NONE,
       stroke="#FFFFFF", strokeWidth=14, opacity=50, cap="round")
# guard hairs: the summer brown dusting the back curve
for i, (x1, y1, x2, y2) in enumerate([(430,516,426,496),(470,494,468,472),
                                      (512,486,514,464),(556,494,562,472),
                                      (596,510,606,490),(630,536,644,520)]):
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Guard hair {i+1}", fill=NONE,
           stroke="#6A5238", strokeWidth=4, opacity=45, cap="round")
# flank fur strokes, cool gray-blue
for i, (x1, y1, x2, y2) in enumerate([(400,600,386,634),(440,640,430,672),
                                      (600,620,612,652),(560,680,566,708)]):
    d.path(f"M{x1},{y1} Q{(x1+x2)/2+4},{(y1+y2)/2} {x2},{y2}", f"Flank fur {i+1}",
           fill=NONE, stroke="#A8BAC8", strokeWidth=5, opacity=45, cap="round")

# --- tail: the thick brush wrapped over the paws, tip tucked beside the nose ----------
ribbon((655,618),(600,745),(436,722), 96, 30, "Tail wrap", TAIL_GRAD,
       stroke=INK, strokeWidth=5)
# tail upper edge fur lines
d.path("M640,640 C590,720 500,742 448,722", "Tail fur 1", fill=NONE,
       stroke="#A8BAC8", strokeWidth=5, opacity=50, cap="round")
d.path("M615,662 C570,722 500,738 458,724", "Tail fur 2", fill=NONE,
       stroke="#A8BAC8", strokeWidth=4, opacity=40, cap="round")
# tail tip tucked close to the nose — the comma's point
d.path("M452,712 C440,722 436,736 446,744 C458,750 472,744 474,732 C474,720 464,710 452,712 Z",
       "Tail tip", fill="#F4F8FA", stroke=INK, strokeWidth=4)

# --- head: tucked, facing the viewer, muzzle down toward the tail tip ------------------
# ears: short round furry triangles on the head's top curve
d.path("M536,472 C528,444 540,420 564,414 C584,424 590,450 582,474 C566,462 550,462 536,472 Z",
       "Ear L", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.path("M540,462 C538,444 548,430 562,426 C572,434 576,448 572,462 C560,452 550,452 540,462 Z",
       "Ear inner L", fill=BROWN_GRAD, opacity=70, stroke=NONE)
d.path("M620,486 C622,456 642,438 666,440 C680,456 680,482 668,500 C652,486 636,482 620,486 Z",
       "Ear R", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.path("M630,478 C634,460 646,450 660,450 C668,460 668,476 660,486 C650,476 640,474 630,478 Z",
       "Ear inner R", fill=BROWN_GRAD, opacity=70, stroke=NONE)
# head wedge: crown between the ears, cheeks tapering to the tucked muzzle
HEAD = ("M522,514 C528,478 560,458 596,462 C634,466 660,490 662,524 "
        "C664,556 648,586 620,600 C600,610 574,610 556,598 "
        "C534,584 518,552 522,514 Z")
d.path(HEAD, "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=6)
# fur strokes over the head-to-body seam
d.path("M530,540 C516,570 514,600 524,624", "Neck seam fur", fill=NONE,
     stroke="#A8BAC8", strokeWidth=6, opacity=45, cap="round")
d.path("M652,560 C656,584 650,608 636,626", "Neck seam fur R", fill=NONE,
     stroke="#A8BAC8", strokeWidth=5, opacity=40, cap="round")
# cheek fur scallops (head centred near x=592 — mirrored by hand)
d.path("M540,556 C530,570 528,586 534,600", "Cheek fur L", fill=NONE,
     stroke="#A8BAC8", strokeWidth=5, opacity=45, cap="round")
d.path("M644,556 C654,570 656,586 650,600", "Cheek fur R", fill=NONE,
     stroke="#A8BAC8", strokeWidth=5, opacity=45, cap="round")
# muzzle taper + dark nose resting at the tail tip
d.path("M560,598 C572,612 596,614 612,602 C612,622 600,640 584,642 C568,640 558,620 560,598 Z",
       "Muzzle", fill="#EDF2F6", stroke=NONE)
d.path("M576,626 C584,620 596,622 600,630 C598,640 586,644 578,640 C572,636 572,630 576,626 Z",
       "Nose", fill="#141A22", stroke=NONE)
# eyes: dark almonds, calm and level — the lemming-year stare
d.path("M548,540 C556,528 574,526 586,534 C580,548 560,552 548,540 Z",
       "Eye L", fill="#141A22", stroke=NONE)
d.path("M636,540 C628,528 610,526 598,534 C604,548 624,552 636,540 Z",
       "Eye R", fill="#141A22", stroke=NONE)
d.shape("ellipse", "Glint L", x=560, y=532, width=5, height=5, fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=620, y=532, width=5, height=5, fill="#FFFFFF", opacity=85, stroke=NONE)
# brow shading
d.path("M544,524 C556,514 576,512 590,518", "Brow shade L", fill=NONE,
     stroke="#A8BAC8", strokeWidth=5, opacity=40, cap="round")
d.path("M640,524 C628,514 608,512 594,518", "Brow shade R", fill=NONE,
     stroke="#A8BAC8", strokeWidth=5, opacity=40, cap="round")
# two short whiskers over the tail
for i, (x1, y1, x2, y2) in enumerate([(566,606,500,622),(570,614,508,634)]):
    d.path(f"M{x1},{y1} Q{(x1+x2)/2},{min(y1,y2)-6} {x2},{y2}", f"Whisker {i+1}",
           fill=NONE, stroke="#DCE6EC", strokeWidth=2.5, opacity=60, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0F1A2E", strokeWidth=6)

# --- name -----------------------------------------------------------------------------
d.text("ARCTIC FOX", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#D2DEEA", justify="center")

d.finish("arctic-fox-V1R00")
