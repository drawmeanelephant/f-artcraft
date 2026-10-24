#!/usr/bin/env python3
"""APH-032 Neppy Sysdream — motivational-poster aphorism plate V1R00.
A COMING SOON poster that never arrives: inside the gilt card, a login
dialog for NEPTUNE, an OS that was canceled — ghost desktop icons behind
it, a password field full of dots with a blinking caret, a dead LOG IN
button, and a spinner cursor that never finishes its circle. Cold
phosphor teal on slate night, one amber promise. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-032 Neppy Sysdream — Motivational Poster", 1000, 1000)

INK = "#0E1420"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#182430"}, {"offset": 1, "color": "#080C14"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3A4E62"}, {"offset": 0.7, "color": "#1F2B3A"},
    {"offset": 1, "color": "#0E1420"}]}}
POSTER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1D2733"}, {"offset": 1, "color": "#10151D"}]}}
DLG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E3C4C"}, {"offset": 1, "color": "#1B242F"}]}}
TITLE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3C4E60"}, {"offset": 1, "color": "#2A3745"}]}}
FIELD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#10171F"}, {"offset": 1, "color": "#182130"}]}}
CYAN = "#7FD8E8"
CYAN_DIM = "#4E8A98"
AMBER = "#E8A850"
FRAME = "#8FA8BC"
HEAD = "#ECF2F4"
PUNCH = "#CBD8DE"
CREAM = "#ECF2F4"
FAINT = "#7E8FA0"
GHOST = "#5E7286"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#3E5A70", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#9FD0DC", strokeWidth=3, opacity=30)
d.shape("ellipse", "Patina 1", x=200, y=170, width=200, height=110,
        fill="#2E4254", opacity=22, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=620, width=200, height=110,
        fill="#2E4254", opacity=18, stroke=NONE)
for i, (x, y, w) in enumerate([(215, 280, 7), (790, 255, 8), (165, 480, 6),
                               (838, 475, 7), (250, 655, 6), (755, 665, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#46607A", opacity=35, stroke=NONE)
# dead pixels on the plate — the desktop that never rendered
for i, (x, y) in enumerate([(255, 200), (715, 170), (825, 340), (180, 380),
                            (310, 540), (725, 555), (190, 610)]):
    d.shape("ellipse", f"Dead pixel {i+1}", x=x, y=y, width=3, height=3,
            fill=CYAN, opacity=45, stroke=NONE)

# --- the poster card -------------------------------------------------------------
PX, PY, PW, PH = 220, 150, 560, 440
d.shape("rectangle", "Poster shadow", x=PX + 8, y=PY + 10, width=PW,
        height=PH, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Poster", x=PX, y=PY, width=PW, height=PH,
        fill=POSTER_GRAD, stroke="#35465A", strokeWidth=4)
d.shape("rectangle", "Frame outer", x=PX + 16, y=PY + 16,
        width=PW - 32, height=PH - 32, fill=NONE, stroke=FRAME,
        strokeWidth=2, opacity=80)
d.shape("rectangle", "Frame inner", x=PX + 24, y=PY + 24,
        width=PW - 48, height=PH - 48, fill=NONE, stroke=AMBER,
        strokeWidth=1.5, opacity=60)

# headline
r = d.text("THE SYSTEM ISN'T RESTING", "Headline", x=500, y=PY + 62,
           size=29, font="Virelai Sans", color=HEAD, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "headline tracking", ids=[r["id"]], tracking=20)
d.path("M350,244 L472,244 M528,244 L650,244", "Headline rules", fill=NONE,
       stroke=AMBER, strokeWidth=2, opacity=80)
d.path(rot_rect_path(500, 244, 10, 10, 45), "Headline diamond",
       fill=AMBER, opacity=85, stroke=NONE)

# --- ghost desktop: icons for a machine that never shipped -----------------------
def ghost_icon(cx, cy, kind, label):
    if kind == "folder":
        d.path(f"M{cx - 16},{cy - 8} L{cx - 6},{cy - 8} L{cx - 3},{cy - 12} "
               f"L{cx + 16},{cy - 12} L{cx + 16},{cy + 10} L{cx - 16},{cy + 10} Z",
               f"{label} body", fill=NONE, stroke=GHOST, strokeWidth=2,
               opacity=22)
    elif kind == "doc":
        d.path(f"M{cx - 10},{cy - 14} L{cx + 4},{cy - 14} L{cx + 10},{cy - 8} "
               f"L{cx + 10},{cy + 14} L{cx - 10},{cy + 14} Z",
               f"{label} body", fill=NONE, stroke=GHOST, strokeWidth=2,
               opacity=22)
        d.path(f"M{cx + 4},{cy - 14} L{cx + 4},{cy - 8} L{cx + 10},{cy - 8}",
               f"{label} fold", fill=NONE, stroke=GHOST, strokeWidth=1.5,
               opacity=22)
        for j in range(3):
            d.path(f"M{cx - 6},{cy - 2 + j * 5} L{cx + 6},{cy - 2 + j * 5}",
                   f"{label} line {j+1}", fill=NONE, stroke=GHOST,
                   strokeWidth=1.5, opacity=20)
    else:  # trash
        d.path(f"M{cx - 9},{cy - 8} L{cx - 7},{cy + 12} L{cx + 7},{cy + 12} "
               f"L{cx + 9},{cy - 8} Z", f"{label} body", fill=NONE,
               stroke=GHOST, strokeWidth=2, opacity=22)
        d.path(f"M{cx - 12},{cy - 8} L{cx + 12},{cy - 8} "
               f"M{cx - 4},{cy - 12} L{cx + 4},{cy - 12}",
               f"{label} lid", fill=NONE, stroke=GHOST, strokeWidth=2,
               opacity=22)

ghost_icon(268, 300, "folder", "Ghost folder")
ghost_icon(268, 366, "doc", "Ghost doc")
ghost_icon(732, 300, "doc", "Ghost doc 2")
ghost_icon(732, 366, "trash", "Ghost trash")
# a second ghost window stacked behind the dialog
d.shape("rectangle", "Ghost window", x=372, y=290, width=300, height=196,
        radius=10, fill=NONE, stroke=GHOST, strokeWidth=2.5, opacity=18)

# --- the NEPTUNE login dialog ------------------------------------------------------
DX, DY, DW, DH = 350, 305, 300, 190
d.shape("ellipse", "Dialog shadow", x=DX - 8, y=DY + DH - 2, width=DW + 16,
        height=12, fill="#000000", opacity=35, stroke=NONE)
d.shape("rectangle", "Dialog", x=DX, y=DY, width=DW, height=DH, radius=10,
        fill=DLG_GRAD, stroke="#0C121A", strokeWidth=3)
# title bar
d.path(f"M{DX},{DY + 26} L{DX + DW},{DY + 26}", "Title rule", fill=NONE,
       stroke="#0C121A", strokeWidth=2, opacity=70)
d.path(f"M{DX + 10},{DY + 26} L{DX + 10},{DY + 10} Q{DX + 10},{DY} "
       f"{DX + 26},{DY} L{DX + DW - 26},{DY} Q{DX + DW - 10},{DY} "
       f"{DX + DW - 10},{DY + 10} L{DX + DW - 10},{DY + 26} Z",
       "Title bar", fill=TITLE_GRAD, stroke=NONE, opacity=90)
d.text("NEPTUNE", "OS name", x=DX + 22, y=DY + 18, size=11,
       font="Source Sans 3", color=HEAD, justify="left")
# canceled: the name is struck through
d.path(f"M{DX + 20},{DY + 14} L{DX + 84},{DY + 14}", "Name strike",
       fill=NONE, stroke="#E86A5A", strokeWidth=2, cap="round", opacity=75)
# the forever promise, an amber pill on the title bar
PX2, PY2 = DX + DW - 96, DY + 6
d.shape("rectangle", "Coming soon pill", x=PX2, y=PY2, width=86, height=15,
        radius=7.5, fill=NONE, stroke=AMBER, strokeWidth=1.5,
        dash=[3, 3], opacity=90)
d.text("COMING SOON", "Coming soon", x=PX2 + 43, y=PY2 + 11, size=8,
       font="Source Sans 3", color=AMBER, justify="center")
# dead window controls, top left is taken by the name — controls on the pill's left
for i, cx in enumerate([DX + DW - 120, DX + DW - 134]):
    d.shape("ellipse", f"Win control {i+1}", x=cx, y=DY + 9, width=9,
            height=9, fill=NONE, stroke=GHOST, strokeWidth=1.5, opacity=60)

# username field: filled, greyed — it remembers you
FY = DY + 48
d.text("USER", "User label", x=DX + 20, y=FY - 4, size=8,
       font="Source Sans 3", color=FAINT, justify="left")
d.shape("rectangle", "User field", x=DX + 20, y=FY, width=DW - 40,
        height=22, radius=4, fill=FIELD_GRAD, stroke="#3E4E60",
        strokeWidth=1.5)
d.text("neppy", "User text", x=DX + 30, y=FY + 15, size=11,
       font="Source Sans 3", color=FAINT, justify="left")

# password field: all dots, caret still blinking
PY3 = FY + 44
d.text("PASSWORD", "Pass label", x=DX + 20, y=PY3 - 4, size=8,
       font="Source Sans 3", color=FAINT, justify="left")
d.shape("rectangle", "Pass field", x=DX + 20, y=PY3, width=DW - 40,
        height=22, radius=4, fill=FIELD_GRAD, stroke=CYAN_DIM,
        strokeWidth=1.5)
d.text("••••••••••", "Pass dots", x=DX + 30, y=PY3 + 15, size=11,
       font="Source Sans 3", color=CYAN, justify="left")
# the blinking caret
d.shape("rectangle", "Caret", x=DX + 98, y=PY3 + 4, width=2, height=14,
        fill=CYAN, opacity=90, stroke=NONE)

# the dead LOG IN button — enabled style, but nothing answers
BY = PY3 + 36
d.shape("rectangle", "Login button", x=DX + DW/2 - 45, y=BY, width=90,
        height=24, radius=5, fill=NONE, stroke=CYAN_DIM, strokeWidth=1.5,
        dash=[4, 3], opacity=70)
d.text("LOG IN", "Login label", x=DX + DW/2, y=BY + 16, size=10,
       font="Source Sans 3", color=CYAN_DIM, justify="center")

# the spinner cursor, forever mid-wait, parked at the button
SCX, SCY = DX + DW/2 + 66, BY + 8
d.path(f"M{SCX + 11},{SCY} A11,11 0 1 1 {SCX},{SCY - 11}",
       "Spinner", fill=NONE, stroke=CYAN, strokeWidth=2.5, cap="round",
       dash=[5, 4], opacity=75)
# ghost arrow cursor trailing it
d.path(f"M{SCX + 18},{SCY + 16} L{SCX + 18},{SCY + 34} L{SCX + 23},{SCY + 29} "
       f"L{SCX + 27},{SCY + 36} L{SCX + 30},{SCY + 34} L{SCX + 26},{SCY + 27} "
       f"L{SCX + 32},{SCY + 27} Z", "Ghost cursor", fill=NONE,
       stroke=GHOST, strokeWidth=2, opacity=45)

# --- punchline sub-caption -------------------------------------------------------------
r = d.text("IT IS WAITING FOR A FUTURE", "Punchline 1", x=500,
           y=PY + PH - 58, size=20, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch1 tracking", ids=[r["id"]], tracking=90)
r = d.text("THAT WAS CANCELED.", "Punchline 2", x=500,
           y=PY + PH - 32, size=20, font="Virelai Sans", color=PUNCH,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "punch2 tracking", ids=[r["id"]], tracking=90)

# --- flourish on the plate below the poster ----------------------------------------------
d.path("M415,668 L485,668 M515,668 L585,668", "Flourish rules", fill=NONE,
       stroke=AMBER, strokeWidth=2, opacity=55)
d.path(rot_rect_path(500, 668, 9, 9, 45), "Flourish diamond", fill=AMBER,
       opacity=60, stroke=NONE)

# --- name + role ----------------------------------------------------------------------
d.text("NEPPY SYSDREAM", "Name", x=500, y=905, size=56,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("WAITING FOR A FUTURE THAT WAS CANCELED", "Role", x=500,
           y=950, size=18, font="Virelai Sans", color=FAINT,
           justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=110)

d.finish("aph-032-neppy-sysdream-V1R00")
