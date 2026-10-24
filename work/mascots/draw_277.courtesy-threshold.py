#!/usr/bin/env python3
"""Courtesy Threshold — mascot portrait V1R00.
A bouncer mascot smiling beside a polished oak door with a brass handle,
ergonomic waiting-room chairs nearby. The welcome remains audible;
the opening does not. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Courtesy Threshold — Mascot Portrait", 1000, 1000)

INK = "#2A1C10"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1D150E"}, {"offset": 1, "color": "#0B0705"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#B08C60"}, {"offset": 0.7, "color": "#84663F"},
    {"offset": 1, "color": "#4E3B24"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#56432C"}, {"offset": 1, "color": "#241A10"}]}}
OAK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#A87846"}, {"offset": 0.6, "color": "#7E532C"},
    {"offset": 1, "color": "#5A3A1E"}]}}
OAK_DARK = "#4E3218"
OAK_GRAIN = "#6E4624"
OAK_SHEEN = "#C99658"
BRASS_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4C26A"}, {"offset": 1, "color": "#A67C30"}]}}
CHAIR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7FA69E"}, {"offset": 1, "color": "#4A6C64"}]}}
CHAIR_DARK = "#3A5A52"
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C2AE92"}, {"offset": 0.7, "color": "#9E8A70"},
    {"offset": 1, "color": "#74634E"}]}}
FUR_MID = "#9E8A70"
SUIT = "#4A4038"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#A88A5E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E4D2B0", strokeWidth=3, opacity=50)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#584430", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#1A120A",
       strokeWidth=4, opacity=70)

# --- the polished oak door ---------------------------------------------------------
d.shape("ellipse", "Door shadow", x=400, y=688, width=260, height=16,
        fill="#120C06", opacity=40, stroke=NONE)
# frame + crown
d.path("M396,196 L644,196 L644,700 L396,700 Z", "Door frame",
       fill="#5C3E20", stroke=INK, strokeWidth=4)
d.path("M388,178 L652,178 L652,204 L388,204 Z", "Crown molding",
       fill=OAK_GRAD, stroke=INK, strokeWidth=4)
# door slab
d.path("M414,214 L626,214 L626,700 L414,700 Z", "Door slab",
       fill=OAK_GRAD, stroke=INK, strokeWidth=3.5)
# wood grain
for i, x in enumerate([438, 470, 502, 534, 566, 598]):
    d.path(f"M{x},224 C{x-5},340 {x+5},470 {x-3},688", f"Grain {i+1}",
           fill=NONE, stroke=OAK_GRAIN, strokeWidth=2, opacity=45)
# sheen down the polished face
d.path("M428,220 L470,220 L452,694 L424,694 Z", "Polish sheen",
       fill=OAK_SHEEN, opacity=16, stroke=NONE)
# four recessed panels: two tall up top, two square below
for i, (x0, y0, w, h) in enumerate([(438,244,74,190),(528,244,74,190),
                                     (438,462,74,170),(528,462,74,170)]):
    d.path(f"M{x0},{y0} L{x0+w},{y0} L{x0+w},{y0+h} L{x0},{y0+h} Z",
           f"Panel {i+1}", fill="#6A4522", stroke=INK, strokeWidth=3)
    d.path(f"M{x0+8},{y0+8} L{x0+w-8},{y0+8} L{x0+w-8},{y0+h-8} L{x0+8},{y0+h-8} Z",
           f"Panel {i+1} bevel", fill=NONE, stroke=OAK_SHEEN,
           strokeWidth=2, opacity=50)
# brass kick plate + hinges
d.path("M424,648 L616,648 L616,690 L424,690 Z", "Kick plate",
       fill=BRASS_GRAD, stroke=INK, strokeWidth=3)
for i, y in enumerate([262, 596]):
    d.path(f"M404,{y} L424,{y} L424,{y+34} L404,{y+34} Z", f"Hinge {i+1}",
           fill=BRASS_GRAD, stroke=INK, strokeWidth=2.5)
# brass lever handle on backplate + keyhole below
d.path("M580,452 L612,452 L612,512 L580,512 Z", "Handle plate",
       fill=BRASS_GRAD, stroke=INK, strokeWidth=3)
d.path("M596,470 L596,486 L566,486 C556,486 552,476 560,470 Z",
       "Lever", fill=BRASS_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Keyhole top", x=592, y=494, width=8, height=8,
        fill=INK, stroke=NONE)
d.path("M592,500 L600,500 L598,510 L594,510 Z", "Keyhole slot",
       fill=INK, stroke=NONE)
# threshold light: a sliver of glow escaping under the door
d.path("M414,700 L626,700 L640,706 L400,706 Z", "Threshold glow",
       fill="#F0D89A", opacity=35, stroke=NONE)

# --- ergonomic waiting-room chairs, queued politely -----------------------------------
def chair(cx, sc, tag):
    d.shape("ellipse", f"{tag} shadow", x=cx-46*sc, y=686, width=92*sc,
            height=12*sc, fill="#120C06", opacity=30, stroke=NONE)
    # lumbar-curved back, centered over the seat
    d.path(f"M{cx-36*sc},{570} "
           f"C{cx-42*sc},{514} {cx-16*sc},{492} {cx+4*sc},{498} "
           f"C{cx+22*sc},{492} {cx+36*sc},{514} {cx+30*sc},{570} "
           f"C{cx+8*sc},{560} {cx-14*sc},{560} {cx-36*sc},{570} Z",
           f"{tag} back", fill=CHAIR_GRAD, stroke=INK, strokeWidth=3.5)
    # seat
    d.path(f"M{cx-40*sc},{580} C{cx-20*sc},{572} {cx+24*sc},{572} {cx+40*sc},{580} "
           f"L{cx+34*sc},{598} C{cx+14*sc},{606} {cx-22*sc},{606} {cx-38*sc},{598} Z",
           f"{tag} seat", fill=CHAIR_GRAD, stroke=INK, strokeWidth=3.5)
    # gas post + star base
    d.path(f"M{cx},{604} L{cx},{664}", f"{tag} post", fill=NONE,
           stroke=CHAIR_DARK, strokeWidth=5)
    for j, (dx, dy) in enumerate([(-30,690),(0,694),(30,690)]):
        d.path(f"M{cx},{664} L{cx+dx*sc},{dy}", f"{tag} leg {j+1}",
               fill=NONE, stroke=CHAIR_DARK, strokeWidth=4.5, cap="round")

chair(716, 1.0, "Chair near")
chair(806, 0.86, "Chair far")

# --- the bouncer, smiling at the exact point where passage thins ----------------------
d.shape("ellipse", "Bouncer shadow", x=180, y=684, width=200, height=18,
        fill="#120C06", opacity=35, stroke=NONE)
# broad body in suit tones at the shoulders
d.path("M236,688 C216,620 214,540 244,492 C272,452 342,450 372,494 "
       "C398,532 398,616 382,688 Z",
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# suit shoulders + lapels
d.path("M244,492 C260,470 296,458 310,458 L306,520 L268,536 Z",
       "Lapel L", fill=SUIT, stroke=INK, strokeWidth=3)
d.path("M372,494 C356,470 324,458 310,458 L314,520 L350,536 Z",
       "Lapel R", fill=SUIT, stroke=INK, strokeWidth=3)
d.path("M296,474 L324,474 L318,494 L302,494 Z", "Bowtie", fill=SUIT,
       stroke=INK, strokeWidth=2.5)
# arms crossed: two forearm bands across the chest, paws tucked
d.path("M252,556 C286,572 330,576 368,564", "Forearm top", fill=NONE,
       stroke=FUR_MID, strokeWidth=17, cap="round")
d.path("M256,588 C290,600 334,602 366,592", "Forearm low", fill=NONE,
       stroke=FUR_MID, strokeWidth=17, cap="round")
d.shape("ellipse", "Paw tucked L", x=246, y=576, width=24, height=20,
        fill=FUR_MID, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Paw tucked R", x=356, y=548, width=24, height=20,
        fill=FUR_MID, stroke=INK, strokeWidth=3)
# head with the permanent welcome
d.shape("ellipse", "Head", x=246, y=352, width=132, height=126,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
for ex in (258, 366):
    d.shape("ellipse", f"Ear {ex}", x=ex-11, y=348, width=26, height=24,
            fill=FUR_MID, stroke=INK, strokeWidth=3.5)
d.path("M274,418 C281,424 290,424 296,418", "Eye L", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M322,418 C329,424 338,424 344,418", "Eye R", fill=NONE,
       stroke=INK, strokeWidth=4.5, cap="round")
d.path("M284,448 C296,458 324,458 336,448", "Smile", fill=NONE,
       stroke=INK, strokeWidth=5, cap="round")
# earpiece wire — the answer arrives from elsewhere
d.shape("ellipse", "Earpiece", x=362, y=424, width=10, height=10,
        fill=SUIT, stroke=INK, strokeWidth=2)
d.path("M367,434 C360,452 352,466 344,476", "Wire", fill=NONE,
       stroke=SUIT, strokeWidth=2.5, opacity=80)

# --- captions -------------------------------------------------------------------------
d.text("COURTESY THRESHOLD", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#F0E0BC", justify="center")
r = d.text("YOU ARE MOST WELCOME TO WAIT", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#CDAF82", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("277.courtesy-threshold-V1R00")
