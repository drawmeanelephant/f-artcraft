#!/usr/bin/env python3
"""Kindy McExistentialcrisis — mascot portrait V1R00.
Junior Verification Officer: a small apologetic mascot in the cone of a
dim pendant lamp, oversized verification clipboard clutched to its chest
(Form 51-E, boxes half-ticked), a CRT at its elbow looping the same log
lines forever. Institutional sage plate, phosphor green screen, one
devastated little sweat drop. 1000x1000.
House style: gradients + translucent shading, never flat fills.
Plate = circle center (500,460) r420."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Kindy McExistentialcrisis — Mascot Plate", 1000, 1000)

INK = "#262A24"   # warm dark ink, never black
BG_GRAD = {"gradient": {"kind": "linear", "start": [0, 0], "end": [0, 1000], "stops": [
    {"offset": 0, "color": "#131A14"}, {"offset": 1, "color": "#070A07"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#AEB8A0"}, {"offset": 0.62, "color": "#707E66"},
    {"offset": 1, "color": "#3E4A3C"}]}}
BODY_GRAD = {"gradient": {"kind": "linear", "start": [0, 400], "end": [0, 720], "stops": [
    {"offset": 0, "color": "#E0C2B4"}, {"offset": 0.55, "color": "#B08A7C"},
    {"offset": 1, "color": "#7C584E"}]}}
BELLY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F2E4D8"}, {"offset": 1, "color": "#CEAFA0"}]}}
CASE_GRAD = {"gradient": {"kind": "linear", "start": [0, 360], "end": [0, 600], "stops": [
    {"offset": 0, "color": "#565E52"}, {"offset": 1, "color": "#343A32"}]}}
SCR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#1E3A28"}, {"offset": 1, "color": "#0C1C12"}]}}
BOARD_GRAD = {"gradient": {"kind": "linear", "start": [0, 470], "end": [0, 700], "stops": [
    {"offset": 0, "color": "#D8C8A0"}, {"offset": 1, "color": "#A8946C"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0EAD4"}, {"offset": 1, "color": "#D4C9A8"}]}}

PCX, PCY, PR = 500, 460, 420

def on_disc(x, y, pad=0):
    return math.hypot(x - PCX, y - PCY) <= PR - pad

# --- backdrop + plate ---------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate halo", x=60, y=20, width=880, height=880,
        fill="#8E9A80", opacity=8, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#1A2018", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8DCC8", strokeWidth=3, opacity=38)
# filing-room patina
d.shape("ellipse", "Patina 1", x=170, y=560, width=240, height=150,
        fill="#8A9478", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=580, y=150, width=250, height=140,
        fill="#C4CCB2", opacity=14, stroke=NONE)
for i, (x, y, w) in enumerate([(198,335,6),(812,320,5),(168,540,7),(848,548,6),
                               (250,762,5),(740,758,6),(144,436,5),(858,612,5),
                               (330,150,4),(704,206,5),(216,646,4),(876,446,4),
                               (398,118,5),(602,124,5)]):
    assert on_disc(x, y, 12), (x, y)
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#E4E8D6", opacity=42, stroke=NONE)
# ghost arcs on the dark backdrop
d.path("M62,150 A95,95 0 0 1 157,62", "Ghost arc TL",
       fill=NONE, stroke="#4E5E4A", strokeWidth=14, opacity=10, cap="round")
d.path("M938,762 A110,110 0 0 1 848,874", "Ghost arc BR",
       fill=NONE, stroke="#4E5E4A", strokeWidth=10, opacity=8, cap="round")

# --- the dim overhead light --------------------------------------------------------------
# pendant cord + shade at the top of the disc
d.path("M500,66 L500,128", "Lamp cord", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")
d.path("M462,166 L538,166 L522,124 L478,124 Z", "Lamp shade",
       fill="#3A4034", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Bulb", x=490, y=164, width=20, height=18,
        fill="#F4E0A0", opacity=90, stroke=INK, strokeWidth=3)
# the cone of dim light falling on the scene
d.path("M472,180 L528,180 L800,722 L200,722 Z", "Light cone",
       fill="#F4E8C0", opacity=9, stroke=NONE)
d.path("M482,182 L518,182 L640,700 L360,700 Z", "Light cone core",
       fill="#F8EED2", opacity=8, stroke=NONE)
# pool of light on the ground
d.shape("ellipse", "Light pool", x=210, y=676, width=580, height=76,
        fill="#F4E8C0", opacity=10, stroke=NONE)

# --- the CRT looping its logs ----------------------------------------------------------------
# keyboard slab first
d.shape("rectangle", "Keyboard", x=618, y=600, width=230, height=44, radius=10,
        fill="#424A40", stroke=INK, strokeWidth=4)
d.path("M634,614 L822,614 M634,624 L822,624 M634,634 L800,634",
       "Key grooves", fill=NONE, stroke="#5E6A58", strokeWidth=4,
       cap="round", opacity=80)
# case
d.shape("rectangle", "CRT case", x=612, y=356, width=252, height=236,
        radius=16, fill=CASE_GRAD, stroke=INK, strokeWidth=6)
# screen bulge
d.shape("rectangle", "CRT screen", x=632, y=376, width=182, height=146,
        radius=14, fill=SCR_GRAD, stroke="#121A10", strokeWidth=4)
# scanlines
for i in range(4):
    d.shape("rectangle", f"Scan {i+1}", x=636, y=390 + i * 32, width=174,
            height=4, fill="#000000", opacity=18, stroke=NONE)
# the looping logs: same five lines, forever
log_w = [120, 84, 132, 66, 104]
for i, w in enumerate(log_w):
    d.shape("rectangle", f"Log {i+1}", x=644, y=392 + i * 22, width=w,
            height=8, radius=3, fill="#7FE08A", opacity=80, stroke=NONE)
# one amber warning line that always comes back
d.shape("rectangle", "Log warn", x=644, y=392 + 2 * 22, width=40,
        height=8, radius=3, fill="#E8C45E", opacity=90, stroke=NONE)
# the loop arrow, chasing itself at the bottom of the screen
d.path("M768,506 A17,17 0 1 1 756,478", "Loop arc",
       fill=NONE, stroke="#7FE08A", strokeWidth=4, opacity=85, cap="round")
d.path("M750,472 L766,474 L754,486 Z", "Loop arrow",
       fill="#7FE08A", opacity=85, stroke=NONE)
# vents + power LED + badge
for i in range(4):
    d.path("M826,%d L842,%d" % (392 + i * 14, 392 + i * 14),
           f"Vent {i+1}", fill=NONE, stroke="#5E6A58", strokeWidth=4,
           cap="round")
d.shape("ellipse", "CRT LED", x=830, y=470, width=12, height=12,
        fill="#8AE07A", stroke=INK, strokeWidth=2)
d.text("EXIST", "CRT badge", x=834, y=516, size=13, font="Virelai Sans",
       color="#C9CDB6", justify="center")
# green phosphor wash on the floor in front of the set
d.shape("ellipse", "Phosphor wash", x=600, y=560, width=240, height=60,
        fill="#7FE08A", opacity=10, stroke=NONE)
for x, y in [(612, 356), (864, 356), (864, 592), (612, 592)]:
    assert on_disc(x, y, 0), (x, y)

# --- ground shadows (the dim light still casts them) ---------------------------------------
d.shape("ellipse", "Ground shadow", x=210, y=694, width=300, height=28,
        fill="#141A12", opacity=30, stroke=NONE)
d.shape("ellipse", "CRT shadow", x=596, y=648, width=270, height=24,
        fill="#141A12", opacity=26, stroke=NONE)

# --- Kindy ---------------------------------------------------------------------------
KX, KY = 350, 572

def body_path(cx, cy):
    return ("M%.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f "
            "C%.0f,%.0f %.0f,%.0f %.0f,%.0f Z" % (
        cx,      cy - 152,
        cx + 110, cy - 152, cx + 146, cy - 80, cx + 138, cy - 6,
        cx + 130, cy + 88,  cx + 88,  cy + 136, cx,       cy + 136,
        cx - 92,  cy + 136, cx - 132, cy + 90,  cx - 140, cy - 2,
        cx - 148, cy - 78,  cx - 112, cy - 152, cx,       cy - 152))

d.path(body_path(KX, KY), "Body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# belly + sheen + shade
d.shape("ellipse", "Belly", x=272, y=574, width=156, height=114,
        fill=BELLY_GRAD, opacity=70, stroke=NONE)
d.shape("ellipse", "Head sheen", x=262, y=426, width=180, height=60,
        fill="#FFFFFF", opacity=20, stroke=NONE)
d.path("M252,678 C310,702 392,702 448,676 C392,694 306,694 252,678 Z",
       "Base shade", fill="#5E4238", opacity=32, stroke=NONE)

# feet
d.shape("ellipse", "Foot L", x=258, y=694, width=70, height=28,
        fill="#8A6256", stroke=INK, strokeWidth=5)
d.shape("ellipse", "Foot R", x=376, y=694, width=70, height=28,
        fill="#8A6256", stroke=INK, strokeWidth=5)

# --- the oversized clipboard, clutched to the chest ------------------------------------
cb = []
def cbshape(shape_, label, **kw):
    r = d.shape(shape_, label, **kw); cb.append(r); return r
def cbpath(dd, label, **kw):
    r = d.path(dd, label, **kw); cb.append(r); return r
def cbtext(t, label, **kw):
    r = d.text(t, label, **kw); cb.append(r); return r

cbshape("rectangle", "Clip board", x=204, y=512, width=150, height=188,
        radius=10, fill=BOARD_GRAD, stroke=INK, strokeWidth=5)
# metal clip
cbshape("rectangle", "Clip", x=242, y=504, width=74, height=26, radius=10,
        fill="#8E9690", stroke=INK, strokeWidth=4)
cbshape("ellipse", "Clip bolt", x=272, y=512, width=14, height=10,
        fill="#5E665E", stroke=INK, strokeWidth=2)
# the form itself
cbshape("rectangle", "Form sheet", x=216, y=528, width=126, height=160,
        radius=4, fill=PAPER_GRAD, stroke="#8E7E5E", strokeWidth=2)
t = cbtext("FORM 51-E", "Form title", x=279, y=552, size=14,
           font="Virelai Sans", color="#5E5238", justify="center")
if t and t.get("id"):
    # Virelai has no digits: byte-range fallback for "51"
    d.cmd("text.setStyle", "form digits", ids=[t["id"]], start=5, end=7,
          font="Source Sans 3")
cbpath("M224,562 L334,562", "Title rule", fill=NONE, stroke="#B4A480",
       strokeWidth=2)
# four verification rows: box + label line
row_states = ["tick", "tick", "nope", "blank"]
for i, st_ in enumerate(row_states):
    y = 574 + i * 28
    cbshape("rectangle", f"Box {i+1}", x=226, y=y, width=18, height=18,
            radius=3, fill="#F8F2E0", stroke="#6E6046", strokeWidth=2.5)
    if st_ == "tick":
        cbpath("M230,%d L235,%d L243,%d" % (y + 9, y + 13, y + 4),
               f"Tick {i+1}", fill=NONE, stroke="#4E7A46",
               strokeWidth=3.5, cap="round", join="round")
    elif st_ == "nope":
        cbpath("M230,%d L240,%d M240,%d L230,%d" % (y + 5, y + 14,
               y + 5, y + 14), f"Nope {i+1}", fill=NONE,
               stroke="#A84A3E", strokeWidth=3, cap="round")
    else:
        cbtext("?", "Blank q", x=235, y=y + 15, size=13,
               font="Source Sans 3", color="#8E7E5E", justify="center")
    cbshape("rectangle", f"Row line {i+1}", x=252, y=y + 6, width=78,
            height=5, radius=2, fill="#A89878", opacity=80, stroke=NONE)
# a Friendly Warning sticky flagged off the top corner
cbshape("rectangle", "Warning tab", x=330, y=524, width=34, height=30,
        radius=4, fill="#E8C45E", stroke=INK, strokeWidth=2.5)
for r in cb:
    if r and r.get("id"):
        d.cmd("object.rotate", f"cb rot {r['id']}", ids=[r["id"]],
              angle=-7, origin=[279, 607])

# arms + paws: both wrapped onto the clipboard
# right arm reaches from the body to the board's right edge
d.path("M462,602 C430,606 398,600 372,590", "Arm R",
       fill=NONE, stroke="#B08A7C", strokeWidth=24, cap="round")
d.shape("ellipse", "Paw R", x=348, y=574, width=32, height=30,
        fill="#C09888", stroke=INK, strokeWidth=4)
# left paw just peeking around the board's lower-left corner
d.shape("ellipse", "Paw L", x=200, y=646, width=30, height=28,
        fill="#C09888", stroke=INK, strokeWidth=4)
d.path("M214,650 C226,640 234,628 236,616", "Grip curl",
       fill=NONE, stroke=INK, strokeWidth=3, cap="round", opacity=70)

# face: one eye wide with dread, one mid-blink of pure apology
# left eye — wide
d.shape("ellipse", "Eye white L", x=400, y=458, width=48, height=46,
        fill="#F8F2E8", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil L", x=417, y=470, width=16, height=16,
        fill="#2E2624", stroke=NONE)
d.shape("ellipse", "Glint L", x=421, y=474, width=5, height=5,
        fill="#FFFFFF", opacity=90, stroke=NONE)
# right eye — mid-blink, lid sliding
d.shape("ellipse", "Eye white R", x=344, y=458, width=46, height=44,
        fill="#F8F2E8", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Pupil R", x=360, y=476, width=14, height=14,
        fill="#2E2624", stroke=NONE)
d.shape("ellipse", "Lid R", x=340, y=452, width=54, height=26,
        fill="#C09888", stroke=NONE)
d.path("M346,474 C358,479 374,479 386,474", "Blink crease",
       fill=NONE, stroke=INK, strokeWidth=3.5, opacity=75, cap="round")
# brows: the apologetic pair, left up, right level
d.path("M402,446 C414,438 430,436 442,442", "Brow R2",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
d.path("M348,440 C360,430 376,428 388,434", "Brow L2",
       fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
# small uncertain wavy smile — cheerful, technically
d.path("M384,548 C396,542 408,554 420,548 C428,544 434,548 438,552",
       "Mouth", fill=NONE, stroke=INK, strokeWidth=4.5, cap="round")
# one devastated little sweat drop off the temple
d.path("M470,452 C482,468 486,480 470,486 C454,480 458,468 470,452 Z",
       "Sweat drop", fill="#BFE0EC", stroke=INK, strokeWidth=2.5, opacity=90)
# faint blush — the job requires it
d.shape("ellipse", "Blush", x=404, y=522, width=28, height=14,
        fill="#C87E6E", opacity=38, stroke=NONE)

# --- name + role ---------------------------------------------------------------------------
d.text("KINDY MCEXISTENTIALCRISIS", "Name", x=500, y=930, size=40,
       font="Virelai Sans", color="#E4E2CE", justify="center")
r = d.text("JUNIOR VERIFICATION OFFICER", "Role", x=500, y=968, size=21,
           font="Virelai Sans", color="#A8B29A", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=140)

d.finish("019.kindy-mcexistentialcrisis-V1R00")
