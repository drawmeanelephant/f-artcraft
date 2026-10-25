#!/usr/bin/env python3
"""American Quarter Horse — milestone card V1R00. The stock horse at
rest but coiled: head carried low, neck level out of high withers, a
hindquarter that outweighs everything else on the frame. Sorrel-copper
coat over ranch-country ochres; a faded rail fence line on the far side
of the disc. Compact frame — shorter back, deep heart girth, big round
hip. 1000x1000. House style: gradients + translucent shading, never
flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("American Quarter Horse — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241A12"                    # warm dark ink, never pure black


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


def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad


def rim_x(y, side=-1):
    return PCX + side * math.sqrt(PR * PR - (y - PCY) ** 2)


def find(o, oid):
    if isinstance(o, dict):
        if o.get("id") == oid and "bounds" in o: return o
        o = list(o.values())
    if isinstance(o, list):
        for v in o:
            hit = find(v, oid)
            if hit: return hit


BG_GRAD = lin(0, 0, 0, 1000, (0, "#1A120C"), (1, "#0B0604"))
PLATE_GRAD = rad((0, "#C8A06A"), (0.55, "#8E6A40"), (1, "#443024"))
COAT_GRAD = lin(320, 480, 720, 800, (0, "#B87A44"), (0.5, "#7E4E28"), (1, "#3A2212"))
DIM_GRAD = lin(320, 480, 720, 800, (0, "#7E5228"), (1, "#2C1A0E"))
HAIR_GRAD = lin(660, 540, 740, 700, (0, "#3A2414"), (1, "#1C1008"))
FLOOR_GRAD = lin(0, 730, 0, 880, (0, "#6E5230"), (0.55, "#4A3820"), (1, "#241A0E"))

# --- backdrop + mesa-dusk plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#38281A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EFD8AC", strokeWidth=3, opacity=38)

# low sun sinking right
d.shape("ellipse", "Dusk sun", x=600, y=240, width=110, height=110,
        fill="#F0CE8E", opacity=20, stroke=NONE)
# thin light pooling upper-left
d.shape("ellipse", "Light pool", x=245, y=150, width=400, height=230,
        fill="#F2DFAF", opacity=12, stroke=NONE)
# dust lenses
for i, (x, y, w) in enumerate([(320, 330, 90), (565, 245, 70), (715, 365, 80),
                               (250, 475, 60), (755, 495, 64), (455, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Dust {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#EAD6A6", opacity=10, stroke=NONE)

# faded rail fence on the far side of the pasture
d.path("M620,642 C700,638 780,640 830,646", "Fence rail", fill=NONE,
       stroke="#3E3220", strokeWidth=4, opacity=30, cap="round")
for i, x in enumerate([650, 745, 828]):
    assert on_disc(x, 655, 12), i
    d.path(f"M{x},632 L{x},660", f"Fence post {i+1}", fill=NONE,
           stroke="#3E3220", strokeWidth=4, opacity=30, cap="round")

# --- dusty floor, closing on the disc arc ------------------------------------------
fy = 780
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#C8A468", strokeWidth=5, opacity=40, cap="round")
d.path("M330,822 C430,810 560,808 680,816", "Dust line", fill=NONE,
       stroke="#3A2C16", strokeWidth=4, opacity=45, cap="round")
# dry tufts on the crest
for i, (x, y) in enumerate([(340, 800), (425, 828), (545, 834), (640, 820), (695, 798)]):
    assert on_disc(x, y + 8, 14), i
    for j, (dx, dy) in enumerate([(-12, 8), (-4, -6), (4, -12), (12, -2)]):
        d.path(f"M{x + dx * 0.3:.0f},{y + 12} L{x + dx:.0f},{y + dy:.0f}",
               f"Tuft {i+1}.{j+1}", fill=NONE, stroke="#9A7C46",
               strokeWidth=3.5, opacity=65, cap="round")

# soft shadow under the horse
d.shape("ellipse", "Horse shadow", x=295, y=764, width=420, height=30,
        fill="#171106", opacity=33, stroke=NONE)

# --- the quarter horse, head low, facing left ---------------------------------------
# tail — thick, natural, hanging with a soft wave
d.path(smooth([(700, 552), (722, 578), (730, 618), (726, 654), (714, 684),
               (702, 692), (692, 678), (690, 640), (690, 600), (688, 572)]),
       "Tail", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M706,570 C714,604 716,640 712,670",
                        "M700,566 C706,598 708,634 704,664"]):
    d.path(dd, f"Tail strand {i+1}", fill=NONE, stroke="#5E4028",
           strokeWidth=3.5, opacity=50, cap="round")

# legs before the body — stocky, the near hind slightly cocked at rest
d.path(smooth([(428, 652), (434, 700), (431, 742), (428, 770), (434, 784),
               (420, 788), (410, 780), (410, 744), (414, 706), (418, 664)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(460, 650), (466, 698), (463, 740), (460, 770), (466, 786),
               (452, 790), (440, 782), (438, 744), (440, 706), (442, 664)]),
       "Front leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path(smooth([(604, 650), (626, 672), (632, 708), (622, 742), (612, 770),
               (618, 784), (602, 788), (590, 776), (588, 740), (596, 704),
               (590, 666)]),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(644, 642), (670, 664), (678, 704), (668, 740), (658, 772),
               (664, 788), (648, 792), (634, 780), (630, 744), (636, 704),
               (626, 662)]),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# one silhouette: small plain head held low -> level neck -> high withers
# -> short back -> huge round hip -> deep girth -> broad chest -> jaw
d.path(smooth([(296, 578), (306, 566), (316, 550), (330, 532), (344, 518),
               (362, 508), (384, 512), (424, 522), (462, 534), (490, 545),
               (570, 552), (668, 556), (702, 586), (712, 634), (692, 668),
               (656, 686), (558, 700), (470, 690), (424, 664), (404, 630),
               (404, 600), (392, 570), (378, 542), (366, 528), (352, 532),
               (330, 548), (316, 562), (300, 572)]),
       "Horse", fill=COAT_GRAD, stroke=INK, strokeWidth=6)

# small dark hooves
for i, (cx, cy) in enumerate([(452, 787), (415, 785), (648, 790), (603, 785)]):
    d.path(f"M{cx - 14},{cy - 8} C{cx - 6},{cy - 12} {cx + 8},{cy - 12} {cx + 14},{cy - 6} "
           f"C{cx + 12},{cy + 3} {cx - 10},{cy + 5} {cx - 14},{cy - 1} Z",
           f"Hoof {i+1}", fill="#150D09", stroke=INK, strokeWidth=3)

# muscle shading — the powerful hindquarter gets the biggest mass
d.path("M492,548 C560,542 630,546 686,564 C626,550 558,546 492,548 Z",
       "Topline sheen", fill="#DCA868", opacity=38, stroke=NONE)
d.path("M706,592 C712,622 706,650 688,668 C700,646 704,616 706,592 Z",
       "Quarter shade", fill="#1E1410", opacity=30, stroke=NONE)
# the hip's big round muscle — translucent bulge shading
d.shape("ellipse", "Hip mass", x=640, y=585, width=60, height=70,
        fill="#1E1410", opacity=13, stroke=NONE)
d.path("M512,690 C556,697 608,695 646,684 C610,700 556,702 516,696 Z",
       "Barrel shade", fill="#1E1410", opacity=25, stroke=NONE)
# gaskin + stifle planes
d.path("M656,660 C668,682 674,706 672,728 C662,706 656,682 654,662 Z",
       "Gaskin plane", fill="#1E1410", opacity=25, stroke=NONE)
d.path("M424,608 C434,634 438,660 434,684 C426,660 422,632 422,608 Z",
       "Shoulder shade", fill="#1E1410", opacity=28, stroke=NONE)
# throatlatch shadow
d.path("M368,530 C378,518 384,500 384,480 C390,502 386,524 374,538 Z",
       "Throatlatch", fill="#1E1410", opacity=35, stroke=NONE)

# mane — short band along the level crest
d.path(smooth([(364, 508), (400, 516), (438, 528), (472, 540), (490, 548),
               (498, 560), (482, 550), (448, 536), (410, 522), (380, 514),
               (364, 514)]),
       "Mane", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)

# ears — relaxed, slightly out
d.path("M354,514 L358,470 L384,500 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M378,506 L394,476 L396,502 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M362,506 L364,482", "Ear inner", fill=NONE, stroke="#0F0A08",
       strokeWidth=3, opacity=55, cap="round")

# forehead sheen
d.shape("ellipse", "Forehead sheen", x=336, y=514, width=24, height=16,
        fill="#DCA868", opacity=30, stroke=NONE)

# eye — calm, low-set on the dropped head
d.path("M334,540 C342,532 356,532 362,540 C360,552 346,556 338,550 "
       "C333,546 332,544 334,540 Z", "Eye",
       fill=rad((0, "#6E4A24"), (0.7, "#422A12"), (1, "#1E1208")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=342, y=538, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=344, y=539, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
d.path("M330,526 C344,520 358,520 368,526", "Brow", fill=NONE,
       stroke="#241812", strokeWidth=4, opacity=55, cap="round")

# nostril + mouth on the low muzzle
d.path("M298,566 C292,571 292,580 299,583 C307,585 312,579 310,572 "
       "C307,565 301,563 298,566 Z", "Nostril", fill="#120B07",
       stroke=INK, strokeWidth=3)
d.path("M297,573 C301,569 307,569 310,572", "Nostril sheen", fill=NONE,
       stroke="#8A705A", strokeWidth=2.5, opacity=70, cap="round")
d.path("M308,584 C318,588 330,590 342,589", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=75, cap="round")
d.path("M340,570 C354,574 368,572 378,564", "Cheek line", fill=NONE,
       stroke="#241812", strokeWidth=3, opacity=40, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#352718", strokeWidth=6)

# --- captions -------------------------------------------------------------------
nr = d.text("AMERICAN QUARTER HORSE", "Name", x=500, y=934, size=48, font="Virelai Sans",
            color="#EFDCB4", justify="center")
LINE2, SZ2, TRK = "STOCK HORSE · UNITED STATES", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#CCB388", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b
nb = find(d.call("inspect_document", {}, "inspect")["layers"], nr["id"])["bounds"]
print("name bounds", {k: round(v) for k, v in nb.items()})
assert nb["x"] >= 10 and nb["x"] + nb["width"] <= 990, nb

d.finish("american-quarter-horse-V1R00")
