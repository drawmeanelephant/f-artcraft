# Animals — field plates, wave 11 (proposal)

Proposed tracking issue for the eleventh wave of the animal field-plate
series. Waves 1–10 plus the issue-driven singles have shipped ~211 plates
across ordinary, unusual, extinct, cryptid and aquatic animals (see
`art/animals/` and closed issues #541, #997, #1029, #1060, #1093 and
#998–#1146). No animal plates are open or claimed as of this writing.

Wave 11 leans on the uncovered taxonomy niches rather than another lap of
the same phyla: first cetacean since the narwhal, first pinniped, first
bat, first ratite, first anatid, first arachnid — rounded out with one
armored fossil fish and one river cryptid so the wave still spans the
series' full range.

## Format (from PROMPTS.md — Field plates)

- 1000×1000 canvas: dark moody backdrop → large gradient plate disc
  (center 500,460, r≈420) → the animal → name in caps, Virelai Sans
  ~56–60pt at the bottom (y≈930); a second tracked line under it carries
  the binomial in caps (~22–24pt, y≈968, ≤760pt wide so it clears the
  rim arc).
- Portrait when the face is the point; full-body or profile when the
  silhouette is. The whole subject stays inside the rim.
- Gradients + translucent shading, never flat fills. Warm dark ink,
  never pure black. Thin geometry (whiskers, claws, frill ribs)
  needs ≥3pt of stroke and must be judged at @2x.
- First pass is `<slug>-V1R00`. Deliverables:
  `art/animals/<slug>/<slug>-V1R00.vectorcraft` + `.svg` + `@2x.png`;
  driving script `work/animals/draw_<slug>.py`; the `.pdf` proof stays
  in `work/out/` (local only).
- Known trap: decorative shapes near the plate's lower edge must close
  on the disc's own arc (`A420,420 0 0 1 …`) or they leak past the rim.

## Leaf briefs

Each becomes its own `Animal — field plate: <name>` issue
(`type:illustration`, `work:original`), filed in the style of
`prompts/issues/spectacled-bear.md`. None duplicate `art/animals/` or
closed issues.

1. `orca` — *Orcinus orca*; tight spyhop breach at dusk, black saddle
   and white eye-patch reading against a cold blue-grey sea.
2. `walrus` — hauled-out three-quarter portrait; whiskered muzzle and
   ivory tusks catching the light, creased hide in warm translucent
   layers. First pinniped.
3. `three-toed-sloth` — hanging in profile beneath a branch, algae-green
   cast over the brown coat, one long clawed arm reaching; serene.
4. `flying-fox` — roosting upside down wrapped in its own leathery wing
   cloak, fox-like face peering out of the fold. First chiropteran.
5. `ostrich` — running profile across a dry pan, plumed wings
   half-lifted for balance, neck low, dust kicking at the feet.
6. `bald-eagle` — perched bust portrait; white head and hooked gold
   beak in profile, mantle feathers layered like shingles.
7. `black-swan` — gliding on a dark water chord, neck in a low S,
   crimson bill, a hint of white flight feathers at the rear edge.
   First anatid.
8. `eyelash-viper` — yellow-morph coil on a wet leaf, raised
   supraciliary "lash" scales, heat-pit face turned toward the viewer.
9. `frilled-lizard` — threat display: frill flared wide as a fan,
   mouth open, body upright on the hind legs; silhouette-first.
10. `peacock-spider` — male *Maratus* mid-display, iridescent abdominal
    fan raised like a peacock tail, third legs waving. First arachnid.
11. `dunkleosteus` — Devonian armored fish, bony head plates shearing
    open, body tapering back into darkness; the wave's extinct+aquatic.
12. `kappa` — river cryptid seated on a stone, the water-filled dish on
    its head glinting, webbed hands, small carapace behind.

## Acceptance

- [ ] Each leaf brief becomes its own sub-issue linked from the
      tracking issue; roster checked against `art/animals/` and closed
      issues at filing time.
- [ ] One active claim per worker; `Closes #<leaf>` on each art PR.
- [ ] Every plate proofed at @2x: rim containment, ≥3pt thin geometry,
      caption stack clear of the arc.
