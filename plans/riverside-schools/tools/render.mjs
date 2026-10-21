// 카드 HTML의 <section class="card" id="..."> 하나마다 PNG 한 장으로 렌더한다.
// 사용: node tools/render.mjs tools/batch01.html content/batch01/cards
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || "playwright");
import path from "node:path";
import fs from "node:fs";

const [, , htmlArg, outArg] = process.argv;
if (!htmlArg || !outArg) {
  console.error("usage: node render.mjs <cards.html> <out-dir>");
  process.exit(1);
}
const htmlPath = path.resolve(htmlArg);
const outDir = path.resolve(outArg);
fs.mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const page = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1 });
await page.goto("file://" + htmlPath);
await page.evaluate(() => document.fonts.ready);

const ids = await page.$$eval("section.card", (els) => els.map((e) => e.id));
for (const id of ids) {
  const file = path.join(outDir, `${id}.png`);
  await page.locator(`#${id}`).screenshot({ path: file });
  console.log("wrote", path.relative(process.cwd(), file));
}
await browser.close();
