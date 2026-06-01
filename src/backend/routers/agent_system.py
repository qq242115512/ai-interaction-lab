"""Agent system router — exposes 15-role pipeline metadata, status, lessons, and knowledge graph.

Endpoints:
    GET /api/agent-system/status    — agent list + summary from SKILL.md/LESSONS.md on disk
    GET /api/agent-system/pipeline  — full pipeline DAG definition
    GET /api/agent-system/lessons   — structured lessons parsed from all LESSONS.md files
    GET /api/agent-system/knowledge — Hindsight knowledge graph (placeholder if empty)
"""

import os
import re
import logging
from pathlib import Path
from fastapi import APIRouter

logger = logging.getLogger("design-mentor")

router = APIRouter()

# ---------------------------------------------------------------------------
# Configuration — where the agent skill files live
# ---------------------------------------------------------------------------
_AGENTS_DIR_ENV = os.getenv("AGENT_SKILLS_DIR", "")
_DEFAULT_CANDIDATES = [
    Path("C:/Users/qq242/.claude/skills/agents"),
    Path.home() / ".claude" / "skills" / "agents",
    Path("/mnt/c/Users/qq242/.claude/skills/agents"),
]

def _resolve_agents_dir() -> Path | None:
    if _AGENTS_DIR_ENV:
        p = Path(_AGENTS_DIR_ENV)
        if p.is_dir():
            return p
    for candidate in _DEFAULT_CANDIDATES:
        if candidate.is_dir():
            return candidate
    return None

AGENTS_DIR = _resolve_agents_dir()

