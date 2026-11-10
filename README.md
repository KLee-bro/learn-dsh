# learn-dsh

**LearnHarness-style teaching harness as a DeepSeek Harness plugin.**

Adapted from [amosblomqvist/learnharness](https://github.com/amosblomqvist/learnharness)
(AGPL-3.0). It turns a DeepSeek Harness session into a tutor that **measures
before it teaches**: probes your current understanding, plans the minimal
dependency tree to your goal, teaches **one reasoning step at a time with a
check after every step**, runs retrieval practice, and accumulates a persistent
knowledge graph across sessions.

```
probe (binary-search every knowledge strand)
  → plan (minimal dependency tree, shown as a coarse map)
    → teach (step → check → repair-or-continue)
      → practice (retrieval drills, adaptive hints)
        → knowledge graph (~/.dsh/learn/graph.json)
```

## What's inside

| Path | What it is |
|---|---|
| `learn.patch.yml` | Bundle patch: inserts a `learn` agent preset (persona + fs/bash/web/todo/ask-user/skill tools) |
| `skills/learn-teach/` | The teaching session doctrine (probe → plan → teach → record) + full theory reference |
| `skills/learn-practice/` | Retrieval drill doctrine: one problem at a time, adaptive hints, slip/gap/misconception triage |
| `skills/learn-graph/` | Knowledge-graph reader/writer rules |
| `scripts/learn_graph.py` | Graph engine (Python stdlib only): propositions + reasoning chains with provenance, JSON store |

No JS plugin code — the whole plugin is a declarative patch layer plus skills.

## Install

### Desktop DeepSeek Harness (manual, no build step)

```sh
# 1. copy the package into the profile
mkdir -p ~/.dsh/profiles/desktop/node_modules/@likai
cp -R learn-dsh ~/.dsh/profiles/desktop/node_modules/@likai/learn-dsh

# 2. append the preset insert to the profile patch layer
cat learn.patch.yml >> ~/.dsh/profiles/desktop/cordis.patch.yml

# 3. make the skills available everywhere
mkdir -p ~/.dsh/skills
cp -R skills/* ~/.dsh/skills/

# 4. restart DeepSeek Harness and pick the "Learn" preset
```

If your deployment ships the plugin-manager tools, `dsh plugin install learn-dsh`
handles steps 1–2.

### Skills-only (any preset)

```sh
mkdir -p ~/.dsh/skills && cp -R skills/* ~/.dsh/skills/
```

## Usage

- **Teach**: "教我 TCP 三次握手" / "teach me the chain rule" — the agent probes
  your level question by question (answer confidently and it escalates; miss and
  it narrows in), shows a plan map, then teaches with a check after every step.
- **Practice**: "练一下刚才学的三次握手" — drills without re-teaching; hints
  adapt to your reasoning.
- **Graph**: propositions/chains live in `~/.dsh/learn/graph.json`.

```sh
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py stats
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py propositions
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py find "*握手*"
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py add-proposition \
  --name "三次握手" --statement "TCP 连接建立需要 SYN、SYN-ACK、ACK 三次交互"
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py add-chain \
  --premise n_0001 --premise n_0002 --conclusion n_0003
```

The graph is what makes sessions compose: the next lesson skips everything you
already hold and starts at your knowledge edge.

## Why this beats "explain X to me"

| | Plain chat | learn-dsh |
|---|---|---|
| Starting point | author's guess | probed edge of your understanding |
| Errors | found when you notice | caught at the step, repaired before anything is built on it |
| Goal | explanation delivered | goal understanding feels obviously true |
| Memory | none | persistent propositions + reasoning chains |
| Your effort | reading + logistics | material only (the agent owns logistics) |

Cost: roughly 1.5× the tokens of a plain explanation, spent on interaction
instead of lecture volume.

## Requirements

- DeepSeek Harness desktop ( Cordis bundle patch layer, `@deepseek-ai/dsh-agent-preset`,
  `@deepseek-ai/dsh-skill-filesystem` — all shipped in the harness)
- Node ≥ 22 for the host; Python 3 for `learn_graph.py` (stdlib only)

## License

AGPL-3.0 (inherited from LearnHarness, whose methodology and doctrine this
plugin adapts). See [LICENSE](LICENSE).
