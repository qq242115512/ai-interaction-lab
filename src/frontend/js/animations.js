/**
 * AI 交互模式实验室 — GSAP 动画系统 v4
 *
 * 设计语言：Indigo + Coral 新品牌色，Tailwind-first
 *
 * 规则：
 *   1. 所有入场动画由 GSAP 统一控制，CSS 只定义静态样式
 *   2. 每个 gsap.from() 前先 gsap.set() 确保初始可见性可控
 *   3. 首屏直接播放，折叠线以下用 ScrollTrigger + once: true
 *   4. 尊重 prefers-reduced-motion
 */
document.addEventListener("DOMContentLoaded", function () {
  if (typeof gsap === "undefined") return;
  gsap.registerPlugin(ScrollTrigger);

  var mm = gsap.matchMedia();

  /* ================================================================
     Nav bar — fade down from top
     ================================================================ */
  var navbar = document.getElementById("navbar");
  if (navbar) {
    gsap.set(navbar, { autoAlpha: 1 });
    gsap.from(navbar, {
      y: -20,
      autoAlpha: 0,
      duration: 0.55,
      ease: "power3.out",
    });
  }

  /* ================================================================
     Hero eyebrow — fade up
     ================================================================ */
  var heroEyebrow = document.getElementById("hero-eyebrow");
  if (heroEyebrow) {
    gsap.set(heroEyebrow, { autoAlpha: 1 });
    gsap.from(heroEyebrow, {
      y: 16,
      autoAlpha: 0,
      duration: 0.5,
      ease: "power3.out",
      delay: 0.12,
    });
  }

  /* ================================================================
     Hero title — fade up from 30px
     ================================================================ */
  var heroTitle = document.getElementById("hero-title");
  if (heroTitle) {
    gsap.set(heroTitle, { autoAlpha: 1 });
    gsap.from(heroTitle, {
      y: 30,
      autoAlpha: 0,
      duration: 0.65,
      ease: "power3.out",
      delay: 0.18,
    });
  }

  /* ================================================================
     Hero subtitle — fade up from 20px, delay 0.15s after title
     ================================================================ */
  var heroSubtitle = document.getElementById("hero-subtitle");
  if (heroSubtitle) {
    gsap.set(heroSubtitle, { autoAlpha: 1 });
    gsap.from(heroSubtitle, {
      y: 20,
      autoAlpha: 0,
      duration: 0.5,
      ease: "power3.out",
      delay: 0.33,
    });
  }

  /* ================================================================
     CTA buttons — fade up, stagger 0.1s
     ================================================================ */
  var heroCtas = document.getElementById("hero-ctas");
  if (heroCtas) {
    var ctaButtons = heroCtas.querySelectorAll("a");
    gsap.set(ctaButtons, { autoAlpha: 1 });
    gsap.from(ctaButtons, {
      y: 20,
      autoAlpha: 0,
      duration: 0.5,
      stagger: 0.1,
      delay: 0.42,
      ease: "power3.out",
    });
  }

  /* ================================================================
     Section title — decorative divider + heading fade up
     ================================================================ */
  var sectionDivider = document.getElementById("section-divider");
  var sectionHeading = document.getElementById("section-heading");

  if (sectionDivider) {
    gsap.set(sectionDivider, { autoAlpha: 1 });
    gsap.from(sectionDivider, {
      y: 20,
      autoAlpha: 0,
      duration: 0.55,
      ease: "power3.out",
      scrollTrigger: {
        trigger: sectionDivider,
        start: "top 85%",
        once: true,
      },
    });
  }

  if (sectionHeading) {
    gsap.set(sectionHeading, { autoAlpha: 1 });
    gsap.from(sectionHeading, {
      y: 20,
      autoAlpha: 0,
      duration: 0.55,
      delay: 0.1,
      ease: "power3.out",
      scrollTrigger: {
        trigger: sectionHeading,
        start: "top 85%",
        once: true,
      },
    });
  }

  /* ================================================================
     Pattern cards — staggered fade-up from 40px
     ================================================================ */
  var cards = document.querySelectorAll(".pattern-card");
  if (cards.length) {
    gsap.set(cards, { autoAlpha: 1 });
    gsap.from(cards, {
      y: 40,
      autoAlpha: 0,
      duration: 0.6,
      stagger: 0.08,
      delay: 0.3,
      ease: "power3.out",
    });
  }

  /* ================================================================
     About CTA dark panel — fade up on scroll
     ================================================================ */
  var aboutCta = document.getElementById("about-cta");
  if (aboutCta) {
    gsap.set(aboutCta, { autoAlpha: 1 });
    gsap.from(aboutCta, {
      y: 36,
      autoAlpha: 0,
      duration: 0.6,
      ease: "power3.out",
      scrollTrigger: {
        trigger: aboutCta,
        start: "top 85%",
        once: true,
      },
    });
  }

  /* ================================================================
     Footer — fade up on scroll
     ================================================================ */
  var footer = document.getElementById("footer");
  if (footer) {
    gsap.set(footer, { autoAlpha: 1 });
    gsap.from(footer, {
      y: 30,
      autoAlpha: 0,
      duration: 0.6,
      ease: "power3.out",
      scrollTrigger: {
        trigger: footer,
        start: "top 90%",
        once: true,
      },
    });
  }

  /* ================================================================
     Mobile hamburger menu toggle
     ================================================================ */
  var hamburger = document.getElementById("hamburger");
  var mobileMenu = document.getElementById("mobile-menu");
  if (hamburger && mobileMenu) {
    hamburger.addEventListener("click", function () {
      var isOpen = mobileMenu.classList.contains("open");
      if (isOpen) {
        mobileMenu.classList.remove("open");
      } else {
        mobileMenu.classList.add("open");
      }
    });
  }

  /* ================================================================
     Reduced-motion support
     ================================================================ */
  mm.add("(prefers-reduced-motion: reduce)", function () {
    gsap.globalTimeline.timeScale(0);
    return function () {
      gsap.globalTimeline.timeScale(1);
    };
  });

  /* ================================================================
     Refresh ScrollTrigger after all animations are set up
     ================================================================ */
  ScrollTrigger.refresh();
});
