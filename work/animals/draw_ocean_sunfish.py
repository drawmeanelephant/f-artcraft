#!/usr/bin/env python3
"""Ocean sunfish — field-guide plate V1R00. Full body in profile facing left:
a headstone-tall silvery disc of a fish, tall dorsal and anal fins, scalloped
clavus instead of a tail, tiny pectoral fin, blunt beak mouth, faint mottling.
Deep blue plate with one sun shaft from above. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Ocean Sunfish — Field Plate", 1000, 1000)
rng = random.Random(23)

INK = "#16242E"
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#081620"}, {"offset": 1, "color": "#020609"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2E5E7C"}, {"offset": 0.6, "color": "#17374E"},
    {"offset": 1, "color": "#0A1D2D"}]}}
FISH_GRAD = {"gradient": {"kind": "linear", "start": [0, 240], "end": [0, 740], "stops": [
    {"offset": 0, "color": "#7E8E9A"}, {"offset": 0.38, "color": "#B9C4CC"},
    {"offset": 0.7, "color": "#A8B4BC"}, {"offset": 1, "color": "#5E6E7A"}]}}
FIN_GRAD = {"gradient": {"kind": "linear", "start": [0, 200], "end": [0, 760], "stops": [
    {"offset": 0, "color": "#8B9AA6"}, {"offset": 1, "color": "#4E5E6A"}]}}
SHAFT_GRAD = {"gradient": {"kind": "linear", "start": [0, 60], "end": [0, 820], "stops": [
    {"offset": 0, "color": "#D6ECFA", "opacity": 0},
    {"offset": 0.16, "color": "#D6ECFA", "opacity": 0.26},
    {"offset": 0.75, "color": "#BCDDF2", "opacity": 0.13},
    {"offset": 1, "color": "#BCDDF2", "opacity": 0}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def scale_path(dstr, cx, cy, s):
    """Scale every (x,y) pair in an absolute-coords path about (cx,cy)."""
    import re
    out, k = [], 0
    for tok in re.findall(r"[-\d.]+|[A-Za-z]", dstr):
        if tok.isalpha():
            out.append(tok); k = 0; continue
        v = float(tok)
        out.append(str(round((cx + (v - cx) * s) if k % 2 == 0
                             else (cy + (v - cy) * s), 1)))
        k += 1
    return " ".join(out)

S = 1.08          # whole-fish scale about the body centre
CXS, CYS = 515, 470
def sp(dstr):
    return scale_path(dstr, CXS, CYS, S)
def se(x, y, w, h):
    """Scale an ellipse's x/y/w/h about the same centre."""
    return (round(CXS + (x + w / 2 - CXS) * S - w * S / 2, 1),
            round(CYS + (y + h / 2 - CYS) * S - h * S / 2, 1),
            round(w * S, 1), round(h * S, 1))

# --- backdrop + plate -------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#2E5E7C", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0A1826", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#9CC4DA", strokeWidth=3, opacity=35)
# one broad sun shaft angling down through the disc
d.path("M560,62 L668,62 L560,830 L430,830 Z", "Sun shaft", fill=SHAFT_GRAD, stroke=NONE)
d.shape("ellipse", "Shaft bloom", x=470, y=110, width=300, height=120,
        fill="#D6ECFA", opacity=8, stroke=NONE)
# marine snow
for i, (x, y, w) in enumerate([(180,330,6),(820,300,5),(160,520,7),(850,500,6),(240,720,5),(760,740,7),
                               (140,420,5),(870,600,5),(420,100,5),(620,110,6),(300,140,4),(700,180,5),
                               (330,820,5),(660,820,4),(120,600,4),(880,380,4),(520,860,4),(210,640,4),
                               (790,660,5),(450,780,4)]):
    assert on_disc(x + w / 2, y + w / 2, 8), (x, y)
    d.shape("ellipse", f"Marine snow {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8F2F8", opacity=40, stroke=NONE)

# --- body silhouette: headstone with dorsal / anal sails and a scalloped clavus ----
BODY = ("M300,482 "
        "C297,428 322,378 372,346 "           # forehead up from the snout
        "C438,306 508,288 566,282 "          # back rising to the dorsal base
        "C576,246 592,214 614,198 "          # dorsal leading edge
        "C636,228 654,262 664,300 "          # dorsal trailing edge
        "C700,332 724,388 730,442 "          # rear flank into the clavus
        "Q742,458 730,476 Q744,494 728,512 " # scalloped clavus edge
        "Q742,530 726,548 Q736,564 720,580 " # clavus continues
        "C712,616 686,652 650,676 "          # lower rear flank
        "C644,706 630,732 612,748 "          # anal fin trailing edge
        "C592,724 576,692 570,664 "          # anal fin leading edge
        "C520,686 452,668 402,632 "          # belly
        "C362,606 330,560 312,520 "          # chin / throat
        "C301,505 298,492 300,482 Z")        # blunt snout
