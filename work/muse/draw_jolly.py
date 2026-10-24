#!/usr/bin/env python3
# Jolly, the regular Muse mascot - three VectorCraft illustrations.
import sys, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

INK = "#2B2620"
FUR = {"gradient": {"kind": "radial", "stops": [{"offset": 0, "color": "#F3E5C8"}, {"offset": 1, "color": "#DCC7A0"}]}}
FURSOLID = "#E7D5B0"
FACE = {"gradient": {"kind": "radial", "stops": [{"offset": 0, "color": "#FCF0D6"}, {"offset": 1, "color": "#F5E0B4"}]}}
SHADE = "#C9B18A"; GOLD = "#B98A2F"; GOLD_D = "#8A7648"; PAPER = "#F7F2E4"

def jolly(d, cx=450, wave=False, look=(0, 0)):
    ox = cx - 450  # x offset from canonical 450-centred drawing
    def X(x): return x + ox
    # arms first (roots tuck behind body)
    d.path(f"M{X(246)},540 C{X(206)},640 {X(190)},720 {X(196)},792", "Arm L",
           fill=NONE, stroke=FURSOLID, strokeWidth=66, cap="round")
    d.shape("ellipse", "Hand L", x=X(166), y=762, width=64, height=78, fill=FURSOLID, stroke=NONE)
    if wave:
        d.path(f"M{X(648)},520 C{X(716)},446 {X(752)},384 {X(762)},302", "Arm R wave",
               fill=NONE, stroke=FURSOLID, strokeWidth=66, cap="round")
        d.shape("ellipse", "Hand R", x=X(730), y=232, width=68, height=84, fill=FURSOLID, stroke=NONE)
        for r, a0, a1 in [(50, -38, 38), (74, -34, 34), (98, -30, 30)]:
            pts = []
            for i in range(13):
                a = math.radians(a0 + (a1 - a0) * i / 12)
                pts.append(f"{X(768) + r * math.cos(a):.0f},{278 + r * math.sin(a):.0f}")
            d.path("M" + " L".join(pts), f"Wave arc {r}", fill=NONE, stroke=GOLD, strokeWidth=5, opacity=65, cap="round")
    else:
        d.path(f"M{X(654)},540 C{X(694)},640 {X(710)},720 {X(704)},792", "Arm R",
               fill=NONE, stroke=FURSOLID, strokeWidth=66, cap="round")
        d.shape("ellipse", "Hand R", x=X(672), y=762, width=64, height=78, fill=FURSOLID, stroke=NONE)
    # body blob
    d.path(f"M{X(450)},150 C{X(596)},150 {X(668)},262 {X(676)},420 C{X(681)},545 {X(714)},648 {X(710)},756 "
           f"C{X(706)},852 {X(638)},916 {X(556)},930 L{X(344)},930 C{X(262)},916 {X(194)},852 {X(190)},756 "
           f"C{X(186)},648 {X(219)},545 {X(224)},420 C{X(232)},262 {X(304)},150 {X(450)},150 Z",
           "Body", fill=FUR, stroke=NONE)
    # side shading crescents
    d.path(f"M{X(238)},420 C{X(228)},548 {X(202)},652 {X(206)},752 C{X(209)},836 {X(258)},894 {X(326)},920 "
           f"C{X(262)},904 {X(202)},848 {X(198)},756 C{X(194)},650 {X(222)},540 {X(238)},420 Z",
           "Shade L", fill=SHADE, opacity=28, stroke=NONE)
    d.path(f"M{X(662)},420 C{X(672)},548 {X(698)},652 {X(694)},752 C{X(691)},836 {X(642)},894 {X(574)},920 "
           f"C{X(638)},904 {X(698)},848 {X(702)},756 C{X(706)},650 {X(678)},540 {X(662)},420 Z",
           "Shade R", fill=SHADE, opacity=28, stroke=NONE)
    d.shape("ellipse", "Belly highlight", x=X(300), y=560, width=300, height=300, fill="#FFFFFF", opacity=13, stroke=NONE)
    # feet
    for lbl, fx in [("Foot L", 288), ("Foot R", 484)]:
        d.shape("ellipse", lbl, x=X(fx), y=908, width=128, height=54, fill="#E2CDA6", stroke=NONE)
        d.path(f"M{X(fx + 14)},916 C{X(fx + 44)},906 {X(fx + 84)},906 {X(fx + 114)},916", lbl + " shade",
               fill=NONE, stroke=SHADE, strokeWidth=4, opacity=55, cap="round")
    # face plate
    d.path(f"M{X(278)},332 C{X(278)},246 {X(352)},200 {X(450)},200 C{X(548)},200 {X(622)},246 {X(622)},332 "
           f"C{X(622)},414 {X(548)},452 {X(450)},452 C{X(352)},452 {X(278)},414 {X(278)},332 Z",
           "Face", fill=FACE, stroke=NONE)
    d.path(f"M{X(318)},256 C{X(362)},216 {X(538)},216 {X(582)},256", "Face top shade",
           fill=NONE, stroke="#E4C88F", strokeWidth=7, opacity=50, cap="round")
    # blush
    for lbl, bx in [("Blush L", 310), ("Blush R", 506)]:
        d.shape("ellipse", lbl, x=X(bx), y=352, width=84, height=42, fill="#F2A48C", opacity=38, stroke=NONE)
        d.shape("ellipse", lbl + " core", x=X(bx + 18), y=362, width=48, height=22, fill="#EE9B82", opacity=30, stroke=NONE)
    # eyes + smile
    lx, ly = look
    for lbl, ex in [("Eye L", 372), ("Eye R", 528)]:
        d.shape("ellipse", lbl, x=X(ex - 17 + lx), y=305 + ly, width=34, height=34, fill=INK, stroke=NONE)
        d.shape("ellipse", lbl + " glint", x=X(ex - 8 + lx), y=311 + ly, width=10, height=10, fill="#FFFFFF", stroke=NONE)
    d.path(f"M{X(424)},372 C{X(438)},385 {X(462)},385 {X(476)},372", "Smile",
           fill=NONE, stroke=INK, strokeWidth=6.5, cap="round")
    # fur tufts along the top of the head
    for i, deg in enumerate(range(196, 345, 15)):
        a = math.radians(deg)
        px, py = X(450) + 218 * math.cos(a), 468 + 318 * math.sin(a)
        tx, ty = -math.sin(a), math.cos(a)
        pts = []
        for k, (along, out) in enumerate([(-13, 0), (-5, -11), (2, 0), (9, -10), (15, 1)]):
            pts.append(f"{px + tx * along + math.cos(a) * out:.0f},{py + ty * along + math.sin(a) * out:.0f}")
        d.path("M" + " L".join(pts), f"Tuft {i}", fill=NONE, stroke=SHADE, strokeWidth=4.5, opacity=55, cap="round")
    # fur ticks inside the body
    rng = random.Random(7)
    n = 0
    while n < 26:
        tx, ty = rng.uniform(250, 650), rng.uniform(520, 880)
        if ((tx - 450) / 235) ** 2 + ((ty - 690) / 215) ** 2 > 1: continue
        ang = math.radians(rng.uniform(-18, 18))
        L = rng.uniform(11, 19)
        d.path(f"M{X(tx)}, {ty} L{X(tx) + L * math.sin(ang):.0f},{ty + L * math.cos(ang):.0f}", f"Tick {n}",
               fill=NONE, stroke="#CBB289", strokeWidth=4, opacity=45, cap="round")
        n += 1

