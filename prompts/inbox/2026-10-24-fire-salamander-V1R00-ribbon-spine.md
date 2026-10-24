# Fire salamander V1R00 — tapered ribbons need a head cap and a real curve

- Kind: lesson
- Source: issue #1076, `work/animals/draw_fire_salamander.py`,
  `art/animals/fire-salamander/fire-salamander-V1R00.*`
- Applies to: field plates, animals
- Status: pending

### Evidence

The body is a ribbon generated from a spine polyline + halfwidth
profile (normals offset both sides, Q-smoothed). First pass used a
near-straight diagonal spine: the proof read as a banded cigar — every
yellow band landed as a perfect ring and the head end closed flat.
Fixes that made it an animal: (a) the spine needs genuine curvature —
a belly bow mid-body and a tail hooking back at the tip, not a straight
rake with a taper; (b) the ribbon's front end must be capped with a
drawn head wedge, wider than the neck, or the close `Z` cuts a flat
nose; (c) warning bands read organic when some are broken — vary span
and slide the band centre along the flank normal (`off`) rather than
always ringing the full width; (d) parotoid patches behind the eyes +
two crown spots carry the species badge better than body spots alone.

### Proposed change

For `prompts/series/20-field-plates.md` known traps: when generating a
ribbon body from a spine, budget three extra elements — a head cap
shape, one direction reversal somewhere in the curve, and markings
that break (partial bars), not rings that wrap.
