#!/usr/bin/env python3
"""Greater bilby — field plate V1R00. Sitting profile facing left on a red
desert night: the enormous rabbit ears erect, the long possum snout lowered
to sniff, the hunched bandicoot body on its haunches, big hind foot stretched
forward, the long crested tail trailing black-tipped over the sand. Coolabah
mood: a gnarled river-red gum leans in from the right behind a dune ridge.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Greater Bilby — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#160E0C"

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

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#0D0A12"), (1, "#040307"))
PLATE_GRAD = rad((0, "#8A6A52"), (0.5, "#463229"), (1, "#14100E"))
DUNE_GRAD  = lin(0, 560, 0, 700, (0, "#33201A"), (1, "#160E0C"))
FLOOR_GRAD = lin(0, 668, 0, 880, (0, "#4A2E1E"), (1, "#1A0E08"))
COAT      = rad((0, "#A8ACBC"), (0.6, "#6E7284"), (1, "#3C404E"))
DARKFUR   = lin(0, 380, 0, 700, (0, "#565A6C"), (1, "#262832"))
BELLY     = rad((0, "#D8D4CC"), (1, "#9A948A"))
TRUNK_GRAD = lin(680, 180, 780, 700, (0, "#3E3226"), (1, "#1A120C"))
PINK = "#C99AA0"

# --- backdrop + desert-night plate ---------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(150,140,4),(860,130,5),(120,440,3),(890,480,4),
                               (180,720,4),(850,740,4),(260,180,3)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8CCC4", opacity=30, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#8A6A52", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#241812", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C0A8", strokeWidth=3, opacity=40)

# low moon upper-left, glow kept inside the disc
MX, MY = 280, 208
for i, (r_, op) in enumerate([(62, 7), (50, 11), (40, 15)]):
    d.shape("ellipse", f"Moon glow {i+1}", x=MX-r_, y=MY-r_, width=2*r_, height=2*r_,
            fill="#F0E4C8", opacity=op, stroke=NONE)
d.shape("ellipse", "Moon", x=MX-34, y=MY-34, width=68, height=68,
        fill=rad((0, "#F6EFD8"), (0.75, "#E4D8B4"), (1, "#BCA880")), stroke=NONE)
for i, (x, y, w) in enumerate([(380,120,4),(520,105,5),(640,140,4),(450,170,3),
                               (700,230,3),(160,330,4),(300,320,3)]):
    assert on_disc(x, y, 15), (x, y)
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8DCC8", opacity=45, stroke=NONE)

# --- dune ridge band, closes on the arc ----------------------------------------
ry_ = 596
rl, rr = disc_x(ry_, -1), disc_x(ry_, 1)
d.path(f"M{rl:.1f},{ry_} C220,576 360,592 500,584 C640,576 760,588 {rr:.1f},{ry_} "
       f"A{R},{R} 0 0 1 {rl:.1f},{ry_} Z", "Dune", fill=DUNE_GRAD, opacity=90, stroke=NONE)

# --- the coolabah: gnarled gum leaning in from the right -------------------------
d.path("M758,668 C748,590 744,510 752,440 C758,388 770,340 792,300 "
       "C800,285 812,274 826,268 C820,290 810,308 800,330 "
       "C790,360 784,400 782,446 C780,524 784,600 792,668 Z",
       "Coolabah trunk", fill=TRUNK_GRAD, stroke=INK, strokeWidth=3)
# limbs forking off
d.path("M790,310 C760,280 730,268 700,264", "Limb L", fill=NONE,
       stroke="#2A2018", strokeWidth=14, cap="round")
d.path("M806,282 C830,250 852,232 872,222", "Limb R", fill=NONE,
       stroke="#2A2018", strokeWidth=12, cap="round")
# sparse gum canopy blobs + drooping leaves
for i, (cx, cy, w, h, op) in enumerate([(700,258,90,54,65),(800,232,80,48,60),
                                        (836,224,60,40,55),(756,296,58,38,50),
                                        (700,300,44,30,45)]):
    assert on_disc(cx, cy, 8), (cx, cy)
    d.shape("ellipse", f"Canopy {i+1}", x=cx-w/2, y=cy-h/2, width=w, height=h,
            fill=rad((0, "#5E6E50"), (1, "#2C3826")), opacity=op, stroke=NONE)
for i, (x, y) in enumerate([(722,284),(782,262),(840,244),(690,286)]):
    d.path(f"M{x},{y} C{x-4},{y+18} {x-2},{y+30} {x+2},{y+40}",
           f"Leaf drop {i+1}", fill=NONE, stroke="#46543A",
           strokeWidth=4, opacity=60, cap="round")
# bark scars on the trunk
for i, (x, y) in enumerate([(764,420),(772,500),(762,580),(776,360)]):
    d.path(f"M{x},{y} L{x+12},{y-4}", f"Bark scar {i+1}", fill=NONE,
           stroke="#120C08", strokeWidth=4, opacity=70, cap="round")

# --- red-sand floor closing on the arc ------------------------------------------
fy = 668
fl, fr = disc_x(fy, -1), disc_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C260,652 400,664 540,656 C660,652 780,660 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl+10:.1f},{fy-2} C260,650 400,660 540,654 C660,650 770,656 {fr-10:.1f},{fy-2}",
       "Floor light", fill=NONE, stroke="#D8A878", strokeWidth=4, opacity=30, cap="round")
# gibber stones
for i, (x, y, w) in enumerate([(240,690,16),(420,700,12),(560,690,14),(760,706,15),
                               (320,720,11),(640,724,12),(480,740,10)]):
    d.shape("ellipse", f"Stone {i+1}", x=x, y=y, width=w, height=w*0.7,
            fill="#1E120C", opacity=70, stroke=NONE)

# contact shadow under the sitting body
d.shape("ellipse", "Body shadow", x=370, y=638, width=330, height=48,
        fill="#0A0503", opacity=45, stroke=NONE)

# --- the long crested tail trailing over the sand --------------------------------
d.path("M664,560 C720,584 770,620 800,660 C818,684 826,706 822,724",
       "Tail", fill=NONE, stroke="#6A6E7E", strokeWidth=15, cap="round")
d.path("M664,560 C720,584 770,620 800,660", "Tail light", fill=NONE,
       stroke="#9AA0B0", strokeWidth=5, opacity=50, cap="round")
# black crest tuft at the tip
d.path("M806,700 C820,690 838,692 848,704 C844,720 828,730 812,726 "
       "C800,720 800,708 806,700 Z",
       "Tail crest", fill="#18141A", stroke=NONE)

# --- the bilby: hunched on its haunches, nose down -------------------------------
BODY = ("M312,488 "                              # nose tip, lowered sniffing
        "C328,462 350,440 380,426 "              # long snout to the brow
        "C398,418 414,414 428,414 "              # poll (ears rise here)
        "C448,412 462,408 478,404 "              # back of head
        "C510,394 548,392 584,404 "              # neck into the hunched back
        "C624,416 654,442 670,478 "              # high rump dome
        "C682,506 686,536 680,564 "              # rump to tail seat
        "C668,598 640,626 596,642 "              # haunch underside
        "C548,656 480,658 428,646 "              # belly low on the ground
        "C396,640 374,622 366,596 "              # chest bottom
        "C360,576 358,556 358,540 "              # chest front
        "C354,524 344,512 330,502 "              # throat/jaw to the chin
        "C322,496 316,492 312,488 Z")            # back to nose
d.path(BODY, "Bilby", fill=COAT, stroke=INK, strokeWidth=5)
# pale belly wash
d.shape("ellipse", "Belly light", x=420, y=560, width=190, height=60,
        fill="#D8D4CC", opacity=22, stroke=NONE)
# back shading under the dome
d.path("M478,406 C520,396 570,396 612,410 C650,422 672,450 680,480 "
       "C660,448 620,424 570,414 C540,408 506,406 478,406 Z",
       "Back shade", fill=DARKFUR, opacity=50, stroke=NONE)

# --- the big hind foot stretched forward on the sand -----------------------------
d.path("M430,634 C400,646 356,654 310,654 C292,654 280,650 282,642 "
       "C286,632 308,628 334,628 C370,626 410,626 436,630 Z",
       "Hind foot", fill="#8A8E9E", stroke=INK, strokeWidth=3.5)
for j, (tx, ty) in enumerate([(292,640),(286,648),(292,655)]):
    d.path(f"M{tx+12},{ty-2} L{tx},{ty+2}", f"Foot claw {j+1}",
           fill=NONE, stroke="#E8E4DC", strokeWidth=3.5, cap="round")
# foreleg tucked under the chest, small digging claws
d.path("M382,560 C378,584 376,606 380,626", "Foreleg", fill=NONE,
       stroke="#5E6274", strokeWidth=12, cap="round")
for j, (tx, ty) in enumerate([(370,638),(380,640),(390,636)]):
    d.path(f"M{tx-8},{ty-10} L{tx},{ty}", f"Foreclaw {j+1}",
           fill=NONE, stroke="#E8E4DC", strokeWidth=3, cap="round")

# --- the ears: the species code, two huge blades ---------------------------------
d.path("M414,414 C430,340 446,282 474,240 C486,224 498,218 508,224 "
       "C510,238 502,256 490,276 C470,314 446,364 434,418 Z",
       "Ear far", fill=DARKFUR, stroke=INK, strokeWidth=3.5)
d.path("M396,416 C372,336 354,272 356,218 C356,202 362,192 372,194 "
       "C384,200 390,220 394,246 C400,300 404,360 416,412 Z",
       "Ear near", fill=COAT, stroke=INK, strokeWidth=4)
d.path("M368,398 C356,336 348,276 356,224 C362,268 372,320 382,372 Z",
       "Ear near inner", fill=PINK, opacity=55, stroke=NONE)
d.path("M356,220 C352,270 356,330 368,390", "Ear rim light",
       fill=NONE, stroke="#E8E4DC", strokeWidth=3, opacity=45, cap="round")

# --- face -----------------------------------------------------------------------
# snout shading toward the nose + pink nose tip
d.path("M312,488 C318,474 332,462 348,454 C340,468 326,482 314,490 Z",
       "Snout shade", fill="#565A6C", opacity=45, stroke=NONE)
d.path("M332,494 C344,498 360,498 372,492", "Mouth line",
       fill=NONE, stroke=INK, strokeWidth=3, opacity=70, cap="round")
d.shape("ellipse", "Nose", x=304, y=480, width=16, height=12,
        fill=rad((0, "#D89AA0"), (1, "#9A5E66")), stroke=NONE)
# big dark almond eye
d.path("M388,458 C398,448 416,446 428,454 C420,468 400,470 388,458 Z",
       "Eye", fill="#141018", stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Glint", x=408, y=450, width=5, height=5,
        fill="#FFFFFF", opacity=90, stroke=NONE)
# whiskers
for i, (x2, y2) in enumerate([(278,478),(280,492),(290,504)]):
    d.path(f"M330,{484+i*6} C312,{480+i*6} {x2+14},{y2-3} {x2},{y2}",
           f"Whisker {i+1}", fill=NONE, stroke="#D8D4CC",
           strokeWidth=2, opacity=55, cap="round")
# cheek + jaw accent
d.path("M344,508 C362,516 384,516 400,508", "Jaw line",
       fill=NONE, stroke="#4A4E5E", strokeWidth=3, opacity=60, cap="round")

# --- spinifex tufts + a few drifting leaves --------------------------------------
def tuft(x, y, s, label, lean=0, color="#B89858"):
    for j, (dx, bend) in enumerate([(-16, -26), (0, 0), (16, 26), (-6, -12), (8, 14)]):
        x2 = x + dx * s + bend * s * 0.4 + lean
        y2 = y - (34 - abs(dx)) * s
        d.path(f"M{x},{y} C{x + dx*s*0.3 + lean},{y - (20-abs(dx)*0.4)*s} "
               f"{x2 - bend*s*0.3},{y2 + 14*s} {x2},{y2}",
               f"{label} blade {j+1}", fill=NONE, stroke=color,
               strokeWidth=3.5, opacity=70, cap="round")

tuft(216, 716, 0.85, "Spinifex L", -6)
tuft(596, 724, 0.7, "Spinifex M", 4)
tuft(760, 740, 0.6, "Spinifex R", 3)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#120A06", strokeWidth=6)

# --- name ----------------------------------------------------------------------
r1 = d.text("GREATER BILBY", "Name", x=500, y=962, size=52, font="Virelai Sans",
            color="#E4D0B0", justify="center")

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

d.finish("greater-bilby-V1R00")
