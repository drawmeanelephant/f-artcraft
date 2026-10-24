#!/usr/bin/env python3
"""Canon Dust Deputy — mascot portrait V1R00.
A dust-bunny deputy on a weekly round it was never assigned, feather-dusting
a dead hyperlink in a forgotten appendix. Its badge is drawn in the dust;
it will be gone by noon and re-drawn anyway. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Canon Dust Deputy — Mascot Portrait", 1000, 1000)

INK = "#262230"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A1A24"}, {"offset": 1, "color": "#0B0B10"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#746E84"}, {"offset": 0.7, "color": "#4A4458"},
    {"offset": 1, "color": "#211E2B"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#463F54"}, {"offset": 1, "color": "#1D1A26"}]}}
PAGE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E0D4B0"}, {"offset": 1, "color": "#B0A280"}]}}
PAGE_DK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C4B48E"}, {"offset": 1, "color": "#8E8062"}]}}
DUST = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B4AC9E"}, {"offset": 0.72, "color": "#8A8274"},
    {"offset": 1, "color": "#5E584C"}]}}
HAT = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#8A6E4C"}, {"offset": 1, "color": "#54401F"}]}}
SHELF = "#332D42"
LINK_BLUE = "#7A8AA6"
DUST_PALE = "#C8C0AC"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A829E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8D2E2", strokeWidth=3, opacity=45)
# archive gloom: the appendix is not lit for visitors
d.shape("ellipse", "Shelf gloom", x=190, y=140, width=620, height=560,
        fill="#D8CCA8", opacity=7, stroke=NONE)
for i, (x, y, w) in enumerate([(190,230,8),(804,232,7),(158,516,9),(836,540,8),
                               (252,764,7),(750,746,9),(134,388,6),(864,390,7),
                               (394,112,7),(612,110,8),(334,820,6),(668,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E586E", opacity=45, stroke=NONE)
# dust motes: the jurisdiction itself
for i, (x, y, w) in enumerate([(262,290,6),(740,272,8),(330,210,5),(676,214,6),
                               (506,186,5),(230,436,6),(774,444,7),(300,340,5),
                               (706,348,5),(560,300,4)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill=DUST_PALE, opacity=32, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc -------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#14111C",
       strokeWidth=4, opacity=70)

# --- the stacks around it: volumes nobody has opened ------------------------------
d.path("M196,698 L206,470 L244,468 L236,698 Z", "Lean 1",
       fill=SHELF, stroke=INK, strokeWidth=4, join="round", opacity=85)
d.path("M232,698 L252,505 L286,512 L268,698 Z", "Lean 2",
       fill=SHELF, stroke=INK, strokeWidth=4, join="round", opacity=80)
d.path("M168,698 L176,528 L204,526 L198,698 Z", "Lean 3",
       fill=SHELF, stroke=INK, strokeWidth=4, join="round", opacity=75)
d.path("M208,496 L240,494 M206,640 L238,638 M252,540 L280,546",
       "Spine bands", fill=NONE, stroke="#4E4662", strokeWidth=4,
       cap="round", opacity=70)
d.path("M708,658 L808,654 L812,676 L706,680 Z", "Stack 1",
       fill=SHELF, stroke=INK, strokeWidth=4, join="round", opacity=85)
d.path("M720,634 L800,632 L806,654 L716,656 Z", "Stack 2",
       fill=SHELF, stroke=INK, strokeWidth=4, join="round", opacity=80)
d.path("M732,612 L792,612 L798,632 L728,634 Z", "Stack 3",
       fill=SHELF, stroke=INK, strokeWidth=4, join="round", opacity=75)
d.path("M714,662 L806,658 M724,638 L798,636", "Stack bands", fill=NONE,
       stroke="#4E4662", strokeWidth=4, cap="round", opacity=70)
# a web in the stacks' corner: the archive's own filing system
d.path("M812,224 C800,264 796,304 802,344 M786,206 C780,252 778,296 784,334",
       "Web strands", fill=NONE, stroke="#E8E2D0", strokeWidth=2.5,
       cap="round", opacity=30)

# --- the forgotten appendix: open to the page nobody cites --------------------------
d.shape("ellipse", "Book shadow", x=290, y=676, width=420, height=22,
        fill="#0C0A12", opacity=50, stroke=NONE)
# cover boards peeking past the pages
d.path("M300,556 L498,538 L498,582 L300,592 Z", "Cover L",
       fill="#4E4258", stroke=INK, strokeWidth=4, join="round")
d.path("M498,538 L700,556 L700,592 L498,582 Z", "Cover R",
       fill="#4E4258", stroke=INK, strokeWidth=4, join="round")
# page block
d.path("M310,548 C365,536 445,530 498,538 L498,680 C440,674 365,672 310,682 Z",
       "Page L", fill=PAGE, stroke=INK, strokeWidth=4, join="round")
d.path("M498,538 C555,530 635,536 690,548 L690,682 C635,672 555,674 498,680 Z",
       "Page R", fill=PAGE_DK, stroke=INK, strokeWidth=4, join="round")
d.path("M498,538 L498,680", "Spine crease", fill=NONE, stroke=INK,
       strokeWidth=4, opacity=60)
# appendix type: dense small rules, unreferenced for decades
for i in range(5):
    y = 562 + i*18
    d.path(f"M330,{y} L470,{y-5}", f"Left rule {i+1}", fill=NONE,
           stroke="#8E8062", strokeWidth=3, opacity=55)
for i in range(5):
    y = 562 + i*18
    d.path(f"M528,{y-5} L664,{y}", f"Right rule {i+1}", fill=NONE,
           stroke="#7E7050", strokeWidth=3, opacity=55)
# the corner cobweb: the appendix's only footnote
d.path("M672,546 C654,564 646,584 648,606 M690,564 C670,574 658,590 656,612 "
       "M686,588 C672,596 662,608 660,626", "Cobweb", fill=NONE,
       stroke="#E8E2D0", strokeWidth=2.5, cap="round", opacity=45)

# --- the dead hyperlink: decommissioned, dusted weekly, load-bearing ----------------
# the link glyph: two chain rings gone grey, still underlined
d.shape("ellipse", "Link ring A", x=552, y=560, width=66, height=46,
        fill=NONE, stroke=LINK_BLUE, strokeWidth=8)
d.shape("ellipse", "Link ring B", x=596, y=586, width=66, height=46,
        fill=NONE, stroke=LINK_BLUE, strokeWidth=8)
d.path("M550,650 L676,650", "Link underline", fill=NONE, stroke=LINK_BLUE,
       strokeWidth=5, cap="round", opacity=80)
# the crack through it: the destination that isn't there
d.path("M608,564 L598,586 L612,598 L602,622", "Link crack", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round", join="round", opacity=70)
# dust film settling over the monument
d.path("M548,556 C584,548 640,550 672,562 L672,652 C640,644 584,642 548,650 Z",
       "Dust film", fill=DUST_PALE, opacity=20, stroke=NONE)

# --- the Deputy: fluff with authority ----------------------------------------------
d.shape("ellipse", "Deputy shadow", x=322, y=650, width=180, height=18,
        fill="#0C0A12", opacity=45, stroke=NONE)
# dust-bunny body: a scalloped blob of accumulated jurisdiction
d.path("M355,639 C326,629 314,603 321,581 C309,565 314,538 333,529 "
       "C329,509 340,488 362,485 C365,464 386,452 408,459 "
       "C415,440 441,435 458,449 C477,445 494,461 492,481 "
       "C511,488 518,509 509,526 C523,541 525,565 511,579 "
       "C518,598 509,622 487,629 C482,649 461,658 441,651 "
       "C422,663 396,661 384,646 C372,653 357,651 355,639 Z",
       "Deputy body", fill=DUST, stroke=INK, strokeWidth=5, join="round")
# inner fluff: the loose structure of lore
for i, (x, y, r) in enumerate([(370,540,20),(418,505,22),(445,555,18),
                               (385,585,17),(458,520,16)]):
    d.path(f"M{x},{y} C{x+9},{y-r//3} {x+r},{y-r//3} {x+r},{y+r//4}",
           f"Fluff {i+1}", fill=NONE, stroke="#6E6858", strokeWidth=3,
           cap="round", opacity=55)
# the badge: drawn in the dust this morning, translucent, already fading
pts = []
for i in range(12):
    a = math.radians(-90 + i*30)
    rr = 30 if i % 2 == 0 else 15
    pts.append(f"{400+rr*math.cos(a):.1f},{562+rr*math.sin(a):.1f}")
d.path("M" + " L".join(pts) + " Z", "Dust badge", fill=DUST_PALE,
       stroke=INK, strokeWidth=3, opacity=60, join="round")
# face: round eyes the color of settled authority
d.shape("ellipse", "Eye L", x=398, y=496, width=17, height=20,
        fill="#2E2A34", stroke=NONE)
d.shape("ellipse", "Eye R", x=434, y=496, width=17, height=20,
        fill="#2E2A34", stroke=NONE)
d.shape("ellipse", "Glint L", x=401, y=499, width=6, height=6,
        fill="#FFF", opacity=80, stroke=NONE)
d.shape("ellipse", "Glint R", x=437, y=499, width=6, height=6,
        fill="#FFF", opacity=80, stroke=NONE)
# level deputy mouth
d.path("M408,530 C416,535 428,535 436,530", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# hat: regulation, older than the registry that issued it
d.path("M395,462 C420,445 475,440 508,452 C513,442 505,425 482,420 "
       "C457,416 430,421 417,434 C405,446 398,455 395,462 Z",
       "Hat crown", fill=HAT, stroke=INK, strokeWidth=5, join="round")
d.path("M378,466 C415,450 490,445 525,458 C533,466 528,474 513,476 "
       "C470,470 415,474 385,480 C373,477 370,471 378,466 Z",
       "Hat brim", fill=HAT, stroke=INK, strokeWidth=5, join="round")
d.path("M428,435 C445,426 470,424 486,429", "Hat dent", fill=NONE,
       stroke="#3E2E14", strokeWidth=3, cap="round", opacity=70)

# --- the duster: equipment never assigned, deployed anyway --------------------------
d.path("M505,568 L578,543", "Duster handle", fill=NONE, stroke="#8A6E4C",
       strokeWidth=7, cap="round")
# feather plume: three soft sweeps aimed at the dead link
d.path("M578,545 C602,524 624,514 647,512 C634,528 618,540 598,548 Z",
       "Plume 1", fill="#D8D2C4", stroke=INK, strokeWidth=3, join="round")
d.path("M578,545 C606,538 630,538 650,545 C634,554 614,558 596,556 Z",
       "Plume 2", fill="#C4BDB0", stroke=INK, strokeWidth=3, join="round")
d.path("M578,545 C600,554 618,564 630,576 C612,578 594,572 582,562 Z",
       "Plume 3", fill="#B0A89A", stroke=INK, strokeWidth=3, join="round")
# raised dust: two faint streaks where the plume has just passed
d.path("M646,552 C664,546 680,546 694,550", "Dust streak 1", fill=NONE,
       stroke=DUST_PALE, strokeWidth=4, cap="round", opacity=35)
d.path("M650,578 C666,574 680,575 692,579", "Dust streak 2", fill=NONE,
       stroke=DUST_PALE, strokeWidth=4, cap="round", opacity=28)

# --- captions -----------------------------------------------------------------------
d.text("CANON DUST DEPUTY", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#DDD6E4", justify="center")
r = d.text("THE DUST IS LOAD-BEARING", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A49CB8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("250.canon-dust-deputy-V1R00")
