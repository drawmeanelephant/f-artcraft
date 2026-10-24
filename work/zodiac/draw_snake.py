#!/usr/bin/env python3
"""Snake — Celestial Seal V1R00. Fire element. A gold-green serpent coiled
in three turns, head raised frontally with vertical pupils and a forked
tongue; the sixth branch. 1000x1000."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (NONE, INK, GOLD, GOLD_HI, lin, rad, gold_lin,
                          smooth, cloud, coin, blossom, ribbon, bez)
from orient.zodiac import ZodiacPlate

p = ZodiacPlate("snake-V1R00", "SNAKE", "蛇", "巳", "fire", "2025 · 2037", "Snake")
d = p.d

SC_HI = "#E0C878"
SC = "#B09444"
SC_LO = "#786020"
SC_DEEP = "#43340C"
BELLY = "#F6E4A8"

cloud(d, 252, 262, 0.85, "Cloud upper L", fill=GOLD, opacity=10)
cloud(d, 748, 262, 0.85, "Cloud upper R", fill=GOLD, opacity=10)
d.shape("ellipse", "Head halo", x=310, y=210, width=380, height=380,
        fill=rad((0, "#F2A24E", 18), (0.65, "#F2A24E", 6), (1, "#F2A24E", 0)), stroke=NONE)

def coil_arc(cx, cy, r, a0, a1, width, label, color_hi=SC_HI, color=SC, color_lo=SC_LO):
    steps = 44
    pts = []
    for i in range(steps + 1):
        a = math.radians(a0 + (a1 - a0) * i / steps)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.path(smooth(pts), f"{label} ink", fill=NONE, stroke=INK,
           strokeWidth=width + 9, cap="round")
    d.path(smooth(pts), label, fill=NONE,
           stroke=lin(0, cy - r, 0, cy + r, (0, color_hi), (0.5, color), (1, color_lo)),
           strokeWidth=width, cap="round")
    inner = []
    for i in range(2, steps - 1):
        a = math.radians(a0 + (a1 - a0) * i / steps)
        rr = r - width * 0.27
        inner.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.path(smooth(inner), f"{label} sheen", fill=NONE, stroke=BELLY,
           strokeWidth=max(3, width * 0.16), opacity=38, cap="round")
    for i in range(4, steps - 3, 4):
        a = math.radians(a0 + (a1 - a0) * i / steps)
        nx, ny = math.cos(a), math.sin(a)
        tx, ty = -ny, nx
        px, py = cx + r * nx, cy + r * ny
        for off in (-0.18, 0.08):
            qx, qy = px + nx * width * off, py + ny * width * off
            d.path(f"M{qx - tx*width*0.15:.1f},{qy - ty*width*0.15:.1f} "
                   f"Q{qx + nx*4:.1f},{qy + ny*4:.1f} "
                   f"{qx + tx*width*0.15:.1f},{qy + ty*width*0.15:.1f}",
                   f"{label} scale {i}-{off}", fill=NONE, stroke=SC_DEEP,
                   strokeWidth=2, opacity=42, cap="round")

coil_arc(500, 664, 178, 196, 8, 66, "Coil outer")
coil_arc(500, 664, 122, 8, 196, 58, "Coil middle")
coil_arc(500, 664, 70, 200, 20, 50, "Coil inner")
d.path("M500,628 C520,638 524,664 508,678 C492,692 466,684 458,664 "
       "C450,644 466,624 486,624 C470,634 468,652 480,662 C492,672 508,666 512,652",
       "Coil tail", fill=NONE, stroke=INK, strokeWidth=46, cap="round")
d.path("M500,628 C520,638 524,664 508,678 C492,692 466,684 458,664 "
       "C450,644 466,624 486,624 C470,634 468,652 480,662 C492,672 508,666 512,652",
       "Coil tail colour", fill=NONE, stroke=SC, strokeWidth=37, cap="round")

# neck rising from the coil
NECK = ("M448,628 C450,540 468,478 492,452 L508,452 "
        "C532,478 550,540 552,628 Z")
d.path(NECK, "Neck", fill=lin(0, 448, 0, 566, (0, SC_HI), (0.5, SC), (1, SC_LO)),
       stroke=INK, strokeWidth=7)
for i in range(7):
    y = 476 + i * 20
    w = 54 - i * 3
    d.path(f"M{500-w/2:.1f},{y:.1f} Q500,{y+9:.1f} {500+w/2:.1f},{y:.1f}",
           f"Neck band {i+1}", fill=NONE, stroke=SC_DEEP, strokeWidth=2.2, opacity=38, cap="round")

# lower neck, drawn over the coil so head and body connect
d.path("M448,620 C452,560 470,510 492,486 L508,486 C530,510 548,560 552,620 Z",
       "Neck lower", fill=lin(0, 480, 0, 630, (0, SC), (0.6, SC_LO), (1, SC_DEEP)),
       stroke=INK, strokeWidth=7)
for i in range(3):
    y = 520 + i * 24
    w = 70 - i * 10
    d.path(f"M{500-w/2:.1f},{y:.1f} Q500,{y+10:.1f} {500+w/2:.1f},{y:.1f}",
           f"Lower neck band {i+1}", fill=NONE, stroke=SC_DEEP, strokeWidth=2.2,
           opacity=40, cap="round")

# --- frontal head --------------------------------------------------------------------
HEAD = ("M500,330 C560,330 606,348 620,384 C634,420 616,454 582,470 "
        "C556,482 528,486 500,486 C472,486 444,482 418,470 "
        "C384,454 366,420 380,384 C394,348 440,330 500,330 Z")
d.path(HEAD, "Head", fill=lin(0, 330, 0, 486, (0, SC_HI), (0.45, SC), (1, SC_LO)),
       stroke=INK, strokeWidth=7)
d.path("M420,354 C452,338 548,338 580,354 C558,372 442,372 420,354 Z",
       "Head light", fill="#FFF0B8", opacity=28, stroke=NONE)
# brow ridges
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 74
    d.path(f"M{x - 44:.1f},380 C{x - 16:.1f},360 {x + 26:.1f},362 {x + 44:.1f},384",
           f"Brow ridge {nm}", fill=NONE, stroke="#5E4A14", strokeWidth=8, cap="round")
# eyes
for sign, nm in ((-1, "L"), (1, "R")):
    x = 500 + sign * 72
    d.shape("ellipse", f"Eye {nm}", x=x - 30, y=390, width=60, height=52,
            fill=rad((0, "#FFF0B0"), (1, "#D8A83E")), stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Pupil {nm}", x=x - 6, y=396, width=12, height=38,
            fill="#1A1208", stroke=NONE)
    d.shape("ellipse", f"Glint {nm}", x=x + 1, y=398, width=6, height=8,
            fill="#FFFFFF", opacity=85, stroke=NONE)
# nostrils
for sign, nm in ((-1, "L"), (1, "R")):
    d.shape("ellipse", f"Nostril {nm}", x=500 + sign*20 - 4, y=426, width=9, height=6,
            fill="#3E3210", stroke=NONE)
# mouth
d.path("M456,450 C476,462 490,462 500,456 C510,462 524,462 544,450",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=3.6, cap="round")
# tongue out to the right
d.path("M544,452 C568,456 590,468 606,486 M606,486 L626,482 M606,486 L618,504",
       "Forked tongue", fill=NONE, stroke="#D8403A", strokeWidth=5, cap="round")
# head scales
for i, (x, y, r) in enumerate([(500,370,11), (474,386,9), (526,386,9),
                                (500,398,9), (448,400,7), (552,400,7)]):
    d.path(f"M{x-r:.1f},{y:.1f} A{r},{r*0.7:.1f} 0 0 1 {x+r:.1f},{y:.1f}",
           f"Head scale {i+1}", fill=NONE, stroke="#5E4A14", strokeWidth=2, opacity=45, cap="round")
# cheek plates
for sign, nm in ((-1, "L"), (1, "R")):
    for k, (dx, dy) in enumerate([(96, 420), (104, 438), (88, 452)]):
        d.shape("ellipse", f"Cheek plate {nm}{k+1}", x=500 + sign*dx - 12, y=dy,
                width=24, height=10, fill=SC_LO, opacity=45, stroke=NONE,
                rotation=sign * 24)

# fire wisps behind the head
for i, (x, y, h) in enumerate([(676, 392, 84), (660, 340, 64), (324, 392, 84), (340, 340, 64)]):
    d.path(f"M{x:.1f},{y:.1f} C{x - 16:.1f},{y - h*0.35:.1f} {x - 4:.1f},{y - h*0.7:.1f} "
           f"{x + 8:.1f},{y - h:.1f} C{x + 24:.1f},{y - h*0.6:.1f} {x + 18:.1f},{y - h*0.3:.1f} "
           f"{x:.1f},{y:.1f} Z", f"Flame {i+1}",
           fill=lin(0, y - h, 0, y, (0, "#FFD88A"), (0.6, "#E88232"), (1, "#B03A1E")),
           opacity=70, stroke=NONE)

p.close()
