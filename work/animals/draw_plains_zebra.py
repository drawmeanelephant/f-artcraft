#!/usr/bin/env python3
"""Plains zebra — field-guide plate V1R00. Face-forward: the long cream head
under an erect striped-mane mohawk, bold black-brown stripes fanning off the
centerline and converging at the soft dark muzzle, big calm eyes, tall ears.
Dry-season plate — dusty sun glow behind the head, an acacia silhouette,
straw tufts, the baked earth closing on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Plains Zebra — Field Plate", 1000, 1000)

INK = "#2E2218"                    # warm dark ink, never pure black
STRIPE = "#2A1E14"
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD = lin(0, 0, 0, 1000, (0, "#1E140C"), (1, "#0A0604"))
PLATE_GRAD = rad((0, "#EAD9A8"), (0.55, "#C8A468"), (1, "#8A6A40"))
COAT_GRAD = rad((0, "#F8F0DC"), (0.6, "#EADCC0"), (1, "#C4B294"))
NECK_GRAD = lin(0, 560, 0, 880, (0, "#EEDFC2"), (1, "#C9B696"))
MUZZLE_GRAD = rad((0, "#6A5040"), (0.7, "#503A2C"), (1, "#32241A"))
EARTH_GRAD = lin(0, 760, 0, 880, (0, "#B08A50"), (1, "#6E4E2C"))

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

# --- backdrop + dust-glow plate ------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#C8A468", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E4426", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F4E8C8", strokeWidth=3, opacity=45)
# dusty sun, low behind where the head will be
d.shape("ellipse", "Dust sun", x=360, y=250, width=280, height=280, fill="#F8ECC8", opacity=30, stroke=NONE)
d.shape("ellipse", "Dust sun core", x=400, y=290, width=200, height=200, fill="#FCF4D8", opacity=30, stroke=NONE)
# heat haze bands
for i, (x, y, w, h, o) in enumerate([(180,300,240,30,14),(580,260,220,26,12),(150,480,280,34,12),(620,470,240,30,11)]):
    d.shape("ellipse", f"Haze {i+1}", x=x, y=y, width=w, height=h, fill="#F4E4B8", opacity=o, stroke=NONE)
# dust motes
for i, (x, y, w) in enumerate([(220,220,5),(340,160,4),(560,150,5),(700,200,4),(810,300,5),
                               (160,420,4),(860,430,4),(300,380,3),(660,350,3),(460,180,3)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Dust mote {i+1}", x=x, y=y, width=w, height=w, fill="#F4E8C0", opacity=40, stroke=NONE)

# small flat-top acacia silhouettes inside the rim
for side, sx in ((-1, 232), (1, 768)):
    d.path(f"M{sx},560 L{sx + side*4},520 L{sx + side*4},498 M{sx + side*4},516 "
           f"L{sx + side*22},492 M{sx + side*4},522 L{sx - side*16},500",
           f"Acacia trunk {'L' if side < 0 else 'R'}", fill=NONE, stroke="#4A3620",
           strokeWidth=5, opacity=55, cap="round")
    d.shape("ellipse", f"Acacia crown {'L' if side < 0 else 'R'}",
            x=sx - 52, y=470, width=104, height=24, fill="#4A3620", opacity=50, stroke=NONE)

# --- baked earth floor, closing on the disc's own arc -----------------------------------
fy = 756
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C330,744 430,762 500,754 C580,746 680,748 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Dry earth", fill=EARTH_GRAD, stroke=NONE)
for i, dd in enumerate(["M280,790 L340,804 L400,796", "M580,800 L660,786 L730,794", "M420,840 L490,830 L560,842"]):
    d.path(dd, f"Earth crack {i+1}", fill=NONE, stroke="#5E4226", strokeWidth=3, opacity=45, cap="round")
# straw tufts
for i, (x, y, s) in enumerate([(216, 766, 1), (262, 780, -1), (330, 770, 1), (700, 776, -1),
                               (764, 764, 1), (640, 786, -1), (460, 772, 1), (560, 770, -1)]):
    for j, (dx, dy) in enumerate([(-8, -26), (0, -34), (8, -24)]):
        tx = x + dx + s * j * 3
        d.path(f"M{x},{y} Q{x + dx*0.5},{y + dy*0.6} {tx},{y + dy}",
               f"Straw {i+1}.{j+1}", fill=NONE, stroke="#C8B06A", strokeWidth=3.5, opacity=65, cap="round")

# --- neck + chest, closing on the disc's own arc ------------------------------------------
ny = 700
nl, nr = rim_x(ny, side=-1), rim_x(ny, side=1)
d.path(f"M{nl:.1f},{ny} C300,690 340,610 386,560 C400,546 600,546 614,560 "
       f"C660,610 700,690 {nr:.1f},{ny} A{R},{R} 0 0 1 {nl:.1f},{ny} Z",
       "Neck", fill=NECK_GRAD, stroke=NONE)
pair(f"M{nl + 14:.1f},{ny - 4} C306,684 346,612 388,564", "Neck edge",
     fill=NONE, stroke=INK, strokeWidth=6, cap="round")
# bold chest bands — the plains zebra's throat chevrons
for i, (dd_, w_) in enumerate([
        ("M330,640 C400,668 600,668 670,640", 17),
        ("M296,700 C380,730 620,730 704,700", 18),
        ("M270,764 C370,796 630,796 730,764", 18),
        ("M330,828 C420,854 580,854 670,828", 16)]):
    d.path(dd_, f"Chest stripe {i+1}", fill=NONE, stroke=STRIPE,
           strokeWidth=w_, opacity=88, cap="round")
# shoulder edge stripes turning down
pair("M348,600 C330,644 322,690 326,734", "Shoulder stripe", fill=NONE,
     stroke=STRIPE, strokeWidth=12, opacity=80, cap="round")

# --- the erect striped mane: alternating tuft spikes along the crown ridge ----------------
for k, (bx, tx, ty) in enumerate([(438, 398, 246), (458, 424, 226), (478, 452, 214),
                                  (500, 486, 208), (522, 524, 212), (542, 558, 224),
                                  (560, 590, 244)]):
    by = 300 + abs(k - 3) * 4
    mx, my = (bx + tx) / 2, (by + ty) / 2
    nx, ny = -(ty - by), tx - bx
    ln = math.hypot(nx, ny) or 1
    nx, ny = nx / ln * 8, ny / ln * 8
    d.path(f"M{bx - 9},{by} Q{mx + nx:.0f},{my + ny:.0f} {tx},{ty} "
           f"Q{mx - nx:.0f},{my - ny:.0f} {bx + 9},{by} Z",
           f"Mane tuft {k+1}", fill=STRIPE if k % 2 == 0 else "#EADCC0",
           stroke=INK, strokeWidth=2.5)

# --- ears: tall, pointed, tipping outward --------------------------------------------------
pair("M372,368 C346,338 336,292 348,252 C356,224 382,208 406,218 "
     "C426,227 432,258 424,292 C416,326 398,354 372,368 Z",
     "Ear", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
pair("M376,348 C360,324 354,292 362,264 C368,244 386,234 400,242 "
     "C412,250 414,272 408,296 C402,318 392,336 376,348 Z",
     "Inner ear", fill="#C9B696", opacity=80, stroke=NONE)
pair("M352,262 C358,240 374,226 394,226", "Ear rim light", fill=NONE,
     stroke="#F8F0DC", strokeWidth=4, opacity=60, cap="round")
# dark ear-tip bands
pair("M350,270 C354,246 366,230 384,222 C380,244 368,260 350,270 Z",
     "Ear tip", fill=STRIPE, opacity=85, stroke=NONE)

# --- head: the long cream wedge -------------------------------------------------------------
HEAD = ("M500,290 C556,290 606,318 632,364 C654,404 660,456 646,506 "
        "C638,540 622,576 596,606 C578,632 556,660 540,684 "
        "C530,700 470,700 460,684 C444,660 422,632 404,606 "
        "C378,576 362,540 354,506 C340,456 346,404 368,364 "
        "C394,318 444,290 500,290 Z")
d.path(HEAD, "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=7)

# --- the barcode: stripes fanning off the centerline -----------------------------------------
# forehead fan, sweeping outward-down from staggered origins along the centerline
for i, dd in enumerate([
        "M494,318 C472,332 452,352 438,378",
        "M486,334 C456,352 430,380 414,414",
        "M476,352 C442,378 416,412 404,456",
        "M464,372 C434,402 412,442 402,492"]):
    d.path(dd, f"Forehead stripe {i+1}", fill=NONE, stroke=STRIPE,
           strokeWidth=9 - i, opacity=85, cap="round")
    d.path(mirror(dd), f"Forehead stripe {i+1} R", fill=NONE, stroke=STRIPE,
           strokeWidth=9 - i, opacity=85, cap="round")
# cheek sweeps under the eyes, converging toward the muzzle
for i, dd in enumerate([
        "M404,486 C420,514 442,534 468,546",
        "M398,532 C418,560 444,578 472,586",
        "M412,572 C432,596 456,612 482,618"]):
    d.path(dd, f"Cheek stripe {i+1}", fill=NONE, stroke=STRIPE,
           strokeWidth=8 - i, opacity=85, cap="round")
    d.path(mirror(dd), f"Cheek stripe {i+1} R", fill=NONE, stroke=STRIPE,
           strokeWidth=8 - i, opacity=85, cap="round")
# short bridge bars between the eyes
d.path("M500,330 C502,360 502,390 500,418", "Bridge stripe", fill=NONE,
       stroke=STRIPE, strokeWidth=7, opacity=80, cap="round")

# --- soft modelling under the stripes --------------------------------------------------------
d.shape("ellipse", "Crown sheen", x=440, y=308, width=140, height=56, fill="#FFFFFF", opacity=20, stroke=NONE)
pair("M362,470 C352,504 358,540 378,568", "Jaw edge light", fill=NONE,
     stroke="#F8F0DC", strokeWidth=4, opacity=35, cap="round")

# --- eyes: big, calm, long-lidded -------------------------------------------------------------
pair("M400,470 C414,452 444,448 462,460 C454,480 420,486 400,470 Z",
     "Eye", fill="#2A1C12", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Iris L", x=424, y=458, width=15, height=15, fill="#4A2E18", stroke=NONE)
d.shape("ellipse", "Iris R", x=561, y=458, width=15, height=15, fill="#4A2E18", stroke=NONE)
d.shape("ellipse", "Glint L", x=428, y=460, width=5, height=5, fill="#FFF4E0", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=565, y=460, width=5, height=5, fill="#FFF4E0", opacity=85, stroke=NONE)
pair("M396,466 C412,448 446,444 466,458", "Upper lid", fill=NONE,
     stroke=INK, strokeWidth=6, cap="round")
pair("M394,458 C388,452 384,446 382,438 M398,452 C394,446 391,440 390,434",
     "Lash", fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
pair("M404,484 C422,494 448,492 462,482", "Under eye", fill=NONE,
     stroke="#B4A284", strokeWidth=3, opacity=55, cap="round")

# --- the soft dark muzzle ----------------------------------------------------------------------
d.path("M500,560 C534,560 558,584 564,618 C570,650 556,682 528,694 "
       "C514,700 486,700 472,694 C444,682 430,650 436,618 "
       "C442,584 466,560 500,560 Z",
       "Muzzle", fill=MUZZLE_GRAD, stroke=NONE)
d.shape("ellipse", "Muzzle sheen", x=462, y=580, width=76, height=40, fill="#8A6E58", opacity=35, stroke=NONE)
# nostril commas
pair("M452,628 C448,612 462,600 478,604 C490,608 494,622 488,634 "
     "C480,646 460,644 454,634 C452,632 452,630 452,628 Z",
     "Nostril", fill="#140C08", stroke=INK, strokeWidth=3)
d.path("M500,668 C498,678 496,686 492,692 M500,668 C502,678 504,686 508,692",
       "Mouth", fill=NONE, stroke="#140C08", strokeWidth=4, opacity=70, cap="round")
# muzzle rim
d.path("M440,634 C434,660 444,682 466,693", "Muzzle edge L", fill=NONE,
       stroke="#1C120C", strokeWidth=4, opacity=55, cap="round")

# --- name ------------------------------------------------------------------------------------
d.text("PLAINS ZEBRA", "Name", x=500, y=962, size=56, font="Virelai Sans",
       color="#F4E8C8", justify="center")

d.finish("plains-zebra-V1R00")
