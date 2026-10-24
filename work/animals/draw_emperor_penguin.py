#!/usr/bin/env python3
"""Emperor penguin — field-guide plate V1R00. Front-on upright, head tipped a
quarter left: black hood, gold auricular patches melting into the pale chest,
white belly, decurved bill with its rose stripe. A downy chick huddles at the
feet — the coldest nursery on Earth. Whiteout plate: blowing snow, a ghost
huddle at the horizon, ice floor closing on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math, re, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Emperor Penguin — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#10141A"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

def mirror(dd):
    out, toks, ex = [], re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd), True
    for t in toks:
        if t.isalpha():
            out.append(t); ex = True
        elif ex:
            out.append(f"{1000 - float(t):g},"); ex = False
        else:
            out[-1] += f"{float(t):g}"; ex = True
    return " ".join(out)

def pair(dd, label, **kw):
    d.path(dd, f"{label} L", **kw)
    d.path(mirror(dd), f"{label} R", **kw)

BG_GRAD = lin(0, 0, 0, 1000, (0, "#101822"), (1, "#04070C"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#9FB4C4"), (0.45, "#D4E0E8"), (1, "#EDF3F6"))
ICE_GRAD = lin(0, 700, 0, 880, (0, "#C8D8E2"), (1, "#7E97A6"))
BODY_GRAD = rad((0, "#2E3844"), (0.55, "#1C242E"), (1, "#0B0F15"))
BELLY_GRAD = lin(0, 400, 0, 760, (0, "#F4E2AC"), (0.3, "#F4F2EC"), (1, "#D6E0E8"))
HEAD_GRAD = rad((0, "#38404C"), (0.6, "#1A212A"), (1, "#0A0E13"))
GOLD_GRAD = lin(0, 340, 0, 460, (0, "#E8A83E"), (0.6, "#F2CE74"), (1, "#F6E8BC"))
CHICK_GRAD = rad((0, "#A8B0B4"), (0.7, "#7E868C"), (1, "#565E64"))
BILL_GRAD = lin(0, 300, 0, 380, (0, "#2A3038"), (1, "#10141A"))

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#AEC2D0", opacity=10, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5E7686", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=45)
# whiteout: snow driving across the plate, faint horizontal streaks
rng = random.Random(9)
for i in range(26):
    x = 140 + rng.uniform(0, 720); y = 100 + rng.uniform(0, 540)
    ln = rng.uniform(20, 70)
    if not (on_disc(x, y, 20) and on_disc(x + ln, y + ln * 0.12, 20)):
        continue
    d.path(f"M{x:.0f},{y:.0f} L{x + ln:.0f},{y + ln * 0.12:.0f}", f"Snow streak {i+1}",
           fill=NONE, stroke="#FFFFFF", strokeWidth=2, opacity=18, cap="round")
for i, (x, y, w) in enumerate([(210,180,5),(760,160,6),(170,340,5),(840,320,6),(320,110,5),
                               (680,110,5),(250,480,5),(810,470,5),(430,120,4),(590,140,4)]):
    assert on_disc(x + w/2, y + w/2, 8), (x, y)
    d.shape("ellipse", f"Flake {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=55, stroke=NONE)
# ghost huddle at the horizon: the colony lost in the blow
for i, (x, y, w, h, op) in enumerate([(230,590,34,66,20),(280,600,28,54,16),(740,592,36,68,20),
                                      (790,606,26,50,15),(360,600,24,44,13),(680,602,24,46,13)]):
    assert on_disc(x, y, 5)
    d.shape("ellipse", f"Huddle ghost {i+1}", x=x - w/2, y=y - h, width=w, height=h,
            fill="#6E8292", opacity=op, stroke=NONE)
    d.shape("ellipse", f"Huddle head {i+1}", x=x - w*0.3, y=y - h - 8, width=w*0.6, height=h*0.4,
            fill="#6E8292", opacity=op, stroke=NONE)

# --- ice floor, closing on the disc's own arc ---------------------------------------
fy = 700
fdx = math.sqrt(R * R - (fy - CY) ** 2)
x0, x1 = CX - fdx, CX + fdx
d.path(f"M{x0:.1f},{fy} C330,694 670,694 {x1:.1f},{fy} "
       f"A{R},{R} 0 0 1 {x0:.1f},{fy} Z", "Ice floor", fill=ICE_GRAD, stroke=NONE)
d.path(f"M{x0 + 4:.1f},{fy} C330,694 670,694 {x1 - 4:.1f},{fy}",
       "Horizon light", fill=NONE, stroke="#F4FAFC", strokeWidth=3, opacity=50, cap="round")
# pressure ridges + spindrift on the ice
for i, dd in enumerate(["M220,760 C330,752 430,754 520,758", "M560,786 C650,780 740,782 800,788",
                        "M280,830 C400,824 540,826 650,830"]):
    d.path(dd, f"Ice ridge {i+1}", fill=NONE, stroke="#8EA4B2",
           strokeWidth=4, opacity=35, cap="round")
for i, dd in enumerate(["M170,712 C290,706 420,708 470,712", "M560,716 C660,710 760,712 830,718"]):
    d.path(dd, f"Spindrift {i+1}", fill=NONE, stroke="#FFFFFF",
           strokeWidth=5, opacity=22, cap="round")
# contact shadow on the ice
d.shape("ellipse", "Penguin shadow", x=390, y=764, width=230, height=26,
        fill="#4E6474", opacity=35, stroke=NONE)

# --- feet + tail stub first (they tuck under the body) --------------------------------
for sgn in (-1, 1):
    fx = 500 + sgn * 46
    d.path(f"M{fx - 40},770 C{fx - 44},758 {fx - 30},750 {fx - 8},750 "
           f"C{fx + 22},750 {fx + 44},756 {fx + 46},768 "
           f"C{fx + 40},778 {fx + 16},782 {fx - 2},782 C{fx - 24},782 {fx - 38},778 {fx - 40},770 Z",
           f"Foot {'L' if sgn < 0 else 'R'}", fill=lin(0, 750, 0, 782, (0, "#2E363E"), (1, "#14181E")),
           stroke=INK, strokeWidth=3.5)
    for k in range(3):
        tx = fx - 26 + sgn * k * 14 if sgn < 0 else fx - 26 + k * 14
        d.path(f"M{tx},{774} L{tx + 12},{776}", f"Toe seam {'L' if sgn < 0 else 'R'}{k}",
               fill=NONE, stroke="#0A0E12", strokeWidth=2, opacity=60, cap="round")

# --- body: the upright teardrop ---------------------------------------------------------
BODY = ("M500,264 C542,264 568,286 574,318 C579,346 572,370 556,388 "
        "C596,422 620,472 626,530 C632,596 622,662 600,706 "
        "C582,742 546,756 500,756 C454,756 418,742 400,706 "
        "C378,662 368,596 374,530 C380,472 404,422 444,388 "
        "C428,370 421,346 426,318 C432,286 458,264 500,264 Z")
d.path(BODY, "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)

# belly shield: white, with the gold chest wash pouring in from the throat
BELLY = ("M500,396 C456,398 424,424 408,468 C392,516 390,584 402,646 "
         "C414,706 452,742 500,744 C548,742 586,706 598,646 "
         "C610,584 608,516 592,468 C576,424 544,398 500,396 Z")
d.path(BELLY, "Belly", fill=BELLY_GRAD, stroke=NONE)
# belly edge feathering: a soft dark seam where black meets white
d.path("M408,468 C392,516 390,584 402,646 M592,468 C608,516 610,584 598,646",
       "Belly seam", fill=NONE, stroke="#8A9298", strokeWidth=3, opacity=30, cap="round")
# the gold wash: auricular glow spreading across the upper chest
d.path("M500,352 C468,356 446,378 438,412 C432,438 436,462 452,478 "
       "C470,492 530,492 548,478 C564,462 568,438 562,412 "
       "C554,378 532,356 500,352 Z", "Chest gold wash",
       fill=GOLD_GRAD, opacity=80, stroke=NONE)
# auricular patches: the signature orange-gold flames on each cheek
pair("M474,332 C456,334 442,346 438,364 C434,380 438,398 450,408 "
     "C460,416 472,414 478,402 C482,388 480,358 474,332 Z",
     "Auricular patch", fill=lin(0, 332, 0, 416, (0, "#E8A83E"), (1, "#F2CE74")),
     opacity=85, stroke=NONE)
# faint fade strokes where the gold dissolves into the chest
pair("M486,416 C480,432 482,448 490,460", "Gold fade",
     fill=NONE, stroke="#F2CE74", strokeWidth=8, opacity=25, cap="round")

# --- flippers: dark blades pinned along the flanks --------------------------------------
pair("M404,430 C388,470 384,540 392,606 C396,648 410,682 428,700 "
     "C422,660 418,600 420,540 C421,496 418,458 404,430 Z",
     "Flipper", fill=lin(0, 430, 0, 700, (0, "#232C36"), (1, "#0C1015")),
     stroke=INK, strokeWidth=4)
pair("M404,452 C396,500 394,560 400,614", "Flipper sheen",
     fill=NONE, stroke="#7E94A6", strokeWidth=4, opacity=30, cap="round")

# --- head ----------------------------------------------------------------------------------
HEAD = ("M500,256 C540,256 566,276 572,308 C578,336 570,362 552,378 "
        "C536,392 518,398 500,398 C482,398 464,392 448,378 "
        "C430,362 422,336 428,308 C434,276 460,256 500,256 Z")
d.path(HEAD, "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Crown light", x=460, y=264, width=80, height=26,
        fill="#8A9AAA", opacity=25, stroke=NONE)
# the eye, tipped a quarter left
d.shape("ellipse", "Eye", x=466, y=308, width=13, height=12, fill="#06080C", stroke=NONE)
d.shape("ellipse", "Eye glint", x=469, y=310, width=3.5, height=3.5, fill="#FFFFFF",
        opacity=85, stroke=NONE)
d.shape("ellipse", "Far eye", x=524, y=310, width=9, height=9, fill="#0A0E14", stroke=NONE)
# the decurved bill: upper black, rose-orange stripe along the lower mandible
d.path("M486,318 C458,320 430,330 410,348 C400,358 398,368 404,374 "
       "C424,368 452,362 478,356 C486,348 488,332 486,318 Z",
       "Bill", fill=BILL_GRAD, stroke=INK, strokeWidth=3.5)
d.path("M412,364 C432,354 458,346 480,342 C484,344 484,348 482,352 "
       "C462,358 438,364 416,370 C412,368 411,366 412,364 Z",
       "Bill stripe", fill=lin(0, 342, 0, 370, (0, "#E8946A"), (1, "#C66A48")),
       stroke="#8A4A34", strokeWidth=1.5)
d.shape("ellipse", "Nostril", x=470, y=326, width=5, height=3, fill="#06080C",
        opacity=80, stroke=NONE)
# throat shadow under the chin
d.path("M470,386 C490,394 516,394 536,384", "Chin shade",
       fill=NONE, stroke="#06090E", strokeWidth=8, opacity=35, cap="round")

# --- the chick: grey down huddled at the feet ------------------------------------------
chx, chy = 640, 706
d.shape("ellipse", "Chick shadow", x=chx - 52, y=chy + 48, width=104, height=16,
        fill="#4E6474", opacity=30, stroke=NONE)
d.path(f"M{chx},{chy - 8} C{chx + 36},{chy - 8} {chx + 52},{chy + 14} {chx + 52},{chy + 36} "
       f"C{chx + 52},{chy + 52} {chx + 30},{chy + 60} {chx},{chy + 60} "
       f"C{chx - 30},{chy + 60} {chx - 52},{chy + 52} {chx - 52},{chy + 36} "
       f"C{chx - 52},{chy + 14} {chx - 36},{chy - 8} {chx},{chy - 8} Z",
       "Chick", fill=CHICK_GRAD, stroke=INK, strokeWidth=4)
# downy fuzz ticks around the chick's edge
for k, a in enumerate(range(200, 341, 20)):
    t = math.radians(a)
    x, y = chx + 52 * math.cos(t), chy + 34 + 26 * math.sin(t)
    d.path(f"M{x - 4:.0f},{y - 3:.0f} L{x + 4:.0f},{y + 3:.0f}", f"Chick fuzz {k+1}",
           fill=NONE, stroke="#B8C0C4", strokeWidth=2, opacity=45, cap="round")
# the chick's face: dark horseshoe mask + pale heart
d.path(f"M{chx},{chy + 6} C{chx - 20},{chy + 6} {chx - 28},{chy + 18} {chx - 28},{chy + 32} "
       f"C{chx - 28},{chy + 44} {chx - 16},{chy + 50} {chx},{chy + 50} "
       f"C{chx + 16},{chy + 50} {chx + 28},{chy + 44} {chx + 28},{chy + 32} "
       f"C{chx + 28},{chy + 18} {chx + 20},{chy + 6} {chx},{chy + 6} Z",
       "Chick face", fill="#1E242C", stroke=NONE)
d.shape("ellipse", "Chick face heart", x=chx - 17, y=chy + 18, width=34, height=24,
        fill="#E8ECEE", stroke=NONE)
d.shape("ellipse", "Chick eye L", x=chx - 11, y=chy + 24, width=6, height=6, fill="#0A0E12", stroke=NONE)
d.shape("ellipse", "Chick eye R", x=chx + 5, y=chy + 24, width=6, height=6, fill="#0A0E12", stroke=NONE)
d.shape("ellipse", "Chick beak", x=chx - 4, y=chy + 32, width=8, height=5, fill="#10151B", stroke=NONE)

# --- caption ---------------------------------------------------------------------------
r1 = d.text("EMPEROR PENGUIN", "Name", x=500, y=938, size=50, font="Virelai Sans",
            color="#E4EDF2", justify="center")
LINE2, SZ2, TRK = "APTENODYTES FORSTERI", 22, 250
r = d.text(LINE2, "Second line", x=500, y=974, size=SZ2, font="Virelai Sans",
           color="#9AB0BE", justify="center")
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

d.finish("emperor-penguin-V1R00")
