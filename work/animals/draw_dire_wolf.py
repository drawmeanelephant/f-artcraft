#!/usr/bin/env python3
"""Dire wolf — field-guide plate V1R00. Head and shoulders in profile, muzzle
thrown up at a low amber moon: heavier skull and ruff than its gray cousin.
La Brea tar-seep floor with bubbles and a half-sunk tusk, pack silhouettes
wading the far shore, on a bone-amber dusk plate. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Dire Wolf — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#241708"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [dict({"offset": o, "color": c},
                           **({"opacity": p[0]} if p and p[0] is not None else {}))
                      for o, c, *p in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#1E150C"), (1, "#070503"))
PLATE_GRAD = rad((0, "#C89B5E", None), (0.55, "#8A5E30", None), (1, "#3A2712", None))
COAT_GRAD = lin(0, 260, 0, 740, (0, "#7A5A3A"), (0.55, "#563E26"), (1, "#33220F"))
DARK_GRAD = lin(0, 280, 0, 600, (0, "#42301E"), (1, "#241708"))
PALE_GRAD = rad((0, "#D8B57E", None), (1, "#A87F4C", None))
TAR_GRAD = lin(0, 730, 0, 890, (0, "#211A12"), (1, "#080604"))

# --- backdrop + La Brea dusk plate ------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#8A5E30", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#241708", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8DCC0", strokeWidth=3, opacity=40)

# low amber moon the wolf is singing to — soft radial fading to nothing
d.shape("ellipse", "Moon", x=258, y=138, width=116, height=116,
        fill=rad((0, "#F6DFAE", 95), (0.62, "#E8C88E", 55), (1, "#E8C88E", 0)),
        stroke=NONE)
# dusk glow band low behind the shoulders — last light over the seep
d.path("M160,640 C260,622 400,618 540,630 C430,644 280,650 160,640 Z",
       "Dusk band", fill="#E8963C", opacity=18, stroke=NONE)
# dust motes in the amber air
for i, (x, y, w) in enumerate([(210,300,4),(300,230,5),(430,160,4),(640,150,5),(760,250,4),
                               (840,360,4),(170,430,5),(850,480,4),(250,540,4),(720,380,3),
                               (350,400,3),(580,230,3),(190,610,4),(860,590,3),(420,620,3)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w, fill="#F2DCA8", opacity=45, stroke=NONE)

# howl marks: two thin arcs travelling up-left off the muzzle
d.path("M322,282 C288,262 262,238 250,206", "Howl arc 1",
       fill=NONE, stroke="#F2DCA8", strokeWidth=4, opacity=30, cap="round")
d.path("M300,306 C262,296 232,278 214,252", "Howl arc 2",
       fill=NONE, stroke="#F2DCA8", strokeWidth=4, opacity=22, cap="round")

# --- tar floor: seep edge on top, bottom closes on the disc arc ----------------
ly = 748
ldx = math.sqrt(R * R - (ly - CY) ** 2)
d.path(f"M{CX-ldx:.1f},{ly} C340,730 460,742 560,734 C650,727 720,738 {CX+ldx:.1f},{ly} "
       f"A{R},{R} 0 0 1 {CX-ldx:.1f},{ly} Z", "Tar seep", fill=TAR_GRAD, stroke=NONE)
# sky reflection on the tar skin
d.path(f"M{CX-ldx+10:.1f},{ly-3} C340,728 460,738 560,730 C650,723 700,732 {CX+ldx-12:.1f},{ly-3}",
       "Tar gloss", fill=NONE, stroke="#E8C88E", strokeWidth=4, opacity=35, cap="round")
# tar bubbles, domes half-broken through the skin
for i, (x, y, w) in enumerate([(300, 742, 26), (368, 752, 16), (646, 740, 22), (712, 754, 14)]):
    d.path(f"M{x-w/2},{y} A{w/2},{w/2} 0 0 1 {x+w/2},{y} Z",
           f"Bubble {i+1}", fill="#3A2E1E", opacity=85, stroke=NONE)
    d.shape("ellipse", f"Bubble glint {i+1}", x=x-w*0.28, y=y-w*0.42, width=w*0.22, height=w*0.14,
            fill="#F2DCA8", opacity=45, stroke=NONE)
# a mammoth tusk half-sunk at the left edge of the seep
d.path("M212,744 C206,700 218,662 252,636 C240,668 234,704 240,740 Z",
       "Tusk", fill=lin(212, 636, 260, 744, (0, "#E0C89A"), (1, "#8A6E42")),
       stroke="#241708", strokeWidth=4)

# --- distant pack, wading the far shore ----------------------------------------
def pack_wolf(x, y, s, label):
    """Tiny howling wolf silhouette, feet at (x,y), facing left, s ~1 = 70pt wide."""
    p = (f"M{x},{y} L{x+2*s},{y-16*s} C{x-2*s},{y-26*s} {x-8*s},{y-34*s} {x-12*s},{y-46*s} "
         f"L{x-14*s},{y-52*s} L{x-8*s},{y-50*s} C{x-4*s},{y-56*s} {x+2*s},{y-58*s} {x+6*s},{y-56*s} "
         f"L{x+8*s},{y-62*s} L{x+11*s},{y-56*s} C{x+16*s},{y-52*s} {x+20*s},{y-44*s} {x+22*s},{y-38*s} "
         f"C{x+34*s},{y-30*s} {x+46*s},{y-28*s} {x+56*s},{y-30*s} "
         f"L{x+68*s},{y-42*s} L{x+70*s},{y-38*s} C{x+64*s},{y-30*s} {x+60*s},{y-24*s} {x+58*s},{y-20*s} "
         f"L{x+56*s},{y} L{x+50*s},{y} L{x+48*s},{y-14*s} C{x+38*s},{y-12*s} {x+24*s},{y-12*s} {x+14*s},{y-14*s} "
         f"L{x+12*s},{y} Z")
    d.path(p, label, fill="#1A120A", opacity=80, stroke=NONE)

pack_wolf(700, 742, 0.8, "Pack wolf 1")
pack_wolf(755, 746, 0.55, "Pack wolf 2")

# --- dire wolf: head + shoulders, muzzle thrown up at the moon -------------------
# ears first: bases get buried by the silhouette so they grow out of the skull
d.path("M556,368 C562,338 580,314 606,302 C612,326 608,356 594,390 "
       "C578,396 562,384 556,368 Z",
       "Ear far", fill=DARK_GRAD, stroke=INK, strokeWidth=5)
d.path("M508,352 C512,316 526,286 550,264 C558,258 566,260 570,268 "
       "C580,296 582,340 574,378 C552,380 520,370 508,352 Z",
       "Ear near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# one silhouette: nose tip → mouth gape → chin → throat → chest hackles →
# back of neck → skull crown → muzzle bridge → nose
SILH = ("M352,268 C356,282 360,292 366,302 C394,332 424,358 452,376 "
        "C432,370 406,358 390,346 C388,364 396,386 408,402 "
        "C424,424 448,440 476,450 C488,500 494,556 498,606 "
        "C502,650 510,684 524,706 "
        "L538,688 L552,710 L568,688 L584,712 L600,690 L616,712 L630,690 L644,706 "
        "C660,662 668,608 664,556 C660,505 644,462 616,428 "
        "C598,404 576,388 552,376 C540,368 528,360 516,354 "
        "C494,344 476,336 460,326 C430,308 394,290 366,274 "
        "C358,268 352,266 352,268 Z")
d.path(SILH, "Wolf", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# mouth interior deep in the gape
d.path("M382,330 C404,346 426,362 444,372 C424,364 404,352 388,342 Z",
       "Mouth dark", fill="#140C04", opacity=80, stroke=NONE)
# ear details
d.path("M516,330 C520,306 528,286 542,272 C548,288 550,308 546,326 "
       "C536,334 524,336 516,330 Z",
       "Ear inner", fill="#241708", opacity=70, stroke=NONE)
d.path("M512,322 C516,300 524,282 538,268", "Ear rim light",
       fill=NONE, stroke="#E8DCC0", strokeWidth=3, opacity=40, cap="round")

# dark saddle down the back of the neck — heavier than the gray wolf's
d.path("M600,420 C636,452 656,500 660,556 C664,612 656,660 640,700 "
       "C632,650 622,590 604,540 C590,498 576,458 566,430 Z",
       "Saddle", fill=DARK_GRAD, opacity=75, stroke=NONE)
for i, dd in enumerate(["M622,470 C634,510 640,556 634,602",
                        "M596,500 C608,542 614,586 610,630",
                        "M646,520 C652,558 650,596 642,630"]):
    d.path(dd, f"Guard hair {i+1}", fill=NONE, stroke="#1E140A", strokeWidth=4, opacity=40, cap="round")

# pale cheek + throat ruff — the dire wolf's heavy dewlap, tucked under the jaw
d.path("M404,414 C402,442 408,474 424,498 C414,516 414,544 430,564 "
       "C454,590 494,598 522,586 C544,574 556,550 552,524 "
       "C548,498 528,478 502,468 C466,452 432,434 404,414 Z",
       "Cheek ruff", fill=PALE_GRAD, opacity=80, stroke=NONE)
for i, dd in enumerate(["M424,486 C444,494 464,494 478,486",
                        "M428,522 C450,532 474,534 492,526",
                        "M446,556 C466,566 488,570 508,564"]):
    d.path(dd, f"Ruff fur {i+1}", fill=NONE, stroke="#8A6A42", strokeWidth=4, opacity=45, cap="round")

# muzzle shading: dark bridge, pale lower jaw
d.path("M370,286 C390,298 414,312 436,326 C452,334 464,340 472,344 "
       "C456,338 436,328 418,318 C400,308 382,296 370,286 Z",
       "Muzzle bridge", fill=DARK_GRAD, opacity=50, stroke=NONE)
d.path("M392,352 C402,368 416,384 434,394 C418,392 402,382 392,368 C388,360 388,356 392,352 Z",
       "Lower jaw pale", fill=PALE_GRAD, opacity=55, stroke=NONE)
# nose leather at the muzzle tip
d.path("M348,272 C344,260 350,250 362,248 C374,246 384,254 384,266 C384,278 374,286 362,284 C354,282 350,278 348,272 Z",
       "Nose", fill=rad((0, "#463A28", None), (1, "#0E0A04", None)), stroke=INK, strokeWidth=3)
d.shape("ellipse", "Nose glint", x=354, y=254, width=8, height=5, fill="#FFFFFF", opacity=40, stroke=NONE)
# lip line along the upper jaw
d.path("M366,302 C392,330 420,356 448,376", "Upper lip",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")

# the eye: squinted mid-howl, amber, set on the muzzle axis
d.path("M436,352 C448,336 474,332 492,344 C480,362 452,366 436,352 Z",
       "Eye", fill=rad((0, "#E8A83C", None), (0.6, "#A86E1E", None), (1, "#5E3C0C", None)),
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil", x=460, y=343, width=11, height=13, fill="#0E0A04", stroke=NONE)
d.shape("ellipse", "Glint", x=463, y=346, width=5, height=5, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M432,350 C446,334 476,330 496,342", "Upper lid",
       fill=NONE, stroke=INK, strokeWidth=6, cap="round")
d.path("M440,364 C454,370 474,368 488,360", "Lower lid light",
       fill=NONE, stroke="#E8DCC0", strokeWidth=3, opacity=45, cap="round")
d.path("M430,336 C450,324 476,322 496,330", "Brow",
       fill=NONE, stroke="#1E140A", strokeWidth=7, opacity=35, cap="round")

# hackle texture along the chest front
for i, dd in enumerate(["M478,560 C472,584 472,610 480,630",
                        "M498,618 C494,640 496,662 504,676",
                        "M630,560 C636,584 636,612 628,634",
                        "M606,604 C610,628 608,652 600,668"]):
    d.path(dd, f"Hackle {i+1}", fill=NONE, stroke="#1E140A", strokeWidth=4, opacity=40, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0C0804", strokeWidth=6)

# --- name ----------------------------------------------------------------------
d.text("DIRE WOLF", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#EDDFC2", justify="center")

d.finish("dire-wolf-V1R00")
