## Golden Week V1R00 — ground bands must be built ON the disc arc, not clipped by it

- Kind: lesson
- Source: #991, `work/holidays/draw_golden_week.py`,
  `art/holidays/golden-week/` native and proof
- Applies to: festival seals / any plate with a ground or horizon inside the disc
- Status: pending

### Evidence

First pass drew the spring hills as ordinary wavy paths ending in a
straight "below the canvas" return edge (`L880,880 Q500,906 120,880 Z`).
On a rectangular canvas that idiom is safe; inside a circular plate it
left ~175k px outside r430 and `check_rim.py` failed the proof. The fix
was to make the rim do the closing: `rim_hill()` walks the inner disc arc
(r = PR-4) over the angle range the hill should occupy, then walks back
along a crest whose depth is `depth_mid * sin(pi*t)**0.8`, so the crest
automatically lands exactly on the rim at both ends — no clipping mask,
no spill. Wobble frequency matters: `sin(phase + i*2.4)` produced a
jagged grass-blade crest, `sin(phase + i*0.85)` reads as rolling hills.

Koinobori note that survived its own critique: a streamer body built as
one ribbon (spine + widths, forked notch cut into the tail cap) holds the
flowing-cloth read; scallop scale arcs bulged *toward the tail* read as
wind-filled scales.

### Proposed change

Add to the holiday-seal notes in `prompts/`: any ground, floor or horizon
band inside a seal disc should close on the inner disc arc (sample the
arc, walk back along the crest) rather than draw a full shape and rely on
the rim to crop it — the rim is a stroke, not a clip.
