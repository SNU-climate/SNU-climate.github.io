// 모든 테마·페이지를 휴대폰 폭(360px)으로 열어 가로 넘침과 JS 오류를 검사한다.
// 사용: node scripts/check_layout.mjs [theme ...]   (기본: site/ 아래 모든 테마)
// 문제가 있으면 종료 코드 1.
import { createRequire } from 'module';
import { fileURLToPath, pathToFileURL } from 'url';
import path from 'path';
import fs from 'fs';
import os from 'os';

const require = createRequire(path.join(os.homedir(), '.local/opt/shot/package.json'));
const { chromium } = require('playwright');

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', 'site');
const themes = process.argv.slice(2).length ? process.argv.slice(2)
  : fs.readdirSync(root).filter(d => !d.startsWith('_') && fs.statSync(path.join(root, d)).isDirectory());

function pages(dir) {
  const out = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory() && !['assets', 'static'].includes(e.name)) out.push(...pages(p));
    else if (e.name.endsWith('.html')) out.push(p);
  }
  return out;
}

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 360, height: 780 } });
let problems = 0, total = 0;
for (const th of themes) {
  const list = pages(path.join(root, th));
  let bad = 0;
  for (const f of list) {
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => errs.push(String(e.message || e)));
    await p.goto(pathToFileURL(f).href, { waitUntil: 'load', timeout: 30000 });
    await p.waitForTimeout(150);
    const over = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    const rel = path.relative(path.join(root, th), f);
    if (over > 1) { console.log(`[${th}] ${rel}: 가로 넘침 ${over}px`); bad++; }
    for (const e of errs) { console.log(`[${th}] ${rel}: JS 오류 ${e}`); bad++; }
    await p.close();
    total++;
  }
  console.log(`[${th}] ${list.length} pages, 문제 ${bad}`);
  problems += bad;
}
await browser.close();
console.log(`합계: ${total} pages, 문제 ${problems}`);
process.exit(problems ? 1 : 0);
