#!/usr/bin/env python3
"""Pocket Consensus — mascot portrait V1R00.
A warm pocket-dwelling mascot sealing a folded micro-agreement at body
temperature, in the seconds between the third nod and the first agenda item.
Three figures in a hallway; the room has not filled yet.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Pocket Consensus — Mascot Portrait", 1000, 1000)

INK = "#33261F"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1E140C"}, {"offset": 1, "color": "#0D0906"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E5638"}, {"offset": 0.7, "color": "#413024"},
    {"offset": 1, "color": "#1D140C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A2C20"}, {"offset": 1, "color": "#17100A"}]}}
COAT_A = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#544E66"}, {"offset": 1, "color": "#2C2838"}]}}
COAT_B = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E5A52"}, {"offset": 1, "color": "#28332C"}]}}
COAT_C = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E483A"}, {"offset": 1, "color": "#322420"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8C0A2"}, {"offset": 1, "color": "#A88E70"}]}}
IMP_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4C464"}, {"offset": 0.7, "color": "#D8952E"},
    {"offset": 1, "color": "#9A5E18"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F2EAD8"}, {"offset": 1, "color": "#CDBF9E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A8886A", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EEDCC0", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#584430", opacity=45, stroke=NONE)

# --- the hallway: sconce glow, far door, converging baseboards -------------------
d.shape("ellipse", "Sconce glow", x=410, y=110, width=180, height=140,
        fill="#F0C878", opacity=12, stroke=NONE)
d.shape("ellipse", "Sconce glow 2", x=455, y=140, width=90, height=75,
        fill="#F0C878", opacity=14, stroke=NONE)
d.shape("rectangle", "Sconce", x=486, y=172, width=28, height=36,
        fill="#8A6A34", stroke=INK, strokeWidth=3, radius=6)
d.shape("ellipse", "Sconce flame", x=491, y=158, width=18, height=22,
        fill="#F0D08A", opacity=85, stroke=INK, strokeWidth=2)
# the door the larger room will arrive through — distant, between the group
d.shape("rectangle", "Door frame", x=566, y=238, width=86, height=144,
        fill="#241A12", stroke=INK, strokeWidth=4, radius=3)
d.shape("rectangle", "Door slab", x=575, y=247, width=63, height=126,
        fill="#3A2C1E", stroke=INK, strokeWidth=3, radius=2)
d.shape("rectangle", "Door light", x=641, y=247, width=6, height=126,
        fill="#D8A860", opacity=35, stroke=NONE)
d.shape("ellipse", "Door knob", x=632, y=305, width=7, height=7,
        fill="#8A6A34", stroke=NONE)
# baseboards converging on the doorway
d.path("M185,690 L566,385 M835,690 L652,385", "Baseboards", fill=NONE,
       stroke="#241A12", strokeWidth=5, cap="round", opacity=70)
d.path("M185,672 L566,378 M835,672 L652,378", "Baseboard caps", fill=NONE,
       stroke="#584430", strokeWidth=3, cap="round", opacity=45)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#120C08",
       strokeWidth=4, opacity=70)

# --- three figures mid-nod -----------------------------------------------------------
def figure(cx, head_y, coat, label, eye_dir):
    # eye_dir: +1 if glancing right, -1 if glancing left, 0 if facing out
    d.shape("ellipse", f"{label} shadow", x=cx-78, y=688, width=156,
            height=20, fill="#0C0805", opacity=50, stroke=NONE)
    # coat: shoulders to floor
    d.path(f"M{cx-58},{head_y+62} C{cx-70},{head_y+70} {cx-76},{head_y+88} "
           f"{cx-78},{head_y+110} L{cx-84},700 L{cx+84},700 "
           f"L{cx+78},{head_y+110} C{cx+76},{head_y+88} {cx+70},{head_y+70} "
           f"{cx+58},{head_y+62} Z",
           f"{label} coat", fill=coat, stroke=INK, strokeWidth=6,
           join="round")
    # lapels
    d.path(f"M{cx-16},{head_y+66} L{cx-30},{head_y+112} L{cx-12},{head_y+96}",
           f"{label} lapel L", fill=NONE, stroke=INK, strokeWidth=3.5,
           opacity=70)
    d.path(f"M{cx+16},{head_y+66} L{cx+30},{head_y+112} L{cx+12},{head_y+96}",
           f"{label} lapel R", fill=NONE, stroke=INK, strokeWidth=3.5,
           opacity=70)
    for k in range(3):
        d.shape("ellipse", f"{label} button {k+1}", x=cx-4,
                y=head_y+130+k*40, width=8, height=8, fill="#1E1610",
                stroke=NONE, opacity=80)
    # head, tipped a nod forward
    d.shape("ellipse", f"{label} head", x=cx-26, y=head_y, width=52,
            height=58, fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
    # ear + hairline hint
    d.path(f"M{cx-20},{head_y+16} C{cx-12},{head_y+6} {cx+12},{head_y+6} "
           f"{cx+20},{head_y+16}", f"{label} hair", fill=NONE, stroke=INK,
           strokeWidth=4, cap="round", opacity=60)
    # eyes mid-lower on the face — the nod lowers the gaze
    ex = cx + eye_dir*7
    d.path(f"M{ex-16},{head_y+36} C{ex-12},{head_y+41} {ex-6},{head_y+41} "
           f"{ex-3},{head_y+36}", f"{label} eye L", fill=NONE, stroke=INK,
           strokeWidth=3.5, cap="round")
    d.path(f"M{ex+3},{head_y+36} C{ex+7},{head_y+41} {ex+13},{head_y+41} "
           f"{ex+16},{head_y+36}", f"{label} eye R", fill=NONE, stroke=INK,
           strokeWidth=3.5, cap="round")
    # the nod itself: twin arcs beside the chin
    nx = cx + eye_dir*30
    d.path(f"M{nx-8},{head_y+34} C{nx-2},{head_y+44} {nx-6},{head_y+54} "
           f"{nx-12},{head_y+62}", f"{label} nod 1", fill=NONE,
           stroke="#E0C898", strokeWidth=3, cap="round", opacity=55)
    d.path(f"M{nx+6},{head_y+30} C{nx+12},{head_y+42} {nx+8},{head_y+54} "
           f"{nx+2},{head_y+64}", f"{label} nod 2", fill=NONE,
           stroke="#E0C898", strokeWidth=3, cap="round", opacity=40)

figure(340, 392, COAT_A, "Fig A", 1)    # glancing in, right
figure(700, 402, COAT_C, "Fig C", -1)   # glancing in, left
figure(520, 376, COAT_B, "Fig B", 0)    # host of the pocket, faces out

# --- the micro-agreement going into the breast pocket ---------------------------------
# breast pocket on Fig B's left chest (viewer's right)
d.shape("rectangle", "Pocket", x=548, y=536, width=48, height=40,
        fill="#3A463E", stroke=INK, strokeWidth=4, radius=4)
d.path("M548,548 L596,548", "Pocket slit", fill=NONE, stroke="#141C16",
       strokeWidth=3)
# folded agreement, half in — the crease was made standing
d.path(rot_rect_path(562, 528, 34, 30, -10), "Agreement", fill=PAPER_GRAD,
       stroke=INK, strokeWidth=3)
d.path("M552,520 L574,528 L558,540 Z", "Agreement fold", fill="#DCD0B4",
       stroke=INK, strokeWidth=2, join="round", opacity=90)
d.shape("ellipse", "Agreement seal", x=563, y=530, width=9, height=9,
        fill="#A84838", stroke=INK, strokeWidth=1.5)
# a pocket's warmth: it is sealed at body temperature
d.shape("ellipse", "Pocket warmth", x=538, y=500, width=104, height=94,
        fill="#F0B858", opacity=13, stroke=NONE)

# --- the mascot: a warm pocket imp finishing the seal ----------------------------------
d.shape("ellipse", "Imp glow", x=566, y=510, width=90, height=86,
        fill="#F4C464", opacity=12, stroke=NONE)
# body perched on the pocket's edge
d.path("M582,556 C582,534 596,520 612,520 C630,520 642,534 642,554 "
       "C642,572 632,584 612,584 C594,584 582,574 582,556 Z",
       "Imp body", fill=IMP_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Imp sheen", x=592, y=528, width=30, height=14,
        fill="#FFFFFF", opacity=22, stroke=NONE)
# feet hooked over the pocket lip
d.path("M592,582 C592,590 588,594 584,594 M626,582 C626,590 630,594 634,594",
       "Imp feet", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# face: focused, pleased
d.path("M598,544 C602,540 608,540 611,544", "Imp eye L", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
d.path("M619,544 C622,540 628,540 632,544", "Imp eye R", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
d.path("M606,560 C610,564 617,564 621,560", "Imp smile", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
d.shape("ellipse", "Imp blush L", x=592, y=550, width=12, height=7,
        fill="#C06A40", opacity=45, stroke=NONE)
d.shape("ellipse", "Imp blush R", x=628, y=550, width=12, height=7,
        fill="#C06A40", opacity=45, stroke=NONE)
# arms pressing the agreement down into the pocket
d.path("M584,556 C572,550 566,542 564,532", "Imp arm L", fill=NONE,
       stroke=INK, strokeWidth=6, cap="round")
d.shape("ellipse", "Imp hand L", x=558, y=526, width=13, height=11,
        fill="#D8952E", stroke=INK, strokeWidth=2.5)
# the wax-seal thumb: its mark is the sealing itself
d.shape("ellipse", "Imp seal thumb", x=560, y=524, width=7, height=7,
        fill="#A84838", stroke=NONE, opacity=85)
# a single warm mote above the work
d.shape("ellipse", "Warm mote", x=610, y=492, width=6, height=6,
        fill="#F4C464", opacity=45, stroke=NONE)
d.shape("ellipse", "Warm mote 2", x=560, y=478, width=5, height=5,
        fill="#F4C464", opacity=35, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("POCKET CONSENSUS", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#F4E4CC", justify="center")
r = d.text("SEALED BEFORE THE ROOM FILLS", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8A880", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("258.pocket-consensus-V1R00")
