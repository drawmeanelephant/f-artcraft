#!/usr/bin/env python3
"""Snow leopard — field-guide plate V1R00. Face-forward, lying sphinx-style
on a snowy ledge: the pale stare up top, smoky rosettes over a silver-grey
coat, and the huge tail swept in front of the paws, its tip curling up.
Cool alpine plate with jagged peaks; the ledge closes on the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Snow Leopard — Field Plate", 1000, 1000)

INK = "#2A2C32"
SPOT = "#3C3D44"
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#1B2533"), (1, "#070B11"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#7F98AE"), (0.5, "#C2D2DE"), (1, "#E8EFF4"))
COAT_GRAD = rad((0, "#F2F0EC"), (0.65, "#D2CEC6"), (1, "#9E9990"))
BODY_GRAD = lin(0, 440, 0, 770, (0, "#DAD6CE"), (1, "#A6A198"))
TAIL_GRAD = lin(0, 660, 0, 840, (0, "#E4E0D8"), (1, "#A29D94"))
PALE_GRAD = rad((0, "#FFFFFF"), (1, "#E2E0DC"))
IRIS_GRAD = rad((0, "#E4EEDC"), (0.6, "#B8C8B4"), (1, "#7E9286"))
EAR_GRAD = lin(0, 250, 0, 330, (0, "#4A4A52"), (1, "#A8A39A"))
ROCK_GRAD = lin(0, 740, 0, 880, (0, "#7A8796"), (1, "#4A5664"))

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

def spot(x, y, w, h, label, op=75):
    d.shape("ellipse", label, x=x - w/2, y=y - h/2, width=w, height=h, fill=SPOT, opacity=op, stroke=NONE)

def rosette(cx, cy, r, label, rot=0, op=58):
    """Broken ring of smoky arcs around a slightly darker centre."""
    d.shape("ellipse", f"{label} centre", x=cx - r*0.8, y=cy - r*0.7, width=r*1.6, height=r*1.4,
            fill="#8E8A84", opacity=30, stroke=NONE)
    for k, (a0, a1, wf) in enumerate([(0, 70, 0.5), (95, 150, 0.38), (172, 262, 0.55), (288, 336, 0.34)]):
        t0, t1 = math.radians(a0 + rot), math.radians(a1 + rot)
        x0, y0 = cx + r*math.cos(t0), cy + r*0.85*math.sin(t0)
        x1, y1 = cx + r*math.cos(t1), cy + r*0.85*math.sin(t1)
        d.path(f"M{x0:.1f},{y0:.1f} A{r},{r*0.85:.1f} 0 0 1 {x1:.1f},{y1:.1f}", f"{label} blotch {k+1}",
               fill=NONE, stroke=SPOT, strokeWidth=max(3, r*wf), opacity=op, cap="round")

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

# --- backdrop + alpine plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(120,110,5),(880,140,4),(60,460,4),(940,400,5),(140,880,4),(870,870,5),(40,700,3),(955,680,4)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w, fill="#D4E2EE", opacity=35, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4C5E70", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=50)
d.shape("ellipse", "Cloud bank L", x=140, y=300, width=260, height=50, fill="#FFFFFF", opacity=22, stroke=NONE)
d.shape("ellipse", "Cloud bank R", x=620, y=250, width=240, height=44, fill="#FFFFFF", opacity=20, stroke=NONE)
# jagged peaks (every vertex inside the disc)
d.path("M150,600 L220,470 L260,510 L330,380 L380,450 L420,410 L470,470 L540,350 L600,440 "
       "L650,400 L720,500 L770,450 L850,600 Z",
       "Peaks", fill=lin(0, 350, 0, 600, (0, "#8A9FB2"), (1, "#6A8094")), opacity=70, stroke=NONE)
d.path("M330,380 L350,420 L338,428 L362,446 M540,350 L560,390 L546,396 L574,420 "
       "M770,450 L790,480 L806,500 M220,470 L236,494 L254,504",
       "Peak snow", fill=NONE, stroke="#FFFFFF", strokeWidth=5, opacity=60, cap="round")
for i, (x, y, w) in enumerate([(210,220,5),(300,170,4),(420,120,5),(640,130,4),(760,200,5),(820,330,4),
                               (180,380,4),(860,420,5)]):
    d.shape("ellipse", f"Snowflake {i+1}", x=x, y=y, width=w, height=w, fill="#FFFFFF", opacity=70, stroke=NONE)

# rock ledge: top edge across, bottom closes on the disc arc
ly = 720
ldx = math.sqrt(R*R - (ly - CY)**2)
d.path(f"M{CX-ldx:.1f},{ly} C300,700 420,712 520,708 C640,704 720,712 {CX+ldx:.1f},{ly} "
       f"A{R},{R} 0 0 1 {CX-ldx:.1f},{ly} Z", "Ledge", fill=ROCK_GRAD, stroke=NONE)
d.path(f"M{CX-ldx+6:.1f},{ly} C300,698 420,708 520,704 C640,700 720,708 {CX+ldx-6:.1f},{ly} "
       f"C700,724 600,722 520,724 C420,726 300,724 {CX-ldx+6:.1f},{ly} Z",
       "Ledge snow", fill=lin(0, 698, 0, 726, (0, "#FFFFFF"), (1, "#D4E0EA")), opacity=90, stroke=NONE)
for i, dd in enumerate(["M240,780 L300,800 L360,792", "M640,800 L700,780 L760,786", "M420,850 L480,840 L560,852"]):
    d.path(dd, f"Rock crack {i+1}", fill=NONE, stroke="#3A4450", strokeWidth=3, opacity=45, cap="round")

# --- body: lying, broad shoulders -------------------------------------------------------
d.path("M356,450 C304,510 270,610 282,712 C290,744 710,744 718,712 "
       "C730,610 696,510 644,450 Z", "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
for i, (x, y, r, rot) in enumerate([(330,560,18,0),(316,630,16,40),(350,680,14,80),(670,560,18,20),
                                    (684,630,16,60),(650,682,14,10),(370,500,14,30),(630,500,14,50)]):
    rosette(x, y, r, f"Body rosette {i+1}", rot)
# pale chest ruff
d.path("M432,490 C404,560 414,640 456,700 C476,722 524,722 544,700 "
       "C586,640 596,560 568,490 Z", "Chest ruff", fill=PALE_GRAD, opacity=85, stroke=NONE)
for i, dd in enumerate(["M450,560 C460,590 470,620 480,640", "M550,560 C540,590 530,620 520,640",
                        "M500,580 L500,650"]):
    d.path(dd, f"Chest fur {i+1}", fill=NONE, stroke="#B8B4AC", strokeWidth=4, opacity=40, cap="round")

# --- the huge tail, swept in front of the paws ------------------------------------------
spine = [cubic((676,640), (756,720), (640,812), (460,794), i/18) for i in range(19)]
spine += [cubic((460,794), (350,778), (270,744), (272,660), i/14) for i in range(1, 15)]
Lp, Rp, norms = [], [], []
n = len(spine)
for i, (x, y) in enumerate(spine):
    ax, ay = spine[max(i - 1, 0)]; bx, by = spine[min(i + 1, n - 1)]
    dx, dy = bx - ax, by - ay
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy/ln, dx/ln
    w = (80 - 14*i/(n - 1)) / 2
    norms.append((nx, ny, w))
    Lp.append((x + nx*w, y + ny*w)); Rp.append((x - nx*w, y - ny*w))
ex, ey = spine[-1]
tnx, tny, tw = norms[-1]
dd = "M%.1f,%.1f " % Lp[0] + " ".join("L%.1f,%.1f" % p for p in Lp[1:])
dd += " A%.1f,%.1f 0 0 0 %.1f,%.1f " % (tw, tw, Rp[-1][0], Rp[-1][1])
dd += " ".join("L%.1f,%.1f" % p for p in reversed(Rp[:-1])) + " Z"
d.path(dd, "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=6)
# under-shade along the lower edge, light along the top
d.path("M" + " L".join("%.1f,%.1f" % (x - nx*w*0.6, y - ny*w*0.6) for (x, y), (nx, ny, w) in zip(spine[2:-3], norms[2:-3])),
       "Tail shade", fill=NONE, stroke="#8A867E", strokeWidth=14, opacity=30, cap="round")
d.path("M" + " L".join("%.1f,%.1f" % (x + nx*w*0.5, y + ny*w*0.5) for (x, y), (nx, ny, w) in zip(spine[3:-4], norms[3:-4])),
       "Tail light", fill=NONE, stroke="#FFFFFF", strokeWidth=8, opacity=35, cap="round")
for k, i in enumerate([3, 7, 11, 15, 19, 23, 27]):
    (x, y), (nx, ny, w) = spine[i], norms[i]
    off = 0.35 if k % 2 == 0 else -0.3
    rosette(x + nx*w*off, y + ny*w*off, 15, f"Tail rosette {k+1}", rot=k*37)
# smoky tip
d.path("M%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f Z" % (Lp[-3][0], Lp[-3][1], tw + 2, tw + 2, Rp[-3][0], Rp[-3][1]),
       "Tail tip", fill=lin(0, 630, 0, 690, (0, "#2E2F36"), (1, "#5A5A60")), opacity=80, stroke=NONE)

# --- hip fur on the right covers the tail root --------------------------------------
d.path("M640,578 C700,574 750,622 750,684 C750,724 726,746 696,748 "
       "C660,744 636,716 634,680 C632,640 630,600 640,578 Z", "Hip", fill=BODY_GRAD, stroke=NONE)
d.path("M726,616 C742,638 750,660 750,684 C750,724 726,746 696,748", "Hip edge",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
rosette(700, 676, 15, "Hip rosette", 15)
rosette(676, 620, 12, "Hip rosette 2", 70)

# front legs + big fluffy paws
LEG_L = "M356,596 C350,640 356,690 364,730 L450,730 C454,690 452,640 446,596 Z"
pair(LEG_L, "Foreleg", fill=BODY_GRAD, stroke=NONE)
pair("M358,610 C352,650 356,690 364,730", "Foreleg outer edge", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
pair("M446,620 C452,660 454,694 450,730", "Foreleg inner edge", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
pair("M372,610 C368,650 370,690 376,724", "Foreleg sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=6, opacity=35, cap="round")
PAW_L = "M338,734 C334,706 366,694 404,694 C444,694 470,708 468,736 C466,760 436,770 404,770 C368,770 340,760 338,734 Z"
pair(PAW_L, "Paw", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
for j, x in enumerate([380, 404, 428]):
    pair(f"M{x},{752} L{x},{768}", f"Toe line {j+1}", fill=NONE, stroke=INK, strokeWidth=3, opacity=60, cap="round")
for j, (x, y, w, h) in enumerate([(392,630,14,12),(414,664,12,10),(388,690,10,9),(418,716,9,8)]):
    spot(x, y, w, h, f"Leg spot L{j+1}"); spot(1000 - x, y, w, h, f"Leg spot R{j+1}")

# --- cheek ruff + ears -----------------------------------------------------------------
pair("M372,410 C344,422 326,446 334,472 C322,488 332,510 352,514 C366,528 388,530 404,516 Z",
     "Cheek ruff", fill=COAT_GRAD, stroke=INK, strokeWidth=4)
EAR = "M362,330 C346,296 356,262 386,256 C414,252 432,276 430,304 Z"
pair(EAR, "Ear", fill=EAR_GRAD, stroke=INK, strokeWidth=5)
pair("M372,320 C362,296 370,274 390,272 C408,270 418,288 416,304 Z", "Inner ear",
     fill=lin(0, 270, 0, 320, (0, "#C4C0B8"), (1, "#F4F2EE")), opacity=85, stroke=NONE)

# --- head ----------------------------------------------------------------------------------
HEAD = ("M500,272 C576,272 640,304 656,370 C670,428 650,486 610,516 "
        "C578,540 540,550 500,550 C460,550 422,540 390,516 "
        "C350,486 330,428 344,370 C360,304 424,272 500,272 Z")
d.path(HEAD, "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Brow light", x=420, y=286, width=160, height=50, fill="#FFFFFF", opacity=25, stroke=NONE)
# forehead spot field
for i, (x, y, w) in enumerate([(500,300,10),(478,312,9),(522,312,9),(458,328,8),(500,326,9),(542,328,8),
                               (480,344,8),(520,344,8),(440,346,7),(560,346,7),(500,352,7),(424,330,6),(576,330,6)]):
    spot(x, y, w, w*0.85, f"Forehead spot {i+1}")
# cheek spot lines sweeping from the outer eye corners
for j, (x, y, w) in enumerate([(396,420,9),(388,440,8),(386,462,8),(392,484,7),(370,430,7),(366,456,6)]):
    spot(x, y, w, w, f"Cheek spot L{j+1}"); spot(1000 - x, y, w, w, f"Cheek spot R{j+1}")
pair("M380,382 C372,398 368,418 372,438", "Cheek stripe", fill=NONE, stroke=SPOT, strokeWidth=5, opacity=65, cap="round")

# --- the pale stare ----------------------------------------------------------------------
EYE = "M406,402 C424,380 460,376 480,396 C466,420 428,424 406,402 Z"
pair(EYE, "Eye", fill=IRIS_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Pupil L", x=438, y=391, width=11, height=13, fill="#14161A", stroke=NONE)
d.shape("ellipse", "Pupil R", x=551, y=391, width=11, height=13, fill="#14161A", stroke=NONE)
d.shape("ellipse", "Glint L", x=440, y=393, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=553, y=393, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
pair("M402,400 C422,378 462,374 484,396", "Upper lid", fill=NONE, stroke=INK, strokeWidth=7, cap="round")
pair("M408,384 C428,370 456,368 478,378", "Brow shadow", fill=NONE, stroke="#6E6A64", strokeWidth=8, opacity=22, cap="round")
pair("M418,416 C436,424 458,420 472,408", "Eye white rim", fill=NONE, stroke="#FFFFFF", strokeWidth=5, opacity=60, cap="round")
pair("M478,398 C476,414 472,428 466,440", "Tear line", fill=NONE, stroke=SPOT, strokeWidth=4, opacity=75, cap="round")

# --- muzzle ----------------------------------------------------------------------------------
d.path("M500,424 C520,424 530,448 538,464 C566,470 592,488 592,510 "
       "C590,534 552,546 500,546 C448,546 410,534 408,510 "
       "C408,488 434,470 462,464 C470,448 480,424 500,424 Z",
       "Muzzle pale", fill=PALE_GRAD, opacity=90, stroke=NONE)
d.path("M476,456 C490,450 510,450 524,456 C522,472 510,482 500,484 C490,482 478,472 476,456 Z",
       "Nose", fill=lin(0, 450, 0, 484, (0, "#C8A8A0"), (1, "#8A6A66")), stroke=INK, strokeWidth=4)
d.shape("ellipse", "Nose glint", x=486, y=455, width=10, height=5, fill="#FFFFFF", opacity=45, stroke=NONE)
d.path("M500,484 L500,500", "Philtrum", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
pair("M500,500 C490,505 476,507 464,506", "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
for j, (x, y) in enumerate([(448,490),(458,498),(446,502),(456,486)]):
    spot(x, y, 4, 4, f"Whisker dot L{j+1}", op=55); spot(1000 - x, y, 4, 4, f"Whisker dot R{j+1}", op=55)
d.path("M470,536 C488,544 512,544 530,536", "Chin shade", fill=NONE, stroke="#9E9990", strokeWidth=8, opacity=25, cap="round")
for j, (x1, y1, x2, y2) in enumerate([(440,488,320,462),(440,496,314,498),(444,504,322,534),(448,510,340,560)]):
    pair(f"M{x1},{y1} Q{(x1+x2)/2},{min(y1, y2) - 6} {x2},{y2}", f"Whisker {j+1}",
         fill=NONE, stroke="#FFFFFF", strokeWidth=2, opacity=75, cap="round")

# --- name ------------------------------------------------------------------------------------
d.text("SNOW LEOPARD", "Name", x=500, y=960, size=48, font="Virelai Sans",
       color="#DCE6EE", justify="center")

d.finish("snow-leopard-V1R00")
