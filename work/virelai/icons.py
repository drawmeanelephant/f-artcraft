#!/usr/bin/env python3
"""Shared app-icon shapes for #1248 — the launcher/dock fleet.

Register: above the VirelaiChrome glyph set — same warm-INK stroke family,
fuller character, light cel shading (style-bible §"Two visual registers").
Every icon sits in the shared frame: a navy-family rounded tile (the
WALLPAPER.QOI field stepped one shade lighter) with a soft top sheen, so
the set reads as one family in the launcher grid; the glyph carries the
per-app accent hue on top.

64x64 master on transparent; must read at 24 (dock) and 16 (file rows).
Rule of thumb applied throughout: filled masses and >=3px strokes at
master — detail that died at 16 px in proofing gets dropped, not shrunk.

    new_doc(d, "icon-gofiles-V1R00")
    frame(d)
    SHAPES["gofiles"](d)
    d.finish("icon-gofiles-V1R00")

Every glyph takes (d, ox=0, oy=0) so the contact sheet can re-run the set
on a grid (`draw_sheet_icons.py`).
"""
import math

from vc import NONE, rot_rect_path
from virelai.vkit import DARK, INK, NAVY, BUN, BUN_MID, BUN_SHADE, BUN_DEEP, GLOVE

W = H = 64
SW = 3.0                     # outline weight at master (thin-geometry rule)

# glyph palette — shipped tokens + sampled fixture colors only
PAPER = "#E6EDF3"            # dark-theme Ink: light faces on navy
WHITE = "#FFFFFF"
SLATE = "#94A3B8"            # Muted — metal parts
SLATE_D = "#64748B"
BLUE = DARK["Accent"]        # 3B82F6
BLUE_D = "#2563EB"           # light-theme Accent
BLUE_L = "#BFDBFE"           # light-theme Selection — globe lines
GREEN = DARK["Success"]      # 22C55E
GREEN_D = "#16A34A"
RED = DARK["Danger"]         # EF4444
AMBER = DARK["Warning"]      # F59E0B
GOLD = BUN                   # mascot bun — the house warm accent
TEAL = "#7FD4C8"             # sampled bow-tie dot
CHARCOAL = "#2E3A44"         # dark-theme Rule — dark objects vs navy plate
FIELD = "#23233A"            # plate mid tone — punch-through holes
SURFACE = "#222D35"          # dark Surface — titlebars
SCREEN = "#0F0F1C"           # near-navy screen interiors (wallpaper shadow)
LETTUCE = "#8BC34A"          # mascot filling, sampled
SEED = "#FFF0C2"             # sesame, sampled
PUPIL = "#3A2530"            # mascot eye ink, sampled

PLATE_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#2E2E4A"},
    {"offset": 0.55, "color": "#23233A"},
    {"offset": 1, "color": "#181828"}]}}
SHEEN_GRAD = {"gradient": {"kind": "linear", "stops": [
    {"offset": 0, "color": "#7A7AA8", "opacity": 0.28},
    {"offset": 1, "color": "#7A7AA8", "opacity": 0}]}}


def new_doc(d, slug):
    return d.call("run_command", {"command": "file.new", "params": {
        "name": slug, "width": W, "height": H, "units": "Pixels",
        "backgroundContents": "transparent", "colorMode": "rgb"}},
        "file.new")


def _rr(x, y, w, h, r):
    """Rounded-rect path (draw_shape has no corner radius)."""
    r = min(r, w / 2, h / 2)
    return (f"M{x+r},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} "
            f"L{x+w},{y+h-r} Q{x+w},{y+h} {x+w-r},{y+h} "
            f"L{x+r},{y+h} Q{x},{y+h} {x},{y+h-r} "
            f"L{x},{y+r} Q{x},{y} {x+r},{y} Z")


def _star4(cx, cy, r, rin=None):
    """Four-point sparkle; r = tip radius."""
    rin = rin if rin is not None else r * 0.34
    return (f"M{cx},{cy-r} C{cx+rin},{cy-rin} {cx+rin},{cy-rin} {cx+r},{cy} "
            f"C{cx+rin},{cy+rin} {cx+rin},{cy+rin} {cx},{cy+r} "
            f"C{cx-rin},{cy+rin} {cx-rin},{cy+rin} {cx-r},{cy} "
            f"C{cx-rin},{cy-rin} {cx-rin},{cy-rin} {cx},{cy-r} Z")


def frame(d, ox=0, oy=0):
    """The shared icon tile: navy-family squircle + ink edge + top sheen."""
    d.path(_rr(ox + 4, oy + 4, 56, 56, 14), "plate",
           fill=PLATE_GRAD, stroke=INK, strokeWidth=SW, join="round")
    d.path(_rr(ox + 10, oy + 8, 44, 18, 8), "sheen",
           fill=SHEEN_GRAD, stroke=NONE)


