// Render video.html frame by frame with Playwright, composite the live
// before/after recordings into their panels, and add the score.
//
//   node render.mjs stills 3 15 28 40 57 70 82 97 112 121   # PNG stills into stills/
//   node render.mjs video [--fps 30] [--workers 4] [--audio score.wav] [--out feature-map-daily.mp4]
//
// The animation is a pure renderFrame(t). The four recordings in clips/ were
// made with `control-openhands browser record` on two stacks (the commit before
// PR #18870 and its merge); window.CLIPS says where each one is cropped, where
// it goes, when it starts and where it is cut (just before Save). Each clip
// holds its last frame until its panel fades out.
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
const FPS = +opt('fps', 30), WORKERS = +opt('workers', 4), OUT = opt('out', 'feature-map-daily.mp4');
const exe = [process.env.CHROMIUM].find(p => p && existsSync(p));

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
const run = (cmd, a) => new Promise((ok, no) => spawn(cmd, a, { stdio: 'inherit' }).on('close', c => c ? no(new Error(cmd + ' ' + c)) : ok()));

if (mode === 'stills') {
  await mkdir(join(here, 'stills'), { recursive: true });
  const page = await openPage();
  for (const t of args.slice(1).filter(a => isFinite(a))) {
    const name = `film-${String(t).replace('.', '_')}s.png`;
    await writeFile(join(here, 'stills', name), await grab(page, +t)); console.log('stills/' + name);
  }
} else if (mode === 'video') {
  const page0 = await openPage();
  const [dur, clips, T] = await page0.evaluate(() => [window.DURATION, window.CLIPS, null]);
  await page0.close();
  const total = Math.round(dur * FPS), per = Math.ceil(total / WORKERS);
  const tmp = join(here, '.segments'); await rm(tmp, { recursive: true, force: true }); await mkdir(tmp);
  console.log(`${dur}s → ${total} frames, ${WORKERS} workers`);
  await Promise.all(Array.from({ length: WORKERS }, async (_, w) => {
    const a = w * per, b = Math.min(total, a + per); if (a >= b) return;
    const page = await openPage();
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', join(tmp, `seg${w}.mp4`)], { stdio: ['pipe', 'inherit', 'inherit'] });
    const done = new Promise((ok, no) => ff.on('close', c => c ? no(new Error('ffmpeg ' + c)) : ok()));
    for (let f = a; f < b; f++) {
      const png = await grab(page, f / FPS);
      if (!ff.stdin.write(png)) await new Promise(r => ff.stdin.once('drain', r));
      if ((f - a) % 300 === 0) console.log(`worker ${w}: frame ${f}/${b}`);
    }
    ff.stdin.end(); await done; await page.close();
  }));
  await writeFile(join(tmp, 'list.txt'), Array.from({ length: WORKERS }, (_, w) => `file 'seg${w}.mp4'`).join('\n'));
  const base = join(tmp, 'base.mp4');
  await run('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', join(tmp, 'list.txt'), '-c', 'copy', base]);

  // Composite: each clip cropped, scaled into its box, delayed to its start,
  // its last frame held; shown only while its scene is on screen (with a fade).
  const inputs = ['-i', base], parts = [];
  let last = '0:v';
  clips.forEach((c, i) => {
    inputs.push('-i', join(here, c.file));
    const [cx, cy, cw, ch] = c.crop, [bx, by, bw, bh] = c.box;
    const end = c.at < 90 ? 90.0 : 104.0; // the scene's fade-out start
    parts.push(`[${i + 1}:v]trim=duration=${c.cut},fps=${FPS},crop=${cw}:${ch}:${cx}:${cy},scale=${bw}:${bh}:flags=lanczos,format=yuva420p,` +
      `tpad=stop_mode=clone:stop_duration=30,setpts=PTS-STARTPTS+${c.at}/TB,` +
      `fade=t=in:st=${c.at}:d=0.4:alpha=1,fade=t=out:st=${end}:d=0.45:alpha=1[c${i}]`);
    parts.push(`[${last}][c${i}]overlay=${bx}:${by}:eof_action=pass:enable='between(t,${c.at},${end + 0.5})'[v${i}]`);
    last = `v${i}`;
  });
  const audio = opt('audio');
  const a = ['-y', '-loglevel', 'error', ...inputs];
  if (audio) a.push('-i', audio);
  a.push('-filter_complex', parts.join(';'), '-map', `[${last}]`);
  if (audio) a.push('-map', `${clips.length + 1}:a`, '-af', `volume=${opt('audio-gain', '0')}dB`, '-c:a', 'aac', '-b:a', '160k');
  a.push('-t', String(dur), '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', join(here, OUT));
  await run('ffmpeg', a);
  await rm(tmp, { recursive: true, force: true });
  console.log('wrote ' + OUT);
}
await browser.close(); server.close();
