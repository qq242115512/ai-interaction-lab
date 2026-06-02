"""
Generate agents.json from local skill files.
Reads all SKILL.md and LESSONS.md from ~/.claude/skills/agents/
Run: python scripts/generate_agents_data.py
Output: src/backend/data/agents.json
"""
import json
import re
from pathlib import Path

AGENTS_DIR = Path.home() / ".claude" / "skills" / "agents"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_FILE = OUTPUT_DIR / "agents.json"

# Agent metadata not stored in SKILL.md
AGENT_META = {
    "orchestrator": {"id": "orchestrator", "name_zh": "协调器", "stage": "coordination",
                      "icon": "🎯", "order": 1},
    "scout": {"id": "scout", "name_zh": "侦察兵", "stage": "scout",
              "icon": "🔍", "order": 2},
    "ba": {"id": "ba", "name_zh": "业务分析师", "stage": "requirements",
           "icon": "📋", "order": 3},
    "adversarial-reviewer": {"id": "adversarial-reviewer", "name_zh": "对抗审查员",
                              "stage": "requirements", "icon": "⚔️", "order": 4},
    "pm": {"id": "pm", "name_zh": "项目经理", "stage": "requirements",
           "icon": "📊", "order": 5},
    "designer": {"id": "designer", "name_zh": "设计师", "stage": "design",
                 "icon": "🎨", "order": 6},
    "frontend": {"id": "frontend", "name_zh": "前端开发", "stage": "implementation",
                 "icon": "💻", "order": 7},
    "backend": {"id": "backend", "name_zh": "后端开发", "stage": "implementation",
                "icon": "⚙️", "order": 8},
    "fullstack": {"id": "fullstack", "name_zh": "全栈开发", "stage": "implementation",
                  "icon": "🔧", "order": 9},
    "code-reviewer": {"id": "code-reviewer", "name_zh": "代码审查员", "stage": "implementation",
                       "icon": "👀", "order": 10},
    "qa": {"id": "qa", "name_zh": "测试工程师", "stage": "implementation",
           "icon": "🧪", "order": 11},
    "security": {"id": "security", "name_zh": "安全审计员", "stage": "implementation",
                 "icon": "🔒", "order": 12},
    "devops": {"id": "devops", "name_zh": "运维工程师", "stage": "delivery",
               "icon": "🚀", "order": 13},
    "tech-writer": {"id": "tech-writer", "name_zh": "技术文档撰写", "stage": "delivery",
                    "icon": "📝", "order": 14},
    "memory-curator": {"id": "memory-curator", "name_zh": "记忆策展人", "stage": "delivery",
                        "icon": "🗄️", "order": 15},
}

PIPELINE_STAGES = [
    {"id": "scout", "name": "调研摸底",
     "description": "确认技术栈、文件结构、命令可用性，发现缺口",
     "order": 1, "roles": ["scout"]},
    {"id": "requirements", "name": "需求分析",
     "description": "用户故事、验收标准、对抗审查、风险登记",
     "order": 2, "roles": ["ba", "adversarial-reviewer", "pm"]},
    {"id": "design", "name": "设计",
     "description": "视觉设计、交互状态、设计Token、WCAG无障碍",
     "order": 3, "roles": ["designer"]},
    {"id": "implementation", "name": "实现与验证",
     "description": "前后端开发、代码审查、测试、安全加固",
     "order": 4, "roles": ["frontend", "backend", "fullstack", "code-reviewer", "qa", "security"]},
    {"id": "delivery", "name": "交付与归档",
     "description": "部署上线、文档编写、记忆归档、教训飞轮",
     "order": 5, "roles": ["devops", "tech-writer", "memory-curator"]},
]

ROLE_RESPONSIBILITIES = {
    "orchestrator": ["协调分发", "质量把关", "接口契约", "技术分解", "范围裁剪"],
    "scout": ["技术栈摸底", "文件结构确认", "命令可用性检查"],
    "ba": ["需求澄清", "用户故事编写", "验收标准定义"],
    "adversarial-reviewer": ["常规审查", "元审查（审Orchestrator）", "预验尸"],
    "pm": ["任务路由", "风险登记册", "阶段门检查", "进度追踪"],
    "designer": ["视觉设计", "交互状态设计", "设计Token", "WCAG无障碍"],
    "frontend": ["HTML/CSS/JS实现", "GSAP动画", "响应式设计"],
    "backend": ["API开发", "数据库设计", "业务逻辑"],
    "fullstack": ["端到端开发", "前后端集成"],
    "code-reviewer": ["5层分层审查", "安全审查", "性能审查"],
    "qa": ["功能测试", "AI专项测试", "自动化测试"],
    "security": ["安全漏洞审计", "注入测试", "依赖审计"],
    "devops": ["部署运维", "CI/CD", "环境管理"],
    "tech-writer": ["README撰写", "API文档", "Changelog"],
    "memory-curator": ["会话归档", "Session Handoff", "教训管理"],
}


