(() => {
  const openForm = document.getElementById('open-filters');
  const weekForm = document.getElementById('week-filters');
  const openRows = [...document.querySelectorAll('.issue-card')];
  const weekRows = [...document.querySelectorAll('.closure-row')];
  const openSearch = document.getElementById('open-search');
  const openAuthor = document.getElementById('open-author');
  const openCoverage = document.getElementById('open-coverage');
  const weekSearch = document.getElementById('week-search');
  const weekGroup = document.getElementById('week-group');
  const ownDetails = document.getElementById('own-closures');
  let ownWasOpen = false;
  let weekWasFiltered = false;

  function filterOpen() {
    const query = openSearch.value.trim().toLowerCase().replace(/#/g, '');
    let visible = 0;
    for (const row of openRows) {
      const coverage = openCoverage.value;
      const show = row.dataset.search.includes(query)
        && (openAuthor.value === 'all' || row.dataset.author === openAuthor.value)
        && (coverage === 'all' || coverage === row.dataset.coverage
          || (coverage === 'matched' && row.dataset.coverage !== 'none'));
      row.hidden = !show;
      if (show) visible++;
    }
    document.getElementById('open-result').textContent = visible
      ? `${visible} of 59 open issues shown.`
      : 'No open issues match these filters. Clear the filters to see all 59.';
  }

  function filterWeek() {
    const query = weekSearch.value.trim().toLowerCase().replace(/#/g, '');
    const filtering = Boolean(query || weekGroup.value !== 'all');
    if (filtering && !weekWasFiltered) ownWasOpen = ownDetails.open;
    if (filtering) ownDetails.open = true;
    else if (weekWasFiltered) ownDetails.open = ownWasOpen;
    weekWasFiltered = filtering;
    let visible = 0;
    for (const row of weekRows) {
      const show = row.dataset.search.includes(query)
        && (weekGroup.value === 'all' || row.dataset.group === weekGroup.value);
      row.hidden = !show;
      if (show) visible++;
    }
    for (const group of document.querySelectorAll('.week-group')) {
      group.hidden = ![...group.querySelectorAll('.closure-row')].some(row => !row.hidden);
    }
    document.getElementById('week-result').textContent = visible
      ? `${visible} of 67 closures shown. The enyst / smolpaws list can be expanded below.`
      : 'No closures match these filters. Clear the filters to see all 67.';
  }

  for (const [form, update] of [[openForm, filterOpen], [weekForm, filterWeek]]) {
    form.hidden = false;
    form.addEventListener('input', update);
    form.addEventListener('change', update);
    form.addEventListener('submit', event => event.preventDefault());
    form.addEventListener('reset', () => requestAnimationFrame(update));
  }
  document.getElementById('open-result').hidden = false;
  document.getElementById('week-result').hidden = false;
  filterOpen();
  filterWeek();
})();
