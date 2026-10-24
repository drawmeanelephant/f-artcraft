#!/usr/bin/env python3
"""Shared sexiburger mascot builder for the virelai brand pieces (#1254)
and the pose set (#1250).

Character truth: user/src/lib/fixtures/qoi/mascot_64x64.qoi (head-on fixture)
and image/WALLPAPER.QOI (alive pose — eyes, gloves, polka-dot bow tie).
Palette from vkit: BUN lit/mid, BUN_SHADE/DEEP shadow, warm-dark INK outlines,
white gloves. Cel shading — flat fills + one shadow tone, thick outlines,
rounded terminals. Same character, poses are not redesigns.

    from virelai.sexiburger import mascot, POSES
    mascot(d, cx, top, h, arms="up")
    mascot(d, cx, top, h, **POSES["wave"])

`h` is total mascot height in px; local frame is 160x230 units scaled to h.
Returns the inked bounding box approx (x, y, w, h) for layout checks.

Pose rig (all optional, backwards compatible with the brand pieces):
  arms        "up" | "out" | "down" — presets for BOTH arms
  arm_left / arm_right  ((p0),(p1),(p2)) control triple in local units,
              overrides that side's preset
  gloves      bool or (left, right)
  eyes        "open" | "closed" (∪ lids) | "happy" (∩ arcs)
  pupils      (dx, dy) shift in local units (think looks up, oops aside)
  mouth       "smile" | "grin" (open) | "flat" | "wavy" | "o"
  brows       None | "raise" | "angle" (guard)
  props       iterable of prop names / ("name", args...) drawn last, in
              local coords: "zzz", "confetti", "sweat", "padlock",
              ("wave", gx, gy) — arcs around a glove tip at (gx, gy)
"""
import math

from virelai.vkit import BUN, BUN_MID, BUN_SHADE, BUN_DEEP, GLOVE, INK

# fillings sampled off the fixture
LETTUCE = "#8BC34A"
LETTUCE_D = "#6FA03A"
TOMATO = "#E04B35"
PATTY = "#5E3D49"
CHEESE = "#FFC93C"
SEED = "#FFF0C2"
BOWTIE = "#D94F3D"
BOWTIE_DOT = "#7FD4C8"
PUPIL = "#3A2530"

# prop-only colors (vkit DARK tokens + reads on both surfaces)
ACCENT = "#3B82F6"
GREEN = "#22C55E"
WARN = "#F59E0B"
DROP = "#9CD8F0"
LOCK = "#94A3B8"

ARM_PRESETS = {
    "up":   (((-56, 122), (-98, 96), (-112, 56)),
             ((56, 122), (98, 96), (112, 56))),
    "out":  (((-56, 122), (-112, 118), (-136, 104)),
             ((56, 122), (112, 118), (136, 104))),
    "down": (((-56, 122), (-84, 152), (-76, 184)),
             ((56, 122), (84, 152), (76, 184))),
}

# Issue #1250 — the six poses. All drawn at the same slot:
# mascot(d, 32, 5, 52, **POSES[name]) on a 64x64 canvas.
POSES = {
    "wave": {
        "mouth": "grin",
        "arm_right": ((56, 122), (96, 84), (106, 42)),
        "arm_left":  ((-56, 122), (-84, 152), (-76, 184)),
        "props": [("wave", 112, 40)],
    },
    "sleep": {
        "eyes": "closed", "mouth": "o", "arms": "down",
        "props": ["zzz"],
    },
    "think": {
        "pupils": (0, -5), "mouth": "flat", "brows": "raise",
        "arm_right": ((56, 122), (80, 150), (26, 160)),
        "arm_left":  ((-56, 122), (-84, 152), (-76, 184)),
    },
    "celebrate": {
        "eyes": "happy", "mouth": "grin", "arms": "up",
        "props": ["confetti"],
    },
    "oops": {
        "pupils": (5, 0), "mouth": "wavy",
        "arm_left":  ((-56, 122), (-100, 130), (-108, 92)),
        "arm_right": ((56, 122), (100, 130), (108, 92)),
        "props": ["sweat"],
    },
    "locked": {
        "mouth": "flat", "brows": "angle",
        "arm_left":  ((-56, 122), (-70, 160), (-20, 186)),
        "arm_right": ((56, 122), (70, 160), (20, 186)),
        "props": ["padlock"],
    },
}