def backdrop(d, w, h, cx=450, cy=520, r=352):
    d.shape("rectangle", "Backdrop", x=0, y=0, width=w, height=h, fill=PAPER, stroke=NONE)
    d.shape("ellipse", "Halo", x=cx - r, y=cy - r, width=2 * r, height=2 * r, fill="#EFE3C8", stroke=NONE)
    d.shape("ellipse", "Halo ring", x=cx - r, y=cy - r, width=2 * r, height=2 * r, fill=NONE, stroke=GOLD, strokeWidth=1.6, opacity=55)
    d.shape("ellipse", "Ground shadow", x=cx - 195, y=950, width=390, height=38, fill="#3A2E1C", opacity=10, stroke=NONE)

# ---------- Piece 1: portrait ----------
d = Draw()
d.new_doc("Jolly - Portrait", 900, 1050)
backdrop(d, 900, 1050)
jolly(d)
d.text("JOLLY", "Caption", x=450, y=1032, size=36, font="Virelai Sans", color=GOLD_D, justify="center")
d.finish("jolly-portrait")

# ---------- Piece 2: waving ----------
d = Draw()
d.new_doc("Jolly - Waving", 900, 1050)
backdrop(d, 900, 1050)
jolly(d, wave=True)
for i, (sx, sy, s) in enumerate([(150, 190, 16), (692, 118, 12)]):
    d.path(f"M{sx},{sy - s} C{sx + s * 0.18},{sy - s * 0.18} {sx + s * 0.18},{sy - s * 0.18} {sx + s},{sy} "
           f"C{sx + s * 0.18},{sy + s * 0.18} {sx + s * 0.18},{sy + s * 0.18} {sx},{sy + s} "
           f"C{sx - s * 0.18},{sy + s * 0.18} {sx - s * 0.18},{sy + s * 0.18} {sx - s},{sy} "
           f"C{sx - s * 0.18},{sy - s * 0.18} {sx - s * 0.18},{sy - s * 0.18} {sx},{sy - s} Z",
           f"Sparkle {i}", fill=GOLD, stroke=NONE)
