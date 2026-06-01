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
