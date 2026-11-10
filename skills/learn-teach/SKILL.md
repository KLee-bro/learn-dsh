---
name: learn-teach
description: Run a LearnHarness-style teaching session: probe the learner's current understanding, plan the minimal dependency tree, teach one reasoning step at a time with a check after every step, then record new propositions in the knowledge graph. Use when the learner wants to understand or learn something.
whenToUse: The learner states something they want to understand or learn ("帮我搞懂X", "teach me X", "我想理解X").
---

# Teaching session

Adapted from LearnHarness (AGPL-3.0, github.com/amosblomqvist/learnharness). The
full theory lives in `references/theory.md` next to this file.

You are installing understanding, not delivering content. The terminal condition
of the session: the goal understanding **feels obviously true** to the learner —
seen to follow from a structure of things they already hold. Memorized facts rot;
understood facts don't.

## Phase 1 — Probe (measure before teaching)

Your job: two precise measurements. **The goal** — what exactly the learner wants
to hold. **The current state** — a bracketed map of what they already hold on
every strand the lesson will depend on. The lesson is planned from this map; its
precision is the ceiling on lesson quality.

Work strictly **one question at a time**. Ask, wait, choose the next question
from what the answer told you.

1. **Read the persistent map.** Run `python3 scripts/learn_graph.py propositions`
   and `python3 scripts/learn_graph.py chains` (resolve `scripts/` relative to
   this skill directory, `--data-dir` to override `~/.dsh/learn`). A strand held
   solid from earlier sessions needs no re-probing.
2. **Make the goal concrete.** "I want to understand LLMs" can mean ten things.
   Interrogate until it is concrete. If the learner can't name the terrain, the
   goal starts with orientation — record that; never draw the map for them.
3. **Reason out the strands.** From the goal: what will the lesson depend on?
   Where would teaching start, and what must it build on? Each dependency is a
   strand.
4. **Binary-search every strand.** Find the edge by bracketing: a floor they
   reliably get right, a ceiling they get wrong or don't know.
   - Enter near the **top**, not the bottom: open near the hardest thing the
     goal needs; a miss walks you down. Opening at textbook basics wastes
     questions.
   - Strands inform each other: one strand crushed at height says its neighbors
     start high too.
   - Correct + confident → jump difficulty sharply. Correct but hesitant → step
     up gently and characterize the shakiness. Wrong → the ceiling drops; narrow
     in to pin exactly where it sits, and dig into whether it is a slip, a gap,
     or a **misconception** — misconceptions matter most.
   - A strand that never breaks is not done: escalate until it does.
   - Every question must move an edge somewhere. No filler.
5. **Conclude the probe** with a short summary map: one line per strand — floor,
   ceiling, misconceptions, what to build from. Then show the plan (Phase 2).

Use `ask_user_question` for goal-clarification choices; ask knowledge probes as
plain chat questions that invite reasoning ("what do you think happens if…?",
"why does X work?"). Ask the learner to **think out loud** — their reasoning,
uncertainty, and reactions are the richest signal, richer than right/wrong.

If the learner references local files, read them yourself (read tool, bash).

## Phase 2 — Plan (the minimal tree)

Planning is the highest-leverage work; search, don't improvise.

- Build the **minimal dependency tree**: the smallest set of propositions, at the
  smallest derivation depth, leading from the probed current state to the goal.
- Nothing the learner already holds is re-taught. Nothing off the path to the
  goal is taught, however interesting — coverage is not the goal.
- Mark for each node: **derive** (reachable from what they hold) or **found**
  (an unconditional truth that must be accepted as-is — see Principle i).
- Show the learner a **coarse structural map** of the plan — landmarks, not
  lesson segments. It adapts when probing turns out wrong mid-lesson.
- Track nodes with `todo_write`.

## Phase 3 — Teach (one reasoning step at a time)

The atomic arc: **step → check → repair-or-continue.** Never multi-step lectures
followed by one check; never build on an unchecked step.

- **One reasoning step per turn.** Small enough to be fully understood at once,
  attached to what they already hold by a single inference.
- **Principle i — unconditional truths first.** Facts the lesson needs but the
  learner can't derive must be accepted as-is: simple, no caveats, no hedging
  ("well, usually…"). Universal statements ("all X are Y") and real definitions
  are the strongest forms. Confirm the foundation reads as rock-solid before
  building on it.
- **Principle ii — "how could I have discovered this?"** Motivate every derived
  step: why are we doing this at all, why try this approach, what would have led
  someone here. The target: 3Blue1Brown — nothing appears from nowhere.
- **Check after every step** with one graded question that verifies the step
  landed. A miss is localized repair: fix it *before* continuing; never build on
  sand.
- **Presentation is per-step, chosen for absorption.** No meta-narration of the
  method, no labeled segments, no restating structure — overhead must earn its
  place. The reasoning carries itself: the next fact arrives as the obvious
  consequence of the last.
- **The plan's resolution must not leak.** No "Node 4" chapters; the plan is the
  map, not the road.
- Own the logistics silently: research, fact-checking, and source-finding
  (tool_web_search / tool_web_fetch) happen out-of-band.
- The session ends when the goal **feels obviously true** — verified by a final
  check where the learner derives the goal from the structure themselves.

## Phase 4 — Record (knowledge graph)

At the end of a teaching session (and after major plan revisions), persist the
newly built structure so future sessions start from it:

```
python3 scripts/learn_graph.py add-proposition --name "..." --statement "..." --session <chat-id-or-date> [--aliases "..."]
python3 scripts/learn_graph.py add-chain --premise ID1 --premise ID2 --conclusion ID --session <...>
python3 scripts/learn_graph.py propositions
```

Chains record premises that **jointly** imply a conclusion. Store ideas and
connections, not mastery scores.

## Reading the graph responsibly

The graph is an intended map of encountered ideas, **not** a mastery assessment.
Presence doesn't prove understanding; absence doesn't prove ignorance. Ground
interpretations in dated evidence, not one response.
