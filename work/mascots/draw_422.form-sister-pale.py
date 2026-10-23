#!/usr/bin/env python3
"""Form Sister Pale — mascot portrait V1R00. HTTP 422, "Unprocessable Content".
Pale sister reviewing an immaculate form, stack of onboarding forms beside her.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Form Sister Pale — Mascot Portrait", 1000, 1000)

INK = "#33262E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#241E2E"}, {"offset": 1, "color": "#0F0B16"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E6EBE2"}, {"offset": 0.7, "color": "#B9C7B9"},
    {"offset": 1, "color": "#7E9184"}]}}
HABIT_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A5264"}, {"offset": 0.7, "color": "#333A49"},
    {"offset": 1, "color": "#232834"}]}}
WIMPLE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FBF7EA"}, {"offset": 1, "color": "#DCD2B8"}]}}
FACE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F7E8D8"}, {"offset": 1, "color": "#DEC0AC"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#FDFBF2"}, {"offset": 1, "color": "#E8E2CE"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#5F7364", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#EFF4EC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(205,215,7),(785,205,6),(235,710,7),(750,700,7),(165,445,6),
                               (840,460,6),(345,145,6),(645,140,7),(290,795,6),(705,800,6)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5F7364", opacity=40, stroke=NONE)

# --- stack of onboarding forms, beside her (right) ------------------------------
d.shape("ellipse", "Stack shadow", x=614, y=748, width=230, height=26,
        fill="#31463B", opacity=35, stroke=NONE)
sheets = [(-8, "M628,700 L806,688 L814,742 L636,754 Z"),
          (-4, "M622,712 L800,700 L808,754 L630,766 Z"),
          (0,  "M630,724 L808,712 L816,766 L638,778 Z")]
for i, (dy, pp) in enumerate(sheets):
    d.path(pp, f"Stack sheet {i+1}", fill=PAPER_GRAD, stroke=INK,
           strokeWidth=4, join="round")
# ruled lines + a red REJECTED-free checklist on the top sheet — all immaculate
d.path("M652,736 L764,728 M654,746 L766,738", "Top sheet rules",
       fill=NONE, stroke="#9A9482", strokeWidth=3, opacity=80)
d.path("M652,756 L664,754 L668,760 L660,762 Z", "Top sheet tickbox",
       fill=NONE, stroke=INK, strokeWidth=2.5)
d.path("M656,756 L660,759 L665,753", "Top sheet tick",
       fill=NONE, stroke="#4A7A52", strokeWidth=2.5, cap="round")
# page corner lift
d.path("M788,714 L808,712 L796,724 Z", "Corner lift", fill="#DCD2B8", stroke=INK, strokeWidth=2)

# --- the sister -------------------------------------------------------------------
# ground shadow
d.shape("ellipse", "Figure shadow", x=290, y=756, width=290, height=30,
        fill="#31463B", opacity=40, stroke=NONE)
# habit body: bell of dark cloth
d.path("M335,742 C332,640 340,540 372,472 C396,424 440,404 468,414 "
       "C520,430 556,500 562,580 C566,650 564,700 560,742 Z",
       "Habit", fill=HABIT_GRAD, stroke=INK, strokeWidth=7, join="round")
# habit shading fold
d.path("M370,720 C368,620 380,530 408,470", "Habit fold L",
       fill=NONE, stroke="#1E222C", strokeWidth=8, opacity=45, cap="round")
d.path("M536,700 C540,620 530,540 505,480", "Habit fold R",
       fill=NONE, stroke="#1E222C", strokeWidth=7, opacity=40, cap="round")
# veil: dark drape over and behind the head
d.path("M352,430 C344,340 400,268 470,272 C540,276 580,344 574,430 "
       "C590,470 584,510 560,530 C540,480 400,480 384,532 C360,510 346,470 352,430 Z",
       "Veil", fill=HABIT_GRAD, stroke=INK, strokeWidth=6, join="round")
# wimple: white frame around the face
d.path("M470,306 C400,306 372,360 376,420 C380,476 420,512 470,512 "
       "C520,512 560,476 564,420 C568,360 540,306 470,306 Z",
       "Wimple", fill=WIMPLE_GRAD, stroke=INK, strokeWidth=5)
# face
d.shape("ellipse", "Face", x=404, y=340, width=132, height=136,
        fill=FACE_GRAD, stroke=INK, strokeWidth=5)
# wimple band across forehead
d.path("M404,382 C420,340 520,340 536,382 C530,350 500,330 470,330 C440,330 410,350 404,382 Z",
       "Wimple band", fill=WIMPLE_GRAD, stroke=INK, strokeWidth=4)
# spectacles — reviewing
d.shape("ellipse", "Lens L", x=420, y=398, width=36, height=34,
        fill="#FFFFFF", opacity=30, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Lens R", x=486, y=398, width=36, height=34,
        fill="#FFFFFF", opacity=30, stroke=INK, strokeWidth=3.5)
d.path("M456,412 L486,412", "Spec bridge", fill=NONE, stroke=INK, strokeWidth=3.5)
# eyes behind lenses, lowered toward the form
d.path("M430,414 C436,420 446,420 452,414", "Eye L",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
d.path("M496,414 C502,420 512,420 518,414", "Eye R",
       fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# prim mouth
d.path("M458,452 L486,452", "Mouth", fill=NONE, stroke=INK, strokeWidth=4, cap="round")
# faint pale blush
d.shape("ellipse", "Cheek L", x=416, y=436, width=24, height=10, fill="#D9A08C", opacity=35, stroke=NONE)
d.shape("ellipse", "Cheek R", x=502, y=436, width=24, height=10, fill="#D9A08C", opacity=35, stroke=NONE)

# --- the immaculate form on a clipboard, held before her ---------------------------
d.path("M398,552 L534,540 L546,668 L410,680 Z", "Clipboard",
       fill="#8A6238", stroke=INK, strokeWidth=5, join="round")
d.path("M410,562 L522,552 L532,656 L420,666 Z", "Form sheet",
       fill=PAPER_GRAD, stroke=INK, strokeWidth=3)
d.path("M450,548 L490,545 L492,558 L452,561 Z", "Clip", fill="#C9C2A8",
       stroke=INK, strokeWidth=3, join="round")
# immaculate rows: tickboxes all ticked, tidy rules
for j, yy in enumerate([580, 604, 628]):
    d.path(f"M424,{yy} L434,{yy-1} L435,{yy+9} L425,{yy+10} Z", f"Form box {j+1}",
           fill=NONE, stroke=INK, strokeWidth=2.2)
    d.path(f"M427,{yy+3} L430,{yy+6} L434,{yy} ", f"Form tick {j+1}",
           fill=NONE, stroke="#4A7A52", strokeWidth=2.5, cap="round")
    d.path(f"M444,{yy+3} L516,{yy-1}", f"Form rule {j+1}",
           fill=NONE, stroke="#9A9482", strokeWidth=3, opacity=80)
d.path("M424,648 L516,642", "Form rule last", fill=NONE, stroke="#9A9482", strokeWidth=3, opacity=80)
# hands: small pale hands at the board's edges
d.shape("ellipse", "Hand L", x=386, y=596, width=34, height=40, fill=FACE_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Hand R", x=528, y=580, width=34, height=40, fill=FACE_GRAD, stroke=INK, strokeWidth=4)
# sleeves
d.path("M372,570 C384,556 400,556 408,570 L396,600 C384,592 374,584 372,570 Z",
       "Sleeve L", fill=HABIT_GRAD, stroke=INK, strokeWidth=4)
d.path("M548,556 C560,548 572,552 576,566 L556,592 C550,580 546,568 548,556 Z",
       "Sleeve R", fill=HABIT_GRAD, stroke=INK, strokeWidth=4)

# --- name + role -------------------------------------------------------------------
d.text("FORM SISTER PALE", "Name", x=500, y=930, size=58, font="Virelai Sans",
       color="#E8EEE4", justify="center")
d.text(" ".join("UNPROCESSABLE CONTENT"), "Role", x=500, y=968, size=23, font="Virelai Sans",
       color="#A4BCA8", justify="center")

d.finish("422.form-sister-pale-V1R00")