# ---------------------------------------------------------------------------
# Hard-coded role metadata (canonical, derived from CLAUDE.md)
# ---------------------------------------------------------------------------
_ROLE_META: dict[str, dict] = {
    "orchestrator": {
        "name": "Orchestrator",
        "name_zh": "协调器",
        "icon": "🎯",
        "model": "Opus",
        "stage": "coordination",
        "responsibilities": ["协调分发", "质量把关", "接口契约", "技术分解", "范围裁剪"],
        "depends_on": [],
        "feeds_into": ["scout"],
        "description": "协调分发、质量把关、接口契约",
    },
    "scout": {
        "name": "Scout",
        "name_zh": "侦察兵",
        "icon": "🔍",
        "model": "Sonnet",
        "stage": "scout",
        "responsibilities": ["技术栈摸底", "文件结构确认", "命令可用性检查"],
        "depends_on": ["orchestrator"],
        "feeds_into": ["ba"],
        "description": "摸底调研、技术栈文档",
    },
    "ba": {
        "name": "BA",
        "name_zh": "业务分析师",
        "icon": "📋",
        "model": "Sonnet",
        "stage": "requirements",
        "responsibilities": ["需求澄清", "用户故事编写", "验收标准定义"],
        "depends_on": ["scout"],
        "feeds_into": ["adversarial-reviewer"],
        "description": "需求澄清、用户故事、验收标准",
    },
    "adversarial-reviewer": {
        "name": "Adversarial Reviewer",
        "name_zh": "对抗审查员",
        "icon": "⚔️",
        "model": "Opus",
        "stage": "requirements",
        "responsibilities": ["常规审查", "元审查（审Orchestrator）", "预验尸"],
        "depends_on": ["ba"],
        "feeds_into": ["pm"],
        "description": "常规审查+元审查+预验尸",
    },
    "pm": {
        "name": "PM",
        "name_zh": "项目经理",
        "icon": "📊",
        "model": "Sonnet",
        "stage": "requirements",
        "responsibilities": ["任务路由", "风险登记册", "阶段门检查", "进度追踪"],
        "depends_on": ["adversarial-reviewer"],
        "feeds_into": ["designer"],
        "description": "任务路由、风险登记册、阶段门检查",
    },
    "designer": {
        "name": "UX/UI Designer",
        "name_zh": "设计师",
        "icon": "🎨",
        "model": "Opus",
        "stage": "design",
        "responsibilities": ["视觉设计", "交互状态设计", "设计Token", "WCAG无障碍"],
        "depends_on": ["pm"],
        "feeds_into": ["frontend", "backend", "fullstack"],
        "description": "视觉设计、交互状态、设计Token、WCAG",
    },
    "frontend": {
        "name": "Frontend Developer",
        "name_zh": "前端开发",
        "icon": "💻",
        "model": "Sonnet",
        "stage": "implementation",
        "responsibilities": ["HTML/CSS/JS实现", "GSAP动画", "响应式适配"],
        "depends_on": ["designer"],
        "feeds_into": ["code-reviewer"],
        "description": "HTML/CSS/JS/GSAP 实现",
    },
    "backend": {
        "name": "Backend Developer",
        "name_zh": "后端开发",
        "icon": "⚙️",
        "model": "Sonnet",
        "stage": "implementation",
        "responsibilities": ["API开发", "数据库设计", "业务逻辑"],
        "depends_on": ["designer"],
        "feeds_into": ["code-reviewer"],
        "description": "API/数据库/业务逻辑",
    },
    "fullstack": {
        "name": "Fullstack Developer",
        "name_zh": "全栈开发",
        "icon": "🔧",
        "model": "Sonnet",
        "stage": "implementation",
        "responsibilities": ["端到端垂直切片", "前后端联调"],
        "depends_on": ["designer"],
        "feeds_into": ["code-reviewer"],
        "description": "端到端垂直切片（<5页面优先）",
    },
    "code-reviewer": {
        "name": "Code Reviewer",
        "name_zh": "代码审查员",
        "icon": "👀",
        "model": "Sonnet",
        "stage": "implementation",
        "responsibilities": ["5层分层代码审查"],
        "depends_on": ["frontend", "backend", "fullstack"],
        "feeds_into": ["qa"],
        "description": "5层分层代码审查",
    },
    "qa": {
        "name": "QA Engineer",
        "name_zh": "测试工程师",
        "icon": "🧪",
        "model": "Sonnet",
        "stage": "implementation",
        "responsibilities": ["AI专项测试", "传统功能测试", "回归测试"],
        "depends_on": ["code-reviewer"],
        "feeds_into": ["security"],
        "description": "AI专项测试+传统测试",
    },
    "security": {
        "name": "Security Guardian",
        "name_zh": "安全卫士",
        "icon": "🛡️",
        "model": "Sonnet",
        "stage": "implementation",
        "responsibilities": ["安全漏洞审计", "注入防护", "CSP策略"],
        "depends_on": ["qa"],
        "feeds_into": ["devops"],
        "description": "安全漏洞审计",
    },
    "devops": {
        "name": "DevOps Engineer",
        "name_zh": "运维工程师",
        "icon": "🚀",
        "model": "Sonnet",
        "stage": "delivery",
        "responsibilities": ["部署", "CI/CD", "Git版本管理", "回滚"],
        "depends_on": ["security"],
        "feeds_into": ["tech-writer"],
        "description": "部署、CI/CD、Git版本管理",
    },
    "tech-writer": {
        "name": "Technical Writer",
        "name_zh": "技术文档工程师",
        "icon": "📝",
        "model": "Sonnet",
        "stage": "delivery",
        "responsibilities": ["文档编写", "ADR架构决策记录", "Changelog"],
        "depends_on": ["devops"],
        "feeds_into": ["memory-curator"],
        "description": "文档、ADR、Changelog",
    },
    "memory-curator": {
        "name": "Memory Curator",
        "name_zh": "记忆策展人",
        "icon": "🧠",
        "model": "Sonnet",
        "stage": "delivery",
        "responsibilities": ["跨会话记忆归档", "Session State", "教训管理"],
        "depends_on": ["tech-writer"],
        "feeds_into": [],
        "description": "跨会话记忆、Session State、教训管理",
    },
}

_AGENT_ORDER = [
    "orchestrator", "scout", "ba", "adversarial-reviewer", "pm",
    "designer",
    "frontend", "backend", "fullstack", "code-reviewer", "qa", "security",
    "devops", "tech-writer", "memory-curator",
]

# ---------------------------------------------------------------------------
# Pipeline stage definitions
# ---------------------------------------------------------------------------
_PIPELINE_STAGES = [
    {
        "id": "scout",
        "name": "调研摸底",
        "description": "确认技术栈、文件结构、命令可用性，发现缺口",
        "order": 1,
        "roles": ["scout"],
    },
    {
        "id": "requirements",
        "name": "需求分析",
        "description": "用户故事、验收标准、对抗审查、风险登记",
        "order": 2,
        "roles": ["ba", "adversarial-reviewer", "pm"],
    },
    {
        "id": "design",
        "name": "设计",
        "description": "视觉设计、交互状态、设计Token、WCAG无障碍",
        "order": 3,
        "roles": ["designer"],
    },
    {
        "id": "implementation",
        "name": "实现与验证",
        "description": "前后端开发、代码审查、测试、安全加固",
        "order": 4,
        "roles": ["frontend", "backend", "fullstack", "code-reviewer", "qa", "security"],
    },
    {
        "id": "delivery",
        "name": "交付与归档",
        "description": "部署上线、文档编写、记忆归档、教训飞轮",
        "order": 5,
        "roles": ["devops", "tech-writer", "memory-curator"],
    },
]

