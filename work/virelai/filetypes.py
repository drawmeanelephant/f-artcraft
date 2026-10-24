#!/usr/bin/env python3
"""Shared file-type icon shapes for #1257 — the GOFILES gutter family.

Register: between chrome glyphs and app icons — document-convention
silhouettes (dog-ear page, familiar glyphs) in the VirelaiChrome stroke
family: geometric, rounded joins, warm-INK outlines, flat fills, ONE
accent hue per family so types differentiate by hue at list scale.

32x32 master on transparent; the primary render is 16-20 px list rows on
alternating light AND dark backgrounds — every shape carries an ink edge
(read on light) around a light fill (read on dark). Detail that died at
16 px in proofing was dropped, not shrunk.

    new_doc(d, "filetype-text-V1R00")
    SHAPES["text"](d)
    d.finish("filetype-text-V1R00")
"""
from vc import NONE
from virelai.vkit import INK, BUN, BUN_MID, BUN_SHADE, NAVY

W = H = 32
WHITE = "#FFFFFF"
SW = 2.4                     # outline weight at master (~1.2 px at 16)

# one accent hue per family (shipped/sampled tokens only)
AMBER = BUN                  # folder family — mascot gold
AMBER_D = BUN_MID
SLATE = "#64748B"            # text lines (LIGHT Muted — reads on white page)
SLATE_L = "#94A3B8"
GREEN = "#22C55E"            # image — shipped Success
TEAL = "#7FD4C8"             # audio — sampled bow-tie dot
RED = "#EF4444"              # document — shipped Danger
CARDBOARD = BUN_SHADE        # archive — "#DA761E" cardboard
TAPE = "#9D4A0D"             # archive tape — sampled deep shade
TERM = "#22C55E"             # binary glyph — terminal green on navy
BLUE = "#3B82F6"             # contact — shipped Accent
DEEP_AMBER = "#F59E0B"       # calendar — shipped Warning
BORDER_D = "#334155"         # dark-theme Border: navy chip's edge


def new_doc(d, slug):
    return d.call("run_command", {"command": "file.new", "params": {
        "name": slug, "width": W, "height": H, "units": "Pixels",
        "backgroundContents": "transparent", "colorMode": "rgb"}},
        "file.new")


def _rrect(x, y, w, h, r):
    """Rounded-rect path (draw_shape has no corner radius)."""
    r = min(r, w / 2, h / 2)
    return (f"M{x+r},{y} L{x+w-r},{y} Q{x+w},{y} {x+w},{y+r} "
            f"L{x+w},{y+h-r} Q{x+w},{y+h} {x+w-r},{y+h} "
            f"L{x+r},{y+h} Q{x},{y+h} {x},{y+h-r} "
            f"L{x},{y+r} Q{x},{y} {x+r},{y} Z")


def _page(x, y, w, h, ear):
    """Dog-ear page outline; returns (page_path, ear_triangle_path)."""
    p = (f"M{x},{y} L{x+w-ear},{y} L{x+w},{y+ear} L{x+w},{y+h} "
         f"L{x},{y+h} Z")
    e = (f"M{x+w-ear},{y} L{x+w},{y+ear} L{x+w-ear},{y+ear} Z")
    return p, e


def _part(d, path_d, label, fill=WHITE, sw=SW):
    d.path(path_d, label, fill=fill, stroke=INK, strokeWidth=sw,
           join="round")


def _page_with_ear(d, x=9, y=5, w=14, h=22, ear=4):
    p, e = _page(x, y, w, h, ear)
    _part(d, p, "page")
    _part(d, e, "ear", fill="#E2E8F0", sw=1.6)


def _line(d, x, y, w, label, color=SLATE, h=1.9):
    d.path(_rrect(x, y, w, h, h / 2), label, fill=color, stroke=NONE)


# --- the family ---------------------------------------------------------------

def folder(d):
    """Tab folder — mascot-gold two-tone, front face overlapping."""
    _part(d, "M4,9.5 Q4,7.5 6,7.5 L11.5,7.5 Q12.8,7.5 13.5,8.6 "
             "L15,10.8 L26,10.8 Q28,10.8 28,12.5 L28,25 "
             "Q28,27 26,27 L6,27 Q4,27 4,25 Z", "back", fill=AMBER_D)
    _part(d, _rrect(4, 13.5, 24, 13.5, 2.5), "front", fill=AMBER)


def folder_open(d):
    """Expanded folder — flap swung down, dark opening behind it."""
    _part(d, "M4,9.5 Q4,7.5 6,7.5 L11.5,7.5 Q12.8,7.5 13.5,8.6 "
             "L15,10.8 L26,10.8 Q28,10.8 28,12.5 L28,24 "
             "Q28,26 26,26 L6,26 Q4,26 4,24 Z", "back", fill=AMBER_D)
    d.path("M5.5,11.8 L26.5,11.8 L26.5,18 L5.5,18 Z",
           "opening", fill=INK, stroke=NONE)
    _part(d, "M4,16 L28,16 L25,26.5 L7,26.5 Z", "flap", fill=AMBER)


