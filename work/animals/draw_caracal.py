#!/usr/bin/env python3
"""Caracal — field-guide plate V1R00. Stern, symmetrical head-and-shoulders
portrait, face forward: tall ears topped by long inky tufts, sandy-tawny coat,
white muzzle and eye patches, black tear lines and whisker spots. Dusk plate:
warm horizon glow low, violet sky high, first stars; the shoulders close on
the disc's own arc.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Caracal — Field Plate", 1000, 1000)

INK = "#2A1A14"
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#2E1F3E"), (1, "#0C0812"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#6E4C7C"), (0.38, "#B87C8E"),
                 (0.68, "#EBA982"), (1, "#F8D7A2"))
HEAD_GRAD = rad((0, "#E8BC88"), (0.68, "#CF9660"), (1, "#9C663C"))
BUST_GRAD = lin(0, 620, 0, 880, (0, "#C68C58"), (1, "#8E5A34"))
TUFT_GRAD = lin(0, 100, 0, 220, (0, "#050404"), (1, "#2A1E18"))
WHITE_GRAD = rad((0, "#FFFDF8"), (1, "#EADCC8"))
IRIS_GRAD = rad((0, "#F2D36A"), (0.7, "#D8A038"), (1, "#9C6A1E"))

def ear_grad(tx):
    return lin(tx, 170, tx, 440, (0, "#17100C"), (0.38, "#5A3A24"), (1, "#C08A58"))

def mirror(dd):
    """Mirror an absolute M/L/C/Q/Z path across x=500."""
    out, toks = [], re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd)
    expect_x = True
    for t in toks:
        if t.isalpha():
            out.append(t); expect_x = True; continue
        v = float(t)
        if expect_x:
            out.append(f"{1000 - v:g},"); expect_x = False
        else:
            out[-1] += f"{v:g}"; expect_x = True
    return " ".join(out)

def pair(dd, label, **kw):
    d.path(dd, f"{label} L", **kw)
    d.path(mirror(dd), f"{label} R", **kw)

def ribbon(p0, p1, p2, w0, w1, label, fill, samples=16, **kw):
    """Tapered filled stroke along a quadratic — used for the ear tufts."""
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

# --- backdrop + dusk plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(120,120,5),(880,160,6),(70,420,4),(930,380,5),(150,860,5),(860,880,4),(40,700,4),(950,640,5)]):
    d.shape("ellipse", f"Sky star {i+1}", x=x, y=y, width=w, height=w, fill="#E8D8F0", opacity=40, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5A3A5E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFE8D0", strokeWidth=3, opacity=50)
# horizon glow sitting behind the shoulders
d.shape("ellipse", "Horizon glow", x=180, y=560, width=640, height=260, fill="#FFE6B8", opacity=30, stroke=NONE)
d.shape("ellipse", "Sun haze", x=330, y=600, width=340, height=180, fill="#FFF0CC", opacity=30, stroke=NONE)
d.shape("ellipse", "Dusk cloud L", x=150, y=430, width=220, height=40, fill="#F6C6A6", opacity=26, stroke=NONE)
d.shape("ellipse", "Dusk cloud R", x=640, y=470, width=210, height=36, fill="#F6C6A6", opacity=22, stroke=NONE)
for i, (x, y, w) in enumerate([(220,230,6),(780,220,7),(180,330,4),(820,320,5),(420,92,5),(600,100,4),
                               (690,150,4),(300,150,5),(140,410,4),(860,420,4)]):
    d.shape("ellipse", f"Plate star {i+1}", x=x, y=y, width=w, height=w, fill="#FFF4E6", opacity=55, stroke=NONE)

# savanna horizon: a low ridge closing on the disc arc
ry = 760
rdx = math.sqrt(R*R - (ry - CY)**2)
d.path(f"M{CX-rdx:.1f},{ry} C330,742 420,752 500,746 C590,740 680,748 {CX+rdx:.1f},{ry} "
       f"A{R},{R} 0 0 1 {CX-rdx:.1f},{ry} Z",
       "Horizon ridge", fill=lin(0, 740, 0, 880, (0, "#8E5A6A"), (1, "#5A3448")), opacity=70, stroke=NONE)

# --- shoulders / bust (closes on the disc arc) -------------------------------------------
by = 800
bdx = math.sqrt(R*R - (by - CY)**2)
d.path(f"M368,610 C336,668 300,736 {CX-bdx:.1f},{by} "
       f"A{R},{R} 0 0 0 {CX+bdx:.1f},{by} "
       f"C700,736 664,668 632,610 Z",
       "Bust", fill=BUST_GRAD, stroke=NONE)
pair("M368,612 C336,668 300,736 262,792", "Shoulder line", fill=NONE, stroke=INK, strokeWidth=6, cap="round")
# white throat + chest blaze
d.path("M416,640 C428,708 466,770 500,838 C534,770 572,708 584,640 C550,662 450,662 416,640 Z",
       "Throat white", fill=WHITE_GRAD, opacity=80, stroke=NONE)
pair("M330,720 C360,700 392,690 420,690", "Chest fur", fill=NONE, stroke="#7A4C2C", strokeWidth=5, opacity=35, cap="round")
pair("M300,770 C340,748 380,740 412,742", "Chest fur 2", fill=NONE, stroke="#7A4C2C", strokeWidth=5, opacity=30, cap="round")
d.path("M380,700 C420,680 580,680 620,700", "Collar shade", fill=NONE,
       stroke="#6A4024", strokeWidth=16, opacity=22, cap="round")

# --- ears: tall, upright, slightly flared ----------------------------------------------
EAR_L = "M352,462 C330,390 316,290 322,196 C362,250 420,322 462,384 Z"
d.path(EAR_L, "Ear L", fill=ear_grad(322), stroke=INK, strokeWidth=6)
d.path(mirror(EAR_L), "Ear R", fill=ear_grad(678), stroke=INK, strokeWidth=6)
INNER_L = "M362,440 C348,380 338,306 340,240 C372,286 412,338 444,388 Z"
pair(INNER_L, "Inner ear", fill=lin(0, 240, 0, 440, (0, "#C9A88E"), (1, "#F6E6D2")), opacity=88, stroke=NONE)
# pale fringe hairs inside the ear
for j, (a, b, c2) in enumerate([((360,430),(352,380),(350,330)), ((376,418),(372,370),(366,320)),
                                 ((392,410),(392,370),(386,330)), ((408,404),(410,370),(404,340))]):
    pair(f"M{a[0]},{a[1]} Q{b[0]},{b[1]} {c2[0]},{c2[1]}", f"Ear fringe {j+1}",
         fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=45, cap="round")
pair("M336,250 C334,310 340,380 354,440", "Ear rim light", fill=NONE,
     stroke="#E8B884", strokeWidth=4, opacity=30, cap="round")

# --- the tufts: long inky flames off each ear tip --------------------------------------------
TUFT = ("M318,232 C312,192 308,150 314,112 C322,138 328,152 330,162 "
        "C334,148 338,136 344,124 C346,160 346,200 344,232 Z")
d.path(TUFT, "Tuft L", fill=TUFT_GRAD, stroke=NONE)
d.path(mirror(TUFT), "Tuft R", fill=TUFT_GRAD, stroke=NONE)
pair("M318,176 Q306,150 302,122", "Tuft flick outer", fill=NONE, stroke="#120C0A", strokeWidth=4, cap="round")
pair("M340,180 Q350,156 356,134", "Tuft flick inner", fill=NONE, stroke="#120C0A", strokeWidth=3, cap="round")
pair("M326,214 C322,180 320,150 318,126", "Tuft sheen", fill=NONE, stroke="#9A8AA4", strokeWidth=3, opacity=40, cap="round")
pair("M338,210 C338,184 340,160 342,138", "Tuft sheen 2", fill=NONE, stroke="#9A8AA4", strokeWidth=2, opacity=30, cap="round")

# --- head ------------------------------------------------------------------------------------
HEAD = ("M500,372 C584,372 650,404 672,470 C690,530 670,594 632,632 "
        "C594,668 548,684 500,684 C452,684 406,668 368,632 "
        "C330,594 310,530 328,470 C350,404 416,372 500,372 Z")
d.path(HEAD, "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Crown light", x=410, y=384, width=180, height=60, fill="#FFE8C4", opacity=22, stroke=NONE)
pair("M344,560 C356,600 380,630 410,650", "Cheek shade", fill=NONE,
     stroke="#8A5630", strokeWidth=16, opacity=22, cap="round")
# forehead: two fine dark stripes rising from the inner brows
pair("M474,470 C470,440 468,414 470,388", "Brow stripe", fill=NONE,
     stroke="#3A2416", strokeWidth=5, opacity=70, cap="round")
pair("M486,468 C486,446 486,426 488,404", "Brow stripe fine", fill=NONE,
     stroke="#3A2416", strokeWidth=3, opacity=45, cap="round")
# white eye patches above and below each eye
pair("M392,470 C412,456 444,454 462,466 C446,472 414,476 392,470 Z", "Brow white",
     fill=WHITE_GRAD, opacity=85, stroke=NONE)
pair("M396,524 C416,540 446,544 464,534 C446,548 414,550 396,524 Z", "Under-eye white",
     fill=WHITE_GRAD, opacity=85, stroke=NONE)

# --- eyes: almond, lids drawn low = stern ---------------------------------------------------
EYE_L = "M394,500 C410,482 446,476 466,494 C452,516 418,522 394,500 Z"
pair(EYE_L, "Eye", fill=IRIS_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Pupil L", x=425, y=484, width=14, height=32, fill="#120A06", stroke=NONE)
d.shape("ellipse", "Pupil R", x=561, y=484, width=14, height=32, fill="#120A06", stroke=NONE)
d.shape("ellipse", "Glint L", x=428, y=490, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=564, y=490, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
# heavy upper lid, sloping down toward the nose
pair("M390,494 C414,474 448,474 470,496", "Upper lid", fill=NONE, stroke=INK, strokeWidth=7, cap="round")
pair("M396,488 C420,474 446,474 466,486", "Lid shade", fill=NONE, stroke="#3A2416", strokeWidth=6, opacity=30, cap="round")
# black tear line: inner eye corner down to the muzzle
pair("M466,500 C462,526 456,548 450,566", "Tear line", fill=NONE, stroke="#140C08", strokeWidth=6, cap="round")

# --- muzzle ------------------------------------------------------------------------------------
d.path("M500,528 C520,528 532,556 540,574 C566,580 600,596 604,624 "
       "C604,650 560,668 500,668 C440,668 396,650 396,624 "
       "C400,596 434,580 460,574 C468,556 480,528 500,528 Z",
       "Muzzle white", fill=WHITE_GRAD, opacity=92, stroke=NONE)
d.path("M484,500 C490,530 494,556 496,574 M516,500 C510,530 506,556 504,574",
       "Bridge light", fill=NONE, stroke="#F2D2A6", strokeWidth=6, opacity=40, cap="round")
# whisker-pad spots
pair("M420,600 C432,592 452,594 458,604 C450,614 428,614 420,600 Z", "Whisker spot",
     fill="#1C120C", opacity=85, stroke=NONE)
for j, (x, y) in enumerate([(430,616),(444,620),(438,630)]):
    d.shape("ellipse", f"Whisker dot L{j+1}", x=x, y=y, width=4, height=4, fill="#6A4A3A", opacity=60, stroke=NONE)
    d.shape("ellipse", f"Whisker dot R{j+1}", x=1000-x-4, y=y, width=4, height=4, fill="#6A4A3A", opacity=60, stroke=NONE)
# nose
d.path("M478,574 C490,568 510,568 522,574 C520,588 508,598 500,600 C492,598 480,588 478,574 Z",
       "Nose", fill=lin(0, 568, 0, 600, (0, "#C47A6A"), (1, "#7A3A30")), stroke=INK, strokeWidth=4)
d.shape("ellipse", "Nose glint", x=488, y=574, width=10, height=5, fill="#FFFFFF", opacity=40, stroke=NONE)
# mouth: philtrum + downturned line
d.path("M500,600 L500,620", "Philtrum", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
pair("M500,620 C488,630 474,632 462,628", "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M470,646 C486,654 514,654 530,646", "Chin shade", fill=NONE,
       stroke="#BCA48A", strokeWidth=6, opacity=45, cap="round")
# whiskers
for j, (x1, y1, x2, y2) in enumerate([(424,604,300,580),(426,612,296,616),(430,620,306,650),(436,626,326,676)]):
    pair(f"M{x1},{y1} Q{(x1+x2)/2},{min(y1,y2)-6} {x2},{y2}", f"Whisker {j+1}",
         fill=NONE, stroke="#FFFFFF", strokeWidth=2, opacity=70, cap="round")

# --- name ------------------------------------------------------------------------------------
d.text("CARACAL", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#F2D8C2", justify="center")

d.finish("caracal-V1R00")