# ---------------------------------------------------------------------------
# Category inference heuristics for lessons
# ---------------------------------------------------------------------------
# NOTE: all patterns must be lowercase — the search runs on text.lower()
# Ordered by priority: more specific categories checked first
_CATEGORY_KEYWORDS: list[tuple[str, str]] = [
    ("orchestrat|协调.*分发|多实例|同一.*agent.*spawn|上下文断裂|agent.*dispatch|agent.*handoff|跨会话保留|会丢失上下文", "orchestration"),
    ("闭环验证|元教训|任何修改都必须|改了.*配置.*确认.*生效|验证.*真的能用|skill\\\\(.*\\\\)验证|mcp.*验证|skill.*目录.*不是", "orchestration"),
    ("注入|绕过.*过滤|前缀注入|system:|忽略.*忘记.*无视|角色.*扮演.*泄露|csp|csrf|重放|xss", "security"),
    ("只写文档没写代码|security baseline|rate.*limit.*代码|限流.*未实现", "security"),
    ("动画.*混用|gsap.*css|css.*gsap|opacity.*抢|动画.*控制权|gsap\\\\.from|scrolltrigger|autoalpha|tween|css 动画", "animation"),
    ("nginx.*验证|sed.*nginx|nginx -t|配置文件.*崩|多个端点.*404|端点.*404|curl.*验证.*端点", "deployment"),
    ("docker.*hub.*墙|拉镜像|ghcr|registry|镜像.*不可用|docker.*pull.*超时", "deployment"),
    ("postgresql|pg.*version|wal|数据库.*崩溃|嵌入式.*pg|数据全丢|wsl2.*强关", "infrastructure"),
    ("部署|deploy|服务器.*配置|docker|nginx|https|域名|dns", "deployment"),
    ("流式.*非流式|stream.*fallback|流式端点|解析失败.*重试|json.*解析.*降级", "api-design"),
    ("ttl.*过期|内存.*会话|待确认.*清理|永久占用内存|session.*ttl|确认操作.*过期", "api-design"),
    ("api|端点|流式|stream|fallback|降级|重试", "api-design"),
    ("重构.*函数声明|残留代码|语法错误.*罢工|脚本罢工|整页.*脚本|console.*语法错误", "code-quality"),
    ("技能目录.*不是|单数.*复数|skill.*扫描|settings\\\\.json.*注册|路径.*差一个字母", "configuration"),
    ("动画|animation", "animation"),
    ("安全|security", "security"),
]

def _infer_category(text: str, bug_description: str = "") -> str:
    """Infer lesson category from keyword matching.

    Searches the bug_description (title) first with higher priority,
    then falls back to the full body text.
    """
    lower_title = bug_description.lower() if bug_description else ""
    lower_full = text.lower()

    # Priority round 1: search bug_description only
    for pattern, cat in _CATEGORY_KEYWORDS:
        parts = pattern.split("|")
        for p in parts:
            if lower_title and re.search(p, lower_title):
                return cat

    # Priority round 2: search full text
    for pattern, cat in _CATEGORY_KEYWORDS:
        parts = pattern.split("|")
        for p in parts:
            if re.search(p, lower_full):
                return cat

    return "general"

def _infer_severity(text: str) -> str:
    """Infer severity: high if the problem caused breakage or silent failure."""
    high_signals = [
        "罢工", "全部消失", "不可见", "404", "全废", "全丢",
        "数据全丢", "永久不可见", "整页", "卡在", "崩溃",
        "永远不", "一个都找不到", "无信号", "零报错",
        "脚本罢工", "多个端点", "整个文件结构崩",
    ]
    for signal in high_signals:
        if signal in text:
            return "high"
    return "medium"

# ---------------------------------------------------------------------------
# Helpers — file system
# ---------------------------------------------------------------------------

