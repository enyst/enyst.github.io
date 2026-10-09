(() => {
  "use strict";
  const input = document.querySelector("#issue-search");
  const select = document.querySelector("#status-filter");
  const cohort = document.querySelector("#run-filter");
  const clear = document.querySelector("#clear-filters");
  const rows = [...document.querySelectorAll(".issue-row")];
  if (!input || !select || !rows.length) return;
  document.querySelectorAll("video[data-preview-time]").forEach(video => {
    const preview = () => {
      if (video.paused && video.currentTime === 0 && video.duration > 0) {
        video.currentTime = Math.min(Number(video.dataset.previewTime), video.duration / 2);
      }
    };
    if (video.readyState >= 1) preview();
    else video.addEventListener("loadedmetadata", preview, { once: true });
  });
  const output = document.querySelector("#result-count");
  const empty = document.querySelector("#no-results");
  const normalize = value => value.toLocaleLowerCase().normalize("NFKD").replace(/[\u0300-\u036f]/g, "");
  const index = rows.map(row => ({ row, text: normalize(row.dataset.search || row.textContent), states: row.dataset.states.split(" ") }));
  function filter() {
    const words = normalize(input.value.trim()).split(/\s+/).filter(Boolean);
    const state = select.value;
    let visible = 0;
    index.forEach(({row, text, states}) => {
      row.hidden = !words.every(word => text.includes(word)) || (state !== "all" && !states.includes(state)) || (cohort.value !== "all" && row.dataset.cohort !== cohort.value);
      const detail = document.getElementById(row.id.replace("issue-", "detail-"));
      if (detail) detail.hidden = row.hidden;
      if (!row.hidden) visible++;
    });
    document.querySelectorAll(".theme-group, .repo-section").forEach(group => {
      const count = group.querySelectorAll(".issue-row:not([hidden])").length;
      group.hidden = count === 0;
      const label = group.querySelector(":scope > header .count");
      if (label) label.textContent = `${count} ${count === 1 ? "issue" : "issues"}`;
    });
    document.querySelectorAll(".detail-theme, .detail-repo").forEach(group => {
      const count = group.querySelectorAll(".issue-detail:not([hidden])").length;
      group.hidden = count === 0;
      const label = group.querySelector(":scope > header .count");
      if (label) label.textContent = `${count} ${count === 1 ? "issue" : "issues"}`;
    });
    document.querySelectorAll(".repo-nav a[data-repo]").forEach(link => {
      const section = document.getElementById(link.dataset.repo);
      const count = section.querySelectorAll(".issue-row:not([hidden])").length;
      link.parentElement.hidden = count === 0;
      link.querySelector(".count").textContent = count;
    });
    output.textContent = `Showing ${visible} of ${rows.length} issues`;
    empty.hidden = visible !== 0;
    clear.disabled = !input.value && state === "all" && cohort.value === "all";
  }
  input.addEventListener("input", filter);
  select.addEventListener("change", filter);
  cohort.addEventListener("change", filter);
  clear.addEventListener("click", () => { input.value = ""; select.value = "all"; cohort.value = "all"; filter(); input.focus(); });
  let beforePrint = null;
  window.addEventListener("beforeprint", () => {
    beforePrint = { query: input.value, status: select.value, cohort: cohort.value };
    input.value = "";
    select.value = "all";
    cohort.value = "all";
    filter();
  });
  window.addEventListener("afterprint", () => {
    if (!beforePrint) return;
    input.value = beforePrint.query;
    select.value = beforePrint.status;
    cohort.value = beforePrint.cohort;
    beforePrint = null;
    filter();
  });
  document.body.classList.add("js");
  const requestedRun = new URLSearchParams(location.search).get("run");
  if ([...cohort.options].some(option => option.value === requestedRun)) cohort.value = requestedRun;
  filter();
})();
