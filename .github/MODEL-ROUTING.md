# Find the model's strengths before widening its lane

Native files make experiments and repairs cheaper. They do not supply
judgment, anatomy, composition or interaction understanding a model lacks.
The target is **cost per accepted result**, including retries, review and
repair, not the cheapest first draft. No benchmark is launched by this
document; model calls and their spend need an approved trial budget.

## Test task families, not one universal model ranking

Start with bounded adaptations of approved work. These are hypotheses to
test, not claims about what inexpensive models can already do:

| Family | Bounded trial | What can still fail |
| --- | --- | --- |
| Palette/material variation | Same approved object and geometry, one new lighting/palette brief | Flat volume, broken material, unreadable type |
| Geometric/icon family | Extend a small approved icon family at specified sizes | Inconsistent stroke, optical weight, poor small-size reading |
| UI states/layout | Extend existing components to named states or a longer-label layout | Missing focus/disabled meaning, detached instances, overset |
| Organic subject/pose | A modest pose change from an approved native | Anatomy, silhouette, expression and recognizable identity |
| Defect repair | One verified rim, spacing or attachment defect | Fixing one symptom while damaging composition elsewhere |
| Visual critique | Find defects in known-bad and known-good proofs | Missing real defects or inventing faults in correct work |

Do not assume a model that writes reliable geometry also judges a face,
or that an inexpensive generator is a reliable visual reviewer.
Original art direction remains a separate capability.

## A small, comparable trial

1. Choose only the families we need now. Pin approved native inputs,
   references, tool build and acceptance constraints. Use at least two
   distinct examples in a family, including one held-out example.
2. Give candidates the same information and a fixed edit/render budget.
   Record exact provider/model/options; never call an unknown price
   “cheap.” Use separate immutable revisions and unique drivers.
3. Allow at most **two edit → render → inspect passes** in the pilot.
   Record help received, including corrected scripts or senior-model
   critique. A rescued result is assisted performance, not independent
   success. If the same defect persists, stop and escalate.
4. Check the saved native reopens and remains editable; render with the
   actual app. Check boundaries, type, artifact completeness and task
   constraints. UI work also checks states, component reuse, layout and
   the target renderer's contract.
5. Review proofs without model names against the approved reference and
   fixed brief. Prefer human or independently qualified visual review.
   Mechanical checks alone do not approve artistic quality; self-critique
   alone does not qualify its own generator.
6. Compare acceptable results, regressions, assistance, elapsed time,
   total tokens/cost if available, reviewer effort and repair cost.
   Report missing cost data as unknown. A rejected native costs money too.

## Route narrowly, and keep the escape hatch

Record a dated, provisional profile per **model + task family + tool
build**, not a permanent verdict on the whole model. A pass earns a
bounded lane first; it does not unlock every variation or original design.
Re-evaluate after meaningful model/tool changes.

Until evidence exists, keep assignments explicit. Do not automatically
route every `work:variation` issue to a lower-cost model, relax acceptance
to improve pass rates, or send the same failing task through endless
retries. Escalation preserves the last approved native and identifies the
missing skill. Use [the trial note](../prompts/templates/model-trial.md) to
capture results without editing the shared prompt bank.
