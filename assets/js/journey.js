(() => {
  const arrows = document.querySelector(".journey-arrows");
  if (!arrows) return;

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (prefersReducedMotion) {
    arrows.classList.add("is-visible");
    return;
  }

  document.documentElement.classList.add("journey-enhanced");

  const checkVisibility = () => {
    const doc = document.documentElement;
    const maxScroll = Math.max(doc.scrollHeight - window.innerHeight, 1);
    const progress = window.scrollY / maxScroll;
    arrows.classList.toggle("is-visible", progress >= 0.15);
  };

  checkVisibility();
  window.addEventListener("scroll", checkVisibility, { passive: true });
  window.addEventListener("resize", checkVisibility);
})();

(() => {
  const section = document.querySelector("#what-i-do.about-cards");
  if (!section) return;

  const track = section.querySelector(".about-card-grid");
  const bg = section.querySelector(".about-section-bg");
  if (!track || !bg) return;

  const mobileQuery = window.matchMedia("(max-width: 760px)");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  let rafId = 0;

  const setBackgroundFromScroll = () => {
    rafId = 0;
    if (!mobileQuery.matches || reducedMotion.matches) {
      section.style.setProperty("--what-i-do-bg-x", "50%");
      return;
    }
    const max = Math.max(track.scrollWidth - track.clientWidth, 1);
    const progress = Math.min(Math.max(track.scrollLeft / max, 0), 1);
    const x = 38 + progress * 24;
    section.style.setProperty("--what-i-do-bg-x", `${x}%`);
  };

  const onScroll = () => {
    if (rafId) return;
    rafId = window.requestAnimationFrame(setBackgroundFromScroll);
  };

  setBackgroundFromScroll();
  track.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", setBackgroundFromScroll);
  if (mobileQuery.addEventListener) {
    mobileQuery.addEventListener("change", setBackgroundFromScroll);
    reducedMotion.addEventListener("change", setBackgroundFromScroll);
  }
})();

(() => {
  const openButtons = document.querySelectorAll("[data-project-open]");
  const closeButtons = document.querySelectorAll("[data-project-close]");
  if (!openButtons.length && !closeButtons.length) return;

  const overlays = Array.from(document.querySelectorAll(".project-mobile-overlay"));

  const anyOpen = () => overlays.some((el) => !el.hasAttribute("hidden"));
  const getOpenOverlay = () => overlays.find((el) => !el.hasAttribute("hidden")) || null;
  const syncOverlayClass = () => {
    document.documentElement.classList.toggle("project-overlay-open", anyOpen());
  };

  const openOverlay = (id, trigger, startIndex) => {
    const target = document.getElementById(id);
    if (!target) return;
    target.removeAttribute("hidden");
    if (trigger) trigger.setAttribute("aria-expanded", "true");
    const track = target.querySelector(".project-gallery-mobile-track");
    if (track) {
      const index = Number.isFinite(startIndex) ? startIndex : 0;
      const targetItem = track.querySelector(`[data-project-item-index="${index}"]`) || track.firstElementChild;
      if (targetItem) {
        targetItem.scrollIntoView({ behavior: "auto", inline: "start", block: "nearest" });
      }
    }
    syncOverlayClass();
  };

  const closeOverlay = (id) => {
    const target = document.getElementById(id);
    if (!target) return;
    target.setAttribute("hidden", "");
    const triggers = document.querySelectorAll(`[data-project-open="${id}"]`);
    triggers.forEach((el) => el.setAttribute("aria-expanded", "false"));
    syncOverlayClass();
  };

  openButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-project-open");
      if (!id) return;
      const startIndex = Number.parseInt(btn.getAttribute("data-project-index") || "0", 10);
      openOverlay(id, btn, Number.isNaN(startIndex) ? 0 : startIndex);
    });
    btn.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") return;
      event.preventDefault();
      const id = btn.getAttribute("data-project-open");
      if (!id) return;
      const startIndex = Number.parseInt(btn.getAttribute("data-project-index") || "0", 10);
      openOverlay(id, btn, Number.isNaN(startIndex) ? 0 : startIndex);
    });
  });

  closeButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-project-close");
      if (!id) return;
      closeOverlay(id);
    });
  });

  overlays.forEach((overlay) => {
    overlay.addEventListener("click", (event) => {
      if (event.target !== overlay) return;
      closeOverlay(overlay.id);
    });
  });

  const moveOverlayIndex = (overlay, delta) => {
    if (!overlay) return;
    const track = overlay.querySelector(".project-gallery-mobile-track");
    if (!track) return;
    const items = Array.from(track.querySelectorAll("[data-project-item-index]"));
    if (!items.length) return;

    const viewportCenter = track.getBoundingClientRect().top + track.clientHeight / 2;
    let currentIndex = 0;
    let bestDistance = Number.POSITIVE_INFINITY;

    items.forEach((item, idx) => {
      const rect = item.getBoundingClientRect();
      const center = rect.top + rect.height / 2;
      const distance = Math.abs(center - viewportCenter);
      if (distance < bestDistance) {
        bestDistance = distance;
        currentIndex = idx;
      }
    });

    const nextIndex = Math.min(Math.max(currentIndex + delta, 0), items.length - 1);
    const target = items[nextIndex];
    if (!target) return;
    target.scrollIntoView({ behavior: "smooth", block: "start", inline: "nearest" });
  };

  document.addEventListener("keydown", (event) => {
    const openOverlay = getOpenOverlay();
    if (!openOverlay) return;

    if (event.key === "Escape") {
      event.preventDefault();
      closeOverlay(openOverlay.id);
      return;
    }

    if (event.key === "ArrowDown" || event.key === "ArrowRight") {
      event.preventDefault();
      moveOverlayIndex(openOverlay, 1);
      return;
    }

    if (event.key === "ArrowUp" || event.key === "ArrowLeft") {
      event.preventDefault();
      moveOverlayIndex(openOverlay, -1);
    }
  });

  syncOverlayClass();
})();
