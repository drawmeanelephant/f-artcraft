## Quagga V1R00 — extinction drawn as opacity, not erasure

- Kind: analysis
- Source: issue #1057; `work/animals/draw_quagga.py`, `art/animals/quagga/quagga-V1R00.*`
- Applies to: animals field plates; extinct subjects; translucent shading
- Status: pending

### Evidence

Proof `work/out/quagga-V1R00@2x.png`. The species code IS the brief: front a
zebra, rear a rumor. Forebody, neck and head fully drawn with bold bands;
the flank stripes step down in opacity 88→72→48→26→14, the last one
continuing *past* the seam onto the translucent hindquarter so the fade
reads as a dissolve rather than a knife cut. Hindquarter and rear legs at
opacity ~42 with the low veld sun (a soft radial, op 40 core → 0 edge)
placed exactly behind them so the light literally shines through the
ghost. Four "drift flecks" at op 12–22 trail off the rump edge.

Working notes: a translucent object still takes a stroke — the ghost
quarter keeps a thin INK outline at shared opacity, which is what keeps it
reading as the same animal rather than weather. The dapple spots inside the
ghost at op 18 give the rumor a skin. Hard seam risk: end opaque masses
mid-body *under* the stripe fade, and let one stripe cross the boundary.

### Proposed change

For `prompts/series/20-field-plates.md`: extinct or vanished subjects can
spend transparency as vocabulary — split the silhouette into solid +
ghosted shells and put the light source inside the ghost. The technique
generalizes (thylacine, passenger pigeon, aurochs) but should stay rare;
one vanishing animal per wall of plates is poignant, three is a gimmick.
