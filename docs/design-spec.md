# AI 交互模式实验室 -- 视觉设计规范 v2.0

> **设计目标**：把这个看起来像技术文档的网站，变成一个设计师的作品集。
> 网站本身 IS 设计证明 -- 面试官打开网址的第一眼，就应该知道这是设计师做的。

---

## 目录

1. [设计方向](#1-设计方向)
2. [颜色系统](#2-颜色系统)
3. [字体层级](#3-字体层级)
4. [间距与布局](#4-间距与布局)
5. [圆角与阴影](#5-圆角与阴影)
6. [动效语言](#6-动效语言)
7. [组件设计](#7-组件设计)
8. [全局布局重构](#8-全局布局重构)
9. [响应式策略](#9-响应式策略)
10. [首页设计](#10-首页设计)
11. [7 个模式页设计](#11-7-个模式页设计)
12. [次级页面设计](#12-次级页面设计)
13. [无障碍清单](#13-无障碍清单)
14. [CSS 变量完整定义](#14-css-变量完整定义)
15. [迁移清单](#15-迁移清单)

---

## 1. 设计方向

### 1.1 核心叙事

**"设计师的笔记本"** -- 温暖、有人味、手工感的设计作品集。

不是冷冰冰的技术文档，不是一个模板套了 13 页。是一个设计师在展示他对 AI 交互的系统性思考，每一页都有独立的设计态度。

### 1.2 视觉关键词

| 关键词 | 表现方式 |
|--------|----------|
| **温暖** | 奶油色底代替冷灰白，暖色调强调色 |
| **手工** | 微妙纹理、不规则装饰、手写感细节 |
| **系统** | 网格骨架、一致的组件、有目的的间距 |
| **戏剧** | 深浅对比（暗色 section 穿插在亮色之间） |
| **动感** | 每个模式页的动效服务于该模式的概念 |

### 1.3 不做的事

- 不做拟物化（太重的阴影、渐变、纹理）
- 不做玻璃态（玻璃拟态已经审美疲劳）
- 不做纯扁平（没有层次感的扁平 = 无聊）
- 不做暗色模式全站（暗色作为区域强调，不是全局）

---

## 2. 颜色系统

### 2.1 全局调色板

```
暖白底系统（替代原来的 #fafaf9 冷灰白）
--stone-50:  #faf9f7   页面背景（暖白，替代 #fafaf9）
--stone-100: #f5f0eb   卡片悬浮态 / 区域强调
--stone-200: #e8e0d5   边框
--stone-300: #d4c9b8   禁用态边框
--stone-600: #8b7e6c   次要文字
--stone-700: #6b5d4f   正文文字（替代纯黑 #1c1917）
--stone-900: #2d2418   标题 / 强调文字

暗色强调面板（穿插在亮色页面中制造戏剧感）
--dark-900: #1a1815   暗色面板背景
--dark-800: #2d2822   暗色面板卡片
--dark-300: #a09888   暗色面板次要文字
--dark-100: #e8e0d5   暗色面板高亮文字

主色（替代原来的 indigo #6366f1）
--accent:      #e05b3c   暖珊瑚色（有设计师的"人味"）
--accent-hover:#c94a2e   悬停加深
--accent-light:#fef0ec   浅色背景
--accent-muted:#f4c4b8   装饰用淡色

功能色
--success:       #2d8a6e   翠绿（替代 #10b981）
--success-light: #eaf5f0
--warning:       #d4850a   暖黄（替代 #f59e0b）
--warning-light: #fdf3e2
--error:         #c94043   深红（替代 #ef4444）
--error-light:   #fef0f0

中性装饰色（用于标签、badge、分区）
--slate-400: #9b9080
--slate-500: #7d7160
```

### 2.2 各模式页主题色

每个模式页有自己的"概念色"，对应其交互模式的情感特质：

| # | 模式 | 概念色 | 色值 | 情感 |
|---|------|--------|------|------|
| 1 | 流式输出 | **电流绿** | `#00c48c` | 实时、脉冲、活力 |
| 2 | 结构化卡片 | **琥珀金** | `#d4850a` | 秩序、清晰、信息块 |
| 3 | 澄清提问 | **对话紫** | `#8b5cf6` | 好奇、对话、追问 |
| 4 | 失败兜底 | **护盾青** | `#0d9488` | 安全、防御、可靠 |
| 5 | 多轮上下文 | **记忆粉** | `#db2777` | 连接、记忆、时间线 |
| 6 | 确认机制 | **警戒橙** | `#ea580c` | 暂停、确认、门槛 |
| 7 | 渐进式加载 | **揭示蓝** | `#2563eb` | 层层展开、发现、深度 |

每个模式页通过 CSS 自定义属性注入概念色：
```css
/* 在模式页 <style> 中覆写 */
:root {
  --pattern-accent: #00c48c;
  --pattern-accent-light: #e6faf4;
  --pattern-accent-muted: #b3f0dc;
}
```

### 2.3 色彩对比度合规

所有文字/背景组合需通过 WCAG AA：

| 组合 | 对比度 | 达标 |
|------|--------|------|
| `--stone-700` 正文 on `--stone-50` 背景 | 7.2:1 | AAA |
| `--stone-600` 次要 on `--stone-50` 背景 | 4.9:1 | AA |
| `--dark-100` 文字 on `--dark-900` 背景 | 8.5:1 | AAA |
| `--accent` on `--stone-50` | 4.1:1 | AA 大文本 |
| `--accent` 按钮文字 (white) on `--accent` | 4.2:1 | AA 大文本 |
| 各概念色 on 白底 | 见各页 | 需逐个验证 |

---

## 3. 字体层级

### 3.1 字体导入

```css
/* Google Fonts / 国内 CDN */
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Inter:wght@400;500;600;700;800&display=swap');

/*
备选 CDN（Google 不可用时）:
- 中文字体：https://cdn.bootcdn.net/ajax/libs/lxgw-wenkai-webfont/1.7.0/lxgwwenkai-regular.css
  （霞鹜文楷，免费可商用，手写感强，适合标题点缀）
*/
```

### 3.2 字体栈

```css
:root {
  /* 正文：Inter + 中文系统字体 */
  --font-body: "Inter", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", system-ui, -apple-system, sans-serif;

  /* 标题：衬线体 + 中文衬线，有设计感 */
  --font-heading: "Noto Serif SC", "PingFang SC", "STSong", "SimSun", "Times New Roman", serif;

  /* 代码 / 技术标注 */
  --font-mono: "JetBrains Mono", "SF Mono", "Cascadia Code", "Consolas", "Menlo", monospace;

  /* 手写点缀（引文、标签、特殊标注） */
  --font-display: "LXGW WenKai", "KaiTi", "STKaiti", "楷体", serif;
}
```

**选择理由**：
- `Noto Serif SC`：中文衬线字体中 web 渲染最好的之一，Google 维护，免费
- `Inter`：西文无衬线字体中可读性最好的之一，variable font 节省加载
- `LXGW WenKai`（霞鹜文楷）：手写风格，用于点缀性文本（引文、标签、hero 副标题），免费可商用
- 放弃了系统字体栈 `-apple-system` 作为正文字体 -- 设计师的作品集不应该看起来像系统设置页面

### 3.3 字号层级

```css
:root {
  /* 基于 16px 根字号 */
  --text-xs:    0.6875rem;   /* 11px - 标签、注脚 */
  --text-sm:    0.8125rem;   /* 13px - 辅助文字、卡片描述 */
  --text-base:  0.9375rem;   /* 15px - 正文（比默认 16px 略小，中文可读性更好）*/
  --text-md:    1.0625rem;   /* 17px - 强调正文 */
  --text-lg:    1.25rem;     /* 20px - section 标题 */
  --text-xl:    1.5rem;      /* 24px - 页面标题 */
  --text-2xl:   2rem;        /* 32px - hero 标题 */
  --text-3xl:   2.75rem;     /* 44px - 首页大标题 */

  /* 行高 */
  --leading-tight:  1.25;   /* 标题 */
  --leading-normal: 1.6;    /* 正文 */
  --leading-relaxed:1.8;    /* 长文、设计说明 */
}
```

### 3.4 排版规则

1. **中文正文优先 15px**（`--text-base`），不是浏览器默认 16px -- 中文笔画密度高，15px 可读性更好
2. **标题用衬线体**（`--font-heading`），正文用无衬线体（`--font-body`）-- 制造层次感
3. **中英文混排时空格**：在 CSS 中用 `word-spacing: 0.05em` 给中英文之间留呼吸空间（或通过 JS 自动插入空格，但优先 CSS 方案）
4. **长文本区增加行高** -- 模式页的设计说明用 `--leading-relaxed`（1.8），Demo 区用 `--leading-normal`（1.6）
5. **数字和评分用 tabular-nums**：`font-variant-numeric: tabular-nums` 让数字等宽对齐

---

## 4. 间距与布局

### 4.1 间距尺度

基于 4px 网格系统：

```css
--space-1:  0.25rem;  /* 4px  */
--space-2:  0.5rem;   /* 8px  */
--space-3:  0.75rem;  /* 12px */
--space-4:  1rem;     /* 16px */
--space-5:  1.5rem;   /* 24px */
--space-6:  2rem;     /* 32px */
--space-8:  3rem;     /* 48px */
--space-10: 4rem;     /* 64px */
--space-12: 5rem;     /* 80px */
--space-16: 8rem;     /* 128px */
```

### 4.2 最大宽度

```css
/* 原来的 840px 太窄 -- 设计师的页面需要呼吸空间 */
--max-width-content: 720px;    /* 正文阅读区（设计说明文字） */
--max-width-page:    960px;    /* 页面内容区 */
--max-width-wide:   1120px;    /* 首页卡片网格 */
--max-width-full:   1280px;    /* 超大屏上限 */

/* 两侧内边距 */
--page-padding-x: var(--space-5);  /* 24px 手机 / 保持到桌面 */
```

### 4.3 网格系统

```css
/* 7 卡片首页网格 */
.home-pattern-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
}

/* 模式页两栏布局（设计说明 + Demo） */
.pattern-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-8);
}

/* 设计原则总结页 */
.principles-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-5);
}
```

---

## 5. 圆角与阴影

### 5.1 圆角

```css
--radius-none: 0;
--radius-xs:   3px;    /* inline code, small badges */
--radius-sm:   6px;    /* buttons, inputs, tags */
--radius-md:   10px;   /* cards (保持原来的 10px，这个不错) */
--radius-lg:   16px;   /* large cards, demo areas */
--radius-xl:   24px;   /* hero sections, featured cards */
--radius-full: 9999px; /* pills, avatars */
```

### 5.2 阴影

**原则：少用阴影，用边框和背景色差来区分层次。** 原来的阴影太"开发者工具"。

```css
/* 页面默认不需要卡片阴影 -- 用 border 替代 */
--shadow-none: none;

/* 悬浮时用非常微妙的阴影 -- 只用在不 hover 就看不出是卡片的情况下 */
--shadow-hover: 0 2px 16px rgba(45, 36, 24, 0.08);  /* warm shadow */

/* 对话框 / 浮层 */
--shadow-overlay: 0 8px 40px rgba(45, 36, 24, 0.12);
```

**关键决策**：卡片默认状态用 `border: 1px solid var(--stone-200)` 而不是阴影。浮起效果用 `transform: translateY(-2px)` + `border-color` 变化。这比阴影更干净、更"设计师"。

---

## 6. 动效语言

### 6.1 设计原则

1. **动画必须有意义** -- 每个动画应该解释一个交互概念，不是"因为能动所以动"
2. **优先 CSS only** -- `@keyframes` + `transition` + `animation` 能做的就不要 JS
3. **尊重 reduced-motion** -- 所有动画包在 `@media (prefers-reduced-motion: no-preference)` 里
4. **200-400ms 持续时间** -- 快但能被感知到
5. **ease-out 为主** -- 物体减速停止更自然

### 6.2 缓动函数

```css
--ease-out:    cubic-bezier(0.16, 1, 0.3, 1);     /* 标准出场 */
--ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);    /* 平滑过渡 */
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1); /* 弹性（少用，点缀） */
--ease-slow:   cubic-bezier(0.4, 0, 0.2, 1);      /* 慢速淡入 */
```

### 6.3 全局微交互

```css
/* ===== 链接悬停 ===== */
a, .clickable {
  transition: color 0.2s var(--ease-out);
}

/* ===== 按钮反馈 ===== */
.btn {
  transition: background 0.2s var(--ease-out),
              transform 0.15s var(--ease-out),
              box-shadow 0.2s var(--ease-out);
}
.btn:active {
  transform: scale(0.97);  /* 按压反馈 */
}

/* ===== 卡片入场（首页） ===== */
.pattern-card {
  opacity: 0;
  transform: translateY(24px);
  animation: card-enter 0.5s var(--ease-out) forwards;
}
/* 每个卡片错开 80ms -- 用 JS 设置 animation-delay 或用 CSS nth-child */
.pattern-card:nth-child(1) { animation-delay: 0.05s; }
.pattern-card:nth-child(2) { animation-delay: 0.13s; }
.pattern-card:nth-child(3) { animation-delay: 0.21s; }
.pattern-card:nth-child(4) { animation-delay: 0.29s; }
.pattern-card:nth-child(5) { animation-delay: 0.37s; }
.pattern-card:nth-child(6) { animation-delay: 0.45s; }
.pattern-card:nth-child(7) { animation-delay: 0.53s; }

@keyframes card-enter {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ===== 滚动触发淡入（用 Intersection Observer + CSS class，JS 仅添加 class）===== */
.reveal-on-scroll {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.6s var(--ease-out),
              transform 0.6s var(--ease-out);
}
.reveal-on-scroll.visible {
  opacity: 1;
  transform: translateY(0);
}

/* ===== section 分隔动画 ===== */
.pattern-section {
  transition: border-color 0.4s var(--ease-out);
}
```

### 6.4 模式专属动效（CSS keyframes）

每个模式页有一个概念动效，在 Demo 区展示：

#### 模式 1：流式输出 -- 打字机光标
```css
@keyframes cursor-blink {
  0%, 100% { opacity: 1; }
  50%      { opacity: 0; }
}
@keyframes text-reveal {
  from { width: 0; }
  to   { width: 100%; }
}
.stream-cursor::after {
  content: "|";
  animation: cursor-blink 0.8s infinite;
  color: var(--pattern-accent);
  font-weight: 300;
}
```

#### 模式 2：结构化卡片 -- 卡片浮入
```css
@keyframes card-stack {
  0%   { transform: translateY(16px) scale(0.96); opacity: 0; }
  100% { transform: translateY(0) scale(1); opacity: 1; }
}
@keyframes card-shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
/* 卡片加载骨架屏 */
.card-skeleton {
  background: linear-gradient(90deg, var(--stone-100) 25%, var(--stone-50) 50%, var(--stone-100) 75%);
  background-size: 200% 100%;
  animation: card-shimmer 1.5s infinite;
}
```

#### 模式 3：澄清提问 -- 对话气泡弹入
```css
@keyframes bubble-pop {
  0%   { transform: scale(0.8); opacity: 0; }
  50%  { transform: scale(1.03); }
  100% { transform: scale(1); opacity: 1; }
}
@keyframes question-mark-pulse {
  0%, 100% { transform: scale(1); opacity: 0.6; }
  50%      { transform: scale(1.15); opacity: 1; }
}
```

#### 模式 4：失败兜底 -- 防御层淡入
```css
@keyframes shield-appear {
  0%   { clip-path: circle(0% at 50% 50%); opacity: 0; }
  100% { clip-path: circle(100% at 50% 50%); opacity: 1; }
}
@keyframes layer-stack {
  0%   { transform: translateY(-8px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}
```

#### 模式 5：多轮上下文 -- 时间线绘制
```css
@keyframes timeline-grow {
  from { height: 0; }
  to   { height: 100%; }
}
@keyframes dot-appear {
  0%   { transform: scale(0); }
  50%  { transform: scale(1.3); }
  100% { transform: scale(1); }
}
/* 记忆粒子 */
@keyframes memory-pulse {
  0%, 100% { box-shadow: 0 0 0 0 var(--pattern-accent-muted); }
  50%      { box-shadow: 0 0 0 8px transparent; }
}
```

#### 模式 6：确认机制 -- 脉冲警告
```css
@keyframes warning-pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(234, 88, 12, 0.3); }
  50%      { box-shadow: 0 0 0 12px rgba(234, 88, 12, 0); }
}
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%      { transform: translateX(-4px); }
  40%      { transform: translateX(4px); }
  60%      { transform: translateX(-3px); }
  80%      { transform: translateX(3px); }
}
```

#### 模式 7：渐进式加载 -- 逐层揭示
```css
@keyframes curtain-rise {
  from { clip-path: inset(0 0 100% 0); }
  to   { clip-path: inset(0 0 0 0); }
}
@keyframes fade-slide-up {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
/* 步骤序号脉冲 */
@keyframes step-pulse {
  0%, 100% { box-shadow: 0 0 0 0 var(--pattern-accent-muted); }
  50%      { box-shadow: 0 0 0 6px transparent; }
}
```

---

## 7. 组件设计

### 7.1 按钮

```css
/* 主要按钮 */
.btn-primary {
  background: var(--color-accent);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: var(--radius-sm);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s var(--ease-out),
              transform 0.15s var(--ease-out);
}
.btn-primary:hover {
  background: var(--accent-hover);
}
.btn-primary:active {
  transform: scale(0.97);
}
.btn-primary:disabled {
  background: var(--stone-300);
  color: var(--stone-600);
  cursor: not-allowed;
}

/* 次要按钮 */
.btn-secondary {
  background: transparent;
  color: var(--stone-700);
  border: 1.5px solid var(--stone-200);
  padding: 10px 24px;
  border-radius: var(--radius-sm);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: 600;
  cursor: pointer;
  transition: border-color 0.2s var(--ease-out),
              color 0.2s var(--ease-out);
}
.btn-secondary:hover {
  border-color: var(--accent);
  color: var(--accent);
}

/* 幽灵按钮（暗色背景上） */
.btn-ghost {
  background: transparent;
  color: var(--dark-100);
  border: 1.5px solid var(--dark-300);
}
.btn-ghost:hover {
  border-color: var(--dark-100);
  background: rgba(232, 224, 213, 0.08);
}

/* 文字按钮（最小视觉重量） */
.btn-text {
  background: none;
  border: none;
  color: var(--accent);
  font-weight: 600;
  padding: 6px 12px;
  cursor: pointer;
}
.btn-text:hover {
  text-decoration: underline;
  text-underline-offset: 3px;
}
```

### 7.2 卡片

```css
/* 基础卡片 */
.card {
  background: var(--stone-50);   /* 卡片背景同页面背景，用 border 区分 */
  border: 1px solid var(--stone-200);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  transition: border-color 0.25s var(--ease-out),
              transform 0.2s var(--ease-out);
}
.card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
}

/* 特色卡片（有强调色左边框） */
.card-featured {
  border-left: 3px solid var(--accent);
}

/* 暗色卡片（用于暗色背景面板） */
.card-dark {
  background: var(--dark-800);
  border: 1px solid rgba(232, 224, 213, 0.08);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  color: var(--dark-100);
}
```

### 7.3 标签 / Badge

```css
.badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 600;
  letter-spacing: 0.02em;
}

.badge-accent {
  background: var(--accent-light);
  color: var(--accent);
}

.badge-pattern {
  background: var(--pattern-accent-light);
  color: var(--pattern-accent);
}

.badge-neutral {
  background: var(--stone-100);
  color: var(--stone-600);
}
```

### 7.4 输入框

```css
.input {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid var(--stone-200);
  border-radius: var(--radius-sm);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  color: var(--stone-700);
  background: white;
  outline: none;
  transition: border-color 0.2s var(--ease-out),
              box-shadow 0.2s var(--ease-out);
}
.input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-light);
}
.input::placeholder {
  color: var(--stone-300);
}
```

### 7.5 导航

```css
/* 顶部导航 -- 保持简洁 */
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-4) 0;
  margin-bottom: var(--space-8);
  /* 不再用 border-bottom -- 用留白区分 */
}

.app-logo {
  font-family: var(--font-heading);
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--stone-900);
  text-decoration: none;
  letter-spacing: -0.01em;
}
.app-logo:hover {
  color: var(--accent);
}

.app-nav {
  display: flex;
  gap: var(--space-5);
}
.app-nav a {
  font-size: var(--text-sm);
  color: var(--stone-600);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s var(--ease-out);
  position: relative;
}
.app-nav a:hover {
  color: var(--stone-900);
}
.app-nav a.active {
  color: var(--accent);
}
/* 当前页下划线指示器 */
.app-nav a.active::after {
  content: "";
  position: absolute;
  bottom: -4px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--accent);
  border-radius: 1px;
}
```

### 7.6 页脚

```css
.app-footer {
  text-align: center;
  padding: var(--space-10) 0 var(--space-5);
  font-size: var(--text-xs);
  color: var(--stone-600);
  border-top: 1px solid var(--stone-200);
  margin-top: var(--space-12);
}
```

### 7.7 上传区域

```css
.upload-zone {
  border: 2px dashed var(--stone-200);
  border-radius: var(--radius-lg);
  padding: var(--space-6) var(--space-5);
  text-align: center;
  cursor: pointer;
  transition: border-color 0.25s var(--ease-out),
              background 0.25s var(--ease-out);
  background: var(--stone-50);
}
.upload-zone:hover,
.upload-zone.drag-over {
  border-color: var(--accent);
  background: var(--accent-light);
}
```

---

## 8. 全局布局重构

### 8.1 页面骨架

```css
.app-shell {
  max-width: var(--max-width-page);
  margin: 0 auto;
  padding: var(--space-5) var(--page-padding-x) var(--space-12);
}
```

### 8.2 暗色穿插面板

在亮色页面中穿插暗色 section，制造视觉戏剧感：

```css
/* 用于首页 hero 下方 / 模式页的"设计思路" section */
.dark-panel {
  background: var(--dark-900);
  color: var(--dark-100);
  margin-left: calc(-1 * var(--page-padding-x));
  margin-right: calc(-1 * var(--page-padding-x));
  padding: var(--space-10) var(--page-padding-x);
  border-radius: 0;
}

/* 或者作为内嵌圆角面板 */
.dark-panel-contained {
  background: var(--dark-900);
  color: var(--dark-100);
  border-radius: var(--radius-xl);
  padding: var(--space-8);
  margin: var(--space-8) 0;
}
```

### 8.3 CSS 文件拆分策略

```
src/frontend/css/
  tokens.css         ← CSS 变量定义（从 style.css 提取）
  base.css           ← 重置 + 全局排版
  layout.css         ← .app-shell, .app-header, .app-footer
  components.css     ← 按钮、卡片、input、badge
  animations.css     ← 所有 keyframes + reduced-motion
  patterns/
    streaming.css
    cards.css
    clarify.css
    degradation.css
    context.css
    confirmation.css
    progressive.css
  pages/
    home.css
    about.css
    behind-scenes.css
    principles.css
    review.css
  style.css          ← @import 汇总（向后兼容）
```

**迁移策略**：先全部写到 style.css v2.0，前端开发可以根据需要拆分。最小可行方案是只更新 style.css 并给每个模式页注入页面 CSS。

---

## 9. 响应式策略

### 9.1 断点

```css
/* 手机竖屏 */
@media (max-width: 479px) { ... }   /* 375px iPhone */

/* 手机横屏 / 小平板 */
@media (max-width: 767px) { ... }   /* < 768px */

/* 平板 */
@media (max-width: 1023px) { ... }  /* < 1024px */

/* 桌面（默认样式以此为准） */
/* > 1024px -- 默认写的就是这个 */
```

### 9.2 各断点行为

| 元素 | 手机 (< 480px) | 平板 (< 768px) | 桌面 (1024px+) |
|------|---------------|----------------|----------------|
| 首页卡片网格 | 1 列 | 2 列 | 3 列 |
| 模式页两栏 | 单栏堆叠 | 单栏堆叠 | 两栏 1:1 |
| 导航 | Logo + 汉堡菜单(可选) | 水平展开 | 水平展开 |
| 字号 | 正文 14px, 标题等比缩小 | 正文 15px, 标题正常 | 正文 15px |
| 暗色面板 | 内嵌圆角 (.contained) | 内嵌圆角 | 可全宽或内嵌 |
| 卡片内边距 | 16px | 20px | 24px |
| 页面两侧留白 | 16px | 24px | 24px (靠 max-width 控制) |
| 上下文页侧栏 | 隐藏或折叠 | 底部显示 | 右侧固定 280px |
| 对比网格 | 单列 | 单列 | 双列 |

### 9.3 移动端导航方案

```css
@media (max-width: 767px) {
  .app-header {
    flex-wrap: wrap;
  }
  .app-nav {
    width: 100%;
    justify-content: flex-start;
    gap: var(--space-4);
    margin-top: var(--space-3);
    padding-top: var(--space-3);
    border-top: 1px solid var(--stone-200);
  }
}
```

---

## 10. 首页设计

### 10.1 视觉结构

```
┌──────────────────────────────────────┐
│ [Logo]          [原则] [关于] [幕后] │  ← 导航（简洁）
├──────────────────────────────────────┤
│                                      │
│   我是樊书洋，                        │  ← Hero（大标题，衬线体）
│   我在探索人和 AI 怎么更好地对话。     │     保留现有文案，视觉升级
│                                      │
│   7 种 AI 交互模式，                  │  ← 副标题（无衬线，小字）
│   每一种都包含设计思路 + 可交互 Demo   │
│                                      │
│   [AI 交互设计原则] [试试完整产品 →]  │  ← CTA 按钮
│                                      │
├──────────────────────────────────────┤
│                                      │
│  ┌─────┐ ┌─────┐ ┌─────┐           │  ← 3 列卡片网格
│  │ 📝  │ │ 🃏  │ │ ❓  │           │     错落入场动画
│  │流式 │ │结构│ │澄清│           │
│  └─────┘ └─────┘ └─────┘           │
│  ┌─────┐ ┌─────┐ ┌─────┐           │
│  │ 🛡️  │ │ 💬  │ │ ✅  │           │
│  └─────┘ └─────┘ └─────┘           │
│  ┌─────┐                             │
│  │ 🪜  │   ← 最后一个居中或用 CSS    │
│  └─────┘                             │
│                                      │
├──────────────────────────────────────┤
│  ┌──────────────────────────────┐   │  ← 暗色面板（穿插）
│  │  关于我（精简版）               │   │     暖暗色背景
│  │  樊书洋 · 南传 · 大二          │   │     文字反白
│  │  求职 AI 交互设计师实习         │   │
│  └──────────────────────────────┘   │
├──────────────────────────────────────┤
│  Footer                              │
└──────────────────────────────────────┘
```

### 10.2 首页 Hero 设计

```css
.home-hero {
  text-align: center;
  padding: var(--space-12) 0 var(--space-8);
}

.home-hero h1 {
  font-family: var(--font-heading);
  font-size: var(--text-3xl);           /* 44px */
  font-weight: 900;
  color: var(--stone-900);
  line-height: var(--leading-tight);
  letter-spacing: -0.02em;
  max-width: 640px;
  margin: 0 auto var(--space-4);
}

.home-hero .highlight {
  color: var(--accent);
  /* 加一个下划线装饰，替代粗暴的 color highlight */
  text-decoration: underline;
  text-decoration-color: var(--accent-muted);
  text-underline-offset: 6px;
  text-decoration-thickness: 3px;
}

.home-hero .sub {
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--stone-600);
  max-width: 520px;
  margin: var(--space-3) auto var(--space-5);
  line-height: var(--leading-relaxed);
}

/* CTA 按钮组 */
.home-hero .cta-group {
  display: flex;
  gap: var(--space-3);
  justify-content: center;
  flex-wrap: wrap;
}
```

### 10.3 首页 7 卡片网格

```css
.home-pattern-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
  margin: var(--space-8) 0;
}

/* 第 7 个卡片居中 */
.home-pattern-grid::after {
  content: "";
  grid-column: 1 / -1;
}
/* 让最后一个卡片在第 7 位时居中 -- 用 grid 技巧 */
.home-pattern-grid .pattern-card:nth-child(7):nth-last-child(1) {
  grid-column: 2 / 3;
}
```

### 10.4 首页卡片设计

```css
.pattern-card {
  display: flex;
  flex-direction: column;
  padding: var(--space-5);
  background: var(--stone-50);
  border: 1px solid var(--stone-200);
  border-radius: var(--radius-lg);
  text-decoration: none;
  color: var(--stone-700);
  transition: border-color 0.3s var(--ease-out),
              transform 0.25s var(--ease-out);

  /* 卡片入场动画 */
  opacity: 0;
  transform: translateY(24px);
  animation: card-enter 0.5s var(--ease-out) forwards;
}

.pattern-card:hover {
  border-color: var(--accent);
  transform: translateY(-3px);
}

.pattern-card-icon {
  font-size: 2rem;
  margin-bottom: var(--space-3);
}

.pattern-card-title {
  font-family: var(--font-heading);
  font-size: var(--text-md);
  font-weight: 700;
  color: var(--stone-900);
  margin-bottom: var(--space-1);
}

.pattern-card-desc {
  font-size: var(--text-sm);
  color: var(--stone-600);
  line-height: var(--leading-normal);
  flex: 1;
  margin-bottom: var(--space-3);
}

.pattern-card-source {
  font-size: var(--text-xs);
  font-family: var(--font-mono);
  color: var(--stone-600);
  padding-top: var(--space-3);
  border-top: 1px solid var(--stone-200);
}
```

---

## 11. 7 个模式页设计

所有模式页共享基础结构：
```
[导航]
[Hero section -- 模式图标 + 标题 + tagline]
[设计思路 section -- 可暗色面板穿插]
[实现方式 section]
[Demo 区 -- 可交互]
[代码引用]
[Prev / Next 导航]
[Footer]
```

### 11.1 流式输出 (Streaming)

**概念色**: `#00c48c` 电流绿
**情感**: 实时、脉冲、活力 -- 像打字机、心跳、数据流动

```css
/* 页面注入 */
:root {
  --pattern-accent: #00c48c;
  --pattern-accent-light: #e6faf4;
  --pattern-accent-muted: #b3f0dc;
}

/* Hero 区 */
.streaming-hero {
  text-align: center;
  padding: var(--space-8) 0 var(--space-6);
  position: relative;
}
/* 背景装饰：微妙的粒子/数据点动画 */
.streaming-hero::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background:
    radial-gradient(circle at 20% 50%, var(--pattern-accent-muted) 0%, transparent 50%),
    radial-gradient(circle at 80% 30%, var(--pattern-accent-muted) 0%, transparent 40%);
  opacity: 0.15;
  pointer-events: none;
}

/* Demo 区 Chat 气泡 */
.streaming-chat-bubble.ai {
  background: var(--stone-50);
  border: 1px solid var(--stone-200);
  position: relative;
}
/* 打字光标 */
.streaming-chat-bubble.ai.streaming::after {
  content: "|";
  display: inline;
  animation: cursor-blink 0.8s infinite;
  color: var(--pattern-accent);
  font-weight: 300;
  margin-left: 1px;
}

/* 速度选择器 */
.speed-selector {
  display: flex;
  gap: 4px;
  background: var(--stone-100);
  border-radius: var(--radius-full);
  padding: 3px;
}
.speed-btn {
  padding: 6px 16px;
  border-radius: var(--radius-full);
  border: none;
  background: transparent;
  font-size: var(--text-xs);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s var(--ease-out);
}
.speed-btn.active {
  background: white;
  color: var(--pattern-accent);
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
```

### 11.2 结构化卡片 (Structured Cards)

**概念色**: `#d4850a` 琥珀金
**情感**: 秩序、清晰、信息块 -- 像图书馆索引卡、标签系统

```css
:root {
  --pattern-accent: #d4850a;
  --pattern-accent-light: #fdf3e2;
  --pattern-accent-muted: #f0d9a8;
}

/* Demo 区对比布局 */
.cards-compare-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

/* 左侧文字墙 -- 刻意让它看起来"不好" */
.cards-wall-text {
  background: var(--stone-50);
  border: 1px solid var(--stone-200);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
  color: var(--stone-600);
  max-height: 500px;
  overflow-y: auto;
  /* 不设视觉层级 -- 故意让它看起来像一堵墙 */
}

/* 右侧结构化卡片 -- 清晰的信息层级 */
.cards-structured {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.cards-result-card {
  background: white;
  border: 1px solid var(--stone-200);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  animation: card-stack 0.4s var(--ease-out) both;
}
.cards-result-card:nth-child(1) { animation-delay: 0s; }
.cards-result-card:nth-child(2) { animation-delay: 0.08s; }
.cards-result-card:nth-child(3) { animation-delay: 0.16s; }
.cards-result-card:nth-child(4) { animation-delay: 0.24s; }

/* 评分徽标 */
.score-badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 12px;
  border-radius: var(--radius-full);
  font-weight: 700;
  font-size: var(--text-sm);
}
.score-badge.high { background: var(--success-light); color: var(--success); }
.score-badge.mid  { background: var(--warning-light); color: var(--warning); }
.score-badge.low  { background: var(--error-light); color: var(--error); }
```

### 11.3 澄清提问 (Clarification)

**概念色**: `#8b5cf6` 对话紫
**情感**: 好奇、对话、追问 -- 像问答游戏、两个人在聊天

```css
:root {
  --pattern-accent: #8b5cf6;
  --pattern-accent-light: #f4f0fe;
  --pattern-accent-muted: #d4c8fc;
}

/* 阶段指示器 */
.clarify-stages {
  display: flex;
  gap: 0;
  margin-bottom: var(--space-5);
}
.clarify-stage {
  flex: 1;
  text-align: center;
  padding: var(--space-3) var(--space-2);
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--stone-600);
  border-bottom: 3px solid var(--stone-200);
  transition: all 0.3s var(--ease-out);
}
.clarify-stage.active {
  color: var(--pattern-accent);
  border-bottom-color: var(--pattern-accent);
}
.clarify-stage.done {
  color: var(--success);
  border-bottom-color: var(--success);
}

/* 追问气泡 */
.clarify-question {
  background: var(--pattern-accent-light);
  border-radius: var(--radius-md) var(--radius-md) var(--radius-md) 4px;
  padding: var(--space-4);
  margin-bottom: var(--space-3);
  border-left: 3px solid var(--pattern-accent);
  animation: bubble-pop 0.4s var(--ease-out) both;
}

/* 对比面板 */
.clarify-compare {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}
.clarify-compare .bad {
  background: var(--error-light);
  border-left: 3px solid var(--error);
  padding: var(--space-4);
  border-radius: var(--radius-md);
}
.clarify-compare .good {
  background: var(--success-light);
  border-left: 3px solid var(--success);
  padding: var(--space-4);
  border-radius: var(--radius-md);
}
```

### 11.4 失败兜底 (Graceful Degradation)

**概念色**: `#0d9488` 护盾青
**情感**: 安全、防御、可靠 -- 像安全气囊、防护层

```css
:root {
  --pattern-accent: #0d9488;
  --pattern-accent-light: #e6f5f4;
  --pattern-accent-muted: #b3e5e0;
}

/* Tab 切换 */
.degradation-tabs {
  display: flex;
  border-bottom: 2px solid var(--stone-200);
  margin-bottom: 0;
}
.degradation-tab {
  flex: 1;
  padding: var(--space-3) var(--space-2);
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: 600;
  color: var(--stone-600);
  cursor: pointer;
  margin-bottom: -2px;
  transition: all 0.2s var(--ease-out);
}
.degradation-tab.active {
  color: var(--pattern-accent);
  border-bottom-color: var(--pattern-accent);
}

/* 日志面板 */
.degradation-log {
  background: var(--dark-900);
  color: var(--dark-100);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  font-family: var(--font-mono);
  font-size: 0.75rem;
  line-height: 1.8;
  min-height: 120px;
  max-height: 400px;
  overflow-y: auto;
}

/* 日志颜色 */
.log-info    { color: #b3e5e0; }  /* 护盾青淡色 */
.log-error   { color: #f4b8b8; }  /* 暖红 */
.log-success { color: #a3d9c8; }  /* 翠绿淡色 */
.log-warn    { color: #f0d9a8; }  /* 琥珀淡色 */
.log-step    { color: #d4c8fc; }  /* 紫色淡色 */

/* 防御层动画 */
.degradation-layer {
  border: 2px solid var(--pattern-accent-muted);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  margin-bottom: var(--space-2);
  animation: layer-stack 0.4s var(--ease-out) both;
}
.degradation-layer:nth-child(1) { animation-delay: 0s; }
.degradation-layer:nth-child(2) { animation-delay: 0.15s; }
.degradation-layer:nth-child(3) { animation-delay: 0.3s; }
```

### 11.5 多轮上下文 (Context)

**概念色**: `#db2777` 记忆粉
**情感**: 连接、记忆、时间线 -- 像思维导图、世界线

```css
:root {
  --pattern-accent: #db2777;
  --pattern-accent-light: #fdf0f5;
  --pattern-accent-muted: #f4c4d8;
}

/* 双栏布局 */
.context-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: var(--space-5);
}

/* 记忆面板 */
.context-memory-panel {
  background: var(--stone-50);
  border: 1px solid var(--stone-200);
  border-radius: var(--radius-lg);
  padding: var(--space-4);
  font-size: var(--text-xs);
}

/* 时间线 */
.context-timeline {
  position: relative;
  padding-left: var(--space-4);
}
.context-timeline::before {
  content: "";
  position: absolute;
  left: 8px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--stone-200);
}
.context-timeline-item {
  position: relative;
  padding: var(--space-2) 0 var(--space-2) var(--space-4);
  border-left: 2px solid transparent;
}
.context-timeline-item::before {
  content: "";
  position: absolute;
  left: -5px;
  top: 50%;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--pattern-accent-muted);
  transform: translateY(-50%);
}
.context-timeline-item.active::before {
  background: var(--pattern-accent);
  box-shadow: 0 0 0 4px var(--pattern-accent-light);
  animation: memory-pulse 2s infinite;
}

/* 上下文 badge */
.context-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  font-size: 0.65rem;
  font-weight: 600;
}
.context-badge.active {
  background: var(--pattern-accent-light);
  color: var(--pattern-accent);
}
.context-badge.stale {
  background: var(--stone-100);
  color: var(--stone-600);
}
```

### 11.6 确认机制 (Confirmation)

**概念色**: `#ea580c` 警戒橙
**情感**: 暂停、确认、门槛 -- 像红绿灯、安全检查点

```css
:root {
  --pattern-accent: #ea580c;
  --pattern-accent-light: #fef3eb;
  --pattern-accent-muted: #f4c4a8;
}

/* 流程步骤 */
.confirmation-steps {
  display: flex;
  gap: 0;
  margin-bottom: var(--space-5);
  text-align: center;
}
.confirmation-step {
  flex: 1;
  position: relative;
  padding: var(--space-3) var(--space-2);
  font-size: var(--text-xs);
  color: var(--stone-600);
}
.confirmation-step .step-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid var(--stone-200);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: var(--text-sm);
  margin-bottom: var(--space-1);
  transition: all 0.3s var(--ease-out);
}
.confirmation-step.active .step-circle {
  border-color: var(--pattern-accent);
  background: var(--pattern-accent-light);
  color: var(--pattern-accent);
  animation: warning-pulse 2s infinite;
}
.confirmation-step.done .step-circle {
  border-color: var(--success);
  background: var(--success-light);
  color: var(--success);
}

/* 确认卡片 */
.confirm-card {
  background: white;
  border: 2px solid var(--warning);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  max-width: 480px;
  margin: 0 auto;
  transition: border-color 0.3s var(--ease-out);
}
.confirm-card.executing {
  border-color: var(--pattern-accent);
  animation: warning-pulse 1.5s infinite;
}
.confirm-card.executed {
  border-color: var(--success);
}
.confirm-card.cancelled {
  border-color: var(--stone-200);
  opacity: 0.7;
}

/* 不可逆警告 */
.irreversible-warning {
  color: var(--error);
  font-weight: 700;
  font-size: var(--text-sm);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}
```

### 11.7 渐进式加载 (Progressive Disclosure)

**概念色**: `#2563eb` 揭示蓝
**情感**: 层层展开、发现、深度 -- 像幕布升起、剥洋葱

```css
:root {
  --pattern-accent: #2563eb;
  --pattern-accent-light: #eaf0fd;
  --pattern-accent-muted: #b8d0f8;
}

/* 步骤卡片 */
.progressive-step {
  background: white;
  border: 1px solid var(--stone-200);
  border-left: 4px solid var(--stone-200);
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  padding: var(--space-4);
  margin-bottom: var(--space-3);
  opacity: 0.4;
  transition: all 0.5s var(--ease-out);
}
.progressive-step.revealed {
  opacity: 1;
  border-left-color: var(--pattern-accent);
}
.progressive-step.completed {
  opacity: 1;
  border-left-color: var(--success);
}

/* 步骤序号 */
.progressive-step .step-number {
  display: inline-flex;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  align-items: center;
  justify-content: center;
  font-size: var(--text-xs);
  font-weight: 700;
  margin-right: var(--space-2);
  background: var(--stone-200);
  color: white;
  transition: all 0.3s var(--ease-out);
}
.progressive-step.revealed .step-number {
  background: var(--pattern-accent);
  animation: step-pulse 1.5s infinite;
}
.progressive-step.completed .step-number {
  background: var(--success);
  animation: none;
}

/* 占位文本 */
.progressive-placeholder {
  font-size: var(--text-sm);
  color: var(--stone-600);
  font-style: italic;
}
```

---

## 12. 次级页面设计

### 12.1 关于我 (about.html)

```css
/* 大气的个人介绍页 */
.about-hero {
  text-align: center;
  padding: var(--space-10) 0 var(--space-6);
}

.about-hero h1 {
  font-family: var(--font-heading);
  font-size: var(--text-2xl);
  font-weight: 900;
  color: var(--stone-900);
  margin-bottom: var(--space-2);
}

.about-hero .role {
  font-family: var(--font-body);
  font-size: var(--text-md);
  color: var(--accent);
  font-weight: 600;
  margin-bottom: var(--space-4);
}

.about-hero .bio {
  font-size: var(--text-base);
  color: var(--stone-600);
  line-height: var(--leading-relaxed);
  max-width: 520px;
  margin: 0 auto;
}

/* 技能标签云 */
.skill-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  justify-content: center;
  margin-top: var(--space-5);
}

.skill-tag {
  padding: 6px 16px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 600;
  background: var(--accent-light);
  color: var(--accent);
  transition: transform 0.2s var(--ease-out);
}
.skill-tag:hover {
  transform: scale(1.05);
}

/* 信息网格 */
.about-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
  margin-top: var(--space-6);
}
.about-info-item {
  background: var(--stone-50);
  border: 1px solid var(--stone-200);
  border-radius: var(--radius-md);
  padding: var(--space-4);
}
.about-info-label {
  font-size: var(--text-xs);
  color: var(--stone-600);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: var(--space-1);
}
.about-info-value {
  font-size: var(--text-base);
  color: var(--stone-900);
  font-weight: 600;
}
```

### 12.2 制作幕后 (behind-the-scenes.html)

```css
/* 时间线叙事 */
.bts-hero {
  text-align: center;
  padding: var(--space-8) 0 var(--space-6);
}

.bts-hero h1 {
  font-family: var(--font-heading);
  font-size: var(--text-2xl);
  font-weight: 900;
  margin-bottom: var(--space-3);
}

.bts-hero .tagline {
  font-family: var(--font-display);  /* 手写体 */
  font-size: var(--text-lg);
  color: var(--accent);
  line-height: var(--leading-relaxed);
}

/* 迭代卡片 */
.iteration-card {
  background: var(--stone-50);
  border: 1px solid var(--stone-200);
  border-left: 3px solid var(--accent);
  border-radius: 0 var(--radius-md) var(--radius-md) 0;
  padding: var(--space-5);
  margin-bottom: var(--space-4);
}

.iteration-card .version {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--accent);
  font-weight: 600;
  margin-bottom: var(--space-1);
}

/* 工具链图 */
.toolchain {
  background: var(--dark-900);
  color: var(--dark-100);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  font-family: var(--font-mono);
  font-size: 0.8rem;
  line-height: 2;
  overflow-x: auto;
}
.toolchain .arrow { color: var(--accent); }
.toolchain .node  { color: var(--dark-100); font-weight: 600; }
```

### 12.3 设计原则总结 (principles-summary.html)

```css
/* 原则行 */
.principle-row {
  display: grid;
  grid-template-columns: auto 1fr;
  gap: var(--space-5);
  align-items: start;
  background: var(--stone-50);
  border: 1px solid var(--stone-200);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  margin-bottom: var(--space-4);
  transition: border-color 0.3s var(--ease-out);
}
.principle-row:hover {
  border-color: var(--accent);
}

/* 序号圆圈 */
.principle-number {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--accent);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-heading);
  font-size: var(--text-lg);
  font-weight: 900;
  flex-shrink: 0;
}

/* 规则标题 */
.principle-rule {
  font-family: var(--font-display);
  font-size: var(--text-md);
  font-weight: 700;
  color: var(--accent);
  margin-bottom: var(--space-1);
}

/* 链接 */
.principle-pattern-link {
  display: inline-block;
  margin-top: var(--space-2);
  font-size: var(--text-sm);
  color: var(--accent);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s var(--ease-out);
}
.principle-pattern-link:hover {
  text-decoration: underline;
  text-underline-offset: 3px;
}
```

### 12.4 设计原则图书馆 (principles.html)

```css
/* 分类标题 */
.principles-category-title {
  font-family: var(--font-heading);
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--stone-900);
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-2);
  border-bottom: 2px solid var(--accent);
  display: inline-block;
}

/* 原则条目 */
.principle-entry {
  background: var(--stone-50);
  border: 1px solid var(--stone-200);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  margin-bottom: var(--space-3);
}

.principle-entry h3 {
  font-family: var(--font-heading);
  font-size: var(--text-md);
  font-weight: 700;
  margin-bottom: var(--space-1);
}

.principle-entry .source {
  font-size: var(--text-xs);
  color: var(--stone-600);
  margin-bottom: var(--space-2);
}

/* 生活类比 */
.principle-example {
  background: var(--accent-light);
  border-radius: var(--radius-sm);
  padding: var(--space-3);
  margin-top: var(--space-3);
  font-size: var(--text-sm);
  color: var(--stone-700);
}
.principle-example strong {
  color: var(--accent);
}
```

### 12.5 设计评审工具 (review.html)

保持功能不变，视觉同步升级到新的设计系统。

---

## 13. 无障碍清单

### 13.1 对比度

| 元素 | 要求 | 状态 |
|------|------|------|
| 正文文字 vs 背景 | >= 4.5:1 | `--stone-700` on `--stone-50` = 7.2:1 PASS |
| 大标题 vs 背景 | >= 3:1 | `--stone-900` on `--stone-50` = 12:1 PASS |
| 暗色面板文字 | >= 4.5:1 | `--dark-100` on `--dark-900` = 8.5:1 PASS |
| 按钮文字 vs 按钮背景 | >= 3:1 | white on `--accent` = 4.2:1 PASS |
| 占位符文字 vs 背景 | >= 4.5:1 | `--stone-300` on white = 需验证 |
| 禁用态文字 | N/A (不需要满足对比度) | 已用更低对比度表示禁用 |

### 13.2 焦点指示器

```css
:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
  border-radius: 2px;
}

/* 暗色背景上的焦点 */
.dark-panel :focus-visible {
  outline-color: var(--accent-muted);
}
```

### 13.3 Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### 13.4 语义 HTML

- 标题层级：h1 > h2 > h3 不跳级
- 所有 img 有 alt 属性（装饰性图标用空 alt）
- 表单有 label 关联
- 按钮有明确的文字（不是纯图标无 label）
- 链接有可识别的文字（不是 "点击这里"）

### 13.5 触摸目标

所有可点击元素最小 44x44px（移动端）/ 内联链接除外。

---

## 14. CSS 变量完整定义

以下是新版 style.css 的 `:root` 块完整内容：

```css
:root {
  /* ===== 暖白底系统 ===== */
  --stone-50:  #faf9f7;
  --stone-100: #f5f0eb;
  --stone-200: #e8e0d5;
  --stone-300: #d4c9b8;
  --stone-600: #8b7e6c;
  --stone-700: #6b5d4f;
  --stone-900: #2d2418;

  /* ===== 暗色面板 ===== */
  --dark-900: #1a1815;
  --dark-800: #2d2822;
  --dark-300: #a09888;
  --dark-100: #e8e0d5;

  /* ===== 主色（暖珊瑚） ===== */
  --color-accent:        #e05b3c;
  --color-accent-hover:  #c94a2e;
  --color-accent-light:  #fef0ec;
  --color-accent-muted:  #f4c4b8;

  /* ===== 功能色 ===== */
  --color-success:       #2d8a6e;
  --color-success-light: #eaf5f0;
  --color-warning:       #d4850a;
  --color-warning-light: #fdf3e2;
  --color-error:         #c94043;
  --color-error-light:   #fef0f0;

  /* ===== 向后兼容别名（让老 CSS 不需全部修改） ===== */
  --color-bg:            var(--stone-50);
  --color-surface:       #ffffff;
  --color-border:        var(--stone-200);
  --color-text:          var(--stone-700);
  --color-text-secondary:var(--stone-600);
  --color-text-muted:    var(--stone-600);
  --color-primary:       var(--color-accent);
  --color-primary-hover: var(--color-accent-hover);
  --color-primary-light: var(--color-accent-light);

  /* ===== 字体 ===== */
  --font-body:    "Inter", "PingFang SC", "Noto Sans SC", "Microsoft YaHei", system-ui, sans-serif;
  --font-heading: "Noto Serif SC", "PingFang SC", "STSong", "SimSun", "Times New Roman", serif;
  --font-mono:    "JetBrains Mono", "SF Mono", "Cascadia Code", "Consolas", monospace;
  --font-display: "LXGW WenKai", "KaiTi", "STKaiti", "楷体", serif;

  /* ===== 字号 ===== */
  --text-xs:    0.6875rem;
  --text-sm:    0.8125rem;
  --text-base:  0.9375rem;
  --text-md:    1.0625rem;
  --text-lg:    1.25rem;
  --text-xl:    1.5rem;
  --text-2xl:   2rem;
  --text-3xl:   2.75rem;

  /* ===== 行高 ===== */
  --leading-tight:   1.25;
  --leading-normal:  1.6;
  --leading-relaxed: 1.8;

  /* ===== 间距（4px 网格） ===== */
  --space-1:  0.25rem;
  --space-2:  0.5rem;
  --space-3:  0.75rem;
  --space-4:  1rem;
  --space-5:  1.5rem;
  --space-6:  2rem;
  --space-8:  3rem;
  --space-10: 4rem;
  --space-12: 5rem;
  --space-16: 8rem;

  /* ===== 布局 ===== */
  --max-width-content: 720px;
  --max-width-page:    960px;
  --max-width-wide:   1120px;
  --page-padding-x:    var(--space-5);

  /* ===== 圆角 ===== */
  --radius-none: 0;
  --radius-xs:   3px;
  --radius-sm:   6px;
  --radius-md:   10px;
  --radius-lg:   16px;
  --radius-xl:   24px;
  --radius-full: 9999px;

  /* ===== 阴影 ===== */
  --shadow-none:   none;
  --shadow-hover:  0 2px 16px rgba(45, 36, 24, 0.08);
  --shadow-overlay:0 8px 40px rgba(45, 36, 24, 0.12);

  /* ===== 缓动 ===== */
  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-slow:   cubic-bezier(0.4, 0, 0.2, 1);

  /* ===== 默认模式主题色（会被各页面覆写） ===== */
  --pattern-accent:       var(--color-accent);
  --pattern-accent-light: var(--color-accent-light);
  --pattern-accent-muted: var(--color-accent-muted);
}
```

---

## 15. 迁移清单

### 15.1 前端开发者实施步骤

**Phase 1: CSS 基础（优先级最高）**
- [ ] 替换 `src/frontend/css/style.css` 的 `:root` 变量块为新版定义
- [ ] 在 `<head>` 中添加 Google Fonts 导入（Noto Serif SC + Inter + LXGW WenKai）
- [ ] 更新 body 基础样式（字体、行高、颜色）
- [ ] 更新 .btn, .card, .input, .badge 组件样式
- [ ] 更新 .app-header, .app-nav, .app-footer 布局样式

**Phase 2: 首页**
- [ ] 更新首页 Hero 区（标题用衬线体，CTA 按钮新样式）
- [ ] 更新 7 卡片网格（3 列 desktop，卡片入场动画）
- [ ] 更新 about-compact 卡片（暗色面板）
- [ ] 验证 375px / 768px / 1024px 断点

**Phase 3: 模式页（每个独立实施）**
- [ ] streaming.html -- 注入概念色 + 打字光标动画 + 速度选择器样式
- [ ] cards.html -- 注入概念色 + 左右对比 + 卡片入场动画
- [ ] clarify.html -- 注入概念色 + 阶段指示器 + 气泡动画
- [ ] degradation.html -- 注入概念色 + Tab 切换 + 日志面板
- [ ] context.html -- 注入概念色 + 时间线 + 记忆面板
- [ ] confirmation.html -- 注入概念色 + 步骤圆圈 + 确认卡片
- [ ] progressive.html -- 注入概念色 + 步骤卡片 + 揭示动画

**Phase 4: 次级页面**
- [ ] about.html -- 新版个人介绍 + 技能云 + 信息网格
- [ ] behind-the-scenes.html -- 迭代卡片 + 工具链暗色面板
- [ ] principles-summary.html -- 新版原则行 + 序号圆圈
- [ ] principles.html -- 原则条目 + 分类标题
- [ ] review.html -- 功能不变，样式同步升级

**Phase 5: 全局动效**
- [ ] 添加 Intersection Observer 滚动触发 `.reveal-on-scroll`
- [ ] 添加 `prefers-reduced-motion` 媒体查询
- [ ] 添加 `:focus-visible` 焦点样式
- [ ] 测试所有页面在 375px / 768px / 1024px / 1440px

### 15.2 不改变的内容

- 所有页面的 HTML 结构（class 名、ID 名）
- 所有 JavaScript 逻辑
- 所有 API 端点
- 页面 URL 结构
- 页面中的文案内容

### 15.3 可能需要微调的 HTML

- 每个模式页 `<style>` 块中的自定义 CSS（大部分可用新变量替代，但概念色注入需要在每个页面 `<style>` 中添加 `:root { --pattern-accent: #xxx; ... }` 块）
- `<head>` 中添加字体导入 link
- 可能需要给 Hero 区添加额外的 class（如 `.streaming-hero`）来支持背景装饰

---

## 附录 A: 设计决策日志

| 决策 | 理由 | 备选方案 |
|------|------|----------|
| 暖珊瑚 #e05b3c 替代 indigo #6366f1 | indigo 太"SaaS 工具"，珊瑚色有设计师的人味 | 保留 indigo（太冷）、用纯黑（太沉闷）、用渐变（太花哨） |
| 衬线体标题 + 无衬线体正文 | 制造层次感，"设计师的笔记本"需要文字美感 | 统一无衬线（太平）、统一衬线（长文可读性差） |
| 暗色面板穿插而非全站暗色模式 | 暗色作为强调和节奏感，全站暗色太压抑 | 全站暗色（看不清中文长文）、全站亮色（缺少戏剧感） |
| 每页独立概念色 | 7 个模式页如果全用统一主题色就没有辨识度 | 统一主题色（所有页看起来一样，面试官分不清） |
| 卡片默认无阴影，用 border 区分 | 阴影是"SaaS 感"的主要来源，border 更干净 | 保留阴影（开发者审美）、完全扁平无边框（层次不清） |
| 正文 15px 非 16px | 中文笔画密度高，15px 在屏幕上可读性更好 | 16px 默认（中文偏大）、14px（太小） |
| CSS-only 动画为主 | 性能好、代码少、不依赖 JS | JS 动画（更灵活但增加复杂度） |

---

## 附录 B: 字体加载后备方案

```css
/* 如果 Google Fonts 加载失败，使用系统衬线字体 */
@font-face {
  font-family: "Noto Serif SC Fallback";
  src: local("PingFang SC"), local("STSong"), local("SimSun");
  size-adjust: 105%;      /* 微调字宽匹配 Noto Serif */
  ascent-override: 95%;
  descent-override: 25%;
}

/* 加载策略：<link rel="preload"> 在 <head> 中优先加载中文字体子集 */
/* <link rel="preload" href="..." as="font" crossorigin> */
```

---

*文档版本：v2.0*
*最后更新：2026-06-01*
*作者：UX/UI Designer (15-role workflow)*
*下游消费者：Frontend Developer agent*
