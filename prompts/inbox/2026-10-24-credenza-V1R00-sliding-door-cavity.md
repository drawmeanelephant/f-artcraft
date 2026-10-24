## Credenza V1R00 — sliding-door bays need the interior drawn *before* the shell

- Kind: lesson
- Source: #1197, `work/furniture/draw_credenza.py`, `art/furniture/credenza/credenza-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates (any closed-top case with an open bay)
- Status: pending

### Evidence

A credenza's sliding door slides *past the carcass end* and overhangs the
silhouette — a cheap way to show the mechanism and open a bay at once.
Two order-of-operations failures taught the rule:

1. Interior slabs drawn after the carcass shell paint their pale faces over
   the top slab's `+y` face — the whole case reads open-topped. Interior
   must be drawn first; the nearer shell faces then occlude it everywhere
   except the mouth.
2. The reveal above a closed door is not empty space: the downward sight
   line through even a 0.2in gap exposes the bay's interior. If only the
   open bay is modelled, the reveal over the closed door shows unmodelled
   darkness — a void. Interior back wall and floor must span the *full*
   carcass width. A pale lining on the far side wall overcorrects (reads as
   a bright wedge at the silhouette); the stock `EXT` wall face plus the
   full-width back reads as honest interior shadow.
3. The top slab's `-x` end face is back-facing and culled, leaving a pale
   trapezoid where the left cheek should cap — patch it with an explicit
   `quad3` end cap in a dark ramp.

A tapered leg is just a `box()` whose bottom ring is smaller and offset —
keep the `box()` corner order or `FACES` maps wrong quads.

### Proposed change

For `prompts/series/` furniture notes on next consolidation: "Closed-top
cases: draw interior slabs first, shell after — the shell occludes the
interior except at the mouth; model interior across the *full* width
because the reveal over a closed door looks in. Cull leaves end-cap holes
at silhouette corners; patch them with explicit dark quads." A proposal
does not override current house rules.
