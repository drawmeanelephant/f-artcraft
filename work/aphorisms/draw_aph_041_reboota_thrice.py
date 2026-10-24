#!/usr/bin/env python3
"""APH-041 Reboota Thrice — motivational-poster aphorism plate V1R00.
A NEVER GIVE UP poster: a power button pressed three times, a monitor
showing three boot frames — dark, blinking, loading — and a row of fans
whirring underneath like little prayers. Hope loads one frame at a time.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-041 Reboota Thrice — Motivational Poster", 1000, 1000)

INK = "#0C1614"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#14201C"}, {"offset": 1, "color": "#080E0C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2E4A40"}, {"offset": 0.7, "color": "#1A2E28"},
    {"offset": 1, "color": "#0C1614"}]}}
POSTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E322C"}, {"offset": 1, "color": "#101A16"}]}}
MON_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A4A46"}, {"offset": 1, "color": "#1E2A26"}]}}
PANE_DARK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#122019"}, {"offset": 1, "color": "#0A120E"}]}}
PANE_LIT = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#2E6A4C"}, {"offset": 1, "color": "#0E1E16"}]}}
GOLD = "#F0C060"
FRAME = "#B8D0C4"
HEAD = "#EEF6F0"
PUNCH = "#D2DCD4"
FAINT = "#88A098"
PHOS = "#7FE0A8"
PHOS_DIM = "#3E8A60"
TRACE = "#4A6A5C"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#46685C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#BCE0CE", strokeWidth=3, opacity=30)
d.shape("ellipse", "Patina 1", x=195, y=178, width=205, height=115,
        fill="#2A4438", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=618, y=632, width=205, height=108,
        fill="#2A4438", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(220, 276, 7), (786, 264, 8), (172, 482, 6),
                               (832, 480, 7), (254, 660, 6), (750, 662, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E6A56", opacity=35, stroke=NONE)
# tiny leds on the plate, still lit after all these years
for i, (x, y, op) in enumerate([(270, 218, 46), (294, 210, 32),
                                 (702, 588, 46), (726, 596, 32)]):
    d.shape("ellipse", f"LED {i+1}", x=x, y=y, width=6, height=6,
            fill=PHOS, opacity=op, stroke=NONE)

# --- the poster card -------------------------------------------------------------
PX, PY, PW, PH = 220, 150, 560, 440
d.shape("rectangle", "Poster shadow", x=PX + 8, y=PY + 10, width=PW,
        height=PH, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Poster", x=PX, y=PY, width=PW, height=PH,
        fill=POSTER_GRAD, stroke="#2E4A40", strokeWidth=4)
d.shape("rectangle", "Frame outer", x=PX + 16, y=PY + 16,
        width=PW - 32, height=PH - 32, fill=NONE, stroke=FRAME,
        strokeWidth=2, opacity=80)
d.shape("rectangle", "Frame inner", x=PX + 24, y=PY + 24,
        width=PW - 48, height=PH - 48, fill=NONE, stroke=GOLD,
        strokeWidth=1.5, opacity=60)

# kicker + two-line headline
r = d.text("NEVER GIVE UP", "Kicker", x=500, y=PY + 40, size=12,
           font="Virelai Sans", color=GOLD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "kicker tracking", ids=[r["id"]], tracking=280)
r = d.text("DID YOU TRY IT AGAIN?", "Headline 1", x=500, y=PY + 68,
           size=28, font="Virelai Sans", color=HEAD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "head1 tracking", ids=[r["id"]], tracking=15)
r = d.text("AND AGAIN?", "Headline 2", x=500, y=PY + 100,
           size=28, font="Virelai Sans", color=PHOS, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "head2 tracking", ids=[r["id"]], tracking=15)
d.path("M350,274 L472,274 M528,274 L650,274", "Headline rules", fill=NONE,
       stroke=GOLD, strokeWidth=2, opacity=80)
d.path(rot_rect_path(500, 274, 10, 10, 45), "Headline diamond",
       fill=GOLD, opacity=85, stroke=NONE)

# --- the power button, pressed three times -------------------------------------------
# concentric press rings, each push fainter than the last
for i, (rr, op) in enumerate([(36, 45), (50, 28), (64, 15)]):
    d.shape("ellipse", f"Press ring {i+1}", x=318 - rr, y=398 - rr,
            width=rr * 2, height=rr * 2, fill=NONE, stroke=GOLD,
            strokeWidth=1.5, opacity=op)
# button housing + cap
d.shape("ellipse", "Button shadow", x=296, y=430, width=56, height=10,
        fill="#000000", opacity=35, stroke=NONE)
d.shape("ellipse", "Button housing", x=286, y=366, width=64, height=64,
        fill="#24332C", stroke="#0A140F", strokeWidth=3)
d.shape("ellipse", "Button cap", x=294, y=374, width=48, height=48,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#4A685C"},
            {"offset": 1, "color": "#223228"}]}},
        stroke="#0A140F", strokeWidth=2)
# the power glyph: arc with a gap at top + stem
d.path("M333.4,381.6 A24,24 0 1 1 302.6,381.6", "Power arc", fill=NONE,
       stroke=PHOS, strokeWidth=3, cap="round", opacity=90)
d.path("M318,372 L318,394", "Power stem", fill=NONE, stroke=PHOS,
       strokeWidth=3, cap="round", opacity=90)
# trace to the monitor + via dot
d.path("M382,398 L400,398", "Trace to monitor", fill=NONE, stroke=TRACE,
       strokeWidth=1.5, opacity=40)
d.shape("ellipse", "Via 1", x=389, y=396, width=4, height=4, fill=TRACE,
        opacity=50, stroke=NONE)

# --- the monitor with three boot frames ----------------------------------------------
MX, MY, MW, MH = 400, 302, 310, 132
d.shape("ellipse", "Monitor shadow", x=MX + 30, y=MY + MH + 18,
        width=MW - 60, height=12, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Monitor", x=MX, y=MY, width=MW, height=MH,
        radius=10, fill=MON_GRAD, stroke="#0A140F", strokeWidth=3)
SX, SY = MX + 12, MY + 12
PANES = [(SX, 88), (SX + 94, 88), (SX + 188, 98)]
for i, (px, pw) in enumerate(PANES):
    fill = PANE_LIT if i == 2 else PANE_DARK
    d.shape("rectangle", f"Frame {i+1}", x=px, y=SY, width=pw,
            height=78, radius=4, fill=fill, stroke="#060C09",
            strokeWidth=2)
# TRY 1: nothing but a no-signal dash
d.path(f"M{SX + 34},{SY + 38} L{SX + 54},{SY + 38}", "No signal", fill=NONE,
       stroke="#3A5048", strokeWidth=3, cap="round", opacity=70)
# TRY 2: a caret and boot dots, still thinking
d.shape("rectangle", "Boot caret", x=SX + 106, y=SY + 56, width=10,
        height=3, fill=PHOS_DIM, opacity=85, stroke=NONE)
for i in range(3):
    d.shape("ellipse", f"Boot dot {i+1}", x=SX + 108 + i * 10,
            y=SY + 32, width=4, height=4, fill=PHOS_DIM,
            opacity=35 + i * 18, stroke=NONE)
# TRY 3: the frame where hope loads — progress bar partway
d.shape("ellipse", "Hope glow", x=SX + 200, y=SY + 10, width=74,
        height=56, fill=PHOS, opacity=12, stroke=NONE)
TBX, TBY, TBW = SX + 200, SY + 44, 74
d.shape("rectangle", "Load track", x=TBX, y=TBY, width=TBW, height=8,
        radius=4, fill="#0E1E16", stroke="#28503C", strokeWidth=1.5)
d.shape("rectangle", "Load fill", x=TBX + 1.5, y=TBY + 1.5,
        width=(TBW - 3) * 0.62, height=5, radius=2.5, fill=PHOS,
        opacity=90, stroke=NONE)
for i in range(3):
    d.shape("ellipse", f"Hope dot {i+1}", x=SX + 214 + i * 10,
            y=SY + 22, width=4, height=4, fill=PHOS,
            opacity=60 + i * 12, stroke=NONE)
# attempt labels under each frame
for i, (px, pw) in enumerate(PANES):
    d.text(f"TRY {i+1}", f"Try label {i+1}", x=px + pw/2, y=SY + 92,
           size=7.5, font="Source Sans 3",
           color=PHOS if i == 2 else FAINT, justify="center")
# bezel brand + stand
d.text("REBOOTA MK III", "Bezel brand", x=MX + MW/2, y=MY + MH - 8,
       size=7, font="Source Sans 3", color="#6A8078", justify="center")
d.shape("ellipse", "Monitor LED", x=MX + MW - 20, y=MY + MH - 14,
        width=6, height=6, fill=PHOS, opacity=90, stroke=NONE)
d.shape("rectangle", "Monitor stem", x=MX + MW/2 - 13, y=MY + MH - 2,
        width=26, height=18, radius=3, fill="#1E2A26",
        stroke="#0A140F", strokeWidth=2)
d.shape("rectangle", "Monitor foot", x=MX + MW/2 - 32, y=MY + MH + 14,
        width=64, height=9, radius=4.5, fill="#1E2A26",
        stroke="#0A140F", strokeWidth=2)

# --- the fans, whirring like prayers -----------------------------------------------------
FANS = [(450, 510, 16), (528, 514, 13), (606, 510, 16)]
d.shape("ellipse", "Fan row shadow", x=420, y=524, width=216, height=10,
        fill="#000000", opacity=25, stroke=NONE)
for i, (fx, fy, fr) in enumerate(FANS):
    d.shape("ellipse", f"Fan {i+1} ring", x=fx - fr, y=fy - fr,
            width=fr * 2, height=fr * 2, fill="#16241E",
            stroke="#3A5048", strokeWidth=2)
    # blades: three arcs inside, spun
    for b in range(3):
        a = math.radians(b * 120 + 20)
        bx, by = fx + (fr - 5) * math.cos(a), fy + (fr - 5) * math.sin(a)
        d.shape("ellipse", f"Fan {i+1} blade {b+1}", x=bx - 3, y=by - 3,
                width=6, height=6, fill="#4A6A5C", opacity=80,
                stroke=NONE)
    d.shape("ellipse", f"Fan {i+1} hub", x=fx - 2.5, y=fy - 2.5,
            width=5, height=5, fill=FAINT, opacity=80, stroke=NONE)
    # motion arcs, still spinning
    d.path(f"M{fx - fr - 4},{fy - 2} A{fr + 4},{fr + 4} 0 0 1 {fx - 2},{fy - fr - 4}",
           f"Fan {i+1} spin", fill=NONE, stroke=PHOS_DIM,
           strokeWidth=1.5, dash=[3, 3], cap="round", opacity=50)
    # the prayer: a small swirl rising off each fan
    d.path(f"M{fx + 2},{fy - fr - 6} c6,-2 8,-8 2,-11 c-5,-2 -9,2 -5,6 "
           f"c3,3 8,2 9,-2", f"Prayer {i+1}", fill=NONE, stroke=GOLD,
           strokeWidth=1.5, cap="round", opacity=55)

# --- punchline sub-caption -------------------------------------------------------------
r = d.text("HOPE LOADS ONE FRAME AT A TIME.", "Punchline", x=500,
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
d.text("REBOOTA THRICE", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=HEAD, justify="center")
r = d.text("DID YOU TRY IT AGAIN", "Role", x=500, y=950,
           size=18, font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-041-reboota-thrice-V1R00")
