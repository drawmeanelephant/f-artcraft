#!/usr/bin/env python3
"""Sidebar Mercy — mascot portrait V1R00.
A sidebar-panel mascot behind a desk, glancing toward a barely-ajar door.
One finger rises toward her mouth; the other hand slides an approval card
(A-OK) and a folded alternate form (FORM B) into reach along the desktop.
The official answer, DENIED, lies face-up on the other side. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Sidebar Mercy — Mascot Portrait", 1000, 1000)

INK = "#1E1A14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#141A14"}, {"offset": 1, "color": "#080A08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#828A70"}, {"offset": 0.7, "color": "#59604C"},
    {"offset": 1, "color": "#2E3226"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#463E2E"}, {"offset": 1, "color": "#1E1810"}]}}
DOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A2E26"}, {"offset": 1, "color": "#181C16"}]}}
PANEL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A6672"}, {"offset": 1, "color": "#5E3A46"}]}}
HEADBAND_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E4E5C"}, {"offset": 1, "color": "#4E2E3A"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7E5C3A"}, {"offset": 1, "color": "#4A3220"}]}}
DESKF_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E3622"}, {"offset": 1, "color": "#2A1C10"}]}}
CARD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4DC9A"}, {"offset": 0.75, "color": "#D9B25E"},
    {"offset": 1, "color": "#A87E36"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EDE4D0"}, {"offset": 1, "color": "#C9BCA0"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A8A074", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4E0C2", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#4E5238", opacity=45, stroke=NONE)

# --- floor --------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#100C08",
       strokeWidth=4, opacity=70)

# --- the door, barely ajar, upper left -------------------------------------------
d.shape("ellipse", "Door light pool", x=170, y=680, width=160, height=22,
        fill="#E8CE96", opacity=14, stroke=NONE)
d.path("M230,250 L262,250 L262,676 L230,676 Z", "Door gap light",
       fill="#E8D096", stroke=NONE, opacity=70)
d.path("M230,250 L186,272 L186,650 L230,676 Z", "Door slab",
       fill=DOOR_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Door knob", x=196, y=452, width=9, height=9,
        fill="#B8A06A", stroke=INK, strokeWidth=2.5)

# --- warm halo behind the mascot --------------------------------------------------
d.shape("ellipse", "Mercy halo", x=340, y=300, width=380, height=380,
        fill="#F0D8A0", opacity=10, stroke=NONE)
d.shape("ellipse", "Mascot shadow", x=390, y=682, width=280, height=22,
        fill="#0C0806", opacity=45, stroke=NONE)

# --- sidebar panel body ------------------------------------------------------------
d.shape("rectangle", "Panel body", x=408, y=392, width=184, height=300,
        fill=PANEL_GRAD, stroke=INK, strokeWidth=6, radius=26)
# header band
d.path("M408,418 C408,404 420,392 434,392 L566,392 C580,392 592,404 592,418 "
       "L592,452 L408,452 Z", "Header band", fill=HEADBAND_GRAD,
       stroke=INK, strokeWidth=5)
# header dots, like a window chrome
for i, x in enumerate([420, 436, 452]):
    d.shape("ellipse", f"Chrome dot {i+1}", x=x, y=402, width=8, height=8,
            fill="#E8CE96" if i == 0 else "#8A5E6C", stroke=INK,
            strokeWidth=2, opacity=90 if i else 70)
# list rows down the panel — the middle row is the merciful one, lit
for i, (y, lit) in enumerate([(478, False), (512, True), (546, False),
                              (580, False), (614, False)]):
    w = 128 if i % 2 == 0 else 104
    d.shape("rectangle", f"Row {i+1}", x=432, y=y, width=w, height=16,
            fill="#F0D8A0" if lit else "#7E5060",
            stroke=NONE, radius=8, opacity=85 if lit else 60)
d.shape("ellipse", "Row glow", x=424, y=504, width=152, height=32,
        fill="#F0D8A0", opacity=18, stroke=NONE)
# a paperclip hairpin at the panel's top corner
d.path("M586,378 C586,368 598,366 600,376 C602,386 592,390 588,382 "
       "C584,372 594,364 602,370", "Paperclip", fill=NONE, stroke="#D9B25E",
       strokeWidth=4, cap="round")

# --- face: the sideways glance ------------------------------------------------------
# eyes: pupils carried hard left, toward the door
d.shape("ellipse", "Eye L", x=470, y=414, width=20, height=22,
        fill="#F4E8D4", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Eye R", x=514, y=414, width=20, height=22,
        fill="#F4E8D4", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Pupil L", x=471, y=421, width=9, height=10,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Pupil R", x=515, y=421, width=9, height=10,
        fill=INK, stroke=NONE)
d.path("M466,400 C474,394 484,394 492,398 M512,398 C520,394 530,394 538,400",
       "Brows", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# a small closed, careful mouth
d.path("M489,438 C496,442 505,442 512,438", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")

# --- left arm: the hush --------------------------------------------------------------
d.path("M408,540 C388,522 384,494 398,474", "Hush arm", fill=NONE,
       stroke="#6E4250", strokeWidth=16, cap="round")
d.path("M398,474 C404,462 414,456 426,456", "Hush hand", fill=NONE,
       stroke="#8A5A68", strokeWidth=13, cap="round")
d.path("M424,452 L424,436", "Hush finger", fill=NONE, stroke="#8A5A68",
       strokeWidth=8, cap="round")

# --- desk ----------------------------------------------------------------------------
d.shape("rectangle", "Desk top", x=238, y=606, width=548, height=26,
        fill=DESK_GRAD, stroke=INK, strokeWidth=5, radius=8)
d.path("M238,632 L786,632 L774,700 L250,700 Z", "Desk front",
       fill=DESKF_GRAD, stroke=INK, strokeWidth=5)
d.shape("ellipse", "Desk sheen", x=300, y=610, width=180, height=10,
        fill="#FFFFFF", opacity=12, stroke=NONE)

# the official answer: DENIED, face-up where everyone can see it
d.path(rot_rect_path(310, 578, 96, 66, -6), "Denied form",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=3.5)
d.path(rot_rect_path(310, 560, 60, 5, -6), "Denied headrule",
       fill=NONE, stroke="#8A7A60", strokeWidth=3, opacity=80)
d.text("DENIED", "Denied stamp", x=310, y=586, size=16,
       font="Virelai Sans", color="#9A3A30", justify="center")
d.path(rot_rect_path(310, 600, 52, 4, -6), "Denied rule 2",
       fill=NONE, stroke="#8A7A60", strokeWidth=3, opacity=70)

# --- right arm: the slide -------------------------------------------------------------
# light pool where the mercy lands
d.shape("ellipse", "Mercy pool", x=600, y=592, width=170, height=30,
        fill="#F0D8A0", opacity=16, stroke=NONE)
d.path("M592,548 C634,556 668,574 692,592", "Slide arm", fill=NONE,
       stroke="#6E4250", strokeWidth=16, cap="round")
d.shape("ellipse", "Slide hand", x=684, y=584, width=26, height=20,
        fill="#8A5A68", stroke=INK, strokeWidth=3.5)

# motion arcs trailing the card
d.path("M600,570 C618,568 634,570 648,576 M596,592 C614,590 630,592 644,598",
       "Slide streaks", fill=NONE, stroke="#E8CE96", strokeWidth=3.5,
       cap="round", opacity=55)

# the approval card, glowing faintly, riding ahead of her hand
d.path(rot_rect_path(736, 586, 74, 46, -8), "Approval card",
       fill=CARD_GRAD, stroke=INK, strokeWidth=4)
d.text("A-OK", "Card text", x=736, y=592, size=17, font="Virelai Sans",
       color="#4A3410", justify="center")
# the alternate form, folded, tucked just under it
d.path(rot_rect_path(722, 614, 88, 30, 6), "Alt form",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=3.5)
d.path(rot_rect_path(736, 614, 26, 30, 6), "Alt form fold",
       fill="#D8CBAE", stroke=INK, strokeWidth=2.5)
d.text("FORM B", "Alt label", x=712, y=620, size=11, font="Virelai Sans",
       color="#6E5E44", justify="center")

# --- dust in the thin door light --------------------------------------------------------
for i, (x, y, w) in enumerate([(246,330,4),(238,430,4),(252,520,4),(222,580,4),
                               (640,330,5),(700,300,4),(350,300,5),(760,420,4)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#E8D8AE", opacity=45, stroke=NONE)

# --- captions ----------------------------------------------------------------------------
d.text("SIDEBAR MERCY", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#EAE8D2", justify="center")
r = d.text("HELP ARRIVES OFF-TICKET", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#B4B494", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("260.sidebar-mercy-V1R00")
