#!/usr/bin/env python3
"""Proxy Lantern — mascot portrait V1R00.
The lantern is chained to the front desk and glowing over the intake
form. Its light is real; the lock and the remedy belong to another
office entirely. Illumination without jurisdiction. 1000x1000.
Gradients + translucent shading, no flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Proxy Lantern — Mascot Portrait", 1000, 1000)

INK = "#241D22"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#141C26"}, {"offset": 1, "color": "#080C12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#46505E"}, {"offset": 0.7, "color": "#303946"},
    {"offset": 1, "color": "#1A2029"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#38414E"}, {"offset": 1, "color": "#161C26"}]}}
GLOW = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4BE6A"}, {"offset": 0.55, "color": "#B07A46"},
    {"offset": 1, "color": "#4E3E42"}]}}
GLASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FADA98"}, {"offset": 0.55, "color": "#EFB257"},
    {"offset": 1, "color": "#CA8138"}]}}
FRAME = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E4C3E"}, {"offset": 1, "color": "#372B23"}]}}
BRASS_WORN = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C9A05C"}, {"offset": 0.5, "color": "#96702F"},
    {"offset": 1, "color": "#5E4620"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E5266"}, {"offset": 1, "color": "#2C2E40"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F7EDD6"}, {"offset": 1, "color": "#DFCFA9"}]}}
AMBER = "#F0B45C"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E7C8E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D4E0", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(196,236,8),(798,232,7),(160,528,9),(834,548,8),
                               (250,764,7),(748,750,9),(138,396,6),(860,392,7),
                               (394,114,7),(610,110,8),(336,822,6),(662,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A4352", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#10151E",
       strokeWidth=4, opacity=70)

# --- the lantern's reach: warm radius against the cool dark ---------------------------
d.shape("ellipse", "Lantern glow", x=380, y=250, width=460, height=430,
        fill=GLOW, opacity=72, stroke=NONE)

# --- the front desk --------------------------------------------------------------------
d.path("M228,632 L772,632 L806,698 L194,698 Z", "Desk top",
       fill=DESK_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M194,698 L806,698 L794,724 L206,724 Z", "Desk edge",
       fill="#333648", stroke=INK, strokeWidth=4, join="round")
# the light pool on the desktop — the desk is lit, not empowered
d.shape("ellipse", "Desk glow pool", x=380, y=626, width=340, height=36,
        fill=AMBER, opacity=24, stroke=NONE)
d.shape("ellipse", "Desk sheen", x=300, y=640, width=170, height=13,
        fill="#7E86A4", opacity=20, stroke=NONE)

# --- the intake form, lit by delegated warmth ---------------------------------------------
d.path(rot_rect_path(415, 604, 150, 104, -6), "Intake form",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=4)
# form heading bar + ruled lines
d.path("M362,566 L446,560", "Form heading", fill=NONE, stroke="#8A7A58",
       strokeWidth=5, cap="round", opacity=80)
for i, y in enumerate([582, 596, 610]):
    d.path(f"M352,{y} L472,{y - 8}", f"Form line {i+1}", fill=NONE,
           stroke="#A89878", strokeWidth=2.5, opacity=75)
# checkbox column, none of them the box that matters
for i, y in enumerate([624, 638]):
    d.shape("rectangle", f"Checkbox {i+1}", x=352, y=y, width=10,
            height=10, fill="#F7EDD6", stroke=INK, strokeWidth=2.5)
    d.path(f"M370,{y+7} L440,{y+4}", f"Checkbox label {i+1}", fill=NONE,
           stroke="#B8A884", strokeWidth=2.5, opacity=70)
# signature line, unsigned
d.path("M408,650 L462,647", "Signature line", fill=NONE, stroke="#8A7A58",
       strokeWidth=2.5, cap="round", opacity=80)
# a pen set down beside it
d.path(rot_rect_path(316, 648, 64, 8, 18), "Pen", fill="#3E3548",
       stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pen tip", x=344, y=662, width=10, height=8,
        fill=BRASS_WORN, stroke=INK, strokeWidth=2.5)

# --- the lantern, warm and tethered -------------------------------------------------------
d.shape("ellipse", "Lantern shadow", x=520, y=636, width=160, height=22,
        fill="#0C0A14", opacity=50, stroke=NONE)
# worn brass handle: ring + bail, rubbed bright where hands have held it
d.shape("ellipse", "Handle ring", x=596, y=316, width=30, height=30,
        fill=NONE, stroke=INK, strokeWidth=5)
d.path("M568,382 C562,332 658,332 652,382", "Bail", fill=NONE,
       stroke=BRASS_WORN, strokeWidth=7, cap="round")
d.path("M580,352 C590,340 630,340 640,352", "Bail wear", fill=NONE,
       stroke="#EDD096", strokeWidth=3, cap="round", opacity=80)
# chimney + cap
d.path("M578,382 L644,382 L648,404 L574,404 Z", "Chimney",
       fill=FRAME, stroke=INK, strokeWidth=4, join="round")
d.path("M548,404 L674,404 L680,422 L542,422 Z", "Cap",
       fill=FRAME, stroke=INK, strokeWidth=4, join="round")
d.shape("rectangle", "Top rail", x=546, y=422, width=128, height=15,
        radius=4, fill=FRAME, stroke=INK, strokeWidth=4)
# glass: the light is real
d.shape("rectangle", "Glass", x=562, y=439, width=98, height=178,
        fill=GLASS, stroke=INK, strokeWidth=4)
d.path("M594,439 L594,617 M628,439 L628,617 M562,498 L660,498 "
       "M562,558 L660,558", "Mullions", fill=NONE, stroke=INK,
       strokeWidth=3.5, opacity=75)
# the mascot face in the glass: two calm eyes over the flame
d.shape("ellipse", "Eye L", x=584, y=462, width=13, height=15,
        fill="#3A2214", opacity=85, stroke=NONE)
d.shape("ellipse", "Eye R", x=624, y=462, width=13, height=15,
        fill="#3A2214", opacity=85, stroke=NONE)
# the flame, mid-burn
d.shape("ellipse", "Flame glow", x=584, y=540, width=54, height=60,
        fill="#FCE9BC", opacity=42, stroke=NONE)
d.path("M611,592 C598,576 598,552 611,534 C624,552 624,576 611,592 Z",
       "Flame", fill="#FDF3D2", stroke=INK, strokeWidth=3)
d.path("M611,586 C605,576 605,564 611,552 C617,564 617,576 611,586 Z",
       "Flame core", fill="#FFFDF4", stroke=NONE)
# base + foot
d.shape("rectangle", "Base rail", x=546, y=617, width=128, height=17,
        radius=4, fill=FRAME, stroke=INK, strokeWidth=4)
d.path("M542,634 L678,634 L694,668 L526,668 Z", "Foot",
       fill=FRAME, stroke=INK, strokeWidth=4, join="round")
# sheen on the glass edge
d.path("M568,446 L576,446 L576,608 L568,608 Z", "Glass sheen",
       fill="#FFFFFF", opacity=18, stroke=NONE)

# --- the chain to the desk: present, accounted for --------------------------------------
# catenary from the bail down to a bolted eye on the desktop
d.path("M626,332 C690,352 738,430 752,540 C757,576 757,606 754,628",
       "Chain line", fill=NONE, stroke="#8A7648", strokeWidth=5,
       cap="round")
# readable links along the drop
for i, (x, y, r) in enumerate([(664,352,-30),(696,384,-20),(722,426,-8),
                               (740,472,0),(750,520,4),(756,566,3),
                               (756,600,2)]):
    d.shape("ellipse", f"Link {i+1}", x=x - 6, y=y - 8, width=13,
            height=17, fill=NONE, stroke=BRASS_WORN, strokeWidth=4)
# bolted anchor on the desktop — the chain's other end is furniture
d.shape("ellipse", "Anchor plate", x=736, y=622, width=40, height=14,
        fill=BRASS_WORN, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Anchor ring", x=748, y=604, width=16, height=20,
        fill=NONE, stroke=INK, strokeWidth=4)

# --- motes in the warm radius --------------------------------------------------------------
for i, (x, y, w) in enumerate([(300,430,5),(340,540,6),(700,280,5),(820,470,6),
                               (250,620,5),(840,300,5),(420,250,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8C88E", opacity=40, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("PROXY LANTERN", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#F2E6CE", justify="center")
r = d.text("DELEGATED REASSURANCE ENTITY", "Role", x=500, y=968,
           size=23, font="Virelai Sans", color="#D4A877",
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("294.proxy-lantern-V1R00")
