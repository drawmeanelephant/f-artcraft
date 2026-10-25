## Australian shepherd V1R00 — merle as placed patches, ear fold direction

- Kind: analysis
- Source: issue #1511; `work/dog-breeds/draw_australian_shepherd.py`,
  `art/dog-breeds/australian-shepherd/australian-shepherd-V1R00.{vectorcraft,svg}`,
  proof `work/out/australian-shepherd-V1R00@2x.png`
- Applies to: dog-breeds milestone cards; merle/marbled coats; profile ears
- Status: pending

### Evidence

Blue merle at the working trot on a dusty gold disc. Two critique loops.
The merle() blob helper (dalmatian's irregular spot, enlarged) at ~85%
opacity over a silver-blue gradient reads as marbling well enough at plate
scale — though at this size it borders on polka-dot; a revision could drop
patch opacity to ~70% and overlap pairs for softer marble. White collar,
blaze and socks plus copper points map the breed.

The tipped ear taught the grammar a nuance: the fold flap must hinge
*toward the muzzle*, not backward — hinging it to +x produced a pennant
flag. In profile the flap may legitimately poke ~20px past the base's
front edge; that reads as a flop, not a horn. Horn = flap pointing up or
out along the ear's own axis.

First-pass head was too long and drooped at the nose — raised the nose
tip ~10pt and shortened the skull. Copper cheek belongs mid-face under
the eye, not low on the jaw.

Survives its critique: bobtail stub present, trot diagonal reads, all
markings placed, rim clean, milestone clears by 69pt.

### Proposed change

Add to the ear rule in the milestone grammar: profile fold flaps hinge
forward-down toward the nose and may cross the base silhouette's front
edge; backward or upward flaps read as horns/flags. Candidate for
consolidation.
