#!/usr/bin/env python3
"""Melody Errorflood — mascot portrait V1R00. Notification Maestro:
a bell-headed conductor auditioning notification pings on a punched
piano roll, a shrine of ISA sound cards standing behind her.
SoundBlaster-16 heritage: green PCBs, gold fingers, FM-synthesis pride.
Warm mahogany plate on a plum-night backdrop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Melody Errorflood — Mascot Plate", 1000, 1000)

INK = "#2A2018"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#1B0F14"}, {"offset": 1, "color": "#0A0508"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A5A60"}, {"offset": 0.62, "color": "#55343C"},
    {"offset": 1, "color": "#2A141C"}]}}
PCB_GRAD = {"gradient": {"kind": "linear", "start": [0, 180], "end": [0, 480], "stops": [
    {"offset": 0, "color": "#4A7A54"}, {"offset": 1, "color": "#2A4A34"}]}}
TUX_GRAD = {"gradient": {"kind": "linear", "start": [0, 470], "end": [0, 760], "stops": [
    {"offset": 0, "color": "#3A3244"}, {"offset": 0.55, "color": "#241E30"},
    {"offset": 1, "color": "#14101E"}]}}
BELL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F6D488"}, {"offset": 0.6, "color": "#DDAF4E"},
    {"offset": 1, "color": "#A97822"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "start": [0, 596], "end": [0, 664], "stops": [
    {"offset": 0, "color": "#EFE4C4"}, {"offset": 0.5, "color": "#DCCDA6"},
    {"offset": 1, "color": "#BFAD80"}]}}
PING_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFECB0"}, {"offset": 0.65, "color": "#F0BC4E"},
    {"offset": 1, "color": "#C8862A"}]}}
CRIMSON = "#C23A48"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#8A5A62", opacity=9, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1C1210", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E0C4B4", strokeWidth=3, opacity=30)
# warm concert glow where she conducts
d.shape("ellipse", "Stage glow", x=330, y=330, width=340, height=280,
        fill="#E8B86A", opacity=10, stroke=NONE)
# patina + flecks
d.shape("ellipse", "Patina 1", x=560, y=140, width=250, height=140,
        fill="#9A6A68", opacity=16, stroke=NONE)
d.shape("ellipse", "Patina 2", x=170, y=620, width=240, height=140,
        fill="#3E242E", opacity=22, stroke=NONE)
for i, (x, y, w) in enumerate([(212,344,5),(798,340,6),(178,548,5),(846,556,5),
                               (262,762,5),(728,768,6),(152,448,5),(858,628,5),
                               (432,124,5),(604,132,6),(338,158,4),(702,208,5),
                               (248,648,4),(672,716,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#EBD9C0", opacity=32, stroke=NONE)
# ghost arcs on the dark backdrop
d.path("M935,150 A105,105 0 0 0 845,60", "Ghost arc TR",
       fill=NONE, stroke="#5E3A44", strokeWidth=14, opacity=10, cap="round")
d.path("M75,770 A120,120 0 0 0 185,875", "Ghost arc BL",
       fill=NONE, stroke="#5E3A44", strokeWidth=10, opacity=8, cap="round")

# --- the shrine of ISA sound cards -------------------------------------------------
def isa_card(cx, cy, w, h, deg, label):
    """A sound card standing like a shrine tablet: green PCB, gold
    edge fingers at the foot, metal bracket strip, two jack circles."""
    d.path(rot_rect_path(cx, cy, w, h, deg), f"{label} PCB",
           fill=PCB_GRAD, stroke=INK, strokeWidth=4)
    # metal bracket along the card's left edge
    bx, by = cx - w / 2 + 12, cy - 6
    d.path(rot_rect_path(bx, by, 16, h - 24, deg), f"{label} bracket",
           fill={"gradient": {"kind": "linear", "stops": [
               {"offset": 0, "color": "#B8BEC6"}, {"offset": 1, "color": "#6E7680"}]}},
           stroke=INK, strokeWidth=2.5)
    # audio jacks on the bracket
    for j, oy in enumerate((-h / 4, 0)):
        d.shape("ellipse", f"{label} jack {j+1}", x=int(bx - 6), y=int(by + oy - 6),
                width=12, height=12, fill="#14181E", stroke=INK, strokeWidth=2)
    # chips
    for j, (ox, oy, cw, ch) in enumerate([(w * 0.12, -h * 0.18, w * 0.3, h * 0.14),
                                         (w * 0.08, h * 0.08, w * 0.24, h * 0.2),
                                         (w * 0.42, h * 0.05, w * 0.18, h * 0.12)]):
        d.path(rot_rect_path(cx + ox, cy + oy, cw, ch, deg), f"{label} chip {j+1}",
               fill="#16181E", stroke="#0A0C10", strokeWidth=2)
    # gold edge-connector fingers along the bottom edge
    for j in range(6):
        gx = cx - w * 0.18 + j * (w * 0.1)
        d.path(rot_rect_path(gx, cy + h / 2 - 7, w * 0.055, 14, deg),
               f"{label} finger {j+1}", fill="#D8AE4E", stroke=INK, strokeWidth=1.5)
    # faint circuit traces
    d.path(rot_rect_path(cx + w * 0.1, cy - h * 0.32, w * 0.55, 4, deg),
           f"{label} trace", fill="#8FB894", opacity=40, stroke=NONE)

isa_card(306, 322, 150, 240, -6, "Card L")
isa_card(694, 316, 150, 240, 6, "Card R")
isa_card(500, 292, 170, 264, 0, "Card C")
# candle-dot reverence between the cards
for i, (x, y) in enumerate([(402, 208), (598, 200), (500, 132)]):
    assert on_disc(x, y, 8), (x, y)
    d.shape("ellipse", f"Shrine votive {i+1}", x=x - 4, y=y - 4, width=8, height=8,
            fill="#F0C060", opacity=60, stroke=NONE)

# --- the maestro -------------------------------------------------------------------
# tails behind, then the body
d.path("M430,700 C408,728 400,756 406,780 C428,772 444,750 450,726 Z",
       "Tail L", fill=TUX_GRAD, stroke=INK, strokeWidth=4)
d.path("M570,700 C592,728 600,756 594,780 C572,772 556,750 550,726 Z",
       "Tail R", fill=TUX_GRAD, stroke=INK, strokeWidth=4)
d.path("M500,460 C566,460 606,512 612,590 C616,650 606,706 588,738 "
       "C548,758 452,758 412,738 C394,706 384,650 388,590 "
       "C394,512 434,460 500,460 Z",
       "Tux body", fill=TUX_GRAD, stroke=INK, strokeWidth=5)
# shirt front + buttons
d.path("M500,470 C528,470 546,492 548,530 L546,700 C524,714 476,714 454,700 "
       "L452,530 C454,492 472,470 500,470 Z",
       "Shirt front", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#F4EAD4"}, {"offset": 1, "color": "#D4C4A0"}]}},
       stroke=INK, strokeWidth=3)
for j, yy in enumerate((560, 610, 660)):
    d.shape("ellipse", f"Stud {j+1}", x=495, y=yy, width=10, height=10,
            fill="#2A2018", stroke=NONE)
# lapels
d.path("M452,530 L500,478 L500,560 C478,548 462,540 452,530 Z",
       "Lapel L", fill="#1A1624", stroke=INK, strokeWidth=3)
d.path("M548,530 L500,478 L500,560 C522,548 538,540 548,530 Z",
       "Lapel R", fill="#1A1624", stroke=INK, strokeWidth=3)
# crimson bowtie
d.path("M498,486 L468,470 C456,464 448,474 452,488 C456,500 466,504 476,498 L498,486 Z",
       "Bowtie L", fill=CRIMSON, stroke=INK, strokeWidth=2.5)
d.path("M502,486 L532,470 C544,464 552,474 548,488 C544,500 534,504 524,498 L502,486 Z",
       "Bowtie R", fill=CRIMSON, stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Bowtie knot", x=493, y=480, width=14, height=14,
        fill="#9E2E3A", stroke=INK, strokeWidth=2)
# left arm: open conducting palm
d.path("M414,540 C380,556 356,584 348,616 C356,630 374,632 386,622 "
       "C396,596 412,572 432,558 Z",
       "Sleeve L", fill=TUX_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Palm L", x=338, y=608, width=34, height=28,
        fill="#E8C8A8", stroke=INK, strokeWidth=3)
for j, dx in enumerate((0, 9, 18)):
    d.path(f"M{344 + dx},610 L{342 + dx},598", f"Finger {j+1}",
           fill=NONE, stroke=INK, strokeWidth=2.5, cap="round")
# right arm raised with the baton
d.path("M586,540 C616,510 640,478 654,446 C666,442 680,452 682,466 "
       "C664,506 636,540 606,562 C594,556 586,548 586,540 Z",
       "Sleeve R", fill=TUX_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=648, y=440, width=32, height=28,
        fill="#E8C8A8", stroke=INK, strokeWidth=3)
# baton: thin cream wand, tip catching the light
d.path("M664,448 L736,346", "Baton",
       fill=NONE, stroke="#F0E6CC", strokeWidth=4.5, cap="round")
d.shape("ellipse", "Baton tip glow", x=730, y=340, width=14, height=14,
        fill="#FFF4D0", opacity=85, stroke=NONE)

# --- her head is the notification bell ---------------------------------------------
d.path("M500,318 C552,318 584,356 586,406 C587,436 596,452 604,462 "
       "L396,462 C404,452 413,436 414,406 C416,356 448,318 500,318 Z",
       "Bell head", fill=BELL_GRAD, stroke=INK, strokeWidth=5)
# bell lip + clapper
d.path("M396,462 C396,482 604,482 604,462 L596,470 C560,484 440,484 404,470 Z",
       "Bell lip", fill="#B57E22", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Clapper", x=490, y=478, width=20, height=18,
        fill="#7A5216", stroke=INK, strokeWidth=3)
# crown highlight + shade
d.shape("ellipse", "Bell crown light", x=446, y=336, width=90, height=56,
        fill="#FFF0C0", opacity=35, stroke=NONE)
d.path("M560,350 C578,380 584,416 580,448 L604,462 C596,452 587,436 586,406 "
       "C584,364 574,340 560,350 Z",
       "Bell shade", fill="#8A5E1C", opacity=30, stroke=NONE)
# the maestro's focus: keen eyes, one brow arched at a sour ping
d.shape("ellipse", "Eye L", x=452, y=408, width=20, height=24,
        fill="#241C10", stroke=NONE)
d.shape("ellipse", "Eye R", x=528, y=408, width=20, height=24,
        fill="#241C10", stroke=NONE)
d.shape("ellipse", "Glint L", x=458, y=414, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint R", x=534, y=414, width=6, height=6,
        fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M444,392 Q458,382 474,390", "Brow L",
       fill=NONE, stroke="#241C10", strokeWidth=4.5, cap="round")
d.path("M524,384 Q540,374 556,382", "Brow R (arched)",
       fill=NONE, stroke="#241C10", strokeWidth=4.5, cap="round")
d.path("M484,448 Q500,456 516,448", "Mouth",
       fill=NONE, stroke="#241C10", strokeWidth=4, cap="round")

# --- the piano roll she reads --------------------------------------------------------
# paper strip across her midsection, ends rolled on their axles
d.shape("rectangle", "Roll shadow", x=176, y=610, width=652, height=64,
        radius=8, fill="#140A08", opacity=40, stroke=NONE)
d.shape("rectangle", "Roll paper", x=170, y=594, width=660, height=64,
        radius=6, fill=PAPER_GRAD, stroke="#6A5638", strokeWidth=3)
for side, ex in (("L", 178), ("R", 800)):
    d.shape("rectangle", f"Roll spool {side}", x=ex, y=582, width=22, height=88,
            radius=10, fill={"gradient": {"kind": "linear", "stops": [
                {"offset": 0, "color": "#8A6A44"}, {"offset": 1, "color": "#4E3A24"}]}},
            stroke=INK, strokeWidth=3)
    d.shape("ellipse", f"Roll axle {side}", x=ex + 6, y=620, width=10, height=10,
            fill="#2A2018", stroke=NONE)
# punched notes — the auditioning queue
NOTES = [232, 258, 300, 344, 372, 420, 468, 492, 540, 566, 610, 656, 700, 744]
for i, nx in enumerate(NOTES):
    lit = i in (4, 8, 11)
    d.shape("rectangle", f"Note slot {i+1}", x=nx, y=620 if not lit else 616,
            width=16, height=10 if not lit else 18, radius=4,
            fill="#5A4630" if not lit else "#C8862A",
            opacity=90 if not lit else 95, stroke=NONE)
    if lit:
        d.shape("ellipse", f"Note glow {i+1}", x=nx - 6, y=604, width=28, height=40,
                fill="#F0BC4E", opacity=25, stroke=NONE)

# --- the pings, rising off the lit notes ----------------------------------------------
def ping(cx, cy, s, label):
    """A tiny notification bell + sound arcs, size s at (cx,cy)."""
    d.path(f"M{cx},{cy - s} C{cx + s * 0.55},{cy - s} {cx + s * 0.7},{cy - s * 0.5} "
           f"{cx + s * 0.7},{cy - s * 0.1} L{cx + s * 0.8},{cy + s * 0.25} "
           f"L{cx - s * 0.8},{cy + s * 0.25} L{cx - s * 0.7},{cy - s * 0.1} "
           f"C{cx - s * 0.7},{cy - s * 0.5} {cx - s * 0.55},{cy - s} {cx},{cy - s} Z",
           f"{label} bell", fill=PING_GRAD, stroke=INK, strokeWidth=2.5)
    d.shape("ellipse", f"{label} clap", x=int(cx - s * 0.16), y=int(cy + s * 0.3),
            width=int(s * 0.32), height=int(s * 0.28), fill=INK, stroke=NONE)
    for k, rr in enumerate((1.15, 1.5)):
        d.path(f"M{cx + s * rr},{cy - s * 0.2} A{s * rr},{s * rr} 0 0 1 "
               f"{cx + s * rr * 0.35},{cy - s * rr * 1.05}",
               f"{label} arc {k+1}", fill=NONE, stroke="#F0BC4E",
               strokeWidth=2.5, opacity=60 - k * 20, cap="round")

ping(384, 560, 22, "Ping 1")
ping(548, 540, 26, "Ping 2")
ping(664, 560, 22, "Ping 3")
# one sour ping she's frowning at — dimmer, flat
d.path("M716,540 C716,530 724,524 732,524 L732,556 L716,556 Z", "Flat ping",
       fill="#8A7A56", opacity=55, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("MELODY ERRORFLOOD", "Name", x=500, y=930, size=52, font="Virelai Sans",
       color="#F0DFC8", justify="center")
r = d.text("NOTIFICATION MAESTRO", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8A488", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("031.melody-errorflood-V1R00")
