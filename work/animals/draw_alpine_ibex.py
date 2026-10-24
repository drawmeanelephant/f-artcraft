#!/usr/bin/env python3
"""Alpine ibex — field plate V1R00. The dam-wall goat: full-body profile
facing left, standing square on a narrow granite ledge that floats over a
misty void — the salt-lick pose made portrait. The ribbed scimitar horn
arcs up and back over the whole body; a smaller dark echo for the far horn.
Slate-cold plate, pale sun, one distant cousin on a higher shelf.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Alpine Ibex — Field Plate", 1000, 1000)

INK = "#1C1A16"   # warm dark ink, never pure black
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

def quad(p0, p1, p2, t):
    x = (1-t)**2*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0]
    y = (1-t)**2*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1]
    tx = 2*(1-t)*(p1[0]-p0[0]) + 2*t*(p2[0]-p1[0])
    ty = 2*(1-t)*(p1[1]-p0[1]) + 2*t*(p2[1]-p1[1])
    return (x, y), (tx, ty)

def ribbon(p0, p1, p2, w0, w1, label, fill, samples=22, **kw):
    """Tapered filled stroke along a quadratic — the scimitar horn."""
    Lp, Rp = [], []
    for i in range(samples + 1):
        t = i / samples
        (x, y), (dx, dy) = quad(p0, p1, p2, t)
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy/ln, dx/ln
        w = (w0 + (w1 - w0)*t) / 2
        Lp.append((x + nx*w, y + ny*w)); Rp.append((x - nx*w, y - ny*w))
    dd = "M%.1f,%.1f " % Lp[0] + " ".join("L%.1f,%.1f" % p for p in Lp[1:])
    dd += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rp)) + " Z"
    d.path(dd, label, fill=fill, **kw)

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#10161E"), (1, "#04060A"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#C9D3DC"), (0.45, "#93A1AF"),
                 (0.78, "#5F6E7E"), (1, "#3A4452"))
STONE_GRAD = lin(0, 686, 0, 745, (0, "#98928a"), (0.5, "#6E685E"), (1, "#3E3A34"))
BODY_GRAD  = rad((0, "#A6977E"), (0.55, "#7E6E58"), (1, "#4E4334"))
HORN_GRAD  = lin(360, 340, 610, 180, (0, "#7A6E5C"), (0.6, "#4E463A"), (1, "#2E2820"))
LEG_GRAD   = lin(0, 540, 0, 695, (0, "#453729"), (1, "#1E170E"))

# --- backdrop + slate alpine plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#C9D3DC", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#26303C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8EFF4", strokeWidth=3, opacity=40)
# pale sun + high cold haze
d.shape("ellipse", "Sun glow", x=560, y=140, width=320, height=300,
        fill=rad((0, "#F0F4F0", 40), (0.6, "#E4ECEF", 15), (1, "#E4ECEF", 0)), stroke=NONE)
d.shape("ellipse", "Sun core", x=690, y=250, width=52, height=52,
        fill="#F4F6EE", opacity=55, stroke=NONE)
for i, dd in enumerate(["M150,300 C360,278 640,284 850,308",
                        "M110,420 C340,398 660,404 890,432",
                        "M180,540 C400,522 640,526 820,544"]):
    d.path(dd, f"Mist band {i+1}", fill=NONE, stroke="#E8EFF2",
           strokeWidth=20, opacity=9, cap="round")
for i, dd in enumerate(["M200,350 C420,332 640,338 800,356",
                        "M240,480 C440,464 620,468 770,482"]):
    d.path(dd, f"Mist line {i+1}", fill=NONE, stroke="#EEF4F6",
           strokeWidth=5, opacity=22, cap="round")
# spindrift specks
for i, (x, y, w) in enumerate([(240,220,5),(410,160,4),(620,120,5),(790,200,4),(180,380,5),
                               (840,360,5),(320,290,4),(700,330,4),(150,510,5),(860,500,4)]):
    assert on_disc(x + w / 2, y + w / 2, 8), (x, y)
    d.shape("ellipse", f"Spindrift {i+1}", x=x, y=y, width=w, height=w,
            fill="#F2F6F8", opacity=45, stroke=NONE)

# --- a distant cousin on a higher shelf, far right ------------------------------------
d.path("M712,468 L712,458 C740,452 800,450 852,456 L866,460 L868,468 Z",
       "High shelf", fill="#5E6C7A", opacity=50, stroke=NONE)
# tiny ibex silhouette on it — humped back, dropped head, horn arc
d.path("M768,452 C766,442 772,434 784,432 C796,430 806,434 810,442 "
       "C813,449 810,454 802,456 L780,456 C773,455 769,454 768,452 Z",
       "Cousin body", fill="#33302C", opacity=80, stroke=NONE)
d.path("M760,452 C754,444 756,434 764,430 C760,438 760,446 764,452 Z",
       "Cousin head", fill="#33302C", opacity=80, stroke=NONE)
d.path("M772,436 C780,424 792,418 804,418", "Cousin horn", fill=NONE,
       stroke="#33302C", strokeWidth=4, opacity=80, cap="round")
for i, x in enumerate([776, 796]):
    d.path(f"M{x},455 L{x},466", f"Cousin leg {i+1}", fill=NONE,
           stroke="#33302C", strokeWidth=3, opacity=80, cap="round")

# --- the floating ledge: a granite slab over the void ----------------------------------
d.path("M205,692 C380,682 620,686 795,696 L798,722 C620,738 400,740 210,726 "
       "L196,706 Z",
       "Ledge", fill=STONE_GRAD, stroke="#2E2A24", strokeWidth=3)
d.path("M210,692 C380,682 620,686 790,695", "Ledge crest", fill=NONE,
       stroke="#DAD6CC", strokeWidth=4, opacity=60, cap="round")
# strata + cracks on the face
d.path("M230,708 C400,700 600,702 770,712", "Strata 1", fill=NONE,
       stroke="#4E483E", strokeWidth=3, opacity=40, cap="round")
d.path("M300,724 C450,718 620,720 730,726", "Strata 2", fill=NONE,
       stroke="#4E483E", strokeWidth=2.5, opacity=30, cap="round")
for i, (x0, y0, x1, y1) in enumerate([(330,694,322,724),(520,690,528,720),(680,692,672,722)]):
    d.path(f"M{x0},{y0} C{x0-4},{y0+10} {x1+4},{y1-10} {x1},{y1}",
           f"Crack {i+1}", fill=NONE, stroke="#3A342C", strokeWidth=2.5,
           opacity=45, cap="round")
# pale salt grit along the top edge the goat came for
for i, (x, y, w) in enumerate([(300,690,10),(360,688,7),(430,687,9),(510,686,8),
                               (590,688,10),(660,690,7),(730,692,9)]):
    d.shape("ellipse", f"Salt fleck {i+1}", x=x, y=y, width=w, height=4,
            fill="#E4E0D4", opacity=50, stroke=NONE)
# mist curling below the slab — the void the dam wall drops into
for i, dd in enumerate(["M170,760 C380,744 640,748 830,766",
                        "M230,800 C420,786 600,790 760,804"]):
    d.path(dd, f"Void mist {i+1}", fill=NONE, stroke="#E4ECF0",
           strokeWidth=16, opacity=10, cap="round")

# --- legs: four stocky columns planted on the slab ---------------------------------------
for i, (x0, w0, x1, w1, tone) in enumerate([
        (436, 30, 430, 20, "near"),  # front near
        (470, 26, 476, 18, "far"),   # front far
        (636, 26, 630, 18, "far"),   # rear far
        (682, 30, 690, 20, "near")]):# rear near
    fill = LEG_GRAD if tone == "near" else "#2E2418"
    d.path(f"M{x0-w0//2},540 L{x0+w0//2},540 L{x1+w1//2},688 L{x1-w1//2},688 Z",
           f"Leg {tone} {i+1}", fill=fill, stroke=INK, strokeWidth=4)
    # cloven hoof standing proud on the edge
    d.path(f"M{x1-w1//2-2},684 L{x1+w1//2+3},684 L{x1+w1//2+5},693 L{x1-w1//2-4},693 Z",
           f"Hoof {tone} {i+1}", fill="#171008", stroke=INK, strokeWidth=2.5)
    d.path(f"M{x1+1},684 L{x1+1},692", f"Cleft {tone} {i+1}", fill=NONE,
           stroke="#3A2E1C", strokeWidth=1.5, opacity=60)

# --- the goat body ----------------------------------------------------------------------
BODY = ("M270,418 "                          # nose tip
        "C282,398 306,382 334,372 "          # face front up to the brow
        "C344,368 350,362 356,352 "          # poll where the horns seat
        "C380,344 430,340 480,346 "          # neck into withers
        "C560,352 650,362 706,382 "          # level back
        "C734,394 748,418 746,446 "          # round rump
        "C744,478 734,504 716,524 "          # rear edge
        "C680,542 620,550 552,550 "          # rear underline
        "C490,550 440,544 414,530 "          # belly tucking up
        "C398,518 392,506 390,492 "          # deep chest front
        "C360,476 330,466 306,452 "          # throat to jaw
        "C288,442 276,430 270,418 Z")        # chin back to the nose
d.path(BODY, "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# shading: chest light, dorsal stripe, belly shade
d.shape("ellipse", "Chest light", x=380, y=430, width=90, height=100,
        fill=rad((0, "#C4B294", 30), (0.7, "#C4B294", 12), (1, "#C4B294", 0)), stroke=NONE)
d.path("M470,352 C560,352 650,364 710,384", "Dorsal stripe", fill=NONE,
       stroke="#3E3222", strokeWidth=9, opacity=35, cap="round")
d.path("M480,544 C560,550 650,544 712,522", "Belly shade", fill=NONE,
       stroke="#32281C", strokeWidth=9, opacity=30, cap="round")
d.path("M420,380 C480,362 560,360 640,374", "Back light", fill=NONE,
       stroke="#D8CDB4", strokeWidth=7, opacity=35, cap="round")
# stub tail
d.path("M742,430 C756,442 760,458 754,472 C748,464 742,450 738,438 Z",
       "Tail", fill="#3E3222", stroke=INK, strokeWidth=2.5)

# --- face: level-held head, dark muzzle, the small goatee ----------------------------------
d.path("M268,416 C274,398 290,384 312,378 C322,384 324,398 318,414 "
       "C312,434 298,446 284,446 C276,440 270,430 268,416 Z",
       "Muzzle mask", fill="#322A20", opacity=50, stroke=NONE)
d.shape("ellipse", "Nostril", x=274, y=412, width=13, height=9,
        fill="#120C06", stroke=NONE)
d.path("M282,438 C296,445 312,447 326,443", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# the goatee — short dark fringe on the chin
d.path("M306,446 C318,454 332,458 346,458 L342,472 L334,460 L328,474 "
       "L320,460 L314,470 L310,456 C306,452 305,448 306,446 Z",
       "Goatee", fill="#241C12", opacity=90, stroke=NONE)
# the calm eye under a strong brow
d.path("M330,404 C340,395 356,395 364,404 C356,413 340,413 330,404 Z",
       "Eye", fill=rad((0, "#5E4020"), (0.75, "#241808"), (1, "#0E0804")),
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye glint", x=346, y=400, width=5, height=5,
        fill="#FFFFFF", opacity=85, stroke=NONE)
d.path("M328,396 C342,388 360,388 372,396", "Brow ridge", fill=NONE,
       stroke="#3E362A", strokeWidth=4, opacity=45, cap="round")

# --- ear tucked below the horn base ---------------------------------------------------------
d.path("M386,396 C408,384 434,386 448,400 C438,414 412,418 396,408 Z",
       "Ear", fill="#6E5F48", stroke=INK, strokeWidth=3.5)
d.path("M398,400 C414,392 430,394 441,402", "Ear shade", fill=NONE,
       stroke="#3A2E1C", strokeWidth=3.5, opacity=55, cap="round")

# --- the horns: ribbed scimitars arcing up and back --------------------------------------------
HP0, HP1, HP2 = (356, 348), (430, 108), (612, 222)
# far horn — a darker echo offset behind
ribbon((362, 350), (448, 116), (622, 234), 24, 5, "Horn far",
       "#2E2820", opacity=95, stroke=NONE)
# near horn — the great arc
ribbon(HP0, HP1, HP2, 30, 6, "Horn near", HORN_GRAD, stroke=INK, strokeWidth=4)
# transverse ridges across the front of the near horn — the ibex fingerprint
for i, t in enumerate([0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.88]):
    (x, y), (tx, ty) = quad(HP0, HP1, HP2, t)
    ln = math.hypot(tx, ty) or 1
    nx, ny = -ty/ln, tx/ln
    w = (30 + (6 - 30)*t) / 2
    d.path(f"M{x - nx*w*0.9:.0f},{y - ny*w*0.9:.0f} L{x + nx*w*0.9:.0f},{y + ny*w*0.9:.0f}",
           f"Horn ridge {i+1}", fill=NONE, stroke="#241C12", strokeWidth=3.5,
           opacity=60, cap="round")
# leading-edge sheen up the outside of the arc
d.path("M370,330 C400,260 460,180 560,190", "Horn sheen", fill=NONE,
       stroke="#CFC4A8", strokeWidth=4, opacity=45, cap="round")

# --- rim over everything so decor closes under it ------------------------------------------------
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#26303C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring 2", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8EFF4", strokeWidth=3, opacity=28)

# --- name -------------------------------------------------------------------------------------
r1 = d.text("ALPINE IBEX", "Name", x=500, y=962, size=58, font="Virelai Sans",
            color="#E4EAF0", justify="center")

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

d.finish("alpine-ibex-V1R00")
