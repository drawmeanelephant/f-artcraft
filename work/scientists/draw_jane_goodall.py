#!/usr/bin/env python3
"""Jane Goodall — milestone card V1R00. Khaki field clothes, binoculars
at the neck, seated at a Gombe-green forest edge while a young chimp
reaches toward her open hand — patience is the pose. Centre part, low
ponytail. The forest floor is a chord band closed on the disc's own
lower arc; big leaf masses hang in the upper dark. 1000x1000. House
style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Jane Goodall — Milestone Card", 1000, 1000)

PCX, PCY, PR = 500, 460, 420
INK = "#1E150F"                    # warm dark ink, never pure black
SS3 = "Source Sans 3"              # Virelai Sans has no digit glyphs


def _stops(*pairs):
    out = []
    for p in pairs:
        s = {"offset": p[0], "color": p[1]}
        if len(p) > 2:
            s["opacity"] = p[2]
        out.append(s)
    return out


def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": _stops(*stops)}}


def rad(*stops):
    return {"gradient": {"kind": "radial", "stops": _stops(*stops)}}


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


BG_GRAD = lin(0, 0, 0, 1000, (0, "#0D140A"), (1, "#040603"))
PLATE_GRAD = rad((0, "#687E56"), (0.5, "#3E5238"), (1, "#152012"))
SKIN_GRAD = lin(420, 320, 500, 540, (0, "#E2B98E"), (0.55, "#BE9468"), (1, "#8A6848"))
SKIN_DIM = lin(420, 320, 500, 540, (0, "#BE986E"), (1, "#7A5C40"))
HAIR_GRAD = lin(410, 290, 520, 470, (0, "#6E5638"), (0.5, "#453322"), (1, "#1E140C"))
KHAKI_GRAD = lin(350, 540, 560, 780, (0, "#A89A70"), (0.5, "#6E6250"), (1, "#3A3424"))
PANT_GRAD = lin(330, 640, 560, 790, (0, "#6A6248"), (0.5, "#463F2C"), (1, "#221E14"))
FLOOR_GRAD = lin(0, 750, 0, 890, (0, "#3E422A"), (0.55, "#262A1A"), (1, "#101206"))
CHIMP_GRAD = lin(600, 600, 740, 780, (0, "#4C4238"), (0.5, "#302920"), (1, "#181310"))
CHIMP_SKIN = "#8A7458"
LEAF = "#2E4A2C"
LEAF_HI = "#567A48"

# --- backdrop + Gombe-green plate ---------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2A3624", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE4CC", strokeWidth=3, opacity=34)

# canopy light pooling upper-left
d.shape("ellipse", "Light pool", x=235, y=145, width=380, height=220,
        fill="#E4EAD0", opacity=11, stroke=NONE)

# --- forest edge: big leaves hanging into the upper dark -----------------------------
# left frond cluster — broad leaves angled down-inward, inside the rim
for i, (lx, ly, ang, ln, op) in enumerate([(196, 210, 65, 150, 62),
                                         (260, 170, 80, 110, 55),
                                         (170, 330, 55, 130, 50)]):
    a = math.radians(ang)
    tx, ty = lx + ln * math.cos(a), ly + ln * math.sin(a)
    vx, vy = -math.sin(a), math.cos(a)
    w = ln * 0.26
    pts = [(lx, ly),
           (lx + ln * 0.35 * math.cos(a) + vx * w, ly + ln * 0.35 * math.sin(a) + vy * w),
           (tx + vx * w * 0.3, ty + vy * w * 0.3),
           (tx, ty),
           (tx - vx * w * 0.3, ty - vy * w * 0.3),
           (lx + ln * 0.35 * math.cos(a) - vx * w, ly + ln * 0.35 * math.sin(a) - vy * w)]
    assert on_disc(tx, ty, 8) and on_disc(lx + vx * w, ly + vy * w, 4), i
    d.path(smooth(pts, k=0.9), f"Leaf L{i+1}", fill=LEAF, opacity=op,
           stroke=INK, strokeWidth=3)
    d.path(f"M{lx},{ly} L{tx:.0f},{ty:.0f}", f"Leaf vein L{i+1}",
           fill=NONE, stroke=LEAF_HI, strokeWidth=2.5, opacity=50,
           cap="round")
# right frond — drooping palm over the chimp's side
for i, (lx, ly, ang, ln, op) in enumerate([(792, 190, 118, 150, 60),
                                           (720, 140, 105, 110, 50)]):
    a = math.radians(ang)
    tx, ty = lx + ln * math.cos(a), ly + ln * math.sin(a)
    vx, vy = -math.sin(a), math.cos(a)
    w = ln * 0.24
    pts = [(lx, ly),
           (lx + ln * 0.35 * math.cos(a) + vx * w, ly + ln * 0.35 * math.sin(a) + vy * w),
           (tx + vx * w * 0.3, ty + vy * w * 0.3),
           (tx, ty),
           (tx - vx * w * 0.3, ty - vy * w * 0.3),
           (lx + ln * 0.35 * math.cos(a) - vx * w, ly + ln * 0.35 * math.sin(a) - vy * w)]
    assert on_disc(tx, ty, 8) and on_disc(lx - vx * w, ly - vy * w, 4), i
    d.path(smooth(pts, k=0.9), f"Leaf R{i+1}", fill=LEAF, opacity=op,
           stroke=INK, strokeWidth=3)
    d.path(f"M{lx},{ly} L{tx:.0f},{ty:.0f}", f"Leaf vein R{i+1}",
           fill=NONE, stroke=LEAF_HI, strokeWidth=2.5, opacity=50,
           cap="round")

# --- the forest floor — a chord band closed on the disc's arc -------------------------
fj = 772
jl, jr = rim_x(fj, -1), rim_x(fj, 1)
d.path(f"M{jl:.1f},{fj} C360,{fj - 16} 640,{fj - 16} {jr:.1f},{fj} "
       f"A{PR},{PR} 0 0 1 {jl:.1f},{fj} Z", "Forest floor",
       fill=FLOOR_GRAD, stroke=INK, strokeWidth=4)
# grass tufts at the band's ends
for i, (gx, gy, gdeg) in enumerate([(258, 764, -18), (282, 770, 8),
                                    (726, 766, -10), (752, 758, 14)]):
    assert on_disc(gx, gy - 26, 6), i
    for s in (-1, 0, 1):
        a = math.radians(gdeg + s * 16 - 90)
        d.path(f"M{gx},{gy} L{gx + 26 * math.cos(a):.0f},"
               f"{gy + 26 * math.sin(a):.0f}", f"Grass {i+1}.{s+2}",
               fill=NONE, stroke=LEAF_HI, strokeWidth=3, opacity=45,
               cap="round")

# --- Jane, seated — folded-leg mound, torso, open offered hand -------------------------
# seated lower body — knees up, legs folded across the floor
d.path(smooth([(332, 766), (330, 706), (352, 662), (392, 644), (440, 650),
               (486, 640), (520, 668), (548, 716), (560, 766)], k=0.9),
       "Legs folded", fill=PANT_GRAD, stroke=INK, strokeWidth=4.5)
# knee creases + a field boot at the right end
d.path("M392,656 C384,690 384,720 392,750", "Knee crease L", fill=NONE,
       stroke="#221E14", strokeWidth=4, opacity=45, cap="round")
d.path("M486,648 C478,684 478,720 486,752", "Knee crease R", fill=NONE,
       stroke="#221E14", strokeWidth=4, opacity=45, cap="round")
d.path(smooth([(516, 730), (552, 722), (576, 736), (580, 762), (560, 776),
               (522, 776), (510, 756)]), "Boot", fill="#2A241A",
       stroke=INK, strokeWidth=3.5)

# khaki shirt torso — sits on the leg mound
d.path(smooth([(368, 700), (366, 640), (378, 590), (398, 560), (424, 546),
               (452, 542), (486, 546), (510, 566), (524, 606), (528, 660),
               (524, 706)], k=0.9), "Shirt", fill=KHAKI_GRAD,
       stroke=INK, strokeWidth=4.5)
# rolled sleeves + shirt placket
d.path("M448,552 L452,690", "Placket", fill=NONE, stroke="#4E4632",
       strokeWidth=3, opacity=60, cap="round")
d.path(smooth([(388, 566), (402, 556), (424, 550), (436, 558), (430, 580),
               (402, 586), (388, 580)]), "Collar L", fill=KHAKI_GRAD,
       stroke=INK, strokeWidth=3)
d.path(smooth([(486, 550), (506, 556), (518, 566), (514, 584), (490, 584),
               (478, 566)]), "Collar R", fill=KHAKI_GRAD, stroke=INK,
       strokeWidth=3)

# binoculars on a strap at her chest — the field signature
d.path("M436,556 C440,592 446,614 456,630 M498,556 C494,592 488,614 480,630",
       "Bino strap", fill=NONE, stroke="#241E14", strokeWidth=3.5,
       opacity=80, cap="round")
d.path("M442,630 L490,630 L494,668 L438,668 Z", "Binocs",
       fill=lin(438, 630, 494, 668, (0, "#3A362C"), (1, "#181510")),
       stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Bino L", x=446, y=650, width=16, height=18,
        fill="#0E0C08", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Bino R", x=470, y=650, width=16, height=18,
        fill="#0E0C08", stroke=INK, strokeWidth=3)

# left arm — resting on the raised left knee, open and still
d.path(smooth([(388, 570), (366, 604), (356, 646), (352, 692), (360, 716),
               (378, 720), (390, 702), (396, 656), (404, 610), (404, 580)],
              k=0.9), "Arm L", fill=KHAKI_GRAD, stroke=INK,
       strokeWidth=4)
d.path(smooth([(352, 704), (360, 696), (376, 698), (384, 708), (378, 722),
               (360, 722)]), "Hand L", fill=SKIN_GRAD, stroke=INK,
       strokeWidth=3.5)

# right arm — extended low toward the chimp, palm open and up
d.path(smooth([(508, 566), (534, 592), (554, 626), (572, 656), (592, 676),
               (596, 692), (584, 700), (566, 688), (542, 656), (522, 624),
               (504, 592), (498, 572)], k=0.9), "Arm R",
       fill=KHAKI_GRAD, stroke=INK, strokeWidth=4)
# forearm skin below the rolled cuff
d.path(smooth([(566, 652), (584, 668), (596, 684), (590, 696), (574, 690),
               (558, 672)]), "Forearm", fill=SKIN_GRAD, stroke=INK,
       strokeWidth=3)
# the offered hand — palm up, fingers soft
d.path(smooth([(590, 686), (604, 680), (620, 682), (630, 692), (624, 704),
               (606, 706), (592, 700)]), "Hand offered", fill=SKIN_GRAD,
       stroke=INK, strokeWidth=3.5)
d.path("M604,690 L622,690", "Palm line", fill=NONE, stroke="#8A6248",
       strokeWidth=2.5, opacity=65, cap="round")

# neck
d.path("M448,502 L448,544 C456,552 478,552 486,544 L486,502 Z", "Neck",
       fill=SKIN_DIM, stroke=INK, strokeWidth=3.5)

# --- head: centre part, low ponytail, weathered tan ----------------------------------
# hair cap + low ponytail swinging behind the right shoulder
d.path(smooth([(404, 432), (394, 382), (400, 334), (422, 300), (456, 286),
               (492, 294), (514, 324), (520, 372), (514, 424), (504, 446),
               (496, 420), (500, 372), (494, 330), (478, 306), (458, 300),
               (438, 308), (424, 334), (418, 376), (420, 420)], k=0.85),
       "Hair", fill=HAIR_GRAD, stroke=INK, strokeWidth=3.5)
d.path(smooth([(508, 430), (524, 452), (532, 492), (530, 534), (520, 552),
               (508, 548), (502, 512), (500, 470)], k=0.9), "Ponytail",
       fill=HAIR_GRAD, stroke=INK, strokeWidth=3.5)
# centre part + pulled strands
d.path("M458,294 L456,326", "Parting", fill=NONE, stroke="#140C06",
       strokeWidth=3, opacity=70, cap="round")
for i, dd in enumerate(["M422,340 C440,318 460,308 480,308",
                        "M418,380 C436,352 460,336 488,334"]):
    d.path(dd, f"Hair sweep {i+1}", fill=NONE, stroke="#8A6C44",
           strokeWidth=2.5, opacity=50, cap="round")

# face — oval, sun-warmed, tipped toward the reaching chimp
d.path(smooth([(458, 308), (496, 326), (504, 382), (498, 440), (486, 488),
               (470, 512), (456, 518), (442, 512), (426, 488), (414, 440),
               (408, 382), (416, 326)], k=0.85), "Face",
       fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
d.path("M406,408 C400,412 398,426 404,438 C408,444 414,442 416,434",
       "Ear L", fill=SKIN_DIM, stroke=INK, strokeWidth=3)

# features — warm eyes on the chimp, faint smile
d.path("M420,394 C431,388 445,387 455,393", "Brow L", fill=NONE,
       stroke="#3E2E1E", strokeWidth=4.5, opacity=80, cap="round")
d.path("M466,393 C477,387 491,388 500,394", "Brow R", fill=NONE,
       stroke="#3E2E1E", strokeWidth=4.5, opacity=80, cap="round")
d.path("M423,414 C430,407 445,407 452,413 C445,420 430,420 423,414 Z",
       "Eye L", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.path("M467,413 C474,406 488,406 495,412 C488,419 474,419 467,413 Z",
       "Eye R", fill="#EFE4D0", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Iris L", x=440, y=410, width=10, height=10,
        fill="#2E221A", stroke=NONE)
d.shape("ellipse", "Iris R", x=483, y=409, width=10, height=10,
        fill="#2E221A", stroke=NONE)
d.shape("ellipse", "Glint L", x=443, y=412, width=3.2, height=3.2,
        fill="#FFF4DC", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=486, y=411, width=3.2, height=3.2,
        fill="#FFF4DC", opacity=90, stroke=NONE)
d.path("M460,416 C465,432 466,448 461,460", "Nose shade", fill=NONE,
       stroke="#9A7658", strokeWidth=3.5, opacity=45, cap="round")
d.path("M453,462 C459,466 469,466 475,461", "Nose base", fill=NONE,
       stroke="#8A6248", strokeWidth=3, opacity=55, cap="round")
d.path("M442,490 C452,497 468,497 478,489", "Mouth", fill=NONE,
       stroke="#7E4C3E", strokeWidth=3.5, opacity=75, cap="round")

# --- the young chimp — small, reaching to the offered hand -----------------------------
# body — hunched quadruped mass on the floor, facing her
d.path(smooth([(636, 700), (644, 664), (668, 646), (698, 648), (722, 668),
               (732, 700), (730, 736), (722, 764), (656, 764), (640, 738)],
              k=0.9), "Chimp body", fill=CHIMP_GRAD, stroke=INK,
       strokeWidth=4.5)
# rear foot planted, knuckle forelimb down
d.path(smooth([(688, 764), (700, 738), (716, 722), (728, 728), (724, 748),
               (714, 764)]), "Hind leg", fill=CHIMP_GRAD, stroke=INK,
       strokeWidth=3.5)
d.path("M652,712 L644,760 L656,766 L664,718 Z", "Forelimb",
       fill=CHIMP_GRAD, stroke=INK, strokeWidth=3.5)

# reaching arm — from the shoulder up-left to her hand; a thick stroke
# plus the small hand
d.path("M650,662 C636,668 622,678 612,690", "Chimp arm", fill=NONE,
       stroke="#3A322A", strokeWidth=15, cap="round")
d.path(smooth([(606, 682), (618, 678), (626, 686), (622, 698), (610, 700),
               (602, 692)]), "Chimp hand", fill=CHIMP_SKIN, stroke=INK,
       strokeWidth=3)

# head — big for the body, pale face, wide ears
d.path(smooth([(600, 652), (590, 628), (596, 600), (616, 584), (640, 586),
               (656, 604), (658, 628), (648, 652), (626, 662)], k=0.9),
       "Chimp head", fill=CHIMP_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Chimp ear L", x=584, y=606, width=20, height=24,
        fill=CHIMP_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Chimp ear R", x=644, y=596, width=18, height=22,
        fill=CHIMP_GRAD, stroke=INK, strokeWidth=3)
# pale face mask + brow + eyes on her
d.path(smooth([(606, 640), (600, 622), (606, 604), (620, 594), (636, 598),
               (646, 612), (644, 634), (634, 650), (618, 652)], k=0.9),
       "Chimp face", fill=CHIMP_SKIN, stroke=INK, strokeWidth=3)
d.path("M608,612 C616,606 630,605 638,610", "Chimp brow", fill=NONE,
       stroke="#241E16", strokeWidth=4, opacity=80, cap="round")
d.shape("ellipse", "Chimp eye L", x=612, y=618, width=9, height=10,
        fill="#181210", stroke=NONE)
d.shape("ellipse", "Chimp eye R", x=630, y=615, width=9, height=10,
        fill="#181210", stroke=NONE)
d.shape("ellipse", "Chimp glint", x=614, y=620, width=2.8, height=2.8,
        fill="#FFF4DC", opacity=80, stroke=NONE)
d.path("M616,642 C622,646 632,645 637,640", "Chimp mouth", fill=NONE,
       stroke="#4A3A28", strokeWidth=3, opacity=70, cap="round")
# faint dark crown cap on the head top
d.path("M598,606 C606,592 622,584 640,588", "Chimp crown", fill=NONE,
       stroke="#241E16", strokeWidth=5, opacity=55, cap="round")

# plate rim over everything so decor closes under it
d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#28301F", strokeWidth=6)

# --- captions ---------------------------------------------------------------------
d.text("JANE GOODALL", "Name", x=500, y=934, size=56, font="Virelai Sans",
       color="#E8ECE0", justify="center")
LINE2, SZ2, TRK = "TOOL-MAKING CHIMPS · 1960", 22, 480
r = d.text(LINE2, "Milestone", x=500, y=970, size=SZ2, font=SS3,
           color="#C4CCBC", justify="center")
d.cmd("text.setStyle", "Milestone tracking", id=r["id"], tracking=TRK)

b = find(d.call("inspect_document", {}, "inspect")["layers"], r["id"])["bounds"]
print("milestone bounds", {k: round(v) for k, v in b.items()})
nearest = (min(max(PCX, b["x"]), b["x"] + b["width"]),
           min(max(PCY, b["y"]), b["y"] + b["height"]))
clear = math.hypot(nearest[0] - PCX, nearest[1] - PCY) - (PR + 3)
print("clears rim by %.1f" % clear)
assert clear > 0 and b["width"] <= 760 and b["x"] >= 10 and b["x"] + b["width"] <= 990, b

d.finish("jane-goodall-V1R00")
