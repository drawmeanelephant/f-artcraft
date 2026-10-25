#!/usr/bin/env python3
"""Bernese mountain dog — milestone card V1R00. A broad, gentle draft dog
standing square in profile: jet-black body, rust points on brow, cheek and
legs, the white blaze running forehead to nose, the big white cross on the
chest and white socks planted on the carpet. Drop ears, bushy tail carried
low with a soft lift. Alpine dusk disc, snow-flecked meadow floor that
closes on the disc's arc. 1000x1000. House style: gradients + translucent
shading, never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Bernese Mountain Dog — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241C18"                    # warm dark ink, never pure black
RUST = "#A85A28"


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#0E1020"), (1, "#05050B"))
PLATE_GRAD = rad((0, "#8E8AAE"), (0.55, "#5A5878"), (1, "#2C2C44"))
COAT_GRAD = lin(320, 480, 700, 790, (0, "#3E3833"), (0.5, "#26211C"), (1, "#12100C"))
DIM_GRAD = lin(320, 480, 700, 790, (0, "#2A2520"), (1, "#0E0B08"))
WHITE_GRAD = lin(300, 540, 480, 790, (0, "#F2EDE0"), (1, "#D0C4A6"))
FLOOR_GRAD = lin(0, 760, 0, 890, (0, "#4E5268"), (0.55, "#363A4E"), (1, "#1B1D2B"))

# --- backdrop + alpine-dusk plate ------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#262A40", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DADCE8", strokeWidth=3, opacity=38)

# alpenglow pooling upper-left — a faint warm note in the dusk
d.shape("ellipse", "Light pool", x=250, y=150, width=400, height=230,
        fill="#F0DCC8", opacity=13, stroke=NONE)
# valley haze in thin lenses
for i, (x, y, w) in enumerate([(320, 330, 90), (565, 245, 70), (710, 360, 80),
                               (252, 470, 60), (748, 490, 64), (450, 195, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#DCDCE8", opacity=12, stroke=NONE)

# --- snow-flecked meadow floor, closing on the disc arc ---------------------------
fy = 790
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,778 400,800 500,790 C600,780 700,786 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,778 400,800 500,790 C600,780 700,786 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#8E92AE", strokeWidth=5, opacity=42, cap="round")
# snow flecks resting on the meadow
for i, (x, y, w) in enumerate([(346, 814, 30), (452, 836, 26), (562, 842, 32), (664, 820, 26)]):
    assert on_disc(x, y, 14), i
    d.shape("ellipse", f"Snow {i+1}", x=x - w / 2, y=y - 5, width=w, height=11,
            fill="#D8DCE6", opacity=45, stroke=NONE)
# alpine grass ticks through the snow
for i, (x, y) in enumerate([(396, 824), (610, 834)]):
    assert on_disc(x, y - 8, 16), i
    for j, (dx, dy) in enumerate([(-8, 8), (0, -10), (8, 6)]):
        d.path(f"M{x:.0f},{y + 10} L{x + dx:.0f},{y + dy:.0f}",
               f"Grass {i+1}.{j+1}", fill=NONE, stroke="#6E7448",
               strokeWidth=3.5, opacity=60, cap="round")

# broad shadow the dog stands over
d.shape("ellipse", "Dog shadow", x=280, y=762, width=470, height=32,
        fill="#0F0E1A", opacity=34, stroke=NONE)

# --- the bernese, standing square in profile --------------------------------------
# tail — bushy, carried low off the rump with a soft lift at the white tip
d.path(smooth([(694, 566), (730, 594), (752, 634), (760, 672), (752, 696),
               (732, 704), (714, 690), (700, 654), (688, 610)]),
       "Tail", fill=lin(690, 570, 760, 700, (0, "#332D28"), (1, "#171310")),
       stroke=INK, strokeWidth=5)
d.path("M724,678 C738,672 752,678 754,690 C748,700 732,702 724,694 "
       "C720,688 720,682 724,678 Z", "Tail white tip", fill=WHITE_GRAD,
       stroke=INK, strokeWidth=3.5)

# far-side legs — dimmer columns a step behind
d.path(smooth([(452, 668), (460, 706), (458, 748), (452, 772), (438, 774),
               (432, 748), (434, 704), (438, 668)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path("M430,764 C444,758 460,762 462,772 C458,782 442,786 430,780 "
       "C424,774 424,768 430,764 Z", "Front sock far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=4)
d.path(smooth([(586, 662), (598, 706), (600, 748), (594, 772), (580, 774),
               (574, 748), (576, 704), (580, 664)]),
       "Hind leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path("M572,764 C586,758 602,762 604,772 C600,782 584,786 572,780 "
       "C566,774 566,768 572,764 Z", "Hind sock far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=4)

# body — the broad barrel: level topline, deep chest, calm weight
d.path(smooth([(398, 545), (452, 508), (542, 496), (632, 506), (690, 538),
               (714, 592), (712, 648), (682, 688), (620, 704), (540, 708),
               (458, 702), (406, 678), (386, 622), (388, 574)]),
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# topline sheen — dusk light along the back
d.path("M430,540 C510,514 600,514 672,544 C600,526 510,524 430,552 Z",
       "Back sheen", fill="#8A94AE", opacity=28, stroke=NONE)

# near hind leg — column with a quiet hock bend, rust above the white sock
d.path(smooth([(644, 664), (664, 706), (668, 742), (662, 770), (646, 774),
               (636, 744), (636, 702), (638, 668)]),
       "Hind leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path("M638,704 C650,698 666,700 670,712 C664,724 646,726 638,718 "
       "C634,712 634,708 638,704 Z", "Hind rust", fill=RUST,
       stroke=INK, strokeWidth=3.5, opacity=90)
d.path("M634,752 C650,744 670,748 674,762 C670,776 652,784 636,778 "
       "C628,770 628,758 634,752 Z", "Hind sock near", fill=WHITE_GRAD,
       stroke=INK, strokeWidth=4)

# near front leg — straight column carrying the chest
d.path(smooth([(394, 662), (404, 706), (402, 748), (396, 772), (380, 774),
               (374, 746), (376, 700), (380, 664)]),
       "Front leg near", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
d.path("M378,706 C390,700 406,702 410,714 C404,726 386,728 378,720 "
       "C374,714 374,710 378,706 Z", "Front rust", fill=RUST,
       stroke=INK, strokeWidth=3.5, opacity=90)
d.path("M372,752 C388,744 408,748 412,762 C408,776 390,784 374,778 "
       "C366,770 366,758 372,752 Z", "Front sock near", fill=WHITE_GRAD,
       stroke=INK, strokeWidth=4)

# the white cross — blaze of the chest running throat to between the legs
d.path(smooth([(356, 556), (386, 580), (410, 630), (418, 690), (406, 736),
               (386, 748), (366, 730), (354, 668), (348, 606)]),
       "Chest cross", fill=WHITE_GRAD, opacity=94, stroke=NONE)

# neck ruff — thick mane bridging skull to withers
d.path(smooth([(352, 494), (388, 476), (428, 490), (450, 528), (450, 570),
               (420, 596), (382, 592), (358, 562), (346, 522)]),
       "Neck ruff", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# head — broad skull, kind eye, drop ear hanging beside the cheek
d.path(smooth([(368, 452), (340, 436), (308, 434), (282, 444), (262, 462),
               (254, 480), (260, 498), (278, 512), (306, 520), (338, 520),
               (362, 506), (372, 480)]),
       "Skull + muzzle", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# the white blaze — a stripe off the forehead running down the muzzle front
d.path(smooth([(300, 438), (316, 438), (314, 458), (304, 478), (290, 492),
               (274, 500), (262, 496), (258, 484), (264, 468), (282, 456)]),
       "Blaze", fill=WHITE_GRAD, opacity=95, stroke=NONE)
# rust points — brow dot and the cheek edge
d.path("M324,444 C332,438 344,438 350,444 C344,450 332,450 324,444 Z",
       "Brow rust", fill=RUST, opacity=90, stroke=NONE)
d.path("M292,492 C306,486 324,488 332,498 C322,508 302,508 292,502 Z",
       "Cheek rust", fill=RUST, opacity=80, stroke=NONE)

# drop ear — soft triangle hanging beside the skull
d.path(smooth([(352, 452), (382, 462), (392, 494), (388, 528), (370, 546),
               (352, 538), (344, 504), (344, 474)]),
       "Ear", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path("M356,470 C366,486 368,508 362,528", "Ear fold line", fill=NONE,
       stroke="#0E0B08", strokeWidth=3.5, opacity=50, cap="round")

# eye — the gentle dark almond
d.path("M298,462 C308,454 322,454 330,462 C326,472 312,476 302,472 "
       "C294,468 292,466 298,462 Z", "Eye",
       fill=rad((0, "#6E4A22"), (0.7, "#40280E"), (1, "#1E1004")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=310, y=461, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=313, y=463, width=4.5, height=4.5, fill="#FFF4D8",
        opacity=90, stroke=NONE)
# nose — broad dark leather
d.path("M254,478 C244,480 240,488 244,496 C250,502 262,500 266,492 "
       "C266,484 262,478 254,478 Z", "Nose", fill="#17100C",
       stroke=INK, strokeWidth=3)
d.path("M248,488 C252,484 258,483 262,485", "Nose sheen", fill=NONE,
       stroke="#5E5046", strokeWidth=2.5, opacity=70, cap="round")
# mouth — the soft level line
d.path("M262,508 C274,514 290,514 302,508", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")

# coat texture — long-hair ticks on chest edge, belly and britches
for i, dd in enumerate(["M352,600 C346,614 344,630 348,644",
                        "M376,640 C372,656 372,672 378,686",
                        "M500,700 C504,712 504,724 500,734",
                        "M560,702 C566,714 566,726 562,736",
                        "M660,660 C668,672 670,686 666,698"]):
    d.path(dd, f"Fur {i+1}", fill=NONE, stroke="#0E0B08",
           strokeWidth=3.5, opacity=50, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#222636", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("BERNESE MOUNTAIN DOG", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E8EAF0", justify="center")
LINE2, SZ2, TRK = "WORKING · SWITZERLAND", 22, 270
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#B8BCCB", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("bernese-mountain-dog-V1R00")
