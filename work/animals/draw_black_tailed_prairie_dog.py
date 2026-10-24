#!/usr/bin/env python3
"""Black-tailed prairie dog — field plate V1R00. A town with a grammar of
its own: the sentinel bolt upright on its burrow mound, forepaws folded
on the chest, head high and scanning — the stubby black-tipped tail
kicked out behind. Shortgrass plate, sentinel mood: a wide dusty dusk
sky, a low sun sunk on the horizon, and two small neighbours holding the
same pose down the colony crest. Floor closes on the disc arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Black-tailed Prairie Dog — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#1A140E"                    # warm dark ink, never pure black

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
    return math.hypot(x - CX, y - CY) <= R - pad

def disc_x(y, side):
    return CX + side * math.sqrt(R * R - (y - CY) ** 2)

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#181018"), (1, "#070407"))
PLATE_GRAD = rad((0, "#C09A6C"), (0.5, "#6E5238"), (1, "#241812"))
FLOOR_GRAD = lin(0, 620, 0, 880, (0, "#4E3E28"), (1, "#181008"))
COAT      = rad((0, "#D8B478"), (0.55, "#A67E4E"), (1, "#6E4E2C"))
BELLY     = rad((0, "#E8CCA0"), (1, "#B8905E"))

# --- backdrop + dusty dusk plate --------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(150,120,4),(860,130,5),(115,450,3),(885,510,4),
                               (180,730,4),(855,760,4),(270,150,3)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#E0D0C0", opacity=26, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#C09A6C", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#281A10", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0DCB8", strokeWidth=3, opacity=38)

# the sun going down: a fat dusty disc half-sunk on the horizon line
SX, SY = 330, 470
for i, (r_, op) in enumerate([(105, 6), (82, 10), (64, 15)]):
    d.shape("ellipse", f"Sun glow {i+1}", x=SX-r_, y=SY-r_, width=2*r_, height=2*r_,
            fill="#F0B878", opacity=op, stroke=NONE)
d.shape("ellipse", "Sun", x=SX-50, y=SY-50, width=100, height=100,
        fill=rad((0, "#F8DCA0"), (0.7, "#EEA860"), (1, "#C07838")), stroke=NONE)
# thin dusk cloud bands crossing the sun
for i, (y, x0, x1, op) in enumerate([(430, 150, 690, 30), (478, 120, 560, 26),
                                     (520, 560, 850, 22), (356, 480, 860, 18)]):
    d.path(f"M{x0},{y} C{(x0+x1)/2},{y-8} {(x0+x1)/2},{y+8} {x1},{y}",
           f"Cloud band {i+1}", fill=NONE, stroke="#8E6644",
           strokeWidth=10, opacity=op, cap="round")

# --- shortgrass floor closing on the arc -------------------------------------------
fy = 648
fl, fr = disc_x(fy, -1), disc_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C260,634 400,644 540,636 C660,632 780,640 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl+10:.1f},{fy-2} C260,632 400,640 540,634 C660,630 770,636 {fr-10:.1f},{fy-2}",
       "Floor light", fill=NONE, stroke="#E8C890", strokeWidth=4, opacity=28, cap="round")
# sun clipping under the skyline glow right at the crest
d.shape("ellipse", "Horizon glow", x=560, y=596, width=300, height=60,
        fill=rad((0, "#F0B878", 30), (1, "#F0B878", 0)), stroke=NONE)

# the town: two neighbours holding the same watch down the crest + spare mounds
for i, (x, s) in enumerate([(236, 1.0), (776, 0.85)]):
    assert on_disc(x, 640, 10), x
    # burrow hump
    d.shape("ellipse", f"Far mound {i+1}", x=x-44*s, y=636, width=88*s, height=26*s,
            fill="#2E2214", opacity=85, stroke=NONE)
    # upright silhouette: head-on-body, one dark stroke of a figure
    d.path(f"M{x-10*s},636 C{x-14*s},616 {x-12*s},596 {x-4*s},584 "
           f"C{x+2*s},574 {x+12*s},576 {x+14*s},588 "
           f"C{x+16*s},604 {x+16*s},622 {x+12*s},636 Z",
           f"Far sentinel {i+1}", fill="#1C130A", opacity=92, stroke=NONE)
d.shape("ellipse", "Empty mound", x=660, y=646, width=90, height=24,
        fill="#2E2214", opacity=80, stroke=NONE)
# its black hole mouth
d.shape("ellipse", "Burrow mouth", x=686, y=650, width=34, height=14,
        fill="#0A0603", opacity=85, stroke=NONE)

# --- the sentinel's own mound: a worked dome of excavated soil ----------------------
d.path("M390,700 C420,652 470,636 540,636 C610,636 660,652 690,700 "
       "C660,724 420,724 390,700 Z", "Mound",
       fill=rad((0, "#8A6A44"), (0.65, "#5E462C"), (1, "#382A18")),
       stroke=INK, strokeWidth=4)
# crater lip behind the feet
d.path("M430,668 C470,648 610,648 650,668", "Crater lip", fill=NONE,
       stroke="#3A2A16", strokeWidth=8, opacity=70, cap="round")
# crumb flecks kicked out of the dig
for i, (x, y, w) in enumerate([(430,706,9),(470,714,7),(530,718,8),(590,714,7),
                               (640,706,9),(500,724,6),(560,722,6)]):
    d.shape("ellipse", f"Crumb {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#A8834E", opacity=60, stroke=NONE)

# === the sentinel ==================================================================
# hind feet planted wide at the crater lip
for sgn, lab in ((-1, "L"), (1, "R")):
    fx = 540 + sgn * 52
    d.path(f"M{fx-38},668 C{fx-40},652 {fx-26},644 {fx-8},644 "
           f"C{fx+14},644 {fx+34},652 {fx+38},664 "
           f"C{fx+40},672 {fx+30},678 {fx+14},678 "
           f"C{fx-14},678 {fx-36},678 {fx-38},668 Z",
           f"Hind foot {lab}", fill="#7E5E38", stroke=INK, strokeWidth=3.5)

# the stub tail kicked out behind, black tip showing
d.path("M606,620 C640,628 668,646 680,668 C684,676 678,684 666,682 "
       "C640,676 618,660 604,640 C598,632 598,622 606,620 Z",
       "Tail", fill="#8A6A44", stroke=INK, strokeWidth=3.5)
d.path("M664,656 C676,664 682,672 680,678 C676,686 662,684 652,676 "
       "C656,668 660,660 664,656 Z",
       "Tail black tip", fill="#1E160E", stroke=NONE)

# upright body: a leaning column, chest to the left, hips wide on the mound
d.path("M516,368 "                                   # crown of the head
       "C552,368 576,384 584,412 "                   # back of skull to nape
       "C596,446 606,480 612,516 "                   # long back descending
       "C620,556 628,600 620,640 "                   # hip rounding onto the mound
       "C610,664 580,674 544,674 "                   # seat
       "C508,674 478,666 466,646 "                   # belly bottom on the mound
       "C452,618 452,570 458,530 "                   # chest rising
       "C462,500 466,470 462,442 "                   # throat
       "C458,412 478,368 516,368 Z",                 # face front up to crown
       "Body", fill=COAT, stroke=INK, strokeWidth=6)
# pale belly wash running down the front
d.path("M486,420 C472,470 468,540 478,606 C486,644 512,662 546,662 "
       "C516,650 500,610 496,556 C492,506 494,460 486,420 Z",
       "Belly light", fill=BELLY, opacity=45, stroke=NONE)
# dusk rim on the back edge
d.path("M586,420 C600,470 612,540 616,606", "Rim light back", fill=NONE,
       stroke="#F0D0A0", strokeWidth=6, opacity=26, cap="round")
# guard-hair flicks along the silhouette
for i, (x, y, dx, dy) in enumerate([(458,520,-12,-4),(454,570,-12,-2),(460,620,-10,2),
                                    (612,500,12,-4),(620,560,12,-2),(618,616,10,2)]):
    d.path(f"M{x},{y} L{x+dx},{y+dy}", f"Guard hair {i+1}",
           fill=NONE, stroke="#C8A068", strokeWidth=2.5, opacity=55, cap="round")

# forepaws folded on the chest — the sentinel's tucked hands
for sgn, lab in ((-1, "L"), (1, "R")):
    px = 500 + sgn * 26
    d.path(f"M{px-14},486 C{px-16},470 {px-8},458 {px+4},456 "
           f"C{px+16},454 {px+24},464 {px+22},478 "
           f"C{px+20},490 {px+10},498 {px},498 "
           f"C{px-10},498 {px-12},494 {px-14},486 Z",
           f"Forepaw {lab}", fill="#8A6A44", stroke=INK, strokeWidth=3)
    for j in range(2):
        d.path(f"M{px-6},{470+j*8} q6,-4 12,0", f"Digit {lab}{j+1}",
               fill=NONE, stroke="#2A1E10", strokeWidth=2.5, opacity=70, cap="round")
# thin forearm crease running up from the paws
d.path("M474,498 C476,470 482,446 492,428", "Forearm crease", fill=NONE,
       stroke="#6E4E2C", strokeWidth=3.5, opacity=60, cap="round")

# --- head: blunt muzzle tipped up, scanning ----------------------------------------
d.path("M516,338 "                                   # crown
       "C548,338 572,354 580,380 "                   # back of skull
       "C586,400 582,418 566,430 "                   # nape into jaw
       "C552,442 532,448 514,446 "                   # chin/throat
       "C492,444 474,434 466,418 "                   # cheek
       "C456,404 452,388 456,372 "                   # muzzle front
       "C462,352 486,338 516,338 Z",                 # snout bridge up to crown
       "Head", fill=rad((0, "#D8B478"), (0.65, "#AC8250"), (1, "#7A5832")),
       stroke=INK, strokeWidth=5)
# muzzle: paler wash down the snout bridge and jaw
d.path("M482,388 C470,398 464,412 468,426 C476,436 494,442 510,440 "
       "C498,428 492,412 494,396 C492,386 488,384 482,388 Z",
       "Muzzle light", fill="#E8CCA0", opacity=38, stroke=NONE)
# small rounded ear laid back on the skull
d.path("M552,352 C562,340 578,338 586,348 C592,356 588,370 576,374 "
       "C564,376 552,366 552,352 Z", "Ear", fill="#8A6A44",
       stroke=INK, strokeWidth=3.5)
d.path("M560,354 C566,348 576,348 580,354 C582,360 578,366 570,366 "
       "C564,366 558,360 560,354 Z", "Ear in", fill="#5E4226", opacity=80, stroke=NONE)
# eye: dark bead, white brow tick above
d.shape("ellipse", "Eye", x=498, y=382, width=24, height=26,
        fill="#140E08", stroke=NONE)
d.shape("ellipse", "Glint", x=504, y=388, width=7, height=7,
        fill="#FFFFFF", opacity=92, stroke=NONE)
d.path("M494,374 C502,368 514,368 522,374", "Brow tick", fill=NONE,
       stroke="#E8CCA0", strokeWidth=3, opacity=70, cap="round")
# nose at the blunt tip, mouth line tucked under
d.path("M458,392 C450,386 450,376 460,374 C470,372 478,380 476,390 "
       "C474,398 464,398 458,392 Z", "Nose", fill="#1E160E", stroke=NONE)
d.path("M462,402 C472,412 486,418 500,420", "Mouth", fill=NONE,
       stroke="#5E4226", strokeWidth=3, opacity=75, cap="round")

# shortgrass tufts around the mound, bending in the evening wind
def tuft(x, y, h, lean, lab):
    for j in range(3):
        dx = (j - 1) * 12 + lean
        d.path(f"M{x+j*4},{y} C{x+j*4+dx*0.3},{y-h*0.5} {x+j*4+dx*0.8},{y-h*0.8} {x+j*4+dx},{y-h}",
               f"{lab} blade {j+1}", fill=NONE, stroke="#7A6438",
               strokeWidth=3.5, opacity=80, cap="round")
tuft(300, 700, 60, -18, "Tuft L1")
tuft(380, 730, 46, -14, "Tuft L2")
tuft(660, 720, 56, -16, "Tuft R1")
tuft(740, 690, 44, -12, "Tuft R2")
# dry seedheads nodding over the left tuft
for j, (x, y) in enumerate([(288, 646), (306, 652)]):
    d.shape("ellipse", f"Seedhead {j+1}", x=x, y=y, width=9, height=16,
            fill="#C8A868", opacity=75, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#140C08", strokeWidth=6)

# --- name --------------------------------------------------------------------------
r1 = d.text("BLACK-TAILED PRAIRIE DOG", "Name", x=500, y=962, size=40,
            font="Virelai Sans", color="#F0DCB8", justify="center")

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

d.finish("black-tailed-prairie-dog-V1R00")
