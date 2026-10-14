/* Progressive enhancement: every report row remains readable without JS. */
document.querySelectorAll('[data-report-filter]').forEach((form) => {
  const target = document.getElementById(form.dataset.reportFilter);
  const search = form.querySelector('input[type="search"]');
  const choice = form.querySelector('select');
  const result = document.getElementById(form.dataset.result);
  const rows = [...target.querySelectorAll('[data-search]')];
  const empty = target.querySelector('.empty-filter');
  const update = () => {
    const query = search.value.trim().toLowerCase();
    const selected = choice?.value || 'all';
    let shown = 0;
    rows.forEach((row) => {
      const matchChoice = selected === 'all' || row.dataset.group === selected;
      row.hidden = !(matchChoice && row.dataset.search.includes(query));
      if (!row.hidden) shown += 1;
    });
    result.textContent = `Showing ${shown} of ${rows.length} ${form.dataset.noun}.`;
    if (empty) empty.hidden = shown !== 0;
    target.querySelectorAll('[data-filter-subgroup]').forEach((group) => {
      group.hidden = ![...group.querySelectorAll('[data-search]')].some((row) => !row.hidden);
    });
  };
  form.hidden = false;
  result.hidden = false;
  form.addEventListener('input', update);
  form.addEventListener('change', update);
  form.addEventListener('reset', () => requestAnimationFrame(update));
  update();
});
