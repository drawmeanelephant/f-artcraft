#!/usr/bin/env python3
"""Polar bear — field-guide plate V1R00. Face-forward, patient: the cream head
low over the ice edge, small rounded ears, long muzzle and the big black nose,
two huge forepaws resting on the floe. Arctic-night plate — deep sea-dark disc,
aurora ribbons and their faint reflection on the ice, which closes on the
disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Polar Bear — Field Plate", 1000, 1000)

INK = "#241C14"                    # warm dark ink, never pure black
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

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0C1A28"), (1, "#030810"))
PLATE_GRAD = rad((0, "#3E6E84"), (0.55, "#1E4054"), (1, "#0A1E2E"))
FUR_GRAD = rad((0, "#FFFCF2"), (0.6, "#EFE9DC"), (1, "#C4BBAA"))
MUZZLE_GRAD = rad((0, "#FFFBF0"), (0.7, "#ECE5D6"), (1, "#CFC6B4"))
NOSE_GRAD = lin(0, 600, 0, 660, (0, "#3A342E"), (1, "#14100C"))
ICE_GRAD = lin(0, 700, 0, 880, (0, "#F2FAFC"), (0.4, "#C9DEE8"), (1, "#7FA4B6"))
PAW_GRAD = rad((0, "#FBF6EA"), (0.7, "#E4DDCB"), (1, "#BDB4A2"))

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

def on_disc(x, y, pad=0, r=R):
    return math.hypot(x - CX, y - CY) <= r - pad

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

# --- backdrop + arctic-night plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(140,120,4),(860,140,5),(60,400,4),(940,380,4),(110,850,4),(890,860,5),(45,660,3),(950,650,4)]):
    d.shape("ellipse", f"Backdrop star {i+1}", x=x, y=y, width=w, height=w, fill="#CFE4F0", opacity=35, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#3E6E84", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0A1E2C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BFE0EE", strokeWidth=3, opacity=35)

# aurora ribbons: thick soft strokes fading out at both ends, all inside the disc
AURORA = [
    ("M215,240 C340,180 470,260 620,190 C690,160 745,170 780,205",
     linO(215, 240, 780, 205, (0, "#78F0C0", 0), (0.3, "#78F0C0", 55),
          (0.75, "#58D8E8", 40), (1, "#58D8E8", 0)), 66, 90),
    ("M185,340 C320,290 460,360 600,300 C680,265 740,280 790,310",
     linO(185, 340, 790, 310, (0, "#58D8E8", 0), (0.35, "#58D8E8", 30),
          (0.8, "#78F0C0", 22), (1, "#78F0C0", 0)), 44, 80),
    ("M280,160 C420,110 580,160 700,140",
     linO(280, 160, 700, 140, (0, "#A0F0D8", 0), (0.5, "#A0F0D8", 35),
          (1, "#A0F0D8", 0)), 26, 85),
]
for i, (dd_, grad, w_, op) in enumerate(AURORA):
    d.path(dd_, f"Aurora band {i+1}", fill=NONE, stroke=grad,
           strokeWidth=w_, opacity=op, cap="round")
# stars + falling snow
for i, (x, y, w) in enumerate([(200,240,5),(320,150,4),(450,110,5),(610,120,4),(740,170,5),(830,280,4),
                               (170,380,4),(860,420,5),(260,470,3),(780,480,3),(400,190,3),(680,240,3)]):
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w, fill="#E4F2F8", opacity=60, stroke=NONE)
for i, (x, y, w) in enumerate([(240,330,4),(540,300,4),(700,340,4),(380,380,3),(620,410,4),(180,500,4),(820,520,4)]):
    d.shape("ellipse", f"Snow {i+1}", x=x, y=y, width=w, height=w, fill="#FFFFFF", opacity=45, stroke=NONE)

# --- shoulders massed behind the floe, closing on the disc's own arc -------------------
sy = 690
sl, sr = rim_x(sy, side=-1), rim_x(sy, side=1)
d.path(f"M{sl:.1f},{sy} C260,690 310,610 380,580 C420,564 580,564 620,580 "
       f"C690,610 740,690 {sr:.1f},{sy} A{R},{R} 0 0 1 {sl:.1f},{sy} Z",
       "Shoulders", fill=FUR_GRAD, stroke=NONE)
pair(f"M{sl + 14:.1f},{sy - 4} C268,682 316,616 382,586", "Shoulder edge",
     fill=NONE, stroke="#8E97A0", strokeWidth=5, opacity=60, cap="round")
# cool shadow pooling at the chest
d.shape("ellipse", "Chest shade", x=400, y=600, width=200, height=120, fill="#9AA8B4", opacity=25, stroke=NONE)

# --- the ice floe: top edge wavy, bottom closes on the disc's arc -----------------------
fy = 700
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C300,690 400,706 500,698 C610,690 720,704 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Ice floe", fill=ICE_GRAD, stroke=NONE)
# snow lip along the top edge
d.path(f"M{fl + 8:.1f},{fy} C310,691 400,705 500,698 C600,691 710,703 {fr - 8:.1f},{fy}",
       "Floe edge light", fill=NONE, stroke="#FFFFFF", strokeWidth=5, opacity=70, cap="round")
# under-ice shadow band + cracks
d.path("M300,780 C400,760 620,760 720,782 C640,800 400,800 300,780 Z",
       "Under ice", fill="#5E8496", opacity=35, stroke=NONE)
for i, dd in enumerate(["M280,740 L360,760 L420,752", "M590,758 L660,742 L730,750", "M420,820 L500,806 L580,818"]):
    d.path(dd, f"Ice crack {i+1}", fill=NONE, stroke="#5E8496", strokeWidth=3, opacity=50, cap="round")
# aurora reflection on the ice
d.shape("ellipse", "Aurora reflection", x=340, y=716, width=320, height=26,
        fill="#78F0C0", opacity=14, stroke=NONE)

# --- ears: small, rounded, tucked against the crown ---------------------------------------
pair("M362,322 C350,300 322,304 318,330 C314,356 332,372 352,368 "
     "C362,352 364,336 362,322 Z",
     "Ear", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
pair("M348,332 C338,326 328,334 328,348 C328,360 340,366 348,362",
     "Inner ear", fill=NONE, stroke="#C4BBAA", strokeWidth=5, opacity=70, cap="round")

# --- head ---------------------------------------------------------------------------------
HEAD = ("M500,292 C568,292 632,326 662,384 C684,428 684,486 660,534 "
        "C640,574 606,606 564,628 C542,650 522,660 500,660 C478,660 458,650 436,628 "
        "C394,606 360,574 340,534 C316,486 316,428 338,384 "
        "C368,326 432,292 500,292 Z")
d.path(HEAD, "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=7)
# cool shadow on the shaded (right) flank + warm sheen on the crown
d.path("M560,330 C620,360 656,420 654,486 C650,552 610,600 560,628 "
       "C600,584 620,530 616,470 C612,412 592,364 560,330 Z",
       "Flank shade", fill="#A8B4BE", opacity=30, stroke=NONE)
d.shape("ellipse", "Crown sheen", x=420, y=306, width=180, height=64, fill="#FFFFFF", opacity=22, stroke=NONE)
# cheek ruff strokes
pair("M352,470 C338,502 344,540 366,566", "Cheek edge", fill=NONE,
     stroke="#B4AB9A", strokeWidth=5, opacity=60, cap="round")

# --- long muzzle --------------------------------------------------------------------------
d.path("M500,462 C548,462 580,496 588,540 C594,582 578,626 546,648 "
       "C524,660 476,660 454,648 C422,626 406,582 412,540 "
       "C420,496 452,462 500,462 Z",
       "Muzzle", fill=MUZZLE_GRAD, stroke=NONE)
# muzzle bridge light + side shade
d.path("M478,480 C470,520 470,570 478,612", "Bridge shade L", fill=NONE,
       stroke="#C4BBAA", strokeWidth=6, opacity=45, cap="round")
d.path("M524,482 C532,520 532,568 526,610", "Bridge light", fill=NONE,
       stroke="#FFFFFF", strokeWidth=5, opacity=40, cap="round")
# the big black nose
d.path("M500,604 C528,604 548,618 550,636 C552,656 530,668 500,668 "
       "C470,668 448,656 450,636 C452,618 472,604 500,604 Z",
       "Nose", fill=NOSE_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose glint", x=470, y=612, width=22, height=10, fill="#FFFFFF", opacity=30, stroke=NONE)
# nostril marks
pair("M470,632 C474,624 484,620 492,622", "Nostril mark", fill=NONE,
     stroke="#0C0806", strokeWidth=4, opacity=70, cap="round")

# --- the patient eyes: small, warm, heavy-lidded -------------------------------------------
pair("M416,470 C428,458 452,456 466,466 C460,480 434,484 416,470 Z",
     "Eye", fill="#2E2118", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris L", x=434, y=462, width=13, height=13, fill="#4A2E18", stroke=NONE)
d.shape("ellipse", "Iris R", x=553, y=462, width=13, height=13, fill="#4A2E18", stroke=NONE)
d.shape("ellipse", "Glint L", x=437, y=464, width=4, height=4, fill="#FFF8EC", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=556, y=464, width=4, height=4, fill="#FFF8EC", opacity=85, stroke=NONE)
pair("M412,466 C426,452 456,450 472,462", "Upper lid", fill=NONE,
     stroke=INK, strokeWidth=5, cap="round")
pair("M416,484 C432,492 456,492 468,484", "Under eye", fill=NONE,
     stroke="#B4AB9A", strokeWidth=3, opacity=55, cap="round")
# brow suggestion lines
pair("M414,438 C434,428 460,428 478,438", "Brow line", fill=NONE,
     stroke="#C4BBAA", strokeWidth=5, opacity=50, cap="round")

# --- the big forepaws on the floe edge ------------------------------------------------------
pair("M300,724 C292,682 316,652 360,648 C404,644 434,668 436,706 "
     "C438,740 414,762 372,764 C334,766 306,752 300,724 Z",
     "Paw", fill=PAW_GRAD, stroke=INK, strokeWidth=5)
for j, x in enumerate([330, 358, 386]):
    pair(f"M{x},664 C{x - 5},688 {x - 5},712 {x + 2},734", f"Toe {j+1}",
         fill=NONE, stroke="#A89E8C", strokeWidth=4, opacity=65, cap="round")
    pair(f"M{x + 3},742 C{x + 6},748 {x + 8},754 {x + 7},760", f"Claw {j+1}",
         fill=NONE, stroke="#3A342C", strokeWidth=4, opacity=75, cap="round")
pair("M316,668 C334,656 360,652 386,658", "Paw light", fill=NONE,
     stroke="#FFFFFF", strokeWidth=5, opacity=55, cap="round")

# --- name ------------------------------------------------------------------------------------
d.text("POLAR BEAR", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#DCEDF4", justify="center")

d.finish("polar-bear-V1R00")
