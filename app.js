const fmt = new Intl.NumberFormat('en-US');
const palette = ['#b8b8ff', '#64748b', '#ff7f0e', '#7bd85a', '#b8bec8', '#b87922', '#8fb3ff', '#ff7b93'];
const categoryColors = { community: '#b8b8ff', org: '#64748b', bot: '#ff7f0e' };
let DATA;

function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  Object.entries(attrs).forEach(([key, value]) => {
    if (key === 'class') node.className = value;
    else if (key === 'style') node.setAttribute('style', value);
    else node.setAttribute(key, value);
  });
  children.forEach((child) => node.append(child?.nodeType ? child : document.createTextNode(String(child))));
  return node;
}

function sparkline(values) {
  const ticks = '▁▂▃▄▅▆▇█';
  const max = Math.max(...values, 0);
  if (!max) return '·'.repeat(values.length);
  return values.map((value) => (value ? ticks[Math.round((value / max) * (ticks.length - 1))] : '·')).join('');
}

function makeSortableTable(table, columns, rows, defaultSort) {
  let currentRows = rows;
  let sort = { ...defaultSort };

  function getValue(row, key) {
    return typeof key === 'function' ? key(row) : row[key];
  }

  function render() {
    const sorted = [...currentRows].sort((a, b) => {
      const av = getValue(a, sort.key);
      const bv = getValue(b, sort.key);
      if (typeof av === 'number' && typeof bv === 'number') return sort.dir * (av - bv);
      return sort.dir * String(av ?? '').localeCompare(String(bv ?? ''));
    });

    const thead = el('thead');
    const headerRow = el('tr');
    columns.forEach((column) => {
      const th = el('th', { class: column.num ? 'num' : '' });
      const active = sort.key === column.key;
      const arrow = active ? (sort.dir === 1 ? '↑' : '↓') : '↕';
      const button = el('button', {}, [`${column.label} ${arrow}`]);
      button.onclick = () => {
        sort = { key: column.key, dir: active ? -sort.dir : (column.defaultDir ?? -1) };
        render();
      };
      th.append(button);
      headerRow.append(th);
    });
    thead.append(headerRow);

    const tbody = el('tbody');
    sorted.forEach((row) => {
      const tr = el('tr');
      columns.forEach((column) => {
        const raw = getValue(row, column.key);
        const content = column.render ? column.render(row, raw) : (typeof raw === 'number' ? fmt.format(raw) : raw);
        tr.append(el('td', { class: column.num ? 'num' : '' }, [content]));
      });
      tbody.append(tr);
    });
    table.replaceChildren(thead, tbody);
  }

  render();
  return {
    setRows(nextRows) {
      currentRows = nextRows;
      render();
    }
  };
}

function lineChart(target, title, months, series) {
  const width = 1360;
  const height = 430;
  const left = 58;
  const right = 24;
  const top = 38;
  const bottom = 82;
  const plotWidth = width - left - right;
  const plotHeight = height - top - bottom;
  const maxY = Math.max(1, ...series.flatMap((item) => item.values));
  const topY = Math.ceil((maxY * 1.12) / 50) * 50;
  const x = (index) => left + (index * plotWidth) / Math.max(1, months.length - 1);
  const y = (value) => top + plotHeight - (value / topY) * plotHeight;

  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
  svg.setAttribute('class', 'chart');

  const titleNode = document.createElementNS('http://www.w3.org/2000/svg', 'text');
  titleNode.setAttribute('x', left);
  titleNode.setAttribute('y', 24);
  titleNode.setAttribute('font-family', 'var(--serif)');
  titleNode.setAttribute('font-size', '22');
  titleNode.setAttribute('font-weight', '800');
  titleNode.textContent = title;
  svg.append(titleNode);

  for (let index = 0; index <= 5; index += 1) {
    const value = Math.round((topY * index) / 5);
    const yy = y(value);
    const grid = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    grid.setAttribute('x1', left);
    grid.setAttribute('x2', width - right);
    grid.setAttribute('y1', yy);
    grid.setAttribute('y2', yy);
    grid.setAttribute('stroke', '#e2d7c3');
    svg.append(grid);

    const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    label.setAttribute('x', left - 10);
    label.setAttribute('y', yy + 4);
    label.setAttribute('text-anchor', 'end');
    label.setAttribute('font-size', '11');
    label.setAttribute('fill', '#68716b');
    label.textContent = value;
    svg.append(label);
  }

  months.forEach((month, index) => {
    if (index % 2 !== 0 && index !== months.length - 1) return;
    const xx = x(index);
    const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    label.setAttribute('x', xx);
    label.setAttribute('y', height - 34);
    label.setAttribute('transform', `rotate(-45 ${xx} ${height - 34})`);
    label.setAttribute('font-size', '10');
    label.setAttribute('fill', '#68716b');
    label.textContent = month;
    svg.append(label);
  });

  series.forEach((item) => {
    const points = item.values.map((value, index) => `${x(index).toFixed(1)},${y(value).toFixed(1)}`).join(' ');
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
    line.setAttribute('points', points);
    line.setAttribute('fill', 'none');
    line.setAttribute('stroke', item.color);
    line.setAttribute('stroke-width', '3');
    line.setAttribute('stroke-linecap', 'round');
    line.setAttribute('stroke-linejoin', 'round');
    line.setAttribute('opacity', '.9');
    svg.append(line);
  });

  const legend = el('div', { class: 'legend' }, series.map((item) =>
    el('span', {}, [el('i', { class: 'swatch', style: `background:${item.color}` }), item.name])
  ));
  target.replaceChildren(svg, legend);
}

