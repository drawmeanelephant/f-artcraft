#!/usr/bin/env python3
"""Wildebeest — field plate V1R00. The committee animal crossing the Mara:
buffalo horns off a low boss, goat beard, horse tail, ox chest, all on one
slope-backed body — mid-stride through silt water, head low. Far bank holds
the distant herd queueing for the crossing under its own dust. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Wildebeest — Field Plate", 1000, 1000)

INK = "#2A1C0E"   # warm dark ink, never pure black
PCX, PCY, PR = 500, 460, 420

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

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def rim_x(y, side):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#1A1208"), (1, "#070503"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#DCC998"), (0.45, "#B09B64"),
                 (0.75, "#77653C"), (1, "#463B22"))
BANK_GRAD  = lin(0, 540, 0, 600, (0, "#B39357"), (1, "#6E5830"))
WATER_GRAD = lin(0, 630, 0, 880, (0, "#8A7A48"), (0.5, "#5E5530"), (1, "#332E16"))
BODY_GRAD  = rad((0, "#A3977F"), (0.55, "#7A6E5C"), (1, "#4E453A"))
HORN_GRAD  = lin(360, 390, 320, 520, (0, "#4A3C28"), (1, "#1E160C"))
MANE_GRAD  = lin(380, 330, 560, 390, (0, "#2E2418"), (1, "#171008"))
LEG_GRAD   = lin(0, 560, 0, 670, (0, "#4E4434"), (1, "#241D12"))

# --- backdrop + Mara dusk plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#DCC998", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3A2E18", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E4BC", strokeWidth=3, opacity=40)
# low sun burning through the crossing dust, left of centre
d.shape("ellipse", "Sun glow", x=210, y=180, width=320, height=320,
        fill=rad((0, "#F0D8A0", 45), (0.6, "#E8C88E", 18), (1, "#E8C88E", 0)), stroke=NONE)
d.shape("ellipse", "Sun core", x=340, y=300, width=60, height=60,
        fill="#F4E2B4", opacity=55, stroke=NONE)
# dust bands hanging over the river
for i, dd in enumerate(["M170,330 C360,308 620,314 820,338",
                        "M130,430 C340,410 660,416 870,442",
                        "M210,510 C400,494 640,498 790,516"]):
    d.path(dd, f"Dust band {i+1}", fill=NONE, stroke="#E8D2A0",
           strokeWidth=22, opacity=10, cap="round")
for i, dd in enumerate(["M220,370 C400,354 640,358 800,376",
                        "M260,470 C430,456 620,460 760,474"]):
    d.path(dd, f"Dust line {i+1}", fill=NONE, stroke="#F0DCA8",
           strokeWidth=5, opacity=22, cap="round")

# --- far bank: a low ochre shelf the herd is queueing on ------------------------------
d.path("M110,552 C300,540 700,540 890,552 L890,580 C700,594 300,594 110,580 Z",
       "Far bank", fill=BANK_GRAD, opacity=85, stroke=NONE)
d.path("M110,552 C300,540 700,540 890,552", "Bank crest", fill=NONE,
       stroke="#E4CD96", strokeWidth=4, opacity=45, cap="round")
# dark scrub ticks along the bank
for i, (x, y, h) in enumerate([(160,548,16),(300,546,20),(430,544,14),(580,543,18),
                               (700,544,15),(830,548,17)]):
    d.path(f"M{x},{y} L{x-3},{y-h} M{x},{y} L{x+4},{y-h+4}", f"Scrub {i+1}",
           fill=NONE, stroke="#5E4A28", strokeWidth=3, opacity=50, cap="round")

# --- the distant herd: tiny gnu commas marching down to the crossing ------------------
def herd(x, y, s, i):
    """Far-side wildebeest: humped back, dropped head, horn tick."""
    d.shape("ellipse", f"Herd body {i}", x=x, y=y-10*s, width=22*s, height=12*s,
            fill="#33240F", opacity=85, stroke=NONE)
    d.shape("ellipse", f"Herd head {i}", x=x-7*s, y=y-8*s, width=10*s, height=9*s,
            fill="#33240F", opacity=85, stroke=NONE)
    d.path(f"M{x-5*s:.0f},{y-9*s:.0f} L{x-8*s:.0f},{y-14*s:.0f}",
           f"Herd horn {i}", fill=NONE, stroke="#221808",
           strokeWidth=2.5, opacity=80, cap="round")

for i, (x, s) in enumerate([(490,1.0),(540,1.1),(585,0.95),(625,1.15),(668,1.0),
                            (710,1.1),(755,0.95),(795,1.1),(838,1.0),(868,0.9)]):
    herd(x, 548 + (i % 3) * 3, s, i+1)
# dust the herd raises — soft blobs riding just above the bank line
for i, (x, y, w) in enumerate([(520,516,64),(610,508,78),(700,514,70),(790,510,74)]):
    d.shape("ellipse", f"Herd dust {i+1}", x=x, y=y, width=w, height=w*0.45,
            fill="#E0C48C", opacity=20, stroke=NONE)
# two followers already swimming behind the hero: back + head above the waterline
for i, (x, y, s) in enumerate([(806, 636, 1.0), (852, 640, 0.8)]):
    d.path(f"M{x-16*s:.0f},{y} C{x-10*s:.0f},{y-10*s:.0f} {x+6*s:.0f},{y-12*s:.0f} "
           f"{x+14*s:.0f},{y-4*s:.0f} L{x+16*s:.0f},{y} Z",
           f"Swimmer back {i+1}", fill="#3E3018", opacity=85, stroke=NONE)
    d.path(f"M{x-14*s:.0f},{y-2:.0f} C{x-20*s:.0f},{y-16*s:.0f} {x-26*s:.0f},{y-18*s:.0f} "
           f"{x-30*s:.0f},{y-10*s:.0f} L{x-28*s:.0f},{y-2:.0f} Z",
           f"Swimmer head {i+1}", fill="#3E3018", opacity=85, stroke=NONE)

# --- the river: silt water closing on the disc's own arc -------------------------------
wy = 642
wxl, wxr = rim_x(wy, -1), rim_x(wy, 1)
d.path(f"M{wxl:.1f},{wy} C300,{wy-16} 500,{wy+4} 700,{wy-10} L{wxr:.1f},{wy} "
       f"A{PR},{PR} 0 0 1 {wxl:.1f},{wy} Z",
       "River", fill=WATER_GRAD, stroke=NONE)
d.path(f"M{wxl+6:.1f},{wy-2} C300,{wy-18} 500,{wy+2} 700,{wy-12} L{wxr-6:.1f},{wy-2}",
       "Waterline", fill=NONE, stroke="#D8C896", strokeWidth=3.5,
       opacity=45, cap="round")
# current lines — bounded inside the rim at each depth
for i, (y, pad) in enumerate([(668, 30), (700, 40), (735, 55), (772, 75), (812, 95)]):
    xl, xr = rim_x(y, -1) + pad, rim_x(y, 1) - pad
    xm = (xl + xr) / 2
    d.path(f"M{xl:.0f},{y} C{xm-60},{y-8} {xm+60},{y+8} {xr:.0f},{y}",
           f"Current {i+1}", fill=NONE, stroke="#9A8C58", strokeWidth=4,
           opacity=max(14, 34 - i * 4), cap="round")

# --- tail first: root hides under the rump ---------------------------------------------
d.path("M738,402 C764,438 780,488 782,544 C784,568 778,588 766,596 "
       "C772,570 770,542 762,514 C752,478 740,442 726,418 Z",
       "Tail", fill="#241C12", stroke=INK, strokeWidth=3)
d.path("M768,540 C776,562 774,582 764,596", "Tail tuft", fill=NONE,
       stroke="#120D08", strokeWidth=8, opacity=70, cap="round")

# --- legs: bent strides into the water ----------------------------------------------------------
d.path("M434,558 L462,560 C458,590 452,618 442,644 L436,666 L414,664 "
       "L424,636 C430,612 432,584 434,558 Z",
       "Leg front near", fill=LEG_GRAD, stroke=INK, strokeWidth=4)
d.path("M468,560 L494,562 C492,594 490,626 488,656 L466,656 "
       "C466,626 466,594 468,560 Z",
       "Leg front far", fill="#35291A", stroke=INK, strokeWidth=4)
d.path("M634,558 L660,556 C656,592 648,624 640,652 L620,650 "
       "C626,620 630,588 634,558 Z",
       "Leg rear far", fill="#35291A", stroke=INK, strokeWidth=4)
d.path("M676,552 L708,548 C714,582 722,616 730,648 L748,666 L722,670 "
       "L706,644 C696,614 686,584 676,552 Z",
       "Leg rear near", fill=LEG_GRAD, stroke=INK, strokeWidth=4)

# --- the committee body ------------------------------------------------------------------
BODY = ("M272,494 "                          # nose tip
        "C282,468 302,448 330,436 "          # roman nose bridge up the face
        "C348,428 358,408 366,388 "          # forehead into the poll
        "C380,362 412,342 458,332 "          # crest of neck rising steeply
        "C500,324 540,328 580,344 "          # high withers hump
        "C634,362 694,380 724,404 "          # long slope down to the rump
        "C744,418 752,442 748,470 "          # rump rounds
        "C744,500 734,526 718,548 "          # rear edge tucking up, lean
        "C690,562 640,570 580,572 "          # rear underline
        "C510,575 460,572 430,562 "          # belly
        "C408,552 396,548 386,536 "          # deep chest front
        "C352,522 312,510 288,498 "          # jaw underside
        "C282,497 276,496 272,494 Z")        # chin back to the nose
d.path(BODY, "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# shoulder mass sits darker; back picks up the low sun
d.shape("ellipse", "Shoulder shade", x=440, y=380, width=180, height=190,
        fill=rad((0, "#4E453A", 35), (0.65, "#4E453A", 18), (1, "#4E453A", 0)), stroke=NONE)
d.path("M400,358 C470,334 560,336 640,368", "Back light", fill=NONE,
       stroke="#D8C8A0", strokeWidth=8, opacity=35, cap="round")
d.path("M490,568 C570,574 650,564 712,540", "Belly shade", fill=NONE,
       stroke="#33291C", strokeWidth=10, opacity=30, cap="round")
d.path("M392,480 C406,510 420,538 440,558", "Shoulder line", fill=NONE,
       stroke="#3E362A", strokeWidth=5, opacity=35, cap="round")

# --- the erect mane: a tall ragged crest from poll to withers ------------------------------------
crest = [(390, 372), (418, 350), (455, 338), (492, 330), (528, 329), (560, 334), (586, 342)]
top = []
for i, (x, y) in enumerate(crest):
    ht = 34 if i in (1, 2, 3, 4) else 20
    top.append((x - 9, y - ht))
d.path("M" + " L".join(f"{x},{y}" for x, y in crest) +
       " L" + " L".join(f"{x},{y}" for x, y in reversed(top)) + " Z",
       "Mane", fill=MANE_GRAD, stroke=INK, strokeWidth=3)
for i, (x, y) in enumerate(crest[1:-1]):
    d.path(f"M{x-5},{y-16} L{x-13},{y-36}", f"Mane spike {i+1}", fill=NONE,
           stroke="#0E0A06", strokeWidth=4.5, opacity=55, cap="round")

# --- brindled stripes: a few bars on neck + forequarter ------------------------------------
for i, (x, y0, y1, bend) in enumerate([(468, 380, 516, 8), (500, 374, 526, -4),
                                       (532, 374, 526, 10), (564, 380, 520, -6)]):
    d.path(f"M{x},{y0} C{x+bend},{y0+45} {x+bend-4},{y1-45} {x-8},{y1}",
           f"Stripe {i+1}", fill=NONE, stroke="#3A3226", strokeWidth=5,
           opacity=38, cap="round")

# --- face: dark muzzle at the nose only, so the horns read against the tan cheek ------------------
d.path("M272,492 C278,468 296,450 320,442 C330,448 332,462 326,478 "
       "C320,498 306,512 292,514 C282,510 274,502 272,492 Z",
       "Muzzle mask", fill="#32281C", opacity=55, stroke=NONE)
d.path("M288,458 C302,444 320,436 336,432", "Bridge light", fill=NONE,
       stroke="#C0B294", strokeWidth=5, opacity=35, cap="round")
# square muzzle, nostril, mouth
d.shape("ellipse", "Nostril", x=278, y=486, width=15, height=10,
        fill="#120C06", stroke=NONE)
d.path("M288,508 C302,515 318,517 332,512", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M322,510 C338,516 356,518 370,514", "Jaw muscle", fill=NONE,
       stroke="#3E362A", strokeWidth=4, opacity=40, cap="round")
# the calm eye, below the brow
d.path("M340,448 C350,439 366,439 374,448 C366,457 350,457 340,448 Z",
       "Eye", fill=rad((0, "#4E3418"), (0.75, "#1E1408"), (1, "#0E0804")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye glint", x=356, y=444, width=5, height=5,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M338,440 C352,432 370,432 382,440", "Brow ridge", fill=NONE,
       stroke="#3E362A", strokeWidth=4, opacity=45, cap="round")

# --- ear tucked under the boss ------------------------------------------------------------------
d.path("M392,416 C414,403 442,405 456,420 C446,436 418,441 400,430 Z",
       "Ear", fill="#6E5F48", stroke=INK, strokeWidth=3.5)
d.path("M404,420 C420,411 438,413 449,422", "Ear shade", fill=NONE,
       stroke="#3A2E1C", strokeWidth=3.5, opacity=55, cap="round")

# --- the boss: a knobby band across the poll, forelock spilling under it -------------------------
d.path("M336,388 C350,366 388,354 416,366 C428,372 430,384 422,394 "
       "C396,382 364,388 344,404 C336,398 332,392 336,388 Z",
       "Horn boss", fill="#7A6238", stroke=INK, strokeWidth=4)
d.path("M350,380 C374,364 400,362 416,372", "Boss light", fill=NONE,
       stroke="#E2CF9E", strokeWidth=4, opacity=55, cap="round")
for i, dd in enumerate(["M372,392 C368,406 370,420 376,430",
                        "M392,390 C390,404 392,416 398,426",
                        "M410,392 C410,404 413,414 419,422"]):
    d.path(dd, f"Forelock {i+1}", fill=NONE, stroke="#2E2418",
           strokeWidth=4.5, opacity=60, cap="round")

# --- gnu horns: twin crescents hooking down the face, tips curling up ----------------------------
# far horn — a darker echo tucked just behind the near one
d.path("M370,386 C342,398 318,424 308,456 C301,478 304,498 315,507 "
       "C324,513 336,509 340,498 C330,490 328,470 338,447 "
       "C350,421 364,402 382,392 Z",
       "Horn far", fill="#3A2C1A", stroke=INK, strokeWidth=4)
# near horn — the readable one, broad crescent forward of the cheek
d.path("M356,394 C324,412 298,444 288,480 C282,502 288,522 301,529 "
       "C312,535 325,529 328,517 C318,508 316,486 327,461 "
       "C340,432 358,412 378,401 Z",
       "Horn near", fill=lin(370, 390, 300, 525, (0, "#6E5636"), (0.6, "#4A3A24"), (1, "#2A2014")),
       stroke=INK, strokeWidth=4.5)
d.path("M296,516 C288,497 291,475 305,453", "Horn sheen", fill=NONE,
       stroke="#E2CF9E", strokeWidth=4, opacity=55, cap="round")
d.path("M340,408 C324,426 311,450 305,477", "Horn ridge", fill=NONE,
       stroke="#241C10", strokeWidth=3, opacity=45, cap="round")

# --- the pale beard hugging the jawline ---------------------------------------------------------
d.path("M296,504 C312,520 338,533 366,540 L361,550 L350,541 L344,553 "
       "L334,542 L327,552 L319,539 L310,543 L305,526 C300,517 297,509 296,504 Z",
       "Beard", fill="#B0A284", opacity=80, stroke="#6E6044", strokeWidth=2.5)
for i, dd in enumerate(["M312,528 C310,539 312,547 316,552",
                        "M330,538 C328,549 330,557 334,562",
                        "M348,543 C346,554 348,562 352,567"]):
    d.path(dd, f"Beard wisp {i+1}", fill=NONE, stroke="#9E9070",
           strokeWidth=3.5, opacity=55, cap="round")
# dewlap: dark fringe hanging off the throat behind the beard
for i, dd in enumerate(["M378,540 C380,552 384,560 390,566",
                        "M392,546 C394,556 398,564 404,568",
                        "M406,552 C408,560 412,566 418,570"]):
    d.path(dd, f"Dewlap {i+1}", fill=NONE, stroke="#2E2418",
           strokeWidth=4, opacity=60, cap="round")

# --- wading evidence: splash rings + bow wave + wake ----------------------------------------------
for i, (x, y, w) in enumerate([(420, 650, 54), (480, 652, 42), (630, 650, 46), (718, 648, 58)]):
    d.shape("ellipse", f"Splash {i+1}", x=x-w//2, y=y-9, width=w, height=18,
            fill="#EAE2C8", opacity=50, stroke=NONE)
for i, (x, y, w) in enumerate([(420, 656, 66), (706, 654, 76)]):
    d.shape("ellipse", f"Ring {i+1}", x=x-w//2, y=y-10, width=w, height=20,
            fill=NONE, stroke="#E8DCB8", strokeWidth=3, opacity=45)
# droplets kicked off the shoulders
for i, (x, y, w) in enumerate([(400,620,8),(416,608,6),(688,614,8),(672,606,6),(440,626,7)]):
    d.shape("ellipse", f"Drop {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0E8CE", opacity=60, stroke=NONE)
# bow wave ahead of the chest, wake trailing behind
d.path("M370,652 C388,644 408,642 426,646", "Bow wave", fill=NONE,
       stroke="#F0E4C0", strokeWidth=5, opacity=50, cap="round")
for i, (x0, y) in enumerate([(740, 656), (772, 664), (800, 672)]):
    assert on_disc(x0 + 36, y, 8), (x0, y)
    d.path(f"M{x0},{y} C{x0+14},{y-6} {x0+28},{y-4} {x0+40},{y-10}",
           f"Wake {i+1}", fill=NONE, stroke="#C8BC92", strokeWidth=3.5,
           opacity=40 - i * 8, cap="round")

# --- rim over everything so decor closes under it ------------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#3A2E18", strokeWidth=6)
d.shape("ellipse", "Plate inner ring 2", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E4BC", strokeWidth=3, opacity=28)

# --- name -------------------------------------------------------------------------------------
r1 = d.text("WILDEBEEST", "Name", x=500, y=962, size=58, font="Virelai Sans",
            color="#EADCB4", justify="center")

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

d.finish("wildebeest-V1R00")
