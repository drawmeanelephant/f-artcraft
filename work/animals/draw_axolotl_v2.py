#!/usr/bin/env python3
"""Axolotl — field plate V2R00, a rendition of V1R00.

V1 was a front-on cartoon face in a mint tank. This take is the animal:
full body in lateral profile, drifting right in a near-black tank, cold
caustic light from above and the six gill branches lit from behind so they
read as the only warm thing on the plate. Leucistic pink against deep teal.
1000x1000. House style: gradients + translucent shading, never flat fills.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Axolotl — Field Plate V2", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#3A2230"


BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#07161B"}, {"offset": 0.55, "color": "#040D11"},
    {"offset": 1, "color": "#010507"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#20505A"}, {"offset": 0.5, "color": "#123039"},
    {"offset": 1, "color": "#061115"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [0, 392], "end": [0, 572], "stops": [
    {"offset": 0, "color": "#FFF3F4"}, {"offset": 0.3, "color": "#FBD9DF"},
    {"offset": 0.68, "color": "#E9AEBF"}, {"offset": 1, "color": "#C07E99"}]}}
FIN_GRAD = {"gradient": {"kind": "linear", "start": [0, 436], "end": [0, 566], "stops": [
    {"offset": 0, "color": "#FFD9E1"}, {"offset": 0.55, "color": "#F0AFC2"},
    {"offset": 1, "color": "#C97F9B"}]}}
GILL_GRAD = {"gradient": {"kind": "linear", "angle": 200, "stops": [
    {"offset": 0, "color": "#FFC2CB"}, {"offset": 0.5, "color": "#F5738F"},
    {"offset": 1, "color": "#B93257"}]}}
GILL_FAR = {"gradient": {"kind": "linear", "angle": 200, "stops": [
    {"offset": 0, "color": "#C88096"}, {"offset": 1, "color": "#7E2C48"}]}}
SUB_GRAD = {"gradient": {"kind": "linear", "start": [0, 640], "end": [0, 780], "stops": [
    {"offset": 0, "color": "#1A3C42"}, {"offset": 1, "color": "#0A1B20"}]}}


def cr(pts, closed=False, tension=1.0):
    """Catmull-Rom through pts, as cubic Béziers."""
    n = len(pts)
    if n < 2:
        return ""
    ext = ([pts[-1]] + list(pts) + [pts[0], pts[1]]) if closed else \
          ([pts[0]] + list(pts) + [pts[-1]])
    dd = "M%.1f,%.1f " % pts[0]
    for i in range(1, n if closed else n - 1):
        p0, p1, p2, p3 = ext[i], ext[i + 1], ext[i + 2], ext[i + 3]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * tension, p1[1] + (p2[1] - p0[1]) / 6 * tension)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * tension, p2[1] - (p3[1] - p1[1]) / 6 * tension)
        dd += "C%.1f,%.1f %.1f,%.1f %.1f,%.1f " % (c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    return dd + ("Z" if closed else "")


# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0B2228", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BCEAF0", strokeWidth=3, opacity=24)

# water: one broad light shaft from the upper left, plus ripple bands
d.shape("ellipse", "Light shaft", x=120, y=60, width=420, height=330,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#9FE8F2", "opacity": 0.55},
            {"offset": 1, "color": "#9FE8F2", "opacity": 0}]}}, stroke=NONE, opacity=40)
d.shape("ellipse", "Light shaft 2", x=380, y=50, width=300, height=240,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#D6FBFF", "opacity": 0.4},
            {"offset": 1, "color": "#D6FBFF", "opacity": 0}]}}, stroke=NONE, opacity=30)
for i, (y, x0, x1, op) in enumerate([(150, 300, 690, 20), (188, 250, 730, 15),
                                     (228, 300, 650, 12), (272, 350, 610, 9)]):
    mid = (x0 + x1) / 2
    d.path(f"M{x0},{y} C{mid - 70},{y - 11} {mid - 20},{y + 11} {mid + 40},{y} "
           f"C{mid + 90},{y - 11} {x1 - 40},{y + 9} {x1},{y}",
           f"Ripple {i+1}", fill=NONE, stroke="#E8FDFF", strokeWidth=4, opacity=op, cap="round")

# substrate: a low soft mound resting on the disc's own arc
d.path("M180,700 C240,660 330,664 420,700 C510,736 620,742 700,716 "
       "C760,696 800,690 826,700 A420,420 0 0 1 174,700 Z",
       "Substrate", fill=SUB_GRAD, opacity=55, stroke=NONE)
d.path("M174,700 C300,690 420,724 540,736 C660,748 760,732 826,700",
       "Substrate crest", fill=NONE, stroke="#4E8A92", strokeWidth=3, opacity=26, cap="round")
# eelgrass off the mound: tapered blades, thin geometry kept above 4pt
for i, (xb, h, sway, w) in enumerate([(196, 210, 28, 14), (222, 264, -22, 12),
                                      (250, 218, 34, 12), (838, 150, -18, 10)]):
    left, right = [], []
    for k in range(9):
        t = k / 8
        cx = xb + sway * math.sin(t * 2.6) * t
        cy = 694 - h * t
        ww = w * (1 - 0.85 * t) * (1 + 0.2 * math.sin(t * 6))
        left.append((cx - ww / 2, cy))
        right.append((cx + ww / 2, cy))
    dd = "M%.1f,694 " % left[0][0]
    for p in left[1:]:
        dd += "L%.1f,%.1f " % p
    for p in reversed(right[1:]):
        dd += "L%.1f,%.1f " % p
    d.path(dd + "Z", f"Eelgrass {i+1}", fill="#2A6064", opacity=62, stroke=NONE)
    d.path("M%.1f,694 " % xb + " ".join("L%.1f,%.1f" % p for p in
           [(xb + sway * math.sin((k / 8) * 2.6) * (k / 8) + 1, 694 - h * (k / 8)) for k in range(1, 9)]),
           f"Eelgrass vein {i+1}", fill=NONE, stroke="#57A0A4", strokeWidth=2.6, opacity=34, cap="round")

# floating motes
for i, (x, y, w, op) in enumerate([(205, 330, 6, 38), (775, 300, 7, 32), (176, 520, 6, 26),
                                   (838, 470, 6, 28), (300, 780, 7, 24), (720, 800, 6, 22),
                                   (620, 130, 5, 28), (380, 118, 4, 24), (872, 620, 5, 20)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#D9F8FF", opacity=op, stroke=NONE)

# --- the animal -----------------------------------------------------------------
# top edge, snout to tail tip
TOP = [(198, 466), (222, 440), (258, 424), (300, 414), (346, 408), (400, 404),
       (452, 406), (500, 414), (542, 428), (572, 444), (620, 458), (668, 474),
       (714, 492), (748, 508), (766, 518)]
# bottom edge, tail tip back to snout
BOT = [(766, 522), (738, 520), (706, 520), (668, 512), (630, 504), (596, 498),
       (566, 500), (542, 508), (514, 522), (478, 534), (440, 542), (400, 544),
       (360, 540), (322, 530), (288, 518), (256, 506), (226, 492), (206, 480)]

# far-side limbs, behind the body
def limb(hip, knot, foot, label, far=False):
    w = 24 if not far else 19
    col = "#B4748C" if far else {"gradient": {"kind": "linear", "angle": 90, "stops": [
        {"offset": 0, "color": "#F9D3DB"}, {"offset": 1, "color": "#DFA0B5"}]}}
    d.path(f"M{hip[0]},{hip[1]} Q{knot[0]:.0f},{knot[1]:.0f} {foot[0]:.0f},{foot[1]:.0f}",
           f"{label} limb", fill=NONE, stroke=col, strokeWidth=w, cap="round",
           opacity=85 if far else 100)
    for j in range(4):
        sa = math.radians(28 + j * 38)
        tl = 19 if not far else 15
        d.path(f"M{foot[0]:.0f},{foot[1]:.0f} L{foot[0] + math.cos(sa) * tl:.1f},"
               f"{foot[1] + math.sin(sa) * tl:.1f}", f"{label} toe {j+1}", fill=NONE,
               stroke="#B9768E" if far else "#F6CBD5", strokeWidth=11 if not far else 9,
               cap="round", opacity=85 if far else 100)


limb((424, 480), (410, 536), (424, 580), "Far front leg", far=True)
limb((534, 486), (562, 546), (572, 588), "Far rear leg", far=True)

# far-side gills
def gill(bx, by, ang, length, label, far=False):
    a = math.radians(ang)
    ex = bx + math.cos(a) * length
    ey = by + math.sin(a) * length
    mx = bx + math.cos(a - 0.32) * length * 0.55
    my = by + math.sin(a - 0.32) * length * 0.55 - 12
    grad = GILL_FAR if far else GILL_GRAD
    op = 80 if far else 100
    d.path(f"M{bx},{by} Q{mx:.1f},{my:.1f} {ex:.1f},{ey:.1f}", f"{label} stalk",
           fill=NONE, stroke=grad, strokeWidth=11 if not far else 8, cap="round", opacity=op)
    # dense feathering on both sides of the stalk
    for j in range(13):
        t = 0.10 + 0.88 * j / 12
        px = (1 - t) ** 2 * bx + 2 * (1 - t) * t * mx + t * t * ex
        py = (1 - t) ** 2 * by + 2 * (1 - t) * t * my + t * t * ey
        side = 1 if j % 2 == 0 else -1
        sa = a + side * (0.95 - 0.12 * t)
        ln = (17 * (1 - 0.52 * t) + 2.4 * math.sin(j * 1.9)) * (0.8 if far else 1.0)
        d.path(f"M{px:.1f},{py:.1f} Q{px + math.cos(sa + 0.4) * ln * 0.72:.1f},"
               f"{py + math.sin(sa + 0.4) * ln * 0.72:.1f} "
               f"{px + math.cos(sa) * ln:.1f},{py + math.sin(sa) * ln:.1f}",
               f"{label} filament {j+1}", fill=NONE, stroke=grad,
               strokeWidth=4.4 if not far else 3.2, cap="round", opacity=op - 6)


for i, (bx, by, ang, ln) in enumerate([(336, 418, -76, 84), (344, 436, -52, 96),
                                       (352, 454, -28, 88)]):
    gill(bx + 10, by - 16, ang, ln * 0.9, f"Far gill {i+1}", far=True)


# --- tail: one continuous fin wrapping the tip ----------------------------------
# the fin's inner edge is the body edge itself, so no second outline can show
tail_top = TOP[9:]
tail_bot = BOT[:6]
H_T = [0, 10, 17, 19, 13, 0]
H_B = [0, 11, 17, 15, 7, 0]
outer_top = [(x, y - h) for (x, y), h in zip(tail_top, H_T)]
outer_bot = [(x, y + h) for (x, y), h in zip(tail_bot, H_B)]
TIP = (777, 532)
# two simple bands, no self-intersection at the tip
dorsal_band = cr(tail_top + list(reversed(outer_top)), closed=True)
ventral_band = cr(list(reversed(tail_bot)) + outer_bot, closed=True)
d.path(dorsal_band, "Dorsal fin", fill="#F6C2D0", stroke=NONE, opacity=42)
d.path(ventral_band, "Ventral fin", fill="#F0B4C6", stroke=NONE, opacity=38)
d.path(cr(outer_top[1:]), "Dorsal fin edge", fill=NONE, stroke="#FFE2E9",
       strokeWidth=2.4, opacity=42, cap="round")
d.path(cr(outer_bot[:-1]), "Ventral fin edge", fill=NONE, stroke="#FFE2E9",
       strokeWidth=2.4, opacity=38, cap="round")
for i in range(1, len(tail_top) - 1):
    (x0, y0), (ox, oy) = tail_top[i], outer_top[i]
    d.path(f"M{x0},{y0} L{ox:.1f},{oy + 3:.1f}", f"Dorsal fin ray {i}",
           fill=NONE, stroke="#FFF0F4", strokeWidth=2.2, opacity=24, cap="round")
for i in range(1, len(tail_bot) - 1):
    (x0, y0), (ox, oy) = tail_bot[i], outer_bot[i]
    d.path(f"M{x0},{y0} L{ox:.1f},{oy - 3:.1f}", f"Ventral fin ray {i}",
           fill=NONE, stroke="#FFF0F4", strokeWidth=2.2, opacity=22, cap="round")

# body
d.path(cr(TOP + BOT, closed=True), "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=5)

# shading passes that follow the body
d.path(cr([(258, 424), (300, 414), (346, 408), (400, 404)]), "Head top sheen",
       fill=NONE, stroke="#FFFFFF", strokeWidth=14, opacity=22, cap="round")
d.path(cr([(400, 420), (452, 420), (500, 428), (542, 440)]), "Back sheen",
       fill=NONE, stroke="#FFFFFF", strokeWidth=12, opacity=18, cap="round")
d.path(cr([(300, 508), (360, 528), (400, 534), (440, 532)]), "Jaw shade",
       fill=NONE, stroke="#B06E88", strokeWidth=12, opacity=28, cap="round")
d.path(cr([(470, 524), (514, 514), (548, 500), (578, 494)]), "Belly shade",
       fill=NONE, stroke="#A9637E", strokeWidth=10, opacity=24, cap="round")
d.path(cr([(600, 452), (650, 468), (700, 486), (745, 508), (768, 524)]), "Tail rim light",
       fill=NONE, stroke="#CFF6FF", strokeWidth=3.6, opacity=22, cap="round")

# belly volume: one soft pass along the ventral edge, head to tail
d.path(cr([(232, 486), (288, 518), (340, 536), (400, 544), (452, 540), (500, 530),
           (548, 512), (596, 498), (640, 506), (690, 514)]),
       "Belly volume", fill=NONE, stroke="#A05E7A", strokeWidth=18, opacity=22, cap="round")
# and a rim of colder light on the back so the body reads round
d.path(cr([(262, 418), (300, 410), (346, 404), (400, 400), (452, 402), (500, 410)]),
       "Back light", fill=NONE, stroke="#FFF6F8", strokeWidth=9, opacity=30, cap="round")

# the tail darkens toward the tip so the body doesn't end in a white point
d.path(cr(tail_top + list(reversed(tail_bot)), closed=True), "Tail shade",
       fill={"gradient": {"kind": "linear", "start": [552, 462], "end": [766, 518], "stops": [
           {"offset": 0, "color": "#B06E88", "opacity": 0.0},
           {"offset": 0.5, "color": "#AE6C86", "opacity": 0.22},
           {"offset": 1, "color": "#9E5A78", "opacity": 0.5}]}},
       stroke=NONE)

# faint freckles
for i, (x, y, w) in enumerate([(286, 442, 5), (320, 434, 4), (368, 430, 5), (410, 428, 4),
                               (452, 432, 5), (494, 438, 4), (530, 448, 4), (566, 462, 4),
                               (606, 480, 4), (648, 494, 3), (686, 508, 3), (340, 452, 3)]):
    d.shape("ellipse", f"Freckle {i+1}", x=x, y=y, width=w, height=w,
            fill="#BE7C96", opacity=30, stroke=NONE)

# head details
d.shape("ellipse", "Eye socket", x=238, y=416, width=34, height=30,
        fill="#FFEDF1", opacity=55, stroke=NONE)
d.shape("ellipse", "Eye", x=244, y=421, width=22, height=20, fill="#2A1B24",
        stroke="#8E5064", strokeWidth=2.5)
d.shape("ellipse", "Eye glint", x=247, y=424, width=7, height=7, fill="#FFFFFF", opacity=92, stroke=NONE)
d.path("M240,414 C250,408 262,410 268,418", "Brow", fill=NONE, stroke="#C487A0",
       strokeWidth=3, opacity=45, cap="round")
d.shape("ellipse", "Nostril", x=209, y=458, width=5, height=4, fill="#8E5064", opacity=65, stroke=NONE)
d.path("M201,482 C220,492 244,496 266,490", "Mouth", fill=NONE, stroke="#7A4458",
       strokeWidth=3.6, cap="round", opacity=85)
d.path("M214,470 C223,472 229,478 231,486", "Snout crease", fill=NONE, stroke="#CE93A6",
       strokeWidth=3, opacity=45, cap="round")

# near limbs
limb((408, 474), (392, 534), (404, 578), "Near front leg")
limb((522, 480), (552, 542), (562, 586), "Near rear leg")

# near gills, the warm note over everything
for i, (bx, by, ang, ln) in enumerate([(332, 422, -74, 92), (340, 440, -48, 104),
                                       (348, 458, -24, 96)]):
    gill(bx, by, ang, ln, f"Near gill {i+1}")
d.shape("ellipse", "Gill bloom", x=250, y=300, width=260, height=230,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FF8FA6", "opacity": 0.42},
            {"offset": 1, "color": "#FF8FA6", "opacity": 0}]}}, stroke=NONE, opacity=45)

# --- rim redrawn so nothing leaks past the disc ---------------------------------
# nothing may show outside the disc: repaint the backdrop over the ring,
# then the rim gets drawn back on top of it
d.shape("ellipse", "Backdrop mask", x=-200, y=-240, width=1400, height=1400,
        fill=NONE, stroke=BG_GRAD, strokeWidth=560)

d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#0B2228", strokeWidth=6)
d.shape("ellipse", "Rim highlight", x=88, y=48, width=824, height=824,
        fill=NONE, stroke="#8FD0DA", strokeWidth=2, opacity=16)

d.text("AXOLOTL", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#DDF0F2", justify="center")

print("body bbox x %.0f..%.0f y %.0f..%.0f" % (min(p[0] for p in TOP + BOT), max(p[0] for p in TOP + BOT),
                                               min(p[1] for p in TOP + BOT), max(p[1] for p in TOP + BOT)))
d.finish("axolotl-V2R00")
