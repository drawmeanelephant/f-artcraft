#!/usr/bin/env python3
"""Complimentary Ghostline — mascot portrait V1R00.
A translucent ghost haunting an emptied datacenter: unplugged server
racks, a support line ringing forever unanswered, and a sticky note
promising the service is only resting. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Complimentary Ghostline — Mascot Portrait", 1000, 1000)

INK = "#1C1A26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0A0C14"}, {"offset": 1, "color": "#04060C"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E4460"}, {"offset": 0.7, "color": "#262C42"},
    {"offset": 1, "color": "#12141F"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2A2E3E"}, {"offset": 1, "color": "#12141E"}]}}
RACK = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A4250"}, {"offset": 1, "color": "#1A2028"}]}}
GHOST = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F0F2FF"}, {"offset": 0.7, "color": "#B8C2E8"},
    {"offset": 1, "color": "#7E88B8"}]}}
PHONE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E4458"}, {"offset": 1, "color": "#262030"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6E7694", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#CCD4EC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#2C3248", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#080A10",
       strokeWidth=4, opacity=70)

# --- server racks, both dead and unplugged -------------------------------------------
def rack(x, label):
    d.shape("ellipse", f"{label} shadow", x=x-14, y=680, width=150, height=20,
            fill="#05070C", opacity=50, stroke=NONE)
    d.shape("rectangle", label, x=x, y=330, width=122, height=356,
            fill=RACK, stroke=INK, strokeWidth=5, radius=6)
    # vent slats + unit bays
    for i, by in enumerate(range(352, 660, 44)):
        d.shape("rectangle", f"{label} bay {i}", x=x+12, y=by, width=98,
                height=30, fill="#20262F", stroke="#0E1218", strokeWidth=2.5,
                radius=3)
        for vx in range(0, 4):
            d.path(f"M{x+22+vx*12},{by+8} L{x+22+vx*12},{by+22}",
                   f"{label} vent {i}-{vx}", fill=NONE, stroke="#0C1016",
                   strokeWidth=2, opacity=70)
    return x
rack(210, "Rack L")
rack(668, "Rack R")
# status LEDs: all dark but one dying amber
d.shape("ellipse", "LED L1", x=306, y=362, width=7, height=7,
        fill="#3A3026", stroke=NONE)
d.shape("ellipse", "LED L2", x=306, y=406, width=7, height=7,
        fill="#E8A84A", stroke=NONE, opacity=85)
d.shape("ellipse", "LED L2 halo", x=302, y=402, width=15, height=15,
        fill="#E8A84A", opacity=15, stroke=NONE)
d.shape("ellipse", "LED R1", x=676, y=362, width=7, height=7,
        fill="#3A3026", stroke=NONE)
d.shape("ellipse", "LED R2", x=676, y=450, width=7, height=7,
        fill="#3A3026", stroke=NONE)
# cobweb on the left rack corner
d.path("M210,330 L252,330 C244,352 228,366 210,372 Z", "Cobweb",
       fill=NONE, stroke="#9AA4BC", strokeWidth=1.5, opacity=40)
d.path("M210,330 C220,346 234,358 252,362 M210,352 C218,358 226,362 236,364",
       "Cobweb strands", fill=NONE, stroke="#9AA4BC", strokeWidth=1.2,
       opacity=35)
# sticky note promising return
d.path(rot_rect_path(268, 500, 56, 44, -6), "Sticky note",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#E8D88A"}, {"offset": 1, "color": "#B8A85E"}]}},
       stroke=INK, strokeWidth=2.5)
d.text("BACK", "Note line 1", x=267, y=504, size=11, font="Virelai Sans",
       color="#5E5230", justify="center")
d.text("SOON", "Note line 2", x=266, y=520, size=11, font="Virelai Sans",
       color="#5E5230", justify="center")
# unplugged cables drooping from the racks
d.path("M236,686 C236,720 300,724 318,700 C330,684 344,684 352,696",
       "Cable L", fill=NONE, stroke="#0E1218", strokeWidth=6, cap="round")
d.path("M764,686 C764,716 716,720 700,702", "Cable R", fill=NONE,
       stroke="#0E1218", strokeWidth=6, cap="round")
# dead wall socket + loose plug
d.shape("rectangle", "Socket", x=352, y=676, width=30, height=24,
        fill="#3E4454", stroke=INK, strokeWidth=3, radius=4)
d.path("M360,684 L360,690 M372,684 L372,690", "Socket holes", fill=NONE,
       stroke="#0C1016", strokeWidth=3, cap="round")
d.path(rot_rect_path(392, 706, 26, 16, -18), "Loose plug",
       fill="#2A3038", stroke=INK, strokeWidth=3)
d.path("M404,700 L414,694 M404,706 L414,700", "Plug prongs", fill=NONE,
       stroke=INK, strokeWidth=3, cap="round")

# --- the ghost: translucent, hovering between the racks --------------------------------
d.shape("ellipse", "Ghost glow", x=330, y=250, width=330, height=330,
        fill="#A8B4E8", opacity=12, stroke=NONE)
d.shape("ellipse", "Ghost floor light", x=400, y=664, width=200, height=26,
        fill="#A8B4E8", opacity=14, stroke=NONE)
# body with wavy hem
d.path("M500,330 C436,330 396,382 396,452 L396,560 "
       "C408,548 420,548 430,560 C442,574 456,574 468,560 "
       "C478,550 490,550 500,560 C510,550 522,550 532,560 "
       "C544,574 558,574 570,560 C580,548 592,548 604,560 L604,452 "
       "C604,382 564,330 500,330 Z", "Ghost body", fill=GHOST,
       stroke=INK, strokeWidth=5, opacity=88)
# stubby arms raised in a faint shrug
d.path("M398,470 C368,478 348,498 342,524 C356,514 372,510 390,512 "
       "C398,498 400,484 398,470 Z", "Arm L", fill=GHOST, stroke=INK,
       strokeWidth=4, opacity=88)
d.path("M602,470 C632,478 652,498 658,524 C644,514 628,510 610,512 "
       "C602,498 600,484 602,470 Z", "Arm R", fill=GHOST, stroke=INK,
       strokeWidth=4, opacity=88)
# hollow eyes + small apologetic mouth
d.shape("ellipse", "Eye L", x=452, y=416, width=26, height=34,
        fill="#1C1A26", stroke=NONE, opacity=85)
d.shape("ellipse", "Eye R", x=522, y=416, width=26, height=34,
        fill="#1C1A26", stroke=NONE, opacity=85)
d.shape("ellipse", "Eye glint L", x=458, y=424, width=8, height=10,
        fill="#A8B4E8", opacity=70, stroke=NONE)
d.shape("ellipse", "Eye glint R", x=528, y=424, width=8, height=10,
        fill="#A8B4E8", opacity=70, stroke=NONE)
d.path("M486,478 C494,470 506,470 514,478", "Mouth", fill=NONE,
       stroke="#3A3450", strokeWidth=4, cap="round", opacity=80)
# sheen along the left edge
d.path("M412,420 C410,380 436,352 466,342", "Ghost sheen", fill=NONE,
       stroke="#FFFFFF", strokeWidth=5, cap="round", opacity=35)

# --- the support line, ringing unanswered ----------------------------------------------
d.shape("ellipse", "Phone shadow", x=560, y=678, width=130, height=16,
        fill="#05070C", opacity=50, stroke=NONE)
# base + handset resting on the cradle
d.path("M566,660 L674,660 L686,690 L554,690 Z", "Phone base",
       fill=PHONE, stroke=INK, strokeWidth=4, join="round")
d.path("M580,632 L660,632 C668,632 674,640 674,648 L674,660 L566,660 "
       "L566,648 C566,640 572,632 580,632 Z", "Handset",
       fill=PHONE, stroke=INK, strokeWidth=4, join="round")
d.shape("ellipse", "Handset earpiece", x=572, y=640, width=22, height=16,
        fill="#1A1622", stroke=INK, strokeWidth=2.5)
d.shape("ellipse", "Handset mic", x=648, y=640, width=22, height=16,
        fill="#1A1622", stroke=INK, strokeWidth=2.5)
# keypad
for i in range(3):
    for j in range(3):
        d.shape("ellipse", f"Key {i}-{j}", x=596+j*22, y=666+i*8,
                width=8, height=5, fill="#0E1218", stroke=NONE)
# cord dangling to a cut end — nobody home
d.path("M672,682 C690,696 688,716 672,722 C660,726 648,720 652,710",
       "Phone cord", fill=NONE, stroke="#0E1218", strokeWidth=4,
       cap="round")
# ring arcs above the handset, fading
for i, rr in enumerate([30, 48, 66]):
    d.path(f"M{620-rr},{610-rr//3} A{rr},{rr} 0 0 1 {620+rr},{610-rr//3}",
           f"Ring {i+1}", fill=NONE, stroke="#E8D88A",
           strokeWidth=3.5, cap="round", opacity=70-i*20)
# a faint "ON HOLD" ticket taped above the phone
d.path(rot_rect_path(700, 580, 64, 26, 5), "Hold tag",
       fill="#B8B0C8", stroke=INK, strokeWidth=2.5, opacity=80)
d.text("ON HOLD", "Hold text", x=700, y=586, size=10, font="Virelai Sans",
       color="#3A3450", justify="center")

# --- dust motes in the empty air ---------------------------------------------------------
for i, (x, y, w) in enumerate([(330,260,5),(660,270,6),(420,240,4),
                               (580,300,5),(250,430,5),(740,430,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#A8B4E8", opacity=30, stroke=NONE)

# --- captions ----------------------------------------------------------------------
d.text("COMPLIMENTARY GHOSTLINE", "Name", x=500, y=930, size=50,
       font="Virelai Sans", color="#CCD4EC", justify="center")
r = d.text("FORMALLY OVER, TEXTUALLY ONGOING", "Role", x=500, y=968,
           size=23, font="Virelai Sans", color="#8A94BC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("324.complimentary-ghostline-V1R00")
