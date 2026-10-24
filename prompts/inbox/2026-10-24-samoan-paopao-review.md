## Samoan paopao V1R00 — outrigger separation comes from elevation, not angle

- Kind: analysis
- Source: #1122, `work/vehicles/samoan-paopao-V1R00.py`, `art/vehicles/samoan-paopao/`
- Applies to: field plates — watercraft and multi-part subjects
- Status: pending

### Evidence

The brief's real problem is occlusion: in a true side view the ama float
hides behind the hull and the kiato booms point at the viewer. The fix that
works is a shallow elevated profile from the outrigger side — water chord
at y=510, hull waterline just under it, float dropped ~175pt lower as the
near object — so the lagoon itself is the separator and both booms read as
full spars arcing over the gap. Booms drawn dead-plumb read as table legs;
a modest lateral bow on the spine (cubic + tapered ribbon, w 9.5->6.5)
sells "flexible lashed pole" without inventing geometry. Sennit lashing is
two passes of short diagonal strokes (parallel, then cross) at each joint —
all at 3.2pt, since the brief floors lashings at 3pt; a lighter second pass
at 0.8x width slipped under the floor until corrected.

Decked bow/stern is simpler than it looks: draw the full dark interior band
first, then lay wood deck wedges over the ends, then the near-gunwale
stroke — no boolean work. The plate-halo convention (r440, opacity ~9)
silently fails `check_rim.py`'s r430 scan; r422 keeps the halo and the
check. One soft radial behind the horizon + a stacked set of shrinking
amber ellipses under it carries "last light over a lagoon" without
touching the boat.

### Proposed change

For `prompts/series/` watercraft notes on next consolidation: "Separate a
hull from its outrigger with viewpoint elevation — float as foreground
object across a water band — and bow the boom spines visibly; keep every
lash stroke >=3pt." A proposal does not override current house rules.
