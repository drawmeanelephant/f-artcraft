#!/usr/bin/env python3
"""Pink fairy armadillo — field-guide plate V1R00. Side view facing left,
half-buried in loose sand: pale pink banded carapace catching the light,
white silky fur showing at every seam, blunt rear plate, small pink ear,
a tiny milky blind-looking eye and big digging claws. Sand palette, dusk.
1000x1000. House style: gradients + translucent shading, never flat fills."""
import sys, os, math, random, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vc import Draw, NONE

d = D0 = Draw()
d.new_doc("Pink Fairy Armadillo — Field Plate", 1000, 1000)

INK = "#5A2E33"
CX, CY, R = 500, 460, 420          # plate disc centre + radius
random.seed(61)

def lin(x0, y0, x1, y1, *stops):
    return {"gradient": {"kind": "linear", "start": [x0, y0], "end": [x1, y1],
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rad(*stops):
    return {"gradient": {"kind": "radial",
            "stops": [{"offset": o, "color": c} for o, c in stops]}}

def rim(y):
    dx = math.sqrt(R*R - (y - CY)**2)
    return CX - dx, CX + dx

def ground(label, yl, yr, mid, fill, xf=None, **kw):
    """Band whose top runs rim-to-rim through `mid` (C-curve control pairs)
    and whose bottom closes on the disc's own arc."""
    xl, _ = rim(yl); _, xr = rim(yr)
    big = 1 if (yl + yr)/2 < CY else 0
    if xf:
        mid = xf.tpath(mid.replace("{xr}", "")) + " {xr}"
    dd = f"M{xl:.1f},{yl} " + mid.format(xr=f"{xr:.1f},{yr}") + \
         f" A{R},{R} 0 {big} 1 {xl:.1f},{yl} Z"
    D0.path(dd, label, fill=fill, stroke=NONE, **kw)

class Xf:
    """Scale/translate proxy over Draw: the animal is laid out in a compact
    frame, then enlarged into the plate. Uppercase path commands are absolute,
    lowercase ones only scale."""
    def __init__(self, base, px, py, ox, oy, k):
        self.b, self.px, self.py, self.ox, self.oy, self.k = base, px, py, ox, oy, k
    def P(self, x, y):
        return self.ox + (x - self.px)*self.k, self.oy + (y - self.py)*self.k
    def tpath(self, dd):
        out, nums, cmd = [], [], "M"
        for t in re.findall(r"[A-Za-z]|-?\d*\.?\d+", dd):
            if t.isalpha():
                out.append(t); cmd = t; continue
            nums.append(float(t))
            if len(nums) == 2:
                x, y = self.P(*nums) if cmd.isupper() else (nums[0]*self.k, nums[1]*self.k)
                out.append(f"{x:.1f},{y:.1f}"); nums = []
        return " ".join(out)
    def tpaint(self, p):
        if isinstance(p, dict) and "start" in p.get("gradient", {}):
            g = dict(p["gradient"])
            g["start"] = list(self.P(*g["start"])); g["end"] = list(self.P(*g["end"]))
            return {"gradient": g}
        return p
    def _kw(self, kw):
        for key in ("fill", "stroke"):
            if key in kw:
                kw[key] = self.tpaint(kw[key])
        return kw
    def path(self, dd, label, **kw):
        return self.b.path(self.tpath(dd), label, **self._kw(kw))
    def shape(self, kind, label, x, y, width, height, **kw):
        x, y = self.P(x, y)
        return self.b.shape(kind, label, x=x, y=y, width=width*self.k, height=height*self.k, **self._kw(kw))

BG_GRAD = lin(0, 0, 0, 1000, (0, "#2E1C1E"), (1, "#100809"))
PLATE_GRAD = lin(0, 40, 0, 640, (0, "#F7E9D2"), (0.6, "#F0D7B0"), (1, "#E6C291"))
DUNE_FAR = lin(0, 430, 0, 640, (0, "#E2BE8A"), (1, "#D2A86E"))
DUNE_MID = lin(0, 500, 0, 660, (0, "#D9AE74"), (1, "#C49660"))
SAND = lin(0, 540, 0, 880, (0, "#EDCE9C"), (0.5, "#DDB57C"), (1, "#C29560"))
SHELL_A = lin(0, 395, 0, 570, (0, "#FFEDEE"), (0.4, "#F7C7CE"), (1, "#DE8E9E"))
SHELL_B = lin(0, 395, 0, 570, (0, "#FCE2E5"), (0.4, "#F2BAC3"), (1, "#D58294"))
HEAD_GRAD = lin(190, 440, 340, 570, (0, "#F9D3D8"), (0.55, "#EDAAB6"), (1, "#D68A99"))
REAR_GRAD = rad((0, "#F6C2CA"), (0.7, "#E29AA8"), (1, "#C67486"))
FUR = "#FFFCF6"

# --- backdrop + sand plate ----------------------------------------------------------------
d.shape("rectangle", "Backdrop", x=0, y=0, width=1000, height=1000, fill=BG_GRAD, stroke=NONE)
for i, (x, y, w) in enumerate([(110,150,4),(880,110,5),(50,500,4),(950,430,4),(120,880,4),(890,880,5),(30,740,3),(960,700,4)]):
    d.shape("ellipse", f"Sky fleck {i+1}", x=x, y=y, width=w, height=w, fill="#F2D8C8", opacity=30, stroke=NONE)
d.shape("ellipse", "Plate", x=80, y=40, width=840, height=840,
        fill=PLATE_GRAD, stroke="#8A6440", strokeWidth=6)
d.shape("ellipse", "Plate inner ring", x=104, y=64, width=792, height=792,
        fill=NONE, stroke="#FFF6E6", strokeWidth=3, opacity=60)
# low dusk sun + haze
d.shape("ellipse", "Sun halo", x=196, y=196, width=180, height=180, fill="#FFF4DE", opacity=30, stroke=NONE)
d.shape("ellipse", "Sun", x=241, y=241, width=90, height=90,
        fill=rad((0, "#FFF8EA"), (1, "#F8DDB8")), opacity=85, stroke=NONE)
for i, (x, y, w, h) in enumerate([(560,200,240,26),(180,330,200,20),(620,300,170,16)]):
    d.shape("ellipse", f"Haze {i+1}", x=x, y=y, width=w, height=h, fill="#FFFFFF", opacity=22, stroke=NONE)

# far dunes, each closing on the disc arc
ground("Dune far", 470, 440, "C260,420 380,400 520,430 C640,455 740,420 {xr}", DUNE_FAR, opacity=70)
d.path("M300,414 C380,402 450,410 520,430", "Dune far crest", fill=NONE, stroke="#FFF2DC",
       strokeWidth=4, opacity=55, cap="round")
ground("Dune mid", 520, 500, "C230,500 340,478 470,500 C590,520 700,486 {xr}", DUNE_MID, opacity=75)
d.path("M620,500 C680,492 740,488 820,498", "Dune mid crest", fill=NONE, stroke="#FFF2DC",
       strokeWidth=4, opacity=45, cap="round")
# dry scrub on the far dune
for i, (x, y) in enumerate([(700, 452), (742, 446), (180, 470)]):
    for k, dx in enumerate([-12, -6, 0, 6, 12]):
        d.path(f"M{x},{y} Q{x+dx*0.6},{y-14} {x+dx},{y-24+abs(dx)}", f"Scrub {i+1}-{k+1}",
               fill=NONE, stroke="#A27A4C", strokeWidth=3, opacity=55, cap="round")

# --- the armadillo --------------------------------------------------------------------------
d = A = Xf(D0, 469, 570, 500, 604, 1.18)
SX0, SX1, SBASE, SH = 318, 726, 568, 168
SCX, SA = (SX0 + SX1)/2, (SX1 - SX0)/2

def ytop(x):
    """Carapace profile: rounder at the front, blunt at the rear."""
    t = max(-1.0, min(1.0, (x - SCX)/SA))
    p = 2.4 if t < 0 else 4.5
    return SBASE - SH*(1 - abs(t)**p)**(1/p)

# rear sand spray (behind the mound)
for i in range(26):
    x, y = random.uniform(748, 800), random.uniform(440, 548)
    if math.hypot(*(p - c for p, c in zip(A.P(x, y), (CX, CY)))) > R - 34:
        continue
    w = random.choice([3, 4, 5, 6])
    d.shape("ellipse", f"Spray grain {i+1}", x=x, y=y, width=w, height=w,
            fill=random.choice(["#C99A62", "#E3BE86", "#B88850"]), opacity=random.choice([60, 75, 90]), stroke=NONE)
for i, (x, y, w, h, op) in enumerate([(738,490,60,44,22),(752,456,46,34,16),(722,520,80,40,26)]):
    d.shape("ellipse", f"Dust puff {i+1}", x=x, y=y, width=w, height=h, fill="#F3DDB6", opacity=op, stroke=NONE)

# white fur skirt under the carapace (mostly buried)
d.path("M300,548 C380,560 520,566 720,560 L724,598 C560,606 400,604 296,594 Z",
       "Fur skirt", fill=lin(0, 548, 0, 600, (0, "#FFFFFF"), (1, "#EADFD2")), stroke=NONE)
for i in range(18):
    x = 312 + i*23
    d.path(f"M{x},{562} Q{x-4},{574} {x-10},{584}", f"Skirt wisp {i+1}", fill=NONE,
           stroke="#D9CBBB", strokeWidth=3, opacity=55, cap="round")

# head shield + snout (tucked under the carapace front)
d.path("M354,472 C330,450 296,444 264,462 C242,476 214,514 192,544 "
       "C186,554 194,562 208,561 C240,558 280,562 312,570 L356,572 Z",
       "Head", fill=HEAD_GRAD, stroke=INK, strokeWidth=5)
# head-shield scale grid
for i, dd in enumerate(["M330,456 C310,470 292,486 278,500", "M306,452 C290,466 274,482 262,494",
                        "M282,462 C268,474 256,486 246,496", "M262,480 C296,476 322,482 344,492",
                        "M248,494 C272,490 292,492 310,498"]):
    d.path(dd, f"Head shield seam {i+1}", fill=NONE, stroke=INK, strokeWidth=3, opacity=40, cap="round")
d.path("M232,494 C262,474 300,460 336,458", "Head shield sheen", fill=NONE, stroke="#FFFFFF",
       strokeWidth=6, opacity=40, cap="round")
# snout tip, nostril, mouth
d.path("M206,538 C196,544 188,550 190,556 C194,562 206,562 214,556 Z", "Nose pad",
       fill=lin(0, 538, 0, 562, (0, "#E9919F"), (1, "#C26478")), stroke=NONE)
d.shape("ellipse", "Nostril", x=193, y=549, width=6, height=5, fill="#6E2F3A", opacity=80, stroke=NONE)
d.path("M210,560 C232,562 252,564 270,568", "Mouth", fill=NONE, stroke=INK, strokeWidth=3, opacity=70, cap="round")
# cheek fur under the jaw
for i, (x, y) in enumerate([(232,566),(252,568),(272,570),(292,572)]):
    d.path(f"M{x},{y} Q{x-6},{y+8} {x-12},{y+14}", f"Cheek fur {i+1}", fill=NONE,
           stroke=FUR, strokeWidth=3, opacity=90, cap="round")
# tiny milky eye
d.shape("ellipse", "Eye socket", x=262, y=502, width=16, height=13, fill="#B86E7E", opacity=45, stroke=NONE)
d.shape("ellipse", "Eye", x=265, y=504, width=10, height=9, fill="#2A1418", stroke=NONE)
d.shape("ellipse", "Eye film", x=265, y=504, width=10, height=9, fill="#DCD6E6", opacity=45, stroke=NONE)
d.shape("ellipse", "Eye glint", x=267, y=505, width=3, height=3, fill="#FFFFFF", opacity=80, stroke=NONE)
# small pink ear
d.path("M300,486 C298,470 306,460 318,462 C326,466 324,480 314,492 Z", "Ear",
       fill=lin(0, 460, 0, 492, (0, "#F7B8C3"), (1, "#DC8396")), stroke=INK, strokeWidth=3)
d.path("M306,482 C306,472 311,467 316,469 C318,474 316,480 311,486 Z", "Ear inner",
       fill="#C46479", opacity=50, stroke=NONE)

# carapace: base dome, then each band drawn as its own gradient strip
N = 17
xs = [SX0 + 8 + (SX1 - SX0 - 14)*k/N for k in range(N + 1)]
def bow(x):
    return (x - SCX)/SA*12
dome = f"M{SX0},{SBASE} " + " ".join(f"L{x:.1f},{ytop(x):.1f}" for x in
                                     [SX0 + (SX1 - SX0)*i/60 for i in range(61)]) + f" L{SX1},{SBASE} Z"
d.path(dome, "Carapace", fill=SHELL_A, stroke=INK, strokeWidth=5)
for k in range(N):
    xa, xb = xs[k], xs[k + 1]
    top = " ".join(f"L{x:.1f},{ytop(x) + 1.5:.1f}" for x in [xa + (xb - xa)*i/4 for i in range(5)])
    ya, yb = ytop(xa), ytop(xb)
    dd = (f"M{xa:.1f},{ya + 1.5:.1f} {top[1:]} "
          f"Q{xb + bow(xb):.1f},{(yb + SBASE)/2:.1f} {xb:.1f},{SBASE - 2} "
          f"L{xa:.1f},{SBASE - 2} Q{xa + bow(xa):.1f},{(ya + SBASE)/2:.1f} {xa:.1f},{ya + 1.5:.1f} Z")
    d.path(dd, f"Band {k+1}", fill=SHELL_A if k % 2 else SHELL_B, stroke=NONE)
    # front lip of each band catches the light
    d.path(f"M{xa + 3:.1f},{ya + 6:.1f} Q{xa + bow(xa) + 3:.1f},{(ya + SBASE)/2:.1f} {xa + 3:.1f},{SBASE - 18}",
           f"Band lip {k+1}", fill=NONE, stroke="#FFFFFF", strokeWidth=3, opacity=45, cap="round")
# seams with white fur escaping at each one
for k in range(1, N):
    x = xs[k]; y = ytop(x)
    d.path(f"M{x:.1f},{y + 1:.1f} Q{x + bow(x):.1f},{(y + SBASE)/2:.1f} {x:.1f},{SBASE - 2}",
           f"Seam {k}", fill=NONE, stroke=INK, strokeWidth=3, opacity=75, cap="round")
    for j in range(random.choice([1, 2, 2, 3])):
        yy = random.uniform(y + 24, SBASE - 40)
        ln = random.uniform(8, 16); dx = random.choice([-1, 1])
        d.path(f"M{x + bow(x)*0.3:.1f},{yy:.1f} q{dx*random.uniform(2, 6):.1f},{ln*0.5:.1f} {dx*3 - random.uniform(2, 6):.1f},{ln:.1f}",
               f"Seam fur {k}-{j+1}", fill=NONE, stroke=FUR, strokeWidth=3,
               opacity=random.choice([70, 85, 95]), cap="round")
    if random.random() < 0.55:
        d.path(f"M{x:.1f},{y + 2:.1f} q{random.uniform(-6, -2):.1f},-6 {random.uniform(-10, -5):.1f},{random.uniform(-10, -6):.1f}",
               f"Seam crest fur {k}", fill=NONE, stroke=FUR, strokeWidth=3, opacity=75, cap="round")
# banded gradient catching light: long specular along the crown, shade along the base
crest = " ".join(f"L{x:.1f},{ytop(x) + 26:.1f}" for x in range(372, 690, 12))
d.path("M" + crest[1:], "Carapace sheen", fill=NONE, stroke="#FFFFFF", strokeWidth=12, opacity=34, cap="round")
crest2 = " ".join(f"L{x:.1f},{ytop(x) + 14:.1f}" for x in range(420, 640, 12))
d.path("M" + crest2[1:], "Carapace glint", fill=NONE, stroke="#FFFFFF", strokeWidth=4, opacity=60, cap="round")
d.path(f"M{SX0 + 30},{SBASE - 14} L{SX1 - 16},{SBASE - 14}", "Carapace base shade", fill=NONE,
       stroke="#B0607A", strokeWidth=18, opacity=24, cap="round")
rear = f"M{SX1 - 120},{SBASE} " + " ".join(f"L{x:.1f},{ytop(x) + 2:.1f}" for x in range(SX1 - 120, SX1 + 1, 10)) + f" L{SX1},{SBASE} Z"
d.path(rear, "Carapace rear shade", fill=lin(SX1 - 120, 0, SX1, 0, (0, "#F6C7CE"), (1, "#A9566C")), opacity=30, stroke=NONE)
d.path(dome, "Carapace outline", fill=NONE, stroke=INK, strokeWidth=5)
# blunt rear plate
d.path("M716,440 C736,442 750,470 752,506 C754,546 744,580 728,590 L712,590 C720,560 722,470 716,440 Z",
       "Rear plate", fill=REAR_GRAD, stroke=INK, strokeWidth=4)
for i, dd in enumerate(["M724,462 C734,476 740,500 740,526", "M722,488 C730,500 732,520 732,540",
                        "M740,470 C746,490 748,514 746,540"]):
    d.path(dd, f"Rear plate ring {i+1}", fill=NONE, stroke=INK, strokeWidth=3, opacity=35, cap="round")
d.path("M722,448 C736,458 744,476 746,494", "Rear plate light", fill=NONE, stroke="#FFFFFF",
       strokeWidth=4, opacity=40, cap="round")
for i, (x, y) in enumerate([(718,446),(726,444),(712,456)]):
    d.path(f"M{x},{y} q-2,-7 -7,-11", f"Rear fur {i+1}", fill=NONE, stroke=FUR, strokeWidth=3, opacity=85, cap="round")


# --- loose sand: foreground heap closes on the disc arc --------------------------------------
ground("Sand", 640, 582,
       "C186,604 214,594 250,590 C290,584 314,566 346,552 C400,536 500,540 600,536 "
       "C660,534 700,520 736,512 C756,508 772,510 780,514 C786,518 792,526 {xr}", SAND, xf=A)
d.path("M196,600 C220,592 250,590 290,584 C314,566 346,552 400,537 C500,540 600,536 660,534 C700,520 736,512 772,514",
       "Sand crest light", fill=NONE, stroke="#FFF2DA", strokeWidth=4, opacity=70, cap="round")
# loose grains trickling down the shell flank and heaped against the rear plate
for i, (x, y, w) in enumerate([(372,540,5),(410,532,4),(452,534,6),(512,534,4),(566,532,5),(620,530,4),
                               (668,524,5),(700,514,6),(722,506,4),(740,502,5),(434,528,3),(588,528,3),
                               (480,470,4),(536,452,3),(602,462,4),(650,476,3)]):
    d.shape("ellipse", f"Loose grain {i+1}", x=x, y=y, width=w, height=w, fill="#D4A86E", opacity=85, stroke=NONE)
# sand shading + ripples, all comfortably inside the disc (plate frame)
d = D0
for i, (x, y, w, h) in enumerate([(300,672,200,18),(560,684,220,20),(240,770,160,14),(470,786,240,18),
                                  (380,846,180,12),(640,816,120,14)]):
    d.shape("ellipse", f"Sand shade {i+1}", x=x, y=y, width=w, height=h, fill="#B88B56", opacity=22, stroke=NONE)
for i, dd in enumerate(["M200,700 C280,688 360,692 440,704", "M500,712 C590,700 680,704 770,716",
                        "M180,752 C280,740 380,746 450,756", "M520,770 C610,758 700,762 760,770",
                        "M260,810 C350,798 450,802 540,812", "M570,840 C620,834 660,836 700,840"]):
    d.path(dd, f"Ripple {i+1}", fill=NONE, stroke="#A87C48", strokeWidth=3, opacity=40, cap="round")
for i, (x, y, w) in enumerate([(230,724,10),(620,736,8),(340,782,7),(700,790,9),(460,830,8)]):
    d.shape("ellipse", f"Pebble {i+1}", x=x, y=y, width=w*1.4, height=w,
            fill=lin(0, y, 0, y + w, (0, "#C9A57A"), (1, "#8E6A44")), stroke=NONE)
# armadillo shadow in the sand
d = A
d.path("M340,556 C420,544 520,546 620,542 C680,540 720,526 760,520", "Sand heave shade", fill=NONE,
       stroke="#B98A52", strokeWidth=10, opacity=28, cap="round")

# claws breaking the sand in front of the face, sand kicked up by them
for i, (x, y, ang) in enumerate([(236,590,0), (250,592,8), (264,594,16)]):
    d.path(f"M{x},{y} C{x-8},{y-4} {x-18},{y-2} {x-24},{y+8} C{x-16},{y+4} {x-8},{y+6} {x+2},{y+8} Z",
           f"Claw {i+1}", fill=lin(0, y - 4, 0, y + 8, (0, "#FFF8EC"), (1, "#D8C6AE")), stroke=INK, strokeWidth=2)
for i in range(12):
    x, y = random.uniform(190, 236), random.uniform(560, 588)
    w = random.choice([3, 4, 5])
    d.shape("ellipse", f"Claw grain {i+1}", x=x, y=y, width=w, height=w, fill="#C99A62", opacity=80, stroke=NONE)

# foreground scrub tufts (plate frame)
d = D0
for i, (x, y) in enumerate([(190, 690), (802, 700), (226, 806)]):
    for k, dx in enumerate([-16, -9, -3, 3, 9, 16]):
        d.path(f"M{x},{y} Q{x+dx*0.5},{y-18} {x+dx*1.2},{y-34+abs(dx)}", f"Tuft {i+1}-{k+1}",
               fill=NONE, stroke=lin(0, y - 34, 0, y, (0, "#C9A46A"), (1, "#8C6A3E")), strokeWidth=3, cap="round")

# --- name -------------------------------------------------------------------------------------
d.text("PINK FAIRY ARMADILLO", "Name", x=500, y=962, size=52, font="Virelai Sans",
       color="#F4DCD6", justify="center")

d.finish("pink-fairy-armadillo-V1R00")
