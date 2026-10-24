#!/usr/bin/env python3
"""Windsor chair — field plate V2R01, refinement of V2R00.

V2R00 carried four half-finished seat constructions from its iteration, and
the last one to run was a plain concentric ellipse — so the seat read as a
disc stuck on legs. This pass keeps the room, the raking light and the cast
shadow, and gives the seat a single construction: a shield-shaped plank with
visible thickness, a dished top that is deepest toward the back, and a
rounded-over front lip that catches the low sun.
1000x1000. House style: gradients + translucent shading, never flat fills.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Windsor Chair — Field Plate V2R01", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#241308"

BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0E0806"}, {"offset": 1, "color": "#050302"}]}}
WALL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C89A66"}, {"offset": 0.38, "color": "#9A6A3C"},
    {"offset": 0.72, "color": "#57331C"}, {"offset": 1, "color": "#2A170E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "start": [0, 660], "end": [0, 880], "stops": [
    {"offset": 0, "color": "#43281A"}, {"offset": 1, "color": "#1A0E08"}]}}
WOOD = {"gradient": {"kind": "linear", "start": [330, 250], "end": [700, 780], "stops": [
    {"offset": 0, "color": "#B07844"}, {"offset": 0.35, "color": "#83512A"},
    {"offset": 0.75, "color": "#5A3319"}, {"offset": 1, "color": "#3A1E0F"}]}}
WOOD_LIGHT = {"gradient": {"kind": "linear", "start": [300, 240], "end": [720, 760], "stops": [
    {"offset": 0, "color": "#C98F52"}, {"offset": 0.45, "color": "#96602F"},
    {"offset": 1, "color": "#4C2A14"}]}}
SEAT_GRAD = {"gradient": {"kind": "linear", "start": [300, 292], "end": [700, 420], "stops": [
    {"offset": 0, "color": "#B67C46"}, {"offset": 0.35, "color": "#94603A"},
    {"offset": 0.72, "color": "#6C401F"}, {"offset": 1, "color": "#42250F"}]}}
DISH_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6A3E1E"}, {"offset": 0.5, "color": "#7A4A24"},
    {"offset": 0.82, "color": "#845027"}, {"offset": 1, "color": "#8A5628"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=WALL_GRAD, stroke="#331B0F", strokeWidth=6)
d.shape("ellipse", "Inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E6C39A", strokeWidth=3, opacity=16)

# light pool from the upper left, and plaster stains
d.shape("ellipse", "Light pool", x=110, y=60, width=480, height=440,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FFE0B0", "opacity": 0.75},
            {"offset": 1, "color": "#FFE0B0", "opacity": 0}]}}, stroke=NONE, opacity=60)
for i, (x, y, w, h, op) in enumerate([(200, 140, 210, 130, 12), (600, 110, 180, 100, 10),
                                      (690, 620, 240, 140, 16), (160, 630, 190, 120, 13)]):
    d.shape("ellipse", f"Plaster tone {i+1}", x=x, y=y, width=w, height=h,
            fill="#5E3A1E", opacity=op, stroke=NONE)

# floor
d.path("M149,690 C300,676 500,684 640,694 C720,700 800,700 851,690 "
       "L851,690 A420,420 0 0 1 149,690 Z", "Floor", fill=FLOOR_GRAD, opacity=90, stroke=NONE)
d.path("M170,690 C320,678 480,686 620,694 C700,699 790,698 838,690", "Floor edge",
       fill=NONE, stroke="#8A5730", strokeWidth=3, opacity=45, cap="round")

# --- chair geometry (local frame), drawn twice: shadow, then the chair ----------
S_ = 1.02
OX, OY = 292, 206


def mk(shift_x=0.0, shift_y=0.0, shear=0.0, squash=1.0):
    def T(x, y):
        return (OX + (x + shear * (560 - y)) * S_ + shift_x,
                OY + y * S_ * squash + shift_y)
    return T


T = mk()
SH = mk(shift_x=66, shift_y=-10, shear=0.26, squash=0.96)

SPINDLE_X = [96, 124, 152, 180, 208, 236, 264, 292, 320]
LEGS = [
    ((126, 360), (104, 420), (110, 498), (92, 590), 15),
    ((296, 356), (322, 416), (316, 496), (334, 594), 15),
    ((150, 342), (142, 418), (146, 484), (140, 550), 12),
    ((272, 340), (280, 416), (276, 482), (284, 546), 12),
]
STRETCHERS = [((100, 504), (146, 512)), ((280, 508), (328, 502)),
              ((146, 512), (280, 508))]

# shield-shaped seat rim, in the chair's local frame; +y is the front edge
SEAT_RIM = [(84, 332), (98, 308), (140, 296), (192, 292), (240, 294), (286, 300),
            (322, 310), (338, 334), (340, 358), (326, 378), (288, 392),
            (244, 400), (210, 402), (174, 400), (132, 392), (94, 378), (78, 356)]
SEAT_TILT = -4.5          # back edge a touch higher than the front
SEAT_CX, SEAT_CY = 210, 346


def hoop_y(x):
    return 40 + 0.00205 * (x - 210) ** 2


def seg(pts):
    return "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (tuple(sum(pts, ())))


def seat_pts(Tf, sx=1.0, sy=1.0, dy=0.0, dx=0.0):
    out = []
    rt = math.radians(SEAT_TILT)
    cs, sn = math.cos(rt), math.sin(rt)
    for x, y in SEAT_RIM:
        lx = (x - SEAT_CX) * sx + dx
        ly = (y - SEAT_CY) * sy + dy
        out.append(Tf(SEAT_CX + lx * cs - ly * sn, SEAT_CY + lx * sn + ly * cs))
    return out


def seat_path(Tf, sx=1.0, sy=1.0, dy=0.0, dx=0.0):
    pts = seat_pts(Tf, sx, sy, dy, dx)
    n = len(pts)
    mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2)
            for i in range(n)]
    dd = "M%.1f,%.1f " % mids[-1]
    for i in range(n):
        dd += "Q%.1f,%.1f %.1f,%.1f " % (pts[i][0], pts[i][1], mids[i][0], mids[i][1])
    return dd + "Z"


def draw_chair(Tf, shadow=False):
    wall = "#3A2112"
    op = 20

    def stroke(dd, label, w, grad, cap="round"):
        if shadow:
            d.path(dd, label, fill=NONE, stroke=wall, strokeWidth=w, cap=cap, opacity=op)
        else:
            d.path(dd, label + " edge", fill=NONE, stroke=INK, strokeWidth=w + 2.4,
                   cap=cap, opacity=95)
            d.path(dd, label, fill=NONE, stroke=grad, strokeWidth=w, cap=cap)

    if shadow:
        ex, ey = Tf(210, 596)
        d.shape("ellipse", "Floor shadow", x=ex - 176, y=ey - 26, width=352, height=52,
                fill={"gradient": {"kind": "radial", "stops": [
                    {"offset": 0, "color": "#120804", "opacity": 0.55},
                    {"offset": 1, "color": "#120804", "opacity": 0}]}}, stroke=NONE, opacity=90)

    # back legs
    for i in (2, 3):
        top, knee, ank, bot, w = LEGS[i]
        stroke(seg([Tf(*top), Tf(*knee), Tf(*ank), Tf(*bot)]), f"Back leg {i+1}", w * S_, WOOD_LIGHT)

    # stretchers
    for i, (a, b) in enumerate(STRETCHERS):
        p0, p1 = Tf(*a), Tf(*b)
        stroke("M%.1f,%.1f L%.1f,%.1f" % (p0 + p1), f"Stretcher {i+1}", 7 * S_, WOOD)

    # hoop back
    hoop = ("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f "
            "C%.1f,%.1f %.1f,%.1f %.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
                *Tf(78, 348),
                *Tf(56, 250), *Tf(62, 156), *Tf(92, 98),
                *Tf(112, 60), *Tf(152, 40), *Tf(210, 38),
                *Tf(268, 40), *Tf(308, 60), *Tf(328, 98),
                *Tf(358, 156), *Tf(364, 250), *Tf(342, 348)))
    stroke(hoop, "Hoop back", 17 * S_, WOOD_LIGHT)

    # spindles, splayed from the seat deck up into the hoop
    for i, x in enumerate(SPINDLE_X):
        lean = (x - 210) * 0.05
        p0, p1 = Tf(x + lean, 336), Tf(x, hoop_y(x) + 12)
        dd = "M%.1f,%.1f L%.1f,%.1f" % (p0 + p1)
        stroke(dd, f"Spindle {i+1}", 7.6 * S_, WOOD_LIGHT if i % 4 else WOOD)
        if not shadow:
            mid_y = p0[1] + (p1[1] - p0[1]) * 0.42
            d.shape("ellipse", f"Spindle knuckle {i+1}", x=p0[0] - 6.2, y=mid_y - 5.6,
                    width=12.4, height=11.2, fill="#7C4A26", stroke=NONE)

    # legs before the seat, so the plank caps them
    for i in range(4):
        top, knee, ank, bot, w = LEGS[i]
        stroke(seg([Tf(*top), Tf(*knee), Tf(*ank), Tf(*bot)]), f"Leg {i+1}", w * S_, WOOD_LIGHT)
        if not shadow:
            px, py = Tf(knee[0] + (ank[0] - knee[0]) * 0.62, knee[1] + (ank[1] - knee[1]) * 0.62)
            d.shape("ellipse", f"Leg bead {i+1}", x=px - 7.6, y=py - 6.8,
                    width=15.2, height=13.6, fill="#9A6438", stroke=NONE, opacity=90)

    # --- seat: a plank seen almost edge-on, dished toward the back -------------
    # the top face is foreshortened hard, so the front face of the board shows
    # as a band and the seat reads as something you could sit on, not a disc
    SEAT_SY = 0.80
    FACE_GRAD = {"gradient": {"kind": "linear", "start": [0, 380], "end": [0, 440], "stops": [
        {"offset": 0, "color": "#8A5628"}, {"offset": 0.42, "color": "#4E2E17"},
        {"offset": 1, "color": "#2A160C"}]}}
    if shadow:
        d.path(seat_path(Tf, 1.0, SEAT_SY, 18), "Seat shadow", fill=wall, opacity=op, stroke=NONE)
    else:
        # front face: the same shield pushed down, only its lower half showing
        d.path(seat_path(Tf, 1.0, SEAT_SY, 18), "Seat front face", fill=FACE_GRAD, stroke=NONE)
        d.path(seat_path(Tf, 1.0, SEAT_SY, 0), "Seat board", fill=SEAT_GRAD, stroke=NONE)
        # outline only where the board turns away from the light
        rim = seat_pts(Tf, 1.0, SEAT_SY)
        d.path("M%.1f,%.1f " % rim[8] + " ".join("L%.1f,%.1f" % p for p in rim[8:16]),
               "Seat front outline", fill=NONE, stroke=INK, strokeWidth=3.0,
               opacity=90, cap="round")
        d.path("M%.1f,%.1f " % rim[3] + " ".join("L%.1f,%.1f" % p for p in rim[3:9]),
               "Seat back outline", fill=NONE, stroke=INK, strokeWidth=2.6,
               opacity=55, cap="round")
        # the dish: an oval inset flattened with the board, set behind centre
        d.path(seat_path(Tf, 0.90, SEAT_SY * 0.62, -8, -2), "Seat dish",
               fill=DISH_GRAD, stroke=NONE)
        # grain, lying with the board and kept to the front half so it reads as
        # figure in the elm rather than a set of ridges
        for j, k in enumerate((0.58, 0.72)):
            gp = seat_pts(Tf, 0.72 - j * 0.05, SEAT_SY * 0.40 - j * 0.03, -8 + k * 34)
            d.path("M%.1f,%.1f " % gp[2] + " ".join("L%.1f,%.1f" % p for p in gp[2:8]),
                   f"Seat grain {j+1}", fill=NONE, stroke="#2E1B0D", strokeWidth=2.4,
                   opacity=16, cap="round")

    # the seat throws a shadow down onto the legs it stands on
    if not shadow:
        cx, cy = Tf(210, 404)
        d.shape("ellipse", "Under-seat shade", x=cx - 118, y=cy + 8, width=236, height=54,
                fill={"gradient": {"kind": "radial", "stops": [
                    {"offset": 0, "color": "#170B05", "opacity": 0.5},
                    {"offset": 1, "color": "#170B05", "opacity": 0}]}}, stroke=NONE, opacity=70)


draw_chair(SH, shadow=True)
draw_chair(T, shadow=False)

# raking light on the chair's left edge
for i, (a, b, w) in enumerate([((80, 330), (94, 100), 4.4), ((328, 96), (356, 250), 3.0),
                               ((104, 356), (88, 586), 3.4)]):
    p0, p1 = T(*a), T(*b)
    d.path("M%.1f,%.1f L%.1f,%.1f" % (p0 + p1), f"Rim {i+1}", fill=NONE,
           stroke="#F6C48A", strokeWidth=w, opacity=40, cap="round")

# --- plate rim over everything ---------------------------------------------------
d.shape("ellipse", "Backdrop mask", x=-200, y=-240, width=1400, height=1400,
        fill=NONE, stroke=BG_GRAD, strokeWidth=560)

d.shape("ellipse", "Plate rim", x=80, y=40, width=840, height=840,
        fill=NONE, stroke="#331B0F", strokeWidth=6)
d.shape("ellipse", "Rim light", x=94, y=54, width=812, height=812,
        fill=NONE, stroke="#FFD9A0", strokeWidth=2.4, opacity=20)

d.text("WINDSOR CHAIR", "Name", x=500, y=944, size=50, font="Virelai Sans",
       color="#F6E0C2", justify="center")
d.text("ELM SEAT  ·  ASH SPINDLES", "Spec", x=500, y=976, size=21, font="Virelai Sans",
       color="#D8AF80", justify="center")

d.finish("windsor-chair-V2R01")
