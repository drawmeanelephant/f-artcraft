#!/usr/bin/env python3
"""Ledger Shadeledger — mascot portrait V1R00.
A spectral auditor holding an abacus among unbalanced ledgers, a quill
glowing faint in candlelight. 1000x1000. Gradients + translucent
shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE, rot_rect_path

d = Draw()
d.new_doc("Ledger Shadeledger — Mascot Portrait", 1000, 1000)

INK = "#241C26"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#151020"}, {"offset": 1, "color": "#0A0710"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#3E3550"}, {"offset": 0.7, "color": "#262038"},
    {"offset": 1, "color": "#120E1C"}]}}
GHOST = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D8E4EE"}, {"offset": 0.55, "color": "#A0B4CC"},
    {"offset": 1, "color": "#6E7E9E"}]}}
SPECTRAL = "#9FE8DC"
WOOD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A5636"}, {"offset": 1, "color": "#4A321E"}]}}
LEDGER_A = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#5E4A66"}, {"offset": 1, "color": "#3A2E44"}]}}
LEDGER_B = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#6E4A3A"}, {"offset": 1, "color": "#462C22"}]}}
LEDGER_C = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#44544E"}, {"offset": 1, "color": "#2A3833"}]}}
CANDLE = "#F0B860"

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000,
        fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#6A5E80", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#DCD4EC", strokeWidth=3, opacity=40)
for i, (x, y, w) in enumerate([(193,232,8),(800,234,7),(158,522,9),(835,542,8),
                               (245,768,7),(755,746,9),(132,392,6),(862,394,7),
                               (390,110,7),(614,112,8),(332,824,6),(666,818,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w,
            fill="#403850", opacity=45, stroke=NONE)

# tally scratches ghosted into the plate — the audit never ends
d.path("M700,190 l14,26 M716,190 l14,26 M732,190 l14,26 M748,190 l14,26 "
       "M696,206 L768,216", "Tally A", fill=NONE, stroke="#554A6E",
       strokeWidth=4, opacity=30, cap="round")
d.path("M196,300 l12,24 M210,300 l12,24 M224,300 l12,24 "
       "M192,314 L238,322", "Tally B", fill=NONE, stroke="#554A6E",
       strokeWidth=4, opacity=25, cap="round")

# --- floor ----------------------------------------------------------------------
d.shape("ellipse", "Floor", x=170, y=690, width=660, height=115,
        fill="#181226", opacity=85, stroke=NONE)
d.shape("ellipse", "Stack shadow", x=200, y=712, width=200, height=32,
        fill="#060410", opacity=55, stroke=NONE)
d.shape("ellipse", "Ghost shadow", x=400, y=724, width=220, height=30,
        fill="#060410", opacity=40, stroke=NONE)
d.shape("ellipse", "Right stack shadow", x=640, y=714, width=200, height=30,
        fill="#060410", opacity=55, stroke=NONE)

# --- left stack of ledgers, leaning into the unbalance -----------------------------
d.path(rot_rect_path(300, 706, 180, 36, -6), "Ledger L1",
       fill=LEDGER_C, stroke=INK, strokeWidth=5, join="round")
d.path(rot_rect_path(306, 670, 168, 34, -10), "Ledger L2",
       fill=LEDGER_A, stroke=INK, strokeWidth=5, join="round")
d.path(rot_rect_path(314, 634, 150, 32, -14), "Ledger L3",
       fill=LEDGER_B, stroke=INK, strokeWidth=5, join="round")
# page blocks at the fore-edges
d.path(rot_rect_path(376, 690, 20, 26, -6), "Pages L1",
       fill="#D8C9A4", stroke=INK, strokeWidth=3)
d.path(rot_rect_path(366, 652, 20, 24, -10), "Pages L2",
       fill="#D8C9A4", stroke=INK, strokeWidth=3)
d.path(rot_rect_path(356, 614, 18, 22, -14), "Pages L3",
       fill="#D8C9A4", stroke=INK, strokeWidth=3)
# the top one is mid-slide, off the pile entirely
d.path(rot_rect_path(292, 566, 140, 30, -22), "Ledger sliding",
       fill=LEDGER_A, stroke=INK, strokeWidth=5, join="round")
d.path(rot_rect_path(356, 542, 18, 22, -22), "Pages sliding",
       fill="#D8C9A4", stroke=INK, strokeWidth=3)
# loose receipts drifting off the lean
for i, (x, y, deg) in enumerate([(390, 480, 18), (250, 440, -14), (340, 390, 8)]):
    d.path(rot_rect_path(x, y, 44, 30, deg), f"Receipt {i+1}",
           fill="#D8C9A4", opacity=90, stroke=INK, strokeWidth=2)
d.path("M378,474 L402,478 M248,434 L272,430", "Receipt lines", fill=NONE,
       stroke="#8A744E", strokeWidth=2, opacity=70)

# --- right stack: steadier, carrying the candle --------------------------------------
d.path(rot_rect_path(726, 700, 170, 36, 2), "Ledger R1",
       fill=LEDGER_B, stroke=INK, strokeWidth=5, join="round")
d.path(rot_rect_path(722, 664, 158, 34, -3), "Ledger R2",
       fill=LEDGER_C, stroke=INK, strokeWidth=5, join="round")
d.path(rot_rect_path(700, 634, 18, 24, 2), "Pages R1",
       fill="#D8C9A4", stroke=INK, strokeWidth=3)
d.path(rot_rect_path(690, 598, 18, 24, -3), "Pages R2",
       fill="#D8C9A4", stroke=INK, strokeWidth=3)
# open ledger on top, pages breathing
d.path("M648,606 C672,592 700,592 712,602 C724,592 752,592 776,606 "
       "L776,634 C752,622 724,622 712,630 C700,622 672,622 648,634 Z",
       "Ledger open", fill="#D8C9A4", stroke=INK, strokeWidth=4,
       join="round")
d.path("M712,602 L712,630", "Open spine", fill=NONE, stroke=INK, strokeWidth=3)
for i, y in enumerate((610, 620)):
    d.path(f"M656,{y} C672,{y-5} 692,{y-5} 704,{y}", f"Open line L{i+1}",
           fill=NONE, stroke="#8A744E", strokeWidth=2, opacity=75)
    d.path(f"M720,{y} C732,{y-5} 752,{y-5} 768,{y}", f"Open line R{i+1}",
           fill=NONE, stroke="#8A744E", strokeWidth=2, opacity=75)
# the quill, lying across the open page, glowing faint in the candlelight
d.path("M652,632 C680,614 724,596 766,586 C748,604 716,622 686,636 "
       "C672,640 660,638 652,632 Z", "Quill", fill=SPECTRAL, opacity=70,
       stroke=INK, strokeWidth=3, join="round")
d.path("M660,630 L758,590", "Quill shaft", fill=NONE, stroke="#4E8A80",
       strokeWidth=3, opacity=80)
d.shape("ellipse", "Quill glow", x=640, y=576, width=140, height=70,
        fill=SPECTRAL, opacity=12, stroke=NONE)
# candle standing on the left page corner
d.shape("ellipse", "Candle glow wide", x=600, y=480, width=150, height=140,
        fill=CANDLE, opacity=10, stroke=NONE)
d.shape("ellipse", "Candle glow tight", x=628, y=505, width=60, height=70,
        fill=CANDLE, opacity=18, stroke=NONE)
d.shape("rectangle", "Candle", x=648, y=542, width=20, height=52,
        fill="#E4D6B4", stroke=INK, strokeWidth=3, radius=4)
d.path("M658,536 C654,526 656,516 660,508 C664,516 664,526 658,536 Z",
       "Candle flame", fill=CANDLE, stroke=NONE, opacity=95)
d.path("M658,530 C656,524 657,519 659,515 C661,519 661,524 658,530 Z",
       "Flame core", fill="#F8E2A8", stroke=NONE)
# wax drip
d.path("M650,556 C648,564 650,570 648,576", "Wax drip", fill=NONE,
       stroke="#E4D6B4", strokeWidth=4, cap="round", opacity=80)

# --- Ledger Shadeledger: the spectral auditor ----------------------------------------
# wispy tail first (behind the torso hem)
d.path("M470,640 C456,690 460,730 484,762 C478,730 484,700 494,676 "
       "C506,700 508,730 502,758 C522,732 528,692 522,648 Z",
       "Tail wisps", fill="#7E8EAC", opacity=75, stroke=NONE)
# body: translucent shroud, shoulders to vanishing hem
d.path("M496,320 C556,320 590,372 594,446 C598,520 584,600 560,660 "
       "C540,690 452,690 432,660 C408,600 394,520 398,446 "
       "C402,372 436,320 496,320 Z",
       "Ghost body", fill=GHOST, stroke=INK, strokeWidth=6, opacity=88)
# spectral inner glow — the audit light
d.shape("ellipse", "Spectral core", x=462, y=440, width=70, height=100,
        fill=SPECTRAL, opacity=22, stroke=NONE)
# hood/brow ridge shading
d.path("M430,360 C456,334 536,334 562,360 C536,352 456,352 430,360 Z",
       "Hood shade", fill="#7E8EAC", opacity=60, stroke=NONE)
# hollow eyes — coldly resolute
d.shape("ellipse", "Eye L", x=458, y=384, width=26, height=34,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye R", x=508, y=384, width=26, height=34,
        fill=INK, stroke=NONE)
d.shape("ellipse", "Eye ember L", x=464, y=398, width=10, height=12,
        fill=SPECTRAL, opacity=90, stroke=NONE)
d.shape("ellipse", "Eye ember R", x=514, y=398, width=10, height=12,
        fill=SPECTRAL, opacity=90, stroke=NONE)
# flat mouth — nothing resolves
d.path("M478,448 L514,448", "Mouth", fill=NONE, stroke=INK,
       strokeWidth=5, cap="round")
# arms: left steadies the abacus, right counts the air
d.path("M424,470 C400,492 392,516 398,540", "Arm L", fill=NONE,
       stroke="#A0B4CC", strokeWidth=14, cap="round", opacity=90)
d.shape("ellipse", "Hand L", x=392, y=534, width=20, height=17,
        fill="#A0B4CC", stroke=INK, strokeWidth=3, opacity=95)
d.path("M570,470 C590,500 592,526 586,548", "Arm R", fill=NONE,
       stroke="#A0B4CC", strokeWidth=14, cap="round", opacity=90)
d.shape("ellipse", "Hand R", x=576, y=540, width=20, height=17,
        fill="#A0B4CC", stroke=INK, strokeWidth=3, opacity=95)
# --- the abacus she listens with -----------------------------------------------------
d.path(rot_rect_path(490, 570, 168, 118, -3), "Abacus frame",
       fill=NONE, stroke="#8A6A44", strokeWidth=10, join="round")
for i, off in enumerate((-38, -13, 12, 37)):
    # rods run across the tilted frame (rotate ~-3deg)
    d.path(rot_rect_path(490, 570+off, 150, 5, -3), f"Rod {i+1}",
           fill="#8A6A44", stroke=NONE)
# beads: unbalanced groups — 3 left on top rod, 5 right on the next, etc.
for i, (off, groups) in enumerate([(-38, ((-52, 3), (30, 2))),
                                   (-13, ((-20, 4), (44, 2))),
                                   (12, ((-60, 2), (10, 5))),
                                   (37, ((-30, 3), (36, 3)))]):
    for base, n in groups:
        for k in range(n):
            bx = 490 + (base + k*13)
            by = 570 + off - (bx - 490) * 0.052
            d.shape("ellipse", f"Bead {i+1}-{base}-{k}", x=bx-6, y=by-8,
                    width=12, height=15,
                    fill="#C05A48" if (i + k) % 3 == 0 else "#B0A4C8",
                    stroke=INK, strokeWidth=2)
# one bead floating mid-rod — the discrepancy she is listening for
d.shape("ellipse", "Lost bead", x=486, y=520, width=12, height=15,
        fill=SPECTRAL, opacity=90, stroke=INK, strokeWidth=2)
d.shape("ellipse", "Bead aura", x=476, y=508, width=32, height=36,
        fill=SPECTRAL, opacity=25, stroke=NONE)

# --- captions ---------------------------------------------------------------------------
d.text("LEDGER SHADELEDGER", "Name", x=500, y=930, size=54,
       font="Virelai Sans", color="#E0D8F0", justify="center")
r = d.text("FISCAL SPECTER", "Role", x=500, y=968, size=23,
           font="Virelai Sans", color="#A294C0", justify="center")
if r and r.get("id"):
    d.cmd("text.setStyle", "role tracking", ids=[r["id"]], tracking=200)

d.finish("202.ledger-shadeledger-V1R00")
