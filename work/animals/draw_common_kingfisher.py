#!/usr/bin/env python3
"""Common kingfisher — field plate V1R00. A turquoise bolt hunched on a snag
over the river: dagger bill levelled at the water, crown barred in teal, the
electric cyan stripe running down the back, rusty breast, white throat patch,
tiny orange feet. Below, a fish flashes pale under the surface inside its own
ripple rings. Riverbank plate, fish-flash mood — dark water, reed darks.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Common Kingfisher — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#14181A"   # warm dark ink, never pure black

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

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0A1414"), (1, "#030707"))
PLATE_GRAD = rad((0, "#7E9E96"), (0.55, "#46685E"), (1, "#182B26"))
WATER_GRAD = lin(0, 700, 0, 880, (0, "#3A7E8A"), (0.5, "#1E4A54"), (1, "#0E2A32"))
BACK_GRAD  = lin(480, 400, 620, 640, (0, "#3AC8DC"), (0.55, "#2E8FA8"), (1, "#17566E"))
ORANGE_GRAD = rad((0, "#E8842E"), (0.65, "#CE6A20"), (1, "#9E4814"))
BILL_GRAD  = lin(445, 455, 315, 490, (0, "#2E343A"), (1, "#14171B"))

# --- backdrop + riverbank plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#7E9E96", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#12231E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D4E2DC", strokeWidth=3, opacity=35)

# a cool shaft of bank light, upper right
d.shape("ellipse", "Bank light", x=540, y=120, width=340, height=230,
        fill=rad((0, "#E4ECDC", 24), (0.6, "#E4ECDC", 9), (1, "#E4ECDC", 0)), stroke=NONE)

# willow wands hanging in from the top rim
for i, (x, y, ln, s) in enumerate([(230, 175, 145, 1), (275, 135, 115, -1),
                                   (745, 160, 155, -1), (795, 215, 105, 1)]):
    assert on_disc(x, y, 15) and on_disc(x + 10 * s, y + ln, 15), (x, y)
    d.path(f"M{x},{y} C{x + 8 * s},{y + ln * 0.4:.0f} {x + 4 * s},{y + ln * 0.8:.0f} {x + 10 * s},{y + ln}",
           f"Wand {i+1}", fill=NONE, stroke="#223A30", strokeWidth=4,
           opacity=50, cap="round")
    for k in range(3):
        ly = y + 30 + k * (ln / 3.4)
        lx = x + 5 * s * (k + 1)
        d.path(f"M{lx:.0f},{ly:.0f} l{14 * s},{4} M{lx:.0f},{ly + 4:.0f} l{12 * s},6",
               f"Wand {i+1} leaf {k+1}", fill=NONE, stroke="#2E4A3C",
               strokeWidth=3, opacity=45, cap="round")

# --- the river: a dark reach of water closing on the disc's own arc -----------------
yl, yr = 706, 726
xl, xr = rim_x(yl, -1), rim_x(yr, 1)
d.path(f"M{xl:.1f},{yl} C280,698 400,712 540,704 C660,697 760,714 {xr:.1f},{yr} "
       f"A{PR},{PR} 0 0 1 {xl:.1f},{yl} Z", "Water", fill=WATER_GRAD, stroke=NONE)
# surface light along the waterline
d.path(f"M{xl + 8:.1f},{yl} C280,698 400,712 540,704 C660,697 760,714 {xr - 8:.1f},{yr}",
       "Waterline light", fill=NONE, stroke="#9EC8C0", strokeWidth=3.5, opacity=45, cap="round")
# the fish, pale under the surface, inside its own ripple rings
d.path("M600,762 C632,748 668,750 694,768 C668,782 628,784 600,774 Z "
       "M694,768 L718,754 L714,778 Z",
       "Fish", fill="#C4B98E", opacity=40, stroke=NONE)
d.shape("ellipse", "Fish eye", x=615, y=758, width=6, height=6,
        fill="#1E2A28", opacity=55, stroke=NONE)
d.path("M596,758 C580,752 566,754 556,762", "Fish wake", fill=NONE,
       stroke="#9EC8C0", strokeWidth=3, opacity=35, cap="round")
for i, (w, op) in enumerate([(150, 30), (210, 22), (270, 15)]):
    d.shape("ellipse", f"Ripple {i+1}", x=640 - w / 2, y=762 - w / 8, width=w, height=w / 4,
            fill=NONE, stroke="#9EC8C0", strokeWidth=3, opacity=op)
# current strokes drifting downstream
for i, (x, y, ln) in enumerate([(280, 760, 70), (390, 800, 80), (750, 790, 65)]):
    d.path(f"M{x},{y} C{x + ln * 0.4:.0f},{y - 6} {x + ln * 0.7:.0f},{y + 5} {x + ln},{y}",
           f"Current {i+1}", fill=NONE, stroke="#5E9A94", strokeWidth=3,
           opacity=30, cap="round")
# reed darks standing in the water at the left
for i, (x, h) in enumerate([(215, 120), (245, 95)]):
    d.path(f"M{x},740 C{x - 5},{740 - h * 0.6:.0f} {x + 4},{740 - h:.0f} {x + 2},{740 - h - 26:.0f}",
           f"Reed {i+1}", fill=NONE, stroke="#1E332A", strokeWidth=5,
           opacity=60, cap="round")

# the snag — a dead branch rising out of the water, flat seat on top
d.path("M452,760 C458,720 470,690 486,668 L505,648 C510,640 518,635 528,634 "
       "L566,630 L566,642 L532,644 C522,646 514,652 508,660 "
       "C490,682 476,720 470,762 Z",
       "Snag", fill=lin(455, 770, 520, 640, (0, "#3A2E22"), (1, "#5E4C36")),
       stroke=INK, strokeWidth=4)
d.path("M520,636 L560,632", "Seat light", fill=NONE,
       stroke="#9E8460", strokeWidth=3, opacity=55, cap="round")
# a little up-thrust twig fork on the snag
d.path("M470,694 C462,676 460,660 464,646", "Snag fork", fill=NONE,
       stroke="#4A3A28", strokeWidth=4, cap="round")
# the bird's contact shade where it grips
d.shape("ellipse", "Grip shade", x=492, y=626, width=90, height=14,
        fill=rad((0, "#100A06", 45), (1, "#100A06", 0)), stroke=NONE)

# === the kingfisher ==============================================================
# the bird draws 1.3x about the perch contact so it fills the plate
import re
K, PX, PY = 1.3, 530, 636

def P(x, y):
    return (PX + K * (x - PX), PY + K * (y - PY))

def T(dstr):
    """scale every x,y pair in path data about (PX,PY)"""
    idx = [0]
    def rep(m):
        v = float(m.group(0))
        r = PX + K * (v - PX) if idx[0] % 2 == 0 else PY + K * (v - PY)
        idx[0] += 1
        return f"{r:.1f}"
    return re.sub(r"-?\d+\.?\d*", rep, dstr)

def bird_path(dstr, label, **kw):
    if "strokeWidth" in kw: kw["strokeWidth"] = kw["strokeWidth"] * K
    return d.path(T(dstr), label, **kw)

def bird_dot(x, y, w, h, label, **kw):
    bx, by = P(x, y)
    return d.shape("ellipse", label, x=bx, y=by, width=w * K, height=h * K, **kw)

# short tail kicking down-right, squared off
bird_path("M560,600 C580,616 600,640 616,668 L628,690 C612,694 596,690 582,678 "
          "C566,664 556,640 552,616 Z",
          "Tail", fill=lin(560, 600, 625, 690, (0, "#2E8FA8"), (1, "#17566E")),
          stroke=INK, strokeWidth=4)
for i in range(2):
    bird_path(f"M{572 + i * 12},{624 + i * 6} L{596 + i * 12},{664 + i * 6}",
              f"Tail split {i+1}", fill=NONE, stroke="#0E3A4A",
              strokeWidth=2.5, opacity=60, cap="round")

# body — orange breast and belly, the pear tilted forward over the bill
bird_path("M470,468 C440,486 428,522 436,556 C444,592 472,618 510,626 "
          "C546,632 578,622 592,598 C604,578 606,552 596,528 "
          "C580,494 540,472 500,464 C488,462 478,464 470,468 Z",
          "Body", fill=ORANGE_GRAD, stroke=INK, strokeWidth=5)
# belly deepening toward the vent
bird_path("M500,560 C530,572 556,588 566,606", "Belly shade", fill=NONE,
          stroke="#8E3E10", strokeWidth=12, opacity=30, cap="round")

# the blue mantle: back + folded wing carried over the shoulders
bird_path("M468,462 C500,442 545,440 578,458 C600,470 610,494 610,520 "
          "C610,548 600,572 584,588 C588,556 584,524 570,498 "
          "C552,470 518,458 486,462 C478,464 472,466 468,462 Z",
          "Mantle", fill=BACK_GRAD, stroke=INK, strokeWidth=4)
# the electric stripe — a bolt of cyan down the back, the bird's name in light
bird_path("M492,452 C528,450 560,462 580,486 C588,496 594,508 598,522 "
          "C586,514 574,504 560,496 C540,480 516,464 492,452 Z",
          "Back flash", fill=rad((0, "#66E4F2"), (0.7, "#3AC8DC"), (1, "#1E7A96")),
          opacity=95, stroke=NONE)
# speckled wing coverts — rows of pale turquoise dots on the folded wing
for row, (yy, n, x0) in enumerate([(492, 4, 516), (518, 4, 522), (544, 3, 530)]):
    for j in range(n):
        x = x0 + j * 22 + (row % 2) * 10
        bird_dot(x, yy, 7, 5, f"Covert spot {row * 4 + j + 1}",
                 fill="#9EDCE8", opacity=65, stroke=NONE)
# covert bar lines under the spots
for i, dd in enumerate(["M510,512 C540,502 568,502 592,514",
                        "M516,540 C544,530 570,530 590,540"]):
    bird_path(dd, f"Covert bar {i+1}", fill=NONE, stroke="#0E3A4A",
              strokeWidth=3, opacity=50, cap="round")

# head — big for the body, crown barred teal, cheek chestnut
bird_path("M446,432 C470,404 516,398 548,416 C576,432 588,462 580,490 "
          "C572,514 548,530 518,530 C486,530 458,514 448,488 "
          "C440,468 438,448 446,432 Z",
          "Head", fill=BACK_GRAD, stroke=INK, strokeWidth=5)
# chestnut cheek — the rufous ear-coverts sweeping under the eye to the breast
bird_path("M452,470 C468,480 492,486 514,490 C532,494 546,504 552,518 "
          "C538,530 512,534 488,528 C464,520 450,500 452,470 Z",
          "Cheek chestnut", fill="#C8601E", opacity=90, stroke=NONE)
# the white neck patch behind the cheek — the other kingfisher tell
bird_path("M556,470 C566,478 570,490 568,502 C558,506 546,502 538,492 "
          "C544,482 550,475 556,470 Z",
          "Neck patch", fill="#F0EBDC", opacity=95, stroke="#A89E88", strokeWidth=2)
# crown barring — fine dark arcs across the teal cap
for i, (y, w) in enumerate([(424, 60), (438, 78), (452, 88)]):
    bird_path(f"M{500 - w / 2},{y} Q500,{y + 10} {500 + w / 2},{y}",
              f"Crown bar {i+1}", fill=NONE, stroke="#0E3A4A", strokeWidth=3,
              opacity=55, cap="round")

# the dagger — long, straight, levelled at the water, a whisper of red at the base
bird_path("M452,448 C430,454 390,462 352,470 C338,473 322,478 310,484 "
          "C322,490 344,492 368,490 C400,486 432,478 452,470 "
          "C458,462 458,454 452,448 Z",
          "Bill", fill=BILL_GRAD, stroke=INK, strokeWidth=4)
bird_path("M448,470 C420,480 380,488 348,490", "Mandible split", fill=NONE,
          stroke="#05070A", strokeWidth=2.5, opacity=70, cap="round")
bird_path("M450,472 C438,478 424,482 410,485", "Bill base red", fill=NONE,
          stroke="#B8482A", strokeWidth=4, opacity=70, cap="round")
bird_path("M448,452 C420,458 388,464 360,470", "Culmen light", fill=NONE,
          stroke="#5E6A72", strokeWidth=2.5, opacity=50, cap="round")
# dark lore — the mask line from bill base through the eye
bird_path("M452,452 C470,442 494,438 514,442 C500,452 480,458 462,458 Z",
          "Lore", fill="#0E1214", opacity=85, stroke=NONE)

# eye — a dark bead set in the lore, one glint
bird_dot(486, 444, 20, 20, "Eye", fill="#10151A", stroke=INK, strokeWidth=2.5)
bird_dot(491, 447, 5, 5, "Glint", fill="#F4F8F2", opacity=90, stroke=NONE)

# legs + feet — bright orange wire gripping the snag seat
for i, (x, y) in enumerate([(515, 612), (548, 616)]):
    bird_path(f"M{x},{y} C{x - 3},{y + 8} {x - 2},{y + 12} {x},{y + 16}",
              f"Leg {i+1}", fill=NONE, stroke="#D8552A", strokeWidth=6, cap="round")
    fx, fy = P(x, y + 16)
    for k, (tx, ty) in enumerate([(-14, 4), (-4, 7), (7, 7), (15, 3)]):
        tx, ty = tx * K, ty * K
        d.path(f"M{fx:.1f},{fy:.1f} C{fx + tx * 0.5:.1f},{fy + 3:.1f} "
               f"{fx + tx * 0.8:.1f},{fy + ty * 0.6:.1f} {fx + tx:.1f},{fy + ty:.1f}",
               f"Toe {i * 4 + k + 1}", fill=NONE, stroke="#D8552A",
               strokeWidth=4 * K, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0E1C16", strokeWidth=6)
d.shape("ellipse", "Plate inner ring 2", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D4E2DC", strokeWidth=3, opacity=28)

# --- name -------------------------------------------------------------------------
r1 = d.text("COMMON KINGFISHER", "Name", x=500, y=962, size=56, font="Virelai Sans",
            color="#D4E2DC", justify="center")

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

d.finish("common-kingfisher-V1R00")
