#!/usr/bin/env python3
"""Oryx — field-guide plate V1R00. Head-and-shoulders profile facing
right: scimitar horns sweeping back like drawn calligraphy over a white
mask ruled with black war-paint — eye-band, nose wedge, chin edging. Sand
and charcoal against a cold violet dusk plate; neck and shoulder merge
into one mass closing on the disc's own arc. 1000x1000. House style:
gradients + translucent shading, never flat."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Oryx — Field Plate", 1000, 1000)

INK = "#241A14"
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def ribbon(p0, p1, p2, w0, w1, label, fill, samples=18, **kw):
    """Tapered filled stroke along a quadratic — the scimitar horns, the eye-band."""
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

BG_GRAD = lin(0, 0, 0, 1000, (0, "#1A1428"), (1, "#090611"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#4E3F6E"), (0.42, "#7E5C84"),
                 (0.72, "#B88C92"), (1, "#E2C9A4"))
SAND_GRAD = lin(500, 400, 640, 830, (0, "#E8D6B2"), (1, "#A88860"))
MASK_GRAD = rad((0, "#F8F2E6"), (0.7, "#EADCC4"), (1, "#CBB694"))
CHARCOAL = lin(460, 340, 620, 430, (0, "#38302C"), (1, "#181414"))
HORN_GRAD = lin(500, 330, 260, 180, (0, "#4A3C30"), (1, "#1C1614"))
HORN_FAR_GRAD = lin(480, 340, 250, 200, (0, "#3A2E26"), (1, "#161010"))
EYE_GRAD = rad((0, "#4A3424"), (1, "#120A05"))
EAR_GRAD = lin(420, 380, 480, 420, (0, "#CBAE84"), (1, "#A08456"))

# --- backdrop + cold violet dusk plate -------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4A3A5E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E2F2", strokeWidth=3, opacity=45)
d.shape("ellipse", "Horizon glow", x=200, y=560, width=560, height=240,
        fill="#F0D8B4", opacity=25, stroke=NONE)
d.shape("ellipse", "Patina", x=170, y=180, width=220, height=120, fill="#CBB8D4", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(220,170,5),(340,120,4),(640,110,5),(760,190,4),(180,300,4),(830,330,5),
                               (700,260,4),(260,420,4),(160,600,5),(860,520,4)]):
    d.shape("ellipse", f"Dusk star {i+1}", x=x, y=y, width=w, height=w,
            fill="#F4EAF6", opacity=50, stroke=NONE)

# faint dune ridges, all inside the disc
d.path("M160,600 C240,580 320,576 400,586", "Dune far", fill=NONE,
       stroke="#C9A284", strokeWidth=8, opacity=22, cap="round")
d.path("M190,650 C260,634 330,632 390,640", "Dune near", fill=NONE,
       stroke="#B08C72", strokeWidth=7, opacity=18, cap="round")
# a dry desert shrub silhouette
d.path("M240,600 L238,572 M238,584 L222,568 M240,580 L256,564 M242,592 L262,584",
       "Shrub", fill=NONE, stroke="#6E5244", strokeWidth=4, opacity=32, cap="round")

# --- far horn first: its base hides behind the skull --------------------------------
ribbon((486,332), (368,238), (254,200), 15, 4, "Horn far",
       HORN_FAR_GRAD, stroke=NONE)
d.path("M470,310 C420,270 360,232 300,212", "Horn far sheen", fill=NONE,
       stroke="#9E8A78", strokeWidth=3, opacity=30, cap="round")

# --- ear: small pointed leaf below the horns ------------------------------------------
d.path("M486,390 C464,378 440,376 420,386 C426,400 444,410 464,412 "
       "C474,408 482,400 486,390 Z",
       "Ear", fill=EAR_GRAD, stroke=INK, strokeWidth=4)
d.path("M472,392 C456,386 442,386 430,390", "Ear shade", fill=NONE,
       stroke="#6E5240", strokeWidth=4, opacity=40, cap="round")

# --- neck + shoulder: one mass closing on the disc's own arc ----------------------------
NECK = ("M545,436 C586,478 616,540 634,604 C648,650 668,700 690,740 "
        "C706,768 720,790 732,810 A420,420 0 0 1 268,810 "
        "C320,780 380,730 424,676 C448,648 460,610 464,570 "
        "C466,520 470,470 480,424 C494,410 522,416 545,436 Z")
d.path(NECK, "Neck and shoulder", fill=SAND_GRAD, stroke=INK, strokeWidth=6)
# shading: throat shade, nape light, withers hollow
d.path("M560,450 C596,494 622,550 638,608", "Throat shade", fill=NONE,
       stroke="#6E5240", strokeWidth=14, opacity=25, cap="round")
d.path("M452,600 C456,556 462,508 474,464", "Nape light", fill=NONE,
       stroke="#F4E4C2", strokeWidth=10, opacity=30, cap="round")
d.path("M420,700 C440,670 452,640 456,610", "Withers shade", fill=NONE,
       stroke="#6E5240", strokeWidth=12, opacity=20, cap="round")
# chest shadow pooling under the throat + a soft neck fold
d.path("M600,620 C630,660 658,700 690,740 C704,760 716,780 726,796 "
       "C700,790 668,772 644,744 C622,712 606,668 600,620 Z",
       "Chest shadow", fill="#8A7050", opacity=30, stroke=NONE)
d.path("M510,520 C530,570 552,620 576,668", "Neck fold", fill=NONE,
       stroke="#8A7050", strokeWidth=6, opacity=28, cap="round")
d.path("M478,560 C480,520 486,482 498,452", "Nape sheen", fill=NONE,
       stroke="#F8ECD2", strokeWidth=6, opacity=30, cap="round")
# the charcoal flank stripe riding the lower edge of the bust
d.path("M304,794 C380,822 460,832 500,834 C580,832 656,818 714,794",
       "Flank stripe", fill=NONE, stroke="#1E1818", strokeWidth=11, opacity=60, cap="round")

# --- head: the white mask --------------------------------------------------------------
HEAD = ("M498,318 C530,322 560,336 590,352 C614,364 632,378 642,392 "
        "C646,400 640,408 630,412 C608,420 580,426 556,432 "
        "C536,436 514,438 496,434 C480,428 470,412 468,394 "
        "C466,368 476,336 498,318 Z")
d.path(HEAD, "Head", fill=MASK_GRAD, stroke=INK, strokeWidth=6)
# soft shading on the mask
d.path("M512,332 C546,338 578,352 606,370", "Forehead light", fill=NONE,
       stroke="#FFFFFF", strokeWidth=8, opacity=40, cap="round")
d.path("M500,420 C520,428 544,428 566,424", "Jaw shade", fill=NONE,
       stroke="#8A7050", strokeWidth=7, opacity=30, cap="round")

# war-paint: black nose wedge, bold eye-band, chin edging, poll wedge
d.path("M614,370 C630,378 641,388 644,398 C640,408 628,414 612,416 "
       "C606,404 606,386 614,370 Z",
       "Nose wedge", fill=CHARCOAL, stroke=NONE)
d.shape("ellipse", "Nostril", x=624, y=392, width=9, height=6, fill="#080606", stroke=NONE)
ribbon((500,336), (552,378), (600,418), 27, 12, "Eye band",
       CHARCOAL, stroke=NONE)
d.path("M552,424 C574,420 594,414 612,406", "Chin edge", fill=NONE,
       stroke="#1E1818", strokeWidth=5, opacity=75, cap="round")
d.path("M484,314 C504,312 524,322 534,336 C518,332 500,328 486,326 Z",
       "Poll wedge", fill=CHARCOAL, stroke=NONE)
# the white blaze between the war-paint reads through the gaps
d.path("M508,352 C528,360 550,374 568,390", "Blaze light", fill=NONE,
       stroke="#FFFFFF", strokeWidth=9, opacity=55, cap="round")

# eye set inside the eye-band
d.shape("ellipse", "Eye", x=538, y=368, width=25, height=22, fill=EYE_GRAD,
        stroke="#0E0806", strokeWidth=3)
d.shape("ellipse", "Eye glint", x=545, y=372, width=7, height=7, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M534,368 C544,360 558,360 568,368", "Brow accent", fill=NONE,
       stroke="#F8F2E6", strokeWidth=4, opacity=60, cap="round")
# mouth line
d.path("M610,416 C596,420 582,424 570,426", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")

# --- near horn: the scimitar, thick base to calligraphy point -----------------------------
ribbon((500,322), (388,208), (272,176), 17, 4, "Horn near",
       HORN_GRAD, stroke=NONE)
d.path("M488,300 C436,256 372,216 306,194", "Horn sheen", fill=NONE,
       stroke="#B09A88", strokeWidth=3, opacity=35, cap="round")
# ring ridges near the horn base
for i, (x, y, a) in enumerate([(490,330,-52),(480,315,-50),(468,300,-48),(458,285,-46)]):
    t = math.radians(a)
    d.path(f"M{x},{y} L{x+14*math.cos(t):.0f},{y+14*math.sin(t):.0f}", f"Horn ridge {i+1}",
           fill=NONE, stroke="#100C0A", strokeWidth=3, opacity=55, cap="round")

# --- rim redrawn so the plate edge stays crisp ----------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#4A3A5E", strokeWidth=6)

# --- name ------------------------------------------------------------------------------------
d.text("ORYX", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#E8DCF0", justify="center")

d.finish("oryx-V1R00")
