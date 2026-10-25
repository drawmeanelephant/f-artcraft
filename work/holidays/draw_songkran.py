#!/usr/bin/env python3
"""Songkran — Festival Seal V1R00.

Thai new year: a brass pedestal bowl of scented water with frangipani
blossoms afloat, and two fountain arcs of splash rising off the rim —
the splashes kept in the house's soft-puff cloud language, translucent
radial puffs with a droplet tail. Deep teal field, aqua + gold. 1000x1000.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orient.plate import (Plate, PCX, PCY, PR, NONE, INK, GOLD, GOLD_HI, PAPER,
                          LATIN, CJK, lin, rad, gold_lin, smooth, blend)
from festival_kit import (seal_disc, glow, dust, ring_dots, caption)

SLUG = "songkran-V1R00"
SS3 = "Source Sans 3"

TEAL_HI = "#2E6B74"
TEAL_LO = "#071C22"
AQUA = "#8EE2E0"
AQUA_LO = "#3E9EA4"
FOAM = "#E8FAF6"
FRANGI = "#FFF6E4"
FRANGI_EDGE = "#F2D8E0"
FRANGI_CORE = "#F6C85A"

p = Plate("Songkran — Festival Seal", 1000, 1000)
d = p.d


def inside(x, y, pad=0, label=""):
    if math.hypot(x - PCX, y - PCY) > PR - pad:
        raise AssertionError(f"outside disc: {label} ({x:.0f},{y:.0f})")
    return (x, y)


# --- field ------------------------------------------------------------------
p.backdrop(top="#0E2A30", bottom="#040C0E", glow=("#2E6B74", 16))
dust(d, n=42, r=404, colors=("#C8F0EA", "#F6E3B8"), seed=23,
     smin=0.8, smax=2.2, opmin=8, opmax=22, label="Backdrop dust")
seal_disc(p, TEAL_HI, TEAL_LO, rim="#D8BC78", rim2="#1E3E32")
dust(d, n=58, r=392, colors=("#C8F0EA", "#F6E3B8", "#8EE2E0"), seed=13,
     smin=1.0, smax=2.8, opmin=9, opmax=26, label="Disc dust")

# field guides + cool light welling up under the bowl
for rr, op in ((170, 12), (254, 9), (332, 8)):
    d.shape("ellipse", f"Field ring {rr}", x=PCX - rr, y=PCY - rr,
            width=2 * rr, height=2 * rr, fill=NONE, stroke="#9ADCD6",
            strokeWidth=1.4, opacity=op)
ring_dots(d, r=398, n=56, size=2.6, color="#C8B078", opacity=32)
glow(d, 500, 620, 320, "#7ADAD4", a=20, label="Water light", squash=0.8)
glow(d, 500, 380, 260, "#BFF2EA", a=12, label="Mist light")


# --- splash language ---------------------------------------------------------
def water_puff(cx, cy, r, opacity=44, seed=7, label="Splash puff",
               squash=0.9):
    """Soft cloud-language splash: radial heart + overlapping aqua lobes."""
    d.shape("ellipse", f"{label} heart", x=cx - r, y=cy - r * squash,
            width=2 * r, height=2 * r * squash,
            fill=rad((0, FOAM, min(80, opacity + 30)),
                     (0.55, AQUA, opacity), (1, AQUA, 0)), stroke=NONE)
    s = seed
    for i in range(9):
        s = (1103515245 * s + 12345) % (2 ** 31)
        a = math.tau * (s / 2 ** 31)
        s = (1103515245 * s + 12345) % (2 ** 31)
        rr = r * (0.26 + 0.62 * (s / 2 ** 31))
        s = (1103515245 * s + 12345) % (2 ** 31)
        pr = r * (0.22 + 0.24 * (s / 2 ** 31))
        px, py = cx + math.cos(a) * rr, cy + math.sin(a) * rr * squash
        d.shape("ellipse", f"{label} lobe {i+1}", x=px - pr,
                y=py - pr * squash, width=pr * 2, height=pr * 2 * squash,
                fill=rad((0, FOAM, opacity), (0.6, AQUA, opacity * 0.5),
                         (1, AQUA, 0)), stroke=NONE)


def qbez(p0, pc, p1, t):
    mt = 1 - t
    return (mt * mt * p0[0] + 2 * mt * t * pc[0] + t * t * p1[0],
            mt * mt * p0[1] + 2 * mt * t * pc[1] + t * t * p1[1])


def qtan(p0, pc, p1, t):
    return (2 * (1 - t) * (pc[0] - p0[0]) + 2 * t * (p1[0] - pc[0]),
            2 * (1 - t) * (pc[1] - p0[1]) + 2 * t * (p1[1] - pc[1]))


def splash_arc(x0, y0, apex, x1, y1, label, seed=5):
    """Thrown water: a parabolic jet from the bowl rim landing on the field,
    foam puffs along the falling side, a burst where it lands."""
    p0, pc, p1 = (x0, y0), apex, (x1, y1)
    # stream body — deep aqua under a foam core
    d.path(f"M{x0:.1f},{y0:.1f} Q{apex[0]:.1f},{apex[1]:.1f} "
           f"{x1:.1f},{y1:.1f}", f"{label} stream", fill=NONE,
           stroke=AQUA_LO, strokeWidth=18, opacity=58, cap="round")
    d.path(f"M{x0:.1f},{y0 - 2:.1f} Q{apex[0]:.1f},{apex[1] - 4:.1f} "
           f"{x1:.1f},{y1 - 1:.1f}", f"{label} stream hi", fill=NONE,
           stroke=FOAM, strokeWidth=7, opacity=52, cap="round")
    # break-up: foam puffs along the falling third of the arc
    for i, t in enumerate((0.52, 0.66, 0.79, 0.90)):
        bx, by = qbez(p0, pc, p1, t)
        water_puff(bx, by, 34 - i * 3, opacity=42 - i * 4,
                   seed=seed + i * 5, label=f"{label} foam {i+1}")
    # droplets flung outward beyond the stream
    rnd = random.Random(seed)
    for i in range(10):
        t = 0.42 + 0.56 * rnd.random()
        bx, by = qbez(p0, pc, p1, t)
        tx, ty = qtan(p0, pc, p1, t)
        outx = -1 if bx < PCX else 1
        dd = 16 + rnd.random() * 34
        px, py = bx + outx * dd, by - dd * 0.30
        s = 3.0 + rnd.random() * 4.4
        ang = math.degrees(math.atan2(ty, tx * outx))
        d.shape("ellipse", f"{label} drop {i+1}", x=px - s * 1.5,
                y=py - s * 0.8, width=s * 3.0, height=s * 1.6,
                fill=FOAM if i % 3 else AQUA, opacity=58 + i % 3 * 12,
                stroke=NONE, rotation=round(ang, 1))
    # landing burst: low wide puff + a flattened ring
    water_puff(x1, y1, 40, opacity=44, seed=seed + 11, squash=0.55,
               label=f"{label} land")
    d.shape("ellipse", f"{label} land ring", x=x1 - 58, y=y1 + 8, width=116,
            height=18, fill=NONE, stroke=AQUA, strokeWidth=2.4, opacity=36)
    d.shape("ellipse", f"{label} land ring 2", x=x1 - 34, y=y1 + 14,
            width=68, height=12, fill=NONE, stroke=FOAM, strokeWidth=1.8,
            opacity=30)


import random

# two jets sloshing out of the bowl, cresting and falling to the field floor
splash_arc(392, 610, (210, 268), 168, 700, "Splash L", seed=21)
splash_arc(608, 610, (790, 268), 832, 700, "Splash R", seed=33)

# a short fountain burst above the bowl mouth
water_puff(500, 452, 40, opacity=40, seed=41, label="Fountain")
water_puff(500, 500, 26, opacity=32, seed=47, label="Fountain low")
for i, (px, py, s, ang) in enumerate([(452, 420, 4.0, -115), (548, 418, 4.4, -65),
                                      (486, 396, 3.6, -90), (520, 440, 3.2, -70)]):
    d.shape("ellipse", f"Fountain drop {i+1}", x=px - s * 1.5,
            y=py - s * 0.8, width=s * 3.0, height=s * 1.6, fill=FOAM,
            opacity=64, stroke=NONE, rotation=ang)

# stray droplets over the field
for i, (px, py, s, ang) in enumerate([(300, 340, 4.6, -115), (700, 340, 4.2, -65),
                                      (240, 520, 3.8, -135), (760, 520, 4.4, -45),
                                      (416, 336, 3.4, -100), (584, 336, 3.8, -80)]):
    d.shape("ellipse", f"Stray drop {i+1}", x=px - s * 1.5, y=py - s * 0.8,
            width=s * 3.0, height=s * 1.6,
            fill=AQUA if i % 2 else FOAM, opacity=56, stroke=NONE,
            rotation=ang)


# --- frangipani ---------------------------------------------------------------
def frangipani(cx, cy, r, rot, label, opacity=96):
    """Five rounded pinwheel petals, cream-white with a golden throat."""
    for i in range(5):
        a = math.radians(rot + i * 72)
        px = cx + math.cos(a) * r * 0.52
        py = cy + math.sin(a) * r * 0.52
        # petal: rounded lobe leaning into the pinwheel
        d.shape("ellipse", f"{label} petal {i+1}",
                x=px - r * 0.46, y=py - r * 0.30, width=r * 0.94,
                height=r * 0.58,
                fill=rad((0, "#FFFDF4"), (0.55, FRANGI), (1, FRANGI_EDGE)),
                stroke="#C8A88A", strokeWidth=1.0, opacity=opacity,
                rotation=round(math.degrees(a) + 14, 1))
    d.shape("ellipse", f"{label} core", x=cx - r * 0.16, y=cy - r * 0.16,
            width=r * 0.32, height=r * 0.32,
            fill=rad((0, "#FFE89A"), (1, FRANGI_CORE)), stroke="#C8943C",
            strokeWidth=0.8)


# --- brass pedestal bowl ------------------------------------------------------
WX, WY = 500, 640   # rim centre

# shadow under the foot
d.shape("ellipse", "Bowl ground shadow", x=WX - 210, y=WY + 118, width=420,
        height=34, fill=rad((0, INK, 46), (0.6, INK, 22), (1, INK, 0)),
        stroke=NONE)

# pedestal foot
d.path(f"M{WX - 66:.1f},{WY + 88:.1f} C{WX - 80:.1f},{WY + 108:.1f} "
       f"{WX - 74:.1f},{WY + 124:.1f} {WX - 82:.1f},{WY + 132:.1f} "
       f"C{WX - 40:.1f},{WY + 146:.1f} {WX + 40:.1f},{WY + 146:.1f} "
       f"{WX + 82:.1f},{WY + 132:.1f} C{WX + 74:.1f},{WY + 124:.1f} "
       f"{WX + 80:.1f},{WY + 108:.1f} {WX + 66:.1f},{WY + 88:.1f} Z",
       "Bowl foot",
       fill=lin((WX - 70, WY + 88), (WX + 70, WY + 146),
                (0, "#B8852E"), (0.5, "#8A5A1C"), (1, "#4E3010")),
       stroke=INK, strokeWidth=2.6)
d.path(f"M{WX - 70:.1f},{WY + 96:.1f} Q{WX:.1f},{WY + 108:.1f} "
       f"{WX + 70:.1f},{WY + 96:.1f}", "Foot flare", fill=NONE,
       stroke="#E8C074", strokeWidth=2.2, opacity=50, cap="round")

# stem + belly of the pedestal bowl
d.path(f"M{WX - 40:.1f},{WY + 40:.1f} C{WX - 46:.1f},{WY + 62:.1f} "
       f"{WX - 62:.1f},{WY + 78:.1f} {WX - 66:.1f},{WY + 92:.1f} "
       f"L{WX + 66:.1f},{WY + 92:.1f} "
       f"C{WX + 62:.1f},{WY + 78:.1f} {WX + 46:.1f},{WY + 62:.1f} "
       f"{WX + 40:.1f},{WY + 40:.1f} Z", "Bowl stem",
       fill=lin((WX - 44, WY + 40), (WX + 44, WY + 92),
                (0, "#D8A04E"), (0.5, "#A8722A"), (1, "#6E4214")),
       stroke=INK, strokeWidth=2.6)

# wide bowl belly
d.path(f"M{WX - 178:.1f},{WY - 8:.1f} "
       f"C{WX - 168:.1f},{WY + 44:.1f} {WX - 104:.1f},{WY + 64:.1f} "
       f"{WX:.1f},{WY + 66:.1f} "
       f"C{WX + 104:.1f},{WY + 64:.1f} {WX + 168:.1f},{WY + 44:.1f} "
       f"{WX + 178:.1f},{WY - 8:.1f} Z", "Bowl belly",
       fill=lin((WX - 160, WY), (WX + 160, WY + 66),
                (0, "#E8B45E"), (0.45, "#C08A34"), (0.8, "#8A5A1C"),
                (1, "#5E3A12")),
       stroke=INK, strokeWidth=3.0)
# belly sheen + engraved band
d.path(f"M{WX - 150:.1f},{WY + 18:.1f} C{WX - 120:.1f},{WY + 40:.1f} "
       f"{WX - 80:.1f},{WY + 52:.1f} {WX - 40:.1f},{WY + 56:.1f}",
       "Bowl sheen", fill=NONE, stroke="#F8DCA0", strokeWidth=4,
       opacity=30, cap="round")
d.path(f"M{WX - 150:.1f},{WY + 34:.1f} Q{WX:.1f},{WY + 62:.1f} "
       f"{WX + 150:.1f},{WY + 34:.1f}", "Bowl band", fill=NONE,
       stroke="#F6D998", strokeWidth=2.0, opacity=44, cap="round")
for i in range(9):
    t = (i + 0.5) / 9
    bx = WX - 132 + 264 * t
    by = WY + 42 + 8 * math.sin(math.pi * t)
    d.shape("ellipse", f"Band dot {i+1}", x=bx - 2.6, y=by - 2.6, width=5.2,
            height=5.2, fill="#FBE6B4", opacity=55, stroke=NONE)

# rim: rolled gold lip
d.shape("ellipse", "Bowl rim", x=WX - 184, y=WY - 26, width=368, height=48,
        fill=lin((0, WY - 26), (0, WY + 22),
                 (0, "#F6D998"), (0.5, "#D8A04E"), (1, "#96601E")),
        stroke=INK, strokeWidth=3.0)
# water inside the mouth
d.shape("ellipse", "Bowl water", x=WX - 162, y=WY - 18, width=324, height=34,
        fill=rad((0, "#D8F8F0"), (0.6, "#8ED8CE"), (1, "#4E9E98")),
        stroke="#3E7E78", strokeWidth=1.8)
# water surface glints
d.path(f"M{WX - 130:.1f},{WY - 6:.1f} Q{WX - 60:.1f},{WY + 2:.1f} "
       f"{WX + 10:.1f},{WY - 4:.1f}", "Water glint", fill=NONE,
       stroke="#FFFFFF", strokeWidth=2.4, opacity=44, cap="round")
d.path(f"M{WX + 40:.1f},{WY + 4:.1f} Q{WX + 90:.1f},{WY + 8:.1f} "
       f"{WX + 138:.1f},{WY + 2:.1f}", "Water glint 2", fill=NONE,
       stroke="#CFF2EA", strokeWidth=2.0, opacity=36, cap="round")

# frangipani floating on the water + one on the rim's left shoulder
frangipani(WX - 62, WY - 4, 34, -12, "Frangipani 1")
frangipani(WX + 44, WY + 2, 28, 24, "Frangipani 2")
frangipani(WX + 116, WY - 6, 24, 60, "Frangipani 3")
frangipani(WX - 172, WY + 8, 22, -40, "Frangipani rim")

# --- seal chop + caption ------------------------------------------------------
CHX, CHY, CHW, CHH = 848, 102, 108, 54
d.shape("rectangle", "Chop shadow", x=CHX + 3, y=CHY + 4, width=CHW,
        height=CHH, radius=5, fill="#000000", opacity=30, stroke=NONE)
d.shape("rectangle", "Chop", x=CHX, y=CHY, width=CHW, height=CHH, radius=5,
        fill=lin((CHX, CHY), (CHX + CHW, CHY + CHH), (0, "#B23A30"),
                 (1, "#7E1F1B")), stroke="#5E1412", strokeWidth=2)
d.shape("rectangle", "Chop inner", x=CHX + 4, y=CHY + 4, width=CHW - 8,
        height=CHH - 8, radius=2, fill=NONE, stroke=GOLD_HI,
        strokeWidth=1.5, opacity=70)
d.text("สงกรานต์", "Chop text", x=CHX + CHW / 2, y=CHY + CHH * 0.66, size=18,
       font=SS3, color=GOLD_HI, justify="center")

caption(p, "SONGKRAN", "สงกรานต์ · APR 13–15 · WATER FESTIVAL",
        name_color="#EFF6EA", sub_color="#A8C8BC",
        name_size=52, tracking_name=84, sub_size=20, tracking_sub=44,
        sub_font=SS3)
p.finish(SLUG)