def _part(d, path_d, label, fill=PAPER, sw=SW, stroke=INK):
    d.path(path_d, label, fill=fill, stroke=stroke, strokeWidth=sw,
           join="round")


def _dot(d, cx, cy, r, label, fill, sw=0, stroke=NONE):
    d.shape("ellipse", label, x=cx - r, y=cy - r, width=2 * r,
            height=2 * r, fill=fill, stroke=stroke, strokeWidth=sw)


def _s(d, path_d, label, color, w, **kw):
    """Stroked detail line — round caps/joins per the chrome rule."""
    a = dict(fill=NONE, stroke=color, strokeWidth=w, cap="round",
             join="round")
    a.update(kw)
    d.path(path_d, label, **a)


def _band(d, path_d, label, color, w, edge=INK):
    """Two-pass stroke: ink-edged band (reads as a fill at small size)."""
    _s(d, path_d, f"{label} edge", edge, w + 2.2)
    _s(d, path_d, label, color, w)


# --- wave 1: core desk --------------------------------------------------------

def gocalc(d, ox=0, oy=0):
    """GOCALC — calculator: paper body, dark screen, amber equals bar."""
    _part(d, _rr(ox + 21, oy + 13, 22, 38, 5), "body")
    _part(d, _rr(ox + 25, oy + 17.5, 14, 7.5, 2), "screen",
          fill=SCREEN, sw=2)
    for r_, y in enumerate([30.5, 35.5]):
        for c_, x in enumerate([27, 32, 37]):
            _dot(d, ox + x, oy + y, 2.1, f"btn {r_}{c_}", INK)
    _part(d, _rr(ox + 27, oy + 41, 10, 4.5, 2.2), "equals",
          fill=AMBER, sw=1.8)


def note(d, ox=0, oy=0):
    """NOTE — dog-ear page with a pencil laid across it."""
    _part(d, f"M{ox+20},{oy+13} L{ox+36},{oy+13} L{ox+42},{oy+19} "
             f"L{ox+42},{oy+49} L{ox+20},{oy+49} Z", "page")
    _part(d, f"M{ox+36},{oy+13} L{ox+42},{oy+19} L{ox+36},{oy+19} Z",
          "ear", fill="#CBD5E1", sw=1.8)
    for i, y in enumerate([25, 30, 35]):
        d.path(_rr(ox + 23.5, oy + y, 12 if i < 2 else 8, 2.4, 1.2),
               f"line {i+1}", fill=SLATE_D, stroke=NONE)
    # pencil: amber body on the diagonal, wood collar, ink point
    _part(d, rot_rect_path(ox + 38, oy + 38.5, 21, 6.5, -45), "pencil",
          fill=AMBER, sw=2.4)
    _part(d, f"M{ox+27},{oy+49.5} L{ox+30.5},{oy+43} L{ox+35},{oy+46.5} Z",
          "pencil tip", fill=PUPIL, sw=1.6)


def goedit(d, ox=0, oy=0):
    """GOEDIT — code brackets: teal chevrons, amber slash."""
    _s(d, f"M{ox+26},{oy+22} L{ox+17},{oy+32} L{ox+26},{oy+42}",
       "left bracket", TEAL, 5.5)
    _s(d, f"M{ox+38},{oy+22} L{ox+47},{oy+32} L{ox+38},{oy+42}",
       "right bracket", TEAL, 5.5)
    _s(d, f"M{ox+35.5},{oy+19} L{ox+28.5},{oy+45}", "slash", AMBER, 5)


def gofiles(d, ox=0, oy=0):
    """GOFILES — tab folder, mascot-gold two-tone (echoes filetype-folder)."""
    _part(d, f"M{ox+14},{oy+19} Q{ox+14},{oy+16} {ox+17},{oy+16} "
             f"L{ox+26},{oy+16} Q{ox+28},{oy+16} {ox+29},{oy+17.5} "
             f"L{ox+31},{oy+20} L{ox+47},{oy+20} Q{ox+50},{oy+20} "
             f"{ox+50},{oy+23} L{ox+50},{oy+44} Q{ox+50},{oy+46} "
             f"{ox+47},{oy+46} L{ox+17},{oy+46} Q{ox+14},{oy+46} "
             f"{ox+14},{oy+44} Z", "back", fill=BUN_MID)
    _part(d, _rr(ox + 14, oy + 25, 36, 21, 4), "front", fill=GOLD)


