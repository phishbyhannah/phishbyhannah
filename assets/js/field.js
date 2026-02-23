(() => {
  const toggles = document.querySelectorAll(".field-panel-toggle");
  const launcherButtons = document.querySelectorAll(".field-launching-btn[data-open-panel]");
  if (!toggles.length && !launcherButtons.length) return;

  const prefersReducedMotion =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const setPanelState = (toggle, open) => {
    const targetId = toggle.getAttribute("aria-controls");
    const panel = targetId ? document.getElementById(targetId) : null;
    const card = toggle.closest(".field-panel-card");
    if (!panel || !card) return;

    toggle.setAttribute("aria-expanded", String(open));
    toggle.textContent = open ? "Hide details" : "View details";
    card.classList.toggle("is-open", open);
    panel.hidden = !open;
  };

  const closeOtherPanels = (activeTargetId) => {
    toggles.forEach((otherToggle) => {
      if (otherToggle.getAttribute("aria-controls") === activeTargetId) return;
      setPanelState(otherToggle, false);
    });
  };

  // Ensure clean accordion default state with only one panel open.
  const initializeAccordion = () => {
    let opened = false;
    toggles.forEach((toggle) => {
      const open = !opened && toggle.getAttribute("aria-expanded") === "true";
      if (open) opened = true;
      setPanelState(toggle, open);
    });
    if (!opened && toggles[0]) setPanelState(toggles[0], true);
  };

  toggles.forEach((toggle) => {
    toggle.addEventListener("click", () => {
      const targetId = toggle.getAttribute("aria-controls");
      const isOpen = toggle.getAttribute("aria-expanded") === "true";
      if (!isOpen) closeOtherPanels(targetId);
      setPanelState(toggle, !isOpen);
    });
  });

  launcherButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const panelId = button.getAttribute("data-open-panel");
      if (!panelId) return;

      const targetToggle = document.querySelector(`.field-panel-toggle[aria-controls="${panelId}"]`);
      const targetPanel = document.getElementById(panelId);
      const targetCard = targetPanel ? targetPanel.closest(".field-panel-card") : null;
      if (!targetToggle || !targetCard) return;

      closeOtherPanels(panelId);
      setPanelState(targetToggle, true);

      const top = targetCard.getBoundingClientRect().top + window.scrollY - 24;
      window.scrollTo({
        top,
        behavior: prefersReducedMotion ? "auto" : "smooth",
      });
    });
  });

  initializeAccordion();
})();
