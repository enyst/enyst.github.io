/* Progressive enhancement only: all recipes and family links are static HTML. */
(() => {
  "use strict";

  const normalize = (value) => value
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLocaleLowerCase()
    .trim();

  function setupSearch({ inputId, itemSelector, statusId, emptyId, groupSelector, noun }) {
    const input = document.getElementById(inputId);
    if (!input) return;
    const items = Array.from(document.querySelectorAll(itemSelector));
    if (!items.length) return;
    const searchBox = input.closest(".search-box");
    if (searchBox) searchBox.hidden = false;
    const status = document.getElementById(statusId);
    const empty = document.getElementById(emptyId);
    const groups = Array.from(document.querySelectorAll(groupSelector)).map((group) => {
      if (group.matches("h3.recipe-group")) {
        const recipes = [];
        for (let sibling = group.nextElementSibling; sibling; sibling = sibling.nextElementSibling) {
          if (sibling.matches("h3.recipe-group")) break;
          if (sibling.matches(itemSelector)) recipes.push(sibling);
        }
        return { heading: group, items: recipes };
      }
      return { container: group, items: Array.from(group.querySelectorAll(itemSelector)) };
    });
    const searchText = new Map(items.map((item) => [
      item, normalize(item.dataset.search || item.textContent || ""),
    ]));

    const update = () => {
      const terms = normalize(input.value).split(/\s+/).filter(Boolean);
      let shown = 0;
      for (const item of items) {
        const matches = terms.every((term) => searchText.get(item).includes(term));
        item.hidden = !matches;
        if (matches) shown += 1;
      }
      for (const group of groups) {
        const hasResults = group.items.some((item) => !item.hidden);
        if (group.container) group.container.hidden = !hasResults;
        if (group.heading) group.heading.hidden = !hasResults;
      }
      if (status) {
        status.textContent = terms.length
          ? `Showing ${shown} of ${items.length} ${noun}.`
          : `Showing all ${items.length} ${noun}.`;
      }
      if (empty) empty.hidden = shown !== 0;
    };
    input.addEventListener("input", update);
    input.addEventListener("search", update);
    update();
  }

  function fallbackCopy(text) {
    const field = document.createElement("textarea");
    field.value = text;
    field.readOnly = true;
    field.setAttribute("aria-hidden", "true");
    field.style.cssText = "position:fixed;left:-9999px;top:0;opacity:0;";
    document.body.append(field);
    field.select();
    let copied = false;
    try {
      copied = document.execCommand("copy");
    } catch (_) {
      copied = false;
    } finally {
      field.remove();
    }
    return copied;
  }

  function setupCopy() {
    const resetTimers = new WeakMap();
    for (const button of document.querySelectorAll("button.copy-command")) {
      const code = button.closest(".command-line")?.querySelector("code");
      if (!code) continue;
      button.hidden = false;
      button.type = "button";
      button.setAttribute("aria-live", "polite");
      const originalText = button.textContent;
      const originalLabel = button.getAttribute("aria-label");
      button.addEventListener("click", async () => {
        // textContent preserves the literal command: never parse or execute it.
        const command = code.textContent;
        let copied = false;
        try {
          if (navigator.clipboard?.writeText) {
            await navigator.clipboard.writeText(command);
            copied = true;
          } else {
            copied = fallbackCopy(command);
          }
        } catch (_) {
          copied = fallbackCopy(command);
        }
        clearTimeout(resetTimers.get(button));
        button.dataset.copyState = copied ? "copied" : "failed";
        button.textContent = copied ? "Copied" : "Copy unavailable";
        button.setAttribute("aria-label", copied
          ? "Command copied to clipboard"
          : "Clipboard unavailable. Select the command text to copy it.");
        button.focus({ preventScroll: true });
        resetTimers.set(button, setTimeout(() => {
          button.textContent = originalText;
          if (originalLabel === null) button.removeAttribute("aria-label");
          else button.setAttribute("aria-label", originalLabel);
          delete button.dataset.copyState;
        }, copied ? 2200 : 5000));
      });
    }
  }

  function revealHash() {
    if (!window.location.hash) return;
    let id;
    try {
      id = decodeURIComponent(window.location.hash.slice(1));
    } catch (_) {
      return;
    }
    const target = document.getElementById(id);
    if (!target) return;
    const recipe = target.closest("article.recipe");
    if (recipe?.hidden) {
      const input = document.getElementById("recipe-search");
      if (input) {
        input.value = "";
        input.dispatchEvent(new Event("input", { bubbles: true }));
      }
    }
    for (let detail = target.closest("details"); detail; detail = detail.parentElement?.closest("details")) {
      detail.open = true;
    }
    requestAnimationFrame(() => target.scrollIntoView({ block: "start", behavior: "auto" }));
  }

  function setupRecipeToc() {
    const toc = document.querySelector("details.recipe-toc");
    if (!toc) return;
    const desktop = window.matchMedia("(min-width: 761px)");
    const update = () => { toc.open = desktop.matches; };
    update();
    desktop.addEventListener("change", update);
  }

  function initialize() {
    document.documentElement.classList.add("feature-map-js");
    setupSearch({
      inputId: "family-search", itemSelector: ".family-card", statusId: "search-status",
      emptyId: "search-empty", groupSelector: "#family-list > section", noun: "families",
    });
    setupSearch({
      inputId: "recipe-search", itemSelector: "article.recipe", statusId: "recipe-search-status",
      emptyId: "recipe-search-empty", groupSelector: "#recipe-list > h3.recipe-group", noun: "recipes",
    });
    setupCopy();
    setupRecipeToc();
    revealHash();
    window.addEventListener("hashchange", revealHash);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
})();
