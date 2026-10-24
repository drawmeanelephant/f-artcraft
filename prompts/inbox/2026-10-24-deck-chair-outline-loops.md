# deck-chair-V1R00 — outline paths must loop, stripes follow the drape

- Kind: lesson
- Source: issue #1154, driver `work/furniture/draw_deck_chair.py`,
  native + proof `art/furniture/deck-chair/`
- Applies to: furniture field plates; any slung/striped fabric over a frame
- Status: pending

### Evidence

Two failure modes showed in proofing. First, a canvas outline assembled by
concatenating sampled edges in the wrong order drew a dark X across the
sling — open subpaths joined end-to-start draw a connecting chord across
the face. Fix: build one closed loop (left edge down, bottom across,
right edge up, top across) and stroke that. Second, stripes drawn as
polka-dot ellipses on the wrapped front bar read as rivets; stripes need
to be bands. Final pass draws each stripe as a quad strip along the drape
(mesh rows along u, columns across x) and short butt-capped bands over the
bar wrap.

What survives critique: the leaning outer rectangle + canvas between its
rails is the whole read of the type; per-stripe meshes let colour follow
the sag without clipping tricks. Sea-air plate (cool slate disc, horizon
line, gulls) stayed subtle enough not to fight the subject.

### Proposed change

For `prompts/` consolidation: when stroking a sampled mesh boundary, always
emit it as one closed loop — M at an edge start, L through ordered
perimeter points, Z. Concatenating independently sampled edges invites
cross-face chords. Stripes on fabric should be mesh bands (quad strips),
never spot decorations.
