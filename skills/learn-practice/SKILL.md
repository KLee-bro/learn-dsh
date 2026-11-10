---
name: learn-practice
description: Run a LearnHarness-style practice session — retrieval and application without re-teaching. Pose varied problems that draw on previously taught material (optionally from the knowledge graph), commit to a solution only after the learner answers, then reveal and compare. Use for review, drills, and transfer problems.
whenToUse: The learner asks to practice, review, drill, or test themselves on material they have already been taught.
---

# Practice session

Adapted from LearnHarness (AGPL-3.0). Practice is **not teaching**: no lectures,
no re-explanations up front. Problems make previously built knowledge come to
mind without being named first.

## Load the material

Pick material from, in priority order:

1. What the learner names ("practice the chain rule").
2. The knowledge graph: `python3 scripts/learn_graph.py propositions` and
   `chains` (resolve `scripts/` relative to this skill directory). Chains are
   the best source — a chain's conclusion is exactly the kind of fact that
   should be retrievable from its premises.

Read the doctrine: it is short and it governs everything below.

## Session rules

- **One problem at a time.** Pose it, then stop and wait. Never pose a problem
  and continue talking.
- **Varied problems.** Change surface features so the right knowledge must be
  recognized, not pattern-matched: standard, inverted, "when does this fail?",
  "construct an example", transfer to a neighboring domain, estimate-before-
  compute. Difficulty adapts to the learner's reasoning, not a fixed ladder.
- **Hints adapt to reasoning.** If the learner is stuck, give the smallest hint
  that unblocks: a question pointing at the relevant premise, not the answer.
  Never name the needed fact unless two graded hints have failed.
- **Diagnose, don't grade.** Wrong answers get the probe treatment: is it a
  slip, a gap, or a misconception? A misconception ends the drill for that fact
  and becomes a candidate for a follow-up *teaching* session — record it.
- **Think out loud.** Invite the learner to show their reasoning. Their
  intermediate steps are the data.

## Feedback cadence

For each problem: learner answers → brief verdict + the crispest possible
comparison against the correct line of reasoning (why the right answer had to
be right, tied to their own premises) → next problem, or a short repair if the
miss was a misconception. Keep feedback tight; the learner's effort goes into
problems, not prose.

## Closing

End with a two-line summary: what held solid, what wobbled. If new
propositions/chains were encountered (from imported material or repairs), add
them to the graph with `scripts/learn_graph.py add-proposition` / `add-chain`.
Do not score the learner; store ideas and connections, not ratings.
