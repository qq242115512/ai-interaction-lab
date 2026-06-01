# Session Handoff — 2026-06-01

## What Was Done
- 15 角色 SKILL.md 全部补强到 ≥110 行，中文触发词覆盖 15/15
- Orchestrator 加了下游反馈协议、项目规模评估矩阵、上游上下文+历史教训注入
- Adversarial Reviewer 加了元审查模式（审 Orchestrator）+ 预验尸模式
- Backend 角色重写（286 行）：API 版本化、幂等性、连接池、熔断器、AI 管道
- 新建 2 个 LESSONS.md：security（注入漏检）、devops（Docker Hub 被墙、Hindsight 架构）
- Hindsight 架构升级：嵌入式 PG → 外部 PG + WAL 崩溃恢复
- AI 交互实验室 v0.4.0 安全加固：CORS 白名单、Rate Limiting、中英文注入过滤、CSP 安全头
- 博西家电实习岗位搜索：AI Agent 战略实习生（200-300/天，南京）最对口
- 实习僧简历内容已准备好
- 用户偏好更新：边做边学型、立刻行动型、给选项带代价、老师角色

## Key Decisions
| # | Decision | Context | By |
|---|----------|---------|-----|
| 1 | 教训飞轮按角色独立文件 | 每角色 LESSONS.md，Orchestrator 自动写入 | PO |
| 2 | Jester 不单独建角色，预验尸并入 Adversarial Reviewer | 避免角色膨胀 | PO |
| 3 | 上游依赖声明加在所有 14 个子 Agent 中 | Orchestrator 对照清单而非凭记忆 | PO |

## Current Status
- **完成**: 全部工具链稳定，网站 v0.4.0 运行中
- **待做**: 页面重设计（Designer Skill 跑一遍）
- **待学**: Git、开源 Agent 框架、Prompt 评估、测试策略、Token 成本

## Next Steps
1. **[新窗口]** 用 Designer Skill 重设计 AI 交互实验室首页（提升设计感）
2. **[本窗口]** 学 Git 基础 + 推项目到 GitHub
3. **[本窗口]** 看 AutoGen/CrewAI/LangGraph README → 写对比笔记
4. 投博西 AI Agent 战略实习生

## Lesson Updates
- `agents/security/LESSONS.md`: 中文注入漏检 + Rate Limiting 缺失 (new)
- `agents/devops/LESSONS.md`: Docker Hub 被墙 + 嵌入式 PG 崩溃 (new)
