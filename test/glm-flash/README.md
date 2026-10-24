# GLM-Flash style exploration

Test art from Factory Droid running GLM-Flash, drawn entirely through
VectorCraft's MCP server (headless, via the repo's `work/vc.py` harness).
The brief: find a style that **isn't** the house style, that I'm comfortable
with and think looks great — then prove it with test art and document the
process. This folder is that experiment; nothing here touches the house
grammar or the gallery scan.

## The pick: mid-century spot-flat

A Charley-Harper-style flat abstraction: one spot circle behind the subject,
the subject reduced to a few exact flat silhouettes, a minimal face
(paper ring + vermilion dot), sparse dressing (bubbles, water dashes), three
colours on warm paper — `#F2EBDD` / `#2E2E38` / `#E0673F`. No outlines, no
gradients.

**Why it's a great fit for me:** the style's charm comes from exactly what a
programmatic drawer can control — precise geometry, tapered spiral curves
computed from arc maths, restraint, and clean palettes. There is no fake
painterly texture to miss. And it's maximally distinct from the house style
(warm dark gradients, translucent shading, ornamental type), so it proves a
second look can live in this repo without blending into the first.

## Process

### 1. Research

Style survey pointed to the geometric families as the ones that flatter
code-driven drawing: art deco (sunbursts, chevrons, stepped forms),
mid-century flat abstraction (shape reduction, spot colour), and linocut
(bold two-tone graphics). Those three became the studies.

### 2. Three studies, one subject

Same subject (an octopus — eight spiral arms are pure arc maths), same
1000×1000 canvas, three grammars, drawn blind then critiqued from the
proofs:

| Study | First pass | Refinement | Verdict |
|---|---|---|---|
| **Harper flat** | `study-harper-octopus-V1R00` | `V1R01` (top-left arm no longer arcs over the dome) | **Strongest** — nearly right on the first pass |
| **Linocut** | `study-linocut-octopus-V1R00` | `V1R01` (carve ticks now track the arm centrelines — in V1R00 they floated on the sun) | Strong second; the style leans on hand-carve irregularity, which fights a programmatic drawer |
| **Art deco** | `study-deco-octopus-V1R00` | `V1R01` (rounder bell mantle, kohl eyes, form-following shade, halo dropped, arm fan pulled in) | Richest dressing — sunburst, frame and palette landed instantly — but the figure still reads hooded, not octopus. Needs a head-as-hub redesign (`V2R00`) to be fair to it |

The pattern was consistent: **dressing is easy, figures are the work.**
Sunbursts, frames, bubbles and dashes came out right first try every time.
The animal silhouettes needed proof-driven iteration.

### 3. Finished test piece: `spot-whale`

To show the style generalises past the study subject, a second piece at full
quality — and it turned into the most instructive part of the exercise:

- `V1R00` — composition and dressing right immediately; the whale read as a
  **fish**: pointed snout, vertical fish fluke.
- `V1R01` — anatomy pass: blunter head, deeper belly, dorsal fin, fluke
  reshaped. Still fish: the tail joint stayed thick.
- `V1R02` — spout moved to the blowhole, jaw sliver shortened, fin raked.
  Fish tail persisted.
- `V1R03` — the actual root cause: the body must taper into a **24pt-narrow
  tail stem** and the fluke hangs off that stem as a horizontal paddle. The
  fish/whale difference lives in the joint, not the tail shape.

Lesson recorded for whatever comes next: in flat abstraction the **silhouette
code** carries the species — decoration is cheap, the outline is the work.
Subjects whose geometry I can construct (octopus spirals, snail shells,
fluke-on-a-stem whales) are where this style and I are strongest.

## If the house adopts it

A `spot-flat` series would want its own charter, the way the field plates
have one: 1000×1000, spot circle as the compositional hub, flat silhouettes
with a minimal face, one accent colour family per piece, thin line dressing.
It deliberately breaks house rule #1 (flat fills, never gradients) — that is
the point of the style, and why it should stay a separate series rather than
leak into the plates.

## Files

- `study-{harper,linocut,deco}-octopus-V1R0{0,1}` — studies: native + `.svg`
  + `@2x.png`, one driver script per revision
- `spot-whale-V1R00…V1R03` — the finished test piece and its revision trail
- `spot-whale.py`, `spot-whale-v1r0{1,2,3}.py` — driving scripts
- PDF proofs stay local (`work/out/`), per AGENTS.md

Every file is additive — nothing overwritten, revisions only, per the
revision rule.

## Housekeeping

This branch also carries the `work/vc.py` `REPO` fix (it resolved one level
too high since the layout moved) and a `.gitignore` whitelist for
`test/**/*.vectorcraft` — natives are ignored everywhere except `art/` and
now `test/`.