def goterm(d, ox=0, oy=0):
    """GOTERM — dark console window, green prompt + cursor."""
    _part(d, _rr(ox + 13, oy + 17, 38, 30, 5), "window", fill=SCREEN)
    _s(d, f"M{ox+19},{oy+25} L{ox+26},{oy+30} L{ox+19},{oy+35}",
       "prompt", GREEN, 4.5)
    _s(d, f"M{ox+29},{oy+38.5} L{ox+39},{oy+38.5}", "cursor", GREEN, 4.5)


def web(d, ox=0, oy=0):
    """WEB — globe: accent-blue sphere, light meridian + equator."""
    _dot(d, ox + 32, oy + 32, 16, "sphere", BLUE, sw=SW, stroke=INK)
    # cel light wedge, upper left
    d.path(f"M{ox+20.5},{oy+24} C{ox+23},{oy+19} {ox+29},{oy+16.5} "
           f"{ox+34},{oy+17} C{ox+28},{oy+19} {ox+24},{oy+21.5} "
           f"{ox+22},{oy+27} Z", "sphere light", fill="#7FB3FA",
           stroke=NONE)
    d.shape("ellipse", "meridian", x=ox + 27.5, y=oy + 17, width=9,
            height=30, fill=NONE, stroke=BLUE_L, strokeWidth=3)
    _s(d, f"M{ox+17},{oy+32} L{ox+47},{oy+32}", "equator", BLUE_L, 3)


def pulse(d, ox=0, oy=0):
    """PULSE — heartbeat trace, success-green, one bold polyline."""
    _s(d, f"M{ox+15},{oy+34} L{ox+23},{oy+34} L{ox+28},{oy+22} "
          f"L{ox+34},{oy+46} L{ox+39},{oy+30} L{ox+43},{oy+34} "
          f"L{ox+50},{oy+34}", "trace", GREEN, 5)


def gotop(d, ox=0, oy=0):
    """GOTOP — gauge: slate arc band with red zone, amber needle."""
    _band(d, f"M{ox+17},{oy+42} Q{ox+32},{oy+18} {ox+47},{oy+42}",
          "dial", SLATE, 6)
    _s(d, f"M{ox+42},{oy+27.5} Q{ox+46.5},{oy+33} {ox+47},{oy+40}",
       "red zone", RED, 6)
    _s(d, f"M{ox+32},{oy+38} L{ox+41},{oy+27}", "needle", AMBER, 4.5)
    _dot(d, ox + 32, oy + 39, 4, "hub", PAPER, sw=2.2, stroke=INK)


def goa11y(d, ox=0, oy=0):
    """GOA11Y — universal access figure, paper on accent disc."""
    _dot(d, ox + 32, oy + 32, 16, "disc", BLUE, sw=SW, stroke=INK)
    _dot(d, ox + 32, oy + 23.5, 2.8, "head", PAPER)
    _part(d, _rr(ox + 21, oy + 27, 22, 4.5, 2.2), "arms", sw=0,
          stroke=NONE)
    _part(d, _rr(ox + 30, oy + 29, 4, 9, 2), "torso", sw=0, stroke=NONE)
    _part(d, rot_rect_path(ox + 29.5, oy + 40.5, 4, 9, 14), "leg L",
          sw=0, stroke=NONE)
    _part(d, rot_rect_path(ox + 34.5, oy + 40.5, 4, 9, -14), "leg R",
          sw=0, stroke=NONE)


# --- wave 2: system -----------------------------------------------------------

def gosh(d, ox=0, oy=0):
    """GOSH — scallop shell: mascot-gold fan, warm ribs (not a second
    terminal — the shell is a seashell)."""
    _part(d, f"M{ox+32},{oy+50} "
             f"C{ox+22},{oy+44} {ox+14},{oy+36} {ox+14},{oy+27} "
             f"C{ox+14},{oy+20} {ox+20},{oy+14} {ox+26},{oy+14} "
             f"C{ox+29},{oy+14} {ox+31},{oy+15} {ox+32},{oy+17} "
             f"C{ox+33},{oy+15} {ox+35},{oy+14} {ox+38},{oy+14} "
             f"C{ox+44},{oy+14} {ox+50},{oy+20} {ox+50},{oy+27} "
             f"C{ox+50},{oy+36} {ox+42},{oy+44} {ox+32},{oy+50} Z",
          "shell", fill=GOLD)
    for i, (tx, ty) in enumerate([(20, 21), (26, 16.5), (32, 16),
                                  (38, 16.5), (44, 21)]):
        _s(d, f"M{ox+32},{oy+47.5} L{ox+tx},{oy+ty}", f"rib {i+1}",
           BUN_SHADE, 2.4)
    _part(d, _rr(ox + 28.5, oy + 47, 7, 4.5, 2), "hinge",
          fill=BUN_MID, sw=2)


