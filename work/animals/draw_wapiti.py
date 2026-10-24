#!/usr/bin/env python3
"""Wapiti — field plate V1R00. Bull elk bugling in profile facing left:
head thrown back, mouth open, the rack sweeping back over a rut-swollen
maned neck. Aspen plate, rut mood — pale trunks and gold foliage in misty
conifer dusk, cold breath curling off the open gape, a valley ridge and
grass floor closing on the disc arc. Bust lands on the rim (arc close).
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Wapiti — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#150E0A"

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

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#0B1418"), (1, "#030608"))
PLATE_GRAD = rad((0, "#5E7268"), (0.55, "#33483E"), (1, "#0F1C15"))
RIDGE_GRAD = lin(0, 520, 0, 880, (0, "#1A2A22"), (1, "#0A130D"))
FLOOR_GRAD = lin(0, 758, 0, 880, (0, "#2A3A2C"), (1, "#0B130C"))
COAT      = lin(0, 200, 0, 840, (0, "#6B462A"), (0.45, "#452C1A"), (1, "#211008"))
DARKFUR   = lin(0, 260, 0, 760, (0, "#38210F"), (1, "#180C05"))
ANTLER    = lin(0, 90, 0, 260, (0, "#E8DCB8"), (1, "#A8905F"))
ANTLER_FAR = lin(0, 90, 0, 260, (0, "#B3A075"), (1, "#6E5D40"))
TRUNK_GRAD = lin(0, 180, 0, 780, (0, "#F0EBD6"), (1, "#B4AF96"))
GOLD = "#E4B64A"

# --- backdrop + dusk plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(150,140,4),(860,120,5),(120,430,3),(890,470,4),
                               (180,710,4),(850,730,4),(250,190,3)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8D4C8", opacity=30, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#5E7268", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1E2E24", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C6D4C0", strokeWidth=3, opacity=40)
# high faint stars inside the disc
for i, (x, y, w) in enumerate([(300,120,4),(420,95,5),(580,110,4),(500,150,3)]):
    assert on_disc(x, y, 25), (x, y)
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w,
            fill="#DCE6DC", opacity=45, stroke=NONE)

# --- valley ridge: dark conifer band across the middle, closes on the arc ------
ry_ = 560
rl, rr = disc_x(ry_, -1), disc_x(ry_, 1)
d.path(f"M{rl:.1f},{ry_} C240,540 360,552 460,544 C560,536 660,552 760,546 "
       f"C810,544 850,548 {rr:.1f},{ry_} A{R},{R} 0 0 1 {rl:.1f},{ry_} Z",
       "Ridge", fill=RIDGE_GRAD, opacity=85, stroke=NONE)
# conifer spires on the ridge crest
for i, (x, y, h, w) in enumerate([(180,548,66,40),(248,542,84,46),(700,548,74,42),
                                  (780,552,56,36),(330,556,60,38),(640,556,52,34)]):
    assert on_disc(x, y - h + 10, 8), (x, y)
    d.path(f"M{x-w/2},{y} L{x},{y-h} L{x+w/2},{y} Z",
           f"Conifer {i+1}", fill="#12211A", opacity=80, stroke=NONE)
# valley mist bands over the ridge
for i, (y, op) in enumerate([(500, 10), (534, 8)]):
    d.path(f"M170,{y} C320,{y-12} 480,{y+10} 640,{y-8} C720,{y-12} 800,{y-4} 840,{y}",
           f"Mist {i+1}", fill=NONE, stroke="#CCD8CC", strokeWidth=14,
           opacity=op, cap="round")

# --- aspen trunks: pale columns rising inside the plate ------------------------
def aspen(x0, ytop, ybot, w, label, lean=0):
    d.path(f"M{x0-w/2},{ytop} C{x0-w/2+lean},{ytop+200} {x0-w/2+lean},{ybot-200} {x0-w/2},{ybot} "
           f"L{x0+w/2},{ybot} C{x0+w/2+lean},{ybot-200} {x0+w/2+lean},{ytop+200} {x0+w/2},{ytop} Z",
           f"{label} trunk", fill=TRUNK_GRAD, stroke="#4A4636", strokeWidth=3)
    # bark scars: short dark marks
    for j, (sy, sw) in enumerate([(ytop+40, 12), (ytop+95, 9), (ytop+160, 13),
                                  (ytop+235, 8), (ytop+320, 11), (ytop+430, 9)]):
        if sy < ybot - 20:
            d.path(f"M{x0-sw/2+lean*0.5},{sy} L{x0+sw/2+lean*0.5},{sy-3}",
                   f"{label} scar {j+1}", fill=NONE, stroke="#3A362A",
                   strokeWidth=4, opacity=75, cap="round")

aspen(218, 190, 800, 22, "Aspen L", lean=-6)
aspen(742, 168, 800, 24, "Aspen R", lean=8)

# gold foliage clusters crowning the trunks — overlapping blobs, not pom-poms
for i, (cx, cy, w, h, op) in enumerate([(238,196,110,80,62),(262,240,72,54,55),
                                        (200,258,60,44,50),(736,182,96,78,62),
                                        (770,226,64,48,52),(706,240,70,50,55),
                                        (300,180,54,40,45),(684,180,50,38,45)]):
    assert on_disc(cx, cy, 15), (cx, cy)
    d.shape("ellipse", f"Foliage {i+1}", x=cx-w/2, y=cy-h/2, width=w, height=h,
            fill=rad((0, "#EDC45A"), (0.7, "#D9A83C"), (1, "#A87B28")),
            opacity=op, stroke=NONE)
for i, (x, y, s) in enumerate([(330,140,9),(620,96,8),(252,330,7),(688,300,7),
                               (420,180,6),(560,250,6),(760,380,7)]):
    assert on_disc(x, y, 15), (x, y)
    d.path(f"M{x},{y} Q{x+s},{y+s*0.4} {x+s*0.6},{y+s*1.4} "
           f"Q{x-s*0.4},{y+s} {x},{y} Z",
           f"Drift leaf {i+1}", fill=GOLD, opacity=65, stroke=NONE)

# --- grass floor closing on the arc --------------------------------------------
fy = 758
fl, fr = disc_x(fy, -1), disc_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,744 430,756 560,748 C660,744 740,752 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl+10:.1f},{fy-2} C300,742 430,752 560,746 C660,742 730,748 {fr-10:.1f},{fy-2}",
       "Floor light", fill=NONE, stroke="#C4D4A8", strokeWidth=4, opacity=30, cap="round")

# --- antlers as filled silhouettes: the top edge zigzags through the tine tips,
#     the bottom edge is the beam's underside (the moose technique) --------------
def antler_filled(ox, oy, sc, grad, label, op=None):
    P = lambda x, y: (398 + (x - 398) * sc + ox, 224 + (y - 224) * sc + oy)
    # top edge: beam-edge runs broken by narrow tine spikes
    top = [(400,212),
           (396,206),(336,182),(412,196), (424,190),
           (420,184),(366,146),(434,178), (448,176),
           (454,170),(424,112),(472,166), (490,164),
           (498,158),(496,100),(518,158), (542,158),
           (556,152),(570,96),(592,154),
           (618,160),(660,168),
           (684,170),(730,158),(716,184),(750,198),(726,212),(736,236),(714,224)]
    pts = [P(*p) for p in top]
    tips = [pts[i] for i in (2, 6, 10, 14, 18, 23, 25, 27)]
    for pt in tips:
        assert on_disc(pt[0], pt[1], 22), (label, pt)
    seg = " ".join(f"L{x:.0f},{y:.0f}" for x, y in pts)
    dd = (f"M{P(390,238)[0]:.0f},{P(390,238)[1]:.0f} "
          f"C{P(394,228)[0]:.0f},{P(394,228)[1]:.0f} {P(397,220)[0]:.0f},{P(397,220)[1]:.0f} "
          f"{P(400,214)[0]:.0f},{P(400,214)[1]:.0f} " + seg +
          f" C{P(700,208)[0]:.0f},{P(700,208)[1]:.0f} {P(650,184)[0]:.0f},{P(650,184)[1]:.0f} "
          f"{P(600,176)[0]:.0f},{P(600,176)[1]:.0f} "
          f"C{P(540,168)[0]:.0f},{P(540,168)[1]:.0f} {P(470,184)[0]:.0f},{P(470,184)[1]:.0f} "
          f"{P(416,210)[0]:.0f},{P(416,210)[1]:.0f} "
          f"C{P(408,220)[0]:.0f},{P(408,220)[1]:.0f} {P(400,230)[0]:.0f},{P(400,230)[1]:.0f} "
          f"{P(402,238)[0]:.0f},{P(402,238)[1]:.0f} Z")
    kw = {"fill": grad, "stroke": INK, "strokeWidth": 4.5}
    if op: kw["opacity"] = op
    d.path(dd, label, **kw)

antler_filled(10, -6, 0.82, ANTLER_FAR, "Antler far", op=90)

# --- the bull: one silhouette, mouth open, base lands on the rim ---------------
ELK = ("M253.4,800 "
       "C275,755 292,700 310,645 "          # brisket rising
       "C325,600 340,555 356,510 "          # neck front lower
       "C365,468 376,440 384,415 "          # throat
       "C388,395 390,380 384,368 "          # under-jaw
       "C372,350 352,335 335,322 "          # jaw to chin tip
       "C330,314 330,306 336,300 "          # chin front to lower lip
       "C348,294 358,290 364,284 "          # mouth cavity: lips corner
       "C356,270 344,252 330,232 "          # upper-jaw underside to the nose
       "C318,222 304,214 292,208 "          # nose tip
       "C300,196 316,192 332,198 "          # nose bridge
       "C348,202 368,206 385,212 "          # forehead to poll
       "C428,236 452,262 474,296 "          # back of head into the mane
       "C506,340 534,392 558,436 "          # mane line down the neck
       "C572,456 592,460 612,468 "          # shoulder-hump step
       "C650,486 682,540 706,610 "          # shoulder descent
       "C726,664 738,730 746.6,800 "        # to the rim
       "A420,420 0 0 1 253.4,800 Z")        # base closes on the disc arc
d.path(ELK, "Wapiti", fill=COAT, stroke=INK, strokeWidth=6)

# neck mane: dark mass over the throat and chest front
d.path("M384,415 C376,452 364,492 352,532 C340,576 326,624 316,664 "
       "C308,698 300,734 296,764 C292,732 294,696 300,662 "
       "C292,672 288,686 286,704 C280,664 290,608 308,566 "
       "C326,526 348,486 368,450 C376,436 382,424 384,415 Z",
       "Throat mane", fill=DARKFUR, opacity=85, stroke=NONE)
# mane-flow shading strokes hugging the neck-back line
for i, dd in enumerate(["M462,330 C492,378 520,430 546,484",
                        "M572,480 C606,524 640,578 666,634"]):
    d.path(dd, f"Neck shade {i+1}", fill=NONE, stroke="#160B05",
           strokeWidth=12, opacity=30, cap="round")
# shoulder mass shading
d.path("M616,480 C652,524 684,576 706,636 C720,678 732,724 738,762 "
       "C708,722 676,672 648,620 C630,578 616,528 616,480 Z",
       "Shoulder shade", fill="#160B05", opacity=45, stroke=NONE)
d.path("M640,500 C672,540 698,588 716,640 C704,592 678,540 652,498 Z",
       "Shoulder light", fill="#8A5E34", opacity=28, stroke=NONE)
# dusk rim-light along the mane and back
d.path("M476,300 C508,346 538,400 562,442 C580,470 604,478 626,492 "
       "C664,520 692,566 708,622",
       "Back rim light", fill=NONE, stroke="#BEC8AC", strokeWidth=4,
       opacity=35, cap="round")

# ear swept back under the rack
d.path("M416,262 C440,254 470,262 486,282 C476,300 444,306 422,296 Z",
       "Ear", fill=DARKFUR, stroke=INK, strokeWidth=3.5)
d.path("M428,272 C444,268 462,274 472,284", "Ear inner",
       fill=NONE, stroke="#5E3E22", strokeWidth=3, opacity=60, cap="round")

# face: eye, nostril, jaw accents
d.path("M352,262 C362,250 380,248 392,258 C382,272 362,274 352,262 Z",
       "Eye", fill=rad((0, "#B87F38"), (0.65, "#6E4418"), (1, "#2E1A08")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil", x=367, y=253, width=10, height=12, fill="#0C0602", stroke=NONE)
d.shape("ellipse", "Glint", x=369, y=255, width=4, height=4, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M348,256 C362,245 382,243 396,252", "Brow",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M290,214 C294,206 302,202 309,204 C306,212 298,216 292,216 Z",
       "Nostril", fill="#0C0602", stroke=NONE)
# muzzle bridge highlight + lower-lip line
d.path("M300,232 C312,214 338,208 358,216 C346,230 320,238 300,232 Z",
       "Muzzle light", fill="#8A6242", opacity=40, stroke=NONE)
d.path("M336,300 C346,294 356,289 362,286", "Lower lip",
       fill=NONE, stroke=INK, strokeWidth=3.5, opacity=70, cap="round")
# tongue hint inside the open gape
d.path("M336,296 C346,288 356,284 362,282 C356,292 346,298 338,300 Z",
       "Tongue", fill="#2A1210", opacity=80, stroke=NONE)

# near antler over the poll
antler_filled(0, 0, 1.0, ANTLER, "Antler near")

# cold-morning breath: two soft puffs drifting off the gape
for i, (x, y, w, op) in enumerate([(262,222,26,12),(238,196,36,8)]):
    d.shape("ellipse", f"Breath {i+1}", x=x-w/2, y=y-w/2, width=w, height=w*0.8,
            fill="#DCE8E2", opacity=op, stroke=NONE)

# grass tufts over the chest base and floor
def tuft(x, y, s, label, lean=0):
    for j, (dx, bend) in enumerate([(-16, -26), (0, 0), (16, 26), (-6, -12), (8, 14)]):
        x2 = x + dx * s + bend * s * 0.4 + lean
        y2 = y - (34 - abs(dx)) * s
        d.path(f"M{x},{y} C{x + dx*s*0.3 + lean},{y - (20-abs(dx)*0.4)*s} "
               f"{x2 - bend*s*0.3},{y2 + 14*s} {x2},{y2}",
               f"{label} blade {j+1}", fill=NONE, stroke="#7E9060",
               strokeWidth=3.5, opacity=75, cap="round")

tuft(300, 812, 0.9, "Tuft L", -6)
tuft(700, 816, 0.85, "Tuft R", 5)
tuft(590, 840, 0.7, "Tuft M")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0A120C", strokeWidth=6)

# --- name ----------------------------------------------------------------------
r1 = d.text("WAPITI", "Name", x=500, y=962, size=60, font="Virelai Sans",
            color="#E6D8B4", justify="center")

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

d.finish("wapiti-V1R00")
