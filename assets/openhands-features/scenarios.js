/* Progressive enhancement: all scripts and source are already in the HTML. */
(() => {
  'use strict';
  const search = document.getElementById('scenario-search');
  const familyFilter = document.getElementById('family-filter');
  const stateFilter = document.getElementById('state-filter');
  const status = document.getElementById('result-count');
  const activeFamily = document.body.dataset.viewFamily;
  if (activeFamily) familyFilter.value = activeFamily;
  const families = [...document.querySelectorAll('.family')].map(element => ({
    element,
    scripts: [...element.querySelectorAll('.scenario')].map(node => ({
      node, search: node.dataset.search.toLocaleLowerCase(), states: node.dataset.states.split(' '),
    })),
    notes: element.querySelector('.family-notes'),
  }));
  const total = families.reduce((sum, f) => sum + f.scripts.length, 0);

  function applyFilters() {
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    let visibleFamilies = 0;
    let noteMatches = 0;
    for (const family of families) {
      const inFamily = familyFilter.value === 'all' || familyFilter.value === family.element.dataset.family;
      let familyCount = 0;
      for (const script of family.scripts) {
        const matches = inFamily && terms.every(term => script.search.includes(term)) &&
          (stateFilter.value === 'all' || script.states.includes(stateFilter.value));
        script.node.hidden = !matches;
        if (matches) familyCount += 1;
      }
      const notesText = family.notes.dataset.search.toLocaleLowerCase();
      const matchesNotes = inFamily && terms.length > 0 && terms.every(term => notesText.includes(term)) &&
        (stateFilter.value === 'all' || family.notes.dataset.states.split(' ').includes(stateFilter.value));
      // Unscoped known-issue notes still appear when a bug search matches them.
      family.element.hidden = !(familyCount || matchesNotes);
      family.notes.hidden = !(familyCount || matchesNotes);
      if (matchesNotes) { family.notes.open = true; noteMatches += 1; }
      if (familyCount || matchesNotes) visibleFamilies += 1;
      visible += familyCount;
    }
    status.textContent = `${visible} of ${total} scripts & contracts · ${visibleFamilies} ${visibleFamilies === 1 ? 'family' : 'families'}` +
      (noteMatches ? ` · matching family notes in ${noteMatches}` : '');
    document.getElementById('empty-results').hidden = visible > 0 || noteMatches > 0;
  }

  function reset() {
    search.value = '';
    familyFilter.value = activeFamily || 'all';
    stateFilter.value = 'all';
    applyFilters();
  }

  function revealHash() {
    if (!location.hash) return;
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    const family = target.closest('.family');
    const ownScenario = target.closest('.scenario');
    const filtersExcludeTarget = family?.hidden || ownScenario?.hidden ||
      (family && (search.value || stateFilter.value !== 'all' ||
        (familyFilter.value !== 'all' && familyFilter.value !== family.dataset.family)));
    if (filtersExcludeTarget || target.classList.contains('feature-anchor')) reset();
    // A stable behavior ID points at the first scenario that exercises it.
    const scenario = target.classList.contains('feature-anchor') ? target.nextElementSibling : target.closest('.scenario');
    let next = scenario;
    while (next?.classList.contains('feature-anchor')) next = next.nextElementSibling;
    if (next?.classList.contains('scenario')) next.open = true;
    for (let parent = target; parent; parent = parent.parentElement) {
      if (parent.tagName === 'DETAILS') parent.open = true;
    }
    target.scrollIntoView({block: 'start', behavior: 'instant'});
  }

  search.addEventListener('input', applyFilters);
  familyFilter.addEventListener('change', () => {
    if (activeFamily && familyFilter.value !== activeFamily) {
      location.href = familyFilter.value === 'all' ? 'scenarios.html' : `scenarios-${familyFilter.value}.html`;
      return;
    }
    applyFilters();
  });
  stateFilter.addEventListener('change', applyFilters);
  document.getElementById('reset-filters').addEventListener('click', reset);
  document.querySelector('.tools').hidden = false;
  const browse = document.querySelector('.family-nav details');
  const phone = matchMedia('(max-width: 700px)');
  function navigationSize() { browse.open = !phone.matches; }
  navigationSize();
  phone.addEventListener('change', navigationSize);
  applyFilters();
  if (!location.hash && activeFamily) document.querySelector('.scenario').open = true;
  revealHash();
  addEventListener('hashchange', revealHash);
})();
