#!/usr/bin/env python3
"""Addax — field-guide plate V1R00. Face-forward bust: twin corkscrew horns
spiralling off a dark forehead toupee, bone-white coat, wide splayed desert
hooves planted in the dunes. Heat-haze amber plate.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Addax — Field Plate", 1000, 1000)

INK = "#3B2F22"
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#33241A"), (1, "#120A06"))
PLATE_GRAD = rad((0, "#F6DCA6"), (0.65, "#DCA75C"), (1, "#96622C"))
COAT_GRAD = rad((0, "#FBF4E2"), (0.6, "#E6DCC4"), (1, "#B3A686"))
NECK_GRAD = lin(0, 560, 0, 820, (0, "#F2EAD6"), (1, "#BFb28E"))
HORN_GRAD = lin(0, 150, 0, 430, (0, "#E2D3AC"), (1, "#9A8560"))
HORN_FAR  = lin(0, 150, 0, 430, (0, "#B3A27E"), (1, "#6E5E42"))
TOUPEE    = lin(0, 360, 0, 470, (0, "#5A4128"), (1, "#33241A"))
DUNE_GRAD = lin(0, 760, 0, 880, (0, "#C68A44"), (1, "#7A4E20"))
EAR_GRAD  = lin(0, 440, 0, 520, (0, "#D9CDAF"), (1, "#A8987A"))

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

def disc_x(y, side, r=420):
    return CX + side*math.sqrt(r*r - (y - CY)**2)

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]
    y = u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
    dx = 3*u*u*(p1[0]-p0[0]) + 6*u*t*(p2[0]-p1[0]) + 3*t*t*(p3[0]-p2[0])
    dy = 3*u*u*(p1[1]-p0[1]) + 6*u*t*(p2[1]-p1[1]) + 3*t*t*(p3[1]-p2[1])
    return (x, y), (dx, dy)

# --- backdrop + heat-haze plate -----------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
# faint heat shimmer behind the plate
for i, (x0, y0, x1) in enumerate([(60,180,240),(700,140,940),(90,520,280),(720,600,930),(150,860,330),(660,860,890)]):
    d.path(f"M{x0},{y0} C{x0+40},{y0-14} {x0+80},{y0+14} {x0+120},{y0} "
           f"C{x0+140},{y0-10} {x1-30},{y0+8} {x1},{y0-4}", f"Haze {i+1}",
           fill=NONE, stroke="#C98A4A", strokeWidth=4, opacity=18, cap="round")
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A4E24", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F8E8C4", strokeWidth=3, opacity=55)
# low sun + shimmer lines inside the plate
d.shape("ellipse", "Sun", x=590, y=150, width=120, height=120,
        fill=rad((0, "#FFE9B0"), (1, "#F0B45E")), opacity=70, stroke=NONE)
d.shape("ellipse", "Sun halo", x=560, y=120, width=180, height=180,
        fill="#FFE9B0", opacity=14, stroke=NONE)
for i, (x0, y0, x1) in enumerate([(180,320,360),(620,340,830),(160,450,340),(660,470,840),(230,230,390)]):
    d.path(f"M{x0},{y0} C{x0+50},{y0-10} {x0+100},{y0+10} {x1},{y0-6}", f"Shimmer {i+1}",
           fill=NONE, stroke="#FFE4B0", strokeWidth=5, opacity=25, cap="round")
for i, (x, y, w) in enumerate([(200,380,6),(800,260,7),(160,580,7),(840,560,6),(300,150,5),
                               (430,120,5),(760,180,6),(250,690,6),(750,700,6)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#A8743A", opacity=35, stroke=NONE)

# rolling dunes — back ridge then the foreground dune, both close on the disc arc
dy = 768
d.path(f"M{disc_x(dy,-1):.1f},{dy} C330,742 420,762 540,752 C640,744 700,758 {disc_x(dy,1):.1f},{dy-6} "
       f"A{R},{R} 0 0 1 {disc_x(dy,-1):.1f},{dy} Z", "Dune back", fill="#B87E3C", opacity=55, stroke=NONE)
gy = 812
d.path(f"M{disc_x(gy,-1):.1f},{gy} C280,796 400,806 500,802 C600,798 720,808 {disc_x(gy,1):.1f},{gy} "
       f"A{R},{R} 0 0 1 {disc_x(gy,-1):.1f},{gy} Z", "Dune front", fill=DUNE_GRAD, stroke=NONE)
d.path(f"M{disc_x(gy,-1)+10:.1f},{gy-4} C280,792 400,802 500,798 C600,794 720,804 {disc_x(gy,1)-10:.1f},{gy-4}",
       "Dune crest light", fill=NONE, stroke="#EDC078", strokeWidth=5, opacity=45, cap="round")

# --- corkscrew horns (markhor technique: tapered ribbon + rotated ridges) -------
def horn(spine, w0, w1, label, fill, twists=2.6, amp=0.42, n_ridges=8, samples=30,
         ridge_col="#6E5E42", sheen_col="#F6ECD2"):
    left, right, mid = [], [], []
    for i in range(samples + 1):
        t = i / samples
        (x, y), (dx, dy) = cubic(*spine, t)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0)*t) / 2
        ph = math.sin(t*math.pi*2*twists)
        mid.append((x, y, nx, ny, w))
        left.append((x + nx*w*(1 + amp*ph), y + ny*w*(1 + amp*ph)))
        right.append((x - nx*w*(1 - amp*ph), y - ny*w*(1 - amp*ph)))
    dd = "M%.1f,%.1f " % left[0] + " ".join("L%.1f,%.1f" % p for p in left[1:])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(right)) + " Z"
    d.path(dd, label, fill=fill, stroke=INK, strokeWidth=5)
    for j in range(n_ridges):
        t = 0.08 + 0.84*j/(n_ridges - 1)
        x, y, nx, ny, w = mid[round(t*samples)]
        ang = math.radians(24)   # one consistent tilt reads as a screw thread
        rx, ry = nx*math.cos(ang) - ny*math.sin(ang), nx*math.sin(ang) + ny*math.cos(ang)
        e = w * 1.15
        d.path("M%.1f,%.1f L%.1f,%.1f" % (x - rx*e, y - ry*e, x + rx*e, y + ry*e),
               f"{label} ridge {j+1}", fill=NONE, stroke=ridge_col,
               strokeWidth=5, opacity=75, cap="round")
    e0, e1, e2 = mid[2], mid[samples//2], mid[samples - 3]
    d.path("M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (
        e0[0] + e0[2]*e0[4]*0.8, e0[1] + e0[3]*e0[4]*0.8,
        e1[0] + e1[2]*e1[4]*0.8, e1[1] + e1[3]*e1[4]*0.8,
        e2[0] + e2[2]*e2[4]*0.8, e2[1] + e2[3]*e2[4]*0.8),
        f"{label} sheen", fill=NONE, stroke=sheen_col, strokeWidth=6,
        opacity=30, cap="round")

# one horn per side — thick at the base, corkscrewing up and slightly out
horn([(452, 445), (420, 330), (400, 240), (368, 150)], 60, 8,
     "Horn L", HORN_GRAD, twists=3.0, amp=0.5, n_ridges=10)
horn([(548, 445), (580, 330), (600, 240), (632, 150)], 60, 8,
     "Horn R", HORN_GRAD, twists=3.0, amp=0.5, n_ridges=10)

# --- ears, held low and wide -----------------------------------------------------
EAR = "M382,470 C340,452 300,458 284,486 C296,512 340,522 376,508 Z"
pair(EAR, "Ear", fill=EAR_GRAD, stroke=INK, strokeWidth=5)
pair("M368,480 C340,468 314,472 304,488 C314,504 344,508 366,498 Z",
     "Inner ear", fill="#8E8064", opacity=60, stroke=NONE)

# --- neck + chest + splayed forelegs: one silhouette, no seam lines -------------
d.path("M390,560 C352,612 340,668 348,720 "
       "C352,760 358,792 362,822 L448,822 C452,792 458,760 462,742 "
       "C480,754 520,754 538,742 C542,760 548,792 552,822 L638,822 "
       "C642,792 648,760 652,720 C660,668 648,612 610,560 Z",
       "Neck + chest + forelegs", fill=NECK_GRAD, stroke=INK, strokeWidth=6)
# chest shading + sunlit edge
d.shape("ellipse", "Chest light", x=435, y=580, width=130, height=120,
        fill="#FFFFFF", opacity=18, stroke=NONE)
d.path("M356,610 C348,660 348,700 356,744", "Chest shade L", fill=NONE,
       stroke="#9C8E70", strokeWidth=10, opacity=30, cap="round")
d.path("M644,610 C652,660 652,700 644,744", "Chest shade R", fill=NONE,
       stroke="#9C8E70", strokeWidth=10, opacity=30, cap="round")
# leg shading where the belly shadow falls
d.path("M470,748 C486,758 514,758 530,748 C524,764 512,772 500,772 C488,772 476,764 470,748 Z",
       "Belly shade", fill="#9C8E70", opacity=28, stroke=NONE)

# --- wide desert hooves under each leg --------------------------------------------
for side, hx in (("L", 396), ("R", 604)):
    d.path(f"M{hx-48},830 C{hx-46},804 {hx-26},792 {hx},792 C{hx+26},792 {hx+46},804 {hx+48},830 "
           f"C{hx+46},846 {hx+24},852 {hx},852 C{hx-24},852 {hx-46},846 {hx-48},830 Z",
           f"Hoof {side}", fill=lin(0, 792, 0, 852, (0, "#6E5E44"), (1, "#3E3222")),
           stroke=INK, strokeWidth=4)
    d.path(f"M{hx},800 L{hx},840", f"Hoof cleft {side}", fill=NONE,
           stroke="#2C2216", strokeWidth=4, cap="round")
    d.path(f"M{hx-34},812 C{hx-18},802 {hx+18},802 {hx+34},812", f"Hoof light {side}",
           fill=NONE, stroke="#A89468", strokeWidth=4, opacity=50, cap="round")

# --- head: short pale face under the toupee -----------------------------------------
d.path("M500,398 C568,398 620,440 626,506 C630,556 612,606 574,638 "
       "C552,656 526,664 500,664 C474,664 448,656 426,638 "
       "C388,606 370,556 374,506 C380,440 432,398 500,398 Z",
       "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=7)
d.shape("ellipse", "Brow light", x=432, y=408, width=136, height=54,
        fill="#FFFFFF", opacity=20, stroke=NONE)
# the dark forehead toupee between the horn bases — widow's-peak fringe
d.path("M444,410 C466,398 534,398 556,410 C576,424 584,448 578,470 "
       "L566,458 L562,486 L540,462 L530,494 L512,466 L500,498 "
       "L488,466 L470,494 L460,462 L438,486 L434,458 L422,470 "
       "C416,448 424,424 444,410 Z",
       "Toupee", fill=TOUPEE, stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M462,414 C468,440 466,462 460,478", "M500,406 L500,488",
                        "M538,414 C532,440 534,462 540,478", "M480,410 C484,436 482,462 476,480",
                        "M520,410 C516,436 518,462 524,480"]):
    d.path(dd, f"Toupee strand {i+1}", fill=NONE, stroke="#241A10",
           strokeWidth=4, opacity=50, cap="round")
d.path("M446,426 C472,410 528,410 554,426", "Toupee sheen", fill=NONE,
       stroke="#8A6A44", strokeWidth=6, opacity=45, cap="round")

# white face blaze running down the bridge
d.path("M500,486 C514,486 522,514 524,552 C526,594 518,624 500,630 "
       "C482,624 474,594 476,552 C478,514 486,486 500,486 Z",
       "Face blaze", fill="#FBF4E2", opacity=85, stroke=NONE)
# soft shading under the cheeks
d.path("M402,530 C410,574 428,612 454,638", "Cheek shade L", fill=NONE,
       stroke="#9C8E70", strokeWidth=12, opacity=28, cap="round")
d.path("M598,530 C590,574 572,612 546,638", "Cheek shade R", fill=NONE,
       stroke="#9C8E70", strokeWidth=12, opacity=28, cap="round")

# --- eyes: dark, calm, slightly hooded -------------------------------------------------
for side, cx in (("L", 432), ("R", 568)):
    cy = 528
    d.shape("ellipse", f"Socket {side}", x=cx-34, y=cy-32, width=68, height=64,
            fill="#A8987A", opacity=30, stroke=NONE)
    d.path(f"M{cx-26},{cy-6} C{cx-18},{cy-22} {cx+18},{cy-22} {cx+26},{cy-6} "
           f"C{cx+18},{cy+10} {cx-18},{cy+10} {cx-26},{cy-6} Z",
           f"Eye {side}", fill="#241C14", stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Glint {side}", x=cx-10, y=cy-14, width=9, height=8,
            fill="#FFFFFF", opacity=80, stroke=NONE)
    pair(f"M{cx-28},{cy-14} C{cx-16},{cy-26} {cx+16},{cy-26} {cx+30},{cy-14}", "Upper lid",
         fill=NONE, stroke=INK, strokeWidth=5, cap="round")
    pair(f"M{cx-24},{cy+8} C{cx-8},{cy+16} {cx+10},{cy+16} {cx+26},{cy+8}", "Lash line",
         fill=NONE, stroke="#6E5E42", strokeWidth=3, opacity=60, cap="round")

# --- muzzle: wide dark nostrils on the pale nose -----------------------------------------
d.shape("ellipse", "Muzzle", x=450, y=590, width=100, height=60,
        fill="#E4DCC8", opacity=70, stroke=NONE)
d.path("M464,614 C472,604 490,602 494,616 C496,626 486,634 476,632 C466,630 460,622 464,614 Z",
       "Nostril L", fill="#332619", stroke=NONE)
d.path("M536,614 C528,604 510,602 506,616 C504,626 514,634 524,632 C534,630 540,622 536,614 Z",
       "Nostril R", fill="#332619", stroke=NONE)
d.path("M472,640 C488,650 512,650 528,640", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M500,632 L500,640", "Philtrum", fill=NONE, stroke=INK, strokeWidth=4, cap="round")

# --- name --------------------------------------------------------------------------------
d.text("ADDAX", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#F2DCA8", justify="center")

d.finish("addax-V1R00")