def gohelp(d, ox=0, oy=0):
    """GOHELP — lifebuoy: white ring, red diagonal straps."""
    _dot(d, ox + 32, oy + 32, 15, "ring", PAPER, sw=SW, stroke=INK)
    for i, deg in enumerate([45, -45]):
        _part(d, rot_rect_path(ox + 32, oy + 32, 32, 7, deg),
              f"strap {i+1}", fill=RED, sw=2)
    _dot(d, ox + 32, oy + 32, 7, "hole", FIELD, sw=2.5, stroke=INK)


def gowelcome(d, ox=0, oy=0):
    """GOWELCOME — waving mascot bust: bun dome, lettuce frill, glove."""
    # glove up first (behind dome edge), waving
    _dot(d, ox + 48, oy + 22, 4.6, "glove", GLOVE, sw=2.6, stroke=INK)
    _dot(d, ox + 52.4, oy + 19.4, 2.2, "glove thumb", GLOVE, sw=2,
         stroke=INK)
    _s(d, f"M{ox+54},{oy+26} Q{ox+56.5},{oy+22} {ox+55.5},{oy+17.5}",
       "wave 1", PAPER, 2.6)
    _s(d, f"M{ox+49},{oy+14.5} Q{ox+52},{oy+12} {ox+55.5},{oy+13}",
       "wave 2", PAPER, 2.6)
    # dome
    _part(d, f"M{ox+17},{oy+40} C{ox+17},{oy+25} {ox+23},{oy+16.5} "
             f"{ox+32},{oy+16.5} C{ox+41},{oy+16.5} {ox+47},{oy+25} "
             f"{ox+47},{oy+40} Z", "dome", fill=GOLD, sw=3.2)
    d.path(f"M{ox+21},{oy+30} C{ox+23},{oy+23} {ox+28},{oy+19.5} "
           f"{ox+33},{oy+19} C{ox+28},{oy+21.5} {ox+24.5},{oy+25.5} "
           f"{ox+23.5},{oy+31} Z", "dome light", fill="#FFD98A",
           stroke=NONE)
    for i, (sx, sy) in enumerate([(26, 22), (35, 20.5), (41, 26)]):
        d.shape("ellipse", f"seed {i+1}", x=ox + sx - 1.8, y=oy + sy - 1,
                width=3.6, height=2, fill=SEED, stroke=NONE)
    # lettuce frill at the dome base
    _part(d, f"M{ox+17},{oy+37} L{ox+47},{oy+37} L{ox+47},{oy+41} "
             f"Q{ox+44},{oy+46.5} {ox+41},{oy+41.5} "
             f"Q{ox+38},{oy+46.5} {ox+35},{oy+41.5} "
             f"Q{ox+32},{oy+46.5} {ox+29},{oy+41.5} "
             f"Q{ox+26},{oy+46.5} {ox+23},{oy+41.5} "
             f"Q{ox+20},{oy+46.5} {ox+17},{oy+41} Z",
          "lettuce", fill=LETTUCE, sw=2.6)
    # face: big cartoon eyes + grin on the dome
    for i, ex in enumerate([26, 38]):
        d.shape("ellipse", f"eye {i+1}", x=ox + ex - 3.4, y=oy + 25.5,
                width=6.8, height=8, fill=WHITE, stroke=INK,
                strokeWidth=2.4)
        _dot(d, ox + ex + 0.6, oy + 31, 2.1, f"pupil {i+1}", PUPIL)
    _s(d, f"M{ox+26.5},{oy+36.5} Q{ox+32},{oy+39.5} {ox+37.5},{oy+36.5}",
       "smile", INK, 2.6)


def goset(d, ox=0, oy=0):
    """GOSET — gear: 8 teeth under an inked disc (protruding edges keep
    the ink; no internal seams), punched hub."""
    for i in range(8):
        a = math.radians(i * 45)
        _part(d, rot_rect_path(ox + 32 + 13 * math.cos(a),
                               oy + 32 + 13 * math.sin(a), 9, 8, i * 45),
              f"tooth {i+1}", fill=SLATE, sw=2.6)
    _dot(d, ox + 32, oy + 32, 13, "disc", SLATE, sw=SW, stroke=INK)
    d.path(f"M{ox+22},{oy+30} C{ox+24},{oy+24} {ox+29},{oy+20.5} "
           f"{ox+34},{oy+20.5} C{ox+29},{oy+22.5} {ox+25.5},{oy+25.5} "
           f"{ox+24},{oy+31} Z", "disc light", fill="#C3CEDA", stroke=NONE)
    _dot(d, ox + 32, oy + 32, 5.5, "hub", FIELD, sw=2.4, stroke=INK)


