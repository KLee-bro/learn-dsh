# learn-dsh — LearnHarness methodology as a DeepSeek Harness plugin

Brings the teaching harness from [amosblomqvist/learnharness](https://github.com/amosblomqvist/learnharness)
(AGPL-3.0) into DeepSeek Harness as a bundle plugin: an agent preset `learn` plus
three skills (`learn-teach`, `learn-practice`, `learn-graph`) and a persistent
knowledge graph stored at `~/.dsh/learn/graph.json`.

## What you get

- **Preset `learn`** — a session composition (persona + tools + skills) tuned for
  teaching. Switch to it in the GUI's preset picker.
- **learn-teach** — probe → plan (minimal dependency tree) → teach one reasoning
  step at a time with a check after every step → record propositions/chains.
- **learn-practice** — retrieval drills over previously taught material and the
  graph, one problem at a time, adaptive hints.
- **learn-graph** — read/search/extend `~/.dsh/learn/graph.json`
  (propositions + reasoning chains with provenance).

## Install status on this machine

Already installed and verified here:

- Package copied to `~/.dsh/profiles/desktop/node_modules/@likai/learn-dsh`.
- Full preset insert (`preset-learn`) appended to
  `~/.dsh/profiles/desktop/cordis.patch.yml` (YAML validated with a
  `!!js`-tolerant parser: 13 plugins).
- Skills copied to `~/.dsh/skills/` — `learn-graph` and `learn-practice` already
  appear in the session skill catalog; `learn-teach` was touched after the
  initial scan to retrigger discovery.

Restart DeepSeek Harness to load the `learn` preset, then pick **Learn** in the
preset picker.

## Manual install (other machines) — Option A: plugin manager

```sh
dsh plugin install /path/to/learn-dsh
```

## Manual install — Option B: same mechanism the helmd plugin uses

```sh
cp -R /Users/likai/work/helmd/learn-dsh ~/.dsh/profiles/desktop/node_modules/@likai/learn-dsh
cat >> ~/.dsh/profiles/desktop/cordis.patch.yml <<'EOF'
- insert:
    - id: preset-learn
      name: '@deepseek-ai/dsh-agent-preset'
      config:
        id: learn
        name: Learn
        description: "learn: LearnHarness-style tutor (probe -> plan -> teach -> practice)."
        order: 20
EOF
```

Then restart DeepSeek Harness (or `dsh plugin install` inside the profile to
re-link). The patch YAML in `learn.patch.yml` carries the full plugin list; the
minimal insert above is only needed if you install manually without the bundle
loader.

## Skills without the preset

If you only want the skills in your normal preset, copy them into the user skill
root and they appear in every session (rank 400 `user-dsh`):

```sh
mkdir -p ~/.dsh/skills
cp -R /Users/likai/work/helmd/learn-dsh/skills/* ~/.dsh/skills/
```

## Knowledge graph

```sh
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py stats
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py propositions
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py find "*chain rule*"
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py add-proposition \
  --name "Packets" --statement "All inter-computer communication is packets" \
  --session chat-2026-11-10
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py add-chain \
  --premise n_0001 --premise n_0002 --conclusion n_0003
```

## Verification status

- `learn_graph.py` — exercised end to end (add/remove/find/chains/json/stats) on
  a temp data dir; all commands behaved as documented.
- `learn.patch.yml` — written against the config schemas documented in the
  installed DSH bundle's package references (`dsh-agent-preset`, `dsh-persona`,
  `dsh-skill-filesystem.bundledSkillDir`); not yet live-installed into this
  profile. Install and check the preset picker for `Learn`.

## Attribution

Methodology and prompt doctrine adapted from LearnHarness
(github.com/amosblomqvist/learnharness), AGPL-3.0. This plugin keeps the same
license.
