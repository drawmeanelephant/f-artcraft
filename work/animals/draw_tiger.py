#!/usr/bin/env python3
"""Tiger — field-guide plate V1R00. Face-forward portrait: burnt-orange coat,
white cheek ruffs, the 'king' mark on the forehead, a level amber stare.
Jungle-green plate under a dark backdrop, a hush of monsoon mist across the
middle distance, tall grass rising from a floor that closes on the disc's own
arc — the grass blades rhyme with the stripes. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Tiger — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#1C1208"
STRIPE = "#221408"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def mirror(dd):
    out, toks, ex = [], re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd), True
    for t in toks:
        if t.isalpha():
            out.append(t); ex = True
        elif ex:
            out.append(f"{1000 - float(t):g},"); ex = False
        else:
            out[-1] += f"{float(t):g}"; ex = True
    return " ".join(out)

def pair(dd, label, **kw):
    d.path(dd, f"{label} L", **kw)
    d.path(mirror(dd), f"{label} R", **kw)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#12200F"), (1, "#050A04"))
PLATE_GRAD = rad((0, "#93B08A"), (0.55, "#67855F"), (1, "#3E5A42"))
COAT_GRAD = rad((0, "#F4AC4E"), (0.6, "#DE8A2E"), (1, "#A85E14"))
PALE_GRAD = rad((0, "#FBF6E8"), (1, "#E4D6B8"))
GRASS_GRAD = lin(0, 730, 0, 880, (0, "#4E6B48"), (1, "#22351F"))

# --- backdrop + jungle plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#67855F", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2A4230", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4F0DC", strokeWidth=3, opacity=40)
# canopy gloom at the top corners + hanging leaves
d.path("M104,240 C160,180 230,150 300,140 C250,180 200,240 180,300 C150,290 120,270 104,240 Z",
       "Canopy L", fill="#2E4A34", opacity=55, stroke=NONE)
d.path("M896,230 C840,175 770,148 700,140 C755,180 800,235 822,295 C852,285 880,262 896,230 Z",
       "Canopy R", fill="#2E4A34", opacity=55, stroke=NONE)
for i, (x, y, w, h, r_) in enumerate([(170,330,20,44,-18),(218,290,16,38,14),(800,300,18,42,20),(846,340,15,36,-12)]):
    assert on_disc(x + w/2, y + h/2, 25), (x, y)
    d.shape("ellipse", f"Leaf {i+1}", x=x, y=y, width=w, height=h, fill="#3E5E42", opacity=50, stroke=NONE)
# monsoon hush: a mist band across the middle distance
for i, (y, h, op) in enumerate([(300, 60, 20), (350, 44, 16), (392, 30, 12)]):
    d.shape("ellipse", f"Mist {i+1}", x=140, y=y, width=720, height=h,
            fill="#DCE8D8", opacity=op, stroke=NONE)
# faint rain threads, upper left
for i, (x, y, ln_) in enumerate([(240,180,56),(300,150,44),(372,190,50),(640,170,48),
                                 (716,200,52),(780,150,40),(196,240,38),(830,230,42)]):
    d.path(f"M{x},{y} L{x-10},{y+ln_}", f"Rain {i+1}", fill=NONE,
           stroke="#CFE0CC", strokeWidth=2.5, opacity=18, cap="round")

# tall-grass floor: top edge sways, bottom closes on the disc arc
ly = 742
ldx = math.sqrt(R * R - (ly - CY) ** 2)
d.path(f"M{CX-ldx:.1f},{ly} C300,728 420,736 520,732 C630,728 700,734 {CX+ldx:.1f},{ly} "
       f"A{R},{R} 0 0 1 {CX-ldx:.1f},{ly} Z", "Grass floor", fill=GRASS_GRAD, stroke=NONE)
# tall blades rising from the floor — stripe-rhythm silhouettes
for i, (x, h, bend) in enumerate([(196,120,-24),(252,150,18),(310,104,-14),(372,140,26),
                                  (438,90,-18),(566,96,16),(628,146,-22),(690,110,18),
                                  (748,142,-16),(806,96,20),(160,84,-14),(852,72,12)]):
    for j, dx in enumerate([-9, 0, 9]):
        x0 = x + dx
        x1 = x0 + bend * (0.8 + 0.2 * j)
        d.path(f"M{x0},{ly+10} Q{x0+bend*0.4},{ly-h*0.55} {x1},{ly-h*(0.9+0.1*j)}",
               f"Blade {i+1}.{j+1}", fill=NONE,
               stroke="#1E3018" if j != 1 else "#33502C", strokeWidth=5 if j == 1 else 4,
               opacity=60, cap="round")
# dew flecks
for i, (x, y, w) in enumerate([(200,300,4),(810,300,5),(170,480,5),(840,470,4),(250,620,4),
                               (760,640,5),(150,400,4),(860,390,4),(420,110,4),(600,120,5),
                               (330,130,4),(700,140,4),(320,800,5),(670,806,4),(500,846,4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Dew {i+1}", x=x, y=y, width=w, height=w, fill="#E4F0DC", opacity=35, stroke=NONE)

# --- ears: dark backs with a pale flash, tucked behind the crown ------------------
EAR = "M398,368 C378,350 376,318 394,298 C412,280 444,280 460,296 C472,310 472,336 458,356 C442,374 416,380 398,368 Z"
pair(EAR, "Ear", fill=rad((0, "#4A2E14"), (1, "#221408")), stroke=INK, strokeWidth=5)
pair("M404,348 C392,336 392,316 402,304 C412,294 430,294 440,304 C448,314 446,332 434,344 C424,352 412,354 404,348 Z",
     "Ear flash", fill=PALE_GRAD, opacity=65, stroke=NONE)

# --- head ------------------------------------------------------------------------------
HEAD = ("M500,320 C578,320 646,366 662,440 C674,498 658,556 614,596 "
        "C588,620 544,634 500,634 C456,634 412,620 386,596 "
        "C342,556 326,498 338,440 C354,366 422,320 500,320 Z")
d.path(HEAD, "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# cheek ruffs: white fans flaring below the cheeks
RUFF = ("M352,470 C330,500 322,540 336,574 C312,586 306,616 322,638 "
        "C346,664 390,668 424,650 C444,638 452,612 444,588 C432,556 424,524 428,494 Z")
pair(RUFF, "Cheek ruff", fill=PALE_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M336,540 C356,546 376,544 392,534",
                        "M330,584 C352,592 374,592 392,584",
                        "M342,624 C362,632 384,632 402,624"]):
    pair(dd, f"Ruff fur {i+1}", fill=NONE, stroke="#C8B890", strokeWidth=4, opacity=45, cap="round")
# white chin + throat
d.path("M440,600 C460,640 540,640 560,600 C556,660 444,660 440,600 Z",
       "Throat white", fill=PALE_GRAD, opacity=90, stroke=NONE)

# crown shade + brow light
d.shape("ellipse", "Brow light", x=425, y=345, width=150, height=46, fill="#FFD894", opacity=22, stroke=NONE)

# --- stripes: the 'king' mark on the forehead -------------------------------------------
for i, (x0, y0, x1, y1, w_) in enumerate([(470,330,452,392,10),(500,322,500,386,11),(530,330,548,392,10),
                                          (440,344,414,400,9),(560,344,586,400,9)]):
    d.path(f"M{x0},{y0} Q{(x0+x1)/2},{(y0+y1)/2-10} {x1},{y1}", f"Crown stripe {i+1}",
           fill=NONE, stroke=STRIPE, strokeWidth=w_, opacity=90, cap="round")
# temple fans: stripes sweeping back toward the ears
for i, dd in enumerate(["M370,360 C400,370 420,388 432,410",
                        "M356,398 C388,406 410,422 424,442",
                        "M350,438 C384,444 406,458 418,476"]):
    pair(dd, f"Temple stripe {i+1}", fill=NONE, stroke=STRIPE, strokeWidth=9, opacity=85, cap="round")
# cheek-edge stripes above the ruff
for i, dd in enumerate(["M352,482 C380,486 400,494 414,506",
                        "M348,518 C378,522 398,530 410,540"]):
    pair(dd, f"Cheek stripe {i+1}", fill=NONE, stroke=STRIPE, strokeWidth=8, opacity=80, cap="round")

# --- the stare ---------------------------------------------------------------------------
EYE = "M412,434 C432,414 468,412 488,432 C472,452 434,454 412,434 Z"
pair(EYE, "Eye", fill=rad((0, "#F2BC4C"), (0.6, "#C88A24"), (1, "#7A4E10")),
     stroke=INK, strokeWidth=5)
d.shape("ellipse", "Pupil L", x=448, y=426, width=12, height=14, fill="#120A04", stroke=NONE)
d.shape("ellipse", "Pupil R", x=540, y=426, width=12, height=14, fill="#120A04", stroke=NONE)
d.shape("ellipse", "Glint L", x=451, y=429, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=543, y=429, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
# heavy level lids — the stare that doesn't vanish
pair("M408,432 C430,412 470,410 492,430", "Upper lid",
     fill=NONE, stroke=INK, strokeWidth=8, cap="round")
pair("M414,412 C436,398 466,396 488,406", "Brow shadow",
     fill=NONE, stroke="#8A5A18", strokeWidth=8, opacity=30, cap="round")
pair("M420,448 C438,454 462,452 478,442", "Lower lid light",
     fill=NONE, stroke="#FFE8B0", strokeWidth=4, opacity=50, cap="round")

# --- muzzle --------------------------------------------------------------------------------
d.path("M500,452 C530,452 552,472 562,498 C590,506 606,530 602,560 "
       "C598,594 556,614 500,614 C444,614 402,594 398,560 "
       "C394,530 410,506 438,498 C448,472 470,452 500,452 Z",
       "Muzzle pale", fill=PALE_GRAD, opacity=92, stroke=NONE)
d.path("M470,492 C482,484 518,484 530,492 C534,508 522,524 500,528 C478,524 466,508 470,492 Z",
       "Nose", fill=lin(0, 484, 0, 528, (0, "#C07A6A"), (1, "#7A3E30")), stroke=INK, strokeWidth=4)
d.shape("ellipse", "Nose glint", x=482, y=491, width=12, height=5, fill="#FFD8C8", opacity=45, stroke=NONE)
d.path("M500,528 L500,546", "Philtrum", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
pair("M500,546 C488,556 470,560 454,556", "Mouth",
     fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M474,598 C490,606 510,606 526,598", "Chin shade",
     fill=NONE, stroke="#C8B890", strokeWidth=7, opacity=30, cap="round")
# whisker dots + whiskers
for j, (x, y) in enumerate([(436,518),(452,524),(432,532),(448,538),(464,520),(458,532)]):
    d.shape("ellipse", f"Whisker dot L{j+1}", x=x-3, y=y-3, width=6, height=6,
            fill="#6E4A1E", opacity=55, stroke=NONE)
    d.shape("ellipse", f"Whisker dot R{j+1}", x=1000-x-3, y=y-3, width=6, height=6,
            fill="#6E4A1E", opacity=55, stroke=NONE)
for j, (x1, y1, x2, y2) in enumerate([(444,520,330,496),(446,530,322,522),(450,540,336,550)]):
    pair(f"M{x1},{y1} Q{(x1+x2)/2},{min(y1,y2)-8} {x2},{y2}", f"Whisker {j+1}",
         fill=NONE, stroke="#FFF6E0", strokeWidth=2, opacity=55, cap="round")

# foreground blades crossing the ruff tips — the stripes vanish in tall grass
for i, (x, h, bend) in enumerate([(346, 96, -14), (654, 96, 14), (306, 74, 10), (694, 74, -10)]):
    d.path(f"M{x},{ly+12} Q{x+bend*0.4},{ly+12-h*0.55} {x+bend},{ly+12-h}",
           f"Front blade {i+1}", fill=NONE, stroke="#1E3018", strokeWidth=4.5,
           opacity=70, cap="round")

# --- caption --------------------------------------------------------------------------------
d.text("TIGER", "Name", x=500, y=942, size=60, font="Virelai Sans",
       color="#E4F0DC", justify="center")
o = d.text("PANTHERA TIGRIS", "Binomial", x=500, y=976, size=22, font="Virelai Sans",
           color="#A8C49E", justify="center")
if o and "id" in o:
    d.cmd("text.setStyle", "Binomial tracking", ids=[o["id"]], tracking=400)

d.finish("tiger-V1R00")
