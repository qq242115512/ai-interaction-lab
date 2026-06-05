# Session Handoff — 2026-06-05

## What Was Done
- **CI/CD 自托管 Runner 部署成功**：git push → 90 秒 → 自动上线（v0.5.1）
- 六层网络代理全部配置（Windows 终端 + Git + Docker + WSL2）
- GitHub Actions Runner 注册到仓库 ai-interaction-lab，命名 fan-laptop
- deploy.yml 走 WSL2 Ubuntu 的 rsync/ssh 部署到阿里云，全链路国内通
- 代码规范检查移到本地 check.bat（Ruff + 安全扫描 + pytest），push 前跑
- Tailwind CSS 决策更新：旧页面不改，新页面用 Tailwind
- 11 条社区实践知识写入 CLAUDE.md
- Playwright 指向 Edge（不再需要装 Chrome）
- 服务器 run.cmd 在 C:\Users\qq242\runner\ 后台运行

## Key Decisions
| # | Decision | Context | By |
|---|----------|---------|-----|
| 1 | 自托管 Runner（笔记本）替代 GitHub Cloud Runner | 美国连中国 22 端口被墙 | PO |
| 2 | CI 检查放本地 check.bat 而非 GitHub Actions | Windows 上 WSL 命令调试成本太高 | PO |
| 3 | Tailwind CSS 新页面优先，旧页面不动 | AI 在 Tailwind 上训练数据远超裸 CSS | PO |
| 4 | Docker 代理指向 WSL2 宿主机 IP | 172.22.112.1:10808，重启后 IP 可能变 | PO |

## Current Status
- **网站**：v0.5.1 运行中
- **Runner**：C:\Users\qq242\runner\run.cmd 后台运行中
- **提醒**：WSL2 重启后 Docker 代理 IP 可能需要更新
- **GitHub**：已推送 47+ 文件，10000+ 行代码

## Next Steps
1. Prompt 评估体系（最该补的社区实践）
2. 给 agents.html 用 Tailwind 重写一版看看效果
3. Runner 如果掉线：开 cmd → cd C:\Users\qq242\runner → run.cmd
4. 投博西 AI Agent 战略实习生
