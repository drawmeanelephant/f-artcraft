# Consolidation agent brief

Use a separate consolidation branch based on current main. This is a
maintenance pass, not an art revision or permission to publish anything.

1. Read `AGENTS.md`, `prompts/README.md`, the source fragments and all pending
   inbox notes. Check the referenced revisions and proofs where available;
   do not turn an unverified claim into a rule.
2. Group repeated lessons. Fold verified, general constraints into the
   relevant core/series fragment; retain concrete per-piece findings in
   `prompts/analysis/`. Keep guest appreciation distinct from in-house
   critique. Preserve all original prompts and cultural guardrails.
3. For conflicting proposals, prefer demonstrated evidence under current
   rules. Leave unresolved notes pending and ask the user if a design
   decision is needed. Do not silently erase an objection.
4. Keep prompt status honest: a draft is not an issue, a closed issue is not
   proof of merged artwork, and a merged piece is not proof it passed its
   critique. Do not maintain exhaustive roster prose from memory; inspect
   the current tree when an inventory is needed.
5. Move only resolved notes to `prompts/archive/`, preserving their content.
   Record the resolution and destination in a new
   `prompts/analysis/<date>-<batch>.md` file, with links to the archived notes.
   Leave unresolved notes in the inbox. Do not rewrite prior artwork,
   revision-specific drivers or archived evidence.
6. Run:

   ```sh
   python3 -m unittest discover -s work -p 'test_build_prompts.py'
   python3 work/build_prompts.py --output PROMPTS.md
   ```

7. Review the diff: no lost prompts, links still work, proposals are clearly
   marked, and no generated site files or PDF proofs are included. Explain
   which lessons were adopted, deferred or rejected.

Keep the consolidation commit separate from art tasks. Do not post issues,
schedule agents, commit, push or open a PR unless that action was requested.
