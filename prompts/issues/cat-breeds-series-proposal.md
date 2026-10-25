# Cat breeds — milestone cards, new series (proposal)

Status: draft proposal, not posted. One tracking issue plus twelve leaf
issues; each leaf is one new piece.

## Rationale

The natural sibling of `dog-breeds` and `horse-breeds`: a third domestic
breed series on the same chassis. Cats give the plate a different
geometry — compact bodies, negative-space poses, coat texture as the
whole drawing — and they don't collide with `art/animals/`, which covers
wild species (pallas-cat is wild, not a domestic breed).

## Format (milestone cards — field-plate chassis)

- 1000×1000 canvas: dark moody backdrop → large gradient plate disc
  (centre 500,460, r≈420) → subject → name in caps, Virelai Sans ~56–60pt
  at y≈930.
- The milestone line under the name in caps, Virelai Sans ~22–24pt, wide
  tracking, y≈968, ≤760pt wide — check it clears the disc's lower arc.
- Gradients and translucent shading, never flat fills. Warm dark ink,
  never pure black. Nothing crosses the rim; shapes near the lower edge
  close on the disc's own arc.
- Keep the breed-defining traits accurate to type (coat length, ear set,
  tail, points); thin essentials — whiskers, tufts — ≥3pt or they vanish
  at plate scale, and the whole cat inside the rim. The milestone line
  is the body/coat class and origin — `CLASS · ORIGIN` — where CLASS is
  the one-word signature trait (SHORTHAIR, LONGHAIR, HAIRLESS, TAILLESS,
  TICKED, FOLD, SWIMMER …).
- First pass is `<slug>-V1R00`. Deliverables on main:
  `art/cat-breeds/<slug>/<slug>-V1R00.vectorcraft` + `.svg` and driver
  `work/cat-breeds/draw_<slug>.py`; the `@2x.png` proof goes to the
  `media` branch; the `.pdf` stays in `work/out/` (local only).
- New directories on first leaf: `art/cat-breeds/`, `work/cat-breeds/`.

## Proposed leaves (12)

### abyssinian — `TICKED · ABYSSINIA`

The ticked tabby shimmer: lithe oriental body, large ears, every hair
banded. Alert standing pose; banding the coat tones is the whole
drawing.

### bengal — `HYBRID · UNITED STATES`

The miniature leopard: rosetted or marbled gold coat, athletic stance
mid-prowl. Wild-cat pattern at domestic scale — rosettes, not stripes.

### british shorthair — `SHORTHAIR · BRITAIN`

The plush teddy bear: cobby body, dense blue-grey coat, copper eyes,
round cheeks. Seated loaf; density of coat shown by sheen zones, not
hatching every hair.

### maine coon — `LONGHAIR · MAINE`

The gentle giant: ear tufts and lynx tips, long rectangular body, bushy
tail. Standing profile so the tail drapes the floor ellipse.

### manx — `TAILLESS · ISLE OF MAN`

The rumpy: round everything — round head, round rump, no tail, hind legs
longer than front. The absence of a tail is the silhouette; compose so
the rump reads.

### persian — `LONGHAIR · PERSIA`

Flat face under a waterfall of coat; stocky body hidden in fur. Big
round copper eyes do the work — keep the face from going smug.

### ragdoll — `POINTED · CALIFORNIA`

Blue-eyed pointed soft-body: the breed's limp-doll flop translated to a
relaxed sprawl — the only card allowed to abandon a standing pose
entirely.

### russian blue — `SHORTHAIR · RUSSIA`

Silver-tipped blue coat, emerald eyes, faintly smiling mouth corners.
Elegant arch of neck; the double coat's silver sheen is the gradient
test.

### scottish fold — `FOLD · SCOTLAND`

Folded ears lying flat to the skull like a bonnet, owl-round face. The
breed's upright Buddha sit is permitted — and charming.

### siamese — `SHORTHAIR · SIAM`

Cream body, seal points, angular wedge head, whippy tail. The mask is
the portrait; keep the blue eyes subtle, not cartoon-cyan.

### sphynx — `HAIRLESS · CANADA`

No coat to hide behind: wrinkled warm skin, bat ears, pot-bellied sit or
a regal stretch. Translucency sells living skin, not plastic.

### turkish van — `SWIMMER · TURKEY`

The swimming cat: white body, auburn head-and-tail markings (the van
pattern), half out of water or beside a pool with drops on the coat.

## Alternates pool

egyptian-mau · norwegian-forest-cat · japanese-bobtail · devon-rex ·
cornish-rex · bombay · birman · chartreux · korat · munchkin ·
savannah · ocicat · siberian · tonkinese · burmese · himalayan ·
somali · american-shorthair · oriental-shorthair · turkish-angora

## Posting notes

When the user approves posting: one `type:tracking` parent issue titled
"Cat breeds — milestone cards, wave 1" with this format block and a
checklist of leaf issues; each leaf gets `type:illustration` +
`work:original`, inlines the format/delivery paragraph, and carries its
own brief, slug and milestone line. Claiming follows
`work/issue_claim.py`; see `.github/CLAIMS.md` and `.github/LABELS.md`.
