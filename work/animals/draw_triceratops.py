#!/usr/bin/env python3
"""Triceratops — field-guide plate V1R00. Full profile facing left: the great
scalloped frill, two brow horns sweeping forward over a hooked beak, the
little nose horn, column legs planted on a mud floodplain. Overhead the end
of the era arrives as a thin ember streak and a drift of ash. Floodplain
plate, end-of-era mood. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Triceratops — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#241A0C"                    # warm dark ink, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

def cubic(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

def ribbon_pts(p0, p1, p2, p3, w0, w1, n=20):
    L, Rr = [], []
    for k in range(n + 1):
        t = k / n
        x, y = cubic(p0, p1, p2, p3, t)
        x0, y0 = cubic(p0, p1, p2, p3, max(0, t - 0.01))
        x1, y1 = cubic(p0, p1, p2, p3, min(1, t + 0.01))
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x - dy/ln * w, y + dx/ln * w))
        Rr.append((x + dy/ln * w, y - dx/ln * w))
    return L, Rr

def ribbon(p0, p1, p2, p3, w0, w1, label, n=20, **kw):
    L, Rr = ribbon_pts(p0, p1, p2, p3, w0, w1, n)
    s = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    s += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    return d.path(s, label, **kw)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#191410"), (1, "#0A0705"))
PLATE_GRAD = rad((0, "#CCC9A4"), (0.6, "#8E8C68"), (1, "#4C4E38"))
FLOOR_GRAD = lin(0, 700, 0, 880, (0, "#7E7250"), (0.6, "#4E4228"), (1, "#241C0E"))
HIDE_GRAD = rad((0, "#8F7D54"), (0.55, "#6A5A3A"), (1, "#3B3119"))
HIDE_DARK = "#3A3018"
IVORY = lin(0, 240, 0, 380, (0, "#F2E8CE"), (1, "#C4A878"))
FRILL_SHEEN = "#A89468"

# --- backdrop + floodplain plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876,
        fill="#8E8C68", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E4228", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8E4CC", strokeWidth=3, opacity=45)

# high smoke haze bands
for i, dd in enumerate(["M180,210 C330,194 540,196 700,214",
                        "M240,286 C380,272 560,274 720,290"]):
    d.path(dd, f"Haze {i+1}", fill=NONE, stroke="#D8D2B4",
           strokeWidth=6, opacity=14, cap="round")

# --- the bolide: the era ending in the upper left --------------------------------
# smoke trail, a tapering curved sliver drifting down-left
d.path("M392,84 C344,108 300,142 248,194 C266,196 296,172 326,146 "
       "C354,122 380,100 392,84 Z", "Bolide trail", fill="#E0D2B0",
       opacity=32, stroke=NONE)
d.path("M378,92 C340,114 306,142 268,182", "Trail core", fill=NONE,
       stroke="#F2E4C0", strokeWidth=5, opacity=45, cap="round")
# head glow + core
d.shape("ellipse", "Bolide glow", x=196, y=160, width=116, height=88,
        fill=rad((0, "#F6ECD4", 60), (1, "#E8C088", 0)), stroke=NONE)
d.shape("ellipse", "Bolide head", x=218, y=176, width=52, height=40,
        fill="#F6ECD4", opacity=85, stroke=NONE)
d.shape("ellipse", "Bolide core", x=232, y=186, width=24, height=18,
        fill="#FFFDF4", opacity=95, stroke=NONE)

# ash motes drifting down through the sky
for i, (x, y, w) in enumerate([
        (300, 300, 6), (420, 250, 5), (540, 300, 7), (660, 240, 5),
        (760, 320, 6), (240, 380, 5), (360, 400, 7), (500, 360, 5),
        (640, 410, 6), (780, 430, 5), (450, 170, 5), (700, 160, 6)]):
    d.shape("ellipse", f"Ash {i+1}", x=x, y=y, width=w, height=w*0.8,
            fill="#E8DCC2", opacity=35, stroke=NONE)

# --- floodplain floor, closing on the disc's own arc ------------------------------
fy = 714
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C320,702 420,718 540,710 C660,702 760,706 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Mud floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl+6:.0f},{fy} C320,702 420,718 540,710 C660,702 760,706 {fr-6:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#A8A074", strokeWidth=5, opacity=40, cap="round")
# low dark ridge of the far shore
d.path("M186,700 C320,688 430,694 560,690 C680,686 780,692 830,700",
       "Far shore", fill=NONE, stroke="#3E3A26", strokeWidth=7, opacity=45, cap="round")
# ember light crawling along the horizon
d.shape("ellipse", "Horizon ember", x=280, y=684, width=440, height=22,
        fill="#C4683A", opacity=16, stroke=NONE)
# standing pool reflecting the pale sky
d.shape("ellipse", "Pool", x=280, y=738, width=230, height=18,
        fill="#B8B094", opacity=30, stroke=NONE)
d.shape("ellipse", "Pool sheen", x=310, y=742, width=150, height=8,
        fill="#E4DEC4", opacity=30, stroke=NONE)
# mud clumps
for i, (x, y, w) in enumerate([(600,742,14),(700,756,10),(240,760,12),(760,738,9),(480,772,8)]):
    d.shape("ellipse", f"Clod {i+1}", x=x, y=y, width=w, height=w*0.6,
            fill="#33291A", opacity=50, stroke=NONE)

# horsetail reeds at the floor edges — thin geometry needs >=3.5pt
for i, (x, top, lean) in enumerate([(192, 620, -4), (220, 646, 3), (246, 632, -2),
                                    (786, 636, 4), (814, 610, -3)]):
    d.path(f"M{x},{fy-2} C{x+lean},{fy-40} {x+lean},{top+30} {x+lean*2},{top}",
           f"Reed {i+1}", fill=NONE, stroke="#4E5A34", strokeWidth=5,
           opacity=80, cap="round")
    d.path(f"M{x+lean*2-6},{top} L{x+lean*2+6},{top} L{x+lean*2},{top-18} Z",
           f"Reed cone {i+1}", fill="#5E6C3E", opacity=85, stroke=NONE)
    for j in range(2):
        ry = top + 24 + j * 26
        d.path(f"M{x+lean-5},{ry} L{x+lean+5},{ry-1}", f"Reed joint {i+1}-{j+1}",
               fill=NONE, stroke="#77854A", strokeWidth=3, opacity=60, cap="round")

# contact shadow — wide and low under the whole animal
d.shape("ellipse", "Contact shadow", x=380, y=698, width=400, height=20,
        fill="#14180C", opacity=45, stroke=NONE)

# === the animal =====================================================================
# --- tail: short and thick, tapering right --------------------------------------------
ribbon((768, 452), (820, 448), (862, 458), (886, 478), 54, 6,
       "Tail", fill=lin(768, 446, 886, 480, (0, "#6A5A3A"), (0.7, "#54452A"), (1, "#3B3119")),
       stroke=INK, strokeWidth=5)

# --- far legs: a half-pace behind, darker ---------------------------------------------
d.path("M556,548 C550,584 548,622 554,656 C558,680 556,700 552,710 "
       "C556,718 570,720 578,714 C582,706 582,696 580,688 "
       "C578,662 580,636 586,610 C592,582 592,560 586,546 "
       "C574,538 564,540 556,548 Z",
       "Front leg far", fill=HIDE_DARK, stroke=INK, strokeWidth=4)
d.path("M640,560 C632,594 632,630 640,660 C644,682 644,700 640,710 "
       "C644,718 658,720 666,714 C670,706 670,696 668,688 "
       "C666,660 668,634 676,608 C682,582 682,562 674,550 "
       "C662,542 648,546 640,560 Z",
       "Rear leg far", fill=HIDE_DARK, stroke=INK, strokeWidth=4)

# --- torso: the broad barrel, shoulder rising to the hip -------------------------------
d.path("M424,452 C460,412 534,390 616,394 C680,398 738,416 770,448 "
       "C788,468 794,494 788,518 C780,550 754,572 720,586 "
       "C656,610 556,612 494,598 C450,588 424,564 414,532 "
       "C406,506 410,476 424,452 Z",
       "Torso", fill=HIDE_GRAD, stroke=INK, strokeWidth=6)
# dorsal shade along the spine
d.path("M448,430 C500,404 580,394 660,402 C700,406 734,418 756,438 "
       "C720,424 640,414 560,416 C512,418 472,424 448,430 Z",
       "Dorsal shade", fill="#241A0C", opacity=28, stroke=NONE)
# belly light on the underside
d.path("M440,548 C500,580 620,588 706,568 C660,596 540,602 480,584 "
       "C456,576 442,562 440,548 Z", "Belly light",
       fill="#B0A074", opacity=40, stroke=NONE)
# shoulder and hip creases
d.path("M470,470 C458,506 458,548 472,580", "Shoulder crease", fill=NONE,
       stroke="#241A0C", strokeWidth=5, opacity=35, cap="round")
d.path("M712,470 C726,502 728,540 716,570", "Hip crease", fill=NONE,
       stroke="#241A0C", strokeWidth=5, opacity=35, cap="round")
# flank mottle — dry skin flecks
for i, (x, y, w) in enumerate([
        (500, 460, 22), (560, 480, 18), (620, 458, 20), (680, 478, 16),
        (530, 516, 14), (590, 530, 16), (650, 520, 14), (470, 500, 12)]):
    d.shape("ellipse", f"Flank fleck {i+1}", x=x, y=y, width=w, height=w*0.55,
            fill="#3B3119", opacity=25, stroke=NONE)

# --- neck mass under the frill, bridging head to chest ------------------------------------
d.path("M304,414 C340,424 380,444 410,470 C430,488 442,514 446,540 "
       "C448,556 436,566 420,562 C390,554 356,534 336,506 "
       "C316,478 304,448 304,414 Z",
       "Neck", fill=HIDE_GRAD, stroke=NONE)
d.path("M322,470 C352,494 396,516 436,524", "Neck fold", fill=NONE,
       stroke="#241A0C", strokeWidth=5, opacity=35, cap="round")

# --- near legs: columns planted on the mud ----------------------------------------------
d.path("M474,548 C468,584 466,624 472,660 C475,682 474,700 470,712 "
       "C474,722 490,726 502,720 C508,714 510,706 508,698 "
       "C506,672 508,646 514,620 C520,590 522,564 516,544 "
       "C502,534 484,536 474,548 Z",
       "Front leg near", fill=HIDE_GRAD, stroke=INK, strokeWidth=5)
d.path("M470,700 C468,710 470,718 478,722 L506,722 C512,718 512,708 506,702 "
       "C494,706 480,706 470,700 Z", "Front hoof", fill="#4A3E22",
       stroke=INK, strokeWidth=4)
for i, xx in enumerate([482, 494]):
    d.path(f"M{xx},706 L{xx-1},720", f"Front toe {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3, opacity=60, cap="round")
d.path("M690,556 C680,592 678,632 686,664 C690,688 689,706 685,716 "
       "C691,724 711,726 721,718 C725,710 725,700 721,692 "
       "C719,664 721,636 729,610 C737,584 737,560 729,544 "
       "C715,536 698,540 690,556 Z",
       "Rear leg near", fill=HIDE_GRAD, stroke=INK, strokeWidth=5)
d.path("M685,704 C683,712 686,720 694,723 L720,723 C726,719 726,710 720,704 "
       "C708,708 695,708 685,704 Z", "Rear hoof", fill="#4A3E22",
       stroke=INK, strokeWidth=4)
for i, xx in enumerate([697, 709]):
    d.path(f"M{xx},708 L{xx-1},721", f"Rear toe {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3, opacity=60, cap="round")

# --- the frill: a scalloped shield rising behind the skull ------------------------------
d.path("M330,430 C336,344 368,272 424,240 C452,226 478,232 486,256 "
       "C492,278 486,308 472,334 C458,364 436,392 410,412 "
       "C384,430 356,438 336,436 C330,434 328,432 330,430 Z",
       "Frill", fill=rad((0, "#9A8A5E"), (0.6, "#76663E"), (1, "#4A3E20")),
       stroke=INK, strokeWidth=6)
# epoccipital scallops riding the rim
for i, (x, y) in enumerate([(430,238), (458,232), (480,246), (486,274),
                            (480,302), (466,330), (446,356)]):
    d.shape("ellipse", f"Epoccipital {i+1}", x=x-9, y=y-9, width=18, height=18,
            fill=FRILL_SHEEN, stroke=INK, strokeWidth=3.5)
# pale sheen inside the shield
d.path("M352,400 C362,336 392,286 436,258 C420,300 396,356 380,404 "
       "C370,410 358,408 352,400 Z", "Frill sheen",
       fill="#B8A87A", opacity=40, stroke=NONE)
# two radial grooves of the frill
d.path("M352,392 C372,332 402,284 440,254", "Frill groove 1", fill=NONE,
       stroke="#4A3E20", strokeWidth=4, opacity=50, cap="round")
d.path("M382,412 C408,352 442,306 476,276", "Frill groove 2", fill=NONE,
       stroke="#4A3E20", strokeWidth=4, opacity=45, cap="round")

# --- far brow horn: behind the skull, darker --------------------------------------------
ribbon((366,336), (330,296), (292,256), (268,230), 20, 3,
       "Brow horn far", fill="#A8905E", stroke=INK, strokeWidth=3.5)

# --- head: deep face running forward to the hooked beak ---------------------------------
d.path("M336,364 C314,344 284,340 262,354 C244,366 232,384 228,404 "
       "C224,422 228,438 240,446 C254,454 274,454 290,446 "
       "C310,436 326,416 332,392 C334,380 336,372 336,364 Z",
       "Head", fill=lin(336, 352, 228, 442, (0, "#8F7D54"), (0.6, "#6A5A3A"), (1, "#4A3E22")),
       stroke=INK, strokeWidth=5)
# hooked keratin beak
d.path("M228,414 C220,426 220,440 230,448 C238,454 250,450 254,440 "
       "C256,432 252,422 244,418 C238,414 232,412 228,414 Z",
       "Beak", fill="#D8CBA8", stroke=INK, strokeWidth=4)
# mouth line under the jaw
d.path("M242,444 C264,452 294,448 316,434", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=80, cap="round")
# jaw shade
d.path("M268,444 C290,442 314,430 328,412", "Jaw shade", fill=NONE,
       stroke="#241A0C", strokeWidth=5, opacity=35, cap="round")
# nostril + eye under the brow
d.shape("ellipse", "Nostril", x=238, y=420, width=13, height=9,
        fill="#241A0C", opacity=75, stroke=NONE)
d.shape("ellipse", "Eye socket", x=290, y=388, width=30, height=24,
        fill="#241A0C", opacity=40, stroke=NONE)
d.shape("ellipse", "Eye", x=298, y=392, width=15, height=14,
        fill="#140E06", stroke=NONE)
d.shape("ellipse", "Eye glint", x=302, y=395, width=4.5, height=4.5,
        fill="#FFEDC8", opacity=85, stroke=NONE)

# --- the horns ---------------------------------------------------------------------------
# near brow horn sweeping forward and up — the species tell
ribbon((336,346), (286,310), (240,280), (212,246), 28, 3,
       "Brow horn near", fill=IVORY, stroke=INK, strokeWidth=4.5)
# little nose horn on the bridge
d.path("M222,396 C218,372 224,350 240,338 C254,350 260,374 254,396 "
       "C244,404 230,404 222,396 Z", "Nose horn",
       fill=IVORY, stroke=INK, strokeWidth=4)

# a few ash motes settling on the animal itself
for i, (x, y, w) in enumerate([(520, 430, 5), (640, 452, 6), (450, 480, 4)]):
    d.shape("ellipse", f"Settled ash {i+1}", x=x, y=y, width=w, height=w*0.8,
            fill="#E8DCC2", opacity=45, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#33361E", strokeWidth=6)

# --- name ---------------------------------------------------------------------------------
d.text("TRICERATOPS", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#E3DFC0", justify="center")

d.finish("triceratops-V1R00")