def goview(d, ox=0, oy=0):
    """GOVIEW — landscape card: teal sky, two green peaks, gold sun."""
    _part(d, _rr(ox + 14, oy + 17, 36, 30, 5), "frame",
          fill={"gradient": {"kind": "linear", "stops": [
              {"offset": 0, "color": "#BFEBE0"},
              {"offset": 1, "color": "#63BFB4"}]}})
    d.path(f"M{ox+17},{oy+42} L{ox+27},{oy+28} L{ox+37},{oy+42} Z",
           "peak big", fill=GREEN_D, stroke=NONE)
    d.path(f"M{ox+29},{oy+42} L{ox+37},{oy+32} L{ox+46},{oy+42} Z",
           "peak small", fill="#1F7A4D", stroke=NONE)
    _dot(d, ox + 40, oy + 24.5, 3.4, "sun", GOLD, sw=1.8, stroke=INK)
    _s(d, f"M{ox+15.5},{oy+42} L{ox+48.5},{oy+42}", "ground",
       "#1F7A4D", 2.4)


def gosound(d, ox=0, oy=0):
    """GOSOUND — speaker cone + two teal wave arcs."""
    _part(d, f"M{ox+18},{oy+27} L{ox+26},{oy+27} L{ox+37},{oy+19} "
             f"L{ox+37},{oy+45} L{ox+26},{oy+37} L{ox+18},{oy+37} Z",
          "speaker")
    _s(d, f"M{ox+42},{oy+27} Q{ox+46},{oy+32} {ox+42},{oy+37}",
       "wave in", TEAL, 4)
    _s(d, f"M{ox+46.5},{oy+23} Q{ox+52.5},{oy+32} {ox+46.5},{oy+41}",
       "wave out", TEAL, 4)


def gostore(d, ox=0, oy=0):
    """GOSTORE — shopping bag: gold trapezoid, ink handle, teal brand dot."""
    _part(d, f"M{ox+22},{oy+22} L{ox+42},{oy+22} L{ox+45.5},{oy+48} "
             f"L{ox+18.5},{oy+48} Z", "bag", fill=GOLD)
    _s(d, f"M{ox+26},{oy+24} C{ox+26},{oy+16.5} {ox+28.5},{oy+14} "
          f"{ox+32},{oy+14} C{ox+35.5},{oy+14} {ox+38},{oy+16.5} "
          f"{ox+38},{oy+24}", "handle", INK, 4)
    _dot(d, ox + 32, oy + 35, 2.6, "brand dot", TEAL)


def gosnap(d, ox=0, oy=0):
    """GOSNAP — camera: slate body + hump, navy lens with glass glint."""
    _part(d, _rr(ox + 24, oy + 16, 12, 7, 2.5), "hump", fill=SLATE,
          sw=2.6)
    _part(d, _rr(ox + 13, oy + 21, 38, 26, 5), "body", fill=SLATE)
    _dot(d, ox + 32, oy + 34, 9, "lens", SCREEN, sw=SW, stroke=INK)
    _dot(d, ox + 32, oy + 34, 4.6, "glass", "#1E40AF")
    _dot(d, ox + 29.6, oy + 31.4, 1.7, "glint", WHITE)
    _part(d, _rr(ox + 42, oy + 18.5, 6, 4.5, 2), "shutter", fill=RED,
          sw=2)


def tabwm(d, ox=0, oy=0):
    """TABWM — tabbed window: ghost window behind, paper front with a
    tab bump on a Surface-dark titlebar (the fallback desktop)."""
    _part(d, _rr(ox + 21, oy + 14, 29, 22, 4), "back window",
          fill=SLATE_D, sw=2.6)
    _part(d, _rr(ox + 14, oy + 23, 36, 26, 5), "front")
    d.path(f"M{ox+19},{oy+23} L{ox+45},{oy+23} Q{ox+50},{oy+23} "
           f"{ox+50},{oy+28} L{ox+50},{oy+31} L{ox+14},{oy+31} "
           f"L{ox+14},{oy+28} Q{ox+14},{oy+23} {ox+19},{oy+23} Z",
           "titlebar", fill=SURFACE, stroke=NONE)
    _part(d, _rr(ox + 18, oy + 19, 13, 7, 3), "tab", sw=2.2)
    _dot(d, ox + 44, oy + 27, 1.8, "close", "#F1F5F9")
    for i, (y, w_) in enumerate([(36.5, 21), (42, 14)]):
        d.path(_rr(ox + 18, oy + y, w_, 2.6, 1.3), f"line {i+1}",
               fill=SLATE_D, stroke=NONE)


