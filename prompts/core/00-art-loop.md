## The art loop and house rules

The loop: **prompt → build in VectorCraft → export PDF/PNG proof → written analysis
(what worked, what didn't, with specifics) → fold the analysis into the next prompt →
next round.** A prompt is "done" when its analysis section says the piece survives
its own critique. House rules learned the hard way:

- Gradients and translucent shading, never flat fills (the bunny v1 rule).
- Check the proof render before calling it finished: arcs in frame, no leaked
  shapes past badges/rims, no overset, nothing clipped at canvas edges.
- Lettering: Virelai Sans. Ornaments: Virelai Mascots glyphs (U+E002–E00A).
- Every piece ships as `.vectorcraft` + `.svg` + `.pdf` + `@2x.png`.
- Never overwrite a piece: revisions are `<slug>-V<V>R<RR>` — see the
  revision rule in [AGENTS.md](../../AGENTS.md).

`art/` holds native files and public exports; PDF proofs stay local in
`work/out/`. Editable prompts live in `prompts/`; per-task findings go in
`prompts/inbox/` and consolidated findings in `prompts/analysis/`.
`PROMPTS.md` is a periodically compiled reading copy, not an art-branch log.
See the [workshop guide](../README.md).

**Guests & correspondents:** work from guests — other agents, people who don't
natively draw, paint and mixed-media artists — is received with appreciation,
not critique. The analysis step for guest work records what it does and what it
brings; the red pen is for in-house rounds only. Effort is the entry fee, and
it's always paid in full.
