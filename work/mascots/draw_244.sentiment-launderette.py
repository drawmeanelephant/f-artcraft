#!/usr/bin/env python3
"""Sentiment Launderette — mascot portrait V1R00.
A front-loading launderette mascot mid-cycle: raw feedback forms tumbling in
the drum, the lint trap catching the grit the wash can't release. Dial eyes,
foam crown, a sound like closure. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Sentiment Launderette — Mascot Portrait", 1000, 1000)

INK = "#1E262C"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#121B21"}, {"offset": 1, "color": "#090E12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#71909C"}, {"offset": 0.7, "color": "#4C6873"},
    {"offset": 1, "color": "#27383F"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3C525A"}, {"offset": 1, "color": "#1E2C32"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DCE6E8"}, {"offset": 0.72, "color": "#A9BEC3"},
    {"offset": 1, "color": "#6E848B"}]}}
PANEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8FA6AC"}, {"offset": 1, "color": "#6E848B"}]}}
GLASS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#44606C"}, {"offset": 1, "color": "#18242B"}]}}
FOAM = "#CFE8EA"
PAGE = "#EFE8D2"
RAGE = "#B8544E"
WAVE = "#9FD4D8"

# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8FA8B0", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D8DC", strokeWidth=3, opacity=45)
for i, (x, y, w) in enumerate([(186,236,8),(806,232,7),(152,518,9),(840,542,8),
                               (248,768,7),(752,752,9),(128,390,6),(866,394,7),
                               (388,110,7),(618,108,8),(332,824,6),(666,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5A747E", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E161A",
       strokeWidth=4, opacity=70)

# --- stray bubbles: what escapes the drum ----------------------------------------
for i, (x, y, r) in enumerate([(706,238,10),(738,282,7),(682,300,6),
                               (252,318,8),(282,272,5)]):
    d.shape("ellipse", f"Bubble {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=NONE, stroke=FOAM, strokeWidth=2, opacity=40)
d.shape("ellipse", "Bubble hi 1", x=709, y=241, width=4, height=4,
        fill=FOAM, opacity=50, stroke=NONE)

# --- the Launderette: enamel body, dial eyes, foam crown --------------------------
d.shape("ellipse", "Mascot shadow", x=380, y=716, width=240, height=24,
        fill="#0C1418", opacity=50, stroke=NONE)
# feet
d.shape("rectangle", "Foot L", x=412, y=704, width=52, height=28,
        fill="#5E747B", stroke=INK, strokeWidth=4, radius=8)
d.shape("rectangle", "Foot R", x=536, y=704, width=52, height=28,
        fill="#5E747B", stroke=INK, strokeWidth=4, radius=8)
# body: the machine itself
d.shape("rectangle", "Body", x=370, y=395, width=260, height=320,
        fill=BODY_GRAD, stroke=INK, strokeWidth=6, radius=28)
d.shape("ellipse", "Body sheen", x=392, y=470, width=60, height=150,
        fill="#FFFFFF", opacity=10, stroke=NONE)

# control panel strip
d.shape("rectangle", "Panel", x=388, y=412, width=224, height=46,
        fill=PANEL_GRAD, stroke=INK, strokeWidth=4, radius=10)
# dial-eyes: needles resting low, mid-cycle patience
d.shape("ellipse", "Dial L", x=424, y=418, width=34, height=34,
        fill="#E4ECEE", stroke=INK, strokeWidth=4)
d.path("M441,435 L433,443", "Dial L needle", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.shape("ellipse", "Dial R", x=542, y=418, width=34, height=34,
        fill="#E4ECEE", stroke=INK, strokeWidth=4)
d.path("M559,435 L551,443", "Dial R needle", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
# the cycle-end light: lit, patient, unapologetic
d.shape("ellipse", "Cycle light", x=493, y=428, width=14, height=14,
        fill="#D8A85C", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Cycle glow", x=486, y=421, width=28, height=28,
        fill="#E8C884", opacity=30, stroke=NONE)
# a sound like closure — two faint arcs off the light
d.path("M514,424 a14,12 0 0 1 0,18", "Tone arc 1", fill=NONE, stroke=WAVE,
       strokeWidth=3, cap="round", opacity=70)
d.path("M524,418 a22,20 0 0 1 0,28", "Tone arc 2", fill=NONE, stroke=WAVE,
       strokeWidth=3, cap="round", opacity=45)
# mouth: the grille of small vents
for i, x in enumerate([488, 499, 510]):
    d.path(f"M{x},466 L{x},478", f"Grille {i+1}", fill=NONE, stroke=INK,
           strokeWidth=4, cap="round")

# foam crown: suds that never quite settle
for i, (x, y, r) in enumerate([(430,382,20),(470,372,24),(514,376,22),
                               (552,384,18),(410,392,14),(586,396,12)]):
    d.shape("ellipse", f"Suds {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=FOAM, stroke=INK, strokeWidth=4)
for i, (x, y, r) in enumerate([(436,386,6),(476,376,7),(520,380,6)]):
    d.shape("ellipse", f"Suds hi {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill="#FFFFFF", opacity=45, stroke=NONE)

# porthole: the drum, mid-turn
d.shape("ellipse", "Porthole ring", x=410, y=478, width=180, height=180,
        fill="#2A363C", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Porthole glass", x=424, y=492, width=152, height=152,
        fill=GLASS_GRAD, stroke="#10181C", strokeWidth=3)
# drum ribs inside
for ang_cx, ang_cy, w, h, deg in [(500,568,120,10,30),(500,568,120,10,150),
                                  (500,568,120,10,270)]:
    d.path(rot_rect_path(ang_cx, ang_cy, w, h, deg),
           f"Drum rib {deg}", fill="#26363E", stroke=NONE, opacity=70)
# tumbling feedback forms — the raw input, mid-cycle
d.path(rot_rect_path(500,540,52,64,-28), "Form 1", fill=PAGE,
       stroke=INK, strokeWidth=3, join="round")
d.path(rot_rect_path(468,590,48,58,18), "Form 2", fill="#DED4B8",
       stroke=INK, strokeWidth=3, join="round")
d.path(rot_rect_path(534,586,44,54,55), "Form 3", fill=PAGE,
       stroke=INK, strokeWidth=3, join="round")
# the wash motion itself
d.path("M446,540 a56,56 0 0 1 96,30", "Drum motion", fill=NONE,
       stroke=WAVE, strokeWidth=4, cap="round", opacity=45)
# suds pooled in the drum floor
d.path("M436,606 a64,40 0 0 0 128,0 Z", "Drum foam", fill=FOAM,
       stroke=NONE, opacity=55)
d.shape("ellipse", "Glass sheen", x=440, y=500, width=56, height=28,
        fill="#FFFFFF", opacity=16, stroke=NONE)
# hinge nubs
d.shape("ellipse", "Hinge", x=412, y=550, width=14, height=36,
        fill="#5E747B", stroke=INK, strokeWidth=3)

# left arm: pouring the measure that starts the cycle
d.path("M378,536 C352,522 332,506 320,486", "Arm L", fill=NONE,
       stroke="#7E9298", strokeWidth=16, cap="round")
d.shape("ellipse", "Palm L", x=296, y=462, width=30, height=24,
        fill="#A9BEC3", stroke=INK, strokeWidth=4)
# the detergent scoop, tipped
d.path("M268,446 L312,452 L306,486 L262,478 Z", "Scoop cup", fill="#8FA6AC",
       stroke=INK, strokeWidth=4, join="round")
d.path("M270,448 L310,454", "Scoop rim", fill=NONE, stroke="#5E747B",
       strokeWidth=3)
# powder falling — measured, never hurried
for i, (x, y, r) in enumerate([(296,494,3),(306,512,2),(290,522,2)]):
    d.shape("ellipse", f"Powder {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill="#E4ECEE", opacity=70, stroke=NONE)

# lint trap: the only part of the system that fills — drawer pulled out
d.path("M544,650 L606,650 L606,660 L544,660 Z", "Trap slot",
       fill="#14202A", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Trap drawer", x=538, y=658, width=72, height=44,
        fill=PANEL_GRAD, stroke=INK, strokeWidth=4, radius=5)
d.path("M548,672 L600,672 M548,682 L600,682 M548,692 L600,692",
       "Trap grille", fill=NONE, stroke="#3E545C", strokeWidth=2,
       opacity=80)
# the grit it caught: dark specks + one pointy scrap of rage
for i, (x, y, r) in enumerate([(552,646,3),(566,643,2),(582,647,3),
                               (596,644,2)]):
    d.shape("ellipse", f"Grit {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill="#2A2018", stroke=NONE)
d.path("M556,650 L566,640 L574,650 L584,638 L592,648", "Rage scrap",
       fill=NONE, stroke=RAGE, strokeWidth=4, cap="round", join="round")
# right arm: the hand that empties it on a schedule nobody recorded
d.path("M622,576 C640,610 630,646 610,668", "Arm R", fill=NONE,
       stroke="#7E9298", strokeWidth=16, cap="round")
d.shape("ellipse", "Palm R", x=596, y=662, width=26, height=20,
        fill="#A9BEC3", stroke=INK, strokeWidth=4)

# floor foam: what the room mops up later
d.shape("ellipse", "Floor foam", x=390, y=722, width=220, height=26,
        fill=FOAM, opacity=30, stroke=NONE)
for i, (x, y, r) in enumerate([(628,714,8),(652,722,6),(370,720,7)]):
    d.shape("ellipse", f"Floor bubble {i+1}", x=x, y=y, width=r*2, height=r*2,
            fill=NONE, stroke=FOAM, strokeWidth=2, opacity=45)

# --- captions ---------------------------------------------------------------------
d.text("SENTIMENT LAUNDERETTE", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#DCE8EA", justify="center")
r = d.text("A SOUND LIKE CLOSURE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9FB8BE", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("244.sentiment-launderette-V1R00")
