#!/usr/bin/env python3
"""Draft File Derrick — mascot portrait V1R00. Unfinalized Record Custodian:
a weary file-folder clerk with a 'draft' hang-tag and a custodian's keyring,
standing guard beside a draft window that never finishes ("Still saving…"),
a blinking cursor stalled over two unclosed parentheses, unsent drafts
piled at his feet. Dusty manila-and-lamplight palette. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Draft File Derrick — Mascot Plate", 1000, 1000)

INK = "#3E3226"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#1E1811"}, {"offset": 1, "color": "#0A0705"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8CDB4"}, {"offset": 0.62, "color": "#A69577"},
    {"offset": 1, "color": "#6E5E45"}]}}
FOLDER_GRAD = {"gradient": {"kind": "linear", "start": [0, 390], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#EAD9A8"}, {"offset": 0.55, "color": "#C9B27E"},
    {"offset": 1, "color": "#9A8052"}]}}
WINDOW_GRAD = {"gradient": {"kind": "linear", "start": [0, 200], "end": [0, 330], "stops": [
    {"offset": 0, "color": "#F0EAD8"}, {"offset": 1, "color": "#CFC4A8"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2EBD8"}, {"offset": 1, "color": "#D0C3A2"}]}}
AMBER = "#D89A3E"

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate -----------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#B09A70", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#2A2114", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8DFC8", strokeWidth=3, opacity=40)
# patina + flecks: the dust of unsent things
d.shape("ellipse", "Patina 1", x=190, y=160, width=240, height=150, fill="#C4B691", opacity=16, stroke=NONE)
d.shape("ellipse", "Patina 2", x=580, y=620, width=250, height=150, fill="#8A7A58", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(210,350,6),(790,340,5),(180,560,7),(830,570,6),(250,750,5),
                               (750,780,6),(150,460,5),(860,450,4),(440,130,5),(630,150,6),
                               (330,160,4),(700,230,5),(180,650,4),(540,120,4)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#EAE0C8", opacity=45, stroke=NONE)

# --- the draft window: open, never closing -------------------------------------------
WX, WY, WW, WH = 556, 202, 258, 128
d.shape("rectangle", "Window shadow", x=WX + 8, y=WY + 10, width=WW, height=WH, radius=12,
        fill="#2A2114", opacity=25, stroke=NONE)
d.shape("rectangle", "Window", x=WX, y=WY, width=WW, height=WH, radius=12,
        fill=WINDOW_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Title bar", x=WX, y=WY, width=WW, height=30, radius=12,
        fill="#4A4038", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Title bar square", x=WX, y=WY + 15, width=WW, height=15,
        fill="#4A4038", stroke=NONE)
for i, cx in enumerate([WX + 18, WX + 36, WX + 54]):
    d.shape("ellipse", f"Window dot {i+1}", x=cx - 5, y=WY + 10, width=10, height=10,
            fill=["#C46A5A", "#D8A34E", "#8AA06A"][i], stroke=INK, strokeWidth=1.5)
d.text("untitled (draft)", "Window title", x=WX + 132, y=WY + 21, size=13,
       font="Source Sans 3", color="#D8D0BC", justify="center")
d.text("Still saving…", "Window text", x=WX + WW / 2, y=WY + 82, size=21,
       font="Source Sans 3", color="#4A4038", justify="center")
# the three dots that never resolve
for i in range(3):
    d.shape("ellipse", f"Ellipsis dot {i+1}", x=WX + WW / 2 - 26 + i * 22, y=WY + 100,
            width=8, height=8, fill="#7A6E58", opacity=40 + i * 20, stroke=NONE)
for x, y in [(WX, WY), (WX + WW, WY), (WX, WY + WH), (WX + WW, WY + WH)]:
    assert on_disc(x, y, 6), (x, y)

# --- unclosed parentheses + the blinking cursor ---------------------------------------
# nested open parens, stroked: the sentence never lands
d.path("M780,442 C736,452 700,492 700,536 C700,580 736,620 780,630",
       "Paren outer", fill=NONE, stroke=INK, strokeWidth=11, cap="round")
d.path("M724,466 C694,474 670,502 670,534 C670,566 694,594 724,602",
       "Paren inner", fill=NONE, stroke=INK, strokeWidth=8, cap="round", opacity=75)
# block cursor parked where the third paren should be
d.shape("rectangle", "Cursor block", x=636, y=520, width=16, height=30,
        fill=AMBER, stroke=NONE, opacity=90)
d.shape("rectangle", "Cursor sheen", x=636, y=520, width=16, height=8,
        fill="#FFE8C0", stroke=NONE, opacity=70)
d.text("autosave", "Autosave note", x=700, y=668, size=13, font="Source Sans 3",
       color="#6E5E45", justify="center")

# --- Derrick: the folder clerk ----------------------------------------------------------
# ground shadow + the unsent pile at his feet
d.shape("ellipse", "Ground shadow", x=282, y=688, width=270, height=24,
        fill="#1E160C", opacity=28, stroke=NONE)
for k, (cx, cy, deg) in enumerate([(250, 680, -8), (285, 694, 4), (560, 688, 10)]):
    d.path(rot_rect_path(cx, cy, 64, 80, deg), f"Loose draft {k+1}",
           fill=PAPER_GRAD, stroke=INK, strokeWidth=2.5)
    d.path(rot_rect_path(cx + 14, cy - 30, 18, 14, deg), f"Draft fold {k+1}",
           fill="#B8A886", stroke=NONE, opacity=80)
    for j in range(3):
        d.path(rot_rect_path(cx, cy - 8 + j * 14, 40, 3, deg),
               f"Draft line {k+1}.{j+1}", fill="#8A7A5C", stroke=NONE, opacity=55)

# folder tab behind the body
d.shape("rectangle", "Folder tab", x=318, y=384, width=96, height=48, radius=12,
        fill=FOLDER_GRAD, stroke=INK, strokeWidth=6)
# body: the folder itself
d.shape("rectangle", "Body", x=300, y=416, width=258, height=276, radius=26,
        fill=FOLDER_GRAD, stroke=INK, strokeWidth=6)
# folder crease line across the top
d.path("M300,448 L558,448", "Folder crease", fill=NONE, stroke=INK,
       strokeWidth=3, opacity=50)
# belly highlight + bottom shade
d.shape("ellipse", "Body sheen", x=340, y=436, width=170, height=56,
        fill="#FFF6DC", opacity=22, stroke=NONE)
d.path("M320,662 C380,684 478,684 538,662 C480,676 380,676 320,662 Z",
       "Base shade", fill="#7A6238", opacity=35, stroke=NONE)

# hang-tag on a string from the tab: "draft"
d.path("M366,428 C356,452 344,468 330,478", "Tag string",
       fill=NONE, stroke=INK, strokeWidth=2.5)
d.path(rot_rect_path(316, 496, 78, 34, -12), "Draft tag",
       fill="#E8DCC0", stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Tag hole", x=352, y=484, width=7, height=7,
        fill="#A69577", stroke=INK, strokeWidth=2)
d.text("draft", "Tag text", x=312, y=504, size=16, font="Source Sans 3",
       color="#5A4A32", justify="center")

# face: two tired eyes, lids at half-mast, pupils small and resigned
def eye(cx, cy):
    d.shape("ellipse", f"Eye white {cx}", x=cx - 24, y=cy - 20, width=48, height=42,
            fill="#F6F0DC", stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Pupil {cx}", x=cx - 7, y=cy + 6, width=14, height=14,
            fill="#2E2416", stroke=NONE)
    d.shape("ellipse", f"Glint {cx}", x=cx - 4, y=cy + 9, width=4, height=4,
            fill="#FFFFFF", opacity=80, stroke=NONE)
    # heavy lid sagging over the top
    d.shape("ellipse", f"Lid {cx}", x=cx - 26, y=cy - 28, width=52, height=30,
            fill="#C9B27E", stroke=NONE)
    d.path(f"M{cx-22},{cy-14:.0f} C{cx-8},{cy-8:.0f} {cx+8},{cy-8:.0f} {cx+22},{cy-14:.0f}",
           f"Lid crease {cx}", fill=NONE, stroke=INK, strokeWidth=3,
           opacity=65, cap="round")
    # the permanent under-eye bag of unfinished business
    d.path(f"M{cx-18},{cy+26:.0f} C{cx-6},{cy+30:.0f} {cx+6},{cy+30:.0f} {cx+18},{cy+26:.0f}",
           f"Eye bag {cx}", fill=NONE, stroke="#7A6238", strokeWidth=2.5,
           opacity=55, cap="round")

eye(382, 512)
eye(478, 512)
# flat mouth: he has stopped expecting the save to complete
d.path("M402,600 L456,600", "Mouth", fill=NONE, stroke=INK, strokeWidth=5, cap="round")

# custodian's keyring on the right hip: keys to rooms no one opens
d.path("M558,560 C580,566 592,580 596,600", "Key arm",
       fill=NONE, stroke="#B39E6E", strokeWidth=18, cap="round")
d.shape("ellipse", "Key ring", x=584, y=596, width=34, height=34,
        fill=NONE, stroke="#D8C88E", strokeWidth=6)
d.path("M596,628 L596,664 L608,664 L608,652 L616,652 L616,644 L606,644 L606,628 Z",
       "Key 1", fill="#C8B06A", stroke=INK, strokeWidth=2.5)
d.path("M610,624 L624,656 L634,650 L628,642 L636,638 L630,630 L622,634 L616,620 Z",
       "Key 2", fill="#B89C56", stroke=INK, strokeWidth=2.5)

# feet
d.shape("ellipse", "Foot L", x=352, y=686, width=52, height=22,
        fill="#8A7448", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Foot R", x=456, y=686, width=52, height=22,
        fill="#8A7448", stroke=INK, strokeWidth=3)

# --- name + role ------------------------------------------------------------------------
d.text("DRAFT FILE DERRICK", "Name", x=500, y=930, size=54, font="Virelai Sans",
       color="#EADFC2", justify="center")
d.text("UNFINALIZED RECORD CUSTODIAN", "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#B8A884", justify="center")
doc = d.call("inspect_document", {"kind": "Type"}, "inspect type")
for n in (doc or {}).get("nodes", []):
    if str(n.get("name", "")) == "Role":
        d.call("run_command", {"command": "text.setStyle",
               "params": {"id": n["id"], "tracking": 220}}, "track role")

d.finish("009.draft-file-derrick-V1R00")
