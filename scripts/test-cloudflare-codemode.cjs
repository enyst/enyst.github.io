// Run against a local preview or the published page. Requires Playwright + Chrome.
// PLAYWRIGHT_MODULE=/path/to/playwright node scripts/test-cloudflare-codemode.cjs <url>
// Set SCREENSHOT_DIR to an existing directory to also capture desktop/mobile views.
const assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(process.argv[2] || 'http://127.0.0.1:8138/arch/cloudflare-codemode.html');
 assert.equal(await page.locator('.question').count(),5);
 assert.deepEqual(await page.locator('main > section').evaluateAll(ns=>ns.map(n=>n.id)),['background','intuition','code','quiz','codeact']);
 for(let i=0;i<5;i++)for(let j=0;j<3;j++){
  await page.locator(`.question[data-question="${i}"] .answer`).nth(j).click();
  assert.equal(await page.locator(`#feedback-${i} li`).count(),3);
 }
 await page.locator('#reset-quiz').click();
 assert.equal(await page.locator('.answer[aria-pressed="true"]').count(),0);
 for(const [i,j] of [1,2,0,2,0].entries())await page.locator(`.question[data-question="${i}"] .answer`).nth(j).click();
 assert.match(await page.locator('#quiz-score').innerText(),/5 \/ 5 answered · 5 correct/);
 await page.locator('#program-mode').click();assert.match(await page.locator('#composition-metric').innerText(),/1 code action/);
 await page.locator('#start-replay').click();assert.match(await page.locator('#replay-metric').innerText(),/writes: 0/);
 await page.locator('#approve-replay').click();assert.match(await page.locator('#replay-metric').innerText(),/writes: 1/);
 assert.equal(await page.locator('#approve-replay').isDisabled(),true);
 await page.locator('#reset-replay').click();assert.equal(await page.locator('#approve-replay').isDisabled(),true);
 const missing=await page.locator('a[href^="#"]').evaluateAll(as=>as.filter(a=>!document.getElementById(a.hash.slice(1))).map(a=>a.hash));assert.deepEqual(missing,[]);
 for(const width of [1440,834,390,320]){
  await page.setViewportSize({width,height:1000});await page.evaluate(()=>scrollTo(0,0));
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,`page overflow at ${width}`);
  const bad=await page.locator('button').evaluateAll(bs=>bs.filter(b=>b.getBoundingClientRect().width<20).map(b=>b.id));assert.deepEqual(bad,[]);
  if(process.env.SCREENSHOT_DIR && (width===1440||width===390))await page.screenshot({path:`${process.env.SCREENSHOT_DIR}/codemode-${width}.png`,fullPage:true});
 }
 // External scripts/fonts would defeat the self-contained lesson requirement.
 assert.equal(await page.locator('script[src],link[rel="stylesheet"]').count(),0);
 assert.deepEqual(errors,[]);
 console.log('PASS: all 15 quiz choices with feedback, score/reset, both traces, anchors, no external assets, 4 viewport widths, no browser errors.');
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
