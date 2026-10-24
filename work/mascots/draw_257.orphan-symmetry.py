#!/usr/bin/env python3
"""Orphan Symmetry — mascot portrait V1R00.
A small caretaker with a brass ruler seating the last orphaned icon into a
perfectly spaced grid of dead buttons and links that lead nowhere. Its ledger,
the one object not arranged, lies open on the floor in the order things were lost.
1000x1000. Gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Orphan Symmetry — Mascot Portrait", 1000, 1000)

INK = "#342C30"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#0E1220"}, {"offset": 1, "color": "#070A12"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#465270"}, {"offset": 0.7, "color": "#2A3246"},
    {"offset": 1, "color": "#131A28"}]}}
FLOOR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#262E3E"}, {"offset": 1, "color": "#0F131C"}]}}
TILE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A445E"}, {"offset": 1, "color": "#222A3E"}]}}
HELD_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#57648A"}, {"offset": 1, "color": "#333D58"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#8AA8A2"}, {"offset": 0.7, "color": "#5E827C"},
    {"offset": 1, "color": "#3C5652"}]}}
BRASS = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8B468"}, {"offset": 1, "color": "#96702E"}]}}
LEDGER = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8CCB0"}, {"offset": 1, "color": "#B0A180"}]}}
ICON = "#9AA6B8"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#7A86A0", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#D0D8E4", strokeWidth=3, opacity=55)
for i, (x, y, w) in enumerate([(193,233,8),(801,230,7),(157,524,9),(837,544,8),
                               (247,766,7),(753,749,9),(133,393,6),(864,391,7),
                               (391,113,7),(613,110,8),(333,823,6),(665,821,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#3A4660", opacity=45, stroke=NONE)

# --- floor ----------------------------------------------------------------------
d.path("M156,700 L844,700 A420,420 0 0 1 156,700 Z", "Floor",
       fill=FLOOR_GRAD, stroke=NONE)
d.path("M156,700 L844,700", "Floor line", fill=NONE, stroke="#0B0F16",
       strokeWidth=4, opacity=70)

# --- the grid: 4 x 3 dead icons, one empty slot -------------------------------------
COLS = [288, 386, 484, 582]
ROWS = [208, 306, 404]
TS = 72
EMPTY = (0, 2)          # bottom-left slot, being filled

def tile(cx0, cy0, label, grad=TILE_GRAD, op=92):
    d.shape("rectangle", label, x=cx0, y=cy0, width=TS, height=TS,
            fill=grad, stroke=INK, strokeWidth=4, radius=10, opacity=op)
    d.shape("ellipse", f"{label} sheen", x=cx0+10, y=cy0+8, width=34,
            height=14, fill="#FFFFFF", opacity=10, stroke=NONE)

def orphan_x(cx0, cy0, label):
    # the little top-right X each ward wears: no parent
    x, y = cx0+TS-15, cy0+9
    d.path(f"M{x},{y} L{x+7},{y+7} M{x+7},{y} L{x},{y+7}", label,
           fill=NONE, stroke="#8A6A50", strokeWidth=2.5, cap="round",
           opacity=75)

def icon(kind, cx, cy, tag):
    S = ICON; W = 4
    if kind == "link":      # two chain links that no longer meet
        d.path(rot_rect_path(cx-9, cy+7, 24, 13, -40), f"{tag} link a",
               fill=NONE, stroke=S, strokeWidth=W)
        d.path(rot_rect_path(cx+9, cy-7, 24, 13, -40), f"{tag} link b",
               fill=NONE, stroke=S, strokeWidth=W)
        d.path(f"M{cx-5},{cy-3} l5,-4 M{cx+1},{cy+3} l5,-4",
               f"{tag} gap sparks", fill=NONE, stroke=S, strokeWidth=2.5,
               cap="round", opacity=70)
    elif kind == "wifi":    # arcs with a slash: signal to nowhere
        for r in (10, 18, 26):
            d.path(f"M{cx-r},{cy+8} A{r},{r} 0 0 1 {cx+r},{cy+8}",
                   f"{tag} arc {r}", fill=NONE, stroke=S, strokeWidth=W,
                   cap="round")
        d.path(f"M{cx-20},{cy-16} L{cx+20},{cy+24}", f"{tag} slash",
               fill=NONE, stroke="#8A6A50", strokeWidth=W, cap="round")
    elif kind == "gear":    # a gear with a tooth gone
        d.shape("ellipse", f"{tag} ring", x=cx-14, y=cy-14, width=28,
                height=28, fill=NONE, stroke=S, strokeWidth=W)
        for i in range(8):
            if i == 3:
                continue  # the missing tooth
            a = math.radians(i*45)
            x1, y1 = cx+16*math.cos(a), cy+16*math.sin(a)
            x2, y2 = cx+23*math.cos(a), cy+23*math.sin(a)
            d.path(f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}",
                   f"{tag} tooth {i}", fill=NONE, stroke=S, strokeWidth=W,
                   cap="round")
        a = math.radians(3*45)
        d.path(f"M{cx+19*math.cos(a)-3:.0f},{cy+19*math.sin(a)-3:.0f} l6,6",
               f"{tag} tooth gap", fill=NONE, stroke="#8A6A50",
               strokeWidth=2.5, cap="round", opacity=70)
    elif kind == "play":    # a play button nobody can press
        d.path(f"M{cx-9},{cy-13} L{cx+13},{cy} L{cx-9},{cy+13} Z",
               f"{tag} tri", fill=NONE, stroke=S, strokeWidth=W,
               join="round")
        d.path(f"M{cx-14},{cy-16} L{cx+6},{cy+14}", f"{tag} crack",
               fill=NONE, stroke=S, strokeWidth=2.5, cap="round", opacity=60)
    elif kind == "folder":  # a folder that lost its parent
        d.path(f"M{cx-18},{cy-6} L{cx-5},{cy-6} L{cx-1},{cy-12} "
               f"L{cx+18},{cy-12} L{cx+18},{cy+13} L{cx-18},{cy+13} Z",
               f"{tag} folder", fill=NONE, stroke=S, strokeWidth=W,
               join="round")
        d.path(f"M{cx+3},{cy-2} C{cx+8},{cy-4} {cx+10},{cy+2} {cx+4},{cy+5}",
               f"{tag} q", fill=NONE, stroke=S, strokeWidth=3, cap="round")
        d.shape("ellipse", f"{tag} qdot", x=cx+2, y=cy+8, width=4, height=4,
                fill=S, stroke=NONE)
    elif kind == "button":  # a dead OK button
        d.shape("rectangle", f"{tag} pill", x=cx-22, y=cy-10, width=44,
                height=20, fill="#2A3348", stroke=S, strokeWidth=3.5,
                radius=10)
        d.text("OK", f"{tag} label", x=cx, y=cy+5, size=13,
               font="Virelai Sans", color="#6E7A8C", justify="center")
    elif kind == "image":   # a placeholder that outlived its picture
        d.shape("rectangle", f"{tag} frame", x=cx-18, y=cy-15, width=36,
                height=30, fill=NONE, stroke=S, strokeWidth=W, radius=3)
        d.shape("ellipse", f"{tag} sun", x=cx-11, y=cy-8, width=7, height=7,
                fill=NONE, stroke=S, strokeWidth=2.5)
        d.path(f"M{cx-16},{cy+13} L{cx-5},{cy+1} L{cx+2},{cy+9} "
               f"L{cx+8},{cy+3} L{cx+16},{cy+13}", f"{tag} mountain",
               fill=NONE, stroke=S, strokeWidth=2.5, join="round")
    elif kind == "arrow":   # an arrow fired at the void
        d.path(f"M{cx-18},{cy} L{cx+6},{cy} M{cx},{cy-7} L{cx+8},{cy} "
               f"L{cx},{cy+7}", f"{tag} arrow", fill=NONE, stroke=S,
               strokeWidth=W, cap="round")
        for j in range(3):
            d.shape("ellipse", f"{tag} fade {j}", x=cx+14+j*8, y=cy-2,
                    width=4, height=4, fill=S, stroke=NONE,
                    opacity=55-j*15)
    elif kind == "heart":   # a hollow like
        d.path(f"M{cx},{cy+13} C{cx-17},{cy+3} {cx-15},{cy-12} {cx},{cy-3} "
               f"C{cx+15},{cy-12} {cx+17},{cy+3} {cx},{cy+13} Z",
               f"{tag} heart", fill=NONE, stroke=S, strokeWidth=W,
               join="round")
        d.path(f"M{cx-3},{cy-3} l4,6 l-5,5", f"{tag} crack", fill=NONE,
               stroke=S, strokeWidth=2, cap="round", opacity=60)
    elif kind == "chat":    # a reply that never sends
        d.shape("rectangle", f"{tag} bubble", x=cx-18, y=cy-13, width=36,
                height=24, fill=NONE, stroke=S, strokeWidth=W, radius=8)
        d.path(f"M{cx-10},{cy+11} L{cx-12},{cy+19} L{cx-3},{cy+11}",
               f"{tag} tail", fill=NONE, stroke=S, strokeWidth=3,
               join="round")
        for j in range(3):
            d.shape("ellipse", f"{tag} dot {j}", x=cx-11+j*10, y=cy-3,
                    width=5, height=5, fill=S, stroke=NONE, opacity=70)
    elif kind == "dl":      # a download with no tray to land in
        d.path(f"M{cx},{cy-15} L{cx},{cy+5} M{cx-8},{cy-2} L{cx},{cy+7} "
               f"L{cx+8},{cy-2}", f"{tag} arrow", fill=NONE, stroke=S,
               strokeWidth=W, cap="round")
        for j, (x0, x1) in enumerate([(cx-14, cx-6), (cx-4, cx+4),
                                      (cx+6, cx+14)]):
            d.path(f"M{x0},{cy+17} L{x1},{cy+17}", f"{tag} tray dash {j}",
                   fill=NONE, stroke=S, strokeWidth=3, cap="round",
                   opacity=45)
    elif kind == "bell":    # a notification silenced forever
        d.path(f"M{cx-13},{cy+6} C{cx-13},{cy-8} {cx-7},{cy-15} {cx},{cy-15} "
               f"C{cx+7},{cy-15} {cx+13},{cy-8} {cx+13},{cy+6} "
               f"L{cx+16},{cy+12} L{cx-16},{cy+12} Z",
               f"{tag} dome", fill=NONE, stroke=S, strokeWidth=W,
               join="round")
        d.shape("ellipse", f"{tag} clapper", x=cx-3, y=cy+15, width=6,
                height=6, fill=S, stroke=NONE)
        d.path(f"M{cx-19},{cy-17} L{cx+19},{cy+17}", f"{tag} slash",
               fill=NONE, stroke="#8A6A50", strokeWidth=W, cap="round")

KINDS = [["link", "wifi", "gear", "play"],
         ["folder", "button", "image", "arrow"],
         ["heart", "chat", "dl", "bell"]]
for r_i, ry in enumerate(ROWS):
    for c_i, cx0 in enumerate(COLS):
        if (c_i, r_i) == EMPTY:
            continue
        tile(cx0, ry, f"Tile r{r_i} c{c_i}")
        icon(KINDS[r_i][c_i], cx0+TS/2, ry+TS/2, f"icon{r_i}{c_i}")
        orphan_x(cx0, ry, f"orphan{r_i}{c_i}")

# the empty slot: dashed vacancy the caretaker is filling
ex, ey = COLS[EMPTY[0]], ROWS[EMPTY[1]]
for i in range(4):
    x0 = ex + 6 + i*16
    d.path(f"M{x0},{ey} L{min(x0+9, ex+TS-6)},{ey}", f"Slot top {i}",
           fill=NONE, stroke="#5E6A7E", strokeWidth=3, cap="round",
           opacity=60)
    d.path(f"M{x0},{ey+TS} L{min(x0+9, ex+TS-6)},{ey+TS}", f"Slot bot {i}",
           fill=NONE, stroke="#5E6A7E", strokeWidth=3, cap="round",
           opacity=60)
for i in range(4):
    y0 = ey + 6 + i*16
    d.path(f"M{ex},{y0} L{ex},{min(y0+9, ey+TS-6)}", f"Slot L {i}",
           fill=NONE, stroke="#5E6A7E", strokeWidth=3, cap="round",
           opacity=60)
    d.path(f"M{ex+TS},{y0} L{ex+TS},{min(y0+9, ey+TS-6)}", f"Slot R {i}",
           fill=NONE, stroke="#5E6A7E", strokeWidth=3, cap="round",
           opacity=60)
d.shape("ellipse", "Slot glow", x=ex+16, y=ey+16, width=40, height=40,
        fill="#8FA0C0", opacity=12, stroke=NONE)

# spacing ticks between columns — its wards are more precise than the attached
for i, gx in enumerate([374, 472, 570]):
    d.path(f"M{gx-5},180 L{gx+5},180 M{gx},175 L{gx},185",
           f"Measure tick {i+1}", fill=NONE, stroke="#C8A050",
           strokeWidth=2.5, cap="round", opacity=55)

# --- a dead link escaping the grid, into nowhere -------------------------------------
d.path("M670,340 C720,330 745,315 770,290", "Escape dash 1", fill=NONE,
       stroke="#6E7A8C", strokeWidth=3, cap="round", opacity=55)
d.path("M782,278 L800,264", "Escape dash 2", fill=NONE, stroke="#6E7A8C",
       strokeWidth=3, cap="round", opacity=35)
t = d.text("404", "Nowhere label", x=812, y=262, size=17,
           font="Source Sans 3", color="#6E7A8C", justify="left")
if t and t.get("id"):
    d.cmd("object.setProps", "nowhere fade", ids=[t["id"]], opacity=70)

# --- the ledger: open, asymmetric, in the order things were lost ----------------------
d.path(rot_rect_path(468, 668, 78, 40, -7), "Ledger", fill=LEDGER,
       stroke=INK, strokeWidth=3, opacity=95)
d.path(rot_rect_path(468, 668, 6, 40, -7), "Ledger spine", fill="#8A7A5C",
       stroke=INK, strokeWidth=2)
for i, (y0, w, sl) in enumerate([(655, 52, -3), (665, 38, 2),
                                 (675, 46, -1)]):
    d.path(f"M438,{y0} l{w},{sl}", f"Ledger row {i+1}", fill=NONE,
           stroke="#6E5E44", strokeWidth=2.5, cap="round", opacity=70)

# --- the mascot: a small precise caretaker --------------------------------------------
d.shape("ellipse", "Mascot shadow", x=250, y=688, width=160, height=18,
        fill="#080C12", opacity=50, stroke=NONE)
# brass ruler staff, tip on the floor — the edge every grid is checked against
d.shape("rectangle", "Ruler staff", x=252, y=452, width=14, height=238,
        fill=BRASS, stroke=INK, strokeWidth=3, radius=3)
for i in range(14):
    y0 = 460 + i*16
    tick = 8 if i % 2 else 12
    d.path(f"M252,{y0} L{252-tick},{y0}", f"Ruler tick {i+1}", fill=NONE,
           stroke=INK, strokeWidth=2, cap="round", opacity=70)
# body: a rounded slab, shaped like its own wards
d.shape("rectangle", "Body", x=288, y=520, width=96, height=150,
        fill=BODY_GRAD, stroke=INK, strokeWidth=6, radius=30)
d.shape("ellipse", "Body sheen", x=300, y=534, width=48, height=20,
        fill="#FFFFFF", opacity=18, stroke=NONE)
# feet
d.shape("ellipse", "Foot L", x=300, y=664, width=26, height=14,
        fill="#3C5652", stroke=INK, strokeWidth=4)
d.shape("ellipse", "Foot R", x=346, y=664, width=26, height=14,
        fill="#3C5652", stroke=INK, strokeWidth=4)
# face: calm, level gaze — a surveyor's patience
d.shape("ellipse", "Eye L", x=312, y=556, width=9, height=11, fill=INK,
        stroke=NONE)
d.shape("ellipse", "Eye R", x=348, y=556, width=9, height=11, fill=INK,
        stroke=NONE)
d.path("M320,590 L348,590", "Mouth", fill=NONE, stroke=INK, strokeWidth=4,
       cap="round")
d.shape("ellipse", "Blush L", x=298, y=574, width=16, height=8,
        fill="#B0788A", opacity=35, stroke=NONE)
d.shape("ellipse", "Blush R", x=356, y=574, width=16, height=8,
        fill="#B0788A", opacity=35, stroke=NONE)
# a little level vial worn as a brooch
d.shape("rectangle", "Level vial", x=322, y=610, width=28, height=10,
        fill="#C8A050", stroke=INK, strokeWidth=2.5, radius=5)
d.shape("ellipse", "Level bubble", x=333, y=612, width=6, height=6,
        fill="#3C5652", stroke=NONE)
# arms: left hand rests on the ruler, right hand lifts the tile home
d.path("M290,556 C274,552 264,548 258,540", "Arm L", fill=NONE, stroke=INK,
       strokeWidth=7, cap="round")
d.shape("ellipse", "Hand L", x=252, y=532, width=15, height=13,
        fill="#5E827C", stroke=INK, strokeWidth=3)
d.path("M384,540 C372,522 362,506 352,492", "Arm R", fill=NONE, stroke=INK,
       strokeWidth=7, cap="round")
# the tile being placed, tilted a degree off true — about to be corrected
d.path(rot_rect_path(330, 452, TS, TS, -12), "Held tile", fill=HELD_GRAD,
       stroke=INK, strokeWidth=4, opacity=95)
icon("dl", 330, 452, "held")
d.shape("ellipse", "Hand R", x=340, y=484, width=15, height=13,
        fill="#5E827C", stroke=INK, strokeWidth=3)
# motion ticks: almost seated
d.path("M366,398 C374,392 386,390 396,392", "Motion tick 1", fill=NONE,
       stroke="#C8A050", strokeWidth=3, cap="round", opacity=60)
d.path("M286,398 C280,392 272,390 264,392", "Motion tick 2", fill=NONE,
       stroke="#C8A050", strokeWidth=3, cap="round", opacity=45)

# --- captions ----------------------------------------------------------------------
d.text("ORPHAN SYMMETRY", "Name", x=500, y=930, size=56,
       font="Virelai Sans", color="#DCE4EE", justify="center")
r = d.text("COMPENSATORY RITUAL", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#96A4BC", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("257.orphan-symmetry-V1R00")
