#!/usr/bin/env python3
"""Warm Hold Music — mascot portrait V1R00.
A lounge mascot in a fedora playing a looping saxophone line to a desk
phone whose receiver sits off the hook; the melody literally loops —
a ring of notes orbiting the room and coming back around. The hold
light stays lit. 1000x1000. Gradients + translucent shading, no flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Warm Hold Music — Mascot Portrait", 1000, 1000)

INK = "#241C14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E0C14"}, {"offset": 1, "color": "#070609"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#564A6E"}, {"offset": 0.7, "color": "#3A324E"},
    {"offset": 1, "color": "#221C30"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E3450"}, {"offset": 1, "color": "#1E1828"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D0B294"}, {"offset": 0.7, "color": "#A8875F"},
    {"offset": 1, "color": "#7E6244"}]}}
SAX_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8BC62"}, {"offset": 0.7, "color": "#B8862E"},
    {"offset": 1, "color": "#7A5418"}]}}
PHONE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A4458"}, {"offset": 1, "color": "#322C3E"}]}}
HAT_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E5244"}, {"offset": 1, "color": "#3E362C"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A88A66", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EAD8BC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E423A", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#100C16",
       strokeWidth=4, opacity=70)

# --- stage halo + the melody's literal loop ----------------------------------------
d.shape("ellipse", "Stage halo", x=290, y=300, width=480, height=370,
        fill="#E8A86A", opacity=10, stroke=NONE)
# the loop: a staff-like orbit that always comes back around
d.path("M560,560 C700,560 800,505 800,415 C800,335 715,290 615,290 "
       "C520,290 435,335 435,415 C435,485 505,530 590,535",
       "Melody loop", fill=NONE, stroke="#D8A24E", strokeWidth=3,
       opacity=45)
# notes riding the loop
for i, (cx, cy, o) in enumerate([(792, 372, 80), (700, 292, 75),
                                 (468, 322, 70), (438, 472, 60)]):
    d.path(rot_rect_path(cx, cy, 17, 12, -15), f"Loop note head {i+1}",
           fill="#E8BC6A", opacity=o, stroke=NONE)
    d.path(f"M{cx+8},{cy-4} L{cx+8},{cy-34} C{cx+16},{cy-30} "
           f"{cx+21},{cy-24} {cx+21},{cy-16}", f"Loop note stem {i+1}",
           fill=NONE, stroke="#E8BC6A", strokeWidth=3, cap="round",
           opacity=o)

# --- the stool ----------------------------------------------------------------------
d.shape("ellipse", "Stool seat", x=352, y=636, width=140, height=24,
        fill="#4E4258", stroke=INK, strokeWidth=4)
for i, (x1, x2) in enumerate([(376, 366), (462, 474)]):
    d.path(f"M{x1},652 L{x2},690", f"Stool leg {i+1}", fill=NONE,
           stroke="#3A3044", strokeWidth=7, cap="round")

# --- the mascot, seated, mid-phrase ---------------------------------------------------
d.shape("ellipse", "Mascot shadow", x=330, y=682, width=230, height=20,
        fill="#0C0810", opacity=45, stroke=NONE)
d.shape("ellipse", "Body", x=330, y=500, width=170, height=178,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# feet dangling off the stool
for x in (352, 448):
    d.shape("ellipse", f"Foot {x}", x=x, y=670, width=54, height=24,
            fill="#7E6244", stroke=INK, strokeWidth=4)
# head
d.shape("ellipse", "Head", x=348, y=368, width=134, height=130,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# ears tucked under the hat
for ex in (356, 472):
    d.shape("ellipse", f"Ear {ex}", x=ex-10, y=382, width=24, height=22,
            fill="#A8875F", stroke=INK, strokeWidth=3.5)
# fedora
d.shape("ellipse", "Hat brim", x=344, y=380, width=148, height=26,
        fill=HAT_GRAD, stroke=INK, strokeWidth=4)
d.path("M368,388 C368,350 392,334 418,334 C444,334 468,350 468,388 Z",
       "Hat crown", fill=HAT_GRAD, stroke=INK, strokeWidth=4)
d.path("M370,376 L466,376", "Hat band", fill=NONE, stroke="#2A241E",
       strokeWidth=7)
# face: eyes closed, deep in the loop
d.path("M372,432 C380,440 392,440 400,432", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
d.path("M424,432 C432,440 444,440 452,432", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# puffed cheek on the blowing side
d.shape("ellipse", "Puffed cheek", x=446, y=452, width=24, height=20,
        fill="#D0B294", opacity=70, stroke=NONE)
d.shape("ellipse", "Embouchure", x=470, y=462, width=10, height=8,
        fill=INK, stroke=NONE)

# --- the saxophone ----------------------------------------------------------------------
# mouthpiece into the mouth
d.path("M478,466 L492,478", "Mouthpiece", fill=NONE, stroke="#3A2E1C",
       strokeWidth=7, cap="round")
# neck curving down into the body
d.path("M492,478 C512,494 524,514 528,538", "Sax neck", fill=NONE,
       stroke="#C89A3E", strokeWidth=13, cap="round")
# body tube: the long J down to the bell
d.path("M528,538 C530,570 528,598 540,618 C552,638 578,642 596,628 "
       "C610,617 614,598 608,580", "Sax body", fill=NONE,
       stroke=SAX_GRAD, strokeWidth=30, cap="round")
# bell: the flare where the loop pours out
d.shape("ellipse", "Bell", x=586, y=540, width=56, height=66,
        fill=SAX_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Bell throat", x=596, y=552, width=36, height=42,
        fill="#5E3E12", stroke=NONE)
d.shape("ellipse", "Bell rim light", x=592, y=544, width=20, height=14,
        fill="#F4DC9A", opacity=70, stroke=NONE)
# keywork down the tube
for i, (kx, ky) in enumerate([(522,560),(524,582),(528,604),(538,622)]):
    d.shape("ellipse", f"Key {i+1}", x=kx, y=ky, width=7, height=7,
            fill="#F4DC9A", stroke=INK, strokeWidth=1.5)
# paws on the horn
d.shape("ellipse", "Paw upper", x=508, y=532, width=24, height=20,
        fill="#A8875F", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Paw lower", x=516, y=596, width=24, height=20,
        fill="#A8875F", stroke=INK, strokeWidth=3.5)
# strap from neck to horn
d.path("M452,498 C480,512 506,524 524,536", "Sax strap", fill=NONE,
       stroke="#3A2E20", strokeWidth=4, opacity=80)

# --- a fresh note leaving the bell ------------------------------------------------------
d.path(rot_rect_path(668, 556, 18, 13, -15), "Fresh note head",
       fill="#E8BC6A", opacity=85, stroke=NONE)
d.path("M677,551 L677,517 C685,521 690,528 690,536", "Fresh note stem",
       fill=NONE, stroke="#E8BC6A", strokeWidth=3.5, cap="round",
       opacity=85)

# --- the phone on its little table: still on hold -----------------------------------------
d.shape("ellipse", "Table shadow", x=650, y=684, width=150, height=16,
        fill="#0C0810", opacity=40, stroke=NONE)
d.shape("ellipse", "Table foot", x=690, y=688, width=60, height=12,
        fill="#3A3044", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Table leg", x=708, y=570, width=12, height=120,
        fill="#3A3044", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Table top", x=652, y=556, width=124, height=18,
        fill="#4E4258", stroke=INK, strokeWidth=4)
# phone base with rotary dial
d.path("M664,556 L664,522 C664,512 672,506 684,506 L744,506 "
       "C756,506 764,512 764,522 L764,556 Z", "Phone base",
       fill=PHONE_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Dial", x=700, y=518, width=28, height=28,
        fill="#241F2E", stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Dial hub", x=710, y=528, width=8, height=8,
        fill="#6E6480", stroke=NONE)
# the receiver, off the hook, dangling over the table's edge by its cord
d.path("M762,548 C776,556 784,564 785,576 C786,584 782,590 776,592",
       "Cord", fill=NONE, stroke="#241F2E", strokeWidth=3, cap="round")
d.path(rot_rect_path(784, 614, 58, 18, 78), "Receiver",
       fill="#3E3850", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Receiver earpiece", x=780, y=634, width=18, height=15,
        fill="#3E3850", stroke=INK, strokeWidth=3)
# the hold light: still lit, still holding
d.shape("ellipse", "Hold glow", x=742, y=514, width=22, height=22,
        fill="#E85A4A", opacity=25, stroke=NONE)
d.shape("ellipse", "Hold light", x=748, y=520, width=9, height=9,
        fill="#E85A4A", stroke=NONE)
d.text("ON HOLD", "Hold label", x=714, y=551, size=10,
       font="Virelai Sans", color="#B8ACCC", justify="center")

# --- stray lounge motes ---------------------------------------------------------------
for i, (x, y, w) in enumerate([(280,400,6),(250,560,5),(620,240,5),(860,480,6),
                               (230,650,6),(820,300,5),(560,220,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8BC6A", opacity=40, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("WARM HOLD MUSIC", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F0E2CE", justify="center")
r = d.text("PROGRESS, SIMULATED IN JAZZ", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8A884", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("266.warm-hold-music-V1R00")
