# AI 交互模式实验室

## 项目目标

展示 7 种 AI 交互模式的作品集网站 + 一套 15 角色 AI Agent 协作体系的完整文档和源码。面试官打开网址看到可交互 Demo，打开 GitHub 看到 Agent 架构设计。

核心叙事：不会写代码的设计学生，用 AI 工具链从零做出了解 AI 交互设计的产品 + 设计了让 AI 团队不出错的协作体系。

## 技术栈

- **前端**：纯 HTML/CSS/JS + GSAP 动画库
- **后端**：FastAPI + Pydantic + httpx
- **AI 管道**：GLM-4V（视觉识别）→ DeepSeek（推理+流式输出）
- **部署**：阿里云 Ubuntu + Nginx + systemd + HTTPS
- **代码**：`src/backend/`（Python）、`src/frontend/`（静态文件）、`src/deploy/`（部署配置）
- **仓库**：https://github.com/qq242115512/ai-interaction-lab

## 15 角色工作流

所有角色定义在 `C:\Users\qq242\.claude\skills\agents\` 下。每个角色有 SKILL.md（方法论）和 LESSONS.md（历史教训）。

### 流水线顺序

```
PO (用户)
  → Orchestrator (协调+分发)
    → Scout (摸底：技术栈/结构/命令/缺口)
    → BA (需求：用户故事+验收标准)
    → Orchestrator (技术分解+接口契约+范围裁剪)
    → Adversarial Reviewer (对抗审查：常规审查 + 元审查 + 预验尸)
    → PM (任务路由+进度追踪+阶段门检查)
    → Designer (视觉+交互设计)
    → Frontend / Backend / Fullstack (实现)
    → Code Reviewer (5层分层审查)
    → QA (测试+AI专项测试)
    → Security Guardian (安全审计)
    → DevOps (部署+回滚)
    → Technical Writer (文档+Changelog)
    → Memory Curator (记忆归档+教训飞轮)
