# Horse breeds — milestone cards, wave 2 (proposal)

Status: draft proposal, not posted. One tracking issue plus twelve leaf
issues; each leaf is one new piece. Wave 1 shipped via #1561 (leaves
#1514–1528) — every leaf below is new.

## Wave 1 inventory (do not duplicate)

akhal-teke · american-quarter-horse · andalusian · appaloosa · arabian ·
belgian · clydesdale · friesian · icelandic · lipizzaner · morgan ·
mustang · percheron · shetland-pony · thoroughbred

Wave 1 covered draft, baroque, hotblood, gaited, pony, feral, stock and
classical types — all European, North American or Arabian. Wave 2 adds
Asia (marwari), the cob/vanner build, the harness racer and the
warmblood.

## Format (milestone cards — field-plate chassis)

- 1000×1000 canvas: dark moody backdrop → large gradient plate disc
  (centre 500,460, r≈420) → subject → name in caps, Virelai Sans ~56–60pt
  at y≈930.
- The milestone line under the name in caps, Virelai Sans ~22–24pt, wide
  tracking, y≈968, ≤760pt wide — check it clears the disc's lower arc.
- Gradients and translucent shading, never flat fills. Warm dark ink,
  never pure black. Nothing crosses the rim; shapes near the lower edge
  close on the disc's own arc.
- Keep the breed-defining traits accurate to type (build, feather, coat);
  thin essentials ≥3pt and the whole horse inside the rim. The milestone
  line is the type and origin — `TYPE · ORIGIN`. No tack unless the
  brief asks.
- First pass is `<slug>-V1R00`. Deliverables on main:
  `art/horse-breeds/<slug>/<slug>-V1R00.vectorcraft` + `.svg` and driver
  `work/horse-breeds/draw_<slug>.py`; the `@2x.png` proof goes to the
  `media` branch; the `.pdf` stays in `work/out/` (local only).

## Proposed leaves (12)

### american saddlebred — `GAITED · KENTUCKY`

The peacock of the show ring: extreme high head carriage, arched neck,
animated trot, tail set high. Park-horse posture; chestnut or bay with
flaxen accents.

### camargue — `FERAL · SOUTHERN FRANCE`

White horse of the marsh: compact grey-white standing hock-deep in
shallow water, marsh grass at the rim. A soft reflection under chest and
belly; slate-blue disc palette.

### connemara — `PONY · IRELAND`

Irish sport pony: quality pony head, strong quarters, usually grey.
Standing on a green turf floor; kind eye, none of the draft heaviness.

### fjord — `PONY · NORWAY`

Dun with the black dorsal stripe running forelock to tail; the upright
two-tone mane is the signature. Blocky, sure-footed stance — a working
mountain pony, not a toy.

### gypsy vanner — `COB · BRITISH ISLES`

Piebald or skewbald cob with full feather from knee to hoof, heavy mane
and tail. The feather is the plate's texture — layered translucent
strands, never a solid boot.

### haflinger — `MOUNTAIN · TYROL`

Chestnut with a flaxen, near-white mane and tail, compact mountain
build. Alpine backdrop; gold-on-cream is the coat's whole argument, so
grade it, don't flatten it.

### lusitano — `IBERIAN · PORTUGAL`

Baroque Iberian, but not the wave-1 andalusian redrawn: more convex
profile, deeper grey or bay, working-equitation energy — a collected
canter or levade rather than a parade stand.

### marwari — `HOTBLOOD · INDIA`

The scimitar ears: tips curled inward until they touch. Lean desert
horse, often chestnut; the ear lyre must read at plate scale — draw the
curl, don't imply it.

### shire — `DRAFT · ENGLAND`

The tallest of the tall: massive draft with heavy lower-leg feather,
usually bay or black with white socks and blaze. Keep it gentle-giant;
feather strands ≥3pt and separated.

### standardbred — `HARNESS · UNITED STATES`

The trotter: longer-bodied and lower-slung than the thoroughbred,
plainer head, mid-trot. A thin-wheeled racing sulky is the one
permitted tack prop — drawn thin, generic, and behind the horse.

### tennessee walking horse — `GAITED · TENNESSEE`

The running walk: head nodding in rhythm, front foot overstride, long
gliding hind reach. Flat-shod show form; the overstride is the breed —
draw the reach, not a generic trot.

### trakehner — `WARMBLOOD · EAST PRUSSIA`

The refined warmblood: floated trot, uphill athletic build, large gentle
eye. Keep the shoulder bare — no real brand marks; the horse is the
specimen.

## Alternates pool

american-paint-horse · knabstrupper · suffolk-punch · hanoverian ·
oldenburg · holsteiner · welsh-cob · exmoor-pony · dartmoor-pony ·
fell-pony · paso-fino · rocky-mountain-horse · missouri-fox-trotter ·
mangalarga-marchador · hackney · cleveland-bay · norman-cob ·
noriker · bashkir-curly

## Posting notes

When the user approves posting: one `type:tracking` parent issue titled
"Horse breeds — milestone cards, wave 2" with this format block and a
checklist of leaf issues; each leaf gets `type:illustration` +
`work:original`, inlines the format/delivery paragraph, and carries its
own brief, slug and milestone line. Claiming follows
`work/issue_claim.py`; see `.github/CLAIMS.md` and `.github/LABELS.md`.
