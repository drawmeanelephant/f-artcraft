#!/usr/bin/env python3
"""Pallas's cat — field-guide plate V1R00. Face-forward: the flattest, widest,
grumpiest face on the steppe. Low-set ears drowned in dense fur, amber eyes
squinting under a heavy flat brow, round pupils, cheeks massed in layered
gradient tufts. Cold stone-grey plate with a strip of wind-blown snow.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Pallas's Cat — Field Plate", 1000, 1000)

INK = "#2E2C2A"
CX, CY, R = 500, 460, 420          # plate disc centre + radius

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#1F2630"), (1, "#080C11"))
PLATE_GRAD = rad((0, "#DDE0DA"), (0.7, "#ADB3AC"), (1, "#6F7A72"))
FUR_GRAD  = rad((0, "#CFCBBB"), (0.55, "#A5A193"), (1, "#6E6A5E"))
FUR_DARK  = lin(0, 300, 0, 560, (0, "#6E6A5E"), (1, "#8B8779"))
FACE_GRAD = rad((0, "#DDD9CB"), (0.6, "#BDB9AA"), (1, "#8B8779"))
IRIS_GRAD = rad((0, "#F6C95C"), (0.6, "#DE9A2E"), (1, "#9C5E12"))
EAR_GRAD  = lin(0, 380, 0, 480, (0, "#5C584E"), (1, "#837F71"))
SNOW_GRAD = lin(0, 790, 0, 880, (0, "#E8ECE8"), (1, "#B9C2BC"))

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

def disc_x(y, side, r=420):
    return CX + side*math.sqrt(r*r - (y - CY)**2)

def fluff(cx, cy, rx, ry, n, depth, label, squash_top=None, **kw):
    """Tuft-edged blob: alternating outer tips / inner notches around an ellipse."""
    pts = []
    steps = n * 2
    for i in range(steps):
        a = 2*math.pi*i/steps - math.pi/2     # start at the top
        rr = 1.0 if i % 2 == 0 else 1.0 - depth
        x, y = cx + rx*rr*math.cos(a), cy + ry*rr*math.sin(a)
        if squash_top is not None and y < squash_top:
            y = squash_top + (y - squash_top)*0.25   # flatten the crown
        pts.append((x, y))
    pts.append(pts[0])
    d.path("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z", label, **kw)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(110,120,4),(190,70,3),(70,300,5),(920,110,4),(860,200,3),
                               (940,430,5),(60,560,4),(130,830,4),(890,820,5),(930,640,3)]):
    d.shape("ellipse", f"Snow mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8E2E8", opacity=40, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5A645C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EEF2EA", strokeWidth=3, opacity=55)
# cold patina + steppe wind streaks
d.shape("ellipse", "Patina 1", x=170, y=180, width=240, height=140, fill="#98A29A", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=620, width=230, height=130, fill="#98A29A", opacity=20, stroke=NONE)
for i, (x0, y0, x1, y1) in enumerate([(150,250,300,238),(680,300,830,288),(140,470,290,462),
                                      (700,520,850,510),(240,140,380,132)]):
    d.path(f"M{x0},{y0} C{(x0+x1)/2},{y0-8} {(x0+x1)/2},{y1+8} {x1},{y1}",
           f"Wind streak {i+1}", fill=NONE, stroke="#E4EAE2", strokeWidth=4, opacity=22, cap="round")
for i, (x, y, w) in enumerate([(210,300,7),(780,260,7),(160,430,8),(830,450,7),(300,160,6),
                               (640,140,7),(260,700,6),(740,700,6),(180,600,5),(820,610,5)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#7C857C", opacity=38, stroke=NONE)

# wind-blown snow ground — lower edge closes on the disc's own arc
gy = 806
d.path(f"M{disc_x(gy,-1):.1f},{gy} C300,786 420,798 500,794 C580,790 700,800 {disc_x(gy,1):.1f},{gy} "
       f"A{R},{R} 0 0 1 {disc_x(gy,-1):.1f},{gy} Z", "Snow ground", fill=SNOW_GRAD, opacity=80, stroke=NONE)
d.path(f"M{disc_x(gy,-1)+8:.1f},{gy-2} C300,784 420,794 500,790 C580,786 700,796 {disc_x(gy,1)-8:.1f},{gy-2}",
       "Snow crest light", fill=NONE, stroke="#FFFFFF", strokeWidth=5, opacity=45, cap="round")
# sparse dry grass poking through the snow (kept inside the disc)
for i, (x, y, dx) in enumerate([(268,806,-16),(284,810,-8),(300,812,2),
                                (700,812,-2),(716,810,8),(732,806,16)]):
    d.path(f"M{x},{y} C{x+dx*0.4},{y-16} {x+dx*0.8},{y-26} {x+dx},{y-34}",
           f"Grass {i+1}", fill=NONE, stroke="#8A8468", strokeWidth=4, opacity=55, cap="round")

# --- the whole cat is one dense tuft mass -------------------------------------
fluff(500, 545, 232, 205, 30, 0.10, "Fluff mass", squash_top=352,
      fill=FUR_GRAD, stroke=INK, strokeWidth=7)
# darker dorsal cap over the crown, lighter chest mass below
fluff(500, 470, 208, 150, 24, 0.10, "Dorsal cap", squash_top=352,
      fill=FUR_DARK, opacity=55, stroke=NONE)
fluff(500, 640, 190, 130, 22, 0.10, "Chest fluff",
      fill=rad((0, "#DAD6C8"), (0.6, "#B4B0A2"), (1, "#87837A")),
      opacity=80, stroke=NONE)
# frosted guard hairs along the crown rim
for i in range(15):
    a = math.radians(210 + i*8.6)
    x0, y0 = 500 + 176*math.cos(a), 468 + 118*math.sin(a)
    x1, y1 = 500 + 196*math.cos(a), 468 + 128*math.sin(a)
    d.path(f"M{x0:.0f},{y0:.0f} L{x1:.0f},{y1:.0f}", f"Frost hair {i+1}",
           fill=NONE, stroke="#EDEAE0", strokeWidth=4, opacity=45, cap="round")
# layered fur strokes massing down the chest
for i, (x0, y0, x1, y1) in enumerate([
        (500,560,498,700),(456,566,440,690),(544,566,560,690),
        (410,586,392,700),(590,586,608,700),(368,620,356,712),
        (632,620,644,712),(470,650,466,715),(530,650,534,715)]):
    d.path(f"M{x0},{y0} C{(x0+x1)/2},{(y0+y1)/2 - 12} {(x0+x1)/2},{(y0+y1)/2 + 12} {x1},{y1}",
           f"Chest fur {i+1}", fill=NONE, stroke="#7E7A6E", strokeWidth=6, opacity=35, cap="round")
for i, (x0, y0, x1, y1) in enumerate([
        (500,600,500,720),(430,600,418,700),(570,600,582,700),(480,680,478,740),(520,680,522,740)]):
    d.path(f"M{x0},{y0} C{(x0+x1)/2},{(y0+y1)/2} {(x0+x1)/2},{(y0+y1)/2} {x1},{y1}",
           f"Chest fur light {i+1}", fill=NONE, stroke="#E2DED2", strokeWidth=4, opacity=30, cap="round")

# --- low-set ears: small, drowned in fur at the sides of the crown --------------
EAR = "M356,424 C326,412 306,428 304,456 C302,482 322,502 350,500 C362,480 364,448 356,424 Z"
pair(EAR, "Ear", fill=EAR_GRAD, stroke=INK, strokeWidth=5)
pair("M348,442 C330,434 318,444 317,460 C316,476 328,488 344,486 C351,472 352,456 348,442 Z",
     "Inner ear", fill="#4A463E", opacity=70, stroke=NONE)
# ear-rim fur tufts swallowing the ears
pair("M318,496 C306,486 302,472 306,456 M334,500 C325,493 321,483 323,471",
     "Ear fur", fill=NONE, stroke="#8B8779", strokeWidth=5, opacity=60, cap="round")

# --- the flat face mask --------------------------------------------------------
d.shape("ellipse", "Face mask", x=352, y=418, width=296, height=190,
        fill=FACE_GRAD, stroke=NONE)
d.shape("ellipse", "Brow shadow", x=380, y=428, width=240, height=56,
        fill="#5C584E", opacity=35, stroke=NONE)
d.shape("ellipse", "Forehead light", x=438, y=396, width=124, height=36,
        fill="#FFFFFF", opacity=11, stroke=NONE)
# faint dark forehead stripes
for i, (x, y) in enumerate([(470,442),(500,438),(530,442),(452,452),(548,452)]):
    d.path(f"M{x},{y} l0,16", f"Forehead stripe {i+1}", fill=NONE,
           stroke="#6E6A5E", strokeWidth=5, opacity=45, cap="round")
# cheek stripes sweeping down-outward from the eye corners
for i, (x0, y0, x1, y1) in enumerate([(388,512,368,556),(396,520,382,566),(404,528,396,576)]):
    pair(f"M{x0},{y0} C{x0-8},{(y0+y1)/2} {x1+6},{(y0+y1)/2} {x1},{y1}", f"Cheek stripe {i+1}",
         fill=NONE, stroke="#6E6A5E", strokeWidth=5, opacity=40, cap="round")

# --- eyes: amber, round-pupilled, crushed under a flat drooping lid -------------
for side, cx in (("L", 430), ("R", 570)):
    cy = 500
    d.shape("ellipse", f"Socket {side}", x=cx-38, y=cy-36, width=76, height=72,
            fill="#8B8779", opacity=40, stroke=NONE)
    d.shape("ellipse", f"Iris {side}", x=cx-26, y=cy-26, width=52, height=52,
            fill=IRIS_GRAD, stroke=INK, strokeWidth=4)
    # round pupil — the manul tell (not a slit)
    d.shape("ellipse", f"Pupil {side}", x=cx-9, y=cy-8, width=18, height=18,
            fill="#161310", stroke=NONE)
    d.shape("ellipse", f"Glint {side}", x=cx-12, y=cy-14, width=9, height=8,
            fill="#FFFFFF", opacity=85, stroke=NONE)
# the scowl: a heavy flat lid chopping the top of each eye, angled down inward
pair("M394,482 C410,478 432,478 452,486 C448,494 432,498 414,497 C404,496 396,490 394,482 Z",
     "Upper lid", fill="#6E6A5E", stroke=INK, strokeWidth=4)
pair("M390,480 C408,474 434,474 456,486", "Lid edge", fill=NONE,
     stroke=INK, strokeWidth=6, cap="round")
# brow line slanting down toward the nose — the permanent frown
pair("M386,462 C412,452 440,452 464,464", "Scowl brow", fill=NONE,
     stroke="#57534A", strokeWidth=9, opacity=70, cap="round")
pair("M404,506 C416,512 436,512 448,505", "Under-eye fur", fill=NONE,
     stroke="#7E7A6E", strokeWidth=4, opacity=40, cap="round")

# --- tiny nose, short muzzle, downturned mouth -----------------------------------
d.path("M478,556 C486,548 514,548 522,556 C522,568 512,574 500,574 C488,574 478,568 478,556 Z",
       "Nose", fill=lin(0, 548, 0, 574, (0, "#B08A7E"), (1, "#7E5A50")), stroke=INK, strokeWidth=4)
d.shape("ellipse", "Nose glint", x=488, y=552, width=10, height=5, fill="#FFFFFF", opacity=45, stroke=NONE)
d.path("M500,574 L500,588", "Philtrum", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# the grumpy mouth: downturned ω
d.path("M500,590 C492,600 480,604 468,600 M500,590 C508,600 520,604 532,600",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
d.path("M468,600 C474,608 486,610 500,609 C514,610 526,608 532,600",
       "Chin shade", fill=NONE, stroke="#8B8779", strokeWidth=6, opacity=40, cap="round")
# muzzle puff either side of the philtrum
d.shape("ellipse", "Muzzle puff L", x=440, y=556, width=56, height=48, fill="#DDD9CB", opacity=45, stroke=NONE)
d.shape("ellipse", "Muzzle puff R", x=504, y=556, width=56, height=48, fill="#DDD9CB", opacity=45, stroke=NONE)
for j, (x, y) in enumerate([(452,566),(462,574),(450,578),(460,560)]):
    d.shape("ellipse", f"Whisker dot L{j+1}", x=x-2, y=y-2, width=4, height=4, fill="#57534A", opacity=55, stroke=NONE)
    d.shape("ellipse", f"Whisker dot R{j+1}", x=1000-x-2, y=y-2, width=4, height=4, fill="#57534A", opacity=55, stroke=NONE)
# long whiskers sweeping sideways
for j, (x1, y1, x2, y2) in enumerate([(444,560,296,536),(442,570,288,566),(444,580,296,596),(448,588,310,624)]):
    pair(f"M{x1},{y1} Q{(x1+x2)/2},{min(y1,y2)-8} {x2},{y2}", f"Whisker {j+1}",
         fill=NONE, stroke="#F2EFE6", strokeWidth=2.5, opacity=75, cap="round")

# --- furry front paws tucked at the base -----------------------------------------
for side, cx in (("L", 430), ("R", 570)):
    d.shape("ellipse", f"Paw {side}", x=cx-46, y=768, width=92, height=52,
            fill=rad((0, "#CFCBBB"), (0.7, "#A5A193"), (1, "#847F73")),
            stroke=INK, strokeWidth=5)
    for k, dx in enumerate((-18, 0, 18)):
        d.path(f"M{cx+dx},788 L{cx+dx},806", f"Paw toe {side}{k+1}", fill=NONE,
               stroke=INK, strokeWidth=3, opacity=55, cap="round")
# paw fur fringe over the toes
for side, x0 in (("L", 396), ("R", 540)):
    d.path(f"M{x0},782 L{x0+8},792 L{x0+16},780 L{x0+24},792 L{x0+32},780 L{x0+40},792 L{x0+48},782",
           f"Paw fringe {side}", fill=NONE, stroke="#B4B0A2", strokeWidth=4, opacity=60)

# --- name -------------------------------------------------------------------------
d.text("PALLAS'S CAT", "Name", x=500, y=960, size=52, font="Virelai Sans",
       color="#D5DCD4", justify="center")

d.finish("pallas-cat-V1R00")
