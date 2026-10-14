/* The HTML contains the complete inventory; JS adds local filtering only. */
(() => {
  const form = document.getElementById('inventory-filter');
  const list = document.getElementById('inventory-list');
  if (!form || !list) return;
  const search = document.getElementById('inventory-search');
  const group = document.getElementById('inventory-group');
  const author = document.getElementById('inventory-author');
  const result = document.getElementById('inventory-result');
  const empty = document.getElementById('inventory-empty');
  const rows = [...list.querySelectorAll('[data-search]')];
  const sections = [...list.querySelectorAll('[data-inventory-section]')];
  const update = () => {
    const query = search.value.trim().toLocaleLowerCase();
    let shown = 0;
    rows.forEach((row) => {
      const inGroup = group.value === 'all' || row.dataset.group === group.value || (group.value === 'open' && row.dataset.group !== 'closed') || (group.value === 'no-active-own' && row.dataset.group !== 'closed' && row.dataset.ownOpen === '0');
      const byAuthor = author.value === 'all' || row.dataset.author === author.value;
      row.hidden = !(inGroup && byAuthor && row.dataset.search.includes(query));
      if (!row.hidden) shown += 1;
    });
    sections.forEach((section) => { section.hidden = ![...section.querySelectorAll('[data-search]')].some((row) => !row.hidden); });
    empty.hidden = shown !== 0;
    result.textContent = `Showing ${shown} of ${rows.length} issues · ${group.selectedOptions[0].textContent}.`;
  };
  const revealHash = () => {
    let fragment;
    try { fragment = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const element = document.getElementById(fragment);
    if (!element || !list.contains(element)) return;
    const wantedGroup = element.dataset.group || element.id;
    if (![...group.options].some((option) => option.value === wantedGroup)) return;
    group.value = wantedGroup;
    search.value = '';
    author.value = 'all';
    update();
    requestAnimationFrame(() => element.scrollIntoView());
  };
  form.hidden = false;
  result.hidden = false;
  form.addEventListener('submit', (event) => event.preventDefault());
  form.addEventListener('input', update);
  form.addEventListener('change', update);
  form.addEventListener('reset', () => requestAnimationFrame(update));
  document.querySelectorAll('[data-show-group]').forEach((link) => {
    link.addEventListener('click', () => {
      group.value = link.dataset.showGroup;
      search.value = '';
      author.value = 'all';
      update();
      requestAnimationFrame(() => document.getElementById(link.dataset.showGroup)?.scrollIntoView());
    });
  });
  window.addEventListener('hashchange', revealHash);
  update();
  revealHash();
})();
