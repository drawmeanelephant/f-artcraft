#!/usr/bin/env python3
"""Pending Jurisdiction — mascot portrait V1R00.
A translucent sheet-ghost holding a ticket gone soft in a hallway between
two departments; both doors stay shut. 1000x1000. Gradients + translucent
shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Pending Jurisdiction — Mascot Portrait", 1000, 1000)

INK = "#1E2430"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#131C26"}, {"offset": 1, "color": "#080D14"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#56707E"}, {"offset": 0.7, "color": "#37495A"},
    {"offset": 1, "color": "#1B2634"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E3E4E"}, {"offset": 1, "color": "#141D28"}]}}
GHOST_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8F0F6"}, {"offset": 0.7, "color": "#BCCBD8"},
    {"offset": 1, "color": "#8AA0B2"}]}}
DOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A4A5E"}, {"offset": 1, "color": "#22303F"}]}}
TICKET = "#EDE2C8"
LAMP_GLOW = "#E8D9A0"

# --- backdrop + plate -----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E8A9C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8DCE8", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(190,234,8),(804,230,7),(156,520,9),(840,544,8),
                               (250,766,7),(750,750,9),(132,390,6),(868,392,7),
                               (392,112,7),(614,110,8),(332,824,6),(670,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E6474", opacity=45, stroke=NONE)

# --- hallway floor: bottom segment closed on the disc's own arc ------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
# perspective boards converging on a vanishing point behind the ghost
for i, x in enumerate([220, 340, 660, 780]):
    d.path(f"M{x},700 L500,430", f"Floor board {i+1}", fill=NONE,
           stroke="#1A2430", strokeWidth=3, opacity=60)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E141E",
       strokeWidth=4, opacity=70)

# --- the ceiling lamp that lights nobody's responsibility ------------------------
d.path("M500,60 L500,108", "Lamp cord", fill=NONE, stroke="#0E141E",
       strokeWidth=4)
d.shape("ellipse", "Lamp shade", x=462, y=104, width=76, height=34,
        fill="#3A4A5E", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Lamp bulb", x=482, y=132, width=36, height=24,
        fill=LAMP_GLOW, stroke=INK, strokeWidth=4)
d.path("M470,150 L530,150 L640,330 L360,330 Z", "Lamp glow", fill=LAMP_GLOW,
       opacity=8, stroke=NONE)

# --- left door: NETWORK, declined politely ---------------------------------------
d.shape("rectangle", "Door L frame", x=176, y=298, width=160, height=350,
        fill="#5A6E82", stroke=INK, strokeWidth=5, radius=4)
d.shape("rectangle", "Door L", x=192, y=314, width=128, height=334,
        fill=DOOR_GRAD, stroke=INK, strokeWidth=5, radius=3)
d.shape("rectangle", "Door L panel", x=208, y=340, width=96, height=120,
        fill=NONE, stroke="#171F2B", strokeWidth=4, radius=4)
d.shape("rectangle", "Door L panel 2", x=208, y=486, width=96, height=120,
        fill=NONE, stroke="#171F2B", strokeWidth=4, radius=4)
d.shape("ellipse", "Knob L", x=298, y=470, width=16, height=16,
        fill="#8A9CAE", stroke=INK, strokeWidth=3)
# name plate
d.shape("rectangle", "Plate L", x=196, y=260, width=120, height=30,
        fill="#8A9CAE", stroke=INK, strokeWidth=4, radius=3)
d.text("NETWORK", "Dept L", x=256, y=281, size=15, font="Virelai Sans",
       color="#1E2430", justify="center")
# the written refusal, filed and dated, left at the threshold
d.path("M206,656 L268,656 L268,682 L206,682 Z", "Refusal L",
       fill="#D8CCB2", stroke=INK, strokeWidth=3, join="round")
d.path("M206,656 L237,672 L268,656", "Refusal L flap", fill=NONE,
       stroke="#8A7A5E", strokeWidth=3)
d.text("NO.", "Refusal L text", x=226, y=679, size=11, font="Virelai Sans",
       color="#7A6A4E", justify="left")

# --- right door: DEV, also declined ----------------------------------------------
d.shape("rectangle", "Door R frame", x=664, y=298, width=160, height=350,
        fill="#5A6E82", stroke=INK, strokeWidth=5, radius=4)
d.shape("rectangle", "Door R", x=680, y=314, width=128, height=334,
        fill=DOOR_GRAD, stroke=INK, strokeWidth=5, radius=3)
d.shape("rectangle", "Door R panel", x=696, y=340, width=96, height=120,
        fill=NONE, stroke="#171F2B", strokeWidth=4, radius=4)
d.shape("rectangle", "Door R panel 2", x=696, y=486, width=96, height=120,
        fill=NONE, stroke="#171F2B", strokeWidth=4, radius=4)
d.shape("ellipse", "Knob R", x=686, y=470, width=16, height=16,
        fill="#8A9CAE", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Plate R", x=684, y=260, width=120, height=30,
        fill="#8A9CAE", stroke=INK, strokeWidth=4, radius=3)
d.text("DEV", "Dept R", x=744, y=281, size=15, font="Virelai Sans",
       color="#1E2430", justify="center")
d.path("M732,656 L794,656 L794,682 L732,682 Z", "Refusal R",
       fill="#D8CCB2", stroke=INK, strokeWidth=3, join="round")
d.path("M732,656 L763,672 L794,656", "Refusal R flap", fill=NONE,
       stroke="#8A7A5E", strokeWidth=3)
d.text("NO.", "Refusal R text", x=752, y=679, size=11, font="Virelai Sans",
       color="#7A6A4E", justify="left")

# --- the 'progress' folder: forty-one quarters of dated refusals -------------------
d.path("M598,662 L622,662 L628,670 L676,670 L676,700 L598,700 Z",
       "Progress folder", fill="#C9B06A", stroke=INK, strokeWidth=4,
       join="round")
d.text("PROGRESS", "Folder label", x=606, y=690, size=11, font="Virelai Sans",
       color="#5A4A28", justify="left")

# --- Pending Jurisdiction: the ghost of a mandate ----------------------------------
d.shape("ellipse", "Ghost shadow", x=392, y=648, width=216, height=26,
        fill="#0A1018", opacity=40, stroke=NONE)
# sheet ghost: dome head, straight sides, scalloped hem — hovering
d.path("M500,310 C570,310 610,370 610,450 L610,598 "
       "C596,584 581,584 567,598 C553,584 538,584 524,598 "
       "C510,584 495,584 481,598 C467,584 452,584 438,598 "
       "C424,584 410,584 396,598 L396,450 C396,370 430,310 500,310 Z",
       "Ghost body", fill=GHOST_GRAD, stroke=INK, strokeWidth=6, opacity=86)
# spectral inner light
d.shape("ellipse", "Ghost glow", x=440, y=380, width=120, height=160,
        fill="#FFFFFF", opacity=16, stroke=NONE)
# hem shadow
d.path("M400,586 C440,574 560,574 606,586", "Hem shade", fill=NONE,
       stroke="#8AA0B2", strokeWidth=5, cap="round", opacity=50)

# the unassigned ticket: it has gone soft in its grip — drooping claim form
d.path("M414,486 C462,474 538,474 586,486 L580,548 C538,560 462,560 420,548 Z",
       "Ticket", fill=TICKET, stroke=INK, strokeWidth=4, join="round")
d.text("UNASSIGNED", "Ticket title", x=500, y=512, size=17,
       font="Virelai Sans", color="#5A4A34", justify="center")
d.path("M448,534 L552,534", "Owner line", fill=NONE, stroke="#8A7A5E",
       strokeWidth=3, opacity=70)
d.text("SIG: 0", "Sig count", x=452, y=530, size=12, font="Source Sans 3",
       color="#8A5A4A", justify="left")

# arms: two nubs holding the ticket edges
d.path("M400,470 C400,490 408,500 420,506", "Arm L", fill=NONE,
       stroke="#BCCBD8", strokeWidth=16, cap="round")
d.path("M600,470 C600,490 592,500 580,506", "Arm R", fill=NONE,
       stroke="#BCCBD8", strokeWidth=16, cap="round")
d.shape("ellipse", "Palm L", x=410, y=494, width=22, height=18,
        fill="#D4E0EA", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Palm R", x=568, y=494, width=22, height=18,
        fill="#D4E0EA", stroke=INK, strokeWidth=4)

# face: hollow eyes, small open mouth — no resentment, only the embargo
d.shape("ellipse", "Eye L", x=452, y=390, width=26, height=34,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=522, y=390, width=26, height=34,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Mouth", x=486, y=446, width=28, height=22,
        fill=INK, stroke=NONE, opacity=80)
d.shape("ellipse", "Eye hi L", x=458, y=396, width=8, height=10,
        fill="#E8F0F6", stroke=NONE, opacity=85)
d.shape("ellipse", "Eye hi R", x=528, y=396, width=8, height=10,
        fill="#E8F0F6", stroke=NONE, opacity=85)

# --- captions ----------------------------------------------------------------------
d.text("PENDING JURISDICTION", "Name", x=500, y=930, size=52,
       font="Virelai Sans", color="#C8DCE8", justify="center")
r = d.text("CERTIFIER OF NON-OWNERSHIP", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#92AAC0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("236.pending-jurisdiction-V1R00")
