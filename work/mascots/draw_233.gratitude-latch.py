#!/usr/bin/env python3
"""Gratitude Latch — mascot portrait V1R00.
A resolved support ticket, punched and pinned. In the transcript, the
user's 'thanks' is caught mid-word by a brass sentiment latch — lever
thrown, jaw shut, NON-RETURN printed on the part. Everything the user
said after minute two is filed below as post-resolution sentiment.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Gratitude Latch — Mascot Portrait", 1000, 1000)

INK = "#332820"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#241C18"}, {"offset": 1, "color": "#0E0A08"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#6E5548"}, {"offset": 0.7, "color": "#463730"},
    {"offset": 1, "color": "#1E1613"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#4C3B32"}, {"offset": 1, "color": "#1C1410"}]}}
CARD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#F4EDDA"}, {"offset": 1, "color": "#D9CCA9"}]}}
BUBBLE = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#DEE8D8"}, {"offset": 1, "color": "#BCCBB2"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#E4C273"}, {"offset": 0.55, "color": "#B08A42"},
    {"offset": 1, "color": "#7A5A26"}]}}
BRASS_DARK = "#6E5224"
GREEN = "#3E9E64"
RED_PIN = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E88A72"}, {"offset": 1, "color": "#9E3E2E"}]}}

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#9A7A5E", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E8D6BC", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(196,240,8),(798,236,7),(162,524,9),(832,548,8),
                               (250,762,7),(750,746,9),(136,394,6),(862,396,7),
                               (396,114,7),(610,112,8),(336,820,6),(664,816,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#5A4538", opacity=45, stroke=NONE)

# --- floor ---------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0E0A06",
       strokeWidth=4, opacity=70)

# --- the ticket -------------------------------------------------------------------
d.shape("ellipse", "Ticket shadow", x=230, y=716, width=540, height=30,
        fill="#060404", opacity=50, stroke=NONE)
d.shape("rectangle", "Ticket", x=255, y=230, width=490, height=480,
        fill=CARD, stroke=INK, strokeWidth=5, radius=16)
# punch holes along the top edge
for i in range(15):
    d.shape("ellipse", f"Punch {i+1}", x=283 + i * 30, y=244, width=10, height=10,
            fill="#3E3228", opacity=35, stroke=NONE)
# pin holding it to the board
d.shape("ellipse", "Pin", x=486, y=222, width=28, height=28,
        fill=RED_PIN, stroke=INK, strokeWidth=3)
d.shape("ellipse", "Pin shine", x=492, y=228, width=8, height=8,
        fill="#F8D8C8", opacity=85, stroke=NONE)
d.path("M500,250 L500,262", "Pin point", fill=NONE, stroke=INK,
       strokeWidth=4, cap="round")

# header: labels left, certified-resolved chip right
d.text("TICKET", "Ticket label", x=285, y=292, size=15, font="Virelai Sans",
       color="#6A5A46")
# digits go to Source Sans 3 — Virelai Sans has none
d.text("NO. 4471", "Ticket number", x=285, y=316, size=16,
       font="Source Sans 3", color="#8A7A60")
d.shape("rectangle", "Status chip", x=592, y=268, width=130, height=32,
        fill=GREEN, stroke=INK, strokeWidth=3, radius=16, opacity=85)
d.text("RESOLVED", "Status chip text", x=657, y=289, size=14,
       font="Virelai Sans", color="#F0F4E8", justify="center")
d.path("M255,338 L745,338", "Header rule", fill=NONE, stroke=INK,
       strokeWidth=3, opacity=45)

# transcript: agent rows left, user rows right, all squiggle
d.shape("ellipse", "Agent avatar", x=282, y=356, width=18, height=18,
        fill="#8A7A60", stroke=NONE)
d.shape("rectangle", "Agent line 1", x=310, y=360, width=190, height=11,
        fill="#9A8C70", stroke=NONE, radius=5, opacity=85)
d.shape("rectangle", "Agent line 2", x=310, y=386, width=148, height=11,
        fill="#9A8C70", stroke=NONE, radius=5, opacity=70)
d.shape("rectangle", "User line 1", x=556, y=360, width=156, height=11,
        fill="#7E9A7A", stroke=NONE, radius=5, opacity=75)
d.shape("rectangle", "User line 2", x=556, y=386, width=134, height=11,
        fill="#7E9A7A", stroke=NONE, radius=5, opacity=75)

# engineering-diagram enclosure around the latch zone
d.shape("rectangle", "Latch enclosure", x=386, y=396, width=320, height=240,
        fill=NONE, stroke="#8A7A5E", strokeWidth=2, opacity=45)
d.text("SENTIMENT LATCH", "Enclosure label", x=400, y=426, size=12,
       font="Virelai Sans", color="#8A7A5E")

# the user's bubble with 'thanks' inside — drawn before the clamp
d.shape("rectangle", "User bubble", x=410, y=496, width=260, height=116,
        fill=BUBBLE, stroke="#7E9A7A", strokeWidth=3, radius=12)
d.path("M432,612 L424,632 L456,612 Z", "Bubble tail", fill="#BCCBB2",
       stroke="#7E9A7A", strokeWidth=3, join="round")
d.text("thanks", "The word", x=540, y=570, size=46, font="Source Sans 3",
       color="#3E4A3A", justify="center")

# --- the latch: two jaws, side brackets, thrown lever — clamped shut -------------
# jaws bite the word's edges, top and bottom; the word stays legible between
d.shape("rectangle", "Jaw top", x=430, y=520, width=220, height=22,
        fill=BRASS, stroke=INK, strokeWidth=4, radius=8)
d.shape("rectangle", "Jaw bottom", x=430, y=582, width=220, height=20,
        fill=BRASS, stroke=INK, strokeWidth=4, radius=8)
# NON-RETURN, printed on the part — it was specified
d.text("NON-RETURN", "Part marking", x=540, y=535, size=11,
       font="Virelai Sans", color="#4A3418", justify="center")
# side brackets tie the jaws into a clamp frame
d.shape("rectangle", "Bracket L", x=412, y=516, width=28, height=90,
        fill=BRASS, stroke=INK, strokeWidth=4, radius=8)
d.shape("rectangle", "Bracket R", x=640, y=516, width=28, height=90,
        fill=BRASS, stroke=INK, strokeWidth=4, radius=8)
d.shape("ellipse", "Bracket rivet L", x=420, y=580, width=12, height=12,
        fill="#E4C273", stroke=INK, strokeWidth=3)
d.shape("ellipse", "Bracket rivet R", x=648, y=580, width=12, height=12,
        fill="#E4C273", stroke=INK, strokeWidth=3)
# pivot on the left bracket, lever thrown up-right
d.shape("ellipse", "Pivot", x=414, y=546, width=28, height=28,
        fill=BRASS, stroke=INK, strokeWidth=4)
d.path("M434,552 L580,472", "Lever arm", fill=NONE, stroke=BRASS_DARK,
       strokeWidth=15, cap="round")
d.shape("ellipse", "Lever knob", x=566, y=456, width=30, height=30,
        fill="#6A4434", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Knob shine", x=572, y=462, width=9, height=9,
        fill="#C89A80", opacity=80, stroke=NONE)

# --- post-resolution sentiment -----------------------------------------------------
d.shape("rectangle", "Post line 1", x=310, y=634, width=180, height=11,
        fill="#9A8C70", stroke=NONE, radius=5, opacity=32)
d.shape("rectangle", "Post line 2", x=310, y=658, width=126, height=11,
        fill="#9A8C70", stroke=NONE, radius=5, opacity=32)
d.text("FILED AS POST-RESOLUTION SENTIMENT", "Filed note", x=310, y=692,
       size=12, font="Virelai Sans", color="#8A7A5E")

# certification stamp, bottom right — flat, official, green
d.shape("rectangle", "Stamp outer", x=536, y=622, width=196, height=58,
        fill=NONE, stroke=GREEN, strokeWidth=5, radius=8, opacity=85)
d.shape("rectangle", "Stamp inner", x=544, y=630, width=180, height=42,
        fill=NONE, stroke=GREEN, strokeWidth=2, radius=5, opacity=60)
d.text("RESOLVED", "Stamp text", x=650, y=658, size=18, font="Virelai Sans",
       color=GREEN, justify="center")
d.path("M560,648 L570,658 L586,638", "Stamp check", fill=NONE,
       stroke=GREEN, strokeWidth=5, cap="round", join="round", opacity=85)

# --- captions ---------------------------------------------------------------------------
d.text("GRATITUDE LATCH", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#F0E4CC", justify="center")
r = d.text("THE USER EXPRESSED GRATITUDE", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#C4A888", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("233.gratitude-latch-V1R00")
