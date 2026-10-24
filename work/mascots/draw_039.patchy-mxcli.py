#!/usr/bin/env python3
"""Patchy Mx.CLI — mascot portrait V1R00. Phantom footnote: a thermal-
printer entity stamping TODO: CLARIFY into finished documents, printed
disclaimers feeding from the slot in its chest. Manila-paper plate on a
deep plum-ink backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Patchy Mx.CLI — Mascot Plate", 1000, 1000)

INK = "#241C16"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#1B1522"}, {"offset": 1, "color": "#0A070E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7E7057"}, {"offset": 0.62, "color": "#57493A"},
    {"offset": 1, "color": "#2C241D"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [0, 290], "end": [0, 790], "stops": [
    {"offset": 0, "color": "#D8D0BE"}, {"offset": 0.55, "color": "#B0A696"},
    {"offset": 1, "color": "#7E7668"}]}}
PANEL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2A2620"}, {"offset": 1, "color": "#12100C"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2EDE0"}, {"offset": 1, "color": "#D4CBB4"}]}}
FEED_GRAD = {"gradient": {"kind": "linear", "start": [460, 540], "end": [620, 830], "stops": [
    {"offset": 0, "color": "#EFE8D6"}, {"offset": 1, "color": "#C9BFA6"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9C6C40"}, {"offset": 1, "color": "#5E3C22"}]}}
STAMP_RED = "#B03A2E"
AMBER = "#F2B84A"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#8A7A5A", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#18100C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C8A0", strokeWidth=3, opacity=28)
# archive patina + flecks
d.shape("ellipse", "Patina 1", x=190, y=350, width=230, height=150,
        fill="#4E4232", opacity=25, stroke=NONE)
d.shape("ellipse", "Patina 2", x=630, y=600, width=220, height=140,
        fill="#8A7858", opacity=15, stroke=NONE)
for i, (x, y, w) in enumerate([(220,330,5),(790,335,6),(185,555,5),(848,565,5),
                               (255,765,5),(735,760,6),(158,450,5),(855,445,5),
                               (435,125,5),(600,135,6),(330,155,4),(705,195,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#E4D6B4", opacity=30, stroke=NONE)
# ruled-line ghosts across the plate — a page that outgrew its margins
for j, yy in enumerate((240, 480, 700)):
    d.path(f"M170,{yy} L830,{yy}", f"Ruled ghost {j+1}",
           fill=NONE, stroke="#E4D6B4", strokeWidth=1, opacity=5)
# ghost arcs on the dark backdrop
d.path("M932,148 A108,108 0 0 0 838,58", "Ghost arc TR",
       fill=NONE, stroke="#6A5A40", strokeWidth=14, opacity=10, cap="round")
d.path("M72,768 A122,122 0 0 0 182,878", "Ghost arc BL",
       fill=NONE, stroke="#6A5A40", strokeWidth=10, opacity=8, cap="round")

# --- the finished document, already stamped -----------------------------------------
dx0, dy0 = 268, 445   # doc center, tilted -6 deg
d.path(rot_rect_path(dx0 + 6, dy0 + 8, 190, 250, -6), "Doc shadow",
       fill="#000000", opacity=35, stroke=NONE)
d.path(rot_rect_path(dx0, dy0, 190, 250, -6), "Finished doc",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=4)
# folded top-right corner
d.path("M330,334 L348,356 L322,360 Z", "Doc fold",
       fill="#D4CBB4", stroke=INK, strokeWidth=2.5)
# neat finished lines
for i in range(8):
    w = 120 if i % 3 else 140
    d.path(rot_rect_path(dx0 - 12 + (140 - w) / 2 * 0, dy0 - 88 + i * 22, w, 5, -6),
           f"Doc line {i+1}", fill="#8A8272", opacity=70, stroke=NONE)
# title bar on the doc
d.path(rot_rect_path(dx0 - 10, dy0 - 102, 150, 9, -6), "Doc title",
       fill="#5A5344", opacity=80, stroke=NONE)
# signature squiggle, bottom
d.path("M212,558 C222,549 230,565 240,557 C248,551 254,563 262,557",
       "Doc signature", fill=NONE, stroke="#4A5A7A", strokeWidth=2.5,
       opacity=80, cap="round")
# the red verdict, stamped twice — compulsive
d.path(rot_rect_path(252, 412, 168, 40, -14), "Stamp frame 1",
       fill=NONE, stroke=STAMP_RED, strokeWidth=3.5, opacity=80)
r = d.text("TODO: CLARIFY", "Stamp text 1", x=252, y=420, size=15,
           font="Virelai Sans", color=STAMP_RED, justify="center")
if r and r.get("id"):
    d.cmd("object.rotate", "stamp tilt 1", ids=[r["id"]], angle=-14,
          origin=[252, 412])
d.path(rot_rect_path(252, 524, 168, 40, -11), "Stamp frame 2",
       fill=NONE, stroke=STAMP_RED, strokeWidth=3, opacity=28)
r = d.text("TODO: CLARIFY", "Stamp text 2", x=252, y=531, size=15,
           font="Virelai Sans", color=STAMP_RED, justify="center")
if r and r.get("id"):
    d.cmd("object.rotate", "stamp tilt 2", ids=[r["id"]], angle=-11,
          origin=[252, 524])
    d.cmd("object.setProps", "ghost stamp fade", ids=[r["id"]], opacity=28)

# --- phantom footnote asterisk, hovering by its head -----------------------------------
ax, ay = 398, 218
d.shape("ellipse", "Footnote aura", x=ax - 18, y=ay - 18, width=56, height=56,
        fill="#E4D6B4", opacity=12, stroke=NONE)
for deg in (90, 30, 150):
    t = math.radians(deg)
    x2, y2 = ax + 15 * math.cos(t), ay + 15 * math.sin(t)
    x1, y1 = ax - 15 * math.cos(t), ay - 15 * math.sin(t)
    d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}", f"Asterisk {deg}",
           fill=NONE, stroke="#E4D6B4", strokeWidth=4, opacity=75, cap="round")

# --- floating scraps of YAML debris, upper right ----------------------------------------
for i, (sx, sy, ww, hh, deg) in enumerate([(700, 210, 64, 44, 14),
                                           (768, 285, 56, 40, -10),
                                           (672, 320, 48, 36, 6)]):
    d.path(rot_rect_path(sx, sy, ww, hh, deg), f"YAML scrap {i+1}",
           fill=PAPER_GRAD, stroke=INK, strokeWidth=2.5, opacity=95)
for i, (x1, y1, x2, y2) in enumerate([(686, 206, 712, 206), (688, 216, 706, 216),
                                      (754, 282, 782, 282), (756, 292, 774, 292),
                                      (660, 318, 686, 318)]):
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Scrap mark {i+1}",
           fill=NONE, stroke="#8A8272", strokeWidth=3, opacity=70, cap="round")
# the triple dash of frontmatter on the top scrap
for i in range(3):
    d.path(f"M{690 + i * 10},228 L{694 + i * 10},228", f"YAML dash {i+1}",
           fill=NONE, stroke="#5A5344", strokeWidth=3.5, cap="round")

# --- Patchy -----------------------------------------------------------------------------
# feet
d.path(rot_rect_path(468, 788, 56, 26, 0), "Foot L",
       fill="#6A6256", stroke=INK, strokeWidth=4)
d.path(rot_rect_path(568, 788, 56, 26, 0), "Foot R",
       fill="#6A6256", stroke=INK, strokeWidth=4)
# torso: the printer body
d.shape("rectangle", "Torso", x=424, y=440, width=200, height=350,
        radius=26, fill=BODY_GRAD, stroke=INK, strokeWidth=5)
# torso panel seams + bolts
d.path("M436,660 L612,660", "Torso seam",
       fill=NONE, stroke="#6A6256", strokeWidth=3, opacity=55)
for i, (bx, by) in enumerate([(440, 456), (608, 456), (440, 772), (608, 772)]):
    d.shape("ellipse", f"Bolt {i+1}", x=bx, y=by, width=9, height=9,
            fill="#8A8072", stroke=INK, strokeWidth=1.5)
# chest slot — the disclaimer feed
d.shape("rectangle", "Chest slot", x=452, y=514, width=144, height=26,
        radius=10, fill=PANEL_GRAD, stroke=INK, strokeWidth=4)
d.path("M462,527 L586,527", "Slot glow",
       fill=NONE, stroke=AMBER, strokeWidth=3, opacity=45, cap="round")
# the disclaimer strip, feeding down and curling right
d.path("M476,540 C470,600 486,650 522,690 C556,728 566,760 548,806 "
       "L596,806 C616,752 600,706 566,666 C534,630 524,590 528,540 Z",
       "Disclaimer feed", fill=FEED_GRAD, stroke=INK, strokeWidth=3.5)
# printed micro-lines on the strip
for i, (y, x1, x2) in enumerate([(570, 482, 524), (600, 488, 528), (632, 500, 534),
                                 (668, 516, 548), (704, 540, 560), (742, 552, 566)]):
    d.path(f"M{x1},{y} L{x2},{y}", f"Feed line {i+1}",
           fill=NONE, stroke="#8A8272", strokeWidth=3, opacity=60, cap="round")
# tiny checkbox squares down the strip
for i, (x, y) in enumerate([(492, 586), (504, 618), (522, 652), (540, 690), (556, 728)]):
    d.shape("rectangle", f"Feed box {i+1}", x=x, y=y, width=7, height=7,
            fill=NONE, stroke="#6A6256", strokeWidth=1.5, opacity=70)
# head unit
d.shape("rectangle", "Head", x=442, y=296, width=164, height=150,
        radius=20, fill=BODY_GRAD, stroke=INK, strokeWidth=5)
# mini page feeding out of the head's top slot
d.shape("rectangle", "Head slot", x=486, y=292, width=76, height=12,
        radius=5, fill=PANEL_GRAD, stroke=INK, strokeWidth=3)
d.path(rot_rect_path(524, 262, 54, 46, -4), "Head page",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=3)
for i, ww in enumerate((34, 28, 36)):
    d.path(rot_rect_path(524, 252 + i * 9, ww, 4, -4), f"Head page line {i+1}",
           fill="#8A8272", opacity=70, stroke=NONE)
# face panel: dark screen, amber eyes
d.shape("rectangle", "Face panel", x=462, y=336, width=124, height=76,
        radius=10, fill=PANEL_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Eye glow L", x=486, y=360, width=26, height=26,
        fill=AMBER, opacity=28, stroke=NONE)
d.shape("ellipse", "Eye glow R", x=536, y=360, width=26, height=26,
        fill=AMBER, opacity=28, stroke=NONE)
d.shape("ellipse", "Eye L", x=492, y=366, width=14, height=14,
        fill=AMBER, stroke="#8A5C14", strokeWidth=1.5)
d.shape("ellipse", "Eye R", x=542, y=366, width=14, height=14,
        fill=AMBER, stroke="#8A5C14", strokeWidth=1.5)
# status LEDs under the face
d.shape("ellipse", "LED 1", x=560, y=424, width=8, height=8,
        fill="#4AC85A", stroke="#1E5E28", strokeWidth=1.5)
d.shape("ellipse", "LED 2", x=574, y=424, width=8, height=8,
        fill=AMBER, stroke="#8A5C14", strokeWidth=1.5)
# left arm reaching left, pressing the stamp down onto the doc
d.path("M424,500 C390,492 360,486 342,478 C334,464 338,450 350,444 "
       "C374,448 404,458 428,470 Z",
       "Arm L", fill=BODY_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Elbow joint", x=392, y=468, width=26, height=26,
        fill="#8A8072", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Hand L", x=312, y=452, width=38, height=34,
        fill="#9A9082", stroke=INK, strokeWidth=3.5)
# the rubber stamp in its grip: wood dome, neck, red base on the doc
d.path("M306,484 L306,464 C306,440 348,440 348,464 L348,484 Z",
       "Stamp handle", fill=WOOD_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Stamp knob", x=318, y=432, width=18, height=16,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=3)
d.path(rot_rect_path(327, 494, 64, 18, -8), "Stamp rubber",
       fill=STAMP_RED, stroke=INK, strokeWidth=3)
# right arm down, holding the next stack of finished documents
d.path("M624,560 C656,600 668,650 664,700 C650,712 632,710 624,698 "
       "C624,650 620,606 614,574 Z",
       "Arm R", fill=BODY_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=634, y=688, width=38, height=34,
        fill="#9A9082", stroke=INK, strokeWidth=3.5)
# the waiting stack, fanned in its hand
for i, deg in enumerate((8, 0, -8)):
    d.path(rot_rect_path(668, 742 - i * 6, 96, 60, deg), f"Stack sheet {i+1}",
           fill=PAPER_GRAD, stroke=INK, strokeWidth=2.5)
for i in range(3):
    d.path(rot_rect_path(668, 728 - i * 0, 60, 4, 8), f"Stack line {i+1}",
           fill="#8A8272", opacity=65, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("PATCHY MX.CLI", "Name", x=500, y=930, size=56, font="Virelai Sans",
       color="#E4D6B8", justify="center")
r = d.text("PHANTOM FOOTNOTE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B89A6A", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=230)

d.finish("039.patchy-mxcli-V1R00")
