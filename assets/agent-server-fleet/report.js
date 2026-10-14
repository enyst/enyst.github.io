(() => {
  const form = document.querySelector('#filters');
  const query = document.querySelector('#query');
  const category = document.querySelector('#category');
  const status = document.querySelector('#status');
  const rows = [...document.querySelectorAll('.pr')];
  const topics = [...document.querySelectorAll('.topic')];
  const count = document.querySelector('#count');
  const params = new URLSearchParams(location.search);
  query.value = params.get('q') || '';
  if ([...category.options].some(option => option.value === params.get('topic'))) {
    category.value = params.get('topic');
  }
  if ([...status.options].some(option => option.value === params.get('status'))) {
    status.value = params.get('status');
  }
  function filter() {
    const words = query.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let shown = 0;
    for (const row of rows) {
      row.hidden = !words.every(word => row.dataset.search.includes(word)) ||
        Boolean(category.value && row.dataset.category !== category.value) ||
        Boolean(status.value && row.dataset.status !== status.value);
      if (!row.hidden) shown++;
    }
    for (const topic of topics) topic.hidden = ![...topic.querySelectorAll('.pr')].some(row => !row.hidden);
    count.textContent = `Showing ${shown} of ${rows.length} fix PRs.`;
    document.querySelector('#empty').hidden = shown !== 0;
    const url = new URL(location.href);
    if (query.value.trim()) url.searchParams.set('q', query.value.trim());
    else url.searchParams.delete('q');
    if (category.value) url.searchParams.set('topic', category.value);
    else url.searchParams.delete('topic');
    if (status.value) url.searchParams.set('status', status.value);
    else url.searchParams.delete('status');
    history.replaceState(null, '', url);
  }
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('input', filter);
  form.addEventListener('change', filter);
  form.addEventListener('reset', () => { query.value = ''; category.value = ''; status.value = ''; filter(); });
  document.querySelector('.controls').hidden = false;
  filter();
})();