def parse_frontmatter(text: str) -> dict:
    """Extract YAML-like frontmatter fields from SKILL.md."""
    fields = {}
    patterns = {
        "name": r"^name:\s*(.+)$",
        "model": r"^model:\s*(.+)$",
        "skills": r"^skills:\s*\[(.*?)\]$",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            value = match.group(1).strip()
            if key == "skills":
                value = [s.strip() for s in value.split(",") if s.strip()]
            fields[key] = value
    return fields


def count_lines(filepath: Path) -> int:
    try:
        return len(filepath.read_text(encoding="utf-8").splitlines())
    except Exception:
        return 0


def parse_lessons(filepath: Path) -> list[dict]:
    """Parse LESSONS.md into structured lesson data."""
    if not filepath.exists():
        return []
    text = filepath.read_text(encoding="utf-8")
    lessons = []
    current_date = None
    current_project = None
    for line in text.splitlines():
        date_match = re.match(r"^##\s+(\d{4}-\d{2}-\d{2})\s*—\s*(.+)$", line)
        if date_match:
            current_date = date_match.group(1)
            current_project = date_match.group(2)
            continue
        lesson_match = re.match(r"^-\s+\*\*(.+?)\*\*\s*(.*)$", line)
        if lesson_match and current_date:
            lessons.append({
                "date": current_date,
                "project": current_project,
                "title": lesson_match.group(1).strip(),
                "detail": lesson_match.group(2).strip()[:200],
            })
    return lessons


def main():
    agents = []
    all_lessons = []
    lesson_by_agent = {}
    lesson_by_category = {}

    for meta_key, meta in AGENT_META.items():
        agent_dir = AGENTS_DIR / meta_key
        skill_file = agent_dir / "SKILL.md"
        lessons_file = agent_dir / "LESSONS.md"

        skill_lines = 0
        skill_info = {}
        has_lessons = False
        lesson_count = 0

        if skill_file.exists():
            text = skill_file.read_text(encoding="utf-8")
            skill_lines = len(text.splitlines())
            skill_info = parse_frontmatter(text)

        agent_lessons = parse_lessons(lessons_file)
        has_lessons = len(agent_lessons) > 0
        lesson_count = len(agent_lessons)
        all_lessons.extend(agent_lessons)
        lesson_by_agent[meta_key] = agent_lessons

        agents.append({
            "id": meta["id"],
            "name": skill_info.get("name", meta_key),
            "name_zh": meta["name_zh"],
            "stage": meta["stage"],
            "icon": meta["icon"],
            "model": skill_info.get("model", "Sonnet"),
            "skill_lines": skill_lines,
            "has_lessons": has_lessons,
            "lessons_count": lesson_count,
            "description": "、".join(ROLE_RESPONSIBILITIES.get(meta_key, [])),
            "responsibilities": ROLE_RESPONSIBILITIES.get(meta_key, []),
            "order": meta["order"],
            "skill_count": len(skill_info.get("skills", [])),
        })

    for agent in agents:
        for lesson in lesson_by_agent.get(agent["id"], []):
            cat = lesson.get("project", "其他")
            lesson_by_category[cat] = lesson_by_category.get(cat, 0) + 1

    # Role dependency graph
    roles_pipeline = []
    for meta_key, meta in sorted(AGENT_META.items(), key=lambda x: x[1]["order"]):
        upstream = []
        downstream = []
        prev_key = None
        for k, v in sorted(AGENT_META.items(), key=lambda x: x[1]["order"]):
            if v["order"] == meta["order"] - 1:
                upstream.append(k)
            if v["order"] == meta["order"] + 1:
                downstream.append(k)
        roles_pipeline.append({
            "id": meta["id"],
            "name": meta_key.replace("-", " ").title(),
            "name_zh": meta["name_zh"],
            "stage": meta["stage"],
            "icon": meta["icon"],
            "model": [a["model"] for a in agents if a["id"] == meta["id"]][0],
            "responsibilities": ROLE_RESPONSIBILITIES.get(meta_key, []),
            "depends_on": upstream,
            "feeds_into": downstream,
        })

    output = {
        "generated_at": __import__("datetime").datetime.now().isoformat(),
        "summary": {
            "total_agents": len(agents),
            "total_lessons": len(all_lessons),
            "agents_with_lessons": sum(1 for a in agents if a["has_lessons"]),
        },
        "agents": sorted(agents, key=lambda a: a["order"]),
        "pipeline": {
            "stages": PIPELINE_STAGES,
            "roles": roles_pipeline,
        },
        "lessons": {
            "items": all_lessons,
            "summary": {
                "total_lessons": len(all_lessons),
                "by_agent": {k: len(v) for k, v in lesson_by_agent.items() if v},
                "by_category": lesson_by_category,
            },
        },
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {OUTPUT_FILE}")
    print(f"  {len(agents)} agents, {len(all_lessons)} lessons")
    print(f"  Agents with lessons: {[a['id'] for a in agents if a['has_lessons']]}")


if __name__ == "__main__":
    main()
