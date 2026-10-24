#!/usr/bin/env python3
"""Virginia opossum — field plate V1R00. The continent's only marsupial doing
the thing it's famous for: playing dead on a moonlit lawn — on its side,
forepaws curled in the air, tongue lolling, naked tail flopped in a curl,
scattered corn kernels the raider came for. Night-yard plate: picket fence
on the ridge, fireflies over the grass, floor closes on the disc arc.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Virginia Opossum — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#14101A"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def disc_x(y, side):
    return CX + side * math.sqrt(R * R - (y - CY) ** 2)

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#0A1018"), (1, "#030509"))
PLATE_GRAD = rad((0, "#4A5E6E"), (0.55, "#253544"), (1, "#0B141E"))
FLOOR_GRAD = lin(0, 640, 0, 880, (0, "#1E332A"), (1, "#0A130E"))
COAT      = rad((0, "#9AA0A8"), (0.6, "#6E747E"), (1, "#3C4048"))
DARKFUR   = lin(0, 380, 0, 700, (0, "#4E545E"), (1, "#262A32"))
FACE      = rad((0, "#E6E6DA"), (1, "#B4B4A8"))
PINK = "#D89AA0"
CORN = "#E4BE4E"

# --- backdrop + night plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(140,120,4),(870,140,5),(110,450,3),(890,500,4),
                               (170,730,4),(860,760,4),(250,170,3)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8D4D8", opacity=30, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#4A5E6E", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1A2A34", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BCCCD8", strokeWidth=3, opacity=40)

# moon upper-right, glow kept inside the disc
MX, MY = 655, 196
for i, (r_, op) in enumerate([(72, 7), (58, 11), (46, 16)]):
    d.shape("ellipse", f"Moon glow {i+1}", x=MX-r_, y=MY-r_, width=2*r_, height=2*r_,
            fill="#E4ECDC", opacity=op, stroke=NONE)
d.shape("ellipse", "Moon", x=MX-38, y=MY-38, width=76, height=76,
        fill=rad((0, "#F6F6E4"), (0.75, "#E8E6CC"), (1, "#C4C2A6")), stroke=NONE)
for i, (ox, oy, w) in enumerate([(-12, -8, 15), (10, 6, 11), (-4, 16, 8)]):
    d.shape("ellipse", f"Moon mare {i+1}", x=MX+ox-w/2, y=MY+oy-w/2,
            width=w, height=w, fill="#B2B094", opacity=30, stroke=NONE)
for i, (x, y, w) in enumerate([(300,130,4),(440,110,5),(560,140,4),(210,260,3),
                               (360,200,4),(490,170,3),(160,420,4)]):
    assert on_disc(x, y, 15), (x, y)
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w,
            fill="#DCE6E0", opacity=45, stroke=NONE)

# --- picket fence on the ridge, bases hidden under the floor -------------------
for i, x in enumerate([190, 300, 410, 590, 700, 810]):
    d.path(f"M{x-10},700 L{x-10},566 L{x},550 L{x+10},566 L{x+10},700 Z",
           f"Picket {i+1}", fill="#162430", opacity=92, stroke=NONE)
d.path("M170,612 L836,600", "Fence rail", fill=NONE, stroke="#162430",
       strokeWidth=12, opacity=88, cap="round")

# --- lawn floor closing on the arc ---------------------------------------------
fy = 656
fl, fr = disc_x(fy, -1), disc_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C260,640 400,652 540,644 C660,640 780,650 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl+10:.1f},{fy-2} C260,638 400,648 540,642 C660,638 770,646 {fr-10:.1f},{fy-2}",
       "Floor light", fill=NONE, stroke="#A8C8B0", strokeWidth=4, opacity=30, cap="round")
# fireflies over the grass
for i, (x, y) in enumerate([(190,560),(280,500),(720,540),(800,600),(640,480),(330,620)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Firefly glow {i+1}", x=x-7, y=y-7, width=14, height=14,
            fill="#E8D87A", opacity=15, stroke=NONE)
    d.shape("ellipse", f"Firefly {i+1}", x=x-2, y=y-2, width=5, height=5,
            fill="#F0E08A", opacity=85, stroke=NONE)

# contact shadow hugging the belly on the grass
d.shape("ellipse", "Body shadow", x=310, y=634, width=400, height=60,
        fill="#04080A", opacity=45, stroke=NONE)

# --- the naked tail: curls out of the rump, flops back toward the body ---------
d.path("M700,560 C766,590 786,648 758,696 C740,726 706,738 676,724",
       "Tail base", fill=NONE, stroke="#A8848C", strokeWidth=26, cap="round")
d.path("M700,560 C766,590 786,648 758,696", "Tail light",
       fill=NONE, stroke="#C4A0A6", strokeWidth=8, opacity=50, cap="round")
d.path("M758,696 C740,726 706,738 676,724",
       "Tail tip", fill=NONE, stroke="#B08E94", strokeWidth=15, cap="round")

# --- body on its side: elongated shaggy mound, belly sagging onto the lawn -----
BODY = ("M262,478 "                              # nose tip, head tipped back
        "C280,448 304,424 332,410 "              # long snout top to forehead
        "C348,402 364,398 380,400 "              # poll
        "C402,404 420,402 442,398 "              # back of head
        "C486,392 540,392 594,402 "              # neck into a long low spine
        "C648,412 688,440 706,478 "              # to the rump
        "C718,506 722,530 716,556 "              # rump to tail seat
        "C706,588 680,622 634,640 "              # belly right
        "C580,658 480,664 396,654 "              # long flat belly on the grass
        "C350,648 324,632 310,606 "              # chest bottom
        "C300,584 298,560 302,540 "              # chest front
        "C304,526 300,514 292,504 "              # throat/jaw
        "C280,496 268,488 262,478 Z")            # back to nose
d.path(BODY, "Opossum", fill=COAT, stroke=INK, strokeWidth=6)
# grizzled dark saddle along the spine
d.path("M430,404 C470,394 520,390 570,398 C630,406 676,428 700,464 "
       "C668,440 610,420 550,414 C500,410 460,410 430,404 Z",
       "Saddle", fill=DARKFUR, opacity=60, stroke=NONE)
# flank shading: darker under the belly run, pale wash on the flank
d.shape("ellipse", "Belly light", x=410, y=540, width=220, height=64,
        fill="#C8CCD0", opacity=16, stroke=NONE)
d.path("M400,632 C480,646 570,646 640,624", "Belly line",
       fill=NONE, stroke="#262A32", strokeWidth=6, opacity=40, cap="round")
# guard-hair flicks along the spine edge
for i, (x, y, dx, dy) in enumerate([(436,400,14,-14),(486,392,16,-12),(546,394,16,-10),
                                    (606,406,16,-8),(662,428,14,-6),(386,410,12,-14),
                                    (700,468,12,-2),(510,390,14,-12)]):
    d.path(f"M{x},{y} L{x+dx},{y+dy}", f"Guard hair {i+1}",
           fill=NONE, stroke="#C8CCD0", strokeWidth=2.5, opacity=55, cap="round")

# --- flopped hind foot lying on the grass at the rump side ----------------------
d.path("M662,630 C686,636 710,648 726,664 C732,672 728,680 716,678 "
       "C692,672 668,660 652,644 C646,636 652,626 662,630 Z",
       "Hind foot", fill="#8A8288", stroke=INK, strokeWidth=3.5)
for j, (tx, ty) in enumerate([(734,668),(738,676),(732,684),(722,690)]):
    d.path(f"M{tx-10},{ty-8} L{tx},{ty}", f"Hind toe {j+1}",
           fill=NONE, stroke=PINK, strokeWidth=5, cap="round")

# --- forepaws curled in the air: the faint's signature --------------------------
def paw(wx, wy, px, py, label):
    d.path(f"M{wx},{wy} C{wx-8},{wy-34} {px-6},{py+24} {px},{py+8}",
           f"{label} wrist", fill=NONE, stroke="#7E848E",
           strokeWidth=13, cap="round")
    d.shape("ellipse", f"{label} palm", x=px-16, y=py-12, width=34, height=28,
            fill="#8A8E96", stroke=INK, strokeWidth=3)
    for j, ang in enumerate([-55, -20, 15, 50]):
        a = math.radians(ang)
        x1, y1 = px + 10 * math.cos(a), py - 8 + 10 * math.sin(a)
        x2, y2 = px + 24 * math.cos(a), py - 8 + 22 * math.sin(a)
        d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"{label} finger {j+1}",
               fill=NONE, stroke=PINK, strokeWidth=4.5, cap="round")

paw(442, 420, 410, 330, "Forepaw L")
paw(512, 414, 500, 318, "Forepaw R")
paw(654, 430, 646, 338, "Hindpaw")

# --- head: tipped back, mouth slack, tongue lolling -----------------------------
d.path("M262,478 C272,456 290,436 314,422 C336,410 358,402 374,400 "
       "C380,420 376,440 364,454 C348,472 326,484 302,486 "
       "C286,488 268,486 262,478 Z",
       "Face", fill=FACE, opacity=90, stroke=NONE)
# ears: dark rounds, pink-lined, the near ear flopped
d.shape("ellipse", "Ear far", x=394, y=378, width=42, height=38,
        fill="#1C1820", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Ear near", x=352, y=364, width=56, height=52,
        fill="#1C1820", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Ear near inner", x=365, y=380, width=29, height=25,
        fill="#C98A92", opacity=70, stroke=NONE)
d.path("M352,382 C360,370 376,364 390,368", "Ear rim light",
       fill=NONE, stroke="#E4DCE4", strokeWidth=3, opacity=50, cap="round")
# nose: pink, soft
d.path("M254,472 C256,462 264,456 273,458 C278,462 278,470 272,476 "
       "C266,481 256,480 254,472 Z",
       "Nose", fill=rad((0, "#E4A8AE"), (1, "#B06A74")), stroke=NONE)
d.shape("ellipse", "Nostril", x=257, y=464, width=6, height=5, fill="#5E3038", stroke=NONE)
# mouth slack + tongue lolling out the corner
d.path("M268,490 C280,498 296,502 312,500", "Mouth line",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
d.path("M288,502 C286,512 290,520 298,522 C306,524 310,518 308,510 "
       "C304,504 294,500 288,502 Z",
       "Tongue", fill=rad((0, "#E09AA2"), (1, "#A8606A")), stroke=INK, strokeWidth=2)
# half-mast swooning eye
d.path("M330,448 C338,440 352,438 362,444", "Lid",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.shape("ellipse", "Eye", x=336, y=446, width=18, height=12,
        fill="#181018", stroke=NONE)
d.path("M330,458 C340,464 356,464 366,458", "Under eye",
       fill=NONE, stroke="#8A8E96", strokeWidth=3, opacity=60, cap="round")
# whiskers
for i, (x2, y2) in enumerate([(232,478),(236,494),(244,508)]):
    d.path(f"M274,{484+i*7} C254,{482+i*7} {x2+10},{y2-2} {x2},{y2}",
           f"Whisker {i+1}", fill=NONE, stroke="#D8DCE0",
           strokeWidth=2, opacity=55, cap="round")
# cheek shading
d.path("M328,476 C344,484 360,484 372,476 C362,490 342,494 328,484 Z",
       "Jowl shade", fill="#9A9EA6", opacity=45, stroke=NONE)

# --- moon-corn: kernels spilled beside the raider --------------------------------
for i, (x, y, s, a) in enumerate([(264,678,14,-25),(292,700,13,30),(320,682,12,-10),
                                  (352,706,14,55),(250,716,11,70),(300,730,12,-45),
                                  (686,742,13,20),(716,722,12,-60),(380,724,11,15)]):
    r_ = math.radians(a); c_, s_ = math.cos(r_), math.sin(r_)
    tx, ty = x + s * c_, y + s * s_
    d.path(f"M{x},{y} L{(x+tx)/2 - s_*4:.0f},{(y+ty)/2 + c_*4:.0f} "
           f"L{tx:.0f},{ty:.0f} L{(x+tx)/2 + s_*4:.0f},{(y+ty)/2 - c_*4:.0f} Z",
           f"Kernel {i+1}", fill=CORN, opacity=90, stroke=NONE)
# grass tufts
def tuft(x, y, s, label, lean=0):
    for j, (dx, bend) in enumerate([(-16, -26), (0, 0), (16, 26), (-6, -12), (8, 14)]):
        x2 = x + dx * s + bend * s * 0.4 + lean
        y2 = y - (34 - abs(dx)) * s
        d.path(f"M{x},{y} C{x + dx*s*0.3 + lean},{y - (20-abs(dx)*0.4)*s} "
               f"{x2 - bend*s*0.3},{y2 + 14*s} {x2},{y2}",
               f"{label} blade {j+1}", fill=NONE, stroke="#5E7A5E",
               strokeWidth=3.5, opacity=70, cap="round")

tuft(216, 720, 0.85, "Tuft L", -6)
tuft(784, 730, 0.8, "Tuft R", 5)
tuft(470, 764, 0.7, "Tuft M")
tuft(346, 668, 0.55, "Tuft belly L", -4)
tuft(650, 662, 0.5, "Tuft belly R", 3)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0A1218", strokeWidth=6)

# --- name ----------------------------------------------------------------------
r1 = d.text("VIRGINIA OPOSSUM", "Name", x=500, y=962, size=47, font="Virelai Sans",
            color="#DCDCE0", justify="center")

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
b = find(layers, r1["id"])["bounds"]
print("name bounds", {k: round(v) for k, v in b.items()})
assert b["width"] <= 800 and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("virginia-opossum-V1R00")
