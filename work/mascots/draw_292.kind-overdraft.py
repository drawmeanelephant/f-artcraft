#!/usr/bin/env python3
"""Kind Overdraft — mascot portrait V1R00.
The clerk slides a written promise under the brass teller grate.
The promise is real; the drawer behind the bars was audited empty
before the promise was drafted. Warmth issued in a currency the
institution does not print. 1000x1000.
Gradients + translucent shading, no flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Kind Overdraft — Mascot Portrait", 1000, 1000)

INK = "#241C1E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A1420"}, {"offset": 1, "color": "#0B0810"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#54484E"}, {"offset": 0.7, "color": "#3A3138"},
    {"offset": 1, "color": "#1E1922"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#443A40"}, {"offset": 1, "color": "#1C161E"}]}}
VAULT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#221C28"}, {"offset": 0.75, "color": "#14101A"},
    {"offset": 1, "color": "#0C0910"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#D8B494"}, {"offset": 0.7, "color": "#AC8560"},
    {"offset": 1, "color": "#7C5E42"}]}}
BRASS_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E2BC6C"}, {"offset": 0.55, "color": "#B08A44"},
    {"offset": 1, "color": "#74562A"}]}}
BAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D6AE62"}, {"offset": 0.5, "color": "#9A7436"},
    {"offset": 1, "color": "#624A24"}]}}
COUNTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E4652"}, {"offset": 1, "color": "#2A2430"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4EAD2"}, {"offset": 1, "color": "#D8C8A4"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#78626C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D8C8CE", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(198,238,8),(800,234,7),(162,530,9),(836,550,8),
                               (252,766,7),(750,752,9),(140,398,6),(862,394,7),
                               (396,116,7),(612,112,8),(338,824,6),(664,822,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#443C48", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#120E16",
       strokeWidth=4, opacity=70)

# --- the vault behind the grate: nothing in it -------------------------------------
# window opening, arched top
d.path("M282,560 L282,300 C282,236 352,196 450,196 C548,196 618,236 "
       "618,300 L618,560 Z", "Vault opening", fill=VAULT_GRAD,
       stroke=INK, strokeWidth=5)
# the faint ring of the vault door at the back — sealed on empty
d.shape("ellipse", "Vault door ring", x=352, y=290, width=196, height=196,
        fill=NONE, stroke="#3E3648", strokeWidth=6, opacity=55)
d.shape("ellipse", "Vault door hub", x=432, y=370, width=36, height=36,
        fill=NONE, stroke="#3E3648", strokeWidth=5, opacity=50)
# bare shelf lines, kept for the record
d.path("M300,500 L600,500", "Empty shelf", fill=NONE, stroke="#322C3C",
       strokeWidth=5, opacity=70)
# one cobweb in the vault's corner — the only deposit on file
d.path("M296,318 C316,322 334,334 342,354 M296,318 C306,338 310,356 "
       "308,374 M296,318 L296,300 M296,318 C320,312 342,314 358,326",
       "Cobweb", fill=NONE, stroke="#5A5464", strokeWidth=2.5,
       opacity=55, cap="round")
# motes in the dark
for i, (x, y, w) in enumerate([(380,330,5),(510,430,6),(560,300,4),(420,470,5)]):
    d.shape("ellipse", f"Vault mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#6A6276", opacity=40, stroke=NONE)

# --- the brass teller grate ---------------------------------------------------------
# vertical bars over the opening
for bx in range(314, 600, 36):
    d.path(f"M{bx},540 L{bx},252", f"Bar {bx}", fill=NONE,
           stroke=BAR_GRAD, strokeWidth=9, cap="round")
    d.path(f"M{bx-2},540 L{bx-2},252", f"Bar glint {bx}", fill=NONE,
           stroke="#EFD39A", strokeWidth=2.5, cap="round", opacity=55)
# top and mid rails
d.path("M288,258 L612,258", "Top rail", fill=NONE, stroke=BRASS_GRAD,
       strokeWidth=12, cap="round")
d.path("M288,400 L612,400", "Mid rail", fill=NONE, stroke=BRASS_GRAD,
       strokeWidth=10, cap="round")
# bottom rail raised off the counter — the only way anything gets through
d.path("M288,534 L612,534", "Bottom rail", fill=NONE, stroke=BRASS_GRAD,
       strokeWidth=11, cap="round")
# arched frame over the window
d.path("M276,560 L276,300 C276,228 350,186 450,186 C550,186 624,228 "
       "624,300 L624,560", "Window frame", fill=NONE, stroke=BRASS_GRAD,
       strokeWidth=10, join="round")
# frame studs
for sx in (300, 390, 510, 600):
    d.shape("ellipse", f"Frame stud {sx}", x=sx - 5, y=214, width=10,
            height=10, fill="#E8C87E", stroke=INK, strokeWidth=3)

# --- the counter ----------------------------------------------------------------------
d.path("M238,560 L762,560 L796,616 L204,616 Z", "Counter top",
       fill=COUNTER_GRAD, stroke=INK, strokeWidth=5, join="round")
d.path("M204,616 L796,616 L786,642 L214,642 Z", "Counter edge",
       fill="#322B38", stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Counter sheen", x=300, y=570, width=200, height=14,
        fill="#8A8098", opacity=20, stroke=NONE)

# --- the written promise, sliding under the grate -------------------------------------
# the slip: front half on the counter, far half already in the vault dark
d.path("M398,552 L508,548 L516,566 L406,572 Z", "Promise slip",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=3.5, join="round")
# crease where it folds under the bottom rail
d.path("M460,550 L466,569", "Slip crease", fill=NONE, stroke="#B8A880",
       strokeWidth=2.5, opacity=80)
# the part past the bars, dimmed by the vault
d.path("M466,550 L508,548 L516,566 L474,568 Z", "Slip in shadow",
       fill="#8A7E66", opacity=55, stroke=NONE)
# one careful line of script on the near half
d.path("M410,558 L444,556 M412,564 L450,562", "Promise script", fill=NONE,
       stroke="#6A5E48", strokeWidth=2.5, cap="round", opacity=85)
# the small heart seal — warmth, notarized
d.path("M496,552 C492,548 486,550 487,555 C488,559 494,562 498,565 "
       "C502,562 508,559 509,555 C510,550 504,548 500,552 C499,553 "
       "498,552 496,552 Z", "Heart seal", fill="#B4445C", stroke=INK,
       strokeWidth=2.5)

# --- the clerk, leaning over the counter ----------------------------------------------
d.shape("ellipse", "Body", x=600, y=492, width=190, height=160,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
for ex in (634, 756):
    d.shape("ellipse", f"Ear {ex}", x=ex - 11, y=352, width=25, height=23,
            fill="#AC8560", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Head", x=622, y=356, width=158, height=140,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# earnest eyes — it means every word it cannot pay
d.shape("ellipse", "Eye L", x=654, y=412, width=16, height=19,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=716, y=412, width=16, height=19,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Glint L", x=658, y=416, width=5, height=5,
        fill="#FFF6E4", opacity=85, stroke=NONE)
d.shape("ellipse", "Glint R", x=720, y=416, width=5, height=5,
        fill="#FFF6E4", opacity=85, stroke=NONE)
# gentle apologetic mouth
d.path("M678,458 C686,463 698,463 706,458", "Mouth", fill=NONE,
       stroke=INK, strokeWidth=3.5, cap="round")
# the reaching arm, sliding the promise under the bars
d.path("M624,540 C580,548 540,554 512,558", "Arm reaching", fill=NONE,
       stroke="#AC8560", strokeWidth=17, cap="round")
d.shape("ellipse", "Paw on slip", x=492, y=544, width=32, height=26,
        fill="#D8B494", stroke=INK, strokeWidth=4)
# the other paw holding the ledger of issued warmth
d.path("M760,540 C772,552 778,566 780,580", "Arm ledger", fill=NONE,
       stroke="#AC8560", strokeWidth=16, cap="round")
d.path("M736,566 L802,556 L812,596 L746,606 Z", "Ledger", fill="#5A4450",
       stroke=INK, strokeWidth=4, join="round")
d.path("M748,578 L790,572 M750,588 L792,582", "Ledger lines", fill=NONE,
       stroke="#3A2C36", strokeWidth=2.5, opacity=80)
d.shape("ellipse", "Paw ledger", x=770, y=570, width=30, height=26,
        fill="#D8B494", stroke=INK, strokeWidth=4)

# --- the till drawer under the counter, open and empty ----------------------------------
d.path("M320,650 L470,650 L462,690 L328,690 Z", "Till drawer",
       fill="#1E1826", stroke=INK, strokeWidth=4, join="round")
d.path("M332,662 L458,662", "Drawer lip", fill=NONE, stroke="#B08A44",
       strokeWidth=4, opacity=70, cap="round")

# --- motes on the warm side --------------------------------------------------------------
for i, (x, y, w) in enumerate([(252,428,5),(306,300,6),(664,250,5),(820,480,6),
                               (232,634,5),(830,620,5),(380,240,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#C4A8B4", opacity=35, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("KIND OVERDRAFT", "Name", x=500, y=930, size=58,
       font="Virelai Sans", color="#F0E4D2", justify="center")
r = d.text("TENDER IN A CURRENCY NOT PRINTED", "Role", x=500, y=968,
           size=23, font="Virelai Sans", color="#C4A2AC",
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("292.kind-overdraft-V1R00")