# --- wave 3: life -------------------------------------------------------------

def gostalgia(d, ox=0, oy=0):
    """GOSTALGIA — retro computer: paper CRT, dark screen, green dash."""
    _part(d, _rr(ox + 17, oy + 14, 30, 24, 4), "crt")
    _part(d, _rr(ox + 21, oy + 18, 22, 13, 2), "screen", fill=SCREEN,
          sw=2)
    _s(d, f"M{ox+24.5},{oy+26.5} L{ox+31},{oy+26.5}", "dash", GREEN, 3)
    _part(d, _rr(ox + 28, oy + 38, 8, 4.5, 1.5), "neck", fill=SLATE_D,
          sw=2)
    _part(d, _rr(ox + 21, oy + 42.5, 22, 4.5, 2), "foot", sw=2.4)


def goinfer(d, ox=0, oy=0):
    """GOINFER — neural sparkle: big teal four-star + small companions."""
    _part(d, _star4(ox + 32, oy + 32, 17, 5.6), "star big", fill=TEAL)
    _part(d, _star4(ox + 20, oy + 44.5, 6, 2.1), "star small", fill=PAPER,
          sw=2.2)
    _dot(d, ox + 46, oy + 19, 2.2, "mote", PAPER)


def gorec(d, ox=0, oy=0):
    """GOREC — microphone: slate capsule, ink-edged cradle, red rec dot."""
    _band(d, f"M{ox+20},{oy+28} C{ox+20},{oy+38.5} {ox+26},{oy+42.5} "
             f"{ox+32},{oy+42.5} C{ox+38},{oy+42.5} {ox+44},{oy+38.5} "
             f"{ox+44},{oy+28}", "cradle", SLATE, 4)
    _part(d, _rr(ox + 26, oy + 13, 12, 21, 6), "capsule", fill=SLATE)
    _dot(d, ox + 32, oy + 19.5, 2.1, "rec", RED)
    _part(d, _rr(ox + 30.5, oy + 42.5, 3, 4.5, 1.2), "stem", fill=SLATE,
          sw=2)
    _part(d, _rr(ox + 24, oy + 47, 16, 4, 2), "base", fill=SLATE, sw=2.2)


def goassist(d, ox=0, oy=0):
    """GOASSIST — assistant face: paper bot head, antenna, ink features."""
    _s(d, f"M{ox+32},{oy+18} L{ox+32},{oy+12.5}", "antenna", INK, 3)
    _dot(d, ox + 32, oy + 11.5, 2.6, "antenna tip", BLUE, sw=1.8,
         stroke=INK)
    _part(d, _rr(ox + 13, oy + 28, 5, 8, 2), "ear L", fill=SLATE, sw=2.2)
    _part(d, _rr(ox + 46, oy + 28, 5, 8, 2), "ear R", fill=SLATE, sw=2.2)
    _part(d, _rr(ox + 17, oy + 18, 30, 28, 8), "head")
    _dot(d, ox + 26, oy + 29, 3.1, "eye L", INK)
    _dot(d, ox + 38, oy + 29, 3.1, "eye R", INK)
    _dot(d, ox + 27, oy + 28, 1.1, "glint L", WHITE)
    _dot(d, ox + 39, oy + 28, 1.1, "glint R", WHITE)
    _s(d, f"M{ox+26},{oy+37} Q{ox+32},{oy+41} {ox+38},{oy+37}",
       "smile", INK, 3)


def gosheet(d, ox=0, oy=0):
    """GOSHEET — spreadsheet: paper table, green header, grid + active cell."""
    _part(d, _rr(ox + 15, oy + 17, 34, 30, 4), "page")
    d.path(f"M{ox+19},{oy+17} L{ox+45},{oy+17} Q{ox+49},{oy+17} "
           f"{ox+49},{oy+21} L{ox+49},{oy+24} L{ox+15},{oy+24} "
           f"L{ox+15},{oy+21} Q{ox+15},{oy+17} {ox+19},{oy+17} Z",
           "header", fill=GREEN, stroke=NONE)
    for i, x in enumerate([26.3, 37.6]):
        d.path(_rr(ox + x, oy + 24, 1.5, 23, 0.7), f"col {i+1}",
               fill=SLATE_D, stroke=NONE)
    for i, y in enumerate([31.7, 39.3]):
        d.path(_rr(ox + 15, oy + y, 34, 1.5, 0.7), f"row {i+1}",
               fill=SLATE_D, stroke=NONE)
    d.path(_rr(ox + 17.5, oy + 26.5, 7, 4, 1), "cell A1",
           fill=BLUE_L, stroke=NONE)


