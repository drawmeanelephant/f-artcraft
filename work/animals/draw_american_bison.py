#!/usr/bin/env python3
"""American bison — field plate V1R00. Profile facing left into the weather:
the great shoulder hump crests over a low-carried head, the dark shaggy cape
ends in a ragged hem mid-body and the hindquarters run shorter-haired and
tawny. Short black horns, a beard under the chin, breath fogging at the
muzzle. Plains plate, blizzard-edge mood: steel-blue disc, wind streaks,
snowdrift closing on the floor arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("American Bison — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#181008"   # warm near-black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def radO(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def disc_x(y, side):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)

def smooth(pts, closed=True):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0C1620"), (1, "#04070B"))
PLATE_GRAD = rad((0, "#BCCFDC"), (0.55, "#7E97AA"), (1, "#33485C"))
CAPE_GRAD  = rad((0, "#443428"), (0.6, "#261B12"), (1, "#120C07"))
HIND_GRAD  = rad((0, "#7E6244"), (0.65, "#523C28"), (1, "#2E2014"))
SNOW_GRAD  = lin(0, 700, 0, 880, (0, "#F2F8FC"), (1, "#A8C2D6"))
MUZZLE_GRAD = rad((0, "#4A3B2C"), (1, "#221810"))

# --- backdrop + plate --------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#9EBBD0", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#26404F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8F2F8", strokeWidth=3, opacity=40)

# blizzard: wind streaks driving left-to-right across the plate
for i, dd in enumerate(["M150,250 C330,224 560,224 770,252",
                        "M210,330 C400,306 610,308 800,336",
                        "M120,410 C320,388 560,390 760,420",
                        "M300,180 C450,168 580,170 690,186"]):
    d.path(dd, f"Wind streak {i+1}", fill=NONE, stroke="#E8F2F8",
           strokeWidth=6, opacity=18, cap="round")
# snowflakes riding the wind
for i, (x, y, w) in enumerate([(190,290,7),(760,240,6),(160,470,8),(830,430,7),(250,150,6),(720,140,7),
                               (400,110,6),(600,105,7),(140,580,6),(860,560,6),(330,190,5),(690,220,5),
                               (480,150,5),(540,340,6),(230,520,5)]):
    assert on_disc(x + w / 2, y + w / 2, 6), (x, y)
    d.shape("ellipse", f"Flake {i+1}", x=x, y=y, width=w, height=w,
            fill="#F4FAFD", opacity=50, stroke=NONE)

# --- hind legs first (behind the body mass) --------------------------------------------
for i, (x0, shade) in enumerate([(640, "#241A10"), (676, "#342618")]):
    d.path(f"M{x0},610 C{x0 - 4},662 {x0 - 2},706 {x0 - 2},742",
           f"Rear leg {i+1}", fill=NONE, stroke=shade, strokeWidth=16, cap="round")
    d.path(f"M{x0 - 12},738 L{x0 + 10},738 L{x0 + 7},750 L{x0 - 9},750 Z",
           f"Rear hoof {i+1}", fill="#0E0A05", stroke=NONE)

# --- tail: short, hanging at the rump -----------------------------------------------------
d.path("M716,512 C726,548 726,578 718,600", "Tail", fill=NONE,
       stroke="#221812", strokeWidth=6, cap="round")
d.shape("ellipse", "Tail tuft", x=710, y=592, width=16, height=26,
        fill="#140D07", stroke=NONE)

# --- body mass: head carried low, hump cresting behind the poll -----------------------------
# nose -> near-vertical face -> poll -> dip -> hump crest -> sloping back -> rump
d.path(smooth([(288, 596), (286, 566), (298, 532), (306, 488), (322, 452),
               (348, 438), (366, 446), (394, 410), (438, 390), (490, 396),
               (556, 416), (640, 444), (692, 472), (722, 512), (726, 566),
               (706, 622), (664, 652), (560, 672), (470, 676), (380, 668),
               (330, 646), (306, 622)]),
       "Body", fill=CAPE_GRAD, stroke=INK, strokeWidth=5)

# tawny hindquarters washing over the rear third
d.path(smooth([(566, 446), (630, 464), (684, 492), (714, 534), (714, 584),
               (692, 630), (634, 654), (580, 662), (556, 632), (552, 580),
               (556, 524), (552, 480)]),
       "Hindquarters", fill=HIND_GRAD, opacity=85, stroke=NONE)
# the cape edge: a ragged vertical fringe where the shag ends
fringe = "M552,452 "
for fy, fx in [(478, 546), (502, 556), (526, 547), (550, 557), (574, 548),
               (598, 558), (622, 550), (646, 558)]:
    fringe += f"L{fx},{fy} "
fringe += "L564,662 L568,452 Z"
d.path(fringe, "Cape fringe", fill="#160E07", opacity=38, stroke=NONE)
# a few loose guard hairs crossing the seam
for i, dd in enumerate(["M548,470 C556,520 556,570 548,620",
                        "M560,486 C566,530 564,586 556,640"]):
    d.path(dd, f"Cape hair {i+1}", fill=NONE, stroke="#0E0904",
           strokeWidth=4, opacity=30, cap="round")

# ragged shag hem under the cape
hem = "M330,664 "
teeth = [(352, 692), (372, 668), (394, 696), (414, 670), (438, 696), (458, 672),
         (480, 694), (500, 672), (522, 690), (540, 666)]
for tx, ty in teeth:
    hem += f"L{tx},{ty} "
hem += "L552,656 C500,676 400,678 330,664 Z"
d.path(hem, "Cape hem", fill="#1A1109", opacity=80, stroke=NONE)

# throat fringe: hair chaps hanging off the face front and chest
chaps = "M300,540 "
for cx_, cy_ in [(288, 566), (298, 590), (290, 614), (304, 638), (314, 662),
                 (330, 682), (348, 660), (356, 686), (370, 664)]:
    chaps += f"L{cx_},{cy_} "
chaps += "C340,700 300,686 290,648 C284,610 292,570 300,540 Z"
d.path(chaps, "Throat chaps", fill="#120B05", opacity=80, stroke=NONE)

# hump sheen + shag texture strokes following the crest
d.path("M384,414 C424,398 476,402 518,420", "Hump light", fill=NONE,
       stroke="#6E5840", strokeWidth=9, opacity=35, cap="round")
for i, dd in enumerate(["M400,430 C416,418 436,412 458,414",
                        "M414,452 C432,440 456,434 478,438",
                        "M430,476 C450,464 476,460 500,466",
                        "M380,452 C394,442 412,436 428,438"]):
    d.path(dd, f"Shag {i+1}", fill=NONE, stroke="#0E0904",
           strokeWidth=4, opacity=35, cap="round")

# --- forelegs under the cape hem ---------------------------------------------------------
for i, (x0, shade) in enumerate([(388, "#160F08"), (424, "#20160C")]):
    d.path(f"M{x0},664 C{x0 - 2},700 {x0 - 4},722 {x0 - 4},744",
           f"Foreleg {i+1}", fill=NONE, stroke=shade, strokeWidth=17, cap="round")
    d.path(f"M{x0 - 14},740 L{x0 + 8},740 L{x0 + 5},752 L{x0 - 11},752 Z",
           f"Fore hoof {i+1}", fill="#0E0A05", stroke=NONE)

# --- beard + jaw fringe --------------------------------------------------------------------
d.path("M298,614 L312,650 L326,626 L340,654 L354,630 L364,650 C344,664 314,656 298,614 Z",
       "Beard", fill="#120C06", opacity=85, stroke=NONE)

# --- woolly crown: the felted cap over forehead and poll ---------------------------------------
d.path("M304,488 C308,462 322,444 348,436 C376,428 400,436 412,452 "
       "C396,462 380,464 364,462 C348,470 330,478 316,496 Z",
       "Wool crown", fill="#2E2216", opacity=80, stroke=NONE)

# --- horns: short black hooks over the brow -------------------------------------------------
d.path("M344,462 C324,452 306,438 296,418 C293,408 301,404 308,412 "
       "C321,426 336,438 352,448 Z",
       "Horn near", fill="#2A241E", stroke="#0E0A05", strokeWidth=2)
d.path("M368,452 C360,436 358,420 362,404 C370,398 376,404 376,414 "
       "C376,430 374,442 368,452 Z",
       "Horn far", fill="#241F1A", stroke="#0E0A05", strokeWidth=2)
# horn light
d.path("M312,424 C322,436 332,446 342,452", "Horn light", fill=NONE,
       stroke="#6E6458", strokeWidth=3, opacity=50, cap="round")

# --- ear tucked under the horn ---------------------------------------------------------------
d.shape("ellipse", "Ear", x=366, y=462, width=34, height=22,
        fill="#1C130B", stroke=INK, strokeWidth=3)

# --- muzzle shading + nose ---------------------------------------------------------------------
d.shape("ellipse", "Muzzle", x=280, y=576, width=42, height=38,
        fill=MUZZLE_GRAD, opacity=85, stroke=NONE)
d.shape("ellipse", "Nostril", x=284, y=586, width=13, height=15,
        fill="#0A0603", stroke=NONE)
d.path("M292,610 C308,620 326,624 344,620", "Mouth line", fill=NONE,
       stroke="#0E0A05", strokeWidth=4, opacity=60, cap="round")

# --- eye: small, sunk in the brow ----------------------------------------------------------------
d.shape("ellipse", "Eye", x=330, y=508, width=14, height=12, fill="#0A0603", stroke=NONE)
d.shape("ellipse", "Eye glint", x=333, y=510, width=4, height=4, fill="#DCE8F0", opacity=70, stroke=NONE)

# --- breath fog rolling off the muzzle -------------------------------------------------------------
d.shape("ellipse", "Breath fog", x=196, y=560, width=130, height=90,
        fill=radO((0, "#E8F2F8", 28), (0.6, "#E8F2F8", 12), (1, "#E8F2F8", 0)), stroke=NONE)
d.shape("ellipse", "Breath puff", x=232, y=576, width=70, height=44,
        fill=radO((0, "#F0F6FA", 40), (1, "#F0F6FA", 0)), stroke=NONE)

# --- snowdrift floor, closing on the disc's own arc --------------------------------------------------
GY = 752
gl, gr = disc_x(GY, -1), disc_x(GY, 1)
d.path(f"M{gl:.1f},{GY} C300,{GY-14} 420,{GY-4} 520,{GY-8} C620,{GY-12} 700,{GY-6} {gr:.1f},{GY} "
       f"A{PR},{PR} 0 0 1 {gl:.1f},{GY} Z", "Snowdrift", fill=SNOW_GRAD,
       stroke="#8FACC0", strokeWidth=4)
d.path(f"M{gl+40:.0f},{GY+16} C380,{GY+8} 620,{GY+8} {gr-40:.0f},{GY+18}",
       "Drift shade", fill=NONE, stroke="#9FBDD0", strokeWidth=5, opacity=45, cap="round")
# sastrugi: wind-carved ridges on the drift
for i, dd in enumerate([f"M{gl+60:.0f},{GY+40} C360,{GY+32} 480,{GY+36} 560,{GY+40}",
                        f"M{gl+140:.0f},{GY+64} C420,{GY+56} 560,{GY+60} 700,{GY+66}"]):
    d.path(dd, f"Sastrugi {i+1}", fill=NONE, stroke="#B8CFDE",
           strokeWidth=4, opacity=55, cap="round")
# spindrift crawling across the ground in front of the hooves
d.path(f"M{gl+20:.0f},{GY+26} C340,{GY+16} 560,{GY+22} {gr-20:.0f},{GY+30}",
       "Spindrift", fill=NONE, stroke="#F4FAFD", strokeWidth=8, opacity=30, cap="round")

# --- name ---------------------------------------------------------------------------------------------
r1 = d.text("AMERICAN BISON", "Name", x=500, y=962, size=56, font="Virelai Sans",
            color="#E4EDF4", justify="center")

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

d.finish("american-bison-V1R00")
