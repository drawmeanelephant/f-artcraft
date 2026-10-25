#!/usr/bin/env python3
"""Labrador retriever — milestone card V1R00. Head-and-shoulders portrait
in three-quarter, head lifted as if marking a fall over wet marsh: broad
skull, kind dark eyes, drop ears, the otter tail just visible curling up
behind the shoulder. Black coat carried by sheen, never flat black; the
bust closes on the disc's own arc (portrait rule). Wet-marsh disc:
dark water, reed strokes, low mist. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Labrador Retriever — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#201915"                    # warm dark ink, never pure black


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#101A18"), (1, "#060B0A"))
PLATE_GRAD = rad((0, "#9FB4A4"), (0.55, "#647F72"), (1, "#33463E"))
COAT_GRAD = lin(380, 330, 640, 780, (0, "#4A4038"), (0.5, "#2C251F"), (1, "#16100D"))
DIM_GRAD = lin(380, 330, 640, 780, (0, "#352C25"), (1, "#120D0B"))
WATER_GRAD = lin(0, 760, 0, 880, (0, "#4E6258"), (0.55, "#32453C"), (1, "#1C2A24"))

# --- backdrop + marsh plate ----------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#26382F", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8E4D4", strokeWidth=3, opacity=38)

# thin dawn light pooling upper-centre
d.shape("ellipse", "Light pool", x=320, y=140, width=380, height=230,
        fill="#E4E8CC", opacity=14, stroke=NONE)
# marsh mist in thin lenses
for i, (x, y, w) in enumerate([(300, 300, 80), (620, 230, 70), (720, 360, 75),
                               (240, 450, 60), (760, 470, 60), (460, 190, 55)]):
    assert on_disc(x, y, 20), i
    d.shape("ellipse", f"Mist {i+1}", x=x - w / 2, y=y - w / 5, width=w, height=w * 0.4,
            fill="#E4ECD8", opacity=11, stroke=NONE)

# reeds behind the dog, rising off the waterline inside the rim
for i, (x, y0, y1, lean) in enumerate([(218, 640, 470, -14), (238, 660, 520, -6),
                                       (782, 650, 480, 12), (762, 670, 540, 4),
                                       (256, 700, 590, -10)]):
    y_rim = PCY + math.sqrt(max(0, PR * PR - (x - PCX) ** 2)) - 240
    assert on_disc(x, y0, 8), i
    d.path(f"M{x},{y0} C{x + lean * 0.5},{(y0 + y1) / 2} {x + lean},{y1 + 30} {x + lean},{y1}",
           f"Reed {i+1}", fill=NONE, stroke="#3A4E40", strokeWidth=4.5,
           opacity=60, cap="round")
    d.path(f"M{x + lean},{y1} l{3 if lean > 0 else -3},-16",
           f"Reed tip {i+1}", fill=NONE, stroke="#55684E", strokeWidth=4,
           opacity=55, cap="round")

# --- marsh water, closing on the disc arc ---------------------------------------
wy = 800
wl, wr = rim_x(wy, -1), rim_x(wy, 1)
d.path(f"M{wl:.1f},{wy} C320,792 420,812 500,802 C580,792 680,798 {wr:.1f},{wy} "
       f"A{PR},{PR} 0 0 1 {wl:.1f},{wy} Z", "Water", fill=WATER_GRAD, stroke=NONE)
d.path(f"M{wl + 8:.0f},{wy} C320,792 420,812 500,802 C580,792 680,798 {wr - 8:.0f},{wy}",
       "Waterline", fill=NONE, stroke="#9AB0A0", strokeWidth=5, opacity=40, cap="round")
# ripple glints on the water
for i, dd in enumerate(["M330,830 C370,824 410,824 450,830",
                        "M560,838 C600,832 640,832 680,838",
                        "M400,852 C430,848 460,848 490,852"]):
    d.path(dd, f"Ripple {i+1}", fill=NONE, stroke="#A8BCAC",
           strokeWidth=3.5, opacity=30, cap="round")

# soft shadow where the bust meets the water
d.shape("ellipse", "Bust shadow", x=280, y=782, width=440, height=34,
        fill="#0E1410", opacity=30, stroke=NONE)

# --- the labrador, three-quarter bust, head lifted left -------------------------
# otter tail first — thick at the base, tapering, just showing behind the
# right shoulder, held level with a slight upward curve
d.path(smooth([(660, 640), (716, 620), (762, 596), (788, 566), (792, 540),
               (780, 528), (758, 548), (726, 574), (690, 598), (656, 612)]),
       "Otter tail", fill=DIM_GRAD, stroke=INK, strokeWidth=5)
d.path("M762,560 C774,548 786,536 792,526", "Tail sheen", fill=NONE,
       stroke="#6A5C4C", strokeWidth=4, opacity=60, cap="round")

# shoulders + chest: sides land on the rim at y~810, bottom closes on the arc
sl, sr = rim_x(810, -1) + 14, rim_x(810, 1) - 14
d.path(smooth([(sl, 810), (292, 756), (310, 690), (352, 636), (400, 606),
               (470, 596), (560, 600), (640, 622), (700, 668), (722, 734),
               (sr, 810), (640, 850), (500, 862), (360, 848)]),
       "Shoulders", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# sheen along the shoulder topline and chest edge
d.path("M330,700 C380,660 440,640 520,640 C600,642 664,668 706,714",
       "Shoulder sheen", fill=NONE, stroke="#5E5142", strokeWidth=6,
       opacity=45, cap="round")
d.path("M316,738 C336,712 358,692 382,678", "Chest sheen", fill=NONE,
       stroke="#6A5C48", strokeWidth=5, opacity=40, cap="round")

# neck — one wedge rising off the shoulders into the back of the lifted head
d.path(smooth([(420, 660), (430, 600), (446, 548), (470, 512), (510, 500),
               (556, 510), (590, 540), (606, 580), (606, 624), (590, 660),
               (560, 680), (470, 680)]),
       "Neck", fill=COAT_GRAD, stroke=INK, strokeWidth=6)

# head — one silhouette, skull flowing into the lifted muzzle, nose highest.
# three-quarter to the left: we see the left flank of the face, both eyes.
d.path(smooth([(298, 438), (316, 424), (352, 412), (376, 398), (396, 372),
               (428, 350), (474, 344), (524, 348), (558, 370), (576, 406),
               (578, 448), (566, 486), (538, 514), (500, 532), (452, 538),
               (404, 530), (368, 510), (340, 488), (316, 466)]),
       "Head", fill=COAT_GRAD, stroke=INK, strokeWidth=6)
# crown sheen — wet sheen catching the light along the skull top
d.path("M398,390 C428,364 480,354 532,364 C482,364 436,376 404,404 Z",
       "Crown sheen", fill="#6E6050", opacity=40, stroke=NONE)
# the stop — the dip where muzzle meets forehead, and the cheek groove
d.path("M372,400 C380,412 382,424 378,438", "Stop", fill=NONE,
       stroke="#0F0A08", strokeWidth=4, opacity=50, cap="round")
d.path("M420,472 C460,484 512,484 548,470", "Cheek line", fill=NONE,
       stroke="#17110D", strokeWidth=4, opacity=40, cap="round")
# flew — the lab's soft square lip under the muzzle
d.path("M300,452 C316,470 342,484 372,492", "Flew", fill=NONE,
       stroke="#17110D", strokeWidth=4.5, opacity=65, cap="round")
# closed mouth — soft level line under the flew
d.path("M316,468 C336,480 362,486 388,488", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, opacity=80, cap="round")
# nose — broad black, sitting at the lifted muzzle tip
d.path("M292,424 C280,428 276,438 284,446 C292,452 306,448 312,438 "
       "C314,428 304,420 292,424 Z", "Nose", fill="#120C09",
       stroke=INK, strokeWidth=3.5)
d.path("M286,432 C292,427 300,426 306,430", "Nose sheen", fill=NONE,
       stroke="#7A6A58", strokeWidth=3, opacity=75, cap="round")
# bridge sheen running off the nose back to the stop
d.path("M314,436 C336,424 356,416 374,412", "Bridge sheen", fill=NONE,
       stroke="#5E5044", strokeWidth=4, opacity=45, cap="round")

# drop ears — near ear hangs behind the jaw against the neck; far ear
# folds down the right of the skull
d.path(smooth([(404, 392), (386, 414), (378, 452), (380, 492), (396, 520),
               (416, 524), (426, 500), (424, 462), (418, 424)]),
       "Ear near", fill=DIM_GRAD, stroke=INK, strokeWidth=5)
d.path(smooth([(552, 396), (572, 416), (584, 450), (584, 488), (574, 516),
               (556, 528), (544, 512), (540, 474), (542, 428)]),
       "Ear far", fill=DIM_GRAD, stroke=INK, strokeWidth=4.5)
d.path("M398,424 C392,452 392,482 400,504", "Ear fold L", fill=NONE,
       stroke="#0F0A08", strokeWidth=3.5, opacity=50, cap="round")
d.path("M560,426 C566,452 566,482 560,504", "Ear fold R", fill=NONE,
       stroke="#0F0A08", strokeWidth=3.5, opacity=45, cap="round")

# kind dark eyes — lifted toward the fall, soft not hard
d.path("M396,442 C404,432 420,430 430,438 C428,451 412,456 402,451 "
       "C396,447 394,446 396,442 Z", "Eye near",
       fill=rad((0, "#7A5428"), (0.7, "#4A3016"), (1, "#241608")),
       stroke=INK, strokeWidth=3.5)
d.path("M500,434 C508,425 522,424 530,431 C529,442 515,447 506,443 "
       "C500,439 498,438 500,434 Z", "Eye far",
       fill=rad((0, "#7A5428"), (0.7, "#4A3016"), (1, "#241608")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil near", x=403, y=433, width=10, height=11, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Pupil far", x=507, y=426, width=9, height=10, fill="#0E0806", stroke=NONE)
d.shape("ellipse", "Glint near", x=405, y=434, width=4.5, height=4.5, fill="#FFF4D8", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint far", x=509, y=427, width=4, height=4, fill="#FFF4D8", opacity=85, stroke=NONE)
# soft lids — kind eyes, brows level
d.path("M392,432 C406,424 422,424 432,430", "Brow near", fill=NONE,
       stroke="#0F0A08", strokeWidth=3.5, opacity=50, cap="round")
d.path("M496,424 C508,418 524,418 534,424", "Brow far", fill=NONE,
       stroke="#0F0A08", strokeWidth=3.5, opacity=45, cap="round")

# (older mouth/cheek guide strokes removed — the flew above carries the lip)

# wet sheen strokes on neck and shoulder — the marsh dog is damp
for i, dd in enumerate(["M446,560 C480,548 524,548 556,560",
                        "M452,648 C496,638 548,640 584,654"]):
    d.path(dd, f"Sheen {i+1}", fill=NONE, stroke="#6E5E4A",
           strokeWidth=5, opacity=18, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#22352B", strokeWidth=6)

# --- captions -------------------------------------------------------------------
d.text("LABRADOR RETRIEVER", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E8ECDC", justify="center")
LINE2, SZ2, TRK = "SPORTING · NEWFOUNDLAND", 22, 280
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font="Virelai Sans",
           color="#BCC8B4", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("labrador-retriever-V1R00")
