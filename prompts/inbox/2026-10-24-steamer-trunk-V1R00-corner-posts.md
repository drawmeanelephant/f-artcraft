## Steamer trunk V1R00 — corner caps that only hug the corner read as floating blocks

- Kind: lesson
- Source: #1200, `work/furniture/draw_steamer_trunk.py`, `art/furniture/steamer-trunk/steamer-trunk-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates (trunks, crates, bound boxes)
- Status: pending

### Evidence

Short corner caps (~5in tall) wrapping a trunk's bottom corners rendered
as detached pillars floating beside the carcass — a capped corner only
works if it visibly overlaps the edge; a small proud cap beside a light
face reads as a separate object. The fix was to make them full-height
iron-bound corner posts (Y0..lid top), which turned a bug into the
trunk's signature frame. A side-effect trap worth remembering: computing
corner extents with sign-flip expressions inverted one box (x0 > x1) —
`box()` does not normalize its corners and an inverted prism culls wrong.

Hardware on a face must be flush: grab-handle mounts at +0.5in off the
end face showed a see-through gap (the mount's inner face is culled).
Seat them at +0.05 and let the grip sag between them. Paper labels are
rotated quads + two scribble lines — text-free, legible at @2x.

### Proposed change

For `prompts/series/` furniture notes on next consolidation: "On bound
boxes, run corner iron full height — small caps float. Hardware mounts
flush (≤0.1in) or the culled inner face shows a gap. Never emit an
inverted box()." A proposal does not override current house rules.
