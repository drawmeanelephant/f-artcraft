#!/usr/bin/env python3
"""Pleading Margin — mascot portrait V1R00.
A typeset intake form, perfect and unbothered, while a desperate plea in blue
pen climbs out of the bottom margin, up the side, and curls under the fields.
Tearstains on the page. 1000x1000. Gradients + translucent shading, never flat."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Pleading Margin — Mascot Portrait", 1000, 1000)

INK = "#33292B"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A2530"}, {"offset": 1, "color": "#080D13"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5E7284"}, {"offset": 0.7, "color": "#3A4A58"},
    {"offset": 1, "color": "#1E2A34"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F6EFDC"}, {"offset": 0.6, "color": "#EDE2C6"},
    {"offset": 1, "color": "#DCCDA9"}]}}
TYPE = "#6A6E78"        # typeset grey ink
RULE = "#9AA4AE"        # ruled lines
PEN = "#2B4CC4"         # ballpoint blue
PEN_DK = "#1E3590"
STAMP = "#A85048"
TEAR = "#8FB4CC"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A8FA0", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D6DE", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E5464", opacity=45, stroke=NONE)

# --- the form -------------------------------------------------------------------
d.shape("rectangle", "Paper shadow", x=312, y=128, width=408, height=560,
        fill="#060A0E", opacity=45, stroke=NONE, radius=6)
d.shape("rectangle", "Form", x=300, y=115, width=400, height=560,
        fill=PAPER, stroke=INK, strokeWidth=5, radius=3)
# header
d.text("BUREAU OF CONTINUITY", "Form bureau", x=335, y=152, size=15,
       font="American Typewriter", color=TYPE, justify="left")
d.text("FORM XII-C — SERVICE REQUEST", "Form title", x=335, y=174, size=17,
       font="American Typewriter", color="#4A4E58", justify="left")
d.path("M330,190 L670,190 M330,195 L670,195", "Header rules", fill=NONE,
       stroke=TYPE, strokeWidth=2, opacity=80)
# fields: label + ruled answer line
for i, label in enumerate(["NAME", "ACCOUNT", "REQUEST", "JUSTIFICATION"]):
    y = 235 + i * 52
    d.text(label, f"Field {label}", x=335, y=y, size=13,
           font="American Typewriter", color=TYPE, justify="left")
    lx = 335 + len(label) * 8.4 + 14
    d.path(f"M{lx:.0f},{y+2} L668,{y+2}", f"Rule {label}", fill=NONE,
           stroke=RULE, strokeWidth=2, opacity=85)
# ruled writing lines, lower half
for i in range(4):
    y = 470 + i * 34
    d.path(f"M335,{y} L668,{y}", f"Blank rule {i+1}", fill=NONE,
           stroke=RULE, strokeWidth=2, opacity=60)
# checkbox row
for i, label in enumerate(["APPROVED", "DENIED"]):
    x = 335 + i * 160
    d.shape("rectangle", f"Box {label}", x=x, y=615, width=16, height=16,
            fill=NONE, stroke=TYPE, strokeWidth=2)
    d.text(label, f"Box label {label}", x=x+24, y=629, size=12,
           font="American Typewriter", color=TYPE, justify="left")
# faint typeset footer
d.text("DO NOT WRITE IN THIS SPACE", "Form warning", x=335, y=650, size=11,
       font="American Typewriter", color="#9A9484", justify="left")

# DENIED stamp, faded red, rotated on the lower half
st = d.shape("rectangle", "Denied frame", x=470, y=545, width=190, height=58,
             fill=NONE, stroke=STAMP, strokeWidth=6, radius=8, opacity=55)
tx = d.text("DENIED", "Denied word", x=487, y=585, size=38,
            font="American Typewriter", color=STAMP, justify="left")
for obj, nm in [(st, "stamp frame rot"), (tx, "stamp word rot")]:
    if obj and obj.get("id"):
        d.cmd("object.rotate", nm, ids=[obj["id"]], angle=-13,
              origin=[565, 574])
        d.cmd("object.setProps", nm + " fade", ids=[obj["id"]], opacity=52)

# --- the plea: blue pen, climbing the margin --------------------------------------
# first line along the bottom margin, nearly level — inside the paper edge
p1 = d.text("please do not", "Plea 1", x=352, y=670, size=20,
            font="Bradley Hand", color=PEN, justify="left")
if p1 and p1.get("id"):
    d.cmd("object.rotate", "plea1 rot", ids=[p1["id"]], angle=-4,
          origin=[425, 663])
# second line runs straight up the right margin
p2 = d.text("shut off the", "Plea 2", x=692, y=612, size=23,
            font="Bradley Hand", color=PEN, justify="left")
if p2 and p2.get("id"):
    d.cmd("object.rotate", "plea2 rot", ids=[p2["id"]], angle=88,
          origin=[692, 612])
# the last word, biggest, continuing the climb
p3 = d.text("POWER", "Plea 3", x=694, y=430, size=34,
            font="Bradley Hand", color=PEN_DK, justify="left")
if p3 and p3.get("id"):
    d.cmd("object.rotate", "plea3 rot", ids=[p3["id"]], angle=84,
          origin=[694, 430])
# pressure strokes: double underline running beside the climb, frantic
d.path("M652,600 C648,540 646,470 650,400 M660,606 C656,546 654,478 658,412",
       "Climb underlines", fill=NONE, stroke=PEN_DK, strokeWidth=3,
       cap="round", opacity=85)
# exclamation scribble at the top of the climb, still on paper
d.path("M672,214 C674,200 676,186 678,175 M679,162 L680,158",
       "Exclamation", fill=NONE, stroke=PEN_DK, strokeWidth=4, cap="round")
# curl under the last field: the plea reaching into the ruled area
d.path("M606,668 C634,656 654,646 662,634 C666,624 658,618 648,622",
       "Plea curl", fill=NONE, stroke=PEN, strokeWidth=3, cap="round",
       opacity=80)
# a second, fainter pass — the pen pressing two sheets down
d.path("M366,668 C414,660 474,658 534,662", "Plea ghost", fill=NONE,
       stroke=PEN, strokeWidth=2, cap="round", opacity=30)
# small arrow from margin to the DENIED box
d.path("M560,668 C574,650 586,638 596,630 M596,630 L590,642 M596,630 L584,634",
       "Plea arrow", fill=NONE, stroke=PEN, strokeWidth=3, cap="round",
       opacity=85)
# cross-out scribble over the signature line corner
d.path("M620,556 C636,548 652,546 668,550 M622,562 C640,556 654,554 666,556",
       "Margin scratch", fill=NONE, stroke=PEN, strokeWidth=2.5,
       cap="round", opacity=55)

# --- tearstains -------------------------------------------------------------------
# big stain where the plea gathers, lower right of the page
d.shape("ellipse", "Tear 1 outer", x=585, y=560, width=110, height=86,
        fill=TEAR, opacity=14, stroke=NONE)
d.shape("ellipse", "Tear 1 lobe", x=630, y=590, width=64, height=52,
        fill=TEAR, opacity=12, stroke=NONE)
d.path("M596,576 C606,560 636,554 662,560 C690,566 700,588 690,606 C680,624 648,632 622,626 C600,620 588,596 596,576 Z",
       "Tear 1 rim", fill=NONE, stroke=TEAR, strokeWidth=2.5, opacity=30)
# a thinner trail running down from it
d.path("M640,646 C644,662 642,676 638,688 C636,694 632,698 630,700",
       "Tear trail", fill=NONE, stroke=TEAR, strokeWidth=5, cap="round",
       opacity=16)
# older stain, upper left over the NAME field
d.shape("ellipse", "Tear 2 outer", x=420, y=200, width=86, height=66,
        fill=TEAR, opacity=10, stroke=NONE)
d.path("M430,214 C440,202 466,198 486,204 C502,210 506,226 496,238 C484,250 456,252 440,244 C428,236 424,224 430,214 Z",
       "Tear 2 rim", fill=NONE, stroke=TEAR, strokeWidth=2, opacity=22)

# --- captions ------------------------------------------------------------------
d.text("PLEADING MARGIN", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E8E0C8", justify="center")
r = d.text("UNTRANSCRIBED MARGINALIA", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9FB4C0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("316.pleading-margin-V1R00")