d.path(sp(BODY), "Body", fill=FISH_GRAD, stroke=INK, strokeWidth=7)

# faint vertical mottling + blotches, seeded so the pattern is stable
for i in range(30):
    x = rng.uniform(330, 700); y = rng.uniform(310, 680)
    cx, cy = x, y
    # stay inside a shrunken oval approximation of the body
    if ((cx - 515) / 195) ** 2 + ((cy - 490) / 185) ** 2 > 1:
        continue
    w = rng.uniform(8, 26); h = w * rng.uniform(0.4, 0.8)
    col = rng.choice(["#E2E9EE", "#E2E9EE", "#5A6A76", "#7C8C98"])
    ex, ey, ew, eh = se(x, y, w, h)
    d.shape("ellipse", f"Mottle {i+1}", x=ex, y=ey,
            width=ew, height=eh, fill=col,
            opacity=rng.randint(14, 30), stroke=NONE)
# soft flank shading + lit shoulder where the shaft lands
ex, ey, ew, eh = se(430, 300, 200, 90)
d.shape("ellipse", "Shoulder light", x=ex, y=ey, width=ew, height=eh,
        fill="#FFFFFF", opacity=12, stroke=NONE)
ex, ey, ew, eh = se(380, 590, 240, 80)
d.shape("ellipse", "Belly shade", x=ex, y=ey, width=ew, height=eh,
        fill="#3E505C", opacity=18, stroke=NONE)
d.path(sp("M660,330 C706,372 726,430 726,478"), "Rear shade", fill=NONE,
       stroke="#3E505C", strokeWidth=26, opacity=22, cap="round")
# faint body striations
for i, dd in enumerate(["M400,370 C420,430 424,520 410,600",
                        "M455,345 C472,420 476,540 460,640",
                        "M520,330 C536,420 538,550 522,660"]):
    d.path(sp(dd), f"Striation {i+1}", fill=NONE, stroke="#5A6A76",
           strokeWidth=3, opacity=18, cap="round")

# --- clavus rim + fin creases -----------------------------------------------------
d.path(sp("M730,442 Q742,458 730,476 Q744,494 728,512 Q742,530 726,548 Q736,564 720,580"),
       "Clavus rim light", fill=NONE, stroke="#DDE6EC", strokeWidth=3,
       opacity=50, cap="round")
d.path(sp("M614,206 C600,246 594,282 596,312"), "Dorsal crease", fill=NONE,
       stroke="#3E505C", strokeWidth=4, opacity=30, cap="round")
d.path(sp("M614,738 C600,704 592,676 592,652"), "Anal crease", fill=NONE,
       stroke="#3E505C", strokeWidth=4, opacity=30, cap="round")

# --- tiny pectoral fin -------------------------------------------------------------
d.path(sp("M436,514 C462,500 486,506 492,528 C484,548 458,556 440,544 "
       "C432,534 430,524 436,514 Z"),
       "Pectoral fin", fill=FIN_GRAD, stroke=INK, strokeWidth=4)
d.path(sp("M444,522 C458,516 472,518 482,528"), "Fin ray", fill=NONE,
       stroke="#3E505C", strokeWidth=3, opacity=45, cap="round")

# --- face: small eye, gill slit, blunt beak mouth ----------------------------------
ex, ey, ew, eh = se(338, 428, 44, 42)
d.shape("ellipse", "Eye socket", x=ex, y=ey, width=ew, height=eh,
        fill="#93A3AE", opacity=45, stroke=NONE)
ex, ey, ew, eh = se(346, 436, 25, 24)
d.shape("ellipse", "Eye", x=ex, y=ey, width=ew, height=eh, fill="#141E26",
        stroke=INK, strokeWidth=3)
ex, ey, ew, eh = se(352, 441, 7, 7)
d.shape("ellipse", "Eye glint", x=ex, y=ey, width=ew, height=eh,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.path(sp("M398,468 C406,500 406,532 396,560"), "Gill slit", fill=NONE,
       stroke="#3E505C", strokeWidth=5, opacity=40, cap="round")
# the beak: a small puckered mouth at the blunt snout
d.path(sp("M300,478 C310,472 322,472 330,478 C322,486 310,486 300,482 Z"),
       "Beak", fill="#3E505C", stroke=INK, strokeWidth=3)
d.path(sp("M302,489 C312,493 322,493 330,489"), "Mouth line", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")

# --- name ---------------------------------------------------------------------------
d.text("OCEAN SUNFISH", "Name", x=500, y=960, size=58, font="Virelai Sans",
       color="#D8E6F0", justify="center")

print("sunfish extent check")
d.finish("ocean-sunfish-V1R00")
