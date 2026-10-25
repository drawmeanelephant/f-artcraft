## Milestone cards (dog breeds) — the grammar established by border-collie V1R00

- Kind: rule proposal
- Source: issue #1498; `work/dog-breeds/draw_border_collie.py`,
  `art/dog-breeds/border-collie/border-collie-V1R00.{vectorcraft,svg}`,
  proof `work/out/border-collie-V1R00@2x.png`
- Applies to: the whole dog-breeds milestone series (#1498–#1513 and later waves)
- Status: pending

### Evidence

First card of the series shipped after three render-and-critique loops.
The grammar that survived its own critique:

- **Chassis is field plate, verbatim.** 1000×1000, dark linear-gradient
  backdrop, plate disc ellipse (80,40,840,840) centre 500,460 r420 with a
  radial world-keyed gradient, inner ring 792 at ~40% opacity, rim stroke
  re-drawn *last* over all decor.
- **Caption stack is two lines, both below the disc.** Name in caps,
  Virelai Sans 56pt at y≈934, `text.setStyle` tracking 60. Milestone line
  `GROUP · ORIGIN` in caps, 22pt at y≈970, tracking ~280 — comes out
  ~540–600pt wide, well under the 760pt cap and clear of the lower arc;
  verify with `inspect_document` bounds + `math.hypot` against (500,460),
  not by eyeball. The `·` separator renders fine in Virelai Sans.
- **The dog owns the lower two-thirds of the disc.** A ground line —
  floor/crest/chord closed on the disc's own arc
  (`M rim_x(fy),fy C … A420,420 0 0 1 back Z`, `fy`≈770–790) — gives the
  feet somewhere to stand and doubles as the world cue (peat, marsh,
  snow). Breed-world accents sit ON that floor at ≤70% opacity.
- **Face the stance, not the camera, unless the brief says stare.** The
  collie's brief wanted the gaze on the viewer; a frontal head on a
  profile body worked — skull broad between the ears tapering to the
  muzzle, blaze as one shape running forehead→muzzle, eyes flanking it.
- **Ears: draw base triangle + a separate fold flap.** Semi-pricked =
  short erect triangle plus a smaller darker triangle hinged inward-down
  off the tip. Pointing the flap up-and-out reads as horns — the fold
  must land *inside* the base silhouette.
- **Markings are overlay shapes, not strokes.** White bib/blaze/socks/
  tail-tip drawn as filled shapes with the same warm-cream gradient;
  coat black is a warm dark ramp (#463B34→#191210), never pure black.
- **The old traps all still apply**: decor asserts `on_disc` with pad;
  gallop/crouch legs want one hard joint bend, never tapered sausages;
  thin fur/whisker strokes ≥3pt; `check_rim.py` on the @2x before
  shipping. Skip the 8%-opacity `Plate halo` — it trips check_rim at
  r>430 on lighter backdrops.
- **Breed accuracy checklist before shipping**: coat colour + marking
  map, ear set (erect/semi-pricked/drop/button), tail carriage
  (low/level/curled-over-back), head shape, and the brief's signature
  pose. Get the silhouette right first; texture strokes are cheap.

### Proposed change

Adopt the above as the milestone-card recipe; destination
`prompts/series/` (a dog-breeds/milestone-cards note) at the next
consolidation. Until then, `work/dog-breeds/draw_border_collie.py` is
the reference driver — copy its chassis wholesale and replace the dog.
