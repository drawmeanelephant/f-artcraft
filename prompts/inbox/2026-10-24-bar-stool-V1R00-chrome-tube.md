## Bar stool V1R00 — chrome tube legs, cushion from two rims + hull

- Kind: lesson
- Source: #1186, `work/furniture/draw_bar_stool.py`, `art/furniture/bar-stool/bar-stool-V1R00.{vectorcraft,svg,@2x.png}`
- Applies to: furniture field plates; stools, chrome tubing, round cushions
- Status: pending

### Evidence

The vinyl cushion is two sampled rim circles (top at seat height, bottom
slightly wider for the welt flare); the side wall is the convex hull of
both projected rims, the crown is the top rim drawn over it — no analytic
ellipse needed. Specular sells vinyl: one soft radial sheen patch on the
crown plus a 4pt highlight strip just under the welt on the lit side.

Chrome reads with a fast dark→white→dark gradient across each tube
(`#33383E → #E9EEF2 at 0.32 → #20242A`) — the hard early highlight is
what distinguishes it from pale wood. A footrest ring drawn entirely
before the legs passes behind the near legs automatically, which is the
physically right read for a ring welded inside the leg cone; no
depth-sorting needed. Rubber feet are just dark ellipses + contact
shadows at each leg tip.

### Proposed change

For `prompts/series/` furniture notes on next consolidation: "Round
cushions: side wall = hull(top rim + bottom rim), crown = top rim over
it, welt = stroked rim. Chrome wants a hard highlight early in the
gradient (white by ~0.3), not a soft ramp." A proposal does not override
current house rules.
