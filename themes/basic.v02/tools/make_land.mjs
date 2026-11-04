// 연구 지역 지도의 바탕(육지) SVG를 만든다. 빌드 때는 쓰지 않고, 결과 파일 assets/land.svg만 쓰인다.
// 사용: node themes/basic.v02/tools/make_land.mjs   (→ themes/basic.v02/assets/land.svg)
// 투영: 등장방형(equirectangular), 중심 경도 160°E(태평양 중심), 1° = 2px → 720×360.
// 템플릿(research.html, research_topic.html)의 점 좌표식과 같아야 한다: x = 360 + 2·wrap(lon − 160), y = 180 − 2·lat
import fs from 'fs';
import path from 'path';
import vm from 'vm';
import { fileURLToPath } from 'url';

const here = path.dirname(fileURLToPath(import.meta.url));
const ctx = { window: {}, self: {} };
ctx.globalThis = ctx;
vm.createContext(ctx);
for (const f of ['d3-array.min.js', 'd3-geo.min.js', 'topojson-client.min.js', 'world-110m.js']) {
  vm.runInContext(fs.readFileSync(path.join(here, 'vendor', f), 'utf8'), ctx);
}
const d3 = ctx.d3, topojson = ctx.topojson, world = ctx.window.WORLD_LAND_110M;
const CENTER = 160;
const proj = d3.geoEquirectangular().rotate([-CENTER, 0]).scale(360 / Math.PI).translate([360, 180]).precision(0.2);
const land = topojson.feature(world, world.objects.land);
const d = d3.geoPath(proj).digits(1)(land);
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 360" width="720" height="360">
<!-- Natural Earth 1:110m land (public domain) via world-atlas@2.0.2 (ISC), projected with d3-geo (ISC). Equirectangular, center ${CENTER}°E. -->
<path fill="#8796ad" fill-opacity=".42" stroke="#8796ad" stroke-opacity=".7" stroke-width=".5" d="${d}"/>
</svg>
`;
const out = path.join(here, '..', 'assets', 'land.svg');
fs.writeFileSync(out, svg);
console.log(out, (svg.length / 1024).toFixed(1) + ' KB');
