<div align="center">

# learn-dsh

**Turn DeepSeek Harness into a tutor that makes knowledge feel *obviously true*.**

**把 DeepSeek Harness 变成一个让知识"显然如此"的私人教师。**

English | [中文](#中文)

</div>

---

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

一个基于 [amosblomqvist/learnharness](https://github.com/amosblomqvist/learnharness)
改造的 DeepSeek Harness 插件。它**先测量、再教学**：

```
摸底（逐题二分，定位你知识的确切边界）
  → 规划（通往目标的最小依赖树）
    → 教学（一小步 → 一道检查题 → 修或进）
      → 练习（检索式刷题，提示随你的推理自适应）
        → 知识图谱（~/.dsh/learn/graph.json，跨会话累积）
```

## ⭐ Why you want this / 你能得到什么

**English.** Ask a chatbot "explain X" and you get a lecture you'll forget in
three days. This plugin is different on four dimensions:

| | Plain chat / 普通对话 | learn-dsh |
|---|---|---|
| Where it starts | the author's guess of your level | the **probed edge** of your actual understanding — everything you already hold is skipped, never re-taught |
| When errors surface | when you eventually notice | **at the step**, one check question after every single reasoning step — a misconception is repaired before anything is built on it |
| What "learned" means | you can recite it | it **feels obviously true** — you can derive it yourself from things you already accept |
| Memory | none, every session starts from zero | a persistent **knowledge graph** of propositions and reasoning chains; the next lesson starts where the last one ended |

**中文。** 你对 ChatGPT 说"给我讲讲 X"，得到的是一篇三天后就忘的讲义。这个插件在四个维度上完全不同：

| | 普通对话 | learn-dsh |
|---|---|---|
| 从哪讲起 | 作者猜的水平 | **实测**的知识边界——你已掌握的跳过不讲 |
| 错误何时暴露 | 等你自己发现 | **每一步都有检查题**，误解当场修掉，绝不带着裂缝往上盖 |
| 什么叫"学会了" | 能背出来 | **觉得显然如此**——能从你已接受的事实自己推出来 |
| 记忆 | 无，每次从零开始 | 持久**知识图谱**：命题 + 推理链，下次课从上次结束处继续 |

## 🎯 A taste of it / 一个例子看懂它

**English.** You say: *"Teach me TCP's three-way handshake."*

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

**中文。** 你说：**"教我 TCP 三次握手。"**

ChatGPT：甩给你一张图和 SYN、SYN-ACK、ACK 三个词。你点头。你忘了。

learn-dsh 是这样做的：

> **摸底（3 道题，不是 20 道）：**
> "先不管握手——两台电脑走 TCP 通信时，中间实际传的是什么？" 你答"信号？"——
> 上界降下来。"听说过数据包吗？"——"知道啊，数据会拆成包发。"下界找到了。
> 再两题锁定：你手里握着的是"数据包"，缺的是"为什么需要连接"。
>
> **规划（展示给你）：**
> `数据包（已掌握）→ 为什么传输需要双方确认 → 序号是什么 → 为什么恰好 3 次，
> 2 次和 4 次为什么不行 → 你的目标`
>
> **教学（每步落地，立即检查）：**
> 一小步："包会丢、会迟到、会重复——关于可靠性的一切设计都从这一句话推出来。"
> 检查题：*"同一个包被发了两次、收到两次，接收方需要告诉发送方什么？"*
> 你："某种确认。" ✅ 落地了——下一步，每一步都从上一步推导出来。
>
> **终点：** 最后一道检查题让你**自己推出**为什么 2 次不行（你的原话："因为服务端
> 不知道它的回应有没有到达……哦！所以第三次握手是服务端确认自己的 SYN-ACK 到了"）。
> 这就是"咔哒"一声——**现在觉得显然，下个月还是觉得显然**。而且图谱已经把它存下
> 了，下周学 TLS 时从这里开始，而不是从零开始。

That is the difference: not a better explanation — a **teaching system**.

这就是区别：不是更好的讲解，而是一套**教学系统**。

## 📦 What's inside / 仓库内容

| Path / 路径 | What it is / 说明 |
|---|---|
| `learn.patch.yml` + `package.json` | Bundle patch: inserts the `learn` agent preset (persona + fs/bash/web/todo/ask-user/skill tools) / 补丁层：插入 `learn` preset（教学人格 + 全套工具），无 JS 代码 |
| `skills/learn-teach/` | Teaching doctrine (probe → plan → teach → record) + full theory / 教学会话完整方法论，附理论全文 |
| `skills/learn-practice/` | Retrieval drills: one problem at a time, adaptive hints, slip/gap/misconception triage / 练习会话：一次一题、提示自适应、错因三分法 |
| `skills/learn-graph/` + `scripts/learn_graph.py` | Knowledge-graph engine, Python stdlib only / 知识图谱引擎（命题 + 推理链 + 来源，纯标准库） |

## 🚀 Install / 安装

### DeepSeek Harness desktop (manual, no build step / 手动安装)

```sh
# 1. copy the package into the profile / 把包复制进 profile
mkdir -p ~/.dsh/profiles/desktop/node_modules/@likai
cp -R learn-dsh ~/.dsh/profiles/desktop/node_modules/@likai/learn-dsh

# 2. append the preset insert to the profile patch layer / 追加 preset 到补丁层
cat learn.patch.yml >> ~/.dsh/profiles/desktop/cordis.patch.yml

# 3. make the skills available everywhere / 技能装到用户根目录
mkdir -p ~/.dsh/skills
cp -R skills/* ~/.dsh/skills/

# 4. restart DeepSeek Harness and pick the "Learn" preset / 重启后选 Learn preset
```

If your deployment ships the plugin-manager tools, `dsh plugin install learn-dsh`
handles steps 1–2. / 如果你的部署带插件管理工具，`dsh plugin install learn-dsh` 一步完成前两步。

### Skills-only (works in any preset / 只装技能，任何 preset 可用)

```sh
mkdir -p ~/.dsh/skills && cp -R skills/* ~/.dsh/skills/
```

## 💬 Usage / 怎么用

**Teach / 教学：**

```
教我 TCP 三次握手        → probes you, then teaches one checked step at a time
Teach me the chain rule  → 同上，英文也可以
```

**Practice / 练习：**

```
练一下刚才学的三次握手    → drills without re-teaching; hints adapt to your reasoning
```

**Graph / 图谱（可选，手动维护）：**

```sh
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py stats
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py propositions
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py find "*握手*"
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py add-proposition \
  --name "三次握手" --statement "TCP 连接建立需要 SYN、SYN-ACK、ACK 三次交互"
python3 ~/.dsh/skills/learn-graph/scripts/learn_graph.py add-chain \
  --premise n_0001 --premise n_0002 --conclusion n_0003
```

## 🔌 Why a plugin instead of using LearnHarness directly / 为什么做成插件，而不是直接用 LearnHarness

**English.** LearnHarness is a **standalone Electron app**: its own chat UI, its
own model-provider configuration, its own storage. If you already live inside
DeepSeek Harness — your presets, tools (bash, web, filesystem, todos,
sub-agents), settings and session history — adopting LearnHarness directly means
rebuilding that life in a second app: re-configuring API keys, giving up your
toolchain, keeping two chat histories.

This plugin takes LearnHarness's **actual asset** — the teaching methodology,
distilled in its prompts and theory docs — and mounts it **inside the harness
you already use**:

- **One environment.** Same models, keys, permission presets, and session
  history you already have. Nothing to migrate.
- **The harness's tools power the method.** Research during a lesson uses the
  harness's web tools; reading your own PDFs uses its filesystem tools; the
  graph lives next to your other harness data (`~/.dsh/`).
- **Composable.** The teaching persona is a preset row + skills, so you can
  cherry-pick: skills-only (zero prompt change, on-demand), full preset (always
  a tutor), or copy fragments into your own presets.
- **No second app to update, sign, notarize, or keep open.** It's a 14-file
  declarative patch — read every line before you install it.

In short: **direct use = adopting a new product; the plugin = injecting a
method into the product you already chose.**

**中文。** LearnHarness 是一个**独立的 Electron 应用**：自带聊天界面、自己的
模型配置、自己的存储。如果你平时已经生活在 DeepSeek Harness 里——你的 preset、
工具（bash、web、文件系统、todo、子代理）、会话历史都在这里——直接用
LearnHarness 意味着在第二个应用里重建这套生活：重新配 API key、放弃现有工具链、
维护两份聊天记录。

这个插件拿走 LearnHarness **真正的资产**——凝结在其提示词和理论文档里的教学
方法论——然后**装进你本来就在用的 harness**：

- **一个环境。** 模型、key、权限、会话历史全是你现有的，零迁移。
- **harness 的工具为方法论供能。** 课上查资料用 harness 的 web 工具，读你本地
  的 PDF 用文件系统工具，图谱存在你其它 harness 数据旁边（`~/.dsh/`）。
- **可组合。** 教学人格 = 一个 preset 行 + 三个 skill，可以拆开用：只装技能
  （不改变默认行为，随叫随到）、整套 preset（永远当老师）、或把片段抄进你自己的 preset。
- **没有第二个应用要安装、更新、签名。** 全部是 14 个文件的声明式补丁——装之前每一行都能读完。

一句话：**直接用 = 接受一个新产品；用 plugin = 把一套方法注入你已经选定的产品。**

## 🙏 Acknowledgements / 致谢

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

本项目得以存在，全因为
**[amosblomqvist/learnharness](https://github.com/amosblomqvist/learnharness)**。
教学方法论——摸底、最小依赖树、每步一查、无条件事实先行、"你自己怎么会发现它"——
以及 `skills/learn-teach/references/theory.md` 里 bundled 的理论文档，都改编自
该项目的提示词与文档。我做的是一个把这套方法带进 DeepSeek Harness 的插件；
**方法论的全部功劳属于原作者**。请给上游项目点 star；如果可以，直接使用完整
应用——它有专门的教学界面、交互演示和图谱视图，是这个插件没有的。

## Requirements / 环境要求

- DeepSeek Harness desktop (Cordis patch layer, `dsh-agent-preset`,
  `dsh-skill-filesystem` — all shipped in the harness)
- Node ≥ 22 on the host; Python 3 for `learn_graph.py` (stdlib only)

## License / 许可

AGPL-3.0 (inherited from LearnHarness). See [LICENSE](LICENSE).
/ AGPL-3.0（继承自上游 LearnHarness），详见 [LICENSE](LICENSE)。
