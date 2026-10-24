#!/usr/bin/env python3
"""Soft Escalation Clerk — mascot portrait V1R00.
A careful clerk easing a bubble-wrapped incident report under the manager's
door; kit laid out: ruler, lavender sachet, wrap roll. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Soft Escalation Clerk — Mascot Portrait", 1000, 1000)

INK = "#2B2530"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1C1826"}, {"offset": 1, "color": "#0C0A12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#7A6E82"}, {"offset": 0.7, "color": "#524A60"},
    {"offset": 1, "color": "#282232"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#443A50"}, {"offset": 1, "color": "#201A2A"}]}}
CLERK_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B8A6AC"}, {"offset": 0.72, "color": "#8C7A82"},
    {"offset": 1, "color": "#5E505A"}]}}
DOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E5E54"}, {"offset": 1, "color": "#2B3833"}]}}
PAPER = "#EBDFC6"
WRAP = "#C9DCE8"
LIGHT = "#F0DCA0"
TAG_RED = "#B0605E"

# --- backdrop + plate --------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8E7E9A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DECFE8", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(188,232,8),(806,230,7),(156,518,9),(838,542,8),
                               (250,766,7),(752,748,9),(132,390,6),(866,392,7),
                               (392,110,7),(614,110,8),(332,822,6),(670,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E526E", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#141020",
       strokeWidth=4, opacity=70)

# --- the manager's door --------------------------------------------------------------
d.shape("ellipse", "Door shadow", x=620, y=686, width=220, height=20,
        fill="#0E0A16", opacity=45, stroke=NONE)
d.shape("rectangle", "Door frame", x=622, y=232, width=180, height=440,
        fill="#6A7A70", stroke=INK, strokeWidth=5, radius=4)
d.shape("rectangle", "Door", x=638, y=248, width=148, height=400,
        fill=DOOR_GRAD, stroke=INK, strokeWidth=5, radius=3)
d.shape("rectangle", "Door panel T", x=656, y=280, width=112, height=140,
        fill=NONE, stroke="#1A2420", strokeWidth=4, radius=4)
d.shape("rectangle", "Door panel B", x=656, y=446, width=112, height=150,
        fill=NONE, stroke="#1A2420", strokeWidth=4, radius=4)
d.shape("ellipse", "Knob", x=654, y=438, width=18, height=18,
        fill="#9AAEA2", stroke=INK, strokeWidth=3)
# the little brass plate that says who waits on the other side
d.shape("rectangle", "Door plate", x=660, y=212, width=104, height=30,
        fill="#C9B06A", stroke=INK, strokeWidth=4, radius=3)
d.text("MANAGER", "Door label", x=712, y=233, size=14, font="Virelai Sans",
       color="#3E3420", justify="center")
# the gap under the door: a warm sliver of other people's authority
d.path("M638,652 L786,652 L786,672 L638,672 Z", "Door gap", fill=LIGHT,
       stroke=NONE, opacity=90)
d.path("M638,652 L786,652 L786,672 L638,672 Z", "Gap glow", fill=LIGHT,
       stroke=NONE, opacity=25)
d.shape("ellipse", "Glow spill", x=610, y=668, width=210, height=24,
        fill=LIGHT, opacity=12, stroke=NONE)

# --- the packet: incident report, wrapped, mid-slide under the gap --------------------
# the right end is already through into the light; the wrap is what gets it there
d.path("M600,648 L768,648 L768,688 L600,688 Z", "Report", fill=PAPER,
       stroke=INK, strokeWidth=4, join="round")
# SEV-2 tag: digits need Source Sans 3 — Virelai has no digit glyphs
d.shape("rectangle", "Sev tag", x=612, y=656, width=52, height=20,
        fill=TAG_RED, stroke=INK, strokeWidth=3, radius=3)
d.text("SEV-2", "Tag text", x=619, y=671, size=13, font="Source Sans 3",
       color="#F4E4DC", justify="left")
# bubble wrap over the part still outside: translucent sheet + bubbles
d.path("M592,640 L692,640 L692,696 L592,696 Z", "Wrap sheet", fill=WRAP,
       stroke="#9AB2C2", strokeWidth=3, opacity=38, join="round")
for row, wy in enumerate([652, 676]):
    for col, wx in enumerate([604, 630, 656]):
        d.shape("ellipse", f"Bubble {row},{col}", x=wx, y=wy,
                width=18, height=18, fill=NONE, stroke="#E8F0F6",
                strokeWidth=2.5, opacity=55)
# the slide line: polish marks where the wrap is already traveling
d.path("M592,696 C630,700 680,700 730,694", "Slide sheen", fill=NONE,
       stroke=LIGHT, strokeWidth=3, cap="round", opacity=40)

# --- the kit --------------------------------------------------------------------------
# ruler for keeping sentences level
d.path("M300,694 L420,686 L422,698 L302,706 Z", "Ruler", fill="#C9B06A",
       stroke=INK, strokeWidth=3, join="round")
for i in range(7):
    x = 312 + i*16
    d.path(f"M{x},{692-i*0.9} L{x+1},{700-i*0.9}", f"Tick {i+1}",
           fill=NONE, stroke="#7A6428", strokeWidth=2, opacity=80)
# lavender sachet
d.path("M248,664 C240,648 256,638 268,646 C280,638 296,648 288,664 "
       "C296,678 280,688 268,682 C256,688 240,678 248,664 Z",
       "Sachet", fill="#9E8EC0", stroke=INK, strokeWidth=4, join="round",
       opacity=95)
d.path("M258,656 C264,650 274,650 280,656", "Sachet knot", fill=NONE,
       stroke="#6E5E94", strokeWidth=3, cap="round")
# the wrap roll, mostly unspooled
d.shape("ellipse", "Roll end", x=176, y=632, width=34, height=60,
        fill=WRAP, stroke=INK, strokeWidth=4, opacity=85)
d.path("M193,632 L240,632 L240,692 L193,692", "Roll side", fill=WRAP,
       stroke=INK, strokeWidth=4, opacity=55)
d.shape("ellipse", "Roll core", x=184, y=650, width=18, height=24,
        fill="#8A7A5E", stroke=INK, strokeWidth=3)
d.path("M240,668 C300,660 360,656 420,652", "Wrap trail", fill=NONE,
       stroke=WRAP, strokeWidth=14, cap="round", opacity=30)

# --- the Clerk: kneeling, easing it through with two level hands -----------------------
d.shape("ellipse", "Clerk shadow", x=330, y=686, width=250, height=24,
        fill="#0E0A16", opacity=45, stroke=NONE)
# kneeling body: low bell, folded over the work
d.path("M440,470 C530,470 570,545 575,640 C575,678 540,696 445,696 "
       "C350,696 320,678 325,640 C330,545 350,470 440,470 Z",
       "Clerk body", fill=CLERK_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body hi", x=372, y=500, width=100, height=46,
        fill="#FFFFFF", opacity=12, stroke=NONE)
# cardigan seam + buttons
d.path("M445,520 L445,660", "Cardigan seam", fill=NONE, stroke="#6A5A64",
       strokeWidth=4, opacity=70)
for i, by in enumerate([545, 585, 625]):
    d.shape("ellipse", f"Button {i+1}", x=438, y=by, width=11, height=11,
            fill="#C9B06A", stroke=INK, strokeWidth=2)

# right arm: extended along the floor, fingertips on the wrap's trailing edge
d.path("M540,560 C572,594 586,620 594,644", "Arm R", fill=NONE,
       stroke="#8C7A82", strokeWidth=19, cap="round")
d.shape("ellipse", "Palm R", x=576, y=636, width=30, height=20,
        fill="#B8A6AC", stroke=INK, strokeWidth=4)
# left arm: comes to rest on the ruler — each incident is measured first
d.path("M360,545 C335,580 330,625 338,660", "Arm L", fill=NONE,
       stroke="#8C7A82", strokeWidth=19, cap="round")
d.shape("ellipse", "Palm L", x=324, y=660, width=30, height=20,
        fill="#B8A6AC", stroke=INK, strokeWidth=4)

# head: neat parting, small glasses, the patience of a clerk who measures twice
d.path("M445,322 C510,322 548,366 548,416 C548,458 508,482 445,482 "
       "C382,482 342,458 342,416 C342,366 380,322 445,322 Z",
       "Head", fill=CLERK_GRAD, stroke=INK, strokeWidth=6)
# tidy hair cap
d.path("M350,404 C350,354 390,318 445,318 C500,318 540,354 540,404 "
       "C516,372 486,360 445,360 C404,360 374,372 350,404 Z",
       "Hair", fill="#4A3E4C", stroke=INK, strokeWidth=5, join="round")
d.path("M445,318 L445,340", "Parting", fill=NONE, stroke="#6E5E70",
       strokeWidth=3, cap="round")
# glasses: level, like the sentences
d.shape("ellipse", "Lens L", x=384, y=402, width=44, height=36,
        fill="#E8F0F6", stroke=INK, strokeWidth=4, opacity=30)
d.shape("ellipse", "Lens R", x=462, y=402, width=44, height=36,
        fill="#E8F0F6", stroke=INK, strokeWidth=4, opacity=30)
d.path("M428,418 L462,418", "Bridge", fill=NONE, stroke=INK, strokeWidth=4)
d.path("M384,416 C392,424 404,424 412,416", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M470,416 C478,424 490,424 498,416", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# level mouth — measured, not hurried
d.path("M428,452 C438,455 452,455 462,452", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# gentle concentration blush
d.shape("ellipse", "Cheek L", x=370, y=430, width=24, height=12,
        fill="#9E7E8C", opacity=40, stroke=NONE)
d.shape("ellipse", "Cheek R", x=496, y=430, width=24, height=12,
        fill="#9E7E8C", opacity=40, stroke=NONE)

# --- captions ---------------------------------------------------------------------------
d.text("SOFT ESCALATION CLERK", "Name", x=500, y=930, size=50,
       font="Virelai Sans", color="#DECFE8", justify="center")
r = d.text("URGENCY AT TWO TEMPERATURES", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A292B4", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("238.soft-escalation-clerk-V1R00")
