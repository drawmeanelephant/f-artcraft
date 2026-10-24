#!/usr/bin/env python3
"""Footnote Pallbearer — mascot portrait V1R00.
A small somber pallbearer in a top hat crosses the face of a document,
shouldering a pole from which a tiny coffin hangs — the coffin marked with
the amber asterisk it was lowered by. One body-text line shows the gap the
fact was lifted from. At the bottom margin waits the separator rule and the
footnote, set at a true 8pt. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Footnote Pallbearer — Mascot Portrait", 1000, 1000)

INK = "#221C26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#121624"}, {"offset": 1, "color": "#07090F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E778C"}, {"offset": 0.7, "color": "#4A5162"},
    {"offset": 1, "color": "#282C3A"}]}}
PAGE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2EAD6"}, {"offset": 1, "color": "#D6CAAC"}]}}
COAT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E3450"}, {"offset": 1, "color": "#221A30"}]}}
RULE = "#8E8672"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#9AA0B8", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8DCEA", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3E4456", opacity=50, stroke=NONE)

# --- the document --------------------------------------------------------------
d.shape("ellipse", "Page shadow", x=252, y=762, width=520, height=34,
        fill="#0A0C12", opacity=40, stroke=NONE)
d.shape("rectangle", "Page", x=240, y=140, width=520, height=620,
        fill=PAGE_GRAD, stroke=INK, strokeWidth=6, radius=8)
# faint dog-ear, top right
d.path("M714,140 L760,140 L760,186 Z", "Dog ear", fill="#C8BC9C",
       stroke=INK, strokeWidth=3)

# body text — three paragraphs of ruled lines
for j, y0 in enumerate([196, 322, 472]):
    for i, w in enumerate([420, 420, 420, 300]):
        if j == 2 and i == 3:
            continue
        y = y0 + i * 26
        d.path(f"M290,{y} L{290+w},{y}", f"Body {j+1}.{i+1}", fill=NONE,
               stroke=RULE, strokeWidth=7, cap="round", opacity=75)
# paragraph 2, line 3 carries the gap where the fact was lifted
y = 322 + 2 * 26
d.path(f"M290,{y} L470,{y} M560,{y} L710,{y}", "Body 2.3 split", fill=NONE,
       stroke=RULE, strokeWidth=7, cap="round", opacity=75)
# the asterisk ghost left behind + hairline tear
d.path("M502,368 L502,386 M494,373 L510,383 M510,373 L494,383",
       "Mark ghost", fill=NONE, stroke="#B8AE94", strokeWidth=2.5,
       cap="round", opacity=80)
d.path("M472,377 L490,377 M562,377 L580,377", "Torn ends", fill=NONE,
       stroke="#B0A68C", strokeWidth=2, cap="round", opacity=60)

# drop cap-ish margin asterisk at paragraph 3 — another burial pending
d.path("M262,452 L262,470 M254,457 L270,467 M270,457 L254,467",
       "Pending mark", fill=NONE, stroke="#C8B06A", strokeWidth=3.5,
       cap="round", opacity=85)

# --- the footnote zone: separator + true 8pt --------------------------------------
d.path("M290,676 L400,676", "Separator rule", fill=NONE, stroke=INK,
       strokeWidth=3, opacity=85)
d.text("*1 the fact remains cited; the room was lost.", "Footnote",
       x=290, y=700, size=8, font="Source Sans 3", color="#6E6858")
d.text("*2 too loud at ten point.", "Footnote 2", x=290, y=714, size=8,
       font="Source Sans 3", color="#6E6858")

# --- the pallbearer, mid-stride down the page ---------------------------------------
d.shape("ellipse", "Bearer shadow", x=560, y=646, width=110, height=16,
        fill="#8A8068", opacity=45, stroke=NONE)
# legs mid-stride
d.path("M604,622 L596,650 M626,622 L638,648", "Legs", fill=NONE,
       stroke="#1C1428", strokeWidth=9, cap="round")
d.path("M590,650 L604,650 M632,648 L646,648", "Shoes", fill=NONE,
       stroke="#1C1428", strokeWidth=7, cap="round")
# coat: a solemn little bell
d.path("M588,628 C582,588 584,552 596,536 L634,536 C646,552 650,588 644,628 "
       "C630,636 600,636 588,628 Z", "Coat", fill=COAT_GRAD,
       stroke=INK, strokeWidth=5)
d.path("M596,544 L592,620", "Coat seam", fill=NONE, stroke="#181224",
       strokeWidth=3, opacity=60)
d.shape("ellipse", "Coat sheen", x=596, y=548, width=24, height=50,
        fill="#FFFFFF", opacity=8, stroke=NONE)
# collar
d.path("M598,538 L615,552 L632,538 L626,530 L604,530 Z", "Collar",
       fill="#4A3E60", stroke=INK, strokeWidth=3.5)
# head, slightly bowed
d.shape("ellipse", "Head", x=598, y=496, width=34, height=34,
        fill="#E8D8BC", stroke=INK, strokeWidth=4.5)
d.path("M606,516 C610,519 614,519 618,516", "Eyes shut", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
d.path("M609,523 C613,525 617,525 621,523", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=2.5, cap="round")
# top hat, tipped low
d.shape("rectangle", "Hat crown", x=600, y=468, width=30, height=30,
        fill="#241C30", stroke=INK, strokeWidth=4, radius=4)
d.shape("ellipse", "Hat brim", x=590, y=494, width=50, height=10,
        fill="#241C30", stroke=INK, strokeWidth=4)
d.path("M600,492 L630,492", "Hat band", fill=NONE, stroke="#4A3E60",
       strokeWidth=4)

# the shoulder pole, sloped like a casket handle
d.path("M588,546 L676,492", "Pole", fill=NONE, stroke="#4E3A28",
       strokeWidth=7, cap="round")
d.path("M600,540 L610,534", "Grip", fill=NONE, stroke="#8A7452",
       strokeWidth=3, cap="round")
# cord from the pole tip down to the coffin
d.path("M676,492 C678,504 678,514 676,524", "Cord", fill=NONE,
       stroke="#5E5038", strokeWidth=3, cap="round")

# the little coffin: the deceased footnote, asterisk-marked
d.path("M658,524 L694,524 L700,548 L686,574 L666,574 L652,548 Z",
       "Coffin", fill="#2E2238", stroke=INK, strokeWidth=4)
d.path("M662,532 L690,532", "Coffin lid seam", fill=NONE, stroke="#4A3A58",
       strokeWidth=3, opacity=80)
# the amber asterisk it was lowered by
d.path("M676,540 L676,560 M666,545 L686,555 M686,545 L666,555",
       "The asterisk", fill=NONE, stroke="#E8A84A", strokeWidth=4,
       cap="round")
d.shape("ellipse", "Asterisk glint", x=683, y=536, width=8, height=8,
        fill="#F4D08E", opacity=80, stroke=NONE)

# --- dim votive specks around the page ------------------------------------------------
for i, (x, y, w) in enumerate([(210,300,5),(790,320,4),(200,540,5),(800,520,4),
                               (300,110,4),(700,105,5),(400,810,4),(620,810,5)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8D0E4", opacity=40, stroke=NONE)

# --- captions ---------------------------------------------------------------------------
d.text("FOOTNOTE PALLBEARER", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E8EAF2", justify="center")
r = d.text("CARRIER OF DEAD CONTEXT", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#AEB4C8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("261.footnote-pallbearer-V1R00")
