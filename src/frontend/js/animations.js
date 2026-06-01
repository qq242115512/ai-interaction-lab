/**
 * AI 交互模式实验室 — GSAP 动画系统 v3
 *
 * 规则（经历了 CSS+GSAP 冲突的教训后）：
 *   1. 所有动效统一在 GSAP 一处控制，CSS 不定义入场动画
 *   2. 每个 gsap.from() 之前先 gsap.set({autoAlpha:1}) 保证元素永不可见
 *   3. 首屏直接播放，折叠线以下用 ScrollTrigger + once:true
 */
document.addEventListener("DOMContentLoaded", function () {
  if (typeof gsap === "undefined") return;
  gsap.registerPlugin(ScrollTrigger);

  var mm = gsap.matchMedia();

  /* ================================================================
     Hero 标题逐行淡入
     ================================================================ */
  var hero = document.querySelector(".hero-statement, .pattern-hero, .lab-hero");
  if (hero) {
    var kids = hero.children;
    gsap.set(kids, { autoAlpha: 1 });
    gsap.from(kids, {
      y: 24,
      autoAlpha: 0,
      duration: 0.6,
      stagger: 0.1,
      ease: "power3.out",
    });
  }

  /* ================================================================
     模式卡片 staggered 入场（首屏直接播放）
     ================================================================ */
  var cards = document.querySelectorAll(".pattern-card");
  if (cards.length) {
    gsap.set(cards, { autoAlpha: 1 });
    gsap.from(cards, {
      y: 40,
      autoAlpha: 0,
      duration: 0.5,
      stagger: 0.06,
      delay: 0.15,
      ease: "power2.out",
    });
  }

  /* ================================================================
     about-card / about-compact 入场
     ================================================================ */
  var aboutCard = document.querySelector(".about-card");
  if (aboutCard) {
    gsap.set(aboutCard, { autoAlpha: 1 });
    gsap.from(aboutCard, {
      y: 30,
      autoAlpha: 0,
      duration: 0.5,
      ease: "power3.out",
    });
  }
  var aboutCompact = document.querySelector(".about-compact");
  if (aboutCompact) {
    gsap.set(aboutCompact, { autoAlpha: 1 });
    gsap.from(aboutCompact, {
      y: 30,
      autoAlpha: 0,
      duration: 0.6,
      delay: 0.3,
      ease: "power3.out",
    });
  }

  /* ================================================================
     折叠线以下：内容区逐节淡入
     ================================================================ */
  var sections = document.querySelectorAll(".pattern-section, .bts-section, .category-section");
  sections.forEach(function (sec) {
    gsap.set(sec, { autoAlpha: 1 });
    gsap.from(sec, {
      y: 30,
      autoAlpha: 0,
      duration: 0.5,
      ease: "power2.out",
      scrollTrigger: { trigger: sec, start: "top 82%", once: true },
    });
  });

  /* ================================================================
     原则条目 staggered
     ================================================================ */
  var entries = document.querySelectorAll(".principle-row, .principle-entry, .iteration-card");
  if (entries.length) {
    gsap.set(entries, { autoAlpha: 1 });
    gsap.from(entries, {
      y: 40,
      autoAlpha: 0,
      duration: 0.5,
      stagger: 0.06,
      ease: "power2.out",
      scrollTrigger: {
        trigger: entries[0].parentElement,
        start: "top 85%",
        once: true,
      },
    });
  }

  /* ================================================================
     principle-badge 弹性弹出
     ================================================================ */
  document.querySelectorAll(".pattern-section div").forEach(function (group) {
    var badges = group.querySelectorAll(".principle-badge");
    if (badges.length > 1) {
      gsap.set(badges, { autoAlpha: 1 });
      gsap.from(badges, {
        scale: 0,
        autoAlpha: 0,
        duration: 0.3,
        stagger: 0.08,
        ease: "back.out(1.7)",
        scrollTrigger: { trigger: group, start: "top 88%", once: true },
      });
    }
  });

  /* ================================================================
     skill-tags / info-item 弹入
     ================================================================ */
  var tags = document.querySelectorAll(".skill-tags .skill-tag");
  if (tags.length) {
    gsap.set(tags, { autoAlpha: 1 });
    gsap.from(tags, {
      scale: 0,
      autoAlpha: 0,
      duration: 0.3,
      stagger: 0.04,
      ease: "back.out(1.7)",
      scrollTrigger: { trigger: tags[0].parentElement, start: "top 90%", once: true },
    });
  }
  var infoItems = document.querySelectorAll(".info-item");
  if (infoItems.length) {
    gsap.set(infoItems, { autoAlpha: 1 });
    gsap.from(infoItems, {
      y: 40,
      autoAlpha: 0,
      duration: 0.5,
      stagger: 0.06,
      ease: "power2.out",
      scrollTrigger: { trigger: infoItems[0].parentElement, start: "top 85%", once: true },
    });
  }

  /* ================================================================
     demo-area 淡入
     ================================================================ */
  document.querySelectorAll(".demo-area").forEach(function (area) {
    gsap.set(area, { autoAlpha: 1 });
    gsap.from(area, {
      y: 20,
      autoAlpha: 0,
      duration: 0.4,
      ease: "power2.out",
      scrollTrigger: { trigger: area, start: "top 85%", once: true },
    });
  });

  /* ================================================================
     确认卡片弹性入场
     ================================================================ */
  var confirmCard = document.querySelector(".confirm-card");
  if (confirmCard) {
    gsap.set(confirmCard, { autoAlpha: 1 });
    gsap.from(confirmCard, {
      scale: 0.92,
      autoAlpha: 0,
      duration: 0.5,
      ease: "back.out(1.7)",
      scrollTrigger: { trigger: confirmCard, start: "top 85%", once: true },
    });
  }

  /* ================================================================
     加载完成后修正位置 + reduced-motion
     ================================================================ */
  ScrollTrigger.refresh();

  mm.add("(prefers-reduced-motion: reduce)", function () {
    gsap.globalTimeline.timeScale(0);
    return function () { gsap.globalTimeline.timeScale(1); };
  });
});
