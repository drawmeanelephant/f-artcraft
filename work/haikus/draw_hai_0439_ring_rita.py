#!/usr/bin/env python3
"""HAI-0439 Ring Rita — haiku plate V1R00. The voluntary panopticon: a smart
doorbell watches its own porch, a request-portal window holds the homeowner's
key, a subscription receipt curls off the housing, and the neighbor's porch
stares back — the mesh is the fee. 1000x1000.
House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("HAI-0439 Ring Rita — Haiku Plate", 1000, 1000)

INK = "#33211B"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#18100C"}, {"offset": 1, "color": "#0B0705"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#473428"}, {"offset": 0.7, "color": "#261B15"},
    {"offset": 1, "color": "#130D0A"}]}}
BODY = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4A5058"}, {"offset": 0.55, "color": "#2C3036"},
    {"offset": 1, "color": "#181B20"}]}}
LENS = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E8F4FA"}, {"offset": 0.45, "color": "#7FB2CC"},
    {"offset": 1, "color": "#1E4256"}]}}
DOOR = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5C4434"}, {"offset": 1, "color": "#33231A"}]}}
PORTAL = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E4250"}, {"offset": 1, "color": "#182630"}]}}
PAPER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#EFE6D8"}, {"offset": 1, "color": "#C4B49E"}]}}
PALE = "#F2E4D8"
SOFT = "#B99C8A"
CYAN = "#9ED4E8"
RED = "#E85C4A"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8C6F5C", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#F0E4D4", strokeWidth=3, opacity=36)
d.shape("ellipse", "Glow pool", x=280, y=220, width=440, height=420,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#D8A86A", "opacity": 0.13},
            {"offset": 1, "color": "#D8A86A", "opacity": 0}]}},
        stroke=NONE)

# --- your porch: door, jamb, mat under watch ------------------------------------
d.shape("rectangle", "Door frame", x=170, y=300, width=158, height=400,
        radius=6, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#2C1F18"}, {"offset": 1, "color": "#1A110C"}]}},
        stroke=INK, strokeWidth=4)
d.shape("rectangle", "Door", x=184, y=314, width=130, height=386,
        radius=4, fill=DOOR, stroke=INK, strokeWidth=3.5)
d.shape("rectangle", "Door panel", x=200, y=340, width=98, height=140,
        radius=4, fill=NONE, stroke="#241812", strokeWidth=3, opacity=70)
d.shape("rectangle", "Door panel low", x=200, y=500, width=98, height=150,
        radius=4, fill=NONE, stroke="#241812", strokeWidth=3, opacity=70)
d.shape("ellipse", "Knob", x=296, y=516, width=14, height=14,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#E8C88A"}, {"offset": 1, "color": "#8A6234"}]}},
        stroke=INK, strokeWidth=2)
# the welcome mat — consent theater
d.shape("rectangle", "Mat", x=176, y=712, width=180, height=42, radius=8,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#4A362A"}, {"offset": 1, "color": "#2A1D15"}]}},
        stroke=INK, strokeWidth=3.5)
r = d.text("WELCOME", "Mat text", x=266, y=741, size=20,
           font="Virelai Sans", color="#8A6E58", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "mat tracking", ids=[r["id"]], tracking=180)

# --- the neighbor's porch sees your porch ----------------------------------------
d.path("M742,478 L810,430 L878,478 Z", "Neighbor roof", fill="#463226",
       stroke=INK, strokeWidth=3.5, join="round")
d.shape("rectangle", "Neighbor wall", x=752, y=478, width=116, height=160,
        fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#52392A"}, {"offset": 1, "color": "#2E1E16"}]}},
        stroke=INK, strokeWidth=3.5)
d.shape("rectangle", "Neighbor door", x=796, y=520, width=44, height=118,
        radius=4, fill="#2C1D14", stroke=INK, strokeWidth=3)
d.shape("rectangle", "Neighbor porch post", x=752, y=478, width=10,
        height=160, fill="#3A281C", stroke=INK, strokeWidth=2)
d.shape("rectangle", "Neighbor window", x=760, y=500, width=26, height=30,
        radius=3, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#D8B878", "opacity": 0.5},
            {"offset": 1, "color": "#8A6838", "opacity": 0.3}]}},
        stroke=INK, strokeWidth=2)
# their doorbell, aimed back at you — one glowing pinprick
d.shape("ellipse", "Neighbor cam glow", x=758, y=540, width=32, height=32,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#9ED4E8", "opacity": 0.5},
            {"offset": 1, "color": "#9ED4E8", "opacity": 0}]}},
        stroke=NONE)
d.shape("ellipse", "Neighbor cam", x=768, y=550, width=12, height=12,
        fill=CYAN, stroke=INK, strokeWidth=2)
# the mesh: porch-to-porch sightline, and both feeding the portal
d.path("M774,556 C700,500 560,430 452,392", "Mesh sightline", fill=NONE,
       stroke=CYAN, strokeWidth=2, opacity=35, dash=[5, 6])
d.path("M774,552 C730,520 700,470 690,420", "Mesh to portal", fill=NONE,
       stroke=CYAN, strokeWidth=2, opacity=28, dash=[5, 6])

# --- the request portal: the key is in their window, not your hand -----------------
d.shape("ellipse", "Portal glow", x=580, y=250, width=270, height=210,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#8FBCD4", "opacity": 0.18},
            {"offset": 1, "color": "#8FBCD4", "opacity": 0}]}},
        stroke=NONE)
d.shape("rectangle", "Portal window", x=586, y=272, width=236, height=170,
        radius=12, fill=PORTAL, stroke="#5C7A8C", strokeWidth=3.5)
d.shape("rectangle", "Portal titlebar", x=586, y=272, width=236, height=34,
        radius=12, fill="#22333E", stroke=NONE, opacity=95)
for i, dx in enumerate([604, 624, 644]):
    d.shape("ellipse", f"Window dot {i+1}", x=dx, y=282, width=12,
            height=12, fill="#5C7A8C", stroke=NONE, opacity=80)
r = d.text("REQUEST PORTAL", "Portal title", x=716, y=297, size=15,
           font="Virelai Sans", color="#9EBCCB", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "portal title tracking", ids=[r["id"]],
          tracking=140)
# shield of the requesting agency
d.path("M632,332 L632,368 C632,392 654,404 666,410 C678,404 700,392 700,368 "
       "L700,332 C688,326 676,322 666,322 C656,322 644,326 632,332 Z",
       "Agency shield", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#7E9EB0"}, {"offset": 1, "color": "#3A5464"}]}},
       stroke=INK, strokeWidth=3)
d.path("M654,366 L662,376 L680,352", "Shield check", fill=NONE,
       stroke="#E4F0F6", strokeWidth=4, cap="round", join="round")
# the house key, held inside the portal glass
d.shape("ellipse", "Key bow", x=728, y=346, width=34, height=34,
        fill=NONE, stroke="#E8C88A", strokeWidth=6)
d.path("M758,362 L798,362 M784,362 L784,376 M796,362 L796,374", "Key shaft",
       fill=NONE, stroke="#E8C88A", strokeWidth=6, cap="round")
# glass sheen over the pane — you can look, not touch
d.path("M600,320 L700,300 M608,380 L760,316", "Glass sheen", fill=NONE,
       stroke="#D8ECF4", strokeWidth=6, opacity=12, cap="round")

# --- Rita: the doorbell that watches its own porch ---------------------------------
d.shape("ellipse", "Doorbell shadow", x=368, y=560, width=150, height=20,
        fill="#080604", opacity=45, stroke=NONE)
# housing
d.shape("rectangle", "Doorbell", x=346, y=270, width=112, height=290,
        radius=26, fill=BODY, stroke=INK, strokeWidth=5)
d.shape("rectangle", "Faceplate", x=358, y=282, width=88, height=266,
        radius=18, fill={"gradient": {"kind": "linear", "stops": [
            {"offset": 0, "color": "#23272D"}, {"offset": 1, "color": "#14171B"}]}},
        stroke="#0E1013", strokeWidth=2)
# the eye: concentric lens, slightly lidded, red REC beside it
d.shape("ellipse", "Lens glow", x=360, y=296, width=84, height=84,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#9ED4E8", "opacity": 0.3},
            {"offset": 1, "color": "#9ED4E8", "opacity": 0}]}},
        stroke=NONE)
d.shape("ellipse", "Lens outer", x=374, y=310, width=56, height=56,
        fill=NONE, stroke="#5C7A8C", strokeWidth=4)
d.shape("ellipse", "Lens iris", x=384, y=320, width=36, height=36,
        fill=LENS, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Lens pupil", x=396, y=332, width=12, height=12,
        fill="#10181E", stroke=NONE)
d.shape("ellipse", "Lens glint", x=390, y=324, width=8, height=8,
        fill="#FFFFFF", stroke=NONE, opacity=90)
d.path("M374,322 Q402,306 430,322", "Lid", fill=NONE, stroke="#14171B",
       strokeWidth=6, cap="round")
d.shape("ellipse", "REC dot", x=440, y=300, width=10, height=10,
        fill=RED, stroke=NONE, opacity=95)
r = d.text("REC", "REC label", x=428, y=312, size=11, font="Virelai Sans",
           color=RED, justify="center")
# field of view: the beam sweeps your own porch
d.path("M430,338 L826,470 L800,660 Z", "FOV beam",
       fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#9ED4E8", "opacity": 0.16},
           {"offset": 1, "color": "#9ED4E8", "opacity": 0.02}]}},
       stroke=NONE)
d.path("M430,338 L826,470 M430,338 L800,660", "FOV edges", fill=NONE,
       stroke=CYAN, strokeWidth=2, opacity=22, dash=[7, 8])
# button: the only part you're allowed to touch
d.shape("ellipse", "Button ring", x=382, y=470, width=40, height=40,
        fill=NONE, stroke="#E8C88A", strokeWidth=4)
d.shape("ellipse", "Button", x=392, y=480, width=20, height=20,
        fill={"gradient": {"kind": "radial", "stops": [
            {"offset": 0, "color": "#F4E2B8"}, {"offset": 1, "color": "#8A6234"}]}},
        stroke=INK, strokeWidth=2.5)
# speaker slots — it talks back
for i, sy in enumerate([528, 540, 552]):
    d.path(f"M376,{sy} L428,{sy}", f"Speaker {i+1}", fill=NONE,
           stroke="#0E1013", strokeWidth=4, cap="round")

# --- the monthly fee: a receipt curling off the housing -----------------------------
d.path("M470,470 L560,462 L566,540 L558,534 L550,542 L542,534 L534,542 "
       "L526,534 L518,542 L510,534 L502,542 L494,534 L486,542 L478,534 "
       "L472,540 Z",
       "Receipt", fill=PAPER, stroke=INK, strokeWidth=3, join="round")
d.path("M482,486 L546,480 M484,500 L548,494", "Receipt head", fill=NONE,
       stroke="#6E5844", strokeWidth=3, opacity=80, cap="round")
d.path("M486,516 L520,512 M530,512 L550,510", "Fee line", fill=NONE,
       stroke="#6E5844", strokeWidth=2.5, opacity=70, cap="round")
d.path("M488,528 L522,524 M534,524 L552,522", "Fee line 2", fill=NONE,
       stroke="#6E5844", strokeWidth=2.5, opacity=55, cap="round")
r = d.text("FEE / MO", "Receipt fee", x=516, y=506, size=12,
           font="Virelai Sans", color="#4A362A", justify="center")

# --- floor crescent, closed on the disc's own arc ----------------------------------
d.path("M206,756 Q500,824 794,756 A420,420 0 0 1 206,756 Z",
       "Floor band", fill={"gradient": {"kind": "linear", "stops": [
           {"offset": 0, "color": "#120C08", "opacity": 0},
           {"offset": 1, "color": "#0A0605", "opacity": 0.55}]}},
       stroke=NONE)

# --- name + key haiku line ----------------------------------------------------------
r = d.text("the monthly fee.", "Key line", x=500, y=898, size=23,
           font="Virelai Sans", color=SOFT, justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "key tracking", ids=[r["id"]], tracking=170)
d.text("RING RITA", "Name", x=500, y=948, size=58,
       font="Virelai Sans", color=PALE, justify="center")

d.finish("hai-0439-ring-rita-V1R00")
