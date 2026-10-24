#!/usr/bin/env python3
"""Local Option Ghost — mascot portrait V1R00.
A translucent ghost at a branch-office desk performs the undocumented
third press on the printer; a small shrine of stapler and candle is kept
on the old server line. 1000x1000. Gradients + translucent shading,
never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Local Option Ghost — Mascot Portrait", 1000, 1000)

INK = "#22201A"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#101812"}, {"offset": 1, "color": "#060A08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E7E72"}, {"offset": 0.7, "color": "#4A5A4E"},
    {"offset": 1, "color": "#2A352C"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E4630"}, {"offset": 1, "color": "#2A1E14"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5E40"}, {"offset": 1, "color": "#4A3624"}]}}
PRINTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#C8CCC4"}, {"offset": 1, "color": "#8A9088"}]}}
GHOST_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#DCE8E2"}, {"offset": 0.7, "color": "#9AB4AC"},
    {"offset": 1, "color": "#6A8A80"}]}}
FLAME_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F8E0A0"}, {"offset": 1, "color": "#D88A38"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8FA394", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCE8DC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#42503F", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#160E08",
       strokeWidth=4, opacity=70)

# --- the old server line: a cable run along the wall to the shrine ----------------
d.path("M150,285 C320,272 520,278 700,268 L700,258", "Server line",
       fill=NONE, stroke="#3E4A42", strokeWidth=5, opacity=80)
for i, x in enumerate([220, 340, 460, 580]):
    d.path(f"M{x},{276 if x%2 else 277} L{x},268", f"Line clip {i+1}",
           fill=NONE, stroke="#5A685C", strokeWidth=4, opacity=70)

# --- the shrine: shelf, surrendered stapler, lit candle ----------------------------
d.shape("ellipse", "Shrine glow", x=690, y=195, width=150, height=105,
        fill="#F0C878", opacity=12, stroke=NONE)
d.shape("rectangle", "Shrine shelf", x=690, y=252, width=160, height=14,
        fill=DESK_GRAD, stroke=INK, strokeWidth=4, radius=3)
d.path("M712,266 L706,284 M830,266 L836,284", "Shelf brackets", fill=NONE,
       stroke=INK, strokeWidth=4, opacity=80)
# the surrendered stapler
d.path("M712,252 L712,240 C712,232 720,228 730,228 L752,228 "
       "C760,228 764,234 764,240 L764,252 Z", "Stapler body",
       fill="#8A4A3E", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Stapler hinge", x=746, y=236, width=8, height=8,
        fill="#C89A62", stroke=INK, strokeWidth=2.5)
# the candle
d.shape("rectangle", "Candle", x=798, y=214, width=18, height=38,
        fill="#E8DCC4", stroke=INK, strokeWidth=3.5, radius=3)
d.path("M807,214 L807,206", "Wick", fill=NONE, stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Flame", x=800, y=188, width=14, height=20,
        fill=FLAME_GRAD, stroke=NONE)
d.shape("ellipse", "Flame glow", x=788, y=178, width=38, height=42,
        fill="#F0C878", opacity=25, stroke=NONE)

# --- the desk -------------------------------------------------------------------
d.shape("ellipse", "Desk shadow", x=290, y=688, width=460, height=22,
        fill="#0E0806", opacity=45, stroke=NONE)
d.shape("rectangle", "Desk top", x=300, y=545, width=420, height=26,
        fill=DESK_GRAD, stroke=INK, strokeWidth=5, radius=4)
d.shape("rectangle", "Desk leg L", x=316, y=571, width=24, height=129,
        fill=DESK_GRAD, stroke=INK, strokeWidth=4)
# drawer pedestal on the right
d.shape("rectangle", "Pedestal", x=610, y=571, width=110, height=129,
        fill=DESK_GRAD, stroke=INK, strokeWidth=4)
for i, y in enumerate([582, 624]):
    d.shape("rectangle", f"Drawer {i+1}", x=620, y=y, width=90, height=32,
            fill=NONE, stroke="#3A2A1A", strokeWidth=3.5, radius=3,
            opacity=85)
    d.shape("ellipse", f"Drawer pull {i+1}", x=658, y=y+12, width=14,
            height=8, fill="#C89A62", stroke=INK, strokeWidth=2.5)
# paperwork waiting on the left end of the desk
d.path(rot_rect_path(368, 532, 90, 26, -3), "Form stack",
       fill="#E4DCC8", stroke=INK, strokeWidth=3.5)
d.path(rot_rect_path(372, 522, 84, 22, 2), "Form top",
       fill="#EFE8D8", stroke=INK, strokeWidth=3)
# pencil cup
d.shape("rectangle", "Pencil cup", x=442, y=512, width=34, height=34,
        fill="#5A685C", stroke=INK, strokeWidth=4, radius=4)
d.path("M452,512 L448,492 M464,512 L470,490", "Pencils", fill=NONE,
       stroke="#C89A62", strokeWidth=4, cap="round")

# --- the printer, mid-job ----------------------------------------------------------
d.shape("rectangle", "Printer body", x=540, y=468, width=160, height=78,
        fill=PRINTER_GRAD, stroke=INK, strokeWidth=5, radius=8)
d.path("M552,486 L688,486", "Lid seam", fill=NONE, stroke="#4A5048",
       strokeWidth=3.5, opacity=80)
d.shape("rectangle", "Output slot", x=566, y=518, width=108, height=12,
        fill="#262A24", stroke=INK, strokeWidth=3, radius=5)
# the page coming out, bent downward
d.path("M580,524 L660,524 L664,574 C640,580 600,580 576,574 Z",
       "Emerging page", fill="#EFE8D8", stroke=INK, strokeWidth=3.5)
d.path("M584,540 L652,540 M586,552 L650,552", "Page lines", fill=NONE,
       stroke="#9A8E76", strokeWidth=3, opacity=70)
# the button — about to receive the third press
d.shape("ellipse", "Button", x=660, y=474, width=16, height=16,
        fill="#84E2A4", stroke=INK, strokeWidth=3)
# status lamp
d.shape("ellipse", "Status lamp", x=560, y=476, width=9, height=9,
        fill="#F2C86A", stroke=NONE)

# --- the Ghost ---------------------------------------------------------------------
d.shape("ellipse", "Ghost pool", x=330, y=680, width=190, height=26,
        fill="#9AB4AC", opacity=18, stroke=NONE)
d.shape("ellipse", "Ghost halo", x=300, y=270, width=240, height=300,
        fill="#C8DCD4", opacity=10, stroke=NONE)
# sheet-ghost body, wavy hem hovering over the floor
d.path("M440,300 C490,300 508,352 506,420 L503,528 C502,544 492,552 482,542 "
       "C474,534 469,544 458,552 C449,558 441,552 439,544 C434,554 422,558 "
       "414,550 C406,542 401,550 395,542 C388,534 384,530 383,518 L380,420 "
       "C378,352 390,300 440,300 Z", "Ghost body", fill=GHOST_GRAD,
       stroke=INK, strokeWidth=6, opacity=82)
d.shape("ellipse", "Ghost highlight", x=400, y=320, width=60, height=110,
        fill="#FFFFFF", opacity=18, stroke=NONE)
# hollow eyes + the small 'o' mouth, facing the printer
d.shape("ellipse", "Eye L", x=420, y=372, width=19, height=28,
        fill="#22201A", stroke=NONE)
d.shape("ellipse", "Eye R", x=462, y=372, width=19, height=28,
        fill="#22201A", stroke=NONE)
d.shape("ellipse", "Mouth", x=448, y=416, width=16, height=20,
        fill="#22201A", opacity=80, stroke=NONE)
# the arm performing the third press on the button
d.path("M495,430 C540,440 600,458 656,476", "Pressing arm", fill=NONE,
       stroke="#9AB4AC", strokeWidth=22, cap="round", opacity=85)
d.shape("ellipse", "Pressing finger", x=652, y=470, width=20, height=16,
        fill="#C8DCD4", stroke=INK, strokeWidth=3.5, opacity=90)
# three press marks: the ritual count
d.path("M690,462 C696,470 696,478 690,486 M702,452 C712,466 712,482 702,496",
       "Press marks", fill=NONE, stroke="#DCE8DC", strokeWidth=4,
       cap="round", opacity=70)
# trailing arm, dangling
d.path("M385,440 C368,465 362,490 366,512", "Trailing arm", fill=NONE,
       stroke="#9AB4AC", strokeWidth=18, cap="round", opacity=75)
# ectoplasm drift
for i, (x, y, w) in enumerate([(320,350,6),(295,420,5),(330,480,5),(540,330,5),
                               (250,300,6),(200,400,5)]):
    d.shape("ellipse", f"Drift {i+1}", x=x, y=y, width=w, height=w,
            fill="#C8DCD4", opacity=35, stroke=NONE)

# --- captions ---------------------------------------------------------------------
d.text("LOCAL OPTION GHOST", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#E4ECE2", justify="center")
r = d.text("CERTIFIER OF UNSHARED PRACTICES", "Role", x=500, y=968,
           size=23, font="Virelai Sans", color="#AEC0AE", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("253.local-option-ghost-V1R00")
