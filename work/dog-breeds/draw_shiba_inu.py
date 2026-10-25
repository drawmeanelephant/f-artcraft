#!/usr/bin/env python3
"""Shiba inu — milestone card V1R00. Seated alert in profile: red-sesame
coat with dark guard ticks, cream urajiro on cheeks, bib, belly and the
underside of the tight tail curl resting on the rump. Triangular ears,
calm self-possessed gaze levelled left. Deep indigo disc, a few autumn
leaves on the carpet. 1000x1000. House style: gradients + translucent
shading, never flat fills. Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Shiba Inu — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#241C18"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#101324"), (1, "#05060C"))
PLATE_GRAD = rad((0, "#8E96B8"), (0.55, "#545E80"), (1, "#2B3248"))
COAT_GRAD = lin(340, 380, 640, 780, (0, "#CC8640"), (0.5, "#A8642C"), (1, "#703E16"))
CREAM_GRAD = lin(300, 480, 480, 780, (0, "#F2E8D2"), (1, "#D2BE9A"))
DIM_GRAD = lin(340, 380, 640, 780, (0, "#8A5624"), (1, "#482408"))
FLOOR_GRAD = lin(0, 750, 0, 880, (0, "#4E5472"), (0.55, "#383C56"), (1, "#1D2030"))

# --- backdrop + indigo plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2A3044", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8DCE8", strokeWidth=3, opacity=38)

# cool dusk light pooling upper-left
d.shape("ellipse", "Light pool", x=250, y=150, width=400, height=230,
        fill="#E6EAF6", opacity=13, stroke=NONE)
# thin mist lenses
for i, (x, y, w) in enumerate([(320, 320, 90), (570, 240, 70), (715, 355, 80),
                               (250, 465, 60), (748, 485, 64), (450, 190, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#DCE0EC", opacity=12, stroke=NONE)

# --- carpet floor, closing on the disc arc -------------------------------------
fy = 780
fl, fr = rim_x(fy, -1), rim_x(fy, 1)
d.path(f"M{fl:.1f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr:.1f},{fy} "
       f"A{PR},{PR} 0 0 1 {fl:.1f},{fy} Z", "Floor", fill=FLOOR_GRAD, stroke=NONE)
d.path(f"M{fl + 8:.0f},{fy} C300,768 400,790 500,780 C600,770 700,776 {fr - 8:.0f},{fy}",
       "Floor crest", fill=NONE, stroke="#8C90AC", strokeWidth=5, opacity=42, cap="round")
# fallen autumn leaves — small two-part ticks scattered on the carpet
for i, (x, y) in enumerate([(370, 812), (480, 834), (590, 830), (672, 808)]):
    assert on_disc(x, y + 8, 16), i
    d.path(f"M{x:.0f},{y + 10} L{x + 6:.0f},{y - 6}",
           f"Leaf stem {i+1}", fill=NONE, stroke="#7A6E50", strokeWidth=3, opacity=60, cap="round")
    d.path(f"M{x + 6:.0f},{y - 6} C{x - 2:.0f},{y - 12} {x - 8:.0f},{y - 4} "
           f"{x - 4:.0f},{y + 4} C{x + 2:.0f},{y + 8} {x + 10:.0f},{y + 4} {x + 12:.0f},{y - 2} Z",
           f"Leaf {i+1}", fill="#8A5A30", opacity=58, stroke=NONE)

# soft shadow the dog sits over
d.shape("ellipse", "Dog shadow", x=320, y=758, width=430, height=32,
        fill="#12101E", opacity=32, stroke=NONE)

# --- the shiba, seated alert, facing left --------------------------------------
# tail — the tight curl lying on the rump: outer fluff ring, darker hollow,
# cream urajiro underside
d.path(smooth([(620, 480), (646, 444), (688, 436), (722, 458), (736, 496),
               (724, 534), (692, 552), (656, 548), (630, 522), (620, 480)]),
       "Tail curl", fill=lin(620, 440, 730, 550, (0, "#C8843E"), (1, "#7A4418")),
       stroke=INK, strokeWidth=5)
d.path(smooth([(662, 486), (678, 472), (698, 476), (706, 494), (700, 514),
               (682, 522), (666, 514), (660, 500)]),
       "Tail hollow", fill="#3A2008", opacity=85, stroke=INK, strokeWidth=3.5)
d.path("M622,516 C634,540 660,554 688,550 C664,560 634,546 620,522 Z",
       "Tail urajiro", fill=CREAM_GRAD, opacity=85, stroke=NONE)
d.path("M626,486 C636,458 664,442 694,448", "Tail curl seam", fill=NONE,
       stroke=INK, strokeWidth=3.5, opacity=55, cap="round")

# body — the seated mass: withers to rump, thigh folded, on the floor
d.path(smooth([(392, 508), (476, 452), (568, 472), (652, 534), (706, 614),
               (724, 700), (712, 756), (640, 768), (548, 762), (540, 720),
               (534, 668), (510, 632), (460, 610), (414, 600), (392, 560)]),
       "Body", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# back sheen — dusk light along the topline
d.path("M410,500 C480,462 570,470 640,520 C570,484 480,476 410,512 Z",
       "Back sheen", fill="#E8B878", opacity=30, stroke=NONE)
# hind paw resting forward on the floor
d.path("M470,736 C492,728 520,732 534,744 C536,758 522,770 496,770 "
       "C476,768 462,756 470,736 Z", "Hind paw", fill=COAT_GRAD,
       stroke=INK, strokeWidth=4.5)
d.path("M470,754 C484,760 512,762 528,756", "Hind paw urajiro", fill=NONE,
       stroke="#D2BE9A", strokeWidth=5, opacity=70, cap="round")
# belly tuck — cream sliver under the folded belly
d.path("M478,652 C520,696 556,726 588,746 C556,740 520,714 486,672 Z",
       "Belly urajiro", fill=CREAM_GRAD, opacity=40, stroke=NONE)

# far front leg — dimmer column just behind
d.path(smooth([(428, 606), (440, 660), (438, 720), (432, 752), (418, 754),
               (410, 720), (412, 656), (416, 610)]),
       "Front leg far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path("M406,744 C422,738 440,742 444,754 C440,766 424,772 410,768 "
       "C402,760 400,750 406,744 Z", "Front paw far", fill=DIM_GRAD,
       stroke=INK, strokeWidth=4)

# chest bib — the urajiro wedge from throat to brisket, then the near leg
d.path(smooth([(352, 560), (386, 580), (404, 624), (404, 690), (392, 748),
               (372, 760), (352, 744), (342, 680), (340, 614)]),
       "Chest bib", fill=CREAM_GRAD, stroke=INK, strokeWidth=4.5)
# near front leg — straight column carrying the weight
d.path(smooth([(368, 640), (384, 690), (384, 736), (376, 762), (358, 764),
               (350, 734), (350, 684), (354, 644)]),
       "Front leg near", fill=CREAM_GRAD, stroke=INK, strokeWidth=5)
d.path("M346,748 C362,740 382,744 386,756 C382,770 364,776 350,770 "
       "C342,762 340,754 346,748 Z", "Front paw near", fill=CREAM_GRAD,
       stroke=INK, strokeWidth=4.5)

# neck — the ruff bridging skull and chest so the head sits on shoulders
d.path(smooth([(354, 444), (390, 428), (430, 468), (446, 520), (438, 566),
               (402, 588), (366, 568), (350, 512), (346, 470)]),
       "Neck ruff", fill=COAT_GRAD, stroke=INK, strokeWidth=5)

# head — wedge skull, muzzle tapering left, cheek cream wrapping under jaw
d.path(smooth([(396, 414), (366, 390), (326, 386), (292, 404), (270, 432),
               (264, 452), (274, 470), (300, 482), (336, 490), (370, 486),
               (394, 462), (400, 436)]),
       "Skull + muzzle", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# urajiro — cream from under the nose wrapping the muzzle sides and cheeks
d.path(smooth([(264, 448), (278, 468), (306, 480), (340, 486), (368, 482),
               (384, 464), (372, 446), (340, 446), (306, 448), (280, 446)]),
       "Cheek urajiro", fill=CREAM_GRAD, opacity=95, stroke=NONE)
# nose — dark leather on the muzzle tip
d.path("M268,444 C258,446 254,454 258,462 C264,468 276,466 280,458 "
       "C280,450 276,444 268,444 Z", "Nose", fill="#17100C",
       stroke=INK, strokeWidth=3)
d.path("M262,454 C266,450 272,449 276,451", "Nose sheen", fill=NONE,
       stroke="#5E5046", strokeWidth=2.5, opacity=70, cap="round")
# mouth — the calm level line
d.path("M270,472 C282,478 298,478 310,472", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")

# ears — two erect triangles, slightly outward, tips sharp
d.path("M330,392 L318,306 L378,368 Z", "Ear L", fill=COAT_GRAD,
       stroke=INK, strokeWidth=5)
d.path("M322,360 L320,326 L344,352 Z", "Ear L inner", fill=DIM_GRAD,
       stroke=NONE, opacity=90)
d.path("M384,392 L404,300 L430,376 Z", "Ear R", fill=COAT_GRAD,
       stroke=INK, strokeWidth=5)
d.path("M396,360 L406,324 L416,356 Z", "Ear R inner", fill=DIM_GRAD,
       stroke=NONE, opacity=90)

# eye — dark almond, calm and level
d.path("M320,426 C330,418 346,418 354,426 C350,436 336,440 326,436 "
       "C318,432 316,430 320,426 Z", "Eye",
       fill=rad((0, "#6E4A20"), (0.7, "#40260E"), (1, "#201004")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=333, y=425, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint", x=336, y=427, width=4.5, height=4.5, fill="#FFF4D8",
        opacity=90, stroke=NONE)
# brow line — the quiet self-possession
d.path("M316,412 C330,406 348,406 360,412", "Brow", fill=NONE,
       stroke="#5E3410", strokeWidth=4, opacity=55, cap="round")

# red-sesame — dark guard-hair ticks along the topline and rump
for i, dd in enumerate(["M440,470 C450,462 462,458 474,458",
                        "M500,470 C510,464 522,462 534,464",
                        "M560,486 C570,482 582,482 592,486",
                        "M620,520 C630,518 640,520 648,526",
                        "M664,570 C672,568 680,572 686,578"]):
    d.path(dd, f"Sesame {i+1}", fill=NONE, stroke="#3A2008",
           strokeWidth=3.5, opacity=50, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#242A3C", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("SHIBA INU", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E8EAF2", justify="center")
LINE2, SZ2, TRK = "NON-SPORTING · JAPAN", 22, 300
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#BCC0D2", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("shiba-inu-V1R00")
