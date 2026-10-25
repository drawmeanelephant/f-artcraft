## Vivaldi V1R00 — held instruments want real scale + painter-order discipline

- Kind: analysis
- Source: issue #1531; `work/musicians/draw_antonio_vivaldi.py`,
  `art/musicians/antonio-vivaldi/antonio-vivaldi-V1R00.{vectorcraft,svg}`,
  proof `work/out/antonio-vivaldi-V1R00@2x.png`
- Applies to: musicians milestone series; any held-prop figure
- Status: pending

### Evidence

Two render loops. First pass failed on scale and painter order:

- **A violin is bigger than you think.** First pass drew the body ~120pt
  long at shoulder height — read as a toy lute floating beside the head.
  Working size at card scale: tailpiece→scroll ≈ 290pt, lower bout ≈ 75pt
  wide, tailpiece tucked under the jaw (chin rest overlaps the chin
  silhouette — that contact is what sells "under the chin").
- **Frontal violinist orientation:** scroll to the viewer's RIGHT (the
  player's left shoulder, mirrored), body under the jaw, neck rising to
  the scroll; bow crosses the body near the waist, frog hand low.
- **Sleeves go UNDER the held prop.** First pass drew the raised sleeve
  over the violin and it printed as a dark mitten glued to the body.
  Paint order: arm → violin → hand on the neck.
- **Auburn hair without a wig reads fine** — crown cap + side waves to
  the jaw + one forehead lock. The hair wants a sheen stroke or it reads
  as a hood.
- **Cassock is nearly the darkest shape on the plate** — it needs the
  white collar band and a lit edge (buttons + front seam) or it turns
  into a flat blob against a mid-tone disc.
- Curling manuscript corner: a closed curl flap off the sheet's corner,
  not a rolled stroke — reads at 2×.

### Proposed change

Held-instrument recipe for the musicians note: prop at real relative
scale, contact point touching the body (chin rest on jaw, mouthpiece on
lip, grip in hand), the prop painted after the arm that holds it, and
one dark part (fingerboard/housing) for contrast against the sleeve.
