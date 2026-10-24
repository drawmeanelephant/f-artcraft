#!/usr/bin/env python3
"""Scopekeeper Emeritus — mascot portrait V1R00.
The custodian finishing the cordon: beige boundary tabs staked with a
surveyor's care around the patch that could not survive being seen,
certificate hung neat and facing inward. Within declared scope.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Scopekeeper Emeritus — Mascot Portrait", 1000, 1000)

INK = "#241E16"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A1B15"}, {"offset": 1, "color": "#12110D"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#57544A"}, {"offset": 0.7, "color": "#3B3830"},
    {"offset": 1, "color": "#1D1B16"}]}}
SCOPE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A8066"}, {"offset": 0.75, "color": "#5C5544"},
    {"offset": 1, "color": "#332E24"}]}}
PATCH_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#1E1A14"}, {"offset": 0.8, "color": "#14110C"},
    {"offset": 1, "color": "#0D0B08"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C4B598"}, {"offset": 0.7, "color": "#9A8A6C"},
    {"offset": 1, "color": "#6E604A"}]}}
PARCH_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDE2C6"}, {"offset": 1, "color": "#C9B892"}]}}
FRAME_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5A38"}, {"offset": 1, "color": "#4A3520"}]}}
TAB_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDE0C2"}, {"offset": 1, "color": "#C4B290"}]}}
SASH_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#47684E"}, {"offset": 1, "color": "#263E2C"}]}}
SEAL_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C05A4E"}, {"offset": 1, "color": "#7E2E28"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A7460", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8CDB4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(198,238,8),(800,234,7),(162,530,9),(836,550,8),
                               (252,766,7),(750,752,9),(140,398,6),(862,394,7),
                               (396,116,7),(612,112,8),(338,824,6),(664,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#45423A", opacity=45, stroke=NONE)

# --- the declared scope: a wash of legibility over the tidy half ----------------
d.path("M180,220 C320,160 560,140 700,180 C820,214 876,320 860,430 "
       "C846,530 760,600 650,620 C560,636 500,600 480,540 "
       "C452,462 420,436 380,424 C300,408 240,400 210,380 "
       "C166,336 150,268 180,220 Z",
       "Scope wash", fill=SCOPE_GRAD, opacity=35, stroke=NONE)

# --- floor under it all, closed on the disc arc --------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#3E392E"}, {"offset": 1, "color": "#1B1812"}]}},
       stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#100D09",
       strokeWidth=4, opacity=70)

# --- the excluded: a dark patch, faintly scribbled, lower left -------------------
d.path("M232,560 C220,516 252,478 300,470 C348,462 396,476 420,512 "
       "C444,548 440,600 412,634 C384,668 330,684 288,668 "
       "C252,654 240,612 232,560 Z", "Excluded patch",
       fill=PATCH_GRAD, stroke="#0A0806", strokeWidth=4)
# what lies beyond the boundary: dim tangles, kept in order by not being kept
d.path("M268,540 C290,520 320,522 318,546 C316,568 288,568 292,592 "
       "C296,614 328,610 330,634", "Tangle 1", fill=NONE,
       stroke="#4A4438", strokeWidth=3, opacity=55, cap="round")
d.path("M340,500 C360,506 374,522 370,544 C366,566 344,572 350,596",
       "Tangle 2", fill=NONE, stroke="#4A4438", strokeWidth=3,
       opacity=45, cap="round")
d.path("M280,610 C300,606 320,612 336,626 M296,646 C310,640 326,642 340,652",
       "Tangle 3", fill=NONE, stroke="#443E32", strokeWidth=2.5,
       opacity=40, cap="round")
# one sheet edge poking out — entered once, at the edge
d.path("M384,648 L416,642 L420,664 L390,670 Z", "Escaped sheet",
       fill="#6A6250", opacity=45, stroke=NONE)

# --- the boundary cordon: stakes, cord, beige tabs --------------------------------
CORDON = [(210, 520), (196, 586), (216, 652), (268, 706), (346, 726), (418, 694)]
# sagging cord between the stakes
for i in range(len(CORDON) - 1):
    x1, y1 = CORDON[i]; x2, y2 = CORDON[i + 1]
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + 14
    d.path(f"M{x1},{y1} Q{mx},{my} {x2},{y2}", f"Cord {i+1}", fill=NONE,
           stroke="#C9B892", strokeWidth=2.5, opacity=70)
# stakes with beige boundary tabs, each planted true
for i, (sx, sy) in enumerate(CORDON):
    d.path(f"M{sx},{sy} L{sx},{sy + 44}", f"Stake {i+1}", fill=NONE,
           stroke="#6E6046", strokeWidth=4, cap="round")
    ang = -14 if i % 2 == 0 else 10
    d.path(rot_rect_path(sx + 14, sy + 2, 30, 18, ang), f"Tab {i+1}",
           fill=TAB_GRAD, stroke=INK, strokeWidth=2.5, join="round")
    # the logged initial — a tiny mark on each tab
    d.path(f"M{sx + 8},{sy + 4} L{sx + 18},{sy + 2}", f"Tab mark {i+1}",
           fill=NONE, stroke="#8A7A5C", strokeWidth=2, opacity=80,
           cap="round")

# --- the certificate, hung neat and facing inward ---------------------------------
d.path(rot_rect_path(676, 300, 200, 150, -4), "Certificate frame",
       fill=FRAME_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path(rot_rect_path(676, 300, 176, 128, -4), "Certificate",
       fill=PARCH_GRAD, stroke="#8A7A5C", strokeWidth=2.5, join="round")
# fine lines of the certified text
for i, dy in enumerate((-38, -22, -6, 10)):
    d.path(f"M616,{300 + dy} L720,{292 + dy}", f"Cert line {i+1}",
           fill=NONE, stroke="#9A8C6C", strokeWidth=2.5, opacity=75,
           cap="round")
# ribbon seal: tails tucked under, medallion on top
d.path("M704,332 L696,362 L710,354 L720,364 L718,334 Z", "Seal tails",
       fill="#8E342E", stroke=INK, strokeWidth=2.5, join="round")
d.shape("ellipse", "Cert seal", x=688, y=318, width=36, height=36,
        fill=SEAL_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Cert seal inner", x=697, y=327, width=18, height=18,
        fill=NONE, stroke="#5E1E1A", strokeWidth=2, opacity=80)

# --- a tidy stack of bound files, the auditable edge -------------------------------
for i, (fy, fw) in enumerate([(640, 130), (616, 116), (594, 122)]):
    d.shape("rectangle", f"File {i+1}", x=640 - fw/2, y=fy, width=fw,
            height=20, fill=PARCH_GRAD, stroke=INK, strokeWidth=3, radius=3)
    d.path(f"M{640 - fw/2 + 8},{fy + 10} L{640 + fw/2 - 8},{fy + 10}",
           f"File line {i+1}", fill=NONE, stroke="#9A8C6C",
           strokeWidth=2, opacity=70, cap="round")

# --- the Scopekeeper Emeritus: spectacles, sash, mallet ------------------------------
d.shape("ellipse", "Body", x=505, y=520, width=180, height=150,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# the stole of office, worn over the audit
d.path("M540,540 C560,600 590,650 640,690 L610,700 C566,660 534,606 "
       "520,548 Z", "Sash", fill=SASH_GRAD, stroke=INK, strokeWidth=3.5,
       join="round", opacity=92)
d.path("M534,548 C552,604 582,652 626,688", "Sash edge", fill=NONE,
       stroke="#C9A85C", strokeWidth=2.5, opacity=70)
d.shape("ellipse", "Sash seal", x=606, y=668, width=26, height=26,
        fill=SEAL_GRAD, stroke=INK, strokeWidth=3)
# ears gone slightly grey with tenure
for ex in (542, 668):
    d.shape("ellipse", f"Ear {ex}", x=ex - 12, y=340, width=25, height=23,
            fill="#9A8A6C", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Head", x=522, y=350, width=156, height=140,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# spectacles: courteous severity, framed
for gx in (562, 638):
    d.shape("ellipse", f"Lens {gx}", x=gx - 22, y=404, width=44, height=40,
            fill=NONE, stroke=INK, strokeWidth=3.5)
d.path("M584,420 L616,420", "Spec bridge", fill=NONE, stroke=INK,
       strokeWidth=3.5, cap="round")
d.path("M540,414 L522,406 M660,414 L678,406", "Spec arms", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")
d.shape("ellipse", "Eye L", x=557, y=418, width=12, height=14,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=633, y=418, width=12, height=14,
        fill=INK, stroke=NONE)
# the mouth that declines to look away — it looks elsewhere, on paper
d.path("M582,466 C592,471 606,471 616,466", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
# grey whisker ticks of emeritus rank
for side, wx in ((-1, 530), (1, 672)):
    for j in range(2):
        d.path(f"M{wx},{440 + j*12} L{wx + side*22},{436 + j*12}",
               f"Whisker {side},{j}", fill=NONE, stroke="#7A6E56",
               strokeWidth=2.5, opacity=70, cap="round")

# the reaching arm, planting the next tab
d.path("M520,590 C470,610 440,640 424,674", "Arm planting", fill=NONE,
       stroke="#9A8A6C", strokeWidth=16, cap="round")
d.shape("ellipse", "Paw on stake", x=402, y=664, width=32, height=26,
        fill="#C4B598", stroke=INK, strokeWidth=4)
# the loose tab in the other paw, beige and ready
d.path("M680,590 C700,606 712,624 718,646", "Arm tabs", fill=NONE,
       stroke="#9A8A6C", strokeWidth=15, cap="round")
d.shape("ellipse", "Paw tabs", x=706, y=640, width=30, height=25,
        fill="#C4B598", stroke=INK, strokeWidth=4)
for j, dy in enumerate((0, 9, 18)):
    d.path(rot_rect_path(746, 618 + dy, 34, 20, 8 + j * 4),
           f"Spare tab {j+1}", fill=TAB_GRAD, stroke=INK, strokeWidth=2.5,
           join="round")

# --- motes ------------------------------------------------------------------------------
for i, (x, y, w) in enumerate([(252,428,5),(330,300,6),(664,140,5),(820,480,6),
                               (240,700,5),(830,620,5),(480,240,5),(760,330,4)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#C4B894", opacity=32, stroke=NONE)

# --- captions ---------------------------------------------------------------------
d.text("SCOPEKEEPER EMERITUS", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#EFE6D0", justify="center")
r = d.text("SCOPE BOUNDARY CUSTODIAN", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B8A88C", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("306.scopekeeper-emeritus-V1R00")