def goreader(d, ox=0, oy=0):
    """GOREADER — open book: deep-warm cover, paper spread, ink spine."""
    _part(d, f"M{ox+15},{oy+19} C{ox+21},{oy+15} {ox+27},{oy+15} "
             f"{ox+32},{oy+18.5} C{ox+37},{oy+15} {ox+43},{oy+15} "
             f"{ox+49},{oy+19} L{ox+49},{oy+46} C{ox+43},{oy+43} "
             f"{ox+37},{oy+43} {ox+32},{oy+46} C{ox+27},{oy+43} "
             f"{ox+21},{oy+43} {ox+15},{oy+46} Z", "cover",
          fill=BUN_DEEP, sw=2.8)
    _part(d, f"M{ox+18},{oy+21.5} C{ox+23},{oy+18.5} {ox+28},{oy+18.5} "
             f"{ox+32},{oy+21} C{ox+36},{oy+18.5} {ox+41},{oy+18.5} "
             f"{ox+46},{oy+21.5} L{ox+46},{oy+42.5} C{ox+41},{oy+40} "
             f"{ox+36},{oy+40} {ox+32},{oy+42.5} C{ox+28},{oy+40} "
             f"{ox+23},{oy+40} {ox+18},{oy+42.5} Z", "pages", sw=2.4)
    _s(d, f"M{ox+32},{oy+20.5} L{ox+32},{oy+42}", "spine", INK, 2.4)
    for i, y in enumerate([26, 31]):
        d.path(_rr(ox + 22, oy + y, 6.5, 1.8, 0.9), f"line L{i+1}",
               fill=SLATE_D, stroke=NONE)
        d.path(_rr(ox + 35.5, oy + y, 6.5, 1.8, 0.9), f"line R{i+1}",
               fill=SLATE_D, stroke=NONE)


def goclock(d, ox=0, oy=0):
    """GOCLOCK — clock at 10:10: paper face, ink hands, amber second."""
    _dot(d, ox + 32, oy + 32, 15, "face", PAPER, sw=3.4, stroke=INK)
    for i, (tx, ty) in enumerate([(32, 20), (44, 32), (32, 44),
                                  (20, 32)]):
        _dot(d, ox + tx, oy + ty, 1.6, f"tick {i+1}", INK)
    _s(d, f"M{ox+32},{oy+32} L{ox+40},{oy+24.5}", "minute", INK, 4)
    _s(d, f"M{ox+32},{oy+32} L{ox+25.5},{oy+26}", "hour", INK, 4)
    _s(d, f"M{ox+32},{oy+33.5} L{ox+38},{oy+39}", "second", AMBER, 2.2)
    _dot(d, ox + 32, oy + 32, 2.4, "pin", INK)


def gomine(d, ox=0, oy=0):
    """GOMINE — round bomb: charcoal body, fuse curve, gold spark."""
    _s(d, f"M{ox+39},{oy+23} C{ox+42.5},{oy+17.5} {ox+46},{oy+15.5} "
          f"{ox+48},{oy+17}", "fuse", INK, 3)
    _part(d, _star4(ox + 49, oy + 14, 5.5, 1.9), "spark", fill=GOLD,
          sw=2)
    _dot(d, ox + 30, oy + 36, 13, "body", CHARCOAL, sw=3.4, stroke=INK)
    _part(d, _rr(ox + 36.5, oy + 21, 6, 5, 1.6), "cap", fill=SLATE_D,
          sw=2.2)
    d.shape("ellipse", "sheen", x=ox + 22.5, y=oy + 27.5, width=7,
            height=4.5, fill="#4A5568", stroke=NONE, opacity=70)


def gosol(d, ox=0, oy=0):
    """GOSOL — playing cards: red back card, paper front with heart pip."""
    _part(d, rot_rect_path(ox + 27, oy + 33, 20, 28, -12), "card back",
          fill=RED)
    _part(d, rot_rect_path(ox + 37, oy + 32, 20, 28, 10), "card front")
    _part(d, f"M{ox+37},{oy+36.5} "
             f"C{ox+33.5},{oy+33.5} {ox+33},{oy+30.5} {ox+35.3},{oy+29.4} "
             f"C{ox+36.5},{oy+28.8} {ox+37},{oy+29.4} {ox+37},{oy+30.2} "
             f"C{ox+37},{oy+29.4} {ox+37.5},{oy+28.8} {ox+38.7},{oy+29.4} "
             f"C{ox+41},{oy+30.5} {ox+40.5},{oy+33.5} {ox+37},{oy+36.5} Z",
          "heart", fill=RED, sw=1.6)


