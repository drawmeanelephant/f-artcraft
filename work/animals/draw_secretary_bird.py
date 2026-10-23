#!/usr/bin/env python3
"""Secretary bird — field-guide plate V1R00. Head/bust portrait, profile facing
left: grey plumage, black-tipped crest quills fanning back like pens tucked
behind an ear, orange bare-skin face mask, long upswept lashes, hooked beak.
Parchment/savanna palette — dignified office-worker energy.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Secretary Bird — Field Plate", 1000, 1000)

INK = "#34363A"
CX, CY = 500, 460          # plate disc centre (r=420)
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#33302A"}, {"offset": 1, "color": "#14130F"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F4ECD8"}, {"offset": 0.7, "color": "#DDCDA6"},
    {"offset": 1, "color": "#B49D6E"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#F1F1EE"}, {"offset": 0.7, "color": "#CFD0CC"},
    {"offset": 1, "color": "#A3A5A2"}]}}
BODY_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4E5E1"}, {"offset": 0.65, "color": "#BDBFBB"},
    {"offset": 1, "color": "#8F928F"}]}}
WING_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#9A9D9B"}, {"offset": 1, "color": "#5F6263"}]}}
MASK_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FFB866"}, {"offset": 0.6, "color": "#F07C30"},
    {"offset": 1, "color": "#C9501C"}]}}
BEAK_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3E4046"}, {"offset": 0.45, "color": "#7E848C"},
    {"offset": 1, "color": "#B6BCC2"}]}}
QUILL_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#55575C"}, {"offset": 1, "color": "#16171A"}]}}

def disc_x(y, side, r=416):
    """x where the horizontal line y meets a circle concentric with the plate."""
    return CX + side*math.sqrt(r*r - (y - CY)**2)

# --- backdrop + plate ---------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8E7A52", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FAF4E4", strokeWidth=3, opacity=60)
d.shape("ellipse", "Patina 1", x=160, y=180, width=240, height=140, fill="#C9B88E", opacity=24, stroke=NONE)
d.shape("ellipse", "Patina 2", x=600, y=600, width=250, height=140, fill="#C9B88E", opacity=20, stroke=NONE)
# low sun behind the head
d.shape("ellipse", "Sun glow", x=430, y=170, width=300, height=300, fill="#FFF6DC", opacity=35, stroke=NONE)
# faint acacia on the left horizon (all vertices well inside the disc)
d.path("M236,668 C232,640 236,612 244,592", "Acacia trunk", fill=NONE,
       stroke="#8E7A52", strokeWidth=7, opacity=30, cap="round")
d.path("M180,596 C196,570 236,560 262,566 C294,558 326,572 334,594 "
       "C306,604 214,606 180,596 Z", "Acacia canopy", fill="#8E7A52", opacity=24, stroke=NONE)
# savanna grass band — lower edge rides the plate's own arc
gy0, gy1 = 668, 712
d.path(f"M{disc_x(gy0, -1, 420):.1f},{gy0} C300,650 420,672 520,660 C640,646 760,664 "
       f"{disc_x(gy0, 1, 420):.1f},{gy0} A420,420 0 0 1 {disc_x(gy0, -1, 420):.1f},{gy0} Z",
       "Grass far", fill="#C7AF7A", opacity=40, stroke=NONE)
d.path(f"M{disc_x(gy1, -1, 420):.1f},{gy1} C320,694 450,716 580,702 C690,690 770,702 "
       f"{disc_x(gy1, 1, 420):.1f},{gy1} A420,420 0 0 1 {disc_x(gy1, -1, 420):.1f},{gy1} Z",
       "Grass near", fill="#B49D6E", opacity=40, stroke=NONE)
for i, (x, y) in enumerate([(170, 640), (210, 660), (262, 652), (742, 646), (790, 660), (830, 650)]):
    d.path(f"M{x},{y+28} C{x-2},{y+14} {x+4},{y+6} {x+8},{y}", f"Grass blade {i+1}",
           fill=NONE, stroke="#9C865A", strokeWidth=4, opacity=45, cap="round")
for i, (x, y, w) in enumerate([(200,300,8),(780,250,7),(150,470,9),(850,470,8),(260,200,7),
                               (720,190,8),(400,120,7),(600,115,7)]):
    d.shape("ellipse", f"Plate fleck {i+1}", x=x, y=y, width=w, height=w, fill="#9C865A", opacity=35, stroke=NONE)

# --- crest quills (behind the head) --------------------------------------------
def quill(base, ang_deg, length, width, label, max_r=372):
    a = math.radians(ang_deg)
    ux, uy = math.cos(a), math.sin(a)
    # shorten so the tip stays inside the plate's inner ring
    while math.hypot(base[0] + ux*length - CX, base[1] + uy*length - CY) > max_r:
        length -= 4
    nx, ny = -uy, ux
    bx, by = base
    tx, ty = bx + ux*length, by + uy*length
    # grey shaft
    sx, sy = bx + ux*length*0.5, by + uy*length*0.5
    d.path(f"M{bx:.1f},{by:.1f} L{sx:.1f},{sy:.1f}", f"{label} shaft",
           fill=NONE, stroke="#6E7074", strokeWidth=5, cap="round")
    # black spatulate vane
    v0 = 0.42
    p0 = (bx + ux*length*v0, by + uy*length*v0)
    w = width / 2
    m = (bx + ux*length*0.78, by + uy*length*0.78)
    dd = (f"M{p0[0]:.1f},{p0[1]:.1f} "
          f"Q{m[0] + nx*w*1.3:.1f},{m[1] + ny*w*1.3:.1f} {tx:.1f},{ty:.1f} "
          f"Q{m[0] - nx*w*1.3:.1f},{m[1] - ny*w*1.3:.1f} {p0[0]:.1f},{p0[1]:.1f} Z")
    d.path(dd, f"{label} vane", fill=QUILL_GRAD, stroke=INK, strokeWidth=3)
    # rachis + sheen down the vane
    d.path(f"M{p0[0]:.1f},{p0[1]:.1f} L{tx - ux*6:.1f},{ty - uy*6:.1f}", f"{label} rachis",
           fill=NONE, stroke="#8A8D92", strokeWidth=2, opacity=55, cap="round")
    d.path(f"M{m[0] + nx*w*0.35 - ux*20:.1f},{m[1] + ny*w*0.35 - uy*20:.1f} "
           f"L{m[0] + nx*w*0.35 + ux*14:.1f},{m[1] + ny*w*0.35 + uy*14:.1f}",
           f"{label} sheen", fill=NONE, stroke="#C9CDD6", strokeWidth=3, opacity=35, cap="round")

# a loose, uneven fan: back row first, then the longer front row over it
for i, (base, ang, L, W) in enumerate([
        ((616, 300), -40, 200, 22), ((640, 330), -8, 190, 22), ((640, 380), 26, 170, 20)]):
    quill(base, ang, L, W, f"Quill back {i+1}")
for i, (base, ang, L, W) in enumerate([
        ((604, 290), -58, 210, 26), ((628, 306), -27, 262, 30), ((644, 340), -14, 240, 28),
        ((648, 360), 6, 268, 30), ((642, 392), 16, 220, 26), ((628, 412), 40, 172, 22)]):
    quill(base, ang, L, W, f"Quill {i+1}")

# --- folded wing on the far shoulder (behind body) ------------------------------
wy0, wy1 = 690, 846
d.path(f"M630,560 C700,568 772,620 {disc_x(wy0, 1):.1f},{wy0} "
       f"A416,416 0 0 1 {disc_x(wy1, 1):.1f},{wy1} C640,770 600,660 630,560 Z",
       "Wing", fill=WING_GRAD, stroke=INK, strokeWidth=6)
# black flight feathers: band closes on the same arc as the wing
d.path(f"M650,724 C700,712 760,716 {disc_x(742, 1):.1f},742 "
       f"A416,416 0 0 1 {disc_x(wy1, 1):.1f},{wy1} C650,808 642,764 650,724 Z",
       "Primaries", fill=QUILL_GRAD, stroke=NONE, opacity=92)
for i, (x0, y0, x1, y1) in enumerate([(700,722,744,800), (676,730,708,822), (660,742,680,834)]):
    d.path(f"M{x0},{y0} Q{(x0+x1)/2+8},{(y0+y1)/2} {x1},{y1}", f"Primary edge {i+1}",
           fill=NONE, stroke="#8A8D92", strokeWidth=3, opacity=45, cap="round")
d.path("M640,600 C690,612 740,650 772,690", "Covert sheen", fill=NONE,
       stroke="#D6D9D6", strokeWidth=6, opacity=35, cap="round")

# --- neck + breast bust: closes on the plate's own arc --------------------------
# narrow neck flaring into the breast; the bottom rides the disc arc, and the
# right edge tucks under the wing so the wing's black band stays in front
by0, by1 = 800, 784
d.path(f"M476,430 L612,392 C632,470 640,540 650,600 C658,660 670,740 {disc_x(by0, 1):.1f},{by0} "
       f"A416,416 0 0 1 {disc_x(by1, -1):.1f},{by1} "
       f"C300,736 384,690 420,630 C446,584 458,520 476,430 Z",
       "Neck and breast", fill=BODY_GRAD, stroke=INK, strokeWidth=7)
# soft neck shading + feather chevrons
d.path("M600,470 C610,540 618,600 630,660", "Neck shade", fill=NONE,
       stroke="#80837F", strokeWidth=22, opacity=20, cap="round")
d.path("M500,480 C492,540 480,600 440,660", "Neck light", fill=NONE,
       stroke="#FFFFFF", strokeWidth=26, opacity=16, cap="round")
for i, (x, y) in enumerate([(540,560),(580,620),(510,640),(600,700),(530,720),(450,720),
                            (580,790),(500,800),(410,790),(330,790)]):
    d.path(f"M{x-22},{y-6} Q{x},{y+8} {x+22},{y-6}", f"Breast chevron {i+1}",
           fill=NONE, stroke="#8C8F8B", strokeWidth=4, opacity=45, cap="round")

# --- head (profile facing left) --------------------------------------------------
d.path("M468,332 C480,282 528,256 580,262 C640,270 672,320 670,376 "
       "C668,432 630,466 580,472 C530,476 490,462 470,442 C454,420 454,362 468,332 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
# darker crown + nape feathering
d.path("M490,298 C520,268 580,258 628,278", "Crown shade", fill=NONE,
       stroke="#8E918E", strokeWidth=16, opacity=35, cap="round")
for i, (x, y) in enumerate([(628,350),(640,390),(626,428),(600,450)]):
    d.path(f"M{x},{y} q14,6 26,2", f"Nape feather {i+1}", fill=NONE,
           stroke="#7E817E", strokeWidth=4, opacity=50, cap="round")
d.shape("ellipse", "Cheek light", x=540, y=420, width=90, height=36, fill="#FFFFFF", opacity=18, stroke=NONE)

# fluffy throat ruff hides the head/neck seam (stays inside the neck's outline)
pts = [(478, 446), (508, 452), (538, 456), (568, 452), (598, 442), (626, 428)]
dd = f"M{pts[0][0]},{pts[0][1]} "
for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
    dd += f"Q{(x0+x1)/2:.0f},{max(y0, y1) + 14} {x1},{y1} "
dd += "L630,486 C580,506 520,506 476,490 Z"
RUFF_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#D2D3CF"}, {"offset": 1, "color": "#B4B6B2"}]}}
d.path(dd, "Throat ruff", fill=RUFF_GRAD, stroke=NONE, opacity=92)
for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
    d.path(f"M{x0},{y0} Q{(x0+x1)/2:.0f},{max(y0, y1) + 14} {x1},{y1}", f"Ruff edge {x0}",
           fill=NONE, stroke="#8C8F8B", strokeWidth=3, opacity=55, cap="round")

# --- beak (drawn under the mask so the orange skin wraps its base) -----------------
# upper mandible: hooked tip
d.path("M490,350 C444,346 396,358 366,382 C352,394 348,414 356,430 "
       "C362,416 374,406 390,404 C424,400 456,404 490,414 Z",
       "Upper mandible", fill=BEAK_GRAD, stroke=INK, strokeWidth=5)
# lower mandible
d.path("M490,414 C452,410 416,410 392,414 C404,428 444,434 488,430 Z",
       "Lower mandible", fill=BEAK_GRAD, stroke=INK, strokeWidth=4)
d.path("M376,384 C400,368 432,360 460,360", "Beak sheen", fill=NONE,
       stroke="#E6EBF0", strokeWidth=4, opacity=45, cap="round")
d.path("M392,414 C424,414 456,414 484,416", "Gape", fill=NONE, stroke=INK, strokeWidth=4, cap="round")

# --- orange bare-skin face mask ---------------------------------------------------
d.path("M458,352 C474,320 530,306 572,320 C598,332 604,372 586,396 "
       "C562,420 508,426 470,418 C452,398 450,370 458,352 Z",
       "Face mask", fill=MASK_GRAD, stroke="#9E3E16", strokeWidth=3)
d.path("M484,330 C510,314 548,312 574,326", "Mask sheen", fill=NONE,
       stroke="#FFE2B8", strokeWidth=5, opacity=45, cap="round")
d.path("M480,404 C510,418 554,416 582,398", "Mask shade", fill=NONE,
       stroke="#A8401A", strokeWidth=6, opacity=35, cap="round")

# soft blue-grey cere just ahead of the mask + nostril
d.path("M458,356 C446,360 438,372 438,386 C438,398 446,406 458,410 C454,392 454,372 458,356 Z",
       "Cere", fill="#AEB8C2", stroke=NONE, opacity=70)
d.shape("ellipse", "Nostril", x=443, y=372, width=11, height=7, fill="#2C2E33", stroke=NONE)

# --- eye + famous lashes -----------------------------------------------------------
d.shape("ellipse", "Eye ring", x=506, y=340, width=56, height=46, fill="#FFD7A0", opacity=45, stroke=NONE)
d.shape("ellipse", "Iris", x=516, y=346, width=36, height=34, fill="#8A5A2A", stroke=NONE)
d.shape("ellipse", "Pupil", x=524, y=352, width=20, height=22, fill="#1C1510", stroke=NONE)
d.shape("ellipse", "Glint", x=528, y=355, width=7, height=7, fill="#FFFFFF", opacity=90, stroke=NONE)
d.path("M506,356 C516,340 546,336 566,350", "Upper lid", fill=NONE,
       stroke=INK, strokeWidth=7, cap="round")
d.path("M512,378 C524,386 548,386 560,376", "Lower lid", fill=NONE,
       stroke=INK, strokeWidth=3, opacity=55, cap="round")
# long lashes: tapered filled curls sweeping forward (beak-ward) and up
def lash(x, y, ang_deg, length, curl, label, w=4.5):
    a = math.radians(ang_deg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    tx, ty = x + ux*length, y + uy*length
    mx, my = x + ux*length*0.55 + nx*curl, y + uy*length*0.55 + ny*curl
    d.path(f"M{x - nx*w/2:.1f},{y - ny*w/2:.1f} Q{mx - nx*w*0.35:.1f},{my - ny*w*0.35:.1f} {tx:.1f},{ty:.1f} "
           f"Q{mx + nx*w*0.35:.1f},{my + ny*w*0.35:.1f} {x + nx*w/2:.1f},{y + ny*w/2:.1f} Z",
           label, fill="#1E1F23", stroke="#1E1F23", strokeWidth=1.5, cap="round")
for i, (x, y, ang, L, curl) in enumerate([
        (510,350,-150,26,-6), (518,344,-128,32,-8), (529,340,-108,36,-9),
        (541,339,-90,36,-9), (552,341,-74,32,-8), (561,346,-58,26,-6)]):
    lash(x, y, ang, L, curl, f"Lash {i+1}")
for i, (x, y, ang, L) in enumerate([(522,383,118,11), (536,386,98,12), (550,383,80,11)]):
    lash(x, y, ang, L, 0, f"Lower lash {i+1}", w=2.5)

# --- name --------------------------------------------------------------------------
d.text("SECRETARY BIRD", "Name", x=500, y=958, size=44, font="Virelai Sans",
       color="#ECE2CA", justify="center")

d.finish("secretary-bird-V1R00")
