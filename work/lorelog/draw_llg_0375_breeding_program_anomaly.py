#!/usr/bin/env python3
"""LLG-0375 Breeding Program Registration Anomaly — V1R00. A human figure
filing themself into the mascot registry at a card catalog, mascots beside
them, a floating frontmatter block with breedingProgram highlighted, a
rejected robot lithium mine in the distance, Datty Puritas observing with a
red pencil. 1000x1000, archive parchment plate."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("LLG-0375 Breeding Program Anomaly", 1000, 1000)

INK = "#33271E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#201E28"}, {"offset": 1, "color": "#0E0C14"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D9C9A4"}, {"offset": 0.72, "color": "#A8916B"},
    {"offset": 1, "color": "#6E5B40"}]}}
CAB_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A6448"}, {"offset": 1, "color": "#4E3E2C"}]}}
SKIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8C9A8"}, {"offset": 1, "color": "#B98F6A"}]}}
DATTY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A8C69A"}, {"offset": 1, "color": "#648A58"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#54462E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EFE3C4", strokeWidth=3, opacity=55)
d.shape("ellipse", "Patina 1", x=170, y=170, width=240, height=150,
        fill="#8C7852", opacity=25, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=680, width=250, height=140,
        fill="#8C7852", opacity=22, stroke=NONE)
for i, (x, y, w) in enumerate([(210,310,8),(790,250,7),(160,540,9),(830,550,8),
                               (260,780,7),(740,770,9),(140,430,6),(860,420,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E5A3C", opacity=40, stroke=NONE)

# --- floating frontmatter block, breedingProgram highlighted -------------------
FM = "FLOATING FRONTMATTER"
d.shape("ellipse", "FM shadow", x=330, y=170, width=360, height=160,
        fill="#3A2E20", opacity=18, stroke=NONE)
d.shape("rectangle", "Frontmatter card", x=330, y=160, width=360, height=150,
        radius=8, fill="#2E2A24", stroke=INK, strokeWidth=4)
d.text("---", "FM fence top", x=348, y=188, size=15, font="Virelai Sans",
       color="#8A7A5E")
d.text("name: applicant-self", "FM line 1", x=348, y=214, size=14,
       font="Virelai Sans", color="#B8A67E")
# highlighted key
d.shape("rectangle", "FM key highlight", x=344, y=224, width=272, height=22,
        radius=4, fill="#E8A33D", opacity=35, stroke=NONE)
d.text("breedingProgram: true", "FM line 2", x=348, y=241, size=14,
       font="Virelai Sans", color="#F2D48A")
d.text("species: human-origin", "FM line 3", x=348, y=268, size=14,
       font="Virelai Sans", color="#B8A67E")
d.text("---", "FM fence bottom", x=348, y=294, size=15,
       font="Virelai Sans", color="#8A7A5E")
# float ticks under the hovering card
for i, (tx, tl) in enumerate([(380, 10), (470, 16), (560, 10), (640, 14)]):
    d.path(f"M{tx},318 L{tx},{318+tl}", f"FM float {i+1}", fill=NONE,
           stroke="#8A7A5E", strokeWidth=3, opacity=40, cap="round")

# --- rejected robot lithium mine, far left distance ----------------------------
ROBOT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E8A92"}, {"offset": 1, "color": "#4E5A62"}]}}
d.shape("rectangle", "Robot body", x=150, y=380, width=86, height=64,
        radius=8, fill=ROBOT_GRAD, stroke=INK, strokeWidth=3, opacity=75)
d.shape("ellipse", "Robot eye", x=182, y=398, width=20, height=20,
        fill="#B03A2E", opacity=75, stroke=NONE)
# drill arm toward the ground
d.path("M236,420 L266,442 L258,458", "Robot drill", fill=NONE,
       stroke="#4E5A62", strokeWidth=8, opacity=75, cap="round")
# little lithium rocks
for i, (rx, ry) in enumerate([(262, 466), (276, 458), (252, 472)]):
    d.path(f"M{rx},{ry} L{rx+8},{ry-8} L{rx+16},{ry} L{rx+8},{ry+6} Z",
           f"Lithium {i+1}", fill="#9AA8B0", opacity=60, stroke=NONE)
# treads
d.shape("rectangle", "Robot tread", x=146, y=444, width=96, height=18,
        radius=9, fill="#3A4046", opacity=75, stroke=NONE)
# rejected: red slash across the whole machine
d.path("M136,368 L280,470", "Reject slash 1", fill=NONE, stroke="#B03A2E",
       strokeWidth=9, opacity=80, cap="round")
d.path("M280,368 L136,470", "Reject slash 2", fill=NONE, stroke="#B03A2E",
       strokeWidth=9, opacity=80, cap="round")

# --- the card catalog -----------------------------------------------------------
d.shape("rectangle", "Catalog", x=400, y=430, width=250, height=280,
        radius=8, fill=CAB_GRAD, stroke=INK, strokeWidth=5)
for r in range(4):
    for c in range(3):
        dx = 416 + c * 76
        dy = 446 + r * 64
        d.shape("rectangle", f"Drawer {r}-{c}", x=dx, y=dy, width=64,
                height=52, radius=4, fill="#6A563C", stroke=INK,
                strokeWidth=2)
        d.shape("rectangle", f"Drawer pull {r}-{c}", x=dx+16, y=dy+30,
                width=32, height=8, radius=3, fill="#3A2E20", stroke=NONE)
        d.shape("rectangle", f"Drawer label {r}-{c}", x=dx+14, y=dy+8,
                width=36, height=14, radius=2, fill="#E8DCC0", stroke=NONE)
# one drawer pulled open, glowing — the registry is receiving the human
d.shape("rectangle", "Open drawer", x=492, y=510, width=64, height=52,
        radius=4, fill="#E8DCC0", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Open drawer card", x=502, y=502, width=44, height=30,
        radius=2, fill="#F2EAD2", stroke=INK, strokeWidth=2)
d.path("M506,512 L542,512 M506,519 L534,519", "Card lines", fill=NONE,
       stroke="#8A7A5E", strokeWidth=2)

# --- the human, filing themself ---------------------------------------------------
HUMAN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5A6E82"}, {"offset": 1, "color": "#33455A"}]}}
# head + torso + legs — standing at the catalog, arm out with a card
d.shape("ellipse", "Human head", x=296, y=452, width=54, height=60,
        fill=SKIN_GRAD, stroke=INK, strokeWidth=3)
d.path("M296,512 C270,530 262,590 268,660 L344,660 C352,590 348,530 336,512 Z",
       "Human torso", fill=HUMAN_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Human leg L", x=284, y=660, width=20, height=72,
        fill="#2E3A48", stroke=NONE)
d.shape("rectangle", "Human leg R", x=312, y=660, width=20, height=72,
        fill="#2E3A48", stroke=NONE)
d.shape("ellipse", "Human shoe L", x=278, y=726, width=34, height=14,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Human shoe R", x=306, y=726, width=34, height=14,
        fill=INK, stroke=NONE)
# arm extended toward the open drawer, card in hand
d.path("M336,540 C380,540 430,534 468,530", "Human arm", fill=NONE,
       stroke="#5A6E82", strokeWidth=14, cap="round")
d.shape("rectangle", "Registry card", x=462, y=512, width=42, height=30,
        radius=2, fill="#F2EAD2", stroke=INK, strokeWidth=2)
d.path("M468,522 L498,522 M468,529 L490,529", "Registry card lines",
       fill=NONE, stroke="#8A7A5E", strokeWidth=2)
# face: looking at the drawer
d.shape("ellipse", "Human eye", x=328, y=478, width=8, height=10,
        fill="#2A1C16", stroke=NONE)
d.path("M324,500 Q333,504 340,498", "Human mouth", fill=NONE, stroke=INK,
       strokeWidth=3, cap="round")
# hair
d.path("M296,472 C296,444 350,444 350,472 C350,458 296,458 296,472 Z",
       "Human hair", fill="#4A3524", stroke=NONE)

# --- the mascots queued beside, watching the filing ------------------------------
def small_mascot(cx, top, w, h, grad, label):
    d.path(f"M{cx-w/2},{top+h*0.35} A{w/2},{h*0.35} 0 0 1 {cx+w/2},{top+h*0.35} "
           f"L{cx+w/2},{top+h} Q{cx},{top+h+8} {cx-w/2},{top+h} Z",
           f"{label} body", fill=grad, stroke=INK, strokeWidth=3)
    ey = top + h * 0.34
    d.shape("ellipse", f"{label} eye L", x=cx-14, y=ey, width=9, height=11,
            fill="#2A1C16", stroke=NONE)
    d.shape("ellipse", f"{label} eye R", x=cx+5, y=ey, width=9, height=11,
            fill="#2A1C16", stroke=NONE)

KINDY_G = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2D48A"}, {"offset": 1, "color": "#C79A4E"}]}}
BRICK_G = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E08A72"}, {"offset": 1, "color": "#A8543E"}]}}
small_mascot(690, 640, 56, 74, KINDY_G, "Mascot A")
small_mascot(762, 656, 52, 70, BRICK_G, "Mascot B")
# little registry number tags on the mascots — they belong here
d.shape("rectangle", "Mascot A tag", x=676, y=694, width=26, height=14,
        radius=2, fill="#E8DCC0", stroke=INK, strokeWidth=2)
d.shape("rectangle", "Mascot B tag", x=750, y=702, width=26, height=14,
        radius=2, fill="#E8DCC0", stroke=INK, strokeWidth=2)

# --- Datty Puritas observing, red pencil in hand ----------------------------------
d.path("M830,560 Q872,544 896,570 L896,676 Q862,692 830,676 Z",
       "Datty body", fill=DATTY_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Datty eye L", x=852, y=596, width=10, height=13,
        fill="#2A1C16", stroke=NONE)
d.shape("ellipse", "Datty eye R", x=876, y=596, width=10, height=13,
        fill="#2A1C16", stroke=NONE)
d.path("M852,626 Q866,632 882,624", "Datty mouth", fill=NONE, stroke=INK,
       strokeWidth=3, cap="round")
# red pencil held up, mid-annotation
d.path("M836,610 L800,570", "Datty pencil", fill=NONE, stroke="#B03A2E",
       strokeWidth=7, cap="round")
d.path("M800,570 L794,560 L806,564 Z", "Pencil tip", fill=INK, stroke=NONE)
# annotation mark floating off the pencil tip
d.path("M776,548 L796,548 M786,538 L786,558", "Annotation mark", fill=NONE,
       stroke="#B03A2E", strokeWidth=4, cap="round")

# --- the caption, on a small ruled strip ------------------------------------------
d.shape("rectangle", "Caption strip", x=170, y=806, width=660, height=34,
        radius=6, fill="#2E2A24", opacity=80, stroke=NONE)
d.text("The archive has decided it would rather adopt you than employ you.",
       "Caption", x=500, y=829, size=16, font="Virelai Sans",
       color="#E8DCC0", justify="center")

# --- name + role -------------------------------------------------------------------
d.text("REGISTRATION ANOMALY", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#EFE3C4", justify="center")
d.text("H U M A N - O R I G I N   R E G I S T R A T I O N", "Role",
       x=500, y=968, size=18, font="Virelai Sans", color="#B8A67E",
       justify="center")

d.finish("llg-0375-breeding-program-anomaly-V1R00")
