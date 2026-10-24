#!/usr/bin/env python3
"""dogbed — commemorative plate V1R00. The Dog Builds Its Own Docs: the
Weimaraner at last in field-plate form — silver-grey, upright, wearing the
orange HTML5 cape, seated over a freshly-rendered document like it just
laid an egg. Grey, orange, and quiet pride. A document compiler, not a CMS.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("dogbed — Commemorative Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#26221F"   # warm dark, never pure black

def on_disc(x, y, pad):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def lin(c0, c1, start=None, end=None):
    g = {"kind": "linear", "stops": [{"offset": 0, "color": c0}, {"offset": 1, "color": c1}]}
    if start: g["start"], g["end"] = [round(v, 1) for v in start], [round(v, 1) for v in end]
    return {"gradient": g}

def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": stops}}

COAT_HI, COAT_LO = "#C8CCD2", "#787F88"
CAPE_HI, CAPE_LO = "#F07030", "#A83410"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=lin("#191410", "#070503", (500, 0), (500, 1000)), stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=rad({"offset": 0, "color": "#3A2E26"},
                 {"offset": 0.65, "color": "#1D1712"},
                 {"offset": 1, "color": "#0C0806"}),
        stroke="#7A5C3E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8CEA8", strokeWidth=3, opacity=24)
# warm dust motes
for i, (x, y, w, o) in enumerate([(215,215,4,26),(790,200,5,24),(160,455,4,22),
                                  (848,430,4,24),(250,745,4,20),(745,770,5,20),
                                  (350,110,3,24),(655,110,4,22),(140,600,3,20),(865,590,4,22)]):
    assert on_disc(x, y, 12)
    d.shape("ellipse", f"Mote {i+1}", x=x-w/2, y=y-w/2, width=w, height=w,
            fill="#E8CEA8", opacity=o, stroke=NONE)
# soft orange ambient pooling behind the dog (the cape's own light)
d.shape("ellipse", "Cape ambient", x=280, y=330, width=440, height=400,
        fill=rad({"offset": 0, "color": "#E8641B", "opacity": 0.20},
                 {"offset": 1, "color": "#E8641B", "opacity": 0}), stroke=NONE)

# --- the ground: a dark mound closing on the disc's own arc --------------------
d.path("M206.1,760 Q500,682 793.9,760 A420,420 0 0 1 206.1,760 Z", "Mound",
       fill=lin("#241A12", "#0D0805", (500, 690), (500, 880)), stroke=NONE)

# --- the cape: orange billow behind the seated body -----------------------------
d.path("M500,468 C420,468 342,518 320,596 C302,662 297,714 306,758 "
       "L694,758 C703,714 698,662 680,596 C658,518 580,468 500,468 Z",
       "Cape", fill=lin(CAPE_HI, CAPE_LO, (320, 470), (690, 760)),
       stroke="#6E2410", strokeWidth=5)
# cape folds + inner shadow
for i, (x0, x1, cx) in enumerate([(330, 420, 350), (680, 585, 655), (470, 480, 470)]):
    d.path(f"M{x0},{640 if i < 2 else 500} Q{cx},{700} {x1},755",
           f"Cape fold {i+1}", fill=NONE, stroke="#7E2A0E", strokeWidth=4,
           opacity=45, cap="round")
# collar band + the HTML5 shield clasp at the throat
d.path("M398,486 Q500,514 602,486 L602,508 Q500,536 398,508 Z",
       "Collar", fill=lin("#4A3826", "#2A1E12", (398, 486), (602, 508)),
       stroke="#241A0E", strokeWidth=3)
d.path("M478,498 L522,498 L519,534 L500,544 L481,534 Z",
       "Shield clasp", fill=lin("#E8641B", "#B03818", (478, 498), (522, 544)),
       stroke="#F2B880", strokeWidth=2.5)
# the angular five, engraved on the clasp
d.path("M513,506 L487,506 L486,517 L507,517 L509,530 L489,530",
       "Clasp five", fill=NONE, stroke="#F7E0C8", strokeWidth=3.5,
       cap="round", join="round")

# --- the dog: seated body ---------------------------------------------------------
d.shape("ellipse", "Dog shadow", x=330, y=716, width=340, height=44,
        fill=rad({"offset": 0, "color": "#000000", "opacity": 0.5},
                 {"offset": 1, "color": "#000000", "opacity": 0}), stroke=NONE)
# haunches + chest, one seated mass
d.path("M500,500 C560,502 608,530 630,592 C655,650 662,700 646,742 "
       "L354,742 C338,700 345,650 370,592 C392,530 440,502 500,500 Z",
       "Body", fill=lin(COAT_HI, COAT_LO, (360, 500), (640, 740)),
       stroke=INK, strokeWidth=6)
# chest light + belly shadow for roundness
d.shape("ellipse", "Chest light", x=425, y=530, width=150, height=120,
        fill=rad({"offset": 0, "color": "#E4E8EC", "opacity": 0.30},
                 {"offset": 1, "color": "#E4E8EC", "opacity": 0}), stroke=NONE)
d.shape("ellipse", "Haunch shadow L", x=350, y=650, width=70, height=90,
        fill="#565C66", opacity=40, stroke=NONE)
d.shape("ellipse", "Haunch shadow R", x=580, y=650, width=70, height=90,
        fill="#565C66", opacity=40, stroke=NONE)
# front legs: slim columns with space between them for the egg
d.path("M438,640 C434,680 434,716 436,744 L478,744 C480,716 480,680 476,640 Z",
       "Leg L", fill=lin("#AEB4BC", "#6E747E", (434, 640), (480, 744)),
       stroke=INK, strokeWidth=4)
d.path("M524,640 C520,680 520,716 522,744 L564,744 C566,716 566,680 562,640 Z",
       "Leg R", fill=lin("#AEB4BC", "#6E747E", (520, 640), (566, 744)),
       stroke=INK, strokeWidth=4)
# paw fronts + toe marks
for i, x in enumerate((444, 460, 530, 546)):
    d.path(f"M{x},736 L{x},744", f"Toe {i+1}", fill=NONE, stroke=INK,
           strokeWidth=2.5, opacity=60, cap="round")
# keel between the forelegs
d.path("M500,560 C496,600 496,630 500,660", "Keel", fill=NONE,
       stroke="#565C66", strokeWidth=3.5, opacity=45, cap="round")

# --- head ------------------------------------------------------------------------
# long drop ears first (behind the skull)
d.path("M394,326 C362,348 354,432 366,516 C372,558 396,572 412,546 "
       "C428,520 424,436 418,378 C413,340 404,318 394,326 Z",
       "Ear L", fill=lin("#9AA0A8", "#5E646E", (360, 320), (425, 570)),
       stroke=INK, strokeWidth=5)
d.path("M606,326 C638,348 646,432 634,516 C628,558 604,572 588,546 "
       "C572,520 576,436 582,378 C587,340 596,318 606,326 Z",
       "Ear R", fill=lin("#9AA0A8", "#5E646E", (575, 320), (640, 570)),
       stroke=INK, strokeWidth=5)
# inner-ear warmth
d.path("M396,360 C380,390 376,460 384,510", "Ear L inner", fill=NONE,
       stroke="#8A7A78", strokeWidth=9, opacity=40, cap="round")
d.path("M604,360 C620,390 624,460 616,510", "Ear R inner", fill=NONE,
       stroke="#8A7A78", strokeWidth=9, opacity=40, cap="round")
# skull, narrowing to the long muzzle
d.path("M500,264 C560,264 604,298 609,350 C613,392 596,418 564,434 "
       "C552,468 532,490 506,497 L494,497 C468,490 448,468 436,434 "
       "C404,418 387,392 391,350 C396,298 440,264 500,264 Z",
       "Head", fill=lin(COAT_HI, COAT_LO, (420, 264), (580, 500)),
       stroke=INK, strokeWidth=6)
# crown light + long-muzzle shading
d.shape("ellipse", "Crown light", x=430, y=280, width=140, height=56,
        fill="#E4E8EC", opacity=28, stroke=NONE)
d.path("M452,420 C452,462 470,490 500,495 C530,490 548,462 548,420 "
       "C530,438 470,438 452,420 Z",
       "Muzzle shade", fill="#8E949E", opacity=45, stroke=NONE)
# amber eyes, level and calm — quiet pride
for side, x in (("L", 446), ("R", 554)):
    d.shape("ellipse", f"Eye {side}", x=x-12, y=372, width=24, height=27,
            fill="#3A3128", stroke=INK, strokeWidth=2.5)
    d.shape("ellipse", f"Iris {side}", x=x-8, y=376, width=16, height=18,
            fill="#C8973F", stroke=NONE)
    d.shape("ellipse", f"Pupil {side}", x=x-4, y=379, width=8, height=11,
            fill="#201A14", stroke=NONE)
    d.shape("ellipse", f"Glint {side}", x=x+1, y=379, width=5, height=5,
            fill="#FFF6E0", opacity=95, stroke=NONE)
# soft brow ridge + stop
d.path("M426,362 Q446,352 466,360", "Brow L", fill=NONE, stroke=INK,
       strokeWidth=3.5, opacity=45, cap="round")
d.path("M534,360 Q554,352 574,362", "Brow R", fill=NONE, stroke=INK,
       strokeWidth=3.5, opacity=45, cap="round")
# nose + philtrum + the faintest satisfied mouth
d.path("M476,456 C476,444 524,444 524,456 C524,470 513,482 500,482 "
       "C487,482 476,470 476,456 Z",
       "Nose", fill="#2E2823", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose glint", x=486, y=450, width=12, height=7,
        fill="#8A8078", opacity=70, stroke=NONE)
d.path("M500,482 L500,498 M500,498 Q482,510 466,502 M500,498 Q518,510 534,502",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3.5, opacity=70, cap="round")

# --- the egg: a freshly-rendered document, still warm -----------------------------
EX, EY = 500, 692
d.shape("ellipse", "Egg glow", x=EX-85, y=EY-75, width=170, height=140,
        fill=rad({"offset": 0, "color": "#F2B850", "opacity": 0.35},
                 {"offset": 1, "color": "#F2B850", "opacity": 0}), stroke=NONE)
# egg-page: a document, but round like something just laid
d.path(f"M{EX},{EY-58} C{EX+38},{EY-58} {EX+52},{EY-20} {EX+52},{EY+14} "
       f"C{EX+52},{EY+48} {EX+28},{EY+62} {EX},{EY+62} C{EX-28},{EY+62} "
       f"{EX-52},{EY+48} {EX-52},{EY+14} C{EX-52},{EY-20} {EX-38},{EY-58} {EX},{EY-58} Z",
       "Doc egg", fill=rad({"offset": 0, "color": "#F8F5EA"},
                           {"offset": 1, "color": "#D5CDB8"}),
       stroke="#9A917A", strokeWidth=4)
# rendered marks: a heading bar and two lines of fresh output
d.path(f"M{EX-26},{EY-22} L{EX+18},{EY-22}", "Egg h1", fill=NONE,
       stroke="#7A7260", strokeWidth=6, cap="round")
d.path(f"M{EX-30},{EY-4} L{EX+30},{EY-4}", "Egg line 1", fill=NONE,
       stroke="#9A917A", strokeWidth=4, opacity=80, cap="round")
d.path(f"M{EX-30},{EY+12} L{EX+12},{EY+12}", "Egg line 2", fill=NONE,
       stroke="#9A917A", strokeWidth=4, opacity=80, cap="round")
# the compiler's little green check, bottom right of the egg
d.path(f"M{EX+18},{EY+30} L{EX+26},{EY+38} L{EX+42},{EY+18}",
       "Egg check", fill=NONE, stroke="#2E7A44", strokeWidth=5, cap="round")
# stray markup glimmer rising off the fresh render
for i, (x, y, w, o) in enumerate([(462,600,5,50),(540,585,4,45),(505,575,4,40)]):
    d.shape("ellipse", f"Glimmer {i+1}", x=x, y=y, width=w, height=w,
            fill="#F2C86A", opacity=o, stroke=NONE)
# faint paw prints on the mound beside the dog — the dog walked here
for i, x in enumerate((312, 690)):
    assert on_disc(x, 736, 16)
    d.shape("ellipse", f"Paw pad {i+1}", x=x-9, y=726, width=18, height=13,
            fill="#4A3A28", opacity=50, stroke=NONE)
    for j, dx in enumerate((-9, 0, 9)):
        d.shape("ellipse", f"Paw toe {i+1}-{j+1}", x=x+dx-3.5, y=716,
                width=7, height=8, fill="#4A3A28", opacity=50, stroke=NONE)

# --- name + role -------------------------------------------------------------------
d.text("DOGBED", "Name", x=500, y=930, size=60, font="Virelai Sans",
       color="#F0E4D4", justify="center")
LINE2, SZ2, TRK = "DOCUMENT COMPILER", 23, 320
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#E8A868", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("dogbed-V1R00")
