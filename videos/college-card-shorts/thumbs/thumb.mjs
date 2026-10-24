// node thumbs/thumb.mjs -> college_a/thumbnail.jpg, college_b/thumbnail.jpg (1080x1920)
import { createRequire } from "node:module";
import { execSync } from "node:child_process";
const { chromium } = createRequire(execSync("npm root -g").toString().trim() + "/")("playwright");
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const css = readFileSync(join(ROOT, "style.css"), "utf8");
const extra = `
.t-card { position:absolute; left:72px; right:72px; top:1060px; background:var(--deep); border-radius:40px; padding:36px 50px; color:var(--cream); }
.t-row { display:flex; justify-content:space-between; align-items:baseline; font:800 44px var(--body); padding:14px 0; }
.t-row + .t-row { border-top:2px solid rgba(243,240,232,.15); }
.t-row b { font:400 96px/1 var(--display); color:var(--mustard); }
.t-row b small { font-size:48px; color:var(--cream); }
.t-foot { position:absolute; left:72px; bottom:150px; display:flex; align-items:center; gap:14px; font:800 40px var(--body); color:var(--cream); }
.t-foot i { width:22px; height:22px; background:var(--red); border-radius:3px; }
`;
const T = {
  a: `<div class="pill" style="top:220px">몬트리올 사립컬리지</div>
<div class="h1 cover on-dark" style="top:340px">
  <span class="ln s2"><span class="m">캐나다 자녀무상교육</span></span>
  <span class="ln xl2" style="font-size:200px"><span class="m mus">압도적으로</span></span>
  <span class="ln xl2" style="font-size:200px"><span class="m mus">저렴하게</span></span>
</div>
<div class="t-card"><div class="t-row">부모 학비 1년<b><small>약 </small>1,000<small>만원대</small></b></div><div class="t-row">아이 공립학교 학비<b>0<small>원</small></b></div></div>`,
  b: `<div class="pill" style="top:220px">몬트리올 사립컬리지</div>
<div class="h1 cover on-dark" style="top:340px">
  <span class="ln xl2" style="font-size:190px"><span class="m">아이 둘</span></span>
  <span class="ln xl2" style="font-size:190px"><span class="m mus">학원비로,</span></span>
  <span class="ln s2"><span class="m">캐나다 자녀무상교육?</span></span>
</div>
<div class="t-card"><div class="t-row">한국 학원비 (2명·월)<b><small>약 </small>121<small>만원</small></b></div><div class="t-row">몬트리올 부모 학비 (월)<b><small>약 </small>90<small>만원대</small></b></div></div>`,
};
const browser = await chromium.launch();
for (const k of ["a", "b"]) {
  const dir = join(ROOT, `college_${k}`);
  const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>${css}${extra}</style></head><body><div id="root"><div class="sc bg-green"><div class="deco d1"></div><div class="deco d2"></div><div class="deco d3"></div>${T[k]}<div class="t-foot"><i></i>AA Canada · 몬트리올 전문</div></div></div></body></html>`;
  writeFileSync(join(dir, "_thumb.html"), html);
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto("file://" + join(dir, "_thumb.html"));
  await page.evaluate(() => Promise.all([document.fonts.load("400 100px \"Black Han Sans\"", "가1"), document.fonts.load("800 40px Pretendard", "가1")]));
  await page.waitForTimeout(300);
  await page.screenshot({ path: join(dir, "thumbnail.jpg"), type: "jpeg", quality: 92 });
}
await browser.close();
