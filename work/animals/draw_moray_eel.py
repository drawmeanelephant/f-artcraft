#!/usr/bin/env python3
"""Moray eel — field plate V1R00. A second set of jaws in the throat, just in
case. Reef-crevice plate, murk mood: two algae-fuzzed rock masses with a
black gap between them, and out of the gap an eel's neck uncoils into the
murk, mouth held open — not striking, holding station while a cleaner
wrasse works the jaw. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Moray Eel — Field Plate", 1000, 1000)
rng = random.Random(41)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#12100A"                    # warm dark ink, never pure black

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

def on_disc(x, y, pad=0, r=R):
    return math.hypot(x - CX, y - CY) <= r - pad

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0A0D08"), (1, "#040503"))
PLATE_GRAD = rad((0, "#5E6B4A"), (0.5, "#333C26"), (1, "#141A0E"))
ROCK_GRAD  = lin(0, 300, 0, 800, (0, "#57503E"), (0.6, "#332C1E"), (1, "#181408"))
EEL_GRAD   = lin(560, 380, 520, 720, (0, "#9EA45C"), (0.5, "#6E7440"), (1, "#33381A"))
MOUTH      = "#2E1014"
TEETH      = "#E2DCC2"

# --- backdrop + murk plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#4A5638", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#161C0E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4D0A0", strokeWidth=3, opacity=26)

# a shaft of dim green light finding the crevice, fading before the rim
d.shape("ellipse", "Murk light", x=300, y=140, width=380, height=260,
        fill=rad((0, "#BCC898", 20), (0.6, "#BCC898", 8), (1, "#BCC898", 0)), stroke=NONE)
# marine snow — sparse motes drifting in the gloom
for i in range(34):
    a = rng.uniform(0, math.tau); rr = math.sqrt(rng.uniform(0, 1)) * 385
    x, y = CX + rr * math.cos(a), CY + rr * math.sin(a)
    if not on_disc(x, y, 18): continue
    w = rng.uniform(2.5, 5.5)
    d.shape("ellipse", f"Mote {i+1}", x=x - w/2, y=y - w/2, width=w, height=w,
            fill="#D4DCB8", opacity=rng.randint(12, 30), stroke=NONE)

# --- the crevice: two rock masses and the black gap between them -----------------------
# left rock — a looming wall from the rim into mid-plate
d.path(f"M{rim_x(330, side=-1):.1f},330 C200,318 268,352 296,400 "
       f"C318,438 330,470 322,506 C312,548 288,584 264,610 "
       f"C244,632 218,650 {rim_x(700, side=-1):.1f},700 "
       f"A{R},{R} 0 0 0 {rim_x(330, side=-1):.1f},330 Z",
       "Rock left", fill=ROCK_GRAD, stroke=INK, strokeWidth=5)
# right rock — the heavier shoulder the neck leans from
d.path(f"M{rim_x(360, side=1):.1f},360 C800,348 742,380 716,428 "
       f"C694,468 686,512 696,556 C706,598 730,634 758,660 "
       f"C786,684 830,700 {rim_x(720, side=1):.1f},720 "
       f"A{R},{R} 0 0 1 {rim_x(360, side=1):.1f},360 Z",
       "Rock right", fill=ROCK_GRAD, stroke=INK, strokeWidth=5)
# the black gap — the crevice throat between the masses
d.path("M322,506 C360,480 420,468 470,478 C540,492 620,470 686,500 "
       "C694,540 700,600 716,660 C700,690 640,706 560,710 "
       "C460,714 360,700 300,660 C284,620 296,550 322,506 Z",
       "Crevice", fill="#0C0A05", opacity=90, stroke=NONE)
# faint lit lip on the gap's edge
d.path("M322,506 C360,480 420,468 470,478", "Gap lip L", fill=NONE,
       stroke="#8E9468", strokeWidth=4, opacity=40, cap="round")
d.path("M560,492 C610,476 660,482 686,500", "Gap lip R", fill=NONE,
       stroke="#8E9468", strokeWidth=4, opacity=35, cap="round")

# strata cracks on the rock faces — they read as reef, not wings
for i, dd in enumerate(["M150,420 C190,412 240,420 288,434",
                        "M140,520 C190,508 240,516 282,532",
                        "M730,450 C780,440 830,446 872,462",
                        "M740,540 C790,532 840,540 878,556",
                        "M770,640 C806,632 838,640 860,650"]):
    d.path(dd, f"Strata {i+1}", fill=NONE, stroke="#241E12",
           strokeWidth=5, opacity=50, cap="round")
# algae fuzz + pocks on the rock faces
for i, (x, y) in enumerate([(180, 380), (240, 350), (150, 470), (270, 560),
                            (760, 420), (800, 480), (740, 560), (820, 620)]):
    for k in (-1, 0, 1):
        d.path(f"M{x},{y} C{x + k*5},{y - 10} {x + k*8},{y - 16} {x + k*10},{y - 22}",
               f"Algae {i*3+k+2}", fill=NONE, stroke="#5E6E38",
               strokeWidth=3, opacity=55, cap="round")
for i, (x, y, w) in enumerate([(210, 440, 18), (300, 480, 14), (770, 470, 20),
                               (730, 600, 15), (240, 620, 16)]):
    d.shape("ellipse", f"Pock {i+1}", x=x - w/2, y=y - w/3, width=w, height=w*0.66,
            fill="#100C06", opacity=55, stroke=NONE)

# sediment floor below the gap, closing on the arc
fy = 712
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C330,696 500,714 650,706 C740,700 820,704 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Sediment", fill="#26200F",
       opacity=85, stroke=NONE)
for i, (x, y, w) in enumerate([(330, 750, 12), (480, 762, 9), (620, 748, 13), (760, 756, 10)]):
    d.shape("ellipse", f"Rubble {i+1}", x=x - w/2, y=y - w/4, width=w, height=w*0.55,
            fill="#4A4028", opacity=50, stroke=NONE)

# === the eel ==========================================================================
# a body coil still in the shadow of the gap — the S below the surface
d.path("M560,690 C540,660 480,660 470,700 C464,728 500,742 540,738",
       "Coil", fill=NONE, stroke="#4A5228", strokeWidth=34, opacity=85, cap="round")

# dorsal fin — a translucent ribbon running the outer edge of the neck
d.path("M588,646 C600,586 588,530 560,488 C546,466 528,452 508,444",
       "Dorsal fin", fill=NONE, stroke="#7E8848", strokeWidth=13, opacity=55, cap="round")

# neck + head in one silhouette: rising out of the gap, bending left, jaws open
d.path("M575,735 C600,660 585,570 550,510 C525,470 495,452 460,445 "
       "C430,438 395,422 372,405 C364,398 356,398 354,406 "
       "C368,416 390,428 415,438 C428,444 438,450 448,458 "
       "C436,470 420,478 400,480 C392,481 388,476 394,470 "
       "C412,462 428,456 442,452 C450,470 462,490 470,510 "
       "C486,560 500,640 505,735 Z",
       "Eel", fill=EEL_GRAD, stroke=INK, strokeWidth=5)
# flank sheen along the outer curve
d.path("M580,700 C596,630 584,556 552,502 C538,478 520,462 498,452",
       "Neck sheen", fill=NONE, stroke="#C8CE8E", strokeWidth=6, opacity=35, cap="round")
# skin mottle — faint darker clouds on the neck
for i, (x, y, w, o) in enumerate([(540, 580, 30, 22), (560, 500, 26, 20),
                                  (505, 650, 34, 20), (470, 470, 22, 18)]):
    d.shape("ellipse", f"Mottle {i+1}", x=x - w/2, y=y - w/3, width=w, height=w*0.66,
            fill="#3E441E", opacity=o, stroke=NONE)

# mouth interior — the dark throat holding the second set of jaws
d.path("M362,404 C380,416 410,432 444,454 C432,466 414,474 398,476 "
       "C388,470 376,458 368,442 C362,428 360,414 362,404 Z",
       "Mouth", fill=MOUTH, stroke="#1A0A0C", strokeWidth=3)
# throat gleam deep inside — the murk of the throat
d.shape("ellipse", "Throat gleam", x=392, y=436, width=18, height=12,
        fill="#6E3038", opacity=60, stroke=NONE)

# needle teeth — fine pale triangles bristling into the gape, both jaws
upper_teeth = [(372, 412), (386, 420), (400, 428), (414, 436), (428, 444)]
lower_teeth = [(402, 472), (414, 466), (426, 460), (438, 454)]
for i, (x, y) in enumerate(upper_teeth):
    d.path(f"M{x},{y} L{x + 3},{y + 10} L{x + 6},{y + 1} Z",
           f"Tooth U{i+1}", fill=TEETH, opacity=85, stroke=NONE)
for i, (x, y) in enumerate(lower_teeth):
    d.path(f"M{x},{y} L{x + 3},{y - 9} L{x + 6},{y} Z",
           f"Tooth L{i+1}", fill=TEETH, opacity=85, stroke=NONE)
# jaw rim lights — the gape reads by its edges
d.path("M358,404 C376,416 404,432 444,454", "Upper jaw light", fill=NONE,
       stroke="#C8CE8E", strokeWidth=3.5, opacity=45, cap="round")
d.path("M396,476 C412,470 428,462 442,454", "Lower jaw light", fill=NONE,
       stroke="#C8CE8E", strokeWidth=3, opacity=40, cap="round")

# eye — small hard bead over the jaw hinge
d.shape("ellipse", "Eye", x=432, y=408, width=14, height=12,
        fill="#141006", stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Eye glint", x=436, y=410, width=3.5, height=3.5,
        fill="#FFF6DC", opacity=80, stroke=NONE)
# anterior nostril tubes — the moray's tell, two stubs on the snout
d.path("M362,396 C360,390 360,384 364,380", "Nostril tube 1", fill=NONE,
       stroke="#8E9452", strokeWidth=4, cap="round")
d.path("M372,398 C372,392 373,386 377,382", "Nostril tube 2", fill=NONE,
       stroke="#8E9452", strokeWidth=4, cap="round")
# gill opening — the small round pore behind the head
d.shape("ellipse", "Gill pore", x=476, y=462, width=11, height=11,
        fill="#181408", opacity=80, stroke=NONE)

# the cleaner wrasse — a slim attendant working the jaw corner
d.path("M470,428 C486,420 504,420 516,428 C504,436 486,436 470,428 Z",
       "Cleaner body", fill="#1C2830", stroke="#0C1216", strokeWidth=2)
d.path("M516,428 L530,422 L528,432 Z", "Cleaner tail",
       fill="#1C2830", stroke="#0C1216", strokeWidth=2)
d.path("M474,427 C488,424 504,424 514,428", "Cleaner stripe", fill=NONE,
       stroke="#C8DCE4", strokeWidth=2.5, opacity=80, cap="round")
d.shape("ellipse", "Cleaner eye", x=480, y=425, width=4, height=4,
        fill="#0C1216", stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0E1208", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
r1 = d.text("MORAY EEL", "Name", x=500, y=962, size=58, font="Virelai Sans",
            color="#C4D0A0", justify="center")

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

d.finish("moray-eel-V1R00")
