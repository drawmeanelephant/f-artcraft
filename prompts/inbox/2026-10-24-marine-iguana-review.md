## marine-iguana-V1R00 — rim math for horizontal tails

- Kind: lesson
- Source: issue #1136, `work/animals/draw_marine_iguana.py`,
  `art/animals/marine-iguana/marine-iguana-V1R00.{vectorcraft,svg}`,
  proof `work/out/marine-iguana-V1R00@2x.png`
- Applies to: field plates, long-tailed lateral poses
- Status: pending

### Evidence

First proof caught a real rim violation: a laterally flattened tail
running down-right along the ledge crossed the disc arc — at x≈785 the
rim is already at y≈770, and the tail tip sat at y≈810. A horizontal
tail reaches the rim far sooner than intuition says: the chord is short
down there. Fix: bury the tail base under the rump, shorten the run,
kick the tip up inside (754,763). Dropping the plank-like vertical
banding for a single lateral crease + two wrinkles also stopped the
tail reading as a woodpile.

What worked: the turquoise bounce — a 28–30% opacity stroke under the
belly and tail plus a wash band on the basalt lip — sold "hauled out on
wet lava at night" without touching the charcoal palette. Salt crust
as a single pale cap over the crown + three specks on the muzzle is
enough; more would read as dandruff.

### Proposed change

Add to `prompts/series/20-field-plates.md` traps: "A tail that runs
horizontally into the lower third of the disc hits the rim arc early —
solve for `disc_x(y)` at the tail's lowest points, not just the tip,
and kick the tip upward rather than letting it run level to the rim."
