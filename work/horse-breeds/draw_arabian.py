#!/usr/bin/env python3
"""Arabian — milestone card V1R00. The desert horse's two signatures:
a dished profile (jibbah forehead bulge, concave drop to a tiny tapered
muzzle) and the tail flagged high like a banner. Body at a slight
three-quarter — offside legs stepped back and dimmed — with the head
held in profile so the dish reads. Arched mitbah neck, high withers,
level croup, fine legs. Desert-dusk palette: plum-dark sky, sand disc,
low sun. 1000x1000. House style: gradients + translucent shading,
never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Arabian — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#231A14"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#1C1220"), (1, "#0A060E"))
PLATE_GRAD = rad((0, "#C9A96E"), (0.55, "#96754A"), (1, "#493523"))
COAT_GRAD = lin(360, 380, 700, 800, (0, "#5C4433"), (0.5, "#3E2C20"), (1, "#201510"))
DIM_GRAD = lin(360, 380, 700, 800, (0, "#3A2C20"), (1, "#160E0A"))
HAIR_GRAD = lin(650, 380, 740, 600, (0, "#2A1C14"), (1, "#120B08"))
FLOOR_GRAD = lin(0, 730, 0, 880, (0, "#7C5E38"), (0.55, "#584124"), (1, "#30220F"))

# --- backdrop + desert-dusk plate ---------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3A2E1C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EED9AC", strokeWidth=3, opacity=38)

# low sun sinking toward the far dune line
d.shape("ellipse", "Dusk sun", x=588, y=248, width=110, height=110,
        fill="#EFCE8E", opacity=22, stroke=NONE)
# thin light pooling upper-left
d.shape("ellipse", "Light pool", x=245, y=150, width=400, height=230,
        fill="#F0DFAF", opacity=12, stroke=NONE)
# heat-shimmer lenses drifting over the sand
for i, (x, y, w) in enumerate([(320, 330, 90), (565, 245, 70), (715, 365, 80),
                               (250, 475, 60), (755, 495, 64), (455, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Shimmer {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#E8D6A4", opacity=10, stroke=NONE)

# --- sand floor, closing on the disc arc ---------------------------------------
fy = 780
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#C9A668", strokeWidth=5, opacity=40, cap="round")
# dune contours below the crest
d.path("M310,820 C410,808 545,806 695,816", "Dune line 1", fill=NONE,
       stroke="#3E2E16", strokeWidth=4, opacity=45, cap="round")
d.path("M360,845 C460,836 580,834 660,840", "Dune line 2", fill=NONE,
       stroke="#2E2210", strokeWidth=4, opacity=40, cap="round")
# dry grass tufts rooted on the crest
for i, (x, y) in enumerate([(335, 800), (420, 826), (545, 832), (640, 818), (692, 798)]):
    assert on_disc(x, y + 8, 14), i
    for j, (dx, dy) in enumerate([(-12, 8), (-4, -6), (4, -12), (12, -2)]):
        d.path(f"M{x + dx * 0.3:.0f},{y + 12} L{x + dx:.0f},{y + dy:.0f}",
               f"Grass {i+1}.{j+1}", fill=NONE, stroke="#9A7C46",
               strokeWidth=3.5, opacity=65, cap="round")

# soft shadow the horse stands over
d.shape("ellipse", "Horse shadow", x=300, y=766, width=410, height=30,
        fill="#171106", opacity=32, stroke=NONE)

# --- the arabian, facing left, body at a slight three-quarter -------------------
# tail first — the flag: slim plume leaning back off a high dock, root
# tucked under the croup so it emerges from the silhouette
d.path(smooth([(668, 568), (692, 508), (706, 448), (716, 396), (738, 392),
               (750, 436), (746, 498), (730, 554), (710, 588), (690, 594)]),
       "Tail", fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
for i, dd in enumerate(["M688,556 C700,508 710,458 718,412",
                        "M702,570 C716,524 726,474 732,426"]):
    d.path(dd, f"Tail strand {i+1}", fill=NONE, stroke="#6A5040",
           strokeWidth=3.5, opacity=55, cap="round")
# hair sheen along the plume's outer edge
d.path("M724,402 C740,442 748,492 742,540", "Tail edge sheen", fill=NONE,
       stroke="#8A6B4E", strokeWidth=4, opacity=40, cap="round")

# legs before the body — tops hide under the silhouette, fine-boned below
d.path(smooth([(430, 652), (434, 700), (431, 740), (426, 768), (431, 786),
               (422, 793), (410, 788), (408, 752), (410, 710), (416, 664)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(458, 652), (464, 698), (461, 738), (458, 764), (465, 786),
               (456, 795), (444, 789), (442, 750), (444, 708), (442, 664)]),
       "Front leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path(smooth([(604, 648), (628, 670), (634, 706), (624, 740), (612, 768),
               (616, 784), (601, 788), (589, 776), (587, 742), (595, 706),
               (590, 666)]),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path(smooth([(642, 642), (670, 666), (680, 702), (668, 738), (656, 772),
               (662, 788), (646, 793), (630, 782), (628, 744), (634, 706),
               (626, 664)]),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# fine tendon line — the "skin over bone" read on the near cannon
d.path("M452,700 C454,730 457,758 460,782", "Cannon tendon", fill=NONE,
       stroke="#241812", strokeWidth=3, opacity=45, cap="round")

# one silhouette: muzzle -> dish -> jibbah -> poll -> arched crest ->
# withers -> level croup -> hindquarter -> tucked flank -> deep chest ->
# throatlatch -> jaw -> chin -> muzzle
d.path(smooth([(292, 466), (304, 455), (316, 446), (330, 432), (340, 412),
               (354, 400), (372, 388), (390, 398), (425, 435), (475, 510),
               (496, 545), (560, 558), (668, 560), (698, 590), (705, 634),
               (684, 664), (650, 680), (558, 692), (478, 686), (428, 666),
               (409, 628), (408, 602), (395, 555), (388, 512), (380, 500),
               (368, 496), (338, 496), (316, 490), (298, 480)]),
       "Horse", fill=COAT_GRAD, stroke=INK, strokeWidth=6)

# small dark hooves capping each leg
for i, (cx, cy) in enumerate([(455, 790), (415, 790), (648, 791), (605, 786)]):
    d.path(f"M{cx - 14},{cy - 8} C{cx - 6},{cy - 12} {cx + 8},{cy - 12} {cx + 14},{cy - 6} "
           f"C{cx + 12},{cy + 3} {cx - 10},{cy + 5} {cx - 14},{cy - 1} Z",
           f"Hoof {i+1}", fill="#150D09", stroke=INK, strokeWidth=3)

# topline sheen + muscle shading kept at the silhouette edges
d.path("M466,552 C538,548 618,552 680,566 C618,556 542,552 466,552 Z",
       "Topline sheen", fill="#B08C64", opacity=35, stroke=NONE)
d.path("M696,592 C702,622 696,648 680,664 C692,644 696,616 696,592 Z",
       "Quarter shade", fill="#1E1410", opacity=30, stroke=NONE)
d.path("M515,682 C558,689 606,687 640,678 C606,694 556,695 518,690 Z",
       "Barrel shade", fill="#1E1410", opacity=25, stroke=NONE)
d.path("M382,404 C414,426 449,474 475,522", "Crest sheen", fill=NONE,
       stroke="#A8886A", strokeWidth=4, opacity=40, cap="round")
# throatlatch shadow — separates the deep jaw from the neck
d.path("M376,502 C388,488 396,468 395,446 C400,472 394,496 382,510 Z",
       "Throatlatch", fill="#1E1410", opacity=35, stroke=NONE)

# mane — a thin elegant band just behind the crest edge
d.path(smooth([(372, 386), (402, 400), (438, 442), (472, 496), (490, 532),
               (500, 548), (485, 540), (456, 496), (420, 446), (392, 408),
               (372, 394)]),
       "Mane", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M398,408 C428,446 458,494 484,542",
                        "M388,404 C416,440 444,486 472,536"]):
    d.path(dd, f"Mane strand {i+1}", fill=NONE, stroke="#0E0806",
           strokeWidth=3, opacity=45, cap="round")

# ears — small, tips curling toward each other
d.path("M360,394 L370,346 L388,386 Z", "Ear near", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4)
d.path("M384,386 L400,352 L402,384 Z", "Ear far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M368,386 L372,358", "Ear inner", fill=NONE, stroke="#0F0A08",
       strokeWidth=3, opacity=55, cap="round")

# forelock wisp over the poll
d.path("M372,390 C363,396 357,407 355,419 C364,411 373,402 381,398 Z",
       "Forelock", fill=HAIR_GRAD, stroke=NONE)
# forehead sheen on the jibbah
d.shape("ellipse", "Jibbah sheen", x=342, y=400, width=26, height=18,
        fill="#8A6B4E", opacity=35, stroke=NONE)

# eye — large, dark, set high and forward
d.path("M340,440 C348,432 362,432 368,440 C366,452 352,456 344,450 "
       "C339,446 338,444 340,440 Z", "Eye",
       fill=rad((0, "#6E4A24"), (0.7, "#422A12"), (1, "#1E1208")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=348, y=438, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=350, y=439, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
d.path("M336,426 C350,420 364,420 374,426", "Brow", fill=NONE,
       stroke="#241812", strokeWidth=4, opacity=55, cap="round")

# nostril — large, thin-skinned, flared at the tiny muzzle tip
d.path("M296,460 C290,465 290,474 297,477 C305,479 310,473 308,466 "
       "C305,459 299,457 296,460 Z", "Nostril", fill="#120B07",
       stroke=INK, strokeWidth=3)
d.path("M295,467 C299,463 305,463 308,466", "Nostril sheen", fill=NONE,
       stroke="#8A705A", strokeWidth=2.5, opacity=70, cap="round")
# quiet mouth
d.path("M304,484 C314,488 326,490 338,489", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=75, cap="round")
# fine facial bone — faint cheek line under the eye
d.path("M346,472 C360,476 374,474 384,466", "Cheek line", fill=NONE,
       stroke="#241812", strokeWidth=3, opacity=40, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#33271A", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("ARABIAN", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#EDDCB4", justify="center")
LINE2, SZ2, TRK = "HOTBLOOD · ARABIA", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#C8B284", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("arabian-V1R00")
