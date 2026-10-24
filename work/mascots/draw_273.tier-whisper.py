#!/usr/bin/env python3
"""Tier Whisper — mascot portrait V1R00.
The mascot leans into a service-desk microphone and lowers the room:
behind it, gold, silver and bronze tiers stand in ascending order —
the hierarchy the org chart declines to print, reproduced in decibels.
1000x1000. Gradients + translucent shading, no flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Tier Whisper — Mascot Portrait", 1000, 1000)

INK = "#1E1820"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#12101C"}, {"offset": 1, "color": "#080710"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#464A66"}, {"offset": 0.7, "color": "#31344C"},
    {"offset": 1, "color": "#1D1F30"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#32344A"}, {"offset": 1, "color": "#181A28"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DCB896"}, {"offset": 0.7, "color": "#B48C64"},
    {"offset": 1, "color": "#886646"}]}}
GOLD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E8C060"}, {"offset": 0.6, "color": "#B8892F"},
    {"offset": 1, "color": "#7C5A1E"}]}}
SILVER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#CCD0DC"}, {"offset": 0.6, "color": "#989CB0"},
    {"offset": 1, "color": "#62667C"}]}}
BRONZE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#CC905C"}, {"offset": 0.6, "color": "#9E6838"},
    {"offset": 1, "color": "#6C4220"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#42465E"}, {"offset": 1, "color": "#282A3C"}]}}
MIC_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8E94AC"}, {"offset": 1, "color": "#4A4E66"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A6A8E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CCC4DE", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3C3E58", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#100E1A",
       strokeWidth=4, opacity=70)

# --- the tiers behind: bronze, gold, silver --------------------------------------
def tier(x1, x2, top, grad, name):
    w = x2 - x1
    d.path(f"M{x1},700 L{x1},{top+22} A{w/2:.0f},22 0 0 1 {x2},{top+22} "
           f"L{x2},700 Z", name, fill=grad, stroke=INK, strokeWidth=4,
           opacity=92)
    # measurement ticks up the left edge — ranked concern, made visible
    for j, ty in enumerate([top + 60, top + 110, top + 160]):
        d.path(f"M{x1+10},{ty} L{x1+34},{ty}", f"{name} tick {j+1}",
               fill=NONE, stroke="#F0E8D8", strokeWidth=3,
               cap="round", opacity=45)
    # sheen
    d.path(f"M{x1+14},{top+40} L{x1+30},{top+40} L{x1+30},690 "
           f"L{x1+14},690 Z", f"{name} sheen", fill="#FFFFFF",
           opacity=10, stroke=NONE)

tier(180, 300, 470, BRONZE_GRAD, "Bronze tier")
tier(415, 545, 372, GOLD_GRAD, "Gold tier")
tier(655, 785, 425, SILVER_GRAD, "Silver tier")

# --- the mascot, leaning in, behind the counter ------------------------------------------
d.shape("ellipse", "Body", x=545, y=478, width=185, height=170,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# head, tipped toward the mic
for ex in (566, 704):
    d.shape("ellipse", f"Ear {ex}", x=ex - 11, y=322, width=26, height=24,
            fill="#B48C64", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Head", x=560, y=326, width=150, height=136,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# one low, conspiratorial lid + one open eye
d.shape("ellipse", "Eye L", x=592, y=384, width=16, height=12,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=662, y=380, width=16, height=20,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint R", x=666, y=384, width=5, height=6,
        fill="#FFF8E8", opacity=90, stroke=NONE)
d.shape("ellipse", "Glint L", x=595, y=386, width=4, height=4,
        fill="#FFF8E8", opacity=80, stroke=NONE)
# pursed whisper mouth, aimed at the capsule
d.shape("ellipse", "Whisper mouth", x=578, y=430, width=14, height=11,
        fill=INK, stroke=NONE)

# --- the service counter ------------------------------------------------------------
d.shape("ellipse", "Counter shadow", x=250, y=760, width=500, height=20,
        fill="#0C0A14", opacity=45, stroke=NONE)
d.path("M290,560 L710,560 L748,638 L252,638 Z", "Counter top",
       fill=DESK_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M252,638 L748,638 L738,660 L262,660 Z", "Counter edge",
       fill="#2E3148", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Counter sheen", x=320, y=570, width=160, height=16,
        fill="#6A70A0", opacity=25, stroke=NONE)

# --- the microphone -------------------------------------------------------------------
# cable coiling on the counter top
d.path("M486,552 C458,556 434,560 424,572 C416,582 424,592 440,590",
       "Mic cable", fill=NONE, stroke="#1A1626", strokeWidth=4,
       cap="round", opacity=85)
d.path("M440,590 C452,588 460,582 458,574", "Cable coil", fill=NONE,
       stroke="#1A1626", strokeWidth=3.5, cap="round", opacity=70)
# weighted base
d.shape("ellipse", "Mic base shadow", x=444, y=556, width=80, height=12,
        fill="#14101E", opacity=55, stroke=NONE)
d.shape("ellipse", "Mic base", x=450, y=540, width=72, height=22,
        fill=MIC_GRAD, stroke=INK, strokeWidth=3.5)
# gooseneck rising to the capsule
d.path("M486,544 C486,510 490,486 504,468", "Gooseneck", fill=NONE,
       stroke="#3A3E56", strokeWidth=7, cap="round")
# capsule head, tilted toward the whisperer
d.path(rot_rect_path(508, 448, 46, 32, -28), "Mic head",
       fill=MIC_GRAD, stroke=INK, strokeWidth=3.5)
# grille lines across the capsule
for i in range(3):
    d.path(rot_rect_path(500 + i * 9, 452 - i * 5, 30, 3.5, -28),
           f"Grille {i+1}", fill="#2C2E42", opacity=85, stroke=NONE)
d.shape("ellipse", "Mic sheen", x=494, y=436, width=14, height=8,
        fill="#D8DCE8", opacity=45, stroke=NONE)

# the cupped paw funnelling the whisper
d.path("M630,452 C608,458 596,464 590,472", "Cup arm", fill=NONE,
       stroke="#B48C64", strokeWidth=18, cap="round")
d.path("M588,440 C568,440 556,456 560,474 C564,490 584,494 596,484 "
       "C588,472 586,456 588,440 Z", "Cup paw", fill="#DCB896",
       stroke=INK, strokeWidth=4, join="round")

# --- the whisper: three arcs no open channel ever captured --------------------------------
for i, x in enumerate([556, 538, 520]):
    d.path(f"M{x},{452 - i*4} C{x-10},{462 - i*4} {x-10},{474 + i*4} "
           f"{x},{484 + i*4}", f"Whisper arc {i+1}", fill=NONE,
           stroke="#C8B8E0", strokeWidth=3, cap="round",
           opacity=70 - i * 15)

# --- a faint gold reply light on the mic base — certain callers only ----------------------
d.shape("ellipse", "Reply glow", x=462, y=536, width=18, height=14,
        fill="#E8C060", opacity=30, stroke=NONE)
d.shape("ellipse", "Reply light", x=466, y=540, width=9, height=7,
        fill="#E8C060", stroke=NONE)

# --- motes ------------------------------------------------------------------------------
for i, (x, y, w) in enumerate([(262,420,5),(244,580,6),(648,220,5),(836,470,6),
                               (224,640,5),(812,300,6),(356,240,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#B8A8E0", opacity=40, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("TIER WHISPER", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#EDE4D4", justify="center")
r = d.text("THE HIERARCHY, IN DECIBELS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B8A8C8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("273.tier-whisper-V1R00")
