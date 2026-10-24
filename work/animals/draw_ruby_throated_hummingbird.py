#!/usr/bin/env python3
"""Ruby-throated hummingbird — field plate V1R00. Cock hovering at a trumpet
bloom in a flower-bed: emerald back, ruby gorget catching light, bill deep in
the corolla, wings read as a blur fan with one crisp wing inside it.
1000x1000. House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420; wingtips and flower stay inside."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Ruby-throated Hummingbird — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#1C2415"

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def smooth(pts, closed=True, k=1.0):
    n = len(pts)
    s = "M%.1f,%.1f" % pts[0]
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        s += " C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (c1 + c2 + p2)
    return s + (" Z" if closed else "")

BG_GRAD    = lin(0, 0, 0, 1000, (0, "#101A12"), (1, "#050704"))
PLATE_GRAD = rad((0, "#A8BC90"), (0.55, "#6E8A5E"), (1, "#3A4E30"))
BACK_GRAD  = rad((0, "#46B470"), (0.55, "#1E7A48"), (1, "#0C4228"))
BELLY_GRAD = lin(540, 480, 560, 560, (0, "#F4F2E2"), (1, "#C8CEB2"))
GORGET     = rad((0, "#F04454"), (0.5, "#C01E36"), (1, "#6E0E1E"))
WING_GRAD  = lin(560, 470, 700, 330, (0, "#3E9E62"), (1, "#0E3E28"))
STEM_GRAD  = lin(330, 820, 420, 460, (0, "#3E6634"), (1, "#5E8A46"))
BLOOM_GRAD = lin(370, 470, 460, 400, (0, "#B83428"), (0.6, "#E85A40"), (1, "#F08A5E"))
FLOOR_GRAD = lin(0, 786, 0, 880, (0, "#4E663C"), (1, "#24361C"))

# --- backdrop + garden plate ------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=62, y=22, width=876, height=876, fill="#6E8A52", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#33402A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4EDD0", strokeWidth=3, opacity=40)
d.shape("ellipse", "Patina 1", x=210, y=200, width=230, height=120, fill="#C4D4A4", opacity=15, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=600, width=220, height=110, fill="#C4D4A4", opacity=13, stroke=NONE)
for i, (x, y, w) in enumerate([(195,360,7),(800,310,8),(160,500,8),(845,480,7),(255,690,7),(750,720,8),
                               (145,610,6),(860,590,6),(390,105,7),(625,115,6),(330,822,6),(700,812,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#41542F", opacity=38, stroke=NONE)
# light pooling where the hover happens
d.shape("ellipse", "Hover light", x=430, y=380, width=300, height=210,
        fill="#EDF2D2", opacity=12, stroke=NONE)

# --- flower-bed floor, closing on the disc's own arc ---------------------------------
gy = 792
gdx = math.sqrt(R * R - (gy - CY) ** 2)
d.path(f"M{CX-gdx:.1f},{gy} C330,786 420,798 500,794 C590,790 670,798 {CX+gdx:.1f},{gy} "
       f"A{R},{R} 0 0 1 {CX-gdx:.1f},{gy} Z",
       "Flower bed", fill=FLOOR_GRAD, opacity=92, stroke=NONE)
# bed leaves
for i, (x0, y0, x1, y1) in enumerate([(280,822,316,806),(690,828,720,812),(600,846,628,834),(360,850,384,840)]):
    d.path(f"M{x0},{y0} Q{(x0+x1)//2},{y0-24} {x1},{y1}", f"Bed leaf {i+1}",
           fill=NONE, stroke="#7EA060", strokeWidth=3.5, opacity=55, cap="round")
# a small fallen petal
d.path("M640,824 q14,-6 22,4 q-12,8 -22,-4 Z", "Fallen petal", fill="#C85640", opacity=70, stroke=NONE)

# hover shadow on the bed
d.shape("ellipse", "Hover shadow", x=470, y=790, width=190, height=16,
        fill="#16220E", opacity=42, stroke=NONE)

# --- the trumpet stem, rising left of the bird ---------------------------------------
d.path("M322,824 C330,720 360,600 396,492", "Stem", fill=NONE,
       stroke=STEM_GRAD, strokeWidth=6, cap="round")
# stem leaves
for i, (x, y, dx, dy) in enumerate([(344,690,-34,-8),(366,582,30,-4),(352,748,34,6)]):
    d.path(f"M{x},{y} q{dx},{dy} {dx*1.7:.0f},{dy+18}", f"Stem leaf {i+1}",
           fill=NONE, stroke="#4E7A3E", strokeWidth=4, opacity=80, cap="round")
# second, half-open bloom on a side spur below the main flower
d.path("M366,610 C372,600 378,594 384,590", "Bloom spur", fill=NONE,
       stroke=STEM_GRAD, strokeWidth=4.5, cap="round")
d.path("M366,584 C382,570 398,560 414,554 L420,566 C406,572 392,580 380,592 Z",
       "Calyx 2", fill="#4E7A3E", stroke=INK, strokeWidth=2.5)
d.path("M380,590 C396,572 412,562 428,558 L434,570 C420,576 406,586 396,598 Z",
       "Corolla 2", fill=BLOOM_GRAD, stroke=INK, strokeWidth=3)
for i, (cx, cy, w, h) in enumerate([(426,556,24,14),(438,564,18,12)]):
    d.shape("ellipse", f"Lip lobe 2.{i+1}", x=cx - w/2, y=cy - h/2, width=w, height=h,
            fill="#F08A5E", opacity=95, stroke="#B83428", strokeWidth=2)

# open trumpet: calyx + corolla tube flaring to the lip the bill enters
d.path("M396,492 C404,470 418,450 438,436 L452,448 C436,460 424,476 420,494 Z",
       "Calyx", fill="#4E7A3E", stroke=INK, strokeWidth=2.5)
d.path("M412,494 C424,462 442,438 468,424 L478,438 C458,452 444,472 438,498 Z",
       "Corolla", fill=BLOOM_GRAD, stroke=INK, strokeWidth=3)
# flared lobes of the lip around the throat opening
for i, (cx, cy, w, h) in enumerate([(468,420,34,20),(486,430,26,18),(452,412,24,16)]):
    d.shape("ellipse", f"Lip lobe {i+1}", x=cx - w/2, y=cy - h/2, width=w, height=h,
            fill="#F08A5E", opacity=95, stroke="#B83428", strokeWidth=2)
# throat depth the bill vanishes into
d.shape("ellipse", "Throat", x=458, y=426, width=26, height=16,
        fill="#7E1E14", stroke=NONE)

# --- the bird, hovering with bill in the bloom ----------------------------------------
# blurred wing fan behind the body (translucent sweep)
for i, (ex, ey, w) in enumerate([(690,330,46),(716,392,42),(672,296,38)]):
    d.path(f"M586,478 C{ex-70},{ey+40} {ex-30},{ey+10} {ex},{ey} "
           f"C{ex-40},{ey+34} {610+20*i},{480} 586,478 Z",
           f"Wing blur {i+1}", fill="#2E7A4E", opacity=16 + i*4, stroke=NONE)
# crisp wing inside the blur: pointed primaries swept up-back
d.path("M580,486 C616,436 662,392 706,368 C700,404 676,448 636,486 "
       "C620,500 596,498 580,486 Z",
       "Wing", fill=WING_GRAD, opacity=88, stroke=INK, strokeWidth=4)
for j, (x1, y1) in enumerate([(700,378),(688,398),(672,420)]):
    d.path(f"M604,478 C640,{y1+40} 670,{y1+18} {x1},{y1}",
           f"Primary {j+1}", fill=NONE, stroke="#0C3824",
           strokeWidth=3, opacity=60, cap="round")

# tail: two forked feathers angled down-back
d.path("M636,522 C662,540 684,566 696,596 L680,590 C666,566 648,544 630,530 Z",
       "Tail R", fill="#12452E", stroke=INK, strokeWidth=3)
d.path("M628,534 C650,556 664,586 668,616 L654,608 C646,582 632,558 618,542 Z",
       "Tail L", fill="#0E3A26", stroke=INK, strokeWidth=3)

# body teardrop: breast low-left, back arcing to the tail root
d.path(smooth([(522,472),(556,452),(600,462),(632,492),(644,518),
               (630,542),(596,552),(556,544),(528,522),(514,494)]),
       "Body", fill=BACK_GRAD, stroke=INK, strokeWidth=4.5)
# white breast wedge below the back line
d.path(smooth([(516,494),(532,524),(556,544),(590,552),(614,544),
               (588,530),(556,516),(530,500)]),
       "Breast", fill=BELLY_GRAD, stroke=NONE, opacity=95)
# the gorget: iridescent ruby shield under the bill
d.path(smooth([(502,478),(522,486),(532,504),(524,520),(504,518),
               (492,500),(490,486)]),
       "Gorget", fill=GORGET, stroke="#4E0A14", strokeWidth=2)
for i, (x, y, w) in enumerate([(502,492,5),(512,498,4),(506,506,4)]):
    d.shape("ellipse", f"Gorget spark {i+1}", x=x, y=y, width=w, height=w,
            fill="#FF9AA2", opacity=70, stroke=NONE)

# head: green crown continuing the back line, white post-ocular spot
d.path(smooth([(494,448),(516,436),(538,444),(544,462),(536,478),
               (514,482),(496,472),(490,458)]),
       "Head", fill=BACK_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Crown light", x=498, y=442, width=26, height=16,
        fill="#7ADCA0", opacity=30, stroke=NONE)
d.shape("ellipse", "Eye", x=506, y=454, width=9, height=10, fill="#0A140C", stroke=NONE)
d.shape("ellipse", "Eye glint", x=508, y=456, width=3, height=3, fill="#FFFFFF", opacity=85, stroke=NONE)
d.shape("ellipse", "Post-ocular spot", x=524, y=462, width=7, height=6,
        fill="#F2F4E4", opacity=85, stroke=NONE)

# bill: long needle, slightly decurved, into the flower throat
d.path("M498,460 C478,448 460,438 446,432 L448,428 C464,434 482,444 500,454 Z",
       "Bill", fill="#16120C", stroke=NONE)

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#2C3A20", strokeWidth=6)

# --- name ------------------------------------------------------------------------------
d.text("RUBY-THROATED HUMMINGBIRD", "Name", x=500, y=962, size=46, font="Virelai Sans",
       color="#E8EDD0", justify="center")

d.finish("ruby-throated-hummingbird-V1R00")
