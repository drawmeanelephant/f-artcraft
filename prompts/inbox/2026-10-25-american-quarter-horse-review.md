## American quarter horse V1R00 — the low head is a topline change, not a head swap

- Kind: analysis
- Source: issue #1517; `work/horse-breeds/draw_american_quarter_horse.py`,
  `art/horse-breeds/american-quarter-horse/american-quarter-horse-V1R00.{vectorcraft,svg}`,
  proof `work/out/american-quarter-horse-V1R00@2x.png`
- Applies to: milestone cards, horse breeds, quadruped pose work
- Status: pending

### Evidence

Shipped after two renders on the single-silhouette recipe. The "low head,
powerful hindquarter" brief works when the WHOLE topline is re-drawn for it:
the crest runs near-level from poll to withers, the jaw hangs below the
neck front edge, and the hip gets an oversized round bulge plus a faint
translucent muscle shade inside it. Shortening the back (~90pt less than
the arabian span) and deepening the girth gave the compact sprinter frame.

Two details worth keeping: the ranch-country cue is a single faded rail
fence (one stroked line + three 4pt posts at 30% opacity) — reads at @2x
without clutter; and a tail drawn inside the rump silhouette edge gets
swallowed — slide it right until it hangs visibly off the dock, even if
that puts the dock 15pt proud of the croup.

Name fit note: `AMERICAN QUARTER HORSE` at the house 56pt would overset;
48pt at y934 lands at ~770pt wide, inside the canvas margins. When the
name is long, drop the size before touching tracking — the milestone line
stays at the spec 22pt/280.

Survives critique as V1R00 with residue: the lowered head verges on
grazing — another 15pt of muzzle lift would read more "alert at rest";
the hip shade ellipse is still a visible disc if you stare.

### Proposed change

For the horse-breeds/milestone note at consolidation: *long names —
reduce point size before reducing tracking, and assert the rendered
bounds of BOTH caption lines, not just the milestone line.*
