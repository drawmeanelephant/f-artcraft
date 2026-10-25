#!/usr/bin/env python3
"""Giant anteater — field plate V1R00. Full body in profile walking left,
snout low, huge brush tail sweeping behind. Diagonal pale-edged dark
shoulder band; forefeet knuckle-walk with claws folded back. Muted
burnt-grass Cerrado disc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Giant Anteater — Field Plate", 1000, 1000)

INK = "#2E1D12"
CX, CY, R = 500, 460, 420

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#241B10"), (1, "#0C0704"))
PLATE_GRAD = rad((0, "#CBB98C"), (0.65, "#9E885C"), (1, "#66522F"))
COAT_GRAD  = lin(500, 415, 500, 630, (0, "#C6B494"), (0.55, "#998560"), (1, "#6B593A"))
LEG_GRAD   = lin(440, 560, 440, 745, (0, "#A18C64"), (1, "#63502F"))
LEG_FAR    = lin(400, 560, 400, 745, (0, "#7E6C48"), (1, "#4A3B22"))
TAIL_GRAD  = lin(650, 430, 860, 540, (0, "#B6A480"), (0.55, "#8A7450"), (1, "#57452B"))
BAND_GRAD  = lin(370, 590, 520, 445, (0, "#2A1C10"), (1, "#140C05"))
GROUND_GRAD = lin(0, 720, 0, 880, (0, "#8C7647"), (1, "#4E3E22"))
CREAM = "#EDE0BE"

def on_disc(x, y, pad=10):
    return math.hypot(x - CX, y - CY) <= R - pad

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3A2C17", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D6AC", strokeWidth=3, opacity=28)
# patina flecks, all inside the disc
for i, (x, y, w, o) in enumerate([(190, 250, 9, 38), (770, 220, 7, 34), (160, 480, 8, 32),
                                  (830, 620, 9, 36), (300, 180, 7, 30), (650, 160, 8, 34),
                                  (240, 690, 7, 32), (760, 720, 8, 30), (420, 130, 6, 30),
                                  (150, 620, 6, 30), (860, 380, 7, 32), (560, 810, 7, 30)]):
    assert on_disc(x + w / 2, y + w / 2), (x, y)
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6B5636", opacity=o, stroke=NONE)
# two distant grass-fire birds, tiny and faint
d.path("M300,196 Q312,186 326,196 M336,190 Q346,182 358,190", "Distant birds",
       fill=NONE, stroke="#5C4A2C", strokeWidth=4, opacity=40, cap="round")

# --- Cerrado ground: chord of the disc, closes on the arc ----------------------
gy = 742
gdx = math.sqrt(R * R - (gy - CY) ** 2)
d.path(f"M{CX-gdx:.1f},{gy} C300,730 420,738 520,734 C620,730 720,736 {CX+gdx:.1f},{gy} "
       f"A{R},{R} 0 0 1 {CX-gdx:.1f},{gy} Z", "Ground", fill=GROUND_GRAD, stroke=NONE)
d.path("M205,742 C300,731 420,739 520,735 C620,731 715,737 795,742", "Ground crest light",
       fill=NONE, stroke="#C7B083", strokeWidth=4, opacity=45, cap="round")
# dry grass tufts on the crest
for i, (x, s) in enumerate([(252, 1), (330, -1), (560, 1), (700, -1), (770, 1)]):
    d.path(f"M{x},{gy-4} Q{x+4*s},{gy-22} {x+10*s},{gy-30} "
           f"M{x+8*s},{gy-4} Q{x+12*s},{gy-18} {x+18*s},{gy-24}",
           f"Grass tuft {i+1}", fill=NONE, stroke="#4E3D1E", strokeWidth=4,
           opacity=65, cap="round")
# seed heads drifting right of the tail
for i, (x, y, w) in enumerate([(760, 640, 6), (800, 600, 5), (835, 660, 6), (790, 560, 5)]):
    assert on_disc(x, y), (x, y)
    d.shape("ellipse", f"Seed mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8C690", opacity=40, stroke=NONE)
d.shape("ellipse", "Anteater shadow", x=280, y=734, width=470, height=26,
        fill="#33260F", opacity=45, stroke=NONE)

# --- limbs --------------------------------------------------------------------
def limb(label, pts, widths, fill, **kw):
    n = len(pts)
    L, Rr = [], []
    for i in range(n):
        ax, ay = pts[max(i - 1, 0)]
        bx, by = pts[min(i + 1, n - 1)]
        dx, dy = bx - ax, by - ay
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = widths[i] / 2
        L.append((pts[i][0] + nx * w, pts[i][1] + ny * w))
        Rr.append((pts[i][0] - nx * w, pts[i][1] - ny * w))
    dd = "M%.1f,%.1f " % L[0]
    for i in range(1, n):
        mx, my = (L[i-1][0] + L[i][0]) / 2, (L[i-1][1] + L[i][1]) / 2
        dd += "Q%.1f,%.1f %.1f,%.1f " % (L[i-1][0], L[i-1][1], mx, my) if i > 1 else "L%.1f,%.1f " % (mx, my)
    dd += "L%.1f,%.1f L%.1f,%.1f " % (L[-1] + Rr[-1])
    for i in range(n - 2, -1, -1):
        dd += "L%.1f,%.1f " % Rr[i]
    d.path(dd + "Z", label, fill=fill, **kw)

def forefist(label, cx, fill, dark=True):
    """Knuckle-walking forefoot: rounded fist, claws folded back along the ground."""
    d.path(f"M{cx+26},742 C{cx+28},726 {cx+16},716 {cx-2},716 "
           f"C{cx-20},716 {cx-32},726 {cx-30},742 Z",
           label, fill=fill, stroke=INK, strokeWidth=4)
    # three folded claws sweeping back under the fist (tips rest rearward)
    claw = "#181008" if dark else "#241812"
    for j, (ox, ln) in enumerate([(-4, 46), (8, 40), (18, 32)]):
        d.path(f"M{cx+ox},{722} C{cx+ox+14},{726} {cx+ox+ln-8},{732} {cx+ox+ln},{742}",
               f"{label} claw {j+1}", fill=NONE, stroke=claw, strokeWidth=6, cap="round")

def hindfoot(label, cx, fill):
    """Plantigrade hind foot, toes forward (left), small claws."""
    d.path(f"M{cx+18},{742} C{cx+20},{728} {cx+8},{720} {cx-10},{722} "
           f"C{cx-34},{724} {cx-52},{730} {cx-54},{740} C{cx-54},{744} {cx-50},{742} {cx+18},{742} Z",
           label, fill=fill, stroke=INK, strokeWidth=4)
    for j, ox in enumerate([-52, -44, -36]):
        d.path(f"M{cx+ox},{738} L{cx+ox-7},{742}", f"{label} toe {j+1}",
               fill=NONE, stroke="#1C1209", strokeWidth=4, cap="round")

# far legs first (behind the body)
limb("Leg far front", [(396, 556), (392, 620), (386, 680), (384, 726)], [64, 46, 38, 34],
     LEG_FAR, stroke=INK, strokeWidth=3)
forefist("Fist far front", 380, LEG_FAR)
limb("Leg far hind", [(596, 580), (604, 646), (600, 700), (594, 728)], [72, 50, 38, 34],
     LEG_FAR, stroke=INK, strokeWidth=3)
hindfoot("Foot far hind", 600, LEG_FAR)

# --- tail plume: behind the rump, sweeping right ------------------------------
d.path("M644,474 C700,430 776,416 830,444 C860,460 872,486 862,514 "
       "C852,544 812,572 756,584 C712,592 676,580 658,554 "
       "C646,534 640,504 644,474 Z",
       "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=6)
# brush strands inside the plume
for i, dd in enumerate([
        "M688,486 C740,462 794,454 838,472",
        "M684,516 C736,496 792,492 844,502",
        "M692,548 C742,534 792,528 832,530",
        "M700,568 C744,560 786,552 818,548"]):
    d.path(dd, f"Tail strand {i+1}", fill=NONE, stroke="#5C4A2C", strokeWidth=4,
           opacity=45, cap="round")
# ragged hair tips on the plume's far edge
for i, (x, y, dx, dy) in enumerate([(858, 492, 16, -6), (852, 516, 18, 4), (838, 540, 16, 10),
                                    (818, 560, 14, 14), (856, 470, 14, -12)]):
    d.path(f"M{x},{y} Q{x+dx/2},{y+dy/2} {x+dx},{y+dy}", f"Tail tip {i+1}",
           fill=NONE, stroke=INK, strokeWidth=4, opacity=60, cap="round")
d.path("M672,470 C724,442 786,432 830,452", "Tail rim light", fill=NONE,
       stroke="#E4D3A4", strokeWidth=5, opacity=40, cap="round")

# --- body + head + snout: one silhouette --------------------------------------
d.path("M196,594 "                                   # nose tip
       "C224,576 258,560 296,548 "                   # snout top
       "C316,542 328,536 340,530 "                   # crown
       "C356,518 372,494 388,468 "                   # neck front to shoulder
       "C398,450 406,440 420,434 "                   # shoulder hump
       "C448,424 486,424 524,430 "                   # back
       "C572,436 632,448 668,466 "                   # back to rump
       "C692,478 702,502 696,526 "                   # rump rear (tail laps over)
       "C690,552 672,570 646,582 "                   # rear down to belly
       "C606,598 540,606 474,606 "                   # belly
       "C428,606 388,598 362,584 "                   # belly to chest
       "C342,574 330,568 318,564 "                   # chest to throat
       "C292,568 262,578 236,586 "                   # snout underside
       "C222,590 208,592 196,594 Z",
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)

# snout shade + top light
d.path("M210,596 C246,584 280,572 312,562 C330,556 344,550 356,544",
       "Snout light", fill=NONE, stroke="#E8D8B0", strokeWidth=4, opacity=40, cap="round")
d.path("M230,592 C264,582 296,572 322,566", "Snout shade", fill=NONE,
       stroke="#54452C", strokeWidth=5, opacity=35, cap="round")
# nose + tiny nostril
d.path("M196,594 C192,590 192,584 197,580 C204,576 212,578 215,584 C216,590 210,594 196,594 Z",
       "Nose", fill=lin(190, 578, 205, 596, (0, "#3A2A1C"), (1, "#0E0804")), stroke=NONE)

# dark diagonal shoulder band with cream borders — the anteater's mark.
# Broad sash: front edge from chest to mid-back, rear edge parallel ~90 behind.
d.path("M356,584 C405,542 460,495 505,452 "
       "C530,455 560,461 592,469 "
       "C552,510 512,558 470,600 "
       "C430,604 390,596 356,584 Z",
       "Shoulder band", fill=BAND_GRAD, stroke=NONE)
d.path("M358,580 C408,540 462,494 503,455", "Band border front", fill=NONE,
       stroke=CREAM, strokeWidth=6, opacity=85, cap="round")
d.path("M588,471 C548,512 510,558 476,596", "Band border rear", fill=NONE,
       stroke=CREAM, strokeWidth=6, opacity=85, cap="round")
# dark chest wash merging band into throat
d.path("M342,560 C356,556 368,560 374,570 C368,582 354,588 342,582 C336,574 336,566 342,560 Z",
       "Chest dark", fill="#1E130A", opacity=45, stroke=NONE)

# coat texture: ticks + belly fur
for i, dd in enumerate(["M430,598 L426,614", "M480,602 L478,616", "M532,600 L531,614",
                        "M584,594 L584,608", "M624,584 L627,598",
                        "M436,468 C458,458 480,452 502,448",
                        "M556,446 C580,448 604,454 626,462",
                        "M650,486 C664,496 674,510 680,526"]):
    d.path(dd, f"Coat fur {i+1}", fill=NONE, stroke="#6E5A38", strokeWidth=3,
           opacity=40, cap="round")
d.path("M424,430 C470,420 540,424 600,436 C630,442 654,452 670,464", "Back rim light",
       fill=NONE, stroke="#EAD9AC", strokeWidth=5, opacity=38, cap="round")

# --- near legs -----------------------------------------------------------------
limb("Leg near front", [(452, 566), (452, 632), (442, 692), (436, 728)],
     [74, 52, 42, 36], LEG_GRAD, stroke=INK, strokeWidth=4)
limb("Leg near hind", [(648, 574), (660, 640), (656, 700), (648, 730)],
     [84, 58, 44, 36], LEG_GRAD, stroke=INK, strokeWidth=4)
# pale forefeet with dark folded claws
forefist("Fist near front", 430, lin(400, 712, 440, 745, (0, "#EAD9B4"), (1, "#B49E72")))
hindfoot("Foot near hind", 656, LEG_GRAD)
# cream sock line down the front of the near foreleg (band continues)
d.path("M446,586 C448,632 442,678 434,716", "Foreleg cream line", fill=NONE,
       stroke=CREAM, strokeWidth=5, opacity=55, cap="round")

# --- face ----------------------------------------------------------------------
# small rounded ear on the crown
d.shape("ellipse", "Ear", x=336, y=516, width=26, height=22, fill="#99815C",
        stroke=INK, strokeWidth=4)
d.shape("ellipse", "Ear inner", x=343, y=523, width=10, height=8,
        fill="#241608", opacity=40, stroke=NONE)
# small hard eye
d.shape("ellipse", "Eye", x=322, y=548, width=13, height=11, fill="#1E1208",
        stroke=INK, strokeWidth=2)
d.shape("ellipse", "Eye glint", x=325, y=550, width=4, height=4, fill="#F4EAD2",
        opacity=90, stroke=NONE)
# mouth hint at snout tip
d.path("M200,592 C214,590 226,588 236,586", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4, opacity=60, cap="round")

# plate rim on top so everything inside closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840, fill=NONE,
        stroke="#2A1E0C", strokeWidth=6)

# --- name + second line --------------------------------------------------------
d.text("GIANT ANTEATER", "Name", x=500, y=932, size=58, font="Virelai Sans",
       color="#E9DDB6", justify="center")
LINE2, SZ2, TRK = "MYRMECOPHAGA TRIDACTYLA", 22, 200
r = d.text(LINE2, "Second line", x=500, y=968, size=SZ2, font="Virelai Sans",
           color="#B9A270", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r["id"], tracking=TRK)
def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
b2 = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("second line bounds", {k: round(v) for k, v in b2.items()})
assert b2["width"] <= 760 and b2["x"] >= 100 and b2["y"] + b2["height"] <= 990, b2

d.finish("giant-anteater-V1R00")
