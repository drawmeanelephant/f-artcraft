## Icelandic V1R00 — the tölt is a forearm lifted to the horizontal

- Kind: analysis
- Source: issue #1526; `work/horse-breeds/draw_icelandic.py`,
  `art/horse-breeds/icelandic/icelandic-V1R00.{vectorcraft,svg}`,
  proof `work/out/icelandic-V1R00@2x.png`
- Applies to: horse-breeds milestone cards; gaited/small horses
- Status: pending

### Evidence

Shipped on the second render (first run tripped the on_disc assert on
two moss tussocks placed too low-right — the assert earns its keep;
check centers against `PR - pad`, ellipse corners decide).

What worked:

- The tölt reads instantly: `leg((436,556),(384,568),(398,634))` puts
  the near forearm horizontal in front of the chest with the cannon
  hanging — the breed's flamboyant front action — while the far hind
  reaches under the belly in the running-walk overstride. Same `leg()`
  helper, a different fold than the friesian/andalusian collected
  fold: the carpus points FORWARD at chest height, not tucked back.
- The double coat is the shetland rule: ragged ticks along the belly
  edge at ~60% opacity, never a furry silhouette.
- Chestnut + flaxen is the right contrast on the volcanic moss-green
  disc — the brief's "volcanic greens and blacks" could have swallowed
  a dark coat; the flaxen mane and tail do double duty as highlights.
- World on ~8 calls: one angular zigzag ridge stroke (join=round),
  one faint steam wisp, five moss tussocks on the black-sand floor.

Survives critique as V1R00 with residue: the raised leg's elbow makes
a small blocky notch on the chest edge; the ridge zigzag is a touch
mechanical — one more peak would break the rhythm.

### Proposed change

For the horse-breeds card note at consolidation: *distinct gaits are
distinct `leg()` folds — collected = carpus tucked back under the
chest, tölt/action = carpus forward at chest height with the cannon
hanging.* No structural divergence.