def text(d):
    """Generic document — dog-ear page, three slate lines."""
    _page_with_ear(d)
    for i, y in enumerate([13, 17, 21]):
        _line(d, 12, y, 8 if i < 2 else 6, f"line {i+1}")


def image(d):
    """Picture card — frame with peaks + sun, green family."""
    _part(d, _rrect(5, 8, 22, 16, 2.5), "frame")
    d.path("M8.5,21.5 L14,13.5 L18.5,21.5 Z", "peak big",
           fill=GREEN, stroke=NONE)
    d.path("M15.5,21.5 L20,15.8 L25,21.5 Z", "peak small",
           fill=GREEN, stroke=NONE)
    d.shape("ellipse", "sun", x=8.5, y=11, width=4.2, height=4.2,
            fill=WHITE, stroke=INK, strokeWidth=1.8)


def audio(d):
    """Eighth note — teal, chunky head + stem + flag."""
    d.shape("ellipse", "head", x=6.5, y=19.5, width=8, height=6,
            fill=TEAL, stroke=INK, strokeWidth=SW)
    _part(d, _rrect(12.4, 6.5, 2.6, 15, 1.3), "stem", fill=TEAL)
    _part(d, "M15,6.5 Q22,7.5 21.2,14 L18.4,14 "
             "Q19,9.2 15,9 Z", "flag", fill=TEAL)


def document(d):
    """Print-style doc — page + red ribbon band + lines (vs plain text)."""
    _page_with_ear(d)
    _part(d, _rrect(10, 10.5, 12, 4.8, 1.6), "band", fill=RED)
    _line(d, 12, 18.5, 8, "line 1")
    _line(d, 12, 22, 6, "line 2")


def archive(d):
    """Cardboard box — seam + center tape strip."""
    _part(d, _rrect(6, 10, 20, 15, 2), "box", fill=CARDBOARD)
    d.path("M6.5,14 L25.5,14", "seam", fill=NONE, stroke=INK,
           strokeWidth=1.6, cap="round")
    d.path(_rrect(14.4, 10.5, 3.2, 14, 0.8), "tape", fill=TAPE,
           stroke=NONE)
    d.path("M6,10 L10.5,6.5 L21.5,6.5 L26,10", "flaps", fill=CARDBOARD,
           stroke=INK, strokeWidth=SW, join="round")


def binary(d):
    """Terminal chip — navy plate, dark-theme Border edge, green >_ glyph."""
    _part(d, _rrect(5, 8, 22, 16, 4), "chip", fill=NAVY, sw=2)
    # re-edge in the shipped dark Border tone so it separates on dark rows
    d.path(_rrect(5, 8, 22, 16, 4), "chip edge", fill=NONE,
           stroke=BORDER_D, strokeWidth=1.4, join="round")
    d.path("M9.5,12.5 L13.8,15.8 L9.5,19.2", "prompt", fill=NONE,
           stroke=TERM, strokeWidth=2.6, cap="round", join="round")
    d.path("M16.5,19.5 L22,19.5", "cursor", fill=NONE, stroke=TERM,
           strokeWidth=2.6, cap="round")


def contact(d):
    """vCard — landscape card, person glyph + field lines."""
    _part(d, _rrect(5.5, 9, 21, 15, 2.5), "card")
    d.shape("ellipse", "head", x=11, y=12.5, width=5, height=5,
            fill=BLUE, stroke=NONE)
    d.path("M8.6,21 Q13.5,15.8 18.4,21 Z", "shoulders",
           fill=BLUE, stroke=NONE)
    _line(d, 20.5, 13.5, 4.5, "field 1", color=SLATE_L, h=1.7)
    _line(d, 20.5, 17.5, 4.5, "field 2", color=SLATE_L, h=1.7)


def calendar(d):
    """ics page — ring-bound header band + dot grid."""
    _part(d, _rrect(8, 8, 16, 19, 2.2), "page")
    _part(d, _rrect(9, 9.4, 14, 4.8, 1.2), "band", fill=DEEP_AMBER, sw=1.4)
    for i, x in enumerate([12.5, 19.5]):
        d.shape("ellipse", f"ring {i+1}", x=x - 1.6, y=5.6,
                width=3.2, height=3.2, fill=WHITE, stroke=INK,
                strokeWidth=1.8)
    for r, y in enumerate([16, 19.8, 23.6]):
        for c, x in enumerate([10.8, 14.9, 19]):
            d.path(_rrect(x, y, 2.6, 2.2, 0.7), f"dot {r}{c}",
                   fill=SLATE_L, stroke=NONE)


SHAPES = {
    "folder": folder, "folder-open": folder_open, "text": text,
    "image": image, "audio": audio, "document": document,
    "archive": archive, "binary": binary, "contact": contact,
    "calendar": calendar,
}
