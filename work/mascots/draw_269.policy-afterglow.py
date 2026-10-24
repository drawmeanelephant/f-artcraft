#!/usr/bin/env python3
"""Policy Afterglow — mascot portrait V1R00.
A mascot standing beside a slide deck that still glows with launch-day
optimism; phosphor lettering on the war-room wall behind; crashed servers
and small electrical fires doing the actual illuminating. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Policy Afterglow — Mascot Portrait", 1000, 1000)

INK = "#2C1E14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#101410"}, {"offset": 1, "color": "#070907"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5C5E4E"}, {"offset": 0.7, "color": "#424436"},
    {"offset": 1, "color": "#26281E"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4038"}, {"offset": 1, "color": "#1C1E18"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C0A87E"}, {"offset": 0.7, "color": "#9A825C"},
    {"offset": 1, "color": "#74603F"}]}}
RACK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#343A3E"}, {"offset": 1, "color": "#1C2022"}]}}
PHOS = "#9FE0AC"      # phosphor lettering
PHOS_DIM = "#6FA87C"
SCREEN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EAF4DC"}, {"offset": 1, "color": "#B8CFA0"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A8A70", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DAD8BC", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#484C3C", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#101208",
       strokeWidth=4, opacity=70)

# --- phosphor lettering on the wall: PARADIGM, SHIFT ------------------------------
d.shape("ellipse", "Phosphor haze", x=255, y=150, width=380, height=150,
        fill=PHOS, opacity=7, stroke=NONE)
d.text("PARADIGM", "Wall word", x=290, y=238, size=58,
       font="Virelai Sans", color=PHOS, justify="left")
d.text("SHIFT", "Wall word two", x=296, y=290, size=34,
       font="Virelai Sans", color=PHOS_DIM, justify="left")

# --- crashed server rack, left ----------------------------------------------------
d.shape("ellipse", "Rack shadow", x=150, y=688, width=140, height=14,
        fill="#0E0A06", opacity=35, stroke=NONE)
d.shape("rectangle", "Rack", x=162, y=398, width=110, height=302,
        fill=RACK_GRAD, stroke=INK, strokeWidth=4, radius=6)
for i, y in enumerate(range(420, 660, 40)):
    d.path(f"M176,{y} L258,{y}", f"Rack slot {i+1}", fill=NONE,
           stroke="#12161A", strokeWidth=6, opacity=80)
d.path("M176,446 L258,446 M176,486 L258,486", "Rack slot b", fill=NONE,
       stroke="#12161A", strokeWidth=6, opacity=80)
# dead status lights: two red, one amber, one dark
d.shape("ellipse", "LED red 1", x=246, y=410, width=8, height=8,
        fill="#C04838", stroke=NONE)
d.shape("ellipse", "LED red 1 glow", x=240, y=404, width=20, height=20,
        fill="#C04838", opacity=25, stroke=NONE)
d.shape("ellipse", "LED red 2", x=246, y=530, width=8, height=8,
        fill="#C04838", stroke=NONE)
d.shape("ellipse", "LED red 2 glow", x=240, y=524, width=20, height=20,
        fill="#C04838", opacity=22, stroke=NONE)
d.shape("ellipse", "LED amber", x=246, y=570, width=8, height=8,
        fill="#C09034", opacity=70, stroke=NONE)
d.shape("ellipse", "LED dark", x=246, y=610, width=8, height=8,
        fill="#3A3E34", stroke=NONE)
# smoke wisp off the rack top
d.path("M205,392 C220,368 192,352 208,330 C220,314 204,300 198,288",
       "Rack smoke", fill=NONE, stroke="#6A6E62", strokeWidth=5,
       cap="round", opacity=30)

# --- the glowing slide deck, projected on the wall ---------------------------------
d.shape("ellipse", "Screen halo", x=430, y=255, width=440, height=290,
        fill="#D8ECC0", opacity=12, stroke=NONE)
d.shape("rectangle", "Slide", x=478, y=298, width=300, height=180,
        fill=SCREEN_GRAD, stroke="#7A8A62", strokeWidth=4, radius=8)
# slide furniture: title bar scribble + a chart that never realized it died
d.path(rot_rect_path(560, 330, 130, 8, 0), "Slide title", fill=NONE,
       stroke="#8AA06E", strokeWidth=4, opacity=80)
d.path("M510,380 L510,452 M510,452 L740,452", "Chart axes", fill=NONE,
       stroke="#6E8256", strokeWidth=3.5, opacity=85)
d.path("M522,398 L576,410 L630,428 L684,440 L730,448", "Chart line",
       fill=NONE, stroke="#A8684A", strokeWidth=4.5, cap="round", opacity=90)
for i, (x, h) in enumerate([(545, 26), (600, 18), (655, 12)]):
    d.shape("rectangle", f"Bar {i+1}", x=x, y=452-h, width=26, height=h,
            fill="#8AA06E", opacity=75, stroke=NONE)
d.path("M700,412 L730,412 M700,428 L726,428", "Legend dashes", fill=NONE,
       stroke="#8AA06E", strokeWidth=4, cap="round", opacity=75)
# the deck's afterglow pooling on the floor
d.shape("ellipse", "Screen floor glow", x=470, y=660, width=320, height=40,
        fill="#D8ECC0", opacity=10, stroke=NONE)

# --- a small server unit, tipped over, quietly on fire ------------------------------
d.shape("ellipse", "Box shadow", x=620, y=688, width=120, height=12,
        fill="#0E0A06", opacity=35, stroke=NONE)
d.path(rot_rect_path(672, 656, 96, 60, -18), "Tipped server",
       fill=RACK_GRAD, stroke=INK, strokeWidth=4)
d.path(rot_rect_path(668, 650, 60, 6, -18), "Tipped slot 1", fill=NONE,
       stroke="#12161A", strokeWidth=4, opacity=80)
d.path(rot_rect_path(664, 668, 56, 6, -18), "Tipped slot 2", fill=NONE,
       stroke="#12161A", strokeWidth=4, opacity=80)
d.shape("ellipse", "Tipped LED", x=700, y=628, width=7, height=7,
        fill="#C04838", stroke=NONE)
# fire at its cable end
d.shape("ellipse", "Fire glow", x=620, y=580, width=110, height=100,
        fill="#E09040", opacity=16, stroke=NONE)
d.path("M654,668 C646,646 656,630 668,616 C680,632 686,650 680,668 Z",
       "Flame outer", fill="#D87830", opacity=88, stroke=NONE)
d.path("M660,668 C654,652 662,640 668,632 C674,642 676,654 672,668 Z",
       "Flame inner", fill="#F0C060", opacity=90, stroke=NONE)
d.path("M662,610 C678,586 648,566 666,540 C676,526 668,508 658,496",
       "Fire smoke", fill=NONE, stroke="#6A6E62", strokeWidth=4.5,
       cap="round", opacity=30)
d.path("M700,600 L712,588 M686,592 L694,580", "Sparks", fill=NONE,
       stroke="#F0C060", strokeWidth=3, cap="round", opacity=80)
# second small fire at the rack's base
d.path("M196,700 C190,684 198,672 208,662 C218,674 222,686 218,700 Z",
       "Rack flame", fill="#D87830", opacity=85, stroke=NONE)
d.path("M201,700 C197,690 203,682 208,676 C213,684 214,692 212,700 Z",
       "Rack flame in", fill="#F0C060", opacity=90, stroke=NONE)
d.shape("ellipse", "Rack fire glow", x=170, y=640, width=90, height=70,
        fill="#E09040", opacity=14, stroke=NONE)

# --- the mascot, presenting nothing ---------------------------------------------------
d.shape("ellipse", "Mascot shadow", x=290, y=686, width=190, height=16,
        fill="#0E0A06", opacity=35, stroke=NONE)
d.shape("ellipse", "Body", x=296, y=482, width=170, height=205,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# collar + tie
d.path("M356,490 L376,509 L396,490 L396,502 L376,521 L356,502 Z",
       "Collar", fill="#E8DCC8", stroke=INK, strokeWidth=3)
d.path("M372,516 L380,516 L378,552 L374,552 Z", "Tie", fill="#4E5A46",
       stroke=INK, strokeWidth=2.5)
# head
d.shape("ellipse", "Head", x=316, y=352, width=134, height=130,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
for ex in (328, 440):
    d.shape("ellipse", f"Ear {ex}", x=ex-11, y=348, width=26, height=24,
            fill="#9A825C", stroke=INK, strokeWidth=3.5)
# face: the calm of someone whose launch was very good
d.shape("ellipse", "Eye L", x=352, y=418, width=10, height=10,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=398, y=418, width=10, height=10,
        fill=INK, stroke=NONE)
d.path("M364,450 C372,455 382,455 390,450", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# the pointer arm, still raised at the deck
d.path("M446,540 C470,516 500,494 528,478", "Arm point", fill=NONE,
       stroke="#9A825C", strokeWidth=17, cap="round")
d.path("M524,482 L588,428", "Pointer", fill=NONE, stroke="#C8B88E",
       strokeWidth=5, cap="round")
d.shape("ellipse", "Paw point", x=514, y=468, width=24, height=20,
        fill="#9A825C", stroke=INK, strokeWidth=3.5)
# the other arm, down, holding the clicker
d.path("M310,540 C292,566 284,594 286,622", "Arm down", fill=NONE,
       stroke="#9A825C", strokeWidth=17, cap="round")
d.shape("ellipse", "Paw low", x=276, y=614, width=24, height=20,
        fill="#9A825C", stroke=INK, strokeWidth=3.5)
d.path(rot_rect_path(292, 636, 12, 26, -12), "Clicker", fill="#3A3E34",
       stroke=INK, strokeWidth=2.5)

# --- stray warm motes in the glow -----------------------------------------------------
for i, (x, y, w) in enumerate([(560,270,5),(700,250,6),(800,330,5),(470,240,5),
                               (830,430,6),(750,540,5),(620,230,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#D8ECC0", opacity=38, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("POLICY AFTERGLOW", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#ECE8D2", justify="center")
r = d.text("IT WAS A VERY GOOD ANNOUNCEMENT", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#BCC4A4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("269.policy-afterglow-V1R00")
