#!/usr/bin/env python3
"""Zhuzhing Ping — mascot portrait V1R00.
Minister of markup maximalism stamping REVIEWED FOREVER! with the
corrupted red pen he calls The Eternal, citation slip already filed,
decorative sparkles escalating everywhere. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Zhuzhing Ping — Mascot Portrait", 1000, 1000)

INK = "#2A1A24"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#17101E"}, {"offset": 1, "color": "#0B0710"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5C3466"}, {"offset": 0.7, "color": "#3C2348"},
    {"offset": 1, "color": "#20142C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#33233E"}, {"offset": 1, "color": "#16101E"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4E6D2"}, {"offset": 0.7, "color": "#DCBAA2"},
    {"offset": 1, "color": "#A87B68"}]}}
PEN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E03A4E"}, {"offset": 1, "color": "#9E1E32"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2E9D2"}, {"offset": 1, "color": "#D9CCA8"}]}}
RUFF_OUTER = "#EFE6F8"
RUFF_INNER = "#C9B4E4"
PEN_DARK = "#52101E"
STAMP = "#C43048"
PAPER = "#EFE4CC"
GOLD = "#EFC86E"
PINK = "#E8A2CC"
VIOLET = "#B28CE0"

def star4(cx, cy, s, label, **kw):
    r = s * 0.22
    d.path(f"M{cx},{cy-s} Q{cx+r},{cy-r} {cx+s},{cy} Q{cx+r},{cy+r} "
           f"{cx},{cy+s} Q{cx-r},{cy+r} {cx-s},{cy} Q{cx-r},{cy-r} "
           f"{cx},{cy-s} Z", label, **kw)

def ruff_path(cx, cy, rx, ry, n=18, k=0.8):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        f = 1.0 if i % 2 == 0 else k
        pts.append((cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A17EBE", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCC8EC", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(190,240,8),(802,234,7),(152,522,9),(842,540,8),
                               (254,768,7),(748,754,9),(130,392,6),(864,398,7),
                               (390,110,7),(618,112,8),(338,822,6),(664,824,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E3460", opacity=50, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#120C18",
       strokeWidth=4, opacity=70)

# --- lint warning chip: stylistic severity ----------------------------------------
d.shape("rectangle", "Lint chip", x=376, y=124, width=248, height=44,
        fill="#2E1E3A", stroke=GOLD, strokeWidth=2, radius=10, opacity=90)
d.text("STYLISTIC SEVERITY", "Lint label", x=500, y=152, size=13,
       font="Virelai Sans", color=GOLD, justify="center")
star4(398, 146, 11, "Chip star L", fill=GOLD, stroke=NONE)
star4(590, 146, 11, "Chip star R", fill=GOLD, stroke=NONE)

# --- citation slip, already filed -------------------------------------------------
d.path(rot_rect_path(268, 330, 150, 196, -8), "Citation slip",
       fill=PAPER_GRAD, stroke="#7E6E50", strokeWidth=3, join="round")
d.path(rot_rect_path(268, 236, 60, 18, -8), "Slip tape", fill="#C9B8E2",
       opacity=55, stroke=NONE)
t = d.text("CITATION", "Slip title", x=268, y=292, size=14,
           font="Virelai Sans", color="#6A5638", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "slip title tilt", ids=[t["id"]], angle=8,
          origin=[268, 292])
for i, (lx1, lx2, ly) in enumerate([(216, 322, 316), (222, 316, 338),
                                    (230, 310, 360)]):
    a = math.radians(-8); c, s = math.cos(a), math.sin(a)
    p1 = (268 + (lx1-268)*c - (ly-330)*s, 330 + (lx1-268)*s + (ly-330)*c)
    p2 = (268 + (lx2-268)*c - (ly-330)*s, 330 + (lx2-268)*s + (ly-330)*c)
    d.path(f"M{p1[0]:.0f},{p1[1]:.0f} L{p2[0]:.0f},{p2[1]:.0f}",
           f"Slip line {i+1}", fill=NONE, stroke="#9A8A68",
           strokeWidth=3, cap="round")
# the red circle-slash of the cited offense
d.shape("ellipse", "Cited mark", x=230, y=376, width=66, height=44,
        fill=NONE, stroke=STAMP, strokeWidth=4, opacity=85)
d.path("M242,406 L288,382", "Cited slash", fill=NONE, stroke=STAMP,
       strokeWidth=4, cap="round", opacity=85)

# --- stray page at right: markup maximalism in progress ----------------------------
d.path(rot_rect_path(742, 622, 176, 126, 6), "Stray page",
       fill=PAPER_GRAD, stroke="#7E6E50", strokeWidth=3, join="round")
for i, ly in enumerate([584, 606, 628]):
    d.path(rot_rect_path(742, ly, 128, 9, 6), f"Stray line {i+1}",
           fill="#B4A480", opacity=70, stroke=NONE)
d.path(rot_rect_path(742, 606, 148, 16, 6), "Strikethrough",
       fill=STAMP, opacity=70, stroke=NONE)
star4(788, 652, 12, "Stray doodle", fill=PINK, opacity=80, stroke=NONE)

# --- the page being stamped ---------------------------------------------------------
d.shape("ellipse", "Page shadow", x=320, y=792, width=240, height=20,
        fill="#08060C", opacity=50, stroke=NONE)
d.path(rot_rect_path(430, 722, 240, 150, -7), "Stamped page",
       fill=PAPER_GRAD, stroke="#7E6E50", strokeWidth=3, join="round")
# margins cited insufficiently bold — now they are legally thick
for i, m in enumerate([12, 22]):
    d.path(rot_rect_path(430 - 240/2 + m + 4, 722, m, 134, -7),
           f"Bold margin {i+1}", fill="#6A5638", opacity=80, stroke=NONE)
# text squiggles drowned under the stamp
for i, ly in enumerate([668, 686]):
    d.path(rot_rect_path(452, ly, 110, 7, -7), f"Page line {i+1}",
           fill="#B4A480", opacity=70, stroke=NONE)
# the impression: REVIEWED FOREVER! in corrupted red
d.path(rot_rect_path(452, 736, 176, 64, -7), "Stamp box", fill=STAMP,
       opacity=16, stroke=STAMP, strokeWidth=4)
t1 = d.text("REVIEWED", "Stamp line 1", x=452, y=730, size=17,
            font="Virelai Sans", color=STAMP, justify="center")
t2 = d.text("FOREVER!", "Stamp line 2", x=452, y=756, size=15,
            font="Virelai Sans", color=STAMP, justify="center")
for t_ in (t1, t2):
    if t_ and t_.get("id"):
        d.cmd("object.rotate", "stamp text tilt", ids=[t_["id"]], angle=7,
              origin=[452, 736])

# --- The Eternal: a corrupted red pen, mid-stamp ------------------------------------
d.path(rot_rect_path(460, 545, 46, 310, -6), "Pen barrel",
       fill=PEN_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path(rot_rect_path(447, 418, 52, 16, -6), "Pen cap band",
       fill=GOLD, stroke=INK, strokeWidth=3, join="round")
# the corruption: dark blotch, drips, glitch notch
d.shape("ellipse", "Pen rot", x=452, y=548, width=30, height=46,
        fill=PEN_DARK, opacity=75, stroke=NONE)
d.path("M460,584 C458,606 464,628 457,648 M470,586 C473,604 468,618 472,634",
       "Pen drips", fill=NONE, stroke=PEN_DARK, strokeWidth=5, cap="round",
       opacity=80)
d.path(rot_rect_path(478, 500, 12, 8, -6), "Glitch notch", fill=INK,
       opacity=80, stroke=NONE)
# fountain nib, still wet
d.path("M458,698 L494,695 L484,722 L477,731 L470,723 Z", "Pen nib",
       fill="#D8B060", stroke=INK, strokeWidth=3, join="round")
d.path("M477,704 L477,728", "Nib slit", fill=NONE, stroke=INK,
       strokeWidth=2)
d.shape("ellipse", "Nib bleed", x=468, y=726, width=20, height=10,
        fill=PEN_DARK, opacity=60, stroke=NONE)
# the impact: ink burst + sparkle concussion
d.shape("ellipse", "Stamp burst", x=416, y=714, width=120, height=34,
        fill=STAMP, opacity=30, stroke=NONE)
d.path("M430,690 L420,672 M476,688 L478,668 M522,696 L534,682",
       "Burst rays", fill=NONE, stroke=STAMP, strokeWidth=3, cap="round",
       opacity=70)
star4(404, 700, 12, "Impact star 1", fill=GOLD, stroke=NONE)
star4(546, 706, 10, "Impact star 2", fill=PINK, stroke=NONE)
for i, (x, y) in enumerate([(448, 744), (506, 750), (396, 728)]):
    d.shape("ellipse", f"Ink spot {i+1}", x=x, y=y, width=7, height=7,
            fill=PEN_DARK, opacity=70, stroke=NONE)

# --- Zhuzhing Ping: editorial pear in full ruff -------------------------------------
d.shape("ellipse", "Ping shadow", x=470, y=686, width=230, height=24,
        fill="#08060C", opacity=50, stroke=NONE)
# arm raised to the stamp — ink edge under flesh stroke
d.path("M512,548 C478,514 456,466 448,414", "Arm ink", fill=NONE,
       stroke=INK, strokeWidth=38, cap="round")
d.path("M512,548 C478,514 456,466 448,414", "Arm", fill=NONE,
       stroke="#DCBAA2", strokeWidth=28, cap="round")
# body
d.path("M580,430 C660,430 700,500 700,580 C700,660 650,700 580,700 "
       "C510,700 460,660 460,580 C460,500 500,430 580,430 Z",
       "Ping body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body hi", x=506, y=470, width=100, height=52,
        fill="#FFFFFF", opacity=14, stroke=NONE)
# the ruff: decorative escalation worn as formalwear
d.path(ruff_path(580, 624, 128, 58), "Ruff outer", fill=RUFF_OUTER,
       stroke=INK, strokeWidth=4, join="round", opacity=95)
d.path(ruff_path(580, 612, 92, 42), "Ruff inner", fill=RUFF_INNER,
       stroke=INK, strokeWidth=3, join="round", opacity=95)
# fist gripping the pen's crown
d.shape("ellipse", "Fist", x=420, y=378, width=66, height=58,
        fill="#DCBAA2", stroke=INK, strokeWidth=5)
for i in range(3):
    d.path(f"M{432+i*16},398 C{434+i*16},410 {444+i*16},410 {446+i*16},398",
           f"Knuckle {i+1}", fill=NONE, stroke=INK, strokeWidth=3,
           cap="round", opacity=70)
# other hand on hip — the posture of issued citations
d.path("M654,566 C676,590 682,616 672,640", "Hip arm ink", fill=NONE,
       stroke=INK, strokeWidth=34, cap="round")
d.path("M654,566 C676,590 682,616 672,640", "Hip arm", fill=NONE,
       stroke="#DCBAA2", strokeWidth=24, cap="round")
d.shape("ellipse", "Hip fist", x=654, y=620, width=44, height=36,
        fill="#DCBAA2", stroke=INK, strokeWidth=4)
# face: eyes down-left on the work, one brow arched in judgment
d.shape("ellipse", "Eye L", x=528, y=496, width=30, height=34,
        fill="#32202A", stroke=NONE)
d.shape("ellipse", "Eye R", x=610, y=496, width=30, height=34,
        fill="#32202A", stroke=NONE)
d.shape("ellipse", "Glint L", x=534, y=514, width=9, height=9,
        fill="#F4E6D2", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=616, y=514, width=9, height=9,
        fill="#F4E6D2", opacity=90, stroke=NONE)
d.path("M524,478 C532,468 550,466 560,474", "Brow L", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M608,470 C618,464 634,464 642,472", "Brow R", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round", opacity=80)
d.path("M562,556 C576,568 600,566 612,552", "Smirk", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.shape("ellipse", "Cheek L", x=512, y=544, width=26, height=13,
        fill="#D88A9E", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=634, y=544, width=26, height=13,
        fill="#D88A9E", opacity=45, stroke=NONE)
# feet nubs
d.shape("ellipse", "Foot L", x=520, y=690, width=40, height=18,
        fill="#A87B68", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Foot R", x=604, y=690, width=40, height=18,
        fill="#A87B68", stroke=INK, strokeWidth=3)

# --- the sparkles keep coming ---------------------------------------------------------
for i, (x, y, s, col) in enumerate([(246,182,26,GOLD),(330,196,13,PINK),
                                    (660,150,20,GOLD),(762,224,15,VIOLET),
                                    (712,330,12,PINK),(176,300,13,VIOLET),
                                    (238,470,15,GOLD),(826,432,17,PINK),
                                    (150,556,11,GOLD),(688,208,9,PINK)]):
    star4(x, y, s, f"Sparkle {i+1}", fill=col, opacity=85, stroke=NONE)
for i, (x, y) in enumerate([(286,150),(700,186),(196,388),(790,372),
                            (300,510),(850,540)]):
    d.shape("ellipse", f"Glint dot {i+1}", x=x, y=y, width=6, height=6,
            fill="#F0E2F4", opacity=60, stroke=NONE)

# --- captions ---------------------------------------------------------------------
d.text("ZHUZHING PING", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#F0E8F8", justify="center")
r = d.text("MINISTER OF MARKUP MAXIMALISM", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8A6DC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("057.zhuzhing-ping-V1R00")
