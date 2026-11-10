<div align="center">

# learn-dsh

**Turn DeepSeek Harness into a tutor that makes knowledge feel *obviously true*.**

[English](#english) | [中文](README.zh-CN.md)

</div>

---

## English

A DeepSeek Harness plugin adapted from
[amosblomqvist/learnharness](https://github.com/amosblomqvist/learnharness) — an
agent harness for learning. It measures before it teaches:

```
probe (binary-search the edge of your understanding)
  → plan (minimal dependency tree to your goal)
    → teach (one step → one check → repair or continue)
      → practice (retrieval drills with adaptive hints)
        → knowledge graph (~/.dsh/learn/graph.json, carries across sessions)
```

### ⭐ Why you want this

Ask a chatbot "explain X" and you get a lecture you'll forget in three days.
This plugin is different on four dimensions:

| | Plain chat | learn-dsh |
|---|---|---|
| Where it starts | the author's guess of your level | the **probed edge** of your actual understanding — everything you already hold is skipped, never re-taught |
| When errors surface | when you eventually notice | **at the step**, one check question after every single reasoning step — a misconception is repaired before anything is built on it |
| What "learned" means | you can recite it | it **feels obviously true** — you can derive it yourself from things you already accept |
| Memory | none, every session starts from zero | a persistent **knowledge graph** of propositions and reasoning chains; the next lesson starts where the last one ended |

### 🎯 A taste of it

You say: *"Teach me TCP's three-way handshake."*

A chatbot dumps a diagram and the words SYN, SYN-ACK, ACK. You nod. You forget.

learn-dsh does this instead:

> **Probe (3 questions, not 20):**
> "Before handshake — when two computers talk over TCP, what actually travels
> between them?" You say "signals?" — the ceiling drops. "Have you heard of a
> packet?" — "yeah, data gets split into packets." Floor found. Two more
> questions pin the strand: you hold *packets*, not *why connections exist*.
>
> **Plan (shown to you):**
> `packets (held) → why delivery needs agreement → what a sequence number is →
> why exactly 3 messages, not 2 or 4 → your goal`
>
> **Teach (each step lands, then is checked):**
> Step: "Packets get lost, delayed, and duplicated — every design about
> reliability follows from just that." Check: *"A packet sent twice arrives
> twice. What does the receiver need to tell the sender?"* You: "some
> confirmation." ✅ It landed — next step, each one deriving from the last.
>
> **Terminal condition:** the final check makes *you* derive why 2 messages
> can't work (your own words: "because the server can't tell if its reply
> arrived… oh, so the third message is the server learning that its SYN-ACK
> landed"). That's the click. **It feels obvious now. It will still feel
> obvious next month** — and the graph stored it, so next week's lesson on
> TLS starts from here, not from zero.

That is the difference: not a better explanation — a **teaching system**.

### 📦 What's inside

| Path | What it is |
|---|---|
| `learn.patch.yml` + `package.json` | Bundle patch: inserts the `learn` agent preset (persona + fs/bash/web/todo/ask-user/skill tools). No JS code |
| `skills/learn-teach/` | Teaching doctrine (probe → plan → teach → record) + full theory reference |
| `skills/learn-practice/` | Retrieval drills: one problem at a time, adaptive hints, slip/gap/misconception triage |
| `skills/learn-graph/` + `scripts/learn_graph.py` | Knowledge-graph engine (propositions + reasoning chains with provenance, Python stdlib only) |

### 🚀 Install

#### DeepSeek Harness desktop (manual, no build step)

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

#### Skills-only (works in any preset)

```sh
mkdir -p ~/.dsh/skills && cp -R skills/* ~/.dsh/skills/
```

### 💬 Usage

**Teach:**

```
Teach me TCP's three-way handshake
→ probes you question by question, then teaches one checked step at a time
```

**Practice:**

```
Drill me on the handshake we just learned
→ retrieval practice without re-teaching; hints adapt to your reasoning
```

**Graph (optional, manual):**

```sh
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py stats
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py propositions
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py find "*handshake*"
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py add-proposition \
  --name "Three-way handshake" --statement "TCP connection setup needs SYN, SYN-ACK, ACK"
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py add-chain \
  --premise n_0001 --premise n_0002 --conclusion n_0003
```

### 🔌 Why a plugin instead of using LearnHarness directly

Picture your actual day. You're working in DeepSeek Harness: your coding
sessions, your files, your web research, your API key — all already set up.
Tonight you want to finally understand the transformer attention mechanism.

**Using LearnHarness directly — the tax you pay:**

1. Download and install a second Electron app (~200 MB).
2. Open it. It knows nothing about you: configure a model provider again —
   find the API key, paste it, pick models, run its setup wizard.
3. Your lesson starts: "attach your notes" — but your notes live where you
   work, in the other app; re-upload them.
4. Mid-lesson it needs to fact-check something: it uses *its* search backend,
   which needs *its* Tavily/Brave key — another key to hunt down.
5. Done learning. Tomorrow morning you're back in DeepSeek Harness for work…
   and to keep learning you must open the *other* window again. Your learning
   history lives there, your work history here, keys configured in both places,
   two apps to update.

You adopted a method and paid for it with a **second life to maintain**.

**The plugin path — what actually happens:** you copy 14 files, restart the
harness, pick the `Learn` preset, and type "teach me attention". That's the
whole migration. The lesson runs on your existing key, your existing permission
presets; when it needs to fact-check, it uses the harness web tools you already
configured; your PDF is read in place by the filesystem tools you already have;
the knowledge graph lands in `~/.dsh/learn/` next to everything else. Next
morning, work session and study session are windows of the same app.

The general points, one line each:

- **One environment.** Same models, keys, permission presets, and session
  history you already have. Nothing to migrate.
- **The harness's tools power the method.** Lesson research uses the harness's
  web tools; your local PDFs are read in place by its filesystem tools; the
  graph lives in `~/.dsh/`.
- **Composable.** Cherry-pick: skills-only (on-demand, zero default change),
  full preset (always a tutor), or copy fragments into your own presets.
- **No second app.** It's 14 declarative files — read every line before you
  install. No app to download, sign, update, or keep open.

In short: **direct use = adopting a new product; the plugin = injecting a
method into the product you already chose.**

### 🙏 Acknowledgements

This project exists because of
**[amosblomqvist/learnharness](https://github.com/amosblomqvist/learnharness)**.
The teaching methodology — probing, the minimal dependency tree, one reasoning
step per check, unconditional truths first, "how could I have discovered
this?" — and the theory document bundled in
`skills/learn-teach/references/theory.md` are adapted from that project's
prompts and docs. I built a plugin that carries that method into DeepSeek
Harness; **all credit for the method belongs to the original author**. Please
star the upstream project, and if you can, use the full app — it has a dedicated
teaching UI, interactive demos, and a knowledge-graph viewer this plugin doesn't
ship.

### Requirements

- DeepSeek Harness desktop (Cordis patch layer, `dsh-agent-preset`,
  `dsh-skill-filesystem` — all shipped in the harness)
- Node ≥ 22 on the host; Python 3 for `learn_graph.py` (stdlib only)

### License

AGPL-3.0 (inherited from LearnHarness). See [LICENSE](LICENSE).
