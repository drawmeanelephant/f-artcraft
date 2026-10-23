#!/usr/bin/env python3
"""Scarlet ibis — field-guide plate V1R00. Full figure wading in profile,
facing left: lacquer-scarlet body, long decurved bill drawn as one tapering
crescent, black-tipped folded wing, thin stilt legs in a shallow lagoon band
closing on the disc's own arc. Deep red-on-ink plate. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Scarlet Ibis — Field Plate", 1000, 1000)

INK = "#2A0C12"
CX, CY, R = 500, 460, 420
BG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#2A1218"}, {"offset": 1, "color": "#0A0407"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#9E3540"}, {"offset": 0.62, "color": "#6E1F2C"},
    {"offset": 1, "color": "#3E1220"}]}}
WATER_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#4E1620"}, {"offset": 1, "color": "#2A0A14"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FF6A52"}, {"offset": 0.55, "color": "#E02830"},
    {"offset": 1, "color": "#9E1224"}]}}
WING_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#E8313A"}, {"offset": 1, "color": "#8E1222"}]}}
NECK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FF5E48"}, {"offset": 0.6, "color": "#D82430"},
    {"offset": 1, "color": "#981426"}]}}
BILL_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#6E2A30"}, {"offset": 0.45, "color": "#33121A"},
    {"offset": 1, "color": "#120609"}]}}
LEG_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#7A2430"}, {"offset": 1, "color": "#2E0E16"}]}}
REED_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#7E3A40"}, {"offset": 1, "color": "#411B22"}]}}

def chord_x(y, r=R):
    h = math.sqrt(r*r - (y - CY)**2)
    return CX - h, CX + h

def rim_y(x):
    return CY + math.sqrt(R*R - (x - CX)**2)

def clamp(x, y, r=400):
    dx, dy = x - CX, y - CY
    k = math.hypot(dx, dy)
    return (x, y) if k <= r else (CX + dx*r/k, CY + dy*r/k)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8E3A42", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E88A80", strokeWidth=3, opacity=45)
# lacquer patina: darker and lighter red blotches + ember flecks
d.shape("ellipse", "Patina 1", x=180, y=180, width=240, height=140, fill="#C04850", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=580, y=580, width=250, height=130, fill="#2E0C14", opacity=24, stroke=NONE)
for i, (x, y, w) in enumerate([(210,300,7),(770,240,6),(170,540,8),(830,430,6),
                               (270,150,6),(640,120,7),(140,660,6),(860,600,6)]):
    d.shape("ellipse", f"Ember fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#E86A5A", opacity=35, stroke=NONE)

# --- reeds rising from the lagoon, roots + tips clamped inside the disc --------
def reed(label, bx, lean, h, w=11, by=764):
    top = clamp(bx + lean, by - h)
    bl = clamp(bx - w/2, by); br = clamp(bx + w/2, by)
    c1 = (bx - lean*0.35, by - h*0.5)
    d.path(f"M{bl[0]:.0f},{bl[1]:.0f} Q{c1[0] - w/2:.0f},{c1[1]:.0f} {top[0]:.0f},{top[1]:.0f} "
           f"Q{c1[0] + w/2:.0f},{c1[1]:.0f} {br[0]:.0f},{br[1]:.0f} Z",
           label, fill=REED_GRAD, opacity=85, stroke=NONE)
    return top
tops = []
for i, (bx, lean, h) in enumerate([(222,26,150),(250,-14,190),(280,34,120)]):
    tops.append(reed(f"Reed {i+1}", bx, lean, h))
# right-rim reeds, shorter
for i, (bx, lean, h) in enumerate([(742,-30,120),(766,10,80)]):
    reed(f"Reed R{i+1}", bx, lean, h)
# seed heads sit on the reed tips
for i, t in enumerate(tops[:2]):
    d.shape("ellipse", f"Seed head {i+1}", x=t[0]-8, y=t[1]-14, width=16, height=44,
            fill="#5E2A30", opacity=90, stroke=INK, strokeWidth=3)

# --- lagoon band: closes on the disc's own arc ---------------------------------
wl, wr = chord_x(764)
d.path(f"M{wl:.1f},764 C360,748 640,748 {wr:.1f},764 A420,420 0 0 1 {wl:.1f},764 Z",
       "Lagoon", fill=WATER_GRAD, stroke=NONE)
d.path(f"M{wl+22:.1f},762 C370,750 630,750 {wr-22:.1f},762", "Water light",
       fill=NONE, stroke="#F0A090", strokeWidth=4, opacity=35, cap="round")
for i, (x, y, w) in enumerate([(330,792,60),(520,806,80),(660,790,54),(430,826,70),(590,840,60)]):
    d.shape("ellipse", f"Ripple {i+1}", x=x-w/2, y=y, width=w, height=w/5,
            fill="#E8786A", opacity=22, stroke=NONE)
# re-stroke the rim over the lagoon so the plate edge stays continuous
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#8E3A42", strokeWidth=6)
d.shape("ellipse", "Plate inner ring over water", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E88A80", strokeWidth=3, opacity=30)
d.shape("ellipse", "Ibis shadow", x=370, y=756, width=280, height=22,
        fill="#18060C", opacity=40, stroke=NONE)

# --- legs: stilt-thin, drawn before the body so tops tuck under it --------------
def leg(label, hip, ankle, foot, far=False):
    hx, hy = hip; ax, ay = ankle; fx, fy = foot
    fill = "#3E1420" if far else LEG_GRAD
    op = 75 if far else 100
    d.path(f"M{hx-6},{hy} C{hx-7},{(hy+ay)/2:.0f} {ax-5},{ay-40} {ax-4},{ay} "
           f"L{fx-3},{fy-6} M{hx+6},{hy} C{hx+7},{(hy+ay)/2:.0f} {ax+5},{ay-40} {ax+4},{ay} "
           f"L{fx+3},{fy-6}",
           f"{label} bone", fill=NONE, stroke=fill, strokeWidth=8, opacity=op, cap="round")
    # ankle joint knot
    d.shape("ellipse", f"{label} ankle", x=ax-7, y=ay-7, width=14, height=14,
            fill=fill, opacity=op, stroke=NONE)
    # toes: three short strokes splaying into the water
    for k, (dx, dy) in enumerate([(-16,7),(0,11),(16,7)]):
        d.path(f"M{fx},{fy-6} L{fx+dx},{fy+dy}", f"{label} toe {k+1}",
               fill=NONE, stroke=fill, strokeWidth=3.5, opacity=op, cap="round")

leg("Far leg", (562,612), (576,716), (588,782), far=True)
leg("Near leg", (500,612), (492,712), (500,780))
# leg reflections in the lagoon
for i, x in enumerate([(500,), (588,)]):
    d.path(f"M{x[0]-4},800 L{x[0]-6},850 M{x[0]+4},802 L{x[0]+5},844",
           f"Leg reflection {i+1}", fill=NONE, stroke="#7E2A34",
           strokeWidth=4, opacity=30, cap="round")

# --- body: plump scarlet teardrop, back held high ------------------------------
d.path("M428,560 C440,516 492,492 560,490 C632,488 694,508 736,544 "
       "C758,564 776,578 800,584 C792,600 764,606 736,602 "
       "C706,624 646,642 574,642 C506,642 450,620 432,592 "
       "C422,578 422,568 428,560 Z",
       "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
# folded wing: darker scarlet coverts + ink-black primaries trailing right
d.path("M520,506 C600,496 680,514 736,548 C764,566 786,580 806,586 "
       "C800,598 776,604 750,600 C700,610 620,600 560,576 "
       "C528,562 514,534 520,506 Z",
       "Wing", fill=WING_GRAD, opacity=85, stroke=NONE)
d.path("M524,508 C600,500 676,516 730,548", "Wing fold line", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=45, cap="round")
# black wingtip mass: the folded primaries read as one dark paddle with
# notched feather ends, rooted deep inside the body silhouette
t1 = clamp(806, 596); t2 = clamp(776, 632); t3 = clamp(730, 656)
d.path("M560,540 C630,540 700,556 756,578 "
       f"C772,584 790,588 {t1[0]:.0f},{t1[1]:.0f} "
       f"C{ t1[0]-24:.0f},{t1[1]+10:.0f} {t2[0]+16:.0f},{t2[1]-14:.0f} {t2[0]:.0f},{t2[1]:.0f} "
       f"C{t2[0]-30:.0f},{t2[1]-2:.0f} {t3[0]+18:.0f},{t3[1]-16:.0f} {t3[0]:.0f},{t3[1]:.0f} "
       "C660,636 600,612 560,580 C548,566 550,550 560,540 Z",
       "Wingtip black", fill="#160A10", stroke=INK, strokeWidth=5, opacity=95)
# feather separations inside the black tip
for i, (x0, y0, x1, y1) in enumerate([(700,566,780,600),(672,586,744,622),(648,604,706,644)]):
    d.path(f"M{x0},{y0} C{x0+30},{y0+8} {x1-30},{y1-6} {x1},{y1}",
           f"Primary split {i+1}", fill=NONE, stroke="#3E2430",
           strokeWidth=4, opacity=80, cap="round")
d.path("M600,552 C660,556 720,574 766,592", "Wingtip sheen", fill=NONE,
       stroke="#6E4658", strokeWidth=5, opacity=45, cap="round")
# lacquer sheen + shading on the body
d.path("M452,540 C520,506 620,502 700,528", "Back lacquer sheen", fill=NONE,
       stroke="#FFC0A8", strokeWidth=9, opacity=40, cap="round")
d.path("M440,600 C510,630 620,634 700,610", "Belly shade", fill=NONE,
       stroke="#5E0C18", strokeWidth=12, opacity=30, cap="round")
d.shape("ellipse", "Breast glow", x=436, y=548, width=120, height=56,
        fill="#FF8A70", opacity=18, stroke=NONE)
# scarlet feather texture: short translucent strokes along the flank
for i, dd in enumerate(["M560,560 C590,570 620,572 648,566", "M540,584 C580,596 624,598 662,588",
                        "M600,540 C640,548 676,556 706,570"]):
    d.path(dd, f"Flank feather {i+1}", fill=NONE, stroke="#8E1220",
           strokeWidth=4, opacity=45, cap="round")

# --- neck: slender S rising from the breast -------------------------------------
d.path("M438,566 C414,516 396,462 387,408 C381,374 378,344 382,318 "
       "L410,310 C408,340 412,372 421,406 C432,450 448,500 466,540 Z",
       "Neck", fill=NECK_GRAD, stroke=INK, strokeWidth=6)
d.path("M394,400 C387,368 385,342 389,322", "Neck sheen", fill=NONE,
       stroke="#FFB09A", strokeWidth=6, opacity=40, cap="round")
d.path("M456,530 C440,492 426,452 419,412", "Neck shade", fill=NONE,
       stroke="#7E1020", strokeWidth=8, opacity=30, cap="round")

# --- head + bare face: wedge flowing into the bill ------------------------------
d.path("M368,316 C356,298 358,276 374,262 C392,246 422,246 442,262 "
       "C456,274 458,294 448,310 C436,326 414,334 394,332 "
       "C380,330 372,326 368,316 Z",
       "Head", fill=NECK_GRAD, stroke=INK, strokeWidth=6)
# bare skin patch around the bill base + eye: deeper crimson
d.path("M372,312 C364,292 372,270 394,262 C410,256 428,260 438,272 "
       "C428,286 416,302 404,318 C392,320 380,318 372,312 Z",
       "Face skin", fill="#8E1624", opacity=85, stroke=NONE)
d.path("M384,266 C400,256 422,256 438,268", "Crown sheen", fill=NONE,
       stroke="#FFB09A", strokeWidth=5, opacity=45, cap="round")
# eye
d.shape("ellipse", "Eye ring", x=392, y=278, width=24, height=22, fill="#D8503E", opacity=60, stroke=NONE)
d.shape("ellipse", "Eye", x=398, y=282, width=13, height=13, fill="#14060A", stroke=NONE)
d.shape("ellipse", "Eye glint", x=401, y=284, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)

# --- bill: one long tapering crescent, decurved ----------------------------------
# upper edge sweeps down-left; lower edge returns a touch shallower
d.path("M388,296 C340,306 288,338 248,386 C224,414 204,444 190,476 "
       "C188,482 184,484 182,480 C184,470 190,452 200,432 "
       "C222,388 262,344 306,318 C336,302 366,294 388,296 Z",
       "Bill", fill=BILL_GRAD, stroke=INK, strokeWidth=4)
# red root where the bill meets the face
d.path("M384,298 C366,302 350,308 336,316 C350,306 366,300 384,298 Z",
       "Bill root", fill="#B23038", stroke=NONE)
# lacquer highlight along the upper ridge
d.path("M376,302 C334,314 290,344 256,386 C238,408 222,432 210,456",
       "Bill sheen", fill=NONE, stroke="#C86458", strokeWidth=4, opacity=65, cap="round")
# lower-edge shade
d.path("M330,326 C296,348 264,380 242,414", "Bill shade", fill=NONE,
       stroke="#08040A", strokeWidth=4, opacity=50, cap="round")
# nostril slit near the base
d.path("M368,304 C356,308 346,312 338,318", "Nostril", fill=NONE,
       stroke="#0A0408", strokeWidth=3, opacity=80, cap="round")

# --- name ----------------------------------------------------------------------
d.text("SCARLET IBIS", "Name", x=500, y=962, size=54, font="Virelai Sans",
       color="#EFC9BE", justify="center")

d.finish("ibis-V1R00")
