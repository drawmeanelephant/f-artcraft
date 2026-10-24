#!/usr/bin/env python3
"""Semantic Seymour — mascot portrait V1R00.
Robed inquisitor in a cape sewn from an unused <aside> element, red pencil
mid-strike over a fan of printed screenshots; condemned <div> tags drift
in the plate behind him. 1000x1000. Gradients + translucent shading."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Semantic Seymour — Mascot Portrait", 1000, 1000)

INK = "#1E1418"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#17121E"}, {"offset": 1, "color": "#0A0710"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#5A4C68"}, {"offset": 0.7, "color": "#3A3048"},
    {"offset": 1, "color": "#1C1826"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#342E3C"}, {"offset": 1, "color": "#161220"}]}}
ROBE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#52446A"}, {"offset": 0.65, "color": "#3A3050"},
    {"offset": 1, "color": "#241E36"}]}}
CAPE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E5A8C"}, {"offset": 0.6, "color": "#50406E"},
    {"offset": 1, "color": "#2E2444"}]}}
SKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4D2B4"}, {"offset": 0.75, "color": "#C4A888"},
    {"offset": 1, "color": "#96785E"}]}}
PAPER = "#EDE6D4"
PENCIL = "#C84646"
TAG_FAINT = "#8A7A9C"

def rot_pt(cx, cy, x, y, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * s,
            cy + (x - cx) * s + (y - cy) * c)

# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E6E92", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C4B8D4", strokeWidth=3, opacity=35)
d.shape("ellipse", "Patina 1", x=210, y=190, width=220, height=140,
        fill="#6E5E82", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=590, y=600, width=240, height=150,
        fill="#6E5E82", opacity=18, stroke=NONE)

# --- the condemned markup: drifting element tags ----------------------------------
# an innocent <main> and <section>, one convicted <div> struck through
for i, (cx, cy, w, deg, label) in enumerate([
        (268, 240, 120, -7, "<main>"), (730, 250, 150, 6, "<section>"),
        (770, 560, 110, -5, "<nav>")]):
    d.path(rot_rect_path(cx, cy, w, 44, deg), f"Tag plate {label}",
           fill="#2E2840", stroke=TAG_FAINT, strokeWidth=2.5,
           join="round", opacity=80)
    t = d.text(label, f"Tag {label}", x=cx, y=cy + 7, size=17,
               font="Source Sans 3", color="#B8AACB", justify="center")
    if t and t.get("id"):
        d.cmd("object.rotate", f"tilt {label}", ids=[t["id"]], angle=deg,
              origin=[cx, cy])
# the convicted div, upper left, struck through in red
d.path(rot_rect_path(240, 430, 116, 48, -6), "Tag plate div",
       fill="#33221F", stroke="#8C5A56", strokeWidth=2.5, join="round",
       opacity=90)
t = d.text("<div>", "Tag div", x=240, y=438, size=19,
           font="Source Sans 3", color="#D09A94", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "div tilt", ids=[t["id"]], angle=-6,
          origin=[240, 430])
p1 = rot_pt(240, 430, 196, 414, -6); p2 = rot_pt(240, 430, 284, 446, -6)
d.path(f"M{p1[0]:.0f},{p1[1]:.0f} L{p2[0]:.0f},{p2[1]:.0f}",
       "Div strike", fill=NONE, stroke=PENCIL, strokeWidth=5,
       cap="round", opacity=90)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0C0810",
       strokeWidth=4, opacity=70)

# --- the <aside> cape, drawn first so the robe sits in it ------------------------
d.shape("ellipse", "Seymour shadow", x=392, y=686, width=250, height=24,
        fill="#05030A", opacity=55, stroke=NONE)
# cape: one unused aside, pressed into service, flaring stage-left
d.path("M470,432 C400,442 336,486 314,560 C296,622 316,676 342,706 "
       "C430,724 570,724 658,706 C676,640 668,560 640,500 "
       "C612,448 556,420 470,432 Z",
       "Aside cape", fill=CAPE_GRAD, stroke=INK, strokeWidth=6,
       join="round")
# cape hem tag: the element identifies itself
d.path(rot_rect_path(346, 664, 108, 34, 8), "Aside label patch",
       fill="#2A2138", stroke="#8A76A8", strokeWidth=2.5, join="round")
t = d.text("<aside>", "Aside label", x=346, y=671, size=15,
           font="Source Sans 3", color="#C4B4DC", justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "aside tilt", ids=[t["id"]], angle=8,
          origin=[346, 664])
# cape fold shading
d.path("M360,520 C344,580 352,640 372,690", "Cape fold", fill=NONE,
       stroke="#241C38", strokeWidth=4, cap="round", opacity=55)
d.path("M620,520 C640,580 642,642 630,690", "Cape fold R", fill=NONE,
       stroke="#241C38", strokeWidth=4, cap="round", opacity=45)

# --- robe body ---------------------------------------------------------------------
d.path("M500,470 C566,470 606,522 612,590 C616,644 626,676 640,700 "
       "C560,714 440,714 360,700 C374,676 384,644 388,590 "
       "C394,522 434,470 500,470 Z",
       "Robe", fill=ROBE_GRAD, stroke=INK, strokeWidth=6, join="round")
d.path("M500,500 L500,690", "Robe seam", fill=NONE, stroke="#241C34",
       strokeWidth=3.5, opacity=60)
# clerical collar band: the validator's vestment
d.path("M440,486 C470,500 530,500 560,486 C552,512 530,524 500,524 "
       "C470,524 448,512 440,486 Z", "Collar", fill="#D8D2E0",
       stroke=INK, strokeWidth=3.5, join="round")

# --- head ---------------------------------------------------------------------------
d.shape("ellipse", "Head", x=432, y=356, width=136, height=124,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=6)
# flat judgy hairline
d.path("M444,384 C460,362 540,362 556,384 C540,372 460,372 444,384 Z",
       "Hairline", fill="#3A2E28", stroke=NONE)
# spectacles: the private validator
d.shape("ellipse", "Lens L", x=448, y=404, width=40, height=34,
        fill="#FFFFFF", opacity=18, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Lens R", x=512, y=404, width=40, height=34,
        fill="#FFFFFF", opacity=18, stroke=INK, strokeWidth=3.5)
d.path("M488,418 L512,418", "Bridge", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
d.shape("ellipse", "Eye L", x=462, y=412, width=13, height=15,
        fill="#241C1C", stroke=NONE)
d.shape("ellipse", "Eye R", x=526, y=412, width=13, height=15,
        fill="#241C1C", stroke=NONE)
# brows doing the judging
d.path("M450,398 L484,392 M516,392 L550,398", "Brows", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
d.path("M478,452 C490,446 510,446 522,452", "Frown", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")

# --- left hand: fan of printed screenshots ----------------------------------------
d.path("M430,580 C400,596 380,616 372,640", "Arm L ink", fill=NONE,
       stroke=INK, strokeWidth=28, cap="round")
d.path("M430,580 C400,596 380,616 372,640", "Arm L", fill=NONE,
       stroke="#3A3050", strokeWidth=19, cap="round")
d.shape("ellipse", "Hand L", x=350, y=620, width=32, height=26,
        fill="#C4A888", stroke=INK, strokeWidth=3.5)
# the printouts fanned in hand — little wireframes on each
for i, (cx, cy, w, h, deg) in enumerate([(296, 560, 128, 92, -16),
                                         (322, 586, 128, 92, -6),
                                         (352, 606, 128, 92, 4)]):
    d.path(rot_rect_path(cx, cy, w, h, deg), f"Printout {i+1}",
           fill=PAPER, stroke="#8A7E64", strokeWidth=2.5, join="round")
    # wireframe: header bar + two column boxes, all rotated with the sheet
    hd = [rot_pt(cx, cy, cx - w/2 + 8, cy - h/2 + 10, deg),
          rot_pt(cx, cy, cx + w/2 - 8, cy - h/2 + 10, deg)]
    d.path(f"M{hd[0][0]:.0f},{hd[0][1]:.0f} L{hd[1][0]:.0f},{hd[1][1]:.0f}",
           f"Printout {i+1} hdr", fill=NONE, stroke="#9A8E74",
           strokeWidth=5, cap="round", opacity=80)
    for j, fx in enumerate([-0.25, 0.25]):
        bx = cx + fx * w; by = cy + h * 0.12
        d.path(rot_rect_path(bx, by, w * 0.36, h * 0.42, deg),
               f"Printout {i+1} col {j+1}", fill=NONE, stroke="#A89878",
               strokeWidth=2, opacity=70)
# red annotation on the top sheet: circled heading + correction
cx, cy, deg = 352, 606, 4
a1 = rot_pt(cx, cy, cx - 30, cy - 18, deg)
d.path(f"M{a1[0]:.0f},{a1[1]:.0f} c-14,-10 2,-26 22,-24 c20,2 26,16 12,26 "
       f"c-12,8 -30,6 -34,-4", "Red circle", fill=NONE, stroke=PENCIL,
       strokeWidth=4, cap="round", opacity=95)
t = d.text("<h1>", "Correction", x=398, y=586, size=14,
           font="Source Sans 3", color=PENCIL, justify="center")
if t and t.get("id"):
    d.cmd("object.rotate", "corr tilt", ids=[t["id"]], angle=4,
          origin=[398, 582])

# --- right hand: the red pencil, mid-strike ---------------------------------------
d.path("M570,580 C606,596 628,620 636,646", "Arm R ink", fill=NONE,
       stroke=INK, strokeWidth=28, cap="round")
d.path("M570,580 C606,596 628,620 636,646", "Arm R", fill=NONE,
       stroke="#3A3050", strokeWidth=19, cap="round")
d.shape("ellipse", "Hand R", x=622, y=636, width=32, height=26,
        fill="#C4A888", stroke=INK, strokeWidth=3.5)
# pencil held low, tip toward the printouts
d.path(rot_rect_path(596, 622, 14, 78, 42), "Pencil body",
       fill=PENCIL, stroke=INK, strokeWidth=3, join="round")
tip = rot_pt(596, 622, 596, 666, 42)
d.path(f"M{tip[0]-7:.0f},{tip[1]-3:.0f} L{tip[0]:.0f},{tip[1]+10:.0f} "
       f"L{tip[0]+7:.0f},{tip[1]-3:.0f} Z", "Pencil tip",
       fill="#E8D8B0", stroke=INK, strokeWidth=2.5, join="round")
d.path(f"M{tip[0]:.0f},{tip[1]+6:.0f} L{tip[0]:.0f},{tip[1]+10:.0f}",
       "Graphite", fill=NONE, stroke="#3A2E2E", strokeWidth=3,
       cap="round")

# --- captions ----------------------------------------------------------------------
d.text("SEMANTIC SEYMOUR", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#E4DEEE", justify="center")
r = d.text("SEMANTIC-STRUCTURE INQUISITOR", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#AEA2C2", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("071.semantic-seymour-V1R00")
