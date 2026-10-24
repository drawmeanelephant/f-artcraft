#!/usr/bin/env python3
"""HAI-0443 Proctor Paul — haiku plate V1R00. Educational surveillance
made visual: the proctoring eye in the screen, the student's averted
gaze flagged as vice, the engagement meter falling, every keystroke
logged into the transcript. Cold indigo ink, one red flag. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Key line exceeds the t-glyph quirk — lettered in caps."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("HAI-0443 Proctor Paul — Haiku Plate", 1000, 1000)

INK = "#211C16"
RED = "#C8503E"
CREAM = "#E4E6EC"
SOFT = "#A0B4D4"
GLOW = "#7EB8E8"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#121624"}, {"offset": 1, "color": "#080A12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3C4E7A"}, {"offset": 0.7, "color": "#242E50"},
    {"offset": 1, "color": "#101528"}]}}
SCREEN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A3A66"}, {"offset": 1, "color": "#141C38"}]}}
BEZEL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A5478"}, {"offset": 1, "color": "#262C48"}]}}
FIG = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E6E92"}, {"offset": 1, "color": "#2C3450"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#546494", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D4DCF0", strokeWidth=3, opacity=40)
d.shape("ellipse", "Screen pool", x=300, y=300, width=400, height=420,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#7EB8E8", "opacity": 0.18},
            {"offset": 1, "color": "#7EB8E8", "opacity": 0}]}},
        stroke=NONE)
# stray logged pixels
for i, (x, y, w) in enumerate([(240,300,6),(760,320,7),(200,560,6),
                               (800,590,6),(330,170,5),(680,180,6)]):
    d.shape("ellipse", f"Logged mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#A0B4D4", opacity=16, stroke=NONE)

# --- the proctoring screen: an eye where the content should be ---------------------
d.shape("rectangle", "Monitor bezel", x=330, y=150, width=340, height=240,
        radius=14, fill=BEZEL, stroke=INK, strokeWidth=6)
d.shape("rectangle", "Monitor screen", x=350, y=170, width=300, height=200,
        radius=8, fill=SCREEN, stroke="#101528", strokeWidth=3)
# webcam nub watching from the bezel
d.shape("ellipse", "Webcam", x=492, y=156, width=16, height=16,
        fill="#101528", stroke="#546494", strokeWidth=2.5)
d.shape("ellipse", "Webcam iris", x=497, y=161, width=6, height=6,
        fill=GLOW, stroke=NONE)
# the eye itself — lid arcs, iris, cold highlight
d.path("M410,270 Q500,215 590,270 Q500,325 410,270 Z",
       "Eye outline", fill={"gradient": {"kind": "radial", "stops": [
           {"offset": 0, "color": "#D8E8F8"}, {"offset": 1, "color": "#8AA8CC"}]}},
       stroke=INK, strokeWidth=4)
d.shape("ellipse", "Iris", x=468, y=238, width=64, height=64,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#7EB8E8"}, {"offset": 1, "color": "#2A4A78"}]}},
        stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil", x=488, y=258, width=24, height=24,
        fill="#0C1020", stroke=NONE)
d.shape("ellipse", "Eye glint", x=482, y=252, width=10, height=10,
        fill="#FFFFFF", opacity=85, stroke=NONE)
# scanlines on the screen — the feed never sleeps
for i, y in enumerate(range(196, 361, 24)):
    d.path(f"M360,{y} L640,{y}", f"Scanline {i+1}", fill=NONE,
           stroke="#7EB8E8", strokeWidth=1.5, opacity=12)
# stand
d.path("M470,390 L470,430 M530,390 L530,430 M440,440 L560,440",
       "Stand", fill=NONE, stroke=INK, strokeWidth=8, cap="round")
# rec dot — always recording
d.shape("ellipse", "REC dot", x=624, y=180, width=14, height=14,
        fill=RED, stroke=NONE)
d.text("rec", "REC label", x=600, y=192, size=12,
       font="Virelai Sans", color="#E8C8C0", justify="center")

# --- the gaze cone: sight-lines that expect you facing -------------------------------
d.path("M420,390 L450,560", "Gaze L", fill=NONE, stroke=GLOW,
       strokeWidth=2.5, dash=[7, 7], opacity=55)
d.path("M580,390 L550,560", "Gaze R", fill=NONE, stroke=GLOW,
       strokeWidth=2.5, dash=[7, 7], opacity=55)
# the beam breaks where the student looks away — the flag rises there
d.path("M462,470 L468,522", "Beam break", fill=NONE, stroke=RED,
       strokeWidth=4, dash=[6, 6], cap="round", opacity=90)

# --- the engagement meter: the transcript now ---------------------------------------
d.shape("rectangle", "Meter frame", x=700, y=500, width=52, height=150,
        radius=10, fill="#141C38", stroke="#546494", strokeWidth=4)
d.shape("rectangle", "Meter fill", x=710, y=608, width=32, height=32,
        radius=5, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#E8A85A"}, {"offset": 1, "color": "#C8503E"}]}},
        stroke=NONE)
d.path("M706,520 L746,520 M706,564 L746,564", "Meter ticks", fill=NONE,
       stroke="#546494", strokeWidth=2, opacity=80)
d.text("engagement", "Meter label", x=726, y=482, size=13,
       font="Virelai Sans", color=SOFT, justify="center")
# trend arrow slumping off the meter
d.path("M706,540 L724,560 L742,584", "Trend", fill=NONE, stroke=RED,
       strokeWidth=3.5, cap="round")
d.path("M742,584 L730,578 L744,570 Z", "Trend head", fill=RED, stroke=NONE)

# --- the flag chip: suspicion logged -------------------------------------------------
d.shape("rectangle", "Flag chip", x=246, y=486, width=220, height=46,
        radius=8, fill="#141C38", stroke=RED, strokeWidth=3)
d.text("flagged: gaze averted", "Flag text", x=356, y=514, size=15,
       font="Virelai Sans", color="#E8C8C0", justify="center")
d.path("M410,470 L462,470", "Flag lead", fill=NONE, stroke=RED,
       strokeWidth=2.5, dash=[4, 4])

# --- the student: face turned from the screen, thinking -------------------------------
# desk
d.path("M340,742 L640,742 M370,742 L370,800 M610,742 L610,800",
       "Desk", fill=NONE, stroke=INK, strokeWidth=7, cap="round")
d.shape("ellipse", "Desk shadow", x=340, y=798, width=300, height=22,
        fill="#080A12", opacity=50, stroke=NONE)
# laptop on the desk, screen glowing toward the student
d.shape("rectangle", "Laptop base", x=400, y=726, width=110, height=16,
        radius=4, fill=BEZEL, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Laptop lid", x=414, y=660, width=84, height=68,
        radius=6, fill=SCREEN, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Lid eye", x=442, y=682, width=28, height=20,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#D8E8F8"},
            {"offset": 1, "color": "#8AA8CC"}]}},
        stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Lid pupil", x=452, y=688, width=10, height=10,
        fill="#0C1020", stroke=NONE)
# the student — seated, head in profile turned AWAY from the laptop
d.path("M540,742 C540,706 544,684 552,670 Q570,660 588,670 "
       "C596,684 600,706 600,742 Z",
       "Student body", fill=FIG, stroke=INK, strokeWidth=5)
# head in left profile — gaze leaving the screen
d.path("M556,668 C550,646 552,624 566,616 C580,608 596,616 598,632 "
       "C599,646 592,660 578,666 Z",
       "Student head", fill=FIG, stroke=INK, strokeWidth=4.5)
d.path("M552,640 L546,646 L552,648", "Profile nose", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round", join="round")
d.shape("ellipse", "Profile eye", x=560, y=632, width=7, height=7,
        fill="#0C1020", stroke=NONE)
# the averted-gaze ray, drifting up toward the thought
d.path("M548,634 C520,606 500,580 490,548", "Averted ray", fill=NONE,
       stroke="#E8C8C0", strokeWidth=2.5, dash=[4, 6], opacity=75,
       cap="round")
# thought bubble — the crime of thinking
for i, (bx, by, bw) in enumerate([(498, 526, 8), (486, 504, 12),
                                  (470, 476, 16)]):
    d.shape("ellipse", f"Thought {i+1}", x=bx - bw / 2, y=by - bw / 2,
            width=bw, height=bw, fill="#D4DCF0", opacity=70, stroke=NONE)
d.text("…", "Thought mark", x=458, y=480, size=26,
       font="Virelai Sans", color="#D4DCF0", justify="center")

# --- the keystroke log: every pause is bio -------------------------------------------
d.shape("rectangle", "Log strip", x=376, y=824, width=248, height=30,
        radius=6, fill="#0C1020", stroke="#3A4670", strokeWidth=2.5)
d.text("log · key key pause key", "Log text", x=500, y=844, size=12,
       font="Virelai Sans", color="#8A9CC4", justify="center")
d.shape("ellipse", "Log cursor", x=616, y=832, width=6, height=14,
        fill="#8A9CC4", opacity=70, stroke=NONE)

# --- caption stack: key line over the name ---------------------------------------------
r = d.text("LOOKING AWAY FROM THE SCREEN MEANS YOU'RE THINKING.",
           "Key line", x=500, y=898, size=19,
           font="Virelai Sans", color=SOFT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=90)
d.text("PROCTOR PAUL", "Name", x=500, y=944, size=56,
       font="Virelai Sans", color=CREAM, justify="center")

d.finish("hai-0443-proctor-paul-V1R00")
