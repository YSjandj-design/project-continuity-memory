# Project Continuity Memory

**接着做项目，而不是重放对话。**

Project Continuity Memory 是一套本地优先、仓库原生的 AI Agent 项目接力协议。
它让 Agent 在跨任务、跨窗口、跨模型或换人之后，从“已经核验的当前状态”继续，
而不是靠重读聊天记录猜测进度。

它只使用两份精简文件：

- `PROJECT_MEMORY.md`：保存跨任务稳定有效的项目认知。
- `HANDOFF.md`：保存当前目标、已验证进度、阻塞、证据和精确下一步。

配套 Agent Skill 规定何时读取、如何处理陈旧状态以及收尾时写回什么；验证脚本
负责控制结构、篇幅和接力完整性。

## 它解决的不是“记住所有聊天”

所有长期 Agent 项目迟早都会遇到一次冷启动：新任务、新窗口、模型切换、上下文
压缩，或者换一个人接手。

聊天记录完整，不等于项目状态清楚。新 Agent 即使看见全部历史，也可能仍然无法
准确回答：

- 现在什么是真的？
- 哪些决定仍然有效？
- 哪些结果已经实际验证？
- 证据在哪里？
- 下一步具体做什么？

Project Continuity Memory 把这些问题变成一份小型、可版本控制、可核验的项目契约。

## 我们真正的优势

- **保存状态，而不是保存回忆**：只记录已经核验的项目现状，不把所有对话都塞进来。
- **两种速度、两层记忆**：稳定认知与即时接力分开演进，避免单一文件越写越胖，
  或为了精简而丢掉长期决定。
- **证据高于记忆**：用户最新指令、实际文件、测试和外部现状始终高于陈旧记录。
- **低上下文恢复**：先读两份短文件，再只展开本轮真正需要的少量事实源。
- **接力可以直接执行**：阻塞、验收证据和精确下一步不是附注，而是协议必填项。
- **天然可审计**：纯 Markdown 与项目同仓维护，普通版本历史就能审查变化。
- **隐私来自架构**：不需要云服务、账号、遥测、数据库、向量检索或联网。
- **足够轻、没有框架锁定**：一个开放 Agent Skill，加一个无第三方依赖的 Python
  工具即可使用。

## 和其他方案相比

这些方案不是互相替代，而是解决不同问题。Project Continuity Memory 刻意保持
克制：它只负责一件事——**可信的项目接力**。

| 方案 | 主要解决什么 | 擅长什么 | Project Continuity Memory 补上的一层 |
|---|---|---|---|
| 对话与用户记忆，例如 [Mem0](https://github.com/mem0ai/mem0)、[Letta](https://github.com/letta-ai/letta) | 记住用户、对话与 Agent 经历 | 个性化和长期 Agent 行为 | 当前项目事实、证据、仍然有效的决定和下一步 |
| 运行时检查点，例如 [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | 恢复工作流运行状态 | 容错、重放和线程级检查点 | 人类可读、跨框架、覆盖整个仓库的项目连续性 |
| 语义知识系统，例如 [Basic Memory](https://github.com/basicmachines-co/basic-memory) | 保存并检索大量知识 | 语义搜索、发现和知识连接 | 固定恢复协议，避免 Agent 被陈旧或无关检索结果带偏 |
| 任务管理器，例如 [GitHub Projects](https://docs.github.com/issues/planning-and-tracking-with-projects) | 跟踪计划、Issue 和负责人 | 优先级、看板、分工和进度 | 为什么相信当前状态、验证过什么、怎样安全接着做 |
| 临时写一份 handoff | 给下一位留一段说明 | 上手简单 | 稳定认知与即时状态分层，并增加冲突规则和严格校验 |

最短的理解方式是：

> 聊天记录讲述发生过什么，任务系统记录计划做什么，记忆系统检索过去的信息；
> Project Continuity Memory 告诉下一个 Agent：现在什么是真的、为什么，以及下一步
> 具体做什么。

## 什么时候值得用

适合：

- 项目会跨任务、窗口、模型、Agent 或人员持续推进；
- 仓库的生命周期比任何一次对话都长；
- 从错误或陈旧状态恢复的代价很高；
- 人类需要随时检查、修正和追踪接力状态；
- 为这件事部署数据库或云端记忆服务显得太重。

不适合一次性问答、随手实验、纯对话记忆，或已经拥有同等“可验证状态接力协议”
的项目。

## 核心特征

- **仓库原生**：纯 Markdown，与项目一起维护。
- **本地优先**：无需账号、服务、数据库、向量检索或网络。
- **事实优先**：当前可验证状态始终高于记忆文件。
- **低上下文成本**：先读两份短文件，再按需展开少量事实源。
- **可审计**：决定、进度和下一步都能回到项目证据。
- **跨 Agent**：使用开放的
  [Agent Skills 规范](https://github.com/agentskills/agentskills)打包。

## 不属于它的范围

- 个人长期记忆
- 完整聊天归档
- 向量数据库或 RAG
- 代码、ADR、计划、测试或任务系统的替代品
- “Agent 永远不会忘记”的承诺

它是这些系统之间的连续性层。

## 隐私红线

公开仓库只从通用化后的 Skill 抽取，不从任何用户的真实项目记忆复制内容。

以下内容不得进入公开仓库：

- 全局或项目级 `AGENTS.md`
- 真实 `PROJECT_MEMORY.md`、`HANDOFF.md`
- 小说 handoff、备份、聊天记录或私人项目材料
- 用户目录路径、私人邮箱或其他可识别信息
- 指向仓库外部的软链接

所有模板和测试数据必须完全虚构。每次提交和 PR 都会运行
`scripts/check_public_release.py` 执行隐私门禁。

## 安装与使用

使用 Agent Skills 安装器：

```bash
npx skills add YSjandj-design/project-continuity-memory
```

也可以从本地克隆目录安装：

```bash
# Codex
cp -R project-continuity-memory ~/.codex/skills/

# Claude Code
cp -R project-continuity-memory ~/.claude/skills/
```

安装后的 Skill 通常从下一条新任务或新会话开始被发现，不应假设当前运行中的
会话会热加载。

初始化项目：

```bash
python3 project-continuity-memory/scripts/pcm.py init \
  --root /path/to/project \
  --project-name "My Project"
```

填写已核验事实后执行严格校验：

```bash
python3 project-continuity-memory/scripts/pcm.py check \
  --root /path/to/project \
  --strict
```

## 恢复链路

1. 完整读取 `PROJECT_MEMORY.md` 和 `HANDOFF.md`。
2. 只打开与当前目标直接相关的 1–5 个事实源。
3. 以用户最新指令和可验证现状优先处理冲突。
4. 执行工作。
5. 只把稳定、已核验的知识晋升到 `PROJECT_MEMORY.md`。
6. 用真实接力点重写 `HANDOFF.md`，不把它无限追加成聊天日记。
7. 运行严格校验。

版本 0.1.0 已完成本地发布候选验收。详细变化见
[CHANGELOG.md](CHANGELOG.md)，参与方式见
[CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

Apache License 2.0，见 [LICENSE](LICENSE)。
