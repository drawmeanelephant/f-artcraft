#!/usr/bin/env python3
"""Manta ray — field-guide plate V1R00. Dorsal view, seven metres of wing
gliding up through cathedral light: shafts lance down from a bright surface
oculus, the abyss pools below on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Manta Ray — Field Plate", 1000, 1000)

INK = "#241E28"                    # warm dark ink, never pure black
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def linO(x0, y0, x1, y1, *stops):
    """linear gradient with per-stop opacity"""
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#08131E"), (1, "#02060B"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#4E86A0"), (0.45, "#22475E"), (1, "#0A1B28"))
WING_GRAD = rad((0, "#46647A"), (0.55, "#2A4256"), (1, "#101D29"))
TAIL_GRAD = lin(500, 570, 520, 790, (0, "#2A4256"), (1, "#0D1822"))
ABYSS_GRAD = lin(0, 720, 0, 880, (0, "#0D2030"), (1, "#04090F"))

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

# --- backdrop + pelagic plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0C2230", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#9CC4D6", strokeWidth=3, opacity=35)

# the oculus: bright surface glow at the top of the water column
d.shape("ellipse", "Oculus", x=340, y=58, width=320, height=130,
        fill=rad((0, "#D8F2F6"), (0.6, "#9CD4E2"), (1, "#5E9AB0")),
        opacity=75, stroke=NONE)
d.shape("ellipse", "Oculus core", x=420, y=66, width=160, height=72,
        fill="#F0FBFC", opacity=55, stroke=NONE)

# cathedral shafts: tapered quads from the oculus, fading before the floor
BEAMS = [
    ((452, 96), (500, 92), (566, 700), (470, 700), 30),   # centre-left broad
    ((508, 92), (546, 96), (700, 620), (628, 636), 24),   # right of centre
    ((400, 104), (438, 98), (344, 560), (292, 540), 18),  # far left, shorter
    ((560, 100), (596, 108), (760, 480), (712, 466), 14), # far right, shortest
    ((466, 98), (498, 94), (404, 660), (356, 648), 16),   # inner left blade
]
for i, (tl, tr, br, bl, op) in enumerate(BEAMS):
    grad = linO(500, 90, 500, 700, (0, "#C8ECF4", op + 18),
                (0.55, "#9AD4E4", op), (1, "#9AD4E4", 0))
    d.path(f"M{tl[0]},{tl[1]} L{tr[0]},{tr[1]} L{br[0]},{br[1]} L{bl[0]},{bl[1]} Z",
           f"Shaft {i+1}", fill=grad, stroke=NONE)

# marine snow drifting through the light
for i, (x, y, w, o) in enumerate([(392,240,5,55),(468,180,4,60),(560,220,5,50),(640,300,4,45),
                                  (430,330,4,40),(520,300,5,55),(610,410,4,35),(360,420,5,40),
                                  (476,440,4,45),(688,360,4,30),(300,330,4,35),(420,560,4,30),
                                  (580,540,5,35),(720,300,5,30),(340,500,4,30),(660,500,4,30)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#EAF6FA", opacity=o, stroke=NONE)

# the abyss pools at the bottom of the disc, closing on its own arc
fy = 742
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C330,728 420,752 500,744 C590,736 670,754 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Abyss", fill=ABYSS_GRAD, stroke=NONE)

# --- the whip tail, curling off behind -----------------------------------------
def quad(p0, p1, p2, t):
    u = 1 - t
    x = u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0]
    y = u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1]
    dx = 2*u*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0])
    dy = 2*u*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1])
    return x, y, dx, dy

def ribbon(root, ctrl, tip, w0, w1, label, n=26):
    L, Rr = [], []
    for k in range(n + 1):
        t = k / n
        x, y, dx, dy = quad(root, ctrl, tip, t)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x + nx*w, y + ny*w)); Rr.append((x - nx*w, y - ny*w))
    dd = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    d.path(dd, label, fill=TAIL_GRAD, stroke=INK, strokeWidth=3)

ribbon((500, 586), (572, 676), (526, 796), 14, 2.5, "Tail")
# dorsal ridge stripe down the tail
d.path("M500,592 C540,660 552,714 534,772", "Tail ridge", fill=NONE,
       stroke="#7FA8BC", strokeWidth=3, opacity=45, cap="round")

# --- the wing disc: one symmetric silhouette ------------------------------------
# nearly straight cephalic edge with two low lobe bumps, convex leading edges
# out to swept-back tips, convex trailing edges meeting at a broad rear.
BODY = ("M500,296 "
        "C490,288 480,286 468,288 "
        "C452,290 442,296 436,306 "
        "C380,312 310,348 252,400 "
        "C214,432 192,446 178,452 "
        "C186,458 198,466 212,474 "
        "C300,512 380,548 448,580 "
        "C470,589 488,594 500,596 "
        "C512,594 530,589 552,580 "
        "C620,548 700,512 788,474 "
        "C802,466 814,458 822,452 "
        "C808,446 786,432 748,400 "
        "C690,348 620,312 564,306 "
        "C558,296 548,290 532,288 "
        "C520,286 510,288 500,296 Z")
d.path(BODY, "Wing disc", fill=WING_GRAD, stroke=INK, strokeWidth=7)

# shadow band hugging the trailing edge (the side turned from the light)
TE = ("M212,474 C300,512 380,548 448,580 C470,589 488,594 500,596 "
      "C512,594 530,589 552,580 C620,548 700,512 788,474")
d.path(TE, "Trailing shade", fill=NONE, stroke="#08141E",
       strokeWidth=20, opacity=30, cap="round")
# rim light along both leading edges, facing the oculus
LE = "M436,306 C380,312 310,348 252,400 C214,432 192,446 178,452"
pair(LE, "Leading light", fill=NONE, stroke="#C4E4EE",
     strokeWidth=7, opacity=55, cap="round")
# cephalic edge rim light between the lobes
d.path("M436,306 C452,296 480,292 500,296 C520,292 548,296 564,306",
       "Cephalic light", fill=NONE, stroke="#C4E4EE", strokeWidth=5,
       opacity=45, cap="round")

# --- dorsal markings: the shoulder chevron and mid-back sheen -------------------
pair("M470,330 C436,340 398,362 366,392 C392,388 428,378 456,366 "
     "C466,352 470,340 470,330 Z",
     "Shoulder mark", fill="#A8C4D2", opacity=38, stroke=NONE)
d.path("M484,322 C482,372 488,432 500,496 C512,432 518,372 516,322 "
       "C506,316 494,316 484,322 Z",
       "Mid-back sheen", fill="#7FA0B4", opacity=26, stroke=NONE)
# speckled shading across the wing span
for i, (x, y, w) in enumerate([(300,420,8),(360,392,6),(430,450,7),(570,450,7),(640,392,6),
                               (700,420,8),(252,446,6),(748,446,6),(470,520,6),(530,520,6)]):
    d.shape("ellipse", f"Wing fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#0C1822", opacity=35, stroke=NONE)

# --- eyes: small ovals just inside the head corners -------------------------------
d.shape("ellipse", "Eye L", x=440, y=314, width=16, height=11,
        fill="#0D1822", opacity=85, stroke=NONE)
d.shape("ellipse", "Eye R", x=544, y=314, width=16, height=11,
        fill="#0D1822", opacity=85, stroke=NONE)
d.shape("ellipse", "Eye glint L", x=444, y=316, width=4, height=4,
        fill="#CFEDF4", opacity=70, stroke=NONE)
d.shape("ellipse", "Eye glint R", x=548, y=316, width=4, height=4,
        fill="#CFEDF4", opacity=70, stroke=NONE)

# --- name ---------------------------------------------------------------------------
d.text("MANTA RAY", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#CFE2EA", justify="center")

d.finish("manta-ray-V1R00")
