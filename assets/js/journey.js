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
