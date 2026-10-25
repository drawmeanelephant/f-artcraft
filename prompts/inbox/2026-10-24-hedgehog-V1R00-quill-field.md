## European hedgehog V1R00 — quills are a coverage problem, not a texture accent

- Kind: lesson
- Source: issue #1103; `work/animals/draw_european_hedgehog.py`,
  `art/animals/european-hedgehog/european-hedgehog-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: animals field plates; spiny/feathered/scaled surface texture
- Status: pending

### Evidence

Proof `work/out/european-hedgehog-V1R00@2x.png`. What the passes showed:

1. First pass scattered ~52 quill strokes by random sampling inside an
   ellipse — most fell outside the dome and the survivor count read as a
   smooth boulder with a comb-over. Fix was rows: nine horizontal runs
   across the dome, a stroke every ~26 pt, lean decreasing toward the
   belly, every third stroke cream for the banded-spine read. A spiny
   subject needs ~100+ strokes on the dome or the brain reads "rock".
2. Vesica leaf blades (two quadratic arcs + a mid-vein, rotated by hand)
   read as leaves; rotated rounded rects read as bandages/confetti. Any
   repeated leaf motif in this series wants the pointed blade.
3. Grounding: foreground canes/stems drawn before the floor fill need
   bases pushed 60-80 pt below the floor crest or they hang in the air.
4. A prop kept clear of the silhouette sells the story — the snail
   reads instantly only once moved fully left of the snout; whisker
   strokes bridging the gap do the "nemesis" narration.

### Proposed change

For `prompts/series/20-field-plates.md` known-traps: *surface texture is
row coverage, not scatter: lay strokes in measured rows across the mass
with a falling lean, and expect to need 3-4x your first density guess.
Pointed leaves are vesica paths — never rotated rounded rects.*
