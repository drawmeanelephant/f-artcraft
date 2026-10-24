#!/usr/bin/env python3
"""Lion's mane jellyfish — field-guide plate V1R00. A bell of fire
trailing a hundred feet of nettle: cold-sea plate, drift-sting mood.
Translucent russet bell mid-water, radial lobe striations, ruffled oral
arms, and a broad curtain of nettle tentacles fading into the abyss band
below — the deep closes on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; every tentacle tip stays inside."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Lion's Mane Jellyfish — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#3A0E14"                    # warm dark ink, never pure black
random.seed(11)

def lin(x0, y0, x1, y1, *stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": ss}}

def rad(*stops):
    ss = []
    for s in stops:
        st = {"offset": s[0], "color": s[1]}
        if len(s) > 2: st["opacity"] = s[2]
        ss.append(st)
    return {"gradient": {"kind": "radial", "stops": ss}}

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

def on_disc(x, y, pad=0, r=R):
    return math.hypot(x - CX, y - CY) <= r - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#041420"), (1, "#01060C"))
PLATE_GRAD = rad((0, "#3E7A8C"), (0.5, "#1C4A5A"), (1, "#081E2A"))
BELL_GRAD = rad((0, "#D8543C"), (0.55, "#A02A28"), (1, "#5E1420"))
ARM = "#E8A88E"
NETTLE = "#E8B49A"

# --- backdrop + cold-sea plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=64, y=24, width=872, height=872,
        fill="#3E7A8C", opacity=12, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0A2832", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8E0E4", strokeWidth=3, opacity=40)

# light shafts leaning down through the cold water
for i, (x0, w0, x1, w1, op) in enumerate([(390, 60, 440, 30, 10),
                                         (520, 90, 545, 45, 8),
                                         (640, 50, 620, 26, 12)]):
    d.path(f"M{x0},70 L{x0 + w0},70 L{x1 + w1},560 L{x1},560 Z",
           f"Shaft {i+1}", fill="#BFE0E8", opacity=op, stroke=NONE)
# plankton drift
for i in range(26):
    x, y = random.uniform(150, 850), random.uniform(120, 800)
    if on_disc(x, y, pad=40):
        w = random.uniform(2.5, 5.5)
        d.shape("ellipse", f"Plankton {i+1}", x=x, y=y, width=w, height=w,
                fill="#C8E0E4", opacity=random.choice([25, 35, 45]), stroke=NONE)
# two far-off drifters — the deep is never empty
for i, (x, y, s, op) in enumerate([(218, 300, 0.32, 30), (800, 250, 0.22, 24)]):
    d.path(f"M{x},{y} C{x-30*s},{y-50*s} {x+30*s},{y-50*s} {x+52*s},{y} "
           f"C{x+52*s},{y+14*s} {x+30*s},{y+20*s} {x},{y+16*s} "
           f"C{x-30*s},{y+20*s} {x-30*s},{y+14*s} {x},{y} Z",
           f"Drifter {i+1}", fill="#C8E0E4", opacity=op, stroke=NONE)
    for k in (-1, 0, 1):
        d.path(f"M{x + k*18*s},{y+16*s} C{x + k*22*s},{y+60*s} "
               f"{x + k*14*s},{y+90*s} {x + k*20*s},{y+120*s}",
               f"Drifter arm {i+1}-{k+2}", fill=NONE, stroke="#C8E0E4",
               strokeWidth=max(2, 5*s), opacity=op, cap="round")

# --- the abyss band below, closing on the disc's own arc -----------------------------
fy = 792
fl, fr = rim_x(fy, side=-1), rim_x(fy, side=1)
d.path(f"M{fl:.1f},{fy} C340,780 470,800 600,792 C680,788 740,786 {fr:.1f},{fy} "
       f"A{R},{R} 0 0 1 {fl:.1f},{fy} Z",
       "Abyss band", fill=lin(0, fy, 0, 880, (0, "#06141C", 55), (1, "#020A10", 85)),
       stroke=NONE)

# --- nettle curtain: the hundred feet, trailing and fading ---------------------------
# thick nettle ropes first — the heavy tails of the cluster
ropes = [(330, 448, 296, 846), (415, 452, 386, 858), (585, 452, 614, 858),
         (668, 448, 706, 842), (500, 456, 506, 870)]
for i, (x0, y0, x1, y1) in enumerate(ropes):
    amp = 18 + i * 3
    d.path(f"M{x0},{y0} C{x0 + amp},{y0 + 140} {x1 - amp},{y1 - 160} {x1},{y1}",
           f"Nettle rope {i+1}", fill=NONE,
           stroke=lin(x0, y0, x1, y1, (0, "#C87A5E", 85), (0.75, "#E8B49A", 45),
                      (1, "#E8B49A", 0)),
           strokeWidth=7, cap="round")
# fine nettle mass — dozens of hair-thin trails across the bell's width
for i in range(34):
    x0 = 296 + i * 12.4 + random.uniform(-6, 6)
    y0 = 442 + random.uniform(-6, 16)
    drift = random.uniform(-70, 70)
    x1 = min(max(x0 + drift, rim_x(850) + 14), rim_x(850, side=1) - 14)
    y1 = random.uniform(790, 864)
    amp = random.uniform(10, 34)
    w = random.choice([2.6, 3.0, 3.4])
    d.path(f"M{x0:.0f},{y0:.0f} C{x0 + amp:.0f},{y0 + 130:.0f} "
           f"{x1 - amp:.0f},{y1 - 170:.0f} {x1:.0f},{y1:.0f}",
           f"Nettle {i+1}", fill=NONE,
           stroke=lin(x0, y0, x1, y1, (0, NETTLE, 60), (0.8, NETTLE, 30),
                      (1, NETTLE, 0)),
           strokeWidth=w, cap="round")

# --- ruffled oral arms — the pale curtain under the bell -----------------------------
for i, (x0, w, y1, s) in enumerate([(430, 34, 700, -1), (478, 42, 726, 1),
                                    (524, 38, 708, -1), (566, 30, 676, 1)]):
    d.path(f"M{x0},{440} C{x0 + s*14},{500} {x0 - s*10},{560} {x0 + s*16},{620} "
           f"C{x0 + s*20},{660} {x0 + s*6},{y1 - 20} {x0 + s*4},{y1} "
           f"C{x0 + s*2},{y1 - 30} {x0 + w - s*10},{640} {x0 + w - s*18},{560} "
           f"C{x0 + w - s*8},{500} {x0 + w},{460} {x0 + w},{440} Z",
           f"Oral arm {i+1}", fill=ARM, opacity=62, stroke="#8A3A34",
           strokeWidth=2.5)
    # the frill down each arm's centre
    d.path(f"M{x0 + w/2},{452} C{x0 + w/2 + s*18},{520} {x0 + w/2 - s*14},{600} "
           f"{x0 + w/2 + s*10},{y1 - 30}",
           f"Oral frill {i+1}", fill=NONE, stroke="#F2C8B4",
           strokeWidth=4, opacity=45, cap="round")

# --- the bell of fire -----------------------------------------------------------------
# dome with a gently scalloped margin of eight lobes
d.path("M252,408 C262,288 368,216 500,212 C632,216 738,288 748,408 "
       "C746,424 734,432 718,430 C700,428 690,440 672,438 "
       "C652,436 646,448 626,446 C606,444 600,452 580,450 "
       "C560,448 552,456 532,454 C512,452 504,458 484,456 "
       "C464,454 456,448 436,450 C416,452 408,444 388,446 "
       "C368,448 360,438 340,440 C320,442 310,432 292,434 "
       "C272,436 258,426 252,408 Z",
       "Bell", fill=BELL_GRAD, stroke=INK, strokeWidth=6, opacity=94)
# translucent cap of cold light on the crown
d.shape("ellipse", "Bell crown light", x=350, y=236, width=300, height=110,
        fill="#F2C88E", opacity=18, stroke=NONE)
# radial lobe striations fanning from the apex
for k in range(9):
    t = k / 8.0
    xm = 300 + t * 400
    xe = 292 + t * 416
    d.path(f"M500,222 C{430 + t*140:.0f},{270} {xm:.0f},{350} {xe:.0f},{430}",
           f"Lobe ray {k+1}", fill=NONE, stroke="#F2C88E",
           strokeWidth=3.5, opacity=22, cap="round")
# darker seams between the lobes
for k in range(8):
    t = (k + 0.5) / 8.0
    xe = 288 + t * 424
    d.path(f"M500,226 C{436 + t*128:.0f},{280} {300 + t*400:.0f},{356} {xe:.0f},{432}",
           f"Lobe seam {k+1}", fill=NONE, stroke="#5E1420",
           strokeWidth=3, opacity=30, cap="round")
# margin shadow — the bell's folded underside lip
d.path("M258,404 C300,432 380,448 500,452 C620,448 700,432 742,404 "
       "C700,442 610,462 500,464 C390,462 300,442 258,404 Z",
       "Margin lip", fill="#4A1018", opacity=45, stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#04101C", strokeWidth=6)

# --- name ---------------------------------------------------------------------------
d.text("LION'S MANE JELLYFISH", "Name", x=500, y=962, size=46, font="Virelai Sans",
       color="#C8E0E4", justify="center")

d.finish("lions-mane-jellyfish-V1R00")
