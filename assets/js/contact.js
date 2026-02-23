(() => {
  const root = document.querySelector(".contact-page");
  if (!root) return;
  window.requestAnimationFrame(() => root.classList.add("is-ready"));
})();
