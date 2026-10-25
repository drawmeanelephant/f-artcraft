## Lipizzaner V1R00 — the levade survives on head/neck separation, not tilt

- Kind: analysis
- Source: issue #1527; `work/horse-breeds/draw_lipizzaner.py`,
  `art/horse-breeds/lipizzaner/lipizzaner-V1R00.{vectorcraft,svg}`,
  proof `work/out/lipizzaner-V1R00@2x.png`
- Applies to: horse-breeds milestone cards; extreme/rearing poses
- Status: pending

### Evidence

Shipped after four render-and-critique loops — the hardest horse so
far. The first three passes all read as SEAL or seahorse, not levade.
What actually fixed it, in order of impact:

- **Jowl notch.** Adding a small chin/jowl dip where the jaw meets the
  throat (`…(376,502),(350,494),(326,500)…`) is what finally split
  head from neck. Without it the front half is one smooth tube and no
  amount of leg work rescues it. Same rule as the friesian mane:
  silhouette features need silhouette notches.
- **Hind legs with a true hock flex** — thigh near-vertical to a low
  hock, then cannon running down-FORWARD to the hoof. The earlier
  straight-ish columns read as the animal's tail-end, not as legs.
- **Haunch as a blunt mass.** The croup face must be nearly vertical
  and full; a tapered rear + hanging tail reads as one continuous
  cone.
- Tilt moderation: ~37° topline reads; steeper looks like falling.

What did NOT fix it: adding belly sag mid-barrel (the torso is not
the problem), longer topline sheens (they emphasise the tube),
interior shading of any kind. The levade reads on the silhouette's
ENDS — head/jowl up front, haunch/hock at the rear — and stays dead
in the middle.

Survives critique as V1R00 with residue: the tail still merges
visually with the rump edge; the near/far fore pair are close
enough to read as one limb from a distance; the school windows are
maybe a touch tall.

### Proposed change

For the horse-breeds card note at consolidation: *extreme poses
(levade, rear, capriole) read on silhouette notches — jaw-to-throat,
stifle-to-flank, dock-to-tail — never on interior shading. Budget
3–4 render loops for any pose where the body axis is not level.*
