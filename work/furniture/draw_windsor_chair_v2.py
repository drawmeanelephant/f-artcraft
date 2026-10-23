#!/usr/bin/env python3
"""Windsor chair — field plate V2R00, a rendition of V1R00.

V1 was pale maple, lit flatly, floating on a dark ground. This take puts the
chair in a room at low sun: dark walnut against a warm plaster disc, the light
raking in from the left, and the chair's own shadow thrown up the wall behind
it — hoop, spindles and legs all read in the shadow. Near-front view, slightly
above, so the saddle of the seat shows.
1000x1000. House style: gradients + translucent shading, never flat fills.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Windsor Chair — Field Plate V2", 1000, 1000)

CX, CY, R = 500, 460, 420
INK = "#241308"


def rim_y(x):
    return CY + math.sqrt(max(R * R - (x - CX) ** 2, 0))


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
SEAT_GRAD = {"gradient": {"kind": "linear", "start": [330, 500], "end": [690, 610], "stops": [
    {"offset": 0, "color": "#9A6432"}, {"offset": 0.5, "color": "#78461F"},
    {"offset": 1, "color": "#43240F"}]}}
SCOOP_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6A3E1E"}, {"offset": 0.75, "color": "#7E4A22"},
    {"offset": 1, "color": "#9A5E2C"}]}}

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
SEAT_RX, SEAT_RY, SEAT_CY = 152, 50, 342
LEGS = [
    ((126, 360), (104, 420), (110, 498), (92, 590), 15),
    ((296, 356), (322, 416), (316, 496), (334, 594), 15),
    ((150, 342), (142, 418), (146, 484), (140, 550), 12),
    ((272, 340), (280, 416), (276, 482), (284, 546), 12),
]
STRETCHERS = [((100, 504), (146, 512)), ((280, 508), (328, 502)),
              ((146, 512), (280, 508))]


def hoop_y(x):
    return 40 + 0.00205 * (x - 210) ** 2


def seg(pts):
    return "M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (tuple(sum(pts, ())))


def draw_chair(Tf, shadow=False):
    wall = "#3A2112" if shadow else None
    op = 17 if shadow else 100

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

    # spindles
    for i, x in enumerate(SPINDLE_X):
        lean = (x - 210) * 0.05
        p0, p1 = Tf(x + lean, 330), Tf(x, hoop_y(x) + 12)
        dd = "M%.1f,%.1f L%.1f,%.1f" % (p0 + p1)
        stroke(dd, f"Spindle {i+1}", 7.6 * S_, WOOD_LIGHT if i % 4 else WOOD)
        if not shadow:
            mx, my = (p0[0] + p1[0]) / 2, p0[1] + (p1[1] - p0[1]) * 0.45
            d.shape("ellipse", f"Spindle knuckle {i+1}", x=mx - 5.8, y=my - 5.2,
                    width=11.6, height=10.4, fill="#7C4A26", stroke=NONE)

    # front legs
    for i in (0, 1):
        top, knee, ank, bot, w = LEGS[i]
        stroke(seg([Tf(*top), Tf(*knee), Tf(*ank), Tf(*bot)]), f"Front leg {i+1}", w * S_, WOOD_LIGHT)
        if not shadow:
            for j, k in enumerate((0.62,)):
                bx = knee[0] + (ank[0] - knee[0]) * k
                by = knee[1] + (ank[1] - knee[1]) * k
                px, py = Tf(bx, by)
                d.shape("ellipse", f"Leg bead {i+1}-{j+1}", x=px - 7.6, y=py - 6.8,
                        width=15.2, height=13.6, fill="#9A6438", stroke=NONE, opacity=90)


    # seat: a shield-shaped saddle, thicker at the back, dipped in the middle
    def seat_pts(sx=1.0, sy=1.0, dy=0.0):
        P = [(82, 328), (104, 308), (154, 300), (210, 298), (266, 300), (316, 308),
             (338, 328), (344, 352), (334, 374), (302, 390), (258, 400), (210, 402),
             (162, 400), (118, 390), (86, 374), (76, 352)]
        out = []
        rt = math.radians(-4.5)
        cs, sn = math.cos(rt), math.sin(rt)
        for x, y in P:
            dx, dy_ = (x - 210) * sx, (y - 342) * sy + dy
            out.append(Tf(210 + dx * cs - dy_ * sn, 342 + dx * sn + dy_ * cs))
        return out

    def seat_path(sx=1.0, sy=1.0, dy=0.0):
        pts = seat_pts(sx, sy, dy)
        n = len(pts)
        mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2)
                for i in range(n)]
        dd = "M%.1f,%.1f " % mids[-1]
        for i in range(n):
            dd += "Q%.1f,%.1f %.1f,%.1f " % (pts[i][0], pts[i][1], mids[i][0], mids[i][1])
        return dd + "Z"

    if shadow:
        d.path(seat_path(), "Seat shadow", fill=wall, opacity=op, stroke=NONE)
    else:
        d.path(seat_path(dy=15), "Seat thickness", fill="#1E0F07", stroke=NONE)
        d.path(seat_path(), "Seat rim", fill="#4A2915", stroke=INK, strokeWidth=3.6)
        d.path(seat_path(0.86, 0.76, -2), "Seat surface", fill=SEAT_GRAD, stroke=NONE)
        d.path(seat_path(0.6, 0.46, 4), "Seat dish", fill={"gradient": {"kind": "linear",
               "start": [0, 520], "end": [0, 590], "stops": [
                   {"offset": 0, "color": "#2E1A0C"}, {"offset": 1, "color": "#5A3418"}]}},
               stroke=NONE, opacity=88)
        d.path(seat_path(0.86, 0.76, -2), "Seat surface edge", fill=NONE, stroke="#2A160C",
               strokeWidth=2.4, opacity=55)
        # light along the lit left rim only
        fx, fy = Tf(210, 380)
        d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
            fx - 132, fy - 34, *Tf(110, 356), *Tf(150, 392), fx - 30, fy + 12),
            "Seat rim light", fill=NONE, stroke="#D6A26A", strokeWidth=4.6, opacity=45, cap="round")

    # front legs
    for i in (0, 1):
        top, knee, ank, bot, w = LEGS[i]
        stroke(seg([Tf(*top), Tf(*knee), Tf(*ank), Tf(*bot)]), f"Front leg {i+1}", w * S_, WOOD_LIGHT)
        if not shadow:
            for j, k in enumerate((0.62,)):
                bx = knee[0] + (ank[0] - knee[0]) * k
                by = knee[1] + (ank[1] - knee[1]) * k
                px, py = Tf(bx, by)
                d.shape("ellipse", f"Leg bead {i+1}-{j+1}", x=px - 7.6, y=py - 6.8,
                        width=15.2, height=13.6, fill="#9A6438", stroke=NONE, opacity=90)


    # seat: a shield-shaped saddle, thicker at the back, dipped in the middle
    def seat_pts(sx=1.0, sy=1.0, dy=0.0):
        P = [(82, 328), (104, 308), (154, 300), (210, 298), (266, 300), (316, 308),
             (338, 328), (344, 352), (334, 374), (302, 390), (258, 400), (210, 402),
             (162, 400), (118, 390), (86, 374), (76, 352)]
        out = []
        rt = math.radians(-4.5)
        cs, sn = math.cos(rt), math.sin(rt)
        for x, y in P:
            dx, dy_ = (x - 210) * sx, (y - 342) * sy + dy
            out.append(Tf(210 + dx * cs - dy_ * sn, 342 + dx * sn + dy_ * cs))
        return out

    def seat_path(sx=1.0, sy=1.0, dy=0.0):
        pts = seat_pts(sx, sy, dy)
        n = len(pts)
        mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2)
                for i in range(n)]
        dd = "M%.1f,%.1f " % mids[-1]
        for i in range(n):
            dd += "Q%.1f,%.1f %.1f,%.1f " % (pts[i][0], pts[i][1], mids[i][0], mids[i][1])
        return dd + "Z"

    if shadow:
        d.path(seat_path(), "Seat shadow", fill=wall, opacity=op, stroke=NONE)
    else:
        d.path(seat_path(dy=13), "Seat thickness", fill="#2A160C", stroke=NONE)
        d.path(seat_path(), "Seat", fill=SEAT_GRAD, stroke=NONE)
        # dip where the back meets the seat
        bx, by = Tf(210, 320)
        d.shape("ellipse", "Saddle dip", x=bx - 142, y=by - 26, width=284, height=52,
                fill={"gradient": {"kind": "radial", "stops": [
                    {"offset": 0, "color": "#40230F", "opacity": 0.75},
                    {"offset": 1, "color": "#40230F", "opacity": 0}]}}, stroke=NONE, opacity=70)
        d.path(seat_path(dy=13), "Seat under-shadow", fill=NONE, stroke="#1C0D06",
               strokeWidth=7, opacity=40)
        d.path(seat_path(), "Seat outline", fill=NONE, stroke=INK, strokeWidth=3.4)
        # front lip: the edge of the saddle catching the light
        fx, fy = Tf(210, 394)
        d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
            fx - 128, fy - 12, *Tf(120, 398), *Tf(210, 408), fx + 6, fy - 2),
            "Seat lip light", fill=NONE, stroke="#E8B87C", strokeWidth=5, opacity=38, cap="round")
        d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
            fx - 118, fy + 7, *Tf(160, 410), *Tf(260, 410), fx + 118, fy + 7),
            "Seat lip shadow", fill=NONE, stroke="#2A160C", strokeWidth=5, opacity=45, cap="round")
    # front legs
    for i in (0, 1):
        top, knee, ank, bot, w = LEGS[i]
        stroke(seg([Tf(*top), Tf(*knee), Tf(*ank), Tf(*bot)]), f"Front leg {i+1}", w * S_, WOOD_LIGHT)
        if not shadow:
            for j, k in enumerate((0.62,)):
                bx = knee[0] + (ank[0] - knee[0]) * k
                by = knee[1] + (ank[1] - knee[1]) * k
                px, py = Tf(bx, by)
                d.shape("ellipse", f"Leg bead {i+1}-{j+1}", x=px - 7.6, y=py - 6.8,
                        width=15.2, height=13.6, fill="#9A6438", stroke=NONE, opacity=90)


    # seat: a shield-shaped saddle, thicker at the back, dipped in the middle
    def seat_pts(sx=1.0, sy=1.0, dy=0.0):
        P = [(82, 328), (104, 308), (154, 300), (210, 298), (266, 300), (316, 308),
             (338, 328), (344, 352), (334, 374), (302, 390), (258, 400), (210, 402),
             (162, 400), (118, 390), (86, 374), (76, 352)]
        out = []
        rt = math.radians(-4.5)
        cs, sn = math.cos(rt), math.sin(rt)
        for x, y in P:
            dx, dy_ = (x - 210) * sx, (y - 342) * sy + dy
            out.append(Tf(210 + dx * cs - dy_ * sn, 342 + dx * sn + dy_ * cs))
        return out

    def seat_path(sx=1.0, sy=1.0, dy=0.0):
        pts = seat_pts(sx, sy, dy)
        n = len(pts)
        mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2)
                for i in range(n)]
        dd = "M%.1f,%.1f " % mids[-1]
        for i in range(n):
            dd += "Q%.1f,%.1f %.1f,%.1f " % (pts[i][0], pts[i][1], mids[i][0], mids[i][1])
        return dd + "Z"

    if shadow:
        d.path(seat_path(), "Seat shadow", fill=wall, opacity=op, stroke=NONE)
    else:
        d.path(seat_path(dy=13), "Seat thickness", fill="#2A160C", stroke=NONE)
        d.path(seat_path(), "Seat", fill=SEAT_GRAD, stroke=NONE)
        # dip where the back meets the seat
        bx, by = Tf(210, 320)
        d.shape("ellipse", "Saddle dip", x=bx - 142, y=by - 26, width=284, height=52,
                fill={"gradient": {"kind": "radial", "stops": [
                    {"offset": 0, "color": "#40230F", "opacity": 0.75},
                    {"offset": 1, "color": "#40230F", "opacity": 0}]}}, stroke=NONE, opacity=70)
        d.path(seat_path(dy=13), "Seat under-shadow", fill=NONE, stroke="#1C0D06",
               strokeWidth=7, opacity=40)
        d.path(seat_path(), "Seat outline", fill=NONE, stroke=INK, strokeWidth=3.4)
        # front lip: the edge of the saddle catching the light
        fx, fy = Tf(210, 394)
        d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
            fx - 128, fy - 12, *Tf(120, 398), *Tf(210, 408), fx + 6, fy - 2),
            "Seat lip light", fill=NONE, stroke="#E8B87C", strokeWidth=5, opacity=38, cap="round")
        d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
            fx - 118, fy + 7, *Tf(160, 410), *Tf(260, 410), fx + 118, fy + 7),
            "Seat lip shadow", fill=NONE, stroke="#2A160C", strokeWidth=5, opacity=45, cap="round")
        for j, k in enumerate((0.30, 0.55, 0.78)):
            gy = by + 18 + k * 52
            d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
                bx - 128 + j * 8, gy, bx - 60, gy + 8, bx + 60, gy + 8, bx + 128 - j * 8, gy),
                f"Seat grain {j+1}", fill=NONE, stroke="#5A3117", strokeWidth=2.4,
                opacity=28, cap="round")

    # front legs
    for i in (0, 1):
        top, knee, ank, bot, w = LEGS[i]
        stroke(seg([Tf(*top), Tf(*knee), Tf(*ank), Tf(*bot)]), f"Front leg {i+1}", w * S_, WOOD_LIGHT)
        if not shadow:
            for j, k in enumerate((0.62,)):
                bx = knee[0] + (ank[0] - knee[0]) * k
                by = knee[1] + (ank[1] - knee[1]) * k
                px, py = Tf(bx, by)
                d.shape("ellipse", f"Leg bead {i+1}-{j+1}", x=px - 7.6, y=py - 6.8,
                        width=15.2, height=13.6, fill="#9A6438", stroke=NONE, opacity=90)


    # seat: a shield-shaped saddle, thicker at the back, dipped in the middle
    def seat_pts(sx=1.0, sy=1.0, dy=0.0):
        P = [(82, 328), (104, 308), (154, 300), (210, 298), (266, 300), (316, 308),
             (338, 328), (344, 352), (334, 374), (302, 390), (258, 400), (210, 402),
             (162, 400), (118, 390), (86, 374), (76, 352)]
        out = []
        rt = math.radians(-4.5)
        cs, sn = math.cos(rt), math.sin(rt)
        for x, y in P:
            dx, dy_ = (x - 210) * sx, (y - 342) * sy + dy
            out.append(Tf(210 + dx * cs - dy_ * sn, 342 + dx * sn + dy_ * cs))
        return out

    def seat_path(sx=1.0, sy=1.0, dy=0.0):
        pts = seat_pts(sx, sy, dy)
        n = len(pts)
        mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2)
                for i in range(n)]
        dd = "M%.1f,%.1f " % mids[-1]
        for i in range(n):
            dd += "Q%.1f,%.1f %.1f,%.1f " % (pts[i][0], pts[i][1], mids[i][0], mids[i][1])
        return dd + "Z"

    if shadow:
        d.path(seat_path(), "Seat shadow", fill=wall, opacity=op, stroke=NONE)
    else:
        d.path(seat_path(dy=14), "Seat thickness", fill="#2A160C", stroke=NONE)
        d.path(seat_path(), "Seat", fill=SEAT_GRAD, stroke=NONE)
        d.path(seat_path(0.98, 0.98), "Seat outline", fill=NONE, stroke=INK, strokeWidth=3.4)
        d.path(seat_path(0.84, 0.82, 2), "Seat rim band", fill="#7E4C24", stroke=NONE, opacity=95)
        d.path(seat_path(0.68, 0.64, 3), "Seat scoop", fill=SCOOP_GRAD, stroke=NONE)
        d.path(seat_path(0.54, 0.5, 5), "Scoop core", fill="#7C4820", stroke=NONE, opacity=55)
        d.path(seat_path(0.72, 0.7, 2), "Seat rim lip", fill=NONE, stroke="#C9955C",
               strokeWidth=2.6, opacity=45)
        cx_, cy_ = Tf(210, 386)
        d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
            cx_ - 96, cy_ - 6, *Tf(150, 392), *Tf(270, 392), cx_ + 96, cy_ - 6),
            "Seat front light", fill=NONE, stroke="#E8BC84", strokeWidth=4.6, opacity=38, cap="round")

    # front legs
    for i in (0, 1):
        top, knee, ank, bot, w = LEGS[i]
        stroke(seg([Tf(*top), Tf(*knee), Tf(*ank), Tf(*bot)]), f"Front leg {i+1}", w * S_, WOOD_LIGHT)
        if not shadow:
            for j, k in enumerate((0.62,)):
                bx = knee[0] + (ank[0] - knee[0]) * k
                by = knee[1] + (ank[1] - knee[1]) * k
                px, py = Tf(bx, by)
                d.shape("ellipse", f"Leg bead {i+1}-{j+1}", x=px - 7.6, y=py - 6.8,
                        width=15.2, height=13.6, fill="#9A6438", stroke=NONE, opacity=90)


    # seat
    cx, cy = Tf(210, SEAT_CY)
    rx, ry = SEAT_RX * S_, SEAT_RY * S_
    if shadow:
        d.shape("ellipse", "Seat shadow", x=cx - rx, y=cy - ry, width=2 * rx, height=2 * ry,
                fill=wall, opacity=op, stroke=NONE)
    else:
        d.shape("ellipse", "Seat outline", x=cx - rx, y=cy - ry, width=2 * rx, height=2 * ry,
                fill=INK, stroke=NONE)
        d.shape("ellipse", "Seat", x=cx - rx + 4, y=cy - ry + 3, width=2 * rx - 8, height=2 * ry - 7,
                fill=SEAT_GRAD, stroke=NONE)
        d.shape("ellipse", "Seat rim band", x=cx - rx * 0.9, y=cy - ry * 0.68,
                width=rx * 1.8, height=ry * 1.32, fill="#8A5628", stroke=NONE, opacity=95)
        d.shape("ellipse", "Seat scoop", x=cx - rx * 0.66, y=cy - ry * 0.44,
                width=rx * 1.32, height=ry * 0.9, fill=SCOOP_GRAD, stroke=NONE)
        d.shape("ellipse", "Scoop shade", x=cx - rx * 0.66, y=cy - ry * 0.36,
                width=rx * 1.32, height=ry * 0.62,
                fill={"gradient": {"kind": "linear", "start": [0, cy - ry * 0.36], "end": [0, cy + ry * 0.4], "stops": [
                    {"offset": 0, "color": "#5E3418", "opacity": 0.5},
                    {"offset": 1, "color": "#5E3418", "opacity": 0}]}}, stroke=NONE)
        # front rim catching the light, plus two grain lines
        d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
            cx - rx * 0.8, cy + ry * 0.52,
            *Tf(120, 396), *Tf(300, 396), cx + rx * 0.8, cy + ry * 0.52),
            "Seat rim light", fill=NONE, stroke="#E8B87C", strokeWidth=4, opacity=45, cap="round")
        for j, k in enumerate((0.22, 0.42, 0.62)):
            d.path("M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
                cx - rx * (0.8 - j * 0.05), cy + ry * k,
                *Tf(140 + j * 20, 340 + 30 * k), *Tf(280 - j * 20, 340 + 30 * k),
                cx + rx * (0.8 - j * 0.05), cy + ry * k),
                f"Seat grain {j+1}", fill=NONE, stroke="#3A2010", strokeWidth=2.6, opacity=35, cap="round")

draw_chair(SH, shadow=True)
draw_chair(T, shadow=False)

# raking light on the chair's left edge
for i, (a, b, w) in enumerate([((80, 330), (94, 100), 4.4), ((328, 96), (356, 250), 3.0),
                               ((104, 356), (88, 586), 3.4)]):
    p0, p1 = T(*a), T(*b)
    d.path("M%.1f,%.1f L%.1f,%.1f" % (p0 + p1), f"Rim {i+1}", fill=NONE,
           stroke="#F6C48A", strokeWidth=w, opacity=40, cap="round")

# --- plate rim over everything ---------------------------------------------------
# nothing may show outside the disc: repaint the backdrop over the ring,
# then the rim gets drawn back on top of it
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

d.finish("windsor-chair-V2R00")
