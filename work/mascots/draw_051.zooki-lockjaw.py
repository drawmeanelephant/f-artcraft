#!/usr/bin/env python3
"""Zooki Lockjaw — mascot portrait V1R00. Server Zookeeper.
A frantic little warden in cap and cape, locked OUTSIDE his own server
cage: brass keyring hoisted overhead, padlock on the latch, ledger card
on the door reading WHO HOLDS THE LATCH, node LEDs blinking smugly
behind the bars. Steel-slate plate on a machine-room night. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Ledger glyphs in Source Sans 3. Plate = circle (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Zooki Lockjaw — Mascot Portrait", 1000, 1000)

INK = "#1E2230"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#10141E"}, {"offset": 1, "color": "#06080E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E6E88"}, {"offset": 0.62, "color": "#3C4A60"},
    {"offset": 1, "color": "#1B2230"}]}}
CAGE_GRAD = {"gradient": {"kind": "linear", "start": [0, 230], "end": [0, 660], "stops": [
    {"offset": 0, "color": "#2A3242"}, {"offset": 1, "color": "#12161F"}]}}
BAR_GRAD = {"gradient": {"kind": "linear", "start": [430, 0], "end": [455, 0], "stops": [
    {"offset": 0, "color": "#8A94A6"}, {"offset": 0.5, "color": "#5A6478"},
    {"offset": 1, "color": "#333B4C"}]}}
COAT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A5878"}, {"offset": 0.7, "color": "#33405C"},
    {"offset": 1, "color": "#20283C"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8D8B8"}, {"offset": 1, "color": "#C0A678"}]}}
BRASS = "#D0A04E"
BRASS_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8BC66"}, {"offset": 1, "color": "#9A7430"}]}}
LED = "#7CE0A8"
CARD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E8D2"}, {"offset": 1, "color": "#CFC2A0"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

def faint_text(t, label, opacity, **kw):
    r = d.text(t, label, **kw)
    if r and r.get("id"):
        d.cmd("object.setProps", f"{label} opacity", id=r["id"],
              opacity=opacity)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#5A6A88", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#10141E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D4E8", strokeWidth=3, opacity=28)
d.shape("ellipse", "Patina 1", x=200, y=280, width=250, height=150,
        fill="#7484A0", opacity=16, stroke=NONE)
d.shape("ellipse", "Patina 2", x=560, y=620, width=260, height=150,
        fill="#2A3346", opacity=32, stroke=NONE)
for i, (x, y, w) in enumerate([(222,342,5),(790,338,6),(182,545,5),(840,572,5),
                               (256,756,5),(730,760,6),(162,452,5),(848,645,5),
                               (432,134,5),(596,140,6),(336,166,4),(700,203,5),
                               (250,656,4),(658,716,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8E2F2", opacity=28, stroke=NONE)
# faint lockfile glyphs drifting
for i, (t, x, y, s) in enumerate([("{ }", 215, 250, 24), ("lock", 775, 205, 19),
                                  ("pid", 172, 645, 19), ("key", 805, 700, 22)]):
    assert on_disc(x, y, 20), (x, y)
    faint_text(t, f"Drift {i+1}", 25, x=x, y=y, size=s,
               font="Source Sans 3", color="#B8C4D8", justify="center")
# ghost arcs on the dark backdrop
d.path("M932,162 A100,100 0 0 0 852,72", "Ghost arc TR",
       fill=NONE, stroke="#6A7A98", strokeWidth=14, opacity=10, cap="round")
d.path("M78,778 A115,115 0 0 0 182,880", "Ghost arc BL",
       fill=NONE, stroke="#6A7A98", strokeWidth=10, opacity=8, cap="round")

# --- the server cage -------------------------------------------------------------
d.shape("ellipse", "Cage shadow", x=420, y=668, width=380, height=42,
        fill="#06080C", opacity=45, stroke=NONE)
# interior darkness + server towers behind the bars
d.shape("rectangle", "Cage interior", x=440, y=240, width=340, height=410,
        radius=10, fill=CAGE_GRAD, stroke=INK, strokeWidth=5)
# server towers — dim stacked units with a few smug LEDs
for j, (rx, rh) in enumerate([(468, 3), (560, 4), (656, 3)]):
    d.shape("rectangle", f"Tower {j+1}", x=rx, y=430, width=76,
            height=200, radius=6, fill="#1A2030", stroke="#0C1018",
            strokeWidth=3)
    for k in range(rh):
        d.shape("ellipse", f"Tower {j+1} led {k+1}", x=rx + 8 + k * 16,
                y=448, width=8, height=8, fill=LED,
                opacity=85 if k % 2 == 0 else 40, stroke=NONE)
        d.shape("ellipse", f"Tower {j+1} glow {k+1}", x=rx + 5 + k * 16,
                y=445, width=14, height=14, fill=LED, opacity=18,
                stroke=NONE)
    for k, yy in enumerate(range(480, 620, 28)):
        d.path(f"M{rx + 10},{yy} L{rx + 66},{yy}",
               f"Tower {j+1} slot {k+1}", fill=NONE, stroke="#2E3648",
               strokeWidth=5, cap="round", opacity=70)
# one tower fan still spinning (dashed arc)
d.path("M694,560 A26,26 0 1 1 692,586", "Fan arc",
       fill=NONE, stroke=LED, strokeWidth=3, dash=[6, 8], opacity=45,
       cap="round")
# cage floor grate
d.path("M440,618 L780,618 L780,650 L440,650 Z", "Floor grate",
       fill="#0E1220", stroke=INK, strokeWidth=3)
# THE BARS — over everything inside
for j, bx in enumerate(range(462, 770, 34)):
    d.path(f"M{bx},252 L{bx},606", f"Bar {j+1}", fill=NONE,
           stroke="#6E788C", strokeWidth=9, cap="round")
    d.path(f"M{bx - 3},252 L{bx - 3},606", f"Bar light {j+1}", fill=NONE,
           stroke="#A8B4C8", strokeWidth=2.5, cap="round", opacity=45)
# horizontal rails
for j, yy in enumerate((252, 606)):
    d.shape("rectangle", f"Rail {j+1}", x=440, y=yy - 10, width=340,
            height=20, radius=8, fill=BAR_GRAD, stroke=INK,
            strokeWidth=3.5)
# door seam + latch side (door is the left half)
d.path("M600,252 L600,606", "Door seam", fill=NONE, stroke="#3A4254",
       strokeWidth=3, opacity=80)
# padlock on the latch — he is outside, it is locked
d.path("M625,400 C625,382 633,372 647,372 C661,372 669,382 669,400",
       "Shackle", fill=NONE, stroke=BRASS, strokeWidth=7, cap="round")
d.shape("rectangle", "Padlock body", x=622, y=400, width=48, height=44,
        radius=9, fill=BRASS_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Keyhole", x=640, y=414, width=12, height=16,
        fill=INK, stroke=NONE)
d.path("M626,410 L666,410", "Lock shine", fill=NONE, stroke="#F4D896",
       strokeWidth=3, cap="round", opacity=60)

# ledger card clipped to the door — WHO HOLDS THE LATCH
d.path("M510,480 L596,480 L600,556 L514,556 Z", "Ledger card",
       fill=CARD_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("rectangle", "Card clip", x=538, y=470, width=30, height=16,
        radius=4, fill="#6E788C", stroke=INK, strokeWidth=2.5)
d.text("WHO HOLDS", "Ledger line 1", x=555, y=512, size=15,
       font="Source Sans 3", color="#3A3220", justify="center")
d.text("THE LATCH", "Ledger line 2", x=555, y=538, size=15,
       font="Source Sans 3", color="#3A3220", justify="center")

# --- Zooki himself -----------------------------------------------------------------
d.shape("ellipse", "Zooki shadow", x=140, y=760, width=280, height=40,
        fill="#06080C", opacity=45, stroke=NONE)
# cape — flowing behind, fully caped
d.path("M228,500 C180,540 158,620 168,700 C176,740 200,756 226,748 "
       "C216,680 220,580 244,512 Z",
       "Cape", fill="#2A3350", stroke=INK, strokeWidth=4)
d.path("M186,560 C176,610 176,660 186,700", "Cape fold",
       fill=NONE, stroke="#46527A", strokeWidth=3, opacity=60,
       cap="round")
# feet — small boots planted wide
d.shape("rectangle", "Boot L", x=222, y=744, width=64, height=30, radius=13,
        fill="#2A2E38", stroke=INK, strokeWidth=3.5)
d.shape("rectangle", "Boot R", x=312, y=744, width=64, height=30, radius=13,
        fill="#2A2E38", stroke=INK, strokeWidth=3.5)
# coat body — warden pear
d.path("M298,466 C240,476 208,540 210,620 C212,700 248,752 300,752 "
       "C352,752 388,700 390,620 C392,540 356,476 298,466 Z",
       "Coat", fill=COAT_GRAD, stroke=INK, strokeWidth=5)
# coat front seam + brass buttons
d.path("M300,560 L300,742", "Coat seam", fill=NONE, stroke="#1A2234",
       strokeWidth=3, opacity=70)
for j, yy in enumerate((580, 620, 660, 700)):
    d.shape("ellipse", f"Button {j+1}", x=288, y=yy, width=11, height=11,
            fill=BRASS, stroke=INK, strokeWidth=2)
# coat rim light
d.path("M224,540 C216,600 218,670 236,716", "Coat rim",
       fill=NONE, stroke="#9AA8C4", strokeWidth=4, opacity=40,
       cap="round")

# head — face disc over the coat collar
d.shape("ellipse", "Head", x=252, y=452, width=96, height=88,
        fill=FACE_GRAD, stroke=INK, strokeWidth=4)
# warden cap — peaked, brass badge
d.path("M246,470 C246,430 270,410 300,410 C330,410 354,430 354,470 "
       "C330,458 270,458 246,470 Z",
       "Cap crown", fill="#33405C", stroke=INK, strokeWidth=4)
d.path("M238,470 C270,458 330,458 362,470 C362,478 354,482 344,482 "
       "L256,482 C246,482 238,478 238,470 Z",
       "Cap brim", fill="#26304A", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Cap badge", x=293, y=424, width=14, height=14,
        fill=BRASS, stroke=INK, strokeWidth=2)

# frantic wide eyes + gritted mouth — the key is in his hand, not the door
d.shape("ellipse", "Eye L", x=266, y=492, width=20, height=22,
        fill="#F8F4E8", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Eye R", x=314, y=492, width=20, height=22,
        fill="#F8F4E8", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil L", x=272, y=498, width=8, height=9,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=320, y=498, width=8, height=9,
        fill=INK, stroke=NONE)
d.path("M262,478 C272,470 284,470 292,476", "Brow L",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
d.path("M310,476 C320,469 332,470 340,477", "Brow R",
       fill=NONE, stroke=INK, strokeWidth=3.5, cap="round")
# gritted mouth — flat bar with tooth ticks
d.shape("rectangle", "Mouth", x=278, y=522, width=44, height=12,
        radius=3, fill="#F8F4E8", stroke=INK, strokeWidth=3)
d.path("M289,522 L289,534 M300,522 L300,534 M311,522 L311,534",
       "Teeth", fill=NONE, stroke=INK, strokeWidth=2, opacity=70)

# left arm clamped on the cage door edge — reaching but locked out
d.path("M376,560 C400,548 420,532 434,512 C446,508 456,518 452,530 "
       "C440,554 416,574 392,586 Z",
       "Arm R", fill=COAT_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand on door", x=430, y=502, width=28, height=28,
        fill="#C0A678", stroke=INK, strokeWidth=3)
# right arm hoisting the keyring overhead
d.path("M236,520 C210,490 200,452 208,420 C220,412 234,418 236,432 "
       "C232,458 240,484 254,502 Z",
       "Arm L", fill=COAT_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand L", x=200, y=400, width=30, height=28,
        fill="#C0A678", stroke=INK, strokeWidth=3)
# THE brass keyring, jangling
d.shape("ellipse", "Keyring", x=196, y=344, width=56, height=56,
        fill=NONE, stroke=BRASS, strokeWidth=8)
d.shape("ellipse", "Ring shine", x=204, y=350, width=18, height=10,
        fill="#F4D896", opacity=60, stroke=NONE)
# five keys hanging off the ring's lower arc
KEYS = [(204, 396, -24), (220, 402, -10), (236, 404, 6), (250, 398, 20)]
for j, (kx, ky, tilt) in enumerate(KEYS):
    # shaft
    d.path(f"M{kx},{ky} L{kx + tilt},{ky + 44}",
           f"Key {j+1} shaft", fill=NONE, stroke=BRASS,
           strokeWidth=5, cap="round")
    # bit teeth
    d.path(f"M{kx + tilt},{ky + 44} l8,-2 M{kx + tilt},{ky + 38} l7,-2",
           f"Key {j+1} teeth", fill=NONE, stroke=BRASS,
           strokeWidth=3.5, cap="round")
    # bow
    d.shape("ellipse", f"Key {j+1} bow", x=kx - 6, y=ky - 10, width=13,
            height=13, fill=NONE, stroke=BRASS, strokeWidth=3.5)
# jangle marks
d.path("M172,360 C164,376 164,392 172,406", "Jangle L",
       fill=NONE, stroke=BRASS, strokeWidth=3, dash=[4, 6], opacity=70,
       cap="round")
d.path("M272,352 C282,368 284,384 278,398", "Jangle R",
       fill=NONE, stroke=BRASS, strokeWidth=3, dash=[4, 6], opacity=70,
       cap="round")

# --- name + role ----------------------------------------------------------------------
d.text("ZOOKI LOCKJAW", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#DEE6F2", justify="center")
r = d.text("SERVER ZOOKEEPER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9DB0CC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("051.zooki-lockjaw-V1R00")