def _count_lines(path: Path) -> int:
    """Count lines in a file. Returns 0 if file is missing."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    except Exception as exc:
        logger.warning(f"Cannot read {path}: {exc}")
        return 0

def _parse_lessons_file(lessons_path: Path) -> list[dict]:
    """Parse a LESSONS.md file and return a list of structured lesson dicts.

    Expected format:
        ## YYYY-MM-DD — Project Name
        - **Bug description**: rest of line
    """
    lessons: list[dict] = []
    if not lessons_path.is_file():
        return lessons

    try:
        content = lessons_path.read_text(encoding="utf-8")
    except Exception as exc:
        logger.warning(f"Cannot read {lessons_path}: {exc}")
        return lessons

    # Split into sections by ## heading
    sections = re.split(r"\n##\s+", content)
    for section in sections[1:]:  # skip preamble (first split chunk before any ##)
        lines = section.strip().split("\n")
        if not lines:
            continue
        # First line is "YYYY-MM-DD — Project Name"
        heading = lines[0].strip()
        heading_match = re.match(r"(\d{4}-\d{2}-\d{2})\s*[—\-]\s*(.+)", heading)
        if not heading_match:
            continue

        date = heading_match.group(1)
        project = heading_match.group(2).strip()

        # Process remaining lines: find `- **` bullets
        i = 1
        while i < len(lines):
            line = lines[i].strip()
            # A lesson bullet: `- **bold text** rest`
            match = re.match(r"-\s*\*\*(.+?)\*\*(.*)", line)
            if match:
                bug_description = match.group(1).strip()
                rest = match.group(2).strip()

                # Collect full body (may span multiple lines until the next bullet or empty line)
                body_parts = [rest] if rest else []
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    if not next_line or re.match(r"-\s*\*\*", next_line) or next_line.startswith("## "):
                        break
                    body_parts.append(next_line)
                    j += 1
                full_body = " ".join(body_parts)

                # Extract fix_rule: look for text after "教训：" or "教训:**" patterns
                fix_rule = ""
                fix_match = re.search(r"教训[：:]\s*\*?\*?\s*(.+)$", full_body)
                if not fix_match:
                    fix_match = re.search(r"修法[：:]\s*(.+)$", full_body)
                if fix_match:
                    fix_rule = fix_match.group(1).strip()
                else:
                    # Use the bug_description itself as a fallback fix hint
                    fix_rule = bug_description

                combined = f"{bug_description} {full_body}"
                category = _infer_category(combined, bug_description)
                severity = _infer_severity(combined)

                lessons.append({
                    "id": "",  # filled in later with sequential numbering
                    "agent": "",  # filled in by caller
                    "agent_name": "",  # filled in by caller
                    "date": date,
                    "project": project,
                    "bug_description": bug_description,
                    "fix_rule": fix_rule,
                    "category": category,
                    "severity": severity,
                })
                i = j
            else:
                i += 1

    return lessons


def _count_lesson_sections(content: str) -> int:
    """Count ## headings that look like dates (YYYY-MM-DD)."""
    return len(re.findall(r"^##\s+\d{4}-\d{2}-\d{2}", content, re.MULTILINE))


def _count_lesson_bullets(content: str) -> int:
    """Count individual lesson bullets (- **...)."""
    return len(re.findall(r"^\s*-\s*\*\*", content, re.MULTILINE))


# ---------------------------------------------------------------------------
# Endpoint 1: GET /api/agent-system/status
# ---------------------------------------------------------------------------

@router.get("/agent-system/status")
async def get_agent_status():
    """Read all 15 agent SKILL.md files from disk and return status info."""
    agents = []
    agents_with_lessons = 0
    total_lessons_bullets = 0

    for agent_id in _AGENT_ORDER:
        meta = _ROLE_META.get(agent_id, {})
        agent_name = meta.get("name", agent_id)
        skill_lines = 0
        has_lessons = False
        lessons_count = 0

        if AGENTS_DIR:
            agent_dir = AGENTS_DIR / agent_id
            skill_path = agent_dir / "SKILL.md"
            lessons_path = agent_dir / "LESSONS.md"

            skill_lines = _count_lines(skill_path)
            if lessons_path.is_file():
                has_lessons = True
                try:
                    content = lessons_path.read_text(encoding="utf-8")
                    lessons_count = _count_lesson_bullets(content)
                except Exception:
                    lessons_count = 0

        if has_lessons:
            agents_with_lessons += 1
            total_lessons_bullets += lessons_count

        agents.append({
            "id": agent_id,
            "name": agent_name,
            "name_zh": meta.get("name_zh", ""),
            "stage": meta.get("stage", "unknown"),
            "icon": meta.get("icon", ""),
            "model": meta.get("model", "Unknown"),
            "skill_lines": skill_lines,
            "has_lessons": has_lessons,
            "lessons_count": lessons_count,
            "description": meta.get("description", ""),
        })

    if not AGENTS_DIR:
        logger.warning("Agent skills directory not found — returning metadata-only status")

    return {
        "agents": agents,
        "summary": {
            "total_agents": len(agents),
            "agents_with_lessons": agents_with_lessons,
            "total_lessons": total_lessons_bullets,
            "pipeline_stages": 5,
        },
    }


# ---------------------------------------------------------------------------
# Endpoint 2: GET /api/agent-system/pipeline
# ---------------------------------------------------------------------------

