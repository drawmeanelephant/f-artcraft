## Red fox V1R00 — drawn tails, not ribbon tails

- Kind: lesson
- Source: issue #1032; `work/animals/draw_red_fox.py`, `art/animals/red-fox/red-fox-V1R00.*`
- Applies to: animals field plates; any subject with a tail that wraps the body
- Status: pending

### Evidence

Proof `work/out/red-fox-V1R00@2x.png`. The brush took three attempts inside
V1R00:

1. A quadratic `ribbon()` whose spine dove right then curled back left
   produced a wedge, not a tail: the start cap showed as a diagonal seam on
   the haunch, the outer edge kinked to a false "tip" at bottom-right, and a
   banded white segment (`seg()` slice of the ribbon edges) read as a plank
   with a sawn-off end. Cutting a band out of a ribbon always gives you the
   band's geometry — parallel chords and a square end — never a fur tip.
2. Burying the ribbon start inside the rump fixed the root but the spine's
   return leg still showed a straight top edge — a tail is judged on its
   outer silhouette, and a ribbon's silhouette is two offset curves that
   only agree at the caps.
3. Final: one hand-drawn crescent path (M-root-tucks-behind-rump → top edge
   sweeps left → tip → bottom edge sweeps right → round root end → close),
   drawn BEFORE the body silhouette so the root disappears behind the rump
   edge. The white tag is a second hand-drawn shape hugging the crescent's
   own outline with a scalloped parting edge — no straight edges anywhere.

Also worth keeping: berries/twigs placed within ~40px of the subject's
outline read as sitting ON the subject — keep hedge fruit clearly outside
the silhouette. Rim check: at x=790 the disc floor is already y=764 — decor
that visually sits "on the ground" near the edges leaks past the rim;
verify r<400 for anything near the disc edge, not just r<420.

### Proposed change

For `prompts/series/20-field-plates.md` known-traps: a tail or limb that
wraps around the body should be drawn as a closed crescent path with its
root end buried under the subject silhouette — ribbons leave visible caps
and kinks; a tip/patch of a different colour is a second closed shape
sharing the crescent's outline, never a ribbon segment cut mid-span.
