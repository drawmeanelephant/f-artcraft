#!/usr/bin/env python3
"""APH-037 Winona Crashington — motivational-poster aphorism plate V1R00.
A CRASH IS A FRIEND poster: an ancient CRT humming in the basement, its
blue screen glowing like a campfire; Winona sits in the wash of it, lost
Notepad documents gathered in her apron. We do not look away.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-037 Winona Crashington — Motivational Poster", 1000, 1000)

INK = "#100E22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#16142A"}, {"offset": 1, "color": "#07060F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E3A66"}, {"offset": 0.7, "color": "#221F40"},
    {"offset": 1, "color": "#100E22"}]}}
POSTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#252244"}, {"offset": 1, "color": "#12102A"}]}}
CRT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E5A6E"}, {"offset": 1, "color": "#322F48"}]}}
SCR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7FB0FF"}, {"offset": 0.55, "color": "#3A6CE0"},
    {"offset": 1, "color": "#1A3C9C"}]}}
FIG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#232040"}, {"offset": 1, "color": "#14122A"}]}}
GOLD = "#E8A858"
FRAME = "#B8B4D8"
HEAD = "#F0EEFA"
PUNCH = "#D2CEEA"
FAINT = "#8C88AC"
GLOW = "#5A8CF0"
PAPER = "#E8E4D8"
RIM = "#6A9AF0"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E4A80", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4BFF0", strokeWidth=3, opacity=30)
d.shape("ellipse", "Patina 1", x=195, y=175, width=205, height=115,
        fill="#363258", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=615, y=635, width=205, height=105,
        fill="#363258", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(218, 278, 7), (786, 262, 8), (170, 482, 6),
                               (834, 480, 7), (252, 658, 6), (750, 664, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4A4680", opacity=35, stroke=NONE)
# stray blue motes on the plate
for i, (x, y, op) in enumerate([(272, 216, 42), (296, 208, 30),
                                 (700, 590, 42), (724, 598, 30)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=6, height=6,
            fill=GLOW, opacity=op, stroke=NONE)

# --- the poster card -------------------------------------------------------------
PX, PY, PW, PH = 220, 150, 560, 440
d.shape("rectangle", "Poster shadow", x=PX + 8, y=PY + 10, width=PW,
        height=PH, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Poster", x=PX, y=PY, width=PW, height=PH,
        fill=POSTER_GRAD, stroke="#3C3862", strokeWidth=4)
d.shape("rectangle", "Frame outer", x=PX + 16, y=PY + 16,
        width=PW - 32, height=PH - 32, fill=NONE, stroke=FRAME,
        strokeWidth=2, opacity=80)
d.shape("rectangle", "Frame inner", x=PX + 24, y=PY + 24,
        width=PW - 48, height=PH - 48, fill=NONE, stroke=GOLD,
        strokeWidth=1.5, opacity=60)

# kicker + two-line headline
r = d.text("CRASH IS A FRIEND", "Kicker", x=500, y=PY + 40, size=12,
           font="Virelai Sans", color=GOLD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "kicker tracking", ids=[r["id"]], tracking=280)
r = d.text("WE DO NOT LOOK AWAY", "Headline 1", x=500, y=PY + 68,
           size=26, font="Virelai Sans", color=HEAD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "head1 tracking", ids=[r["id"]], tracking=15)
r = d.text("FROM THE BLUE SCREEN", "Headline 2", x=500, y=PY + 98,
           size=26, font="Virelai Sans", color=GLOW, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "head2 tracking", ids=[r["id"]], tracking=15)
d.path("M350,272 L472,272 M528,272 L650,272", "Headline rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=80)
d.path(rot_rect_path(500, 272, 10, 10, 45), "Headline diamond",
       fill=GOLD, opacity=85, stroke=NONE)

# --- the blue campfire -------------------------------------------------------------
# glow wash on the poster
d.shape("ellipse", "Glow wash", x=390, y=300, width=250, height=200,
        fill=GLOW, opacity=10, stroke=NONE)
d.shape("ellipse", "Glow pool", x=380, y=505, width=270, height=42,
        fill=GLOW, opacity=14, stroke=NONE)

# Winona, back to us, apron full of lost documents
d.shape("ellipse", "Figure shadow", x=262, y=518, width=130, height=12,
        fill="#000000", opacity=35, stroke=NONE)
# body / apron: trapezoid with soft shoulders
d.path("M302,468 Q325,456 348,468 L374,528 Q324,538 274,528 Z",
       "Apron", fill=FIG_GRAD, stroke="#0A0818", strokeWidth=2.5)
# apron pocket
d.path("M302,498 Q325,505 348,498 L342,515 Q325,521 308,515 Z",
       "Apron pocket", fill="#1B1836", stroke="#0A0818",
       strokeWidth=1.5, opacity=90)
# the rescued notepad pages, held against the apron
d.path(rot_rect_path(316, 462, 20, 26, -14), "Doc 1", fill=PAPER,
       opacity=92, stroke="#9A94B8", strokeWidth=1.2)
d.path(rot_rect_path(338, 464, 20, 26, 9), "Doc 2", fill="#D8D4C8",
       opacity=92, stroke="#9A94B8", strokeWidth=1.2)
for i in range(2):
    d.path(f"M{310 + i * 3},{455 + i * 4} L{324 + i * 2},{451 + i * 5}",
           f"Doc line {i+1}", fill=NONE, stroke="#8A86A8", strokeWidth=1,
           opacity=70)
# head, tipped toward the light
d.shape("ellipse", "Head", x=304, y=410, width=44, height=46,
        fill=FIG_GRAD, stroke="#0A0818", strokeWidth=2.5)
# a wisp of hair caught by the glow
d.path("M344,414 C354,422 356,436 350,448", "Hair wisp", fill=NONE,
       stroke=RIM, strokeWidth=2, cap="round", opacity=70)
# rim light on the screen-facing edges
d.path("M344,468 L372,526", "Apron rim", fill=NONE, stroke=RIM,
       strokeWidth=2.5, cap="round", opacity=60)
d.path("M342,414 C350,424 351,438 346,450", "Head rim", fill=NONE,
       stroke=RIM, strokeWidth=2, cap="round", opacity=55)

# the CRT itself
MX, MY, MW, MH = 428, 322, 168, 118
d.shape("ellipse", "CRT shadow", x=MX - 12, y=MY + MH + 26,
        width=MW + 24, height=14, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "CRT body", x=MX, y=MY, width=MW, height=MH,
        radius=14, fill=CRT_GRAD, stroke="#0A0818", strokeWidth=3)
# screen, glowing
SX, SY, SW, SH = MX + 14, MY + 14, MW - 28, MH - 34
d.shape("rectangle", "Screen", x=SX, y=SY, width=SW, height=SH,
        radius=10, fill=SCR_GRAD, stroke="#0A0E20", strokeWidth=2)
# screen bloom, edges soft
d.shape("ellipse", "Screen bloom", x=SX + 20, y=SY + 12, width=SW - 40,
        height=SH - 24, fill="#A8CCFF", opacity=18, stroke=NONE)
# the old friend's last words, tiny on the glass
d.text("A fatal exception 0E has", "BSOD 1", x=SX + 10, y=SY + 22,
       size=7.5, font="Source Sans 3", color="#D8E4FF", justify="left")
d.text("occurred. Press any key", "BSOD 2", x=SX + 10, y=SY + 34,
       size=7.5, font="Source Sans 3", color="#D8E4FF", justify="left")
d.text("to return to Windows.", "BSOD 3", x=SX + 10, y=SY + 46,
       size=7.5, font="Source Sans 3", color="#D8E4FF", justify="left")
# scanlines
for i in range(4):
    d.path(f"M{SX + 6},{SY + 10 + i * 14} L{SX + SW - 6},{SY + 10 + i * 14}",
           f"Scanline {i+1}", fill=NONE, stroke="#0A1840", strokeWidth=1,
           opacity=30)
# bezel label + power lamp
d.text("CRASHVIEW 2000", "Bezel label", x=MX + MW/2, y=MY + MH - 12,
       size=7, font="Source Sans 3", color="#8A86A8", justify="center")
d.shape("ellipse", "Power lamp", x=MX + MW - 20, y=MY + MH - 16,
        width=6, height=6, fill=GOLD, opacity=90, stroke=NONE)
# stand
d.shape("rectangle", "CRT stem", x=MX + MW/2 - 14, y=MY + MH - 4,
        width=28, height=18, radius=3, fill="#2A2840",
        stroke="#0A0818", strokeWidth=2)
d.shape("rectangle", "CRT foot", x=MX + MW/2 - 34, y=MY + MH + 12,
        width=68, height=10, radius=5, fill="#2A2840",
        stroke="#0A0818", strokeWidth=2)
# power cord wandering off-stage right
d.path("M586,462 C640,470 690,492 730,518", "Power cord", fill=NONE,
       stroke="#0A0818", strokeWidth=3, cap="round", opacity=80)
# motes rising off the blue fire
for i, (x, y, w, op) in enumerate([(462, 300, 5, 45), (508, 288, 4, 38),
                                    (548, 296, 5, 42), (584, 306, 4, 30),
                                    (486, 274, 3, 24), (530, 268, 3, 20)]):
    d.shape("ellipse", f"Ember {i+1}", x=x, y=y, width=w, height=w,
            fill=GLOW, opacity=op, stroke=NONE)

# --- punchline sub-caption -------------------------------------------------------------
r = d.text("WE BATHE IN ITS SOFT LIGHT.", "Punchline", x=500,
           y=PY + PH - 34, size=20, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch tracking", ids=[r["id"]], tracking=80)

# --- flourish on the plate below the poster ----------------------------------------------
d.path("M415,668 L485,668 M515,668 L585,668", "Flourish rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=55)
d.path(rot_rect_path(500, 668, 9, 9, 45), "Flourish diamond", fill=GOLD,
       opacity=60, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("WINONA CRASHINGTON", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=HEAD, justify="center")
r = d.text("WE DO NOT LOOK AWAY", "Role", x=500, y=950,
           size=18, font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-037-winona-crashington-V1R00")
