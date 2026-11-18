const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  for (const f of fs.readdirSync('.').filter(f => f.startsWith('slide-') && f.endsWith('.html'))) {
    await pg.goto('file://' + path.resolve(f)); await pg.screenshot({ path: f.replace('.html', '.png') });
  }
  await b.close();
})();
