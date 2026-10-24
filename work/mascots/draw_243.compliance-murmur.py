#!/usr/bin/env python3
"""Compliance Murmur — mascot portrait V1R00.
A soft figure murmuring assent at a conference table in the meeting's third
hour: fluorescent hum overhead, minutes already recording 'general assent',
the room too tired to fight. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Compliance Murmur — Mascot Portrait", 1000, 1000)

INK = "#241F16"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1B1812"}, {"offset": 1, "color": "#0D0B08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A8062"}, {"offset": 0.7, "color": "#5E5740"},
    {"offset": 1, "color": "#33301F"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A4532"}, {"offset": 1, "color": "#26231A"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#CFC3A4"}, {"offset": 0.72, "color": "#A2946F"},
    {"offset": 1, "color": "#6E6650"}]}}
TABLE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C4E3A"}, {"offset": 1, "color": "#3A3124"}]}}
SILH = "#2E2A1E"
PAGE = "#EDE3CC"
WAVE = "#D4B96A"
GLASS = "#B8C4B2"

# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#9A8E68", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4DAC0", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(182,240,8),(810,236,7),(150,520,9),(842,544,8),
                               (252,770,7),(748,756,9),(126,392,6),(868,396,7),
                               (386,112,7),(622,110,8),(336,826,6),(664,824,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6A6248", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#16130C",
       strokeWidth=4, opacity=70)

# --- fluorescent panel: the suite's own tired hum --------------------------------
d.shape("rectangle", "Light housing", x=368, y=118, width=264, height=30,
        fill="#4A4434", stroke=INK, strokeWidth=4, radius=8)
d.shape("rectangle", "Light tube", x=384, y=126, width=232, height=14,
        fill="#EFE8CE", stroke=NONE, radius=7)
d.shape("ellipse", "Light glow", x=340, y=110, width=320, height=52,
        fill="#F4ECD4", opacity=14, stroke=NONE)
# the hum it shares with the room — faint arcs beside the panel
for i, (x, w) in enumerate([(316, 28), (296, 20)]):
    d.path(f"M{x},{128} a{w},{w} 0 0 0 0,{20+i*8}", f"Hum arc L{i+1}",
           fill=NONE, stroke=WAVE, strokeWidth=3, cap="round", opacity=30)
for i, (x, w) in enumerate([(656, 28), (676, 20)]):
    d.path(f"M{x},{128} a{w},{w} 0 0 1 0,{20+i*8}", f"Hum arc R{i+1}",
           fill=NONE, stroke=WAVE, strokeWidth=3, cap="round", opacity=30)

# --- wall clock: no digits, only the hour the room stopped arguing --------------
d.shape("ellipse", "Clock", x=646, y=196, width=104, height=104,
        fill="#D8CFB6", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Clock face", x=656, y=206, width=84, height=84,
        fill="#CFC6AC", stroke="#8A8066", strokeWidth=2)
for i, (x1, y1, x2, y2) in enumerate([(698,210,698,222),(698,274,698,286),
                                      (660,248,672,248),(724,248,736,248)]):
    d.path(f"M{x1},{y1} L{x2},{y2}", f"Clock tick {i+1}", fill=NONE,
           stroke=INK, strokeWidth=3, cap="round")
d.path("M698,248 L698,222", "Minute hand", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M698,248 L678,248", "Hour hand", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.shape("ellipse", "Clock pin", x=693, y=243, width=10, height=10,
        fill=INK, stroke=NONE)

# --- the Murmur: soft, round, already agreeing ------------------------------------
d.shape("ellipse", "Murmur shadow", x=394, y=688, width=212, height=24,
        fill="#14100A", opacity=45, stroke=NONE)
# body: a pear that has sat too long
d.path("M500,420 C566,420 606,486 606,566 C606,640 566,690 500,690 "
       "C434,690 394,640 394,566 C394,486 434,420 500,420 Z",
       "Murmur body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body hi", x=430, y=470, width=110, height=48,
        fill="#FFFFFF", opacity=12, stroke=NONE)
# the suggestion of a collar long since wilted
d.path("M464,452 L500,482 L536,452", "Collar", fill=NONE, stroke="#5E563E",
       strokeWidth=8, cap="round", join="round")
d.shape("ellipse", "Collar pin", x=493, y=476, width=14, height=14,
        fill="#B8A266", stroke=INK, strokeWidth=3)

# head: round, compliant, under-caffeinated
d.path("M500,282 C556,282 590,322 590,370 C590,416 554,446 500,446 "
       "C446,446 410,416 410,370 C410,322 444,282 500,282 Z",
       "Head", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# sparse comb-over: three hairs doing governance
d.path("M452,300 C470,284 500,280 522,288", "Hair 1", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M478,290 C494,280 516,280 532,292", "Hair 2", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round", opacity=80)
# eyes: half-lidded, already past caring
d.path("M446,376 C454,384 466,384 474,376", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M526,376 C534,384 546,384 554,376", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M444,364 L476,364 M524,364 L556,364", "Lids", fill=NONE,
       stroke="#6A6044", strokeWidth=4, cap="round")
# the mouth: a small open 'm' mid-murmur
d.shape("ellipse", "Mouth", x=486, y=408, width=28, height=18,
        fill="#5E4A38", stroke=INK, strokeWidth=4)
# cheeks: the room's warmth, not its enthusiasm
d.shape("ellipse", "Cheek L", x=430, y=396, width=24, height=12,
        fill="#8A7A50", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=546, y=396, width=24, height=12,
        fill="#8A7A50", opacity=45, stroke=NONE)

# the murmur itself: three soft arcs leaving the mouth, belonging to no speaker
d.path("M536,404 a26,22 0 0 1 0,34", "Murmur arc 1", fill=NONE,
       stroke=WAVE, strokeWidth=4, cap="round", opacity=85)
d.path("M556,396 a40,34 0 0 1 0,52", "Murmur arc 2", fill=NONE,
       stroke=WAVE, strokeWidth=4, cap="round", opacity=60)
d.path("M578,388 a56,46 0 0 1 0,70", "Murmur arc 3", fill=NONE,
       stroke=WAVE, strokeWidth=3, cap="round", opacity=40)

# --- the conference table: the furniture of consensus ------------------------------
d.shape("ellipse", "Table top", x=160, y=618, width=680, height=44,
        fill="#6E5C44", stroke=INK, strokeWidth=5)
d.shape("rectangle", "Table front", x=180, y=640, width=640, height=120,
        fill=TABLE_GRAD, stroke=INK, strokeWidth=5, radius=6)
d.path("M180,690 L820,690", "Table groove", fill=NONE, stroke="#241E12",
       strokeWidth=3, opacity=60)

# the minutes: one page already recording the room's surrender
d.path("M556,606 L700,596 L706,660 L562,668 Z", "Minutes page",
       fill=PAGE, stroke=INK, strokeWidth=4, join="round")
d.text("MINUTES", "Minutes header", x=570, y=620, size=11,
       font="Virelai Sans", color="#8A7A5C", justify="left")
d.path("M568,630 L690,622 M570,638 L692,630", "Minutes rules", fill=NONE,
       stroke="#B4A488", strokeWidth=2, opacity=70)
d.text("GENERAL ASSENT", "Minutes verdict", x=572, y=656, size=10,
       font="Virelai Sans", color="#7A4A3A", justify="left")

# a paper cup nobody claimed
d.path("M336,600 L364,600 L360,646 L340,646 Z", "Cup", fill="#C9BCA0",
       stroke=INK, strokeWidth=4, join="round")
d.path("M338,612 L362,612", "Cup band", fill=NONE, stroke="#8A7A5C",
       strokeWidth=3, opacity=80)
d.shape("ellipse", "Cup sheen", x=340, y=602, width=10, height=36,
        fill="#FFFFFF", opacity=15, stroke=NONE)

# a laptop open to no one
d.path("M418,586 L492,586 L502,622 L408,622 Z", "Laptop lid",
       fill="#4E4636", stroke=INK, strokeWidth=4, join="round")
d.path("M428,594 L482,594 L488,614 L422,614 Z", "Laptop screen",
       fill="#8A8E7C", stroke=NONE)
d.path("M400,622 L512,622 L516,632 L396,632 Z", "Laptop base",
       fill="#5C5340", stroke=INK, strokeWidth=4, join="round")

# --- the room itself: two attendees slumped at the near edge ----------------------
# silhouettes in the foreground, the ones who stopped objecting — head + shoulders
d.path("M204,830 C204,780 232,752 262,752 C292,752 320,780 320,830 Z",
       "Attendee L shoulders", fill=SILH, stroke=INK, strokeWidth=5,
       opacity=92, join="round")
d.shape("ellipse", "Attendee L head", x=234, y=712, width=58, height=58,
        fill=SILH, stroke=INK, strokeWidth=5, opacity=92)
d.path("M244,726 C252,714 270,710 282,716", "Attendee L nod", fill=NONE,
       stroke="#4A4432", strokeWidth=3, cap="round", opacity=70)
d.path("M682,830 C682,780 710,752 742,752 C774,752 802,780 802,830 Z",
       "Attendee R shoulders", fill=SILH, stroke=INK, strokeWidth=5,
       opacity=92, join="round")
d.shape("ellipse", "Attendee R head", x=712, y=716, width=58, height=58,
        fill=SILH, stroke=INK, strokeWidth=5, opacity=92)
d.path("M762,730 C754,716 736,712 724,718", "Attendee R nod", fill=NONE,
       stroke="#4A4432", strokeWidth=3, cap="round", opacity=70)

# --- captions ---------------------------------------------------------------------
d.text("COMPLIANCE MURMUR", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E2D8C0", justify="center")
r = d.text("KEEPER OF THE UNMINUTED YES", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A89E80", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("243.compliance-murmur-V1R00")
