## Bigfoot V1R00 — silhouette integrity and ground-plane props

- Kind: analysis
- Source: issue #1028; `work/animals/draw_bigfoot.py`, `art/animals/bigfoot/bigfoot-V1R00.*`
- Applies to: animals field plates; any subject where the pose IS the subject
- Status: pending

### Evidence

Proof `work/out/bigfoot-V1R00@2x.png`. Two failure modes surfaced and were
fixed in the same revision cycle:

1. A separately-drawn cranial "peak" path layered on the skull read as a
   cap/beret, not a sagittal crest — any blob with its own ink outline
   sitting on a head reads as headwear. Fix: grow the feature out of the
   silhouette itself (one outline sweeping up to the peak) and echo it with
   internal fur strokes.
2. Footprints drawn as upright ovals with tall heel/sole proportions
   floated above the floor line and read as droppings. Fix: foreshorten
   hard — prints on a ground plane are wide flat ellipses (58×24 at
   plate scale) with the toe row compressed, all below the floor crest.

What worked first try: stacked-tier `pine()` silhouettes at two opacities
give treeline depth for ~5 paths per tree; the moon disc behind the head
provides both the glow and the figure's rim-light logic; leaning the torso
~15° forward and sinking the head into the shoulders is what separates
"sasquatch mid-stride" from "bear standing up". Mist echo at opacity 12
keeps the cryptid-blur joke readable without muddying the silhouette.

### Proposed change

For `prompts/series/20-field-plates.md` known-traps: features that grow out
of a head (crests, tufts, horns) must be part of the silhouette path — a
separate shape on top reads as an accessory. Ground-contact props (prints,
spoor, shadows) need foreshortened flat geometry placed below the floor
crest line, never upright ovals straddling it.
