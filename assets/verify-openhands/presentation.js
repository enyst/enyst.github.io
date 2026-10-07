/* No dependencies. Every section and recipe remains readable without this file. */
(() => {
  "use strict";

  function init() {
    const body = document.body;
    const slides = Array.from(document.querySelectorAll("#presentation .slide"));
    if (!slides.length) return;

    const presentToggle = document.getElementById("present-toggle");
    const previous = document.getElementById("prev-slide");
    const next = document.getElementById("next-slide");
    const exitButton = document.getElementById("exit-presentation");
    const counter = document.getElementById("slide-counter");
    const progress = document.getElementById("reading-progress");
    const chapterLinks = Array.from(document.querySelectorAll('.chapter-links a[href^="#"]'));
    const originalToggleText = presentToggle ? presentToggle.textContent : "Present";
    let presenting = false;
    let current = 0;
    let scrollQueued = false;
    document.getElementById("presentation")?.setAttribute("tabindex", "-1");

    function focusCurrentHeading() {
      const heading = slides[current].querySelector("h1, h2");
      if (!heading) return;
      heading.tabIndex = -1;
      heading.focus({ preventScroll: true });
    }

    function hashIndex() {
      let id;
      try { id = decodeURIComponent(window.location.hash.slice(1)); }
      catch (_) { return -1; }
      return slides.findIndex(slide => slide.id === id || slide.contains(document.getElementById(id)));
    }

    function updateProgress() {
      if (!progress) return;
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const fraction = presenting ? (current + 1) / slides.length : max > 0 ? window.scrollY / max : 1;
      progress.style.width = `${Math.min(1, Math.max(0, fraction)) * 100}%`;
    }

    function updateControls() {
      if (counter) counter.textContent = `${String(current + 1).padStart(2, "0")} / ${String(slides.length).padStart(2, "0")}`;
      if (previous) previous.disabled = current === 0;
      if (next) next.disabled = current === slides.length - 1;
      if (presentToggle) {
        presentToggle.setAttribute("aria-pressed", String(presenting));
        presentToggle.textContent = presenting ? "Reading view" : originalToggleText;
      }
      let activeId = slides[current].id;
      let lastChapterIndex = -1;
      chapterLinks.forEach(link => {
        const chapterIndex = slides.findIndex(slide => `#${slide.id}` === link.hash);
        if (chapterIndex >= 0 && chapterIndex <= current && chapterIndex > lastChapterIndex) {
          activeId = slides[chapterIndex].id;
          lastChapterIndex = chapterIndex;
        }
      });
      chapterLinks.forEach(link => {
        if (link.hash === `#${activeId}`) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      });
      updateProgress();
    }

    function setCurrent(index, { navigate = false, scroll = false } = {}) {
      current = Math.max(0, Math.min(slides.length - 1, index));
      slides.forEach((slide, i) => slide.classList.toggle("is-active", i === current));
      if (navigate && slides[current].id) {
        const hash = `#${encodeURIComponent(slides[current].id)}`;
        if (window.location.hash !== hash) history.pushState(null, "", hash);
      }
      updateControls();
      if (scroll) {
        if (presenting) window.scrollTo({ top: 0, behavior: "instant" });
        else slides[current].scrollIntoView({ behavior: "instant", block: "start" });
        if (presenting) focusCurrentHeading();
      }
    }

    function togglePresentation(force) {
      presenting = typeof force === "boolean" ? force : !presenting;
      body.classList.toggle("is-presenting", presenting);
      setCurrent(current, { navigate: true, scroll: true });
      if (!presenting && document.activeElement && document.activeElement.closest(".footer-nav")) {
        presentToggle?.focus({ preventScroll: true });
      }
    }

    presentToggle?.addEventListener("click", () => togglePresentation());
    previous?.addEventListener("click", () => setCurrent(current - 1, { navigate: true, scroll: true }));
    next?.addEventListener("click", () => setCurrent(current + 1, { navigate: true, scroll: true }));
    exitButton?.addEventListener("click", () => togglePresentation(false));

    window.addEventListener("hashchange", () => {
      const index = hashIndex();
      if (index !== -1) setCurrent(index, { scroll: true });
    });

    // Also handle a click to the current fragment, which does not emit hashchange.
    document.addEventListener("click", event => {
      const link = event.target.closest('a[href^="#"]');
      if (!link || !presenting || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      let target;
      try { target = document.getElementById(decodeURIComponent(link.hash.slice(1))); }
      catch (_) { return; }
      const index = slides.findIndex(slide => slide === target || slide.contains(target));
      if (index < 0) return;
      event.preventDefault();
      setCurrent(index, { navigate: true, scroll: true });
    });

    document.addEventListener("keydown", event => {
      if (!presenting || event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey) return;
      if (document.querySelector("dialog[open]")) return;
      if (event.key === "Escape") {
        event.preventDefault();
        togglePresentation(false);
        return;
      }
      if (event.target.closest('input, textarea, select, button, a, details, dialog, [contenteditable="true"], [role="tab"]')) return;
      const steps = { ArrowRight: 1, ArrowDown: 1, PageDown: 1, ArrowLeft: -1, ArrowUp: -1, PageUp: -1 };
      let index;
      if (event.key in steps) index = current + steps[event.key];
      else if (event.key === "Home") index = 0;
      else if (event.key === "End") index = slides.length - 1;
      else return;
      event.preventDefault();
      setCurrent(index, { navigate: true, scroll: true });
    });

    // Scroll position, rather than a forced scroll snap, drives the reading view.
    function onScroll() {
      if (scrollQueued) return;
      scrollQueued = true;
      requestAnimationFrame(() => {
        scrollQueued = false;
        if (!presenting) {
          const readingLine = Math.min(window.innerHeight * .35, 240);
          let index = 0;
          slides.forEach((slide, i) => { if (slide.getBoundingClientRect().top <= readingLine) index = i; });
          if (index !== current) setCurrent(index);
        }
        updateProgress();
      });
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(onScroll, { rootMargin: "-15% 0px -60% 0px", threshold: 0 });
      slides.forEach(slide => observer.observe(slide));
    }

    document.querySelectorAll(".proof-steps").forEach(tablist => {
      const entries = Array.from(tablist.querySelectorAll("button[data-panel]")).map((button, index) => {
        const panel = document.getElementById(button.dataset.panel.replace(/^#/, ""));
        if (!panel) return null;
        if (!button.id) button.id = `${panel.id}-tab-${index + 1}`;
        button.setAttribute("role", "tab");
        button.setAttribute("aria-controls", panel.id);
        panel.setAttribute("role", "tabpanel");
        panel.setAttribute("aria-labelledby", button.id);
        panel.tabIndex = 0;
        return { button, panel };
      }).filter(Boolean);
      if (!entries.length) return;
      tablist.setAttribute("role", "tablist");
      if (!tablist.hasAttribute("aria-label")) tablist.setAttribute("aria-label", "Verification recipe steps");

      function select(index, focus = false) {
        entries.forEach(({ button, panel }, i) => {
          const active = i === index;
          button.setAttribute("aria-selected", String(active));
          button.tabIndex = active ? 0 : -1;
          panel.hidden = !active;
        });
        if (focus) entries[index].button.focus();
      }
      entries.forEach(({ button }, index) => {
        button.addEventListener("click", () => select(index));
        button.addEventListener("keydown", event => {
          let target;
          if (event.key === "ArrowRight") target = (index + 1) % entries.length;
          else if (event.key === "ArrowLeft") target = (index - 1 + entries.length) % entries.length;
          else if (event.key === "Home") target = 0;
          else if (event.key === "End") target = entries.length - 1;
          else return;
          event.preventDefault();
          select(target, true);
        });
      });
      select(0);
    });

    document.querySelectorAll(".copy-code").forEach(button => {
      const code = button.closest(".code-window")?.querySelector("pre code, pre");
      if (!code) { button.hidden = true; return; }
      const original = button.textContent;
      let reset;
      button.addEventListener("click", async () => {
        let copied = false;
        try {
          if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(code.textContent);
            copied = true;
          } else {
            const field = document.createElement("textarea");
            field.value = code.textContent;
            field.style.position = "fixed";
            field.style.opacity = "0";
            field.setAttribute("aria-hidden", "true");
            document.body.appendChild(field);
            field.select();
            copied = document.execCommand("copy");
            field.remove();
            button.focus({ preventScroll: true });
          }
        } catch (_) { copied = false; }
        button.textContent = copied ? "Copied ✓" : "Select to copy";
        button.setAttribute("aria-label", copied ? "Code copied to clipboard" : "Copy unavailable. Select the code to copy it.");
        clearTimeout(reset);
        reset = setTimeout(() => { button.textContent = original; button.removeAttribute("aria-label"); }, 2600);
      });
    });

    const toastImage = document.getElementById("toast-image");
    const toastCaption = document.getElementById("toast-caption");
    document.querySelectorAll(".comparison-controls").forEach(group => {
      const buttons = Array.from(group.querySelectorAll("button[data-image]"));
      if (!toastImage || !buttons.length) return;
      buttons.forEach((button, index) => {
        button.setAttribute("aria-pressed", String(index === 0));
        button.addEventListener("click", () => {
          toastImage.src = button.dataset.image;
          toastImage.alt = button.dataset.alt || button.dataset.caption || toastImage.alt;
          if (toastCaption && button.dataset.caption) toastCaption.textContent = button.dataset.caption;
          buttons.forEach(item => item.setAttribute("aria-pressed", String(item === button)));
        });
      });
    });

    const imageDialog = document.getElementById("image-dialog");
    const expandedImage = document.getElementById("expanded-image");
    const expandedCaption = document.getElementById("expanded-caption");
    const closeImage = document.getElementById("close-image");
    if (imageDialog && expandedImage && typeof imageDialog.showModal === "function") {
      document.querySelectorAll("button.image-zoom").forEach(button => {
        button.addEventListener("click", () => {
          const original = button.querySelector("img");
          if (!original) return;
          expandedImage.src = original.currentSrc || original.src;
          expandedImage.alt = original.alt;
          if (expandedCaption) expandedCaption.textContent = button.closest("figure")?.querySelector("figcaption")?.textContent.trim() || original.alt;
          imageDialog.showModal();
          closeImage?.focus();
        });
      });
      closeImage?.addEventListener("click", () => imageDialog.close());
      imageDialog.addEventListener("click", event => {
        if (event.target !== imageDialog) return;
        const box = imageDialog.getBoundingClientRect();
        if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) imageDialog.close();
      });
    } else {
      document.querySelectorAll("button.image-zoom").forEach(button => {
        button.addEventListener("click", () => {
          const img = button.querySelector("img");
          if (img) window.open(img.currentSrc || img.src, "_blank", "noopener");
        });
      });
    }

    // Closed details and alternate recipe panels must still be present on paper.
    let closedDetails = [];
    window.addEventListener("beforeprint", () => {
      closedDetails = Array.from(document.querySelectorAll(".map-groups details:not([open])"));
      closedDetails.forEach(details => { details.open = true; });
    });
    window.addEventListener("afterprint", () => {
      closedDetails.forEach(details => { details.open = false; });
      closedDetails = [];
    });

    body.classList.add("js");
    const initial = hashIndex();
    setCurrent(initial >= 0 ? initial : 0);
    onScroll();
    window.addEventListener("load", onScroll, { once: true });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init, { once: true });
  else init();
})();
