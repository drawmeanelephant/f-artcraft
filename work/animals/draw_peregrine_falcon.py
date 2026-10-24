#!/usr/bin/env python3
"""Peregrine falcon — field plate V1R00. Folded mid-stoop, diving down-left
past a sea-cliff pinnacle: slate back, wings swept to a blade, tail closed,
dark hood and bold malar stripe, barred cream underparts, yellow cere and
orbital ring. Cliff plate — updraft streaks rising off the crag, speed lines
in the wake, rocky floor closing on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Peregrine Falcon — Field Plate", 1000, 1000)
rng = random.Random(67)

PCX, PCY, PR = 500, 460, 420
INK = "#131110"   # warm near-black

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

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0B1218"), (1, "#030608"))
PLATE_GRAD = rad((0, "#5E7484"), (0.55, "#33444F"), (1, "#141F28"))
CRAG_GRAD  = lin(730, 320, 860, 780, (0, "#4E483E"), (0.6, "#332E26"), (1, "#181512"))
FLOOR_GRAD = lin(0, 770, 0, 880, (0, "#2E2A24"), (1, "#12100C"))
BACK_GRAD  = rad((0, "#5E7486"), (0.5, "#35454F"), (1, "#18232C"))
WING_GRAD  = lin(470, 480, 680, 340, (0, "#3E4E5A"), (1, "#1A2630"))
CREAM_GRAD = lin(380, 600, 640, 400, (0, "#F4ECD6"), (1, "#D2C4A0"))

# --- backdrop + cliff plate --------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#6E8492", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1E303C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D8E0", strokeWidth=3, opacity=28)

# pale sky light upper left — where the bird fell from
d.shape("ellipse", "Sky light", x=210, y=120, width=400, height=280,
        fill=radO((0, "#C2D4DC", 30), (0.6, "#C2D4DC", 12), (1, "#C2D4DC", 0)), stroke=NONE)
# thin scudding cloud
for i, dd in enumerate(["M170,230 C350,206 560,212 780,240",
                        "M200,330 C380,312 580,316 800,338"]):
    d.path(dd, f"Cloud {i+1}", fill=NONE, stroke="#18262E",
           strokeWidth=30, opacity=20, cap="round")
# wind-borne specks
for i, (x, y, w) in enumerate([(260, 200, 5), (720, 170, 5), (200, 440, 5),
                               (820, 480, 5), (390, 140, 4), (640, 130, 4)]):
    assert on_disc(x, y, 10), (x, y)
    d.shape("ellipse", f"Speck {i+1}", x=x - w / 2, y=y - w / 2, width=w, height=w,
            fill="#D8E4EA", opacity=35, stroke=NONE)

# --- updraft: air racing up the cliff face ------------------------------------------
for i, dd in enumerate(["M680,720 C670,630 674,560 684,490",
                        "M650,700 C640,620 644,550 654,480",
                        "M706,680 C698,610 702,540 710,480"]):
    d.path(dd, f"Updraft {i+1}", fill=NONE, stroke="#B8CCD6",
           strokeWidth=4, opacity=22, cap="round")
# speed lines trailing off the swept wingtips
for i, dd in enumerate(["M695,295 L728,268", "M715,325 L746,300", "M660,285 L690,262"]):
    d.path(dd, f"Wake {i+1}", fill=NONE, stroke="#C8DCE4",
           strokeWidth=3, opacity=40, cap="round")

# --- rocky floor closing on the disc's own arc ---------------------------------------
fy = 775
fx0, fx1 = disc_x(fy, -1), disc_x(fy, 1)
d.path(f"M{fx0:.1f},{fy} C320,760 680,760 {fx1:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fx0:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fx0 + 6:.1f},{fy} C320,760 680,760 {fx1 - 6:.1f},{fy}",
       "Floor edge light", fill=NONE, stroke="#7E7668", strokeWidth=3, opacity=30, cap="round")
for i, dd in enumerate(["M280,810 C420,800 580,802 700,810", "M350,845 C470,838 590,840 660,846"]):
    d.path(dd, f"Stratum {i+1}", fill=NONE, stroke="#1C1A14",
           strokeWidth=4, opacity=50, cap="round")

# --- the cliff face: a wall hugging the right rim, closing on the disc arc -------------
# top/bottom chord points on the right rim; the arc between them is the wall's right edge
cy_t, cy_b = 160, 760
cx_t, cx_b = disc_x(cy_t, 1), disc_x(cy_b, 1)
d.path(f"M{cx_t:.1f},{cy_t} "
       "C780,190 750,220 756,260 C762,300 730,330 736,370 "
       "C742,410 700,430 708,470 C716,510 690,540 700,580 "
       "C708,620 720,660 716,690 C714,720 740,742 %.1f,%d "
       f"A{PR},{PR} 0 0 0 {cx_t:.1f},{cy_t} Z" % (cx_b, cy_b),
       "Cliff face", fill=CRAG_GRAD, stroke=INK, strokeWidth=4)
# pale light running down the jagged left edge
d.path("M780,195 C765,230 752,260 758,300 C764,340 734,360 740,400 "
       "C746,430 706,450 712,490 C716,520 695,545 704,580 C710,615 722,655 720,690",
       "Cliff edge light", fill=NONE, stroke="#8E8474", strokeWidth=7, opacity=35, cap="round")
# vertical crack + strata following the face
for i, dd in enumerate(["M780,300 C776,380 786,460 778,540", "M812,600 C808,650 814,700 808,750"]):
    d.path(dd, f"Crack {i+1}", fill=NONE, stroke="#14120E",
           strokeWidth=3.5, opacity=60, cap="round")
for i, dd in enumerate(["M760,260 C790,252 810,258 822,268", "M740,420 C780,410 812,416 828,428",
                        "M730,560 C775,552 815,558 840,570", "M758,680 C798,672 828,678 848,688"]):
    d.path(dd, f"Strata {i+1}", fill=NONE, stroke="#201D18",
           strokeWidth=4, opacity=55, cap="round")
for i, (x, y) in enumerate([(772, 300), (800, 380), (762, 500), (802, 560), (782, 660), (810, 460)]):
    d.shape("ellipse", f"Lichen {i+1}", x=x - 5, y=y - 4, width=10, height=8,
            fill="#8E9678", opacity=40, stroke=NONE)

# === the falcon =====================================================================
# far wing: the darker blade peeking over the back
d.path("M512,441.8 C595.2,370.2 684.8,306.2 761.6,275.4 "
       "C753.9,293.4 738.6,306.2 715.5,319 C633.6,370.2 563.2,421.4 512,470 Z",
       "Far wing", fill="#161E26", stroke=INK, strokeWidth=3)

# body: the stoop teardrop, head low-left, tail closed up-right
BODY = ("M336.6,600.6 C346.9,569.8 357.1,546.8 367.4,539.1 "
        "C385.3,523.8 395.5,518.6 408.3,516.1 "
        "C480,480.2 582.4,429 669.4,380.4 C684.8,372.7 695,367.6 705.3,362.5 "
        "L695,390.6 C633.6,436.7 531.2,514.8 444.2,595.4 "
        "C426.2,610.8 408.3,621 390.4,623.6 C367.4,626.2 349.4,618.5 336.6,600.6 Z")
d.path(BODY, "Body", fill=BACK_GRAD, stroke=INK, strokeWidth=6.5)

# near wing: swept back over the body, tip reaching past the tail
d.path("M467.2,480.2 C556.8,406 661.8,336.9 738.6,301 "
       "C725.8,319 707.8,331.8 684.8,344.6 "
       "C592.6,416.2 512,470 451.8,511 C451.8,498.2 457,487.9 467.2,480.2 Z",
       "Near wing", fill=WING_GRAD, stroke=INK, strokeWidth=4.5)
# leading-edge light + primary seams
d.path("M485.1,472.6 C567,406 656.6,344.6 723.2,313.8", "Wing light", fill=NONE,
       stroke="#8EA4B2", strokeWidth=5, opacity=40, cap="round")
for i, dd in enumerate(["M582.4,431.6 C628.2,364.8 679.9,344.6 720.6,344.6",
                        "M544,459.8 C590.1,421.4 646.4,388.1 692.5,364.9",
                        "M628.5,411.1 C664.6,367.4 697.6,367.6 725.8,354.8"]):
    d.path(dd, f"Primary seam {i+1}", fill=NONE, stroke="#141C24",
           strokeWidth=3.5, opacity=55, cap="round")

# tail banding across the closed point
for i, (x, y) in enumerate([(656.6, 390.6), (677.1, 377.8), (633.6, 403.4)]):
    d.path(f"M{x - 12:.1f},{y - 7:.1f} L{x + 12:.1f},{y + 7:.1f}", f"Tail band {i+1}",
           fill=NONE, stroke="#141C24", strokeWidth=4.5, opacity=50, cap="round")

# barred cream underparts along the belly's lower edge
d.path("M444.2,595.4 C531.2,514.8 620.8,444.4 695,390.6 "
       "C659.2,444.4 582.4,528.9 480,595.4 C467.2,603.1 454.4,603.1 444.2,595.4 Z",
       "Underparts", fill=CREAM_GRAD, opacity=92, stroke=NONE)
for i, (x, y, w) in enumerate([(505.6, 559.6, 23), (556.8, 518.6, 22), (608, 475.1, 20),
                               (656.6, 434.2, 19), (467.2, 582.6, 19)]):
    d.path(f"M{x - w / 2:.1f},{y + 5:.1f} Q{x:.1f},{y - 7:.1f} {x + w / 2:.1f},{y - 2:.1f}",
           f"Belly bar {i+1}", fill=NONE, stroke="#4A3E2C", strokeWidth=4,
           opacity=65, cap="round")
# === head: hood, cheek, malar stripe =================================================
# slate hood over crown and nape
d.path("M336.6,600.6 C346.9,569.8 357.1,546.8 367.4,539.1 "
       "C385.3,523.8 395.5,518.6 408.3,516.1 "
       "C421.1,521.2 428.8,536.6 428.8,551.5 "
       "C416,570.2 395.5,580.1 375,580.1 C357.1,580.1 344.3,592.5 336.6,600.6 Z",
       "Hood", fill="#1E2830", stroke=INK, strokeWidth=3.5)
# cream cheek patch under the hood
d.path("M367.4,575 C390.4,572.4 413.4,559.6 426.2,544.2 "
       "C431.4,569.8 421.1,598 398.1,613.4 "
       "C382.7,623.6 362.2,621 352,610.2 C354.6,592.9 359.7,582.6 367.4,575 Z",
       "Cheek", fill=CREAM_GRAD, opacity=95, stroke=NONE)
# the malar stripe: the falcon's bold mustache dropping off the eye
d.path("M375,569.8 C385.3,567.3 393,572.4 393,582.6 "
       "C393,595.4 385.3,610.8 375,618.5 "
       "C367.4,610.8 364.8,595.4 367.4,582.6 C368.6,575 371.8,572.4 375,569.8 Z",
       "Malar", fill="#1E2830", stroke=NONE)
# eye with its yellow orbital ring
d.shape("ellipse", "Orbital ring", x=362, y=544, width=28, height=28,
        fill="#E8BC3C", opacity=90, stroke=NONE)
d.shape("ellipse", "Eye", x=367, y=549, width=18, height=18, fill="#0C0E10", stroke=NONE)
d.shape("ellipse", "Eye glint", x=371, y=552, width=5.5, height=5.5,
        fill="#FFFFFF", opacity=85, stroke=NONE)
# the beak: small dark hook, yellow cere at its base
d.path("M334.1,585.2 C327.7,592.9 326.4,603.1 331.5,610.8 "
       "C336.6,617.2 346.9,614.6 350.7,607 "
       "C344.3,604.4 340.5,599.3 341.8,591.6 C340.5,586.5 336.6,583.9 334.1,585.2 Z",
       "Beak", fill="#232E38", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Cere", x=339.3, y=580.2, width=11, height=10,
        fill="#E8BC3C", opacity=90, stroke=NONE)

# back sheen along the dorsal line
d.path("M428.8,523.8 C505.6,490.5 595.2,444.4 672,395.7", "Back sheen", fill=NONE,
       stroke="#8EA4B2", strokeWidth=7, opacity=25, cap="round")

# plate rim on top so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#0C1820", strokeWidth=6)
d.shape("ellipse", "Plate inner ring 2", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D8E0", strokeWidth=3, opacity=25)

# --- name ----------------------------------------------------------------------------
r1 = d.text("PEREGRINE FALCON", "Name", x=500, y=962, size=52, font="Virelai Sans",
            color="#DCE6EA", justify="center")

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

d.finish("peregrine-falcon-V1R00")