def goemoji(d, ox=0, oy=0):
    """GOEMOJI — smiley: mascot-gold face, cel shade, ink grin."""
    _dot(d, ox + 32, oy + 32, 15, "face", GOLD, sw=3.4, stroke=INK)
    d.path(f"M{ox+39},{oy+42} C{ox+44},{oy+38} {ox+46},{oy+31} "
           f"{ox+45},{oy+25} C{ox+44},{oy+33} {ox+41},{oy+38.5} "
           f"{ox+36},{oy+41.5} Z", "shade", fill=BUN_MID, stroke=NONE)
    for i, ex in enumerate([26.5, 37.5]):
        d.shape("ellipse", f"eye {i+1}", x=ox + ex - 2.4, y=oy + 26.5,
                width=4.8, height=6, fill=INK, stroke=NONE)
    _s(d, f"M{ox+24},{oy+36} Q{ox+32},{oy+43.5} {ox+40},{oy+36}",
       "grin", INK, 4.5)


def goirc(d, ox=0, oy=0):
    """GOIRC — chat bubble: teal bubble with tail, three white dots."""
    _part(d, f"M{ox+24},{oy+17} L{ox+40},{oy+17} Q{ox+49},{oy+17} "
             f"{ox+49},{oy+26} L{ox+49},{oy+32} Q{ox+49},{oy+41} "
             f"{ox+40},{oy+41} L{ox+31},{oy+41} L{ox+21},{oy+49} "
             f"L{ox+23.5},{oy+41} L{ox+24},{oy+41} Q{ox+15},{oy+41} "
             f"{ox+15},{oy+32} L{ox+15},{oy+26} Q{ox+15},{oy+17} "
             f"{ox+24},{oy+17} Z", "bubble", fill=TEAL)
    for i, x in enumerate([24, 32, 40]):
        _dot(d, ox + x, oy + 29, 2.7, f"dot {i+1}", WHITE)


def govault(d, ox=0, oy=0):
    """GOVAULT — safe: slate door, dark dial with spokes, lever handle."""
    _part(d, _rr(ox + 15, oy + 16, 34, 33, 4), "safe", fill=SLATE_D)
    _part(d, _rr(ox + 19, oy + 20, 26, 25, 3), "door", fill="#CBD5E1",
          sw=2.4)
    _dot(d, ox + 28, oy + 32.5, 6.2, "dial", SCREEN, sw=2.6, stroke=INK)
    for i in range(3):
        a = math.radians(-90 + i * 120)
        _s(d, f"M{ox+28},{oy+32.5} "
              f"L{ox+28 + 5 * math.cos(a)},{oy+32.5 + 5 * math.sin(a)}",
           f"spoke {i+1}", SLATE, 1.8)
    _part(d, _rr(ox + 38, oy + 28.5, 4, 8, 2), "handle", fill=SCREEN,
          sw=2.2)


def gomail(d, ox=0, oy=0):
    """GOMAIL — envelope: paper body, ink flap chevron."""
    _part(d, _rr(ox + 13, oy + 20, 38, 26, 5), "envelope")
    _s(d, f"M{ox+14},{oy+21.5} L{ox+32},{oy+35} L{ox+50},{oy+21.5}",
       "flap", INK, 3)


SHAPES = {
    "gocalc": gocalc, "note": note, "goedit": goedit, "gofiles": gofiles,
    "goterm": goterm, "web": web, "pulse": pulse, "gosh": gosh,
    "gohelp": gohelp, "gowelcome": gowelcome, "gotop": gotop,
    "goset": goset, "goview": goview, "gosound": gosound,
    "gostalgia": gostalgia, "gostore": gostore, "goinfer": goinfer,
    "gorec": gorec, "gosnap": gosnap, "goassist": goassist,
    "gosheet": gosheet, "goreader": goreader, "goclock": goclock,
    "gomine": gomine, "gosol": gosol, "goemoji": goemoji, "goirc": goirc,
    "govault": govault, "gomail": gomail, "goa11y": goa11y,
    "tabwm": tabwm,
}

# checklist order from the issue: core desk, system, life
ORDER = [
    "gofiles", "goedit", "goterm", "web", "note", "gocalc", "gotop",
    "goa11y", "pulse",
    "gosh", "gohelp", "gowelcome", "goset", "goview", "gosound",
    "gostore", "gosnap", "tabwm",
    "gostalgia", "goinfer", "gorec", "goassist", "gosheet", "goreader",
    "goclock", "gomine", "gosol", "goemoji", "goirc", "govault", "gomail",
]
assert sorted(ORDER) == sorted(SHAPES), "ORDER and SHAPES must cover the same 31"
