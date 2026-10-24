#!/usr/bin/env python3
"""Sea otter — field-guide plate V1R00. Rafting on its back in the cold
current: head tipped up, forepaws over the chest cracking a purple urchin,
hind flippers fanned at the far end, tail trailing under the swell, one kelp
frond wrapped round the waist. Swell lines, rising bubbles, kelp stalks off
the sea floor. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Sea Otter — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#140E08"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def quad(p0, p1, p2, t):
    u = 1 - t
    return (u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0],
            u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1])

def ribbon(p0, p1, p2, w0, w1, label, n=20, **kw):
    L, Rr = [], []
    for k in range(n + 1):
        t = k / n
        x, y = quad(p0, p1, p2, t)
        x0, y0 = quad(p0, p1, p2, max(0, t - 0.01))
        x1, y1 = quad(p0, p1, p2, min(1, t + 0.01))
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy) or 1
        w = (w0 + (w1 - w0) * t) / 2
        L.append((x - dy/ln * w, y + dx/ln * w))
        Rr.append((x + dy/ln * w, y - dx/ln * w))
    s = "M%.1f,%.1f " % L[0] + " ".join("L%.1f,%.1f" % p for p in L[1:])
    s += " " + " ".join("L%.1f,%.1f" % p for p in reversed(Rr)) + " Z"
    return d.path(s, label, **kw)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#0A1820"), (1, "#02070B"))
PLATE_GRAD = rad((0, "#A6CCD6"), (0.55, "#6C98A8"), (1, "#33586A"))
FUR = lin(500, 340, 560, 640, (0, "#8A6848"), (0.5, "#6A4A30"), (1, "#422A18"))
KELP = "#5C7A38"
FLOOR_GRAD = lin(0, 740, 0, 880, (0, "#2E4A58"), (1, "#16242C"))

# --- backdrop + cold-current plate -------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#6C98A8", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#22404E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D4E8EE", strokeWidth=3, opacity=45)

# surface light pooling behind the swimmer
d.shape("ellipse", "Light pool", x=250, y=120, width=500, height=330,
        fill=rad((0, "#D8EEF2"), (1, "#D8EEF2")), opacity=30, stroke=NONE)
# swell lines across the upper water
for i, (y, amp, op) in enumerate([(200, 9, 20), (250, 11, 17), (305, 10, 14), (356, 12, 11)]):
    pts = "M170,%.0f" % y + "".join(
        " Q%.0f,%.0f %.0f,%.0f" % (x + 42.5, y + (amp if k % 2 == 0 else -amp), x + 85, y)
        for k, x in enumerate(range(170, 800, 85)))
    d.path(pts, f"Swell {i+1}", fill=NONE, stroke="#C8E4EC", strokeWidth=5,
           opacity=op, cap="round")

# sea floor closing on the disc arc
ly = 758
ldx = math.sqrt(R * R - (ly - CY) ** 2)
d.path(f"M{CX-ldx:.1f},{ly} C340,744 460,750 560,747 C660,744 740,748 {CX+ldx:.1f},{ly} "
       f"A{R},{R} 0 0 1 {CX-ldx:.1f},{ly} Z", "Sea floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{CX-ldx+8:.1f},{ly-2} C340,742 460,748 560,745 C660,742 740,746 {CX+ldx-8:.1f},{ly-2}",
       "Floor light", fill=NONE, stroke="#7EA8B4", strokeWidth=5, opacity=30, cap="round")
# pebbles + a spare urchin on the floor
for i, (x, y, w) in enumerate([(300, 780, 26), (420, 796, 20), (600, 788, 24),
                               (700, 800, 18), (370, 812, 14)]):
    d.shape("ellipse", f"Pebble {i+1}", x=x, y=y, width=w, height=w * 0.55,
            fill="#3E5C68", opacity=70, stroke=NONE)
d.shape("ellipse", "Floor urchin", x=512, y=786, width=30, height=24,
        fill="#38204A", stroke=INK, strokeWidth=2)
for a_ in range(0, 360, 45):
    a = math.radians(a_)
    d.path(f"M{527 + math.cos(a)*13:.0f},{798 + math.sin(a)*10:.0f} "
           f"l{math.cos(a)*9:.0f},{math.sin(a)*9:.0f}", f"Urchin spine {a_}",
           fill=NONE, stroke="#4A2A50", strokeWidth=2.5, cap="round")

# --- kelp stalks rising off the floor -------------------------------------------------
def kelp_stalk(x0, y0, x1, y1, label, flip=1):
    d.path(f"M{x0},{y0} Q{(x0+x1)/2 + 20*flip},{(y0+y1)/2} {x1},{y1}",
           f"{label} stipe", fill=NONE, stroke=KELP, strokeWidth=7,
           opacity=80, cap="round")
    for k in range(4):
        t = (k + 1) / 5
        x, y = quad((x0, y0), ((x0+x1)/2 + 20*flip, (y0+y1)/2), (x1, y1), t)
        s = -1 if k % 2 else 1
        d.path(f"M{x:.0f},{y:.0f} Q{x + 26*s*flip:.0f},{y - 12} {x + 44*s*flip:.0f},{y - 6} "
               f"Q{x + 26*s*flip:.0f},{y + 10} {x:.0f},{y:.0f} Z",
               f"{label} blade {k+1}", fill="#7A9E4C", opacity=70, stroke=NONE)
kelp_stalk(268, 770, 240, 560, "Kelp L", flip=-1)
kelp_stalk(778, 760, 806, 590, "Kelp R", flip=1)

# bubbles rising past the swell
for i, (x, y, w) in enumerate([(780, 520, 16), (806, 462, 11), (770, 402, 20),
                               (812, 340, 13), (790, 282, 9), (240, 480, 8),
                               (214, 420, 12), (238, 356, 7)]):
    assert on_disc(x, y, 10), (x, y)
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w,
            fill="#E4F2F6", opacity=22, stroke=NONE)

# === the sea otter, rafting belly-up ==================================================
# --- tail: trails away under the water, dimming with depth ------------------------------
ribbon((660, 545), (740, 600), (810, 640), 44, 12, "Tail",
       fill=lin(660, 545, 810, 640, (0, "#5E4028"), (1, "#3A2414")),
       stroke=INK, strokeWidth=4, opacity=80)
assert on_disc(810, 640, 10)

# --- body: the floating log, belly up ----------------------------------------------------
d.path("M345,430 C385,400 460,392 540,405 C610,416 665,445 690,480 "
       "C708,505 710,535 695,555 C678,580 630,595 565,598 "
       "C495,600 415,588 372,562 C340,542 328,505 335,470 "
       "C338,452 340,440 345,430 Z", "Body", fill=FUR, stroke=INK, strokeWidth=5)
# pale wet sheen along the belly's waterline curve
d.path("M370,540 C430,570 540,584 640,566", "Water sheen", fill=NONE,
       stroke="#C8E4EC", strokeWidth=10, opacity=35, cap="round")
# sun on the upper flank
d.path("M380,432 C440,408 540,406 620,432", "Flank light", fill=NONE,
       stroke="#C8A678", strokeWidth=9, opacity=40, cap="round")
# fur texture flecks
for i, (x, y, w) in enumerate([(420,480,16),(480,470,13),(540,490,15),(600,505,12),
                               (455,530,11),(580,540,13),(505,550,10)]):
    d.shape("ellipse", f"Fur fleck {i+1}", x=x, y=y, width=w, height=w * 0.6,
            fill="#4A3018", opacity=30, stroke=NONE)

# --- hind flippers: fanned at the far end -----------------------------------------------
d.path("M668,470 C690,440 720,425 748,428 C758,430 758,442 750,450 "
       "C735,465 712,475 692,480 Z", "Flipper top",
       fill="#4A3018", stroke=INK, strokeWidth=4)
d.path("M676,495 C702,478 732,472 756,480 C764,483 762,493 754,498 "
       "C734,508 710,510 692,508 Z", "Flipper low",
       fill="#3E2812", stroke=INK, strokeWidth=4)
# toe seams
for i, (x0, y0, x1, y1) in enumerate([(688,462,724,440),(696,470,734,452),
                                      (700,492,734,486),(706,500,738,494)]):
    d.path(f"M{x0},{y0} L{x1},{y1}", f"Flipper seam {i+1}", fill=NONE,
           stroke="#241408", strokeWidth=2.5, opacity=60, cap="round")

# --- kelp frond wrapped round the waist --------------------------------------------------
d.path("M505,470 C540,505 545,555 525,600 C518,616 500,618 495,602 "
       "C488,578 495,540 488,505 C484,485 492,468 505,470 Z",
       "Kelp wrap", fill="#6E8C44", opacity=75, stroke="#2E4218", strokeWidth=3)
d.path("M522,600 C528,628 522,652 508,668", "Kelp wrap tail", fill=NONE,
       stroke=KELP, strokeWidth=8, opacity=75, cap="round")
d.path("M508,490 C518,522 520,556 512,590", "Kelp wrap vein", fill=NONE,
       stroke="#9CBC6C", strokeWidth=3, opacity=60, cap="round")

# --- head, tipped up at the near end -------------------------------------------------------
# small round ears first
d.shape("ellipse", "Ear L", x=298, y=348, width=30, height=28,
        fill="#5E4028", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Ear R", x=392, y=340, width=30, height=28,
        fill="#5E4028", stroke=INK, strokeWidth=4)
# skull: broad otter head, chin tipped toward the sky
d.path("M360,336 C405,336 438,362 444,400 C450,436 436,468 404,482 "
       "C374,494 330,490 306,470 C282,450 274,416 284,388 "
       "C294,360 322,336 360,336 Z", "Head",
       fill=lin(360, 336, 365, 490, (0, "#8A6848"), (1, "#5E3E24")),
       stroke=INK, strokeWidth=5)
# cream muzzle mask — the otter's pale face
d.path("M352,400 C390,400 418,418 422,446 C425,470 412,486 388,491 "
       "C362,496 330,490 314,474 C298,458 296,436 306,420 "
       "C316,406 332,400 352,400 Z", "Muzzle",
       fill=rad((0, "#F0E2C8"), (1, "#D4BE98")), stroke=NONE)
# grey grizzle on the crown — old otter frosting
d.path("M320,348 C345,338 390,340 412,356 C395,352 350,352 328,362 "
       "C318,366 314,358 320,348 Z", "Crown grizzle", fill="#D8CDB8",
       opacity=55, stroke=NONE)
# the little dark nose, high on the muzzle
d.path("M352,420 C360,414 374,414 382,420 C384,430 376,438 367,439 "
       "C358,438 350,430 352,420 Z", "Nose", fill="#201410", stroke=INK, strokeWidth=3)
# mouth: the contented otter line
d.path("M367,439 C360,447 352,450 344,447 M367,439 C374,447 382,450 390,447",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
# eyes: small, dark, half-lidded in the sun
d.shape("ellipse", "Eye L", x=322, y=392, width=15, height=14,
        fill="#180E06", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Eye R", x=398, y=388, width=15, height=14,
        fill="#180E06", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Glint L", x=325, y=394, width=4, height=4,
        fill="#FFFFFF", opacity=80, stroke=NONE)
d.shape("ellipse", "Glint R", x=401, y=390, width=4, height=4,
        fill="#FFFFFF", opacity=80, stroke=NONE)
# whiskers — the otter's famous bristle
for i, (x1, y1, x2, y2) in enumerate([(330,442,264,428),(332,450,262,448),(334,458,270,470),
                                      (402,438,462,420),(400,447,460,442),(398,455,456,462)]):
    d.path(f"M{x1},{y1} Q{(x1+x2)/2},{min(y1,y2)-6} {x2},{y2}", f"Whisker {i+1}",
           fill=NONE, stroke="#EDE0C4", strokeWidth=2, opacity=60, cap="round")

# --- forepaws over the chest, cracking the urchin ------------------------------------------
# the urchin held between the mitts
d.shape("ellipse", "Urchin", x=440, y=440, width=52, height=44,
        fill=rad((0, "#5E3A66"), (1, "#33184A")), stroke=INK, strokeWidth=3)
for a_ in range(-70, 250, 40):
    a = math.radians(a_)
    d.path(f"M{466 + math.cos(a)*24:.0f},{462 + math.sin(a)*20:.0f} "
           f"l{math.cos(a)*10:.0f},{math.sin(a)*10:.0f}", f"Urchin spine {a_}",
           fill=NONE, stroke="#4A2A50", strokeWidth=3, cap="round")
d.shape("ellipse", "Urchin glint", x=448, y=446, width=12, height=8,
        fill="#9A7AAA", opacity=60, stroke=NONE)
# mitts gripping either side
d.path("M430,428 C418,428 408,438 406,452 C404,468 412,482 426,484 "
       "C438,486 448,478 450,466 C452,450 444,430 430,428 Z",
       "Paw L", fill="#5E4028", stroke=INK, strokeWidth=4)
d.path("M498,424 C510,422 520,432 522,446 C524,462 516,476 502,478 "
       "C490,480 480,472 478,460 C476,444 484,426 498,424 Z",
       "Paw R", fill="#5E4028", stroke=INK, strokeWidth=4)
# thumb seams
d.path("M414,442 C420,452 428,460 438,464", "Paw L seam", fill=NONE,
       stroke="#2E1A0C", strokeWidth=2.5, opacity=60, cap="round")
d.path("M514,436 C508,446 500,454 490,458", "Paw R seam", fill=NONE,
       stroke="#2E1A0C", strokeWidth=2.5, opacity=60, cap="round")

# --- ripples the raft sheds ----------------------------------------------------------------
for i, (cx, cy, rx, ry, op) in enumerate([(505, 480, 320, 150, 22),
                                         (505, 480, 360, 178, 14)]):
    d.shape("ellipse", f"Ripple {i+1}", x=cx - rx, y=cy - ry,
            width=rx * 2, height=ry * 2, fill=NONE, stroke="#D8EEF2",
            strokeWidth=3, opacity=op)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#16262E", strokeWidth=6)

# --- caption ---------------------------------------------------------------------
d.text("SEA OTTER", "Name", x=500, y=940, size=58, font="Virelai Sans",
       color="#D8E8EC", justify="center")
LINE2, SZ2, TRK = "ENHYDRA LUTRIS", 22, 320
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#98BCC8", justify="center")
if r and "id" in r:
    d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
if r and "id" in r:
    b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
    print("second line bounds", {k: round(v) for k, v in b2.items()})
    assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("sea-otter-V1R00")
