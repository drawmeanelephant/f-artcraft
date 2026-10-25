## Jennifer Doudna V1R00 — parametric helix with an abstracted cut

- Kind: lesson / analysis
- Source: issue #1558; `work/scientists/draw_jennifer_doudna.py`,
  `art/scientists/jennifer-doudna/jennifer-doudna-V1R00.{vectorcraft,svg}`,
  proof `work/out/jennifer-doudna-V1R00@2x.png`
- Applies to: scientists milestone series; molecule/DNA decor generally
- Status: pending

### Evidence

Shipped on the first proof. The reusable bits:

- **Parametric helix**: `helix_pts(y0,y1,phase)` samples
  `x = cx + A·sin(2πy/P)` every 9pt; two strands at phase 0 and π stroked
  5pt in two teal tones. Rungs are straight strokes between the strand
  x-positions at each y — skip any rung shorter than ~10pt (the
  crossovers) and the helix reads immediately. Alternate two muted
  base-pair colours (#7FC8A8 / #C8A87E).
- **The edit is a gap, not a gadget.** Splitting both strands into two
  fragment runs (y …414 / 446…) leaves a clean break; blunt cap dots on
  the four strand ends + two chevron ticks (one bright `>` facing the
  cut, one dimmer `<`) + a small radial glow mark the site. Reads as
  "something was cut here" with zero cutlery — matches the brief's
  "scissors motif abstracted into the helix".
- **Modern-lab props differ from the 1900s set**: microfuge rack = dark
  tray + five tube capsules whose caps are the only colour accents
  (5 pastel caps at 75%); micropipette = dark silhouette with a plunger
  button. A ghosted `A T G C G T A` (SS3, opacity 15) + chromatogram
  squiggle is the modern equivalent of Einstein's chalk.
- **Blazer read**: dark navy blazer + cream blouse V + slim collar band
  reads "modern PI" apart from Tu Youyou's white coat — worth keeping
  the wardrobe varied across the series.
- Blonde hair wants a lighter brow colour too (#8A6E48, not the usual
  dark brow stroke).

### Proposed change

Add the parametric helix + cut-site convention to the consolidated
milestone-card note (destination `prompts/series/`): backbone =
`x = cx + A·sin(2πy/P)`, rungs skipped where the strands cross, edits
shown as a clean gap + chevron ticks + glow, never a literal tool.
