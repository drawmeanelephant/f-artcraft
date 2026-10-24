#!/usr/bin/env python3
"""Reboota Thrice — mascot portrait V1R00. Crisis Resolution Technician:
a coverall technician pressing and holding the big glowing power button
on a tower case, monitor behind mid-boot, case fans spinning, a SOLVED
ticket already pinned to the side. Warm steel plate on an indigo night
backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Reboota Thrice — Mascot Plate", 1000, 1000)

INK = "#201C16"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#0D1220"}, {"offset": 1, "color": "#050810"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6A7280"}, {"offset": 0.62, "color": "#40485A"},
    {"offset": 1, "color": "#1C222E"}]}}
SKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0C8A8"}, {"offset": 0.75, "color": "#D8A07A"},
    {"offset": 1, "color": "#B07C58"}]}}
HAIR_GRAD = {"gradient": {"kind": "linear", "start": [0, 300], "end": [0, 520], "stops": [
    {"offset": 0, "color": "#8A5632"}, {"offset": 1, "color": "#4A2E1A"}]}}
SUIT_GRAD = {"gradient": {"kind": "linear", "start": [0, 470], "end": [0, 810], "stops": [
    {"offset": 0, "color": "#4E6E9E"}, {"offset": 0.55, "color": "#33507A"},
    {"offset": 1, "color": "#1E3354"}]}}
CASE_GRAD = {"gradient": {"kind": "linear", "start": [0, 430], "end": [0, 800], "stops": [
    {"offset": 0, "color": "#484F5A"}, {"offset": 1, "color": "#22262E"}]}}
SCREEN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#14281A"}, {"offset": 1, "color": "#081209"}]}}
AMBER = "#F2B84A"
GREEN = "#4AD86A"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#5A7A9C", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#0C1218", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#B8C8D8", strokeWidth=3, opacity=28)
# shop-floor patina + flecks
d.shape("ellipse", "Patina 1", x=200, y=360, width=230, height=150,
        fill="#32405A", opacity=25, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=580, width=230, height=140,
        fill="#7A8494", opacity=14, stroke=NONE)
for i, (x, y, w) in enumerate([(215,335,5),(792,330,6),(188,558,5),(848,568,5),
                               (258,762,5),(738,758,6),(160,452,5),(852,448,5),
                               (432,125,5),(602,132,6),(332,152,4),(702,192,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8D4E0", opacity=30, stroke=NONE)
# power-button glow ambience behind the case
d.shape("ellipse", "Button ambience", x=560, y=420, width=300, height=240,
        fill=AMBER, opacity=8, stroke=NONE)
# ghost arcs on the dark backdrop
d.path("M932,148 A108,108 0 0 0 838,58", "Ghost arc TR",
       fill=NONE, stroke="#4A6A8A", strokeWidth=14, opacity=10, cap="round")
d.path("M72,768 A122,122 0 0 0 182,878", "Ghost arc BL",
       fill=NONE, stroke="#4A6A8A", strokeWidth=10, opacity=8, cap="round")

# --- the monitor, mid-boot, upper left -------------------------------------------------
mx, my = 292, 222
d.path(rot_rect_path(mx + 6, my + 8, 248, 158, -4), "Monitor shadow",
       fill="#000000", opacity=35, stroke=NONE)
d.path(rot_rect_path(mx, my, 248, 158, -4), "Monitor bezel",
       fill="#3A342C", stroke=INK, strokeWidth=4)
d.path(rot_rect_path(mx, my, 208, 118, -4), "Monitor glass",
       fill=SCREEN_GRAD, stroke=INK, strokeWidth=2.5)
# boot lines (strokes — no glyph risk), staggered like POST output
for i, (w, xx) in enumerate([(120, 214), (150, 208), (96, 218), (140, 210)]):
    d.path(rot_rect_path(xx + w / 2, 172 + i * 20, w, 5, -4),
           f"Boot line {i+1}", fill=GREEN, opacity=75, stroke=NONE)
# OS banner + progress bar
d.text("THRICEOS", "OS banner", x=300, y=262, size=15, font="Virelai Sans",
       color=GREEN, justify="center")
d.path(rot_rect_path(300, 282, 150, 14, -4), "Progress shell",
       fill=NONE, stroke=GREEN, strokeWidth=2.5, opacity=80)
for i in range(4):
    d.path(rot_rect_path(240 + i * 16, 282, 12, 8, -4), f"Progress seg {i+1}",
           fill=GREEN, opacity=85, stroke=NONE)
# a cursor blinking at the end of the bar
d.path(rot_rect_path(318, 282, 10, 8, -4), "Progress cursor",
       fill=GREEN, opacity=40, stroke=NONE)
# monitor stand neck + foot
d.path(rot_rect_path(mx, my + 92, 20, 34, -4), "Monitor neck",
       fill="#3A342C", stroke=INK, strokeWidth=3)
d.path(rot_rect_path(mx, my + 122, 96, 16, -4), "Monitor foot",
       fill="#3A342C", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Monitor LED", x=398, y=296, width=8, height=8,
        fill=AMBER, stroke="#8A5C14", strokeWidth=1.5)

# --- the tower case, right — fans spinning ----------------------------------------------
cx0, cy0, cw, ch = 668, 428, 152, 372
d.path(rot_rect_path(cx0 + 8, cy0 + ch / 2 + 6, cw, ch, 2), "Case shadow",
       fill="#000000", opacity=35, stroke=NONE)
d.path(rot_rect_path(cx0, cy0 + ch / 2, cw, ch, 2), "Case body",
       fill=CASE_GRAD, stroke=INK, strokeWidth=5)
# front edge highlight
d.path("M676,440 L684,796", "Case edge light",
       fill=NONE, stroke="#7A8494", strokeWidth=4, opacity=45, cap="round")

def fan(cy, label):
    fx = cx0 + 8
    d.shape("ellipse", f"{label} well", x=fx - 52, y=cy - 52, width=104,
            height=104, fill="#161A20", stroke=INK, strokeWidth=4)
    for k in range(4):
        t = math.radians(k * 90 + 30)
        bx, by = fx + 40 * math.cos(t), cy + 40 * math.sin(t)
        d.path(f"M{fx:.0f},{cy} Q{fx + 26*math.cos(t - 0.6):.0f},"
               f"{cy + 26*math.sin(t - 0.6):.0f} {bx:.0f},{by:.0f}",
               f"{label} blade {k+1}", fill=NONE, stroke="#5E6A78",
               strokeWidth=9, cap="round", opacity=85)
    d.shape("ellipse", f"{label} hub", x=fx - 12, y=cy - 12, width=24,
            height=24, fill="#3A4048", stroke=INK, strokeWidth=2.5)
    # spin arcs — motion, dashed
    d.path(f"M{fx - 62},{cy - 40} A74,74 0 0 1 {fx + 10},{cy - 73}",
           f"{label} spin 1", fill=NONE, stroke="#8A99AA",
           strokeWidth=4, opacity=35, cap="round", dash=[10, 12])
    d.path(f"M{fx + 62},{cy + 40} A74,74 0 0 1 {fx - 10},{cy + 73}",
           f"{label} spin 2", fill=NONE, stroke="#8A99AA",
           strokeWidth=4, opacity=35, cap="round", dash=[10, 12])

fan(548, "Fan A")
fan(688, "Fan B")

# the big power button she is holding down — top of the case
bx, by = 676, 470
d.shape("ellipse", "Button glow", x=bx - 44, y=by - 44, width=88, height=88,
        fill=AMBER, opacity=22, stroke=NONE)
d.shape("ellipse", "Button bezel", x=bx - 30, y=by - 30, width=60, height=60,
        fill="#161A20", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Button face", x=bx - 20, y=by - 20, width=40, height=40,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#FFDFA0"}, {"offset": 0.7, "color": "#E8A83C"},
            {"offset": 1, "color": "#B07218"}]}},
        stroke="#6A440E", strokeWidth=3)
# power glyph: broken ring + stem
d.path(f"M{bx - 9},{by - 6} A12,12 0 1 0 {bx + 9},{by - 6}",
       "Power ring", fill=NONE, stroke="#3A2A10", strokeWidth=4, cap="round")
d.path(f"M{bx},{by - 13} L{bx},{by + 1}", "Power stem",
       fill=NONE, stroke="#3A2A10", strokeWidth=4, cap="round")
# case vents low + LED strip
for i in range(3):
    d.path(f"M700,{768 - i * 14} L788,{764 - i * 14}", f"Case vent {i+1}",
           fill=NONE, stroke="#3A4048", strokeWidth=4, opacity=70, cap="round")
d.shape("ellipse", "Case LED", x=790, y=452, width=9, height=9,
        fill=GREEN, stroke="#1E5E28", strokeWidth=1.5)
d.shape("ellipse", "Case LED glow", x=786, y=448, width=17, height=17,
        fill=GREEN, opacity=30, stroke=NONE)
# the premature SOLVED ticket, dangling from her fingers — drawn after the
# body so it hangs in front of her hip
# (placed in the figure section below)
# power cord spilling onto the plate floor
d.path("M796,800 C770,824 720,826 690,816 C660,806 640,812 622,822",
       "Power cord", fill=NONE, stroke="#161A20", strokeWidth=6,
       cap="round", opacity=85)

# --- Reboota -----------------------------------------------------------------------------
# ponytail behind the head
d.path("M442,340 C400,350 384,392 392,434 C378,424 370,398 376,370 "
       "C384,334 412,314 442,316 Z",
       "Ponytail", fill=HAIR_GRAD, stroke=INK, strokeWidth=4)
# neck + coverall torso
d.path("M470,462 L470,506 L522,506 L522,458 C506,472 484,472 470,462 Z",
       "Neck", fill="#D8A07A", stroke=INK, strokeWidth=3)
d.path("M470,468 C488,480 506,480 522,468 L522,458 C506,472 484,472 470,462 Z",
       "Neck shade", fill="#8A5C3E", opacity=35, stroke=NONE)
# head
d.path("M496,316 C552,316 580,356 578,402 C576,448 544,478 496,478 "
       "C448,478 416,448 414,402 C412,356 440,316 496,316 Z",
       "Head", fill=SKIN_GRAD, stroke=INK, strokeWidth=4)
# hair cap over the crown, swept back into the ponytail
d.path("M414,380 C424,330 458,304 500,302 C548,300 578,334 580,382 "
       "C564,356 540,344 512,346 C518,360 512,372 500,376 "
       "C494,358 480,350 462,352 C464,366 456,376 444,380 "
       "C432,384 420,384 414,380 Z",
       "Hair cap", fill=HAIR_GRAD, stroke=INK, strokeWidth=3.5)
# face: confident, lightly mistaken
d.shape("ellipse", "Eye white L", x=444, y=398, width=38, height=24,
        fill="#F4EDE4", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Eye white R", x=510, y=398, width=38, height=24,
        fill="#F4EDE4", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pupil L", x=458, y=402, width=11, height=12,
        fill="#1E1812", stroke=NONE)
d.shape("ellipse", "Pupil R", x=524, y=402, width=11, height=12,
        fill="#1E1812", stroke=NONE)
d.shape("ellipse", "Glint L", x=456, y=400, width=4, height=4,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=522, y=400, width=4, height=4,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M440,384 C452,374 470,373 480,382", "Brow L",
       fill=NONE, stroke="#3A2416", strokeWidth=5, cap="round")
d.path("M508,380 C522,372 540,373 550,382", "Brow R",
       fill=NONE, stroke="#3A2416", strokeWidth=4, cap="round")
d.path("M496,408 C492,418 490,424 494,430", "Nose",
       fill=NONE, stroke="#A07050", strokeWidth=3, cap="round")
# confident grin
d.path("M466,444 C482,456 512,456 528,442 C522,460 476,462 466,444 Z",
       "Grin", fill="#7A3A34", stroke="#4A241E", strokeWidth=2)
# coverall body
d.path("M496,478 C560,478 592,522 602,592 C610,660 616,740 608,792 "
       "C550,812 444,812 388,792 C380,740 386,660 394,592 "
       "C404,522 432,478 496,478 Z",
       "Coverall", fill=SUIT_GRAD, stroke=INK, strokeWidth=5)
d.path("M560,516 C592,576 606,690 602,786 C582,798 558,804 534,806 "
       "C560,720 566,590 560,516 Z",
       "Suit shade", fill="#152542", opacity=45, stroke=NONE)
d.path("M390,758 C450,780 548,780 606,758 L608,792 C550,812 444,812 388,792 Z",
       "Suit hem shade", fill="#101E36", opacity=40, stroke=NONE)
# hi-vis stripe + zipper + name patch
d.path("M496,512 L500,780", "Zipper", fill=NONE, stroke="#16233C",
       strokeWidth=5)
d.path("M404,600 C440,614 552,614 592,600 L594,622 C554,638 438,638 402,622 Z",
       "Hi-vis stripe", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#F2C84A"}, {"offset": 1, "color": "#D8A024"}]}},
       stroke="#8A6A14", strokeWidth=2.5)
d.shape("rectangle", "Name patch", x=522, y=534, width=54, height=24,
        radius=4, fill="#E8E4DA", stroke=INK, strokeWidth=2.5)
d.text("x3", "Patch tally", x=549, y=551, size=13, font="Source Sans 3",
       color="#33507A", justify="center")
# left arm: hand on hip, elbow cocked — confidence
d.path("M394,560 C366,600 356,646 364,688 C376,698 392,694 398,682 "
       "C394,644 402,608 414,580 Z",
       "Arm L", fill=SUIT_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand on hip", x=368, y=672, width=34, height=30,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
# right arm extended, finger pressed on the power button
d.path("M596,520 C630,506 656,496 672,486 C682,494 684,508 676,518 "
       "C652,532 626,542 604,548 C594,540 590,530 596,520 Z",
       "Arm R", fill=SUIT_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=654, y=472, width=34, height=30,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=3.5)
# the pressing finger, sunk onto the glowing button
d.path("M676,478 L692,478 C698,478 700,486 696,490 L682,492 "
       "C676,492 674,484 676,478 Z",
       "Pressing finger", fill=SKIN_GRAD, stroke=INK, strokeWidth=2.5)
# finger-press contact shadow on the button
d.shape("ellipse", "Press shadow", x=664, y=470, width=22, height=16,
        fill="#8A5C14", opacity=40, stroke=NONE)
# the premature SOLVED ticket, dangling from her left hand
d.path(rot_rect_path(340, 745, 84, 52, 12), "Ticket",
       fill="#E8DCBC", stroke=INK, strokeWidth=3)
r = d.text("SOLVED", "Ticket text", x=340, y=757, size=14,
           font="Virelai Sans", color="#7A3A28", justify="center")
if r and r.get("id"):
    d.cmd("object.rotate", "ticket tilt", ids=[r["id"]], angle=12,
          origin=[340, 745])
t = d.text("(probably)", "Ticket aside", x=340, y=776, size=9,
           font="Source Sans 3", color="#7A6A50", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "ticket aside tilt", ids=[t["id"]], angle=12,
          origin=[340, 772])
d.shape("ellipse", "Ticket pin", x=352, y=712, width=12, height=12,
        fill=AMBER, stroke=INK, strokeWidth=2)
d.path("M384,702 L356,714", "Ticket tether",
       fill=NONE, stroke=INK, strokeWidth=2.5, cap="round")

# --- name + role ----------------------------------------------------------------------
d.text("REBOOTA THRICE", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#DCE4EE", justify="center")
r = d.text("CRISIS RESOLUTION TECHNICIAN", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A8B4C8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=170)

d.finish("041.reboota-thrice-V1R00")