function render() {
  document.getElementById('generated').textContent = `Data generated ${DATA.generated_at}.`;
  document.getElementById('stamps').replaceChildren(
    el('span', { class: 'pill' }, ['Generated ', DATA.generated_at]),
    el('span', { class: 'pill' }, [`${DATA.methodology.target_repos.length} repositories`]),
    el('span', { class: 'pill' }, ['Self-reviews excluded']),
    el('span', { class: 'pill' }, [`${DATA.reviewer_cohort.target_reviewers.length} reviewer accounts`])
  );

  const stats = [
    ['Review events', DATA.totals.review_events],
    ['Community PR reviews', DATA.totals.community_pr_review_events],
    ['Org PR reviews', DATA.totals.org_pr_review_events],
    ['Bot PR reviews', DATA.totals.bot_pr_review_events],
    ['Unique reviewer/PRs', DATA.totals.unique_pr_reviewer_pairs]
  ];
  document.getElementById('stats').replaceChildren(...stats.map(([label, value]) =>
    el('div', { class: 'stat' }, [el('b', {}, [fmt.format(value)]), el('span', {}, [label])])
  ));

  const reviewerColumns = [
    { label: 'Reviewer', key: 'reviewer', defaultDir: 1, render: (row) => el('span', { class: 'reviewer' }, [row.reviewer]) },
    { label: 'Role', key: 'role', defaultDir: 1, render: (row) => {
      const role = row.role || 'community';
      return el('span', { class: `role ${role}` }, [role]);
    } },
    { label: 'Total reviews', key: 'total_reviews', num: true },
    { label: 'Community PR reviews', key: 'community_pr_reviews', num: true },
    { label: 'Org PR reviews', key: 'org_pr_reviews', num: true },
    { label: 'Bot PR reviews', key: 'bot_pr_reviews', num: true },
    { label: 'Unique PRs reviewed', key: 'unique_prs_reviewed', num: true },
    {
      label: 'Monthly sparkline',
      key: (row) => DATA.months.map((month) => row.by_month[month]?.total || 0).join(','),
      render: (row) => el('span', { class: 'spark' }, [sparkline(DATA.months.map((month) => row.by_month[month]?.total || 0))])
    }
  ];
  const reviewerTable = makeSortableTable(document.getElementById('reviewerTable'), reviewerColumns, DATA.reviewers, { key: 'total_reviews', dir: -1 });
  function filterReviewers() {
    const query = document.getElementById('reviewerSearch').value.toLowerCase();
    const role = document.getElementById('roleFilter').value;
    reviewerTable.setRows(DATA.reviewers.filter((row) => {
      const rowRole = row.role || 'community';
      return (!role || rowRole === role) && (row.reviewer.toLowerCase().includes(query) || rowRole.includes(query));
    }));
  }
  document.getElementById('reviewerSearch').oninput = filterReviewers;
  document.getElementById('roleFilter').onchange = filterReviewers;

  makeSortableTable(document.getElementById('repoTable'), [
    { label: 'Repository', key: 'repo', defaultDir: 1 },
    { label: 'Total', key: 'total', num: true },
    { label: 'Community', key: 'community', num: true },
    { label: 'Org', key: 'org', num: true },
    { label: 'Bot', key: 'bot', num: true }
  ], Object.entries(DATA.by_repo).map(([repo, values]) => ({ repo, ...values })), { key: 'total', dir: -1 });

  makeSortableTable(document.getElementById('monthTable'), [
    { label: 'Month', key: 'month', defaultDir: 1 },
    { label: 'Total', key: 'total', num: true },
    { label: 'Community', key: 'community', num: true },
    { label: 'Org', key: 'org', num: true },
    { label: 'Bot', key: 'bot', num: true }
  ], DATA.months.map((month) => ({ month, ...DATA.by_month[month] })), { key: 'month', dir: 1 });

  lineChart(document.getElementById('categoryChart'), 'Review events by PR author category', DATA.months, [
    { name: 'community PRs', color: categoryColors.community, values: DATA.months.map((month) => DATA.by_month[month].community) },
    { name: 'org PRs', color: categoryColors.org, values: DATA.months.map((month) => DATA.by_month[month].org) },
    { name: 'bot PRs', color: categoryColors.bot, values: DATA.months.map((month) => DATA.by_month[month].bot) }
  ]);

  const topSeries = [...DATA.reviewers]
    .sort((a, b) => b.total_reviews - a.total_reviews)
    .filter((row) => row.total_reviews > 0)
    .slice(0, 8)
    .map((row, index) => ({
      name: row.reviewer,
      color: palette[index % palette.length],
      values: DATA.months.map((month) => row.by_month[month]?.total || 0)
    }));
  lineChart(document.getElementById('topReviewerChart'), 'Top reviewers by monthly review events', DATA.months, topSeries);
}

fetch('data/review_analysis_data.json')
  .then((response) => {
    if (!response.ok) throw new Error(`HTTP error ${response.status} while loading data`);
    return response.json();
  })
  .then((data) => { DATA = data; render(); })
  .catch((error) => {
    document.body.prepend(el('pre', { style: 'white-space:pre-wrap;color:#b4483d;padding:20px' }, [`Failed to load report data: ${error.message}`]));
  });
