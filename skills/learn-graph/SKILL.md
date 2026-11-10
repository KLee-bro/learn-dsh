---
name: learn-graph
description: Read, search, extend, and maintain the learner's persistent knowledge graph at ~/.dsh/learn — propositions and reasoning chains accumulated across teaching and practice sessions. Use to review what has been covered, find connections across subjects, or before planning a new lesson.
---

# Knowledge graph

The graph stores **propositions** (individual claims) and **chains** (premises
that jointly imply a conclusion), with provenance to the session that produced
them. Plain JSON at `~/.dsh/learn/graph.json` (override with `--data-dir`).

All operations go through the reader/writer script; resolve `scripts/` relative
to **this skill directory**. Standard library only, no network.

```sh
# Inspect
python3 scripts/learn_graph.py stats
python3 scripts/learn_graph.py propositions [--session ID]
python3 scripts/learn_graph.py chains [--node ID]
python3 scripts/learn_graph.py find "chain rule"        # substring; * is the only wildcard

# Extend
python3 scripts/learn_graph.py add-proposition --name "..." --statement "..." [--aliases "..."] [--session ID]
python3 scripts/learn_graph.py add-chain --premise ID --premise ID --conclusion ID [--session ID]

# Maintain
python3 scripts/learn_graph.py remove ID
python3 scripts/learn_graph.py export --format json     # full graph to stdout
```

## Interpretation rules

- The graph is an **intended map of encountered ideas**, not a mastery record.
  A proposition being present does not establish that the learner understood,
  accepted, or retained it. Absence does not establish ignorance.
- Chains mean **joint** implication: all premises together yield the conclusion.
  A single premise does not.
- Statement text is model-authored and can be wrong; prefer the learner's own
  session record when they disagree.
- `--session` filters propositions by first provenance, not every mention.

## Before planning a lesson

Always read `stats` and search for propositions near the lesson topic. Held
strands skip re-probing; existing chains show you the derivations already built,
so new teaching attaches to them instead of rebuilding.
