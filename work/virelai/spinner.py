#!/usr/bin/env python3
"""Shared frame machinery for virelai spinner pieces (#1255).

A spinner piece is N transparent 32x32 frames on a uniform Nx1 contact
sheet. Each driver supplies `motif(d, cx, cy, frame)` which draws one
frame's contents centered at (cx, cy); this module emits the per-frame
PNGs (32x32 master + @2x) and the canonical sheet piece
(`<slug>-V1R00.{vectorcraft,svg,@2x.png}` = the grid, in animation order).

Loop rule (style bible): frame N-1 leads into frame 0 with no pop — use
rigid rotation or a periodic ramp, never a partial cycle.
"""
import math

FRAME = 32  # master frame edge; reads at 16


def arc_path(cx, cy, r, a0, a1, step_deg=18):
    """SVG path for a circular arc (y-down, degrees) as quadratic segments.

    Control points sit on the tangent intersection: exact for spans < step.
    """
    a0r, a1r = math.radians(a0), math.radians(a1)
    n = max(1, int(math.ceil(abs(a1r - a0r) / math.radians(step_deg))))
    d = f"M{cx + r * math.cos(a0r):.2f},{cy + r * math.sin(a0r):.2f} "
    for i in range(n):
        s0 = a0r + (a1r - a0r) * i / n
        s1 = a0r + (a1r - a0r) * (i + 1) / n
        mid, half = (s0 + s1) / 2, (s1 - s0) / 2
        q = r / math.cos(half)
        d += (f"Q{cx + q * math.cos(mid):.2f},{cy + q * math.sin(mid):.2f} "
              f"{cx + r * math.cos(s1):.2f},{cy + r * math.sin(s1):.2f} ")
    return d


def new_frame_doc(d, name):
    return d.call("run_command", {"command": "file.new", "params": {
        "name": name, "width": FRAME, "height": FRAME, "units": "Pixels",
        "backgroundContents": "transparent", "colorMode": "rgb"}}, "file.new")


def export_frames(d, slug, frames, motif, out):
    """Render each frame to its own doc and export 1x + 2x PNGs."""
    for f in range(frames):
        new_frame_doc(d, f"{slug} f{f:02d}")
        motif(d, FRAME / 2, FRAME / 2, f)
        for scale, suffix in ((1, ""), (2, "@2x")):
            args = {"path": f"{out}/{slug}-f{f:02d}{suffix}.png",
                    "format": "png"}
            if scale != 1:
                args["scale"] = scale
            r = d.call("export", args, f"export f{f:02d}{suffix}")
            print(f"f{f:02d}{suffix}:", json_short(r))
    return frames


def sheet(d, slug, frames, motif):
    """The canonical piece: Nx1 uniform grid, animation order, transparent."""
    d.call("run_command", {"command": "file.new", "params": {
        "name": f"{slug} contact sheet", "width": FRAME * frames,
        "height": FRAME, "units": "Pixels",
        "backgroundContents": "transparent", "colorMode": "rgb"}}, "file.new")
    for f in range(frames):
        motif(d, FRAME / 2 + FRAME * f, FRAME / 2, f)


def json_short(r):
    import json
    return json.dumps(r)[:140] if r else None
