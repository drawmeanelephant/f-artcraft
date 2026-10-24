#!/usr/bin/env python3
"""Giraffe — field-guide plate V1R00. Bust portrait: the long neck rises out of
the grass to a profile head watching the horizon, ossicones and dark tufts,
lid-lashed eye, patchwork coat. Acacia plate under a dark umber backdrop —
big-sky apricot, a flat-top tree on the horizon, two oxpeckers crossing the
sky. Floor closes on the disc's own arc. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Giraffe — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#33200C"
PATCH = "#C88434"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def on_disc(x, y, pad=0):
    return math.hypot(x - CX, y - CY) <= R - pad

BG_GRAD = lin(0, 0, 0, 1000, (0, "#241608"), (1, "#0B0602"))
PLATE_GRAD = rad((0, "#F8E0AC"), (0.55, "#E8BC72"), (1, "#C08C44"))
COAT_GRAD = lin(0, 240, 0, 780, (0, "#F4DCA8"), (0.55, "#ECC888"), (1, "#D8A858"))
SHADE_GRAD = lin(0, 300, 0, 780, (0, "#C89448"), (1, "#9A6424"))
GRASS_GRAD = lin(0, 740, 0, 880, (0, "#A8803C"), (1, "#58401A"))

# --- backdrop + big-sky plate -----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880, fill="#E8BC72", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A541E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFF4D8", strokeWidth=3, opacity=45)
# high haze + two soft clouds
d.shape("ellipse", "Haze", x=200, y=470, width=600, height=70, fill="#FFF0CC", opacity=14, stroke=NONE)
d.shape("ellipse", "Cloud 1", x=180, y=240, width=250, height=42, fill="#FFF6E0", opacity=26, stroke=NONE)
d.shape("ellipse", "Cloud 2", x=590, y=180, width=210, height=36, fill="#FFF6E0", opacity=22, stroke=NONE)
# oxpeckers crossing the big sky
for i, (x, y, s) in enumerate([(250, 300, 1.0), (300, 276, 0.8)]):
    d.path(f"M{x-s*10},{y} Q{x-s*4},{y-s*7} {x},{y} Q{x+s*4},{y-s*7} {x+s*10},{y}",
           f"Bird {i+1}", fill=NONE, stroke="#5E4014", strokeWidth=3, opacity=55, cap="round")

# savanna floor: top edge sways, bottom closes on the disc arc
ly = 750
ldx = math.sqrt(R * R - (ly - CY) ** 2)
d.path(f"M{CX-ldx:.1f},{ly} C310,734 430,744 530,740 C630,736 700,742 {CX+ldx:.1f},{ly} "
       f"A{R},{R} 0 0 1 {CX-ldx:.1f},{ly} Z", "Savanna floor", fill=GRASS_GRAD, stroke=NONE)
d.path(f"M{CX-ldx+8:.1f},{ly-2} C310,732 430,740 530,736 C630,732 700,738 {CX+ldx-8:.1f},{ly-2}",
       "Horizon light", fill=NONE, stroke="#F8E0AC", strokeWidth=4, opacity=40, cap="round")
# the acacia, right side, canopy over the horizon
ax, ay = 748, 636
d.path(f"M{ax},{ly+6} C{ax-6},{ly-40} {ax-14},{ly-76} {ax-26},{ay+22} "
       f"M{ax},{ly+6} C{ax+8},{ly-40} {ax+18},{ly-72} {ax+30},{ay+24} "
       f"M{ax-8},{ly-46} C{ax-20},{ly-58} {ax-30},{ay+40} {ax-38},{ay+28}",
       "Acacia trunk", fill=NONE, stroke="#3A2608", strokeWidth=7, opacity=75, cap="round")
d.path(f"M{ax-96},{ay+18} C{ax-76},{ay-10} {ax-34},{ay-20} {ax-4},{ay-18} "
       f"C{ax+34},{ay-20} {ax+78},{ay-8} {ax+98},{ay+16} "
       f"C{ax+62},{ay+26} {ax-56},{ay+28} {ax-96},{ay+18} Z",
       "Acacia canopy", fill="#4A320C", opacity=70, stroke=NONE)
for px, py in [(ax-96, ay+18), (ax+98, ay+16)]:
    assert on_disc(px, py, 15), (px, py)
d.path(f"M{ax-88},{ay+22} C{ax-40},{ay+30} {ax+40},{ay+30} {ax+90},{ay+20}",
       "Canopy underlight", fill=NONE, stroke="#8A6428", strokeWidth=3, opacity=50, cap="round")
# grass tufts
for i, (x, h) in enumerate([(226,26),(280,20),(340,30),(420,24),(620,26),(680,20),(830,22)]):
    for j, dx in enumerate([-6, 0, 6]):
        bend = dx * 1.6
        d.path(f"M{x+dx},{ly+8} Q{x+dx+bend},{ly+8-h*0.6} {x+dx+bend*1.4},{ly+8-h}",
               f"Tuft {i+1}.{j+1}", fill=NONE, stroke="#4A3410", strokeWidth=3, opacity=55, cap="round")
# dust motes
for i, (x, y, w) in enumerate([(190,300,4),(820,300,5),(165,470,5),(845,450,4),(240,640,4),
                               (790,660,5),(150,390,4),(860,370,4),(410,110,5),(590,100,4),
                               (330,130,4),(700,140,5),(300,810,4),(660,820,5),(500,850,4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w, fill="#8A6224", opacity=32, stroke=NONE)

# --- giraffe: neck rising to a profile head -----------------------------------------
# silhouette: chest base → neck front → throat → jaw → muzzle → forehead → poll → neck back
BODY = ("M430,776 C442,660 458,540 478,452 C486,426 492,410 496,400 "
        "C466,394 434,388 406,380 C378,372 354,362 340,350 "
        "C328,340 328,326 342,318 C368,302 406,294 444,288 "
        "C476,280 508,272 530,272 C552,272 564,286 568,306 "
        "C572,330 566,352 556,368 C568,408 582,458 598,514 "
        "C618,580 640,662 656,730 C662,752 666,766 668,776 Z")
d.path(BODY, "Giraffe", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# shadowed far side of the neck
d.path("M540,380 C560,430 578,490 596,556 C614,622 634,690 650,742 "
       "L610,748 C596,690 580,616 564,548 C550,486 540,430 536,392 Z",
       "Neck shade", fill=SHADE_GRAD, opacity=55, stroke=NONE)

# the short dark mane down the back of the neck
mane = [c for c in [
    (560, 356), (570, 400), (580, 446), (590, 492), (600, 540), (610, 588), (620, 636), (632, 684)]]
for i, (x, y) in enumerate(mane):
    d.path(f"M{x},{y} L{x+16},{y-16} L{x+18},{y+2} Z", f"Mane tuft {i+1}",
           fill="#6E4416", opacity=85, stroke=NONE)

# --- ossicones + ear, rising off the poll ----------------------------------------------
d.path("M508,262 C506,240 506,220 510,204 L520,204 C522,222 522,242 522,262 Z",
       "Ossicone far", fill=SHADE_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Ossicone far knob", x=504, y=188, width=22, height=20,
        fill="#4A2E10", stroke=INK, strokeWidth=2)
d.path("M466,272 C464,246 464,222 468,202 L480,202 C482,224 482,248 482,272 Z",
       "Ossicone near", fill=COAT_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Ossicone knob", x=460, y=186, width=26, height=22,
        fill="#3A240C", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Knob light", x=465, y=190, width=8, height=6, fill="#8A5E28", opacity=60, stroke=NONE)
# ear sweeping back from under the ossicones
d.path("M530,288 C556,274 590,272 616,286 C600,304 570,314 544,310 C534,306 530,298 530,288 Z",
       "Ear", fill=COAT_GRAD, stroke=INK, strokeWidth=4)
d.path("M544,292 C562,282 584,282 600,290", "Ear inner",
       fill=NONE, stroke="#8A5E28", strokeWidth=4, opacity=50, cap="round")

# --- head shading -----------------------------------------------------------------------
# pale blaze down the long face
d.path("M350,326 C380,306 420,294 458,288 C452,306 438,326 416,340 "
       "C392,352 366,348 354,336 C348,331 347,328 350,326 Z",
       "Face blaze", fill="#FBEDC8", opacity=70, stroke=NONE)
# dark muzzle: the soft lips at the tip
d.path("M336,330 C336,340 344,350 358,354 C374,358 392,356 404,348 "
       "C392,360 370,364 352,358 C340,352 332,342 336,330 Z",
       "Muzzle dark", fill="#6E4416", opacity=75, stroke=NONE)
# nostril: the long slit near the tip
d.path("M348,332 C356,322 370,320 380,324 C372,334 356,338 348,332 Z",
       "Nostril", fill="#2E1A08", stroke=NONE)

# --- the patient eye ----------------------------------------------------------------------
d.path("M446,320 C458,304 482,300 498,312 C488,330 460,334 446,320 Z",
       "Eye", fill=rad((0, "#4A3018"), (1, "#1A0E04")), stroke=INK, strokeWidth=4)
d.shape("ellipse", "Eye glint", x=464, y=312, width=8, height=8, fill="#FFF4DC", opacity=90, stroke=NONE)
d.path("M442,318 C456,302 484,298 502,310", "Upper lid",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# lashes: three short flicks off the lid
for i, (x, y) in enumerate([(450, 310), (462, 305), (474, 302)]):
    d.path(f"M{x},{y} L{x-6},{y-8}", f"Lash {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3, cap="round")
d.path("M446,334 C460,340 482,338 496,328", "Lower lid light",
       fill=NONE, stroke="#FBEDC8", strokeWidth=4, opacity=50, cap="round")
d.path("M438,302 C458,290 484,288 504,296", "Brow",
       fill=NONE, stroke="#8A5E28", strokeWidth=7, opacity=35, cap="round")

# --- coat patches ---------------------------------------------------------------------------
# irregular polygonal patches marching down the neck
def patch(cx, cy, w, h, rot, label, op=95):
    t = math.radians(rot); c, s = math.cos(t), math.sin(t)
    pts = []
    for dx, dy in [(-w*0.5, -h*0.42), (-w*0.08, -h*0.55), (w*0.42, -h*0.38),
                   (w*0.55, h*0.05), (w*0.30, h*0.5), (-w*0.2, h*0.55), (-w*0.55, h*0.18)]:
        pts.append((cx + dx*c - dy*s, cy + dx*s + dy*c))
    dd = "M%.1f,%.1f " % pts[0] + " ".join("L%.1f,%.1f" % p for p in pts[1:]) + " Z"
    d.path(dd, label, fill=PATCH, opacity=op, stroke=NONE)
    d.path(dd, f"{label} rim", fill=NONE, stroke="#8A5A20", strokeWidth=2, opacity=40)

for i, (x, y, w, h, r_) in enumerate([
        (480, 430, 56, 44, -18), (540, 470, 48, 40, 12), (470, 500, 50, 42, 8),
        (530, 540, 58, 46, -10), (478, 566, 44, 38, 20), (552, 596, 50, 44, -6),
        (492, 620, 54, 44, 14), (566, 656, 46, 40, -16), (510, 676, 58, 46, 6),
        (584, 706, 44, 38, 10), (534, 726, 52, 42, -8),
        (512, 344, 30, 24, -14), (546, 302, 24, 18, 10), (448, 368, 26, 20, 22)]):
    patch(x, y, w, h, r_, f"Patch {i+1}")
# sheen along the front of the neck
d.path("M470,420 C452,480 440,560 436,640 C434,690 436,730 442,762",
       "Neck sheen", fill=NONE, stroke="#FFF0CC", strokeWidth=10, opacity=25, cap="round")

# --- caption --------------------------------------------------------------------------------
d.text("GIRAFFE", "Name", x=500, y=942, size=60, font="Virelai Sans",
       color="#F8E8C0", justify="center")
o = d.text("GIRAFFA CAMELOPARDALIS", "Binomial", x=500, y=976, size=21, font="Virelai Sans",
           color="#C9A468", justify="center")
if o and "id" in o:
    d.cmd("text.setStyle", "Binomial tracking", ids=[o["id"]], tracking=350)

d.finish("giraffe-V1R00")
