# Insects — field plates, wave 2 (proposal)

Proposed tracking issue for the second wave of the insect field-plate
series. Wave 1 (#68) plus the issue-driven singles shipped 19 plates
heavy on Coleoptera and Lepidoptera (see `art/insects/`). No insect
plates are open or claimed as of this writing.

Wave 2 widens the order coverage instead of restocking the beetles:
seven orders new to the series (Orthoptera, Ephemeroptera, Neuroptera,
Diptera, Mecoptera, plus first damselfly for Odonata and first true
Hymenoptera beyond the leafcutter ant), with two flagship moths and two
beetles chosen for silhouette and colour rather than family count.

## Format (from PROMPTS.md — Field plates: Insects)

- 1000×1000 canvas: dark moody backdrop → large gradient plate disc
  (center 500,460, r≈420) → the insect → name in caps, Virelai Sans
  ~56–60pt at the bottom (y≈930); the second line is the taxonomic
  **order** in caps (~22–24pt, wide tracking, y≈968, ≤760pt wide).
- Three-quarter dorsal pose unless the silhouette is lateral (mayfly,
  scorpionfly). The whole animal — antennae, legs, cerci and all —
  stays inside the disc.
- Wings are translucent with visible venation over the backdrop, never
  an opaque fill. Living specimens only: no pins, no kill jars, no
  shadow box.
- Gradients + translucent shading, never flat fills. Warm dark ink,
  never pure black. Antennae, tarsi and wing veins ≥3pt, judged at @2x.
- First pass is `<slug>-V1R00`. Deliverables:
  `art/insects/<slug>/<slug>-V1R00.vectorcraft` + `.svg` + `@2x.png`;
  driving script `work/insects/draw_<slug>.py`; the `.pdf` proof stays
  in `work/out/` (local only).
- Known trap: decorative shapes near the plate's lower edge must close
  on the disc's own arc (`A420,420 0 0 1 …`) or they leak past the rim.

## Leaf briefs

Each becomes its own `Insect — field plate: <name>` issue
(`type:illustration`, `work:original`), filed in the style of
`prompts/issues/blue-morpho.md`. None duplicate `art/insects/` or
closed issues.

1. `luna-moth` — *Actias luna* (LEPIDOPTERA); wings spread at rest,
   pale-lime scaling fading to cream ribbon tails curling below.
2. `deaths-head-hawkmoth` — *Acherontia atropos* (LEPIDOPTERA); dark
   wings half-folded, the cream skull mark on the thorax doing the
   talking.
3. `goliath-beetle` — *Goliathus goliatus* (COLEOPTERA); three-quarter
   dorsal, white pronotum in black chevrons, mass reading as the
   heaviest beetle alive.
4. `tiger-beetle` — *Cicindela sexguttata* (COLEOPTERA); metallic
   emerald sprinter, long legs mid-stride, jaws forward.
5. `tarantula-hawk-wasp` — *Pepsis* sp. (HYMENOPTERA); blue-black body
   dragging ember-orange wings, antennae curled.
6. `velvet-ant` — *Dasymutilla* sp. (HYMENOPTERA); the wingless female
   "cow killer", scarlet velvet pile over a wasp waist.
7. `ebony-jewelwing` — *Calopteryx maculata* (ODONATA); damselfly at
   rest, satin-black wings folded together over a metallic teal body.
8. `katydid` — *Pterophylla camellifolia* (ORTHOPTERA); leaf-mimic
   wings with full leaf venation, lateral profile. First orthopteran.
9. `mayfly` — *Ephemera* sp. (EPHEMEROPTERA); imago with wings held
   upright like a sail, three long cerci trailing. First of the order.
10. `mantisfly` — Mantispidae (NEUROPTERA); lacewing wings over
    raptorial mantis-style forelegs — convergence on the orchid mantis
    plate is the joke.
11. `stalk-eyed-fly` — Diopsidae (DIPTERA); front-on head study, eyes
    out at the tips of antler-long stalks.
12. `scorpionfly` — *Panorpa* sp. (MECOPTERA); lateral male, the
    upturned scorpion-like tail bulb over patterned wings.

## Acceptance

- [ ] Each leaf brief becomes its own sub-issue linked from the
      tracking issue; roster checked against `art/insects/` and closed
      issues at filing time.
- [ ] One active claim per worker; `Closes #<leaf>` on each art PR.
- [ ] Every plate proofed at @2x: whole animal inside the rim,
      translucent venated wings, order line clear of the arc.
