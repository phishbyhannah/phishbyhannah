(() => {
  const toggles = document.querySelectorAll(".works-toggle");
  if (!toggles.length) return;

  toggles.forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const panelId = toggle.getAttribute("aria-controls");
      const panel = panelId ? document.getElementById(panelId) : null;
      const card = toggle.closest(".works-card");
      if (!panel || !card) return;

      const isOpen = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!isOpen));
      toggle.textContent = isOpen ? "View details" : "Hide details";
      card.classList.toggle("is-open", !isOpen);

      if (isOpen) {
        panel.hidden = true;
      } else {
        panel.hidden = false;
      }
    });
  });
})();
