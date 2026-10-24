#!/usr/bin/env python3
"""Annexa Sorrowmark — mascot portrait V1R00.
A solemn clerk stamping a distress record into a thick appendix while a
pristine executive summary gleams on the other side of the desk. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Annexa Sorrowmark — Mascot Portrait", 1000, 1000)

INK = "#2A2030"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A1626"}, {"offset": 1, "color": "#0B0913"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E5F7E"}, {"offset": 0.7, "color": "#493E5A"},
    {"offset": 1, "color": "#262033"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A3248"}, {"offset": 1, "color": "#1D192B"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#A891B4"}, {"offset": 0.72, "color": "#7A688C"},
    {"offset": 1, "color": "#51455F"}]}}
HAIR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A3C56"}, {"offset": 1, "color": "#2E2438"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#574A62"}, {"offset": 1, "color": "#312940"}]}}
PAGE = "#EBDFC6"
TOME_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E3A5C"}, {"offset": 1, "color": "#2E2138"}]}}
STAMP_RED = "#A84A5E"
SLIDE = "#F2EAD9"

# --- backdrop + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7E6E96", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8CCE8", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(186,232,8),(806,228,7),(154,516,9),(838,540,8),
                               (246,764,7),(754,748,9),(130,388,6),(866,390,7),
                               (390,110,7),(616,108,8),(330,822,6),(668,820,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5C4E74", opacity=45, stroke=NONE)

# --- floor: bottom segment closed on the disc's own arc ------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#120E1C",
       strokeWidth=4, opacity=70)

# --- the desk -------------------------------------------------------------------
d.shape("rectangle", "Desk top", x=170, y=640, width=660, height=26,
        fill="#6A5A76", stroke=INK, strokeWidth=4, radius=8)
d.shape("rectangle", "Desk front", x=190, y=666, width=620, height=110,
        fill=DESK_GRAD, stroke=INK, strokeWidth=5, radius=6)
d.path("M190,700 L810,700", "Desk groove", fill=NONE, stroke="#211B30",
       strokeWidth=3, opacity=60)

# --- executive summary slides: clean, smug, untouched ----------------------------
# fanned stack of three cards, bottom to top
d.path("M238,566 L356,548 L362,616 L244,634 Z", "Slide back",
       fill="#D8CCB4", stroke=INK, strokeWidth=4, join="round")
d.path("M232,558 L350,540 L356,608 L238,626 Z", "Slide mid",
       fill="#E6DCC6", stroke=INK, strokeWidth=4, join="round")
d.path("M226,550 L344,532 L350,600 L232,618 Z", "Slide top",
       fill=SLIDE, stroke=INK, strokeWidth=4, join="round")
# chart on the top card: title bar + a green line that only goes up
d.path("M240,568 L334,553", "Slide header", fill=NONE, stroke="#8A7A5E",
       strokeWidth=6, cap="round", opacity=70)
d.path("M246,604 L272,590 L296,596 L330,566", "Green trend", fill=NONE,
       stroke="#7EA87E", strokeWidth=5, cap="round", join="round")
d.shape("ellipse", "Trend dot", x=326, y=560, width=10, height=10,
        fill="#7EA87E", stroke=INK, strokeWidth=2)
# the smug clean sheen
d.shape("ellipse", "Slide sheen", x=240, y=540, width=90, height=26,
        fill="#FFFFFF", opacity=18, stroke=NONE)

# --- the appendix tome: thick, dark, patiently numbered ---------------------------
# cover lying on desk, page block above
d.shape("ellipse", "Tome shadow", x=560, y=656, width=260, height=22,
        fill="#100C1A", opacity=50, stroke=NONE)
d.shape("rectangle", "Tome cover", x=566, y=612, width=246, height=48,
        fill=TOME_GRAD, stroke=INK, strokeWidth=5, radius=6)
# page block: cream slab with ruled edges
d.shape("rectangle", "Page block", x=578, y=560, width=222, height=56,
        fill=PAGE, stroke=INK, strokeWidth=4, radius=3)
for i in range(4):
    d.path(f"M584,{570+i*11} L794,{570+i*11}", f"Page edge {i+1}",
           fill=NONE, stroke="#B4A488", strokeWidth=2, opacity=70)
# tabs protruding from the fore-edge — she numbers what she exiles
for i, ty in enumerate([560, 578, 596]):
    d.shape("rectangle", f"Tab {i+1}", x=800, y=ty, width=30, height=15,
            fill="#C9B294", stroke=INK, strokeWidth=3, radius=2)
# the tab that is her complete testimony
d.text("84", "Tab 84", x=804, y=608, size=12, font="Source Sans 3",
       color="#4A3A2C", justify="left")
# spine label
d.text("APPENDIX", "Tome label", x=640, y=642, size=15, font="Virelai Sans",
       color="#C4AEB4", justify="left")

# --- Annexa: solemn, mid-stamp ----------------------------------------------------
d.shape("ellipse", "Annexa shadow", x=390, y=620, width=230, height=26,
        fill="#100C1A", opacity=45, stroke=NONE)
# body
d.path("M502,430 C580,430 620,505 620,580 C620,636 585,660 502,660 "
       "C419,660 384,636 384,580 C384,505 424,430 502,430 Z",
       "Annexa body", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
d.shape("ellipse", "Body hi", x=432, y=466, width=110, height=50,
        fill="#FFFFFF", opacity=12, stroke=NONE)
# collar: a neat clerical V
d.path("M466,452 L502,486 L538,452", "Collar", fill=NONE, stroke="#3E3249",
       strokeWidth=8, cap="round", join="round")
d.shape("ellipse", "Brooch", x=494, y=478, width=16, height=16,
        fill="#C9B294", stroke=INK, strokeWidth=3)

# left arm: reaching across to feed the distress record into the annex —
# she reads everything she moves
d.path("M415,548 C445,565 470,578 494,590", "Arm L", fill=NONE,
       stroke="#7A688C", strokeWidth=18, cap="round")
# right arm: raised, holding the stamp over the tome
d.path("M594,540 C640,545 668,555 684,575", "Arm R", fill=NONE,
       stroke="#7A688C", strokeWidth=18, cap="round")
d.shape("ellipse", "Palm R", x=672, y=560, width=30, height=22,
        fill="#A891B4", stroke=INK, strokeWidth=4)
# the stamp: handle + base pressed to the page
d.shape("rectangle", "Stamp handle", x=680, y=540, width=18, height=30,
        fill="#6A5238", stroke=INK, strokeWidth=4, radius=5)
d.shape("ellipse", "Stamp knob", x=676, y=528, width=26, height=18,
        fill="#8A6A48", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Stamp base", x=664, y=570, width=52, height=20,
        fill=STAMP_RED, stroke=INK, strokeWidth=4, radius=4)
# the fresh mark it just left on the page block
d.shape("rectangle", "Stamp imprint", x=722, y=572, width=56, height=26,
        fill=NONE, stroke=STAMP_RED, strokeWidth=3, radius=3, opacity=85)
d.text("FILED", "Imprint text", x=730, y=591, size=14, font="Virelai Sans",
       color=STAMP_RED, justify="left")

# head: round, bun, half-lidded eyes that have read every page
d.path("M502,288 C558,288 592,330 592,378 C592,424 556,452 502,452 "
       "C448,452 412,424 412,378 C412,330 446,288 502,288 Z",
       "Head", fill=BODY_GRAD, stroke=INK, strokeWidth=6)
# hair cap + bun
d.path("M416,366 C416,318 452,284 502,284 C552,284 588,318 588,366 "
       "C566,338 540,326 502,326 C464,326 438,338 416,366 Z",
       "Hair cap", fill=HAIR_GRAD, stroke=INK, strokeWidth=5, join="round")
d.shape("ellipse", "Bun", x=478, y=252, width=48, height=40,
        fill=HAIR_GRAD, stroke=INK, strokeWidth=5)
d.path("M484,270 C494,262 510,262 520,270", "Bun shine", fill=NONE,
       stroke="#6A5878", strokeWidth=3, cap="round", opacity=80)
# eyes: heavy lids, level gaze
d.path("M448,384 C456,392 468,392 476,384", "Eye L", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M528,384 C536,392 548,392 556,384", "Eye R", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
d.path("M446,372 L478,372 M526,372 L558,372", "Lids", fill=NONE,
       stroke="#4E4260", strokeWidth=4, cap="round")
# small even mouth: neither comforted nor cruel
d.path("M484,422 C494,421 510,421 520,422", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# the smudge in the margin: faint cheek marks where the reading pools
d.shape("ellipse", "Cheek L", x=432, y=400, width=24, height=12,
        fill="#7A5E80", opacity=45, stroke=NONE)
d.shape("ellipse", "Cheek R", x=548, y=400, width=24, height=12,
        fill="#7A5E80", opacity=45, stroke=NONE)

# --- the distress record: half-fed into the annex, scream still legible ---------
# drawn last so it reads over her side; the rest is already inside the tome
d.path("M576,548 L488,578 L498,626 L582,594 Z", "Distress page",
       fill=PAGE, stroke=INK, strokeWidth=4, join="round")
d.path("M496,586 L556,568", "Distress header", fill=NONE, stroke="#8A7A68",
       strokeWidth=4, cap="round", opacity=70)
d.path("M498,606 L508,592 L517,612 L527,588 L536,614 L545,596 L552,606",
       "Scream waveform", fill=NONE, stroke="#C4546E", strokeWidth=4,
       cap="round", join="round")
# her palm comes down on the exposed corner — the relocation is never blind
d.shape("ellipse", "Palm L", x=486, y=574, width=32, height=22,
        fill="#A891B4", stroke=INK, strokeWidth=4)

# --- captions ---------------------------------------------------------------------
d.text("ANNEXA SORROWMARK", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#DCCFE8", justify="center")
r = d.text("CUSTODIAN OF THE SEVENTH CLICK", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#9E8EB8", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("235.annexa-sorrowmark-V1R00")
