# Changelog

## v0.5.0 — 多 Agent 协作仪表盘 (2026-06-02)

### 新增

- **第 8 张模式卡片"多 Agent 协作"**：首页新增卡片链接到 agents.html
- **agents.html 仪表盘页面**（1797 行）：
  - 流水线可视化：5 阶段交互式流程图，点击展开 15 角色子节点 + 详情面板
  - Agent 状态网格：15 张角色卡片，带 SKILL.md 进度条和 LESSONS.md 教训计数
  - 教训飞轮：CSS 3D 卡片翻转动画，展示"Bug → 修复规则"的转换
  - 框架对比表：AutoGen vs CrewAI vs LangGraph vs 本体系
  - 知识图谱占位：Hindsight 数据就绪后自动激活
  - Indigo (#4F5CD6) 主题色 + 5 阶段色板
- **agent-system API 路由组**（4 个新端点）：
  - `GET /api/agent-system/status` — 15 角色状态（从 SKILL.md/LESSONS.md 读取）
  - `GET /api/agent-system/pipeline` — 完整流水线 DAG 定义
  - `GET /api/agent-system/lessons` — 结构化教训数据（跨 5 个角色 14 条教训）
  - `GET /api/agent-system/knowledge` — Hindsight 知识图谱快照

### 设计

- Designer Agent 产出 1335 行完整设计包（设计 Token、交互状态表、ASCII 线框图、CSS 动画策略）
- 选择 Indigo 作为第 8 张卡片主题色，与暖珊瑚主色形成互补（蓝-橙色轮距离约 150 度）

### 修复

- 首页 "7 种" 更新为 "8 种"
- 删除 index.html 中残留的测试注释
- 修复 stat-strip 中 querySelector 竞态条件 bug

### 已知问题

- Linux 服务器无法读取 Windows 上的 SKILL.md/LESSONS.md 文件，agent-system 端点返回 fallback 元数据
- SecurityMiddleware 定义但未接入 main.py（v0.4.0 遗留），限流/CSP/注入过滤未实际生效

---

## v0.4.0 — 安全加固 + 页面重设计 (2026-06-01)

### 新增
- 安全中间件：Rate Limiting (20/min/IP)、中英文注入过滤 (12+ 变体)、CSP 安全头
- 15 角色 SKILL.md 全部升级（≥110 行，中文触发词全覆盖）

### 修复
- 12 个 bug 修复（CSS+GSAP 动画冲突、Nginx SSE 缓冲、函数声明残留等）
- 页面重设计：暖珊瑚配色 + GSAP 动画 + Noto Serif SC 字体

---

## v0.3.0 — 初始版本

- 7 种 AI 交互模式页面
- 4 个后端路由组：review、chat、stream、patterns
- 双模型管道：GLM-4V 视觉 + DeepSeek 推理
- 阿里云部署：Nginx + systemd + HTTPS
