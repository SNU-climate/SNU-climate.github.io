// 테마 화면 캡처 (Playwright chromium, ~/.local/opt/shot 에 설치)
// 사용: node scripts/shot.mjs <theme> [page=index] [--full] [--ko] [--dark]
//   → site/_shots/<theme>[_<page>][_ko][_dark].png (1440×900) 와 ..._mobile.png (390×844)
//   --full 이면 페이지 전체 길이로 캡처한다(검토용).
import { createRequire } from 'module';
import { fileURLToPath, pathToFileURL } from 'url';
import path from 'path';
import fs from 'fs';
import os from 'os';

const require = createRequire(path.join(os.homedir(), '.local/opt/shot/package.json'));
const { chromium } = require('playwright');

const args = process.argv.slice(2);
const flags = new Set(args.filter(a => a.startsWith('--')));
const [theme, page = 'index'] = args.filter(a => !a.startsWith('--'));
if (!theme) { console.error('usage: node scripts/shot.mjs <theme> [page] [--full] [--ko] [--dark]'); process.exit(2); }

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', 'site');
const file = path.join(root, theme, flags.has('--ko') ? 'ko' : '', page.endsWith('.html') ? page : `${page}.html`);
if (!fs.existsSync(file)) { console.error('not found: ' + file); process.exit(1); }
const outDir = path.join(root, '_shots');
fs.mkdirSync(outDir, { recursive: true });
const base = [theme, page !== 'index' ? page.replace(/\.html$/, '').replace(/\//g, '-') : '',
  flags.has('--ko') ? 'ko' : '', flags.has('--dark') ? 'dark' : '', flags.has('--full') ? 'full' : '']
  .filter(Boolean).join('_');

const browser = await chromium.launch();
for (const [suffix, vp] of [['', { width: 1440, height: 900 }], ['_mobile', { width: 390, height: 844 }]]) {
  const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: suffix ? 2 : 1,
    colorScheme: flags.has('--dark') ? 'dark' : 'light' });
  const p = await ctx.newPage();
  await p.goto(pathToFileURL(file).href, { waitUntil: 'load', timeout: 30000 });
  await p.waitForTimeout(1200);
  const overflow = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  const out = path.join(outDir, `${base}${suffix}.png`);
  await p.screenshot({ path: out, fullPage: flags.has('--full') });
  console.log(`${out}${overflow > 1 ? `  ⚠ 가로 넘침 ${overflow}px` : ''}`);
  await ctx.close();
}
await browser.close();
