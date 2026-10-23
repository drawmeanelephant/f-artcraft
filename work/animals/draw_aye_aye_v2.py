#!/usr/bin/env python3
"""Aye-aye — field-guide plate V2R00. A new interpretation of the V1R00 bust:
the full animal creeping down a moonlit branch, bushy tail raised behind,
amber eyes glowing straight at the viewer, the long skeletal middle finger
lifted mid-tap over the wood. Nocturnal palette carried over from V1.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = Draw()
d.new_doc("Aye-aye V2 — Field Plate", 1000, 1000)

INK = "#1D1410"
BG_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#1B1428"}, {"offset": 1, "color": "#08060E"}]}}
PLATE_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#E4E8F2"}, {"offset": 0.7, "color": "#B4BCCF"},
    {"offset": 1, "color": "#7E87A0"}]}}
FUR_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#463428"}, {"offset": 0.7, "color": "#2A1D15"},
    {"offset": 1, "color": "#170F0A"}]}}
TAIL_GRAD = {"gradient": {"kind": "linear", "angle": 60, "stops": [
    {"offset": 0, "color": "#3A2B20"}, {"offset": 1, "color": "#110B07"}]}}
HEAD_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#4A382B"}, {"offset": 0.7, "color": "#2C1F17"},
    {"offset": 1, "color": "#1A120C"}]}}
EAR_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3D2C20"}, {"offset": 1, "color": "#201510"}]}}
IRIS_GRAD = {"gradient": {"kind": "radial", "stops": [
    {"offset": 0, "color": "#FBD06A"}, {"offset": 0.6, "color": "#E89A2E"},
    {"offset": 1, "color": "#8A4E10"}]}}
HAND_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#3A2A1E"}, {"offset": 1, "color": "#211710"}]}}
BARK_GRAD = {"gradient": {"kind": "linear", "angle": 90, "stops": [
    {"offset": 0, "color": "#5E5048"}, {"offset": 1, "color": "#231B16"}]}}
LIMB_FAR = "#1A110C"

# --- branch geometry: top edge is a cubic; feet and fingers sit on it ---------------
B0, B1, B2, B3 = (140, 676), (400, 600), (700, 470), (918, 419)
def bez(t, p0=B0, p1=B1, p2=B2, p3=B3):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])
def top_y(x):
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if bez(mid)[0] < x: lo = mid
        else: hi = mid
    return bez(lo)[1]

# --- backdrop + stars + plate ----------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w, o) in enumerate([(55,90,7,60),(130,40,5,45),(60,300,6,50),(45,650,5,40),
                                  (920,60,7,55),(870,120,5,40),(955,320,6,50),(940,700,5,45),
                                  (70,860,6,45),(935,860,5,40)]):
    d.shape("ellipse", f"Star {i+1}", x=x, y=y, width=w, height=w, fill="#C9CEDE", opacity=o, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#4E5570", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#E9EDF5", strokeWidth=3, opacity=50)
d.shape("ellipse", "Crater 1", x=200, y=170, width=180, height=120, fill="#98A0B5", opacity=18, stroke=NONE)
d.shape("ellipse", "Crater 2", x=560, y=640, width=220, height=130, fill="#98A0B5", opacity=15, stroke=NONE)
d.shape("ellipse", "Crater 3", x=520, y=150, width=120, height=80, fill="#98A0B5", opacity=14, stroke=NONE)
d.shape("ellipse", "Crater 4", x=330, y=760, width=140, height=70, fill="#98A0B5", opacity=16, stroke=NONE)
for i, (x, y, w) in enumerate([(250,300,9),(160,450,8),(600,780,8),(430,110,8),(620,120,7),
                               (800,560,9),(700,740,7),(300,820,7)]):
    d.shape("ellipse", f"Moon fleck {i+1}", x=x, y=y, width=w, height=w, fill="#7E87A0", opacity=40, stroke=NONE)

# --- tail: a huge bushy plume raised behind, drawn first ---------------------------------
import math
T0, T1, T2, T3 = (640, 440), (690, 350), (760, 310), (720, 180)
def tail_pt(t):
    return bez(t, T0, T1, T2, T3)
def in_disc(x, y, margin=14):
    return math.hypot(x - 500, y - 460) <= 420 - margin
left, right = [], []
N = 22
for i in range(N + 1):
    t = i / N
    (x, y), (x2, y2) = tail_pt(t), tail_pt(min(t + 0.01, 1.0) if t < 1 else t - 0.01)
    tx_, ty_ = (x2 - x, y2 - y) if t < 1 else (x - x2, y - y2)
    ln = math.hypot(tx_, ty_) or 1
    nx, ny = -ty_ / ln, tx_ / ln
    w = 22 + 46 * math.sin(math.pi * min(t, 0.92) / 0.92 * 0.85)   # fattest two-thirds up
    tuft = 9 if i % 2 else -3                                        # scalloped fur edge
    left.append((x + nx * (w + tuft), y + ny * (w + tuft)))
    right.append((x - nx * (w + tuft * 0.8), y - ny * (w + tuft * 0.8)))
tip = tail_pt(1.0)
pts = left + [(tip[0] - 6, tip[1] - 30)] + right[::-1]
assert all(in_disc(x, y) for x, y in pts), "tail leaves the disc"
dd = f"M{pts[0][0]:.1f},{pts[0][1]:.1f} " + " ".join(
    f"Q{pts[k][0]:.1f},{pts[k][1]:.1f} {(pts[k][0]+pts[k+1][0])/2:.1f},{(pts[k][1]+pts[k+1][1])/2:.1f}"
    for k in range(1, len(pts) - 1)) + f" L{pts[-1][0]:.1f},{pts[-1][1]:.1f} Z"
d.path(dd, "Tail", fill=TAIL_GRAD, stroke=INK, strokeWidth=6)
# grizzled guard hairs inside the plume, following its spine
for i, t in enumerate([0.18, 0.3, 0.42, 0.54, 0.66, 0.78, 0.88]):
    (x, y) = tail_pt(t); (xa, ya) = tail_pt(t + 0.08)
    for j, off in enumerate([-24, 0, 24]):
        d.path(f"M{x+off*0.8:.0f},{y+off*0.3:.0f} L{xa+off*0.6:.0f},{ya+off*0.2:.0f}",
               f"Tail hair {i*3+j+1}", fill=NONE, stroke="#8C7A68", strokeWidth=3,
               opacity=38 if j != 1 else 50, cap="round")
d.path(f"M{tail_pt(0.25)[0]-30:.0f},{tail_pt(0.25)[1]:.0f} C{T1[0]-20},{T1[1]-40} {T2[0]-50},{T2[1]-40} {T3[0]-36},{T3[1]+10}",
       "Tail rim light", fill=NONE, stroke="#B98A4A", strokeWidth=5, opacity=20, cap="round")

# --- branch: both ends close on the disc's own arc ----------------------------------------
d.path(f"M{B0[0]},{B0[1]} C{B1[0]},{B1[1]} {B2[0]},{B2[1]} {B3[0]},{B3[1]} "
       "A420,420 0 0 1 918,501 C700,560 420,690 176,727 A420,420 0 0 1 140,676 Z",
       "Branch", fill=BARK_GRAD, stroke=INK, strokeWidth=6)
d.path("M156,676 C410,604 700,476 900,426", "Branch moonlight", fill=NONE,
       stroke="#C9CEDE", strokeWidth=4, opacity=35, cap="round")
for i, (t0, dy, ln) in enumerate([(0.10, 24, 0.12), (0.30, 40, 0.10), (0.52, 22, 0.14),
                                  (0.70, 46, 0.09), (0.84, 30, 0.08)]):
    a, b = bez(t0), bez(t0 + ln)
    d.path(f"M{a[0]:.0f},{a[1]+dy:.0f} L{b[0]:.0f},{b[1]+dy:.0f}", f"Bark groove {i+1}",
           fill=NONE, stroke="#140E0A", strokeWidth=3, opacity=50, cap="round")
# a gnawed grub-hole: what the tapping is listening for
gx = 184; gy = top_y(gx)
d.shape("ellipse", "Grub hole", x=gx-12, y=gy+10, width=26, height=14, fill="#0C0806", opacity=85, stroke=NONE)
d.path(f"M{gx-14},{gy+12} C{gx-4},{gy+6} {gx+8},{gy+6} {gx+16},{gy+12}", "Grub hole lip",
       fill=NONE, stroke="#7A6656", strokeWidth=2, opacity=60, cap="round")

# --- far limbs (behind the body) ------------------------------------------------------------
fx = 600; fy = top_y(fx)
d.path(f"M560,470 C580,500 590,{fy-10:.0f} {fx},{fy+4:.0f}", "Hind leg far", fill=NONE,
       stroke=LIMB_FAR, strokeWidth=22, cap="round")
hx = 400; hy = top_y(hx)
d.path(f"M410,520 C404,560 402,{hy-14:.0f} {hx},{hy+2:.0f}", "Fore leg far", fill=NONE,
       stroke=LIMB_FAR, strokeWidth=20, cap="round")
for i, k in enumerate([-12, 0, 12]):
    d.path(f"M{hx+k-4},{hy-2:.0f} C{hx+k-6},{hy+10:.0f} {hx+k-2},{hy+18:.0f} {hx+k+4},{hy+20:.0f}",
           f"Far finger {i+1}", fill=NONE, stroke=LIMB_FAR, strokeWidth=6, cap="round")

# --- body: low, arched, creeping down-branch -------------------------------------------------
d.path("M372,470 C420,410 520,380 610,392 C680,402 712,450 690,496 "
       "C664,544 576,560 488,566 C432,570 384,556 360,524 Z",
       "Body", fill=FUR_GRAD, stroke=INK, strokeWidth=7)
d.path("M420,430 C480,398 560,388 620,398", "Back rim light", fill=NONE,
       stroke="#B98A4A", strokeWidth=6, opacity=22, cap="round")
for i, dd in enumerate(["M440,420 C436,404 438,392 444,382", "M486,404 C484,388 486,376 492,366",
                        "M534,396 C534,380 538,368 544,360", "M582,394 C584,378 590,368 598,362",
                        "M628,402 C634,388 642,380 650,376", "M670,430 C682,420 692,416 702,414",
                        "M520,560 C518,574 520,584 526,592", "M570,552 C572,566 576,576 582,582",
                        "M470,566 C466,578 466,588 470,596"]):
    d.path(dd, f"Guard hair {i+1}", fill=NONE, stroke="#8C7A68", strokeWidth=3, opacity=50, cap="round")

# --- near hind leg gripping the branch -------------------------------------------------------
kx = 676; ky = top_y(kx)
d.path("M690,456 C716,470 718,500 700,512 C680,524 648,516 640,494 C632,470 660,446 690,456 Z",
       "Thigh", fill=FUR_GRAD, stroke=INK, strokeWidth=5)
d.path(f"M690,508 C694,{ky-14:.0f} {kx+2},{ky-6:.0f} {kx},{ky+4:.0f}", "Hind shin",
       fill=NONE, stroke="#2A1D15", strokeWidth=14, cap="round")
for i, k in enumerate([-18, -6, 6, 18]):
    x = kx + k; y = top_y(x)
    d.path(f"M{x},{y-4:.0f} C{x-4},{y+8:.0f} {x},{y+16:.0f} {x+6},{y+18:.0f}", f"Hind toe {i+1}",
           fill=NONE, stroke="#2A1D15", strokeWidth=6, cap="round")

# near fore arm runs under the chin, so it is drawn before the head
wx = 304; wy = top_y(wx)
d.path(f"M372,540 C352,580 300,{wy-30:.0f} {wx+6},{wy-18:.0f}", "Fore arm near",
       fill=NONE, stroke="#2A1D15", strokeWidth=22, cap="round")

# --- ears: big leathery lobes, as in V1 --------------------------------------------------------
HX, HY = 318, 470   # head centre
d.path("M286,428 C232,416 180,366 160,300 C152,272 170,256 196,264 "
       "C256,284 304,336 318,398 C322,418 306,432 286,428 Z",
       "Ear L", fill=EAR_GRAD, stroke=INK, strokeWidth=6)
d.path("M350,428 C404,416 456,366 476,300 C484,272 466,256 440,264 "
       "C380,284 332,336 318,398 C314,418 330,432 350,428 Z",
       "Ear R", fill=EAR_GRAD, stroke=INK, strokeWidth=6)
d.path("M286,408 C244,396 204,358 186,306 C182,292 192,284 206,290 "
       "C252,308 288,348 300,392 C304,404 296,412 286,408 Z",
       "Inner ear L", fill="#8A6350", opacity=60, stroke=NONE)
d.path("M350,408 C392,396 432,358 450,306 C454,292 444,284 430,290 "
       "C384,308 348,348 336,392 C332,404 340,412 350,408 Z",
       "Inner ear R", fill="#8A6350", opacity=60, stroke=NONE)
d.path("M200,292 C230,320 262,352 282,388", "Ear vein L", fill=NONE,
       stroke="#4A3226", strokeWidth=3, opacity=45, cap="round")
d.path("M436,292 C406,320 374,352 354,388", "Ear vein R", fill=NONE,
       stroke="#4A3226", strokeWidth=3, opacity=45, cap="round")

# --- head: turned to stare straight out of the plate ---------------------------------------------
d.path(f"M{HX},{HY-82} C{HX+66},{HY-82} {HX+100},{HY-30} {HX+100},{HY+20} "
       f"C{HX+100},{HY+78} {HX+52},{HY+112} {HX+16},{HY+118} "
       f"C{HX+6},{HY+122} {HX-6},{HY+122} {HX-16},{HY+118} "
       f"C{HX-52},{HY+112} {HX-100},{HY+78} {HX-100},{HY+20} "
       f"C{HX-100},{HY-30} {HX-66},{HY-82} {HX},{HY-82} Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=7)
d.path(f"M{HX-60},{HY-56} C{HX-34},{HY-78} {HX},{HY-84} {HX+40},{HY-78}", "Crown rim light",
       fill=NONE, stroke="#B98A4A", strokeWidth=6, opacity=22, cap="round")
for i, dd in enumerate([f"M{HX-20},{HY-80} C{HX-24},{HY-96} {HX-22},{HY-108} {HX-16},{HY-118}",
                        f"M{HX+6},{HY-82} L{HX+4},{HY-114}",
                        f"M{HX+30},{HY-78} C{HX+36},{HY-92} {HX+38},{HY-104} {HX+36},{HY-114}"]):
    d.path(dd, f"Crown tuft {i+1}", fill=NONE, stroke="#6B5340", strokeWidth=4, opacity=70, cap="round")
# brow shadows + amber glow + eyes
for side, ex in (("L", HX-44), ("R", HX+44)):
    ey = HY + 4
    d.shape("ellipse", f"Brow shade {side}", x=ex-46, y=ey-50, width=92, height=30, fill="#0F0A06", opacity=35, stroke=NONE)
    d.shape("ellipse", f"Eye glow {side}", x=ex-62, y=ey-62, width=124, height=124, fill="#F2B03D", opacity=16, stroke=NONE)
    d.shape("ellipse", f"Eye glow inner {side}", x=ex-50, y=ey-50, width=100, height=100, fill="#F2B03D", opacity=14, stroke=NONE)
    d.shape("ellipse", f"Iris {side}", x=ex-38, y=ey-38, width=76, height=76, fill=IRIS_GRAD, stroke=INK, strokeWidth=4)
    d.shape("ellipse", f"Pupil {side}", x=ex-19, y=ey-19, width=38, height=38, fill="#140C08", stroke=NONE)
    d.shape("ellipse", f"Glint {side}", x=ex-16, y=ey-12, width=11, height=11, fill="#FFFFFF", opacity=90, stroke=NONE)
    d.shape("ellipse", f"Glint2 {side}", x=ex+6, y=ey+10, width=6, height=6, fill="#FFD98A", opacity=55, stroke=NONE)
    # heavy brow ridge cuts the top of each iris, slanting down to the nose: the glare
    s_ = 1 if side == "L" else -1
    xi, xo = ex + s_*44, ex - s_*46       # inner (nose side) and outer x
    sweep = 1 if side == "L" else 0
    d.path(f"M{xo},{ey-32} A50,50 0 0 {sweep} {xi},{ey-14} C{ex+s_*10},{ey-24} {ex-s_*20},{ey-30} {xo},{ey-32} Z",
           f"Brow ridge {side}", fill=HEAD_GRAD, stroke=NONE)
    d.path(f"M{xo+s_*4},{ey-31} C{ex-s_*20},{ey-29} {ex+s_*10},{ey-23} {xi-s_*4},{ey-15}",
           f"Brow line {side}", fill=NONE, stroke=INK, strokeWidth=5, cap="round")
# muzzle, nose, incisors
d.shape("ellipse", "Muzzle", x=HX-46, y=HY+50, width=92, height=70, fill="#6B5240", opacity=55, stroke=NONE)
d.path(f"M{HX-12},{HY+70} C{HX-12},{HY+60} {HX+12},{HY+60} {HX+12},{HY+70} "
       f"C{HX+12},{HY+82} {HX+6},{HY+88} {HX},{HY+88} C{HX-6},{HY+88} {HX-12},{HY+82} {HX-12},{HY+70} Z",
       "Nose", fill="#150D08", stroke=INK, strokeWidth=3)
d.path(f"M{HX-22},{HY+104} C{HX-10},{HY+97} {HX+10},{HY+97} {HX+22},{HY+104}", "Mouth",
       fill=NONE, stroke=INK, strokeWidth=5, cap="round")
for i, dd in enumerate([f"M{HX-16},{HY+80} C{HX-46},{HY+72} {HX-70},{HY+74} {HX-88},{HY+82}",
                        f"M{HX+16},{HY+80} C{HX+46},{HY+72} {HX+70},{HY+74} {HX+88},{HY+82}",
                        f"M{HX-94},{HY+40} C{HX-108},{HY+56} {HX-112},{HY+72} {HX-110},{HY+86}",
                        f"M{HX+94},{HY+40} C{HX+108},{HY+56} {HX+112},{HY+72} {HX+110},{HY+86}"]):
    d.path(dd, f"Whisker {i+1}", fill=NONE, stroke="#8A705A", strokeWidth=3, opacity=50, cap="round")

# --- near fore limb + the tapping hand ----------------------------------------------------------
d.shape("ellipse", "Palm", x=wx-20, y=wy-34, width=46, height=34, fill=HAND_GRAD, stroke=INK, strokeWidth=4)
# gripping fingers curled over the wood
for i, k in enumerate([-4, 10]):
    x = wx + k; y = top_y(x)
    d.path(f"M{x},{y-12:.0f} C{x-6},{y-2:.0f} {x-4},{y+10:.0f} {x+4},{y+14:.0f}", f"Grip finger {i+1}",
           fill=NONE, stroke="#2A1D15", strokeWidth=7, cap="round")
# the middle finger: long, skeletal, lifted mid-tap just above the wood
tx = gx + 18; ty = top_y(tx) - 14
kx_, ky_ = (wx + tx) / 2 + 6, min(wy, ty) - 36     # the raised middle joint
d.path(f"M{wx-16},{wy-24:.0f} C{wx-24},{wy-40:.0f} {kx_+12},{ky_:.0f} {kx_},{ky_:.0f} "
       f"C{kx_-12},{ky_:.0f} {tx+4},{ty-18:.0f} {tx},{ty:.0f}",
       "Middle finger", fill=NONE, stroke="#3A2A1E", strokeWidth=6, cap="round")
d.path(f"M{wx-18},{wy-28:.0f} C{wx-26},{wy-42:.0f} {kx_+12},{ky_-2:.0f} {kx_},{ky_-2:.0f}",
       "Finger rim", fill=NONE, stroke="#B98A4A", strokeWidth=2, opacity=50, cap="round")
d.shape("ellipse", "Finger knuckle", x=kx_-6, y=ky_-5, width=12, height=10, fill="#3A2A1E", stroke=INK, strokeWidth=2)
d.shape("ellipse", "Finger tip", x=tx-5, y=ty-4, width=9, height=8, fill="#3A2A1E", stroke=INK, strokeWidth=2)
# tap ripples on the wood under the fingertip
tyw = top_y(tx)
for i, (rw, o) in enumerate([(14, 55), (26, 35), (40, 20)]):
    d.path(f"M{tx-rw},{tyw-4-i*4:.0f} C{tx-rw/2},{tyw-12-i*6:.0f} {tx+rw/2},{tyw-12-i*6:.0f} {tx+rw},{tyw-4-i*4:.0f}",
           f"Tap ring {i+1}", fill=NONE, stroke="#F2B03D", strokeWidth=2.5, opacity=o, cap="round")

# --- name -------------------------------------------------------------------------------------
d.text("AYE-AYE", "Name", x=500, y=962, size=60, font="Virelai Sans",
       color="#C9CEDE", justify="center")

d.finish("aye-aye-V2R00")
