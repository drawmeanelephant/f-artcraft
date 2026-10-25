## masaya-hammock-V1R00 — sagging curves and the hammock read

- Kind: lesson
- Source: issue #1110, driver `work/furniture/masaya-hammock-V1R00.py`,
  native + proof `art/furniture/masaya-hammock/`
- Applies to: furniture field plates; any catenary/hanging-cloth subject
- Status: pending

### Evidence

First render read as a solid dome, not a sling. Cause: a reversed
quadratic-Bezier edge was given a negated sag — but a quadratic traversed
right-to-left keeps the same control point, so the "bottom" edge bowed up
to y~300 and filled a mushroom shape. With the sag sign kept positive on
reversed edges, the cavity opened and the piece read as a hammock on the
first proof after the fix.

What survives critique: gathered-end bridle suspension (no spreader bars,
so the materials line is `COTTON` alone, per the brief's omission clause);
calado openwork as a dark translucent panel behind a small diamond lattice;
fringe restrained to the near rim; the terracotta band as a wall slice
following the bed curves. The interior still borders on a "smile" read —
the lit inner-wall wash and sparse far-side strands help but a deeper
rendering of inner cloth would help more.

### Proposed change

For `prompts/core/` consideration: document the reversed-curve trap —
`par_q`/`smooth`-style helpers are direction-sensitive; when closing a
region along the same sagging edge in reverse, reuse the same sag sign.
Catenary subjects should budget an interior cavity pass (far rim, dark
gradient, lit inner wall) or the subject reads as a solid cutout.
