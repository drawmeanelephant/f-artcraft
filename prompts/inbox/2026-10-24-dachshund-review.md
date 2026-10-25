## Dachshund V1R00 — extreme proportions want the floor, not the eyes

- Kind: analysis
- Source: issue #1504; `work/dog-breeds/draw_dachshund.py`,
  `art/dog-breeds/dachshund/dachshund-V1R00.{vectorcraft,svg}`,
  proof `work/out/dachshund-V1R00@2x.png`
- Applies to: dog-breeds milestone series
- Status: pending

### Evidence

Shipped after two render loops on the border-collie chassis. The breed
is carried almost entirely by silhouette: the barrel has to sit low
enough that the legs read as stubs (feet ~y800, keel ~y730) while the
topline stays dead level — any sag in the middle and it becomes a
generic long dog. Proud head carriage = neck wedge rising off the
withers, nose at the highest point of the outline, level saber tail
continuing the topline rather than curling. A single long drop ear
hanging over the cheek does more for the likeness than any marking.

Two traps found: (1) a short "ear set" guide stroke placed just above
the skull outline printed as a nick on the head dome — guide strokes
near silhouette edges must stay strictly inside the fill or be dropped;
(2) the tan eyebrow dot of the red type only reads if it sits ABOVE the
brow stroke, not on it. Leaf-litter floor + one mushroom at ≤75% opacity
kept the forest-floor brief without crowding the rim. `check_rim` clean,
milestone line cleared the arc by 69pt.

### Proposed change

For the remaining long-bodied or short-legged breeds in the series
(corgi #1508): draw the barrel first and hang the legs off it — legs
drawn first anchor the body too high and the breed reads as normal-
proportioned. Candidate for the milestone-cards series note at
consolidation.
