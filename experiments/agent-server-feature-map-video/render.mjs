// Render video.html frame by frame with Playwright and encode with ffmpeg.
//
//   node render.mjs stills 5 12.5 40        # PNG stills into stills/
//   node render.mjs video [--fps 30] [--workers 4] [--out film.mp4]
//
// Each worker renders a contiguous slice of frames in its own page and pipes
// PNGs into its own ffmpeg; the slices are joined losslessly at the end.
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { readFile, writeFile, mkdir, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const mode = args[0];
const opt = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
const FPS = +opt('fps', 30), WORKERS = +opt('workers', 4), OUT = opt('out', 'agent-server-feature-map.mp4');
const exe = [process.env.CHROMIUM].find(p => p && existsSync(p));

// Fonts load from the page's folder, so serve it over HTTP rather than file://.
const types = { '.html': 'text/html', '.woff2': 'font/woff2', '.js': 'text/javascript' };
const server = createServer(async (req, res) => {
  try { const p = join(here, decodeURIComponent(new URL(req.url, 'http://x').pathname));
    res.writeHead(200, { 'content-type': types[extname(p)] || 'application/octet-stream' }); res.end(await readFile(p)); }
  catch { res.writeHead(404); res.end(); }
}).listen(0);
const url = `http://127.0.0.1:${server.address().port}/video.html`;

const browser = await chromium.launch(exe ? { executablePath: exe } : {});
async function openPage() {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto(url); await page.evaluate(() => window.ready);
  return page;
}
const grab = (page, t) => page.evaluate(t => { window.renderFrame(t); return document.getElementById('c').toDataURL('image/png'); }, t)
  .then(d => Buffer.from(d.split(',')[1], 'base64'));

if (mode === 'stills') {
  await mkdir(join(here, 'stills'), { recursive: true });
  const page = await openPage();
  for (const t of args.slice(1).filter((a, i, l) => !a.startsWith('--') && !(l[i - 1] || '').startsWith('--') && isFinite(a))) {
    const name = opt('prefix', 'still') + '-' + String(t).replace('.', '_') + 's.png';
    await writeFile(join(here, 'stills', name), await grab(page, +t)); console.log('stills/' + name);
  }
} else if (mode === 'video') {
  const page0 = await openPage();
  const dur = await page0.evaluate(() => window.DURATION); await page0.close();
  const total = Math.round(dur * FPS), per = Math.ceil(total / WORKERS);
  const tmp = join(here, '.segments'); await rm(tmp, { recursive: true, force: true }); await mkdir(tmp);
  console.log(`${dur}s → ${total} frames, ${WORKERS} workers`);
  await Promise.all(Array.from({ length: WORKERS }, async (_, w) => {
    const a = w * per, b = Math.min(total, a + per); if (a >= b) return;
    const page = await openPage();
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p', '-tune', 'animation', join(tmp, `seg${w}.mp4`)], { stdio: ['pipe', 'inherit', 'inherit'] });
    const done = new Promise((ok, no) => ff.on('close', c => c ? no(new Error('ffmpeg ' + c)) : ok()));
    for (let f = a; f < b; f++) {
      const png = await grab(page, f / FPS);
      if (!ff.stdin.write(png)) await new Promise(r => ff.stdin.once('drain', r));
      if ((f - a) % 300 === 0) console.log(`worker ${w}: frame ${f}/${b}`);
    }
    ff.stdin.end(); await done;
  }));
  await writeFile(join(tmp, 'list.txt'), Array.from({ length: WORKERS }, (_, w) => `file 'seg${w}.mp4'`).join('\n'));
  const audio = opt('audio');
  const cat = ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', join(tmp, 'list.txt')];
  if (audio) cat.push('-i', audio, '-c:a', 'aac', '-b:a', '160k', '-shortest');
  cat.push('-c:v', 'copy', '-movflags', '+faststart', join(here, OUT));
  await new Promise((ok, no) => spawn('ffmpeg', cat, { stdio: 'inherit' }).on('close', c => c ? no(new Error('concat ' + c)) : ok()));
  await rm(tmp, { recursive: true, force: true });
  console.log('wrote ' + OUT);
}
await browser.close(); server.close();
