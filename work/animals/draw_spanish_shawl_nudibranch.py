#!/usr/bin/env python3
"""Spanish shawl nudibranch — field-guide plate V1R00. Side profile gliding
the reef: violet body under a shag of flame cerata, orange rhinophores up
front, confetti drifting through the water. Reef plate, carnival mood —
the floor closes on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Spanish Shawl Nudibranch — Field Plate", 1000, 1000)

INK = "#2E1A2E"                    # warm dark ink, never pure black
CX, CY, R = 500, 460, 420          # plate disc centre + radius

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

BG_GRAD = lin(0, 0, 0, 1000, (0, "#120A1E"), (1, "#060310"))
PLATE_GRAD = lin(0, 40, 0, 880, (0, "#4E4470"), (0.5, "#2A2444"), (1, "#120E22"))
BODY_GRAD = lin(0, 500, 0, 700, (0, "#8A56C0"), (0.6, "#5A2E8E"), (1, "#381C5E"))
CERAS_A = lin(0, 420, 0, 580, (0, "#FFB25E"), (1, "#E0501E"))   # flame, lit tips
CERAS_B = lin(0, 440, 0, 590, (0, "#F06C2E"), (1, "#B0301C"))   # mid row
CERAS_C = lin(0, 450, 0, 600, (0, "#C04A28"), (1, "#822818"))   # back row, in shade
REEF_GRAD = lin(0, 690, 0, 880, (0, "#3A3448"), (1, "#120E1C"))

def rim_x(y, r=R, side=-1):
    return CX + side * math.sqrt(r * r - (y - CY) ** 2)

# --- backdrop + reef plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#181030", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8A8D8", strokeWidth=3, opacity=35)

# a soft violet-lit glow upper right
d.shape("ellipse", "Water glow", x=430, y=100, width=360, height=230,
        fill=radO((0, "#9A86C8", 36), (0.5, "#7A68A8", 13), (0.72, "#7A68A8", 0),
                  (1, "#7A68A8", 0)), stroke=NONE)

# confetti drifting — tiny bright flecks in the carnival water
for i, (x, y, w, c, o) in enumerate([
        (240, 200, 7, "#F27EA0", 55), (350, 150, 6, "#F2A24E", 50), (560, 140, 7, "#F2E4C8", 45),
        (680, 210, 6, "#F27EA0", 50), (770, 300, 7, "#F2A24E", 45), (180, 330, 6, "#9CD0C8", 45),
        (830, 420, 6, "#F27EA0", 40), (220, 470, 7, "#F2E4C8", 40), (740, 480, 6, "#9CD0C8", 38),
        (300, 460, 6, "#F2A24E", 40), (660, 150, 5, "#F27EA0", 40), (160, 560, 5, "#F2A24E", 35),
        (840, 250, 5, "#F2E4C8", 40), (440, 110, 6, "#9CD0C8", 42), (380, 300, 5, "#F2E4C8", 38),
        (580, 330, 6, "#F27EA0", 42), (250, 390, 5, "#9CD0C8", 36), (720, 380, 5, "#F2A24E", 38)]):
    d.shape("ellipse", f"Confetti {i+1}", x=x, y=y, width=w, height=w,
            fill=c, opacity=o, stroke=NONE)
# a couple of slow bubbles
for i, (x, y, w) in enumerate([(210, 380, 12), (232, 320, 8), (790, 430, 10)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=w, height=w,
            fill="#FFFFFF", opacity=13, stroke="#D8CCF0", strokeWidth=2)

# --- reef floor, closing on the disc's arc ------------------------------------------
ry = 700
rl, rr = rim_x(ry, side=-1), rim_x(ry, side=1)
d.path(f"M{rl:.1f},{ry} C280,688 340,708 420,700 C480,692 560,710 640,700 "
       f"C700,692 760,706 {rr:.1f},{ry} A{R},{R} 0 0 1 {rl:.1f},{ry} Z",
       "Reef", fill=REEF_GRAD, stroke=NONE)
# contact shadow grounding the slug on the reef
d.shape("ellipse", "Contact shadow", x=280, y=682, width=420, height=24,
        fill="#0A0614", opacity=40, stroke=NONE)
# reef stones + two tiny coral tufts
for i, (x, y, w, h) in enumerate([(215, 712, 50, 22), (395, 708, 34, 17),
                                  (615, 710, 42, 19), (735, 714, 36, 15)]):
    d.shape("ellipse", f"Stone {i+1}", x=x, y=y, width=w, height=h,
            fill="#221C30", opacity=85, stroke=NONE)
for i, (x, c) in enumerate([(238, "#C24E78"), (762, "#D8643C")]):
    for j, (dx, h) in enumerate([(-9, 24), (0, 32), (9, 22)]):
        d.path(f"M{x + dx - 4},730 C{x + dx - 6},{730 - h} {x + dx},{730 - h - 6} "
               f"{x + dx + 3},{730 - h} C{x + dx + 5},{730 - h + 4} {x + dx + 4},730 {x + dx + 4},730 Z",
               f"Coral {i+1}-{j+1}", fill=c, opacity=70, stroke=NONE)

# --- the slug: plump arched body, tail lifting off the reef ------------------------------
BODY = ("M252,622 C246,588 262,566 292,558 "
        "C330,542 340,530 362,522 "
        "C460,498 580,504 660,534 "
        "C700,550 722,566 736,586 "
        "C742,594 738,602 728,604 "
        "C680,630 560,664 440,678 "
        "C360,686 280,682 256,654 "
        "C250,644 250,632 252,622 Z")
d.path(BODY, "Foot", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# pale skirt along the foot edge + flank shading
d.path("M262,646 C320,684 560,668 716,602", "Foot skirt", fill=NONE,
       stroke="#C8A8E8", strokeWidth=5, opacity=50, cap="round")
d.shape("ellipse", "Flank shade", x=380, y=612, width=260, height=60,
        fill="#2A1450", opacity=30, stroke=NONE)
d.shape("ellipse", "Dorsal sheen", x=340, y=540, width=240, height=50,
        fill="#B488DC", opacity=30, stroke=NONE)

# --- the shag: clumps of flame cerata over the dorsum ------------------------------------
def ceras(x, by, lean, L, w_, fill, label):
    tx, ty = x + lean, by - L
    d.path(f"M{x - w_},{by} C{x - w_ - 2},{by - L*0.4} {tx - w_*0.8},{ty + L*0.3} {tx},{ty} "
           f"C{tx + w_*0.8},{ty + L*0.3} {x + w_ + 2},{by - L*0.4} {x + w_},{by} Z",
           label, fill=fill, stroke="#7E2A18", strokeWidth=2)

CLUMPS = [352, 404, 456, 508, 560, 612, 656]
# back row — behind the crest line, darker and taller
for ci, cx_ in enumerate(CLUMPS):
    for j, off in enumerate([-13, 2, 15]):
        x = cx_ + off
        by = 552 - 18 * math.sin((x - 320) / 330 * math.pi)
        ceras(x, by, -10 + j * 4, 50 + 10 * ((ci + j) % 3), 8, CERAS_C, f"Ceras b{ci}-{j}")
# mid row — the main flame, four per clump
for ci, cx_ in enumerate(CLUMPS):
    for j, off in enumerate([-16, -5, 7, 17]):
        x = cx_ + off
        by = 566 - 16 * math.sin((x - 320) / 330 * math.pi)
        ceras(x, by, -12 + 16 * (x - 330) / 340, 58 + 12 * math.sin(ci * 1.7 + j),
              9, CERAS_B, f"Ceras m{ci}-{j}")
# front row — brightest tips
for ci, cx_ in enumerate(CLUMPS[:-1]):
    for j, off in enumerate([-10, 4]):
        x = cx_ + off
        by = 578 - 14 * math.sin((x - 320) / 330 * math.pi)
        ceras(x, by, -10 + 14 * (x - 330) / 340, 62 + 8 * math.sin(ci * 2.3 + j),
              10, CERAS_A, f"Ceras f{ci}-{j}")
# two cerata over the head crest
ceras(316, 566, -12, 46, 8, CERAS_A, "Ceras head L")
ceras(340, 560, -6, 52, 8, CERAS_A, "Ceras head R")

# --- rhinophores: ridged orange horns ahead of the shag -----------------------------------
for i, (x, lean) in enumerate([(292, -14), (322, -2)]):
    tx, ty = x + lean, 522
    d.path(f"M{x - 7},556 C{x - 9},{540} {tx - 7},{530} {tx},{ty} "
           f"C{tx + 8},{528} {x + 9},{540} {x + 7},556 Z",
           f"Rhinophore {i+1}", fill=CERAS_A, stroke=INK, strokeWidth=3)
    for j in range(3):
        yy = 546 - j * 8
        lx = x + lean * (556 - yy) / 34
        d.path(f"M{lx - 7:.0f},{yy} C{lx - 2:.0f},{yy - 4} {lx + 3:.0f},{yy - 4} {lx + 7:.0f},{yy}",
               f"Rhinophore {i+1} ridge {j+1}", fill=NONE, stroke="#7E2A18",
               strokeWidth=2, opacity=70, cap="round")

# --- gill plume on the rear dorsum ---------------------------------------------------------
for i, a in enumerate([-58, -29, 0, 29, 58]):
    rad_ = math.radians(a - 95)
    tx, ty = 668 + 42 * math.cos(rad_), 556 + 42 * math.sin(rad_)
    d.path(f"M668,582 Q{668 + 28 * math.cos(rad_ - 0.3):.0f},{566 + 28 * math.sin(rad_):.0f} "
           f"{tx:.0f},{ty:.0f} Q{668 + 28 * math.cos(rad_ + 0.3):.0f},{566 + 28 * math.sin(rad_):.0f} "
           f"672,580 Z", f"Gill plume {i+1}", fill="#F2A24E", opacity=60,
           stroke="#7E2A18", strokeWidth=2)

# --- face ------------------------------------------------------------------------------------
# oral veil fringe at the front lip
for i, (x, y, r_) in enumerate([(258, 600, 11), (254, 622, 10), (258, 646, 9)]):
    d.shape("ellipse", f"Veil bump {i+1}", x=x - r_, y=y - r_, width=r_*2, height=r_*2,
            fill="#6A3A9E", stroke=INK, strokeWidth=3)
# the tiny dark eye tucked at the rhinophore base
d.shape("ellipse", "Eye", x=302, y=556, width=10, height=10,
        fill="#160A20", stroke=NONE)
d.shape("ellipse", "Eye glint", x=304, y=558, width=3, height=3,
        fill="#FFF0E0", opacity=80, stroke=NONE)

# --- name --------------------------------------------------------------------------------------
d.text("SPANISH SHAWL NUDIBRANCH", "Name", x=500, y=962, size=40, font="Virelai Sans",
       color="#D8CCF0", justify="center")

d.finish("spanish-shawl-nudibranch-V1R00")