```

### 15 个角色清单

| # | 角色 | 模型 | 职责 |
|---|------|------|------|
| 1 | Orchestrator | Opus | 协调分发、质量把关、接口契约 |
| 2 | Scout | Sonnet | 摸底调研、技术栈文档 |
| 3 | BA | Sonnet | 需求澄清、用户故事、验收标准 |
| 4 | PM | Sonnet | 任务路由、风险登记册、阶段门检查 |
| 5 | UX/UI Designer | Opus | 视觉设计、交互状态、设计Token、WCAG |
| 6 | Frontend | Sonnet | HTML/CSS/JS/GSAP 实现 |
| 7 | Backend | Sonnet | API/数据库/业务逻辑 |
| 8 | Fullstack | Sonnet | 端到端垂直切片（<5页面优先） |
| 9 | Code Reviewer | Sonnet | 5层分层代码审查 |
| 10 | QA | Sonnet | AI专项测试+传统测试 |
| 11 | Adversarial Reviewer | Opus | 常规审查+元审查(审Orchestrator)+预验尸 |
| 12 | Security Guardian | Sonnet | 安全漏洞审计 |
| 13 | DevOps | Sonnet | 部署、CI/CD、Git版本管理 |
| 14 | Technical Writer | Sonnet | 文档、ADR、Changelog |
| 15 | Memory Curator | Sonnet | 跨会话记忆、Session State、教训管理 |

### 系统机制（已实现）

**项目规模评估矩阵**：S/M/L/XL 四级，决定哪些阶段跳过、哪些必做

**下游反馈协议**：子Agent收到不合格上游产出时，用3点式拒绝（缺什么→为什么阻塞→要什么），静默修补是质量衰减的源头

**Agent Handoff Diff Check**：同一角色被多次调用时，Orchestrator 在后续任务卡片中标注"已有样式/属性锁定"，防止两个实例互相踩

**教训飞轮**：项目结束→Orchestrator提取角色卡片未覆盖的发现→写入对应角色 LESSONS.md→下次启动该角色时自动注入 prompt。5 个角色已有教训档案

**文件锁**：两 Agent 不能同时改同一文件的同一区域。不同区域可并行

### 关键规则

- Orchestrator 不写代码，只协调
- 每个任务必须有接口契约
- 任何修改必须闭环验证（改了配置→确认生效）
- 安装 Skill/MCP 后必须验证真的能用
- 所有完成声明必须验证，不接受"应该没问题"

## 7 个 AI 交互模式

| # | 模式 | 解决什么问题 | 实现 |
|---|------|------------|------|
| 1 | **流式输出** | AI 逐字生成，让用户感知"在工作"，减少等待焦虑 | SSE 逐 token 推送 |
| 2 | **结构化卡片** | 信息用卡片展示，可扫读可分层 | JSON→卡片渲染 |
| 3 | **澄清提问** | AI 不确定时反问用户，不瞎猜 | 两阶段 Prompt |
| 4 | **失败兜底** | API 出错时优雅降级，用户看不到崩溃 | 重试+JSON回退 |
| 5 | **多轮上下文** | AI 记得之前聊了什么 | 会话管理+裁剪 |
| 6 | **确认机制** | 关键操作前确认，人在回路 | 两阶段确认流 |
| 7 | **渐进式加载** | 按认知顺序分步展开，降低信息过载 | SSE 分阶段推送 |

每个模式页面结构：模式名称 → 一句话说明 → 设计思路（引用的设计原则）→ 实现方式 → 可交互 Demo → 源码链接

## 当前项目状态

- **v0.5.0** 运行在 [fanshuyang.top](https://fanshuyang.top)
- 首页：8 张模式卡片（珊瑚色主题 + GSAP 动画）
- 15 个 HTML 页面（about / behind-the-scenes / review / principles / 7 patterns / agents / test）
- 后端 5 个路由组：review、chat、stream、patterns、agent-system
- 安全加固：CORS 白名单、Rate Limiting (20/min/IP)、中英文注入过滤 (12+ 变体)、CSP 安全头
- 页面已重设计（暖珊瑚配色 + GSAP 动画 + Noto Serif SC 字体），修复了 12 个 bug
- GitHub 已推送：47+ 个文件、10000+ 行代码

## 已完成

- **第 8 张卡片"多 Agent 协作仪表盘"**：agents.html + 4 个新 API 端点 + Indigo 主题设计（v0.5.0, 2026-06-02）
- 15 角色卡片全部升级（SKILL.md ≥110 行，中文触发词全覆盖）
- 5 个角色有 LESSONS.md：DevOps / Frontend / Backend / Security / Orchestrator
- 真实项目 M 级工作流跑通（安全加固，2026-06-01）
- 第二次 M 级工作流（第 8 张卡片，2026-06-02）—— 14 角色流程完整跑通
- Hindsight 架构升级（嵌入式 PG → 外部 PG + WAL 崩溃恢复）
- GitHub 仓库已推送

## 待做

- **投递实习**：博西 AI Agent 战略实习生（200-300/天，南京）
- **修复遗留问题**：SecurityMiddleware 定义但未接入 main.py，限流/CSP/注入过滤未实际生效
- 学习：开源 Agent 框架对比（AutoGen/CrewAI/LangGraph）、Git branch/merge
- agent-system 端点数据源从本地文件改为 Hindsight 知识图谱（当前 Linux 服务器读不到 Windows 文件）

## 设计决策

- 前端不用框架（React/Vue），纯 HTML/CSS/JS 对 AI 协作最友好
- 双模型管道（GLM-4V 看 + DeepSeek 评），各司其职
- Prompt 风格：引导式而非说教式
- 所有 AI 输出要求纯 JSON，三层解析回退
- 国内 Docker Hub 被墙，拉镜像用 ghcr.io
- 技能目录是 `skills`（复数），不是 `skill`（单数）
- CSS 动画和 GSAP 不能混用同一组元素
- 改完配置必须立即验证（nginx -t / 刷新页面 / Skill() 调用）

## 社区 2026 成熟实践（面试必知 + 工程决策参考）

> 以下每条都是社区已验证的成熟做法。知道它们的存在 + 能讲清"为什么我们没现在做" = 面试时从"学生会写 Demo"升到"能思考工程权衡的人"。

### 1. Agent 数量：社区最优是 3-5 个，不是 15 个

AutoGen、CrewAI、LangGraph 的真实生产案例通常控制在 5 个以内。15 个角色是你的**思想实验和教学展示**——证明你能系统化分层。但面试官如果问"为什么不用 5 个"，你要能答：

> "15 角色是完整映射真实软件团队——每个岗位都有独立的质量标准和交接契约。但实际执行时按规模裁剪：S 级只跑 3 个（Scout+Fullstack+QA），M 级跑 7 个。大厂框架的 5 个是通用对话式协作，我的核心差异不在数量——在于每个 Agent 不是一段 prompt，而是一套带 I/O 契约、质量标准、历史教训的完整工程角色。"

### 2. Prompt 评估：社区用测试集 + 多维评分，不是人眼看

改 Prompt 之前和之后各跑同一批 50-100 个测试用例，每例按 3-5 个维度打分（准确性、格式合规、幻觉、安全性），改后分数降了就回退。你的 7 个 Prompt 目前靠手动判断。

**你可以做的最简单升级**：准备 10 个典型输入给每个模式的 Demo，写一个 Python 脚本跑它们 → 记录 AI 输出 → 人工打分 → 下次改 Prompt 后重新跑对比。面试时你说"我有 Prompt 评估体系"比"我觉得 Prompt 还行"强一个数量级。

框架：LangSmith（LangChain）、Braintrust、自定义脚本。

### 3. CI/CD：社区从 git push 到部署全自动

真正的 DevOps 管线：`git push → GitHub Actions 自动跑测试 → 自动构建 Docker 镜像 → 自动推送到镜像仓库 → 自动部署到服务器 → 健康检查失败自动回滚`。我们还在手动 `scp` 文件。对现在 1 人项目的 ROI 不高，但概念要知道。

GitHub Actions 对开源项目免费。你只要写一个 `.github/workflows/deploy.yml` 就能自动部署。这是我们之后可以快速加的东西——10 分钟配置，永不再手动 scp。

### 4. 容器化：不只是"用 Docker"

社区标准是 `docker-compose.yml` 定义全栈（前端 + 后端 + 数据库），一条命令 `docker compose up` 拉起全套。开发环境和生产环境一致。你的项目目前是后端 systemd + 前端 Nginx serve 静态文件——可行但面试时加分项是"我会配置 Docker Compose 全链路"。

建议但不现在做：你只有一年服务器，Docker Compose 在本地 WSL2 跑更有意义。

### 5. 可观测性：不止是日志

社区三层体系：
- **日志**（Logs）——你已有，结构化但不完善
- **指标**（Metrics）——请求数、错误率、延迟、API 调用量、token 消耗。用 Prometheus + Grafana
- **追踪**（Tracing）——一个请求从 Nginx → FastAPI → DeepSeek → 返回，每一步花了多少 ms

对我们实用的是**指标**——给你的 API 加一个 Prometheus 端点，在 Grafana 上挂一个仪表盘。面试时打开链接给面试官看"这是我的 AI API 用量监控面板"，比说"应该不会有问题吧"强太多。

### 6. AI Safety 体系：不止是注入过滤

社区 2026 年在做的远不止 Prompt 注入检测：
- **输出安全分类器**：AI 返回的内容过一遍自动审核（有没有生成暴力内容、泄露的信息、虚假声明）
- **红队测试**：专门有人/Agent 负责"攻击"自己的产品，找绕过
- **RLHF/DPO**：通过人类反馈微调模型让它更安全——你用不到但概念要知道
- **OWASP for LLM**：OWASP Top 10 针对 LLM 应用有专门的一版——面试时提这个很加分

### 7. Agent 评估框架：社区在定义"怎么度量 Agent 好不好"

2026 年是 Agent 评估元年。社区在争论的事：
- 一个 Agent 好不好，该用什么指标？任务完成率？重试次数？token 消耗？用户满意度？
- 你的 15 角色体系**暗含了一种评估标准**：每个角色都有输出契约和验证步骤，契约达标率就是天然的质量指标。这件事目前还没有社区标准，你可以提出一个雏形——面试时这是原创贡献

### 8. RAG 进阶：不止是"查资料让 AI 回答"

成熟的 RAG 系统有更多层：
- **Query 改写**：用户问"那上次那个呢"→ 系统先把这个模糊问题改写成"上次项目中 CORS 配置的具体值是什么"
- **重排序**（Re-ranking）：检索返回 20 条，但只取最相关的 3 条塞进 prompt——用 Cross-Encoder 模型过滤
- **引用溯源**：AI 回答的每一句话旁边标上"来源：[文件名] 第 3 段"
- 你的项目中 Hindsight + Memory Curator = 基础 RAG，"经验注入到子 Agent prompt" = 高级 RAG。你能讲清你做到了哪一层

### 9. 前端工程化：社区不用 HTML 裸写

你的项目是纯 HTML，社区主流是：
- **Tailwind CSS**：不需要写 CSS 文件，class 名即样式。AI 生成 Tailwind 非常熟练——比你手写 CSS 快 3-5 倍
- **React/Vue/Svelte**：组件化开发。你项目规模 15 个页面，还没到非用不可——但面试官会问
- **TypeScript**：JS 的类型安全版。你不需要现在学，但概念是"写完代码还没跑，编辑器就先告诉你这里有 bug"

你可以说的：当前纯 HTML/CSS/JS 是为了 AI 协作最友好（无构建层）。后续考虑 Tailwind + 组件化——但保持无框架。

### 10. 数据库：你的项目没有数据库

15 个 HTML 页面的项目不需要数据库。但面试时如果被问"如果用户量大了你怎么存数据"，要能说：
- SQLite（单文件数据库，部署零成本）→ 适合小型项目
- PostgreSQL（你 Hindsight 已经用了）→ 生产标准
- 你的"session 内存字典 + TTL"方案 = 缓存层方案，不是持久化方案。长期应该切 SQLite

### 11. 大厂 2026 真正在做的 AI 产品方向

面试官可能接触的方向（你知道这些不会被问倒）：
- **AI Copilot**（微软/Google 全线产品）：聊天式助手嵌入工具
- **AI Agent**（AutoGPT/CrewAI 等的商业化）：自主执行多步任务
- **RAG + 企业知识库**（最热的企业落地场景）：把公司文档变成可问答
- **多模态 Agent**（图+文+语音混合理解）：你用的 GLM-4V → DeepSeek 其实就是双模态
- **AI-native UI**：不再把 AI 嵌进传统界面，而是从零为 AI 交互设计新 UI 范式——这就是你的项目核心叙事

## 社区实践对照表（我们的项目 vs 社区标准）

| 领域 | 社区 2026 标准 | 我们现在 | 差距 | 优先级 |
|------|---------------|---------|------|--------|
| Agent 数量 | 3-5 个生产 | 15 角色 × 按规模裁剪 | ✅ 有裁减机制 | 无 |
| Prompt 评估 | 测试集+自动评分 | 手动判断 | ⚠️ 可快速补 | 中 |
| CI/CD | git push→自动部署 | 手动 scp | ⚠️ GitHub Actions 10min | 高 |
| 容器化 | Docker Compose 全栈 | systemd + 裸进程 | ⚠️ 本地可用 | 低 |
| 可观测性 | 指标仪表盘 | 结构化日志 | ⚠️ 加 Prometheus | 低 |
| AI Safety | OWASP for LLM | 注入过滤+Rate Limit | ✅ 基础够用 | 低 |
| 数据库 | PostgreSQL/SQLite | 内存字典 | ⚠️ 需要时切 SQLite | 低 |
| 前端工程化 | React/Tailwind/TS | 纯 HTML/CSS/JS | ✅ 有意为之 | 无 |
| 静态分析 | ESLint/Prettier/Ruff | 无 | ⚠️ 加 Ruff 5min | 中 |
| Git 工作流 | Feature Branch + PR | 单人 main 分支 | ✅ 团队协作才需要 | 无 |

**优先级"高"和"中"的意思是**：面试时被问到能说出差距和理由 = 加分。被问到不知道 = 扣分。以上每一条你都应该能讲三句话：社区标准是什么、我们现在做了什么、为什么没做更多。