@router.get("/agent-system/pipeline")
async def get_pipeline():
    """Return the complete pipeline DAG definition."""
    # Build roles list from metadata
    roles = []
    for agent_id in _AGENT_ORDER:
        meta = _ROLE_META.get(agent_id, {})
        roles.append({
            "id": agent_id,
            "name": meta.get("name", agent_id),
            "name_zh": meta.get("name_zh", ""),
            "stage": meta.get("stage", "unknown"),
            "icon": meta.get("icon", ""),
            "model": meta.get("model", "Unknown"),
            "responsibilities": meta.get("responsibilities", []),
            "depends_on": meta.get("depends_on", []),
            "feeds_into": meta.get("feeds_into", []),
        })

    # Build connections from metadata
    connections = []
    seen = set()
    for agent_id in _AGENT_ORDER:
        meta = _ROLE_META.get(agent_id, {})
        for target in meta.get("feeds_into", []):
            pair = (agent_id, target)
            if pair not in seen:
                connections.append({"from": agent_id, "to": target})
                seen.add(pair)

    return {
        "stages": _PIPELINE_STAGES,
        "roles": roles,
        "connections": connections,
    }


# ---------------------------------------------------------------------------
# Endpoint 3: GET /api/agent-system/lessons
# ---------------------------------------------------------------------------

@router.get("/agent-system/lessons")
async def get_lessons():
    """Read all LESSONS.md files from agent directories and return structured data."""
    all_lessons: list[dict] = []
    by_agent: dict[str, int] = {}
    by_category: dict[str, int] = {}

    if not AGENTS_DIR:
        logger.warning("Agent skills directory not found — returning empty lessons")
        return {
            "lessons": [],
            "summary": {
                "total_lessons": 0,
                "by_agent": {},
                "by_category": {},
            },
        }

    lesson_counter = 0

    for agent_id in _AGENT_ORDER:
        meta = _ROLE_META.get(agent_id, {})
        agent_name = meta.get("name", agent_id)
        lessons_path = AGENTS_DIR / agent_id / "LESSONS.md"

        if not lessons_path.is_file():
            continue

        parsed = _parse_lessons_file(lessons_path)
        for lesson in parsed:
            lesson_counter += 1
            lid = f"les-{lesson_counter:03d}"
            lesson["id"] = lid
            lesson["agent"] = agent_id
            lesson["agent_name"] = agent_name

            all_lessons.append(lesson)

            by_agent[agent_id] = by_agent.get(agent_id, 0) + 1
            cat = lesson.get("category", "general")
            by_category[cat] = by_category.get(cat, 0) + 1

    return {
        "lessons": all_lessons,
        "summary": {
            "total_lessons": len(all_lessons),
            "by_agent": by_agent,
            "by_category": by_category,
        },
    }


# ---------------------------------------------------------------------------
# Endpoint 4: GET /api/agent-system/knowledge
# ---------------------------------------------------------------------------

@router.get("/agent-system/knowledge")
async def get_knowledge():
    """Attempt to read from the Hindsight knowledge graph.

    Returns a placeholder when the graph is empty / unreachable, with
    the expected entity/relation structure for when the Memory Curator
    populates it after the first complete project flow.
    """
    # Try Hindsight — the MCP server may expose a local REST API.
    # For now we return the placeholder; this endpoint can be extended
    # to call the Hindsight REST API once it exposes one.
    hindsight_url = os.getenv("HINDSIGHT_API_URL", "")
    if hindsight_url:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{hindsight_url.rstrip('/')}/entities")
                if resp.status_code == 200:
                    data = resp.json()
                    entities = data.get("entities", [])
                    relations = data.get("relations", [])
                    return {
                        "status": "connected",
                        "message": f"知识图谱已连接：{len(entities)} 实体, {len(relations)} 关系",
                        "entities_count": len(entities),
                        "relations_count": len(relations),
                        "entities": entities,
                        "relations": relations,
                    }
        except Exception as exc:
            logger.warning(f"Hindsight API unreachable: {exc}")

    # Placeholder — empty knowledge graph
    logger.info("Knowledge graph is empty — returning placeholder")
    return {
        "status": "empty",
        "message": (
            "知识图谱尚未建立。完成第一个完整项目流程后，Memory Curator "
            "会将关键决策和教训写入 Hindsight。"
        ),
        "entities_count": 0,
        "relations_count": 0,
        "sample_structure": {
            "entity_types": ["Agent", "Project", "Lesson", "Decision", "Bug"],
            "relation_types": ["learned_from", "caused_by", "fixed_by", "reviewed_by"],
        },
    }
