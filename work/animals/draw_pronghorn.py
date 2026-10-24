#!/usr/bin/env python3
"""Pronghorn — field-guide plate V1R00. Head-and-shoulders profile facing
right: the pronged horns (a forward tine on each beam — built by the ghosts
of cheetahs), tan neck with the two white throat bands, black jaw wedge.
Sage-steppe plate, big horizon: pale gold sky, a mesa on the skyline, a
distant herd-mate, sagebrush on a floor that closes on the disc arc.
1000x1000. House style: gradients + translucent shading, never flat.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Pronghorn — Field Plate", 1000, 1000)

INK = "#241606"
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def ribbon(p0, p1, p2, w0, w1, label, fill, samples=18, **kw):
    """Tapered filled stroke along a quadratic — horns, neck bands."""
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

BG_GRAD = lin(0, 0, 0, 1000, (0, "#171108"), (1, "#060402"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#CBC49A"), (0.42, "#B0AE8C"),
                 (0.72, "#C2A878"), (1, "#8A7448"))
TAN_GRAD = lin(500, 380, 640, 840, (0, "#C99B5C"), (0.55, "#A87C44"), (1, "#6E4C26"))
HEAD_GRAD = rad((0, "#D8B078"), (0.65, "#B8905A"), (1, "#8A6438"))
HORN_GRAD = lin(560, 330, 520, 190, (0, "#3E3226"), (1, "#171210"))
CHARCOAL = "#241C14"
WHITE = rad((0, "#F4ECD8"), (1, "#D8CCAC"))
SAGE = "#6E7A58"
SAGE_DK = "#4E5A3E"

# --- backdrop + sage-steppe plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#B0AE8C", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E5232", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8E2C0", strokeWidth=3, opacity=40)
# horizon glow — the big sky pooling light where the steppe begins
d.shape("ellipse", "Horizon glow", x=230, y=540, width=540, height=220,
        fill="#F0DCB0", opacity=25, stroke=NONE)
# thin cloud bands high in the sky
for i, (x0, x1, y) in enumerate([(180, 420, 210), (560, 778, 172), (300, 560, 270)]):
    d.path(f"M{x0},{y} C{(x0+x1)/2},{y-10} {(x0+x1)/2},{y+10} {x1},{y}",
           f"Cloud {i+1}", fill=NONE, stroke="#E4DCB8", strokeWidth=10,
           opacity=18, cap="round")

# mesa silhouette on the skyline, left of the subject
d.path("M168,648 L186,592 C220,584 286,582 340,588 L362,648 Z",
       "Mesa", fill="#8A7A52", opacity=38, stroke=NONE)
d.path("M182,596 C220,588 286,586 336,592", "Mesa cap",
       fill=NONE, stroke="#5E5030", strokeWidth=5, opacity=40, cap="round")

# --- steppe floor: long flat crest ~y660 for the horizon, closes on the arc -------
fy = 664
fdx = math.sqrt(R * R - (fy - CY) ** 2)
d.path(f"M{CX-fdx:.1f},{fy} C360,652 460,662 560,656 C650,652 720,658 {CX+fdx:.1f},{fy} "
       f"A{R},{R} 0 0 1 {CX-fdx:.1f},{fy} Z",
       "Floor", fill=lin(0, fy, 0, 880, (0, "#7A6C44"), (1, "#3A2E18")), stroke=NONE)
d.path(f"M{CX-fdx+8:.1f},{fy-2} C360,650 460,658 560,652 C650,648 720,654 {CX+fdx-8:.1f},{fy-2}",
       "Horizon line", fill=NONE, stroke="#E8DCAC", strokeWidth=4,
       opacity=45, cap="round")

# a herd-mate far out on the horizon — tiny alert profile on the skyline
d.path("M296,622 C296,614 302,608 310,607 L314,594 L318,596 L315,606 "
       "C326,606 336,612 338,622 C340,630 336,638 328,641 "
       "L306,641 C299,636 296,629 296,622 Z",
       "Herd-mate body", fill="#4E4028", opacity=85, stroke=NONE)
d.path("M306,641 L306,662 M326,641 L326,662", "Herd-mate legs",
       fill=NONE, stroke="#4E4028", strokeWidth=3.5, opacity=85, cap="round")

# --- sagebrush tufts --------------------------------------------------------------
def sage(x, y, s, label):
    """Gray-green sagebrush: a spray of short stems + clustered blobs."""
    for j, (dx, dy) in enumerate([(-14,-30),(0,-38),(14,-28),(-7,-16),(8,-18)]):
        d.path(f"M{x},{y} C{x+dx*s*0.4},{y+dy*s*0.5} {x+dx*s*0.8},{y+dy*s*0.8} {x+dx*s},{y+dy*s}",
               f"{label} stem {j+1}", fill=NONE, stroke=SAGE_DK,
               strokeWidth=3, opacity=70, cap="round")
    for j, (dx, dy, w) in enumerate([(-14,-32,22),(0,-40,26),(15,-30,20),(-6,-18,18),(9,-20,16)]):
        d.shape("ellipse", f"{label} puff {j+1}", x=x+dx*s-w*s/2, y=y+dy*s-w*s*0.35,
                width=w*s, height=w*s*0.7, fill=SAGE, opacity=75, stroke=NONE)

sage(216, 716, 1.0, "Sage L")
sage(792, 706, 0.85, "Sage R")
sage(330, 760, 0.7, "Sage M")

# --- far horn + ear first: bases hide behind the skull ------------------------------
ribbon((544,330), (512,236), (492,192), 13, 4, "Horn far",
       lin(544, 330, 492, 192, (0, "#332A20"), (1, "#141010")), stroke=NONE)
ribbon((524,262), (540,246), (556,240), 8, 2.5, "Prong far",
       lin(524, 262, 556, 240, (0, "#2E2620"), (1, "#121010")), stroke=NONE)
# ear: pointed leaf below the horn base
d.path("M520,392 C496,382 470,384 452,398 C460,412 480,420 500,416 "
       "C510,410 516,402 520,392 Z",
       "Ear", fill=lin(500, 382, 470, 418, (0, "#B8905C"), (1, "#8A6438")),
       stroke=INK, strokeWidth=4)
d.path("M508,394 C490,388 474,390 462,398", "Ear shade", fill=NONE,
       stroke="#5E4226", strokeWidth=4, opacity=50, cap="round")

# --- neck + shoulder: one mass closing on the disc's own arc -------------------------
ny = 810
ndx = math.sqrt(R * R - (ny - CY) ** 2)
nxl, nxr = CX - ndx, CX + ndx
NECK = (f"M556,440 C596,486 624,548 640,612 C652,660 670,708 692,748 "
        f"C708,776 720,792 {nxr:.1f},{ny} A420,420 0 0 1 {nxl:.1f},{ny} "
        f"C322,782 380,734 424,680 C450,648 462,612 466,572 "
        f"C468,524 472,474 482,428 C496,412 530,418 556,440 Z")
d.path(NECK, "Neck and shoulder", fill=TAN_GRAD, stroke=INK, strokeWidth=6)
# shading: throat shadow, nape light
d.path("M570,456 C604,500 628,556 642,612", "Throat shade", fill=NONE,
       stroke="#5E4226", strokeWidth=14, opacity=28, cap="round")
d.path("M456,602 C460,558 466,510 478,466", "Nape light", fill=NONE,
       stroke="#EED2A0", strokeWidth=10, opacity=32, cap="round")
# the two white throat bands — the species code on the neck
ribbon((478,540), (560,560), (634,600), 26, 18, "Throat band 1",
       WHITE, opacity=92, stroke=NONE)
ribbon((472,600), (560,624), (646,676), 22, 16, "Throat band 2",
       WHITE, opacity=88, stroke=NONE)
# white chest wash under the bands
d.path("M600,660 C632,700 662,742 692,780 C704,796 712,806 716,812 "
        "C690,806 660,788 640,760 C620,730 606,696 600,660 Z",
       "Chest wash", fill="#E8DCC0", opacity=35, stroke=NONE)

# --- head: tan, pronged horns ---------------------------------------------------------
HEAD = ("M500,318 C534,320 566,334 596,350 C622,362 640,378 650,394 "
        "C654,402 648,410 638,414 C616,422 588,428 564,434 "
        "C544,438 522,440 504,436 C486,430 476,414 474,396 "
        "C472,368 480,336 500,318 Z")
d.path(HEAD, "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=6)
d.path("M514,332 C548,338 580,352 608,370", "Forehead light", fill=NONE,
       stroke="#F4DCA8", strokeWidth=8, opacity=40, cap="round")

# near horn: a thick beam that hooks back at the tip; the forward prong
# juts off the front edge mid-beam — the feature that names the animal
ribbon((572,332), (554,220), (526,180), 18, 5, "Horn near",
       HORN_GRAD, stroke=NONE)
d.path("M526,180 C518,172 510,170 504,174 C512,182 518,186 524,190 Z",
       "Horn hook", fill=HORN_GRAD, stroke=NONE)
ribbon((556,262), (578,244), (602,236), 11, 3, "Prong near",
       HORN_GRAD, stroke=NONE)
# horn sheen along the leading edge
d.path("M564,318 C556,278 548,238 540,204", "Horn sheen", fill=NONE,
       stroke="#8A7660", strokeWidth=3, opacity=40, cap="round")

# markings: black nose tip, dark eye, the black jaw wedge under the ear line
d.path("M622,372 C638,380 649,390 652,400 C648,410 636,416 620,418 "
       "C614,406 614,388 622,372 Z",
       "Nose wedge", fill=CHARCOAL, stroke=NONE)
d.shape("ellipse", "Nostril", x=632, y=394, width=9, height=6,
        fill="#080604", stroke=NONE)
# eye: calm dark amber, set mid-head
d.path("M530,384 C542,374 560,374 570,384 C560,394 542,394 530,384 Z",
       "Eye", fill=rad((0, "#5E3E1E"), (0.7, "#2A1A0C"), (1, "#120A04")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Glint", x=546, y=380, width=5, height=5,
        fill="#FFFFFF", opacity=80, stroke=NONE)
d.path("M528,380 C540,370 560,368 574,378", "Lid",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# jaw wedge: the buck's black cheek patch — a bold wedge from under the ear
# down along the jaw to the chin
d.path("M488,414 C516,422 548,426 578,424 C594,422 608,418 620,410 "
       "C616,428 600,442 576,448 C548,454 516,450 496,438 "
       "C486,430 482,420 488,414 Z",
       "Jaw wedge", fill=CHARCOAL, opacity=92, stroke=NONE)
# chin edging
d.path("M560,436 C580,432 600,426 616,418", "Chin edge", fill=NONE,
       stroke="#1E1610", strokeWidth=4, opacity=70, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#120C04", strokeWidth=6)

# --- name ----------------------------------------------------------------------
d.text("PRONGHORN", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E8DEB4", justify="center")

d.finish("pronghorn-V1R00")
