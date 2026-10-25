#!/usr/bin/env python3
"""Cuban trogon — field plate V1R00. The tocororo (Priotelus temnurus)
perched quiet on a mossy forest branch, turned three-quarter to show
metallic blue-green upperparts, a cool grey chest, the red belly, and
the squared dark tail with white tips — trogon tail, not quetzal
streamers. Caribbean forest plate, deep-emerald mood — canopy shade,
a shaft of humid light, foliage silhouettes closing inside the disc.
1000x1000. House style: gradients + translucent shading, never flat
fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Cuban Trogon — Field Plate", 1000, 1000)

CX, CY, R = 500, 460, 420          # plate disc centre + radius
INK = "#121A14"                    # warm dark ink, never pure black

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
    return math.hypot(x - CX, y - CY) <= R - pad

def disc_x(y, side):
    return CX + side * math.sqrt(R * R - (y - CY) ** 2)

BG_GRAD   = lin(0, 0, 0, 1000, (0, "#0B140E"), (1, "#040806"))
PLATE_GRAD = rad((0, "#56604A"), (0.5, "#2E3A2E"), (1, "#101810"))
UPPER    = rad((0, "#3AA08C"), (0.55, "#1E6E70"), (1, "#12404E"))
HEAD_GR  = rad((0, "#2E6E84"), (0.6, "#1E4E66"), (1, "#122C3E"))
CHEST    = rad((0, "#D8DCD2"), (0.6, "#AEB6AC"), (1, "#7C8478"))
BELLY_GR = rad((0, "#D84040"), (0.6, "#A82630"), (1, "#6E1A22"))
BRANCH   = lin(180, 700, 840, 800, (0, "#5E4C38"), (0.5, "#4A3C2E"), (1, "#322820"))
LEAF     = lin(0, 0, 0, 40, (0, "#6E9450"), (1, "#3A5630"))

# --- backdrop + deep-forest plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(148,118,4),(856,122,5),(118,445,3),(875,498,4),
                               (178,738,4),(852,758,4),(262,148,3)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#CCD8C4", opacity=25, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#56604A", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1C241A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E0CC", strokeWidth=3, opacity=34)

# humid light shaft behind the bird
d.shape("ellipse", "Light shaft", x=320, y=300, width=380, height=330,
        fill=rad((0, "#C8D8A8", 32), (0.6, "#C8D8A8", 10), (1, "#C8D8A8", 0)),
        stroke=NONE)
# patina flecks drifting inside the disc
for i, (x, y, w) in enumerate([(305,175,4),(450,140,5),(595,168,4),(228,265,3),
                               (372,218,4),(525,192,3),(688,148,4),(252,415,3),
                               (748,428,4),(205,555,3)]):
    assert on_disc(x, y, 15), (x, y)
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#DCE4CC", opacity=40, stroke=NONE)

# --- canopy silhouettes: dark foliage masses along the upper disc --------------------
for i, (bx, by, bw, bh) in enumerate([(170, 150, 200, 90), (610, 130, 240, 100),
                                     (330, 105, 160, 70)]):
    assert on_disc(bx + bw/2, by + bh/2, 30), (bx, by)
    d.path(f"M{bx},{by+bh} C{bx+10},{by+bh*0.3} {bx+bw*0.25},{by} {bx+bw*0.45},{by+bh*0.15} "
           f"C{bx+bw*0.65},{by+bh*0.3} {bx+bw*0.8},{by} {bx+bw},{by+bh*0.4} "
           f"C{bx+bw*0.95},{by+bh*0.8} {bx+bw*0.5},{by+bh} {bx},{by+bh} Z",
           f"Canopy {i+1}", fill="#16220F", opacity=88, stroke=NONE)
# a few leaf silhouettes hanging from the canopy edge
for i, (lx, ly, ang) in enumerate([(290, 240, 15), (330, 255, -10), (680, 230, -20),
                                   (640, 250, 12), (730, 215, 8)]):
    t = math.radians(ang); c, s = math.cos(t), math.sin(t)
    pts = [(0, -16), (9, -4), (6, 12), (0, 18), (-6, 12), (-9, -4)]
    d.path("M" + " L".join(f"{lx+px*c-py*s:.0f},{ly+px*s+py*c:.0f}" for px, py in pts) + " Z",
           f"Hang leaf {i+1}", fill="#1E2C14", opacity=85, stroke=NONE)

# --- the branch: a mossy diagonal limb, ends inside the disc -------------------------
d.path("M182,724 C300,706 420,714 540,736 C640,754 720,776 806,800 "
       "L800,822 C714,800 632,778 532,760 C416,738 300,732 186,748 Z",
       "Branch", fill=BRANCH, stroke=INK, strokeWidth=4)
# moss along the top edge
d.path("M190,720 C300,704 420,712 540,734 C620,748 690,766 780,792",
       "Moss line", fill=NONE, stroke="#7A9450", strokeWidth=5,
       opacity=60, cap="round")
# bark grain
for i, (x0, y0, x1, y1) in enumerate([(240, 730, 330, 736), (560, 754, 650, 772),
                                      (360, 726, 430, 730)]):
    d.path(f"M{x0},{y0} C{(x0+x1)/2},{y0-4} {(x0+x1)/2},{y1+4} {x1},{y1}",
           f"Bark grain {i+1}", fill=NONE, stroke="#2A2016", strokeWidth=3,
           opacity=65, cap="round")
# two leaves on a short twig off the branch, lower-left
d.path("M286,734 C270,708 258,692 240,684", "Leaf twig", fill=NONE,
       stroke="#3E3222", strokeWidth=4, cap="round")
for i, (lx, ly, ang) in enumerate([(238, 682, -30), (216, 700, -75)]):
    t = math.radians(ang); c, s = math.cos(t), math.sin(t)
    pts = [(0, -18), (12, -4), (8, 14), (0, 20), (-8, 14), (-12, -4)]
    d.path("M" + " L".join(f"{lx+px*c-py*s:.0f},{ly+px*s+py*c:.0f}" for px, py in pts) + " Z",
           f"Twig leaf {i+1}", fill=LEAF, stroke=INK, strokeWidth=3)

# contact shadow of the bird on the branch
d.shape("ellipse", "Perch shadow", x=452, y=700, width=150, height=26,
        fill="#080A06", opacity=45, stroke=NONE)

# === the tail: long squared feathers dropping behind the branch =====================
# three feathers held nearly parallel — the tocororo's flat blade, not a fan;
# dark upperside, broad white tip bands
for i, (topx, topy, botx, boty, w) in enumerate([(596, 640, 700, 836, 34),
                                               (576, 648, 664, 848, 34),
                                               (556, 650, 630, 844, 32)]):
    d.path(f"M{topx - w/2},{topy} C{topx - w/2 + 6},{(topy+boty)/2} {botx - w/2 + 4},{boty - 60} {botx - w/2},{boty} "
           f"C{botx},{boty + 10} {botx},{boty + 10} {botx + w/2},{boty} "
           f"C{botx + w/2 - 4},{boty - 60} {topx + w/2 - 6},{(topy+boty)/2} {topx + w/2},{topy} Z",
           f"Tail feather {i+1}", fill=lin(topx, topy, botx, boty,
           (0, "#1E3A4E"), (0.7, "#142630"), (1, "#0E1A22")),
           stroke=INK, strokeWidth=3.5)
    # white tip band hugging the feather's end taper
    tw = w/2 - 4
    d.path(f"M{botx - tw},{boty - 30} C{botx - 5},{boty - 34} {botx + 5},{boty - 34} {botx + tw},{boty - 30} "
           f"L{botx + tw - 2},{boty - 4} C{botx + 3},{boty + 8} {botx - 3},{boty + 8} {botx - tw + 2},{boty - 4} Z",
           f"Tail tip {i+1}", fill="#E4E6DC", stroke=NONE)

# === the trogon body: plump, three-quarter, facing left ==============================
# back and folded wing mass — metallic blue-green
d.path("M510,470 "                                   # nape
       "C566,476 604,516 616,570 "                   # back rounding down right
       "C624,616 616,656 592,682 "                   # rump over the tail
       "C566,700 532,704 506,694 "                   # under tail coverts
       "C470,682 448,652 444,612 "                   # belly front
       "C440,566 450,522 474,494 "                   # chest rising
       "C486,480 498,472 510,470 Z",
       "Body", fill=UPPER, stroke=INK, strokeWidth=5.5)
# folded wing: darker teal slab along the flank
d.path("M540,510 C586,522 610,560 612,610 C610,648 596,676 572,688 "
       "C590,660 596,622 590,580 C584,548 566,524 540,510 Z",
       "Wing", fill=lin(540, 510, 600, 690, (0, "#2E7E78"), (1, "#123A44")),
       stroke=INK, strokeWidth=3.5)
# fine covert bars on the wing — the trogon's vermiculated shoulder
for i in range(5):
    wy = 540 + i * 26
    d.path(f"M556,{wy} C574,{wy+8} 588,{wy+22} 592,{wy+40}",
           f"Covert bar {i+1}", fill=NONE, stroke="#0E2830", strokeWidth=3,
           opacity=70, cap="round")
# grey-white chest bib covering the front of the body down to mid-belly
d.path("M492,494 C460,500 440,532 438,574 C436,614 448,652 474,674 "
       "C492,688 514,692 534,686 C514,674 502,648 500,612 "
       "C498,576 504,538 518,508 C510,498 500,492 492,494 Z",
       "Chest bib", fill=CHEST, opacity=95, stroke=NONE)
# red belly spanning the whole lower abdomen, running under the bib's hem
d.path("M474,600 C512,588 556,600 580,634 C594,656 596,678 582,692 "
       "C556,708 512,708 486,692 C468,680 460,656 464,632 "
       "C466,620 468,608 474,600 Z",
       "Red belly", fill=BELLY_GR, stroke=NONE)
# chest-to-belly division line
d.path("M470,606 C498,596 536,598 568,614", "Breast split", fill=NONE,
       stroke="#5E4A40", strokeWidth=3, opacity=55, cap="round")

# feet gripping the branch — small grey, heterodactyl hint (2+2 toes)
for sgn, lab in ((-1, "L"), (1, "R")):
    fx = 486 + (0 if sgn < 0 else 52)
    fy_ = 724 + (0 if sgn < 0 else 6)
    for k in (-1, 1):
        d.path(f"M{fx},{fy_-8} Q{fx + k*10},{fy_+2} {fx + k*9},{fy_+12}",
               f"Toe {lab}{k:+d}", fill=NONE, stroke="#3A3226",
               strokeWidth=3.5, cap="round")
    d.path(f"M{fx-2},{fy_-2} q6,8 4,14", f"Rear toe {lab}", fill=NONE,
           stroke="#3A3226", strokeWidth=3.5, cap="round")

# === head: dark metallic crown, turned slightly toward the viewer ====================
d.path("M472,384 "                                   # crown
       "C522,386 554,418 556,458 "                   # back of skull
       "C558,488 546,512 522,524 "                   # nape to throat
       "C498,534 468,532 448,518 "                   # chin/throat
       "C424,502 414,474 420,446 "                   # cheek/face front
       "C426,412 444,388 472,384 Z",
       "Head", fill=HEAD_GR, stroke=INK, strokeWidth=5)
# grey-white throat where the bib meets the chin
d.path("M448,514 C460,526 482,532 502,530 C490,522 478,512 472,500 "
       "C460,500 452,506 448,514 Z", "Throat patch",
       fill="#C8CCC2", opacity=70, stroke=NONE)
# the eye: dark, large, with a fine pale orbital ring
d.shape("ellipse", "Orbital ring", x=443, y=430, width=40, height=40,
        fill=NONE, stroke="#8FA8B0", strokeWidth=3, opacity=70)
d.shape("ellipse", "Eye", x=448, y=435, width=30, height=30,
        fill="#10160E", stroke=NONE)
d.shape("ellipse", "Glint", x=455, y=440, width=8, height=8,
        fill="#FFFFFF", opacity=92, stroke=NONE)
# coral bill, slightly decurved, darker tip
d.path("M424,468 C406,470 392,480 384,494 C380,502 382,510 390,512 "
       "C402,514 416,510 424,502 C430,496 432,488 430,480 "
       "C428,474 426,470 424,468 Z",
       "Bill", fill=lin(424, 468, 388, 512, (0, "#D8645C"), (1, "#94302E")),
       stroke=INK, strokeWidth=3.5)
d.path("M384,494 C390,500 400,502 408,500", "Bill tip shade", fill=NONE,
       stroke="#5E1E1C", strokeWidth=3, opacity=80, cap="round")
# nape feather texture
for i, (x, y, dx, dy) in enumerate([(540,440,14,-8),(556,470,12,-4),(548,506,10,0)]):
    d.path(f"M{x},{y} L{x+dx},{y+dy}", f"Nape barb {i+1}", fill=NONE,
           stroke="#4EA894", strokeWidth=2.5, opacity=55, cap="round")
# cool rim light down the back
d.path("M560,486 C592,510 610,552 612,600", "Back rim", fill=NONE,
       stroke="#7ED8C0", strokeWidth=5, opacity=30, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0E140C", strokeWidth=6)

# --- captions -----------------------------------------------------------------------
r1 = d.text("CUBAN TROGON", "Name", x=500, y=930, size=58,
            font="Virelai Sans", color="#D8E0CC", justify="center")
r2 = d.text("PRIOTELUS TEMNURUS", "Second line", x=500, y=968, size=22,
            font="Virelai Sans", color="#9AAE8C", justify="center")
d.cmd("text.setStyle", "Second line tracking", id=r2["id"], tracking=300)

def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit
layers = d.call("inspect_document", {}, "inspect")["layers"]
for r, lab, wmax in [(r1, "name", 800), (r2, "line2", 760)]:
    b = find(layers, r["id"])["bounds"]
    print(lab, "bounds", {k: round(v) for k, v in b.items()})
    assert b["width"] <= wmax and b["x"] >= 100 and b["y"] + b["height"] <= 990, b

d.finish("cuban-trogon-V1R00")
