#!/usr/bin/env python3
"""APH-019 Kindy Mcexistentialcrisis — aphorism plate V1R00. A process
loop stamped RESOLVED, the physical stamp still hovering above its own
verdict; in the loop's center a checkbox whose tick overshoots the box
and refuses to leave; a REASON tag tied to it mid-evaporation; and an
APPEAL form at lower left already arcing its UN-STAMP request back up
at the impression. Institutional green plate, amber + brick red.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("APH-019 Kindy Mcexistentialcrisis — Aphorism Plate", 1000, 1000)

INK = "#1C2A1E"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1B2620"}, {"offset": 1, "color": "#080C0A"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#46553F"}, {"offset": 0.7, "color": "#2A362B"},
    {"offset": 1, "color": "#131A14"}]}}
PAPER_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F0E8CC"}, {"offset": 0.65, "color": "#DCCDA2"},
    {"offset": 1, "color": "#B8A878"}]}}
WOOD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5638"}, {"offset": 0.6, "color": "#54381F"},
    {"offset": 1, "color": "#33220F"}]}}
LOOP = "#8FA89B"
LOOP_HI = "#D8E4D2"
AMBER = "#D8A846"
STAMP_RED = "#B0492F"
CREAM = "#EAE4CC"
FAINT = "#8CA08C"
KEY = "#C6D2AE"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A8A62", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#C8D4A8", strokeWidth=3, opacity=40)
# plate patina
d.shape("ellipse", "Patina 1", x=205, y=185, width=200, height=120,
        fill="#5A6E4E", opacity=20, stroke=NONE)
d.shape("ellipse", "Patina 2", x=620, y=590, width=220, height=130,
        fill="#5A6E4E", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(210, 255, 7), (792, 245, 8), (158, 505, 6),
                               (842, 495, 7), (252, 735, 6), (758, 725, 7)]):
    d.shape("ellipse", f"Fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#6E8058", opacity=35, stroke=NONE)

# floor shadow under the paperwork
d.shape("ellipse", "Floor shadow", x=280, y=614, width=380, height=46,
        fill="#000000", opacity=30, stroke=NONE)

# --- the loop: a process cycle carrying a verdict ------------------------------
# thick track arc, 290 degrees, gap at lower right where the arrowhead lands
d.path("M460.8,585.4 A168,168 0 1 1 635.5,504", "Loop track", fill=NONE,
       stroke=LOOP, strokeWidth=28, opacity=80, cap="round")
d.path("M460.8,585.4 A168,168 0 1 1 635.5,504", "Loop centerline",
       fill=NONE, stroke=LOOP_HI, strokeWidth=4, opacity=35)
# arrowhead: travel is clockwise, pointing down-left at the gap
d.path("M620.5,530 L648.5,511.5 L622.5,496.5 Z", "Loop arrowhead",
       fill=LOOP, opacity=85, stroke=NONE)

# --- the persistent checkbox, dead center on the loop --------------------------
d.shape("ellipse", "Checkbox glow", x=430, y=360, width=120, height=120,
        fill=AMBER, opacity=12, stroke=NONE)
d.shape("rectangle", "Checkbox", x=444, y=374, width=92, height=92,
        radius=10, fill=PAPER_GRAD, stroke=INK, strokeWidth=5)
# the tick overshoots its box — it persisted after the reason expired
d.path("M462,418 L488,446 L546,380", "Tick border", fill=NONE,
       stroke=INK, strokeWidth=17, cap="round", join="round")
d.path("M462,418 L488,446 L546,380", "Tick", fill=NONE,
       stroke=AMBER, strokeWidth=11, cap="round", join="round")

# --- the REASON tag, tied on and evaporating -----------------------------------
d.path("M536,424 Q552,428 564,443", "Tag string", fill=NONE,
       stroke=FAINT, strokeWidth=2.5, opacity=60)
d.shape("rectangle", "Reason tag", x=560, y=428, width=92, height=38,
        radius=5, fill=PAPER_GRAD, stroke=INK, strokeWidth=2.5,
        opacity=55)
d.shape("ellipse", "Tag hole", x=564, y=443, width=8, height=8,
        fill=NONE, stroke=INK, strokeWidth=2, opacity=55)
r = d.text("REASON", "Tag text", x=610, y=452, size=12,
           font="Virelai Sans", color=INK, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "tag tracking", ids=[r["id"]], tracking=30)
    d.cmd("object.setProps", "tag text fade", id=r["id"], opacity=60)
d.path("M578,449 L642,445", "Tag strike", fill=NONE, stroke=STAMP_RED,
       strokeWidth=2.5, opacity=60, cap="round")
# the reason, evaporating out through the loop
for i, (ex, ey, er, eo) in enumerate([(668, 440, 4, 35), (684, 432, 3.5, 25),
                                     (700, 422, 3, 16), (714, 410, 2.5, 10)]):
    d.shape("ellipse", f"Reason mote {i+1}", x=ex - er, y=ey - er,
            width=er * 2, height=er * 2, fill="#E8E0C0", opacity=eo,
            stroke=NONE)

# --- the RESOLVED impression, slammed across the loop's top --------------------
d.shape("rectangle", "Impression ghost", x=394, y=210, width=225, height=66,
        radius=4, fill=NONE, stroke=STAMP_RED, strokeWidth=3, opacity=25)
d.shape("rectangle", "Impression", x=390, y=206, width=225, height=66,
        radius=4, fill=NONE, stroke=STAMP_RED, strokeWidth=4.5, opacity=85)
d.shape("rectangle", "Impression inner", x=398, y=214, width=209, height=50,
        radius=3, fill=NONE, stroke=STAMP_RED, strokeWidth=2, opacity=70)
r = d.text("RESOLVED", "Impression text", x=502, y=248, size=25,
           font="Virelai Sans", color=STAMP_RED, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "impression tracking", ids=[r["id"]], tracking=60)
# impact tick where the stamp landed
d.path("M607,282 L617,294", "Impact tick", fill=NONE, stroke=AMBER,
       strokeWidth=3, opacity=50, cap="round")

# --- the physical stamp, hovering above its own verdict -------------------------
d.shape("rectangle", "Stamp base", x=425, y=156, width=155, height=26,
        radius=4, fill="#7E2B22", stroke=INK, strokeWidth=4)
d.shape("rectangle", "Base sheen", x=431, y=160, width=143, height=8,
        fill="#B8543E", opacity=55, stroke=NONE)
d.shape("rectangle", "Stamp collar", x=440, y=136, width=125, height=20,
        radius=3, fill="#8A8970", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Stamp stem", x=490, y=92, width=20, height=44,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Stamp grip", x=455, y=66, width=90, height=40,
        fill=WOOD_GRAD, stroke=INK, strokeWidth=4)
d.shape("ellipse", "Grip sheen", x=472, y=72, width=38, height=13,
        fill="#A8763E", opacity=60, stroke=NONE)

# --- the appeal, filed immediately ---------------------------------------------
d.shape("rectangle", "Appeal shadow", x=248, y=506, width=168, height=124,
        radius=4, fill="#000000", opacity=30, stroke=NONE)
d.shape("rectangle", "Appeal form", x=240, y=498, width=168, height=124,
        radius=4, fill=PAPER_GRAD, stroke=INK, strokeWidth=3.5)
# dog-ear
d.path("M378,498 L408,528 L378,528 Z", "Appeal dog ear",
       fill="#C9B183", stroke=INK, strokeWidth=2.5)
d.text("APPEAL", "Appeal header", x=254, y=526, size=15,
       font="Virelai Sans", color=INK, justify="left")
d.path("M254,540 L394,540", "Appeal rule", fill=NONE, stroke=INK,
       strokeWidth=2, opacity=70)
for k, ly in enumerate([560, 578]):
    d.path(f"M254,{ly} L394,{ly}", f"Appeal line {k+1}", fill=NONE,
           stroke=INK, strokeWidth=1.5, opacity=30)
# the request: an empty box and an un-verb
d.shape("rectangle", "Un-stamp box", x=254, y=592, width=14, height=14,
        fill=NONE, stroke=INK, strokeWidth=2)
d.text("UN-STAMP", "Un-stamp label", x=276, y=604, size=11,
       font="Virelai Sans", color=STAMP_RED, justify="left")
# filing trajectory: dashed arc up into the impression
d.path("M402,500 Q320,415 380,295", "Appeal arc", fill=NONE,
       stroke=AMBER, strokeWidth=3.5, opacity=65, dash=[8, 9],
       cap="round")
d.path("M391,273 L388,299 L372,291 Z", "Appeal arrowhead",
       fill=AMBER, opacity=80, stroke=NONE)

# --- aphorism line + name + role ------------------------------------------------
r = d.text("THE CHECKBOX PERSISTED", "Key line 1", x=500, y=722,
           size=22, font="Virelai Sans", color=KEY, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key1 tracking", ids=[r["id"]], tracking=100)
r = d.text("AFTER THE REASON EXPIRED.", "Key line 2", x=500, y=756,
           size=22, font="Virelai Sans", color=KEY, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key2 tracking", ids=[r["id"]], tracking=100)

d.text("KINDY MCEXISTENTIALCRISIS", "Name", x=500, y=905, size=52,
       font="Virelai Sans", color=CREAM, justify="center")
r = d.text("THE CHECKBOX PERSISTED", "Role", x=500, y=950, size=18,
           font="Virelai Sans", color=FAINT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=160)

d.finish("aph-019-kindy-mcexistentialcrisis-V1R00")