d.text("JOLLY, WAVING", "Caption", x=450, y=1032, size=36, font="Virelai Sans", color=GOLD_D, justify="center")
d.finish("jolly-waving")

# ---------- Piece 3: meets a very small Fart Knocker ----------
d = Draw()
d.new_doc("Jolly Meets Fart Knocker", 1200, 1050)
backdrop(d, 1200, 1050, cx=400)
jolly(d, cx=400, look=(6, 5))
# mini burger at (905, ground 955)
BUN = {"gradient": {"kind": "radial", "stops": [{"offset": 0, "color": "#F5B942"}, {"offset": 1, "color": "#C96A12"}]}}
d.shape("ellipse", "Burger shadow", x=812, y=946, width=186, height=20, fill="#3A2E1C", opacity=12, stroke=NONE)
d.path("M820,902 C820,844 858,810 905,810 C952,810 990,844 990,902 Z", "Mini dome", fill=BUN, stroke=NONE)
for i, (x, y) in enumerate([(862, 848), (905, 836), (946, 850), (884, 866)]):
    d.shape("ellipse", f"Mini sesame {i}", x=x, y=y, width=13, height=7, fill="#FBE3B0", stroke=NONE)
d.shape("rectangle", "Mini lettuce", x=820, y=902, width=170, height=8, fill="#7C9A52", stroke=NONE)
d.shape("rectangle", "Mini tomato", x=820, y=910, width=170, height=7, fill="#C8452C", stroke=NONE)
d.shape("rectangle", "Mini patty", x=820, y=917, width=170, height=10, fill="#6B4226", stroke=NONE)
d.path("M820,927 C820,952 858,968 905,968 C952,968 990,952 990,927 Z", "Mini face", fill="#F2C063", stroke=NONE)
d.shape("ellipse", "Mini eye L", x=876, y=938, width=8, height=10, fill=INK, stroke=NONE)
d.shape("ellipse", "Mini eye R", x=924, y=938, width=8, height=10, fill=INK, stroke=NONE)
d.shape("ellipse", "Mini monocle", x=916, y=932, width=24, height=24, fill="#FFFFFF", opacity=14, stroke=GOLD, strokeWidth=2.6)
d.path("M894,954 C900,958 910,958 916,954", "Mini smile", fill=NONE, stroke=INK, strokeWidth=3, cap="round")
d.path("M897,982 L862,968 C848,962 840,970 842,981 C840,992 848,998 862,993 L897,982 Z", "Mini bowtie L", fill="#23201B", stroke=NONE)
d.path("M913,982 L948,968 C962,962 970,970 968,981 C970,992 962,998 948,993 L913,982 Z", "Mini bowtie R", fill="#23201B", stroke=NONE)
d.shape("rectangle", "Mini knot", x=897, y=970, width=16, height=16, radius=4, fill="#322E28", stroke=NONE)
# a small heart over the burger
d.path("M905,772 C896,752 866,756 866,778 C866,796 888,806 905,822 C922,806 944,796 944,778 C944,756 914,752 905,772 Z",
       "Heart", fill="#D96A5A", stroke=NONE)
d.text("JOLLY MEETS A VERY SMALL FART KNOCKER", "Caption", x=600, y=1032, size=30,
       font="Virelai Sans", color=GOLD_D, justify="center")
d.finish("jolly-meets-fart-knocker")
print("ALL DONE")
