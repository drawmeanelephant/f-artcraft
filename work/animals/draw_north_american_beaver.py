#!/usr/bin/env python3
"""North American beaver — field plate V1R00. The engineer at work on a pond
bank at dusk: sitting on its haunches, both paws on a held stick, the orange
incisor at the gnaw point, the big scaly paddle tail splayed flat on the mud
behind. Fresh-gnaw mood — a pencil-point stump with chips at its base, the
pond band in the foreground, drowned snags and reeds. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("North American Beaver — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#140C06"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def disc_x(y, side):
    return CX + side * math.sqrt(R * R - (y - CY) ** 2)

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#0C1410"), (1, "#030604"))
PLATE_GRAD = rad((0, "#7A6A4E"), (0.5, "#3E352A"), (1, "#12100A"))
WATER_GRAD = lin(0, 700, 0, 880, (0, "#1E3028"), (1, "#08120E"))
BANK_GRAD  = lin(0, 630, 0, 880, (0, "#4A3822"), (1, "#1A1008"))
COAT      = rad((0, "#7A5636"), (0.6, "#4E3320"), (1, "#241408"))
DARKFUR   = lin(0, 380, 0, 700, (0, "#3A2414"), (1, "#180C04"))
TAILGRAD  = rad((0, "#4E463C"), (0.7, "#332C24"), (1, "#1A1610"))
WOOD      = rad((0, "#E0CC9E"), (0.7, "#B09468"), (1, "#7E6440"))

# --- backdrop + pond-dusk plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(150,130,4),(860,140,5),(120,450,3),(890,490,4),
                               (180,720,4),(850,750,4),(250,170,3)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8D4C4", opacity=30, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#7A6A4E", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#241A10", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8CCAC", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(320,120,4),(470,100,5),(610,130,4),(560,200,3),
                               (240,280,4),(680,250,3)]):
    assert on_disc(x, y, 15), (x, y)
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w,
            fill="#E4DCC8", opacity=45, stroke=NONE)

# low ember sun upper-left, glow kept inside the disc
d.shape("ellipse", "Sun glow", x=196, y=180, width=110, height=110, fill="#E8C88A", opacity=12, stroke=NONE)
d.shape("ellipse", "Sun", x=222, y=206, width=58, height=58,
        fill=rad((0, "#F0D8A0"), (0.75, "#D8B06E"), (1, "#A87E42")), opacity=80, stroke=NONE)

# --- drowned snags + reeds behind the bank --------------------------------------
d.path("M268,560 C264,520 260,486 256,452 M256,486 C246,474 238,466 230,460",
       "Snag L", fill=NONE, stroke="#2A2016", strokeWidth=9, cap="round")
d.path("M818,590 C824,548 830,512 838,478", "Snag R", fill=NONE,
       stroke="#2A2016", strokeWidth=8, cap="round")
for i, (x, y, h) in enumerate([(150,690,120),(176,694,90),(836,676,110),(862,680,80)]):
    d.path(f"M{x},{y} C{x-3},{y-h*0.5} {x+2},{y-h*0.8} {x},{y-h}",
           f"Reed {i+1}", fill=NONE, stroke="#3E4E30", strokeWidth=5,
           opacity=80, cap="round")

# --- mud bank closing on the arc -------------------------------------------------
fy = 646
fl, fr = disc_x(fy, -1), disc_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C250,632 400,644 540,638 C660,634 770,642 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Bank", fill=BANK_GRAD, stroke=NONE)

# --- the pond in the foreground, arc-close, ripple rings --------------------------
wy = 724
wl, wr = disc_x(wy, -1), disc_x(wy, 1)
d.path(f"M{wl:.1f},{wy} C240,712 400,722 560,714 C680,708 790,718 {wr:.1f},{wy} "
       f"A{R},{R} 0 0 1 {wl:.1f},{wy} Z", "Pond", fill=WATER_GRAD, opacity=92, stroke=NONE)
for i, (x, w_) in enumerate([(300, 60), (470, 90), (640, 70), (770, 50)]):
    d.path(f"M{x-w_/2},{760+i*14} C{x-20},{756+i*14} {x+20},{764+i*14} {x+w_/2},{760+i*14}",
           f"Ripple {i+1}", fill=NONE, stroke="#7E9E8A",
           strokeWidth=3, opacity=35, cap="round")

# --- the fresh-gnaw stump: pencil point + chips ----------------------------------
d.path("M196,660 L196,556 C190,540 184,530 178,522 C190,506 196,490 200,472 "
       "C206,492 212,506 222,520 C216,532 210,544 206,556 L206,660 Z",
       "Stump", fill=WOOD, stroke=INK, strokeWidth=3.5)
# gnaw rings around the cone
for i, (y, w_) in enumerate([(500, 18), (516, 24), (534, 28)]):
    d.path(f"M{200-w_},{y} C{200-w_/2},{y+5} {200+w_/2},{y+5} {200+w_},{y}",
           f"Gnaw ring {i+1}", fill=NONE, stroke="#8A6E46",
           strokeWidth=3, opacity=70, cap="round")
# wood chips scattered at the base
for i, (x, y, a) in enumerate([(228,668,-30),(246,682,40),(216,690,70),(258,662,-55),(190,676,25)]):
    r_ = math.radians(a); c_, s_ = math.cos(r_), math.sin(r_)
    p = [(-8, -4), (8, -2), (4, 6), (-6, 5)]
    pts = " ".join(f"L{x + u*c_ - v*s_:.0f},{y + u*s_ + v*c_:.0f}" for u, v in p)
    d.path(f"M{x - 8*c_ + 4*s_:.0f},{y - 8*s_ - 4*c_:.0f} {pts} Z",
           f"Chip {i+1}", fill="#D8C4A0", opacity=85, stroke=NONE)

# contact shadow under the beaver
d.shape("ellipse", "Body shadow", x=380, y=640, width=340, height=48,
        fill="#0A0603", opacity=45, stroke=NONE)

# --- the paddle tail splayed on the mud -------------------------------------------
d.path("M686,556 C750,568 800,600 824,644 C838,672 830,696 800,702 "
       "C758,710 706,690 678,650 C662,626 662,590 686,556 Z",
       "Tail", fill=TAILGRAD, stroke=INK, strokeWidth=5)
# scale crosshatch
for i, (x0, y0, x1, y1) in enumerate([(700,570,760,660),(720,562,790,652),
                                      (690,600,750,690),(740,580,810,668),
                                      (700,640,740,700),(730,650,776,690)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Scale hatch {i+1}",
           fill=NONE, stroke="#181410", strokeWidth=2.5, opacity=55, cap="round")
for i, (x0, y0, x1, y1) in enumerate([(760,570,700,660),(790,600,716,684),
                                      (810,640,730,694)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Scale hatch r{i+1}",
           fill=NONE, stroke="#181410", strokeWidth=2.5, opacity=55, cap="round")
d.path("M690,566 C744,576 788,604 812,644", "Tail sheen", fill=NONE,
       stroke="#8A7E6E", strokeWidth=4, opacity=40, cap="round")

# --- the beaver: sitting on its haunches, gnawing a held stick ---------------------
BODY = ("M338,486 "                              # nose tip
        "C352,462 370,444 394,432 "              # muzzle to brow
        "C406,426 418,422 430,422 "              # poll
        "C452,418 470,412 490,408 "              # back of head
        "C530,398 576,398 620,414 "              # rounded back
        "C658,428 682,458 694,496 "              # rump dome
        "C702,524 702,548 696,570 "              # rump to tail seat
        "C680,606 646,632 596,644 "              # haunch underside
        "C548,654 478,656 428,646 "              # belly on the ground
        "C396,640 374,624 366,598 "              # chest bottom
        "C358,578 356,558 358,540 "              # chest front
        "C356,526 350,512 342,500 "              # throat/jaw
        "C338,494 336,490 338,486 Z")            # back to nose
d.path(BODY, "Beaver", fill=COAT, stroke=INK, strokeWidth=5.5)
# darker dome-back shading + belly wash
d.path("M490,410 C540,400 596,402 640,420 C672,434 690,462 698,492 "
       "C676,458 636,432 586,420 C552,412 518,410 490,410 Z",
       "Back shade", fill=DARKFUR, opacity=55, stroke=NONE)
d.shape("ellipse", "Belly light", x=420, y=560, width=180, height=56,
        fill="#9A7A54", opacity=20, stroke=NONE)
# fur texture strokes along the flank
for i, dd in enumerate(["M500,450 C540,470 570,500 596,540",
                        "M470,480 C500,506 524,540 542,576",
                        "M560,430 C596,452 624,482 646,520"]):
    d.path(dd, f"Fur {i+1}", fill=NONE, stroke="#241408",
           strokeWidth=8, opacity=28, cap="round")

# the held stick angled across the chest, gnawed end at the mouth
d.path("M330,470 L480,536", "Stick", fill=NONE, stroke=WOOD,
       strokeWidth=11, cap="round")
d.path("M336,472 L368,484", "Gnawed end", fill=NONE, stroke="#8A6E46",
       strokeWidth=11, cap="round")
# both forepaws gripping the stick
for i, (x, y) in enumerate([(412,504),(446,516)]):
    d.shape("ellipse", f"Paw {i+1}", x=x, y=y, width=30, height=24,
            fill="#3E2A18", stroke=INK, strokeWidth=3)

# --- face ------------------------------------------------------------------------
# small rounded ear + small dark eye + orange incisor
d.shape("ellipse", "Ear", x=418, y=402, width=30, height=26,
        fill=DARKFUR, stroke=INK, strokeWidth=3)
d.path("M390,462 C398,454 412,452 422,458 C414,468 398,470 390,462 Z",
       "Eye", fill="#120A04", stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Glint", x=404, y=456, width=4, height=4,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M336,494 C344,496 352,496 360,494 C356,502 348,506 342,504 "
       "C338,502 336,498 336,494 Z",
       "Incisor", fill="#E8A030", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Nose", x=330, y=478, width=14, height=10,
        fill="#241610", stroke=NONE)
for i, (x2, y2) in enumerate([(304,486),(308,500),(318,510)]):
    d.path(f"M344,{492+i*6} C330,{488+i*6} {x2+12},{y2-3} {x2},{y2}",
           f"Whisker {i+1}", fill=NONE, stroke="#C8B898",
           strokeWidth=2, opacity=55, cap="round")
d.path("M352,510 C370,518 392,518 408,510", "Jaw line",
       fill=NONE, stroke="#241408", strokeWidth=3, opacity=60, cap="round")

# --- sedge tufts -------------------------------------------------------------------
def tuft(x, y, s, label, lean=0, color="#8A9A5E"):
    for j, (dx, bend) in enumerate([(-16, -26), (0, 0), (16, 26), (-6, -12), (8, 14)]):
        x2 = x + dx * s + bend * s * 0.4 + lean
        y2 = y - (34 - abs(dx)) * s
        d.path(f"M{x},{y} C{x + dx*s*0.3 + lean},{y - (20-abs(dx)*0.4)*s} "
               f"{x2 - bend*s*0.3},{y2 + 14*s} {x2},{y2}",
               f"{label} blade {j+1}", fill=NONE, stroke=color,
               strokeWidth=3.5, opacity=70, cap="round")

tuft(248, 700, 0.8, "Sedge L", -6)
tuft(640, 706, 0.7, "Sedge R", 4)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0E0A04", strokeWidth=6)

# --- name ----------------------------------------------------------------------
r1 = d.text("NORTH AMERICAN BEAVER", "Name", x=500, y=962, size=40,
            font="Virelai Sans", color="#E0D4B0", justify="center")

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

d.finish("north-american-beaver-V1R00")