def mascot(d, cx, top, h, arms="up", detail=True, eyes="open", pupils=(0, 0),
           mouth="smile", brows=None, arm_left=None, arm_right=None,
           gloves=True, props=()):
    """Draw the sexiburger. cx = center x, top = dome top y,
    h = total height (~160x230 unit frame). See module docstring for the
    pose rig kwargs."""
    u = h / 230.0

    def X(v):
        return cx + v * u

    def Y(v):
        return top + v * u

    def P(path, name, fill, stroke=INK, sw=4.0, cap="round", op=None):
        kw = dict(fill=fill, stroke=stroke, strokeWidth=max(1.0, sw * u))
        if stroke == "none":
            kw["strokeWidth"] = 0
        if cap:
            kw["cap"] = cap
        if op is not None:
            kw["opacity"] = op
        return d.path(path, name, **kw)

    def EL(vx, vy, w_, h_, name, fill, stroke="none", sw=0.0, op=None):
        kw = dict(x=X(vx) - w_ * u / 2, y=Y(vy) - h_ * u / 2,
                  width=w_ * u, height=h_ * u, fill=fill)
        if stroke != "none":
            kw["stroke"] = stroke
            kw["strokeWidth"] = max(1.0, sw * u)
        else:
            kw["stroke"] = "none"
        if op is not None:
            kw["opacity"] = op
        return d.shape("ellipse", name, **kw)

    def rr(x0, y0, w_, h_, r, name, fill, stroke, sw):
        """Rounded-corner rect in local units (no rounded rect in draw_shape)."""
        p = (f"M{X(x0 + r):.1f},{Y(y0):.1f} L{X(x0 + w_ - r):.1f},{Y(y0):.1f} "
             f"Q{X(x0 + w_):.1f},{Y(y0):.1f} {X(x0 + w_):.1f},{Y(y0 + r):.1f} "
             f"L{X(x0 + w_):.1f},{Y(y0 + h_ - r):.1f} "
             f"Q{X(x0 + w_):.1f},{Y(y0 + h_):.1f} {X(x0 + w_ - r):.1f},{Y(y0 + h_):.1f} "
             f"L{X(x0 + r):.1f},{Y(y0 + h_):.1f} "
             f"Q{X(x0):.1f},{Y(y0 + h_):.1f} {X(x0):.1f},{Y(y0 + h_ - r):.1f} "
             f"L{X(x0):.1f},{Y(y0 + r):.1f} "
             f"Q{X(x0):.1f},{Y(y0):.1f} {X(x0 + r):.1f},{Y(y0):.1f} Z")
        return P(p, name, fill, stroke, sw, cap=None)

    def limb(p0, p1, p2, wb, wt, name, fill=BUN, outline=True):
        """Tapered quad limb: base half-width wb -> tip half-width wt."""
        def norm(a, b):
            dx, dy = b[0] - a[0], b[1] - a[1]
            ln = math.hypot(dx, dy) or 1
            return -dy / ln, dx / ln
        n0 = norm(p0, p1)
        n1 = norm(p1, p2)
        b0l = (p0[0] + n0[0] * wb, p0[1] + n0[1] * wb)
        b0r = (p0[0] - n0[0] * wb, p0[1] - n0[1] * wb)
        t0l = (p2[0] + n1[0] * wt, p2[1] + n1[1] * wt)
        t0r = (p2[0] - n1[0] * wt, p2[1] - n1[1] * wt)
        c1 = (p1[0] + n0[0] * (wb + wt) / 2, p1[1] + n0[1] * (wb + wt) / 2)
        c2 = (p1[0] - n0[0] * (wb + wt) / 2, p1[1] - n0[1] * (wb + wt) / 2)
        dpath = (f"M{X(b0l[0]):.1f},{Y(b0l[1]):.1f} "
                 f"Q{X(c1[0]):.1f},{Y(c1[1]):.1f} {X(t0l[0]):.1f},{Y(t0l[1]):.1f} "
                 f"L{X(t0r[0]):.1f},{Y(t0r[1]):.1f} "
                 f"Q{X(c2[0]):.1f},{Y(c2[1]):.1f} {X(b0r[0]):.1f},{Y(b0r[1]):.1f} Z")
        return P(dpath, name, fill, INK if outline else "none", 3.4, cap=None)

    def glove(vx, vy, mirror, name):
        """White cartoon glove: palm blob + thumb nub."""
        sgn = -1 if mirror else 1
        EL(vx, vy, 30, 26, f"{name} palm", GLOVE, INK, 3.2)
        EL(vx + sgn * 13, vy - 7, 12, 14, f"{name} thumb", GLOVE, INK, 3.0)
        for i in range(3):
            P(f"M{X(vx - sgn * (8 - i * 8)):.1f},{Y(vy - 10):.1f} "
              f"q{sgn * 2 * u:.1f},{-4 * u:.1f} {sgn * 5 * u:.1f},{-6 * u:.1f}",
              f"{name} finger{i}", "none", INK, 2.2)

    def arc(cxu, cyu, r, a0, a1, name, stroke, sw):
        """Stroked arc in local units, angles in degrees (y-down)."""
        x0, y0 = cxu + r * math.cos(math.radians(a0)), cyu + r * math.sin(math.radians(a0))
        x1, y1 = cxu + r * math.cos(math.radians(a1)), cyu + r * math.sin(math.radians(a1))
        am = math.radians((a0 + a1) / 2)
        qx, qy = cxu + r * 1.3 * math.cos(am), cyu + r * 1.3 * math.sin(am)
        P(f"M{X(x0):.1f},{Y(y0):.1f} Q{X(qx):.1f},{Y(qy):.1f} "
          f"{X(x1):.1f},{Y(y1):.1f}", name, "none", stroke, sw)

    # ---- rear tentacles (behind body) --------------------------------------
    limb((-30, 150), (-64, 190), (-92, 208), 13, 6, "leg L2")
    limb((-12, 158), (-22, 196), (-34, 216), 13, 6, "leg L1")
    limb((12, 158), (22, 196), (34, 216), 13, 6, "leg R1")
    limb((30, 150), (64, 190), (92, 208), 13, 6, "leg R2")

    # ---- arms with gloves ----------------------------------------------------
    preset = ARM_PRESETS[arms]
    armL = arm_left if arm_left is not None else preset[0]
    armR = arm_right if arm_right is not None else preset[1]
    gl, gr = gloves if isinstance(gloves, (tuple, list)) else (gloves, gloves)
    limb(*armL, 12, 7, "arm L")
    limb(*armR, 12, 7, "arm R")
    if gl:
        glove(armL[2][0], armL[2][1], True, "glove L")
    if gr:
        glove(armR[2][0], armR[2][1], False, "glove R")

    # ---- body: bottom bun mass ----------------------------------------------
    P(f"M{X(-68):.1f},{Y(112):.1f} "
      f"C{X(-74):.1f},{Y(142):.1f} {X(-62):.1f},{Y(160):.1f} {X(-44):.1f},{Y(170):.1f} "
      f"L{X(44):.1f},{Y(170):.1f} "
      f"C{X(62):.1f},{Y(160):.1f} {X(74):.1f},{Y(142):.1f} {X(68):.1f},{Y(112):.1f} Z",
      "body", BUN, INK, 4.2, cap=None)
    # body shadow wedge (cel)
    P(f"M{X(30):.1f},{Y(120):.1f} C{X(58):.1f},{Y(130):.1f} {X(62):.1f},{Y(150):.1f} "
      f"{X(44):.1f},{Y(164):.1f} L{X(20):.1f},{Y(164):.1f} "
      f"C{X(34):.1f},{Y(146):.1f} {X(36):.1f},{Y(132):.1f} {X(30):.1f},{Y(120):.1f} Z",
      "body shade", BUN_MID, "none", cap=None)

    # ---- fillings: patty / cheese / tomato / lettuce ------------------------
    P(f"M{X(-72):.1f},{Y(94):.1f} L{X(72):.1f},{Y(94):.1f} "
      f"C{X(78):.1f},{Y(94):.1f} {X(80):.1f},{Y(102):.1f} {X(76):.1f},{Y(108):.1f} "
      f"C{X(60):.1f},{Y(114):.1f} {X(-60):.1f},{Y(114):.1f} {X(-76):.1f},{Y(108):.1f} "
      f"C{X(-80):.1f},{Y(102):.1f} {X(-78):.1f},{Y(94):.1f} {X(-72):.1f},{Y(94):.1f} Z",
      "patty", PATTY, INK, 3.6, cap=None)
    # cheese drips over the patty edge
    for i, (vx, dl) in enumerate([(-42, 118), (2, 124), (44, 116)]):
        P(f"M{X(vx - 11):.1f},{Y(98):.1f} L{X(vx + 11):.1f},{Y(98):.1f} "
          f"L{X(vx + 2):.1f},{Y(dl):.1f} Z", f"cheese{i}", CHEESE, INK, 2.6,
          cap=None)
    # tomato band
    P(f"M{X(-76):.1f},{Y(80):.1f} L{X(76):.1f},{Y(80):.1f} L{X(74):.1f},{Y(95):.1f} "
      f"L{X(-74):.1f},{Y(95):.1f} Z", "tomato", TOMATO, INK, 3.2, cap=None)
    # lettuce: wavy frill band
    lett = [(-88, 78), (-66, 88), (-44, 76), (-22, 88), (0, 76),
            (22, 88), (44, 76), (66, 88), (88, 78)]
    lp = f"M{X(-88):.1f},{Y(72):.1f} "
    for i in range(1, len(lett)):
        px_, py_ = lett[i]
        lp += f"Q{X((lett[i-1][0]+px_)/2):.1f},{Y(lett[i-1][1]+10):.1f} {X(px_):.1f},{Y(py_):.1f} "
    lp += (f"L{X(84):.1f},{Y(68):.1f} L{X(-84):.1f},{Y(68):.1f} Z")
    P(lp, "lettuce", LETTUCE, INK, 3.0, cap=None)

    # ---- bun dome -----------------------------------------------------------
    P(f"M{X(-80):.1f},{Y(70):.1f} "
      f"C{X(-80):.1f},{Y(26):.1f} {X(-46):.1f},{Y(2):.1f} {X(0):.1f},{Y(0):.1f} "
      f"C{X(46):.1f},{Y(2):.1f} {X(80):.1f},{Y(26):.1f} {X(80):.1f},{Y(70):.1f} Z",
      "bun dome", BUN, INK, 4.4, cap=None)
    # dome lit crescent + shade wedge (cel)
    P(f"M{X(-64):.1f},{Y(58):.1f} C{X(-66):.1f},{Y(34):.1f} {X(-44):.1f},{Y(14):.1f} "
      f"{X(-18):.1f},{Y(8):.1f} C{X(-38):.1f},{Y(22):.1f} {X(-52):.1f},{Y(42):.1f} "
      f"{X(-56):.1f},{Y(62):.1f} Z", "dome light", "#FFD98A", "none", cap=None)
    P(f"M{X(30):.1f},{Y(6):.1f} C{X(56):.1f},{Y(14):.1f} {X(72):.1f},{Y(36):.1f} "
      f"{X(74):.1f},{Y(66):.1f} L{X(58):.1f},{Y(66):.1f} C{X(58):.1f},{Y(40):.1f} "
      f"{X(48):.1f},{Y(20):.1f} {X(30):.1f},{Y(6):.1f} Z",
      "dome shade", BUN_MID, "none", cap=None)
    # sesame seeds
    seeds = [(-44, 30, -18), (-16, 18, 10), (10, 26, -8), (36, 18, 14),
             (54, 36, -14), (-58, 48, 8), (-26, 44, -12), (2, 50, 16),
             (30, 46, -16), (56, 54, 10)]
    if not detail:
        seeds = seeds[::2]
    for i, (vx, vy, rot) in enumerate(seeds):
        EL(vx, vy, 9, 5, f"seed{i}", SEED)

    # ---- face ---------------------------------------------------------------
    psx, psy = pupils
    if eyes == "open":
        for sgn, vx in [(-1, -22), (1, 22)]:
            EL(vx, 134, 21, 26, f"eye{sgn} white", GLOVE, INK, 3.0)
            EL(vx + sgn * 3 + psx, 137 + psy, 9, 12, f"eye{sgn} pupil", PUPIL)
            EL(vx + sgn * 5 + psx, 133 + psy, 3.6, 4.6, f"eye{sgn} glint",
               "#FFFFFF")
    else:
        # closed: ∪ lids (sleep) ; happy: ∩ arcs (celebrate)
        dy = 9 if eyes == "closed" else -9
        for sgn, vx in [(-1, -22), (1, 22)]:
            P(f"M{X(vx - 10):.1f},{Y(134):.1f} Q{X(vx):.1f},{Y(134 + dy):.1f} "
              f"{X(vx + 10):.1f},{Y(134):.1f}", f"eye{sgn} lid", "none", INK, 3.6)

    if brows == "raise":
        for sgn, vx in [(-1, -22), (1, 22)]:
            P(f"M{X(vx - 9):.1f},{Y(115):.1f} Q{X(vx):.1f},{Y(110):.1f} "
              f"{X(vx + 9):.1f},{Y(115):.1f}", f"brow{sgn}", "none", INK, 2.8)
    elif brows == "angle":
        P(f"M{X(-32):.1f},{Y(110):.1f} L{X(-13):.1f},{Y(117):.1f}",
          "brow L", "none", INK, 3.0)
        P(f"M{X(32):.1f},{Y(110):.1f} L{X(13):.1f},{Y(117):.1f}",
          "brow R", "none", INK, 3.0)

    if mouth == "smile":
        P(f"M{X(-13):.1f},{Y(152):.1f} Q{X(0):.1f},{Y(166):.1f} {X(13):.1f},{Y(152):.1f}",
          "smile", "none", INK, 3.6)
    elif mouth == "grin":
        P(f"M{X(-17):.1f},{Y(150):.1f} Q{X(0):.1f},{Y(157):.1f} {X(17):.1f},{Y(150):.1f} "
          f"Q{X(15):.1f},{Y(169):.1f} {X(0):.1f},{Y(170):.1f} "
          f"Q{X(-15):.1f},{Y(169):.1f} {X(-17):.1f},{Y(150):.1f} Z",
          "grin", PUPIL, INK, 2.8, cap=None)
        EL(0, 165, 14, 6, "tongue", TOMATO)
    elif mouth == "flat":
        P(f"M{X(-10):.1f},{Y(157):.1f} L{X(10):.1f},{Y(157):.1f}",
          "mouth flat", "none", INK, 3.2)
    elif mouth == "wavy":
        P(f"M{X(-14):.1f},{Y(155):.1f} Q{X(-7):.1f},{Y(150):.1f} {X(0):.1f},{Y(155):.1f} "
          f"Q{X(7):.1f},{Y(160):.1f} {X(14):.1f},{Y(155):.1f}",
          "mouth wavy", "none", INK, 3.2)
    elif mouth == "o":
        EL(0, 158, 11, 13, "mouth o", PUPIL, INK, 2.8)

    # ---- polka-dot bow tie ---------------------------------------------------
    kx, ky = 0, 176
    P(f"M{X(kx - 5):.1f},{Y(ky):.1f} L{X(kx - 26):.1f},{Y(ky - 10):.1f} "
      f"L{X(kx - 26):.1f},{Y(ky + 10):.1f} Z", "bow L", BOWTIE, INK, 2.8, cap=None)
    P(f"M{X(kx + 5):.1f},{Y(ky):.1f} L{X(kx + 26):.1f},{Y(ky - 10):.1f} "
      f"L{X(kx + 26):.1f},{Y(ky + 10):.1f} Z", "bow R", BOWTIE, INK, 2.8, cap=None)
    EL(kx, ky, 12, 10, "bow knot", BOWTIE, INK, 2.8)
    if detail:
        for i, (vx, vy) in enumerate([(kx - 18, ky - 4), (kx - 14, ky + 5),
                                      (kx + 16, ky - 5), (kx + 20, ky + 4)]):
            EL(vx, vy, 3.4, 3.4, f"bowdot{i}", BOWTIE_DOT)

    # ---- props (drawn last, on top) -------------------------------------------
    for prop in props:
        name, args = (prop, ()) if isinstance(prop, str) else (prop[0], prop[1:])
        if name == "wave":
            gx, gy = args
            for j, rr_ in enumerate((17, 28)):
                arc(gx, gy, rr_, -80, -15, f"wave{j}", BUN, 4.0)
        elif name == "zzz":
            for i, (zx, zy, zs) in enumerate([(94, 42, 13), (108, 24, 16),
                                              (122, 4, 19)]):
                P(f"M{X(zx):.1f},{Y(zy):.1f} L{X(zx + zs):.1f},{Y(zy):.1f} "
                  f"L{X(zx):.1f},{Y(zy + zs * 0.85):.1f} "
                  f"L{X(zx + zs):.1f},{Y(zy + zs * 0.85):.1f}",
                  f"z{i}", "none", SEED, 4.2)
        elif name == "confetti":
            conf = [(-122, 26, ACCENT, -25), (-104, 4, BOWTIE, 15),
                    (-96, 58, GREEN, 45), (118, 34, WARN, -30),
                    (104, 2, ACCENT, 25), (94, 66, BOWTIE_DOT, -15)]
            for i, (vx, vy, col, rot) in enumerate(conf):
                t = math.radians(rot)
                c, s = math.cos(t), math.sin(t)
                w_, h_ = 12, 5
                pts = []
                for dx, dy in [(-w_/2, -h_/2), (w_/2, -h_/2),
                               (w_/2, h_/2), (-w_/2, h_/2)]:
                    pts.append((vx + dx * c - dy * s, vy + dx * s + dy * c))
                pp = (f"M{X(pts[0][0]):.1f},{Y(pts[0][1]):.1f} " +
                      " ".join(f"L{X(px):.1f},{Y(py):.1f}" for px, py in pts[1:]) + " Z")
                P(pp, f"confetti{i}", col, "none", cap=None)
            EL(-88, 20, 6, 6, "confetti d0", WARN)
            EL(90, 48, 6, 6, "confetti d1", GREEN)
        elif name == "sweat":
            P(f"M{X(-70):.1f},{Y(2):.1f} "
              f"C{X(-61):.1f},{Y(14):.1f} {X(-59):.1f},{Y(20):.1f} {X(-59):.1f},{Y(27):.1f} "
              f"C{X(-59):.1f},{Y(35):.1f} {X(-64):.1f},{Y(39):.1f} {X(-70):.1f},{Y(39):.1f} "
              f"C{X(-76):.1f},{Y(39):.1f} {X(-81):.1f},{Y(35):.1f} {X(-81):.1f},{Y(27):.1f} "
              f"C{X(-81):.1f},{Y(20):.1f} {X(-79):.1f},{Y(14):.1f} {X(-70):.1f},{Y(2):.1f} Z",
              "sweat drop", DROP, INK, 2.8, cap=None)
        elif name == "padlock":
            P(f"M{X(-11):.1f},{Y(188):.1f} C{X(-11):.1f},{Y(166):.1f} "
              f"{X(11):.1f},{Y(166):.1f} {X(11):.1f},{Y(188):.1f}",
              "lock shackle", "none", INK, 5.0)
            rr(-17, 182, 34, 27, 6, "lock body", LOCK, INK, 3.4)
            EL(0, 192, 7, 7, "lock keyhole", PUPIL)
            P(f"M{X(0):.1f},{Y(195):.1f} L{X(0):.1f},{Y(201):.1f}",
              "lock stem", "none", PUPIL, 3.0)

    # rough inked bounds (for layout checks)
    return (cx - 140 * u, top, 280 * u, 230 * u)
