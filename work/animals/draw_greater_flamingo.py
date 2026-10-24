#!/usr/bin/env python3
"""Greater flamingo — field plate V1R00. Profile at the lagoon's edge: the long
S-neck curving down to the sharply bent bill, one pink leg planted in the
shallows while the folded leg tucks beneath, black flight feathers showing at
the rear, ripples and a pale reflection ring the ankle. Teal dusk water, a low
amber salt-glow behind the bird. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Greater Flamingo — Field Plate", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#3A1420"   # dark wine, never pure black

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def linO(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def radO(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c, "opacity": a} for o, c, a in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def disc_x(y, side):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)

def smooth(pts, closed=True):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#0E2024"), (1, "#040B0C"))
PLATE_GRAD = rad((0, "#58A09C"), (0.55, "#2E6468"), (1, "#0E2E34"))
BODY_GRAD  = rad((0, "#F8AEBC"), (0.55, "#E87E92"), (1, "#BE4E68"))
WING_GRAD  = lin(500, 400, 700, 560, (0, "#E07088"), (1, "#A83A54"))
NECK_GRAD  = rad((0, "#F6BEC8"), (0.6, "#E894A4"), (1, "#C06078"))
WATER_GRAD = lin(0, 720, 0, 880, (0, "#3E8284"), (0.4, "#26585E"), (1, "#123238"))

# --- backdrop + lagoon plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#3E8284", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840, fill=PLATE_GRAD, stroke=NONE)

# salt-glow: a low amber dusk blooming on the horizon behind the bird
d.shape("ellipse", "Salt glow", x=230, y=430, width=460, height=270,
        fill=radO((0, "#F0B478", 30), (0.55, "#E89A68", 14), (1, "#E89A68", 0)), stroke=NONE)
d.shape("ellipse", "Glow core", x=330, y=500, width=240, height=130,
        fill=radO((0, "#F8CCA0", 26), (1, "#F8CCA0", 0)), stroke=NONE)
# faint dusk clouds catching the glow, high in the disc
for i, (x, y, w, op) in enumerate([(220, 220, 210, 20), (560, 180, 190, 16), (400, 140, 150, 14)]):
    assert on_disc(x + w / 2, y + 18, 24), i
    d.shape("ellipse", f"Cloud {i+1}", x=x, y=y, width=w, height=36,
            fill=radO((0, "#E8A87C", op), (1, "#E8A87C", 0)), stroke=NONE)
# a few distant birds, salt-glow silhouettes
for i, (x, y, s_) in enumerate([(280, 300, 1.0), (330, 280, 0.75), (705, 330, 0.8)]):
    d.path(f"M{x - 14 * s_},{y} Q{x - 5 * s_},{y - 8 * s_} {x},{y} "
           f"Q{x + 5 * s_},{y - 8 * s_} {x + 14 * s_},{y}",
           f"Distant bird {i+1}", fill=NONE, stroke="#2A3E42", strokeWidth=3 * s_,
           opacity=55, cap="round")

# --- the lagoon floor: shallow water closing on the disc arc -----------------------
wy = 726
wl, wr = disc_x(wy, -1), disc_x(wy, 1)
d.path(f"M{wl:.1f},{wy} C280,716 400,734 500,724 C600,714 700,732 {wr:.1f},{wy} "
       f"A{PR},{PR} 0 0 1 {wl:.1f},{wy} Z", "Lagoon", fill=WATER_GRAD, stroke=NONE)
# warm light licking the waterline
d.path(f"M{wl + 14:.1f},{wy} C290,718 400,732 500,724 C600,716 700,730 {wr - 14:.1f},{wy}",
       "Waterline light", fill=NONE, stroke="#F0B478", strokeWidth=4, opacity=40, cap="round")
# deeper cold band at the disc's floor
d.path(f"M{disc_x(800, -1):.1f},800 C360,786 640,786 {disc_x(800, 1):.1f},800 "
       f"A{PR},{PR} 0 0 1 {disc_x(800, -1):.1f},800 Z",
       "Deep band", fill="#0A2428", opacity=55, stroke=NONE)
# soft wavelets
for i, (x, y, w) in enumerate([(300, 760, 90), (560, 748, 110), (420, 782, 80), (660, 776, 70)]):
    d.path(f"M{x},{y} Q{x + w / 2},{y - 9} {x + w},{y}",
           f"Wavelet {i+1}", fill=NONE, stroke="#6EA8A4", strokeWidth=3, opacity=35, cap="round")

# --- folded leg + standing leg --------------------------------------------------------------
# folded leg: thigh angled down-back, shin folded up beneath the feathers
d.path("M616,556 L660,606 L648,646", "Folded leg", fill=NONE,
       stroke="#D0667E", strokeWidth=9, cap="round")
d.shape("ellipse", "Folded joint", x=653, y=598, width=15, height=15, fill="#D0667E", stroke=NONE)
# standing leg: straight down with the back-bending ankle mid-way, into the water
d.path("M576,548 L570,646 L576,724 L578,742", "Standing leg", fill=NONE,
       stroke="#E8788E", strokeWidth=8, cap="round")
d.shape("ellipse", "Ankle knot", x=563, y=638, width=15, height=15, fill="#E8788E", stroke=NONE)
# ripples where the ankle meets the lagoon
for i, (w, h, op) in enumerate([(54, 14, 55), (92, 22, 40), (136, 30, 26)]):
    d.shape("ellipse", f"Ripple {i+1}", x=576 - w / 2, y=742 - h / 2, width=w, height=h,
            fill=NONE, stroke="#9ED0C8", strokeWidth=3, opacity=op)
# the leg dimming below the waterline
d.path("M576,742 L578,762", "Leg below water", fill=NONE, stroke="#E8788E",
       strokeWidth=7, opacity=35, cap="round")
# the pale reflection smear under the body on the lagoon skin
d.shape("ellipse", "Reflection", x=500, y=740, width=220, height=34,
        fill="#F0A0B0", opacity=16, stroke=NONE)

# --- body: deep oval, breast low-left, back rising to the folded wing --------------------
BODY = [(452, 520), (470, 452), (540, 402), (630, 396), (704, 420),
        (748, 462), (744, 512), (704, 556), (628, 580), (540, 576), (478, 556)]
d.path(smooth(BODY), "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=4)
# underbelly shade + breast light
d.path("M500,540 C560,586 660,586 716,536 C700,592 540,600 500,540 Z",
       "Underbelly shade", fill="#8E3048", opacity=35, stroke=NONE)
d.shape("ellipse", "Breast light", x=470, y=430, width=150, height=90,
        fill="#FCD4DC", opacity=30, stroke=NONE)

# wing: the folded covert mass with scalloped rows, black flights peeking at the rear
d.path("M540,430 C610,404 700,416 742,458 C720,470 700,478 686,496 "
       "C650,522 576,522 540,500 C520,478 522,452 540,430 Z",
       "Wing", fill=WING_GRAD, stroke=NONE)
for i, (y, op) in enumerate([(470, 45), (496, 40)]):
    d.path(f"M556,{y} C610,{y - 16} 676,{y - 8} 716,{y + 10}",
           f"Covert row {i+1}", fill=NONE, stroke="#F4A0B0", strokeWidth=4, opacity=op, cap="round")
# black flight feathers fanning past the tail
for i, (dd, w_) in enumerate([("M700,470 C760,478 800,506 820,540 C780,540 740,524 706,506", 0),
                              ("M692,492 C748,510 782,540 796,576 C760,568 726,548 700,526", 0),
                              ("M676,510 C724,534 750,566 758,600 C726,588 702,564 686,538", 0)]):
    d.path(dd + " Z", f"Flight {i+1}", fill="#241822", opacity=88, stroke=NONE)
    d.path(dd, f"Flight edge {i+1}", fill=NONE, stroke="#4A2832", strokeWidth=3, opacity=60, cap="round")

# --- neck: the long S leaving the breast, rising, then the head dipping low --------------
d.path(smooth([(520, 470), (468, 440), (428, 400), (410, 356), (420, 312),
               (446, 284), (478, 276), (470, 296), (452, 316), (446, 352),
               (456, 392), (482, 428), (530, 462)]),
       "Neck", fill=NECK_GRAD, stroke=INK, strokeWidth=4)
# throat shade down the inner curve + a light along the back of the neck
d.path("M452,318 C442,352 450,392 474,424", "Throat shade", fill=NONE,
       stroke="#B04E66", strokeWidth=6, opacity=40, cap="round")
d.path("M424,352 C418,392 438,430 472,452", "Neck light", fill=NONE,
       stroke="#FCD8DE", strokeWidth=5, opacity=35, cap="round")

# --- head + the broken bill -----------------------------------------------------------------
d.path(smooth([(478, 276), (452, 262), (424, 260), (404, 272), (398, 290),
               (412, 302), (440, 304), (462, 296), (470, 292)]),
       "Head", fill=NECK_GRAD, stroke=INK, strokeWidth=4)
# pale lore patch between eye and bill
d.shape("ellipse", "Lore", x=404, y=270, width=26, height=18, fill="#F8D0D6", opacity=60, stroke=NONE)
d.shape("ellipse", "Eye", x=420, y=272, width=12, height=12, fill="#2A1018", stroke=NONE)
d.shape("ellipse", "Eye glint", x=423, y=274, width=4, height=4, fill="#FFF0F2", opacity=85, stroke=NONE)
# the bill: pink base hinging down at the midpoint, black scoop tip
d.path("M404,278 C384,278 366,286 358,300 C352,312 352,324 356,336 "
       "L388,344 C390,332 392,318 396,308 C400,296 406,288 412,282 Z",
       "Bill", fill=lin(360, 280, 392, 344, (0, "#F0A8AE"), (1, "#D4748A")),
       stroke=INK, strokeWidth=3)
d.path("M358,318 C354,328 356,338 362,346 C370,356 382,360 394,356 "
       "C398,348 394,340 386,336 C376,332 366,326 358,318 Z",
       "Bill tip", fill="#241822", stroke=NONE)
d.path("M396,302 C390,310 388,322 388,334", "Bill hinge", fill=NONE,
       stroke="#8E3048", strokeWidth=3, opacity=60, cap="round")

# plate rim on top so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#06181A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BFE0DA", strokeWidth=3, opacity=28)

# --- name + second line ----------------------------------------------------------------------
r1 = d.text("GREATER FLAMINGO", "Name", x=500, y=940, size=56, font="Virelai Sans",
            color="#DCF0EA", justify="center")
LINE2, SZ2, TRK = "PHOENICOPTERUS ROSEUS", 22, 200
r = d.text(LINE2, "Second line", x=500, y=975, size=SZ2, font="Virelai Sans",
           color="#9EC4B8", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
for rr, lim in ((r1, 800), (r, 760)):
    b = find(layers, rr["id"])["bounds"]
    print("caption bounds", {k: round(v) for k, v in b.items()})
    assert b["width"] <= lim and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("greater-flamingo-V1R00")
