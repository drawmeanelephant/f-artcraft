#!/usr/bin/env python3
"""Sun bear — field-guide plate V1R00. Bust portrait, face forward: near-black
warm fur, tan muzzle, furrowed brow, and the cream crescent chest mark as the
signature. Golden sun-plate with soft rays. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Sun Bear — Field Plate", 1000, 1000)

INK = "#140F0C"
CX, CY, R = 500, 460, 420          # plate disc
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E2116"}, {"offset": 1, "color": "#0E0906"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F8E8BE"}, {"offset": 0.7, "color": "#E4C686"},
    {"offset": 1, "color": "#B99550"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#463B35"}, {"offset": 0.65, "color": "#271F1B"},
    {"offset": 1, "color": "#130F0D"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E2520"}, {"offset": 1, "color": "#110D0B"}]}}
MUZZLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#EDCD98"}, {"offset": 0.65, "color": "#CC9D62"},
    {"offset": 1, "color": "#9A6C3B"}]}}
CRESCENT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FCEFCF"}, {"offset": 0.6, "color": "#EED29A"},
    {"offset": 1, "color": "#CFA764"}]}}
NOSE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A403C"}, {"offset": 1, "color": "#0F0B0A"}]}}
EAR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A302B"}, {"offset": 1, "color": "#16110F"}]}}

def chord_x(y, r):
    h = math.sqrt(r*r - (y - CY)**2)
    return CX - h, CX + h

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6A34", strokeWidth=6)
# sun rays behind the head: centre 70pt above the disc centre, so a 320pt
# ray stays inside the inner ring (70 + 320 < 396)
RX, RY, RL = 500, 390, 320
for i in range(12):
    a0 = math.radians(i*30 + 4); a1 = math.radians(i*30 + 17)
    p0 = (RX + RL*math.cos(a0), RY + RL*math.sin(a0))
    p1 = (RX + RL*math.cos(a1), RY + RL*math.sin(a1))
    d.path(f"M{RX},{RY} L{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f} Z",
           f"Sun ray {i+1}", fill="#FFF6DA", opacity=16, stroke=NONE)
d.shape("ellipse", "Halo", x=270, y=160, width=460, height=460, fill="#FFF3D0", opacity=20, stroke=NONE)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFF4DA", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(190,300,8),(780,260,7),(160,520,9),(830,520,8),(140,420,6),
                               (860,400,7),(380,110,7),(610,105,8),(250,200,6),(730,190,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#A07E40", opacity=40, stroke=NONE)

# --- shoulders: bottom closes on the disc's own arc ------------------------------
by = 780
bl, br = chord_x(by, 417)
d.path(f"M{bl:.1f},{by} C{bl+4:.0f},690 290,610 362,566 C376,530 382,490 392,470 L608,470 "
       f"C618,490 624,530 638,566 C710,610 {br-4:.0f},690 {br:.1f},{by} A417,417 0 0 1 {bl:.1f},{by} Z",
       "Shoulders", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
d.path("M285,660 C310,626 336,600 366,578", "Shoulder sheen L", fill=NONE,
       stroke="#7B6A5E", strokeWidth=8, opacity=35, cap="round")
d.path("M715,660 C690,626 664,600 634,578", "Shoulder sheen R", fill=NONE,
       stroke="#7B6A5E", strokeWidth=8, opacity=35, cap="round")
for i, dd in enumerate(["M300,720 C306,700 316,684 330,670", "M700,720 C694,700 684,684 670,670",
                        "M350,780 C352,756 360,736 372,720", "M650,780 C648,756 640,736 628,720"]):
    d.path(dd, f"Chest fur {i+1}", fill=NONE, stroke="#5A4C43", strokeWidth=5, opacity=45, cap="round")

d.shape("ellipse", "Under-jaw shadow", x=392, y=540, width=216, height=62,
        fill="#050403", opacity=40, stroke=NONE)

# --- the crescent chest mark --------------------------------------------------------
d.path("M378,626 C396,700 448,744 500,746 C552,744 604,700 622,626 "
       "C612,622 600,624 592,632 C580,682 544,708 500,708 "
       "C456,708 420,682 408,632 C400,624 388,622 378,626 Z",
       "Chest crescent", fill=CRESCENT_GRAD, stroke=INK, strokeWidth=5)
d.path("M400,650 C420,700 460,726 500,728 C540,726 580,700 600,650", "Crescent sheen",
       fill=NONE, stroke="#FFFFFF", strokeWidth=5, opacity=40, cap="round")
for i, (x, y, w) in enumerate([(424,676,8),(452,712,7),(546,712,8),(572,680,7),(498,734,6),(398,640,6)]):
    d.shape("ellipse", f"Crescent speck {i+1}", x=x, y=y, width=w, height=w,
            fill="#A9783E", opacity=55, stroke=NONE)

# --- ears -------------------------------------------------------------------------
for side, cx in (("L", 352), ("R", 648)):
    d.shape("ellipse", f"Ear {side}", x=cx - 40, y=242, width=80, height=74,
            fill=EAR_GRAD, stroke=INK, strokeWidth=6)
    d.shape("ellipse", f"Inner ear {side}", x=cx - 22, y=258, width=44, height=40,
            fill="#5B4636", opacity=70, stroke=NONE)

# --- cheek ruff tufts (behind the head so only the points show) -------------------
for side, s in (("L", -1), ("R", 1)):
    x0 = 500 + s*160
    pts = [(x0, 410), (x0 + s*34, 438), (x0 + s*8, 452), (x0 + s*36, 482),
           (x0 + s*4, 494), (x0 + s*26, 526), (x0 - s*30, 540)]
    dd = "M%d,%d " % pts[0] + " ".join("L%d,%d" % p for p in pts[1:]) + " Z"
    d.path(dd, f"Cheek ruff {side}", fill=BODY_GRAD, stroke=INK, strokeWidth=5)

# --- head ----------------------------------------------------------------------
d.path("M500,252 C592,252 662,302 674,382 C684,452 652,522 592,554 "
       "C560,568 440,568 408,554 C348,522 316,452 326,382 "
       "C338,302 408,252 500,252 Z",
       "Head", fill=FUR_GRAD, stroke=INK, strokeWidth=8)
d.path("M400,286 C440,264 560,264 600,286", "Crown sheen", fill=NONE,
       stroke="#857266", strokeWidth=10, opacity=35, cap="round")
d.path("M336,420 C340,470 364,512 400,540", "Cheek rim L", fill=NONE,
       stroke="#C8A777", strokeWidth=6, opacity=28, cap="round")
d.path("M664,420 C660,470 636,512 600,540", "Cheek rim R", fill=NONE,
       stroke="#C8A777", strokeWidth=6, opacity=28, cap="round")
# furrowed forehead wrinkles
for i, dd in enumerate(["M456,318 C468,308 488,306 500,312 C512,306 532,308 544,318",
                        "M440,338 C462,326 488,326 500,332 C512,326 538,326 560,338",
                        "M470,298 C486,292 514,292 530,298"]):
    d.path(dd, f"Brow wrinkle {i+1}", fill=NONE, stroke="#8A7566", strokeWidth=5,
           opacity=40, cap="round")

# --- tan brow patches + muzzle ----------------------------------------------------
d.shape("ellipse", "Brow tan L", x=412, y=350, width=58, height=26, fill="#C99A5E", opacity=35, stroke=NONE)
d.shape("ellipse", "Brow tan R", x=530, y=350, width=58, height=26, fill="#C99A5E", opacity=35, stroke=NONE)
d.path("M500,404 C552,404 592,432 598,478 C604,526 562,560 500,560 "
       "C438,560 396,526 402,478 C408,432 448,404 500,404 Z",
       "Muzzle", fill=MUZZLE_GRAD, stroke=INK, strokeWidth=6)
d.path("M440,424 C470,410 530,410 560,424", "Muzzle sheen", fill=NONE,
       stroke="#FFF0D4", strokeWidth=6, opacity=40, cap="round")
d.path("M418,520 C450,550 550,550 582,520", "Chin shade", fill=NONE,
       stroke="#7C5530", strokeWidth=10, opacity=30, cap="round")
for i, (x, y) in enumerate([(448,478),(436,494),(456,500),(552,478),(564,494),(544,500)]):
    d.shape("ellipse", f"Whisker pore {i+1}", x=x, y=y, width=5, height=5, fill="#6E4A28", opacity=60, stroke=NONE)

# nose
d.path("M470,428 C484,420 516,420 530,428 C540,436 536,452 522,462 "
       "C512,468 488,468 478,462 C464,452 460,436 470,428 Z",
       "Nose", fill=NOSE_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Nose glint", x=484, y=428, width=20, height=8, fill="#FFFFFF", opacity=45, stroke=NONE)
d.shape("ellipse", "Nostril L", x=478, y=446, width=12, height=8, fill="#050403", opacity=80, stroke=NONE)
d.shape("ellipse", "Nostril R", x=510, y=446, width=12, height=8, fill="#050403", opacity=80, stroke=NONE)
# mouth: philtrum then a flat, unimpressed line
d.path("M500,466 L500,494", "Philtrum", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M454,512 C470,500 486,494 500,494 C514,494 530,500 546,512", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M486,512 C492,520 508,520 514,512", "Lower lip", fill=NONE,
       stroke="#7C5530", strokeWidth=4, opacity=60, cap="round")

# --- eyes: small, dark, scowling ----------------------------------------------------
for side, cx, tilt in (("L", 440, 1), ("R", 560, -1)):
    d.shape("ellipse", f"Eye ring {side}", x=cx - 20, y=370, width=40, height=34,
            fill="#5A4A40", opacity=40, stroke=NONE)
    d.shape("ellipse", f"Eye {side}", x=cx - 12, y=377, width=24, height=22,
            fill="#2A1A10", stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"Iris {side}", x=cx - 8, y=380, width=16, height=16,
            fill="#5A3518", opacity=80, stroke=NONE)
    d.shape("ellipse", f"Pupil {side}", x=cx - 5, y=383, width=10, height=10,
            fill="#080504", stroke=NONE)
    d.shape("ellipse", f"Glint {side}", x=cx - 6, y=381, width=6, height=6,
            fill="#FFFFFF", opacity=90, stroke=NONE)
    # heavy lid sloping down toward the nose: the attitude
    x0, x1 = cx - 22*tilt, cx + 20*tilt
    d.path(f"M{x0},{368} C{cx - 6*tilt},{366} {cx + 8*tilt},{372} {x1},{382}",
           f"Lid {side}", fill=NONE, stroke=INK, strokeWidth=7, cap="round")

# --- name ----------------------------------------------------------------------
d.text("SUN BEAR", "Name", x=500, y=962, size=58, font="Virelai Sans",
       color="#F0DDB4", justify="center")

d.finish("sun-bear-V1R00")
