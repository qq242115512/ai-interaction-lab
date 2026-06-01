# AI 交互模式实验室

## 项目目标

把"设计引路人"（AI 设计评审工具）改造为 **AI 交互模式实验室**，部署在 [fanshuyang.top](https://fanshuyang.top)。让面试官打开网址看到 7 种可交互的 AI 交互模式展示，每种模式有说明文字解释设计思路和实现方式。

核心叙事：不会写代码的设计学生，用 AI 工具链从零做出了解 AI 交互设计的作品集项目。

## 技术栈

- **前端**：纯 HTML/CSS/JS（无框架），对 AI 协作最友好
- **后端**：FastAPI + Pydantic + httpx
- **AI 管道**：GLM-4V（视觉识别）→ DeepSeek（推理+流式输出）
- **部署**：阿里云 Ubuntu + Nginx + systemd + HTTPS
- **代码位置**：`src/backend/`（Python）、`src/frontend/`（静态文件）、`src/deploy/`（部署配置）

## 15 角色工作流

所有角色定义在 `C:\Users\qq242\.claude\skill\agents\` 下，每个角色有独立的 SKILL.md。

### 流水线顺序

```
PO (用户) 
  → Orchestrator (协调+分发)
    → Scout (摸底：技术栈/结构/命令/缺口)
    → BA (需求：用户故事+验收标准)
    → Orchestrator (技术分解+接口契约+范围裁剪)
    → Adversarial Reviewer (对抗审查：在开工前找盲点)
    → PM (任务路由+进度追踪)
    → Designer (视觉+交互设计)
    → Frontend / Backend / Fullstack (实现)
    → Code Reviewer (代码审查)
    → QA (测试+行为验证)
    → Security Guardian (安全审计)
    → DevOps (部署)
    → Technical Writer (文档+Changelog)
    → Memory Curator (记忆归档)
```

### 15 个角色清单

| # | 角色 | 模型 | 职责 |
|---|------|------|------|
| 1 | Orchestrator | Opus | 协调分发、质量把关、接口契约 |
| 2 | Scout | Sonnet | 摸底调研、技术栈文档 |
| 3 | BA | Sonnet | 需求澄清、用户故事、验收标准 |
| 4 | PM | Sonnet | 任务路由、进度追踪、合并门 |
| 5 | UX/UI Designer | Opus | 视觉设计、交互状态、设计规范 |
| 6 | Frontend | Sonnet | HTML/CSS/JS 实现 |
| 7 | Backend | Sonnet | API/数据库/业务逻辑 |
| 8 | Fullstack | Sonnet | 端到端垂直切片（小项目优先用这个） |
| 9 | Code Reviewer | Sonnet | 代码质量把关 |
| 10 | QA | Sonnet | 测试、Bug 报告、行为验证 |
| 11 | Adversarial Reviewer | Opus | 盲点发现、失败模式分析 |
| 12 | Security Guardian | Sonnet | 安全漏洞审计 |
| 13 | DevOps | Sonnet | 部署、CI/CD、环境管理 |
| 14 | Technical Writer | Sonnet | 文档、ADR、Changelog |
| 15 | Memory Curator | Sonnet | 跨会话记忆、Session State |

### 关键规则

- Orchestrator 不写代码，只协调
- 每个任务必须有接口契约（输入/输出/格式/消费者）
- 两个角色不能同时改同一个文件
- 所有完成声明必须验证，不接受"应该没问题"
- 项目小（< 5 页面、< 10 端点）优先用 Fullstack 而非拆 Frontend + Backend

## 7 个 AI 交互模式

改造目标：每个模式做成独立可交互的展示页面，包含模式说明 + 交互 Demo。

| # | 模式 | 说明 | 现有代码来源 |
|---|------|------|-------------|
| 1 | **流式输出** | AI 逐字生成内容，不是一次性全给。让用户感知 AI 在工作，减少等待焦虑 | [stream.py](src/backend/routers/stream.py) SSE 端点 |
| 2 | **结构化卡片** | AI 输出用卡片/模块展示，不是一坨纯文本。信息可扫读、可分层 | [review.js](src/frontend/js/review.js) 维度卡片渲染 |
| 3 | **澄清提问** | AI 不确定时反问用户，不瞎猜。减少幻觉、提升输出质量 | [prompts.py](src/backend/services/prompts.py) 改 Prompt |
| 4 | **失败兜底** | API 挂了/超时/返回乱码时优雅降级。用户看不到崩溃 | [utils.py](src/backend/services/utils.py) 重试+JSON 三层回退 |
| 5 | **多轮上下文** | AI 记得前面聊了什么，持续追问。上下文窗口管理 | [chat.py](src/backend/routers/chat.py) 会话历史管理 |
| 6 | **确认机制** | 关键操作前让用户确认。人类在回路中，防止误操作 | ❌ 需新建 |
| 7 | **渐进式加载** | 按认知顺序分步展开信息，不是一次性全给。先结果→再细节→再追问 | [stream.py](src/backend/routers/stream.py) SSE 分阶段推送 |

### 每个模式页面结构

```
[模式名称]
[一句话说明这个模式解决什么问题]
[设计思路：为什么这样设计，引用的设计原则]
[实现方式：技术栈简述]
[可交互 Demo]
[代码来源链接]
```

## 当前项目状态

- **AI 交互模式实验室 v1.1.0** 运行在 [fanshuyang.top](https://fanshuyang.top)
- 首页：7 张模式卡片导航 + 完整产品入口
- /review.html：保留原设计评审工具（上传→选维度→评审→追问）
- /principles.html：设计原则图书馆
- /behind-the-scenes.html：制作幕后
- /about.html：个人介绍页
- /patterns/*.html：7 个交互模式详情页（说明 + Demo）
- 后端 4 个路由组：review、chat、stream、patterns（新增）
- 新增端点：POST /api/clarify、POST /api/confirm、POST /api/execute

## 完成状态

15 角色工作流已完整跑通一次（2026-05-23）：
1. Orchestrator ✅ → 2. Scout ✅ → 3. BA ✅ → 4. Adversarial ✅ → 5. PM ✅ → 6. Designer ✅ → 7. Fullstack ✅ → 8. Code Reviewer ✅ → 9. QA ✅ → 10. Security ✅ → 11. DevOps ✅ → 12. Tech Writer ✅ → 13. Memory Curator ✅

## 设计决策记录

- 前端不用框架（React/Vue），纯 HTML/CSS/JS 对 Claude Code 协作最友好
- 双模型管道（GLM-4V 看 + DeepSeek 评），各司其职
- Prompt 风格：引导式而非说教式，目标用户是设计学生
- 所有 AI 输出要求纯 JSON，三层解析回退保证鲁棒性
- 服务器一年到期后可用 GitHub Pages/Vercel 免费替代
