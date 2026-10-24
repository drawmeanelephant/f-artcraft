#!/usr/bin/env python3
"""Provisional Mint — mascot portrait V1R00.
A clerk mascot in a green eyeshade pressing an official seal onto high-quality
cardstock, the red ink still wet; a stack of freshly minted coins stands
nearby, faces blank — valued later, if ever. 1000x1000.
Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Provisional Mint — Mascot Portrait", 1000, 1000)

INK = "#2C1E14"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1A0F08"}, {"offset": 1, "color": "#0A0604"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8A6046"}, {"offset": 0.7, "color": "#5C4130"},
    {"offset": 1, "color": "#332418"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4E3A28"}, {"offset": 1, "color": "#221610"}]}}
DESK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5638"}, {"offset": 1, "color": "#4E3320"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#C8A87E"}, {"offset": 0.7, "color": "#A08054"},
    {"offset": 1, "color": "#7A5E3C"}]}}
COIN_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E0BC62"}, {"offset": 0.7, "color": "#B8923E"},
    {"offset": 1, "color": "#8A6A2C"}]}}
STAMP_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A6A44"}, {"offset": 1, "color": "#6A4428"}]}}
SEAL = "#A83A32"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#B08A62", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0DCBC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,234,8),(801,229,7),(157,526,9),(837,544,8),
                               (246,766,7),(754,748,9),(133,394,6),(865,389,7),
                               (391,112,7),(613,109,8),(333,824,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5E4832", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#140C08",
       strokeWidth=4, opacity=70)

# --- scene halo ------------------------------------------------------------------
d.shape("ellipse", "Scene halo", x=280, y=330, width=500, height=330,
        fill="#F0B06A", opacity=9, stroke=NONE)

# --- the desk ----------------------------------------------------------------------
d.shape("ellipse", "Desk shadow", x=300, y=684, width=480, height=20,
        fill="#0E0806", opacity=40, stroke=NONE)
d.shape("rectangle", "Desk front", x=300, y=600, width=500, height=100,
        fill=DESK_GRAD, stroke=INK, strokeWidth=5)
d.path("M316,640 L784,640 M316,668 L784,668", "Desk grain", fill=NONE,
       stroke="#3A2416", strokeWidth=3, opacity=60)
d.shape("rectangle", "Desk top", x=280, y=560, width=540, height=44,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#8A6238"}, {"offset": 1, "color": "#5E3F24"}]}},
        stroke=INK, strokeWidth=5)
d.path("M292,574 L808,574", "Desk top grain", fill=NONE, stroke="#4A3018",
       strokeWidth=3, opacity=60)

# --- the mascot, behind the desk -------------------------------------------------------
d.shape("ellipse", "Mascot shadow", x=320, y=690, width=190, height=18,
        fill="#0E0806", opacity=35, stroke=NONE)
d.shape("ellipse", "Body", x=322, y=478, width=176, height=210,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# clerk collar + tie
d.path("M384,486 L404,505 L424,486 L424,498 L404,517 L384,498 Z",
       "Collar", fill="#E8DCC8", stroke=INK, strokeWidth=3)
d.path("M400,512 L408,512 L406,548 L402,548 Z", "Tie", fill="#7A3A3A",
       stroke=INK, strokeWidth=2.5)
# head
d.shape("ellipse", "Head", x=338, y=356, width=136, height=132,
        fill=FUR_GRAD, stroke=INK, strokeWidth=5)
# ears
for ex in (350, 462):
    d.shape("ellipse", f"Ear {ex}", x=ex-11, y=352, width=26, height=24,
            fill="#A08054", stroke=INK, strokeWidth=3.5)
# green eyeshade: mint official
d.path("M340,412 C356,392 376,384 406,384 C436,384 456,392 470,410 "
       "C444,400 368,400 340,412 Z", "Eyeshade band",
       fill="#4A6A48", stroke=INK, strokeWidth=3.5)
d.path("M340,412 C368,402 444,402 470,410 L478,424 C446,412 372,412 344,424 Z",
       "Eyeshade brim", fill="#2E4428", opacity=85, stroke=INK,
       strokeWidth=3)
# face: confidence ahead of verification
d.shape("ellipse", "Eye L", x=372, y=442, width=10, height=10,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=420, y=442, width=10, height=10,
        fill=INK, stroke=NONE)
d.path("M390,466 C398,472 408,472 416,466", "Smile", fill=NONE,
       stroke=INK, strokeWidth=4, cap="round")
# resting paw near the ink pad
d.path("M336,540 C360,562 384,576 408,586", "Arm rest", fill=NONE,
       stroke="#A08054", strokeWidth=16, cap="round")
d.shape("ellipse", "Rest paw", x=398, y=580, width=20, height=16,
        fill="#A08054", stroke=INK, strokeWidth=3.5)

# --- arm pressing the stamp --------------------------------------------------------------
d.path("M456,514 C492,502 528,490 556,482", "Arm press", fill=NONE,
       stroke="#A08054", strokeWidth=18, cap="round")

# --- the seal stamp, mid-stroke ------------------------------------------------------------
d.path("M536,486 L530,472 M598,492 L604,478", "Stamp motion", fill=NONE,
       stroke="#F0D8B8", strokeWidth=3.5, cap="round", opacity=55)
d.shape("ellipse", "Stamp knob", x=546, y=466, width=38, height=32,
        fill=STAMP_GRAD, stroke=INK, strokeWidth=4)
d.shape("rectangle", "Stamp neck", x=556, y=494, width=18, height=44,
        fill=STAMP_GRAD, stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Paw on knob", x=552, y=470, width=24, height=20,
        fill="#A08054", stroke=INK, strokeWidth=3.5)
d.shape("ellipse", "Seal head", x=538, y=532, width=54, height=22,
        fill="#8A3428", stroke=INK, strokeWidth=4)

# --- cardstock: the high-quality stack ------------------------------------------------------
d.path(rot_rect_path(582, 596, 152, 44, -7), "Sheet under 2",
       fill="#DCD2B4", stroke=INK, strokeWidth=2.5)
d.path(rot_rect_path(576, 590, 152, 44, 3), "Sheet under 1",
       fill="#E2D8BC", stroke=INK, strokeWidth=2.5)
d.path(rot_rect_path(570, 584, 152, 46, -4), "Cardstock",
       fill="#EAE0C8", stroke=INK, strokeWidth=3)
# ruled header scribbles, content pending
d.path(rot_rect_path(548, 574, 54, 5, -4), "Scribble 1", fill=NONE,
       stroke="#9A8E76", strokeWidth=2.5, opacity=75)
d.path(rot_rect_path(534, 590, 42, 5, -4), "Scribble 2", fill=NONE,
       stroke="#9A8E76", strokeWidth=2.5, opacity=75)
# the fresh seal impression, wet
d.shape("ellipse", "Seal sheen", x=566, y=560, width=46, height=38,
        fill="#E89058", opacity=25, stroke=NONE)
d.shape("ellipse", "Seal ring", x=572, y=564, width=36, height=32,
        fill=NONE, stroke=SEAL, strokeWidth=3.5)
d.path("M590,570 L593,577 L600,578 L595,583 L596,590 L590,586 L584,590 "
       "L585,583 L580,578 L587,577 Z", "Seal star", fill=NONE,
       stroke=SEAL, strokeWidth=2.5)
d.path("M578,570 C582,566 588,565 593,566", "Wet glint", fill=NONE,
       stroke="#FFFFFF", strokeWidth=2.5, cap="round", opacity=60)
d.shape("ellipse", "Ink drip", x=614, y=592, width=6, height=5,
        fill=SEAL, opacity=70, stroke=NONE)

# --- the ink pad, open ---------------------------------------------------------------------
d.shape("rectangle", "Pad case", x=398, y=576, width=72, height=24,
        fill="#2E3440", stroke=INK, strokeWidth=3.5, radius=5)
d.shape("rectangle", "Pad ink", x=404, y=580, width=60, height=14,
        fill="#8A3030", stroke=NONE, radius=3)
d.path("M410,585 L452,585", "Pad glint", fill=NONE, stroke="#D87A6A",
       strokeWidth=2.5, cap="round", opacity=70)
d.path(rot_rect_path(434, 566, 66, 10, -14), "Pad lid", fill="#3E4450",
       stroke=INK, strokeWidth=3)

# --- freshly minted coins, faces blank -------------------------------------------------------
d.shape("ellipse", "Coin shadow", x=684, y=594, width=140, height=14,
        fill="#0E0806", opacity=35, stroke=NONE)
for i, y in enumerate([588, 576, 564]):
    d.shape("ellipse", f"Coin stack {i+1}", x=668, y=y, width=76, height=16,
            fill=COIN_GRAD, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Coin top face", x=672, y=560, width=68, height=14,
        fill="#E4C470", stroke=INK, strokeWidth=2.5)
d.path("M690,566 L722,566", "Blank face glint", fill=NONE,
       stroke="#F4E0A0", strokeWidth=2.5, cap="round", opacity=75)
# one coin standing on edge, denomination TBD
d.shape("ellipse", "Coin edge", x=760, y=540, width=20, height=62,
        fill=COIN_GRAD, stroke=INK, strokeWidth=3)
d.path("M766,552 L766,590", "Edge glint", fill=NONE, stroke="#F4E0A0",
       strokeWidth=2.5, opacity=70)
# one loose coin on the desk
d.shape("ellipse", "Loose coin", x=792, y=592, width=56, height=13,
        fill=COIN_GRAD, stroke=INK, strokeWidth=2.5)
# minting sparkle
d.path("M770,518 L770,530 M764,524 L776,524", "Mint sparkle", fill=NONE,
       stroke="#F4E0A0", strokeWidth=3, cap="round", opacity=75)

# --- stray warm motes ---------------------------------------------------------------
for i, (x, y, w) in enumerate([(290,380,6),(260,520,5),(700,300,5),(850,470,6),
                               (230,640,6),(830,300,5),(500,270,5)]):
    d.shape("ellipse", f"Mote {i+1}", x=x, y=y, width=w, height=w,
            fill="#F0C898", opacity=40, stroke=NONE)

# --- captions -------------------------------------------------------------------------
d.text("PROVISIONAL MINT", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#F0E2CE", justify="center")
r = d.text("LEGITIMACY, STILL DRYING", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C8A884", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("265.provisional-mint-V1R00")
